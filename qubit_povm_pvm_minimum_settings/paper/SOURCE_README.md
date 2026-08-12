# Manuscript source — version 1.2.0

Build the standard, line-numbered, and one-column PRA PDFs with Tectonic
0.16.9:

```sh
./build.sh
```

The build treats LaTeX, BibTeX, undefined-reference, overfull, and underfull
warnings as errors. `main.tex` is the canonical manuscript; `review.tex` and
`pra.tex` are thin presentation wrappers. `abstract.tex`, `appendices.tex`,
and all figure source files are required. The PRA build uses the vendored
official REVTeX 4.2f runtime under `vendor/revtex-4.2f/`; `pra.bbl` is a
generated APS bibliography frozen with the source so ordinary PDF rebuilds
do not invoke BibTeX's known REVTeX control warning.

The article text, bibliography, and original figure code are CC BY 4.0.
`lineno.sty` is third-party material under the LPPL terms stated in that
file. REVTeX 4.2f is third-party LPPL 1.3c material; see its vendored notice.
See the top-level project license and AI-provenance statement in the full
reproducibility package.
