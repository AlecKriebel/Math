# 3012 / KP-5.5: connected sums of locally flat pairs

**Unsolved after two approaches.** The package isolates the relative
straightening step missing from an attempted higher-codimension proof.

The standard final fiber-preserving isotopy works in every codimension, with
an explicit compactly supported collar extension. What is not established is
that arbitrary locally flat pair charts can be aligned in that form. An
ordinary ambient annulus or sphere isotopy does not preserve the distinguished
submanifold automatically.

- [Full conditional proof and precise gaps](OBSTRUCTION.md)
- [Primary sources, scope, and bibliographic correction](SOURCES.md)
- [Research log](RESEARCH_LOG.md), [status](status.json), [readiness](readiness.json)

The source's connected/oriented conventions and topological category are
retained. The codimension-two theorem is prior work. No numerical experiment
can certify the remaining localization claim, so validation consists of the
proof and source checks. The [independent adversarial review](review/REVIEW.md)
passes this explicitly conditional and unresolved package. Its 19,435 exact
rational controls cover the displayed formulas, not the missing general
straightening theorem. This is AI review, not human peer review.

Run `python3 review/independent_checks.py` to reproduce the independent receipt.

No counterexample, full well-definedness theorem, or novelty claim is made.
