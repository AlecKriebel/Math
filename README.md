# Regular degree-18 endpoint-capacity verifier

This is a self-contained, standard-library-only verification bundle for the
catalog-conditional exclusion of the regular degree-18 endpoint

\[
(e(A),e(H))=(85,128)
\]

in a hypothetical \((5,5;43)\)-graph.

The mathematical statement and proof are in `THEOREM.md`. The focused
prior-art assessment is in `NOVELTY_REVIEW.md`.

## Result

The bundle checks all \(74\cdot843=62,382\) fixed-side catalog pairs:

- 61,939 violate the transversal-capacity inequality strictly;
- 443 attain equality and are eliminated by the unique-minimizer
  high--high-edge contradiction;
- zero pairs remain.

The conclusion is conditional on the completeness and nonisomorphism of the
published \(R(4,5;18)\) and \(R(4,5;24)\) catalogs. The bundle verifies the
exact supplied bytes and every finite calculation; it does not independently
repeat the original catalog enumeration.

## Requirements

- Python 3.10 or newer;
- no third-party Python packages;
- about 150 MB available memory;
- about one minute on a modern laptop.

## Verify

From this directory, run:

```sh
python3 verify_bundle.py
```

The launcher first verifies every file bound by `BUNDLE_MANIFEST.json`, then
runs the independently written checker and all 17 focused tests. Success ends
with a JSON object containing `"valid": true`.

For the two phases separately:

```sh
python3 verify/branch18_regular_endpoint_capacity_cover_check.py --root .
python3 -m unittest tests/branch18_regular_endpoint_capacity_cover_tests.py
```

To regenerate the classification and compact claim manifest before checking:

```sh
python3 src/branch18_regular_endpoint_capacity_cover.py --root .
python3 verify/branch18_regular_endpoint_capacity_cover_check.py --root .
```

Regeneration is deterministic and invokes no SAT solver.

To build a deterministic, metadata-normalized archive outside this directory:

```sh
python3 make_archive.py ../branch18_regular_endpoint_capacity_v1.tar.gz
```

## Provenance

This release was extracted from local research checkpoint
`b14f50dd3b048b2d0e51e6aabd63bb608662f053`. The release deliberately carries
no multi-gigabyte proof history. It contains only the theorem, novelty audit,
two pinned source catalogs, producer, independent checker, tests,
classification stream, and compact manifests.

The original catalog source and data-license attribution are recorded in
`DATA_PROVENANCE.md`.

## Scope

This bundle does not prove that \(R(5,5)=43\), does not improve
\(43\le R(5,5)\le46\), and does not close the regular degree-18 branch. It
excludes one endpoint layer.
