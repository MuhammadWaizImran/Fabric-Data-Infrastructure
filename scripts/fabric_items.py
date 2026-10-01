"""List a plan offline by default. --apply explicitly creates items in ONE existing workspace.

Existing items are reused, never silently overwritten. --update-definitions allows
explicit definition updates. Connection credentials and tenant settings are not created.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import uuid
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_platform.definitions import payload
from analytics_platform.fabric_client import FabricClient


def execute(manifest, bindings, client, workspace, update=False):
    uuid.UUID(workspace)
    if "WORKSPACE_ID" in bindings and bindings["WORKSPACE_ID"] != workspace:
        raise ValueError("WORKSPACE_ID binding does not match --workspace")
    bindings = {**bindings, "WORKSPACE_ID": workspace}
    # Check every file and static binding BEFORE the first network write.
    preview = dict(bindings)
    for item in manifest["items"]:
        payload(ROOT, item, preview)
        if item.get("idBinding"):
            preview[item["idBinding"]] = str(uuid.UUID(int=1))
    existing = client.items(workspace)
    for item in manifest["items"]:
        matches = [row for row in existing if row["displayName"] == item["name"] and row["type"] == item["type"]]
        if len(matches) > 1:
            raise RuntimeError(f"Ambiguous existing item: {item['name']}")
        body = payload(ROOT, item, bindings)
        if matches:
            result = matches[0]
            if update and "definition" in body:
                client.complete(client.request("POST", f"workspaces/{workspace}/items/{result['id']}/updateDefinition", {"definition": body["definition"]}))
                print(f"Updated definition: {item['name']}")
            else:
                print(f"Reused, definition not changed: {item['name']}")
        else:
            result = client.complete(client.request("POST", f"workspaces/{workspace}/items", body))
            if not result.get("id"):
                raise RuntimeError(f"Create operation returned no item ID: {item['name']}")
            existing.append(result)
            print(f"Created: {item['name']}")
        if item.get("idBinding"):
            bindings[item["idBinding"]] = result["id"]
    return bindings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "fabric/manifests/provider.json")
    parser.add_argument("--bindings", type=Path)
    parser.add_argument("--workspace")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--update-definitions", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not args.apply:
        print("OFFLINE PLAN: no authentication, requests, or deployments.")
        for item in manifest["items"]:
            print(f"  {item['type']:18} {item['name']}")
        print("Connection-bound branches: see fabric/connections and docs/coverage.md.")
        return
    if not args.workspace or not args.bindings:
        parser.error("--apply requires --workspace and --bindings")
    bindings = json.loads(args.bindings.read_text(encoding="utf-8"))
    result = execute(manifest, bindings, FabricClient(os.environ.get("FABRIC_TOKEN")), args.workspace, args.update_definitions)
    output = ROOT / "build" / f"fabric-bindings-{args.workspace}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved non-secret ID bindings to {output}")


if __name__ == "__main__":
    main()
