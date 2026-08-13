# Proof-first global dependency audit

Date: 2026-08-12

Scope: the global implication for Outcome P only

Method: proof audit; no topology census, symbolic atlas, or search was run

## Verdict

**CONDITIONAL GLOBAL CLOSURE, WITH ONE SYNTHESIS REPAIR AND ONE STRUCTURAL
WORDING CLARIFICATION.**

Relative to the independently verified convention, cut, bridge, root, and
ordinary-triangle results, Outcome P reduces to one genuinely local theorem.
There is no remaining nonlocal compensation, bridge-gauge, or one-sided-cut
lemma to prove.

The minimal unproved premise is the following full-factor statement.

### Local blob-containment lemma `L_blob`

Let `H` and `H'` be full labelled nontrivial blob factors on the same set of
physical boundary blocks.  Assume that each is induced by a locked
reticulation-preserving `sd_0` standard semi-directed `S_TC` level-2 topology.
Choose admissible incoming presentations of `H` and `H'` **independently**.
Let `PM_H` and `PM_H'` be their open JC boundary-tensor images modulo the
positive port-incidence action

```text
P(g) -> P(g) product_i a_i^[g_i != 0].
```

If a source-relative full-dimensional regular germ of `PM_H` is contained in
`PM_H'`, then the complete labelled semi-directed ported factors `H,H'` are
isomorphic or differ by ordinary triangle redirection `T`.

This statement quantifies over arbitrary finite subdivision words and every
ordered cross-core direction.  It is stochastic on the strict open JC domain;
equality of Zariski closures is not a substitute.  It does not require a
continuous choice of target parameters and does not require the two incoming
presentations to use the same physical boundary.

`L_blob` is the only unproved mathematical premise needed for the topology
classification.  A bounded-support atlas is one possible proof of `L_blob`,
but it is not part of the global implication and no census conclusion is
assumed here.

## Required correction to the existing global draft

The sentence in `reviews/final_theorem_logic/PROMOTION_PROOF.md` saying that
ordinary tree components are fixed by the bridge tree is too strong as
written.  Cut splits recover the **unmarked** reduced component tree.  A
degree-three node can a priori be either an ordinary trivalent median or a
three-port nontrivial blob.

This does not create a new unresolved gate.  A theta with `d` boundary ports
has `d+2` mixed-graph vertices.  Exactly two are reticulations, leaving `d`
nonreticulate vertices.  Its four retained incoming reticulation arrowheads
must have four distinct tails under the no-omnian criterion, so `d>=4`.
Hence a full nontrivial factor with exactly three boundaries can only be the
three-sunlet.  With

```text
a=P(1,1,0),  b=P(1,0,1),  c=P(0,1,1),  t=P(1,2,3),
F=abc-t^2,
```

the ordinary median has `F=0`, while the independently regenerated
three-sunlet pullback is

```text
p0^2 p1 p2 p3^2 p4 p5^2 p6^2 p7 (1-p2)^2 (1-p7),
```

which is strictly positive throughout the open JC cube.
Moreover `F` is arm-multihomogeneous: under positive port scalings it is
multiplied by `(s_1 s_2 s_3)^2`.  Consequently source-relative containment in
either direction cannot replace an ordinary degree-three node by a
nontrivial three-port blob.  Binary ordinary unmarked components have degree
three; nodes of larger degree are automatically nontrivial.

The broader endpoint dichotomy also uses `G=a-bc` on an `F=0` branch for the
two-active cut proof.  `G` is **not** invariant under unrestricted projective
port scaling and is not used for this component-type marker.

The final global theorem should therefore say that the labelled **decorated**
component trees agree: corresponding nodes are both ordinary or both
nontrivial, and corresponding nontrivial factors are isomorphic or
`T`-related.

### Upstream `K4-e` wording clarification

