"""Package tracked files only, excluding Git internals and ignored local data."""
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    names = [name for name in raw.decode("utf-8").split("\0") if name]
    if not names:
        raise RuntimeError("Initialize Git and stage the reviewed repository files first")
    output = ROOT.parent / "azure-fabric-analytics.zip"
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(names):
            path = (ROOT / name).resolve()
            if not path.is_relative_to(ROOT):
                raise ValueError("Tracked path outside repository")
            archive.write(path, "azure-fabric-analytics/" + name)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Archive integrity validation failed")
    print(f"Created {output.name}: {len(names)} files, {output.stat().st_size:,} bytes. Git internals are excluded.")


if __name__ == "__main__":
    main()
