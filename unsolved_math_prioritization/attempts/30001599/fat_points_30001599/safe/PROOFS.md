# Authored proofs and exact scope

## 1. Target and conventions

Let k be an algebraically closed field of characteristic zero, n>=1, and X a nonempty finite set of distinct k-points of P^n. Write R=k[x_0,...,x_n], I=I(X),

    I^(m) = intersection over P in X of I(P)^m,
    a_m = alpha(I^(m)) = min{d : (I^(m))_d != 0},
    a = a_1, m_r = n(r-1)+1, B_r = r*a+(r-1)(n-1).

The target is a_(m_r)>=B_r for every integer r>=1. Both n and X are arbitrary. The multiplicity is uniform at all points. No generic-position hypothesis may be added. Nonempty X avoids the unrelated alpha convention for the unit ideal. The source paragraph does not explicitly state a ground field; characteristic zero is the explicit scope of the direct 2014 follow-up and of our differential proofs. No conclusion for an unspecified larger characteristic scope is inferred.

Source identification: Susan Marie Cooper, “Hilbert Functions and Initial Degrees of Fat Points,” in OWR 45/2010, p. 2626, Conjecture 1; https://ems.press/content/serial-article-files/46305 . The numerical formulation also appears as Conjecture 4.1.8 in Harbourne--Huneke, https://arxiv.org/abs/1103.5809 . These are attribution, not claims that our package resolves either source.

## 2. Differentiation and boundary cases

**Lemma 2.1.** For integers m>=1 and t>=0, a_(m+t)>=a_m+t.

Proof. Take nonzero homogeneous F in I^(m+t) of degree d. Its vanishing at even one point implies d>=m+t. In characteristic zero a nonconstant homogeneous polynomial has a nonzero first partial derivative. Repeating this t times, choosing a nonzero partial at each stage, gives a nonzero homogeneous derivative D of degree d-t. Differentiation lowers local vanishing order by at most one: after a projective linear change placing a point at [1:0:...:0], this follows termwise for the ideal (x_1,...,x_n)^(m+t). Hence D lies in I^(m), and d-t>=a_m. Minimize over F. QED.

In particular a_(m_r)>=a+m_r-1. The difference between the desired bound and this proved lower bound is

    B_r - (a+m_r-1) = (r-1)(a-1).

Thus differentiation alone closes only r=1 or a=1. If a=1, X lies in a hyperplane L=0 and L^m gives a_m<=m; the one-point lower bound gives a_m>=m. So a_m=m and the target is equality, in every characteristic. For n=1 and s=|X|, the distinct linear equations of the points are pairwise coprime; their m-th powers have product degree ms and generate the intersection. Thus a_m=ms, m_r=r, and again the target is equality in every characteristic.

The standard containment I^(nr) subset I^r only gives a_(nr)>=r*a. Lowering the symbolic exponent is not justified by ideal containment. Applying Lemma 2.1 gives a_(nr)>=a_(m_r)+(n-1), an upper estimate for a_(m_r) in terms of a_(nr), not the needed lower estimate.

## 3. Waldschmidt reduction and its exact gap

The product inclusion I^(u) I^(v) subset I^(u+v) shows a_(u+v)<=a_u+a_v. Define w=inf_(m>=1) a_m/m. To verify this is also the limit, fix q and write m=tq+j with 0<=j<q. Set a_0=0. Subadditivity gives a_m<=t*a_q+a_j, so limsup a_m/m<=a_q/q. Taking the infimum over q and comparing with the defining lower bound proves lim a_m/m=w. In particular a_m>=m*w for every m.

Let

    L=(a+n-1)/n, C=(n-1)(a-1)/n.

Direct expansion gives B_r=m_r*L+C. Consequently:

- If w>=B_r/m_r, the target follows.
- Because a_(m_r) is an integer, the weaker strict condition w>(B_r-1)/m_r also suffices.
- If w>=L+delta for delta>0, then the target follows whenever m_r*delta>=C. It also follows from the slightly sharper strict inequality m_r*delta>C-1.
- If the target holds for all r, taking the subsequential limit gives w>=L. The reverse implication does not follow from this calculation.

