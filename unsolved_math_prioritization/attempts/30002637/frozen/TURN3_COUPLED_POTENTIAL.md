# Author turn 3: a coupled potential–Ricci/conformal pencil

Date: 2026-10-03. Target 30002637 / OWR-13106-010. Outcome: unfinished. The two-dimensional test reduces to an explicit matrix, but no universal positive eigenvalue is proved.

## Aim

The first multiplier test need not have a prescribed sign. A different possibility is that mixing u Ric with u g always gives an indefinite quadratic form, even when either individual numerator is nonpositive. This is a genuine attempt to exploit the coupling rather than assuming one diagonal entry positive.

We use the normalization, probability measure, and letters of turn 1: Ric+Hess f=g, u=f−Ef, s=|∇f|², A=|Ric|², r=R, m=Er>0. The existing ν-stability operator and quotient theorem of [Cao–Zhu](https://arxiv.org/abs/2304.01453) remain prior credit. All derivatives and pairings below are weighted by dμ.

## Gradient-divergence projection for the whole pencil

Set H_R=u Ric and H_G=u g. Their weighted divergences are

div_f H_R=d(r/2),   div_f H_G=d(u−u²/2).

For H=pH_R+qH_G, define a=p r/2+q(u−u²/2), solve (Δ_f+1)w=a−Ea, and put

P(H)=H−Hess w−[E〈H,Ric〉/m]Ric.

Then P(H) lies in the true quotient V and Q(P(H))=Q(H). This construction does not assume a raw positive L-direction descends to a positive ν-direction.

Let c=E(ur). From Δ_f r=2r−2A and Δ_f u=−2u,

E(uA)=2E(ur)=2c.

Thus E〈H,Ric〉=(2p+q)c. In particular H_R−2H_G is already Ric-orthogonal, although its divergence still needs removal.

## Exact quadratic matrix

Let −Δ_f φ_j=μ_jφ_j, μ_j>1, and let r_j and a_j be the mean-zero coefficients of r and a_G=u−u²/2. Define

k_j=μ_j(μ_j−2)/[2(μ_j−1)].

For tensors with divergences da and db, the combined divergence/auxiliary-function contribution to the polarized ν-Hessian is Σ_j k_j a_j b_j. It follows that Q(pH_R+qH_G) is the quadratic form with entries

q_RR=E[(u²−s/2)A]+Σ_j k_j r_j²/4−4c²/m,

q_GG=E[u²(r−n)]+Σ_j k_j a_j²−c²/m,

q_RG=E[u²(A−r)]+Σ_j k_j(r_j/2)a_j−2c²/m.

For the mixed leading term, self-adjointness and L(ug)=u(Ric−g) give E〈L(u Ric),ug〉=E[u²(A−r)]. Equivalently this is E[(2u²−s)r], consistent with direct integration by parts.

A strictly positive eigenvalue of this 2×2 matrix is a sufficient instability certificate. Positive trace or negative determinant would suffice. Neither sign follows from the identities currently available.

## Trying the forced scalar identities

The normalized soliton identities yield r+s=n+2u. Weighted integration by parts gives

Es=2Eu²,   E(us)=Eu³,   E(u²s)=(2/3)Eu⁴,

m=n−2Eu²,   c=2Eu²−Eu³.

In particular m>0 bounds the potential variance by n/2. The potential u belongs to scalar drift eigenvalue 2, where k_j=0. Therefore the forced nonconstant eigenfunction does not itself create a positive scalar correction. The coefficients of u² outside this eigenspace and their correlation with r remain essential.

The Ricci-orthogonal choice H_R−2H_G is also gauge-equivalent to df⊗df−u g because Hess(u²)/2=u Hess f+df⊗df. This identifies the corresponding gradient-square tensor but does not fix its sign: its divergence is −d(u²+r)/2, so an auxiliary correction remains.

## Outcome and exact obstruction

The matrix has a negative-semidefinite rank-one scaling-projection term, a scalar correction whose coefficients change sign at μ=2, and curvature/potential moments without a known dominating inequality. The identities above do not presently prove positive trace, negative determinant, or a positive Rayleigh quotient in any fixed coefficient direction.

This attempt neither establishes nor refutes that the pencil works for every non-Einstein shrinker. Replacing the unknown matrix-sign assertion by the desired conclusion would only relocate the problem. A general tensor outside this pencil remains possible; no inference is made from failure to certify these two directions to ν-stability of any soliton.
