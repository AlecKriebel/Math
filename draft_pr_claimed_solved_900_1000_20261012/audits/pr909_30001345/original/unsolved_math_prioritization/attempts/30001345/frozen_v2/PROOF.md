# A multibranch counterexample to summed rough-M semicontinuity

## 1. Exact claim and limits

Work over the complex numbers. For a reduced plane-curve singularity, use the **rough** invariant

\[
\overline M(C,p)=K\cdot(K+D),\qquad D=C'+E_{\mathrm{red}},
\]

on its minimal embedded resolution, with the local canonical divisor supported on the exceptional divisor. For a representative containing finitely many singular points, the invariant of the fiber means the **sum** of their local invariants.

**Theorem.** There is a flat, reduced, one-parameter deformation of an ordinary ninefold plane-curve singularity, in a fixed ball with transverse boundary and with a finite simultaneous normalization, for which

\[
\delta(C_0)=\sum_{p\in\operatorname{Sing}(C_t)}\delta(C_t,p)=36,
\quad
\overline M(C_0,0)=7<12=
\sum_{p\in\operatorname{Sing}(C_t)}\overline M(C_t,p)
\]

for every sufficiently small nonzero complex parameter. More precisely, the explicit equation below works in the closed unit ball for every \(|t|<1/4\); for \(t\ne0\) it has exactly twelve ordinary triple points, all in the open ball of radius \(1/2\).

This disproves summed upper semicontinuity of the stated rough invariant for unrestricted reduced multibranch, delta-constant plane-curve deformations. It gives a negative answer to the unrestricted literal formulation of Question 3, and hence Question 2, on printed page 2446 of Borodzik's Oberwolfach contribution [1]. That page supplies the displayed rough-invariant definition and does not state an irreducibility assumption in Questions 2–3. This conclusion does **not** assert what unstated intended restrictions the author may have had in mind.

The central curve here has nine branches. The result therefore does **not** settle Borodzik's explicitly parametric Conjecture 3.8 in [2]: Definition 2.1 there requires both rationality and a unibranched central fiber. No resolution of a unibranched or fine-M conjecture, and no novelty of the classical arrangement, is claimed.

## 2. Classical arrangement and complete intersection list

Let \(\omega\) be a primitive cube root of unity. The dual Hesse arrangement is the union of the nine projective lines

\[
A_i:\ X-\omega^iY=0,\quad
B_j:\ Y-\omega^jZ=0,\quad
C_k:\ Z-\omega^kX=0,
\qquad i,j,k\in\mathbb Z/3\mathbb Z.
\]

Its equation is

\[
(X^3-Y^3)(Y^3-Z^3)(Z^3-X^3)=0.
\]

This arrangement is classical; for example, [3, Proposition 3.1, printed p. 291] gives its equation and twelve triple points. We verify the exact combinatorics rather than relying on that attribution.

The three lines in each displayed group meet at one coordinate vertex. These three vertices are distinct; at each vertex none of the six lines in the other two groups passes through the vertex. Intersections between groups are the nine points

\[
P_{ij}=[\omega^{i+j}:\omega^j:1].
\]

At \(P_{ij}\), the lines are exactly \(A_i,B_j,C_{-i-j}\). Distinct ordered pairs \((i,j)\) give distinct projective points. All their coordinates are nonzero, so none is a coordinate vertex. They account for every intersection between different groups. All lines through each such point are distinct, so their local tangent directions are distinct: each singularity is an ordinary triple point. No other singularity of a reduced union of smooth distinct lines can occur away from a pair intersection.

As an additional completeness check, the twelve points account for

\[
12\binom32=36=\binom92
\]

pairs. There are no hidden double points, higher-multiplicity points, or remaining pair intersections.

## 3. Choice of infinity and explicit family

Choose the line at infinity

\[
L=X+2Y+4Z=0.
\]

At the three coordinate vertices its values are \(1,2,4\). At each \(P_{ij}\), using the above representative,

\[
|\omega^{i+j}+2\omega^j+4|\ge4-1-2=1.
\]

Thus infinity misses every pair intersection and contains none of the arrangement lines. The affine chart \(L=1\), with coordinates \(u=X/L,v=Y/L\), has \(Z/L=(1-u-2v)/4\). Its nine affine lines have pairwise different directions, since a parallel pair would intersect on \(L=0\).

