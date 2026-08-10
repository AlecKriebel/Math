# Full-dimensional JC ambiguity at the weak/strong tree-child boundary

## Release-candidate status

This is the replacement for the withdrawn version 1.1.1 positive-
classification release.  Its scope is intentionally narrower and matches the
theorem that survives exact adversarial review:

> For every `n >= 4`, two nonisomorphic and non-triangle-equivalent binary
> level-2 semi-directed networks in `W_TC \ S_TC` have open Jukes--Cantor
> model images with a common regular full-dimensional region of dimension
> `2n`.

The four-leaf common point is exact in a quadratic number field, lies strictly
inside the positive-definite JC domain `Theta_0`, agrees in all 256 Fourier
coordinates, and has nonzero rank-eight Jacobian minors on both models.  A
positive analytic inverse for identical cherry substitution proves the
all-taxa extension.

The former claim that all standard strongly tree-child level-2 JC networks
are identifiable modulo triangle redirection remains **unresolved, not
refuted**.  It is not asserted anywhere in the active manuscript or release.
The historical files are preserved under
`quarantine/withdrawn_positive_v1.1.1/` and must not be submitted or cited as
established.

## Active files

- `source/paper/main.tex` — canonical manuscript source
- `submission/` — generated submission PDF after the final release gate
- `reproducibility/` — primary and independent exact implementations
- `docs/PRIOR_WORK_COMPARISON.md` — version-locked literature audit
- `repair/` — forensic reports explaining why the old theorem was withdrawn

## Reproduce

The final release command will be:

```sh
python3 reproducibility/verify_release.py
```

It checks the release manifest before running two independent exact
implementations.  Build the manuscript with Tectonic:

```sh
reproducibility/build_paper.sh
```

Until `repair/FALLBACK_SUBMISSION_SCOPE.md` is marked verified and the
submission PDF is present, this branch remains a release candidate rather
than a publication release.

Manuscript text and figures are licensed CC BY 4.0.  Code is MIT licensed.
