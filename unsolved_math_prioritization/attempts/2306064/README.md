# A coefficient-sum answer to Miller's alpha-convexity question

**2306064 / AMR-022-6064. Complete candidate; separate review pending. One substantive proof approach.**

The [proof](CANDIDATE.md) gives an explicit positive coefficient weight for every real alpha. It recovers exactly the source's n and n² endpoint weights. The interpolation parameter is optimal within the stated one-parameter family for 0<alpha<=1; no broader optimality claim is made.

The triangle-majorization method and two-denominator estimate are credited to existing literature, particularly Kumar–Ravichandran (2017). No priority or human peer-review claim is made.

- [Source and literature audit](SOURCES.md)
- [Readiness gates](readiness.json)
- [Research log](RESEARCH_LOG.md)
- [Exact checker](verify.py) and [receipt](verification.json)

Run `python3 verify.py` in this directory. The checks are finite exact diagnostics; the analytic theorem rests on the written proof.
