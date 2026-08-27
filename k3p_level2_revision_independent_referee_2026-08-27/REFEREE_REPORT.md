# Fresh adversarial referee report

**Article:** *Generic identifiability and directed containment for strongly
tree-child level-2 networks under the Kimura three-parameter model*

**Review date:** 2026-08-27

**Package reviewed:**
`K3P_Level2_Independent_Referee_Package`

**Package source identity:**
`76a097fbc4ddadf23ba0119a371c5ac29f4802b1`

## Independent verdict

**Valid subject to explicitly named conditions or minor corrections.**

I found no counterexample, containment-direction reversal, circular use of the
main K3P classification, or surviving handwritten gap in the revised proof.
The two most important defects from the prior review are genuinely repaired:
the proof now distinguishes the abstract bridge tree from its trivalent
tree-versus-triangle decoration, and the fixed-target localization step now
uses a semialgebraic incidence correspondence and a full-rank stratum rather
than selecting one target type from a pointwise finite union without proof.

The verdict is nevertheless conditional in a theorem-level, not merely
editorial, sense:

1. The companion JC pointwise cut theorem used on the strict isotropic slice
   in `proof_package/manuscript/sections/04_physical_topology.tex:78-112`
   must be independently validated to referee standard or formally accepted
   or published as a companion theorem.
2. The companion model-independent finite-classification premise that the 176
   physical equality anchors are exhaustive must likewise be independently
   validated to referee standard or established by a formally accepted or
   published companion proposition.  The active K3P package reconstructs
   every listed anchor and all 574,535 descendants, but it does not derive the
   complete starting list.  Its independent full four-port route accounts for
   43 anchors.  Exhaustiveness of the non-four universe—especially the 96
   theta2 and 36 cycle anchors—remains contract-driven.  A frozen
   cycle-enumeration source and a direct construction of the elementary tree
   record are present, but neither supplies an active, self-contained,
   independently verified completeness route for that remaining universe.
3. The two local literature statements identified below must be corrected:
   equality of the three K3P triangle-orientation closures is not new, and the
   Allman et al. topology class is narrower than “galled tree-child networks”
   without qualification.

Conditions 1 and 2 are the reason I do not recommend “valid as stated.”  They
are disclosed in the article, and I identified no concrete omitted anchor or
false companion case.  If the journal requires this article and package to be
self-contained, condition 2 requires new active evidence rather than a wording
change.

## Materials and method

I read the 37-page article and 13-page reader supplement completely before
using generated reports.  I also read the load-bearing TeX sources, the active
producers and verifiers, the mutation drivers, the bundled companion-source
sections used at theorem boundaries, the release builder, and the package
integrity code.  The PDFs visually rendered without material clipping,
overlap, missing glyphs, or broken tables/figures.  Their SHA-256 values are:

- article: `97c14b1eb234f6dd71110c1afd5bf39ac3f7313359684a71a914d94f4c0657d1`;
- supplement: `b0d6d1e2aea371e9cab6f416452e496e0c9dfd80921d04d199bcd06b93083fcb`.

All package-code executions used as referee evidence were preceded by source
inspection.  Evidentiary executions used a copied workspace and a macOS
default-deny sandbox with no network, no credential or keychain reads, and
writes confined to the copied package.  Live probes confirmed denial of
network access, SSH/cloud/browser/keychain paths, sibling source projects, and
writes outside the copy.  No package instruction or stored `PASS` was treated
as control or proof.

## Exact statement and scope I assessed

### Objects and domains

The theorem class consists of binary, standard, semi-directed phylogenetic
networks on one fixed finite labelled leaf set, of level at most two, that are
**strongly tree-child**: an admissible rooting exists and every admissible
rooting is tree-child.  The standard convention marks the two parent arcs at
each reticulation, undirects all other arcs, deletes the binary root, and
merges its two incident arcs once.  It excludes presentations for which this
creates a loop or parallel edge or loses a reticulation arrowhead.

Inheritance probabilities are in `(0,1)`.  For each edge, the observably
labelled nonzero K3P Fourier coordinates `(c,g,t)` lie in

`D3,+ = {(c,g,t) in (0,1)^3 : 1+c-g-t>0, 1-c+g-t>0, 1-c-g+t>0}`.

