# Route C: structural reductions for a five-partition theorem

**Discovery checkpoint:** 2026-08-01T15:43:43-07:00  
**Proof-audit checkpoint:** 2026-08-01T15:57:06-07:00  
**Scope:** first-principles work only; no literature or web search was used.  
**Status:** partial positive theorems and exact barriers, not a resolution of
the four-dimensional problem.

Throughout, empty parts are allowed and have diameter zero.  For a compact
set \(K\subset\mathbb R^4\), write \(D=\operatorname {diam}K>0\).

## Claim ledger

The rigorous outputs of this route are:

1. Strict Borsuk partitionability is equivalent to coloring a
   **near-diameter graph with one uniform gap**.  Exact-diameter graph
   colorability alone is insufficient for infinite compact sets.
2. If every bounded set in \(\mathbb R^4\) has a five-partition, then there is
   in fact a dimension-wide constant \(q<1\) such that every such set has a
   five-partition with all part diameters at most \(qD\).  Consequently the
   full assertion is equivalent to a uniform theorem about finite sets.
3. Every diametral pair consists of two uniquely exposed points in the pair
   direction, with a quantitative quadratic separation from its two support
   hyperplanes.  Diametral neighbor directions at one endpoint have mutual
   angle at most \(60^\circ\), but their number need not be finite.
4. If every endpoint of a diametral pair in the convex hull has a unique
   outward normal (global \(C^1\) regularity is unnecessary), five parts
   suffice.  The proof is an explicit regular-simplex cover of the normal
   sphere.  This is a genuine partial class, not an approximation argument
   for arbitrary bodies.
5. A regular-simplex fan gives five smaller-diameter parts whenever the
   circumradius satisfies
   
   \[
   R^2<\frac{3}{10}D^2.
   \]
   
   The angular constant is sharp for this fan, and an exact three-point set
   realizes equality at \(R^2=3D^2/10\).
6. If \(K\) contains the five vertices of a regular four-simplex of side
   \(D\), nearest-vertex cells give five parts with an explicit contraction.
   This also yields, nonconstructively but rigorously, an
   \(\varepsilon>0\) such that every set with
   \(R^2>(2/5-\varepsilon)D^2\) has a five-partition.

Thus a circumradius-based proof is reduced to a middle shell

\[
  \frac{3}{10}\le \frac{R^2}{D^2}\le \frac25-\varepsilon,
\]

plus the problem of handling nonsmooth normal cones uniformly.

## 1. Strictness, closure, and finite obstructions

### 1.1 Closure is harmless; loss of a uniform gap is not

**Lemma 1 (closure equivalence).** A bounded set \(S\) has a partition into
\(k\) sets of diameter strictly below \(D=\operatorname {diam}S\) if and only
if its closure \(K=\overline S\) does.

**Proof.** Restriction proves one implication.  Conversely, suppose
\(S=A_1\sqcup\cdots\sqcup A_k\) and
\(r_i=\operatorname {diam}A_i<D\).  Since there are only finitely many parts,
\(r=\max_i r_i<D\).  The finitely many closures \(\overline {A_i}\) cover
\(\overline S\), and each has diameter at most \(r\).  Remove overlaps in a
fixed order to obtain a partition without increasing any diameter. \(\square\)

The convex hull also has the same diameter:

\[
 \operatorname {diam}(\operatorname {conv}K)=\operatorname {diam}K,
\]

because the distance between two convex combinations is at most the
corresponding weighted average of pairwise distances.  Partitioning the
convex hull is therefore a sufficient positive strategy.  It is not an
equivalent reduction: a partition of \(K\) does not automatically cover its
convex hull after taking the convex hulls of the individual parts.

For \(0\le r<D\), define the threshold graph

\[
 \Gamma_r(K):\qquad xy\in E\quad\Longleftrightarrow\quad
 \lVert x-y\rVert>r.
\]

