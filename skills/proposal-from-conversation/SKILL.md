---
name: proposal-from-conversation
description: Turn a pasted transcript or attached conversation recording into an editable Google Docs, Slides, or Sheets proposal and optionally deploy a separately tracked web/PDF version with Templify. Use when the user wants a proposal created from a call, meeting, interview, or discovery conversation. Do not use for reusable local Office templates.
---

# Proposal from Conversation

Create the proposal with the model and transcription capabilities supplied by the user's agent host. Templify does not provide AI or transcription; its MCP tools only select, inspect, copy, edit, export, deploy, and track Google files.

## Establish the inputs

Identify the conversation source, Google template, intended recipient, output filename, proposal objective, and whether deployment is requested. Use a pasted transcript directly. When audio is attached, transcribe it with the host's native capability; if that capability is unavailable, ask for a transcript. Never upload audio to Templify.

Accept Google Docs, Slides, and Sheets templates. If the user has not supplied an accessible Google file URL or ID, call `choose_google_template`, give them its Picker link, and then poll `get_google_template_selection` after they finish selecting. Always display the complete `pickerUrl` as plain text in a fenced code block; do not hide it behind Markdown link text, because some MCP clients do not make rendered links clickable.

## Create the editable Google file

1. Call `inspect_google_file` with summary detail to understand the source.
2. Call it with structure detail when precise object IDs, ranges, indices, formatting, or layout are needed.
3. Synthesize all proposal content from the conversation in the agent. Do not expect placeholders and do not ask Templify to generate copy.
4. Call `copy_google_file` before making edits. Never edit the source template.
5. Apply typed Google Docs, Slides, or Sheets `batchUpdate` operations to the copy with `apply_google_file_edits`. Use small coherent batches and re-inspect after structural changes when later indices or object IDs depend on them.
6. Inspect the copy and correct incomplete content or obvious structural problems. Leave the editable Google file in the user's Drive.

Do not invent prices, commitments, customer facts, dates, or outcomes that the conversation does not support. Clearly label assumptions and proposed values.

## Deploy and track

Deployment publishes a separate public web/PDF version and consumes Templify quota. Call `deploy_google_file` only when the user has requested deployment or confirms it after reviewing the editable Google file.

Return both `googleFileUrl` and the tracked deployment `url`, plus the PDF URL and expiration. Always show every URL as a complete absolute URL in a fenced code block, including the `https://docs.google.com/...` editable-file URL, public deployment URL, and PDF URL. Do not return only a file ID, relative path, or hide these URLs behind Markdown link text. Free accounts receive the quota and expiry enforced by Templify; never attempt to bypass them.

Use `get_deployment_stats` for analytics, `list_deployments` for management, and `unpublish_deployment` only after the user explicitly requests deletion.
