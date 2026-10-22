# Bounded-polynomial partial sums: accepted partial results

Rank 1032 · problem 2304003 · AMR-022-4003 · unsolved · five mathematical approaches.

This source-free publication preserves the accepted author snapshot and independent audit unchanged. The author and audit records describe their historical preparation and inspection; their statements that publication had not occurred refer to those stages. The independent audit accepts the partial results without mandatory corrections. This is AI-assisted mathematical work, not a claim of human peer review, proof-assistant certification, exhaustive literature coverage, or novelty.

## Scope

- For an arbitrary N-term polynomial with increasing exponents and no degree bound, the sharp natural-prefix growth C_N remains unresolved here between log(N)/pi-O(1) and (1+sqrt(N))/2.
- For d consecutive coefficient slots, A(d,k)=log(min(k,d-k))/pi+O(1), uniformly for 1<=k<d; A(d,d)=1. No general exact two-parameter formula is claimed.
- The exact quadratic value is A(3,2)=2/sqrt(3), also valid for fixed arithmetic-progression triples of exponents. It is not asserted for every three-term support.
- Arbitrary-subset U_N has square-root order. Its scattered favorable signs generally do not form an increasing-exponent prefix.

The [report](accepted/original/public/REPORT.md) contains the complete partial proofs and exact remaining obstruction; the [independent mathematical audit](accepted/audit/public/MATHEMATICAL_AUDIT.md) checks their hypotheses and boundary cases. [Technau (2026)](https://doi.org/10.1017/fms.2026.10213) is credited for published degree-bounded results. Newman (1978) and the 1979 erratum are bibliographic attributions only: their original full texts were not inspected, and the erratum's exact correction is not established here.

## Reproducibility and trust

Obtain the SHA-256 pins for BOOTSTRAP.py, VERIFY_PUBLICATION.py and PUBLICATION_MANIFEST.json independently, such as from the reviewed PR description. A replaced packet cannot authenticate itself. After checking those pins with trusted tools, use a trusted Python 3.10+ interpreter:

    python3 -I -S -B BOOTSTRAP.py
    python3 -I -S -B -O BOOTSTRAP.py
    python3 -I -S -B -OO BOOTSTRAP.py

Full replay requires a nonroot account and an environment enforcing read-only permissions. It authenticates exact file and directory inventories, sizes, hashes, archive member types and bytes, and exact-type/finite JSON declarations before executing accepted code in a copied read-only tree. It actually attempts writes, isolates hostile import locations, and checks bytes and modes afterward. TEST_MUTATIONS.py exercises the outer trust boundary. --integrity-only skips mathematical execution and must not be represented as a full replay.

Each full invocation freshly reruns the author harness in normal/-O/-OO modes: 20 malformed cases and 10 tamper/manifest cases per mode. It also reruns the independent suite: 8,385 dense cuts and other exact identities once per invocation, 64 extra malformed cases and two valid parameter boundaries per mode. Outer-mode repetitions and read-only repetitions are repeated executions, not additional distinct mathematical cases. The preserved receipts are historical; returned fresh replay results are separate evidence. Deep nesting fails closed with nonzero exit and no success stdout but produces an unstructured RecursionError traceback. This diagnostic limitation is disclosed without changing accepted bytes.

The finite checks do not mechanize the analytic proofs, asymptotics, or infinite-family conclusions. Hashes authenticate a snapshot, not mathematical truth. Replay does not retrieve or inspect sources, rehash private datasets, or redo record joins: these default to NOT_RUN. Source and dataset hashes and inspection statements in accepted files remain historical provenance. No source PDFs, extracts, dataset contents, private sources, or private coordination payload are included. Zero GitHub checks or runs means CI NOT_RUN, not a pass.

[PUBLICATION_ALLOWLIST.json](PUBLICATION_ALLOWLIST.json) lists the exact 23 accepted files: 12 author archive members and its archive, nine audit archive members and its archive. The generic external audit instructions were inspected for public suitability before inclusion. The wrapper files are newly authored publication controls; they do not alter the accepted mathematics or count as new approaches.