**Lemma 2 (the correct graph formulation for compact sets).** The following
are equivalent.

1. \(K\) is a union of \(k\) sets, each of diameter below \(D\).
2. For some \(r<D\), the graph \(\Gamma_r(K)\) is \(k\)-colorable.
3. For some \(r<D\), every finite induced subgraph of \(\Gamma_r(K)\) is
   \(k\)-colorable.

**Proof.** A partition has a common upper diameter
\(r=\max_i\operatorname {diam}A_i<D\), and its colors properly color
\(\Gamma_r(K)\).  Conversely, each color class of a proper coloring of
\(\Gamma_r(K)\) has diameter at most \(r\).

For the last equivalence, use graph compactness.  In the compact product
\(\{1,\ldots,k\}^{K}\), the condition that the endpoints of one edge receive
different colors is clopen.  Every finite collection of these constraints is
satisfied by a coloring of the finite set of involved vertices.  The finite
intersection property supplies a coloring satisfying all edge constraints.
\(\square\)

In particular, failure has the exact finite-witness form

\[
 \forall r<D\quad \exists F\subset K\text{ finite such that }
 \chi(\Gamma_r(K)[F])>k.                    \tag{1}
\]

These are finite **near-diameter** obstructions; they need not converge to a
finite obstruction in the exact diameter graph.

### 1.2 A universal positive theorem would automatically be uniform

**Theorem 3 (uniform-gap principle).** Fix \(n,k\).  If every bounded subset
of \(\mathbb R^n\) of positive diameter has a \(k\)-partition into
smaller-diameter parts, then there is a number \(q=q(n,k)<1\) such that every
such set has a \(k\)-partition whose part diameters are at most \(qD\).

**Proof.** By Lemma 1, consider compact sets.  Normalize to diameter one,
translate one point to the origin, and let \(\mathcal H\) be the family of
all resulting compact subsets of the closed unit ball.  The conditions
\(0\in K\) and \(\operatorname {diam}K=1\) are Hausdorff-closed, and the
hyperspace of nonempty compact subsets of a compact metric space is compact.
Thus \(\mathcal H\) is compact.

For each \(K\in\mathcal H\), choose a partition with maximum part diameter
\(r_K<1\).  If the Hausdorff distance from \(L\) to \(K\) is less than
\(\delta\), assign each point of \(L\) the color of a point of \(K\) within
\(\delta\).  The resulting same-color distances are at most
\(r_K+2\delta\).  Taking
\(\delta_K=(1-r_K)/4\) gives a neighborhood of \(K\) with contraction at most
\((1+r_K)/2<1\).  Finitely many such neighborhoods cover \(\mathcal H\); the
maximum of their finitely many contraction factors is the desired \(q<1\).
Scaling and Lemma 1 finish the proof. \(\square\)

**Corollary 4 (uniform finite criterion).** The assertion \(b(4)\le5\) is
equivalent to the existence of \(q<1\) such that every finite
\(F\subset\mathbb R^4\) has a five-partition with maximum part diameter at
most \(q\operatorname {diam}F\).

Only the reverse implication needs comment.  For compact \(K\) of diameter
\(D\), put an edge between pairs farther than \(qD\).  Every finite
\(F\subset K\) can be colored so that same-color distances are at most
\(q\operatorname {diam}F\le qD\).  Graph compactness then colors all of \(K\),
and Lemma 1 handles bounded nonclosed sets.

This is a useful target correction: proving merely that each finite set has
some configuration-dependent strict improvement does not complete the
limiting argument.

### 1.3 Exact-diameter colorability does not control strict diameter

**Exact barrier (the circle).** Embed the unit circle in a coordinate
two-plane of \(\mathbb R^4\).  Its exact diameter graph consists only of
antipodal pairs and is two-colorable: color the two half-open semicircles
differently.  Nevertheless, the circle cannot be partitioned into two sets
of diameter below \(2\).

