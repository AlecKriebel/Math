# Independent proof-logic audit

Checkpoint: 2026-08-26T18:02:08-0700
Completion estimate for the assigned non-computational audit: **100%**.

This audit did not run producer or verifier code and did not accept stored
`PASS` fields.  It addresses the handwritten theorem chain only.  All paths
below are relative to `package_copy/proof_package/`.

## Exact scope restated

The principal theorem concerns two networks on the same finite labelled leaf
set which are binary, level at most two, standard semi-directed under the
single root-suppression convention, and strongly tree-child (at least one
admissible rooting exists and every admissible rooting is tree-child).  State
labels `C,G,T` are fixed.  Every inheritance probability lies in `(0,1)`, and
every edge has positive nontrivial Fourier spectrum in

`D_{3,+}={(c,g,t) in (0,1)^3: 1+c-g-t>0, 1-c+g-t>0, 1-c-g+t>0}`.

Directed containment is source-relative: it requires a connected open
neighborhood of a source point where the source Jacobian has its maximum
physical rank and a physical real-analytic target-parameter section on that
source neighborhood.  The asserted classification is that this relation is
equivalent to equality of the labelled component tree plus labelled
isomorphism of every complete nontriangle factor, allowing only coherent
redirection of an ordinary three-cycle, and equivalent to a common germ which
is regular and full-dimensional in both images and has physical sections.
Complete stochastic images and individual numerical parameters are not
claimed equal.

For each fixed topology, generic identifiability and exact reconstruction are
only outside a topology-dependent proper complex Zariski-closed exceptional
set.  Reconstruction assumes exact-real field/sign operations and real-closed-
field quantifier elimination and makes no complexity, conditioning, sampling,
or finite-data claim.

The continuous-time version replaces the edge domain by
`D_{3,CT}={(c,g,t): c>gt, g>ct, t>cg}` (equivalently strictly positive
symmetric K3P rates); no boundary point is included.  The ordinary-triangle
ambiguity is a common smooth rank-14 germ in the irreducible quartic
hypersurface `H14`, not an ambient-open rank-15 germ.  The weak-class sharpness
claim is existential: for every `n>=3` it constructs two weakly but not
strongly tree-child, nonisomorphic, non-triangle-equivalent networks whose
strict-CT images share a `6n-3` dimensional regular germ.  It does not classify
all weakly tree-child networks.

## Severity-ranked findings

### 1. Major, load-bearing but locally repairable: component decoration is not recovered by cut sets

The cut-transfer theorem proves equality of bridge splits and then states
“Hence the labelled reduced trees of blobs agree”
(`manuscript/sections/04_physical_topology.tex:204-212`).  Equality of edge
splits reconstructs the abstract reduced component-incidence tree, but it does
not distinguish an ordinary trivalent component from a three-boundary cycle
blob: a three-leaf tree and an ordinary three-sunlet have exactly the same
three pendant cut splits.

The global necessity proof immediately invokes the complete local factor
classification for “every corresponding factor”
(`manuscript/sections/10_global_classification.tex:5-16`), while that theorem is
explicitly stated only for complete ported **cycle/theta** factors
(`manuscript/sections/09_restoration_words.tex:103-116`).  Thus the written
proof omits the ordinary-vertex versus cycle-blob case and the inference at
`04_physical_topology.tex:212` is false if “tree of blobs” includes its
ordinary/blob decoration.

This is not presently a counterexample to the theorem because the article
already proves exactly the missing separator: the six-circuit sum of squares
is zero on a three-leaf tree and strictly positive at every strict ordinary
sunlet (`manuscript/sections/05_three_leaf_geometry.tex:53-99`).  Its circuits
are multihomogeneous in each labelled boundary, so zero versus nonzero survives
the positive incidence quotient.  The strong-repair table also shows that a
strong theta has at least four physical boundaries
(`manuscript/sections/08_primitive_bounded.tex:45-73`); hence the only
degree-three blob alternative is a cycle, which serially compresses to the
displayed sunlet map.  The repair is to insert this decoration-separation step
after abstract cut-tree recovery and bridge-orbit extraction, before invoking
the nontrivial-factor theorem.  The analogous companion proof contains this
step explicitly at
`input_frozen/referenced_chat_manuscripts/k2p_level2_source.tex:518-522`.

