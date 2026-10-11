# Fundamental groups of reduced real elliptic divisor spaces

## Statement and scope

Let $E$ be a smooth projective geometrically connected curve of genus one over
ℝ with $E(\mathbb R)\ne\varnothing$, and let $A$ be a reduced effective divisor of degree
$d\ge1$ supported on $E(\mathbb R)$. Write $C_1,\ldots,C_k$ for the real components
occupied by $A$, and put $m_i=\#(A\cap C_i)>0$. Thus
$m_1+\cdots+m_k=d$. Let $F_A$ consist of the effective divisors $D$ satisfying:

1. $D$ has $d$ distinct real support points;
2. $D$ has exactly $m_i$ points on $C_i$, and no points on the other real components;
3. $D$ is linearly equivalent to $A$.

Divisors are unordered. Give $F_A$ the subspace topology from the complex
symmetric product — equivalently, from the complete linear system containing
$A$. Then $F_A$ is connected and has a contractible universal cover, whose
deck group is

$$
K=\{(z_1,\ldots,z_k)\in\mathbb Z^k:z_1+\cdots+z_k=0\}.
$$

Consequently

$$
\pi_1(F_A,A)\cong\mathbb Z^{k-1}.
$$

Moreover, $F_A$ is the entire connected component containing $A$ in the
space of reduced totally real divisors linearly equivalent to $A$. A real
elliptic curve has at most two real components, so the possibilities here are
the trivial group and ℤ.

This statement concerns a fixed divisor class. It does not concern arbitrary
labeled embeddings, divisors with collisions, divisors containing nonreal
pairs, or curves of higher genus. The proof below is an elementary verification
of the stated genus-one result; it makes no claim of novelty.

## Relation to the original cubic problem

Oleg Viro's contribution [S1], printed p. 1289, defines the relevant space
using simple real divisors in a fixed linear-equivalence class. Its cubic
example explicitly gives π₁=0 when the support occupies one real component and
π₁=ℤ when it occupies both. Viro credits Ayşegül Öztürkalan for the initial
examples and observations. That wording does not attribute the proof below,
or sole authorship of a general theorem, to her.

For the original example, a smooth plane $M$-cubic has two real components.
A transverse intersection with another cubic, with all nine intersection
points real, supplies $d=9$. The theorem therefore reproduces the stated
dichotomy for the component based at $A$. The proof only needs the divisor
class of $A$; it does not require the second cubic to be nonsingular.

## Linear equivalence and real descent

Choose $O\in E(\mathbb R)$ as origin. The usual elliptic group structure identifies
$E$ with $\operatorname{Pic}^0(E)$ by
$P\mapsto\mathcal O_E(P-O)$. In particular, for effective degree-$d$
divisors $D=\sum_j P_j$ and $A=\sum_j Q_j$,

$$
D\sim A\quad\Longleftrightarrow\quad
\sum_j P_j=\sum_j Q_j\quad\hbox{in }E(\mathbb C).
\tag{1}
$$

For completeness, the genus-one identification can be obtained directly
from Riemann–Roch. A degree-one line bundle has a one-dimensional space of
sections, since its inverse has negative degree and the canonical bundle of
a genus-one curve is trivial. Its unique effective divisor is therefore one
point. Tensoring any degree-zero line bundle with $\mathcal O_E(O)$ produces that
degree-one line bundle. This proves the required bijection; transporting
tensor product gives the elliptic group law and (1). The resulting
Abel–Jacobi identification is an isomorphism of complex curves and commutes
with complex conjugation because $O$ is real.

There is no extra distinction here between equivalence of these divisors
over ℝ and over ℂ. Indeed, if $D-A=\operatorname{div}(f)$ for a complex
rational function $f$, conjugation preserves $D-A$. Hence
$\overline f/f=c\in\mathbb C^*$, because a rational function without zeros
or poles on a projective connected curve is constant. Conjugating again
gives $c\overline c=1$. Choose $\lambda\in\mathbb C^*$ with
$\lambda/\overline\lambda=c$. Then

$$
\overline{\lambda f}=\overline\lambda\,\overline f
=\overline\lambda c f=\lambda f.
$$

Thus $\lambda f$ is a real rational function with the same divisor. Conversely,
real linear equivalence plainly implies complex linear equivalence.

## The topology being used

The symmetric product $\operatorname{Sym}^d(E(\mathbb C))$ is the quotient
of $E(\mathbb C)^d$ by permutations. Its reduced totally real locus is the
unordered configuration space of distinct points of $E(\mathbb R)$. Fixing the
numbers of points on the real components gives the product