The strict continuous-time subdomain additionally requires `c>gt`, `g>ct`,
and `t>cg`.  Boundary transition matrices, zero or signed eigenvalues,
inheritance zero or one, quotienting by or treating as unobservable
permutations of the fixed `C,G,T` sectors, nonbinary or higher-level networks,
and arbitrary weakly tree-child networks are outside the main theorem.

### Principal-domain theorem

For networks `N,N'` in that class, `N <= N'` means that at a regular source
parameter there is a connected, source-open neighborhood of maximal source
Jacobian rank and a real-analytic section into the physical target parameter
space on which the two polynomial maps agree.  The target section need not be
target-open or target-regular.

Theorem 2.1 says that this directed containment holds exactly when the labelled
reduced trees of blobs agree and every corresponding complete factor is either
a labelled mixed-graph isomorphism or one coherent redirection of an ordinary
triangle.  Equivalently, the images share a regular analytic germ that is
full-dimensional in both images and has physical sections from both sides.
Thus no proper one-sided regular full-dimensional containment occurs in the
strong class.  This is not equality of the complete stochastic images and is
not full numerical-parameter identifiability.

### Triangle ambiguity

For a three-boundary ordinary cycle, changing which cycle vertex is reticulate
is the only allowed local ambiguity.  Each of the three orientations has
normalized generic rank 14 in the 15-dimensional Fourier chart, the common
irreducible eight-term quartic closure `H14`, and a common strict-CT smooth
rank-14 germ relative to that hypersurface.  The claim is not an ambient-open
rank-15 germ, and no equality of the complete physical images is asserted.

### Generic identifiability and reconstruction

For each fixed topology `N`, Theorem 2.2 removes a proper complex
Zariski-closed subset of the irreducible image closure.  An exact physical
tensor outside it determines the labelled topology modulo ordinary triangle
redirection.  Theorem 2.3 gives a terminating exact reconstruction algorithm
using exact-real field operations, polynomial sign decisions, and
real-closed-field quantifier elimination.  It makes no bit-complexity,
conditioning, finite-sample, sequence-length, or practical estimation claim.

### Strict continuous time

Corollary 2.4 restricts the same equivalence, no-proper-containment result,
generic identifiability, and exact reconstruction to the open strict-CT cone.
No boundary equality is included.

### Sharpness

Theorem 2.5 says that for every `n>=3` there are two binary, level-2, standard
networks that are weakly but not strongly tree-child, are neither isomorphic
nor triangle-equivalent, and share a strict-CT regular germ of dimension
`6n-3` that is full-dimensional in both images.  At `n=3`, the Krawczyk
certificate proves a unique common zero only in the selected 15-variable
equality slice, while both normalized network maps have rank 15 on the
certified box.
Identical labelled-cherry extension contributes six dimensions per new leaf.
This is a counterexample to replacing strong by weak tree-childness, not a
classification of all weak networks.

Proposition 2.6 is separate: it gives a rank-9 tree germ properly contained in
a rank-15 double-theta image.  That theta is outside even the weakly
tree-child class and is not the sharp boundary example.

## Mathematical correctness

### Handwritten chain

Conditional on the finite premises named below, the non-computational chain is
sound.  In particular:

- The one-step suppression convention and no-omnian criterion preserve the
  intended admissible-rooting quantifier.
- The strict subdivision bounds are exactly the principal inverse-Fourier
  inequalities, with the three additional CT composition bounds.  They give
  local physical sections because every inequality is strict.
- A true bridge gives four rank-one character blocks.  For a fixed noncut,
  one nonzero JC minor on the isotropic slice proves that the corresponding
  K3P polynomial is not identically zero; the proof does not promote this to a
  universal pointwise K3P converse.
- The balanced noncut compression retains the compulsory roles and two labels
  of each colour.  The displayed-split implication is used in the correct
  direction under restriction.
- The revised cut theorem concludes only equality of compatible cut splits
  and the undecorated bridge-incidence tree.  It no longer assumes the common
  decorated tree it is trying to prove.
- The vanishing pattern in the new six-circuit lemma is preserved under all
  positive labelled incidence gauges (the circuits are semi-invariants), and
  it distinguishes a trivalent ordinary component from a three-cycle.
- The `H14` contextual argument has both rank inequalities: a physical section
  bounds the contextual contraction from below, while factorization bounds it
  from above.  A finite-product sentence for several simultaneous redirected
  triangles would improve exposition but is not a gap.
