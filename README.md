# Templify Agent Plugin

Templify creates branded sales proposal templates and pitch decks, turns conversations into editable proposals in Google Slides, Docs, or Sheets, and publishes tracked web/PDF versions with proposal engagement analytics.

## Websites

- Product: https://trytemplify.com/
- Free AI Proposal Template Generator: https://trytemplify.com/free-ai-proposal-template-generator/
- Templify MCP: https://trytemplify.com/templify-mcp/
- Developer: https://www.irvito.com/

Model choice and transcription are provided by your agent host (Claude Code or Codex), not by these skills. The Templify MCP server only performs deterministic Google file, deployment, and analytics operations.

## Included skills

`branded-template-generator` supports:

- DOCX reports, proposals, briefs, and plans with a dedicated branded cover
- PPTX presentations and pitch materials
- XLSX models, trackers, and structured plans
- Website-informed visual systems
- Stable `{{placeholder}}` contracts for later personalization

The skill creates reusable templates or finished customer documents locally. Templates include a personalization manifest; finished proposals use the supplied customer facts. Upload and deployment occur only when requested, through the MCP handoff below.

`proposal-from-conversation` supports:

- Pasted transcripts or recordings transcribed by the user's agent host
- Google Docs, Slides, and Sheets templates selected with Google Picker
- Editable Drive copies without modifying the source template
- Tracked web/PDF deployment and proposal analytics

This skill can personalize a copy of an existing Google Docs, Slides, or Sheets template, or route a new proposal without a source template to `branded-template-generator`. It never edits a source template. Upload and tracked web/PDF deployment follow the user's authorization.

`google-slides-template-builder` supports:

- Reusable Google Slides proposals, presentation templates, and pitch decks
- Starting from Google's built-in Slides template gallery instead of a local PPTX
- Google-native editing of the copied deck through Templify MCP

Use it when you want a Google-native deck; use `branded-template-generator` for local Office files and `proposal-from-conversation` to personalize a template for a specific recipient.

Templify does not run AI models or transcription on its backend. The plugin connects to the public Templify MCP endpoint for deterministic Google file and deployment operations.

All skills treat file mutations as checkpoints rather than assuming success from a write or MCP response. They analyze locally generated Office files, inspect Google files after copies, uploads, and edit batches, and inspect the public web/PDF representations after deployment. If the runtime cannot perform a visual check, it reports the limitation instead of claiming visual validation.

For terminal compatibility, every Google or deployment handoff includes visible, unshortened absolute URLs. After deployment, the editable Google file, public webpage, and PDF URLs are printed as labeled `https://...` text on separate lines; Markdown links are optional and never replace the raw URLs.

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

For a new connection, the host starts its standard OAuth flow. Templify's branded login page offers **Continue with Google** and an email option. Regular users can sign in with Google directly; test users enter their assigned email to reach password login. An optional OAuth `login_hint` can skip this page when the user supplies an email and the host supports passing it. Passwords and verification codes stay in the browser. Existing authenticated connections are reused. Google access uses the `drive.file` scope and can be revoked from Google Account permissions.

MCP is required for the `proposal-from-conversation` skill, `upload_google_file`, deployment, and analytics. `branded-template-generator` works without it.

### Authoring guidance for MCP-only clients

The server integration exposes `get_authoring_guide` so an agent connected only to MCP can retrieve the same maintained skills without installing this plugin. Server initialization instructions and relevant tool descriptions direct the agent to retrieve the guide before generating a file. The response includes the skill and supporting references inline, including DOCX cover design; it performs no generation, installation, Google writes, or quota-consuming operations.

- `format`: `docx`, `pptx`, or `xlsx` (also used for Google Docs, Slides, and Sheets respectively).
- `workflow`: `create` (default), `personalize_template`, or `google_slides_template` (PPTX only).

For example, a new customer proposal for Google Docs uses `{"format":"docx","workflow":"create"}`. A request to copy and personalize an existing Google template uses `personalize_template`. Uploading an existing user file, checking analytics, or managing billing does not require an authoring guide.

This is model-readable workflow guidance, not automatic local skill installation or a server-enforced design guarantee. Clients must expose the tool and the agent must follow its instructions. The full plugin remains available for native skill discovery.

The MCP backend lives in the separate Google Workspace service repository. Before releasing a skill change to MCP users, export a matching bundle into that service:

