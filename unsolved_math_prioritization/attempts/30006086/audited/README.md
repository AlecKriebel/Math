# Audited loop-invariant partial results

Problem 30006086 / OWR-14298797-002. Status: **unsolved, 5/5**.

Independent audit: **accepted as scoped partial results; no author correction required**. Read `audit/AUDIT_REPORT.md` for the full claim-by-claim review and limitations. The unrestricted generator conjecture and general geometric equivalence problem remain unresolved. This is AI-assisted research, not human peer review or formal proof-assistant certification.

`author/` preserves all nine original frozen files. `AUTHOR_PACKET.zip` preserves the original archive. Author statements that independent review was pending belong to that original freeze; `audit/ACCEPTANCE.json` and the report give the later audit disposition.

## Verify the artifact

Python 3.11 or later, standard library only, no network:

    python3 -B VERIFY_AUDIT.py

This checks every sealed file hash, the original author freeze/archive, byte-identical saved author replay, all 109 independent rank results, 2,137 author controls, and 319 supplemental controls. It verifies saved evidence and integrity; it does not rerun expensive algebra.

## Recompute

    python3 -B author/verify.py > author-replay.json
    python3 -B audit/independent_rank_audit.py
    python3 -B audit/supplemental_controls.py > supplemental-replay.json

The independent rank script prints progress and writes `audit/INDEPENDENT_RANK_REPLAY.json`. The existing `INDEPENDENT_RANK_RESULTS.json` stays untouched. All ranks use exact rational-equivalent arithmetic. Optimized Python (`-O`) is deliberately rejected. The written all-degree proofs require mathematical review and are not consequences of a finite test suite.

The independent full-rank calculation and author replay were completed before the audit was recovered; their finished output was checked rather than needlessly repeated. The supplemental suite and packaging controls were freshly run during completion. See the report for the independent algorithms and exact recovery scope.

No source text/PDFs, dataset contents, or private coordination records are included. Public verification/source metadata and authored work are included. No publication or repository changes were performed by this audit.