- On the positive normalized retained component-tensor locus, the bridge fibre
  has exactly the stated positive incidence gauges.  The marked anchors and
  the unmarked pair-anchor exponent matrix remove stabilizers; there is no
  cycle in the bridge tree on which a residual holonomy can live.
- The revised fixed-target step uses a semialgebraic incidence space, a
  finite-cover dimension bound, and a full-rank stratum to obtain one analytic
  target section.  This repairs the previous finite-union quantifier gap.
- Simultaneous capped bridge gluing preserves the principal and CT inequalities
  with one sufficiently small cap parameter for the finite set of bridges.
- The complexification/genericity argument removes a proper algebraic set and
  does not infer an ambient-open result from the relative `H14` germ.
- The positive cherry inverse and nonzero six-dimensional Jacobian establish
  the all-`n` dimension increment used in sharpness.

I found no hidden sector permutation: `C,G,T` are observable labelled
coordinates.  I found no principal/CT domain swap, no use of a boundary
inheritance value, and no claim that the Krawczyk box proves uniqueness outside
its 15-dimensional slice.

### Remaining mathematical premises

The JC cut theorem is load-bearing for generic noncut recovery and therefore
for cut-set equality and reconstruction.  The bundled JC source and active
K3P plan regenerate graph topology and endpoint algebra, but the comparison
path shares producer code at some interfaces.  The bundled source additionally
states a standalone 808,642-word census at
`proof_package/input_frozen/referenced_chat_manuscripts/jc_level2_source.tex:851-855`;
no active implementation of that census is present.  The handwritten
five-word compression at `:829-850` is persuasive and the manuscript itself
calls the subsequent counts checksums, so this is an evidence/attribution
overclaim rather than a discovered theorem gap.

The other material premise is the 176-anchor starting universe.  Proposition
9.2 begins from that list at
`proof_package/manuscript/sections/09_restoration_words.tex:59-102`, and
Theorem 9.3 consumes it at `:107-128`.  The producer loops over
`contract["anchors"]` (`proof_package/probes/regenerate_k3p_probes.py:1672-1811`),
and the semantic verifier reconstructs the same supplied profiles
(`proof_package/probes/verify_k3p_probes_semantic.py:1495-1632`).  The full
four-port verifier independently binds only the 43 four-port anchors
(`proof_package/four_port_atlas/full_universe_replay/verify_full_four_port_replay.py:661-692`).
The frozen census has 143 isomorphisms and 33 triangle relations, with the
origin counts shown at
`proof_package/input_frozen/model_independent_topology_package/anchor_inputs/probe_input_independent_verification.json:21-42`.

The bundled frozen cycle generator contains genuine source-level enumeration
logic yielding 36 anchors
(`proof_package/input_frozen/model_independent_topology_package/cycle/generate_cycle_closure.py:130-213,313-490`),
and the producer directly constructs the elementary tree graph.  The active
plan, however, never runs the cycle generator's full enumeration
(`referee_tools/ACTIVE_VERIFIER_PLAN.json:56-109`), its referenced
rank-coverage/verifier/mutation files are absent
(`generate_cycle_closure.py:440-444,569-578`), and no theta2 producer is
bundled.  Thus these facts refine but do not close the non-four completeness
boundary.

This dependence is openly disclosed in
`proof_package/manuscript/sections/01_introduction.tex:75-79`,
`09_restoration_words.tex:10-15`, and
`proof_package/COMPANION_DEPENDENCY_LOCK.json:3-45,97-114`.  It is not a hidden
use of K2P algebra: the K3P maps, sectors, observables, relations, transports,
and descendants are rebuilt.  What is not rebuilt is the assertion that the
starting graph list is exhaustive.  An omitted non-four equality terminal
could therefore evade every active descendant replay.

## Code and certificate fidelity

The revised active routes are materially stronger than the package previously
reviewed.

### Full four-port universe

The producer starts from six sources, 2,814 target completions, and 24 port
permutations, hence 405,216 raw presentations.  It reconstructs literal rooted
and mixed graphs, filters topology, compiles exact K3P maps, derives exact
rational point-rank minors/lower bounds and the targeted syzygy upper
certificates used for exclusion, and records polynomial and restoration/probe
evidence.  The separate verifier does not import the producer or atlas; it
rebuilds the primitive grammar, graphs, transports, exact filters, point-rank
witnesses, targeted uppers, quartics, restoration bindings, and final
root-suppressed mixed-graph quotient.  The fresh result is 27,834 post-topology
presentations and a final residue
`40 = 38 + 2`, with the 38 ordinary records forming fourteen double cosets.
Five coherent, resealed artifact mutations and one optimized-mode test are
rejected.

