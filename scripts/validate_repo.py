"""Offline structural validation; does not claim cloud integration validation."""
import ast
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_platform.definitions import payload, TOKEN, within


def main():
    excluded = {".git", ".venv", "build", "__pycache__", "artifacts", ".terraform"}
    files = [path for path in ROOT.rglob("*") if path.is_file() and not excluded.intersection(path.relative_to(ROOT).parts)]
    for path in files:
        if path.suffix in (".json", ".ipynb", ".bim", ".pbism"):
            json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix == ".jsonl":
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    json.loads(line)
        elif path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        if path.suffix == ".ipynb":
            nb = json.loads(path.read_text(encoding="utf-8"))
            for cell in nb["cells"]:
                if cell["cell_type"] == "code":
                    ast.parse("".join(cell["source"]))
                    assert cell["outputs"] == [], f"Notebook output committed: {path}"
        if path.suffix == ".md":
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#")[0]).resolve()
                assert target.exists(), f"Broken local link: {path}: {link}"
    svg = ROOT / "docs/architecture/azure-analytics-end-to-end.svg"
    labels = set("".join(node.itertext()).strip() for node in ET.parse(svg).iter("{http://www.w3.org/2000/svg}text"))
    coverage = json.loads((ROOT / "docs/coverage.json").read_text())
    assert len(labels) == coverage["uniqueLabelCount"]
    assert labels == {row["label"] for row in coverage["components"]}
    for row in coverage["components"]:
        assert row["status"] and row["artifacts"]
        for artifact in row["artifacts"]:
            assert within(ROOT, artifact).is_file(), f"Missing coverage artifact {artifact}"
    for manifest_path in (ROOT / "fabric/manifests").glob("*.json"):
        manifest = json.loads(manifest_path.read_text())
        bindings = {"WORKSPACE_ID": "00000000-0000-0000-0000-000000000001", "LAKEHOUSE_ID": "00000000-0000-0000-0000-000000000002",
                    "SQL_ENDPOINT": "example.datawarehouse.fabric.microsoft.com", "SQL_DATABASE": "00000000-0000-0000-0000-000000000003",
                    "EVENTHUB_CONNECTION_ID": "00000000-0000-0000-0000-000000000004"}
        names = set()
        for item in manifest["items"]:
            assert (item["type"], item["name"]) not in names, "Duplicate manifest item"
            names.add((item["type"], item["name"]))
            payload(ROOT, item, bindings)
            if item.get("idBinding"):
                bindings[item["idBinding"]] = "00000000-0000-0000-0000-000000000005"
    for source in json.loads((ROOT / "fabric/connections/catalog.json").read_text())["sources"]:
        assert within(ROOT, source["setup"]).is_file()
    print(f"PASS: {len(files)} files inspected, {len(labels)} diagram labels mapped, JSON/Python/notebooks/manifests/local links valid.")
    print("Cloud deployment, native report authoring, Spark/SQL/KQL execution and live integration remain untested.")


if __name__ == "__main__":
    main()