Indeed, if both part diameters were at most \(r<2\), choose an odd
\(N=2m+1\) so large that

\[
 2\cos\frac{\pi}{2N}>r.
\]

On the regular \(N\)-gon, join vertex \(j\) to \(j+m\pmod N\).  These edges
form an odd \(N\)-cycle, and every one has the displayed length.  The alleged
partition would properly two-color this odd cycle, a contradiction.

This example simultaneously shows why nonclosed color classes and exact
diameter graphs can hide a supremal distance: each half-open semicircle has
diameter \(2\), although it contains no antipodal pair.

## 2. Geometry of diametral pairs

Let \(C\subset\mathbb R^4\) be compact and convex with diameter \(D\), and let
\(x,y\in C\) satisfy \(\lVert x-y\rVert=D\).  Put
\(u=(y-x)/D\).

**Lemma 5 (quadratic support separation).** For every \(z\in C\),

\[
 \left\langle z-x,u\right\rangle
 \ge \frac{\lVert z-x\rVert^2}{2D},\qquad
 \left\langle z-y,u\right\rangle
 \le-\frac{\lVert z-y\rVert^2}{2D}.        \tag{2}
\]

Consequently the hyperplanes through \(x\) and \(y\) perpendicular to \(u\)
support \(C\), and \(x,y\) are the unique support points in the directions
\((-u,u)\), respectively.

**Proof.** Expand \(\lVert z-y\rVert^2\le D^2\) after writing
\(z-y=z-x-Du\); this gives the first inequality.  Expand
\(\lVert z-x\rVert^2\le D^2\) after writing \(z-x=z-y+Du\); this gives the
second.  Equality with either supporting hyperplane forces the corresponding
squared norm on the right to vanish. \(\square\)

Thus every endpoint of a diameter edge is exposed, even when the boundary is
nonsmooth.  Notice the distinction: it is uniquely exposed by the
**diameter-specific direction**, but it can have many other outward normals.

**Lemma 6 (local \(60^\circ\) constraint).** If \(y,z\) are both diametral
neighbors of \(x\), and

\[
 u=(y-x)/D,\qquad v=(z-x)/D,
\]

then \(\langle u,v\rangle\ge1/2\).  Equality holds exactly when \(y,z\) are
also a diametral pair.

This follows immediately from

\[
 \lVert y-z\rVert^2=2D^2(1-\langle u,v\rangle)\le D^2.
\]

In particular, a clique in a diameter graph is an equidistant set and has at
most five vertices in \(\mathbb R^4\); a five-clique is a regular
four-simplex.  This local fact gives no degeneracy or degree bound.  For an
exact counterexample, take

\[
 x=0,\qquad
 y(t)=\left(\frac{\sqrt3}{2},\frac12\cos t,
                    \frac12\sin t,0\right),\quad 0\le t<2\pi.
\]

The set \(\{x\}\cup\{y(t)\}\) has diameter one, while \(x\) has continuum
many diametral neighbors.  Distances among the \(y(t)\)'s are at most one.

A separate tempting simplification also fails: diametral endpoints need not
be antipodal about the circumcenter.  The three vertices of an equilateral
triangle (embedded in \(\mathbb R^4\)) are all mutually diametral, and their
radial directions from the circumcenter meet at \(120^\circ\), not
\(180^\circ\).

## 3. A complete partial theorem when diameter endpoints are smooth

For a full-dimensional convex body \(C\), let

\[
 E_D(C)=\{x\in C:\text{ some }y\in C\text{ satisfies }
                    \lVert x-y\rVert=\operatorname {diam}C\}.
\]

Call \(x\in\partial C\) *smooth* if it has a unique unit outward normal.
The hypothesis below asks for smoothness only on \(E_D(C)\), not on the
rest of the boundary.

Choose unit vectors \(v_0,\ldots,v_4\in S^3\) forming a regular simplex:

