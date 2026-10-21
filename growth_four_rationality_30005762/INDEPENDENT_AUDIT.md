# Independent audit of the below-four partial research

Date: 2026-10-21 UTC. Target: queue row 1854, ID 30005762.

## Verdict

**ACCEPTED PARTIAL RESULTS ONLY.** The audited partial arguments are correct in the final report reviewed below. They do not solve the conjecture for arbitrary finitely based classes of upper growth strictly less than four. No sum-closure hypothesis has been inserted into that target. The author labels the PP2025 sub-Phi result as an announcement without a recovered complete proof; no result here relies on treating its outline as a verified full proof.

## Independent mathematical checks

1. The length-three corollary follows from the separable-class theorem and proper-subclass theorem. The primary arXiv abstracts were independently retrieved at https://arxiv.org/abs/1007.1014 and https://arxiv.org/abs/1602.00672. Each of 2413 and 3142 contains all four nonmonotone length-three patterns. The strict upper-growth hypothesis excludes every complete Catalan avoidance class. Finite basing is used for the monotone branch. The six-basis-witness inclusion test is necessary only, not sufficient.
2. Independently deriving the maximum split of a 132-avoider gives F_1=1 and F_k=1+xF_{k-1}F_k. The left block exceeds the right block, so the longest increasing subsequence has length max(LIS(left)+1,LIS(right)). This verifies the actual classical increasing-pattern restriction, not a consecutive-pattern interpretation.
3. The recurrence P_0=P_1=1 and P_k=P_{k-1}-xP_{k-2} yields the stated binomial formula and reduced fraction F_k=P_{k-1}/P_k. A shared root would be nonzero and propagate down to P_0, impossible. Thus the reduced denominator degree really is floor(k/2), not merely an upper bound before cancellation.
4. Chebyshev roots give all finite roots of P_k as 1/(4 cos^2(j*pi/(k+1))), for j=1,...,floor(k/2). They are distinct and positive. The unique smallest pole therefore gives the ordinary growth limit 4 cos^2(pi/(k+1)) for k>=2. It increases to four. The automaton dimension conclusion is correctly restricted to unit-length, length-preserving automata; arbitrary large polynomial edge weights would not obey the same state-degree bound.
5. Sum-closure analysis is valid only for actual sum closure. The report constructs a finite class containing every length-twelve permutation that starts with its maximum. This class has growth zero, but its sum closure contains at least 11! indecomposables of size twelve. Their contribution at 1/4 is 155925/65536>1. Taking direct sums of this finite indecomposable subset already produces growth greater than four. Thus the closure reduction cannot preserve the target hypothesis.
6. For a nonnegative matrix M(q) and positive w with M(q)w<w, the weighted sup norm is strictly contracting. This proves convergence of the path series at q, including epsilon transitions if that same certificate holds. To turn an injection into coefficient domination, weights must be genuine path counts (nonnegative integer coefficients), or coefficientwise domination must be explicitly established. Fractional weights plus injection alone would not suffice. The final report explicitly uses nonnegative integer path-count weights, satisfying this requirement.
7. H=1+x^2H^2 is nonrational with upper growth two but is not a hereditary permutation enumeration, because size two exists while size one does not. The finite class of 132-avoiders of size at most N is finitely based by the stated finite forbidden set and agrees with Catalan through degree N. These examples correctly invalidate inference methods, not the conjecture itself.

## Independent computation

The separately authored independent_checks.py checks the closed polynomial formula, degrees, and coprimality for k=1,...,50; it directly enumerates all permutations through length eight and checks 132 avoidance and longest increasing subsequence for k=2,...,8. All checks pass. These finite checks are regressions only. The infinite conclusions above rest on the combinatorial decomposition and exact algebra, not extrapolation.

## Source-gate correction

The original source gate called Av(132) sum-closed. This is false: 1 and 21 both avoid 132, but 1 direct-sum 21 equals 132. The Catalan boundary example and the general target remain unaffected. Delete the sum-closure qualifier or use Av(231) for a sum-closed Catalan class. The final research report explicitly corrects this inherited error and does not rely on it.

## Scope

The author's check_partials.py was inspected and independently rerun successfully. Its emitted JSON exactly matches CHECK_RESULTS.json. The original research audit accepted the exact original report and check-suite bytes. The publication package documents editorial sanitization separately; its inventory records the publication bytes.
