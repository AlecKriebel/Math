# Penner Problem 2: component counting

**11000132 / AMR-109-0132. Status: unsolved, 3/5 substantive approaches.**

The full source asks for a more closed-form component-count expression in Dehn–Thurston or other coordinates. Existing polynomial-bit normal-coordinate algorithms are credited. This package gives an exact expanded permutation formula including boundary arcs, demonstrates its potential exponential expansion, and records narrow arithmetic obstructions. It does not settle the requested general expression or certify its global current open status.

- [Mathematical artifact](OBSTRUCTION.md)
- [Sources and access limitations](SOURCES.md)
- [Readiness gates](readiness.json)
- [Research log](RESEARCH_LOG.md)
- [Exact finite controls](verify.py) and [receipt](verification.json)

Run `python3 verify.py` from this directory. The finite controls test the displayed formulas; they are not a proof of a general compressed algorithm. Separate adversarial review is pending. No novelty or human peer-review claim is made.
