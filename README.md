# Templify Agent Plugin

Templify creates reusable branded Office templates and turns conversations into editable Google Workspace proposals with separately tracked web/PDF deployments.

Model choice and transcription are provided by your agent host (Claude Code or Codex), not by these skills. The Templify MCP server only performs deterministic Google file, deployment, and analytics operations.

## Included skills

`branded-template-generator` supports:

- DOCX reports, proposals, briefs, and plans
- PPTX presentations and pitch materials
- XLSX models, trackers, and structured plans
- Website-informed visual systems
- Stable `{{placeholder}}` contracts for later personalization

The skill creates local files only: it writes the Office file and its personalization manifest to disk and does not upload, publish, email, or share them. To bring a generated file into Google Workspace, use the `upload_google_file` workflow below.

`proposal-from-conversation` supports:

- Pasted transcripts or recordings transcribed by the user's agent host
- Google Docs, Slides, and Sheets templates selected with Google Picker
- Editable Drive copies without modifying the source template
- Tracked web/PDF deployment and proposal analytics

This skill selects an existing Google Docs, Slides, or Sheets template, copies it, edits the copy, and optionally deploys a separately tracked web/PDF version. It never edits the source template.

Templify does not run AI models or transcription on its backend. The plugin connects to the public Templify MCP endpoint for deterministic Google file and deployment operations.

## Model and transcription selection

Which model writes the proposal and which service transcribes audio is decided by the host application, not by the skill. Claude Code and Codex apply their own model, subagent, and speech-to-text settings. The skills supply instructions and MCP tool calls only; they do not select or override a model, and Templify never uploads or transcribes your audio.

## MCP setup

The public Templify MCP endpoint is declared in [.mcp.json](.mcp.json):

```json
{
  "mcpServers": {
    "templify": {
      "type": "http",
      "url": "https://api-3cfmtpoddq-uc.a.run.app/mcp"
    }
  }
}
```

Claude Code and Codex load this configuration when the plugin is installed or enabled. No MCP server is bundled in this repository; the plugin connects to the hosted endpoint over streamable HTTP.

The first Google-dependent call starts an OAuth flow with the `drive.file` scope. Approve access in the browser for the Google account you want to use. Templify then acts only on files that account can access, and you can revoke access at any time from your Google Account permissions.

MCP is required for the `proposal-from-conversation` skill, `upload_google_file`, deployment, and analytics. `branded-template-generator` works without it.

## Claude Code

Test the plugin from the repository's parent directory:

```bash
claude --plugin-dir ./templify-agent-plugin
```

Invoke the skills explicitly:

```text
/templify:branded-template-generator
/templify:proposal-from-conversation
```

Validate the package before publishing:

```bash
claude plugin validate ./templify-agent-plugin
```

## Codex

The plugin contains a Codex manifest and OpenAI UI metadata. During development, install or load the repository using the plugin workflow supported by your Codex client. The skill can also be uploaded as a skills-only plugin from `skills/branded-template-generator/` through the OpenAI plugin submission portal.

Invoke the skills explicitly as:

```text
$branded-template-generator
$proposal-from-conversation
```

### One-prompt setup for any agent

Paste this into a new Claude Code, Codex, or compatible agent session from the plugin repository:

```text
----- BEGIN TEMPLIFY SETUP PROMPT -----
Set up Templify in this agent. Do what you can and guide me through anything that needs my input.

1. Identify this agent and version, then inspect existing plugins, MCP servers, and skills. Preserve existing configuration and avoid duplicates.
2. Install the Templify plugin using this agent's supported plugin or skill workflow. Prefer the local repository at /home/conve/Project/templify-agent-plugin; if it is unavailable, use the Git repository Doc-Failure/templify-agent-plugin. Check the installed client's help or current documentation before running commands.
3. Confirm that the Templify plugin includes both skills and its MCP configuration. Do not copy credentials into chat, shell history, or repository files.
4. Reload or restart the agent only if required. On the first Google-dependent action, let me approve the Templify OAuth flow in my browser.
5. Verify that the Templify MCP tools and skills are discoverable, but do not create, upload, edit, deploy, or purchase anything during setup.

When setup is complete, briefly report what succeeded and any action I must take. Then suggest these tests:
- Generate a local branded DOCX, PPTX, or XLSX template.
- Upload it to Google Drive with Templify, only after I confirm.
- Ask Templify for the current plan status.
----- END TEMPLIFY SETUP PROMPT -----
```

Copy only the text between the `BEGIN` and `END` markers.

### One-prompt first template and deployment

After setup, paste this prompt to interactively create, upload, personalize, and deploy the first template:

```text
----- BEGIN TEMPLIFY FIRST TEMPLATE PROMPT -----
Help me create and deploy my first Templify template interactively.

1. Ask only for missing information, one concise group of questions at a time:
   - Format: DOCX, PPTX, or XLSX
   - Template purpose and intended audience
   - Brand or website URL, or a written style direction
   - Language, tone, approximate length, and required sections
   - Content, placeholders, or source material
   - Local output directory
   - Google Drive folder, if I want a specific folder
2. Summarize the brief with the proposed structure, style source, output path, and placeholders. Wait for my confirmation before generating.
3. Generate and validate the local Office template and its manifest with the branded-template-generator skill.
4. Show me the local files and ask for explicit confirmation before uploading. If confirmed, upload only the Office file with upload_google_file; never upload the manifest unless I explicitly ask.
5. Inspect the uploaded Google file. If I asked for personalization, ask for any missing recipient or proposal information, apply edits only to the uploaded file or a copied file, and re-inspect it.
6. Before deployment, show the Google file URL and ask for explicit confirmation. Ask for any missing deployment title, client name, display mode (scroll or book), and expiration date. Do not invent facts, prices, dates, or commitments.
7. After confirmation, deploy the Google file with deploy_google_file and return the editable Google URL, public deployment URL, PDF URL, deployment ID, and expiration.
8. Do not purchase a plan, change billing, or edit an original source template without my explicit request.
----- END TEMPLIFY FIRST TEMPLATE PROMPT -----
```

