# K3P global analytic infrastructure: theorem-to-evidence map

## Claim boundary

This package independently certifies the K3P-specific analytic infrastructure:
the complete three-sector bridge fibre, physical local product charts,
selected marginal submersions, the common relative rank-14 ordinary-triangle
germ, contextual contraction, simultaneous principal-domain/continuous-time
bridge gluing, and the genericity/reconstruction deduction.

The separately locked K2P package is used only to identify the finite graph
restrictions selected by the atlas, restoration, and probes.  None of its
two-sector polynomial identities, ranks, or physical-domain arguments is used
as K3P evidence.

The earlier version of this package was deliberately fail-closed on a proposed
universal pointwise cut-rank interface.  That interface is now superseded and
is not used.  The active package instead binds the independently sealed
strong-class containment theorem: under source-relative regular
full-dimensional containment, the source and target cut sets agree.  Generic
bridge-tree reconstruction uses only pointwise vanishing at true cuts and
generic nonvanishing at noncuts via the strict isotropic JC slice.  No claim is
made that every arbitrary multi-active strict K3P noncut has rank greater than
four at every parameter point.

## Corrected strong-class containment cut transfer

The load-bearing theorem is directional and class-specific.  Generic cut
recovery first gives

\[
\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)
\]

for a source-relative containment `N preceq N'`.  If a source bridge were
lost, the colored target bridge-tree dichotomy has two cases.  A two-active
case supplies a target bridge crossing the lost source split; the displayed
inclusion would make it a source bridge, contradicting compatibility of
source bridge splits.  The remaining one-active case is one of the complete
204 wrong-split directions, each of which has an exact pointwise rank-greater-
than-four certificate throughout strict `D3+`.  Hence the reverse inclusion
holds without assuming a common bridge tree, target regularity, a target-open
marginal, or the fourteen-orbit classification.

`verify_global_infrastructure.py` invokes the non-importing release verifier
in both ordinary and optimized Python and checks the theorem-manifest hash,
all load-bearing input hashes, both stored release reports, exact claim scope,
and every noncircularity flag.  The bound theorem manifest is
`../cut_recovery/strong_crossbridge/global_transfer/THEOREM_MANIFEST.json`.

## Complete three-sector bridge fibre

Cut every bridge of the recovered reduced tree of factors.  For a component
`v`, write its normalized Fourier boundary tensor as `P_v`, and for a bridge
`e=uv` write its diagonal Fourier spectrum as `k_e(h)`.  Character
conservation gives

\[
Q(\mathbf h)=\prod_vP_v(\mathbf h|_v)\prod_e k_e(h_e).
\]

For each fixed nonzero labelled character `h=C,G,T`, a bridge flattening
block is a positive rank-one matrix.  If
`xy^T=x'y'^T` with all entries positive, division by any fixed positive entry
shows that `x'=s x` and `y'=y/s` for one unique `s>0`.  The all-zero
normalization fixes the zero-sector scalar.  Applying this separately in the
three labelled nonzero sectors and peeling leaves of the component-incidence
tree gives exactly one scale `a[v,e,h]` at every component incidence:

\[
P_v(\mathbf h)\mapsto P_v(\mathbf h)
 \prod_{e\ni v}a[v,e,h_e],\qquad
k_e(h)\mapsto {k_e(h)\over a[u,e,h]a[v,e,h]}.
\]

The verifier checks cancellation separately for each endpoint scale; the
exponents are `1-1=0`.  Leaf peeling reaches every incidence and leaves a
tree, so there is no cycle on which holonomy could circulate.

The action is free.  For an unmarked component of degree `d>=3`, use pair
anchors

\[
(1,2),(1,3),(2,3),(1,4),\ldots,(1,d).
\]

The leading determinant is `-2`, and every later row introduces one new
column.  Thus the exponent matrix has rank `d` for every `d>=3`.  The positive
inverse is

\[
a_1=\sqrt{r_{12}r_{13}/r_{23}},\quad
a_2=\sqrt{r_{12}r_{23}/r_{13}},\quad
a_3=\sqrt{r_{13}r_{23}/r_{12}},\quad
a_k=r_{1k}/a_1.
\]

