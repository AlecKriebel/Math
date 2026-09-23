# Independent verification by finite approximation

Date: 2026-09-22 (America/Los_Angeles).

## Claim and verdict

Let \(K\subset\mathbb R^n\) be compact, convex, and have nonempty
interior, with \(n\ge1\). Write
\[
g_K=\frac1{|K|}\int_K x\,dx,\qquad
C_2(K)=\frac1{|K|}\int_K |x|^2\,dx.
\]
Assume \(r>0\) and \(|v|\ge r\) for every extreme point \(v\) of
\(K\). The candidate's exact claim is valid:
\[
\Delta_r(K):=C_2(K)-\frac{r^2+(n+1)|g_K|^2}{n+2}\ge0,
\]
and equality holds exactly for full-dimensional simplices with all
vertices on \(rS^{n-1}\).

The verification below uses only finite polytope decompositions and
continuity of volume integrals. In particular, it does not assume the
candidate's countable decomposition lemma. The central independent check
is a strictly positive lower bound that survives approximation whenever
there is an extreme point outside an initial extreme simplex.

Mathematical verification completion estimate: **100% for the stated
theorem**. This is not a priority or literature verdict.

## 1. Finite identity

For a full-dimensional simplex \(A=\operatorname{conv}(a_0,\ldots,a_n)\),
the elementary barycentric integral gives
\[
C_2(A)=\frac{q_A+(n+1)|c_A|^2}{n+2},\qquad
q_A=\frac1{n+1}\sum_{i=0}^n|a_i|^2,\quad
c_A=\frac1{n+1}\sum_{i=0}^n a_i.
\]
Indeed, uniform barycentric coordinates satisfy
\(E\lambda_i^2=2/((n+1)(n+2))\) and
\(E\lambda_i\lambda_j=1/((n+1)(n+2))\) for \(i\ne j\).

Suppose a polytope \(P\) is partitioned into finitely many
full-dimensional simplices \(A\), modulo their boundaries, and all their
vertices have norm at least \(r\). Set \(w_A=|A|/|P|\). The simplex
identity and the finite variance identity yield
\[
\Delta_r(P)=\frac1{n+2}\sum_A w_A(q_A-r^2)
 +\frac{n+1}{n+2}\sum_A w_A|c_A-g_P|^2.
\tag{1}
\]
All summands are nonnegative. This proves the finite inequality and,
more importantly, allows fixed summands to be retained through limits.

## 2. Approximation retaining selected simplices

Choose affinely independent extreme points \(v_0,\ldots,v_n\), and put
\(S=\operatorname{conv}(v_0,\ldots,v_n)\). Such points exist because
the extreme points affinely span \(K\). Take a finite or countable dense
set of distinct extreme points that contains these points, and enumerate
the remaining points as \(u_1,u_2,\ldots\). Its nested finite convex
hulls, starting with \(S\), converge to \(K\) in Hausdorff distance.
This follows from the finite-dimensional extreme-point representation
of compact convex sets and compactness.

Each new point lies outside the preceding finite hull: an extreme point
cannot be a convex combination of other points of \(K\). On inserting a
point \(u\) outside a full-dimensional polytope \(P\), its new region
is a finite union of pyramids \(\operatorname{conv}(u,F)\), where
\(F\) ranges over the strictly visible facets of \(P\). Triangulating
each facet with its existing vertices partitions each pyramid into
full-dimensional simplices. Their interiors are disjoint, and their
interiors lie outside \(P\). Consequently, every simplex already
present can be retained unchanged at every later finite stage.

For clarity, no compatibility of triangulations along lower-dimensional
faces is needed here: boundaries have zero \(n\)-dimensional volume,
and all applications are identities for volume integrals.

If \(K\ne S\), some extreme point \(u\) lies outside \(S\); otherwise
the closed convex hull of all extreme points would be contained in
\(S\). Insert this \(u\) first. At least one facet \(F_i\) of \(S\)
is strictly visible from \(u\). If \(v_i\) is the opposite vertex,
then
\[
T=\operatorname{conv}\bigl(u,\{v_j:j\ne i\}\bigr)
\]
is a full-dimensional simplex in the first shell. It has positive volume
and interior disjoint from \(S\). The two centroids satisfy
\[
c_T-c_S=\frac{u-v_i}{n+1}\ne0.
\tag{2}
\]
Both \(S\) and \(T\) are retained in every subsequent finite
decomposition. Every vertex introduced is an extreme point of \(K\),
so the lower norm bound needed for (1) holds throughout.

## 3. Strictness survives the limit

