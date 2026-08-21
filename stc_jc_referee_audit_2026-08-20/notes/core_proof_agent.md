# Core proof audit: strong-class theorem, cuts, bridge fibre, localization, and genericity

Date: 2026-08-20 (America/Los_Angeles)

Scope of this audit: complete mathematical reading of the 31-page manuscript and
the 7-page supplement, followed by an adversarial reconstruction of the main
theorem and its proof dependencies. I treated all scripts and stored outputs as
claims to be checked, not as proofs. I did not contact anyone.

## Bottom line

I found no mathematical counterexample to the strong-class classification. The
human parts of the cut, incidence-fibre, projective-localization, finite-cover,
genericity, triangle-context, and physical-gluing arguments are basically
sound. I independently checked the algebra in the difficult two-active-endpoint
contradiction and performed a strictly larger finite census than the archived
cut verifier.

There is, however, one material load-bearing certificate-coverage defect:
the archived two-colour switching compiler does **not** enumerate every
at-most-eight-port compressed word that the manuscript says it enumerates.
Across the exact full eight-port universe, it omits 393,400 valid standard-strong
colourings. My extended census found no survivor in any omitted case, so this is
not a counterexample and does not change the mathematical conclusion. But the
published proof archive, as packaged, does not establish that handoff without
adding the expanded census or a missing reduction lemma. There is also a real
but repairable central-arm-normalization omission in the written endpoint
argument: the verifier checks the pre-normalized auxiliary inequality, while
the proof uses the normalized one. Continuity at the open-cube boundary repairs
it, and an all-nine-record check confirms the needed inequality.

My recommendation on the core proof alone is: the theorem appears valid, but
the submission needs revision. If the journal treats a false exhaustiveness
claim in a load-bearing proof certificate as substantive, this warrants major
revision until the extended compiler/certificate is incorporated. If the
expanded census is added and authenticated, the remaining core issues are
minor exposition repairs.

## Exact theorem reconstructed

### Object class and conventions

- A rooted presentation is a finite leaf-labelled binary DAG, without parallel
  arcs, whose root has bidegree `(0,2)`, ordinary internal vertices `(1,2)`,
  reticulations `(2,1)`, and leaves `(1,0)`. Every vertex is root-reachable, and
  the root is the lowest stable ancestor. See manuscript Definition 2.1,
  PDF pp. 3--4, `work/source/paper/main.tex:235-262`.
- The fixed semi-directed reduction `sd_0` marks precisely arcs entering
  reticulations, undirects all others, deletes the binary root once, and joins
  its two incident edges once. The resulting mixed graph must already be
  simple and binary; there is no later cleanup in the definition of an
  admissible rooting. See Definition 2.1, PDF pp. 3--4,
  `main.tex:246-261`.
- `S_TC` consists of standard mixed graphs with at least one admissible rooting
  and with **every** admissible rooting tree-child. Lemma 2.2 identifies this
  with the incidence condition that every tail of a retained reticulation edge
  has two undirected incidences. See PDF pp. 4--5,
  `main.tex:280-340`.
- A blob is a nontrivial biconnected block of the underlying simple graph. The
  level is the maximum number of reticulations in a blob. Contracting blobs and
  retaining ordinary trivalent pieces gives the labelled reduced bridge tree.
  See PDF p. 5, `main.tex:342-349`.
- Ordinary triangle redirection changes only the reticulate vertex and the two
  internal arrowheads of one triangle, keeping all labels, underlying edges,
  pendant placements, and outside arrowheads fixed. Both endpoints must remain
  in the theorem class. See Definition 2.3, PDF p. 5,
  `main.tex:351-360`.

### Parameter domain and observational relations

- The state group is `Z_2 x Z_2`. Every physical edge multiplier satisfies
  `0 < x_e < 1`; every inheritance parameter satisfies `0 < lambda_r < 1`;
  the root distribution is uniform. The Fourier coordinate is the positive
  mixture of displayed-tree split monomials in equation (1). See PDF pp. 5--6,
  `main.tex:362-401`.
