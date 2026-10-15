# Review history and v2 changes

## Original author freeze

The original 13-file tree and 19,163-byte archive are preserved unchanged. The archive SHA-256 is 6483242536c534a84072815ae4c3aa9de57fd2769386eb2e5e1ad85041cc6a01. Its manifest SHA-256 is 4869e62250a25e64fc6e4096ea56842a7b23400789f3ba00c14ba81c2c8cd8f7. `original_bindings.json` records every original file's hash and size.

The original proof's SHA-256 is eb96aab30ab17aca553ef83102145c5dd51b2c36895be2b2a028f5090b9aedc1. Its status was a proposed complete proof, not yet independently reviewed.

## First independent audit

Mathematics: PASS; no essential gap found. Exact original archive: PASS. Original verifier: REVISE_REQUIRED, because a nested extra file named MANIFEST.json was skipped by its basename filter. This was a reproducible tooling flaw, not a hidden mathematical objection. It was absent from the actual original archive.

The full report and finding are retained verbatim as `review/first_geometry_audit.md` and `review/original_integrity_finding.md`. The audit supplied a strict verifier, fourteen negative controls, and additional source-backed details. The v2 verifier is that exact strict implementation; its test suite is the audit's exact implementation under the v2 test filename.

## Second independent geometry audit

Mathematics: PASS; no essential gap found. The full report is retained verbatim as `review/second_geometry_audit.md`. It independently justified the fixed-point, arbitrary-characteristic moduli and Picard bridge and recommended four expository expansions.

## This derivative

The proof expands geometric-field minimality, replaces compressed coarse-fiber wording with the finite map to the full coarse scheme, makes projectivity of the universal curve explicit through the marking's relative degree-one bundle, and uses a generic-fiber closed point for numerical descent. Source references and their hypothesis matching are expanded. The theorem and the two-approach count are unchanged.

The original verifier is superseded. A direct regression retains the vulnerable code under `historical/` solely to show the old acceptance and new rejection of the demonstrated extra-file case. It must not be treated as an alternative authoritative verifier.

The first audit linked some Stacks results through section-level URLs; the revised proof links the exact propositions or lemmas (04SZ and 0EX7). The copied reports are historical records and have not been silently edited.

## Current limit

A final independent delta audit must check this v2 proof and tooling before publication. The two earlier PASS verdicts are not presented as approval of unseen changed bytes. None of these AI reviews is formal verification, external human peer review, acceptance by the mathematical community, or proof of historical novelty. Specialist review and a thorough priority search remain outstanding.
