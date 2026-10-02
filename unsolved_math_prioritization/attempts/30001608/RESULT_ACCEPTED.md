# Problem 30001608: source-qualified complete result

**Claimed solved after 4/5 substantive author turns.** For every fixed real lambda > 0, the exact deterministic-first-chunk continuous-time Markov chain stated in [TURN_4.md](TURN_4.md) is irreducible and positive recurrent. The [independent adversarial review](review/ADVERSARIAL_REVIEW.md) passes this full theorem without mandatory mathematical revisions. No unresolved mathematical gap was identified by the proof or review.

The global Foster function combines workload, rounded cohort imbalance, and finite Poisson corrections with monotone ratio cutoffs. First-download interface errors are nonpositive, while all remaining interface errors are explicitly controlled. This proves negative drift outside a finite set without an uncharged sector-switching step or a stationary-mean substitution for the original chain.

## Scope and provenance

- The statement concerns exactly the six rates, denominator x+y+1, permanent seed, and immediately departing complete peers in the deterministic-first-chunk model.
- It holds at every fixed positive real arrival rate. Lambda=0, other protocols, many-chunk generalizations, and bounds uniform in lambda are not asserted.
- The primary OWR 48/2010 statement (printed p. 2782) gives the stability conjecture. The 2009 arXiv Figure 2 independently confirms the rates, but that edition's opposite conjecture is superseded by the later statement.
- The 2011 author-proof details are recovered from the pinned source audit. Fresh HAL PDF and screenshot access were unavailable and are not presented as newly verified downloads. See [source recheck](SOURCE_RECHECK_TURN_4.md) and [original audit](SOURCE_AUDIT.md).
- Finite birth-death balance, Poisson equations, and continuous-time Foster/Dynkin arguments are credited standard tools. Historical priority and worldwide novelty are not certified.

## Validation and reproducibility

The author checker passes 71,165 exact rational assertions over 5,200 states at loads 1/2, 1, 2, 5 and 10. The separate reviewer implementation reconstructs the corrector by a backward recurrence and passes 36,709 exact assertions over 1,908 states at loads 1/7, 7/3 and 13/2. It imports no author code. The reviewer also reran the author checker and reproduced its saved output byte-for-byte. These finite tests supplement the all-state analytic proof.

From this attempt directory, using Python 3.11 or newer:

    python checks/turn4_checks.py > /tmp/30001608-author.json
    cmp /tmp/30001608-author.json checks/turn4_output.json
    python checks/independent_review_portable.py > /tmp/30001608-independent.json
    cmp /tmp/30001608-independent.json review/independent_checks.json
    python verify_package.py

The frozen reviewer program is preserved unchanged at review/independent_check.py. Its portable copy changes exactly one absolute proof-path literal to a repository-relative path; its mathematical code is unchanged. The original review receipt and manifest remain intact.

TURN_4.md, the four turn manifests, and the independent review are frozen evidence. Their pre-acceptance status text records the state when written. CURRENT_STATE_ACCEPTED.json and this document report the later disposition. The queue update changes only this target's row to claimed_solved, 4/5; no queue regeneration or unrelated status update is part of this package.