The certificate replays degrees 3 through 12 and records the uniform
induction for arbitrary degree.  Three block-diagonal copies have rank
`3d`; no relation such as `C=T` appears.  A distinct-spectrum labelled probe
has coordinates `(q_CC,q_GG,q_TT)=(1/4,1/9,1/16)`, so every nonidentity
permutation of `C,G,T` changes the observed coordinate vector and is not a
fixed-label gauge.

Evidence: `../bridge_fibre/K3P_BRIDGE_FIBRE_CERTIFICATE.json`, independently
recomputed by `verify_global_infrastructure.py`.

## Physical local product

For `y=(c,g,t)` in the principal domain, put

\[
B_+=\max\{c,g,t,g+t-c,c+t-g,c+g-t\}<1.
\]

For strict continuous time put

\[
B_{\rm CT}=\max\{c,g,t,gt/c,ct/g,cg/t\}<1.
\]

Choose `R=(1+B)/2` and two isotropic endpoint factors with common coordinate
`sqrt(R)`.  The three-factor split

\[
y=A_u\odot {y\over A_u\odot A_v}\odot A_v
\]

has strict endpoint and residual triples.  Every displayed inequality follows
directly from `R>B`.  In continuous time, for example,
`c/R>gt/R^2` is equivalent to `R>gt/c`.  Strictness is open, so all six
endpoint sector coordinates vary independently near this base while the
residual compensates.  A finite intersection supplies simultaneous charts
on all bridges.

The CT inequalities imply the principal inequalities: set
`u=sqrt(gt/c)`, `v=sqrt(ct/g)`, and `w=sqrt(cg/t)`.  Then `u,v,w` lie in
`(0,1)`, `(c,g,t)=(vw,uw,uv)`, and

\[
1+c-g-t=1+vw-u(w+v)>(1-v)(1-w)>0,
\]

with the other two cases cyclic.

## Every selected marginal is a K3P submersion

For every switching and every retained zero-sum character assignment, an
edge has the sector given by the XOR of the characters below its descendant
mask.  Since the total XOR is zero,
`xor(S^c)=xor(S)`, so split complements are normalized correctly.  A complete
signature records this sector for every switching and retained assignment.
The all-zero signature is invisible.  Edges with one identical complete
signature contribute only through

\[
((c_i,g_i,t_i))_{i=1}^m\longmapsto
(\prod_i c_i,\prod_i g_i,\prod_i t_i).
\]

The Jacobian has three disjoint positive rows.  Selecting derivatives with
respect to `(c_1,g_1,t_1)` gives a diagonal nonzero `3x3` minor, hence
parameter rank and image-tangent rank three.

Physical surjectivity holds for every positive integer `m`.  Choose an
aggregate isotropic prefix `R` strictly between the appropriate bound `B`
and one, take each of the first `m-1` factors equal to
`R^(1/(m-1))`, and take the residual equal to the desired selected triple
divided by `R`.  This gives a physical analytic section; strictness remains
under small target variation.  Inheritance parameters are either retained
with derivative `+1`, complemented by `lambda -> 1-lambda` with derivative
`-1`, or disappear because all switching weights sum to one.

The certificate binds the K3P four-port descriptor report and the topology
fields of the locked restoration/probe selections.  It covers rigid supports,
restoration prefixes, support-plus-one, and support-plus-two restrictions,
including both incoming modes, split complements, invisible classes, and all
inheritance transports.  The proof is uniform rather than a list of sampled
edge products.

Evidence: `../marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json`.

## The common ordinary-triangle germ is relative rank 14

The verifier independently rebuilds the three oriented maps

\[
q_{xyz}=a_xb_yc_z\bigl[\lambda f_y d_z
 +(1-\lambda)f_xe_z\bigr]
\]

with the three labelled port orders.  It expands the eight-term quartic
pullback exactly and obtains zero for every orientation.  At the strict
isotropic common preimage, it recomputes exact rank-14 minors for all three
maps.  The common tensor satisfies the quartic, and the normalized gradient
is nonzero.

The normalized quartic is irreducible over `Q`.  Regard it as a polynomial
linear in `q0CC`.  Its coefficient is the primitive disjoint-support binomial

