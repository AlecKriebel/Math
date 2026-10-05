# Monotone gradient-distance continuity: audited partial results

Problem **30005995 / OWR-14298587-010**, queue rank **803**.

**UNSOLVED, 5/5 approaches completed.** The independent audit accepts this packet only as scoped partial results. It neither proves nor disproves the unrestricted continuity conjecture, and no novelty claim is made.

## What passed review

The frozen author report proves restricted propositions and a conditional blow-up theorem. The independent mathematical addendum supplies the strong local gradient and nonlinear flux compactness argument, preserves both universal quantifiers in the extra hypothesis, and proves continuity of an explicitly defined representative under the global extra hypothesis.

The conditional theorem requires **every blow-up at a singular point to be differentiable at every nonzero point**. Global continuity requires this condition at every singular point. Neither universal requirement has been established generally. The remaining gap is this blow-up regularity hypothesis or another PDE-specific no-spike estimate. The Sobolev spike is an obstruction to a generic inference; it is **not a PDE counterexample**.

## Read the artifacts

- `author/REPORT.md`: immutable original five-approach report.
- `audit/AUDIT.md` and `audit/MATHEMATICAL_ADDENDUM.md`: independent review and precise acceptance boundary. Read the addendum together with the original report.
- `RESULT.json`: machine-readable unresolved disposition.
- `audit/VERIFICATION_METADATA.json`: public source hashes, source inspection history, full-corpus identity and review-hash verification metadata. Four primary PDFs were independently retrieved and matched; their contents are excluded.
- `frozen_archives/`: both original immutable ZIPs, with hashes and sizes in `PUBLICATION_PROVENANCE.json`.
- `QUEUE_DELTA.json`: exact change to the target row's Status and Turns cells; all other queue bytes are preserved, including the existing header and Findings cells.
- `RESEARCH_LOG.md`: publication checkpoints, scope, and completion estimates.

## Reproduce locally

Python 3 standard library only. No network, credentials, PDFs, or corpus files are required.

    python -I -B verify_publication.py --replay --optimized-replay
    python -I -B test_publication_integrity.py

The verifier is independent of the working directory and also operates under optimized Python. It verifies exact recursive membership, all file hashes and sizes, both archive hashes and every archive member, and unchanged author copies. The two arithmetic suites reproduce **22,185 author checks and 40,249 independent checks**, including five symbolic polynomial identities. Explicit runtime checks remain active in optimized mode.

For an optional exact queue comparison, supply separately obtained snapshots from the recorded base and proposed head:

    python -I -B verify_publication.py --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/head-QUEUE.md

The optional `audit/verify_identity.py` accepts separately supplied full catalog, problems, and research-results files. Its source identity verification was independently performed before publication; routine self-contained replay does not repeat full-corpus or primary-document retrieval.

Finite computations are algebraic controls, not a formal verification of the analytic PDE theorem or of imported literature proofs. The bounded repository search found no prior matching attempt; the earlier audit's recursive-tree search was truncated, so absence throughout repository history is not certified.

The publication includes authored proofs, audit, code, results, and public verification metadata only. It contains no copied source PDFs, extracts, images, raw datasets, private sources, private personal data, or private coordination material. Historical statements that no remote writes were performed refer to the preparation or independent audit stage. This packet is prepared for a draft PR only, with no merge, release, DOI, or outreach.
