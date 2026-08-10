# Correct projective bridges and one-sided cut preservation

Date: 2026-08-09  
Scope: the locked standard semi-directed convention and the open JC domain  
Implementation independence: no historical graph, switching, Fourier,
canonicalization, separator, sign, or rank module is imported

Throughout, `S_TC` includes the existence requirement in the definitions
lock: a standard topology has at least one admissible rooting, and every such
rooting is tree-child.  The finite compiler first constructs and validates a
rooted presentation, so no result uses vacuous all-rootings membership.

## 1. Result

**PROVED.** On the reduced, leaf-supported bridge tree of a binary standard
semi-directed strongly tree-child level-2 network, the complete fiber of the
positive JC tensor contraction is the full incidence-scaling action

\[
 P_v\longmapsto P_v\prod_{e\ni v}a_{v,e}^{[h_e\ne0]},
 \qquad
 x_{uv}\longmapsto\frac{x_{uv}}{a_{u,uv}a_{v,uv}}.
\]

The positive regular locus has explicit local analytic slices.  Its intrinsic
coordinates are projective local tensor factors and normalized effective
bridge scales; they are not the original physical bridge multipliers.  The
old reciprocal-only bridge chart is false.

**PROVED.** If two global model germs have the same labelled bridge tree,
source-relative containment localizes to source-relative containment of every
corresponding projective local factor.  No continuous target-parameter
selection is needed, and no change in a distant blob can compensate for a
projectively nonzero local separator.

**PROVED.** For every open JC parameter point of a network in the locked
standard-strong level-2 class, a bipartition is a cut split if and only if its
group-based Fourier flattening has rank at most four.  Consequently