Replace \((u,v)\) by \((x/t,y/t)\) and clear denominators. This yields, for all parameters including zero, the polynomial

\[
\boxed{F(x,y,t)=(x^3-y^3)
\bigl(64y^3-(t-x-2y)^3\bigr)
\bigl((t-x-2y)^3-64x^3\bigr).}
\]

Over \(\mathbb C\), it is the product of the following nine linear forms, with \(q\in\{1,\omega,\omega^2\}\):

\[
a_q=x-qy,\qquad
b_q=qx+(4+2q)y-qt,\qquad
c_q=-(1+4q)x-2y+t.
\]

Indeed, the three products are respectively \(x^3-y^3\), \(64y^3-(t-x-2y)^3\), and \((t-x-2y)^3-64x^3\). All three collections of forms have nonzero x-coefficients. Their spatial directions are exactly the pairwise different directions in the affine chart.

For \(t\ne0\), multiplication by \(t\) is an affine isomorphism from the chart arrangement to \(F_t=0\). Its singularities are precisely the twelve scaled chart points. At \(t=0\), the nine distinct directions become nine distinct lines through the origin. Consequently \(F_0=0\) is an ordinary ninefold point, with no other singularities. All fibers are reduced.

## 4. Flatness, including the analytic representative

As a polynomial in x, \(F\) has degree nine and constant leading coefficient

\[
1\cdot1\cdot(-65)=-65.
\]

Thus \(-F/65\) is monic in x. Polynomial division shows that

\[
R=\mathbb C[x,y,t]/(F)
\]

is free of rank nine over \(\mathbb C[y,t]\), with basis \(1,x,\ldots,x^8\). Since \(\mathbb C[y,t]\) is free over \(\mathbb C[t]\), \(R\) is flat over \(\mathbb C[t]\). This establishes algebraic flatness of the projection to t.

For clarity, flatness also holds directly for the holomorphic restriction used below. At any point with parameter \(t_0\), the local equation is a product of distinct nonvertical plane factors. In the convergent-power-series local ring of the ambient threefold, \(t-t_0\) divides none of these factors. Since that ring is factorial, \(t-t_0\) is a nonzerodivisor modulo their product. The local ring of the family is therefore torsion-free over the one-dimensional regular local base \(\mathbb C\{t-t_0\}\): every nonzero base germ is a unit times a power of \(t-t_0\). A torsion-free module over a discrete valuation ring is flat. Restricting to any open ball preserves this argument. There is no appeal to a merely numerical flatness test.

## 5. Finite simultaneous normalization

Let \(\ell_1,\ldots,\ell_9\) be the nine displayed forms, and write \(H_i=\{\ell_i=0\}\subset\mathbb C^3\). Every \(H_i\) is a smooth plane. Because its x-coefficient is nonzero, projection to \((y,t)\) is an isomorphism \(H_i\simeq\mathbb A^2\), and its projection to t is smooth.

Consider

\[
\nu:\bigsqcup_{i=1}^9H_i\longrightarrow\{F=0\}.
\]

This is finite. On rings its target algebra is

\[
S=\bigoplus_{i=1}^9\mathbb C[x,y,t]/(\ell_i),
\]

a direct sum of nine cyclic finite R-modules. The map \(R\to S\) is injective because the intersection of the nine distinct principal prime ideals \((\ell_i)\) in the polynomial unique-factorization domain is their product \((F)\). It identifies the total ring of fractions with the product of the fraction fields of the plane components. The ring S is normal. Since it is integral over R and integrally closed in that total ring of fractions, it is exactly the integral closure of R: an element integral over R is integral over S and hence lies in S, and every element of S is integral over R. Thus \(\nu\) is the normalization.

For every fixed t, the restrictions of these nine planes are the nine distinct line components of the reduced fiber. Restricting \(\nu\) to that fiber gives the disjoint union of its smooth lines, hence its normalization. The normalization map is therefore simultaneous, not merely a normalization of the total space whose special fiber could fail to normalize the special curve. The same statements hold analytically and after restriction to the ball; finiteness is preserved by restriction, and the local component-normalization description is unchanged. The normalized total family is smooth over the parameter disk.

## 6. One fixed ball, all singularities retained, and the boundary

Let

