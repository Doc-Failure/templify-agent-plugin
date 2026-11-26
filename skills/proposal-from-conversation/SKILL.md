---
name: proposal-from-conversation
description: Turn a sales call, meeting, interview, or discovery transcript into an editable Google Docs, Slides, or Sheets proposal, then optionally publish a tracked web/PDF version and measure proposal views and engagement analytics with Templify. Use for sales proposals, client proposals, pitch decks, and follow-up documents created from conversations; do not use for reusable local Office templates.
---

# Proposal from Conversation

Create the proposal with the model and transcription capabilities supplied by the user's agent host. Templify does not provide AI or transcription; its MCP tools only select, inspect, copy, edit, export, deploy, and track Google files.

## Terminal-safe URLs are mandatory

Whenever an MCP operation returns or identifies a URL, show the complete absolute URL as visible plain text. A Markdown link whose destination is hidden behind link text is never sufficient. Do not shorten, truncate, or replace a URL with a file ID.

After a file is copied or uploaded, show its editable Google URL. Preserve that URL through personalization and show it again after edits. After deployment, the final response must show the editable Google URL, public webpage URL, and PDF URL, each on its own line in a plain-text block exactly like this:

```text
Editable Google file: https://docs.google.com/...
Published webpage: https://...
PDF: https://...
```

The labels may be localized, but every value must begin with `https://` and remain directly copyable from a terminal. A clickable Markdown link may be added separately, but never instead of these raw URLs. If an MCP response supplies only an ID, use the file type and ID to construct the canonical absolute Google URL before handoff. If no valid absolute URL can be obtained, report that explicitly rather than presenting an ID as a link.

## Connect to Templify

For an authorized Google operation that needs a new MCP connection, start the host's normal OAuth login flow. The Templify page offers **Continue with Google** and an email field. Regular users can select Google directly; test users enter their assigned email to reach password login. Passwords and verification codes stay in the browser. Reuse an existing authenticated connection; local-only generation needs no connection.

If the user wants to supply the email in chat and the host supports an OAuth `login_hint`, pass it through the supported login flow to skip the initial page. If the host exposes its pending Templify `/oauth/authorize` URL for opening, set only the encoded `login_hint`, preserving every other parameter, including state, PKCE, client, redirect URI, and resource. Never fabricate an OAuth transaction, request tokens yourself, or store the email in shared MCP configuration. If hints are unsupported, use the browser options and explain the limitation. An email selects the sign-in route; Google or password verification establishes identity.

## Establish the inputs

Identify the conversation source, Google template, intended recipient, output filename, proposal objective, and whether deployment is requested. Use a pasted transcript directly. When audio is attached, transcribe it with the host's native capability; if that capability is unavailable, ask for a transcript. Never upload audio to Templify.

Choose the creation path from the request:

- **New proposal without an existing template:** use `$branded-template-generator` in finished-customer-proposal mode. If that skill is not installed, call `get_authoring_guide` with `workflow: "create"` and the requested format (`docx` for Google Docs, `pptx` for Slides, `xlsx` for Sheets); read its supplied skill and reference contents. Generate and validate the local file, then upload and deploy only as authorized. Do not require the user to choose a template for this path.
- **Personalize an existing template:** accept Google Docs, Slides, and Sheets templates and follow the copy-and-edit workflow below. If the user wants to use a template but has not supplied an accessible URL or ID, call `choose_google_template`, give them its Picker link, and poll `get_google_template_selection` after selection. Display the complete absolute `pickerUrl` using the terminal-safe rule above.

When instructions arrive through `get_authoring_guide`, use the supplied contents directly; no local skill installation is required.

## Create the editable Google file

1. Call `inspect_google_file` with summary detail to understand the source.
2. Call it with structure detail when precise object IDs, ranges, indices, formatting, or layout are needed.
3. Synthesize all proposal content from the conversation in the agent. Do not expect placeholders and do not ask Templify to generate copy.
4. Call `copy_google_file` before making edits. Never edit the source template.
5. Inspect the new copy before editing and confirm that its type, content, structure, and page, slide, or sheet count match the source.
6. Apply the specific supported editing tool for the copied file and requested change (see the table below). After every edit, re-inspect the affected content or structure before making another edit that depends on it.
7. After the final edit, inspect the whole copy at summary detail and the changed regions at structure detail. Analyze content completeness, ordering, editability, and obvious layout risks; correct problems and repeat the relevant inspection. Leave the editable Google file in the user's Drive.

