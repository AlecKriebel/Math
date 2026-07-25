# A universal common-pair capacity hierarchy

> **REFUTATION NOTICE.**  The projection theorem and the cumulative
> inequalities (7)--(9) below are valid.  The finite-support claim that the
> stored five-node candidate survives *every* consequence of the pointwise
> capacity theorem is false: exact base-color strata give violations by 88
> and 120.  The seven-node all-harmonic witness also fails an exact-stratum
> row.  See `common_pair_capacity_hierarchy_adversarial_audit.md` and the
> corrected theorem/certificate in
> `common_pair_capacity_stratified_obstruction.md`.  The original artifact
> is retained as a reproducible cumulative-only calculation.

## Scope

This note proves a family of necessary three-point inequalities for every
spherical kissing code in \(S^4\).  The inequalities do not assume that the
code is symmetric, rigid, maximal, antipodal, or supported on finitely many
inner products.

The final sections audit several finite-support pseudodistributions.  Those
audits are barriers for the indicated relaxations, not upper bounds for the
five-dimensional kissing number.

## Projection theorem

Let \(C\subset S^4\) have
\[
 \langle x,x'\rangle\leq\frac12\qquad(x\ne x').
\]
For \(-1\leq a\leq0\) and \(0<b\leq1/2\), define
\[
 p=p(a,b)=\frac{2b^2}{1+a}
\]
when \(a>-1\).  For a pair \(y,z\in C\), put
\[
 \Gamma_b(y,z)=
 \{x\in C\setminus\{y,z\}:
   \langle x,y\rangle\geq b,
   \langle x,z\rangle\geq b\}.
\]

**Theorem.**  If \(\langle y,z\rangle\leq a\), then
\[
 |\Gamma_b(y,z)|\leq M(p),
 \tag{1}
\]
where
\[
\begin{array}{c|c}
\text{range of }p&M(p)\\ \hline
p>1&0\\
3/4<p\leq1&1\\
2/3<p\leq3/4&2\\
5/8<p\leq2/3&3\\
1/2<p\leq5/8&4\\
p=1/2&6.
\end{array}
\tag{2}
\]
For \(a=-1\), the bound is \(0\).

No assertion is made here when \(p<1/2\).  The endpoints in (2) are
intentional: equality at \(p=3/4,2/3,5/8,1/2\) permits respectively the
antipodal, equilateral-triangle, regular-tetrahedron, and orthoplex equality
patterns in the projected three-dimensional space.

### Proof

Write \(q=\langle y,z\rangle\).  If \(q=-1\), then \(z=-y\), whereas any
\(x\in\Gamma_b(y,z)\) would give
\[
 0=\langle x,y+z\rangle\geq2b>0.
\]
Thus suppose \(q>-1\).  The Gram matrix and inverse of the ordered base
\((y,z)\) are
\[
 B=\begin{pmatrix}1&q\\q&1\end{pmatrix},\qquad
 B^{-1}=\frac1{1-q^2}
 \begin{pmatrix}1&-q\\-q&1\end{pmatrix}.
\]
Because \(q\leq a\leq0\), every entry of \(B^{-1}\) is nonnegative.

For \(x\in\Gamma_b(y,z)\), set
\[
 c_x=(\langle x,y\rangle,\langle x,z\rangle)^{\mathsf T}.
\]
Let \(P\) be orthogonal projection onto
\(\operatorname{span}\{y,z\}\), and put \(\xi_x=(I-P)x\).  Coordinatewise
\(c_x\geq(b,b)^{\mathsf T}\), so for any \(x,w\in\Gamma_b(y,z)\),
\[
\begin{split}
 \langle Px,Pw\rangle
 &=c_x^{\mathsf T}B^{-1}c_w\\
 &\geq (b,b)B^{-1}(b,b)^{\mathsf T}
 =\frac{2b^2}{1+q}
 \geq\frac{2b^2}{1+a}=p.                 \tag{3}
\end{split}
\]
In particular,
\[
 \|\xi_x\|^2=1-\|Px\|^2\leq1-p.          \tag{4}
\]
If \(p>1\), (4) makes \(\Gamma_b(y,z)\) empty.  If \(p=1\), every
common neighbor has zero residual, and two such neighbors would have inner
product at least \(p>1/2\), so there is at most one.

