#!/usr/bin/env python3
"""Bundle the maintained skills for the MCP server; no runtime GitHub dependency."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "branded-template-generator",
    "proposal-from-conversation",
    "google-slides-template-builder",
)


def build_bundle():
    files = {}
    for name in SKILLS:
        directory = ROOT / "skills" / name
        for path in [directory / "SKILL.md", *sorted((directory / "references").glob("*.md"))]:
            key = path.relative_to(ROOT / "skills").as_posix()
            files[key] = path.read_text(encoding="utf-8")
    for key, content in files.items():
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if ":" not in target and not target.startswith("#"):
                resolved = (ROOT / "skills" / key).parent / target.split("#")[0]
                if resolved.resolve().relative_to((ROOT / "skills").resolve()).as_posix() not in files:
                    raise ValueError(f"Unbundled reference in {key}: {target}")
    digest = hashlib.sha256(json.dumps(files, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return {
        "schemaVersion": 1,
        "source": "https://github.com/Doc-Failure/templify-agent-plugin",
        "contentSha256": digest,
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="Fail if the deployed-source bundle is stale")
    args = parser.parse_args()
    content = json.dumps(build_bundle(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != content:
            parser.exit(1, "Authoring bundle is stale; regenerate it before server release.\n")
        print("Authoring bundle matches the maintained skills.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(f"Exported authoring guides to {args.output}")


if __name__ == "__main__":
    main()
