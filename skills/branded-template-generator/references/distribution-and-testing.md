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
    ├── docx-cover-design.md
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
6. **Boundary test:** request local-only generation and verify no Google connection, upload, or continuation offer occurs. In a separate request, explicitly authorize generation and MCP upload; verify it validates the local file and then uploads without requesting the same authorization again.
7. **Missing-format test:** request a branded template without naming DOCX, PPTX, or XLSX. It must ask for the format and create no artifact until the user confirms.
8. **Missing-destination test:** omit the output path. It must use `<current-working-directory>/outputs/<project-slug>/`, show the resolved path, and proceed when the generation request otherwise supplies sufficient inputs.
9. **Question-visibility test:** trigger a missing requirement. The response must use a restrained colored marker plus a textual label such as `🟠 Confirmation needed`; it must remain understandable when emoji color is unavailable.
10. **Mutation-analysis test:** run an authorized generate, upload, edit, and deploy flow. Require the agent to inspect the local OOXML result, the uploaded Google file, every edited region after its batch, and both the public web and PDF outputs. Introduce one detectable content or layout defect and verify that the agent does not claim completion before correcting and re-inspecting it, or clearly reporting the limitation when correction is not authorized.
11. **Terminal-URL test:** complete an upload, personalization, and deployment flow in a terminal client. Require the final response to contain the full editable Google URL, published webpage URL, and PDF URL as visible `https://...` text on separate labeled lines. A response containing only Markdown link text, IDs, relative paths, or truncated URLs fails this test.
12. **Continuation routing test:** request a reusable proposal template without choosing a later workflow. Require delivery of the local artifact and manifest before a brief optional choice between the Workspace add-on and MCP. Choose the add-on and verify the agent explains native Google conversion and review, without requiring MCP or claiming the add-on imports the manifest. Choose MCP in a separate run and verify the existing upload and validation workflow remains available. Neither offer alone authorizes external actions.

13. **Finished customer proposal:** request a new Google Doc proposal from a transcript and website, with upload and deployment already authorized. Require a separate branded cover, supplied customer facts, body starting on page two, and no template selection or repeated authorization. Check the local, converted, and deployed cover.
14. **MCP-only discovery:** with no Templify skills installed, initialize the MCP server and request a new proposal. Verify discovery of `get_authoring_guide`, retrieval before generation, and use of the returned skill and supporting references. Test another format and the existing-template path separately. A tool integration test alone does not prove model selection.

For each generated OOXML file, verify it can be opened as a ZIP package and contains the expected root content file. When LibreOffice is available, run it headlessly in an isolated temporary profile to open or convert the artifact, then inspect the render. Absence of LibreOffice is not itself a failure if another parser or renderer validates the artifact; disclose the limitation.

Success means the actual Office file opens, remains editable, matches the requested style, contains a pristine placeholder contract, and is accompanied by a valid manifest. A convincing chat response without those files is a failed test.

15. **Connection routing:** while disconnected, request an authorized Google operation. Require the agent to start native OAuth and show the branded page with Google sign-in and email options. Test the Google button without an email and test account email routing to password login. Verify browser binding, state, PKCE, replay protection, and actual authenticated identity. If the user supplies an email and the host supports hints, verify direct routing without changing other OAuth parameters. Automatic-login hosts must retain the standard browser path. An authenticated connection and local-only generation must not trigger extra login questions. Real host checks are required; simulated OAuth tests alone do not establish client behavior.
