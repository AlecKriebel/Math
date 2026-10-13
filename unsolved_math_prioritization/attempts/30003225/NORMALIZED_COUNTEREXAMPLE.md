# A three-free-blowup counterexample to the disclosed normalized intersection statement

## Result and precise scope

Work over the formal arc space of the smooth complex surface germ \(X=(\mathbb C^2,0)\). Adopt the following explicit convention: \(c_1=0,c_2,\ldots,c_n\) are the centers in the minimal model of a prime divisor \(E=D_n\); \(D_j\) is created by the blowup of \(c_j\). For \(k<n\), with \(c_{k+1}\) free, let \(\mathcal F_k(E)\) consist of all divisors of the same combinatorial type as \(E\) sharing at least the first \(k\) centers. Put

\[
 I_k(E)=\bigcap_{E'\in\mathcal F_k(E)}\overline N_{E'}.
\]

The normalized assertion

\[
 I_k(E)=C_X(q\operatorname{ord}_{D_k})\qquad\text{for some integer }q>0
\]

is false. Three successive free blowups, with \(k=2\), give

\[
 I_2(E)=\{\operatorname{ord}_t x\ge2,\ \operatorname{ord}_t y\ge3\}
       =C_X(v_{(2,3)}),
\]

while

\[
 C_X(q\operatorname{ord}_{D_2})
       =\{\operatorname{ord}_t x\ge q,\ \operatorname{ord}_t y\ge2q\}.
\]

These sets are different for every positive integer \(q\).

This is a counterexample to the disclosed normalization, whose family uses the paper's explicitly defined relation \(\equiv_{\ge k}\) and whose right side uses the last-shared divisor. It is not an assertion that the normalization is an author-authenticated erratum. In particular, it should not be described as an unqualified resolution of every possible intended interpretation of the printed conjecture. It is different from the two-blowup diagnostic of the literal mixed-index reading: it uses the normalized right-hand divisor throughout.

## 1. The blowups and their two charts

Start with coordinates \((x,y)\) on \(X\). Blow up \(c_1=(0,0)\). In the chart

\[
 x=r,\qquad y=r u,
\]

\(D_1\) is \(r=0\). Choose the free point \(c_2=(r,u)=(0,0)\), corresponding to the tangent line \(y=0\).

Blow up \(c_2\). Its two standard charts are:

\[
 U:\quad r=x,\quad u=xv,\qquad (x,y)=(x,x^2v),
\]

and

\[
 V:\quad r=su,\qquad (x,y)=(su,su^2).
\]

On \(U\), the new divisor \(D_2\) is \(x=0\). On \(V\), it is \(u=0\), while the strict transform of \(D_1\) is \(s=0\). Their unique intersection is \((s,u)=(0,0)\). On the overlap, \(v=1/s\); consequently

\[
 D_2\setminus D_1\simeq\mathbb A^1_v.
\]

Thus every free point of \(D_2\) is, uniquely,

\[
 c_3(a)=(x,v)=(0,a),\qquad a\in\mathbb C.
\]

The omitted point \(v=\infty\) is precisely the satellite point \(D_1\cap D_2\), not an additional member of the free family.

Blow up \(c_3(a)\), and call its exceptional divisor \(E_a\). One standard chart is

\[
 v-a=xw,\qquad (x,y)=(x,a x^2+x^3w).
\]

Here \(E_a\) is \(x=0\); the strict transform of \(D_2\) meets it at the point outside this chart. For completeness, the other chart has

\[
 x=z h,\qquad v-a=h,\qquad (x,y)=(zh,z^2h^2(a+h));
\]

\(E_a\) is \(h=0\), and the strict transform of \(D_2\) is \(z=0\). Its intersection with \(E_a\) corresponds to \(w=\infty\).

The map in the first chart immediately gives

\[
 \operatorname{ord}_{E_a}(x)=1,
 \qquad
 \operatorname{ord}_{E_a}(y-a x^2)=3.
\]

Equivalently, in the regular coordinates \((x,z_a)=(x,y-a x^2)\), \(E_a\) has the monomial valuation with weights \((1,3)\). Likewise, \(D_2\) has weights \((1,2)\) in \((x,y)\).

## 2. Exhaustion of the entire family

Fix \(E=E_0\), created by the three centers \(c_1,c_2,c_3(0)\). The minimal exceptional graph is the marked chain

\[
 D_1\ (-2)\; -\;D_2\ (-2)\; -\;E\ (-1).
\]

All centers after the origin are free; its curvetta multiplicity sequence is \((1,1,1)\). Each \(E_a\) has this same combinatorial type and the same first two centers.

