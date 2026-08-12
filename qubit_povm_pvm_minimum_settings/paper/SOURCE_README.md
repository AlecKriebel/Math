# Manuscript source — version 1.2.0

Build the standard and line-numbered PDFs with Tectonic 0.16.9:

```sh
./build.sh
```

The build treats LaTeX, BibTeX, undefined-reference, overfull, and underfull
warnings as errors. `main.tex` is the canonical manuscript; `review.tex`
defines the line-numbered build. `appendices.tex` and all figure source files
are required.

The article text, bibliography, and original figure code are CC BY 4.0.
`lineno.sty` is third-party material under the LPPL terms stated in that
file. See the top-level project license and AI-provenance statement in the
full reproducibility package.
