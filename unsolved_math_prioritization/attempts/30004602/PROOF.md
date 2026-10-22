# Corrected proof of 3-WLP for arrangement Jacobian quotients

**Status: corrected proof accepted by independent internal AI logical audit.** This is an authored repair of the argument underlying Marchesi-Palezzato-Torielli, Port. Math. 83 (2026), DOI [10.4171/PM/2155](https://doi.org/10.4171/PM/2155). It replaces their false Corollary 3.7 and avoids the false blanket equality p=D-m-2 on p. 9.

This AI-assisted correction edition is unrefereed. Acceptance records an independent internal AI logical audit, not external human peer review, author-approved erratum, journal acceptance, or formal proof-assistant certification.

The complete symbolic proofs, analytical formulas, and all-degree examples are retained. This is not a computational reproduction package: executable code, raw datasets and computational certificate tables, copied source documents and images, and private coordination material are excluded. Historical finite checks are corroboration only. The universal conclusions rest on the written arguments and explicitly named standard dependencies. The historical computations cannot be reproduced from this edition alone.

The characteristic-zero arrangement theorem survives with an explicit proof correction. The published proof is rejected unchanged. No new theorem, target counterexample, novelty, priority, current-openness, or complete current-literature-audit claim is made.

**Exact theorem.** Let K be any characteristic-zero field and let Q be the product of the defining linear forms of a finite central arrangement of distinct hyperplanes in K^3. In the standard grading, S/J(Q), where S=K[x,y,z] and J(Q)=(Q,Q_x,Q_y,Q_z), has 3-WLP. This means three successive degree-one maximal-rank multiplication maps after each preceding form is killed, in every graded degree. The original quotient need not be Artinian. Repeated hyperplanes and positive characteristic are outside the theorem.

## 1. Setup and allowed standard inputs

Initially work over an algebraically closed field of characteristic zero. Let S=K[x0,x1,x2], let I=(f0,f1,f2) be homogeneous of height two, let di=deg(fi), and put D=d0+d1+d2. In the arrangement application all three generators are nonzero, independent, and have the same positive degree. Let Z be the nonempty zero-dimensional projective scheme of I, A=S/I^sat, M=S/I, and N=I^sat/I.

The following standard ingredients are retained as named black boxes, with no claim to reprove their foundational statements:

1. Cohomology of line bundles on P^2 and P^1, including H^1(P^2,O(t))=0 for all t; Serre duality on P^2; H^1(P^1,O(t))=0 for t>=-1.
2. For a semistable rank-two bundle on P^2 in characteristic zero, the splitting on a general line is balanced (the Grauert-Mulich theorem, cited in the published article via Okonek-Schneider-Spindler, *Vector bundles on complex projective spaces*, II, Corollary 2). For first Chern class -D, the summands are O_L(-floor(D/2)) and O_L(-ceil(D/2)).
3. Galligo's characteristic-zero generic-initial-ideal theorem, and the reverse-lex identity for Hilbert functions of generic linear sections. The latter is the ingredient explicitly used in Palezzato-Torielli 2022, Theorem 3.6, citing Conca, *Reduction numbers and initial ideals*, Proc. AMS 131 (2003), Lemma 1.2. The elementary rank consequence is derived in Section 5 below.

Standard commutative-algebra facts used are the depth lemma/Auslander-Buchsbaum over a regular local ring, the equivalence between a saturated homogeneous ideal and its projective ideal sheaf in nonnegative degrees, and finite generation. These are not experimental assumptions.

The first syzygy sequence is

0 -> T -> E=direct_sum_j O_P2(-dj) -> I_Z -> 0.

The kernel T is locally free of rank two: at a point of Z its local module is the first syzygy of an ideal of finite colength in a regular local ring of dimension two and is free; outside Z this is immediate. Its determinant is O(-D). Put m=min{t : H^0(T(t)) != 0}. Cohomology of the sequence gives natural, multiplication-compatible isomorphisms

N_i = H^1(T(i)).

A general linear form ell avoiding the support of Z acts injectively on A in every degree. Write p for the least degree from which its Hilbert function is constant. Then ell:A_i -> A_(i+1) is bijective for i>=p. No Artinian hypothesis on M is introduced.

## 2. A safe replacement for the printed equality

The needed statement is only

p <= D-m-2.                                                     (1)

Here is a proof which remains valid even when the first syzygy is Koszul.

Let t=p-1. The group H^1(I_Z(t)) is nonzero. If p>0, its dimension is length(Z)-dim A_t, positive by minimality of p and injectivity of multiplication on A. If p=0, take t=-1; H^0(O(-1))=0 whereas H^0(O_Z(-1)) has dimension length(Z)>0, giving the same nonvanishing.

The long exact sequence from T(t)->E(t)->I_Z(t), together with H^1(E(t))=0, injects H^1(I_Z(t)) into H^2(T(t)). By Serre duality and the rank-two identity T^*=T(D),

H^2(T(t))^* = H^0(T(D-t-3)).

Consequently H^0(T(D-p-2)) is nonzero, so m<=D-p-2. This is (1). No formula concerning essential/Koszul syzygies is needed.

## 3. Correct bounds for multiplication on N

These reproduce the usable part of published Proposition 3.6, with all shifts displayed.

### 3.1 Split bundle

If T splits into line bundles, H^1(T(i))=0 for every i, so N=0. M=A and any general ell is injective in all degrees. This already gives WLP.

### 3.2 Unstable, nonsplit bundle

Strict instability means m<D/2. A minimal section gives an exact sequence

0 -> O(-m) -> T -> I_Y(m-D) -> 0,                               (2)

where Y is a nonempty finite scheme. There is no divisorial zero part, since removing it would give a section at a smaller twist. If Y were empty, the extension of line bundles would split because H^1(P^2,O(t)) always vanishes. This explains the nonempty assertion and handles the split case separately.

Choose a general line L avoiding Y and Z. Restricting (2) gives a split extension, since H^1(O_L(D-2m))=0. Hence

T|L = O_L(-m) + O_L(m-D).

For t<=D-m, the quotient contribution H^0(I_Y(t+m-D)) is zero, including t=D-m because Y is nonempty. Thus

H^0(T(t)) = H^0(O(t-m))  for t<=D-m.

In the restriction sequence

0 -> T(i) --ell--> T(i+1) -> T|L(i+1) -> 0,

the second summand of the restriction has no section for i<D-m-1. The sections of the first summand lift by the previous identification and the ordinary restriction of plane polynomials. Therefore

ell:N_i -> N_(i+1) is injective for i<=D-m-2.                    (3)

Serre duality identifies the transpose of this multiplication map with the multiplication map on H^1(T(j)), where

j=D-i-4.

Thus (3) also gives

ell:N_i -> N_(i+1) is surjective for i>=m-2.                     (4)

Only these sufficient bounds are needed. No assertion of a universal switch at p, and no sharpness assertion, is used.

Set c=max(p,m-2). By (1) and m<D/2,

c<=D-m-2.

For every nonnegative i<c, (3) gives injectivity on N. For every i>=c, (4) gives surjectivity on N, and i>=p gives bijectivity on A. This is the overlap needed for M.

### 3.3 Semistable bundle

Semistability gives m>=ceil(D/2). The balanced general-line splitting and the same restriction sequence yield the following bounds. If D=2r, multiplication on N is injective for i<=r-2 and surjective for i>=r-2. If D=2r+1, it is injective for i<=r-2 and surjective for i>=r-1. The surjective bounds also follow by substituting j=D-i-4 into the injective bounds.

Let c=floor((D-3)/2). In both parity cases, multiplication on N is injective for i<c and surjective for i>=c. Moreover (1) and semistability give

p<=D-ceil(D/2)-2<=c.

Therefore multiplication on A is bijective whenever i>=c. This establishes the same overlap as in the unstable case. It does not assert surjectivity on N at i=p when p<c; that is exactly the false assertion exposed by four lines.

## 4. Transfer to M and apply to arrangements

Apply multiplication by ell to the exact sequence

0 -> N -> M -> A -> 0.

Since multiplication on A is injective, the Snake lemma identifies the kernels for N and M and gives a short exact sequence of their cokernels ending with the cokernel on A. Hence:

- injectivity on N implies injectivity on M;
- surjectivity on N and on A implies surjectivity on M.

Sections 3.1-3.3 therefore give maximal rank for multiplication on M in every nonnegative degree. This is WLP. The threshold c varies with the bundle and need not equal p.

### Essential arrangements

For an essential central arrangement of d distinct planes in K^3, Euler's formula gives J=(Q_x,Q_y,Q_z), with all degrees e=d-1. Its height is exactly two. Indeed any common irreducible factor of the derivatives would, by Euler, divide Q; at a smooth generic point of its corresponding hyperplane, a derivative normal to that hyperplane is nonzero, contradiction. Thus height is at least two. The intersection line of any pair of arrangement hyperplanes lies in the Jacobian zero set, so height is at most two.

The three partial derivatives are linearly independent: a constant directional derivative annihilating Q would annihilate every distinct linear factor, forcing that direction into the center of the arrangement, which is zero by essentiality. Thus this is precisely the height-two, three-generator situation just treated. WLP follows from the corrected argument with the named standard inputs; the independent logical acceptance is recorded in AUDIT.md, Part II.

### Nonessential arrangements and degenerate cases

If the arrangement has rank two, choose coordinates with Q in K[x,y]. Then

S/J = (K[x,y]/(Q_x,Q_y))[z].

Multiplication by z is injective in every degree. After quotienting by z, the two-variable quotient has 2-WLP, by Section 5. Thus the original quotient has 3-WLP directly. The partial derivatives of a squarefree binary product are relatively prime, but even that fact is not needed for this polynomial-extension argument.

A rank-one arrangement, being a set of distinct hyperplanes, consists of one hyperplane. Its Jacobian ideal is S. The empty arrangement has Q=1 and also J=S. In either case all graded quotient components are zero and the requisite maps have maximal rank trivially. These cases should not be forced into the height-two argument or into a definition of p0 with an empty minimum.

### Descent from the algebraic closure

The arrangement and every graded multiplication matrix are defined over the original characteristic-zero field K, which is infinite. A good ell over the algebraic closure implies that the finitely many necessary maximal-rank minors define a nonempty open condition over K, so one can choose ell over K. Only finitely many degrees are needed: N is finite length and A has constant Hilbert function after p; beyond their bounds, a form avoiding the finite support of Z is automatically an isomorphism on M's tail. For the successive two-variable quotients, reverse-lex generic-section arguments likewise impose only a finite open condition (equivalently one may use the finite regularity truncation in Palezzato-Torielli 2022, Section 5). Successive choices can therefore all be made over K. No uncountable-field assumption is being made.

## 5. Complete 3-WLP and generic-initial bridge

### 5.1 Why two-variable quotients have 2-WLP

Let B be a strongly stable monomial ideal in K[u,v], ordered u>v. If multiplication by v from degree k to k+1 has a nonzero monomial kernel, choose a minimal generator t dividing v times such a kernel monomial. This t must involve v. Let a=deg(t)<=k+1. Strong stability gives u^a in B, hence u^(k+1) in B. But the cokernel of multiplication by v in target degree k+1 is spanned by the class of u^(k+1). It is therefore zero. Thus multiplication by v cannot have both nonzero kernel and nonzero cokernel, and has maximal rank in every degree.

After quotienting by v, the ring is a homogeneous quotient of K[u]. Multiplication by u has maximal rank in every degree, including the zero and polynomial-ring cases. Thus (v,u) gives 2-WLP for the monomial quotient.

For a homogeneous ideal I, characteristic zero makes its reverse-lex gin strongly stable. The generic-section Hilbert-function identity implies that the rank of multiplication by a general form equals the rank of multiplication by the last variable on the gin quotient: use the identity

rank(ell:R_(d-1)->R_d) = dim R_d - dim(R/ell R)_d.

Applying the same identity to successive generic sections transfers k-WLP. This is the WLP part of Palezzato-Torielli 2022 Theorem 3.6; it does not assume Artinianness. Therefore every standard-graded homogeneous quotient of K[u,v] has 2-WLP.

### 5.2 WLP implies 3-WLP in three variables

Take a Lefschetz form ell1 for a homogeneous quotient of K[x,y,z]. Modulo ell1 the algebra is a homogeneous quotient of a polynomial ring on at most two variables. Apply Section 5.1 to choose ell2 and ell3 successively. These forms can be lifted to the original degree-one vector space. The converse is immediate from the definition. This reconstructs the WLP case of the 2022 Corollary 4.9, rather than confusing WLP with 3-WLP by terminology alone.

### 5.3 The generic-initial condition is exactly equivalent

Let B=rgin(J) in variables x>y>z, and suppose B is proper with p0=min{p:y^p in B} finite, as holds in the nonzero height-two arrangement case. Such finiteness also follows directly from strong stability and dim S/B=1: the radical of a strongly stable height-two monomial ideal is (x,y).

If every minimal generator divisible by z has degree at least p0, then for target degree d<p0 multiplication by z is injective. Otherwise a kernel monomial would yield a minimal generator divisible by z of degree at most d. For target degree d>=p0, strong stability of y^p0 implies that all degree-d monomials in x,y lie in B. Thus multiplication by z is surjective. This proves WLP and hence, by Section 5.2, 3-WLP.

Conversely, suppose a minimal generator t divisible by z has degree g<p0. Minimality gives t/z outside B, a nonzero kernel class in source degree g-1. The class y^g is a nonzero cokernel class in target degree g. Multiplication by z then fails maximal rank. By the same gin/generic-section transfer this contradicts WLP, and a fortiori 3-WLP.

This proves the equivalence announced as OWR Theorem 10 and the forward implication in 2022 Proposition 8.5. It also proves precisely the conclusion of 2026 Corollary 3.8 by the corrected WLP argument accepted in AUDIT.md, Part II. Reindexing (x,y,z)=(x0,x1,x2) gives its Theorem 4.7 condition without changing any inequality.

## 6. Dependency boundary and acceptance

The corrected overlap uses no assertion from the false Corollary 3.7 and no use of the false blanket equality p=D-m-2. It reconstructs the usable part of Proposition 3.6 and the diagram argument in Lemma 2.7. Dimca-Popescu's theorem supplies context for identifying the erroneous citation, but the corrected proof does not rely on that theorem as an additional black box.

The independent logical audit accepts this correction, including the saturation inequality, rank-two duality shift D-i-4, threshold overlap, arbitrary-field descent, and gin-section transfer. Its complete reconstruction and dependency boundary appear in AUDIT.md, Part II. This acceptance does not validate the printed argument unchanged or certify the foundational proofs of the named standard inputs.

## 7. Complete all-degree defect examples

The following independent reconstruction is retained from the logical acceptance review. These examples refute two intermediate printed assertions; neither refutes the theorem. Finite-check observations are historical supporting evidence and are not used in the all-degree arguments.

### Independent four-line reconstruction

Take K=Q, s=x+y+z and Q=xyzs. The normals to x,y,z span K^3, so the arrangement is essential. All four factors are distinct and central. Euler's identity gives

J=(Q_x,Q_y,Q_z)=(yzs+xyz,xzs+xyz,xys+xyz).

Thus each generator has degree 3 and D=9. The three cubics are independent, and the ideal has height two. The projective singularities are precisely the six pairwise intersections

[0:0:1], [0:1:0], [1:0:0], [0:1:-1], [1:0:-1], [1:-1:0].

There is no triple intersection in P^2. Locally at each point, Q is a unit times the product of two parameters. The localized Jacobian ideal equals the point's maximal ideal: its two local derivatives have independent linear terms, so Nakayama's lemma applies. Away from these six nodes the projective Jacobian ideal is the unit ideal. Its saturation is therefore the reduced six-point ideal.

Put q0=yzs, q1=xzs, q2=xys and q3=xyz. That six-point ideal is (q0,q1,q2,q3). Here is a degree-independent verification. Restrict a homogeneous form h vanishing at the six points to x=0. The restriction vanishes at the three distinct points on that line and so is divisible by yz(y+z); subtract a multiple of q0. The remainder is xg. At the other three points x is nonzero. In the independent coordinates y,z,s those points are the coordinate points, whose homogeneous ideal is (yz,ys,zs). Hence xg belongs to (q3,q2,q1). In degrees below 3 the same argument says h=0; constant-degree cases are immediate.

The degree-two evaluation matrix in the six monomials is nonsingular (the independently reconstructed determinant is 1 with the stated ordering). Indeed, evaluations at the coordinate points determine the square coefficients, and the other three evaluations determine the mixed coefficients. Consequently the saturated Hilbert function is 1,3,6,6,...: to see the full tail, multiply interpolation quadrics by powers of ell=x+2y+3z, which takes the nonzero values 3,2,1,-1,-2,-1 at the six points. Thus F=1+2t+3t^2 and p=2.

The four q's are independent cubics, while J_3 has basis q0+q3,q1+q3,q2+q3. The module N=J^sat/J is therefore generated by a nonzero cubic class q3. The polynomial identities

xq0=yq1=zq2=sq3

show that (x+s)q3, (y+s)q3 and (z+s)q3 vanish modulo J. The coefficient matrix of these three linear forms has diagonal 2 and off-diagonal 1, with determinant 4. Therefore x,y,z annihilate the class and N=K(-3), in all degrees.

In particular source N_2=0 and target N_3=K. For every linear form, N_2 -> N_3 is nonsurjective. This source degree is i=p=2, exactly within the printed corollary. All its standing hypotheses are satisfied. For M=S/J the Hilbert function is 1,3,6,7,6,6,..., so source degree 2 also contradicts the stronger surjectivity assertion in the printed proof of Theorem 3.3.

There is no failure of WLP here. The same ell gives injections through source degree 2, surjections from source degree 3, and isomorphisms from source degree 4. These statements follow in every degree from N=K(-3) and the saturated quotient, not from a truncated rank table. The separate exact-rational reconstruction through source degree 8 agrees. It also gives minimal total syzygy degree m=5, so the corrected semistable threshold is c=3, as it should be.

### The blanket equality also needs replacement

For I=(x^2,y^2,xz^4), D=9 and I^sat=(x,y^2). To check saturation, the localization at z gives (x,y^2), whose projective support is the single point [0:0:1]; algebraically every degree-five monomial times x belongs to I, so x belongs to I^sat. The reverse containment follows because (x,y^2) is saturated. Its quotient has Hilbert function 1,2,2,..., hence p=1.

The relation (y^2,-x^2,0) has total degree 4. No smaller relation exists: the third coefficient would have negative degree and the two relatively prime quadrics have no relation below total degree 4. Thus m=4 and D-m-2=3, not 1. This is within the height-two, three-generator setting of Section 3.2. The weaker inequality used by the correction is essential to the stated generality.
