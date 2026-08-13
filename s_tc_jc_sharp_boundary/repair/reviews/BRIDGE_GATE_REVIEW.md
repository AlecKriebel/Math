# Adversarial bridge-gate review

Date: 2026-08-09  
Scope: projective bridge quotient, an alternative marginal-localization route,
and the bridge-dependent global logic only.  No manuscript source was edited.

## 1. Verdict

### Status summary

- **PROVED:** On a leaf-supported bridge tree, equality of two positive,
  normalized, JC-symmetric tensor factorizations has exactly the full
  incidence-scaling ambiguity.  There is one scale at each endpoint of each
  bridge.  This statement correctly incorporates the zero-sum character
  constraint.

- **PROVED:** The stabilizer of the incidence action on one local factor is
  trivial if the factor has a retained physical block, and is also trivial for
  an unmarked factor of bridge degree at least three.  An unmarked degree-two
  factor has a one-dimensional stabilizer.  An unmarked degree-one factor is
  completely inaccessible and is forbidden by leaf support.

- **FALSE AS STATED:** The product chart in the repair source is not valid for
  an arbitrary bridge tree.  A retained unmarked degree-two component makes
  the separate local quotients plus one effective coordinate per original
  bridge one dimension too large.  The exact counterexample is given in
  Section 6.

- **PROVED, WITH EXPLICIT REDUCTION HYPOTHESES:** If every bridge-tree
  component either has a retained physical block or has degree at least three,
  the local actions are free, explicit analytic slices exist, and the observed
  positive regular germ is a product of the sliced local tensor germs and one
  intrinsic effective coordinate per bridge.

- **PROVED:** A simpler necessity argument avoids bridge-kernel and product-
  chart claims entirely.  After the bridge tree is known, choose one taxon in
  each component incident to a focal blob.  Marginalization replaces every
  outside branch by a positive JC arm scalar.  Independent adjacent bridge
  multipliers make the global-to-local marginal map a submersion onto a
  relative-open local source germ.  Thus one-sided global containment implies
  one-sided containment of the corresponding local marginal model (or of one
  member of a finite target role/completion union).

- **PROVED, CONDITIONALLY ON THE LOCAL ATLAS:** Direct bounded marginals can
  replace projective tensor peeling for semi-directed topology reconstruction.
  This requires the local atlas to include the ordinary three-valent tree
  factor, tree-versus-cycle/theta directions, root/incoming roles, and all weak
  target completions, with arm-multihomogeneous or sign-stable separators.

- **UNRESOLVED:** The repository has not yet locked the standard reduction,
  LSA trimming, and 2-sub-blob convention.  Consequently the bridge theorem
  must not be promoted for the manuscript's unqualified current class until
  Gate D is closed.  The current dependency file records that gate as open at
  [`repair/DEPENDENCY_GATES.md:5`](../DEPENDENCY_GATES.md).

- **UNRESOLVED:** This review does not certify the finite local atlas,
  bounded-support promotion, cut preservation, or the flagship global
  classification.  The marginal lemma removes the need for projective peeling
  in the *necessity/localization* step, but it does not supply those separate
  results.

The strongest safe bridge conclusion is therefore:

> **PROVED:** the corrected free reduced bridge theorem below is valid for a
> leaf-supported, homeomorphism-reduced component tree with no retained
> unmarked bivalent factor.  
> **UNRESOLVED:** whether the manuscript's present words define exactly that
> class is still a conventions question, not a bridge-algebra question.

## 2. Defects in the submitted bridge proof

### 2.1 The leaf-peeling sentence violates zero-sum conservation

**FALSE PROOF STEP.** The repair proof says to hold “all characters away from
the leaf block at zero” and then compare a nonzero separator sector
([repair source, lines 101--105](</Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/proofs/04_bridges.tex:101>)).
If the leaf side has total character $h\ne0$, global zero-sum forces the
complementary side also to have total $h$, because $G$ has exponent two.
It cannot be all zero.  The correct proof uses a complementary anchor
assignment of total $h$, as in Section 4 below.

This is a proof gap, not a counterexample to the corrected exact-kernel
statement.

### 2.2 The local action is not always free

**FALSE AS STATED.** The repair chooses one independent zero/nonzero anchor
ratio at every incidence and immediately declares an analytic slice
([lines 64--70](</Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/proofs/04_bridges.tex:64>)).
For an unmarked two-boundary factor, local conservation gives
$h_1=h_2$.  Its action is

