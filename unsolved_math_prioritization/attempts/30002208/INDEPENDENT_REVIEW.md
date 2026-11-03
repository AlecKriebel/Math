# Independent mathematical review

Date: 2026-10-21. Target: problem 30002208, ordered row 1881.

## Verdict

The mathematical reductions in `RESEARCH_AUDIT.md` pass this independent check. They do **not** solve the structural characterization problem or establish a converse to the published FS-mean sufficient condition. No novelty claim is certified. This review contains authored arguments, not copied source text.

## Spectral extension formula

The real span D need not be norm closed or an algebra. It contains constants. Restricting any invariant mean to D defines the same positive unital functional Λ, by the matrix-coefficient mean ergodic identity. The FS-mean definition in the published 2026 paper, Definition 3.4, is exactly agreement with these matrix-coefficient values, without a requirement of invariance on all bounded functions. Passing between real functions and their complexification causes no additional condition.

For bounded real g define

    l = sup{Λ(f): f∈D, f≤g},
    u = inf{Λ(f): f∈D, f≥g}.

Constants make both numbers finite, and positivity gives l≤u. If g∉D, assigning g any value t∈[l,u] gives a well-defined positive unital functional on D+Rg. To check positivity, consider f+cg≥0: positive c invokes the lower bound on t, negative c invokes the upper bound, and c=0 uses positivity on D. If g∈D, both endpoints already equal Λ(g).

Every positive unital functional on a subspace containing constants has norm one. Real Hahn–Banach gives a norm-one extension to all bounded real functions, still taking 1 to 1. Such an extension is positive: for h≥0 and M=||h||, its value at M1−h is at most M, so its value at h is nonnegative. In particular t=u is attained. Applying this to g=1_A proves the displayed spectral-majorant formula, including attainment of its left-hand supremum.

Crucial limitation: these are arbitrary positive extensions, not necessarily invariant extensions. Adding invariance would change the class and invalidate the stated identification with FS-means. The audit correctly avoids that change. The implication from failure of P(A) to arbitrarily small spectral majorants is a contrapositive of the known sufficient theorem; the converse remains unproved.

Public source for the terminology: https://doi.org/10.1017/fms.2026.10205 .

## Dilation and finite-index check

For m>0, S is PS if and only if mS is PS. If F+S contains arbitrarily long intervals, then mF+mS+[0,m−1] does too. Conversely, suppose E+mS is thick. Set E_0={e/m:e∈E∩mZ}. Then

    (E+mS)∩mZ = m(E_0+S).

Intersecting arbitrarily long intervals with mZ and rescaling proves E_0+S thick. Thus S is PS. Reflection handles negative m.

If P(mA), test the positive-density set mB; since d*(mB)=d*(B)/m, the dilation equivalence gives P(A). Conversely, split a positive-density B into its m residue classes. Finite subadditivity of upper Banach density ensures that some B_r=B∩(r+mZ) has positive upper Banach density. Its rescaling C=(B_r−r)/m satisfies d*(C)=m d*(B_r)>0. P(A) makes A+C PS, hence m(A+C)+r is PS and is contained in mA+B. This proves P(mA). No unjustified passage from one residue class to all residue classes is needed.

## Other checked reductions

- Finite nonempty F satisfies: F+S is PS iff S is PS. This follows by composing finite thickenings and by monotonicity; it does not require partition regularity.
- Finite modifications of A preserve P. For nonempty sets the proof uses partition regularity of PS and the preceding finite-thickening equivalence. For the empty-set edge, no finite A has P because positive-density non-PS sets exist.
- An elementary witness for that last assertion is B=Z minus the union, over k≥1, of 2^(k+3)+2^(k+4)Z+[-k,k]. Each B+[-k,k] misses a syndetic progression. Counting the O(log N) relevant progressions in [-N,N] bounds the removed proportion by 5/16+O((log N)^2/N), so B has positive upper Banach density.
- Density amplification is valid: an ergodic positive-cylinder-mass measure on the orbit hull of B makes finitely many cylinder translates cover mass greater than 1−ε. Finite-pattern approximation bounds that mass by d*(F+B). Failure of PS persists under finite thickening. This yields arbitrarily-high-density witnesses, not a single density-one witness.
- Intersections of independently amplified witnesses cannot be assumed positive-density: disjoint alternating-block thick sets can both have upper Banach density one. Arbitrary finite-union closure of nonpreservers has not been established.
- The syndetic-hole obstruction has the correct signs and quantifiers. For a failure witness B, take H_k=Z minus (A+B+[-k,k]); conversely the stated complement avoids every required forbidden translate. This is a dual reformulation of the definitions.

## Finite-state criterion

All approximants must be regarded as subsets of the same compact countable-track shift. Their invariant probability measures form nonempty nested compact sets; b≡0 and all h_k≡1 ensure nonemptiness. Compactness of maximizing measures proves α=inf_n α_n. The finite constrained-track projection is a finite-alphabet shift of finite type, and its maximum invariant b-density equals a maximum cycle mean in a finite higher-block graph.

Computability of an individual graph presupposes that A∩[-n,n] is supplied, or that membership in A is available through an oracle. The construction retains quantification over arbitrary gap-bound sequences, has no established convergence modulus, and gives no finite terminating decision procedure. It is an exact variational encoding, not the missing structural solution.