```bash
python3 scripts/export-authoring-guides.py --output <service-repo>/functions/src/data/templifyAuthoringGuides.json
python3 scripts/export-authoring-guides.py --output <service-repo>/functions/src/data/templifyAuthoringGuides.json --check
```

The exporter includes only the maintained skill Markdown and references, checks relative reference completeness, and records a content hash. Commit the generated JSON with the service change; the backend embeds it at build time instead of fetching mutable GitHub content at runtime. Run `npm run test:mcp-authoring` and `npm run build` in the service's `functions/` directory before deployment. Repository changes alone do not update the hosted MCP endpoint: deploy the server, then reconnect or refresh the client's MCP tools and verify `get_authoring_guide` is listed. Clients connected to an older server can still use the installed plugin.

## Published packages

Download the current plugin from [GitHub Releases](https://github.com/Doc-Failure/templify-agent-plugin/releases/latest). Release assets contain the plugin manifests, MCP configuration, all three maintained skills and references, branding assets, and license. `SHA256SUMS.txt` accompanies each release.

The versioned plugin download is separate from the hosted MCP authoring guide. The MCP server serves its embedded `templifyAuthoringGuides.json` bundle; it does not read or install ZIP/TAR archives. Codex Marketplace submission is also separate from a GitHub release.

To prepare a release, update both plugin manifests to the same version, validate the skills and manifests, and commit the source. Build packages from that clean commit:

```bash
python3 scripts/package-release.py --output-dir /tmp/templify-release
```

Tag and push that exact commit, then attach the generated ZIP, TAR.GZ, and checksums to its GitHub Release. Keep release archives out of the source tree. Before releasing authoring changes to MCP users, also synchronize and deploy the backend bundle as described above.

## Claude Code

Install the plugin from its public marketplace:

```text
/plugin marketplace add Doc-Failure/templify-agent-plugin
/plugin install templify@templify
```

Test the plugin from the repository's parent directory:

```bash
claude --plugin-dir ./templify-agent-plugin
```

Invoke the skills explicitly:

```text
/templify:branded-template-generator
/templify:google-slides-template-builder
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
$google-slides-template-builder
$proposal-from-conversation
```

### One-prompt setup for any agent

Paste this into a new Claude Code, Codex, or compatible agent session from the plugin repository:

```text
----- BEGIN TEMPLIFY SETUP PROMPT -----
Set up Templify in this agent. Do what you can and guide me through anything that needs my input.

1. Identify this agent and version, then inspect existing plugins, MCP servers, and skills. Preserve existing configuration and avoid duplicates.
2. Install the Templify plugin using this agent's supported plugin or skill workflow. Use the public Git repository Doc-Failure/templify-agent-plugin, or a local checkout of it if I have one. Check the installed client's help or current documentation before running commands.
3. Confirm that the Templify plugin includes its three skills and its MCP configuration. Do not copy credentials into chat, shell history, or repository files.
4. Reload or restart the agent only if required. If a new connection is needed, start the normal OAuth flow and let me choose Google sign-in or enter my test account email on the Templify page. If I supply an email and the host supports a login hint, pass it as `login_hint` to skip that page. Let me complete authentication in the browser; never ask for passwords or codes in chat.
5. Verify that the Templify MCP tools and skills are discoverable, but do not create, upload, edit, deploy, or purchase anything during setup.

When setup is complete, briefly report what succeeded and any action I must take. Then suggest these tests:
- Generate a local branded DOCX, PPTX, or XLSX template.
- Upload it to Google Drive with Templify, only after I confirm.
- Ask Templify for the current plan status.
----- END TEMPLIFY SETUP PROMPT -----
```

Copy only the text between the `BEGIN` and `END` markers.

### Test prompt: generate a personalized presentation only

After setup, use this prompt when a customer wants a personalized, editable presentation without uploading or deploying it:

```text
----- BEGIN TEMPLIFY PRESENTATION-ONLY PROMPT -----
Use the branded-template-generator skill to create a personalized, editable PPTX presentation for a customer.

Start by asking me for the website URL. In the same message, briefly explain that you will use it to understand the brand's colors, typography, imagery, and tone—not to copy the site pixel for pixel. Wait for my answer before asking for anything else.

Then ask me for the presentation content or source material and any customer-specific facts that are not already included. Infer the presentation's purpose, audience, language, tone, structure, title, and approximate length from that content. Do not ask me to restate information you can infer. Never invent customer facts, prices, dates, claims, or commitments.

Use a sensible local output folder under the current working directory unless I provide another path. Show me a short brief and proposed slide structure, then generate and validate the PPTX and its adjacent personalization manifest. Keep text, charts, and shapes editable. Return clickable paths to both files.

This is a local-generation test only. Do not ask for a Google Drive folder, upload the presentation, personalize a Google copy, or deploy it.
----- END TEMPLIFY PRESENTATION-ONLY PROMPT -----
```

Copy only the text between the `BEGIN` and `END` markers.

### Test prompt: generate and deploy a presentation

Use this shorter prompt to create, upload, personalize, and deploy a customer presentation:

```text
----- BEGIN TEMPLIFY GENERATE-AND-DEPLOY PROMPT -----
Use the branded-template-generator skill to create, upload, and deploy a personalized, editable PPTX presentation for a customer.

Start by asking me for the website URL. In the same message, briefly explain that you will use it to understand the brand's colors, typography, imagery, and tone—not to copy the site pixel for pixel. Wait for my answer before asking for anything else.

Next, ask me for the presentation content or source material and any essential customer-specific facts that are missing. Infer the purpose, audience, language, tone, title, structure, approximate length, and deployment title from the supplied content. Do not ask for the template purpose, a Google Drive folder, or details I already provided. Never invent customer facts, prices, dates, claims, or commitments.

Use a sensible local output folder under the current working directory. Briefly summarize the inferred brief and slide structure, then:

1. Generate and validate the local PPTX and its adjacent manifest.
2. Upload only the PPTX with `upload_google_file` and inspect the editable Google Slides file.
3. Correct any obvious content or layout problems in the uploaded file without editing an unrelated source template.
4. Deploy it with `deploy_google_file`, using scroll mode and the service's default expiration unless the supplied content or my instructions specify otherwise.
5. Return the local file paths, editable Google URL, public deployment URL, PDF URL, deployment ID, and expiration.

This prompt already authorizes upload and deployment, so do not ask for another confirmation. Do not purchase a plan or change billing.
----- END TEMPLIFY GENERATE-AND-DEPLOY PROMPT -----
```

Copy only the text between the `BEGIN` and `END` markers. The agent asks for the website first, gathers only essential missing content, and then completes the requested upload and deployment without extra confirmation prompts.

If the agent cannot install the Git repository directly, clone this repository locally first and rerun the prompt from that checkout. The plugin's MCP endpoint is already declared in `.mcp.json`.

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

- **Account and billing website:** use https://app.trytemplify.com/ with the same Google account connected to MCP. The standalone website shows plan and usage, offers subscriptions through Stripe, and manages existing billing without requiring the Workspace add-on. Purchases are initiated independently on the website; the public MCP tools do not start subscriptions or return checkout links.
- **Manage or cancel:** ask the assistant to manage your subscription. It returns a Stripe customer portal link where you can update your payment method, change plans, or cancel. Pro stays active while the subscription is active or trialing and is removed once it lapses.

Free accounts can deploy up to 5 tracked proposals per month, and each free deployment expires 7 days after creation. Pro removes the monthly deployment limit and lets you choose the expiry, or leave it open-ended. The skills always respect Templify's quota and expiry; they never bypass them.

## MCP tools

| Tool | Purpose |
| --- | --- |
| `get_authoring_guide` | Read the maintained authoring skill and references before creating a proposal or template; requires the server release containing the guide integration. |
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
| `manage_templify_subscription` | Return a Stripe Portal link to update payment details or cancel. |

## Repository layout

```text
.
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .codex-plugin/plugin.json
├── .mcp.json
├── assets/
└── skills/
    ├── branded-template-generator/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    ├── google-slides-template-builder/
    │   ├── SKILL.md
    │   └── agents/openai.yaml
    └── proposal-from-conversation/
        ├── SKILL.md
        └── agents/openai.yaml
```

## Privacy, terms, and support

- Privacy policy: https://trytemplify.com/privacy-policy/
- Terms of service: https://trytemplify.com/terms-of-service/
- Support: https://trytemplify.com/customer-support/ or support@irvito.com

## License

MIT