Assume now \(1/2<p<1\).  A common neighbor with zero residual cannot coexist
with another common neighbor, by (3).  Otherwise every residual is nonzero,
lies in the three-dimensional space
\(\operatorname{span}\{y,z\}^{\perp}\), and distinct common neighbors obey
\[
\begin{split}
 \left\langle
   \frac{\xi_x}{\|\xi_x\|},
   \frac{\xi_w}{\|\xi_w\|}
 \right\rangle
 &=
 \frac{\langle x,w\rangle-\langle Px,Pw\rangle}
      {\|\xi_x\|\|\xi_w\|}\\
 &\leq
 \frac{1/2-p}{1-p}
 =:\alpha(p)<0.                           \tag{5}
\end{split}
\]
The direction of the last inequality is correct because its numerator is
negative and (4) gives
\(\|\xi_x\|\|\xi_w\|\leq1-p\).

For \(m\) unit vectors with pairwise inner products at most
\(\alpha<0\),
\[
 0\leq\left\|\sum_{i=1}^m v_i\right\|^2
 \leq m\bigl(1+(m-1)\alpha\bigr).         \tag{6}
\]
Thus \(\alpha<-1,-1/2,-1/3\) gives respectively \(m\leq1,2,3\).
For every \(\alpha<0\), Rankin's strict-obtuse bound gives \(m\leq4\)
in \(\mathbb R^3\).  For completeness, if five such vectors existed, one
could choose a nonzero relation
\(\sum_i c_i v_i=0\) also satisfying \(\sum_i c_i=0\).  Moving the
negative coefficients to the other side and taking the inner product of
the two sides makes a squared norm strictly negative, a contradiction.
Substitution of (5) shows
\[
\begin{array}{rcl}
\alpha<-1&\Longleftrightarrow&p>3/4,\\
\alpha<-1/2&\Longleftrightarrow&p>2/3,\\
\alpha<-1/3&\Longleftrightarrow&p>5/8.
\end{array}
\]
This proves all rows of (2) with \(p>1/2\).

It remains to treat \(p=1/2\).  If a residual vanishes, it is the only
common neighbor.  Indeed, if \(w\) were another one, then
\[
\frac12\geq\langle x,w\rangle
=\langle Px,Pw\rangle\geq\frac{2b^2}{1+q}\geq p=\frac12.
\]
Equality throughout would force \(q=a\) and both base correlations of the
zero-residual point to equal \(b\), because
\[
 B^{-1}(b,b)^{\mathsf T}=\frac b{1+q}(1,1)^{\mathsf T}>0;
\]
more explicitly, for \(c_x,c_w\geq(b,b)^{\mathsf T}\),
\[
\begin{split}
c_x^{\mathsf T}B^{-1}c_w-(b,b)B^{-1}(b,b)^{\mathsf T}
={}&(c_x-(b,b)^{\mathsf T})^{\mathsf T}B^{-1}c_w\\
 &+(b,b)B^{-1}(c_w-(b,b)^{\mathsf T}),
\end{split}
\]
and both nonnegative terms can vanish only when
\(c_x=c_w=(b,b)^{\mathsf T}\).  Equality in the last step of (3) also
forces \(q=a\).  But then the zero-residual point's projected squared norm
would be only
\[
 (b,b)B^{-1}(b,b)^{\mathsf T}
 =\frac{2b^2}{1+q}=\frac12,
\]
not \(1\).
If all residuals are nonzero, (5)
holds with \(\alpha=0\).  The exact orthoplex bound in \(\mathbb R^3\) is
\(m\leq6\): if \(G\) is their Gram matrix, then
\[
 \operatorname{tr}(G^2)
 =m+2\sum_{i<j}G_{ij}^2
 \leq m-2\sum_{i<j}G_{ij}
 \leq2m,
\]
where \(G_{ij}^2\leq-G_{ij}\) for \(G_{ij}\in[-1,0]\), and the final
inequality is \(\|\sum_i v_i\|^2\geq0\).  Since
\[
 m^2=\operatorname{tr}(G)^2
 \leq\operatorname{rank}(G)\operatorname{tr}(G^2)
 \leq3\operatorname{tr}(G^2),
\]
we get \(m\leq6\).  This completes the proof. \(\square\)

## Monotonicity

On its domain,
\[
 p(a,b)=\frac{2b^2}{1+a}
\]
is nonincreasing in \(a\) and increasing in \(b\).  The table \(M(p)\) is
nonincreasing in \(p\).  Consequently:

