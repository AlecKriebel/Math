# Turn 1: a non-self-dual quasi-supersingular special fiber with an explicit finite Honda lift

AI-assisted proof candidate; independent review pending. The answer to the exact universal self-duality question is negative. For every p>3 and every n≥3 the construction below works over k=an algebraic closure of F_p and W=W(k). Both the special fiber and the p-killed finite flat W-group are non-self-dual. Classical Dieudonne/finite-Honda classification is credited to the primary sources in SOURCE_GATE.md; novelty is not certified.

## 1. Conventions and the six-dimensional module

Use Hoshi's contravariant Dieudonne convention: F is sigma-semilinear and V is sigma^(-1)-semilinear, where sigma(a)=a^p. Their composites are zero on a p-killed module. Let M have k-basis e0,...,e5 and define

    F(e0)=e1, F(e1)=e2, F(e3)=e4;
    V(e0)=e5, V(e3)=e2, V(e5)=e4,

with all other basis images zero. Extend semilinearly, not k-linearly. All displayed coefficients lie in F_p. Directly FV=VF=0 and F^3=V^3=0. Moreover

    imF=kerV=span(e1,e2,e4),
    imV=kerF=span(e2,e4,e5).

Thus M is a deformable object in Hoshi Definition3.4, with no polarization assumed. By Proposition2.5 it corresponds to a finite commutative k-group scheme H killed by p, of rank p^6. The module is connected and so is its dual, but connectedness is not being substituted for quasi-supersingularity.

## 2. An explicit qss filtration

Define

    u=e1+e3+e5,  v=e2+e4,
    w=2e1+e3,   z=e2,
    a=e0,       b=e1.

These six vectors are a basis: the inverse formulas are e0=a, e1=b, e2=z, e3=w−2b, e4=v−z, e5=u−w+b, all with integral coefficients. In this basis the only nonzero images are

    F(u)=v, F(w)=v+z, F(a)=b, F(b)=z;
    V(u)=v, V(w)=z,   V(a)=u−w+b.

In particular M1=span(u,v) and M2=span(u,v,w,z) are F,V-stable, giving

    0 ⊂ M1 ⊂ M2 ⊂ M.

Each successive two-dimensional quotient has a basis (x,y) with F(x)=V(x)=y and F(y)=V(y)=0: use (u,v), (w,z), and (a,b) respectively. The equal-image, exact two-dimensional module is the module of E[p] for a supersingular elliptic curve over algebraically closed k; see Hoshi Lemma4.9 and its rank-two case.

Contravariance reverses this module filtration into a group filtration, without changing its factors. More explicitly, for i=0,1,2,3 let H_i be the subgroup of H with Dieudonne module M/M_(3−i), with M0=0 and M3=M. Exactness of the contravariant equivalence gives 0=H0⊂H1⊂H2⊂H3=H, with all H_i/H_(i−1) isomorphic to supersingular elliptic p-torsion. Thus H is quasi-supersingular in the exact source definition.

## 3. The duality obstruction is intrinsic

For any such module D, define

    delta(D)=dim_k(im F_D^2 ∩ im V_D^2).

A k-linear isomorphism commuting with the semilinear F,V carries both image subspaces to the corresponding image subspaces, so delta is an isomorphism invariant.

In M, the only nonzero second-iterate images are F²(e0)=e2 and V²(e0)=e4. Hence delta(M)=0.

Hoshi Definition2.3 gives F^D(phi)=sigma∘phi∘V and V^D(phi)=sigma^(-1)∘phi∘F on M^D=Hom_k(M,k). Because our matrices have coefficients in F_p, their matrices in the dual basis are respectively V^t and F^t, with the appropriate semilinearity. Thus (F^D)^2 sends e4* to e0*, and (V^D)^2 sends e2* to e0*, with every other basis vector sent to zero. Both images equal span(e0*), so delta(M^D)=1.

Consequently M is not isomorphic to M^D. Proposition2.5(2), which identifies module duality with Cartier duality, proves H is not isomorphic to its Cartier dual. No search over possible bilinear forms or unverified classification of cyclic words is needed.

## 4. A finite Honda system gives an actual W-lift

Take L=span(e0,e3,e5)⊂M, viewed also as a W-submodule through W→k. It is a direct complement to imF=span(e1,e2,e4). The map V restricted to L sends the displayed basis to e5,e2,e4; since k is perfect, this sigma^(-1)-semilinear map is injective.

Check every finite-Honda condition from Hoshi Remark3.5.1:

- N=M is a W-module of finite length6 and pN=0;
- F and V are semilinear for the Witt Frobenius and its inverse through reduction;
- FV=VF=0 equals multiplication by p on N;
- V|L is injective;
- pL=0 and the map L/pL→N/imF is an isomorphism, by the explicit complement.

Therefore (L,M,F,V) is a finite Honda system. Equivalently, L gives the deformation splitting in Definition3.5. Proposition3.11(2) gives an anti-equivalence with p-torsion finite flat commutative W-group schemes when p≠2, and Proposition3.11(5) identifies reduction with forgetting L. Since our p>3, every hypothesis holds. It produces a group scheme G/W killed by p whose special fiber is H. Its rank is p^6 because finite-flat rank is constant over the local base and the special fiber has that rank.

This is an explicit linear-algebra classification datum for the mixed-characteristic lift, not an unqualified claim that every finite group scheme lifts. No requirement that the qss filtration itself lift to W has been imposed: the source hypothesis is on the special fiber.

Cartier duality commutes with base change. If G were self-dual over W, reducing an isomorphism G≅G^D would make H self-dual, contradicting Section3. Hence G is not self-dual either.

## 5. Every n≥3

Let I be the two-dimensional module with basis x,y, F(x)=V(x)=y and F(y)=V(y)=0, equipped with Honda subspace span(x). For n≥3 form

    M_n=M ⊕ I^(n−3),  L_n=L ⊕ span(x)^(n−3).

The Honda conditions hold blockwise. Its corresponding special fiber has the preceding three-step qss filtration followed by the direct-sum elliptic factors, hence is qss of rank p^(2n). Since both F² and V² vanish on I, delta(M_n)=0 and delta(M_n^D)=1. Thus neither the special fiber nor its explicit Honda lift is self-dual for any n≥3.

## 6. Scope and finite controls

This refutes the universal assertion for perfect k by examples over algebraically closed k, for every allowed p>3. It does not classify all perfect-field forms, all qss groups, or all lifts. It does not produce a principally polarized Jacobian or refute the surrounding Coleman conjecture. The source already proves the n≤2 affirmative statement; no contradiction with that result is asserted.

The standard-library checker verifies the integer basis identities, exact F,V/Honda/duality ranks over several prime fields, all direct sums through n=12, and semilinear dual pairings over F_25. These controls supplement the symbolic all-p proof and the cited classification theorem. A full independent source/proof review is required before promotion or publication.
