# A central-valued commutator word that is not polynomial

UTC: 2026-10-24T23:18:44.766302+00:00. **Proposed supporting countermodel, awaiting an independent adversary.** This is not a counterexample or solution to Kourovka21.122 and makes no originality claim. Full-problem discovery estimate **2%**.

## Claim and purpose

There is an explicit profinite solvable group of derived length exactly three on which the derived word

    δ2(x1,x2,x3,x4)=[[x1,x2],[x3,x4]]

has all its values in the centre, but its word map has no finite degree under the iterated right-difference definition of Passi polynomial maps. Thus the metabelian hypothesis in Zozaya2608.02237v1 Theorem4.4 cannot simply be removed to solve21.122 by the polynomial-map image lemma.

## Explicit profinite group

Let R=Z3, let V=R², and write omega(v,w)=det(v,w). The factor1/2 exists in R. Put

    N=V×R,  (v,z)(w,s)=(v+w,z+s+omega(v,w)/2).

This is the compact Heisenberg group. Its inverse is (-v,-z), and

    [(v,z),(w,s)]=(0,omega(v,w)),

using [x,y]=x^-1 y^-1 x y. Its centre contains Z={(0,z):z∈R}. Every M∈SL2(R) acts on N by (v,z)↦(Mv,z), because it preserves omega.

Take

    M=[[10,3],[3,1]], C=M^-1=[[1,-3],[-3,10]], B=C-I=[[0,-3],[-3,9]].

M≡I mod3. For u∈Z3 define M^u by the uniformly convergent binomial series

    M^u=sum_(k>=0) binomial(u,k)(M-I)^k.

The coefficients binomial(u,k) lie in Z3 and (M-I)^k is divisible entrywise by3^k. The series is continuous in u. The identity M^(u+v)=M^uM^v holds first for nonnegative integers and then for all u,v∈Z3 by density and continuity. Likewise det(M^u)=1 by continuity. Thus there is a continuous action of Z3 on N, and we form the compact semidirect product

    G=N semidirect Z3,

with t=(identity_N,1) acting by t(v,z)t^-1=(Mv,z). Its explicit quotients reduce v,z,u modulo3^r. The action descends because M^(3^r)≡I modulo3^r (indeed modulo3^(r+1)), by the binomial congruence. These finite3-groups separate points, so G is profinite, in fact pro-3.

G/N is abelian, so G'≤N. Therefore G''≤[N,N]≤Z, and Z is fixed by the Z3 action. Hence δ2(G)⊆Z(G) and G'''=1. The second derived subgroup is nontrivial by the explicit values below, so the derived length is exactly three.

## Exact one-variable slice

Let a=(e1,0) and b=(e2,0) in N. The horizontal coordinate of [a,t^n] is (C^n-I)e1, and that of [b,t] is Be2. Central coordinates of these inner commutators do not affect their outer commutator. Consequently

    δ2(a,t^n,b,t)=(0,f(n)),
    f(n)=det((C^n-I)e1,Be2), n∈Z.

Let ell(v)=det(v,Be2). Then Be2=(-3,9), so ell is nonzero, and

    f(n)=ell(C^n e1)-ell(e1), ell(e1)=9.

The sequence an=ell(C^n e1) has a0=9,a1=0 and satisfies

    a_(n+2)=11 a_(n+1)-a_n,

because C has trace11 and determinant1. In particular f(0)=0,f(1)=-9,f(2)=-18,f(3)=-108. Since f(1)≠0 in Z3, G'' is nontrivial.

## No finite Passi degree

For additive-valued maps put Δf(n)=f(n+1)-f(n). For every d>=1,

    Δ^d f(n)=ell(C^n B^d e1).                         (1)

Set vd=B^d e1. Since det(B)=-9 and det(e1,Ce1)=-3,

    det(vd,Cvd)=det(B)^d det(e1,Ce1)=(-9)^d(-3)≠0

in Q3. Thus vd,Cvd are linearly independent over Q3. The nonzero linear functional ell cannot vanish on both, so one of Δ^d f(0),Δ^d f(1) is nonzero. No iterated-difference degree bound exists.

If the full central-valued map δ2:G^4→Z3 were polynomial of degreeD, its left translate by (a,1,b,t) and restriction along the homomorphism n↦(1,t^n,1,1) would be polynomial of degree at mostD. Left translation and precomposition by a group homomorphism preserve the right-difference identities directly. This would make f polynomial, contradicting(1). Hence the word map is not Passi-polynomial of any finite degree.

## Why this does not refute21.122

The image can be identified exactly. The map

    G→(V/3V)×Z3,  ((v,z),u)↦(v mod3,u)

is a homomorphism into an abelian group, because M^u≡I mod3. Hence every first commutator has horizontal coordinate in3V and has u-coordinate zero. An outer commutator of two such elements therefore has central coordinate in9Z3. Conversely, for each r∈Z3, let a(r)=(r e1,0) in N. Then

    δ2(a(r),t,b,t)=(0,det(rBe1,Be2))=(0,-9r).

These values cover9Z3. Thus the **set** of δ2-values is exactly the central subgroup9Z3, and has cardinality continuum. This direct argument does not depend on any conciseness theorem. The sequence an is also negative and strictly decreasing for n>=2, giving a separate arithmetic infinitude check.

The exact image simplification was supplied by the independent adversarial reviewer. The example agrees with the prior DKS2020 theorem for multilinear commutators and lies in known linear/analytic positive classes. Its sole role is to falsify a proposed general **polynomial-map shortcut**.

## Primary definitions and scope

Zozaya, *Strong conciseness in profinite metabelian groups*, [arXiv2608.02237v1](https://arxiv.org/html/2608.02237v1), §4 defines Δ_h f(x)=f(x)^-1 f(xh), Proposition4.1 gives the polynomial image dichotomy, and Theorem4.4 explicitly requires metabelian G for central-valued commutator words. DKS, *Strong conciseness in profinite groups*, [arXiv1907.01344v2](https://arxiv.org/abs/1907.01344), Theorem1.1 supplies the known restricted-word background, which the direct image calculation is consistent with. No external theorem is needed for the group construction, exact word-value image, or nonpolynomiality proof.

The independent standard-library checker tests the explicit integer matrix identities, finite quotient actions, Heisenberg automorphism identities, recurrence and finite differences. Finite checks do not replace the all-degree determinant argument. No full21.122 solution, priority conclusion, paper or publication is claimed.
