# Audited Ricci-flow PDE/ODE bridge

**Problem 30001006 / OWR-2045-003, rank 817: substantial partial result, UNSOLVED, 1/5 substantive approaches.**

For every integer n >= 4 and fixed real d > 0, the closed scalar/Weyl curvature cone

    K_d = {R : scal(R) >= d ||W(R)||_HS}

is preserved by the Hamilton ODE if and only if it is preserved under every smooth Ricci flow on every closed n-manifold throughout smooth existence. Every failure of ODE preservation is realized by a smooth initial metric on S^n satisfying the cone condition everywhere and violating it after a sufficiently short positive time. The norm is the Hilbert–Schmidt norm of the curvature operator on exterior two-forms.

The authored analytic proof was accepted by two independent analytic AI audits, with no mathematical correction required. The compact realization controls the analytic Cauchy problem and full metric 3-jet, the entire conformal gluing construction, the normal curvature-Laplacian component, and the nonsmooth scalar-zero boundary. These reviews are not human peer review or formal proof-assistant certification.

## Read the mathematics

1. [Full authored proof](author/APPROACH_1_PDE_REALIZATION.md)
2. [First full audit](audit/AUDIT_REPORT.md) and [explicit estimates and CK-jet supplement](audit/ESTIMATE_SUPPLEMENT.md)
3. [Second full analytic audit](second_audit/SECOND_ANALYTIC_AUDIT.md)
4. [Overlap, primary sources, and limitations](author/OVERLAP_AND_SOURCES.md)

The general high-dimensional classification, proposed threshold n_0 = 12, and global Weyl-cubic extrema remain unresolved here. The interval involving mu_n and beta_n is conditional here on the separate rank-815 algebraic criterion, which these two bridge audits do not re-audit. The rank-815 cone is the same algebraic family under c = 2n(n-1)/d^2; its five ODE approaches are prior work, not five new approaches for this target. The one new approach is the local-to-compact geometric converse. No theorem for arbitrary curvature cones or noncompact Ricci flows is claimed. No novelty, priority, exhaustive literature clearance, or general resolution is claimed.

## Immutable records and chronology

All 33 members of the three authenticated releases and their three ZIP archives are preserved byte-for-byte. The author release's pending-review fields and all releases' no-publication fields describe their historical snapshots. This guide separately records the two subsequent scoped acceptances and publication; it does not rewrite those snapshots.

The first audit's corpus replay remains historical NOT_RUN. The second audit's separately documented fresh full-corpus PASS is in [FRESH_CORPUS_VERIFICATION.json](second_audit/FRESH_CORPUS_VERIFICATION.json). Running this publication verifier does not redownload or replay external corpus files. The second audit's optional corpus verifier requires the user-supplied originals and is separate from portable package verification. The live aggregator page returned HTTP 403 in the earlier source work; full supplied records and the primary report, not an unread live page, support the statement comparison. Xu's published version-of-record body was not inspected; the source searches are bounded.

Only authored proof, audit, code, results, public citations, and public verification metadata are included. Source PDFs, extracts, rendered images, dataset contents, target-record contents, private sources, private personal data, and private coordination material are excluded.

## Reproduce

Python 3.10+ is required; validation used Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0. Install requirements.txt in your chosen environment. From any working directory, use an independently supplied SHA-256 anchor for PUBLICATION_MANIFEST.json:

    python3 -B /path/to/30001006/verify_publication.py --expected-manifest EXPECTED_SHA256
    python3 -O -B /path/to/30001006/verify_publication.py --expected-manifest EXPECTED_SHA256
    python3 -B /path/to/30001006/test_publication_integrity.py --expected-manifest EXPECTED_SHA256

Optionally add --queue /path/to/QUEUE.md to verify the exact publication queue bytes. --integrity-only checks bytes and scope without executing diagnostics. The external hash, verifier, interpreter, and dependencies must be trusted. Recomputing a manifest hash from an untrusted altered package does not authenticate it.

Full replay checks all member bytes and directory inventories, all archive/member bindings, all three diagnostic outputs in ordinary and optimized Python, and both original integrity harnesses. The publication harness additionally runs the complete verifier in ordinary, optimized, relocated, and relocated-optimized modes and rejects 32 actual corrupted copies. Finite and symbolic diagnostics supplement the analytic proof; they do not certify CK existence, geometric gluing, or global curvature inequalities. See PUBLICATION_TEST_RESULTS.json for the actual replay record.

## Repository boundary

Only this attempt directory is added. In QUEUE.md, only this target's Status changes from queued to unsolved and Turns from 0/5 to 1/5. Findings, Chat, DOI, all other rows, and every other queue byte, including the pre-existing embedded header, are preserved. No queue regeneration is performed. Fresh main and bounded exact-ID/code/commit/PR checks are recorded in PUBLICATION_METADATA.json.

This is a draft research publication. No merge, release, DOI creation, or external outreach is part of it. Local and remote replay success are distinct from GitHub CI: zero reported checks is absence of CI evidence, not a CI pass.
