# Local mathematical corrections to arXiv:2609.04414v1

These corrections concern the proof of Theorem 1 and preserve its argument and conclusion. They are authored audit explanations, not changes to or republication of the source PDF.

1. Theorem 3, Stage 2, printed p. 11 / PDF p. 12: use the nonnegative integer potential sum_{T in L}|T| for termination. A replacement S -> S_i has S_i properly contained in S; thus the potential strictly decreases. Counting cut vertices does not always decrease: a flower of three cycles may be replaced by a flower of two cycles with the same common cut vertex.
2. Lemma 3, printed p. 8 / PDF p. 9, edgeless-intersection calculation: use f(I)<1-|I|/2<=0. The final weak inequality handles |I|=2; the conclusion f(I)<0 is unchanged.
3. Lemma 3, same page, intersection-coordinate expansion: d_A(u)+d_B(u)=2d_{A intersection B}(u)+d_{A\B}(u)+d_{B\A}(u)=d_{A intersection B}(u)+d_{A union B}(u). Neighbors in the intersection are counted twice. The row identity stated in the source is correct.
4. Lemma 4, printed p. 9 / PDF p. 10, disconnected case: for k edge-bearing connected components S_i, sum_i b(S_i)=b(S)+(k-1). This explicitly handles every k>=2 and removes any possible ambiguity in the two-component abbreviation.
5. The introduction's general nonnegative-coefficient description does not apply to rows containing isolated induced vertices, whose coefficient is -1. The proof's separate isolated-vertex elimination makes its later uses of coefficient nonnegativity valid.

The bounded definition also needs a formulation bridge to the original unbounded question. If P is the original nonnegative polyhedron, the source's bounded polytope is B=P intersect [0,1]^V. A putative all-small extreme point of P lies in B and stays extreme in B, because every decomposition in B is a decomposition in P. The bounded theorem therefore proves the original assertion without strengthening its claim to half-integrality or to another LP.