Write \(a=|S|>0\), \(b=|T|>0\), and \(V_m=|P_m|\). Keeping the two
centroid terms from (1), and completing the square, gives
\[
\begin{aligned}
\Delta_r(P_m)
&\ge\frac{n+1}{n+2}\left(
\frac a{V_m}|c_S-g_{P_m}|^2+
\frac b{V_m}|c_T-g_{P_m}|^2\right)\\
&\ge\frac{n+1}{n+2}
\frac{ab}{V_m(a+b)}|c_S-c_T|^2\\
&\ge\frac{n+1}{n+2}
\frac{ab}{|K|(a+b)}|c_S-c_T|^2>0.
\end{aligned}
\tag{3}
\]
The second inequality is exactly the elementary identity
\[
a|p-z|^2+b|q-z|^2
=\frac{ab}{a+b}|p-q|^2
 +(a+b)\left|\frac{ap+bq}{a+b}-z\right|^2.
\]

Hausdorff convergence of the nested full-dimensional convex polytopes to
\(K\) implies convergence of their volumes and of their integrals of
\(x\) and \(|x|^2\). One direct justification is that a convex union
with closure \(K\) contains \(\operatorname{int}K\), the boundary of a
convex body has zero volume, and all functions are bounded on the common
compact set \(K\). Dominated convergence then applies. Thus
\(\Delta_r(P_m)\to\Delta_r(K)\).

The strict lower bound in (3) is independent of \(m\). Therefore, if
\(K\ne S\),
\[
\boxed{\quad
\Delta_r(K)\ge
\frac{ab\,|u-v_i|^2}
{(n+1)(n+2)|K|(a+b)}>0.
\quad}
\tag{4}
\]
In particular, equality forces \(K=S\). Applying the simplex identity
to \(S\) then says equality is equivalent to
\(\frac1{n+1}\sum_i |v_i|^2=r^2\). Since every term is at least
\(r^2\), this is equivalent to \(|v_i|=r\) for every \(i\).
Conversely, that vertex condition gives equality immediately.

The inequality itself follows by taking limits in (1), without needing
to assume \(K\ne S\).

## Boundary and hidden-assumption audit

- **Dimension one.** Every convex body is an interval \([a,b]\),
  \(a<b\), with extreme points its endpoints. Directly,
  \(\Delta_r([a,b])=(a^2+b^2-2r^2)/6\). Under the hypothesis,
  equality holds only at \(a=-r,b=r\), exactly the one-dimensional
  inscribed simplex. There is no extra exterior extreme point in this
  case, as required by the strictness argument.
- **Infinitely many extreme points.** Only finite identities are used
  before passing to the limit. The positive contribution from the fixed
  pair \(S,T\) cannot vanish because their positive volumes stay fixed
  and all approximating volumes are bounded by \(|K|\).
- **Extreme set need not be closed.** A subspace of Euclidean space is
  separable; the dense enumeration exists without closedness. Its closed
  convex hull is still \(K\).
- **Centroid away from the origin.** No step assumes \(g_K=0\),
  \(0\in K\), or that \(K\) contains the radius-\(r\) ball. The
  centroid term is retained exactly. The theorem is relative to the
  specified origin; it should not be translated without also changing
  the norm hypothesis appropriately.
- **Nonregular simplices.** Regularity is unnecessary in the stated
  theorem. Even a nonregular inscribed triangle gives equality when its
  centroid is permitted to be nonzero. With the additional condition
  \(g_K=0\), an inscribed triangle must be equilateral, while higher
  dimensions allow nonregular examples. Thus a statement about
  nonregularity only in dimensions above two must be understood in the
  centered setting.
- **Degenerate bodies.** Positive \(n\)-dimensional volume and
  full-dimensional simplices are essential to the displayed definitions.
  Lower-dimensional compact convex sets can instead be treated in their
  affine dimension with the corresponding volume; they are outside this
  theorem as stated.
- **Scale and units.** Both sides of (4) have units of squared length;
  the volume ratio is dimensionless. Rescaling \(K\) and \(r\) by
  the same positive factor scales every deficit by its square.
- **Unjustified limit equality avoided.** It would be insufficient merely
  to note strictness for each approximating polytope: positive deficits
  can tend to zero. Formula (3) supplies the needed fixed positive lower
  bound whenever \(K\) is not a simplex.

## Exact remaining scope

There is no remaining mathematical gap in the theorem under the stated
definitions. Identification with the precise published open problem,
priority, citations, and publication claims require the separate source
and literature audits. This note makes no claim that the elementary
finite-approximation mechanism itself is novel.