$$
B=\prod_{i=1}^k\operatorname{UConf}_{m_i}(C_i).
\tag{2}
$$

This product identification is a homeomorphism: component membership is
locally constant, and one can choose pairwise disjoint small arcs around
the finitely many support points to give local product charts. The
component-count conditions are both open and closed in the reduced real
configuration space.

The topology inherited from the complete linear system is the same one.
For $L=\mathcal O_E(A)$, the zero-divisor map

$$
\mathbb P H^0(E(\mathbb C),L)\to\operatorname{Sym}^d(E(\mathbb C))
$$

is continuous, has image exactly the effective divisors equivalent to
$A$, and is injective: two sections with the same zeros have constant
ratio. It is a homeomorphism onto its image, since its source is compact
and its target Hausdorff. Restricting to the reduced totally real locus
and a fixed distribution preserves the equality of these subspace
topologies. There is no labeling or chosen section in $F_A$.

## Circle coordinates and the Abel condition

The identity component $E(\mathbb R)^0$ is a compact connected one-dimensional
Lie group, hence isomorphic as a Lie group to ℝ/ℤ. Fix such an isomorphism
$\phi:\mathbb R/\mathbb Z\to E(\mathbb R)^0$. Choose one point $b_i$
on each $C_i$. Every point of $C_i$ is uniquely $b_i+\phi(t)$ for
$t\in\mathbb R/\mathbb Z$. Use the same φ on every coset.

For a divisor with the counts $m_i$, its elliptic sum is

$$
\sum_i m_i b_i+
\phi\left(\sum_{i,j}t_{i,j}\pmod {\mathbb Z}\right).
\tag{3}
$$

The first term is fixed. Because $A$ has the same distribution, its sum
lies in this same coset of $E(\mathbb R)^0$. Equations (1) and (3) therefore
reduce the fixed divisor class to one equation

$$
\sum_{i,j}t_{i,j}=\alpha\quad\hbox{in }\mathbb R/\mathbb Z.
\tag{4}
$$

The potentially nonidentity component contributes only the fixed coset
offset. No splitting of the entire real group into a product is needed.
In particular, one must not omit the fixed component-count hypothesis
while using equation (4).

## A universal cover of unordered circle configurations

For $m\ge1$, define

$$
U_m=\{x\in\mathbb R^m:x_1<x_2<\cdots<x_m<x_1+1\}.
$$

For $m=1$, this means $U_1=\mathbb R$. These strict linear inequalities define
a nonempty open convex set. Let $q_m$ send $x$ to the unordered set of
its residues modulo ℤ. It maps onto — and only onto — configurations of
$m$ distinct points of the circle.

Define the affine homeomorphism

$$
T_m(x_1,\ldots,x_m)=(x_2,\ldots,x_m,x_1+1).
$$

It preserves $U_m$, leaves $q_m$ unchanged, and satisfies

$$
T_m^m(x)=x+(1,\ldots,1),\qquad
\sum_j(T_mx)_j=\sum_jx_j+1.
\tag{5}
$$

The points over a configuration are precisely the iterates $T_m^n x$,
$n\in\mathbb Z$. To see this, list all real lifts of the configuration in one
bi-infinite increasing sequence. Every tuple in the fiber consists of
$m$ consecutive entries, starting at exactly one index. Changing the
starting index once applies $T_m$. Formula (5) also proves uniqueness
of the exponent.

This is a covering map, not merely a set quotient. Around a configuration
choose disjoint arcs, one around each point, and a cut outside those arcs.
The neighborhood of configurations having exactly one point in each arc
has an ordered real-lift chart $V\subset U_m$. Its inverse image is
the disjoint union of $T_m^n V$, and each such set maps homeomorphically
onto that neighborhood. These are evenly covered neighborhoods.

The ℤ-action is free by (5). It is properly discontinuous: for a compact
subset of $U_m$, the sum of its coordinates is bounded, so only finitely
many translates can meet that compact subset. The local charts above
give the stronger pointwise disjoint-neighborhood condition. Since
$U_m$ is contractible, it is a universal cover and the full deck group
is generated by $T_m$.

## Fixing the sum and identifying the quotient

Take

$$
U=\prod_i U_{m_i},\qquad
q=\prod_iq_{m_i}:U\longrightarrow B.
$$

After the circle identifications, $q$ is a covering with contractible
total space and deck group $G=\mathbb Z^k$, acting blockwise. Define

$$
s_i(x)=\sum_{j=1}^{m_i}x_{i,j},\qquad s(x)=\sum_i s_i(x).
$$

For $z=(z_1,\ldots,z_k)\in G$, equation (5) gives