Conversely, let \(E'\in\mathcal F_2(E)\). Its minimal model has the same three-center free-chain proximity data and begins with the prescribed \(c_1,c_2\). Its third center must lie on the newest exceptional component \(D_2\): a third blowup centered on \(D_1\setminus D_2\) would not require the blowup at \(c_2\), and so this three-blowup surface would not be the minimal model of the resulting divisor. The third center cannot be \(D_1\cap D_2\), because that is satellite and has different proximity data and weighted graph. It is therefore \(c_3(a)\) for exactly one \(a\in\mathbb C\).

Hence, as a family of prime divisors,

\[
 \mathcal F_2(E)=\{E_a:a\in\mathbb C\}.
\]

For \(a\ne b\), \(E_a,E_b\) share exactly the first two centers; for \(a=b\) they are identical. Thus using contact at least two, rather than exactly two, includes \(E\) and causes no hidden restriction.

## 3. Exact closed Nash cylinders

Write \(\operatorname{ord}_t0=+\infty\). For each \(a\), define

\[
 S_a=\{\gamma:\operatorname{ord}_t x(\gamma)\ge1,
                   \operatorname{ord}_t(y-a x^2)(\gamma)\ge3\}.
\]

The coordinate substitution \((x,y)\mapsto(x,z_a=y-a x^2)\) is a polynomial automorphism fixing the origin. In these coordinates, \(S_a\) is the affine irreducible cylinder obtained by setting the coefficients of \(x\) below degree 1 and those of \(z_a\) below degree 3 equal to zero.

The sublocus of \(S_a\) where \(\operatorname{ord}_t x=1\) is nonempty and dense. Every such arc lifts to the first chart of the third blowup by

\[
 w(t)=\frac{y(t)-a x(t)^2}{x(t)^3}\in\mathbb C[[t]].
\]

Its lift meets \(E_a\) transversely at a finite value of \(w\), hence at a smooth point of the total exceptional divisor. Conversely, every arc with transverse lifting to \(E_a\) has finite \(w\), \(\operatorname{ord}_t x=1\), and \(\operatorname{ord}_t(y-a x^2)\ge3\). Taking the Zariski closure of the transverse locus therefore yields the exact equality

\[
 \boxed{\ \overline N_{E_a}=S_a\ }.
\]

This argument uses the closed Nash set, not merely a necessary valuative inequality or the raw contact stratum. It also includes constant arcs and arcs with \(x=0\) through closure.

Similarly, for any positive integer \(q\), the arcs meeting a general smooth point of \(D_2\) with order \(q\) have

\[
 \operatorname{ord}_t x=q,\qquad y=x^2v.
\]

Their closure is the irreducible coordinate cylinder

\[
 \boxed{\ C_X(q\operatorname{ord}_{D_2})
       =\{\operatorname{ord}_t x\ge q,\operatorname{ord}_t y\ge2q\}.\ }
\]

One may require \(v(0)\ne0\) to describe a smaller dense stratum without changing this closure. These calculations also agree with the standard toric maximal-divisorial-set formula.

## 4. The intersection, computed at two-jet level

The two members \(a=0\) and \(a=1\) already determine the full intersection. Their simultaneous conditions are

\[
 \operatorname{ord}_t y\ge3,\qquad
 \operatorname{ord}_t(y-x^2)\ge3.
\]

Subtracting gives \(\operatorname{ord}_t x^2\ge3\). As orders are integral, this is equivalent to \(\operatorname{ord}_t x\ge2\). Conversely, if \(\operatorname{ord}_t x\ge2\) and \(\operatorname{ord}_t y\ge3\), then \(\operatorname{ord}_t(a x^2)\ge4\) for every \(a\), so \(\operatorname{ord}_t(y-a x^2)\ge3\). Therefore

\[
 \boxed{\ I_2(E)=S_0\cap S_1
        =\{\operatorname{ord}_t x\ge2,\operatorname{ord}_t y\ge3\}.\ }
\]

Explicitly, write centered arcs as

\[
 x=a_1t+a_2t^2+\cdots,\qquad
 y=b_1t+b_2t^2+\cdots.
\]

Then \(S_a\) is defined by

\[
 b_1=0,\qquad b_2-a a_1^2=0.
\]

The reduced intersection has ideal \((a_1,b_1,b_2)\). The scheme-theoretic sum of the ideals for \(a=0,1\) is \((b_1,b_2,a_1^2)\), which is nonreduced; the conjecture concerns closed sets, so its radical is the relevant ideal. No scheme-theoretic multiplicity has been silently identified with a set-theoretic equality.

Since \(\gcd(2,3)=1\), the resulting cylinder is itself the maximal divisorial set for the prime toric valuation \(v_{(2,3)}\). It has a concrete geometric identification: blow up the excluded satellite point \(D_1\cap D_2\). In the second chart of Section 1, set \(s=p\) and \(u=pq\); then

\[
 x=p^2q,\qquad y=p^3q^2.
\]

The resulting exceptional divisor \(F\) is \(p=0\), with generic valuation \(v_F(x)=2\), \(v_F(y)=3\). The locus with exact orders \((2,3)\) lifts to this chart by \(p=x^2/y\), \(q=y^2/x^3\), with \(\operatorname{ord}_t p=1\) and \(q\) a unit. It is dense in the displayed coordinate cylinder. Thus the intersection is precisely \(\overline N_F\): intersecting all the free third-center Nash sets produces the Nash set of the satellite third-center divisor. The failure is the identity of the proposed valuation, not reducibility of this particular intersection.

## 5. No positive integer \(q\) works

If \(q=1\), the arc

\[
 \alpha(t)=(t,t^3)
\]

belongs to \(C_X(\operatorname{ord}_{D_2})\), but not to \(I_2(E)\).

If \(q\ge2\), the arc

\[
 \beta(t)=(t^2,t^3)
\]

belongs to \(I_2(E)\), but not to \(C_X(q\operatorname{ord}_{D_2})\), since its \(y\)-order is 3 whereas \(2q\ge4\).

Both arcs are nonconstant polynomial arcs. Thus the discrepancy is already visible among convergent arcs and is not caused by formal/nonconvergent behavior. This completes the counterexample.

An independent dimension check gives the same obstruction. In the full arc space of \(\mathbb A^2\), the intersection has codimension \(2+3=5\), whereas \(C_X(q\operatorname{ord}_{D_2})\) has codimension \(q+2q=3q\). No positive integer \(q\) satisfies \(5=3q\). In the subspace of arcs centered at the origin, both codimensions decrease by 2, leaving the same obstruction.

## 6. Exact calculation for arbitrary all-free chains with a fixed prefix

The same computation explains the obstruction systematically. Let \(E\) be obtained by \(n\) successive free blowups along a smooth branch. Fix its first \(k\) centers, with \(2\le k<n\). Choose regular coordinates \((x,z)\) in which the fixed branch jet is \(z=0\), so that \(D_k\) has weights \((1,k)\).

Every completion with the same all-free combinatorial type is uniquely specified by coefficients \(a_k,\ldots,a_{n-1}\in\mathbb C\), with transverse arcs given by

\[
 \operatorname{ord}_t x=1,\qquad
 \operatorname{ord}_t\left(z-\sum_{j=k}^{n-1}a_jx^j\right)\ge n.
\]

Indeed, the successive coordinates are obtained by subtracting the chosen coefficient and dividing by \(x\); the one forbidden value at each stage is the satellite point at infinity. The same dense-stratum proof yields

\[
 \overline N_{E_{\boldsymbol a}}
 =\left\{\operatorname{ord}_t x\ge1,
          \operatorname{ord}_t\left(z-\sum_{j=k}^{n-1}a_jx^j\right)\ge n\right\}.
\]

Taking all coefficients zero gives \(\operatorname{ord}_t z\ge n\). Comparing this member with the member having \(a_k=1\) and all other coefficients zero gives \(k\operatorname{ord}_t x\ge n\). These two conditions imply every other member's condition because \(j\ge k\). Consequently

\[
 \boxed{\ I_k(E)
   =\{\operatorname{ord}_t x\ge\lceil n/k\rceil,
       \operatorname{ord}_t z\ge n\}.\ }
\]

On the other hand,

\[
 C_X(q\operatorname{ord}_{D_k})
   =\{\operatorname{ord}_t x\ge q,
       \operatorname{ord}_t z\ge kq\}.
\]

The two independent order thresholds agree exactly when \(k\mid n\), in which case \(q=n/k\). Hence every pair \(2\le k<n\) with \(k\nmid n\) supplies a counterexample within the all-free-chain class. The minimal instance is \((n,k)=(3,2)\).

This extension is not needed for the counterexample in Sections 1–5. It shows that the obstruction is the integral rounding of order conditions under free-center variation, and cannot be removed by arguing that a special parameter value was omitted.

## 7. Source boundaries and existing results

The normalization is motivated by, but not certified by, the contact convention and explicit specialization in Fernández de Bobadilla, Pe Pereira and Popescu-Pampu, *On the generalized Nash problem for smooth germs and adjacencies of curve singularities*, §2 and §4.2:

- https://arxiv.org/abs/1501.06898v3
- https://arxiv.org/pdf/1501.06898v3
- https://doi.org/10.1016/j.aim.2017.09.035

The source's general printed conjecture contains unresolved indexing notation. This report neither authenticates an erratum nor claims to have settled an interpretation different from the explicit one at its start. The primary displayed operation is intersection; a dataset rendering it as union is not the statement analyzed here.

The source already establishes combinatorial invariance of Nash adjacency (Theorem 4.10), finite cylindrical realization of the intersection (Lemma 4.11), and related monotonicity and union/intersection inclusions (Corollaries 4.12–4.13). The present two-member intersection is compatible with those results. The source's Remark 4.14 and Ishii's work cover the stated one-Puiseux-pair specialization at the first exceptional divisor. The counterexample here has \(k=2\); it does not contradict that specialization.

The toric formula used as an independent consistency check appears in Ishii, *Maximal divisorial sets in arc spaces*, Example 2.10 and Lemma 3.11:

- https://arxiv.org/abs/math/0612185
- https://arxiv.org/pdf/math/0612185

The proof above is given directly in blowup charts and coefficient cylinders. No unproved converse from valuative domination to Nash inclusion is used. No claim about the unrelated generalized Nash problem, the paper's Conjecture 2, or the global novelty of this example is made.