\[
 P(h,h)\longmapsto
 P(h,h)(a_1a_2)^{\mathbf 1[h\ne0]}.
\]

Hence $(a_1,a_2)=(t,t^{-1})$ fixes the entire local tensor.  There cannot be
two independent local normalizing equations.  This defect invalidates the
unqualified freeness and dimension assertions at
[lines 72--96](</Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/proofs/04_bridges.tex:72>).

### 2.3 The advertised product chart overcounts retained bivalent factors

**FALSE THEOREM WITHOUT REDUCTION.** The theorem claims

\[
 \prod_v(\widetilde{\mathcal L}_v/A_v)\times
 \prod_{e}J_e
\]

with one $J_e$ for every original edge and dimension

\[
 \sum_v(\dim\widetilde{\mathcal L}_v-\deg v)+|E|.
\]

For the exact three-vertex path in Section 6.1, the observed logarithmic model
has dimension one, while that formula gives dimension two.  The right general
object is

\[
 \left(\prod_v \widetilde{\mathcal L}_v/A_v\right)
 \times
 \left((\mathbb R_{>0})^E/H\right),
\]

locally, where $H$ is the product of the local stabilizers acting on the
edge coordinates.  Equivalently, suppress unmarked bivalent components first;
one maximal chain then has one effective coordinate, not one coordinate per
pre-suppression edge.

### 2.4 “Intrinsic cross-ratios” were asserted, not defined

**PROOF GAP.** The repair source says that cross-ratios recover $j_e$
intrinsically ([lines 116--120](</Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/proofs/04_bridges.tex:116>))
but gives neither valid zero-sum anchors nor a formula.  Section 5.3 supplies
both.

### 2.5 The target product-stratum sentence is unnecessary and unjustified

**PROOF GAP.** Directed localization invokes a target product description on
each regular stratum
([lines 140--149](</Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/proofs/04_bridges.tex:140>)).
A target preimage may be singular, and no argument places all target points in
one such chart.  This can be repaired in two ways:

1. use only the universal intrinsic extraction map; any target realization
   necessarily extracts a target local tensor orbit, without selecting target
   parameters; or
2. use the marginal-localization lemma in Section 8, which requires no bridge
   quotient at all.

### 2.6 The older manuscript source remains false and was not modified

The current manuscript still calls the reciprocal one-parameter action the
complete gauge
([`source/paper/sections/04_bridges.tex:35`](../../source/paper/sections/04_bridges.tex))
and bases its chart on only that quotient
([`source/paper/sections/04_bridges.tex:75`](../../source/paper/sections/04_bridges.tex)).
The numerical triples already printed in the repair source disprove that
claim.  Per the task instruction, this review did not edit those files.

## 3. Exact setup

Let $G=\mathbb Z_2\times\mathbb Z_2$, and let
$\mathcal T=(V,E)$ be a finite tree of components.  For $v\in V$:

- $X_v$ is its set of retained physical character blocks;
- $E(v)$ is its set of bridge incidences;
- the local domain is

\[
 D_v=\left\{(g,h)\in G^{X_v}\times G^{E(v)}:
 \bigoplus_{i\in X_v}g_i\oplus
 \bigoplus_{e\in E(v)}h_e=0\right\};
\]

- $P_v:D_v\to\mathbb R_{>0}$ is normalized by $P_v(0)=1$ and is
  invariant under the diagonal action of
  $\operatorname{Aut}(G)\cong S_3$.

For every bridge $e=uv$, let $x_e>0$.  For a globally zero-sum assignment
$g\in G^{\bigsqcup_v X_v}$, the character $h_e(g)$ is the sum on either
side of the bridge.  The contraction is

\[
 \Gamma(P,x)(g)=
 \prod_{v\in V}P_v(g|_{X_v},(h_e(g))_{e\in E(v)})
 \prod_{e\in E}x_e^{\mathbf1[h_e(g)\ne0]}.
\tag{3.1}
\]

The following hypotheses are explicit.

- **Leaf support:** every side of every bridge contains a retained physical
  block.  This is what LSA trimming and the condition that every cut component
  contains a labelled leaf are meant to ensure.