\[
 \sum_i v_i=0,\qquad \langle v_i,v_j\rangle=-\frac14\quad(i\ne j).
\]

They form a tight frame,

\[
 \sum_i v_i v_i^{\mathsf T}=\frac54 I.
\]

Define five closed normal caps

\[
 F_i=\{n\in S^3:\langle n,v_i\rangle\ge1/4\}.               \tag{3}
\]

These caps cover \(S^3\).  To see this, put
\(a_i=\langle n,v_i\rangle\) and \(M=\max_i a_i\).  Then
\(\sum a_i=0\) and \(\sum a_i^2=5/4\).  With \(b_i=M-a_i\ge0\),

\[
 \frac54=\sum a_i^2=\sum b_i^2-5M^2
 \le (\sum b_i)^2-5M^2=20M^2,
\]

so \(M\ge1/4\).  No \(F_i\) contains an antipodal pair, since membership of
both \(n\) and \(-n\) would require simultaneously
\(\langle n,v_i\rangle\ge1/4\) and
\(\langle n,v_i\rangle\le-1/4\).

**Theorem 7 (smooth diameter endpoints).** If the closed convex hull \(C\) of
a bounded set \(S\subset\mathbb R^4\) is full-dimensional and every point of
\(E_D(C)\) is smooth, then \(S\) has a five-partition into sets of diameter
strictly below \(\operatorname {diam}S\).

**Proof.** It suffices to partition the convex hull \(C\).  On its boundary,
choose one unit outward normal \(\nu(x)\) at each point \(x\), and assign
\(x\) to the least \(i\) for which \(\nu(x)\in F_i\); call the resulting
boundary classes \(B_i\).  No continuity of this selector is assumed.

Fix \(o\in\operatorname {int}C\).  Every \(x\ne o\) lies on a unique radial
segment from \(o\) to a boundary point \(b(x)\).  Give \(x\) the color of
\(b(x)\), and assign \(o\) arbitrarily.  The radial endpoint map is continuous
up to the boundary.  For the only case needed here, if
\(x_m\to p\in\partial C\) and a subsequence of \(b(x_m)\) tends to \(b\), write
\(x_m=o+t_m(b(x_m)-o)\).  A limit \(t<1\) would put \(p\) in the interior of
the segment from the interior point \(o\) to \(b\), hence in
\(\operatorname {int}C\); therefore \(t=1\) and \(b=p\).

If the closure of one color had diameter \(D\), compactness would give a
diametral pair \(p,q\) in that closure.  Every diametral endpoint is on the
boundary: an interior endpoint can be moved slightly directly away from the
other endpoint, increasing their distance.  A sequence of points of color
\(i\) tending to \(p\) has radial endpoints \(p_m\in B_i\) tending to \(p\),
by the preceding paragraph.  By compactness of the unit sphere, a subsequence
of \(\nu(p_m)\) tends to a unit vector \(n_p\in F_i\).  The graph of the
outward-normal relation is closed: passing to the limit in

\[
 \langle z-p_m,\nu(p_m)\rangle\le0\qquad(z\in C)
\]

shows that \(n_p\) is an outward normal at \(p\).  Since \(p\in E_D(C)\) is
smooth, \(n_p\) is its unique outward normal.  The same argument at \(q\)
puts its unique normal \(n_q\) in \(F_i\).  Lemma 5 gives \(n_q=-n_p\), which
is impossible in the antipodal-free cap \(F_i\).  Thus the compact closure of
each color has diameter strictly below \(D\). \(\square\)

In particular, the theorem applies when \(C\) is \(C^1\), but it also permits
nonsmooth boundary points that are not diameter endpoints.

The uniqueness hypothesis is doing real work.  In the cube
\(C=[-1,1]^4\), the opposite vertices

\[
 p=(1,1,1,1),\qquad q=-p
\]