\[
 N\preceq_{\rm JC}N'
 \quad\Longrightarrow\quad
 \operatorname{Cut}(N)\subseteq\operatorname{Cut}(N').
\]

This includes the previously omitted crossing in which the central bridge
joins two active three-port endpoint tensors.

The last conclusion is a pointwise open-domain statement, stronger than the
source-open statement needed for one-sided containment.  It does not by itself
prove equality of bridge trees or the final local topology atlas.

## 2. Universal bridge factorization

Let \(G=\mathbb Z_2\times\mathbb Z_2\), written additively with every element
self-inverse.  Let \(\mathcal T=(V,E)\) be a tree of bridge components.  At
component \(v\), let \(X_v\) be its retained physical character blocks and
let \(E(v)\) be its bridge incidences.  The local conservation domain is

\[
 D_v=\left\{(g,h):
 \bigoplus_{i\in X_v}g_i\oplus
 \bigoplus_{e\in E(v)}h_e=0\right\}.
\]

A local tensor \(P_v:D_v\to\mathbb R_{>0}\) is normalized by \(P_v(0)=1\)
and invariant under the simultaneous action of
\(\operatorname{Aut}(G)\cong S_3\).  Each bridge \(e\) has a positive scalar
\(x_e\).  For a globally zero-sum physical assignment, let \(h_e\) be the
sum on either side of \(e\).  The observed tensor is

\[
 \Gamma(P,x)(g)=
 \prod_{v\in V}P_v(g|_{X_v},(h_e)_{e\ni v})
 \prod_{e\in E}x_e^{[h_e\ne0]}.
 \tag{2.1}
\]

We assume **leaf support**: both sides of every bridge contain a retained
physical block.  LSA trimming and labelled support of every terminal bridge
component give this in the target network class.

### Theorem 2.1 (exact positive fiber)

**PROVED.** Two positive normalized collections \((P,x)\) and \((Q,y)\)
satisfy \(\Gamma(P,x)=\Gamma(Q,y)\) if and only if positive numbers
\(a_{v,e}\), one per bridge incidence, satisfy

\[
 Q_v(g,h)=P_v(g,h)
 \prod_{e\ni v}a_{v,e}^{[h_e\ne0]},
 \qquad
 y_{uv}=\frac{x_{uv}}{a_{u,uv}a_{v,uv}}.
 \tag{2.2}
\]

#### Proof

The reverse implication is immediate from (2.1).  For the converse, root
\(\mathcal T\).  For an edge \(e=pv\), contract the component subtree below
\(v\), excluding the multiplier \(x_e\), to obtain a boundary vector
\(L_e^P(g,h)\); define \(L_e^Q\) similarly.  Contract the complement to
\(R_e^P,R_e^Q\).  In every separator sector \(h\), equality of the observed
tensor gives equality of two positive rank-one matrices:

\[
 L_e^P x_e^{[h\ne0]}(R_e^P)^T
 =L_e^Q y_e^{[h\ne0]}(R_e^Q)^T.
\]

Leaf support supplies at least one row and one column in every sector.
Positive rank-one uniqueness therefore gives

\[
 L_e^Q(g,h)=c_e(h)L_e^P(g,h).
 \tag{2.3}
\]

The all-zero entry is normalized, so \(c_e(0)=1\).  Applying the six group
automorphisms to (2.3) shows that the same positive number \(c_e\) occurs for
all three nonzero characters.  This step uses complementary assignments of
total \(h\) on the two sides; it never violates zero-sum conservation by
setting the complementary side to zero.

If \(f=vw\) ranges over the child edges of \(v\), expand the subtree
contraction in (2.3).  One obtains

\[
 \frac{Q_v}{P_v}
 =c_e(h_e)
 \prod_{f=vw}
 \left(c_f(h_f)^{-1}
       \left(\frac{x_f}{y_f}\right)^{[h_f\ne0]}
 \right).
 \tag{2.4}
\]

At the root the parent factor is absent and the whole-tree ratio is one.
Set \(a_{v,e}=c_e\) at a child endpoint and
\(a_{v,f}=c_f^{-1}x_f/y_f\) at a parent endpoint.  Equation (2.4) is the
first part of (2.2), while on every edge \(f=vw\),

\[
 a_{v,f}a_{w,f}=x_f/y_f.
\]

This proves the exact fiber statement. ∎

### Local stabilizers

**PROVED.** For a component with \(m\) physical blocks and \(d\) bridge
incidences, the stabilizer of the local incidence action is:

- trivial if \(m\ge1\);
- trivial if \(m=0,d\ge3\);
- \(\{(t,t^{-1}):t>0\}\) if \(m=0,d=2\);
- all of \(\mathbb R_{>0}\) if \(m=0,d=1\).

If \(m\ge1\), put one nonzero character \(s\) on a physical block and on
one chosen incidence; the stabilizer equation forces that incidence scale to
one.  If \(m=0\), put \(s\) on any two incidences.  The equations
\(a_i a_j=1\) give the four cases above.

**PROVED.** A retained unmarked bivalent component cannot occur in the locked
standard-strong class.  An ordinary unlabelled singleton component has bridge
degree three.  A cycle blob has at least three ports.  A simple theta blob
with path lengths \((\ell_1,\ell_2,\ell_3)\) has
\(\ell_1+\ell_2+\ell_3-3\) ports.  The only simple two-port theta is
\((1,2,2)\), namely \(K_4-e\).  If its two reticulations are adjacent, one
has a reticulation child.  If they are the nonadjacent degree-two vertices,
their external bridges cannot enter them in an LSA-valid acyclic rooting, so
both pole vertices have two reticulation children.  Hence it has no
tree-child rooting.  Parallel theta cores are excluded by the locked simple
standard reduction.

Thus every unmarked component has degree at least three, while every leaf of
the bridge tree contains a taxon.

### Analytic slices and intrinsic scales

Fix a nonzero \(s\in G\).  If \(X_v\ne\varnothing\), choose a physical block
\(i(v)\) and use the anchors

\[
 R_e(P_v)=P_v(g_{i(v)}=s,h_e=s;\text{ all other characters }0).
 \tag{2.5}
\]

They transform as \(R_e\mapsto a_{v,e}R_e\).  If \(X_v=\varnothing\) and
\(d\ge3\), use pair anchors

\[
 R_{ef}(P_v)=P_v(h_e=h_f=s;\text{ all other }h=0).
 \tag{2.6}
\]

The \(d\) pairs
\((1,2),(1,3),(2,3),(1,4),\ldots,(1,d)\) have full log-exponent rank.  For
desired pair corrections \(r_{ij}\), the unique positive normalizer is

\[
 a_1=\sqrt{r_{12}r_{13}/r_{23}},\quad
 a_2=\sqrt{r_{12}r_{23}/r_{13}},\quad
 a_3=\sqrt{r_{13}r_{23}/r_{12}},\quad
 a_k=r_{1k}/a_1.
 \tag{2.7}
\]

**PROVED.** Equations (2.5)--(2.7) define real-analytic slices on the positive
regular locus.  After formally adjoining one independently variable arm
scale at every incidence, the contraction germ is analytically isomorphic to

\[
 \prod_v \mathcal S_v\times\prod_{e\in E}J_e,
 \tag{2.8}
\]

where \(\mathcal S_v\) is the sliced local tensor germ and \(J_e\) is one
positive **effective** edge scale.  If \(c_{v,e}(P_v)\) denotes the unique
normalizer to the slice, then

\[
 j_e=\frac{x_e}{c_{u,e}(P_u)c_{v,e}(P_v)}
 \tag{2.9}
\]

is invariant under the complete incidence action.  Conversely the sliced
factors and the \(j_e\)'s determine the observed tensor by Theorem 2.1.
Rank-one cut blocks with valid complementary nonzero-sector anchors recover
them recursively.  All operations are multiplication, division by positive
entries, and positive square roots.  Hence both contraction and extraction
are analytic.  The bridge graph is a tree, so there is no cyclic scaling
holonomy.

No \(j_e\) is asserted to equal a physical edge multiplier.  Indeed

\[
 (y,z,x)=(1/2,1/2,1/2),\qquad
 (y,z,x)=(3/5,3/5,25/72)
\]

have the same observable product \(1/8\) and are not related by the withdrawn
reciprocal-only endpoint action.

### Directed localization and no compensation

**PROVED.** Suppose the source and target have the same labelled bridge tree
and a source-relative global model germ is contained in the target image.
Apply the intrinsic analytic extraction map furnished by (2.8) to the common
distributions.  Projection to any focal slice maps a relative-open source
product germ onto a relative-open source local projective germ.  Every image
point is simultaneously the projective factor extracted from a target
factorization.  Thus the focal source projective germ is contained in the
corresponding target projective model (or in one member of a finite union of
target incoming-role completions).  A finite semialgebraic union containing a
source-full-dimensional set has a source-full-dimensional member.

This argument selects no target parameters continuously.  Since projective
extraction is a function of the distribution, changes in other blobs cannot
alter the focal projective orbit.  Therefore cross-blob compensation is
impossible after the bridge trees agree.

There is also a direct marginal proof.  Choose one taxon in every branch
incident to a focal component and marginalize all other taxa.  Each outside
branch becomes one positive JC multiplier

\[
 \kappa_i=\sum_\sigma w_\sigma
 \prod_{a\in\operatorname{path}_\sigma}x_a\in(0,1],
\]

and the adjacent bridge gives an effective arm \(z_i=x_{e_i}\kappa_i\in(0,1)\).
The Jacobian of \((x_{e_i})\mapsto(z_i)\) is
\(\operatorname{diag}(\kappa_i)\), so the source local-plus-arm marginal is a
submersion on its dense regular locus.  This independently rules out distant
compensation for every arm-multihomogeneous zero/sign separator.

## 3. Pointwise cut characterization

For a bipartition \(A\mid B\), arrange the Fourier flattening in four blocks
indexed by the total character \(h\in G\) on side \(A\).  Every block has
positive entries.

### True cuts

**PROVED.** If \(A\mid B\) is a cut split, the \(h\)-block is an outer product
of the two side tensors, multiplied by the bridge scalar when \(h\ne0\).
Every block has rank one, hence the complete flattening has rank at most four.

### Primitive local universe

**PROVED.** Suppressing unported degree-two vertices in a nontrivial subcubic
level-2 blob gives a cycle kernel at cycle rank one and a theta kernel at
cycle rank two.  A bridge-free subcubic graph of cycle rank two is a theta:
after suppressing degree-two vertices, the degree sum and
\(|E|-|V|+1=2\) force exactly two cubic poles joined by three internally
disjoint paths.

The directed cycle kernel has one source and one reticulation sink joined by
two directed paths.  For a theta, classify by the number of reticulation
poles.  Two reticulation poles are incompatible with an acyclic reachable
orientation.  With one reticulation pole, the unique source event and the
second reticulation sink occur on the same remaining path or on different
paths.  With no reticulation pole, the unique source and the two reticulation
sinks have one source--sink pair on a common path or all three on distinct
paths.  These are exactly the four theta kernels encoded in
`verify_cut.py`.

**EXACTLY COMPUTED.** An independent orientation enumeration on three
length-three theta paths gives four canonical classes from 102 raw valid
orientations, with multiplicities \(6,24,24,48\).  A four-cycle gives one
class from 12 raw orientations.  Length three is exhaustive because source
and sink events alternate on a path, there is only one source event, and
there are only two reticulation events; no valid path can contain more than
two events.

Every bounded marginal completion is obtained by:

1. distributing the selected ports in directed order along primitive arcs;
2. choosing which reticulation-sink ports remain selected;
3. selecting root, selected-incoming, or marginalized-incoming role; and
4. putting at most one marginalized repair port on each otherwise empty arc.

Additional marginalized ports on an occupied arc duplicate a descendant-mask
row and contribute only through a serial product.  The map
\((0,1)^k\to(0,1)\), \((x_1,\ldots,x_k)\mapsto\prod_i x_i\), is onto and has
nonzero differential.  Thus this construction is exhaustive for the local
tensors used below.

The standard-strong test in the compiler is not merely a test of its chosen
rooting.  In a standard mixed graph, failure of tree-childness in some
admissible rooting is equivalent to either a reticulation tail or an ordinary
vertex tailing two reticulation edges.  Both are visible before rooting.  If
neither occurs, a tail of one reticulation edge has two undirected incidences,
one parent and one ordinary child in every admissible rooting; all other
internal vertices plainly have an ordinary child.  This proves the local
criterion used by the enumeration.

### Three-port endpoint inequality

For a positive JC-symmetric three-port tensor in the port order
\((1,2;3\text{ central})\), put

\[
 a=P(1,1,0),\quad b=P(1,0,1),\quad c=P(0,1,1),
 \quad t=P(1,2,3),
\]

and \(F=abc-t^2\), \(G=a-bc\).

**EXACTLY COMPUTED.** The primitive compiler generated 76 nontrivial
canonical central-role endpoint tensors.  In 67 cases an exact
factor/Bernstein or inheritance-Bernstein certificate proves \(F>0\)
throughout the complete open cube.  In the remaining nine, \(F=0\)
identically and an exact certificate proves \(G>0\) throughout the complete
open cube.  The compiler also records the ordinary trivalent median
component, whose sliced local tensor is exactly constant and therefore has
\(F=G=0\).  Every nonconstant polynomial was regenerated
from

\[
 \text{rooted graph}\to\text{switchings}\to\text{descendant masks}
 \to\text{JC Fourier coordinates};
\]

the stored graph-to-mask transport is checked before the polynomial is used.

An arbitrary three-terminal endpoint has a unique median bridge-tree
component.  Everything else lies on one of three terminal arms and collapses
to positive scalars \(u,v\in(0,1)\) and \(w\in(0,1]\); the central arm may
have length zero.  Arm scaling sends

\[
 (a,b,c,t)\mapsto(uv,a,uw,b,vw,c,uvw,t).
\]

Hence \(F\mapsto(uvw)^2F\).  If \(F=0,G>0\), then

\[
 G\mapsto uv(a-w^2bc)\ge uv(a-bc)>0.
\]

For the ordinary component \(a=b=c=t=1\) before arm scaling, so the same
formula gives \(F=0\) and \(G=uv(1-w^2)\ge0\), with equality allowed only
when its central arm has length zero.  Thus every arbitrary endpoint satisfies

\[
 F>0\quad\hbox{or}\quad F=0\text{ and }a\ge bc.
 \tag{3.1}
\]

The weak inequality in (3.1) is intentional and is enough because the bridge
joining two active endpoints has its own multiplier strictly below one.

### One active component

**EXACTLY COMPUTED.** Up to leaf relabelling and reticulation-choice
transport, the graph compiler generated 72 four-port tensors, including the
ordinary tree tensor.  Across their three balanced splits, 12 splits were
displayed by every switching.  For each of the remaining 204 directions, the
compiler regenerated a nonzero \(2\times2\) block minor and an exact strict
open-cube sign certificate.  Thus every split not displayed by all switchings
has flattening rank greater than four at every open parameter point.

Independent positive arm scales act by invertible row and column diagonal
matrices on each Fourier block.  They multiply a chosen minor by a positive
monomial, so the conclusion survives arbitrary outside branches.

**EXACTLY COMPUTED.** A separate two-colour switching compiler checked all ten
root/nonroot primitive families after run compression and found no balanced
noncut colouring displayed by every switching.  The compression is complete
for the following reason.  A colour word with two transitions on one directed
segment already prevents the split from being displayed by any switching:
the internal chain remains linearly ordered, and no tree edge can separate two
interlaced colour classes.  Thus a putative common split has at most one
transition on every segment.  Retain at most one occurrence of each colour in
that order.  If this leaves one colour globally singleton although the
original side had at least two taxa, retain a second adjacent occurrence at
the same segment.  These are exactly the words enumerated by the compiler.  If
the full split were displayed by every switching, its balanced restriction
would remain displayed by every restricted switching.  The zero survivor
count therefore lifts to arbitrary subdivisions.

If one switching fails to display the compressed split, the ordinary tree
quartet criterion supplies two taxa of each colour whose induced quartet also
fails to display it.  Marginalized ports are precisely the repair ports
enumerated by the four-port compiler.  This binds the switching census to the
204 strict minors.

### Two active endpoints

Let two three-port endpoint tensors be joined at their third ports by a bridge
of multiplier \(z\in(0,1)\).  Use lower coordinates \(a,b,c,t\) and upper
coordinates \(A,B,C,T\).  Test the crossing split.  If its Fourier flattening
had rank at most four, positivity would force every one of its four blocks to
have rank one.  Four explicitly regenerated minors are

\[
\begin{aligned}
 f_1&=aA-z^2bcBC,\\
 f_2&=zTt-z^2bcBC,\\
 f_3&=zC(At-zTbc),\\
 f_4&=zc(zBCt-Ta).
\end{aligned}
\]

**EXACTLY COMPUTED.** Direct construction of all four \(4\times4\) Fourier
blocks yields 20 nonzero minors up to sign and contains all four \(f_i\).
The following polynomial identities have zero remainder:

\[
\begin{aligned}
 aA-zTt &= f_1-f_2,\\
 z^2CT(abc-t^2)&=zCt(f_1-f_2)-af_3,\\
 z^2ct(ABC-T^2)&=Af_4+zcT(f_1-f_2).
\end{aligned}
\]

Rank one would therefore force \(abc=t^2\) and \(ABC=T^2\).  The endpoint
dichotomy (3.1) then gives \(a\ge bc\) and \(A\ge BC\).  Since every
coordinate is positive and \(0<z<1\),

\[
 aA\ge bcBC>z^2bcBC.
\]

But \(f_1=0\) would give

\[
 aA=z^2bcBC<bcBC,
\]

contradicting the preceding strict inequality.  This is the required two-active-endpoint
crossing argument; it uses no boundary specialization.

### From local crossings to every noncut split

**PROVED.** Colour taxa by the two sides of a balanced candidate split.  If
some bridge has both colours on both sides, choose one taxon of each colour on
each side.  The quartet is the two-active crossing above.

Otherwise there is a unique central bridge-tree component such that every
incident branch is monochromatic.  If either colour occurred at only one
incident branch, that bridge would display the candidate split.  A noncut
split therefore has at least two incident branches of each colour.  The
switching-compression argument and quartet restriction give a four-port
one-active witness.  Its strict minor proves rank greater than four.

Singleton bipartitions are pendant-edge cut splits.  Thus every noncut split
has rank greater than four at every open model point, while every cut split has
rank at most four.

### One-sided consequence

**PROVED.** Let \(N\preceq_{\rm JC}N'\), and let \(A\mid B\) be a cut split
of \(N\).  Every distribution in the source germ has flattening rank at most
four.  If \(A\mid B\) were not a cut split of \(N'\), every open target point
would have rank greater than four by the pointwise theorem.  The two images
would have no common open point at all, a contradiction.  Hence every source
cut is a target cut.

## 4. Exact implementation

`verify_bridge.py` uses only the Python standard library.  It checks exact
rational stabilizer and anchor ranks, 793 independently generated
leaf-supported bridge trees through five vertices, the inaccessible-side
failure, the retained-bivalent stabilizer, the marginal-arm Jacobian, and the
withdrawn reciprocal-chart regression.

`verify_cut.py` uses the Python standard library and SymPy only.  It derives
the primitive orientation classes, constructs every bounded completion,
checks rooted and narrow standard-strong membership, enumerates switchings,
derives all edge descendant masks, regenerates exact Fourier polynomials,
proves signs by rational Bernstein coefficients, verifies graph transports,
and emits the full certificate.

Finite computations are labelled **EXACTLY COMPUTED**.  The general bridge
fiber, arbitrary-subdivision lift, pointwise cut theorem, and one-sided
consequence are mathematical deductions and are labelled **PROVED**.

## 5. Remaining scope

**UNRESOLVED HERE.** This work does not classify the projective local model
germs up to ordinary triangle redirection.  It does not prove the bounded
local topology atlas, probe coherence, root reduction, or converse gluing.
Those are separate nodes in the landmark program.  The present result closes
only the bridge/no-compensation and one-sided cut-preservation nodes.
