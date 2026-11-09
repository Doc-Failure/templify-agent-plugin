#!/usr/bin/env python3
"""Package a clean, committed Templify plugin with checksums for GitHub Releases."""
import argparse
import hashlib
import io
import json
import subprocess
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {"branded-template-generator", "proposal-from-conversation", "google-slides-template-builder"}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if git("status", "--porcelain").strip():
        parser.exit(1, "Commit or otherwise resolve working-tree changes before packaging.\n")
    version = json.loads(git("show", "HEAD:.codex-plugin/plugin.json"))["version"]
    claude_version = json.loads(git("show", "HEAD:.claude-plugin/plugin.json"))["version"]
    if version != claude_version:
        parser.exit(1, "Plugin manifest versions differ.\n")
    archive = git("archive", "--format=zip", "HEAD")
    with zipfile.ZipFile(io.BytesIO(archive)) as package:
        assert package.testzip() is None
        names = set(package.namelist())
        for required in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".mcp.json", "LICENSE"):
            assert required in names, f"Missing {required}"
        found = {name.split('/')[1] for name in names if name.startswith('skills/') and name.endswith('/SKILL.md')}
        assert found == SKILLS, f"Unexpected skills: {found}"
        for name in names:
            parts = Path(name).parts
            assert not name.startswith('/') and '..' not in parts
            assert not set(parts).intersection({".git", "node_modules", "outputs", "releases", "dist"}), name
            assert not any(part == '.env' or part.startswith('.env.') for part in parts), name
    outputs = {
        f"templify-{version}.zip": archive,
        f"templify-{version}.tar.gz": git("archive", "--format=tar.gz", f"--prefix=templify-{version}/", "HEAD"),
    }
    with tarfile.open(fileobj=io.BytesIO(outputs[f"templify-{version}.tar.gz"]), mode="r:gz") as package:
        assert all(member.isfile() or member.isdir() for member in package.getmembers())
    sums = ''.join(f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in outputs.items())
    outputs["SHA256SUMS.txt"] = sums.encode()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        target = args.output_dir / name
        if target.exists():
            parser.exit(1, f"Refusing to overwrite {target}\n")
    for name, data in outputs.items():
        (args.output_dir / name).write_bytes(data)
    print(f"Packaged Templify {version} from commit {git('rev-parse', 'HEAD').decode().strip()}")
    for name in outputs:
        print(args.output_dir / name)


if __name__ == "__main__":
    main()
