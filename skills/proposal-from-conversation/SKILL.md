---
name: proposal-from-conversation
description: Turn a pasted transcript or attached conversation recording into an editable Google Docs, Slides, or Sheets proposal and optionally deploy a separately tracked web/PDF version with Templify. Use when the user wants a proposal created from a call, meeting, interview, or discovery conversation. Do not use for reusable local Office templates.
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

## Establish the inputs

Identify the conversation source, Google template, intended recipient, output filename, proposal objective, and whether deployment is requested. Use a pasted transcript directly. When audio is attached, transcribe it with the host's native capability; if that capability is unavailable, ask for a transcript. Never upload audio to Templify.

Accept Google Docs, Slides, and Sheets templates. If the user has not supplied an accessible Google file URL or ID, call `choose_google_template`, give them its Picker link, and then poll `get_google_template_selection` after they finish selecting. Display the complete absolute `pickerUrl` using the terminal-safe rule above, because some MCP clients do not make rendered links clickable.

## Create the editable Google file

1. Call `inspect_google_file` with summary detail to understand the source.
2. Call it with structure detail when precise object IDs, ranges, indices, formatting, or layout are needed.
3. Synthesize all proposal content from the conversation in the agent. Do not expect placeholders and do not ask Templify to generate copy.
4. Call `copy_google_file` before making edits. Never edit the source template.
5. Inspect the new copy before editing and confirm that its type, content, structure, and page, slide, or sheet count match the source.
6. Apply typed Google Docs, Slides, or Sheets `batchUpdate` operations to the copy with `apply_google_file_edits`. Use small coherent batches. After every batch, re-inspect the affected content or structure before making another edit that depends on it.
7. After the final edit, inspect the whole copy at summary detail and the changed regions at structure detail. Analyze content completeness, ordering, editability, and obvious layout risks; correct problems and repeat the relevant inspection. Leave the editable Google file in the user's Drive.

Do not invent prices, commitments, customer facts, dates, or outcomes that the conversation does not support. Clearly label assumptions and proposed values.

## Analyze every created or changed file

Treat every file-changing MCP operation as unfinished until its result has been inspected. Do not infer quality from a successful tool response alone. This applies to copies, uploads used in the workflow, every edit batch, and deployments.

Use `inspect_google_file` after a Google file is copied, uploaded, or edited. Compare the result with its source or intended change, using summary detail for the whole file and structure detail for affected regions. When analysis finds a problem, fix it if the current request authorizes that file operation, then inspect it again; otherwise report the problem before expanding scope.

After deployment, open and analyze both the returned public web URL and PDF URL with the browsing or document-inspection capability available in the runtime. Confirm that they load, represent the intended edited Google file, contain the expected content and pages, and have no obvious clipping, missing assets, ordering errors, or unreadable output. If a required inspection capability is unavailable, perform the strongest available structural check, state exactly what could not be visually verified, and do not claim that the unchecked representation was validated.

## Deploy and track

Deployment publishes a separate public web/PDF version and consumes Templify quota. Call `deploy_google_file` only when the user has requested deployment or confirms it after reviewing the editable Google file. After deployment, analyze the web and PDF results as required above before handoff.

Return both `googleFileUrl` and the tracked deployment `url`, plus the PDF URL and expiration. Use the required terminal-safe output block and repeat all three absolute URLs even if the editable Google URL was shown earlier. Do not return only a file ID or relative path. Free accounts receive the quota and expiry enforced by Templify; never attempt to bypass them.

Use `get_deployment_stats` for analytics, `list_deployments` for management, and `unpublish_deployment` only after the user explicitly requests deletion.