form a diametral pair.  Yet \(e_1\) is an outward normal at \(p\) and
\(-e_2\) is an outward normal at \(q\).  These two normals are orthogonal, not
antipodal, and both lie in the antipodal-free cap centered at
\((e_1-e_2)/\sqrt2\) with threshold \(1/4\).  Therefore “choose an arbitrary
normal, then color the normal sphere” does not extend Theorem 7 across a
nonsmooth diameter endpoint.

## 4. Circumradius structure and the sharp Jung endpoint

Let \(B(c,R)\) be the minimum enclosing ball of \(K\).  Its contact set is
\(T=K\cap\partial B(c,R)\).

**Lemma 8 (contact balance).** The center \(c\) lies in
\(\operatorname {conv}T\).  Consequently there are \(2\le m\le5\), contact
points \(q_1,\ldots,q_m\), and positive weights \(\lambda_i\) such that

\[
 \sum_i\lambda_i=1,\qquad
 \sum_i\lambda_i(q_i-c)=0.                                  \tag{4}
\]

**Proof.** If \(c\notin\operatorname {conv}T\), compactness and strict
separation give a unit vector \(w\) and \(\alpha>0\) with
\(\langle t-c,w\rangle\ge\alpha\) for every \(t\in T\).  The same lower
bound, with \(\alpha/2\), holds in a relative neighborhood of \(T\) in \(K\).
Moving \(c\) a sufficiently small distance toward \(w\) decreases the
distance to every point in that neighborhood.  The compact complement of a
slightly smaller neighborhood has a uniform radial slack below \(R\), so the
same displacement still leaves all of it inside a ball of radius below
\(R\).  This contradicts minimality.  Caratheodory's theorem in
\(\mathbb R^4\) gives at most five points. \(\square\)

The balance identity gives a sharp and useful defect formula.  Pad the list
to five points by allowing zero weights.  Then

\[
 R^2=\frac12\sum_{i,j}\lambda_i\lambda_j
                   \lVert q_i-q_j\rVert^2                  \tag{5}
\]

and hence

\[
 \boxed{
 \frac25D^2-R^2
 =\frac{D^2}{2}\sum_{i=1}^5(\lambda_i-1/5)^2
 +\frac12\sum_{i\ne j}\lambda_i\lambda_j
       \bigl(D^2-\lVert q_i-q_j\rVert^2\bigr).}             \tag{6}
\]

Every term on the right is nonnegative.  This proves
\(R^2\le2D^2/5\) from first principles.  Equality holds exactly when there
are five equal weights and all ten contact distances equal \(D\), namely when
the contact points form a regular four-simplex of side \(D\).

Formula (6) is stronger than the radius inequality: small Jung defect forces
all five weights toward \(1/5\) and, once those weights are bounded away from
zero, forces every contact distance toward \(D\).

## 5. A five-cone theorem below \(R^2=3D^2/10\)

Retain regular-simplex directions \(v_0,\ldots,v_4\), and define their
maximal-coordinate fan

\[
 C_i=\{x:\langle x,v_i\rangle\ge\langle x,v_j\rangle
                    \text{ for all }j\}.                   \tag{7}
\]

For \(i=0\), this cone is generated by the four unit rays
\(r_j=-v_j\) (\(j=1,\ldots,4\)), whose Gram matrix has diagonal \(1\) and
off-diagonal entries \(-1/4\).  Explicitly, if \(x\in C_0\), then

\[
 \alpha_j=\frac45\bigl(\langle x,v_0\rangle-\langle x,v_j\rangle\bigr)
 \ge0,\qquad
 x=\sum_{j=1}^4\alpha_j(-v_j).
\]

**Lemma 9 (exact angular diameter of a simplex fan cone).** For nonzero
\(x,y\in C_i\),

\[
 \frac{\langle x,y\rangle}{\lVert x\rVert\lVert y\rVert}
 \ge-\frac23.                                                \tag{8}
\]

The constant is attained.

