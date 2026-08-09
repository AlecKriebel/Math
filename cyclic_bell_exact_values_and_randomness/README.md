# Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell Inequalities

Canonical source and verification package for the merged paper

> *Sharp operator bounds, equality structure, and limits of Bell-value
> randomness certification*

Author: Alec Kriebel, Independent Researcher

Version: 1.0, 8 August 2026

Status: unrefereed, AI-assisted research manuscript

## Main result

For the first reduced cyclic Bell operator introduced by Perito et al., the
finite-dimensional tensor-product, approximate, and commuting-operator values
are all

\[
2\csc\!\left(\frac{\pi}{2d}\right).
\]

The polar equality phases admit paired permutations that preserve all
Bell-visible first harmonics. Every such permutation gives exact admissible
maximizers of both relevant cyclic families. For every (d\ge4), an explicit
final-two swap has a nonuniform designated joint-output table, although its
local marginals are uniform. Therefore the maximum scalar Bell value alone
does not certify (2\log_2 d) global random bits across the whole maximizing
face. This does not dispute randomness certification conditioned on the
complete canonical behavior.

## One-command replay

From this directory:

```sh
./reproduce.sh
```

The wrapper runs dependency-free hostile regressions, two independent exact
four-outcome implementations, retained setting checks, all historical hash
manifests, the manuscript build, PDF metadata checks, and local website/link
validation. See `verification/README.md` for component commands and the
limits of computational evidence.

## Package map

- `main.tex` — canonical manuscript source.
- `output/pdf/cyclic_bell_exact_values_and_randomness.pdf` — built manuscript.
- `verification/` — unified tests and frozen verification report.
- `audit/` — fresh adversarial review, claims/dependency ledgers, current
  primary-source priority audit, and limitations.
- `review_packet/` — concise materials for focused specialist review.
- `MERGE_REPORT.md` — source-to-merged disposition.
- `CHANGELOG.md` — corrections, narrowed claims, and presentation changes.
- `manifest.sha256` — integrity manifest for the canonical package.

## Historical source packages

The source directories below remain unchanged and authoritative for their
standalone historical versions:

- `../cyclic_bell_tsirelson_bound/`
- `../cyclic_randomness_counterexample/`
- `../minimum_bell_randomness/`

Their public PDFs remain at their original website URLs. The former landing
pages are compatibility redirects that retain direct links to those PDFs,
immutable source snapshots, hashes, and publication history.

## Reuse and review boundary

The Bell-family definitions, canonical strategies, matching lower bounds,
and second-family SOS belong to the originating work and are cited as such.
The package claims no DOI, submission, endorsement, external review, or
collaboration. Internal adversarial review and passing code are not peer
review.
