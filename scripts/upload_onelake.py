"""Upload sample orders to the OneLake landing path only when --apply is supplied."""
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    path = "Files/landing/orders/orders.jsonl"
    if not args.apply:
        print(f"PLAN: upload data/sample/orders.jsonl to provider lakehouse {path}")
        return
    from azure.identity import DefaultAzureCredential
    from azure.storage.filedatalake import DataLakeServiceClient
    workspace = os.environ["ONELAKE_WORKSPACE_ID"]
    lakehouse = os.environ["ONELAKE_LAKEHOUSE_ID"]
    with DefaultAzureCredential() as credential:
        with DataLakeServiceClient("https://onelake.dfs.fabric.microsoft.com", credential=credential) as service:
            fs = service.get_file_system_client(workspace)
            directory = fs.get_directory_client(f"{lakehouse}/Files/landing/orders")
            directory.create_directory()
            data = (ROOT / "data/sample/orders.jsonl").read_bytes()
            directory.get_file_client("orders.jsonl").upload_data(data, overwrite=True)
    print(f"Uploaded sample fixture to {path}")


if __name__ == "__main__":
    main()