The automatic at-most-one-triangle conclusion remains proved.  The sentence
in `docs/GENERATOR_AND_SUPPORT_THEOREM.md` counts tails in the final mixed
graph, after root suppression; in that language the root is correctly absent
and the no-omnian argument has only two nonreticulate tails.  If the argument
is restated at the rooted-presentation level, the inserted root must be
included: the two ordinary internal vertices and the root provide at most
three tree-child-compatible tails for four incoming reticulation arcs.  Both
formulations prove impossibility, and the exact rooting census independently
finds no tree-child rooting.  The manuscript should keep the level of the
count explicit rather than moving between the two formulations silently.

## Proof-level reduction

Assume `L_blob`.

### 1. One-sided containment forces the same cuts

Let `U` witness `N preceq_JC N'`.  The verified pointwise cut theorem says
that, at every strict open JC point, a bipartition is a cut split exactly when
its four Fourier character blocks have total flattening rank at most four.

If a source cut were a target noncut, a common point of `U` would have rank at
most four as a source distribution and at least five as a target
distribution.  Conversely, if a target cut were a source noncut, the target
rank equations hold on `U`, while the source pointwise theorem gives rank at
least five there.  This second implication does not reverse `preceq`; it
pulls the target cut equation back to the shared source-open set.

Thus the cut sets agree.  Their compatible labelled split system determines
the same reduced unmarked bridge-component tree.  Leaf support and the
exclusion of unmarked bivalent components are part of the verified bridge
package.

### 2. Ordinary and nontrivial component types agree

Apply the homogeneous three-sunlet invariant `F` above at every degree-three
component.  It excludes ordinary-to-blob and blob-to-ordinary source-relative
containment in both directions.  Components of degree greater than three
cannot be ordinary in a binary network.  Therefore the common unmarked tree
has the same ordinary/nontrivial decoration in both networks.

### 3. The bridge quotient localizes containment exactly

On the common leaf-supported component tree, the verified positive
factorization fiber is precisely

```text
P_u -> a_(u,e) P_u,
P_v -> a_(v,e) P_v,
x_e -> x_e/(a_(u,e) a_(v,e)).
```

The endpoint actions have explicit positive analytic slices and the retained
tree has no stabilizing unmarked bivalent component.  The intrinsic
coordinates are projective local tensors and normalized effective bridge
scales; they are not physical edge multipliers.

Pull a source-relative common germ into the analytic product chart and
shrink to a product box.  Vary one focal projective source factor while
holding the other source coordinates fixed.  Projective peeling is an
intrinsic function of the observed distribution.  Hence every target
realization of each point has the same extracted focal orbit, so the focal
source box lies in the corresponding target projective local image.  No
target preimage is selected continuously, and a distant factor cannot alter
the extracted orbit.  If finitely many target incoming presentations are
used, semialgebraic dimension gives one member containing a source-open
subgerm; it need not contain the whole source germ.

### 4. Root factors introduce no extra relation

The verified root reduction represents each root-containing factor by an
incoming-port factor at some real boundary, preserving the projective JC
germ and the exact `sd_0` mixed graph.  The source and target incoming
boundaries may be different.  This is why `L_blob` permits independently
chosen incoming presentations.

### 5. Apply the only missing local lemma

For every corresponding nontrivial component, Steps 3--4 give precisely the
hypothesis of `L_blob`.  Therefore every corresponding pair is labelled
isomorphic or ordinary-`T`-related.  Together with Step 2, this proves the
necessary direction

```text
N preceq_JC N'
  =>
same decorated labelled component tree and every blob pair is iso/T.
```

### 6. Converse gluing is already closed

For an isomorphic local pair, use the same projective germ.  For a `T` pair,
use the independently verified port-labelled common full-dimensional regular
projective germ.  After shrinking all local germs, choose for every bridge a
common effective scale

```text
0 < z_e < min_k a_(u,e)^k a_(v,e)^k,
```

and set `x_e^k=z_e/(a_(u,e)^k a_(v,e)^k)`.  Both physical multipliers then
remain in `(0,1)`.  The component graph is a tree, so the bridge choices are
independent and there is no scaling holonomy.  Analytic extraction is an
inverse on the sliced product, so the glued common germ has full global
dimension and contains regular points for both models.

