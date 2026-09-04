# Website brand extraction

Read this reference only when the user provides a website URL.

## What to inspect

Review the homepage and the most relevant product, service, case-study, and about pages. Inspect linked CSS and, when browser tooling permits, computed styles at representative desktop and mobile widths.

Extract a small evidence-based design system:

- primary, secondary, accent, background, surface, text, and muted colors;
- display and body font families, weights, scale, line height, and letter spacing;
- container widths, spacing rhythm, border radii, borders, shadows, and button treatment;
- recurring geometry, gradients, patterns, illustration or photography treatment;
- logo and other first-party assets that are suitable for the requested document;
- writing voice: terse or explanatory, technical or accessible, bold or restrained.

CSS custom properties, font declarations, repeated computed values, and reusable component classes are stronger signals than isolated decorative values. Prefer styles used in high-salience areas such as the header, hero, calls to action, and section headings.

## Turn evidence into direction

Summarize the findings as design tokens rather than copying the webpage:

```text
Color: ink #..., surface #..., accent #...
Type: display ..., body ...; fallback ...
Shape: ... px radius, ... px strokes
Layout: spacious/compact, asymmetric/grid-led
Motif: one recurring visual idea
Voice: three useful adjectives
```

The target Office application may not contain the site's web fonts or support every CSS effect. Choose metrically and stylistically compatible portable fonts, simplify effects, and retain the hierarchy and character. Do not download or embed fonts without appropriate rights.

## Assets and attribution

Prefer first-party assets hosted on the supplied domain. Confirm whether a logo is an SVG, raster image, CSS mask, or inline symbol before reuse. Ignore tracking pixels and incidental third-party assets. Preserve aspect ratios and do not recolor a logo unless its brand treatment clearly allows it.

Record the URLs used as design sources. If access is blocked or the CSS cannot be inspected, say so and derive the style from the visible page or the user's written direction instead.
