# 2305051: an explicit Blaschke product with a Bloch Cayley transform

**Complete candidate awaiting separate adversarial review.** A deterministic
four-adic integer recursion produces rational finite Blaschke products. Their
locally uniform limit has B(0)=0 and a Bloch Cayley transform. An explicit error
bound makes the construction effective on compact subsets of the disk.

The proof separately excludes a singular inner factor: an angular limit of
the inner function at zero would force a finite positive density of its
Herglotz measure, incompatible with the nonabsorbed unit-step recursion.

- [Full construction, proof, and attribution](CANDIDATE.md)
- [Primary sources and current-literature scope](SOURCES.md)
- [Exact recursion checker](verify_recursion.py), [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [status](status.json), [readiness](readiness.json)

Run `python3 verify_recursion.py` from this folder. Only Python's standard
library is required. The bounded checks do not replace the analytic proof.

Existence was already known, including stronger covering-map results.
Kahane's and Cantón's martingale methods and the classical analytic inputs are
credited. Historical priority is unestablished. The explicit answer is a
fully specified recursion with a compact-uniform convergence bound, rather
than a short closed-form list of all zeros.
