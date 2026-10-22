# Independent initial attack

Scope: exact ordinary coefficient ring in Ohtsuki, Conjecture 7.30, printed pages 490–492, conditional on the fixed-rank invariants of Conjecture 7.29. No candidate proof, helper source text, earlier assessment, or raw preflight output has been opened at this point. The permitted source-record problem field contains an old generic OPEN-TRIAGE label; it supplied no mechanism or proof and is not evidence for the conclusion.

Let x=q−1 and R be the specified Habiro ring. The natural Taylor map R→Z[[x]] permits the further quotient to B=Z[x]/(x²). The rank n specialization sends t to q^n=1+nx in B. If F belongs to the stated inverse limit, its first two Newton coordinates can be written c₀(q)+c₁(q)(t−q); all later terms are multiples of (t−q)(t−q²). At any positive rank n both factors are divisible by x, so the later terms vanish in B. This argument uses compatibility of finite quotient representatives, and does not assume convergence of an infinite series in a field.

Consequently [x]F(q,q^n)=[x]c₀+(n−1)c₁(1), an affine function of n. The required rank-one value is exactly 1, so c₀=1, and the first Taylor coefficient must be proportional to n−1. Thus the finite obstruction is the necessary identity b₃−2b₂+b₁=0, with b₁=0. Equivalently, from ranks 1,2 alone one predicts b₃=2b₂. This is a necessary condition, not a sufficient interpolation criterion.

An independently suggested topology attack is the first perturbative coefficient. In the usual normalized invariant it is expected to be λ(M)n(n²−1), since the theta-graph Lie algebra weight contracts the adjoint Casimir with the dimension: tr(C_ad)=2n(n²−1) under the long-root-length-two convention. The universal scalar is fixed by the sl₂ coefficient 6λ(M). For λ(M)≠0 the first three values would be (0,6λ,24λ), and their second difference is 12λ, contradicting the necessary affine condition. Either orientation gives a nonzero obstruction; the sign is immaterial. A purported proof that all ranks interpolate in this ordinary ring must defeat this jet argument or use a different normalization/coordinate/ring.

The algebraic deduction is complete and directly checkable. The precise outstanding gap at this independent stage is to authenticate the cited topology normalization, establish that the q-coordinate in the source has that coefficient, and exhibit an integral homology sphere with nonzero λ. The theta expression here is an explicit hypothesis to verify, not an authenticated theorem from the candidate. A possible factor or q-to-q^(1/2) convention would rescale all b_n; rank-dependent rescaling must be checked against the exact original statement. A merely nonzero common factor does not remove the contradiction.

Boundary checks: n=1 is a separately stipulated invariant and is used; n=2 determines the free slope; n=3 provides the first obstruction. If λ=0 this first-order test is inconclusive. Rationally inverting x can invalidate the obstruction, so this argument addresses the actual ordinary ring. Finite interpolation of arbitrary tuples over a fraction field is irrelevant to integral coefficients. Allowing coefficients with poles at q=1 also changes the question.

Initial estimated review completion: 8%. This is an attempted independent counterexample mechanism, not a package acceptance verdict.

Actual attack completion UTC: 2026-10-16T17:52:10.761513Z