The threshold B_r/m_r equals L+C/m_r. For n>=2,a>1 it decreases strictly with r. Thus a Waldschmidt estimate that passes r=2 passes every r>=2. However, equality w=L leaves the constant C untreated. Integer rounding by itself closes that deficit exactly when C<1: writing B_r as an integer, ceil(B_r-C)>=B_r iff C<1. For n>=2 and integer a>=1, this holds when a<=2. For example n=2,a=3 gives C=1, leaving exactly one degree missing for every r.

These are elementary conditional criteria, not new estimates for w. The Chudnovsky assertion is w>=(a+n-1)/n; the Demailly assertion is w>=(a_q+n-1)/(q+n-1) for every q>=1. The latter has an independent multiplicity parameter q. Substituting q=m_r does not supply the desired lower bound on a_(m_r); that variable is then on the right side of an upper constraint involving w. The plane versions and recent generic-point results must be used with their actual hypotheses.

For comparison, the uniform plane Nagata assertion concerns sufficiently many very general points, their number s, and degree-to-multiplicity ratio sqrt(s). It is not a statement for arbitrary configurations and does not have the same right side as this target. We do not use Nagata as a theorem here.

## 4. Complete proof of the sharp star-configuration family

Let s>=n hyperplanes H_1,...,H_s in P^n be in linear general position: any n of them meet in one point and no n+1 meet. Let X consist of all these n-fold intersection points. For n=1 this means s distinct points. Then, over characteristic zero,

    a = s-n+1,
    a_(n(r-1)+1) = r*s-n+1 = r*a+(r-1)(n-1)

for every r>=1.

**Upper bound.** Write H_i=(L_i=0). Let Q=product_(i=1)^s L_i and G=product of any s-n+1 of the L_i. At each point of X exactly n of the L_i vanish, and at least one of those n appears in G, since only n-1 factors were omitted. Therefore Q^(r-1)G has multiplicity at least n(r-1)+1 and degree r*s-n+1.

**Lower bound.** Induct on n, and within each dimension on r. The dimension-one case was proved in Section 2. For n>=2 suppose a nonzero F has degree d<r*s-n+1 and multiplicity at least m=n(r-1)+1 at X. On H_i, the subset X intersect H_i is the point star formed by the other s-1 hyperplanes in dimension n-1. By the dimension induction, its initial degree at multiplicity m'=(n-1)(r-1)+1 is

    r*(s-1)-(n-1)+1 = r*(s-1)-n+2.

Lemma 2.1, applied within H_i, raises this lower bound by m-m'=r-1. Thus any nonzero restriction F|H_i would have degree at least r*s-n+1, contrary to d. Hence every L_i divides F, so Q divides F.

If r=1, d<s-n+1<=s, while Q has degree s, an impossibility. If r>=2, the residual F/Q has degree d-s<(r-1)*s-n+1 and multiplicity at least m-n=n(r-2)+1 at every point of X. The induction on r is contradicted. This proves the lower bound. Setting r=1 also proves a=s-n+1. QED.

This is a full proof of a known equality family, not a full solution or a claimed new family.

## 5. Specialization, equal Hilbert functions, and exact witnesses

For fixed degree d and multiplicity m, vanishing of jets at a configuration of affine points is a linear system in the coefficients of a degree-at-most-d polynomial. After homogenization this describes degree-d forms on P^2. The matrix entries are polynomial expressions in the point coordinates. A nonzero maximal minor remains nonzero on a Zariski-open set. Therefore a full-column-rank example proves nonexistence at that degree for general configurations in that open set. It says nothing universal about configurations where that minor vanishes. Specialization may increase the kernel and decrease alpha.

Here is an explicit reason that the reduced Hilbert function cannot substitute for symbolic-power information. Work over Q, or its algebraic closure. Let

    S={(0,0),(0,1),(0,3/2),(1,0),(3,0),(-1,2)},
    T={(0,0),(1,0),(0,1),(2,3),(4,2),(3,5)}.

S is the intersection set of four lines x=0, y=0, x+y=1, x+2y=3; they have no triple intersections. The executable controls verify full column rank modulo 1009 for the six degree-at-most-two monomials at both sets. All denominators are invertible modulo 1009. Nonzero minors modulo this prime lift to nonzero rational minors, so both sets have no conic and have reduced Hilbert function (1,3,6,6,...). Indeed evaluation rank is 6 in degree two and remains 6 for every higher degree since the spaces of affine polynomials are nested. The ranks in degrees zero and one are 1 and 3.

