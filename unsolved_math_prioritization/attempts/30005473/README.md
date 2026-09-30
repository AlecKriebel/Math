# Problem 30005473: discotope exposed-point irreducibility

**Outcome:** complete affirmative proof, independently AI-reviewed and unrefereed; historical priority unconfirmed. One substantive attempt used (1/5). Actual model/effort: gpt-6-astra / xhigh.

- [Typeset proof PDF](proof.pdf) and [LaTeX source](proof.tex)
- [Candidate proof](candidate.md): the exact exposed-point target, a separate generic purely-nonlinear-part extension, and edge cases
- [Independent AI review](REVIEW.md) and [verdict](verdict.json)
- [Source and novelty audit](sources.md): precise source locations and scope distinction
- [Readiness record](readiness.json) and [turn ledger](turns.jsonl)
- [Research log](RESEARCH_LOG.md)
- [Exact sanity checks](checks.py) and [recorded output](checks_output.json)

The theorem states that the complex Zariski closure of the exposed points of any finite Minkowski sum of ellipsoidal discs of dimension at least two is irreducible. It uses a connected real-analytic support-point parametrization and does not need genericity. The general theorem is proved on paper, not certified by finite tests.

Run the checks with Python 3 and SymPy:

    python checks.py

No large search, degree computation, external communication, shared-queue modification, release, or DOI is involved. The work is intended for the dedicated branch `dot/math-30005473` and one draft pull request. No journal submission, release, DOI, or outreach is authorized by this artifact.
