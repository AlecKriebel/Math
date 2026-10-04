# Publication scope: read before interpreting any status label

**Audited disposition: literature-known unrestricted non-isentropic full-Euler existence, only.**

This note is the current publication-level interpretation and supersedes any ambiguous or pending status wording in the unchanged historical author files.

The catalogue's literal existential formulation admits a smooth eternal full-Euler Gaussian solution in odd dimension, already published by Fellner and Schmeiser (2007). Its finite positive mass and energy are verified in [PROOF.md](PROOF.md). Its specific entropy is spatially unbounded.

The independent [audit](audit/AUDIT.md) passed the mathematics, direct prior-art mapping, and this qualified source interpretation. It approved the queue status **already_solved, 1/5** only with this qualification. This is not a new mathematical discovery.

## Excluded claims

This packet does not resolve an isentropic, bounded-specific-entropy, near-constant-entropy Sobolev, or compact-support version of the question. It does not establish that every intended interpretation of Serre's problem is solved. The author's intent beyond the explicit printed statement has not been confirmed. If a narrower target is specified, the existing example must be treated as a partial result or source-scope hold for that target.

The flow's velocity is affine and generally unbounded in space; its temperature is spatially constant. Smoothness means classical smoothness at every finite spacetime point, not decay or unweighted Sobolev control of every primitive variable.

## Evidence and preservation

- Author freeze: 630d9dd1a379f0d40be98e193d4bfe8caaa1a9a3697dc961720202685d0b1e2a.
- Independent audit: [AUDIT_STATUS.json](audit/AUDIT_STATUS.json), verdict PASS_SCOPE_QUALIFIED.
- Author controls: 60 exact checks, with byte-identical replay.
- Independent controls: 20 exact checks.
- All original author and audit files are preserved byte-for-byte. References in their frozen files to a pending review or no remote writes describe the historical author/audit stage, not the later publication status.
- The queue change is limited to this problem's status, turn count, and previously blank Findings cell, where the mandatory scope qualification and a link to this note are recorded.
- Source PDFs, extracted articles, source images, catalogue corpora, raw retrieval records, and private context are excluded.

## Reproduce the controls

Requires Python 3 and SymPy (tested with 1.14.0).

~~~sh
python3 verify.py
python3 audit/independent_checks.py
~~~

The scripts write their JSON results beside themselves. These computations supplement the analytic proofs; they do not certify novelty or any excluded variant.

## Prior publication

K. Fellner and C. Schmeiser, *Classification of Equilibrium Solutions of the Cometary Flow Equation and Explicit Solutions of the Euler Equations for Monatomic Ideal Gases*, Journal of Statistical Physics 129 (2007), 493–507, [DOI 10.1007/s10955-007-9396-8](https://doi.org/10.1007/s10955-007-9396-8), Section 5.

