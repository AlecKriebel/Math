# Independent full-source/proof review request

Problem 30005767 / OWR-14298158-012. One substantive author turn, complete negative candidate; no novelty claim. Proposed disposition after approval: already_solved 1/5. The final manifest binds every portable author file other than itself.

## Exact sources and audit obligations

1. Original official OWR 6/2024 PDF, complete Brignall contribution pp. 290–293, especially Question 5 p. 292. Verify the field uses both sqrt(1−4z) and sqrt(1−6z+5z²), the proper-subclass condition, and the ordinary permutation-length convention. The source hashes and exact URLs are in SOURCE_MANIFEST.json; locally the PDFs are under the sibling sources directory, excluded from the public packet.
2. Callan, Mansour and Shattuck, DMTCS 19:1 (2017), article 6, Theorem 11, pp. 13–14: verify exact class Av(2341,2413,3142), exact radical and the empty term. This is the established enumeration being credited. Inspect its whole local proof; no other classification cases are claimed recertified.
3. Albert, Atkinson and Vatter, preprint 1007.1014v1, Proposition 1.2 and ordinary series definitions/Proposition 1.4: separable direct/skew decomposition framework.

## Proof audit

Read every section of TURN_1.md. Check the proper-class witness 2341=123 skew-sum 1; uniqueness of the *first* indecomposable component; the no-sum-cut/unique-skew-cut boundary lemma; occurrences meeting arbitrary numbers of components; the exact classification of skew-indecomposable 123-avoiding separables as a singleton or two decreasing direct-sum blocks; grammar necessity, sufficiency and no overcounting; formal branch and empty term.

For field exclusion, check that U,V define an actual degree-four biquadratic extension and that a radical whose square lies in Q(z) must occupy one of the four simultaneous eigenspaces. Check all four rational square classes using P's odd degree, P(1/4)=−17/256, V(1/4)=−3/16 and P(1)=1. Finally check minimal quadratic irreducibility and the explicit inverse radical formula sqrt(P)=B−2AC, with A nonzero. A discriminant equation without this cancellation check would be insufficient.

The source's heuristic for Av(2143,2413,3142) and its shifted full-Sep display are not used in the proof. This packet must not be confused with a refutation only of the smaller Catalan-radical field, or with a broader nonseparable class. Neither any related structural question nor novelty/priority is claimed resolved.

## Replay

From checkpoint directory:

    python verify_turn1.py > /tmp/separable_turn1_replay.json
    cmp TURN_1_CHECKS.json /tmp/separable_turn1_replay.json

Only Python 3 standard library is required. Verify the final file hashes and every source PDF hash separately. Finite checks are supporting controls, not substitutes for the written grammar or field argument. Please return a qualified PASS/FAIL, exact mandatory corrections if any, and a portable independent review with its own integrity manifest. No publication is authorized by this request itself.