Thus the right-hand condition implies `bowtie_JC`, and hence `preceq_JC` in
both directions.

### 7. Global conclusion under `L_blob`

The preceding steps prove

```text
N preceq_JC N'
iff
the decorated labelled component trees agree and every corresponding
nontrivial factor is labelled-isomorphic or ordinary-T-related.
```

The right-hand side is symmetric.  Therefore no proper one-sided generic
containment exists, and it also classifies symmetric full-dimensional regular
overlap.

For a fixed taxon set there are finitely many locked standard-strong binary
level-2 topologies: choose one tree-child rooting, use `r<=n-1`, and apply the
binary degree count.  For every non-`T` alternative, absence of
source-relative interior makes the semialgebraic intersection lower
dimensional.  Its Zariski closure inside the irreducible source variety is
proper.  A finite union, enlarged by singular and critical-value loci, is a
proper algebraic exceptional set outside which the canonical topology
**modulo `T`** is determined.

## What the reduction does not prove

1. It does not prove `L_blob`; that is the remaining landmark local theorem.
2. It does not recover physical bridge multipliers.
3. It does not claim equality of complete stochastic images for `T`.
4. It does not imply that every `T` orientation realizes one fixed generic
   distribution.  A reconstruction algorithm may return the canonical
   `T`-quotient class.  Listing the orientations realizing a particular
   distribution requires separate finite semialgebraic membership tests.
5. A nonconstructive proof of `L_blob` gives the classification but not the
   advertised bounded-invariant implementation.  A publishable structural
   reconstruction algorithm needs the proof of `L_blob` to be effective, or
   needs a separate exact local membership procedure.  This is a local
   effectivity requirement, not a nonlocal theorem gap.
6. A triangle-bearing theta is not a bridge sum of a three-sunlet and a
   triangle-free factor: its third path reconnects the same two poles.  The
   verified three-port `T` tensor gives the converse move after contraction,
   but cannot replace the necessity part of `L_blob`.

## Optional finite reduction, without assuming a census

The verified support/submersion/coherence arguments provide a proof strategy
for `L_blob` but are not used as evidence that it is true.  For independently
chosen minimal supports `Q_s,Q_t`, retain the exact union anchor

```text
A = Q_s union Q_t.
```

Each support has at most five tensor ports (incoming plus outgoing), so a
proof independent of stored census overlaps may use the safe bounds
`|A|<=10` and `|A union {p,q}|<=12`.  It is enough to prove, directly from the
graph-derived tensors, that every directed containment on the restoration
anchors and their one-/two-port extensions is isomorphism or `T`.  The
verified marginal-submersion and probe-coherence lemmas then promote that
bounded statement to arbitrary words.  The smaller attained ten-port bound
reported by the frozen certificate is not used in this proof-first audit.

## Missing nonlocal lemmas

**None found.**  In particular, the following are already independently
closed on the locked class:

- both directions of cut preservation under one-sided containment;
- equality of the reduced labelled unmarked component tree;
- the complete incidence-scaling kernel and positive analytic slices;
- intrinsic projective extraction without continuous target choices;
- exclusion of cross-blob compensation;
- root reduction with independently chosen incoming boundaries; and
- simultaneous gluing of finitely many local `T` germs.

The ordinary-versus-blob component marker was omitted from the synthesis, but
its required homogeneous three-sunlet `F` separation is already verified by
`independent/counterexample_search/three_leaf_separator_certificate.json`.
After it is inserted, every unresolved implication is contained in `L_blob`.

The clarified `K4-e` tail count is likewise backed by the existing exact
rooting result and is not an additional nonlocal lemma.

## Release recommendation

Do not promote Outcome P yet.  Replace the global proof ledger by the chain
above, correct the ordinary-component sentence, and focus all remaining
mathematical work on a proof-first proof of `L_blob`.  No further global
census or bridge computation is justified.
