# Full-page visual QA

All six original authored PDF pages were rendered with Poppler 26.08.0, 100 dpi, PNG; each complete page was displayed through view_image and inspected. No UI, tab, or editor action was used. Exact commands/exits/raw stdout/stderr are in PDF_TOOL_BINDINGS.json and pdf_tool_*; image hashes and reproduced-image comparison are in PDF_REPRODUCTION_COMPARISON.json.

1. Title, author, ORCID, date, abstract, attribution section: balanced spacing, legible text, live-reference colors readable, no overlap or clipping.
2. Strict ellipse parameters, inversion/shoelace equation, theorem and star convention, beginning of flag curve: all subscripts, fractions and inequalities readable; equation (1) fits; footer separate from text. Paragraph continuation onto page 3 is ordinary.
3. Flag involutions, isotropic tangent equations and complete focal pole inventory: formulas and contact coordinates legible; no margin overrun; lowest paragraph clear of page number.
4. Odd-grid lemma and full pole-removal argument: dense but readable. Laurent coefficients and determinant signs are visible. Long paragraph continues normally to page 5; no clipping or footer collision.
5. Divisor conclusion, exact triangles, table, qualified source formula and same-caustic even controls: radicals, signs and table focus columns correctly rendered. Wide equations remain in margins; entire table visible; scaling paragraph legible.
6. Scope/access/chronology/AI-assistance statement, license and all eight references: dates, URLs, DOI suffixes and hanging references visible; long URL wraps without clipping; page numbering complete.

The read-only cached-resource untrusted Tectonic 0.16.9 build exited 0 without warnings matching Warning/Overfull/Underfull/undefined/Missing/Error in its complete saved log. All six independently rebuilt page PNGs are byte-identical to the original-page PNGs under the same renderer. Extracted authored text is also identical. PDF files themselves differ in bytes (the later build has a different digest); no deterministic PDF-byte claim is made. This is full-page visual QA of the authored six-page note, not visual certification of every third-party primary PDF.
