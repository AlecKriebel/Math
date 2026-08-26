# Generic identifiability and directed containment for strongly tree-child level-2 networks under K2P

## Promotion status

This is the promoted theorem manuscript for the principal positive K2P
domain.  Every analytic, graph-theoretic, raw-four-port, five-port,
restoration, cycle, ordinary-triangle, probe, genericity, reconstruction,
continuous-time, and weak-sharpness layer cited below has passed its stated
independent replay and adversarial mutations.  In particular, the corrected
all-primitive one- and two-port package has zero unresolved rows, zero missing
or multiple parent bindings, zero cycles, and zero incoherent transport
restrictions.  Its exact primary, independent-replay, mutation, and ledger
hashes are frozen in Section 7 and Appendix A.  The promotion guard passes.

Theorems 8.3, 9.1, 10.1, 11.1, and 12.1 are therefore unconditional under
their stated hypotheses.  “Unconditional” here means that no computational
gate remains; it does not remove any domain, regularity, network-class, or
genericity hypothesis written in the theorem statements.

Every statement is confined to the domain defined below.  Nothing here
classifies any other stochastic sign component.

## 1. Networks, model, and relations

Let \(X\) be a finite labelled leaf set.  A *standard semi-directed network*
is obtained from a rooted binary phylogenetic network by suppressing the
root, forgetting directions on ordinary arcs, and retaining the arrowheads
entering reticulations, under the standard no-parallel-edge and suppression
conventions used by the primitive graph enumeration.  It is *level 2* when
each blob has cyclomatic number at most two.  It is *strongly tree-child*
when every admissible rooted representative is tree-child.  These are the
conventions used throughout; in particular, “strong” is not being replaced
by existence of one tree-child rooting.

For the group \(\mathbb Z_2\times\mathbb Z_2\), use character order
\(0,C,G,T\).  A K2P edge has Fourier spectrum

\[
 (1,s,g,s).
\]

The parameter domain in the main theorem is

\[
 \mathcal D_+
 =\{(s,g):0<s<1,\ 0<g<1,\ g>2s-1\}.
\tag{1.1}
\]

Every inheritance probability is in \((0,1)\).  For a network \(N\), let
\(\Theta_+(N)\) be the corresponding open physical parameter space, let
\(\Phi_N\) be its Fourier polynomial map, let
\(\mathcal M_+(N)=\Phi_N(\Theta_+(N))\), and put

\[
 d_N=\max_{\theta\in\Theta_+(N)}\operatorname{rank}D\Phi_N(\theta).
\]

A source point is *regular* when its Jacobian rank is \(d_N\).

