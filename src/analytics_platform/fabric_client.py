"""Minimal Fabric REST client. No implicit authentication or cloud writes."""
import json
import time
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

API = "https://api.fabric.microsoft.com/v1"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("Unexpected redirect; refusing to forward the bearer token")


class FabricClient:
    def __init__(self, token, opener=None, sleep=time.sleep):
        if not token or not token.strip():
            raise ValueError("Set FABRIC_TOKEN to a current Fabric-audience access token")
        self.token = token.strip()
        self.opener = opener or build_opener(NoRedirect())
        self.sleep = sleep

    @staticmethod
    def url(path):
        url = path if path.startswith("https://") else API + "/" + path.lstrip("/")
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != "api.fabric.microsoft.com" or not parsed.path.startswith("/v1/"):
            raise ValueError("Refusing a Fabric request outside the expected API origin")
        return url

    def request(self, method, path, body=None):
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(self.url(path), data=data, method=method,
                          headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"})
        for attempt in range(6):
            try:
                with self.opener.open(request, timeout=60) as response:
                    raw = response.read()
                    return response.status, dict(response.headers), json.loads(raw) if raw else {}
            except HTTPError as exc:
                # Do not blindly retry writes after ambiguous 5xx responses.
                if exc.code == 429 and attempt < 5:
                    self.sleep(min(float(exc.headers.get("Retry-After", "10")), 60))
                    continue
                raise RuntimeError(f"Fabric API {method} failed with HTTP {exc.code}; check service diagnostics. Response body omitted to protect connection metadata.") from None
        raise RuntimeError("Fabric retry limit reached")

    def complete(self, response):
        status, headers, body = response
        if status != 202:
            return body
        headers = {k.lower(): v for k, v in headers.items()}
        location = headers.get("location")
        if not location:
            operation_id = headers.get("x-ms-operation-id")
            if not operation_id:
                raise RuntimeError("202 response without operation location")
            location = f"{API}/operations/{operation_id}"
        self.url(location)
        deadline = time.monotonic() + 1800
        delay = min(float(headers.get("retry-after", "5")), 60)
        while time.monotonic() < deadline:
            self.sleep(delay)
            _, headers, result = self.request("GET", location)
            state = result.get("status")
            if state == "Succeeded":
                return self.request("GET", location.rstrip("/") + "/result")[2]
            if state in ("Failed", "Cancelled"):
                raise RuntimeError(f"Fabric operation {state}; inspect the operation in Fabric")
            headers = {k.lower(): v for k, v in headers.items()}
            delay = min(float(headers.get("retry-after", "5")), 60)
        raise TimeoutError("Fabric operation exceeded 30 minutes; inspect status before retrying")

    def items(self, workspace):
        path = f"workspaces/{workspace}/items"
        result = []
        seen = set()
        while path:
            url = self.url(path)
            if url in seen:
                raise RuntimeError("Repeated pagination URL")
            seen.add(url)
            _, _, page = self.request("GET", path)
            result.extend(page.get("value", []))
            path = page.get("continuationUri")
            if not path and page.get("continuationToken"):
                from urllib.parse import urlencode
                path = f"workspaces/{workspace}/items?" + urlencode({"continuationToken": page["continuationToken"]})
        return result
