# Linear-time graph covering: credited prior resolution

**Problem:** UnsolvedMath 10000083 / AMR-099-0083, queue rank 446.
**Recommended disposition:** `already_solved`, **0/5 substantive proof-attempt turns**, with an explicit finite-size statement correction.

Quentin Dubroff and Jeff Kahn proved the intended asymptotic conjecture in
*Linear cover time is exponentially unlikely*, Annals of Probability 53(1)
(2025), 1–22, [DOI 10.1214/24-AOP1699](https://doi.org/10.1214/24-AOP1699).
The directly checked primary proof is
[arXiv:2109.01237v2](https://arxiv.org/abs/2109.01237v2), Theorem 1.1,
read with the large-n convention on page 4.

This is a source-status certificate, not a new proof or a priority claim.
The imported report's claim that the general bound is unestablished is stale.
The unqualified all-n wording is false for the two-vertex graph; that elementary
boundary issue must not be hidden when recording the known resolution.

- [KNOWN_RESULT.md](KNOWN_RESULT.md): exact mathematical scope and correspondence
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): original-source identification, versions, access limits
- [PRIOR_ATTEMPT_GATE.md](PRIOR_ATTEMPT_GATE.md): bounded campaign-history and duplicate checks
- [RESEARCH_LOG.md](RESEARCH_LOG.md): dated source-review record and zero-turn accounting
- [STATUS.json](STATUS.json): machine-readable proposed disposition
- [verify.py](verify.py): exact finite boundary controls only

An independent source/scope audit passed. It inspected the core argument
through section 5, without claiming a complete proof reconstruction or
formal verification. The campaign-history gate was not independently
repeated. See [the audit](audit/AUDIT_REPORT.md) for those limits and the
nonblocking reversed-inequality typo in arXiv v2 Theorem 2.3.

The missing n-threshold also occurs in the original informal source, not
only in the catalogue. Both the literal defect and the intended asymptotic
resolution remain explicit. This packet is prepared for one draft PR; no
merge, release, DOI deposit, or external outreach is authorized here.
[PUBLICATION_RECORD.md](PUBLICATION_RECORD.md) records editorial provenance.