- making the allowed base pairs deeper cannot weaken the capacity bound;
- raising the two common-neighbor thresholds cannot weaken it; and
- on a finite ordered support, it suffices to test \(a\) and \(b\) at
  support nodes.  Between consecutive nodes the selected sets are constant,
  and the endpoint with the largest \(p\) is strongest.

The strict and non-strict signs in (2) are forced by the equality cases
listed after the theorem.

## Pair/triple-measure inequalities

Let \(\alpha\) and \(\nu\) be the normalized pair and all-distinct triple
measures
\[
 \alpha(B)=\frac1N\#\{(y,z)\in C^2:y\ne z,
                              \langle y,z\rangle\in B\},
\]
\[
 \nu(E)=\frac1N\#\{(x,y,z)\in C^3:\text{all distinct},\
  (\langle x,y\rangle,\langle x,z\rangle,\langle y,z\rangle)\in E\}.
\]
For every row of (2),
\[
 \int
 {\bf1}_{\{t\leq a,\ u\geq b,\ v\geq b\}}
 \,d\nu(u,v,t)
 \leq M(p)\,\alpha([-1,a]).              \tag{7}
\]
This is just (1) summed over ordered base pairs.  Symmetry gives the
equivalent averaged form
\[
 \frac13\int\left(
 {\bf1}_{\{t\leq a,\ u,v\geq b\}}+
 {\bf1}_{\{v\leq a,\ u,t\geq b\}}+
 {\bf1}_{\{u\leq a,\ v,t\geq b\}}
 \right)d\nu
 \leq M(p)\,\alpha([-1,a]).              \tag{8}
\]

For a finite support \(s_0<\cdots<s_{r-1}\), let \(E_i\) be the number of
unordered pairs of color \(i\), and let \(n_{ijk}\) be the number of
unordered point triples whose three colors, sorted, are \(i\leq j\leq k\).
Define
\[
 c_{a,b}(i,j,k)=
 \#\{\text{edges of the colored triangle with color }\leq a:
       \text{ both other colors are }\geq b\}.
\]
Then (7) is exactly
\[
 \sum_{i\leq j\leq k}c_{a,b}(i,j,k)n_{ijk}
 \leq M(p)\sum_{s_i\leq a}E_i.           \tag{9}
\]
No orbit-size factor is missing.  A qualifying unordered
base-edge/third-vertex incidence contributes once to the left side of (9).
It contributes exactly twice to the fixed-coordinate integral in (7), via
the ordered triples \((x,y,z)\) and \((x,z,y)\).  Thus the two sides of
(7) are respectively
\[
 \frac2N\sum c_{a,b}(i,j,k)n_{ijk}
 \quad\hbox{and}\quad
 \frac{2M(p)}N\sum_{s_i\leq a}E_i.
\]
Multiplication by \(N/2\) gives (9), including when two or three edge colors
of a triangle coincide.

## Exact finite-support audits (cumulative rows only; barrier refuted)

On the five-node support
\[
 \left\{-\frac{77}{100},-\frac7{10},-\frac{11}{25},
 -\frac9{100},\frac{499}{1000}\right\},
\]
the strongest nontrivial cut with \(b=499/1000\) and
\(a=-11/25\) has
\[
 p=\frac{249001}{280000}>\frac34,\qquad M=1.
\]
It is
\[
 n_{044}+n_{144}+n_{244}\leq E_0+E_1+E_2=219.       \tag{10}
\]
The four previously stored local-hybrid triple witnesses have left sides
\(412,434,248,243\), so all four are refuted by (10).  This does not refute
the pair measure or every possible triple extension of it.  The earlier
`local_hybrid_pseudodistribution.json` contains pair data only, so a
three-point inequality cannot be evaluated on it by itself; the audit covers
every stored triple extension of that pair measure.

On the seven-node quarter grid, the exact all-harmonic witness survives all
of the **cumulative threshold rows (7)**.  Three capacity-zero rows are
equalities; among the remaining rows its smallest positive exact slack is
\[
\frac{155474701215499}{60000000000000}.
\]
This is not survival of the full pointwise mechanism.  Selecting the exact
base stratum \(t=-1/4\), rather than the cumulative set \(t\leq-1/4\),
gives a strict violation recorded in the adversarial audit.

The exact source-data audit and any reoptimized finite-support witness are
checked by
`verifiers/verify_common_pair_capacity_hierarchy.py`; discovery code is kept
separate in `experiments/search_common_pair_capacity_hierarchy.py`.
