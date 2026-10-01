import base64
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock
from urllib.error import HTTPError
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_platform.definitions import payload, substitute, within
from analytics_platform.fabric_client import FabricClient
spec = importlib.util.spec_from_file_location("fabric_items", ROOT / "scripts/fabric_items.py")
fabric_items = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fabric_items)


class DefinitionTests(unittest.TestCase):
    def test_nested_json_substitution_preserves_quotes(self):
        self.assertEqual(substitute({"a": ["{{NAME}}"]}, {"NAME": 'hello "world"'}), {"a": ['hello "world"']})

    def test_missing_and_unresolved_bindings_fail(self):
        for bindings in ({}, {"NAME": "REPLACE_WITH_GUID"}, {"NAME": ""}):
            with self.assertRaises(ValueError):
                substitute("{{NAME}}", bindings)

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            within(ROOT, "../outside.txt")

    def test_definition_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "part.json").write_text('{"host":"{{HOST}}"}')
            body = payload(directory, {"name":"demo", "type":"Notebook", "parts":[{"path":"x.json", "source":"part.json"}]}, {"HOST":"example"})
            decoded = json.loads(base64.b64decode(body["definition"]["parts"][0]["payload"]))
            self.assertEqual(decoded, {"host":"example"})


class ClientTests(unittest.TestCase):
    def test_throttled_request_retries(self):
        response = Mock()
        response.status, response.headers = 200, {}
        response.read.return_value = b'{"value":[]}'
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        opener = Mock()
        opener.open.side_effect = [HTTPError("https://api.fabric.microsoft.com/v1/x", 429, "throttle", {"Retry-After":"0"}, None), response]
        client = FabricClient("fake", opener=opener, sleep=lambda _: None)
        self.assertEqual(client.request("GET", "x")[2], {"value":[]})
        self.assertEqual(opener.open.call_count, 2)

    def test_ambiguous_write_failure_is_not_retried(self):
        opener = Mock()
        opener.open.side_effect = HTTPError("https://api.fabric.microsoft.com/v1/x", 500, "error", {}, None)
        client = FabricClient("fake", opener=opener)
        with self.assertRaises(RuntimeError):
            client.request("POST", "x", {"name":"demo"})
        self.assertEqual(opener.open.call_count, 1)

    def test_foreign_origin_rejected(self):
        for url in ("https://example.com/v1/items", "https://api.fabric.microsoft.com.evil.test/v1/items", "https://api.fabric.microsoft.com@evil.test/v1/items"):
            with self.assertRaises(ValueError):
                FabricClient.url(url)

    def test_pagination(self):
        client = FabricClient("fake", sleep=lambda _: None)
        client.request = Mock(side_effect=[(200, {}, {"value":[{"id":"a"}], "continuationUri":"https://api.fabric.microsoft.com/v1/workspaces/w/items?page=2"}), (200, {}, {"value":[{"id":"b"}]})])
        self.assertEqual([row["id"] for row in client.items("w")], ["a", "b"])

    def test_lro_success(self):
        client = FabricClient("fake", sleep=lambda _: None)
        client.request = Mock(side_effect=[(200, {}, {"status":"Running"}), (200, {}, {"status":"Succeeded"}), (200, {}, {"id":"created"})])
        result = client.complete((202, {"Location":"https://api.fabric.microsoft.com/v1/operations/x", "Retry-After":"0"}, {}))
        self.assertEqual(result["id"], "created")

    def test_lro_failure(self):
        client = FabricClient("fake", sleep=lambda _: None)
        client.request = Mock(return_value=(200, {}, {"status":"Failed"}))
        with self.assertRaises(RuntimeError):
            client.complete((202, {"x-ms-operation-id":"x", "retry-after":"0"}, {}))

    def test_preflight_before_any_api_call(self):
        client = Mock()
        manifest = json.loads((ROOT / "fabric/manifests/serving.json").read_text())
        with self.assertRaises(ValueError):
            fabric_items.execute(manifest, {}, client, "00000000-0000-0000-0000-000000000001")
        client.items.assert_not_called()
        client.request.assert_not_called()

    def test_existing_item_is_not_modified(self):
        client = Mock()
        client.items.return_value = [{"id":"existing", "type":"Lakehouse", "displayName":"demo"}]
        result = fabric_items.execute({"items":[{"name":"demo", "type":"Lakehouse", "idBinding":"LH"}]}, {}, client, "00000000-0000-0000-0000-000000000001")
        self.assertEqual(result["LH"], "existing")
        client.request.assert_not_called()

    def test_cross_workspace_binding_rejected(self):
        with self.assertRaises(ValueError):
            fabric_items.execute({"items":[]}, {"WORKSPACE_ID":"wrong"}, Mock(), "00000000-0000-0000-0000-000000000001")


if __name__ == "__main__":
    unittest.main()
