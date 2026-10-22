# Separable permutation rationality: bounded investigation

## Target and verdict
Row 1848, ID 30005757, Vatter's Question 4 on p.283 of Oberwolfach Report 6/2024 asks whether every permutation class C contained in Sep and containing Av(231), or a symmetry, has nonrational ordinary generating function. No universal proof or downward-closed rational counterexample has been established in this investigation. The following are partial results and obstructions, not a solution.

## 1. Source and literature approach
Primary source: https://ems.press/content/serial-article-files/48646 . Albert–Atkinson–Vatter, *Subclasses of the separable permutations* (2011), https://arxiv.org/abs/1007.1014 , proves strong rationality precisely when none of the four Catalan symmetry classes is contained. This does not settle ordinary rationality. The later workshop explicitly asks the converse. Targeted current searches found no verified later resolution. A search result on a different field-of-generating-functions question must not be confused with this problem.

Additional relevant material appears in Brignall's report, pp.290–292, joint with Bóna, Defant, Opler, Vatter. It states nonrationality under the stronger hypotheses C⊕C⊆C and 1⊖C⊆C (Theorem 4, interpreting Bóna). Its structural Conjecture 3 is explicitly incomplete. Our reproduction of Sep∩Av3412 is symmetry-equivalent to the known example on p.292, not new.

## 2. Finite basis and signed tree automata
Sep is well quasi ordered. Therefore its relative forbidden basis for any subclass C is finite: minimal excluded members form an antichain. The global basis is finite too after including 2413 and 3142 and discarding redundant members. For C to contain Av231, every relative forbidden pattern must contain 231. This is a genuine finite reduction, but there is no uniform bound on forbidden lengths.

The program search.py tracks which subpatterns of the forbidden patterns occur. A state is (profile mask, root sign), where root sign 0 denotes the singleton. For a sum or skew composition the new profile contains the profiles of both children, plus every tracked pattern whose corresponding sum/skew cut has its left factor in the left profile and its right factor in the right profile. This is exact because any occurrence crossing the split has precisely such a cut. A rejecting profile contains a forbidden pattern.

Canonical decomposition uses the first sum-indecomposable component as the left child at a plus root, and the first skew-indecomposable component at a minus root. Hence left-child root sign differs from the parent; the right child is arbitrary. Every nontrivial separable permutation has exactly one such representation. The finite system Y_c = singleton contribution + sum Y_a Y_b over allowed transitions is unambiguous and polynomial, providing exact coefficients.

## 3. Small-basis search and elimination
The eight length-four separable patterns containing 231 are 1342, 2314, 2341, 2431, 3241, 3412, 3421, 4231. Every one of the 255 nonempty subsets defines a genuine downward-closed subclass containing Av231. all_length4_results.json records exact coefficients through length 80. A modular Berlekamp–Massey screen is only a search heuristic: absence of a short recurrence is NOT proof of nonrationality. No rational counterexample emerged.

An independently checkable exact example: let F enumerate nonempty Sep∩Av3412, and P,M its sum- and skew-decomposable parts. Since 3412 is sum indecomposable, P=F²/(1+F). In canonical skew decomposition, at most one component is nonsingleton, since two nonsingleton skew-indecomposable components each contain12 and would create3412. Thus
M=x²/(1-x)+P((1-x)^(-2)-1), F=x+P+M.
Eliminating gives
x(x-2)F²+(2x²-3x+1)F+x²-x=0.
The discriminant is (1-x)(1-5x), not a square in Q(x), proving this example nonrational. The formal branch is selected by F(0)=0.

The 1342 symbolic elimination was stopped after expression swell and is inconclusive. It is excluded from acceptance.

## 4. Singularity propagation and cancellation
Nonnegative coefficients and Catalan coefficient domination alone cannot prove the result. Even finite positive polynomial specifications can contain a nonlinear Catalan component and have a rational total. The exact positive-grammar countermodels in singularity_obstructions.md are algebraically checked; it is not a permutation downset and hence not a counterexample to the actual question. One needs a special structural invariant of downward-closed signed-tree languages to rule out cancellation.

## 5. Structural closure/reduction
The established closure criterion C⊕C⊆C and 1⊖C⊆C is stronger than containment of Av231. Arbitrary finite relative bases may destroy either closure. Finite unions/inflation reductions also introduce possible algebraic cancellation: nonrationality is not inherited upward by inclusion. The incomplete workshop structural conjecture therefore cannot be used as a theorem, and even a reduction must justify how nonrationality survives its enumerative operations.

## Remaining gap
A full proof needs a noncancellation theorem specific to all finite-basis downsets of signed separable trees, or an explicit rational class and an exact unambiguous specification. Finite searches, generic positive-system arguments, the strong-rationality characterization, and the closure theorem individually do not supply this.

## Additional exact singleton case: Av4231 inside Sep
Let T be the nonempty Catalan series, T=x(1+T)^2, T(0)=0. Let Q count sum-decomposable members of Av231 (equally of Av312). Since the nonempty Catalan class has singleton contribution x and skew-decomposable contribution xT, Q=(1-x)T-x.

In a skew-decomposable member of Sep∩Av4231, any nonsingleton canonical skew component must occur at an endpoint. Otherwise a singleton selected before and after an increasing pair within it creates4231. A first nonsingleton component must avoid312, and a last nonsingleton component must avoid231. Conversely these restrictions exclude every occurrence of4231: an occurrence crossing components either uses its increasing middle pair in an interior component, or would require312 in the first or231 in the last. Thus the skew-decomposable generating function is
M=(x²+2xQ+Q²)/(1-x)=(1-x)T².
Here the three terms respectively count all-singleton sequences, one nonsingleton endpoint with at least one singleton, and two nonsingleton endpoints separated by any number of singleton components. Since4231 is sum indecomposable, the class is sum closed. Its OGF including empty is
G=1/(1-x-M)=1/((1-x)(1-T²)).
Elimination gives
(4x³-9x²+6x-1)G²+(4x²-5x+1)G+x²=0.
The discriminant is (1-x)²(1-2x)²(1-4x), nonsquare in Q(x). Hence G is nonrational. The branch G(0)=1 is unique at the origin. First12 coefficients match the independently audited automaton. The independent audit addendum accepts this exact derivation; no novelty certification or claim is made.

## Audit and computational limits
The independent audit in INDEPENDENT_AUDIT.md checked all255 bases by brute-force permutations through n7, all124258 profile transitions using actual witness permutations, the3412 exact quadratic, and the C11 dominant-pole obstruction. The automaton has9218 reachable states in total across the255 cases. Symbolic per-state elimination was attempted, but expression swell made the first1342 case impractical in this bounded pass. An experimental3412 symbolic expression agrees with the known radical form but is not used as a certificate. Only the hand-derived exact eliminants above support nonrationality claims.
