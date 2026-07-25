# Paper B: fixed-compression LP(333) shell descent and norm gates

This directory contains the standalone research manuscript
`manuscript.tex` and its compiled `manuscript.pdf`.

The paper is deliberately scoped to the prescribed \(p=37,q=3\)
\(q^2\)-compression chart inside the public-open order-three common
multiplier subgroup ID3, \(\langle10\rangle\). It does not claim a Legendre
pair of length 333, a Hadamard matrix of order 668, a classification of the
full ID3 family, or a classification of unrestricted Legendre pairs.

## Build

From this directory, either of the following commands should work:

```sh
tectonic manuscript.tex
```

or, with a conventional TeX Live installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The checked build used Tectonic. To remove conventional LaTeX intermediate
files while retaining the source and PDF:

```sh
latexmk -c
```

## Read first

- The date is 25 July 2026 and the manuscript is explicitly not peer
  reviewed.
- The authorship and AI-assistance disclaimers are part of the manuscript.
- The July 2026 overlap audit is incorporated: Ramos--Hulak--de Queiroz
  prove that a common fixed multiplier subgroup has order at most six, but
  explicitly leave ID3 \(\langle10\rangle\) open. This manuscript is
  narrower because it additionally fixes the length-37 compression.
- The \(n_9=1\) compressed-profile shell remains open.
- The dense eighteen-orbit exhaustiveness claim uses released production
  provenance. The checkpoint includes the manifest, strict aggregate, all
  729 completed shard records, the pinned helper, and the relevant sources.
  Its strict aggregator reproduces the aggregate without rerunning the
  expensive producer; the detached verifier replays every retained profile
  and orbit.
- The zero order-28,057 count in the exact nine-trit slices is not a profile
  exclusion. It is the expected behavior of a slice that small.

## Reproducibility

Run verification programs from the repository's
`hadamard_668_search/` directory. Section 10 of the manuscript maps every
theorem to its note, certificate, and replay entry point. The most important
artifact directories are:

- `shell_two_exact/`
- `shell_three_mod27/`
- `dense_shell_h0_complete_classification/`
- `h0_new_orbits_lift_triage/`
- `shell_two_physical_margin_lift/`
- `lp333_shell_two_primitive_units/`
- `lp333_shell_two_pair_resultant_norm/`
- `lp333_shell_two_pair_resultant_slices/`

Several full enumerators are intentionally expensive. Read each adjacent
`README.md` or `REPRODUCE.md` before running it. The lightweight detached
certificate verifiers are the appropriate first pass.

The complete immutable checkpoint is:

<https://github.com/AlecKriebel/Math/releases/tag/h668-research-checkpoint-v1.0.0>

The dense production record is the release asset
`../../output/releases/h668-dense-shell-production-v2-v1.0.0.tar.gz`,
with SHA-256
`493f73884ff5b5454f179b7754c0207178eeb70c70c27750daa610f3bda6c2df`.
The adjacent `../../output/releases/README.md` gives a fresh-directory
no-search replay that validates all 729 shards and reproduces aggregate
SHA-256
`3bccde87f456bfcd2f0c3da6ac8cf9cb3635538e831a95951003068ae87cae86`.

## Visual verification

The compiled PDF is rendered to page images during manuscript QA. The
release check is:

```sh
pdfinfo manuscript.pdf
mkdir -p tmp/pdfs
pdftoppm -png -r 120 manuscript.pdf tmp/pdfs/manuscript
```

Inspect the rendered pages for clipped tables, overfull lines, malformed
symbols, and broken URLs. The `tmp/` directory is disposable and is not a
research artifact.