- `M_N^JC` is the open stochastic image and `V_N^JC` its complex Zariski
  closure. `d_N` is the image dimension. A distribution is called regular if
  it has at least one parameter preimage where the parameterization has rank
  `d_N`.
- `N <=_JC N'` is source-relative containment: at a source-regular common
  point, a relatively open neighborhood in the regular source image lies in
  the target image; the target may have larger dimension. `N bowtie_JC N'`
  requires a common germ full-dimensional and regular in both images. See
  Definition 2.4, PDF p. 6, `main.tex:403-420`.

### Main claim

For leaf-labelled binary standard semi-directed strongly tree-child level-2
networks on the same taxon set,

`N <=_JC N'`

if and only if their labelled reduced bridge trees agree and every
corresponding nontrivial blob is label-preserving isomorphic or differs by one
ordinary triangle redirection. The same condition characterizes
`N bowtie_JC N'`; hence directed containment is symmetric within the class.
See Theorem 1.1, PDF pp. 2--3, `main.tex:180-195`.

The corollary says that, for fixed `N`, removal of a proper algebraic subset of
`V_N^JC` makes the topology identifiable within the class modulo ordinary
triangle redirection. See Corollary 1.2, PDF p. 3,
`main.tex:197-202`.

### Dependency graph

1. Definition 2.1 + Lemma 2.2 fix the class and exclude omnians in every
   admissible rooting.
2. Lemmas 3.1--3.2 and Proposition 3.3 reduce a strong blob to a cycle or one
   of four directed theta event cores, with finite repair choices and ordered
   port words. Proposition 3.4 gives at most one triangle per strong blob.
3. Lemmas 4.1--4.2 + finite endpoint/one-active certificates prove pointwise
   recovery of every cut by flattening rank (Theorem 4.3).
4. Corollary 4.5 makes source and target bridge trees identical under one-sided
   containment.
5. Theorem 5.1 identifies the complete positive bridge fibre as the full
   incidence-scaling action. Lemma 5.3 makes this an analytic local product
   chart. Lemma 5.4 is the semialgebraic finite-cover step; Proposition 5.5
   localizes global containment to one projective germ for each blob and rules
   out cross-blob compensation.
6. Lemma 6.2 supplies marginal submersion. The finite decorated-relation
   theorem (Theorem 6.3), restoration forests, and Lemma 6.4's coherent one-
   and two-port probes establish the local blob-containment theorem (Theorem
   6.1).
7. Lemma 6.5 gives the ordinary-triangle common germ in arbitrary unchanged
   context. Lemma 6.6 glues all corresponding local germs using uniformly
   small effective bridge scales.
8. Theorem 1.1 follows. The finite-topology and semialgebraic dimension
   argument on PDF p. 21 (`main.tex:1440-1489`) gives Corollary 1.2.

The supplement's proof map on PDF pp. 1--2,
`work/source/supplement/supplement.tex:54-100`, agrees with this dependency
graph.

## Detailed adversarial audit

### Primitive factors and boundary cases

The Euler-excess calculation in Proposition 3.3 is correct: for a nonroot
factor with `r` reticulations, `e=v+r-1`, so the biconnected core is a cycle for
`r=1` and a theta for `r=2`. The directed-event argument in Lemma 3.2 accounts
for the four acyclic source/sink placements. Strongness is not used to erase a
reticulation stack at core level; it is enforced by occupying one of the listed
repair sets. The `K_4-e` two-triangle theta is correctly excluded from `S_TC`
by the four-arrowhead/two-ordinary-tail count in Proposition 3.4.

Scope/exposition caution: Proposition 3.3 is stated for a factor from any
"standard binary level-2 blob" (PDF p. 7, `main.tex:527-533`), but its proof
invokes the `S_TC` root-reduction lemma at `main.tex:535-537`. Lemma 4.2 is
likewise phrased for a "complete standard level-2 factor" while selecting a
"minimum strong repair" (`main.tex:667-680`). Their uses are only inside the
strong theorem, so inserting `S_TC` in these statements repairs the logical
scope. As written, the proof does not establish the broader formulations.

### Pointwise cut recovery: one-active case