The omission affects the necessity implication of the main classification,
and through it the genericity theorem.  It is conceptually small but logically
load-bearing.

### 2. Moderate, repairable proof-detail gap: finite-cover localization does not spell out the claimed analytic local section

The bridge product lemma asserts a physical local product chart
(`manuscript/sections/06_bridge_fibre.tex:87-103`).  The localization proof then
fixes all but one source factor, covers its focal box by finitely many target
realization sets, and invokes the finite-cover lemma
(`manuscript/sections/07_marginal_localization.tex:68-91`).  Finite-cover
dimension alone proves that one target realization **set** contains a relative
open source subgerm; by itself it does not prove the stronger statement that
this subgerm is regular for the focal source map and carries a physical
real-analytic target-parameter section, as required by the local directed
relation defined at `manuscript/sections/06_bridge_fibre.tex:105-110`.

The missing argument is standard and appears available from the stated
hypotheses: intersect the source-open box with a nonzero focal maximal-minor
locus; restrict the given global analytic target section and the analytic
marginal descriptor; or, equivalently, stratify the fixed-type target incidence
correspondence and take a full-rank projection stratum, exactly as is done
later for genericity at
`manuscript/sections/11_genericity_reconstruction.tex:62-81`.  The polynomial
and rank obstructions used for necessity actually need only open set inclusion,
so I found no resulting counterexample, but the proposition as stated claims
more than its displayed proof establishes.

### 3. Minor/auditability, not a discovered mathematical error: directed primitive completeness is outsourced from the article

The undirected excess-degree argument correctly yields a cycle for one
reticulation and a theta for two.  But the assertion that the directed event
placements are exactly `theta_0,...,theta_3` is compressed to two sentences and
“replayed from the frozen topology package”
(`manuscript/sections/08_primitive_bounded.tex:11-38`).  The supplement itself
points the reader to frozen JC/K2P manuscripts rather than reproducing the
case split (`supplement/reader_supplement.tex:87-93`).  The supplied frozen JC
source does contain a coherent pole/source/sink case analysis at
`input_frozen/referenced_chat_manuscripts/jc_level2_source.tex:472-520` and the
cycle/theta derivation at `:527-570`; I found no omitted directed case in that
argument.  This is therefore a presentation/dependency-boundary issue, not an
identified theorem defect, but the K3P article should cite or reproduce that
load-bearing lemma directly.

### 4. Minor precision: root movement is an analytic physical reparameterization, not literal equality of polynomial maps

`manuscript/sections/04_physical_topology.tex:38-51` says the K3P map is
“unchanged” under moving to any admissible rooting.  What the proof actually
uses is reversibility plus merging/splitting the root edge, hence equality of
physical images and local germs after an analytic physical reparameterization.
The strict subdivision lemma supplies the needed local sections.  This is
sufficient for all later uses, but the statement should distinguish literal
parameter-map equality from rooting-invariant image germs.

## Targeted transitions for which no logical defect was found

- **Fixed semi-directed/strong convention.**  The no-omnian criterion is
  correct in its binary setting; the article proof is compressed, while the
  frozen source gives the admissibility/LSA argument.  Root changes preserve
  displayed unrooted trees and strict physical germs by reversibility and
  subdivision.
- **Balanced noncut compression and directed cut transfer.**  The colored-hull
  dichotomy uses only the target tree.  A crossing target bridge becomes a
  crossing source bridge via the already proved inclusion, contradicting tree
  split compatibility; the remaining central vertex has at least four
  branches and is a blob.  Two-boundary side blobs compress to strict principal
  K3P kernels because convex mixtures preserve positive transition entries and
  positive eigenvalues.  The final four-leaf rank contradiction is pointwise
  and does not assume target regularity or a common bridge tree
  (`manuscript/sections/04_physical_topology.tex:204-280`).