**Proof.** It is enough to take \(i=0\).  Write
\(x=\sum_{j=1}^4 a_jr_j\) and \(y=\sum_{j=1}^4 b_jr_j\), with nonnegative
coefficients.  Rescale so \(\sum a_j=\sum b_j=1\).  Put

\[
 A=\sum a_j^2,\quad B=\sum b_j^2,\quad c=\sum a_jb_j.
\]

Direct use of the Gram matrix gives

\[
 \cos(x,y)=\frac{5c-1}{\sqrt{(5A-1)(5B-1)}}.                \tag{9}
\]

If \(c\ge1/5\), this is nonnegative.  Otherwise set
\(p^2=A-1/4\) and \(q^2=B-1/4\).  Centering the probability vectors \(a,b\)
at \((1/4,\ldots,1/4)\) and applying Cauchy--Schwarz gives

\[
 c\ge\frac14-pq,
 \quad\text{so}\quad pq\ge\frac14-c.
\]

Moreover,

\[
 \begin{aligned}
 \sqrt{(5A-1)(5B-1)}
 &=\sqrt{(5p^2+1/4)(5q^2+1/4)}\\
 &\ge5pq+\frac14
 \ge\frac32-5c
 \ge\frac32(1-5c).
 \end{aligned}
\]

Substitution in (9) proves (8).  Equality is obtained when \(a\) is uniform
on two indices and \(b\) is uniform on the complementary two indices.
\(\square\)

**Theorem 10 (small circumradius regime).** If

\[
 R^2<\frac{3}{10}D^2,                                      \tag{10}
\]

then \(K\) has a five-partition into sets of diameter below \(D\).

**Proof.** Center the fan (7) at \(c\), the circumcenter, and assign every
point to one cone containing its radial vector.  If two same-color points
have radial lengths \(r,s\le R\), Lemma 9 gives

\[
 \lVert x-y\rVert^2
 \le r^2+s^2+\frac43rs
 \le\frac{10}{3}R^2<D^2.
\]

\(\square\)

The strict inequality in (10) cannot simply be replaced by a weak inequality
for this fixed fan.  The following exact example realizes every equality in
the estimate.

Let \(v_0,\ldots,v_4\) be the regular simplex above and put

\[
 a=-\sqrt{\frac23}(v_1+v_2),\qquad
 b=-\sqrt{\frac23}(v_3+v_4),\qquad z=-v_0.
\]

These are unit vectors with

\[
 \langle a,b\rangle=-\frac23,qquad
 \langle a,z\rangle=\langle b,z\rangle=-\frac1{\sqrt6},
 \qquad a+b+\sqrt{\frac23}z=0.
\]

For \(R=\sqrt{3/10}\,D\), the three-point set

\[
 K_*=\{Ra,Rb,Rz\}
\]

has diameter \(D\), realized by \(Ra,Rb\); the other two squared distances
are

\[
 \frac35\left(1+\frac1{\sqrt6}\right)D^2<D^2.
\]

The displayed positive dependence shows that \(0\) is in the convex hull of
the three contact directions, so \(B(0,R)\) is their minimum enclosing ball.
Both \(a,b\in C_0\).  In fact their maximizing-index sets are
\(\{0,3,4\}\) and \(\{0,1,2\}\), so the common “least maximizing index” tie
rule puts the diametral pair in the same cell.  A more adaptive boundary rule
might repair this particular set; the example proves that neither the metric
bound nor the stated fixed tie rule supplies strictness at equality.  Any
claim at the weak threshold needs a separate, closure-stable tie analysis.

## 6. Nearest-anchor cells at the regular-simplex endpoint

The equality case of the Jung bound admits a different, strictly contracting
partition.

**Theorem 11 (regular-simplex anchors).** Suppose \(K\) has diameter \(D\)
and contains five points \(q_0,\ldots,q_4\) with every mutual distance equal
to \(D\).  Then nearest-anchor assignment partitions \(K\) into five sets of
diameter at most \(\kappa D\), where