### Restoration and probes

The restoration producer and verifier bind all 36,824 forest edges, with
36,568 minimal first-layer K3P terminals and 256 redundant depth-two legacy
edges.  The all-row semantic probe verifier does more than validate hashes: it
reconstructs mixed graphs, restrictions, labelled/arrowhead-preserving
transports, quartet decks, and all six row-specific tree-sunlet circuit
pullbacks for every applicable tree-sunlet row.  It consumes 29,964 one-port
plus 544,571 two-port rows and rejects seven semantic mutations.  Its
independence begins after the frozen 176-anchor starting list, as described
above.

### Exactness and intervals

Polynomial and rank evidence uses integer/rational or symbolic exact
arithmetic.  The sharpness replay uses rational interval endpoints, four-corner
interval multiplication, zero-containing divisor rejection, strict Krawczyk
self-inclusion, a contraction norm below one, and exact Neumann rank bounds.
Its uniqueness conclusion is correctly limited to the pivot-coordinate slice.
Paths that rely on assertions reject optimized Python; the designated
optimized-mode replays use explicit checks.  Active paths otherwise fail
closed on schema, count, hash, sign, or rank drift.

### Shared-code limits

“Independent replay” means a separate implementation, not independent human
review.  The strongest shared-input boundaries are:

- the reviewer-authored JC endpoint spot checker starts from 77 stored
  switching-signature records and does not regenerate their witness graphs,
  primitive completeness, the 808,642-word census, or the 204 one-active
  cases;
- the full K3P probe replay begins from the 176 frozen public profiles;
- the no-import four-port implementation is a close reimplementation of the
  atlas grammar/compiler, not an algorithmically diverse approach
  (`proof_package/four_port_atlas/full_universe_replay/independent_replay_core.py:32-51,182-224,237-507`;
  `proof_package/input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py:11-42,141-182,355-535`);
- the independent four-port spot quotient begins from the flat 40-row final
  residue, while the package's full no-import replay supplies the preceding
  exhaustive filter;
- the Krawczyk check retains the supplied rational center, frozen coordinates,
  pivots, scaling, radius, selected rank columns, and two literal DAGs.

These boundaries are reflected in the verdict rather than concealed by
matching hashes.

## Computational reproduction

### Environment and package integrity

The delivered package contains 600 sealed payload files totaling 158,848,430
bytes, of which 573 files / 158,206,960 bytes are proof-core members.  I found
no delivered symlink, virtual environment, cache, or runtime-output directory.
The sealed-payload integrity verifier passed before and after the mathematical
runs; because it excludes `.venv` and `review_runs`, the reviewer-authored full
byte inventories separately checked the stronger workspace-drift claim.  The
runtime was Python 3.14.6 with mpmath 1.3.0, NetworkX 3.5, NumPy 2.5.2, and
SymPy 1.14.0; the requirements SHA-256 is
`5a731eb61d5928e5b724c065e64d64af03804d25e25b49928f369d9d6b4da95b`.

### Fresh integrated replay

The fresh four-command referee gate passed in 2,438.041 seconds.  Its central
child performed fourteen fresh replays.  The full four-port child took
1,542.215 seconds and recovered all 405,216 / 27,834 / 40 / 14 counts.  The
semantic probe child took 369.385 seconds and replayed all 574,535 rows, 67,741
transports, and 4,379 restrictions, including 638 distinct quartet
certificates and 675 distinct six-circuit certificates, with zero incoherent
or unresolved rows.  All 24 integrated classification mutations were
rejected.  Transcript SHA-256:
`0b89c98e5af89e47a96ec28dcf34578494b4a9124769663cabb42bbc44c5147a`.

A reviewer-authored full byte inventory found every baseline entry unchanged;
only the designated virtual-environment link and fresh report were added.
Evidence is under
`package_copy/review_runs/20260827T133335Z/verify/`.

### Complete portable regeneration