$$
s_i(zx)=s_i(x)+z_i,\qquad s(zx)=s(x)+\sum_i z_i.
\tag{6}
$$

Choose a real lift $c$ of α in (4). Then

$$
q^{-1}(F_A)=\coprod_{n\in\mathbb Z}H_n,\qquad
H_n=\{x\in U:s(x)=c+n\}.
\tag{7}
$$

Each $H_n$ is nonempty: start anywhere in $U$, then translate all
coordinates of its first block by $(c+n-s(x))/m_1$. This changes the
total sum as required while preserving all block inequalities. Each
slice is convex and relatively open in its affine hyperplane; it is
contractible, of dimension $d-1$. This includes the point case $d=1$.

Put $H=H_0$. The action of $G$ is transitive on the slice indices,
since $(z_i)\mapsto\sum_i z_i$ maps onto ℤ. Thus $q|_H$ is onto
$F_A$: a lift in $H_n$ can be shifted into $H$ using a deck element
of total exponent $-n$. Two points of $H$ have the same image if and
only if they differ by an element of

$$
K=\ker\left(G\xrightarrow{\sum}\mathbb Z\right).
\tag{8}
$$

We also check the quotient topology. Choose an evenly covered
neighborhood $W\subset B$ with one lift $V\subset U$ meeting $H$,
small enough that $s(V)\subset(c-1/2,c+1/2)$. It can be obtained by
shrinking a lift chart and taking its image. Equation (7) implies

$$
q^{-1}(F_A\cap W)\cap V=H\cap V.
$$

In the other sheets $zV$, the corresponding inverse image is
$z(H\cap V)\subsetH_{\sum_i z_i}$. Exactly those with $z\in K$ meet
$H$. Hence $F_A\cap W$ is evenly covered by $q|_H$, with sheets
$z(H\cap V)$, $z\in K$. In particular,

$$
F_A\cong H/K
\tag{9}
$$

as topological spaces, and $H\toF_A$ is a covering map.

The restricted $K$-action remains free. Proper discontinuity also
follows directly from (6): all block sums are bounded on a compact
subset of $H$, so only finitely many integer exponent vectors can
translate it to meet itself. Thus there is no extra isotropy from
forgetting the order, even for evenly spaced configurations.

Since $H$ is nonempty and convex, it is connected and simply connected.
It follows that $F_A$ is connected, that $H$ is its universal cover,
and that its fundamental group is $K$. Finally, $K$ has the basis
$e_1-e_k,\ldots,e_{k-1}-e_k$ when $k\ge2$, and is trivial when $k=1$.
This proves the formula.

## Connected components and an additional check

The numbers of support points in each component of $E(\mathbb R)$ are
locally constant on the full reduced real divisor space. Consequently
every connected subset has fixed counts. Conversely, the proof just
given shows that every nonempty fixed-count fiber is connected. Thus
the fibers indexed by admissible distributions are precisely the
connected components, and $F_A$ is the one containing $A$.

There is also an explicit deformation retraction that independently
checks the resulting homotopy type. In a block of size $m$, let
$\mu=m^{-1}\sum_jx_j$ and set

$$
r_m(x)_j=\mu+\frac{j-(m+1)/2}{m},\qquad 1\le j\le m.
$$

This equally spaced tuple belongs to $U_m$ and has the same coordinate
sum as $x$. The straight-line homotopy from $x$ to $r_m(x)$ stays
inside $U_m$. Formula (5) shows that $r_m(T_mx)=T_mr_m(x)$, so the
homotopy is deck-equivariant. Applying it in every block preserves
$H$ and descends to a strong deformation retraction of $F_A$.

The retracted locus is described by the block sums $a_i=m_i\mu_i$ with
$\sum_i a_i=c$. The group $K$ acts on these sums by
$(a_i)\mapsto(a_i+z_i)$. Its quotient is a $(k-1)$-torus. Thus
$F_A\simeq(S^1)^{k-1}$, consistently with the universal-cover
calculation. In particular, $F_A$ is contractible when $k=1$.

## Citation

[S1] Oleg Viro, *Round dances of points on a curve*, in *Tropical Geometry:
new directions*, Oberwolfach Report 21/2019, pp. 1288–1289.
[Publisher PDF](https://ems.press/content/serial-article-files/46800),
PDF pages 44–45; mathematical definition and cubic result on printed
p. 1289, PDF page 45. The [publisher record](https://ems.press/journals/owr/articles/16933)
lists the volume as Oberwolfach Reports 16 (2019), no. 2, pp. 1245–1308,
DOI 10.4171/OWR/2019/21, and the publication date as 4 June 2020.