\[
 \kappa^2
 =4\left(\frac{103}{125}-\frac{4\sqrt{15}}{25}\right)
 <1.                                                        \tag{11}
\]

Numerically, the proved (not optimized) value is \(\kappa\approx0.9040\).
The strict inequality in (11) is exact: it is equivalent to
\(287<80\sqrt{15}\), whose square is \(82369<96000\).

**Proof.** Scale to \(D=1\), translate the simplex centroid to zero, and use
the isometric model

\[
 H=\{z\in\mathbb R^5:\sum_jz_j=0\},\qquad
 q_i=\frac1{\sqrt2}\left(e_i-\frac15\mathbf1\right).
\]

Then \(\lVert q_i\rVert^2=2/5\) and the mutual distances are one.  Every
point of \(K\) lies in

\[
 L=\bigcap_{j=0}^4\overline B(q_j,1).
\]

Let \(L_0\) be the part of \(L\) nearest to \(q_0\).  For \(z\in L_0\), put
\(r^2=\lVert z\rVert^2\) and \(s=z_0\).  Nearest-anchor assignment gives
\(z_0\ge z_j\) for every \(j\), hence \(s\ge0\).  The five ball inequalities
give

\[
 z_j\ge \ell:=\frac{r^2-3/5}{\sqrt2}\quad(0\le j\le4).
\]

Thus every coordinate lies in \([\ell,s]\).  From
\((s-z_j)(z_j-\ell)\ge0\), summing over \(j\) and using
\(\sum_jz_j=0\), one obtains

\[
 r^2\le-5s\ell,
 \qquad\text{and therefore}\qquad
 r^2\le\frac{3s}{\sqrt2+5s}.                               \tag{12}
\]

For \(t>0\), since \(\langle z,q_0\rangle=s/\sqrt2\),

\[
 \left\lVert z-tq_0\right\rVert^2
 =r^2-\sqrt2ts+\frac25t^2.
\]

Over all \(s\ge0\), elementary differentiation gives, for \(0<t\le3/2\),

\[
 \max_s\left(\frac{3s}{\sqrt2+5s}-\sqrt2ts\right)
 =\frac{3+2t-2\sqrt{6t}}5.
\]

Taking \(t=2/5\) and applying (12) shows

\[
 L_0\subset \overline B\left(\frac25q_0,\rho\right),
 \qquad
 \rho^2=\frac{103}{125}-\frac{4\sqrt{15}}{25}<\frac14.
\]

The same holds for every \(L_i\) by symmetry.  Hence
\(\operatorname {diam}L_i\le2\rho=\kappa<1\), and arbitrary tie-breaking
among nearest anchors preserves the bound.  Rescale to \(D\). \(\square\)

This endpoint statement is robust.

**Lemma 12 (robust anchor neighborhood).** There is a neighborhood \(U\) of
the regular-simplex five-tuple such that, for every anchor tuple
\((a_0,\ldots,a_4)\in U\), all five sets

\[
 \left(\bigcap_j\overline B(a_j,1)\right)
 \cap\{z:\lVert z-a_i\rVert\le\lVert z-a_j\rVert\ \forall j\}
                                                               \tag{13}
\]

have diameter below one.

**Proof.** Otherwise anchors converging to a regular simplex would admit
points \(x_m,y_m\) in one common cell with
\(\lVert x_m-y_m\rVert\ge1\).  The ball constraints bound both sequences.
Pass to a subsequence.  All inequalities in (13) are closed, so the limits
lie in one regular-simplex cell, contradicting Theorem 11. \(\square\)

Combining this with the exact defect identity gives a second radius regime.

**Corollary 13 (nonexplicit high-circumradius regime).** There exists
\(\varepsilon\in(0,1/10)\) such that every compact
\(K\subset\mathbb R^4\) satisfying

\[
 R^2>\left(\frac25-\varepsilon\right)D^2                  \tag{14}
\]