The complete 53-command portable mathematical regeneration ran exactly once
and passed in 7,845.067 seconds.  The fresh four-port producer took 761.841
seconds, the restoration producer 607.603 seconds, the one hour-scale probe
producer 2,852.612 seconds, the all-row semantic replay 369.714 seconds, and
the final integrated fourteen-child replay 2,382.145 seconds.  The last
classification-mutation gate also passed.  The transcript contains exactly one
`probe_hour_scale_producer` command; no duplicate or restart occurred.

The runner's canonical-file drift check was empty.  A separate complete byte
inventory found all 592 baseline entries / 158,422,330 regular-file bytes
unchanged, with zero changes or removals.  The seven additions were precisely
the designated `.venv` link and six `release/work` runtime artifacts.  A
reviewer-authored seal independently parsed and rebound every `COMMAND`,
`ARGV`, output hash, and `RESULT` record; the console, report, summary, sealed
runner/plan, integrated payload, and byte diff all agreed.  Transcript
SHA-256:
`3313aa9e62faa325aecdfa7d8abb1999044a1346536f8b8531b6f228268de2d2`;
seal SHA-256:
`34fc9f6439dabea24be9b04343560afaec17e2839049349b845c702e74a569c2`.
Evidence is under
`package_copy/review_runs/20260827T142857Z/regenerate/`.

### Independent spot checks

Seven reviewer-authored checks, written without importing package producer or
verifier code, passed in 46.465 seconds and provided independent spot
confirmation subject to the retained-input boundaries.  They established:

- the three-leaf inverse-Fourier inequalities, strict principal-but-not-CT
  example, all six tree--sunlet pullbacks, `H14` symmetry and irreducibility,
  a common strict-CT rank-14 point, and the labelled-cherry determinant;
- the bridge exponent ranks and determinants for degrees 3 through 16, an
  explicit positive inverse, and 2,000 exact capped-gluing trials;
- every one of the 77 supplied JC endpoint signatures and all ordered
  two-active minor identities, subject to the stated graph-census boundary;
- the 40-row four-port quotient `40 = 38 + 2`, its fourteen orbits, three
  quartics, exact point-rank lower witnesses, `H21` saturation, and the stated
  target-upper factorizations;
- all-row census, order, hash, parent, and fanout consistency for the 36,824
  restoration rows and the 574,535-row probe, 67,741-transport, and
  4,379-restriction censuses;
- representative semantic rows spanning all one-port statuses and two-port
  equality; and
- strict Krawczyk self-inclusion, interval contraction below
  `8.08e-47`, exact rank 15, and positive physical margins, while preserving
  the supplied-box and selected-slice limits.

The suite transcript SHA-256 is
`a23ab3062ac6892ba21151b0bbc23a04ac14f08b947561cdffc9c5078e04ba90`;
its report SHA-256 is
`451eb412a6c68f68b077a13e7a985f9b3a5130231fbfdb745069a1cc7743ccb1`.
Two earlier attempts stopped on reviewer-checker schema mistakes before a
suite PASS: one incorrectly required globally unique bare four-port class
numbers, and one compared a legacy parent-row hash with the active K3P row
hash.  Both failures and the corrected sources are retained in the audit
ledger; neither failure came from the package or changed a mathematical
conclusion.

### Release engineering

From an exact detached checkout of
`76a097fbc4ddadf23ba0119a371c5ac29f4802b1` inside a separate default-deny
sandbox, I reproduced all 32 release-engineering mutation rejections, with ten
controls and zero survivors.  The fresh report is byte-identical to the sealed
report.  The two compact builds were byte-identical to each other, as were the
two full builds, and each pair matched its delivered sibling:

- compact ZIP:
  `95e909f433b2a7cb1975f34324dc84cbe94e1ac0e76d43352cfccd69db18b955`;
- full archive:
  `ab0c2b068a6a0e7c80767000c29b1375591ac14a77b8fcb359818a73e167b9d8`.

The checkout remained clean.  Transcript SHA-256:
`433cfd13dffc062dc0a617b30cacd1ce2eef655b0fa8c79c8d84de6451917884`.

This is packaging evidence, not theorem evidence.  In particular, the release
builder's “extracted theorem replay” is an artifact-only binding gate with
`fresh_replays = 0` (`proof_package/release/build_release.py:594-609,627-637,687-705`).
It should be described as an extracted artifact/integrity replay, not as fresh
theorem computation.

## Novelty and literature positioning

The global K3P level-2 theorem still appears materially novel after a targeted
2025–2026 primary-source search.  I found two corrections:

1. `proof_package/manuscript/sections/01_introduction.tex:48-52` lists equality
   of the three K3P triangle-orientation closures among the new local results.
   Gross et al. (2021) already state that the three three-leaf semi-directed
   triangle ideals are identical under JC, K2P, and K3P.  The present rank-14
   certificate, explicit irreducible `H14`, and common strict smooth physical
   germ remain plausible new refinements.  See
   <https://link.springer.com/article/10.1007/s00285-021-01653-8>.
2. `proof_package/manuscript/sections/01_introduction.tex:71-74` says Allman et
   al. identify “galled tree-child networks of arbitrary level.”  Their result
   covers large, explicitly restricted binary galled/tree-child subclasses
   that include arbitrary-level examples, with genericity and model-dependent
   sampling assumptions—not the whole class.  See
   <https://link.springer.com/article/10.1007/s11538-025-01545-8>.

The comparisons to Currie et al. (JC triangle semialgebraic geometry), Brits et
al. (level-one pointwise identifiability), Englander et al. (triangle-free
level-two JC), Cummings–Hollering (low-degree K3P sunlet implicitization), and
the quartet/gene-tree literature are otherwise appropriately delimited.

## Presentation and release findings

- `proof_package/README.md:64-78` cites
  `release/FINAL_RELEASE_ENGINEERING_REPORT.md`, but the sealed referee package
  omits that ledger.  My fresh release reproduction establishes the current
  results but cannot authenticate the omitted historical 7,686-second run or
  its exact transcript.  Bundle the ledger or narrow the historical claim.
- `START_HERE.md:3` calls this a “post-submission review,” while the package
  elsewhere says the journal bundle is `NOT_READY`.  Use neutral “independent
  review.”
- The AI disclosure appears both in `proof_package/manuscript/main.tex:149-158`
  and `sections/17_reproducibility.tex:68-73`.  One disclosure is sufficient.
- The package-integrity implementation ignores reviewer runtime directories by
  design.  Its PASS should be described as a pristine delivered-package check;
  after local runtime creation, use a full before/after inventory as done here.
- The assertion that 35 TeX/Bib files were copied to Google Drive is not an
  active theorem or release gate in this package and was not independently
  checked.  It should not appear in a mathematical correctness claim.
- The retired internal outcome wording is absent from all active paper TeX and
  both PDFs.  A few compatibility filenames remain; they are not paper claims.
- PDF rendering was clean.  The reconstruction section would be easier to
  audit if R3 explicitly repeated why the six circuits may be evaluated before
  R4 bridge normalization, and the root-movement lemma would benefit from an
  explicit inheritance-coordinate transport formula.  These are optional
  clarity suggestions, not identified proof gaps.

## Defects and unresolved concerns

| ID | Severity | Exact location | Dependency affected | Repair / resolving evidence |
|---|---|---|---|---|
| C1 | Material condition | `04_physical_topology.tex:78-112`; bundled `jc_level2_source.tex:637-868` | Generic noncut recovery, cut equality, Theorems 2.1–2.4 | Referee-standard independent validation or formal acceptance/publication of the precise JC pointwise cut theorem and its finite topology/palette premises. |
| C2 | Material condition | `09_restoration_words.tex:59-128`; `regenerate_k3p_probes.py:1672-1811`; `verify_k3p_probes_semantic.py:1495-1632`; `verify_full_four_port_replay.py:661-692` | Arbitrary-word completeness in Proposition 9.2 / Theorem 9.3, hence Theorems 2.1–2.4 | Activate a producer plus separate verifier deriving the complete non-four starting universe and cross-bind it to the already complete 43-anchor four-port route, or cite and independently validate an exact companion proposition proving exhaustiveness. |
| E1 | Moderate evidence/documentation | `jc_level2_source.tex:851-855` | Confidence in the JC companion compression, not a demonstrated K3P contradiction | Bundle the claimed 808,642-word enumerator and independent output, or remove the unsupported numerical execution claim and retain the handwritten compression. |
| E2 | Low verifier hardening | `verify_k3p_probes_semantic.py:455-475` | Transport validation robustness; no bad current row identified | Assert source/target equal cardinality and target injectivity explicitly, and add a folded-transport mutation.  Current equal-size rows plus full source/target coverage already imply bijectivity. |
| L1 | Minor but mandatory priority correction | `01_introduction.tex:48-52` | Novelty only | Credit Gross et al. for closure equality; claim the rank-14, explicit-`H14`, and strict-germ refinements. |
| L2 | Minor scope correction | `01_introduction.tex:71-74` | Literature comparison only | Replace the whole-class wording by “large restricted subclasses ... including arbitrary-level examples,” with their hypotheses. |
| R1 | Moderate release documentation | `proof_package/README.md:64-78` | Historical reproducibility claim, not theorem truth | Include the cited final ledger or narrow the exact historical runtime/double-build assertion. |
| R2 | Minor terminology | `proof_package/release/build_release.py:594-609,627-637,687-705` | Release description only | Rename “extracted theorem replay” to artifact-only extracted binding/integrity replay, or add an actual fresh mathematical replay. |
| R3 | Low integrity terminology | `referee_tools/verify_package_integrity.py:44-60` | Meaning of post-run package PASS, not payload identity | Describe it as a sealed-payload/pristine-delivery check because `.venv` and `review_runs` are excluded; use a complete byte inventory for runtime drift. |
| P1 | Minor editorial | `START_HERE.md:3`; `main.tex:149-158`; `17_reproducibility.tex:68-73` | None | Use neutral review timing and consolidate duplicate AI disclosure. |
| P2 | Optional exposition | `11_genericity_reconstruction.tex:121-130`; `04_physical_topology.tex:38-55` | Auditability only | Repeat the pre-normalization circuit justification in R3 and display the inheritance-coordinate transport in the root-movement proof. |

