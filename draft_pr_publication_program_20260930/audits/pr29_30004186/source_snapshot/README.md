# Peaked Ostrovsky wave: reviewed strong-norm partial theorem

**Result:** nonlinear orbital $W^{1,\infty}$ instability of the peaked periodic reduced Ostrovsky wave, in an explicitly constructed local characteristic solution class containing one transported corner.

**Full source status: unresolved/partial.** This package does not prove an $L^2$ or $H^1$ orbital departure, finite-time blow-up, or uniqueness of global weak/entropy continuations after breakdown. A fixed derivative departure does not automatically imply a fixed weaker-norm departure.

- [Frozen candidate](CANDIDATE.md)
- [Independent adversarial PASS review](independent_review/REVIEW.md) and [verdict](independent_review/verdict.json)
- [Source scope and superseded 2018 nonlinear claim](SOURCE_AUDIT.md)
- [Research log](RESEARCH_LOG.md), [provenance](provenance.json), and [attempt record](turns.json)

A separate AI agent checked the general Banach evolution, uniform local existence, bounded-slope continuation, one-sided derivative equations, moving-corner forcing, and orbital-phase estimate. No mathematical correction was required. All 20 submitted checks and 135 independent exact assertions passed. This is not human peer review or formal verification; historical priority is unconfirmed.

The candidate remains byte-for-byte frozen at SHA-256 `95458afe7f030f3f0aec3b9d5150857e7dedcb8688e6325c4a0407497feb1b6c`. Its original pending-review header describes the pre-review snapshot; the linked report supplies its current status.

The superseded April 2018 arXiv version of Geyer–Pelinovsky claimed a stronger nonlinear conclusion that was removed in the January 2019 revision and published paper. That history is preserved and credited. The present proof constructs its corner-compatible flow directly and does not reuse the unsupported smooth-perturbation or proportional-stability steps of that earlier argument.

## Reproduce exact checks

From this directory, using Python 3 and SymPy (tested 1.14.0):

```sh
python3 check_identities.py
python3 independent_review/independent_checks.py
```

These are small exact identity checks, not simulations or a computational proof of the PDE theorem. One substantive response was used; the original source question is not promoted to a full solved status.
