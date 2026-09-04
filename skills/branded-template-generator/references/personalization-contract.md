# Personalization contract

Use this contract for every generated template so a later skill can personalize it consistently across PPTX, DOCX, and XLSX files.

## Placeholder syntax

Use readable, namespaced tokens:

```text
{{recipient_company_name}}
{{recipient_contact_name}}
{{document_title}}
{{document_summary}}
{{offer_primary_outcome}}
{{commercial_currency}}
{{commercial_total_price}}
{{timeline_start_date}}
{{sender_company_name}}
```

Placeholder keys use lowercase `snake_case`, may contain only letters, digits, underscores, and hyphens, and must be no more than 64 characters. Prefix keys with their semantic group, such as `recipient_`, `proposal_`, or `commercial_`. This matches Templify's current parser. Reuse the exact same token when the same value appears more than once. Do not encode formatting, slide numbers, cell addresses, or business logic in a key.

Manifest field IDs may use dotted semantic names for future automation, but each field must include the exact Templify-compatible `placeholder` key used in the file.

For optional content, keep the placeholder inside a removable section rather than embedding conditional syntax in recipient-facing copy. For lists and tables, use one clearly marked prototype item or row and describe repetition in the manifest.

## Required manifest

Save the manifest beside the exported artifact as `<artifact-basename>.manifest.json`.

```json
{
  "schema_version": "1.0",
  "template": {
    "title": "Branded template title",
    "format": "pptx",
    "source_url": "https://example.com",
    "locale": "en-US"
  },
  "fields": [
    {
      "id": "recipient.company_name",
      "placeholder": "recipient_company_name",
      "type": "short_text",
      "required": true,
      "description": "Recipient's public company name",
      "example": "Northstar Labs"
    }
  ],
  "sections": [
    {
      "id": "case_studies",
      "optional": true,
      "repeatable": true,
      "description": "Relevant proof selected for the recipient"
    }
  ],
  "style": {
    "source_urls": ["https://example.com"],
    "notes": "Short description of the derived visual system"
  }
}
```

Allowed field types are `short_text`, `long_text`, `number`, `currency`, `percentage`, `date`, `url`, `image`, `boolean`, and `list`. Add `format`, `validation`, or `fallback` properties only when they change downstream behavior.

## Format-specific placement

### PowerPoint

Place tokens directly in text shapes and table cells. Give optional or repeatable slides a stable section ID in speaker notes, such as `template-section: case_studies`. Avoid splitting one token across styled text runs. For image replacement, put the same token in the image description/alt-description through Templify's image-placeholder workflow.

### Word

Place tokens as contiguous text. Label optional or repeatable blocks with a short authoring note or bookmark when tooling supports it. Keep table-row prototypes intact and identify their section ID in the manifest. For image replacement, use Templify's image-placeholder workflow rather than visible token text.

### Excel

Place input tokens in dedicated input cells and use formulas elsewhere. Prefer named ranges matching placeholder keys, such as `recipient_company_name`. Record important named ranges or sheet names in an optional `locations` object on the field. Never put tokens inside formulas. For image replacement, use Templify's image-placeholder workflow rather than a formula.

## Validation before handoff

- Search the artifact for `{{` and confirm every unique token is well formed, no more than 64 characters, and mapped by exactly one manifest field.
- Confirm repeated uses of a value share one field ID.
- Confirm sample data, comments, and hidden sheets contain no accidental client information.
- Exercise one representative long value and one missing optional value, then restore the pristine template.
- Confirm personalization can change content without moving or restyling unrelated elements.
