# Global K2P closure proof

> Promotion status: this proof is assembled fail-closed.  The analytic and
> local-to-global layers pass an independent audit after the repairs written
> below.  Promotion still requires the clean corrected restoration and cycle
> packages, the all-primitive one-/two-port transport replay, and the unified
> independent release gate.  Historical rooted `tree--sunlet` classifications
> are not promotion evidence.  No conclusion below concerns the mixed-sign
> stochastic cone.

## 1. Domain and observational relations

An edge has Fourier spectrum \((1,s,g,s)\), and throughout

\[
 \mathcal D_+=\{(s,g):0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

All inheritance probabilities lie in \((0,1)\).  Write \(\Phi_N\) for the
polynomial Fourier parameterization and \(\mathcal M_+(N)\) for its strict
physical image.  On a top-dimensional regular source branch, define
\(N\preceq_+N'\) if a nonempty relatively open source germ is contained in
\(\mathcal M_+(N')\) and admits a regular physical target section.  Define
\(N\bowtie_+N'\) if the two images contain one germ which is full-dimensional
and regular in both.  Neither relation means equality of complete stochastic
images.

The edge-domain certificate proves strict subdivision and hence invariance
under every admissible rooting of the fixed semi-directed graph.  Thus these
relations are well-defined on standard semi-directed networks.

## 2. Pointwise recovery of the decorated tree of blobs

For a true cut split, every Fourier flattening character block is a positive
rank-one outer product; this is model-independent for group-based Markov
models.  More strongly, the displayed-quartet sign theorem supplies a
pointwise statement on \(\mathcal D_+\): two binary semi-directed networks
whose restrictions display different quartet sets have disjoint strict K2P
images.  The proof is by the zero-versus-positive invariants

\[
q_{CCCC}-q_{CCTT},\qquad
q_{CCCC}-q_{CCTT}-q_{CTTC}+q_{CTCT}.
\]

Positive inheritance mixtures preserve their strict signs.  Hence the
labelled tree of blobs is recovered pointwise, not merely generically.  In
particular, if \(N\preceq_+N'\), their labelled trees of blobs agree.

The only decoration not recorded by the contracted tree is an ordinary
degree-three vertex versus a three-sunlet.  For each orientation the exact
K2P polynomial

\[
\mathcal T_i=V^2X_g-X_s^2Y_gZ_g
\]

vanishes on the tree and has a strictly nonzero signed pullback on the
sunlet.  Thus the decoration also agrees.  A strong theta factor has at
least four physical boundaries; it cannot masquerade as an ordinary
three-boundary component.

## 3. Intrinsic two-sector local factors

Cut the common bridge tree.  Positive rank-one uniqueness in the paired
\(\{C,T\}\) sector and the singleton \(G\) sector gives exactly two
incidence scales at each component boundary:

\[
P_v\mapsto P_v\prod_{e\ni v}
a_{v,e}^{[h_e\in\{C,T\}]}b_{v,e}^{[h_e=G]},
\]

\[
s_e\mapsto\frac{s_e}{a_{u,e}a_{v,e}},\qquad
g_e\mapsto\frac{g_e}{b_{u,e}b_{v,e}}.
\]

All-zero normalization fixes the zero sector.  To prove equality of the
\(C\)- and \(T\)-incidence scales, write
\(\rho_e=c_e(C)/c_e(T)>0\).  On a marked component, compare the positive
conservation-supported entries having \(C,C\), respectively \(T,T\), at the
incidence and one retained physical block; K2P invariance before and after
the scale action gives \(\rho_e=1\).  On an unmarked component of degree
\(d\ge3\), the same comparison at every pair of incidences gives
\(\rho_e\rho_f=1\).  Three distinct incidences and positivity force every
\(\rho_e=1\).  The singleton \(G\) orbit remains independent.

For an unmarked component of degree two, the genuine stabilizer
\((\rho_1,\rho_2)=(t,t^{-1})\) remains.  It is absent from the retained strong
class: every primitive finite anchor is marked, every unmarked ordinary
component has degree at least three, and the only simple reduced
two-boundary theta, the path-length \((1,2,2)\) `K4-e`, has no tree-child
rooting.  Peeling the bridge tree now proves completeness and excludes
holonomy.  An unmarked component of degree \(d\ge3\) has the pair-anchor
exponent matrix

\[
(12),(13),(23),(14),\ldots,(1d),
\]

of rank \(d\) and leading determinant \(-2\), separately in each sector.
Hence every retained action is free and has an analytic local slice.

The contraction/extraction maps first give an ambient positive-tensor
quotient chart.  Physical saturation is a separate step.  For an effective
bridge \((s,g)\), choose \(r<1\), sufficiently close to one, so that

\[
 (r,r),\qquad (s/r^2,g/r^2),\qquad (r,r)
\]

all lie strictly in \(\mathcal D_+\).  Strictness supplies a neighborhood in
which the two endpoint pairs vary in four independent coordinates while the
residual pair remains physical.  These endpoint ratios realize precisely the
two incidence scales at each end, and suppression of the two serial
degree-two vertices returns the same standard bridge.  The strict K2P
subdivision lemma makes this construction uniform after shrinking.
Because the bridge graph is a tree these choices have no holonomy.  The
ambient quotient chart therefore restricts, on a constant-rank physical
parameter chart, to the claimed physical local product germ.  No claim is
made that an arbitrary normalized slice tensor is itself physical.

## 4. Localization and the bounded local theorem

Vary one source component in the local product chart while holding the
others and the effective bridge coordinates fixed.  The target section and
intrinsic bridge extraction then give a source-relative projective
containment into the corresponding target component.  Root movement turns a
structural incoming boundary into an actual selected incoming port whenever
needed.

The root movement assertion includes the retained-arrowhead case.  Choose an
ordinary root-to-leaf path in a tree-child rooted partner, suppress the old
root, reverse only the ordinary edges on that path, and insert the new root
on the terminal pendant edge.  Symmetry of K2P transition matrices handles
ordinary reversals and strict subdivision handles the new root edge.  If the
old root subdivides an edge entering a reticulation, inspect each switching:
when that parent is selected the two old root arms enter only through their
serial products; when the other parent is selected the remaining one-child
root stem subtends all observed leaves, hence carries the zero Fourier
character and multiplier one.  Every displayed-tree term is therefore
unchanged, and strong tree-childness supplies an admissible tree-child
rerooting.

The primitive graph theorem gives exactly one cycle kernel and four directed
theta kernels.  Choose a rigid support: every path-sink child and one occupied
port on every segment of a minimum strong repair.  Its outgoing size is two
for a cycle, three for `theta0`, `theta1`, and `theta3`, and four for
`theta2`.  Every support has trivial pointwise labelled stabilizer.  Marginal
restriction is locally open because every serial K2P edge class

\[
(s_1,g_1),\ldots,(s_m,g_m)\longmapsto
\left(\prod_i s_i,\prod_i g_i\right)
\]

has an analytic physical section.  For an effective \((S,G)\in\mathcal
D_+\), choose \(r\) with

\[
\max\{S,G,2S-G,0\}<r^{m-1}<1
\]

and use \((r,r)\) on the first \(m-1\) factors and
\((S/r^{m-1},G/r^{m-1})\) on the last.  This proves both physical
surjectivity and differential rank two, rather than inferring either from an
unconstrained coordinatewise product.

The corrected finite theorem partitions every directed completion into:

1. pointwise displayed-quartet separation or a direct full-map
   \(\mathcal T_i\) zero-versus-strict-sign certificate;
2. a target-rank upper bound strictly below an exact source lower bound;
3. an exact target invariant nonzero on the source;
4. labelled mixed-graph isomorphism;
5. ordinary triangle redirection; or
6. a restoration obligation.

The raw generator retains every incoming mode, minimum repair, path-sink
child, full physical port permutation, omitted physical role, and
source-to-target direction.  The six four-port theta sources give exactly

\[
6(831+1983)4!=405216
\]

presentations.  They partition into 360408 displayed-quartet exclusions,
16974 direct full-map \(\mathcal T_i\) exclusions, 23822 exact-rank
exclusions, 1472 terminal presentations, and 2540 member presentations
representing exactly 997 restoration obligations.  For all 4379
graph-derived descriptors, symbolic log-Jacobian syzygies give an upper bound
equal to the exact rational-minor lower bound.

The four minimum-repaired `theta2` sources give exactly

\[
4(1983+4155)5!=2946240
\]

five-port presentations.  Per source, 735648 are displayed-quartet
exclusions, 632 have direct full-map \(\mathcal T_i\) certificates, and the
280 survivors form 88 rank-excluded, 24 quadratic-separated, and eight
isomorphic classes.  The 56 dummy-bearing raw isomorphism roots expand to 576
six-port and 288 seven-port paths; 760 are quartet-separated and 72 end in
physical labelled isomorphisms.

The two three-port cycle supports give exactly

\[
2(1120)3!=13440
\]

directions: 7452 direct full-map \(\mathcal T_i\) exclusions, 24 no-dummy
isomorphism/triangle terminals, and 5964 fixed-full restoration roots.
Restoring all omitted roles gives 536364 physical completions: 535920
quartet exclusions, 300 direct full-map \(\mathcal T_i\) exclusions, 132 exact quadratic
exclusions, and 12 labelled isomorphisms.  The 132 algebraic leaves form 54
descriptor-pair classes and all have direct strict-\(\mathcal D_+\) witnesses.

The remaining direct obstructions include the exhaustive multihomogeneous
quadratic deck and the independently replayed degree-three, degree-four, and
degree-five certificates.  Every graph terminal stores an explicit labelled
mixed-vertex map and, when applicable, the exact ordinary-triangle edge set.

For every one of the 997 four-port restoration obligations, physical child
generation correlates the
same target record, port match, omitted role, target attachment, and source
insertion edge.  This is invoked only after fixing a hypothetical full
containment between two actual networks.  Retain one actual omitted label in
those same networks and marginalize that full relation; openness of the
source restriction gives the enumerated direct-child containment into the
actual target restriction.  No selected relation is lifted and no target
deletion map is inverted.  The restoration forest separates every such child
and hence excludes every full relation inducing a frozen parent.  The
corrected forest contains 36568 first children: 35758 displayed-quartet
exclusions, 606 direct full-map \(\mathcal T_i\) exclusions, 148 quadratic
separations, 24 transported-quartic separations, and 32 continuing children.
Those 32 have exactly 256 second children, of which 248 are
displayed-quartet exclusions and eight have direct full-map \(\mathcal T_i\)
certificates.  Its transports restrict exactly to their parent transports.
The cycle and `theta2` dummy-terminal restorations above use the same
fixed-full implication; a selected isomorphism is never lifted abstractly.

Graph-terminal presentations with omitted roles are a separate coherence
layer, not members of the 997-parent obstruction forest.  The four-port
terminal ledger has 55 labelled isomorphism/ordinary-triangle classes with 80
selected member presentations.  Exact-relation-first fixed-full expansion yields 26
already physical anchors and 17 restored physical anchors, including four
incoming-role ordinary-triangle anchors that the revoked rooted oracle had
missed.  Their role is to seed the coherent probe reconstruction, not to
exclude a containment.

The all-primitive probe gate must adjoin every physical equality anchor,
classify every one- and two-port direction, and bind each surviving labelled
incidence transport to its exact parent.  A first candidate ledger was
revoked after an independent audit found a root-sensitive three-leaf
restriction oracle that mislabeled exact graph terminals as tree--sunlet
separations.  Equation (L), and hence theorem promotion, is conditional on a
corrected semi-directed-invariant replay with zero unresolved or incoherent
rows.

The corrected probe input consists of 176 distinct physical path records:
43 four-port direct/restored anchors, 96 restored `theta2` anchors, 36 cycle
anchors, and one ordinary-tree anchor.  Their relation census is 143 labelled
isomorphisms and 33 ordinary triangles.  Every edge of each suppressed mixed
graph is an insertion site—pendant arms, reticulation-incoming edges, and the
root-suppressed segment included—and the two artificial-root halves are
identified only after an exact semi-directed isomorphism replay.  This gives
2206 sites on each side and 29964 one-port Cartesian directions before
classification.

Once that final gate passes, the complete bounded relation is

\[
H\preceq_+H'\quad\Longleftrightarrow\quad
H\cong H'\ \text{or}\ H\sim_T H'.
\tag{L}
\]

One-port restrictions locate every omitted label relative to the rigid
support.  Two-port restrictions determine the total order of labels on a
common segment.  To see completeness, root at the fixed incoming support port
and suppress only unported bivalent vertices.  Every additional physical
boundary is attached at a unique subdivision of one of the finitely many
directed core segments.  Therefore its one-port restriction records its
segment, and the restriction of a pair on the same segment records their
order.  Segment membership plus all pair orders reconstructs the complete
finite word on every segment.  Since the restrictions come from the same two
words, the comparisons are transitive, and the certified child transports
all restrict to the same pointwise-rigid anchor.  A probe through a triangle
edge destroys the triangle and fixes literal orientation; otherwise the
unique ordinary triangle persists with its stored edge set.  Thus all probes
assemble to a single labelled full-word isomorphism modulo one coherent
triangle choice at each ordinary triangle factor.

## 5. Necessity

Assume \(N\preceq_+N'\).  Section 2 gives the same labelled decorated tree
of blobs.  Sections 3--4 localize the relation to every pair of corresponding
factors and transfer it, by an open marginal, to the finite theorem.  Formula
(L), restoration, and coherent probes force every corresponding pair to be
labelled-isomorphic or related by one coherent ordinary triangle
redirection.  Distant factors cannot cancel a local separator: bridge
extraction is analytic and its only fibre is the two-sector incidence action,
while every algebraic obstruction is multihomogeneous under that action.

## 6. Sufficiency

For an isomorphic pair, transport a physical parameter section through the
labelled isomorphism.  For an ordinary triangle, let
\(\tau_i:\Theta_i\to Q\) be the three orientation maps.  At the certified
common strict continuous-time point every \(\tau_i\) has rank 9, the full
dimension of the normalized three-boundary K2P tensor space.  Hence all three
maps cover one common open set \(U\subset Q\) with physical analytic
sections.

An embedded triangle also needs a contextual rank argument.  Cut its three
ordinary arms and write the identical remainder of the network as one
analytic contraction

\[
 H:Q\times C\longrightarrow Y.
\]

Choose \((q,c)\) in the nonempty open set \(U\times C\) where \(DH\) has
generic maximal rank \(R\).  Since each \(\tau_i\times\mathrm{id}_C\) is a
submersion,

\[
 \operatorname{rank}D\bigl(H\circ
 (\tau_i\times\mathrm{id}_C)\bigr)=R
\]

for every orientation.  Thus \(H(U\times C)\) contains one
\(R\)-dimensional regular germ which is full-dimensional in every redirected
network image, including when the context reconnects the three arms inside a
level-2 blob.  Separate paired and singleton boundary gauges are absorbed
into sufficiently small strict physical arm pairs.

After choosing analytic incidence slices, let the two physical sections have
positive incidence products \(A_e^{(k)},B_e^{(k)}\).  For each bridge choose
\(s_e>0\) so small that both \(s_e/A_e^{(k)}<1/2\), and choose \(g_e>0\) so
small that both \(g_e/B_e^{(k)}<1\).  The original and both transformed pairs
then lie in \(\mathcal D_+\), because their \(s\)-coordinate is below
\(1/2\).  Shrinking the local germs makes these choices uniform.  Incidence
factors cancel termwise in the global contraction, and the local product
chart proves the expected full rank.  Therefore the two global networks have
a common full-dimensional regular germ.

## 7. Final theorem (K2P-SAME)

Let \(N,N'\) be leaf-labelled binary standard semi-directed strongly
tree-child level-2 networks on the same leaf set.  On \(\mathcal D_+\),

\[
N\preceq_+N'
\quad\Longleftrightarrow\quad
\begin{cases}
\operatorname{ToB}(N)=\operatorname{ToB}(N')
 &\text{as labelled decorated trees},\\
\text{every corresponding factor is labelled-isomorphic}\
\text{or differs by ordinary triangle redirection.}
\end{cases}
\]

Whenever this condition holds, \(N\bowtie_+N'\).  The condition is
symmetric, so there is no proper one-sided containment within the strong
class.  This classifies regular source-relative containment and common germs;
it does not assert equality of complete stochastic images.

## 8. Generic identifiability

For fixed \(n\), only finitely many labelled standard strong level-2
topologies exist.  For a fixed \(N\), take the finite union inside its
irreducible complex image closure of:

* the singular locus and images of source rank-drop strata;
* the Zariski closures of intersections with every topology not equivalent
  to \(N\) under the theorem;
* the zero sets of the finitely many nonidentically-zero cut anchors,
  incidence anchors, rank minors, and local certificate pullbacks used by
  reconstruction.

Every component is proper.  Indeed, stratify the physical source and every
physical target parameter space into finitely many constant-rank
semialgebraic pieces.  If the Zariski closure of one physical intersection
were the entire irreducible source closure, that intersection would have full
real semialgebraic dimension and some regular source stratum would contain a
relatively open germ.  For the target-section clause, stratify the physical
incidence correspondence

\[
 Z=\{(q,\theta'):q=\Phi_{N'}(\theta')\}
\]

over that germ.  Some stratum of \(Z\) projects with full rank, so the
constant-rank theorem supplies a physical analytic target section after
shrinking.  This is exactly \(N\preceq_+N'\), contradicting the
classification.  Outside the resulting proper algebraic exceptional set, an
exact K2P distribution determines the labelled standard semi-directed
topology modulo coherent ordinary triangle redirection.

## 9. Exact reconstruction

For a distribution outside the exceptional set:

1. Fourier transform the pattern table.
2. Evaluate the pointwise quartet sign deck and build the labelled tree of
   blobs.
3. Use the direct full-map \(\mathcal T_i\) polynomials to decorate
   degree-three nodes.
4. Factor the positive bridge blocks in the paired and singleton sectors.
5. Apply the analytic incidence anchors to obtain every projective local
   tensor and both normalized effective bridge coordinates.
6. Evaluate the finite local certificate deck to identify a rigid support.
7. Follow the bound restoration records and their exact transports.
8. Use the all-primitive one- and two-port ledgers to recover every label
   location and segment order.
9. Quotient the one coherent ordinary-triangle choice and return the
   lexicographically least representative of the structural class.  Other
   redirected representatives may be listed as structural alternatives, but
   membership of the particular input distribution in any such alternative
   requires a separate exact semialgebraic membership test.

The procedure terminates.  The largest certified local restriction contains
nine physical ports (a seven-port restored `theta2` anchor plus two probes).
A direct implementation therefore uses \(O(n^9)\) bounded restrictions in
addition to the Fourier transform of the explicit \(4^n\) probability table.
No bit-complexity or physical bridge-parameter identifiability claim is made.

## 10. Strict continuous-time corollary

Restrict every edge to \(0<s<1\), \(s^2<g<1\).  Power subdivision gives the
paired marginal sections.  The displayed-quartet and direct full-map
\(\mathcal T_i\) signs remain strict.  Every nonzero algebraic source witness
stays nonzero on a dense open part of the continuous-time parameter cone
because that cone is nonempty and Euclidean open.  The triangle's exact
common rank-nine point is
continuous-time.  For bridge incidence products
\(A^{(k)},B^{(k)}>0\), \(k=1,2\), choose \(s>0\) small and then

\[
\max\left\{1,{B^{(1)}\over(A^{(1)})^2},
                {B^{(2)}\over(A^{(2)})^2}\right\}s^2
<g<\min\{1,B^{(1)},B^{(2)}\}.
\]

Both the original and transformed bridge pairs are continuous-time.
Therefore the classification, common-germ conclusion, generic-identifiability
corollary, and reconstruction theorem all hold on the strict continuous-time
cone.

## 11. Sharpness

The separate weak-class certificate gives two three-leaf level-2 networks
with rooting censuses \((5,2)\) and \((7,2)\), so both are weakly but not
strongly tree-child.  They are neither isomorphic nor triangle-related.  At
explicit strict continuous-time parameters they produce the same tensor,
and both Jacobians have exact rank 9.  Hence they share a nine-dimensional
regular germ.

Replace the same labelled leaf on both sides by an identical cherry.  In
each K2P sector the local rational observables \((u/v,uv)\) have Jacobian
determinant \(2u/v\ne0\), so the paired sectors add at least four independent
dimensions.  Conversely, the entire cherry-extended tensor factors through
the old tensor and the four new arm eigenvalues, so its image dimension can
increase by at most four.  It therefore increases by exactly four per
cherry.  Iteration yields, for every \(n\ge3\), a common

\[
9+4(n-3)=4n-3
\]

dimensional strict continuous-time germ between nonisomorphic,
non-triangle-related networks in the weak-but-not-strong class.  Pruning the
labelled cherries recovers the base pair, so class membership and
inequivalence persist.  Strong tree-childness is therefore sharp.
