---
name: google-slides-template-builder
description: Create a reusable Google Slides sales proposal, presentation template, or pitch deck from Google's built-in Slides template gallery. Use when the user wants a Google-native presentation or proposal deck based on an existing Google design instead of a locally generated PPTX. Do not use for Google Docs, Sheets, local Office files, or recipient-specific proposal personalization.
---

# Google Slides Template Builder

Create a reusable Google Slides template by starting from a presentation in Google's built-in template gallery, then adapting its slide structure and example content to the user's brief. Preserve the Google-native theme, layouts, typography, shapes, and editable elements.

## Establish the brief

Confirm the presentation's purpose, audience, approximate length, language, and reusable fields. If the user has not selected a gallery design, offer two or three relevant Google Slides template categories or names and ask them to choose before creating a Drive file.

This workflow creates a Google Slides file in the user's Drive. Verify the intended Google account before creating it, especially when more than one Google account is signed in.

## Start from a Google template

When the runtime has browser access to the user's signed-in Google session:

1. Open the official Google Slides template gallery.
2. Select the confirmed Google template.
3. Create a new presentation from it and insert the required template slides.
4. Give the file a descriptive name ending in `— Template`.
5. Confirm that the file belongs to the intended Google account.

Do not imitate or rebuild the design from screenshots. Use the editable elements Google places in the new presentation.

When signed-in browser access is unavailable, ask the user to create a presentation from the Google Slides template gallery. Then call `choose_google_template`, show its complete `pickerUrl` in a fenced code block, and poll `get_google_template_selection` after the user selects the new presentation.

## Make it reusable

Authorize or select the created presentation through Templify before editing it. Call `inspect_google_file` with summary detail, then with structure detail when object IDs or precise slide operations are required.

Adapt the deck to the confirmed brief:

- Keep the Google theme and useful native layouts.
- Retain only the slides needed for the intended reusable structure.
- Replace gallery example copy with stable `{{snake_case_placeholders}}`, reusable instructions, or permanent labels.
- Keep one primary message or purpose per slide.
- Clearly label example figures, dates, prices, claims, and testimonials; never present invented values as facts.
- Use `apply_google_file_edits` in small coherent batches and re-inspect after structural changes.

This skill creates a reusable template, not a recipient-specific proposal. Do not deploy or publish it. Use the proposal personalization workflow later to copy, populate, and optionally deploy the template.

## Validate and return

Inspect the completed presentation and confirm that it remains editable, contains no unintended recipient data, uses consistent placeholders, and has no obviously empty or duplicated slides. When browser rendering is available, visually inspect representative title, content, image, and closing slides for clipping or broken layout.

Return the complete editable `https://docs.google.com/presentation/...` URL in a fenced code block, followed by a concise list of reusable placeholders and any remaining example content.
