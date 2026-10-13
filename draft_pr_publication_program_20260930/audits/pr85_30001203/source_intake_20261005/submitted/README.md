# 30001203: negative Gramian curvature and observability

A complete AI-reviewed counterexample uses a connected double cover of a closed hyperbolic surface, a smooth Nash isometric observation map, and zero dynamics. The Gramian is exactly the hyperbolic metric; every output history has two initial states.

- [Counterexample and all hypotheses](COUNTEREXAMPLE.md)
- [Sources and duplicate gate](SOURCES.md)
- [Research log](RESEARCH_LOG.md)
- [Exact control receipt](verification.json)

[Separate adversarial AI review passed](review/REVIEW.md). This has not undergone human peer review. No historical novelty is claimed. The construction is one substantive attempt. Imported record30001204 is the same question, not a second result.

Reproduce the controls with Python3 and SymPy:
    python verify.py

The checker prints JSON and reads the adjacent COUNTEREXAMPLE.md. It does not construct a Nash embedding numerically; the mathematical proof imports Nash's smooth theorem.
