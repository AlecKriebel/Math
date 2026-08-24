# Exact two-sector bridges, paired marginal openness, and physical gluing

## 1. Setting

Write the K2P Fourier edge vector as `(1,s,g,s)`, with paired sector
`S={C,T}` and singleton sector `G`.  Throughout this note every edge lies in

\[
\mathcal D_+=\{(s,g):0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

All inheritance probabilities are strictly between zero and one.  Consequently
every conservation-supported local Fourier tensor entry is positive.

Cut a standard network at its bridges.  Its component-incidence graph is a
tree `T`.  For a component `v`, let `P_v` be its normalized boundary tensor,
including its retained physical blocks and its bridge characters.  Thus
`P_v(0)=1`.  If `e=uv` is a bridge, write

\[
k_e(h)=1\ (h=0),\qquad k_e(h)=s_e\ (h\in\{C,T\}),\qquad
k_e(G)=g_e.
\]

The global Fourier tensor is

\[
Q(h)=\prod_v P_v(h|_v)\prod_{e\in E(T)}k_e(h_e).
\tag{1}
\]

The character on a bridge is the group sum on either side of its cut.

## 2. Exact positive two-sector bridge fibre

**Theorem.**  On the positive, normalized, K2P-symmetric component-tensor
locus, the complete fibre of (1) is exactly

\[
P_v\longmapsto P_v
 \prod_{e\ni v}a_{v,e}^{[h_e\in\{C,T\}]}
 b_{v,e}^{[h_e=G]},
\]

\[
s_e\longmapsto {s_e\over a_{u,e}a_{v,e}},\qquad
g_e\longmapsto {g_e\over b_{u,e}b_{v,e}},
\tag{2}
\]

where every `a` and `b` is positive.  On physical networks, the fibre is the
intersection of this orbit with all local-realizability, inheritance, arm,
bridge, and K2P inequalities.

**Proof.**  Cut one bridge and fix its character.  The corresponding
flattening block is a positive rank-one matrix.  Positive rank-one
factorization is unique up to one positive scalar, giving a cut scale `c_e(h)`.
All-zero normalization gives `c_e(0)=1`.  The observable K2P symmetry exchanges
`C` and `T`, hence `c_e(C)=c_e(T)`; it does not exchange either with `G`, so
`c_e(G)` is independent.

Temporarily root `T` and peel its leaf components.  Expanding the contraction
at each peeled vertex separately in the paired and singleton sectors assigns
one positive scale at every component incidence.  The resulting equations are
exactly (2).  Induction reaches every vertex because `T` is a tree.  Therefore
there is no further vertex-coupled gauge and no sector holonomy.  Direct
cancellation proves the converse.  The sector labels are observable, so there
is no additional discrete sector exchange.  This proves completeness.  ∎

## 3. Freeness and analytic incidence normalizers

If a component has a retained physical block, choose one such block.  For
each incidence `e`, the conservation-supported entry with the chosen sector
character on that block and on `e` transforms by exactly the incidence scale
at `e`.  These one-incidence anchors give the identity exponent matrix.

An unmarked retained component has degree `d>=3`.  For either sector, use the
pair anchors

\[
(1,2),(1,3),(2,3),(1,4),\ldots,(1,d).
\]

Their exponent matrix has leading determinant `-2`; every later row introduces
one new incidence.  Its rank is `d`, and the positive normalizer is

\[
a_1=\sqrt{r_{12}r_{13}/r_{23}},\quad
a_2=\sqrt{r_{12}r_{23}/r_{13}},\quad
a_3=\sqrt{r_{13}r_{23}/r_{12}},\quad
a_k=r_{1k}/a_1.
\tag{3}
\]

The same construction is applied independently to the paired and singleton
sectors.  Thus the two-sector exponent matrix is block diagonal of rank `2d`.
All entries used in (3) are positive, so the normalizers are real analytic.

The only possible unmarked degree-two stabilizer would be the simple two-port
theta `K4-e`; its reticulation placements violate the strong tree-child
incidence criterion.  Ordinary singleton and cycle components have degree at
least three.  Hence every retained component action is free.

The normalizers first give an **ambient positive-tensor quotient chart**:
projective local tensor germs in the chosen slice, together with two
normalized effective bridge coordinates per bridge, contract analytically
and are extracted analytically by positive rank-one factorization.  This
statement alone does not say that a chosen normalized slice representative is
a physical local-network tensor.

The chart restricts to the required physical local product germ at every
physical regular point.  To see the missing saturation explicitly, split each
physical bridge pair `(s,g)` into three serial pairs

\[
(\alpha_u,\beta_u),\qquad
\left({s\over\alpha_u\alpha_v},
      {g\over\beta_u\beta_v}\right),\qquad
(\alpha_v,\beta_v).
\]

Choose the two endpoint pairs sufficiently near `(1,1)` so that all three
pairs lie strictly in `D_plus`; this is the certified strict K2P subdivision
lemma applied twice.  Strictness is open, so, after shrinking, the four
endpoint coordinates vary independently in a neighborhood while the residual
bridge pair remains in `D_plus`.  Absorbing the endpoint factors into the two
component tensors realizes exactly the four incidence-scale variations in
(2).  Doing this independently on the bridge tree realizes an open
neighborhood of the complete incidence orbit, with no holonomy.  Intersecting
the ambient quotient chart with a constant-rank physical parameter chart now
gives the physical local product germ.  Thus the assertion is about the germ
of physical realizations at a regular point, not about physicality of an
arbitrary normalized slice tensor.

## 4. Paired `(s,g)` marginal open image

Marginalizing a newly restored leaf sets its Fourier character to zero.  Its
pendant multiplier becomes one, while subdivision replaces an effective edge
`(S,G)` by the coordinatewise product of the serial edge pairs.

For any `(S,G)` in `D_plus` and any integer `m>=2`, put

\[
M=\max\{S,G,2S-G,0\}<1.
\]

Choose `r` with `M < r^(m-1) < 1`.  Use `(r,r)` for the first `m-1`
serial edges and

\[
\left(S/r^{m-1},\ G/r^{m-1}\right)
\tag{4}
\]

for the last.  Every `(r,r)` lies in `D_plus`.  The two coordinates in (4)
are positive and below one, and

\[
G/r^{m-1}>2S/r^{m-1}-1
\iff r^{m-1}>2S-G.
\]

Thus (4) is a physical section of every serial-product map.  On a small
neighborhood of `(S,G)`, the same fixed `r` works, so this section is analytic.
The Jacobian of the product map has independent `s` and `g` rows and rank two.
Together with the identity map on all other source edge and inheritance
parameters, this proves that the restriction map from a fixed full source
model to its selected source child has physical open image.  Multiple source
subdivisions compose, and the argument is independent at every restored
source role.  No openness or inverse-lifting assertion is made for an
arbitrary target deletion map.

For the strict continuous-time cone `0<S<1, S^2<G<1`, one may instead use
the coordinate roots `(S^(1/m),G^(1/m))`; each factor again satisfies
`s^2<g`.  Hence the marginal-open-image theorem also holds there.

## 5. Simultaneous physical gluing

Suppose local projective tensors match with positive incidence products

\[
A_e=a_{u,e}a_{v,e},\qquad B_e=b_{u,e}b_{v,e}.
\]

For every bridge independently choose

\[
0<s_e<\min\{1/2,A_e/2\},\qquad
0<g_e<\min\{1,B_e\}.
\]

Then `(s_e,g_e)` is in `D_plus`, because `2s_e-1<0`.  Its transformed pair
`(s_e/A_e,g_e/B_e)` also lies in `D_plus`, for the same reason.  All
inequalities are strict, so a product neighborhood remains physical.  Since
the bridge graph is a tree, choices on different bridges are independent and
there is no holonomy.  This proves simultaneous physical gluing of every
finite collection of local directed relations.

For continuous time, additionally choose `s_e` so small that

\[
\max\{1,B_e/A_e^2\}s_e^2<\min\{1,B_e\},
\]

then choose `g_e` strictly between the two sides.  Both the original and
transformed pairs satisfy `s^2<g`; hence the continuous-time gluing statement
also follows.

## 6. Consequence for restoration

Restoration is used only under a **fixed full containment**.  Suppose fixed
full networks `N -> N'` realize such a containment and their selected
four-port restriction is a frozen restoration-parent presentation.  Choose
an actual omitted physical label of these same two networks and retain it on
both sides.  Marginalizing the fixed full relation to that five-port set and
using openness of the **source** restriction gives a source-open direct-child
containment into the actual target restriction.  Its restored role, target
attachment, source subdivision segment, port match, and parent transport are
fixed by `N,N'` and therefore occur among the finitely enumerated physical
children.  A certificate separating every such child contradicts the
assumed full containment and discharges the parent obligation.

This does not infer a restored relation from an abstract selected relation;
that inference is false in general.  It also makes no target-marginal
open-image claim and does not assert equality of complete stochastic images.
