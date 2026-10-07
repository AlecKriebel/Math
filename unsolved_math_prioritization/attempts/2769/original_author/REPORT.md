# K3 Problem 2 21 research outcome

Problem ID 2769, rank 909. Outcome: partial, stalled after five bounded approaches. No general solution, new minimum, or novel mathematical theorem is claimed. The companion proof records standard subcases and exact reasons that several tempting reductions do not establish the desired minimum.

## Source and scope verification

The exact problem page is https://unsolvedmath.com/problems/2769. Direct retrieval returned HTTP 403; web retrieval returned an internal error. The complete inherited exact-ID record was inspected and its statement and combined record/report hashes matched the expected values. Its report field was empty; the background contained literature triage rather than an inherited mathematical attempt. The prior-work gate therefore passed.

The actual 436-page K3 book was retrieved and Problem 2.21 inspected at printed pages 102–103. The four-page AIM workshop summary was not used as evidence for its contents. K3 discusses g>=1, b>=0, allows essential separating curves, and distinguishes minimum length from the previously studied maximum. Its existence discussion excludes g=1,b>9 and g>=2,b>4g+4, and describes genera one and two as settled. These source statements are contextual literature reports, not conclusions newly proved here.

For b=0, excluding the empty word is essential to the intended nontrivial-fibration interpretation. For b>0, the factors must not include boundary-parallel twists: otherwise writing Delta itself as its b boundary twists would alter the optimization problem.

## Literature distinctions

[BMVHM] defines its main length L as a supremum over nonseparating factorizations. Its auxiliary function allowing homologically essential separating curves still has a different admissible class from arbitrary essential curves. Consequently its maximum-length formula must not be substituted for the requested minimum, or silently transferred across curve conventions.

[BK] provides the low-genus obstruction and construction used in the proof. [Alt] provides stronger answers for restricted hyperelliptic families, which cannot be turned into unrestricted lower bounds.

Two very recent public manuscripts were checked as well:

- Evan Huang, Equivalent genus-2 factorizations of type (4, 3), arXiv:2602.20451v2, posted 5 October 2026. The abstract, introduction and Theorem 1.1 identify the existing Baykur–Korkmaz, Hamada and Xiao fibrations with each other. This does not determine higher-genus minimum lengths. https://arxiv.org/abs/2602.20451
- R. Inanc Baykur and Susumu Hirose, Lefschetz fibrations with handlebody monodromy, arXiv:2610.05537v1, posted 4 October 2026. The abstract, introduction and Theorem 1 concern the additional handlebody-extension condition, including the base-genus restriction h>=2 for nonzero critical-point count. This is not a solution of the unrestricted sphere-base problem. https://arxiv.org/abs/2610.05537

These are manuscript claims with their stated scopes; no independent verification of their complete proofs is represented. The literature pass was bounded, not a comprehensive proof of absence of later work.

## Retained conclusions

The mathematical note proves or reconstructs:

1. The familiar exact value m_1,1=12 from abelianization and a chain relation.
2. The known genus-two seven-node obstruction, with equality type (4,3), and its established realizing construction.
3. The precise dependence of length on Euler characteristic and on b_2-2b_1.
4. An explicit 12-factor homology false positive in every genus at least two.
5. The logical direction of bounds when minimizing over a restricted class.

These are useful validation and scope checks. None closes the general lower-bound/construction gap. Computational matrix checks would be diagnostic only; no computational certificate of minimality is included.

## Repository history coverage

A bounded read-only history check on AlecKriebel/Math used default-branch code search for 2769, and all-state PR and commit searches for the exact ID, KP-2.21, and the positive-factorization phrase. All three returned zero matches. This is not an exhaustive branch/history audit and is not evidence of novelty.

## Acceptance boundary

Accept this package only as an authored partial mathematical audit and a precise failed-reduction report. Reject any label of full solution, new minimum, exhaustive literature coverage, or machine-certified mapping-class equality. No executable is included, so there is no optimized-mode executable claim. Independent review is required before publication.