\[
\overline B=\{(x,y)\in\mathbb C^2:|x|^2+|y|^2\le1\},
\qquad \Delta=\{|t|<1/4\},
\]

and use the restriction of the holomorphic family to the open ball, together with its closure in \(\overline B\) for boundary statements. Put \(C_t=\{F_t=0\}\cap\overline B\).

The three coordinate vertices have chart coordinates \((1,0),(0,1/2),(0,0)\). The other nine points have

\[
(u,v)=\left(\frac{\omega^{i+j}}{\omega^{i+j}+2\omega^j+4},
\frac{\omega^j}{\omega^{i+j}+2\omega^j+4}\right),
\]

and consequently \(|u|^2+|v|^2\le2\). Every moving singular point therefore has norm at most \(\sqrt2|t|<\sqrt2/4<1/2\). All twelve occur in the chosen representative for every nonzero parameter; none escapes through its boundary.

An affine complex line \(ax+by+ct=0\), with \((a,b)\ne0\), has distance

\[
d(t)=\frac{|ct|}{\sqrt{|a|^2+|b|^2}}
\]

from the origin. Each line \(a_q=0\) has distance zero. For \(b_q=0\), \(|q|=1\) and \(|4+2q|\ge2\), so its distance is at most \(|t|/\sqrt5\). For \(c_q=0\), \(|1+4q|\ge3\), so its distance is at most \(|t|/\sqrt{13}\). These distances are all strictly less than one throughout \(\Delta\).

On a complex affine line, squared distance from the origin equals its minimum value plus the squared norm of the line coordinate centered at the closest point. Therefore the intersection with \(\overline B\) is a disk, and intersection with its unit sphere is transverse whenever \(d(t)<1\). All pair intersections are inside the radius-\(1/2\) ball, so these nine boundary circles are disjoint and the fiber is smooth along the boundary. This proves transversality of the entire reduced curve, not just of each branch in isolation.

The circles vary smoothly with the two real coordinates of t: use their smoothly varying closest points, their fixed complex direction vectors, and radii \(\sqrt{1-d(t)^2}\). Along any parameter path they give an isotopy of embedded links in the unit sphere. At t=0, the central curve is a cone of nine distinct lines, with only its origin singular. Radial scaling identifies its unit-sphere intersection with its link on any arbitrarily small sphere. Thus the representative has the required locality and fixed-boundary-link properties. If a smaller ball is desired, replace \((x,y,t)\) by \((\rho x,\rho y,\rho t)\): homogeneity gives the same construction with radius \(\rho\) and parameter radius \(\rho/4\).

In particular, normalization of every restricted fiber consists of exactly nine disks. Their geometric genera are all zero. Reducibility has not been hidden by discarding components or by allowing boundary changes.

## 7. Invariant calculations and the strict inequality

For an ordinary r-fold point,

\[
\delta_r=\binom r2.
\]

Here is one local algebra justification. For relatively prime reduced equations f and g in \(\mathbb C\{x,y\}\), the exact sequence

\[
0\longrightarrow\mathcal O/(fg)
\longrightarrow\mathcal O/(f)\oplus\mathcal O/(g)
\longrightarrow\mathcal O/(f,g)\longrightarrow0
\]

gives \(\delta(fg)=\delta(f)+\delta(g)+I(f,g)\) after comparison with normalization. Each smooth line has delta zero, and distinct lines intersect with multiplicity one. Adding the lines proves the formula.