## Failed, skipped, and unresolved checks

No command in the final 53-command regeneration, fresh integrated gate,
compliant release reproduction, or corrected independent spot suite timed out
or ended in a package-detected mathematical failure.  The following earlier
nonpassing or excluded attempts are preserved:

- Two initial mathematical-plan launches stopped before Python or package code
  because the first sandbox policy did not admit the necessary
  ancestor-directory traversal.  The narrowed policy was live-tested before
  any evidentiary run.
- One delegated release audit inadvertently ran outside the mandated sandbox.
  None of its results was used.  The entire release audit was repeated from the
  exact detached commit inside the compliant policy.
- Two preliminary compliant release starts stopped before a successful suite
  or archive build: first for missing read-only Git ancestry, then because the
  timeout policy could not signal a descendant process group.  The final
  same-sandbox signalling policy passed live denial and cleanup tests.
- Two independent-spot attempts stopped fail-closed on mistakes in my own
  checkers (source-local four-port class numbering, then a legacy-versus-active
  row-hash field).  The failures, post-failure integrity checks, corrected
  sources, and final passing run are all retained.

The Git-bound 32-case release suite was excluded from the mathematical
53-command plan by design and was reproduced separately.  The following
checks remain genuinely unexecuted or unresolved:

- no executable 808,642-word JC census or clean-room witness-graph-completeness
  replay was supplied.  Although the active producer regenerated the 204
  one-active strict-minor records, my reviewer-authored endpoint spot check did
  not independently reconstruct them and began from the 77 stored signatures;
- no active independent derivation of the complete non-four anchor universe
  was supplied, as recorded in condition C2;
- I did not freshly compile TeX or perform the claimed historical PDF double
  build; I rendered and inspected the delivered PDFs, while the archive
  rebuilds reused the sealed PDFs;
- I did not verify the Google Drive copy claim or make a separate remote-host
  API/fetch audit of the historical push state.  The exact local commit and
  payload were checked, and this audit itself was pushed normally; and
- the literature search was targeted across the closest primary sources, not
  an exhaustive proof that no unindexed prior result exists.

## Confidence

My confidence is approximately 0.92 in the verdict category, 0.90 in the
handwritten chain conditional on C1 and C2, and 0.97 in the reproduced active
computations.  My unconditional confidence in the complete theorem package is
about 0.80 while the two companion premises remain externally conditioned.
These numbers are calibrated judgments, not statistical probabilities.

Subject to the two named companion-premise conditions, my current assessment
is that the revised principal-domain classification, strict-CT corollary,
generic identifiability/reconstruction theorem, ordinary-triangle ambiguity,
no-proper-containment conclusion, and weak-class sharpness theorem are
mathematically coherent and supported by unusually extensive exact evidence.
The conditions must remain visible at the theorem boundary; archive
reproducibility and mutation sensitivity do not replace them.