The graph-theoretic crossing-quartet reduction is correct. A noncut split has
at least two leaves per side. Either a bridge has both colours on each side,
yielding two active endpoint components, or the two colour hulls meet in one
component with at least two monochromatic incident branches of each colour.
Selected-leaf-free paths contribute only positive serial products.

The core/repair compression bound `|Q| <= 4`, plus at most four colour
representatives, gives at most eight active ports. Deleting other ordinary
attachments does not remove a core edge or selected repair and therefore
preserves noncutness. The proof should explicitly say `S_TC` in Lemma 4.2 as
noted above.

#### Material archive-coverage defect and independent expanded census

Manuscript Lemma 4.4 claims that a two-colour compiler checks "every compressed
root and nonroot primitive completion" (PDF p. 11,
`main.tex:812-826`). The actual compiler does not:

- `independent/bridge_cut/verify_cut.py:32-35` fixes
  `COMPRESSED_WORDS = ((), (0,), (1,), (0,1), (1,0))`.
- `verify_cut.py:654-681` iterates only products of that palette plus one
  narrowly defined singleton-duplication operation.
- Valid strong words such as `(1,0,1)` on a root-cycle segment are omitted.
  With the reticulation-sink child coloured `0`, this gives two labels of each
  colour and is a legitimate strong noncut compressed configuration.
- The source comment at `verify_cut.py:12-14` says an arbitrary-subdivision
  proof is in `PROOF.md`, but there is no such file anywhere in the archive.
  A full-text search found no palette-reduction lemma elsewhere.

I added the audit-only script
`work/core_extended_word_census.py` (SHA-256
`3f99eed321620c9d4b7fca30c6211be02fbea5f3f13de3da2012b66163f49163`).
It enumerates every binary segment word with total active-port count between
four and eight, including all mandatory sink/incoming structural ports, for
all five cores in root and nonroot modes. It then uses the archived rooted
validity, fixed-mixed strongness, displayed-switching, and colour-split
predicates, but supplies an independent complete word universe. Exact totals:

| Core / role | valid standard-strong | covered by archived palette | omitted | all-switching survivors |
|---|---:|---:|---:|---:|
| cycle / root | 3,112 | 36 | 3,076 | 0 |
| theta_TR_nested / root | 53,860 | 3,544 | 50,316 | 0 |
| theta_TR_separated / root | 53,860 | 3,544 | 50,316 | 0 |
| theta_TT_nested / root | 107,676 | 18,560 | 89,116 | 0 |
| theta_TT_separated / root | 91,464 | 16,996 | 74,468 | 0 |
| cycle / nonroot | 2,686 | 78 | 2,608 | 0 |
| theta_TR_nested / nonroot | 32,592 | 4,900 | 27,692 | 0 |
| theta_TR_separated / nonroot | 32,592 | 4,900 | 27,692 | 0 |
| theta_TT_nested / nonroot | 58,872 | 18,220 | 40,652 | 0 |
| theta_TT_separated / nonroot | 42,660 | 15,196 | 27,464 | 0 |
| **Total** | **479,374** | **85,974** | **393,400** | **0** |

The census considered 808,642 balanced candidates before validity/strongness
filtering. Thus the missing configurations do **not** falsify the switching
claim: every one has a switching that fails the proposed split. They also do
not enlarge the 72 four-active tensor types. Once a wrong switching is chosen,
the ordinary quartet criterion selects four actual labels; other repair and
sink roles become zero-character completions. Serial omitted ports contract to
effective edge products, and the existing four-active enumeration at
`verify_cut.py:440-461` and `verify_cut.py:1040-1063` covers the resulting
tensors. Nevertheless, the submitted certificate's exhaustiveness statement
is false as written and its frozen output does not contain this needed census.
The archive should incorporate the expanded enumeration (preferably with a
separate replay) or provide and verify a genuine reduction to its palette.

### Pointwise cut recovery: two-active endpoints

The four displayed minors and the three algebraic identities in the manuscript
are correct. Writing

