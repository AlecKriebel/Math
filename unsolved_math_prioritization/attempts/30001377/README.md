# 30001377 / OWR-4135-008: sensitivity under an AND layer

**Unsolved after two approaches.** The exact statistic is the uniform expected
pointwise maximum sensitivity. The package proves the logarithmic-fan-in special
case, a logarithmic-amplification control, and the failure of a tempting generic
one-sided transfer inequality.

The Hamming-code control is **not** a counterexample to the original question:
its displayed conjunction factors already have linear input ams. Arbitrarily
large conjunctions of a common low-ams family remain unresolved, as does the
source's weaker subpolynomial implication.

- [Complete deductions and exact gap](OBSTRUCTION.md)
- [Primary-source and prior-attempt audit](SOURCES.md)
- [Exact verifier](verify_controls.py), [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [status](status.json), [readiness](readiness.json)

Run `python3 verify_controls.py`. Standard library only. The 48,145 exact controls
check elementary inequalities and the displayed finite models; they do not
certify the conjecture or a counterexample. Classical constructions are credited.
Separate independent adversarial review is pending. No novelty claim is made.