Do not invent prices, commitments, customer facts, dates, or outcomes that the conversation does not support. Clearly label assumptions and proposed values.

For Google Docs proposals, preserve and personalize an existing cover. If the copied template has no cover, add a dedicated opening page using its brand system unless the user requests otherwise. Keep title, subtitle, and supported recipient/sender metadata on the cover, with pricing and summary content in the body after an explicit page break. Check the cover in the edited file and any exported PDF; never add it to the source template.

## Supported editing tools

Use only the individually exposed editing tools. The former `apply_google_file_edits` operation is removed; do not send raw Google API commands, request arrays, or an operation selector to any replacement tool.

| File type | Task | Tool |
| --- | --- | --- |
| Docs | Replace literal text/placeholders | `replace_google_docs_text` |
| Docs | Insert or append plain text | `insert_google_docs_text` |
| Docs | Separate the cover and body | `insert_google_docs_page_break` |
| Docs | Format a text range | `format_google_docs_text` |
| Docs | Format paragraph alignment, spacing, headings | `format_google_docs_paragraphs` |
| Slides | Replace literal text/placeholders | `replace_google_slides_text` |
| Slides | Set/clear one shape's text | `set_google_slide_text` |
| Slides | Format one shape's text | `format_google_slide_text` |
| Slides | Create one slide from a native layout | `create_google_slide` |
| Slides | Insert a plain-text text box | `insert_google_slide_text_box` |
| Sheets | Write literal values in a finite A1 range | `set_google_sheet_values` |
| Sheets | Set explicitly authorized formulas | `set_google_sheet_formulas` |
| Sheets | Format a bounded cell rectangle | `format_google_sheet_cells` |

All edits require a file created for the connected account by `copy_google_file` or `upload_google_file`. Never edit the original template. Inspect the file first for the correct file kind, tab/shape/sheet IDs and text indexes, then re-inspect after each edit before issuing dependent changes. Docs text indexes are UTF-16; end indexes are exclusive. Sheets formatting uses zero-based grid indexes, while value/formula tools use finite sheet-qualified A1 ranges whose dimensions must exactly match the supplied rectangular matrix. Literal values are written in RAW mode, even if a string begins with '='; formulas use their separate tool and may access external data, so use only formulas the user authorized.

If the requested edit is not supported by an exposed tool, explain the limitation. Do not reconstruct the removed generic executor or fabricate a tool name. For a new proposal, authoring and validating a local Office file before upload remains available. Do not silently replace a user's existing file or broaden the requested changes to work around a missing operation.

## Analyze every created or changed file

Treat every file-changing MCP operation as unfinished until its result has been inspected. Do not infer quality from a successful tool response alone. This applies to copies, uploads used in the workflow, every edit batch, and deployments.

Use `inspect_google_file` after a Google file is copied, uploaded, or edited. Compare the result with its source or intended change, using summary detail for the whole file and structure detail for affected regions. When analysis finds a problem, fix it if the current request authorizes that file operation, then inspect it again; otherwise report the problem before expanding scope.

After deployment, open and analyze both the returned public web URL and PDF URL with the browsing or document-inspection capability available in the runtime. Confirm that they load, represent the intended edited Google file, contain the expected content and pages, and have no obvious clipping, missing assets, ordering errors, or unreadable output. If a required inspection capability is unavailable, perform the strongest available structural check, state exactly what could not be visually verified, and do not claim that the unchecked representation was validated.

## Deploy and track

Deployment publishes a separate public web/PDF version and consumes Templify quota. Call `deploy_google_file` only when the user has requested deployment or confirms it after reviewing the editable Google file. After deployment, analyze the web and PDF results as required above before handoff.

Return both `googleFileUrl` and the tracked deployment `url`, plus the PDF URL and expiration. Use the required terminal-safe output block and repeat all three absolute URLs even if the editable Google URL was shown earlier. Do not return only a file ID or relative path. Free accounts receive the quota and expiry enforced by Templify; never attempt to bypass them.

Use `get_deployment_stats` for analytics, `list_deployments` for management, and `unpublish_deployment` only after the user explicitly requests deletion.