\[
-q_{CGT}q_{G0G}q_{TT0}+q_{CTG}q_{GG0}q_{T0T},
\]

whose exponent difference is primitive, hence it is irreducible.  At the
stored specialization the coefficient is zero and the remainder is `-1`, so
the coefficient does not divide the remainder.  Gauss's lemma proves the
linear polynomial irreducible.

The normalized ambient tensor chart has dimension 15; the smooth hypersurface
`H14` has dimension 14.  Each triangle differential has rank 14 and is
contained in the 14-dimensional tangent kernel of the quartic, so each map
submerses onto a relative neighborhood in `H14`.  Intersect the three
neighborhoods.  The constant-rank theorem gives physical analytic sections
over this one common relative germ in both strict domains.

For an unchanged context, all orientations enter the same labelled
multilinear contraction

\[
\Psi(u,c)(g)=\sum_{\mathbf h}C(g;\mathbf h,c)u(\mathbf h).
\]

This does not assume the context separates the three terminals.  A maximal
minor of this one common map is chosen once.  The physical sections give
contextual rank at least its generic rank, and direct factorization of every
oriented map through the same `Psi` gives the reverse inequality.  Thus the
common contextual germ is full-dimensional relative to each complete
network image.  Its triangle contribution has rank 14, never ambient rank
15.

Evidence: `../triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json`.

## Simultaneous principal-domain and CT bridge gluing

On finitely many compactly contained local germs, every product of the two
endpoint incidence scales has bounds `0<L<=A_h<=U`.  Use the same effective
isotropic spectrum on every network and bridge,

\[
z_C=z_G=z_T=\varepsilon={L^2\over4U},\qquad
x_h={\varepsilon\over A_h}.
\]

Then

\[
{L^2\over4U^2}\le x_h\le {L\over4U}\le {1\over4}.
\]

Every principal composition margin is at least
`1-L/(2U)>=1/2`.  Every CT margin is at least

\[
{L^2\over4U^2}-{L^2\over16U^2}
={3L^2\over16U^2}>0.
\]

The same epsilon therefore works simultaneously for the finite collection.
Incidence factors cancel, and the bridge tree has no holonomy.  The local
product extraction proves that the contracted common germ has the expected
full relative dimension.

## Genericity and exact reconstruction

For fixed leaf count `n`, tree-child paths give `r<=n-1`; degree counting
gives `t=n+r-2` and at most `4n-3` rooted vertices.  Thus only finitely many
labelled topologies occur.  Each complex model closure is irreducible as the
closure of a polynomial image of affine parameter space, and generic
Jacobian rank equals image dimension.

If an inequivalent physical intersection had full source dimension, finite
semialgebraic constant-rank stratification would provide a target analytic
section over a source-relative open regular germ, contradicting the completed
containment classification.  Hence each inequivalent intersection has
dimension at most `d_N-1`.  The finite union of their Zariski closures,
together with singular, source-rank-drop, and certified reconstruction-test
zero loci, is a proper exceptional set `E_N`.

Outside `E_N`, the stored algorithm terminates: exact Fourier transform,
generic cut and bridge-tree recovery, three-sector incidence normalization, finite local
atlas tests, fixed-full restoration, coherent one-/two-port recovery,
triangle-class assembly, and exact semialgebraic feasibility by real-closed-
field quantifier elimination.  This is an exact-oracle termination theorem,
not a practical finite-sequence or numerical-stability claim, and it does not
identify individual edge parameters inside the bridge fibre.

Evidence: `K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json` and the
machine-checked dependency DAG therein.

## Replay and mutations

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python global_infrastructure/generate_global_infrastructure.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python global_infrastructure/verify_global_infrastructure.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python global_infrastructure/test_global_infrastructure_mutations.py
```

The mutation suite rebinds hashes after each mutation so rejection cannot be
attributed merely to stale manifests.  In addition to the algebraic controls,
it rejects restoration of the obsolete pointwise interface, substitution of
the universal pointwise claim, use of a common bridge tree, a corrupted theorem
hash, promotion of generic noncut recovery to a universal pointwise theorem,
and restoration of the old dependency-DAG node.  The optimized verifier bypass
is also rejected.
