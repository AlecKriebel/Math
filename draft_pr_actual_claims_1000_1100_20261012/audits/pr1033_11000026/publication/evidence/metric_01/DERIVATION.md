# Independent derivation of the general metric lemma

Review family: metric_01. Input: submitted PROOF.md at immutable head
`6322305d37b8131f034a1b4c3c5e861e4b04844f`.

This derivation was made after reading the exact submitted claim, before reading
any historical acceptance or independent-audit verdict. Those verdicts and other
fresh-family artifacts have not been used. No general-metric novelty claim is
being reviewed or inferred.

## Exact proposition and quantifiers

Let `(M,d)` be a geodesic metric space, with finite metric distances. Let
`c` be one finite real number with `c >= 0`. Assume:

For every `o,a,b in M`, there exists a minimizing geodesic from `a` to `b`
such that every point `z` on its image satisfies

\[
 d(o,z)\le \max\{d(o,a),d(o,b)\}+c. \tag{H}
\]

The chosen geodesic may depend on the entire triple `(o,a,b)` and need not be
unique. No assertion about every minimizing geodesic is required.

The conclusion is that for every `o in M`, every finite `R >= 0`, and every
`x,y` with `d(o,x),d(o,y) <= R`, there is a continuous rectifiable path
`gamma:[0,1] -> M` with endpoints `x,y`, image in the *original closed ball*
`Bbar(o,R)`, and

\[
 \operatorname{Len}_d(\gamma)\le d(x,y)+4c. \tag{C}
\]

Metric length means the supremum, over finite ordered partitions of the domain,
of the sum of distances between successive image points. Thus an actual path,
not merely a bound on a formal or discrete infimum, is required.

## Independent construction

Write `p=d(o,x)` and `q=d(o,y)`.

If `x=y`, the constant path already proves (C). The following construction also
works without this preliminary simplification, but the simplification explicitly
settles the zero-distance case.

If `R<c`, choose any minimizing radial geodesics from `x` to `o` and from `o`
to `y`, and concatenate them. A radial geodesic parameterized from `o` by
arclength has `d(o,s(t))=t`; hence each of these images lies in `Bbar(o,R)`.
Their total length is `p+q <= 2R < 2c <= d(x,y)+4c`.

Now suppose `R>=c`. Choose arbitrary arclength minimizing geodesics

\[
 u:[0,p]\to M,\quad u(0)=o,\ u(p)=x,\qquad
 v:[0,q]\to M,\quad v(0)=o,\ v(q)=y.
\]

A zero-length radial geodesic has the one-point domain `[0,0]` and constant
image. Set

\[
 \alpha=\min(c,p),\quad\beta=\min(c,q),\qquad
 a=u(p-\alpha),\quad b=v(q-\beta).
\]

Because `u,v` are isometric parametrizations,

\[
 d(x,a)=\alpha,\quad d(y,b)=\beta,\quad
 d(o,a)=p-\alpha=\max(p-c,0),\quad
 d(o,b)=q-\beta=\max(q-c,0).
\]

The nonnegative condition `R-c >= 0` is essential in the next elementary
inequality: since `p,q <= R`,

\[
 \max(p-c,0)\le R-c,\qquad \max(q-c,0)\le R-c. \tag{1}
\]

Apply (H), with the same original center `o`, to the new endpoints `a,b`.
Choose an arclength minimizing geodesic `w:[0,m] -> M`, where `m=d(a,b)`.
Then

\[
 d(o,w(t))\le \max\{d(o,a),d(o,b)\}+c
 \le (R-c)+c=R. \tag{2}
\]

If `a=b`, use the constant middle path; it satisfies (2) directly even if the
word "geodesic" were conventionally reserved for distinct endpoints.

The radial tail `u([p-alpha,p])` has center distances between `p-alpha` and
`p`, all at most `R`. The tail `v([q-beta,q])` similarly stays in the original
ball. These are the only outer pieces.

Let `L=alpha+m+beta`. If `L=0`, all successive vertices are equal, so the
constant path is valid. If `L>0`, define the concatenation on `[0,L]` by

\[
 \eta(s)=
 \begin{cases}
 u(p-s),&0\le s\le\alpha,\\
 w(s-\alpha),&\alpha\le s\le\alpha+m,\\
 v(q-\beta+s-\alpha-m),&\alpha+m\le s\le L.
 \end{cases} \tag{3}
\]

