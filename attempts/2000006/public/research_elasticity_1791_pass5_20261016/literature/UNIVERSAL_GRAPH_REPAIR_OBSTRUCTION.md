# Universal orientation-safe graph rules cannot repair the determinant

16 October 2026. This is an elementary auxiliary obstruction for the inverse-comparison route, not a counterexample to E-6322. It concerns a deliberately explicit universal matrix requirement. Map-dependent comparisons need only preserve the actual derivative and are not excluded.

## 1. Exact matrix classification

**Lemma.** For real 3×3 matrices A and B, the following are equivalent:

- det(A+BH)>0 for every H∈GL⁺(3);
- either A=0 and det B>0, or B=0 and det A>0.

The reverse implication is immediate. For the forward implication, distinguish the rank of B.

If B is invertible and A≠0, put C=B⁻¹A and choose a nonzero vector q with Cq≠0. There is an H∈GL⁺(3) satisfying Hq=−Cq: extend q to a positively oriented basis and extend its prescribed nonzero image to another positively oriented basis. Then (A+BH)q=0, a contradiction. Thus A=0, and the requirement now says det B>0.

If B=0, the requirement is exactly det A>0.

It remains to exclude rank B=r∈{1,2}. Orientation-preserving orthogonal changes in the range and intermediate space reduce B to diag(σ₁,…,σ_r,0,…,0), with σ_i>0, without changing the set of permitted H or the sign of the output determinant. Write A for the transformed matrix. The last 3−r rows of A must be independent; otherwise every A+BH is singular. Choose independent rows q₁,…,q_r which complete those fixed bottom rows to a basis. Either sign of the determinant of this completed basis can be obtained by reversing q₁.

Take the first r rows of H to be t q_i. They can always be completed by unused rows to a matrix H with det H>0. These unused rows have no effect on BH. As t tends to positive infinity,

det(A+BH)=t^r(σ₁⋯σ_r) det[q₁;…;q_r; A_{r+1};…;A₃]+O(t^{r−1}).

Choose the displayed leading coefficient negative. The output determinant is negative for sufficiently large t, contradicting the universal requirement. This completes the classification.

## 2. Consequence for the precise graph family from pass 4

Let D=G(Ω), and let Φ be C¹ on a neighborhood of Dbar×Ωbar. Write

A(z,x)=D_zΦ(z,x),    B(z,x)=D_xΦ(z,x).

Assume the pointwise universal condition

det[A(z,x)+B(z,x)H]>0

for every (z,x)∈D×Ω and every H∈GL⁺(3). Since D×Ω is connected and A,B are continuous, the two alternatives in the lemma cannot switch: each is relatively open in the set of admissible pairs, because the nonzero determinant of its invertible matrix persists locally. They are disjoint and exhaust that set.

Suppose also that Φ(z,x)=x whenever z belongs to a fixed boundary collar in D, for every x∈Ω. This is the sufficient boundary condition in the accepted pass-4 graph theorem. The collar selects the branch A=0, det B>0, so that branch holds everywhere. Therefore Φ is independent of z. Its collar values then give

Φ(z,x)=x throughout D×Ω.

**Corollary.** Under that full-product collar condition, the only smooth graph rule preserving strict orientation for every incoming positive-determinant matrix is the identity rule.

This is stronger than merely observing that convex combinations of GL⁺ matrices may be singular. It classifies every affine-in-H derivative expression arising from a smooth graph transformation. The universal requirement is sufficient for orientation safety, but it is not a hypothesis that E-6322 minimizers or all useful comparisons must satisfy.

## 3. What remains possible

If the boundary condition is only required along the actual inverse graph rather than for all x in the collar, a nontrivial material composition Φ(z,x)=Ψ(x) can survive. Such comparisons were already legitimate. If Ψ is a C¹ orientation-preserving diffeomorphism on a neighborhood of Ωbar, compactness gives constants 0<m≤M<∞ such that

m K(z) ≤ det D(Ψ∘v)(z) = det DΨ(v(z)) K(z) ≤ M K(z).

Consequently one fixed such material diffeomorphism cannot turn an essentially unbounded K into an essentially bounded determinant. This does not rule out a family whose lower determinant constants degenerate with a truncation parameter, or useful variational inequalities obtained from it. Those require quantitative control of the resulting energy.

A graph rule tailored to the actual H=Dv can also avoid the universal obstruction. Its determinant and energy estimates must then use information about that map. The pass-4 graph theorem already settles inverse-class membership once those estimates prove finite V. No such construction yielding an L∞ bound for K has been established here.

## 4. Why unrestricted class closure would still leave an analytic step

The broader claim that every compact W^{1,9/5} addition with finite resulting V is in the exact inverse class remains unproved and undisproved in this investigation. Even if it were proved, it would give a minimality inequality only for final maps whose energy is finite. It would not create orientation-preserving cutoffs or a finite-energy amplitude interval.

Moreover V has no finite polynomial upper bound in |H|: for H_ε=diag(1,1,ε), |H_ε| remains bounded while its a-term is at least a ε⁻⁵. Thus ordinary full-matrix upper-growth hypotheses cannot be recovered merely by enlarging a comparison class. The isolated finite-amplitude example and the smooth affine-minimizer cutoff failure proved in pass 4 make the comparison-energy issue concrete.

For an actual inverse, K(y(x))=1/J(x), and the positive-Jacobian change of variables preserves null sets in both directions on the full-measure inverse sets. Hence E-6322 is exactly the assertion K∈L∞(D) for every inverse of a primal global minimizer. The present argument neither proves nor disproves that assertion.