Copy only the text between the `BEGIN` and `END` markers. The agent must pause for confirmation before generation, upload, personalization, and deployment.

If the agent cannot install the private Git repository directly, clone this repository locally first and rerun the prompt from that checkout. The plugin's MCP endpoint is already declared in `.mcp.json`.

## Usage

### 1. Generate a branded template locally

Invoke `branded-template-generator` and supply the format (DOCX, PPTX, or XLSX), purpose, audience, style source, and an output directory. The skill confirms the brief, derives the visual system, and writes two files to the confirmed directory:

```text
<output-directory>/<template-name>.<docx|pptx|xlsx>
<output-directory>/<template-name>.manifest.json
```

The artifact and manifest stay on your machine. Nothing is uploaded, published, or shared by this skill.

### 2. Upload an Office file to Google

Use `upload_google_file` to send a local `.docx`, `.pptx`, or `.xlsx` to Google Drive and receive the corresponding editable Google Docs, Slides, or Sheets file. This is the bridge from a locally generated template to the Google tools that edit, deploy, and track a file:

```text
Generate locally with branded-template-generator
        ↓ upload_google_file
Editable Google Docs / Slides / Sheets file
        ↓ apply_google_file_edits, deploy_google_file
Tracked web/PDF deployment + analytics
```

Ask for it explicitly, for example: "Upload `./outputs/acme-proposal/proposal.docx` to Google Drive and give me the editable Google Doc." The tool returns the Google file ID and URL, which the remaining MCP tools accept as `file`.

### 3. Turn a conversation into a proposal

Invoke `proposal-from-conversation` with a pasted transcript (or an audio attachment the host can transcribe) and a Google Docs, Slides, or Sheets template. The skill:

1. Uses Google Picker (`choose_google_template` → `get_google_template_selection`) when you have not supplied an accessible template URL or ID.
2. Inspects the source with `inspect_google_file`.
3. Copies it with `copy_google_file`, so the original template is never modified.
4. Applies typed Google `batchUpdate` requests with `apply_google_file_edits`.
5. Publishes a separate tracked version with `deploy_google_file` only after you request or confirm deployment.

Prices, dates, commitments, and customer facts are never invented; assumptions are labeled.

### 4. Deployment URLs

`deploy_google_file` exports the Google file to PDF and publishes a tracked public web version. It returns:

- `deploymentId` — use this for analytics and unpublishing
- `url` — the tracked web deployment (`scroll` or `book` display mode)
- `pdfUrl` — the exported PDF
- `expiresAt` — when the deployment stops being available
- `quota` — monthly usage and remaining allowance

Every deployment is public and tracked separately from the editable Google file. Share the returned `url` for the web version or `pdfUrl` for the PDF.

### 5. Analytics

- `list_deployments` returns your active deployments with their URLs, status, expiry, and view counts.
- `get_deployment_stats` returns analytics for one `deploymentId`: total views, unique visitors, last viewed time, views by day, per-page engagement (average and total time), devices, browsers, and top referrers.
- `unpublish_deployment` permanently removes a deployment and its analytics; use it only when you intend to delete.

Ask the assistant for a summary, for example: "List my deployments and show stats for the Acme proposal."

### 6. Manage your plan

- **Upgrade to Pro:** ask the assistant to upgrade. It returns a secure Stripe Checkout link for the Templify subscription; complete payment in the browser. The Pro plan is applied to the Google account connected to the MCP server.
- **Manage or cancel:** ask the assistant to manage your subscription. It returns a Stripe customer portal link where you can update your payment method, change plans, or cancel. Pro stays active while the subscription is active or trialing and is removed once it lapses.

Free accounts can deploy up to 5 tracked proposals per month, and each free deployment expires 7 days after creation. Pro removes the monthly deployment limit and lets you choose the expiry, or leave it open-ended. The skills always respect Templify's quota and expiry; they never bypass them.

## MCP tools

| Tool | Purpose |
| --- | --- |
| `choose_google_template` | Create a short-lived Google Picker link for a Docs, Slides, or Sheets template. |
| `get_google_template_selection` | Return the file selected with a Picker ticket. |
| `inspect_google_file` | Read metadata and content (`summary` or `structure`) from a Google file. |
| `copy_google_file` | Create an editable Drive copy without changing the source template. |
| `upload_google_file` | Upload a local DOCX, PPTX, or XLSX and get the editable Google file. |
| `apply_google_file_edits` | Apply typed Google batchUpdate requests to a copied file. |
| `deploy_google_file` | Export to PDF and publish a separately tracked web version. |
| `list_deployments` | List your active tracked deployments. |
| `get_deployment_stats` | Return views, visitors, engagement, devices, browsers, and referrers. |
| `unpublish_deployment` | Permanently remove a deployment and its analytics. |
| `get_templify_plan_status` | Show Free/Pro status, quota, and subscription status. |
| `upgrade_templify_pro` | Return a secure Stripe Checkout link for upgrading. |
| `manage_templify_subscription` | Return a Stripe Portal link to update payment details or cancel. |

## Repository layout

```text
.
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── .mcp.json
└── skills/
    ├── branded-template-generator/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    └── proposal-from-conversation/
        ├── SKILL.md
        └── agents/openai.yaml
```

## License

MIT
