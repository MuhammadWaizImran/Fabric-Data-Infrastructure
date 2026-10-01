import base64
import json
from pathlib import Path
import re

TOKEN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def substitute(value, bindings):
    if isinstance(value, dict):
        return {key: substitute(item, bindings) for key, item in value.items()}
    if isinstance(value, list):
        return [substitute(item, bindings) for item in value]
    if isinstance(value, str):
        def replace(match):
            key = match.group(1)
            if key not in bindings or not str(bindings[key]).strip() or str(bindings[key]).startswith("REPLACE_"):
                raise ValueError(f"Missing binding: {key}")
            return str(bindings[key])
        return TOKEN.sub(replace, value)
    return value


def within(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Definition path escapes repository")
    return path


def payload(root, item, bindings):
    body = {"displayName": item["name"], "type": item["type"], "description": item.get("description", "Repository-managed analytics item")}
    if "creationPayload" in item:
        body["creationPayload"] = substitute(item["creationPayload"], bindings)
    if "parts" in item:
        if "creationPayload" in item:
            raise ValueError("Use definition OR creationPayload")
        parts = []
        for part in item["parts"]:
            text = within(root, part["source"]).read_text(encoding="utf-8")
            if part["source"].endswith((".json", ".ipynb", ".bim", ".pbism")):
                text = json.dumps(substitute(json.loads(text), bindings))
            else:
                text = substitute(text, bindings)
            parts.append({"path": part["path"], "payloadType": "InlineBase64", "payload": base64.b64encode(text.encode()).decode()})
        body["definition"] = {"parts": parts}
        if item.get("format"):
            body["definition"]["format"] = item["format"]
    return body
