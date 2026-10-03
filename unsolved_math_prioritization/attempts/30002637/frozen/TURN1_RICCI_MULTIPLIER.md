# Author turn 1: the soliton-potential times Ricci test

Date: 2026-10-03. Target 30002637 / OWR-13106-010. Outcome: unresolved; exact quotient test derived, no universal sign established. This is a substantive unsuccessful proof attempt, 1/5.

## Conventions and credited starting point

Let Ric + Hess f = g on a closed non-Einstein shrinker and normalize dμ=e^{-f}dV/∫e^{-f}dV. Write E for integration against dμ, u=f−Ef, s=|∇f|², A=|Ric|², and r=R. Let Δ_f=Δ−∇f·∇ and L=(1/2)Δ_f+Rm. The actual stability operator N, the gauge decomposition, and its reduction to L on V={div_f h=0, E〈h,Ric〉=0} are prior results of [Cao–Zhu](https://arxiv.org/abs/2304.01453). We use Q(h)=E〈Nh,h〉; its sign is the sign of the ν-Hessian, independent of the positive normalization factor.

Standard shrinker identities are Δ_f u=−2u, Δ_f r=2r−2A, div_f Ric=0, and L(Ric)=Ric. The spectral statement −Δ_f has first nonzero eigenvalue greater than 1 follows from weighted Bochner and compactness (and appears in the cited shrinker literature). These are prior identities, not new results.

## First obstruction: the unweighted natural span

The soliton equation gives Hess f=g−Ric. Since Hess f is a Lie derivative direction and g is scaling, the entire constant span of g, Ric, and Hess f is annihilated by N. Thus non-Einstein behavior does not convert the familiar positive L-eigenvalue of Ric into ν-instability. This eliminates the first naive candidate rather than establishing the target.

## Nonconstant Ricci multiplier

We next test h₀=u Ric. It is generally not gauge or pure scaling. Product differentiation gives

L(u Ric)=u L(Ric)+(Δ_f u/2)Ric+∇_{∇u}Ric=∇_{∇f}Ric.

Consequently

E〈Lh₀,h₀〉=(1/2)E[u∇f(A)]=E[(u²−s/2)A],

using div_f(u∇f)=s−2u². Also

div_f h₀=Ric(∇f,·)=(1/2)dr.

An explicit quotient representative is available. Let w have mean zero and solve

(Δ_f+1)w=(r−Er)/2.

The operator is invertible on mean-zero functions because every nonzero scalar drift eigenvalue is greater than 1. Since div_f Hess w=d(Δ_f w+w), the tensor

h=u Ric−Hess w−(c/m)Ric,

where m=Er=EA>0 and c=E(uA), lies in V. Integration by parts gives E〈Ric,Hess w〉=0. Gauge/scaling invariance implies Q(h)=Q(h₀).

## Exact sign formula

Take an orthonormal mean-zero scalar eigenbasis −Δ_f φ_j=μ_jφ_j, μ_j>1, and expand r−m=Σ_j r_jφ_j. In the N-formula, the auxiliary v solves (Δ_f+1)v=(1/2)Δ_f r, so

v=Σ_j μ_j r_j/[2(μ_j−1)] φ_j.

The divergence and auxiliary-function contributions combine as

(1/4)E|dr|²+(1/2)E[v(Δ_f+1)v]
=Σ_j μ_j(μ_j−2)r_j²/[8(μ_j−1)].

Therefore the exact Rayleigh numerator for this admissible test is

Q(h)=E[(u²−s/2)A]+Σ_j μ_j(μ_j−2)r_j²/[8(μ_j−1)]−c²/m.

This would prove the desired instability whenever its right-hand side is positive. It does not yet prove positivity for every non-Einstein soliton. The scalar spectral contribution is negative for 1<μ_j<2 and positive for μ_j>2; the moment term has no sign supplied by the basic identities; the projection term is nonpositive.

## Checks and remaining gap

- For an Einstein soliton, u=0 and r is constant: the whole formula is zero, consistent with removal of the scaling/Ricci line.
- Every term survives the f→f+constant freedom because u and dμ are unchanged.
- The correction h₀−Hess w removes the entire computed divergence, and the Ricci subtraction removes precisely its weighted Ricci pairing.
- The auxiliary contribution was computed with the negative-spectrum convention for Δ_f, preventing a false sign reversal.

The missing step is a genuinely new inequality making this numerator positive, or a different universally positive quotient tensor. Deriving that inequality from the same instability claim would be circular. No claim is made that this test is universally positive, universally nonpositive, or equivalent to the full problem. The unrestricted compact non-Einstein target remains open after this attempt.
