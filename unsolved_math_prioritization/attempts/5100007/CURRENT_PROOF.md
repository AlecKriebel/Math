# Current proof and qualified scope

Published note: https://doi.org/10.5281/zenodo.23409879. The following October16 analytic derivation establishes the full primitive classification; the original positive proof is preserved separately. The exact contemporary positive theorem and overlapping mechanism are credited to Ferudun DOI10.5281/zenodo.23093258; no novelty or independent-discovery certification. The manuscript in draft_pr_publication_program_20260930/audits/pr200_5100007/publication_package_v2/outer_focal_period.tex is the publication version.

# Primitive parity classification for the outer one-focus product

Independent adversarial derivation, 2026-10-16 UTC. This document makes no novelty, priority, or publication-approval claim.

## 1. Exact theorem and inputs

Let E have semiaxes a>b>0 and foci F_+=(c,0), F_-=(-c,0), c²=a²-b². Fix a proper, strictly nested, nondegenerate confocal *elliptical* caustic with semiaxes α>β>0. Suppose the billiard family has primitive least period N≥3. Intersect the boundary tangents at consecutive billiard vertices to obtain Q_j. For either fixed focus define the ordinary positive product

    P_±(u) = ∏_{j=0}^{N-1} |Q(u+jδ)-F_±|.

Then P_± is independent of real phase u if and only if 4 divides N. The claim holds for every admissible coprime winding. When 4 divides N the two constants are equal. For every positive integer r, the product around r repeated traversals is P_±(u)^r, so repetition cannot restore phase independence to a nonconstant primitive product.

The established canonical parametrization is the only billiard-dynamics input:

    k=c/α ∈ (0,1),  k'=sqrt(1-k²),  0<v<K,
    a=α dn(v)/cn(v),   b=β/cn(v),   β=αk',
    P(u)=(-a sn(u), b cn(u)),   δ=2v,
    v=2Kτ/N,  gcd(τ,N)=1,  0<τ<N/2.