has a five-partition into smaller-diameter sets.

**Proof.** If not, normalize \(D=1\) and take a sequence with
\(R_m^2\to2/5\).  Choose balanced contact representations (4), padded to five
points.  Formula (6) forces every weight to \(1/5\) and every mutual contact
distance to one.  After translating the circumcenters to zero and passing to
a subsequence, the five anchors converge to a regular four-simplex.  Every
point of \(K_m\) lies in all five unit balls about these anchors.  For large
\(m\), Lemma 12 says that nearest-anchor cells have diameter below one, a
contradiction. \(\square\)

An explicit useful next step is to quantify Lemma 12 and combine it with
(6), thereby producing a numerical value of \(\varepsilon\).

## 7. What the partial results rule out and what remains

The following tempting statements are false, with exact witnesses given
above.

| Tempting statement | Exact obstruction |
|---|---|
| A proper coloring of the exact diameter graph gives strict smaller diameter for a compact set. | The unit circle: its antipodal matching is 2-colorable, but its near-diameter graphs contain arbitrarily large odd cycles. |
| Diameter endpoints are antipodal about a circumcenter. | An equilateral triangle. |
| The \(60^\circ\) neighbor-direction lemma gives bounded degree or degeneracy. | The continuum star \(\{0\}\cup\{y(t)\}\). |
| At a nonsmooth point, choosing any outward normal is enough for normal-sphere coloring. | Opposite vertices of the four-cube with selected normals \(e_1,-e_2\). |
| The centered regular-simplex fan is automatically strict at \(R^2\le3D^2/10\). | The exact three-point set \(K_*\) at equality. |
| Pointwise strict improvements on finite approximants pass to a compact limit. | Lemmas 2--4 show that a common threshold is required; the circle displays the failure mechanism. |

The current positive architecture covers:

- every convex hull whose diameter endpoints are smooth, at every
  circumradius;
- every set with \(R^2<3D^2/10\);
- every set containing a regular diameter simplex;
- by compactness, every set in a nonzero band below the sharp Jung radius
  \(R^2=2D^2/5\).

The unresolved circumradius shell is compactly separated from both endpoints,
but the genuine obstruction is not radius alone.  It is the interaction of
diameter-specific normals with multivalued normal cones.  A successful
universal argument must preserve a uniform near-diameter gap (Theorem 3), not
merely separate exact diametral pairs.

Three concrete continuation targets are:

1. Quantify robust nearest-anchor cells from (13), then use (6) to maximize
   the certified high-radius band.
2. In the middle shell, orient or deform the simplex fan using the balanced
   contact set.  Any equality analysis must include boundary tie behavior,
   as \(K_*\) shows.
3. Remove the endpoint-smoothness hypothesis from Theorem 7 by finding a
   closed coloring rule for multivalued normal cones.  The cube example shows
   that an arbitrary normal selector is insufficient; the diameter-specific
   antipodal normals must control the color closures.

## Research checkpoint

**2026-08-01T15:43:43-07:00.** Established the uniform finite-threshold
reduction, the smooth-diameter-endpoint partial theorem, the exact low-radius
fan constant, the regular-simplex anchor contraction, the high-radius
compactness band, and five explicit falsification examples.  No universal
five-partition or counterexample follows yet.

**2026-08-01T15:57:06-07:00.** Completed an exact algebra and hostile
limiting-case audit.  Strengthened the normal-cap theorem from global unique
normality to unique normality only at diameter endpoints; corrected the
contact-balance compactness argument; and checked the radical constants, the
three-point equality witness, and the Jung defect identity with separate
exact symbolic calculations.

Best-guess completion of Route C toward a universal positive proof:
**18%**.  Best-guess completion of the overall four-dimensional resolution
from this route alone: **6%**.  The increase reflects rigorous endpoint
regimes; the middle-radius nonsmooth case remains the central barrier.