- **Arm extension:** near the point under study, multiplying a local nonzero
  boundary sector by an incidence scale is realized within the arm-extended
  local tensor germ.  For a network this is supplied by the ordinary arm-edge
  multiplier, after shrinking the neighborhood so it stays in $(0,1)$.
- **Local regularity:** each local tensor image is taken on a smooth regular
  positive stratum.
- **Reduced-component condition (R):** for every $v$, either
  $X_v\ne\varnothing$, or $\deg_{\mathcal T}(v)\ge3$.

The first two hypotheses concern the factorization itself.  Condition (R) is
needed only for the *separate local quotient product*.

## 4. Exact full-kernel theorem

### Theorem 4.1 (complete positive JC factorization fiber)

**PROVED.** Assume leaf support.  Two collections $(P,x)$ and $(Q,y)$ in
the setup of Section 3 satisfy

\[
 \Gamma(P,x)=\Gamma(Q,y)
\]

if and only if there are positive numbers $a_{v,e}$, one for every
incidence, such that

\[
 Q_v(g,h)=P_v(g,h)
 \prod_{e\in E(v)}a_{v,e}^{\mathbf1[h_e\ne0]},
\tag{4.1}
\]

and

\[
 y_e=\frac{x_e}{a_{u,e}a_{v,e}}
 \qquad(e=uv).
\tag{4.2}
\]

This is an equality-of-fibers statement, not merely a differential-kernel
calculation.

#### Proof

The reverse implication follows immediately from (3.1).  For the forward
implication, root $\mathcal T$ at a component $r$.  For an oriented edge
$e=pv$, let $S_v$ be the component subtree below $v$.  Contract all
factors in $S_v$, excluding the multiplier on $e$, to obtain a positive
aggregate boundary tensor $L^P_e(g_{S_v},h)$; define $L^Q_e$ similarly.

For fixed $h$, the observed cut flattening is a positive rank-one matrix:

\[
 F_h=L^P_e\,x_e^{\mathbf1[h\ne0]}(R^P_e)^{\mathsf T}
     =L^Q_e\,y_e^{\mathbf1[h\ne0]}(R^Q_e)^{\mathsf T}.
\]

Leaf support guarantees at least one valid row and column in every character
sector $h\in G$.  Positive rank-one uniqueness therefore gives

\[
 L^Q_e(g,h)=c_e(h)L^P_e(g,h)
\tag{4.3}
\]

with a scalar depending only on $h$, not on $g$.  The all-zero aggregate
entry is one on both sides, so $c_e(0)=1$.  Both aggregate tensors are
JC-symmetric.  Applying any $\alpha\in\operatorname{Aut}(G)$ to (4.3) gives
$c_e(\alpha h)=c_e(h)$.  Since $\operatorname{Aut}(G)$ acts transitively
on $G\setminus\{0\}$, there is a single $c_e>0$ for the three nonzero
sectors.

Let $f=vw$ range over child edges of $v$.  Expanding the aggregate ratio
recursively gives

\[
 c_e(h_e)=
 \frac{Q_v(g,h)}{P_v(g,h)}
 \prod_{f=vw}
 \left(c_f(h_f)
       \left(\frac{y_f}{x_f}\right)^{\mathbf1[h_f\ne0]}
 \right).
\]

Thus

\[
 \frac{Q_v}{P_v}=
 c_e(h_e)
 \prod_{f=vw}
 \left(c_f(h_f)^{-1}
       \left(\frac{x_f}{y_f}\right)^{\mathbf1[h_f\ne0]}
 \right).
\tag{4.4}
\]

At the root, the same formula holds with the parent factor omitted and the
whole-tree aggregate ratio equal to one.  Define

\[
 a_{v,e}=c_e\quad\text{at the child incidence},
 \qquad
 a_{v,f}=c_f^{-1}\frac{x_f}{y_f}\quad\text{at the parent incidence}.
\]

Equation (4.4) becomes (4.1), and on every edge $f=vw$,

\[
 a_{v,f}a_{w,f}=\frac{x_f}{y_f},
\]

which is (4.2).  This also shows directly why a complementary nonzero-sector
anchor is required: the two sides of a cut must both carry total character
$h$.  ∎

### Corollary 4.2 (global freeness)

**PROVED.** If every leaf component of $\mathcal T$ contains a retained
physical block, the full incidence group acts freely on the total domain
$(P,x)$, even if an unreduced local factor has a stabilizer.

