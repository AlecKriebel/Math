# Problem 30002011: reviewed scoped results, original objective unresolved

**Disposition: unsolved, 5/5 substantive author turns.** The independent audit in [review/ADVERSARIAL_REVIEW.md](review/ADVERSARIAL_REVIEW.md) passes the five-turn scoped mathematics without mandatory revisions. It does not certify a solution of the broader corruption-selection and full-data-refit objective.

## Strongest proved construction

For iid Poisson means drawn from a prior on a fixed bounded interval [0,M], the original Brown–Greenshtein–Ritov three-stage smoother with strictly positive h_n=n^-4 has average regret O_M((log n/log log n)^2/n). Any measurable data-dependent positive h confined to a deterministic window of width O(n^-5/2) has that same order after full-data fitting. In particular, ordinary finite-thinning CV over the explicit grid {k n^-4: 1<=k<=n}, followed by full-data refitting, has that order for every deterministic thinning parameter in (0,1) and finite replication count.

This is a genuinely data-selected shrinking-grid theorem. Its guarantee follows because every permitted output is close to the gap-filled limiting estimator, rather than from unrestricted CV adaptivity. A separate output-distance safeguard handles a broader preliminary grid only by modifying the tuning protocol.

## What remains unresolved

Unmodified selection and full-data refitting on a general candidate grid allowing moderate h have no sharp regret guarantee in this packet. A good positive comparator does not by itself control the unrestricted adaptive deletion correction. Heavy-tail, unrestricted-prior and unspecified deterministic-mean compound-regret extensions are not included. The original OWR statement is an open-ended research objective, not one fully quantified universal CV theorem.

## Credit and evidence

The known gap-filled h=0+ limit is credited to Brown–Greenshtein–Ritov. The fixed-sample, in-sample Robbins rate and matching bounded-prior minimax lower bound are credited to Polyanskiy–Wu, arXiv:2109.03943v2, Theorem 2 and Appendix C. At M=0 regret is identically zero; the nonzero matching minimax rate concerns M>0. Hudson/coupled-bootstrap identities, isotonic projection facts and concentration tools remain credited prior theory. No historical novelty or human peer-review claim is made.

All 40 files in the final author manifest are preserved byte-for-byte, as is the manifest itself. The separate review verified all eight source PDF hashes, reran all 68,121 author assertions with identical receipts, and passed 116,124 independent exact rational assertions. The independent implementation uses max-min isotonic fits and reciprocal exponential-series enclosures without importing author code. Finite controls supplement the analytic review and do not themselves establish asymptotic rates.

## Reproduce

From this directory, with Python 3.11 or newer:

    for k in 1 2 3 4 5; do python checks/verify_turn${k}.py > /tmp/30002011-turn${k}.json; cmp /tmp/30002011-turn${k}.json checks/turn${k}_checks.json; done
    python review/independent_checks.py > /tmp/30002011-independent.json
    cmp /tmp/30002011-independent.json review/independent_output.json
    python verify_package.py

The frozen author files retain their historical and pre-review status text. This document and CURRENT_STATE_REVIEWED.json record the later reviewed disposition. The only queue change is this target's row to unsolved, 5/5. No queue regeneration, merger, release, or sixth author research turn is part of this package.