For r at least three, one blowup resolves an ordinary r-fold point. Its exceptional curve E has \(E^2=-1\), and the r smooth strict transforms meet E transversely at r different points. Adjunction characterizes the local canonical divisor: \((K+E)\cdot E=-2\), hence \(K=E\). With \(D=C'+E\),

\[
\overline M_r=E\cdot(C'+2E)=r-2.
\]

The ordinary node also has \(\overline M_2=0\), since its minimal normal-crossings resolution has no exceptional curve; this agrees with the same formula. Only r=3 and r=9 are needed for the counterexample.

Thus the central values are

\[
\delta(C_0,0)=\binom92=36,\qquad\overline M(C_0,0)=9-2=7.
\]

For every \(0<|t|<1/4\), the complete singular set consists of twelve ordinary triple points, giving

\[
\sum\delta(C_t,p)=12\binom32=36,\qquad
\sum\overline M(C_t,p)=12(3-2)=12.
\]

Consequently the family is delta-constant and the proposed summed upper-semicontinuity inequality fails by exactly five. The finiteness, flatness, normalization and fixed-ball arguments above are independent of these numerical equalities.

## 8. Scope checks against the primary sources

- **[1], printed p. 2446:** the bar on the rough invariant matters. This packet uses its \(K(K+D)\) definition and the unrestricted wording of Questions 2–3. It concerns the sum over singularities in a fixed representative, rather than just the value along one distinguished section.
- **[1], printed p. 2447:** the subsequent setup explicitly permits several nearby singular points in a fixed ball and compares sums of their invariants. This supports the summed interpretation used here. Its one-branch signature estimate and subsequent cuspidal/ordinary-node restriction do not apply to this arrangement and are not being contradicted.
- **[2], Definition 2.1 and Conjecture 3.8, pp. 575 and 577:** the conjecture is restricted to parametric deformations, which include a unibranched-central-fiber requirement. The example fails that hypothesis.
- **[2], Definitions 3.3 and 3.5 and Remark 3.4, pp. 576–577:** the rough and fine invariants are distinguished, and a different multibranch normalization is discussed. We do not silently replace the displayed rough definition by either alternative. The signature estimate has additional singularity hypotheses; it is not being contradicted.

These source comparisons constrain the interpretation of the result. They do not turn it into a claim that every related open problem has been solved. The classical dual Hesse configuration is credited, and this packet makes no global novelty or present-day literature-status claim.

## 9. Optional extension: classical Fermat arrangements

The same reasoning gives an unbounded family of excesses. For an integer \(n\ge3\), the classical arrangement

\[
(X^n-Y^n)(Y^n-Z^n)(Z^n-X^n)=0
\]

has three coordinate vertices of multiplicity n and \(n^2\) other ordinary triple points. The latter are \([\zeta^{i+j}:\zeta^j:1]\), with \(\zeta\) a primitive n-th root and indices modulo n. The same group-incidence argument exhausts all pairs. The infinity \(X+2Y+4Z=0\) again misses all intersections by the identical modulus bound. Its homogenized affine-scaling family has an ordinary \(3n\)-fold central point and a simultaneous normalization into \(3n\) planes, with a sufficiently small fixed-ball representative as above.

Its total delta is constant because

\[
3\binom n2+3n^2=\binom{3n}2,
\]

while the rough-M excess is

\[
\bigl(3(n-2)+n^2\bigr)-(3n-2)=n^2-4.
\]

For n=3 the three vertices are triple points as well, recovering the twelve-point example. This extension is a consequence of the written all-n incidence argument; a finite test range does not prove its universal quantifier.

## 10. Reproducibility and references

`checks.py` independently performs exact rational arithmetic in \(\mathbb Q[\omega]/(\omega^2+\omega+1)\). It enumerates all pair intersections and incidences, checks the chosen infinity, central tangent directions, complete polynomial factorization and x-leading coefficient, computes both invariant totals, and includes intentional-error controls. It also checks the finite Fermat range n=3 through 100. The checker supplements this proof; it does not certify analytic flatness, normalization, boundary transversality, source interpretation, or the all-n extension.

1. Maciej Borodzik, *On deformations of plane curve singularities*, in *Singularities*, Oberwolfach Reports 6 (2009), no. 3, pp. 2446–2448; report published 30 June 2010. [Publisher record](https://ems.press/journals/owr/articles/4086), [official PDF](https://ems.press/content/serial-article-files/46242?nt=1), DOI 10.4171/OWR/2009/43.
2. Maciej Borodzik, *Deformations of singularities of plane curves: topological approach*, Osaka Journal of Mathematics 51 (2014), no. 3, pp. 573–583. [Institutional record](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/), [published PDF](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf), DOI 10.18910/50809. The earlier manuscript is [arXiv:0907.4129v3](https://arxiv.org/abs/0907.4129v3).
3. Xavier Roulleau and Giancarlo Urzúa, *Chern slopes of simply connected complex surfaces of general type are dense in [2,3]*, Annals of Mathematics 182 (2015), pp. 287–306, Proposition 3.1. [Publisher record](https://annals.math.princeton.edu/2015/182-1/p06), DOI 10.4007/annals.2015.182.1.6.