#### Proof

If an incidence action fixes $(P,x)$, a marked leaf factor forces its sole
incidence scale to be one.  Fixing the adjacent edge multiplier forces the
scale at the opposite endpoint to be one.  At a marked component all local
scales are one; at an unmarked component of degree at least three the same is
true by Lemma 5.1; at an unmarked bivalent component the relation
$a_1a_2=1$ propagates a known unit scale to the other incidence.  Peel the
finite tree.  All scales are one.  ∎

Consequently the global incidence orbit has dimension $2|E|$.  This does
*not* imply that every separate local action has orbit dimension $\deg v$.

## 5. Stabilizers, slices, and intrinsic coordinates

### Lemma 5.1 (complete local stabilizer classification)

**PROVED.** Let $d=|E(v)|$ and $m=|X_v|$.  On a positive local tensor:

1. if $m\ge1$, the incidence action is free;
2. if $m=0,d\ge3$, the incidence action is free;
3. if $m=0,d=2$, the stabilizer is
   \({(t,t^{-1}):t>0}\);
4. if $m=0,d=1$, all of $\mathbb R_{>0}$ stabilizes the tensor because
   only $h_1=0$ is allowed.

#### Proof

If $m\ge1$, choose one physical block with character $s\ne0$, set
$h_e=s$, and set every other character to zero.  Conservation holds and a
stabilizing action gives $a_e=1$, separately for every $e$.

If $m=0$, for every pair $e\ne f$ choose $h_e=h_f=s\ne0$, all other
characters zero.  A stabilizer obeys $a_ea_f=1$.  For $d\ge3$, the three
relations on any triple imply $a_e=a_f=a_k=1$, and then every remaining
scale is one.  For $d=2$ there is only $a_1a_2=1$.  For $d=1$,
conservation forces $h_1=0$.  ∎

### 5.2 Explicit analytic slices under condition (R)

**PROVED.** Fix a nonzero $s\in G$ and fix each anchor at its base-point
value rather than globally forcing it to one.

If $X_v\ne\varnothing$, choose a retained block $i(v)$ and, for each
incidence $e$, use

\[
 R_e(P_v)=P_v(g_{i(v)}=s,h_e=s,\text{ all other characters }0).
\tag{5.1}
\]

Under the action, $R_e\mapsto a_{v,e}R_e$, so these $d$ anchors give an
identity exponent matrix.

If $X_v=\varnothing$ and $d\ge3$, use pair anchors

\[
 R_{ef}(P_v)=P_v(h_e=h_f=s,\text{ all other }h=0).
\tag{5.2}
\]

Choose the $d$ pairs

\[
 (1,2),(1,3),(2,3),(1,4),\ldots,(1,d).
\]

Their log-exponent matrix has rank $d$.  If $r_{ef}$ is the required
positive correction of the corresponding anchor ratio, the unique positive
normalizer is

