# Consistent conical bicombings: audited partial results

Problem 30004730 (OWR-8415335-002), rank 783. **UNSOLVED, 5/5 approaches.**

The original question concerns arbitrary metric spaces admitting a conical bicombing, with no completeness assumption. The independent audit passes the scoped partial results and requests no mathematical edits. This is AI-assisted, unrefereed work; no novelty, acceptance, formal-certification or full-resolution claim is made.

## What is established

- An explicit reversible conical tent bicombing shows that naive midpoint subdivision need not enforce consistency. Its space still has a linear consistent bicombing.
- Finite harmonic midpoint strings on complete spaces have a quantitative weighted contraction proof and exact cross-mesh restriction identity.
- Whole-sequence pointwise convergence of the meshes is a sufficient condition for a consistent conical limit. The missing unconditional cross-mesh convergence is not proved.
- A symmetric conical medial midpoint operation on a complete space suffices, but mediality is an extra hypothesis.
- Completion extension and elementary affirmative subclasses are proved. A replacement bicombing on the completion need not preserve the original space.

Proper-space straightness and equal-length convexity do not establish unrestricted conicality. Fixed-mesh contraction is not a cross-mesh convergence estimate, and arbitrary subsequential convergence does not meet the stated sufficient criterion.

## Preserved records and mandatory supplement

Read [author/REPORT.md](author/REPORT.md), [audit/AUDIT.md](audit/AUDIT.md), and [audit/CORRECTIONS.md](audit/CORRECTIONS.md). The original archives and all their extracted files are byte-preserved. Historical author labels saying that an audit is pending remain frozen; the completed independent audit is alongside them.

[METADATA_ADDENDUM.json](METADATA_ADDENDUM.json) supplies the independently reconstructed review hash and preserves the Danielski source-date discrepancy: the versioned HTML header gives 11 May 2025 while its internal manuscript date is 24 August 2026. No single reconciled date is inferred.

## Reproduce

From this folder, run:

    python3 verify_publication.py --queue ../../QUEUE.md

This checks the complete recursive file and directory inventory, original ZIP bytes and member bytes, both frozen manifests, exact queue two-cell preservation, and fresh author/independent finite regressions. Child Python runs explicitly enable assertions even if the wrapper is invoked with optimization enabled. The included provenance checker verifies the supplied author archive; full external corpus/PDF provenance is explicitly NOT_RUN because those inputs are not bundled. Historical successful provenance results remain labeled as audit history, not as freshly replayed external checks.

Only this problem's queue Status and Turns change. Every other queue byte, including existing findings and the stale header, is preserved. No queue regeneration, state-ledger changes, release, merge, DOI or outreach is part of this packet.

The package contains authored exposition/code/results, safe original archives and public verification metadata. Source PDFs, extracts, screenshots, raw corpora and private coordination material are excluded.