`Delta=abc-t^2`, `Gamma=a-bc`, and similarly on the other endpoint, the
identities force both `Delta` values to zero if all four character blocks have
rank one. With `a >= bc`, `A >= BC`, and `0<z<1`, one obtains
`aA >= bcBC > z^2 bcBC`, contradicting `f_1=0`. I independently expanded all
three identities; the archive also regenerates them at
`independent/bridge_cut/verify_cut.py:1201-1257`.

#### Central-arm normalization gap and repair

There is a nontrivial omitted sentence in PDF pp. 10--11. The proof first
divides out each physical central arm (`main.tex:724-730`) and then invokes
`Delta>0` or `Delta=0, Gamma>=0` (`main.tex:737-748`). The verifier, however,
constructs a physical three-port tensor including port arms and checks
`Gamma=a-bc>0` there when `Delta` vanishes:
`independent/bridge_cut/verify_cut.py:961-985`; the separate replay does the
same at `reviews/global_bridge/exact_audit.py:727-744`. `Gamma` is not invariant
under removal of the central arm. If the central multiplier is `u`, then

`Gamma_phys(u) = a - u^2 b_0 c_0`, whereas
`Gamma_normalized = a - b_0 c_0`.

The repair is valid but must be stated. The certificate proves
`Gamma_phys(u)>0` for every `0<u<1`; continuity as `u -> 1` therefore gives
`Gamma_normalized>=0`. (`Delta=0` and its sign are invariant up to a positive
square factor.) I also extracted all nine `Delta=0, Gamma>0` records from
`independent/bridge_cut/cut_certificate.json` and removed their transported
central singleton-signature factor. The record IDs and normalized outcomes
are:

| record IDs | normalized `Gamma` |
|---|---|
| 6, 7, 56, 58, 74, 75, 76 | exactly zero |
| 67, 72 | strictly positive |

For IDs 67 and 72 the normalized expression is respectively a positive arm
monomial times `1-q^2`, where
`q=-(1-lambda)x-lambda y` lies strictly in `(-1,0)`. Hence all nine satisfy the
needed weak inequality. This confirms validity, but Lemma 4.4's prose
(`main.tex:794-810`) overstates what the archived verifier directly checks.

### Exact incidence-scaling bridge fibre

The fibre in Theorem 5.1 is correctly larger than one reciprocal scalar per
bridge. For each bridge and character sector, the flattening block is a
positive rank-one matrix. Positive factor uniqueness gives one scale per
sector; normalization fixes the zero sector and JC symmetry identifies the
three nonzero sectors. Peeling a tree recursively assigns an independent
positive scale to every vertex-edge incidence and produces exactly

`P_v -> P_v product_{e incident v} a_{v,e}^{1[h_e != 0]}`,
`x_e -> x_e/(a_{u,e}a_{v,e})`.

The converse is direct cancellation. Because the bridge graph is a tree, no
cycle holonomy remains. The anchor exponent matrix for an unmarked component
of degree at least three has full rank: its first three pair rows have
determinant `-2`, and each later row introduces a new incidence. Strong cycle
and theta components have enough boundaries; marked leaf components have
one-character anchors. The theorem correctly restricts the physical fibre to
the intersection of the ambient orbit with **all** open local-arm, bridge, and
inheritance constraints. See Theorem 5.1, PDF pp. 13--14,
`main.tex:868-936`.

The resulting local product chart is valid locally at a generic physical
regular point: the constant-rank theorem supplies a section of the chosen
smooth image branch, and openness lets one shrink so all reconstructed
physical multipliers remain strict. The prose should be read after shrinking
away from image self-intersections; the source-open containment always meets
that dense locus.

### Finite cover, projective localization, and no cross-blob compensation

Lemma 5.4 is a correct semialgebraic dimension statement. A full-dimensional
semialgebraic subset of a smooth `d`-manifold has nonempty relative interior,
and a finite cover of a relatively open set therefore contains one
full-dimensional open subgerm. A general relatively open `U` need not itself
be semialgebraic, but it contains a small semialgebraic coordinate ball, as the
proof uses. See PDF pp. 14--15, `main.tex:983-1021`.

