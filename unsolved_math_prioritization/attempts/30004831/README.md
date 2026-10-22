# Hopf cohomological dimension: credited existing negative answer

Problem **30004831 / OWR-8415347-009**, rank 784. **already_solved; 0/5 new research attempts.** The unrestricted question has a negative answer, credited to **Ruipeng Zhu, Example 4.11**. The order-two reconstruction gives monoidally equivalent Hopf algebras with cohomological dimensions **1 and infinity**.

## Scope and attribution

The original question imposes no both-finite, smoothness, or cosemisimplicity assumption. This example does not contradict results requiring both global dimensions finite, both algebras homologically smooth, or cosemisimplicity. Global dimension, Hochschild dimension and projective dimension of the trivial module are the invariant here; trivial-module self-Ext alone is not enough. Read `audit/DIMENSION_CONVENTIONS.md` for the distinction.

The authored proof supplies an explicitly checked bi-Galois object and elementary dimension arguments. Its categorical input is the standard Schauenburg bi-Galois theorem as inspected in Bichon 2022. This is a reconstruction of known mathematics, with an independent AI-assisted audit, not a new solution, formal verification, human peer review, or editorial acceptance claim.

## Immutable evidence and current disposition

- `author/`: exact eleven-file author freeze.
- `audit/`: exact twenty-two-file independent-audit freeze, including its own unchanged author copy. The current mathematical verdict is PASS in `audit/AUDIT.md` and `audit/AUDIT_RESULT.json`.
- `frozen_archives/`: canonical base64 encodings of both original ZIP byte streams. Decode with Python's standard-library base64 module to recover the ZIP files. Every member is checked against its preserved directory.
- The separate `HOPF_30004831_REVIEW_HASH_SUPPLEMENT_RECEIPT.json` independently recomputes the full-record review hash. It supersedes only the earlier audit's limited statement that this hash was merely extracted. All frozen files, including historical audit-pending or extracted-only claims, remain unchanged.
- `PUBLICATION_PROVENANCE.json`: fresh immutable-main binding, complete cached-data hashing and full-record review-hash recomputation; no source records are distributed.

## Source qualifications

The inspected Zhu arXiv v2 has a left-coproduct/left-coaction orientation mismatch and an inclusive normal-basis endpoint that cannot be used literally. Both cautions and the consistent order-two correction remain explicit in the proof and audit. The final journal PDF was not inspected; no assertion is made about its exact displays or an erratum. Publication metadata identifies Zhu's article in J. Pure Appl. Algebra 229(12), article 108123 (2025). Bichon's 2026 finite-case work is reported as a preprint.

Primary references: [Zhu v2](https://arxiv.org/abs/2501.02828v2), [journal DOI](https://doi.org/10.1016/j.jpaa.2025.108123), [Bichon 2022](https://www.numdam.org/articles/10.5802/crmath.329/), [Bichon 2026 v1](https://arxiv.org/abs/2602.12731v1), [original report](https://publications.mfo.de/handle/mfo/3899).

## Portable verification

Python 3.10+, standard library only, no network or external inputs:

    python3 /path/to/packet/verify_publication.py --expected-manifest <publication manifest SHA-256>
    python3 /path/to/packet/test_publication_integrity.py

The verifier rejects optimized Python, validates exact recursive inventory, both ZIP streams and all frozen manifest/member bytes, checks the later supplement pin, then replays **4,543 author assertions, 2,902 independent assertions, and 14 frozen integrity controls**. The independent count includes **313 deliberately false variants**. Both mathematical result files must reproduce byte-for-byte. Publication-specific mutation tests run separately. Finite checks support the written proof and do not certify its unbounded or categorical arguments.

Optional `--queue-before` and `--queue-after` paths check the complete queue bytes and exact permitted patch. Full dataset hashing and primary-source inspection are historical provenance stages; they are not silently replayed by the standalone verifier without those external inputs.

## Repository scope

Only this target's queue Status and Findings are changed. Turns remains 0/5; every other byte, including the stale literal header, is preserved. No historical catalog, assessments, state, other target, release, DOI, merge, or outreach is changed by this draft.