Here all Jacobi functions have modulus k; K=K(k), K'=K(k'). The real point parametrization has period 4K and is injective on that circle. Reversal lets us take the indicated positive winding. This input is credited to Stachel, Theorem 2 and (4.10) in [the preprint](https://arxiv.org/abs/2105.03624v2), corresponding to Theorem 4.3 and (4.9) in [the published paper](https://doi.org/10.1007/s40879-021-00524-2). The permitted original proof supplies that published input; this audit checks and extends the subsequent algebra/divisor mechanism rather than claiming a new proof of the canonical billiard parametrization.

As a consistency check on the caustic, addition formulas give the chord through P(u-v), P(u+v) as

    -x sn(u)/α + y cn(u)/β = 1.

It is tangent to the claimed caustic at (-α sn(u), β cn(u)). Also a²-α²=b²-β²=β² sn²(v)/cn²(v)>0. Thus none of the parameters used below silently introduces a hyperbolic or collapsed caustic.

## 2. Geometry and the paired meromorphic function

Solving the two boundary-tangent equations gives

    Q(u)=(-A sn(u), B cn(u)),
    A=a dn(v)/cn(v),   B=b/cn(v).

For completeness put s=sn(u), z=cn(u), d=dn(u), h=sn(v), C=cn(v), D=dn(v), D₀=1-k²s²h². Adding and subtracting the tangent equations at u±v gives

    -X s C D/a + Y z C/b = D₀,
    -X z/a - Y s D/b = 0.

Their solution is X=-a sD/C, Y=bz/C. For real u the determinant of the original equations is, up to orientation, 2hCd/(abD₀)>0. Thus every Q is finite. Moreover

    (Q_x/a)²+(Q_y/b)² - 1 = h² dn²(u)/C² > 0.

The foci lie strictly inside E, so all real distances used in P_± are strictly positive. The real functions P_± are therefore well defined and continuous. Their squares are locally real analytic. The outer parametrization has period 4K and

    Q(u+2K)=-Q(u).

The shift between the centered pair P(u±v) and the original sequence of consecutive endpoints is a fixed phase offset, immaterial when phase ranges over the family.

Define, algebraically and without choosing any complex square root,

    g_±(u)=(Q_x(u)∓c)²+Q_y(u)²,
    H(u)=g_+(u)g_-(u).

For real u, H(u)=(|Q(u)-F_+| |Q(u)-F_-|)²>0. Put

    κ=k²,  t=sn²(v),  q=1-t,
    U=1-2κt+κt²,  V=1-2t+κt²,  W=1-κt².

Direct substitution yields

    A=α(1-κt)/q,    B=αk'/q,
    A²-B²=α²κV/q²,    B²+c²=α²U/q².

Writing S=sn²(u), one obtains

    H(u)=α⁴/q⁴ [(U+κVS)² - 4κ(1-κt)²q²S]
        =α⁴/q⁴ (1-κS)(U²-κV²S).

The second equality follows by expansion using U+V=2q(1-κt); `check.py` verifies it as an exact polynomial identity. Double-angle formulas give cn(δ)=V/W and dn(δ)=U/W. Hence

    H(u)=C_v dn²(u) J(u),
    J(u)=dn²(δ)-k²cn²(δ)sn²(u),
    C_v=α⁴W²/q⁴>0.                                      (1)

No restriction on the parity of N has entered this factorization.

## 3. Exact divisor, with all collisions checked

Work on the compact connected torus

    T=ℂ/(2Kℤ+2iK'ℤ),    p=iK'.

The function sn² has precisely one double pole on T, at p; dn² has that double pole and a double zero at p+K. The needed shift is

    sn(z+K+iK')=dn(z)/(k cn(z)).

These standard Jacobi facts, including their periods and simple poles/zeros before squaring, were checked against [DLMF 22.4, Tables 22.4.1–3](https://dlmf.nist.gov/22.4). The identities used above are in [DLMF 22.6](https://dlmf.nist.gov/22.6) and [22.8](https://dlmf.nist.gov/22.8).

First suppose cn(δ)≠0. In the real range 0<δ<2K this excludes only δ=K. Then J has a double pole at p with nonzero leading coefficient. The shift identity gives J(p+K+δ)=J(p+K-δ)=0. These two points are distinct on T: equality would mean 2δ∈2Kℤ, which forces δ=K in the stated interval. Neither point equals p (again that would force δ=K), and neither equals p+K (that would force δ=0 or 2K). A degree-two meromorphic function with one double pole has two zeros counting multiplicity, so these distinct zeros of J are simple and exhaust its zeros. There is no collision with the double zero of dn². Therefore

    div(H)=2[p+K]+[p+K+δ]+[p+K-δ]-4[p].                  (2)

In particular, the order-four pole is genuine whenever δ≠K. The assumptions k>0 and cn(δ)≠0 prevent cancellation of its leading term.

If cn(δ)=0 then δ=K and J=k'² is a nonzero constant. Thus

    div(H)=2[p+K]-2[p].                                 (3)

From δ=4Kτ/N=K we get N=4τ. Primitivity gcd(τ,N)=1 then forces τ=1 and N=4. This is the only exceptional primitive case. It cannot occur in either parity class where necessity is at issue. Equivalently V=0 here and A²-B²=0: the outer ellipse becomes a circle, while the original ellipse remains noncircular. Formula (3), rather than (2), handles this degree drop.

## 4. Cyclic norm for every primitive period and winding

Let G be the subgroup of T generated by the real point δ. Its exact order is

    L = N/gcd(N,2),

because δ/(2K)=2τ/N and gcd(τ,N)=1. Explicitly, the subgroup of the real circle obtained after dividing coordinates by 2K is {j/L mod 1: 0≤j<L}, irrespective of the coprime generator. Define

    F(u)=∏_{j=0}^{L-1} H(u+jδ),
    O_x=∑_{g∈G}[x+g].

In the generic case (2), translation by ±δ merely permutes G. Summing translated divisors, with their multiplicities, therefore gives the exact formula

    div(F)=4 O_{p+K}-4 O_p.                              (4)

This step does not assert that individual H-factors have disjoint divisors. All collisions between different translated factors are combined in the divisor sum. Each orbit O_x has L distinct points. The two cosets p+K+G and p+G are either identical or disjoint; they are identical precisely when K∈G.

The normalized point K is 1/2, which belongs to the cyclic subgroup of order L precisely when L is even. Consequently

    K∈G  ⇔  L even  ⇔  4 divides N.                     (5)

For the excluded parities N odd and N≡2 mod 4, L is odd. Equation (4) then has L distinct zeros of order four and L distinct poles of order four, with no cancellation between these disjoint cosets. Hence F is a nonconstant meromorphic function. For 4|N and N≠4, equation (4) is zero, so F is constant. For N=4, equation (3) instead gives div(F)=2O_{p+K}-2O_p=0, since G={0,K}; again F is constant. In every constant case its value is finite and strictly positive because its factors are positive on the real line.

The implication from zero divisor to constancy uses compactness: a meromorphic function with zero divisor has no poles, so is holomorphic on the compact connected torus and is constant. Conversely the nonzero divisors just established forbid constancy.

## 5. Necessity: the real-phase and odd-period issue

There is no need to meromorphically continue the square root defining an ordinary one-focus distance. On the real phase line the geometric antipodal identity gives

    P_-(u)=P_+(u+2K).                                    (6)

This is an equality between products on two phase-shifted orbits. For odd N it does **not** identify an antipodal partner inside the primitive orbit.

Let r=N/L, equal to 1 for odd N and 2 for even N. Since H has period 2K and δ has order L on T, on the real line we have

    P_+(u)² P_-(u)²
      =∏_{j=0}^{N-1} H(u+jδ)
      =F(u)^r.                                          (7)

Suppose either P_+ or P_- were constant as real phase varies. Equation (6) makes the other constant as well. Thus F(u)^r would equal one fixed finite positive number for every real u.

Here is the precise analytic implication. F^r is meromorphic on T and has no poles on the real phase circle, because all H(u+jδ) are finite and positive there. At any point on that circle it is holomorphic in a complex neighborhood. Its difference from the fixed real constant vanishes on a real interval with an accumulation point in that neighborhood, so the holomorphic identity theorem makes it zero there. The meromorphic identity theorem on the connected torus makes it identically zero. Thus F^r would be a constant meromorphic function, whose divisor is zero. But for N odd or N≡2 mod 4, (4) says

    div(F^r)=4r O_{p+K}-4r O_p ≠0,

a contradiction. This proves necessity for **each** focus, every modulus 0<k<1, and every primitive admissible winding. It also proves that the nonconstancy occurs on the real family, not merely at complex phases. No within-orbit antipodal pairing has been invoked in this necessity proof.

## 6. Sufficiency and repetition

If 4|N, put L=N/2. Coprimality makes τ odd, so Lδ=2Kτ and

    Q(u+(j+L)δ)=-Q(u+jδ).

This time the antipodal point really is in the same primitive orbit. Pairing its two distances to the chosen focus gives

    P_+(u)=P_-(u)=∏_{j=0}^{L-1}|Q(u+jδ)-F_+| |Q(u+jδ)-F_-|,
    P_+(u)²=P_-(u)²=F(u).

Sections 3–4 prove that F is a positive constant, including N=4. Positivity then makes each P_± its unique positive square root. This proves sufficiency without selecting a complex square-root branch.

For r repeated traversals every positive distance occurs r times, so the repeated product is P_±^r. The map x↦x^r is injective on (0,∞). It follows that repeated constancy is equivalent to primitive constancy. In particular, repeating an odd or 2 mod 4 orbit enough times to make the traversal count divisible by four does not produce a new invariant.

## 7. Boundary and falsification status

- Circle k=0: excluded; the divisor mechanism degenerates and all periods have a constant one-focus product at the common center. Thus noncircularity is essential to necessity.
- Collapsed caustic, hyperbolic caustic, separatrix, and N=2: excluded by the statement and not inferred by a limiting argument.
- δ=K: checked explicitly; primitivity forces N=4, and the pole order drops from four to two.
- Odd N: treated through (6)–(7); the paired product is not equated with a single-focus product.
- All coprime stars: equations (4)–(5) depend only on the subgroup order, not its chosen generator.
- Nearly circular or large-period numerical families can look nearly constant. The universal obstruction is the exact nonzero divisor, not a finite numerical threshold.

The strongest result established here is the complete stated iff, subject to the standard published canonical parametrization stated in Section 1. No unresolved mathematical gap was found in the parity extension. Numerical controls are separately reproducible finite evidence and are not substituted for the proof.