\[
\begin{aligned}
 a_1&=\sqrt{r_{12}r_{13}/r_{23}},\\
 a_2&=\sqrt{r_{12}r_{23}/r_{13}},\\
 a_3&=\sqrt{r_{13}r_{23}/r_{12}},\\
 a_k&=r_{1k}/a_1\quad(k\ge4).
\end{aligned}
\tag{5.3}

All anchors are positive, so these formulas are real analytic.  They explicitly
respect zero-sum conservation; no invalid single-nonzero-boundary entry is
used.

### Theorem 5.3 (free reduced projective bridge chart)

**PROVED.** Assume leaf support, arm extension, local regularity, and condition
(R).  In a neighborhood of the chosen positive regular point, contraction is
analytically equivalent to

\[
 \prod_{v\in V(\mathcal T)} \mathcal S_v
 \times \prod_{e\in E(\mathcal T)}J_e,
\tag{5.4}
\]

where $\mathcal S_v$ is either slice (5.1) or (5.2), and each $J_e$ is a
positive open interval of an effective bridge coordinate.  The dimension is

\[
 \dim \Gamma=
 \sum_v\bigl(\dim\widetilde{\mathcal L}_v-\deg v\bigr)+|E|.
\tag{5.5}

#### Proof

Lemma 5.1 and formulas (5.1)--(5.3) give a unique analytic local normalizer
$c_v(P_v)=(c_{v,e})$ sending each factor to its slice.  Define

\[
 j_e=\frac{x_e}{c_{u,e}c_{v,e}}.
\tag{5.6}

If the original representation is changed by any incidence action, its new
normalizer changes inversely; hence (5.6) is unchanged.  Theorem 4.1 says that
these are all fibers, so the sliced local tensors and the $j_e$'s determine
the observed tensor uniquely.

They are also recoverable analytically from the observed tensor.  At each cut
and fixed $h$, choose one assignment on each side with total $h$, factor
the positive rank-one block using a positive anchor, and peel the tree.  After
normalizing the extracted local factors by (5.1) or (5.2), for any valid
nonzero-sector cut anchors $g_A^s,g_B^s$,

\[
 j_e=
 \frac{F_s(g_A^s,g_B^s)}
 {L^{\ast}_{A,e}(g_A^s,s)L^{\ast}_{B,e}(g_B^s,s)}.
\tag{5.7}
\]

Here $L^{\ast}_{A,e},L^{\ast}_{B,e}$ are the normalized aggregate side
factors produced by peeling.  Rank-one identities make (5.7) independent of
the chosen valid anchors.  All operations are multiplication, division by
positive entries, and positive square roots, hence analytic.

The contraction and extraction maps are inverse on the sliced positive germ.
Arm extension permits independent small variations of every slice and every
$j_e$; shrinking preserves the physical inequalities.  Formula (5.5)
follows because $\sum_v\deg v=2|E|$.  ∎

### 5.4 Correct general chart with retained stabilizers

**PROVED.** Without condition (R), Theorem 4.1 still gives the exact global
fiber, but (5.4) must be replaced locally by

\[
 \left(\prod_v\widetilde{\mathcal L}_v/A_v\right)
 \times \left((\mathbb R_{>0})^E/H\right),
\tag{5.8}
\]

where $H=\prod_v\operatorname{Stab}_{A_v}(P_v)$ acts on the edge coordinates.
Under leaf support this $H$-action is free on the edge coordinates.  An empty
bivalent vertex removes one effective edge degree.  Suppressing every maximal
chain of such vertices converts (5.8) into the free reduced chart (5.4).

## 6. Exact adversarial counterexamples

### 6.1 Retained unmarked bivalent component

**EXACTLY COMPUTED / FALSE UNREDUCED PRODUCT FORMULA.** Consider the component
tree

\[
 \text{marked leaf factor}\;--\;v\;--\;\text{marked leaf factor},
\]

where $v$ has no physical block.  Each marked endpoint has one nontrivial
JC orbit coordinate; $v$ has the single coordinate $m=P_v(s,s)$; and the
two edges have multipliers $x_1,x_2$.  The only nontrivial observed orbit is

\[
 W=y_Lx_1mx_2y_R.
\]

The universal logarithmic factor map has rank one.  Its kernel has dimension
four, exactly $2|E|$, so Theorem 4.1 remains correct.  But the local
stabilizer at $v$ has dimension one.  Separate local quotients plus two edge
coordinates have dimension two, one too many.  Only the chain product is
intrinsic.

The physical-scale regression

\[
 (y,z,x)=(1/2,1/2,1/2),\qquad
 (y,z,x)=(3/5,3/5,25/72)
\]

has the same effective product $1/8$ and is not in the old reciprocal orbit.

A simple two-port theta core would realize the same local obstruction.  Its
path lengths are $(1,2,2)$, so it has two triangles and is outside the
intended strong reduced class.  It nevertheless disproves the repair theorem
as an unrestricted tensor-tree statement.

### 6.2 A bridge side without a retained taxon

**EXACTLY COMPUTED / NECESSARY HYPOTHESIS.** Take one bridge.  Put two physical
blocks on one side and none on the other.  The separator is forced to zero in
every global coordinate, so the nonzero separator sectors of the marked
factor are invisible.  The independent design matrix has five domain
coordinates, rank one, and kernel dimension four, while incidence scaling has
dimension only two.  Thus leaf support is necessary for Theorem 4.1.

### 6.3 Shared arm parameter

**EXACTLY COMPUTED / NECESSARY HYPOTHESIS FOR MARGINAL OPENNESS.** If two
ports were artificially forced to share one parameter $t$, then
$(z_1,z_2)=(\kappa_1t,\kappa_2t)$ has Jacobian rank one, not two.  The
standard JC network model avoids this: different bridge edges have independent
multipliers.  The marginal lemma must state that independence explicitly.

## 7. Why the intended reduced level-2 class should satisfy (R)

### Proposition 7.1

**PROVED UNDER THE LOCKED SIMPLE/REDUCED CONVENTION.** In a simple binary
level-2 semi-directed network that has at most one triangle per blob, every
blob has at least three incident bridges.  Hence, after suppressing unlabelled
ordinary degree-two vertices, every unmarked bridge-tree component has degree
at least three.

#### Proof

Every internal vertex has total undirected degree three.  In a cycle blob,
every blob vertex has blob-degree two and therefore one external bridge.  A
simple cycle has at least three vertices, so it has at least three ports.

For a theta blob, let the three internally disjoint pole-to-pole paths have
lengths (\ell_1,\ell_2,\ell_3\).  The poles have blob-degree three; every
internal path vertex has blob-degree two and exactly one external bridge.
Thus the number of ports is

\[
 (\ell_1-1)+(\ell_2-1)+(\ell_3-1)
 =\ell_1+\ell_2+\ell_3-3.
\]

Simplicity permits at most one path of length one.  If there were only two
ports, the only simple nondecreasing length triple would be $(1,2,2)$, which
has two triangle cycles.  It is excluded by the at-most-one-triangle property
(and, in the intended theory, by tree-child rootability).  Therefore every
theta blob has at least three ports.  The minimum cases include $(1,2,3)$
and $(2,2,2)$.

Finally, an ordinary unlabelled degree-two component is removed by
homeomorphism reduction; a leaf component carries a labelled block; and an
ordinary internal binary tree component has degree three.  This is condition
(R).  ∎

The manuscript's core argument supports the graph calculation at
[`source/paper/sections/06_support.tex:15`](../../source/paper/sections/06_support.tex)
and its multi-triangle exclusion at
[`source/paper/sections/06_support.tex:52`](../../source/paper/sections/06_support.tex).

### Convention warning

**UNRESOLVED.** The phrase “standard parallel root artifact” in
[`source/paper/sections/02_definitions.tex:7`](../../source/paper/sections/02_definitions.tex)
is not a formal rewrite rule, and Gate D separately lists 2-sub-blob and LSA
conventions as open.  Proposition 7.1 addresses actual bridge-tree blob
vertices.  A 2-sub-blob inside a larger blob is not an edge-cut component and
must either be included in the local atlas or removed by a separately locked
standard suppression rule.  This report does not silently identify those two
conventions.

## 8. Marginal localization without projective peeling

### Lemma 8.1 (one-taxon-per-branch reduction)

**PROVED.** Let $B$ be a focal component with incident bridges
$e_1,\ldots,e_d$.  Assume deleting $B$ leaves $d$ components, each
containing a labelled taxon.  Choose one taxon $t_i$ in the $i$-th
component and marginalize every other taxon.  Then the resulting Fourier
tensor has the form

\[
 \widehat p_B(g_1,\ldots,g_d)=
 P_B(g_1,\ldots,g_d)
 \prod_{i=1}^d z_i^{\mathbf1[g_i\ne0]},
 \qquad \bigoplus_i g_i=0,
\tag{8.1}
\]

where $P_B$ is the focal local tensor and

\[
 z_i=x_{e_i}\kappa_i,
 \qquad 0<z_i<1,
 \qquad 0<\kappa_i\le1.
\tag{8.2}
\]

The $x_{e_i}$'s are the independent adjacent bridge multipliers.  The
outside factor is

\[
 \kappa_i=
 \sum_{\sigma_i}w_{\sigma_i}
 \prod_{a\in\operatorname{path}_{\sigma_i}(B,t_i)}x_a.
\tag{8.3}
\]

#### Proof

Fix a displayed-tree switching.  After all but $t_i$ are marginalized in
the $i$-th branch, every off-path edge has zero descendant character.  The
branch contribution is therefore the product of the JC multipliers on the
unique boundary-to-$t_i$ path when $g_i\ne0$, and one when $g_i=0$.
Inheritance choices in disjoint bridge components are independent, so summing
over outside switchings factors by branch and gives (8.3).  Every summand is
positive, the weights are positive and sum to one, and every nonempty path
product is less than one.  A zero-length outside path gives
$\kappa_i=1$, but the adjacent bridge still makes $z_i<1$.

If the global root lies in one outside branch, stationarity and reversibility
give the same undirected two-state-endpoint Fourier channel; no orientation of
the ordinary bridge is used.  Reticulation choices inside $B$ are independent
of outside choices and remain entirely in $P_B$.  This proves (8.1).  ∎

### Lemma 8.2 (marginal openness)

**PROVED.** Fix all outside parameters except the adjacent bridge multipliers.
The map

\[
 (x_{e_1},\ldots,x_{e_d})\longmapsto(z_1,\ldots,z_d)
\]

has Jacobian

\[
 \operatorname{diag}(\kappa_1,\ldots,\kappa_d)
\]

and determinant $\prod_i\kappa_i>0$.  Therefore local blob parameters and
effective arm parameters range over an open parameter neighborhood
independently.  At any regular point of the arm-extended local
parameterization, its image contains a relative-open local model germ.

#### Proof

Equation (8.2) gives the diagonal Jacobian.  Let $O$ be a nonempty
source-relative open subset of the global model.  Its preimage under the
continuous source parameterization is open.  The critical locus of the local
arm-extended parameterization is a proper algebraic set, so this preimage
meets its complement.  Take a small product box at such a point and freeze the
outside parameters.  The inverse-function theorem first gives an open box in
the local-plus-arm parameter space; the constant-rank theorem then gives a
relative-open subset of the local source image.  ∎

### Theorem 8.3 (directed marginal localization)

**PROVED.** Suppose $N\preceq_{JC}N'$ on a source-relative open regular set
and cut preservation has identified the same labelled bridge tree.  Fix a
focal bridge-tree component and one representative taxon in every incident
leaf block.  Then a relative-open subset of the source's arm-extended local
marginal model is contained in the corresponding target local marginal model.

If standard rooting or marginal suppression presents finitely many target
incoming-role/weak-completion models, the conclusion is that at least one
member of that finite union contains a source-full-dimensional semialgebraic
subset.  If a fixed admissible target rooting is used, the role and completion
are fixed and no union is needed.

#### Proof

By Lemma 8.2, marginalizing the source containment set contains a
relative-open local source germ.  Every point in that marginal set is also the
same marginal of a target distribution.  Lemma 8.1 applied to the target puts
it in the corresponding target arm-extended model.  If finitely many target
roles are allowed, a finite semialgebraic union covers the source-open local
set; dimension of a finite union is the maximum of the dimensions, so one
member has source-full-dimensional intersection.  No target regularity,
target preimage selection, bridge quotient, or physical bridge reconstruction
is used.  ∎

### What this proves about compensation

**PROVED:** Changes in outside blobs cannot compensate for a local separator
on any selected marginal: outside networks alter only the positive arm scalars
$z_i$, and the adjacent bridge multipliers make those scalars locally
independent on the source side.

**UNRESOLVED:** To turn this into the flagship theorem, every local separator
used by the atlas must be verified to survive arbitrary positive arm scaling,
and the weak-completion atlas must be complete.  Those are Gates A and S, not
bridge-factorization facts.

## 9. Direct-marginal reconstruction assessment

### Proposition 9.1 (conditional reconstruction without peeling)

**PROVED, CONDITIONAL ON THE STATED ATLAS HYPOTHESES.** Assume:

1. all cut splits and the labelled homeomorphism-reduced bridge tree are known;
2. there is no retained unmarked degree-two component;
3. the bounded local atlas includes the ordinary three-valent tree factor,
   every cycle/theta factor, both directions of tree-versus-network and
   cycle-versus-theta containment, all root/incoming roles, and all weak target
   completions;
4. every atlas zero/sign decision is invariant under independent positive arm
   scaling; and
5. the support-plus-one/two consistency theorem is valid.

Then the standard semi-directed local decorations and all ordered port words
can be reconstructed from exact leaf marginals, without projective tensor
peeling.

#### Algorithm

For every internal vertex $v$ of the recovered bridge tree:

1. choose one representative taxon from each incident leaf block;
2. evaluate the local atlas on their exact marginal;
3. if the valence is three, include the ordinary tree star among the candidate
   factors; if the valence exceeds three, binary ordinary vertices are already
   excluded and $v$ must be a blob;
4. for a large-valence blob, enumerate bounded port subsets until a rigid
   support is found;
5. evaluate every support-plus-one marginal to locate each remaining port's
   directed segment;
6. evaluate support-plus-two marginals to recover the order of every pair on
   one segment; and
7. canonicalize the resulting labelled cycle/theta word modulo the atlas's
   verified triangle move.

Lemma 8.1 shows that arbitrary outside branches contribute only positive arm
scalars.  Hypothesis 4 makes every atlas decision independent of which taxon
was chosen in a branch.  The support theorem makes the pairwise orders globally
consistent.  This proves the conditional result.

### Missing and fatal cases

1. **Degree-two components / 2-sub-blobs.** A two-boundary JC tensor has only
   one nontrivial effective scalar.  It is indistinguishable from an ordinary
   edge at this interface.  If such an object is retained as a topology, this
   reconstruction cannot identify it, and the naive projective product also
   fails.  It must be excluded structurally or suppressed by the locked
   standard equivalence.

2. **Blob versus ordinary node at valence three.** Cut splits alone do not mark
   a degree-three bridge-tree vertex as a tree vertex or a blob.  A
   cycle/theta-only atlas is insufficient.  The atlas must include exact
   tree-versus-three-port-cycle/theta separation in both one-sided directions.
   This review has not independently certified that table.

3. **Root roles.** The exact marginal is root-free under JC, but a finite atlas
   may encode a distinguished incoming boundary.  Either root relocation must
   identify the fixed role, or all admissible roles must be included and the
   finite-union argument in Theorem 8.3 used.

4. **Weak completions.** When a bounded probe omits ports, the target
   restriction can be weak even though the full target is strong.  Dummy sink
   children and repair ports must remain in the target completion universe.

5. **Genericity across representative choices.** Strict sign identities valid
   on the full open arm cube are safe for every representative.  A merely
   generic nonzero invariant can vanish for a special outside effective arm;
   reconstruction must include those pullbacks in its stated finite
   exceptional algebraic locus.

Subject to these cases, direct marginal reconstruction is sufficient and is
cleaner than attempting to recover physical bridge parameters.

## 10. Independent verifier

The independent verifier is

[`repair/independent/bridge/verify_bridge_gate.py`](../independent/bridge/verify_bridge_gate.py).

It imports none of the project's Fourier, graph, atlas, invariant, or rank
code.  Run:

```bash
python3 repair/independent/bridge/verify_bridge_gate.py
```

It performs the following exact checks:

- constructs all six automorphisms of $G$;
- computes the complete local stabilizer ranks for zero, one, and two physical
  blocks and degrees one through six;
- verifies the physical and pair-anchor exponent matrices exactly;
- checks 793 labelled leaf-supported trees through five vertices, with all
  choices of marked internal components, using integer kernel containments and
  a finite-field nonzero-minor lower bound;
- certifies the retained two-port overcount and the inaccessible-side extra
  kernel;
- enumerates nondecreasing theta path triples, including equal lengths such as
  $(2,2,2)$, under the simple/one-triangle filters;
- checks the positive pair-anchor inverse with exact rational arithmetic; and
- checks the diagonal marginal-arm Jacobian, a two-route outside-network
  multiplier, and the shared-arm rank-one failure.

**IMPORTANT:** the 793 finite kernel tests are adversarial illustrations and
regressions only.  They do **not** prove Theorem 4.1 for arbitrary trees.  The
general proof is the rank-one aggregate-factor argument in Section 4.

## 11. Release recommendation

1. **PROVED:** Theorem 4.1, Lemma 5.1, Theorem 5.3 under condition (R), and
   Lemmas 8.1--8.2 may be used as proof candidates after independent human or
   reviewer-agent checking.
2. **FALSE:** Do not use the unqualified product theorem currently in the
   repair source, and do not use the reciprocal-only theorem in the manuscript.
3. **PREFERRED NECESSITY ROUTE:** Use Theorem 8.3 for localizing one-sided
   containment.  It is shorter, avoids target regularity and bridge gauges,
   and directly matches bounded local atlases.
4. **UNRESOLVED:** Do not close Gate B for the manuscript class until Gate D
   formally rules out or suppresses every retained two-port component and
   locks leaf support after LSA trimming.
5. **UNRESOLVED:** Do not promote the global theorem until the tree-versus-blob
   atlas directions, arm-degree/sign audit, weak completions, and arbitrary-
   subdivision consistency are independently complete.
