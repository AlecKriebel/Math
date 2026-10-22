# Attempt 2: eliminating all first-Schouten-jet invariants

## Target and result

The conformally-flat argument leaves Cotton components. Here an elementary translation-span argument eliminates the entire P, nabla P class, at any negative weight, in every dimension n>=4. This is a scoped theorem; no statement about nabla^2 P or higher is implied. No novelty or full-resolution claim is made.

## Conventions and normalization

Put T_{kij}=nabla_k P_{ij} and use the Fefferman–Graham Cotton convention

    C_{ijk}=T_{kij}-T_{jik}.

Then C is skew in j,k, cyclically sums to zero, and all its traces vanish. The last property follows from div P=dJ. Let S=Sym(T) over all three slots. Directly,

    T_{kij}=S_{ijk}+(C_{ijk}+C_{jik})/3.                 (2.1)

Prescribing u(x)=0 and du(x)=0, its Hessian sets P_hat(x)=0; its third derivatives then set S_hat(x)=0. The leading coefficient of the symmetric third derivative in nabla P_hat is -1. This is the Schouten version of FG Proposition 8.4. Thus any fixed polynomial expression I(P,nabla P), evaluated in this gauge, is a polynomial F(C).

## Independence of the Weyl and Cotton data

Any algebraic Weyl tensor W and any trace-free Cotton tensor C can simultaneously occur at a point with P=0 and S=0. Here is an explicit finite-jet justification.

Define T from (2.1) with S=0. T has symmetry in i,j, cyclic sum zero, and all traces zero. Begin with a quadratic normal-coordinate metric jet having curvature W and Ricci zero. Such a jet is given by the standard quadratic normal-coordinate formula (equivalently FG Theorem 8.3 at order zero). Add the cubic metric term

    h_{ij}(x)= -[(n-2)/(n+1)] T_{kij} x^k |x|^2.      (2.2)

The quadratic and cubic terms do not interact in curvature or its first derivative at the origin, since first derivatives of the metric vanish there. The linearized Ricci formula

    Ric'(h)_{ij}=(partial_i partial^a h_{aj}
       +partial_j partial^a h_{ai}-Delta h_{ij}
       -partial_i partial_j tr h)/2

and the trace/cyclic identities of T give

    partial_k Ric_{ij}(0)=(n-2)T_{kij},
    partial_k R(0)=0.

Therefore nabla_k P_{ij}(0)=T_{kij}. For example, before multiplying by (n-2)/(n+1), the trial h=-T_{kij}x^k|x|^2 has Ricci derivative (n+1)T; this fixes the coefficient in (2.2). The metric is positive definite in a sufficiently small neighborhood; a cutoff gives a smooth local metric. This establishes the needed independence without assuming arbitrary unconstrained full curvature jets.

## Conformal covariance forces Cotton translations

Now start at P=S=0 with arbitrary (W,C). Prescribe u(x)=0 and du(x)=v arbitrarily. Choose Hess(u)=v tensor v-(|v|^2/2)g so that P_hat(x)=0, and choose the third jet to ensure S_hat(x)=0. The exact Cotton law (FG Proposition 6.5) is

    C_hat_{jkl}=C_{jkl}-v^i W_{ijkl}.                 (2.3)

Since u(x)=0, the metric and the value of a scalar conformal invariant at x are unchanged. Thus

    F(C-L_v W)=F(C),    (L_v W)_{jkl}=v^i W_{ijkl},   (2.4)

for every C, W, and v. These are independent variables by the preceding construction. In particular F is invariant under all translations in the linear span of the images of L_v.

## Elementary surjectivity of the translation span

No irreducibility assertion is needed. Given a trace-free Cotton tensor C and a vector v, define an algebraic curvature tensor

    R(v,C)_{ijkl}=v_i C_{jkl}-v_j C_{ikl}
                    +v_k C_{lij}-v_l C_{kij}.

The skew, pair-interchange and first Bianchi identities follow directly from the Cotton identities. Its Ricci tensor (the convention Ric_{jl}=sum_i R_{ijil}) is

    rho(v,C)_{jl}=v^i(C_{jil}+C_{lij}),

and its scalar trace is zero. Let

    W(v,C)=R(v,C)-(rho(v,C) Kulkarni–Nomizu g)/(n-2),

where (rho KN g)_{ijkl}=rho_{ik}g_{jl}+rho_{jl}g_{ik}
-rho_{il}g_{jk}-rho_{jk}g_{il}. W(v,C) is an algebraic Weyl tensor. For an orthonormal basis e_a, direct contraction gives

    sum_a R(e_a,C)_{ajkl}=n C_{jkl},
    sum_a (rho(e_a,C) KN g)_{ajkl}=3 C_{jkl}.

Consequently,

    sum_a L_{e_a} W(e_a,C)
      =[(n-3)(n+1)/(n-2)] C.                         (2.5)

The coefficient is nonzero for n>=4. Hence the translations in (2.4) span the entire Cotton space. Translation invariance can be composed, and scalar multiples are allowed by scaling W, so F(C)=F(0) for every C.

A negative-weight polynomial invariant has no constant monomial, so F(0)=0. Normalize every metric as above to conclude I=0 identically.

## Critical-weight implications and limits

Any nonzero counterexample to AIM Problem 10 must therefore require at least one factor with two or more covariant derivatives of P in every representative entirely within the proposed pure-Schouten class. In particular, the Cotton powers that can occur when n is a multiple of six cannot by themselves complete a P,nabla P invariant.

The condition n>=4 is essential: in dimension three W=0 and Cotton itself is conformally invariant. The factor n-3 in (2.5) correctly detects this exception. The proof also distinguishes the tensor Cotton law from the norm scaling, and always takes u(x)=0 when comparing polynomial values.

## Verification and attribution

checks/verify_cotton_span.py verifies exactly over rational arithmetic the Cotton identities, the Weyl projection, formula (2.5), and the cubic metric Ricci derivative in dimensions 4 through 8. The script checks the displayed formulas; the general proof is the symbolic contraction argument above, not finite sampling. FG, The Ambient Metric, Proposition 6.5, Proposition 8.4 and Theorem 8.3 are the primary geometric inputs. This may be standard invariant-theoretic folklore; priority is unestablished.
