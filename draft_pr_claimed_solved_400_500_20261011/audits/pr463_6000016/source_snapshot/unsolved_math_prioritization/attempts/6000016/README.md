# 6000016 — Stability of Hessian Metrics

**Complete negative argument, frozen for independent audit.** A classical Baues–Goldman family of complete affine tori converges smoothly to the Euclidean Hessian torus. On every noncentral member, the Hessian Codazzi equation would make a strictly positive two-form exact, contradicting Stokes' theorem.

- [Full proof](PROOF.md)
- [Source, scope and attribution gate](SOURCE_GATE.md)
- [Research accounting](RESEARCH_LOG.md): one substantive attempt, complete early
- [Exact symbolic controls](check_exact.py)
- [Recorded check results](exact_results.json)
- [Frozen author file hashes](FROZEN_AUTHOR_MANIFEST.json)

Run `python check_exact.py` with Python 3 and SymPy installed. It writes no files and emits deterministic JSON. Compare its output with exact_results.json. The analytic positivity and integration step is proved in PROOF.md, not replaced by a finite numerical test.

The affine family is already published; no novelty, priority or human peer-review claim is made. The exact live aggregator was inaccessible (HTTP 403), but the original item 5(b) was visually verified. Review status at this freeze: independent audit pending. Any later audit and administrative status should be appended without changing these frozen author files.