- **Bridge fibre/freeness.**  Positive rank-one factorization separately in the
  fixed `C,G,T` blocks gives precisely one scale per incidence and sector.
  Leaf peeling is complete on a tree.  Marked one-character anchors and the
  unmarked pair-anchor matrix with leading determinant `-2` kill stabilizers;
  positivity removes sign branches.  The independent-sector endpoint
  variations in the product chart follow by openness around two isotropic
  factors, although that sentence is terse
  (`manuscript/sections/06_bridge_fibre.tex:20-103`).
- **Marginal descriptors.**  For the restrictions actually used, visible edge
  signatures partition edge parameters into independent coordinatewise product
  classes.  A reticulation is dropped only when its two retained switching
  contributions are literally identical, so their weights sum to one;
  otherwise its parameter or complement is retained
  (`manuscript/sections/07_marginal_localization.tex:27-53`).
- **`H14` and contextual gluing.**  Linear-in-one-variable irreducibility is
  valid because the binomial coefficient is irreducible and does not divide
  the remainder.  Rank 14 at a smooth point gives relative submersions and
  physical sections.  For context, the common open subset of irreducible
  `H14` is dense, so the maximal rank of the single contraction `Psi` on that
  subset equals its global generic rank; this density sentence should be made
  explicit at `manuscript/sections/05_three_leaf_geometry.tex:189-211` but the
  argument is sound.  The capped bridge choice in
  `manuscript/sections/10_global_classification.tex:22-70` correctly keeps both
  effective and actual spectra in `D_{3,CT}` and leaves three independent
  effective directions per bridge.
- **Genericity/real-to-complex passage.**  The total rank-drop image has
  dimension at most `d_N-1`; a full-dimensional target incidence projection
  gives an analytic right inverse and hence the forbidden source-relative
  section.  For a real semialgebraic set, its complex vanishing ideal is the
  complexification of its real vanishing ideal, and the finite faithfully flat
  extension preserves Krull dimension.  I found no quantifier shift at
  `manuscript/sections/11_genericity_reconstruction.tex:3-108`.
- **Exact reconstruction.**  Under the deliberately strong exact-real/QE
  oracle convention, brute-force finite topology enumeration and final
  semialgebraic feasibility already guarantee termination; the earlier
  certificate-guided tests are accelerants.  No practical or parameter-
  identifiability claim is made.
- **All-`n` cherry extension.**  The observables satisfy
  `R_h=u_h/v_h`, `P_h=u_h v_h`; their sector Jacobian determinant is `2u_h/v_h`,
  hence the six-variable determinant is the stated
  `8 u_Cu_Gu_T/(v_Cv_Gv_T)`.  The positive inverse recovers the six new spectra,
  and dividing a coordinate with one cherry leaf assigned zero recovers every
  old tensor coordinate.  Thus no previously hidden old direction appears and
  the image dimension increases by exactly six.  Cherry contraction preserves
  nonisomorphism/non-triangle-equivalence and the old non-tree-child rooting
  (`manuscript/sections/13_sharpness.tex:123-190`).

## Verdict contribution

For the handwritten/non-computational logic alone: **major revision**, not
“invalid.”  Confidence: **0.84**.  The main theorem has a real omitted case in
the necessity chain (Finding 1), but the package already contains a strong
pointwise lemma that appears to repair it without changing the theorem or its
hypotheses.  Finding 2 should also be expanded so the analytic-section
quantifier is explicit.  Conditional on those repairs and on separate positive
audits of the finite and interval certificates, I found no counterexample to
the stated theorem.

## Unexecuted/unresolved checks

- No producer, verifier, mutation, or interval code was run, by assignment.
- The 204-direction algebra, fourteen-orbit atlas, restoration/probe ledgers,
  Krawczyk box, and topology censuses were not independently recomputed here.
- No literature/novelty audit was performed.
- The phrase “complete fibre” was checked mathematically on the stated positive
  conservation-supported locus, but not against every serialized component
  convention in producer code.
