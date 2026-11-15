# Design system for research figures

## Recommended starting defaults (adapt to journal requirements)
- Width: target single-column or double-column width; validate against actual journal specification. Common useful working widths: 85 mm or 180 mm.
- Editable vector elements for text, connectors, legends, axis labels and diagrams.
- Typeface: a consistent accessible sans-serif, mathematics typeset with a glyph-complete font.
- Target final-size labels: typically 7–10 pt, larger for headings; verify actual legibility after insertion in paper.
- Stroke: usually ~0.5–1.25 pt at final size, adjusted by prominence. Use arrows only for genuine direction and flow.
- Prefer white or near-white backgrounds; dark enough text for print, and sufficient contrast in gray-scale.
- Example qualitative palette: blue #3979B7, orange #DF8A35, teal #369D95, magenta #AA6BA4, purple #7769AC, gray #5D6570. Adjust by tested series count and accessibility.
- Use solid/dashed/dotted strokes or marker shape to distinguish data series independently of color.

## Export tests
- Render SVG and PDF and inspect at 100% target size and as thumbnail.
- Check width/height in mm, fonts in PDF, math glyph integrity, arrows and crop positions.
- Check embedded imagery's effective DPI = pixel width / printed width in inches.
- Check for missing links or external dependencies in SVG.
- Verify all derived values, scales, statistical annotations and experimental conditions against the original sources.

## Editorial rules
- Show no new scientific claims, unobserved results or imagined data.
- Preserve visual evidence authenticity and denote schematics or synthetic examples appropriately.
- For statistical figures, maintain consistent meaning of errors (SD, SE, CI) and disclose confidence level.
- When source data is unavailable, improve existing figure layout conservatively and explicitly mark unreconstructed plots as such.
