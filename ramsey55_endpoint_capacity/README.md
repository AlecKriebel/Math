# A transversal-capacity obstruction for a regular R(5,5) endpoint

Status: **provisional research note; not peer reviewed**.

This directory contains the manuscript for a narrow, catalog-conditional
result from the paused `R(5,5)` research program.

The reusable ingredient is a minimum-miss capacity profile for feasible
cross-neighborhoods. Applied to the regular degree-18 endpoint

    (e(A), e(H)) = (85, 128),

the resulting inequality excludes 61,939 of 62,382 fixed-side catalog pairs.
Equality rigidity excludes the remaining 443. Conditional on the published
catalog-completeness and extremal-edge statements, every vertex of a
hypothetical 18-regular `(5,5;43)`-graph lies in at most 84 triangles.

This result does **not** determine `R(5,5)`, improve the known bounds, close
the regular degree-18 branch, or prove the external catalog-completeness
claims.

## Paper and verification

- Manuscript source: [`ramsey55_endpoint_capacity.tex`](ramsey55_endpoint_capacity.tex)
- Rendered paper: [`output/pdf/ramsey55_endpoint_capacity.pdf`](output/pdf/ramsey55_endpoint_capacity.pdf)
- Claim-to-evidence map: [`MANIFEST.md`](MANIFEST.md)
- Priority and scope audit: [`PRIORITY_AUDIT.md`](PRIORITY_AUDIT.md)
- Compact verifier release:
  <https://github.com/AlecKriebel/Math/releases/tag/ramsey55-endpoint-capacity-v1.0.1>
- History-independent verifier source:
  <https://github.com/AlecKriebel/Math/tree/codex/ramsey55-endpoint-capacity-v1>

The release archive SHA-256 is

    de541d6c7ed8be496784397ea0ee3f1b12c2b93cdbc42ba908160095c1d79cc4

From the extracted verifier bundle, run:

```sh
python3 verify_bundle.py
```

The corrected v1.0.1 bundle is repeat-run safe after the documented direct
test commands. Its clean replay returned `valid=true`, reproduced every frozen
artifact byte-for-byte, and passed all 17 tests in under 70 seconds with peak
resident memory below 140 MB.

## Build the paper

Tectonic is required:

```sh
python3 render_paper.py
```

The output is written to `output/pdf/ramsey55_endpoint_capacity.pdf`.

## Authorship and warning

Author: Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI).

Alec Kriebel is a complete amateur and cannot independently validate the
mathematics. The manuscript and verifier are released for expert review.
Passing the checks is evidence about the encoded finite calculation; it is
not peer review and does not establish novelty or the external catalog
premises.
