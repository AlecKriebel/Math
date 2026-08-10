# Full-dimensional JC ambiguity in weakly tree-child level-2 networks

## Verified release status

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
The construction also does not settle the triangle-free weakly tree-child
subclass: its blob contains a triangle as well as failing strong
tree-childness.
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

The release command is:

```sh
python3 reproducibility/verify_release.py
```

It checks the release manifest before running two independent exact
implementations.  Build the manuscript with Tectonic:

```sh
reproducibility/build_paper.sh
```

The independent mathematical audit, final manuscript rereview, deterministic
archive checks, and clean-worktree replay are recorded in `AUDIT_REPORT.md`.
Journal-specific author metadata and formatting remain human submission
choices rather than mathematical release blockers.

Manuscript text and figures are licensed CC BY 4.0.  Code is MIT licensed.