A piece with zero duration is omitted, except for its matching junction value.
The formulas agree at the junctions: first `a`, then `b`. Each piece is
continuous, so the finite pasting is continuous. Each piece has image in the
original closed ball, by (1)-(2) and the radial-tail calculation. Finally set
`gamma(t)=eta(Lt)` for `t in [0,1]`.

## Exact metric-length justification

For `s<t` in a single piece of (3), the distance of the images is `t-s`.
For `s<t` crossing a junction, insert the junction times and use the triangle
inequality on the finitely many pieces. This gives

\[
 d(\eta(s),\eta(t))\le t-s.
\]

Consequently every partition sum for `eta` is at most `L`. For the reverse
bound, the partition consisting of `0,alpha,alpha+m,L`, with duplicate times
removed, has sum

\[
 d(x,a)+d(a,b)+d(b,y)=\alpha+m+\beta=L.
\]

Zero-length pieces contribute zero and do not affect this identity. Therefore
`Len_d(eta)=L`. Linear reparameterization preserves partition sums bijectively,
so `Len_d(gamma)=L`. This proves rectifiability directly from the definition;
no compactness or existence of a restricted-ball shortest path was invoked.

By the ordinary ambient triangle inequality,

\[
 m=d(a,b)\le d(a,x)+d(x,y)+d(y,b)
 =\alpha+d(x,y)+\beta.
\]

Thus

\[
 \operatorname{Len}_d(\gamma)
 =\alpha+m+\beta
 \le d(x,y)+2\alpha+2\beta
 \le d(x,y)+4c.
\]

This proves the exact proposition (C).

## Boundary and assumption audit

| Case | Check |
| --- | --- |
| `R<c` | Radial path has length at most `2R`; no attempt to use a negative inner radius is made. |
| `R=c` | Every point in the ball has `p,q<=c`, so `a=b=o`; the middle piece is constant. |
| `c=0`, any `R>=0` | Retreat amounts vanish, `a=x,b=y`; (H) supplies the required geodesic directly. |
| `R=0,c>0` | First branch applies; a metric ball of radius zero contains only `o`, so the constant path suffices. |
| `R=c=0` | Second branch has all three pieces constant. |
| `p<c` or `q<c` | That endpoint retreats only its actual center distance and lands at `o`; no radial ray beyond `o` is required. |
| `p=c` or `q=c` | The corresponding inner point is exactly `o`, with retreat length exactly `c`. |
| Interior endpoints | Their new center distances may be strictly below `R-c`; (1) remains valid. |
| Boundary endpoints | Inequalities are non-strict throughout; the path may touch the original boundary. |
| `x=y` | The initial constant path has length zero; the unsimplified construction is also within the stated bound. |
| `a=b` | Constant middle path, no division by its length. |
| Nonunique geodesics | Radial choices can be arbitrary; only the middle one must be chosen as (H) promises for `(o,a,b)`. |
| Incomplete or nonproper space | Only three supplied finite minimizing segments and finite pasting are used. |
| Lack of global radial retraction | No map on the whole ball is constructed; the two retreats are independent finite choices. |
| No fellow travelling or thin/thick decomposition | The middle-length bound is a single triangle inequality, independent of tracking behavior. |
| No continuous selection of geodesics | The conclusion is per pair; joint dependence on `(o,x,y)` is not claimed or needed. |

For the intrinsic length distance of the closed ball, define the infimum over
all continuous rectifiable in-ball paths from `x` to `y`, using ambient metric
length. The construction shows this set is nonempty and gives its upper bound.
Every such path has length at least `d(x,y)` by the endpoint partition.
Therefore

\[
 d(x,y)\le d_{\overline B(o,R)}^{\rm int}(x,y)
 \le d(x,y)+4c.
\]

The infimum need not be attained. No intrinsic minimizing geodesic is asserted.

## Conditional Teichmüller specialization

This family proves the abstract implication (H) -> (C). To promote it to the
submitted Teichmüller claim, a separate source-backed family must establish:
actual `d_T=(1/2)inf log K` is geodesic and the cited Lenzhen-Rafi theorem gives
one finite `c_g` for the fixed topology, valid for every center and every
endpoint pair, with the stated non-strict radial bound on a minimizing segment.
The normalization, topology dependence, closed-ball endpoints, and absence of
thickness restrictions belong to that dependency. This review does not assume
its validity merely because the submitted proof cites it.
