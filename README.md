# Templify Agent Plugin

Templify creates reusable, branded Microsoft Word, PowerPoint, and Excel templates from a public website or a visual style brief. Generated templates remain editable and include a machine-readable personalization manifest.

## Included skill

`branded-template-generator` supports:

- DOCX reports, proposals, briefs, and plans
- PPTX presentations and pitch materials
- XLSX models, trackers, and structured plans
- Website-informed visual systems
- Stable `{{placeholder}}` contracts for later personalization

The skill creates local files only. It does not upload, publish, email, or share generated documents.

## Claude Code

Test the plugin from the repository's parent directory:

```bash
claude --plugin-dir ./templify-agent-plugin
```

Invoke the skill explicitly:

```text
/templify:branded-template-generator
```

Validate the package before publishing:

```bash
claude plugin validate ./templify-agent-plugin
```

## Codex

The plugin contains a Codex manifest and OpenAI UI metadata. During development, install or load the repository using the plugin workflow supported by your Codex client. The skill can also be uploaded as a skills-only plugin from `skills/branded-template-generator/` through the OpenAI plugin submission portal.

Invoke it explicitly as:

```text
$branded-template-generator
```

## MCP integration

This repository is ready to host a related MCP server alongside the skill. No MCP server is currently bundled. When one is added, keep its implementation self-contained in this repository and add the platform-specific MCP configuration only after its runtime command or public HTTPS endpoint is available.

## Repository layout

```text
.
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
└── skills/
    └── branded-template-generator/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/
```

## License

MIT
