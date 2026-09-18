---
name: branded-template-generator
description: Derive a visual system from a website or style brief and generate reusable, branded templates as local DOCX, PPTX, or XLSX files, optionally uploading the confirmed result to Google Drive through Templify MCP. Use for editable proposals, reports, briefs, plans, presentations, and spreadsheet models; do not use for filling a template for a specific recipient.
---

# Templify Branded Template Generator

Turn a website or style brief and a content brief into a reusable branded template saved on the local filesystem. The required output is an editable Office Open XML file plus a personalization manifest:

- `.pptx` for visual, presenter-led material;
- `.docx` for detailed, asynchronously reviewed material;
- `.xlsx` for models, trackers, plans, and other editable structured data.

Do not connect to Google, upload, publish, email, or share the result unless the user explicitly requests the optional MCP handoff after generation. A later workflow may import the local file elsewhere.

## Establish the brief

Collect the output format, purpose, audience, offer, source material, website or style direction, language, tone, length, title, reusable sections, and local destination. Do not make the user repeat known information, but do not silently choose missing or ambiguous requirements.

Before researching or generating, present a short brief for confirmation. It must state:

- the selected format: DOCX, PPTX, or XLSX;
- the proposed structure and approximate length;
- the style source;
- the exact output directory.

Make clarification and confirmation messages visually scannable with Markdown and colored emoji markers. Custom HTML/CSS colors and ANSI escape codes are not portable across Codex and Claude, so do not use them. Use this compact pattern:

```markdown
## 🔵 Template brief

- **Format:** DOCX
- **Structure:** Cover + 5 body sections
- **Style source:** https://example.com
- **Output:** `./outputs/example-report/`

## 🟠 Confirmation needed

Should I proceed with this setup?
```

Use `🔵` for the proposed brief, `🟠` for a decision the user must make, and `📁` when emphasizing an output location. Keep the markers restrained and never rely on color alone: always include a textual heading or label.

If the user has not explicitly selected a format, ask which format they want and wait for the answer. Never default to PPTX or infer the format from words such as "template," "proposal," "report," or "presentation." If another material requirement is missing or ambiguous, propose a sensible option and ask the user to confirm it. Begin generation only after the brief is sufficiently defined and the user has confirmed it.

For the destination, use the path supplied by the user. If none is supplied, propose `<current-working-directory>/outputs/<project-slug>/` and ask for confirmation. Interpret `<current-working-directory>` at runtime; never replace it in the published skill with the author's absolute path.

Never invent results, testimonials, prices, dates, biographies, or statistics. Clearly label estimates, examples, and placeholders.

## Derive the visual system

When a website URL is supplied, inspect relevant public pages and stylesheets using the browsing capability available in the current runtime. Read [references/website-brand-extraction.md](references/website-brand-extraction.md). Use the site as visual inspiration rather than making a pixel-for-pixel clone. Do not bypass access restrictions.

Translate the evidence into a compact system of colors, typography roles and fallbacks, spacing, shapes, imagery, charts, and voice. Preserve readable contrast. Use first-party assets only when their use is appropriate; otherwise create original shapes, SVGs, or diagrams.

## Define the reusable contract

Read [references/personalization-contract.md](references/personalization-contract.md). Define reusable fields and repeatable or optional sections before laying out the file. Keep recipient-specific values as stable `{{snake_case_placeholders}}`; keep permanent labels and brand copy as normal text.

Every placeholder in the artifact must map to exactly one manifest field. Save the manifest beside the artifact as `<artifact-basename>.manifest.json`.

## Design the template structure

Plan the information architecture before rendering. Choose sections and layouts that fit the requested template type. For example, a proposal may move from context to approach and next action; a report may move from summary to findings and recommendations; a plan may move from objectives to workstreams, timing, ownership, and measures. Do not impose proposal sections on other template types.

Every DOCX template must begin with a dedicated, full-page cover. Read [references/docx-cover-design.md](references/docx-cover-design.md) for the cover composition pattern: a strong full-bleed visual field, high-contrast title block, restrained accent rule, subtitle, and lower metadata area. Translate that pattern into the brand system derived for the brief; do not copy another brand's colors, logo, wording, or exact artwork. Adding the cover must not force a different body structure or visual direction: preserve the architecture selected for the brief and treat the cover as an opening layer.

Read the selected section in [references/format-guides.md](references/format-guides.md). Maintain one central message per slide or section, distinguish facts from assumptions, and cite external facts with readable links or notes.

Generate the requested file using document-generation capabilities available in the runtime. Suitable implementations include OOXML libraries, office-document tools, or a compatible office suite. Dependencies must be installed only in a project-local or temporary location; never require global installation. Do not rely on the skill author's home directory, browser profile, credentials, fonts, fixed absolute paths, or files outside this skill and the user's stated inputs.

Create the confirmed output directory when needed. Save both files there with the same basename:

```text
<confirmed-output-directory>/<template-name>.<docx|pptx|xlsx>
<confirmed-output-directory>/<template-name>.manifest.json
```

Tell the user this exact destination before generation and return clickable paths to both files afterward. Use a descriptive filename and never overwrite an existing file unless the user explicitly authorizes it. If the preferred web font is unavailable, use a documented portable fallback. Embed or package required images so the artifact does not depend on temporary URLs.

Creating only Markdown, HTML, JSON, screenshots, or a design specification does not satisfy the request. If this runtime truly cannot create the requested OOXML format, explain the missing capability instead of claiming completion.

## Validate and hand off

Before returning:

1. Confirm the artifact and manifest exist in the requested local directory.
2. Open or parse the OOXML package and confirm it is structurally valid.
3. Render or inspect every page, slide, or relevant worksheet when the runtime supports it; check clipping, overflow, broken images, inconsistent spacing, formulas, and unreadable contrast.
4. For DOCX, confirm page one is a standalone cover and body content starts after an explicit page or section break. Check that the title, subtitle, metadata, contrast, and any artwork remain inside the page bounds and render correctly without remote font or image dependencies.
5. Confirm all `{{...}}` tokens are valid and mapped exactly once in the manifest.
6. Exercise one representative long value and one omitted optional value in a disposable copy, then leave the delivered template pristine.

Return clickable local paths for the artifact and manifest, the selected format, a concise description of the design and optional sections, and any assumptions or validation limitations.

## Optional Google handoff

Only when the user explicitly asks to upload the generated artifact, read the confirmed Office file as base64 and call `upload_google_file` with its filename and the exact Office MIME type. Never upload the manifest. Return the resulting editable Google file URL and ID. This upload is separate from proposal personalization: do not edit any source template. When the user has already explicitly requested deployment, do not add another confirmation step before publishing or deploying the uploaded file.

For installation, packaging, and behavioral tests of this skill itself, read [references/distribution-and-testing.md](references/distribution-and-testing.md).
