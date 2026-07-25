# Semiregular \(C_{37}\) conference paper

This folder contains the standalone manuscript:

- `manuscript.tex` -- LaTeX source;
- `manuscript.pdf` -- compiled provisional paper;
- `z37_quotient_census_canonical_625.txt` -- enumerator output containing
  all 625 canonical upper triangles and the census summaries;
- `z37_quotient_census_canonical_625.sha256` -- digest sidecar for that
  certificate; and
- `verify_package.py` -- dependency-free structural and digest check.

The paper is deliberately scoped to the promoted results in
`hadamard_668_search/conference_334_z37_lift/`. It does not claim a
conference graph, a conference matrix, a modulo-four lift, or a Hadamard
matrix of order 668, and it does not claim nonexistence in either the
semiregular lane or the unrestricted conference-graph problem.

## Build

From this folder, either of the following works:

```sh
tectonic manuscript.tex
```

or, with a conventional TeX installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The source uses an inline bibliography, so no BibTeX pass is required.
All paths in the manuscript and commands below are repository-relative;
the package checker resolves its data relative to its own location and can
therefore be invoked from any working directory.

## Package certificate

From the repository root:

```sh
python3 \
  hadamard_668_search/papers/semiregular_c37_conference/verify_package.py
```

The expected canonical-dump SHA-256 is:

```text
c5d8765da49deb39c2ff3407b9d0f265e3ca56c1015d5b0075355c53ca60fb5b
```

The checker verifies the digest, the 625 sequential canonical records,
the quotient square and row-sum equations, the summary counts, uniqueness
of the records, and the absence of an all-zero quotient diagonal.

## Render check

With Poppler installed:

```sh
mkdir -p /tmp/semiregular-c37-render
pdftoppm -png -r 130 manuscript.pdf \
  /tmp/semiregular-c37-render/page
pdfinfo manuscript.pdf
```

Inspect every rendered page for clipped equations, broken tables, and
overfull code blocks.

## Mathematical replay

The paper's Section 11 maps every claim to a promoted verifier or
certificate. The quickest aggregate checks, run from the repository root,
are:

```sh
python3 hadamard_668_search/conference_334_z37_lift/verify_z37_lift_frontier.py
python3 hadamard_668_search/conference_334_z37_lift/verify_rank_two_conjugation_obstruction.py
python3 hadamard_668_search/conference_334_z37_lift/verify_rank_two_jordan_obstruction.py
python3 hadamard_668_search/conference_334_z37_lift/char2_support_realization/verify_all_char2_support.py
python3 hadamard_668_search/conference_334_z37_lift/first_nonconstant_conjugator/verify_first_nonconstant_gauge.py
python3 hadamard_668_search/conference_334_z37_lift/first_nonconstant_conjugator/verify_exceptional_plane_fixed_j.py
```

The exhaustive 625-class quotient census and the five-minute
constant-rank-three audit have separate reproduction commands in the
manuscript.

## Archival location

The immutable companion release is:

<https://github.com/AlecKriebel/Math/releases/tag/h668-research-checkpoint-v1.0.0>

## Draft status

The named author is Alec Kriebel, with heavy ChatGPT 5.6 Sol assistance
disclosed on the title page and in the manuscript. Before any submission,
the author should:

1. add final affiliation and contact metadata;
2. obtain human review of the orderly-enumeration argument;
3. broaden the literature audit beyond the public-source review;
4. decide whether to include the full machine-readable certificates as
   supplementary material; and
5. retain the explicit AI-assistance statement.