Section 4 proves a_3(S)=7 and a_5(S)=11. For T, exact modular matrices have full column rank at (d,m)=(7,3) and (11,5), of ranks 36 and 78 respectively. Thus a_3(T)>=8 and a_5(T)>=12. At degree eight, 45 coefficients are subject to 36 homogeneous jet equations, so a nonzero solution exists. At degree twelve, 91 coefficients are subject to 90 equations, so again a nonzero solution exists. Hence

    a_3(T)=8, a_5(T)=12.

A full-rank degree d rules out every lower degree: multiply a hypothetical lower-degree homogeneous form by any nonzero homogeneous form to reach degree d. No rank-deficient reduction modulo a prime is used to prove existence over Q. Existence comes only from explicit products or dimension count.

For an additional exact family, let U consist of a t-by-t affine grid with t distinct x-coordinates and t distinct y-coordinates. Then a_m(U)=tm. The product of the t vertical lines raised to the m-th power gives the upper bound. If a curve had degree d<tm, its restriction to each vertical line would vanish to order at least m at t distinct points, hence be zero. All t vertical lines divide it. Removing their product leaves multiplicity at least m-1 and degree d-t<t(m-1); induction gives a contradiction. This argument works in any characteristic when the coordinates are distinct. The script verifies t=3,m=1,3 as additional controls.

The 2014 line-count update cited in SOURCE_VERIFICATION handles its specified incidence families for all r. Neither those results nor the equality of reduced Hilbert functions provides the missing comparison for all X.

## 6. A necessary nonreducedness condition for plane counterexamples

**Proposition 6.1.** Let X be any finite set of distinct points of P^2 over an algebraically closed field of characteristic zero, with a=alpha(I(X)). Let r>=3. If a nonzero form F vanishes to order at least 2r-1 at every point of X and has degree strictly smaller than r*a+r-1, then F has a repeated irreducible factor. The same conclusion holds when r=2 and 2<=a<=4. The cases a=1 are already impossible by Section 2.

Proof. Suppose F is squarefree, and write d=deg F and s=|X|. Since no degree-a-1 form vanishes at X, evaluation at the points is injective in that degree, so

    s >= binom(a+1,2) = a(a+1)/2.

There exists a first polar G=sum c_i*(partial F/partial x_i) with no irreducible factor in common with F. To see this, for each factor H of squarefree F, some partial derivative of H is nonzero and not divisible by H in characteristic zero. Reducing the corresponding derivative of F modulo H shows that not all partial derivatives of F are divisible by H. The coefficient choices for which H divides the polar form a proper linear subspace; finitely many such subspaces cannot cover k^3. Choose coefficients outside their union.

At each P in X, ord_P(F)>=m=2r-1 and ord_P(G)>=m-1. The local intersection multiplicity is at least their product. Bezout for curves with no common component yields

    d(d-1) >= sum_P ord_P(F)*ord_P(G)
             >= s*m*(m-1)
             >= a(a+1)*m*(m-1)/2.                  (1)

A counterexample degree satisfies d<=D=r(a+1)-2. Here D>=1 and d>=m, so replacing d by D preserves the upper comparison. Define

    E=D(D-1)-a(a+1)(2r-1)(2r-2)/2.

Putting r=3+t, t>=0, expansion gives

    E = (1-a^2)t^2 + (1-2a-3a^2)t - a(a+7).

For a>=1 this is strictly negative, contradicting (1). For r=2 the same expansion is E=a(a-5), negative for 1<=a<=4. QED.

**Exact remaining gap.** An initial-degree form is not guaranteed to be squarefree. Write F=product_j F_j^(e_j). Its multiplicity vector is the sum of the vectors e_j*ord_P(F_j). The different irreducible factors need not vanish on the same subsets of X, and their multiplicities need not be uniform. Removing a repeated factor generally destroys the uniform hypothesis, so the proposition cannot be iterated as though it proved the target. A suitable inequality controlling these weighted component contributions has not been established here.

For example, the sharp star witnesses of Section 4 at r>=2 explicitly contain repeated line factors. Thus a squarefree restriction removes meaningful extremal behavior and cannot silently replace the original problem.

## 7. Outcome

No full proof, counterexample, or verified prior complete resolution was obtained. The fifth approach ends at the precise nonreduced-component gap above. The correct campaign outcome is exhausted with rigorous partials, subject to independent audit. No remote publication or queue mutation is part of this frozen investigation.