Proposition 5.5 is sound after restricting to a smooth product chart. Varying
one source factor while fixing all other source projective factors and
effective bridge scales produces a focal box. Any target realization of the
same global distribution must have the same intrinsically extracted focal
projective orbit by Theorem 5.1. The finite set of target incoming/completion
types semialgebraically covers the box; Lemma 5.4 fixes one type on an open
subgerm. Other blobs cannot change that extracted orbit, so they cannot cancel
a local separator. See PDF p. 15, `main.tex:1023-1042`.

One exposition detail worth adding: the regular set in Definition 2.4 need not
globally be one manifold (a regular preimage can map to an image
self-intersection). The proof implicitly shrinks to a smooth maximal-rank image
stratum before applying the product and finite-cover arguments. Such a stratum
is dense and every source-open germ contains a full-dimensional branch, so
this does not change the conclusion.

### Marginal submersion, restoration, probes, and local theorem

For each restriction used by the proof, complete switching-signature rows
correctly identify serial JC edge classes, including split complements on
zero-sum assignments. Each effective coordinate is a product
`y=x_1...x_s`; its differential is nonzero on the open cube and the map is
onto `(0,1)`. Retained inheritance choices are unchanged up to parent
permutation/complement. Therefore the descriptor map is submersive. Combining
a selected-rank minor, a full-model rank minor, and the smooth-locus preimage
on the irreducible parameter space gives a dense locus where marginalization
has selected-model rank. The constant-rank theorem then makes restriction open
on the selected image. See Lemma 6.2, PDF pp. 15--16,
`main.tex:1079-1137`.

The restoration logic does not infer a larger marginal from a smaller one. It
fixes the target completion relation first, then obtains every prefix directly
as a marginal of the original full containment. Each prefix therefore has a
source-open selected subgerm and cannot enter a strict-separator state. The
anchor plus one-port probes locates every extra port; two-port probes fix the
order within each interval. Pointwise rigidity forces the same anchor
transport, and Proposition 3.4 ensures at most one triangle per blob, so the
ordinary-triangle choice is coherent. The human assembly argument in Lemma
6.4 is correct, conditional on the bounded atlas/probe certificates. See PDF
pp. 18--19, `main.tex:1277-1331`.

I did not re-audit every bounded-atlas record in this subtask; that remains a
separate code/atlas dependency. The package itself accurately describes the
human/machine boundary in `PROOF_BOUNDARY.md:3-18`, except for the cut-word
coverage defect above.

### Contextual triangle gluing and simultaneous physical gluing

At the certified strict tensor, each of the three three-sunlet orientations
has rank four, the full normalized three-port ambient dimension. The
constant-rank theorem therefore gives a common open tensor neighborhood with
physical analytic sections. In any unchanged context, contraction depends only
on that boundary tensor and the context parameters. Choosing a point where a
generic contraction minor is nonzero makes the common contextual image a
full-dimensional regular germ for all orientations. This is a forward tensor
contraction and does not assume a non-existent inverse factorization inside a
theta. See Lemma 6.5, PDF pp. 19--20,
`main.tex:1338-1380`.

For finitely many corresponding factors, the local physical sections have
bounded positive incidence scales after shrinking. On each bridge one can
choose a common sufficiently small effective scale `z_e` and set the physical
bridge multiplier on side `k` to
`z_e/(a_{u,e}^{(k)}a_{v,e}^{(k)})`; it is then in `(0,1)` on both networks.
The local product chart gives the expected global rank. See Lemma 6.6, PDF p.
20, `main.tex:1387-1421`.

### Genericity argument

For fixed `n`, tree-childness bounds reticulations by `n-1`, binary degree
counting gives finitely many topologies, and each complex model closure is
irreducible as a polynomial-image closure. If the Zariski closure inside
`V_N` of an intersection with a wrong topology were all of `V_N`, the real
semialgebraic intersection would have dimension `d_N`; on a smooth regular
source stratum it would have relative interior, giving forbidden directed
containment. Thus each wrong-topology intersection closure is proper. Finite
union, singular locus, critical-value images, and the explicitly nonzero
observable witness hypersurfaces remain proper. See PDF p. 21,
`main.tex:1440-1489`.

