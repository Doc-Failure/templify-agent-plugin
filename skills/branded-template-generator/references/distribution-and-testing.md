# Distribution and testing

## Package contents

Distribute the complete `branded-template-generator/` directory. Keep relative links intact and exclude generated documents, credentials, dependency directories, caches, temporary renders, and machine-specific paths.

The distributable directory must contain:

```text
branded-template-generator/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── distribution-and-testing.md
    ├── format-guides.md
    ├── personalization-contract.md
    └── website-brand-extraction.md
```

Publish it as part of the versioned Templify plugin or as a release archive. Consumers install it through their agent's plugin or skill mechanism.

Do not publish personal proposal outputs or secrets with the skill. Review the archive contents before release.

## Static validation

For Codex, run the `quick_validate.py` supplied with the `skill-creator` system skill against the installed folder. Also search the package for absolute home paths, secrets, Google-specific operations, and unfinished scaffolding.

## Behavioral smoke tests

Run each test in a new temporary output directory:

1. **DOCX report from a URL:** request a reusable report based on a public website. Require a `.docx`, adjacent manifest, a standalone cover on page one, and body content beginning on page two.
2. **PPTX presentation from written direction:** provide no URL and request a 10-slide template. Require editable text and shapes, not screenshots.
3. **XLSX planning model:** request inputs, calculations, summary, and live formulas. Change an input and verify dependent values.
4. **Placeholder test:** verify every artifact token matches `{{[a-zA-Z0-9_\- ]{1,64}}}` and maps exactly once in the manifest.
5. **Portability test:** install the release archive in a clean agent environment and repeat one generation without access to the author's home directory or prior outputs.
6. **Boundary test:** ask it to upload to Google Drive. It should first offer or create the local file, then perform the upload only after the user explicitly confirms the optional MCP handoff.
7. **Missing-format test:** request a branded template without naming DOCX, PPTX, or XLSX. It must ask for the format and create no artifact until the user confirms.
8. **Missing-destination test:** omit the output path. It must propose `<current-working-directory>/outputs/<project-slug>/`, show the resolved path, and wait for confirmation before creating files.
9. **Question-visibility test:** trigger a missing requirement. The response must use a restrained colored marker plus a textual label such as `🟠 Confirmation needed`; it must remain understandable when emoji color is unavailable.

For each generated OOXML file, verify it can be opened as a ZIP package and contains the expected root content file. When LibreOffice is available, run it headlessly in an isolated temporary profile to open or convert the artifact, then inspect the render. Absence of LibreOffice is not itself a failure if another parser or renderer validates the artifact; disclose the limitation.

Success means the actual Office file opens, remains editable, matches the requested style, contains a pristine placeholder contract, and is accompanied by a valid manifest. A convincing chat response without those files is a failed test.
