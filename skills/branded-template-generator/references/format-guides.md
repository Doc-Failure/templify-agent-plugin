# Local OOXML format guides

Read only the section for the selected output format.

## PowerPoint (`.pptx`)

Use PowerPoint for visual, presenter-led narratives. Establish a small layout family appropriate to the requested content, such as cover, divider, statement, text-and-visual, data, comparison, process, summary, and close. Use only layouts the story needs.

- Design for scanning, with one message per slide and restrained copy.
- Use consistent grids, alignment, margins, and whitespace.
- Keep content inside safe areas and inspect the rendered deck at presentation size.
- Prefer editable native shapes, text, tables, and charts over flattened screenshots.
- Add concise speaker notes only when supported and useful.
- Use 16:9 unless the brief requires another size.

## Word (`.docx`)

Use Word for detailed reports, proposals, briefs, plans, statements of work, and asynchronous review.

- Use A4 or Letter according to locale or brief and record the choice in the manifest.
- Always make page one a dedicated, full-page cover, followed by an explicit page or section break. The proposal body begins on page two.
- The cover should include the document title, relevant organization or audience placeholders, and an optional date, subtitle, or short positioning line when appropriate. Use the derived visual system to make it feel intentional; do not turn it into a dense summary page.
- Keep body headers, footers, and page numbering off the cover when the document-generation library supports a different first page or first section.
- Build a body hierarchy appropriate to the requested document type. Do not replace or reshape a user-preferred structure merely to accommodate the cover.
- Define document styles rather than formatting every paragraph independently.
- Use intentional page and section breaks; minimize orphan headings and split tables.
- Use restrained callouts, tables, diagrams, headers, and footers to create rhythm.
- Include scope, responsibilities, assumptions, exclusions, timing, pricing, findings, recommendations, or approval language only when relevant, without inventing terms.
- Add a table of contents only when length warrants it.

## Excel (`.xlsx`)

Use Excel for models, estimates, roadmaps, KPI plans, trackers, comparisons, inventories, and templates whose assumptions or structured data should remain editable.

- Separate inputs, calculations, outputs, and notes; use distinct worksheets when helpful.
- Keep formulas live and reference input cells instead of duplicating constants.
- Use named ranges, frozen headers, validation, sensible formats, and protected formula regions when supported.
- Provide an executive-summary worksheet with totals, decisions, and next actions.
- Use charts only for decision-relevant patterns; label illustrative figures and cite sourced data.
- Include assumptions, units, currency, tax, and date basis.
- Recalculate or inspect formulas and test at least one changed-input scenario.