We use a source-relative, section-bearing notion of containment.  Write
\(N\preceq_+N'\) when there are a regular point
\(\theta_0\in\Theta_+(N)\), a connected open neighborhood
\(U\subseteq\Theta_+(N)\) on which \(\Phi_N\) has rank \(d_N\), and a real
analytic map \(\sigma:U\to\Theta_+(N')\) such that

\[
 \Phi_N=\Phi_{N'}\circ\sigma\quad\text{on }U.
\tag{1.2}
\]

Write \(N\bowtie_+N'\) when the two images contain a common analytic germ
which is regular and full-dimensional in both images, with physical analytic
sections from both parameter spaces.  These relations concern regular image
germs.  They do not mean equality or inclusion of the complete stochastic
images.

An *ordinary triangle redirection* changes only the semi-directed
orientation of a three-cycle factor incident with exactly three external
arms.  Write \(N\equiv_\triangle N'\) when their labelled decorated trees
of blobs agree, corresponding non-triangle factors are related by labelled
mixed-graph isomorphisms, and each remaining corresponding factor differs by
an ordinary triangle redirection, with all boundary transports coherent.
This is a structural quotient; it is not a claim that every redirected
representative contains every particular distribution of every other
representative.

## 2. Domain, subdivision, and root invariance

### Lemma 2.1 (physical domain and subdivision)

The strict stochastic K2P inequalities for \((1,s,g,s)\) are

\[
 1-g>0,\qquad 1+2s+g>0,\qquad 1-2s+g>0.
\]

On the positive-eigenvalue component these reduce to (1.1).  Every point of
\(\mathcal D_+\) admits a strict K2P subdivision.  In particular, for all
sufficiently small \(\varepsilon>0\),

\[
 (s_B,g_B)=(1-\varepsilon,1-\varepsilon),\qquad
 (s_A,g_A)=\left({s\over1-\varepsilon},{g\over1-\varepsilon}\right)
\]

are both strict physical pairs and multiply coordinatewise to \((s,g)\).

**Proof.**  The inequalities are the inverse Fourier probabilities.  Their
strictness is open, and substitution in the displayed factorization gives
the required sufficiently small interval for \(\varepsilon\).  This avoids
the invalid assertion that arbitrary coordinatewise square roots are
physical.  ∎

### Lemma 2.2 (root movement, including a retained arrowhead)

For the symmetric K2P model, \(\Phi_N\) is unchanged by moving the root to
any admissible rooting of the same standard semi-directed graph.

**Proof.**  Along an ordinary root-to-leaf path, reverse only ordinary arcs;
K2P transition matrices are symmetric.  Subdivide the new root edge using
Lemma 2.1 and suppress the old root.  If the old root lies on an edge entering
a reticulation, inspect each switching.  When that parent is selected, the
two old root arms occur only through their serial products.  When the other
parent is selected, the remaining one-child root stem subtends every
observed leaf and therefore carries total Fourier character zero and
multiplier one.  Every displayed-tree summand is unchanged.  Strong
tree-childness supplies the required admissible tree-child rooting.  ∎

Thus \(\preceq_+\), \(\bowtie_+\), and the structural quotient are
well-defined for the standard semi-directed objects rather than for a
chosen root presentation.

## 3. Pointwise recovery of the decorated tree of blobs

### Lemma 3.1 (displayed-quartet separation)

If two strict physical K2P restrictions display different quartet sets,
their Fourier tensors are unequal.  More precisely, after a physical port
permutation, one of

\[
 q_{CCCC}-q_{CCTT},\qquad
 q_{CCCC}-q_{CCTT}-q_{CTTC}+q_{CTCT}
\tag{3.1}
\]

is zero on one restriction and strictly positive on the other.  Positive
inheritance mixtures preserve the strict sign.

The graph-theoretic displayed-quartet theorem therefore reconstructs the
labelled tree of blobs pointwise from every tensor in \(\mathcal M_+(N)\).
In particular, \(N\preceq_+N'\) implies equality of the labelled trees of
blobs.

### Lemma 3.2 (degree-three decoration)

For each physical orientation of a three-boundary restriction, the
whole-map polynomial

\[
 \mathcal T_i=V^2X_g-X_s^2Y_gZ_g
\tag{3.2}
\]

vanishes identically on the ordinary degree-three tree factor and has a
fixed strict nonzero sign on the corresponding three-cycle factor throughout
\(\mathcal D_+\).  Hence the ordinary-vertex/three-cycle decoration is also
pointwise determined.  A strong theta factor has at least four physical
boundaries and cannot be confused with an ordinary three-boundary factor.

Lemmas 3.1 and 3.2 use whole semi-directed maps.  No rooted
restriction label is used as an oracle.

## 4. The complete two-sector bridge fibre

Cut every bridge of the common decorated tree of blobs.  In each nonzero
character block, positivity and rank-one uniqueness leave an incidence
scale at each side.  The two K2P character orbits are \(\{C,T\}\) and
\(\{G\}\).

### Lemma 4.1 (equality of the \(C\)- and \(T\)-scales)

Let a positive normalized local boundary tensor be transformed by positive
incidence functions \(c_e(h)\), with \(c_e(0)=1\), and suppose both the
original and transformed tensors are K2P-invariant under the exchange
\(C\leftrightarrow T\).  Put

\[
 \rho_e={c_e(C)\over c_e(T)}>0.
\]

If the component is marked by a retained physical block, compare the
positive conservation-supported entries with \(C,C\), respectively
\(T,T\), at incidence \(e\) and that block, with zero elsewhere.  Invariance
before and after scaling gives \(\rho_e=1\) for every incidence.

If the component is unmarked and has degree \(d\ge3\), the analogous
comparison at every pair \(e\ne f\) gives

\[
 \rho_e\rho_f=1.
\]

Three distinct incidences and positivity force all \(\rho_e=1\).

For \(d=2\), and only there, the argument leaves the genuine stabilizer

\[
 (\rho_1,\rho_2)=(t,t^{-1}),\qquad t>0.
\tag{4.1}
\]

This case does not occur in the retained class.  The graph-derived primitive
supports have respectively 3 ports for the cycle, 4 ports for
\(\theta_0,\theta_1,\theta_3\), and 5 ports for \(\theta_2\); restoration
and probing only add marked ports; and every unmarked ordinary component has
degree at least three.  The only simple reduced two-boundary theta has path
lengths \((1,2,2)\), namely \(K_4-e\).  Its exact graph replay enumerates 25
rooted binary acyclic presentations and zero tree-child presentations, so it
is excluded from the strong class.

### Theorem 4.2 (complete bridge fibre)

On \(\mathcal D_+\), the complete positive fibre created by cutting and
regluing bridges is exactly

\[
 P_v\longmapsto P_v\prod_{e\ni v}
 a_{v,e}^{\mathbf 1[h_e\in\{C,T\}]}
 b_{v,e}^{\mathbf 1[h_e=G]},
\tag{4.2}
\]

\[
 s_e\longmapsto{s_e\over a_{u,e}a_{v,e}},\qquad
 g_e\longmapsto{g_e\over b_{u,e}b_{v,e}}.
\tag{4.3}
\]

There is no additional positive gauge.  The action is free on all retained
components and has no two-sector holonomy.

**Proof.**  All-zero normalization fixes the zero-character scale.  Positive
rank-one uniqueness gives one scale in each character block.  Lemma 4.1
identifies the \(C\)- and \(T\)-scales, while the singleton \(G\)-scale is
independent.  For an unmarked degree-\(d\) component, the pair-anchor exponent
rows

\[
 (12),(13),(23),(14),\ldots,(1d)
\]

have rank \(d\), with leading determinant \(-2\), separately in the paired
and singleton sectors.  Marked components use physical identity anchors.
These give analytic normalizers and freeness.  Peeling the bridge tree
excludes any holonomy.  ∎

### Lemma 4.3 (physical local product saturation)

The quotient chart of Theorem 4.2 restricts to a physical local product
chart; it is not merely an ambient positive-tensor quotient.

**Proof.**  For an effective bridge \((s,g)\), choose \(r<1\), sufficiently
close to one, such that

\[
 (r,r),\qquad (s/r^2,g/r^2),\qquad(r,r)
\tag{4.4}
\]

all lie in the interior of \(\mathcal D_+\).  Around this interior serial
split, the two endpoint pairs vary in four independent coordinates while the
residual pair remains physical.  Their ratios realize the four incidence
directions in (4.2)--(4.3).  Suppression of the two serial bivalent vertices
returns the same standard bridge.  Make these choices independently on the
bridge tree and shrink to a constant-rank chart.  ∎

No step asserts that an arbitrary normalized local tensor is itself a
physical network tensor.

## 5. Physical localization, marginal openness, and restoration

### Lemma 5.1 (paired marginal open image)

For every \(m\ge1\), the serial-edge map

\[
 ((s_1,g_1),\ldots,(s_m,g_m))
 \longmapsto\left(\prod_i s_i,\prod_i g_i\right)
\tag{5.1}
\]

maps \(\mathcal D_+^m\) onto \(\mathcal D_+\), has differential rank two,
and has a local physical analytic section.

**Proof.**  Given \((S,G)\in\mathcal D_+\), choose \(r\) with

\[
 \max\{S,G,2S-G,0\}<r^{m-1}<1.
\tag{5.2}
\]

Use \((r,r)\) on the first \(m-1\) factors and
\((S/r^{m-1},G/r^{m-1})\) on the last.  The inequalities in (5.2) put the
last pair strictly in \(\mathcal D_+\).  Varying \((S,G)\) gives the local
section and rank two.  ∎

By Lemmas 2.2, 4.3, and 5.1, a hypothetical global containment localizes to
each corresponding component and to every graph-derived rigid support.
Incoming structural boundaries can be selected by root movement, and
omitted physical roles can be restored by open marginals.

### Lemma 5.2 (fixed-full restoration implication)

Fix actual networks \(N,N'\), a full relation (1.2), a particular omitted
leaf label, a source insertion edge, a target attachment, and the induced
boundary transport.  Marginalizing that same full relation produces the
enumerated child relation, and Lemma 5.1 makes its source restriction open.
Therefore any exact separator for every such physical child excludes the
fixed full parent relation.

The quantifiers in this lemma are essential: it neither lifts an abstract
selected relation nor inverts a target deletion map.  A graph-terminal
relation with an omitted role is expanded relation-first and is not silently
reassigned to the obstruction forest.

## 6. Frozen bounded finite theorem

All rows in this section are generated from primitive graph encodings, retain
the source-to-target direction and all physical port data, and bind exactly
one evidence object.  The authoritative ledgers contain no rooted
classification fields.

### 6.1 Four-port theta universe

The six four-port theta sources yield

\[
 6(831+1983)4!=405{,}216
\]

directed raw presentations, with no duplicate or missing raw identifier:

\[
\begin{array}{lr}
\text{displayed-quartet exclusion}&360{,}408\\
\text{whole-map }\mathcal T_i\text{ strict-sign exclusion}&16{,}974\\
\text{exact directed rank exclusion}&23{,}822\\
\text{direct terminal presentation}&1{,}472\\
\text{restoration-member presentation}&2{,}540.
\end{array}
\tag{6.1}
\]

The terminal presentations bind to 934 exact terminal classes.  The
restoration members bind one-to-one to membership records for exactly 997
canonical parent obligations.  Each rank row contains a nonzero exact source
minor and a symbolic target upper certificate, with strict source-lower
greater than target-upper.  Every quartet row binds its exact displayed
quartet witness.

The compact terminal registry partitions the 934 classes into 839 exact
multihomogeneous quadratics, 36 exact direct polynomial separators, four
additional `F2/F3/F4` hard-case bindings, 20 labelled mixed-graph
isomorphisms, and 35 ordinary-triangle quotients.  The 36-record direct
polynomial overlay is exactly 22 quintic port-orbit obstructions, 12 quartic
obstructions, and two cubic obstructions.  Each has identically zero target
pullback, nonzero rational source pullback, and a strict physical source
witness.  The independent compiler replay and mutation suite bind the
record-to-certificate assignment and reject cubic, quartic, or quintic
reassignment.

### 6.2 Five-port \(\theta_2\) universe

The four minimum-repaired \(\theta_2\) sources yield

\[
 4(1983+4155)5!=2{,}946{,}240
\]

directed presentations:

\[
\begin{array}{lr}
\text{displayed-quartet exclusion}&2{,}942{,}592\\
\text{whole-map }\mathcal T_i\text{ strict-sign exclusion}&2{,}528\\
\text{exact directed rank exclusion}&800\\
\text{direct quadratic separator}&240\\
\text{labelled isomorphism}&80.
\end{array}
\tag{6.2}
\]

All 2,528 sign rows replay on the whole maps.  The 56 dummy-bearing
isomorphism roots generate 864 physical descendants with exactly one parent
and coherent restricted transport.  The terminating descendant forest has
832 leaves: 760 displayed-quartet exclusions and 72 labelled isomorphisms;
it has no missing continuation layer, cycle, or unresolved row.

### 6.3 Three-port cycle universe

The authoritative base ledger has 13,440 directions:

\[
\begin{array}{lr}
\text{whole-map }\mathcal T_i\text{ strict-sign exclusion}&7{,}452\\
\text{fixed-full restoration obligation}&5{,}964\\
\text{labelled isomorphism}&8\\
\text{ordinary triangle relation}&16.
\end{array}
\tag{6.3}
\]

The 5,964 roots generate 536,364 physical completions, partitioned as

\[
\begin{array}{lr}
\text{displayed-quartet strict separator}&535{,}920\\
\text{whole-map }\mathcal T_i\text{ strict-sign exclusion}&300\\
\text{exact directed quadratic separator}&132\\
\text{labelled isomorphism}&12.
\end{array}
\tag{6.4}
\]

There are zero childless roots, unresolved rows, incoherent transports, or
legacy rooted reason fields.

### 6.4 The 997 restoration obligations

The corrected fixed-full forest has 36,568 first children.  Of these,
35,758 have displayed-quartet separators, 606 have whole-map
\(\mathcal T_i\) strict-sign certificates, 148 have exact
multihomogeneous quadratics, 24 have transported exact quartics, and 32 are
continuations.  Those 32 parents have 256 second children: 248 quartet
separators and eight whole-map \(\mathcal T_i\) separators.  Thus the forest
has 36,824 edges, 36,792 terminal leaves, maximum depth two, zero cycles,
zero missing children, zero unresolved leaves, and coherent transport
restriction on every edge.  Every first child has exact graph relation
`none`, so an omitted-role graph terminal has not been smuggled into the
obstruction forest.  Lemma 5.2 therefore discharges all 997 full-parent
obligations.

The exact hashes of these frozen ledgers and their independent replays are
listed in Appendix A.

## 7. Coherent one- and two-port completion

The frozen probe-input contract contains 176 distinct physical anchor paths:
43 four-port direct/restored anchors, 96 restored \(\theta_2\) anchors, 36
cycle anchors, and one ordinary-tree anchor.  Its exact relation census is
143 labelled isomorphisms and 33 ordinary triangles.  Every edge of each
suppressed mixed graph is an insertion site, including pendant arms,
reticulation-incoming edges, and the root-suppressed segment.  Artificial
root halves are identified only after exact semi-directed isomorphism.

### Closed gate \(G_{\mathrm{probe}}\)

The final corrected probe package is frozen with the following values:

\[
\begin{array}{ll}
\text{primary certificate file SHA-256}
 &\texttt{2f4d64b32a905ce2cc06bae7d03215f9239427d421825c2525437ee6ba2ccaf6}\\
\text{primary payload SHA-256}
 &\texttt{964e9f3c241e63a1b0b12b3ceb516c58525d410c3c550e8335b619a6817400e5}\\
\text{independent replay file SHA-256}
 &\texttt{b30e2e32e5eec86875031a8bba82d58689f18859896adeb6a6931888df75209f}\\
\text{independent replay payload SHA-256}
 &\texttt{9e50d3681cf2c572c1575e770c67f95723d8c3e8a3943b5963dec7d07c3bec63}\\
\text{mutation report file SHA-256}
 &\texttt{b0df0584163150c9a823b4e364b8ee46c196ae8abb28fdca4d3d5893a97bfea7}\\
\text{mutation report payload SHA-256}
 &\texttt{58006ed7b6677c055b5cdd7249857dc2f752fb3db9cfbcc5bbe5e0a26e31875f}\\
\text{one-port directed rows}
 &29{,}964\\
\text{two-port directed rows}
 &544{,}571\\
\text{combined ordered-ledger root}
 &\texttt{7868fed6f8e0c10fcb9740da8ffdcb7f64ea68939c99cba6f364da4cfd90bf50}.
\end{array}
\tag{7.1}
\]

The combined root is the SHA-256 of the canonical object containing the
one-port, two-port-parent-inventory, and two-port ordered roots, keyed by
those three names.  The exact census is

\[
\begin{aligned}
29{,}964={}&27{,}758\ \text{quartet}+99\ \mathcal T_i
 +1{,}915\ \text{isomorphism}+192\ \text{triangle},\\
544{,}571={}&511{,}266\ \text{quartet}+576\ \mathcal T_i
 +30{,}969\ \text{isomorphism}+1{,}760\ \text{triangle}.
\end{aligned}
\tag{7.2}
\]

The 2,107 one-port equalities form 469 exact graph-pair-plus-transport
classes and generate every two-port parent exactly once.  All 32,729
two-port equalities have their reversed one-port marginal in that universe.
The 33 triangle anchors generate exactly 192 one-port and 1,760 two-port
triangle equalities, all transporting the same inherited ordinary triangle;
no new triangle is created.  Every required zero gate is zero.

The machine placeholder additionally binds the exact byte hashes of the
one-port ledger, two-port parent inventory, two-port ledger, exact transport
ledger, parent-restriction ledger, and separation-proof registry.  Promotion
requires independent primitive reconstruction of all 176 anchors, complete
site Cartesian coverage, exact-relation precedence, exact quartet and
whole-map \(\mathcal T_i\) replay, transport and parent-restriction replay,
reverse-order coverage, global-triangle coherence, and targeted mutations.

### Lemma 7.1 (word reconstruction)

For two surviving physical local factors,
one-port restrictions determine the directed core segment containing each
omitted boundary and two-port restrictions determine the order of every pair
on a common segment.  Hence the complete labelled subdivision word on every
segment is determined.  All certified transports assemble to one labelled
mixed-graph isomorphism, except for one coherent orientation choice at each
ordinary triangle.

**Proof.**  Root at the fixed incoming support port and suppress only
unported bivalent vertices.  Every additional boundary attaches to a unique
subdivision of a finite directed core segment.  Its one-port restriction
records that segment.  A two-port restriction of two boundaries on the same
segment records their order.  Because these comparisons arise from actual
words they are transitive and recover the unique total word.  The probe gate
binds every child transport to its parent, so the reconstructed segment
words agree on overlaps.  A probe through a triangle edge fixes a literal
orientation; otherwise the unique ordinary triangle survives with its stored
edge set.  The choices are therefore coherent.  ∎

### Theorem 7.2 (bounded local relation)

For every pair \(H,H'\) of retained physical primitive factors,

\[
 H\preceq_+H'
 \quad\Longleftrightarrow\quad
 H\cong H'\ \text{as labelled mixed graphs}
 \quad\text{or}\quad H\equiv_\triangle H'.
\tag{7.3}
\]

**Proof.**  The ledgers in Section 6 assign every raw direction exactly once
to a strict pointwise separator, a strict rank exclusion, an exact direct
algebraic separator, a restoration obligation, a labelled isomorphism, or an
ordinary triangle.  Lemma 5.2 and the terminating forests discharge every
restoration obstruction.  Gate \(G_{\mathrm{probe}}\) and Lemma 7.1 assemble
all equality terminals and exclude every incoherent full extension.  No raw
direction remains.  Conversely, labelled isomorphisms transport parameters,
and ordinary triangles have the common-germ construction in Section 8.  ∎

## 8. Global directed-containment classification

### Lemma 8.1 (necessity)

Let \(N,N'\) be binary standard semi-directed strongly tree-child level-2
networks on the same labelled leaf set.  If \(N\preceq_+N'\), then
\(N\equiv_\triangle N'\).

**Proof.**  Section 3 forces the same labelled decorated tree of blobs.
Theorems 4.2 and Lemma 4.3 extract corresponding local factors, with exactly
the two incidence gauges and no hidden holonomy.  Lemmas 2.2 and 5.1 transfer
each localized relation to a rigid physical support.  Theorem 7.2 classifies
every such direction.  The one-/two-port transports make the local choices
globally coherent.  Distant components cannot cancel a local obstruction:
bridge extraction is analytic, its full fibre is (4.2)--(4.3), and every
finite algebraic certificate is multihomogeneous under that action.  ∎

### Lemma 8.2 (ordinary-triangle contextual sufficiency)

If \(N\equiv_\triangle N'\), then \(N\bowtie_+N'\).

**Proof.**  A labelled mixed-graph isomorphism transports a physical
parameter section.  For an ordinary triangle, let
\(\tau_i:\Theta_i\to Q\), \(i=1,2,3\), be its three normalized orientation
maps.  At the certified common strict continuous-time point, all three have
rank nine, the dimension of the normalized three-boundary K2P tensor space.
They therefore cover one common open set \(U\subset Q\) and have physical
analytic sections.

For an embedded triangle, write the identical external contraction as

\[
 \mathcal H:Q\times C\longrightarrow Y.
\]

Choose \((q,c)\) in the nonempty open subset of \(U\times C\) where
\(D\mathcal H\) has generic maximal rank \(R\).  Since every
\(\tau_i\times\mathrm{id}_C\) is a submersion,

\[
 \operatorname{rank}D\bigl(\mathcal H\circ
 (\tau_i\times\mathrm{id}_C)\bigr)=R
\]

for every orientation.  Thus \(\mathcal H(U\times C)\) supplies the same
full-dimensional regular contextual germ, even when the three arms reconnect
inside a level-2 blob.

For several ordinary-triangle factors, replace \(Q\) by the finite product
\(\prod_j Q_j\), replace \(U\) by \(\prod_j U_j\), and take the product of
the orientation submersions.  The same generic-context rank argument applies
once, so no induction assumes that a previously chosen context remains
generic after the next redirection.

It remains to glue the incidence gauges physically.  For the two local
sections let \(A_e^{(k)},B_e^{(k)}>0\), \(k=1,2\), be their paired- and
singleton-sector incidence products.  Choose \(s_e>0\) so small that
\(s_e/A_e^{(k)}<1/2\) for both \(k\), and then choose \(g_e>0\) so small that
\(g_e/B_e^{(k)}<1\) for both.  The original and both transformed pairs lie
in \(\mathcal D_+\), since each transformed \(s\)-coordinate is below
\(1/2\).  Shrink the germs uniformly.  The incidence factors cancel
termwise in the global contraction, and Lemma 4.3 gives the full-rank global
product germ.  ∎

### Theorem 8.3 (K2P-SAME)

For every finite labelled leaf set \(X\) and
every pair \(N,N'\) of binary standard semi-directed strongly tree-child
level-2 networks on \(X\), with all edge pairs in \(\mathcal D_+\) and all
inheritance probabilities in \((0,1)\),

\[
 \boxed{
 N\preceq_+N'
 \quad\Longleftrightarrow\quad
 N\equiv_\triangle N'
 \quad\Longleftrightarrow\quad
 N\bowtie_+N'.}
\tag{8.1}
\]

In particular, directed regular-germ containment is symmetric within this
class: there is no proper one-sided containment.  The theorem does not assert
equality of complete stochastic images.

**Proof.**  Lemma 8.1 proves necessity and Lemma 8.2 proves sufficiency.  A
common full-dimensional germ with physical sections gives containment in
both directions by definition.  ∎

## 9. Generic identifiability

### Theorem 9.1 (generic structural identifiability)

Fix a binary standard semi-directed strongly
tree-child level-2 network \(N\) on \(X\).  There exists a proper Zariski
closed subset

\[
 E_N\subsetneq\overline{\mathcal M_+(N)}^{\,\mathbb C}
\tag{9.1}
\]

such that every exact physical tensor
\(q\in\mathcal M_+(N)\setminus E_N\) determines the labelled standard
semi-directed topology of \(N\) uniquely modulo
\(\equiv_\triangle\).

**Proof.**  For fixed \(X\), only finitely many labelled standard strong
level-2 topologies occur.  The complex image closure of a fixed
parameterization is irreducible.  Inside it, take the finite union of the
singular locus, the closures of source rank-drop images, the closures of
intersections with each non-equivalent topology, and the zero sets of the
finitely many nonidentically-zero anchors, rank minors, and certificate
pullbacks used by reconstruction.

Every member is proper.  The only nonformal point is a competing physical
intersection.  Stratify the source, target, and incidence set

\[
 Z_{N'}=\{(q,\theta'):q=\Phi_{N'}(\theta')\}
\tag{9.2}
\]

into finitely many constant-rank semialgebraic strata.  If such an
intersection were Zariski dense in the irreducible source closure, it would
have full real semialgebraic dimension.  Some regular source stratum would
then contain an open germ, and some stratum of (9.2) would project onto that
germ with full rank.  The constant-rank theorem supplies a physical analytic
target section after shrinking.  This is \(N\preceq_+N'\), contradicting
Theorem 8.3 for a non-equivalent \(N'\).  ∎

The quantifier is “for each fixed \(N\), outside a proper exceptional set.”
It is not pointwise identifiability at every parameter, and it does not
identify individual bridge parameters within the incidence gauge fibre.

## 10. Exact reconstruction

### Theorem 10.1 (finite exact reconstruction)

There is a terminating exact procedure which,
given a tensor \(q\in\mathcal M_+(N)\setminus E_N\) for some binary standard
semi-directed strongly tree-child level-2 network \(N\), returns the unique
structural class \([N]_{\triangle}\).

**Procedure and proof.**

Here “exact” means that every input coordinate is supplied in a
representation supporting exact field operations, polynomial-sign decisions,
and real-closed-field quantifier elimination (equivalently, through an
exact-real oracle with those operations).  This is a termination model, not a
bit-complexity or numerical-stability claim.

1. Fourier-transform the exact pattern tensor.
2. Evaluate the pointwise quartet sign deck and reconstruct the labelled
   tree of blobs.
3. Evaluate the whole-map \(\mathcal T_i\) deck and decorate every
   degree-three node.
4. Factor the positive bridge blocks in the paired and singleton sectors and
   apply the analytic incidence normalizers.
5. Enumerate the finitely many bounded rigid-support candidates compatible
   with steps 2--4.  Apply the pointwise and polynomial separator tests to the
   recovered local tensors, retaining every candidate not excluded.
6. For each retained candidate, follow only exact fixed-full restoration
   records and their stored transports; the depth is at most two.
7. For each resulting support, apply the frozen one-/two-port probe ledger to
   recover every boundary segment and the complete label order on each
   segment.
8. Assemble every coherent labelled mixed-graph candidate and group the
   finite list into ordinary-triangle classes.  For each such class
   \(\mathcal C\), decide the exact semialgebraic feasibility statement
   \[
      q\in\bigcup_{H\in\mathcal C}\mathcal M_+(H).
   \]
   Since \(q\notin E_N\), exactly one class is feasible; return its canonical
   representative.

Each feasibility query is a finite existential semialgebraic sentence and
terminates by quantifier elimination under the exact-input convention.  The
true class is feasible.  If an inequivalent class were also feasible, then
\(q\) would belong to a competing physical intersection whose Zariski closure
is contained in \(E_N\), a contradiction.

All decks and forests are finite; the restoration depth is at most two and
the word reconstruction terminates.  The largest bounded restriction in the
input contract uses at most nine physical ports, so a direct implementation
uses at most \(O(|X|^9)\) bounded restrictions beyond reading and transforming
the explicit \(4^{|X|}\)-entry tensor.  No numerical stability or
bit-complexity bound is asserted.

The output is a structural triangle class.  Deciding whether the particular
input tensor belongs to the complete stochastic image of another redirected
representative is a separate exact semialgebraic membership problem and is
not claimed here.  ∎

## 11. Strict continuous-time corollary

Let

\[
 \mathcal D_{\mathrm{CT}}
 =\{(s,g):0<s<1,\ s^2<g<1\}.
\tag{11.1}
\]

This is a nonempty Euclidean-open subset of \(\mathcal D_+\).  Define
\(\Theta_{\mathrm{CT}}(N)\), \(\preceq_{\mathrm{CT}}\), and
\(\bowtie_{\mathrm{CT}}\) by replacing every edge domain with (11.1).

### Theorem 11.1 (continuous-time transfer)

The equivalence (8.1), the generic
identifiability statement of Theorem 9.1, and the structural reconstruction
of Theorem 10.1 all hold with \(+\) replaced by \(\mathrm{CT}\).

**Proof.**  Necessity follows because (11.1) is open inside
\(\mathcal D_+\): a continuous-time source germ and target section are also
a \(\mathcal D_+\) germ and section.  For sufficiency, positive power roots
give continuous-time serial subdivisions and marginal sections.  The
triangle common rank-nine witness lies strictly in (11.1).  For two incidence
sections with products \(A^{(k)},B^{(k)}>0\), choose \(s>0\) sufficiently
small and then choose \(g\) in the nonempty interval

\[
 \max\left\{1,{B^{(1)}\over(A^{(1)})^2},
                 {B^{(2)}\over(A^{(2)})^2}\right\}s^2
 <g<\min\{1,B^{(1)},B^{(2)}\}.
\tag{11.2}
\]

Then the original and both gauge-transformed bridge pairs satisfy (11.1).
Finally, every nonzero polynomial witness remains nonzero on a dense open
part of the continuous-time parameter space because that space is Euclidean
open.  The semialgebraic genericity and reconstruction arguments therefore
restrict unchanged.  ∎

No boundary case \(g=s^2\), \(s=0\), \(g=0\), or inheritance probability
in \(\{0,1\}\) is included.

## 12. Sharpness of strong tree-childness

The following theorem also has a proof independent of the finite probe gate.

### Theorem 12.1 (weak-class \(4n-3\) ambiguity)

For every integer \(n\ge3\), there exist two binary level-2 semi-directed
networks on the same \(n\)-leaf labelled set which are weakly tree-child but
not strongly tree-child, are neither labelled-isomorphic nor
ordinary-triangle-equivalent, and whose strict continuous-time K2P images
contain a common full-dimensional regular analytic germ of dimension

\[
 4n-3.
\tag{12.1}
\]

**Proof.**  On three leaves, use the following two rooted presentations and
then suppress the root while retaining reticulation arrowheads.  The first has
arcs

\[
 rS,rL_0,SU,SV,UX,VZ,ZX,UV,ZL_1,XL_2,
\]

with reticulations \(V,X\).  The second has arcs

\[
 rS,rL_0,SU,SX_0,VX_0,UX_1,VX_1,UV,X_0L_1,X_1L_2,
\]

with reticulations \(X_0,X_1\).  They are respectively the certified
\(\theta_0\) factor with an ordinary boundary on its \(V\!\to X\) segment
and the certified bare \(\theta_3\) factor.  Complete root-insertion
enumeration gives respectively

\[
 (\#\text{ admissible rootings},\#\text{ tree-child rootings})
 =(5,2),\qquad(7,2).
\]

Thus both are weak but not strong.  Exact labelled mixed-graph comparison
excludes both isomorphism and ordinary-triangle equivalence.

Put \(\delta=2^{-30}\).  On the first network, assign \((s,g)=(1/7,1/7)\)
to its seven internal edge classes, inheritance parameters
\((15996/16339,1/8)\), and pendant pairs \((s,g)=(x,x)\) at leaves
\(0,1,2\), where

\[
 x={86779\over80}\delta,\qquad {320\over253}\delta,
 \qquad {114373\over20240}\delta,
\]

respectively.  On the second network, assign \((1/4,1/4)\) to every
internal edge class, inheritance parameters \((1/2,1/6)\), and pendant
values

\[
 {16\over3}\delta,\qquad {32\over9}\delta,\qquad {96\over5}\delta.
\]

Every pair is strict continuous-time.  At these rational parameters, the two
maps give the same tensor: the six two-nonzero-character orbit coordinates equal
\(\delta^2\), the three all-nonzero orbit coordinates equal
\(\tfrac45\delta^3\).  Exact nonzero rational
\(9\times9\) minors give rank nine on both sides, the full normalized
three-leaf dimension.  Hence their images share a regular nine-dimensional
germ.

Replace the same labelled leaf on both sides by the same labelled cherry.
If its two edge pairs are \((u_s,u_g)\) and \((v_s,v_g)\), the four local
observables

\[
 R_s={u_s\over v_s},\quad P_s=u_sv_s,\qquad
 R_g={u_g\over v_g},\quad P_g=u_gv_g
\]

have Jacobian determinant

\[
 {4u_su_g\over v_sv_g}\ne0.
\tag{12.2}
\]

The audited physical witness
\((u_s,u_g)=(2/5,4/9)\),
\((v_s,v_g)=(3/7,5/11)\) lies strictly in (11.1), and (12.2) equals
\(2464/675\).  Thus a cherry adds at least four local dimensions.  Conversely
the extended tensor factors through the old tensor and these four edge
coordinates, so it adds at most four.  Iteration gives

\[
 9+4(n-3)=4n-3.
\]

Pruning the labelled cherries recovers the base pair.  It preserves the
existence of both a tree-child and a non-tree-child rooting, and any extended
isomorphism or triangle equivalence would prune to one for the base pair.
All properties therefore persist.  ∎

The theorem proves that the word “strongly” in Theorem 8.3 cannot be weakened
to “weakly,” already within strict continuous time.  It does not claim that
every weak network is ambiguous.

## Appendix A. Frozen evidence manifest

The following hashes are promotion inputs.  File hashes are SHA-256 hashes of
the exact bytes; payload hashes use the canonical semantic-payload convention
of the corresponding package.

| Layer | File SHA-256 | Payload SHA-256 |
|---|---|---|
| Domain, subdivision, rooting | `4e38beb68062deae8f83cd265daacbef8c5d3f6d73ce25ef47a54828b658d450` | `01d03c01482ba1f4f0e43d03c3defbff35bc10a97f8b19412ce96e4ce8025328` |
| Two-sector bridge and marginal | `9231a7b78c13e54b745eba68926276a6551c6c3512d6a85746baba6613c1aacf` | `5abc19f857a02c712d1386b53bf1ecea18ec31db852cb31b24ea7dde688630ee` |
| Independent component-scale audit | `77d3881e7f7d5f90d71339968e3268c5780a0cd51e893e476aac040200e49064` | `02013c3a0d9456c97d64ae06fd20b241057bfdb437f07acea4f15437860b8416` |
| Raw four-port composite ledger | `431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96` | `b4c4cb8a89afcc82edb266ee9fab1e9abc59c4ab977dd00dadc43304b3e4048c` (summary) |
| Raw four-port independent replay | `c5cd73b13265b7acc36f156889b86e2c04715181c6a1d70224cd725b0221a859` | `40770d3068e936a9c5d0e93225fa15feaed90a212d9515e1cb3f2d46c35979e0` |
| Raw four-port terminal registry | `0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d` | `30053d096e140becdf32d3f26cb3634e82fcd5461f89be24f5b83cee344b5b81` |
| Raw four-port mutation report | `83196bc33504fd1e17c8784d2c7530f358e85cff8161c8e5f14ba04a60c42d76` | `dc265e02da504666197320fcab90226fa44cfc5c5906bb4ef5b6f1ab35d44f02` |
| Five-port \(\theta_2\) composite ledger | `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659` | `c89dd764f7c66831db7f6a092fedf666a20f3594ef03647de3e85b5fbf04d0e8` (summary) |
| Five-port \(\theta_2\) independent replay | `dd02a752b2ce41628039d2f6da6fdab77f2a8ffd73b8cd80e2968790dbbf3150` | `7e4283fe726083927b14d483d55644e2892a311b0179aa70d4766576c66ab545` |
| Five-port \(\theta_2\) mutation report | `ec2c6ec092539048b4e7ab9d9cfea01caa985d0f35cae74ca56732dc4cfe4c84` | `5663b87d3f09eaac5e89db69ac5a1cf6069b308abf9bc4242650d0897ded1ff7` |
| Corrected 997-parent restoration forest | `43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8` | `0a3df52751ba38d7e6d4d118ee7068a98b7be7897d0aa732e96a74d7523a88bf` |
| Restoration independent replay | `24fa2e61f60610a8b24c4107ec7f866278f0cc671ca203d7aaa40a37bea291dd` | `36c89ff9729e049a374a9fead8488f7a90e62c617d17e242aca5d340faeb164a` |
| Authoritative cycle promotion | `b560fdf0545c36d576a4cdaf24af9984f6f7231180f20f6927121a57bf816a7a` | `df5e3966822af65e2341660bf3f607ff3635d69d3e5a89854afaef308727f2f1` |
| Ordinary-triangle common germ | `b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885` | `6fd43ae6d38629277c047d3888e970cdab51f4805dce36d71b2430095c1e1aa6` |
| Frozen probe-input contract | `7f686ae99dd5e6dafc1c04396b711d294a0bddd6a25574f9ea809b831ad7b377` | `579919ca13204ddf959b3a159e4849b69c05ac87861eba2221659ec45bd73f38` |
| Independent probe-input replay | `54de1bef73e76fc82132ef3f0250a0579ea401274a302ed4d8fbd015c9e8a053` | `96d14bae9b20646abfe64b85a7ac0f61377182f75479031f621ea0dbe2096fce` |
| Corrected full probe primary | `2f4d64b32a905ce2cc06bae7d03215f9239427d421825c2525437ee6ba2ccaf6` | `964e9f3c241e63a1b0b12b3ceb516c58525d410c3c550e8335b619a6817400e5` |
| Independent primitive/graph/full-map probe audit | `b30e2e32e5eec86875031a8bba82d58689f18859896adeb6a6931888df75209f` | `9e50d3681cf2c572c1575e770c67f95723d8c3e8a3943b5963dec7d07c3bec63` |
| Independent probe mutation report | `b0df0584163150c9a823b4e364b8ee46c196ae8abb28fdca4d3d5893a97bfea7` | `58006ed7b6677c055b5cdd7249857dc2f752fb3db9cfbcc5bbe5e0a26e31875f` |
| Independent structural/algebra probe replay | `bdeba4730b6a9b39d8a542119f0630f52600f8a3512835b30d19e30b4446604e` | `971d0fdc3b84cfd4001574ba80d272841eb809213b24984009dda4556ebc6261` |
| Independent site-transport partition replay | `017068d960e0bfc3d5e44b79b5acc4a8e93195c37d205e8c43321c23a0b77e61` | `a1f80d5ed090a1c6e31067123f0739392384d5124e75296cc76035430710497c` |
| Weak-sharpness primary | `e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd` | `dfecd30ea217810a902add48350025e5f00dfa1255718783df790a9c7e1a5182` |
| Weak-sharpness independent audit | `cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52` | `848cc69e28e3cbd8bc1ab7bbad82b0c3e240354079e95965b433c423edc2d8c5` |

All rows required by Gate \(G_{\mathrm{probe}}\) are present.  The promotion
guard verifies the primary, independent graph replay, mutation report, and
six raw probe ledgers byte-for-byte in addition to the 23 earlier frozen
inputs.

## Appendix B. Scope exclusions

The main classification does not include stochastic boundary points,
singular edge eigenvalues, inheritance probabilities 0 or 1, nonbinary
networks, networks of level greater than two, or networks that are merely
weakly tree-child.  It classifies regular analytic containment germs and
generic structural recovery, not full-image equality, universal parameter
identifiability, noisy-data estimation, numerical conditioning, or model
selection from finite samples.

## Reference

The topology-only primitive, repair, and displayed-quartet results reused in
the graph layer are from A. K. Englander, M. Frohn, E. Gross, N. Holtgrefe,
L. van Iersel, M. Jones, and S. Sullivant, *Identifiability of Phylogenetic
Level-2 Networks under the Jukes--Cantor Model*, bioRxiv
2025.04.18.649493, version 4 (2026-07-04), especially Propositions 2.9--2.10,
Theorem 2.11, and Corollary 2.12.  Only topology-level statements are reused;
all algebraic claims in this manuscript are K2P claims certified by the
artifacts above.
