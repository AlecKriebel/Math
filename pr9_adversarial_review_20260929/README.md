# Adversarial review of pull request 9

**Mathematical verdict: pass. No mathematical or computational revision requested.** The reviewed PR head is `a29887ed0e341851d02fa992c26500d4089267be`; historical priority remains unconfirmed.

Start with [the full review](REVIEW.md) and [verdict](verdict.json). Independent reports cover [convex and analytic structure](analytic_convex_audit.md), [generic faces](generic_face_audit.md), and [exact algebra and reproduction](algebra_reproduction_audit.md). The [research log](RESEARCH_LOG.md) preserves checkpoints, estimates, and a withdrawn provisional finding.

The [snapshot manifest](snapshot_manifest.json) binds the archived candidate and source artifacts. Third-party primary PDFs and render intermediates are retained locally but excluded from Git; the [download manifest](primary_sources/download_manifest.json) records their URLs and hashes.

For exact checks, use Python 3 with SymPy 1.14.0 and mpmath 1.3.0. From this folder run `python source_snapshot/checks.py` for the inspected original checks and `python algebra_independent_checks.py` for the independent checks. The latter writes fresh evidence in this review folder. These examples corroborate the universal proofs and do not replace them.

`python3 reproduce_queue_finding.py` reproduces the inherited queue-regeneration risk in an isolated one-record database, without editing the live queue. It needs the named Git object and the pinned local source cache. The [adversarial classification](queue_finding_adversarial_check.md) explains why this is not a new PR merge blocker.

No PR merge, GitHub review submission, release, DOI, or external outreach is part of this review.