The manuscript could make one implicit point explicit: before concluding that
a full-dimensional intersection yields `N <=_JC N'`, remove the critical-value
image (dimension at most `d_N-1`) and choose the open part on a smooth
source-regular stratum. The subsequent paragraph already proves exactly this
dimension bound, so there is no circularity.

## Concrete defects classified

### Material reproducibility / proof-certificate defect

1. **The two-colour compiler is not exhaustive despite the manuscript's exact
   claim.** Manuscript Lemma 4.4, PDF p. 11,
   `main.tex:812-826`; archive
   `independent/bridge_cut/verify_cut.py:32-35,654-681`. It omits 393,400 valid
   configurations in the full stated eight-port universe. No omitted case is
   an all-switching survivor, as established by the audit census above, so the
   theorem survives. Required repair: add the complete enumeration and frozen
   commitment/replay, or prove and verify a genuine palette-reduction lemma.
   The comment at `verify_cut.py:12-14` references a nonexistent `PROOF.md`.

### Exposition/proof-crosswalk defects

2. **Central-arm normalization is not connected to the certificate.** PDF pp.
   10--11, `main.tex:724-748,794-810`; archive
   `independent/bridge_cut/verify_cut.py:961-985` and
   `reviews/global_bridge/exact_audit.py:727-750`. Add the continuity argument
   `Gamma_phys(u)>0` for all `u<1` implies `Gamma_normalized>=0` at `u=1`, or
   certify the normalized expressions directly. All nine equality records
   pass the corrected check.

3. **Two structural statements are broader than their supplied proof/use.**
   Proposition 3.3, PDF p. 7, `main.tex:527-537`, invokes an `S_TC` root lemma
   despite being stated for any standard level-2 factor. Lemma 4.2, PDF p. 10,
   `main.tex:667-680`, assumes a minimum strong repair without stating the
   strong hypothesis. Restrict both statements to factors induced by the
   theorem's `S_TC` class (or provide broader proofs).

4. **Smooth-stratum shrinking is implicit.** Definition 2.4 regularity does
   not make the entire regular-image set one manifold. The applications in
   Lemma 5.3, Proposition 5.5, Lemma 6.2, and the genericity proof should state
   that they first shrink to a smooth maximal-rank image branch. This is a
   standard valid repair, not a change of claim.

### Supplement/reproducibility presentation defect

5. The supplement still contains `ZENODO_DOI_PENDING` and says it "must be
   replaced before submission" (supplement PDF p. 6,
   `work/source/supplement/supplement.tex:381-385`). This is not mathematical,
   but it is an obvious publication/reproducibility defect.

## Strongest independently verified results and exact remaining gaps

Strongest verified:

- all four two-active minors and all three elimination identities are exact;
- every one of the nine `Delta=0` endpoint types satisfies the **normalized**
  weak `Gamma` inequality (seven equalities, two strict positives);
- the complete binary-word universe through the manuscript's eight-port bound
  has 479,374 valid standard-strong colourings and zero all-switching
  survivors;
- the exact positive bridge fibre is the full incidence action, not a
  reciprocal-per-bridge action;
- semialgebraic finite-cover localization genuinely excludes cross-blob
  compensation;
- contextual triangle and simultaneous physical gluing arguments are locally
  full-dimensional and remain inside the strict physical domain after
  shrinking;
- the genericity step has no circular dependence on the final classification
  once the smooth/critical-value stratification is made explicit.

Exact remaining gaps for the overall paper:

- the submission must incorporate/authenticate the extended word census or an
  equivalent proof; the current frozen cut certificate is not exhaustive;
- the full validity of the main theorem still depends on the separate audit of
  Theorem 6.3's complete decorated atlas, restoration forests, and probe
  records; I did not duplicate that row-level code audit here;
- the endpoint normalization continuity sentence, `S_TC` scope restrictions,
  and smooth-stratum shrinkings should be inserted into the manuscript;
- the pending DOI token must be resolved before publication.

