# Fresh adversarial mathematical review of the 2026-08-25 K2P package

Date: 2026-08-25 (America/Los_Angeles)

Package reviewed, and no other submission package used as theorem authority:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee`

This is a bounded mathematical subreview.  I did not modify any file below
`isolated/`, did not contact anyone, and did not run the submitted full replay
suite.  Stored PASS fields, replay reports, and hashes were treated as
assertions.  The computational exhaustiveness statuses below therefore remain
UNVERIFIED wherever they require the full raw ledgers, canonicalizer, forest,
or probe replay.  This note distinguishes that limitation from a gap in the
mathematical implication that consumes a correctly certified finite premise.

## 1. Outcome

**Mathematical deduction: PASS, conditional only on the explicitly identified
finite exhaustive predicates C04--C09.**  I found no counterexample, invalid
quantifier change, domain error, hidden use of the revoked rooted
tree--sunlet oracle, or unsupported implication in the article's hand proof.
The principal-domain theorem, genericity argument, exact reconstruction
argument, continuous-time restriction, and weak-class sharpness construction
are mathematically coherent.

**Finite exhaustive predicates in this bounded subreview: UNVERIFIED.**  I
independently checked the primitive counts, several graph reductions, printed
polynomial pullbacks, rank determinants, physical boundary points, the
triangle germ, and weak-sharpness formulas.  I did not independently regenerate
every one of the 405,216 raw4, 2,946,240 theta2, 536,364 cycle completion,
36,824 restoration-edge, or 544,571 two-port rows.  End-to-end unconditional
status must therefore be combined with the separate computational audit.

**Counterexample search: none found.**

**Fresh finding:** one nonblocking authority-consistency defect remains in C11.
The crosswalk designates the frozen promotion manuscript as authoritative for
reconstruction, but that manuscript still contains the older instruction to
"select a rigid support" and omits the retain-all-candidates plus final exact
semialgebraic membership step.  The article itself contains the corrected,
valid procedure.  Thus this does not defeat the theorem as published, but the
C11 authority set is not internally self-consistent.  Details and the smallest
repair are in Finding 1.

**Prior C02/stale-authority issue: fixed.**  The current C02 claim, certificate,
and crosswalk scope agree.  The obsolete 377,382/36,404 narrative counts remain
only inside a prominently revoked historical document and do not feed any
current classification predicate.  Details are in Section 5.

Confidence in the hand mathematics: **0.94**.  Confidence that no second
hand-proof defect remains after this bounded rereading: **0.88**.  Confidence
in the complete finite exhaustion from this review alone: **not assessed**
(the relevant gates were intentionally not run).

## 2. Artifact identities and reading scope

I read the complete TeX sources and the complete rendered article and
supplement, including the generated appendix, compression tables,
bibliography, crosswalk, and the load-bearing proof narratives.

| Artifact | SHA-256 | Scope read |
|---|---|---|
| `proof_compression_submission/article/main.tex` | `983ddc75e568ff9278481c5e43159a9dc566c3dfc9aa1db9c6e31ae6c13c5c3c` | all 1,866 lines |
| `proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf` | `9934a92091d069c8764cf8c3aba6b496d482e4e0d5d0a526586f5a0d133f0411` | all 26 physical pages, text and rendered pages |
| `proof_compression_submission/supplement/supplement.tex` | `4166832734f84cd0752f283be6a094249f969e863d084bd11957031f256b8140` | all 956 lines |
| `proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf` | `66161998ec9b30355ac3f6f6467462e8be32230ee52ebf4fbfcaff77fe663866` | all 24 physical pages, text and rendered pages |
| `proof_compression_submission/supplement/certificate_appendix.tex` | `f2444f0308ab2dcccc45dec0704e98b147fffe4bb11fef9ef19cb7f34e688af5` | all 285 lines |
| `proof_compression_submission/supplement/compression_tables.tex` | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` | all 69 lines |
| `proof_compression_submission/article/references.bib` | `14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c` | all 202 lines |
| `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md` | `dc10e5e619b66048797076866a9fbb88373cb6cea09bcb210e690cdd12599406` | complete table, especially lines 14--28 |
| `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json` | `550282c891c3d925f2e06379338f55d7fce6062aeadbaf411fbf45b1374b8d5b` | all claim objects and cited paths/hashes |

The PDF text extractions used for line-by-line comparison had SHA-256
`99abb0002cfbb631196f2566574cdd937b9c8cd84f1dfe1a9201d7a657ef56ed`
(article) and
`b90ca2a9ba940275cf4e7e19b97a9cdb55f8e2f3f8e9a1163e5bb726611fba99`
(supplement).  Rendered contact sheets covered all 50 pages.  I saw no clipped
formula, missing appendix page, or malformed table.  Key source/PDF locations
matched: definitions and domain on article PDF pp. 3--7; bridges pp. 7--9;
localization pp. 9--11; finite grammar and classification pp. 11--16;
triangle/global theorem pp. 17--18; genericity/reconstruction pp. 19--21;
continuous time p. 21; weak sharpness pp. 22--24.  Supplement locations were
grammar pp. 4--5, census pp. 6--7, probes pp. 7--8, calculations/certificate
appendix pp. 8--15, weak sharpness pp. 15--16, crosswalk pp. 16--21, and replay
scope p. 21.

Proof narratives read completely included:

- `work/domain_rooting_closure/PROOF.md`, SHA-256
  `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
- `work/quartet_separation_closure/PROOF.md`, SHA-256 prefix
  `a0f34c91c1a9` (crosswalk C02, Markdown line 17);
- `work/bridge_marginal_closure/PROOF.md`, SHA-256
  `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
- `work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md`,
  SHA-256 prefix `b84af8f9f5a4` (crosswalk C03, line 18);
- `proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md`,
  SHA-256 prefix `05e5ad92a1c7` (crosswalk C04, line 19);
- `work/canonicalizer_completeness/PROOF.md`, SHA-256 prefix
  `7e0e7be28c5b` (crosswalk C04, line 19);
- `work/rank_upper_certificates/PROOF.md`;
- `work/cycle_three_port_closure/PROOF.md`;
- `work/probe_coherence_corrected/PROOF.md`;
- `proof_compression_submission/probe/PROBE_WORD_THEOREM.md`, SHA-256
  `cd4e16a50622a1584d16a4a90b08a55f95c1dfe16849e47eedae11d77b57b56f`;
- `work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`,
  SHA-256
  `add7bc4a34563d0175f4e19ebe7ca2536b77772ff50d7f017628505d7e6c1899`;
- `work/global_theorem_closure/QUANTIFIER_AUDIT.md`;
- `work/global_proof_adversary/AUDIT.md`;
- `work/weak_sharpness_closure/PROOF.md`, SHA-256 prefix
  `dcc36e0ae429` (crosswalk C13, line 28); and
- `work/weak_sharpness_audit/PROOF_AUDIT.md`, SHA-256 prefix
  `d0a4e950a17f` (crosswalk C13, line 28).

I also read the exact tree--sunlet and ordinary-triangle narratives cited by
C10 and the historical/revocation registry needed to determine what is and is
not current authority.

## 3. Claim matrix

In this bounded mathematical subreview, a PASS can concern the deduction or a
hand-checked formula while the separate computational audit supplies the full
finite exhaustion. UNVERIFIED means that the full finite predicate was not
regenerated in this subreview; it does not denote a discovered counterexample.

| Claim | Status in this subreview | Mathematical evidence | Independent attack | Exact remaining gap |
|---|---|---|---|---|
| C01 domain/rooting/subdivision | **PASS** | Article PDF pp. 5--6; `main.tex` principal-domain and rooting section; domain proof SHA `f71a8e...` | Rational boundary points, product and subdivision checks | None found |
| C02 quartet/tree of blobs/raw direction | **PASS** | Article PDF pp. 6--7; current scope at crosswalk MD line 17 and current JSON certificate lines 3--17, 29--47 | Recomputed the seven positive displayed-set sign logic and representative pullbacks | Full 360,408-row replay belongs to computational audit, but the prior authority defect is fixed |
| C03 bridge/marginal/local product | **PASS** | Article PDF pp. 7--9; bridge proof SHA `0677...`; physical repair SHA prefix `b84...` | Re-derived the two gauge scales, D-plus products/sections, and a simultaneous CT gluing example | None found |
| C04 primitive grammar and completion | **UNVERIFIED** | Article PDF pp. 11--13; supplement PDF pp. 4--7; crosswalk MD line 19; hand grammar check PASS | Exact independent completion formula and raw totals; separate primitive orientation enumeration | Did not replay every canonicalizer orbit/raw row in this subreview |
| C05 raw-four rank filter | **UNVERIFIED** | Article PDF pp. 13--15; supplement PDF certificate appendix; crosswalk JSON lines 540--649; certificate semantics check PASS | Recomputed representative symbolic minors by a separate SymPy construction | Did not establish all 3,515 universal plus 75 exceptional representatives in this subreview; crosswalk omits executable rank replay (Finding 2) |
| C06 direct separator families | **UNVERIFIED** | Generated appendix SHA `f244...`; printed table JSON SHA `4a4b58...` at crosswalk JSON lines 652--669; formula spot checks PASS | Recomputed representative F/G pullbacks, strict sign factor, polynomial identities/witnesses | Did not replay the assignment of every direct class to every formula in this subreview |
| C07 corrected full-map universe | **UNVERIFIED** | Article finite theorem and crosswalk MD line 22 | Current counts and scopes are internally consistent; C02 oracle exclusion checked | Composite ledgers not regenerated here |
| C08 restoration forest | **UNVERIFIED** | Article `main.tex:1127--1133`; supplement `supplement.tex:314--329`; forest JSON `/census`; restoration implication check PASS | Checked fixed-full quantifiers and representative continuation logic; no target-deletion inversion | Did not trace all 36,824 graph/transport edges in this subreview |
| C09 coherent probes/word reconstruction | **UNVERIFIED** | Supplement PDF pp. 7--8; `PROBE_WORD_THEOREM.md`; probe JSON `/assembly_theorem`; word-induction check PASS | Checked adjacency-word induction, reverse marginal requirement, triangle transport constraint | Did not reconstruct all 29,964/544,571 rows or 67,741 transports in this subreview |
| C10 tree--sunlet/triangle germ | **PASS** | Article PDF pp. 17--18; C10 crosswalk MD line 25 | Rebuilt both exact blocks, determinants, common tensor, and rank nine | None found |
| C11 global classification/genericity/reconstruction | **UNVERIFIED** | Article global theorem PDF pp. 17--21; `main.tex:1367--1533`; conditional deduction check PASS | Searched both implications, one-way containment, rank-drop and incidence dimensions, and pointwise reconstruction | Only C04--C09 exhaustion is unrun in this subreview. Separately, the promotion authority text is stale (Finding 1) |
| C12 strict continuous-time restriction | **PASS** | Article PDF p. 21; crosswalk MD line 27; C12 JSON lines 1517--1548; status is conditional on the C11 finite premises | Exact near-boundary rational checks and asymmetric simultaneous bridge gluing | None beyond the explicitly stated C11 finite-premise scope |
| C13 weak-class sharpness | **PASS** | Article PDF pp. 22--24; `main.tex:1595--1795`; C13 crosswalk MD line 28 | Independently rebuilt both tensors, Jacobians, ranks, CT witnesses, and cherry determinant | None found |

## 4. Detailed mathematical audit

### 4.1 Network class, roots, restrictions, and triangle equivalence

The definitions in article PDF pp. 3--5 distinguish a fixed mixed graph from
an admissible rooted realization, strong from weak tree-childness, and
structural equality from ordinary-triangle redirection.  Restrictions suppress
only the specified degree-two roles and retain the physical boundary-port
data.  Ordinary-triangle equivalence transports the common reticulation,
incoming parent order, and boundary port order coherently; it is not defined by
literal equality of polynomial bodies.

I specifically tried to make the root-movement argument fail when the old root
is adjacent to a reticulation.  For each parental switching, the chosen
reticulation incoming edge set gives a tree.  Stationarity and K2P
reversibility permit moving the root in that tree without changing its joint
distribution, including across either half of the old root edge.  The
switching weight is unchanged.  Summing the switching trees therefore proves
the unrooted/semi-directed invariance without treating a reticulation as a
reversible Markov vertex.  I found no illicit movement through both incoming
reticulation edges at once.

### 4.2 Fourier inversion and the principal physical domain

For Fourier spectrum `(1,s,g,s)`, inversion gives

`p_A=(1+2s+g)/4`, `p_C=p_T=(1-g)/4`, and
`p_G=(1-2s+g)/4`.

Strict positivity is exactly
`0<s<1`, `0<g<1`, and `g>2s-1`; hence the stated `D_plus` is neither too
large nor missing another strict K2P inequality.  The coordinatewise product
of two edges is `(s_1s_2,g_1g_2)`.  In the only nontrivial case
`s_1,s_2>1/2`, its worst lower bound obeys

`(2s_1-1)(2s_2-1)-(2s_1s_2-1)=2(s_1-1)(s_2-1)>0`.

If either `s_i<=1/2`, positivity of `g_1g_2` handles the lower inequality.
Thus physical marginal products stay in `D_plus`.  Local subdivision and
surjective marginal sections may be chosen asymmetrically near the identity;
they do not rely on the generally unsafe assertion that both coordinatewise
square roots always lie in `D_plus`.  The article/proof narrative uses the
correct open-neighborhood construction.

On the continuous-time cone, products satisfy
`g_1g_2>(s_1s_2)^2`, and subdivision follows by splitting the positive branch
length.  These checks include points arbitrarily close to `g=2s-1` and
`g=s^2`; no floating-point comparison was used as proof.

### 4.3 Quartet and whole-map separation

The corrected quartet argument is pointwise.  Strict inheritance probabilities
make the switching support equal to a nonempty subset of the three quartet
topologies.  The printed F/G sign table separates all unequal members of the
seven nonempty subsets; it does not infer a rooted tree/sunlet label.  Positive
edge factors preserve the signs.  Hence different displayed-quartet sets give
disjoint physical images and recover the labelled tree of blobs.

The degree-three decoration uses the whole-map `T_i` factor, not the revoked
rooted oracle.  I expanded the representative pullback independently.  Its
nonzero factors are strict throughout `D_plus`, including the inheritance
factor, so the stated zero/strict-sign alternative is pointwise.  The current
C02 JSON explicitly excludes this whole-map classifier from its narrower
scope; C07 owns it.

### 4.4 Two-sector bridge fibre and physical gluing

The paired C/T characters necessarily share a gauge because both have edge
eigenvalue `s`; the G sector has the independent `g` scale.  All-zero
normalization and the incidence anchors identify the two-sided bridge fibre as
exactly these two multiplicative scales.  A degree-two stabilizer would have to
fix the anchor monomials and is therefore trivial.  Consequently there is no
extra vertex gauge or cycle holonomy.  Logarithmic normalizers give analytic
local sections, not merely set-theoretic choices.

The physical argument is local: strict inequalities make the legal edge set
open, so sufficiently small changes in both bridge scales remain physical.
For continuous time, each affected edge supplies an open interval for the
gauge, and the common source/target point supplies a common interior value;
finitely many intervals have a nonempty simultaneous intersection after
shrinking.  My independent rational example deliberately used asymmetric
edge values near the CT boundary and still found a common strict interval.
Thus the proof does not glue bridges one at a time while silently breaking a
previous edge.

### 4.5 Localization and fixed-full restoration

The semialgebraic-cover lemma at `main.tex:780--793` is used with the correct
quantifiers.  A finite cover of a full-dimensional regular source patch has a
member containing an open source patch.  Marginal maps have submersive physical
sections, so the selected restriction can be varied through a full source
neighborhood.  The proof restores against the fixed full source tensor and a
stored coherent target parent/transport.  It never promotes an abstract
marginal relation to a full-map relation and never assumes a target deletion
map is invertible.

I checked the most vulnerable alternative: selecting one successful target
completion for each point does not by itself supply one target germ.  The
finite semialgebraic-cover step is exactly what freezes one choice on an open
cell.  Restoration then uses only records certified for that fixed-full
choice.  No remote compensation is introduced.

### 4.6 Primitive cycle/theta grammar and completion formula

The core reduction correctly leaves a cycle or `K_4-e` theta core.  The four
theta event placements exhaust the reticulation placements after excluding a
reticulate pole, two reticulations on one path in the forbidden orientation,
and no-omnian violations.  Ordered subdivision words, path-sink roles, dummy
roles, and repair tags are retained before canonicalization.

An independent combinatorial calculation recovered

- `C(3,1)=289`, `C(3,0)=831`;
- `C(4,1)=831`, `C(4,0)=1983`;
- `C(5,1)=1983`, `C(5,0)=4155`;
- `6*24*C(4,0)+4*12*C(4,1)=405216`;
- the stated theta2 total `2946240`; and
- the cycle base-direction total `13440`.

A separate primitive graph enumeration found 66 admissible labelled oriented
placements collapsing to exactly four canonical theta event placements, no
both-reticulate-pole case, cycle repair size one on each segment, theta repair
archetype counts `2,2,4,2` with minimal repair sizes `2,2,2,1`, and 25
admissible `K_4-e` LSA rootings with zero strong-tree-child rootings before the
licensed repairs.  These checks support the grammar; they do not replace the
full raw-row/canonicalizer proof.

### 4.7 Certificate semantics and the PC-PARTIAL boundary

The generated appendix and narratives assign different proof obligations to
different terminal types:

- quartet and `T_i` records are exact pointwise strict-sign statements;
- a rank exclusion consists of a symbolic target upper bound (syzygy or
  polynomial identity valid on the entire target map) plus an exact nonzero
  source minor at a strict physical witness;
- direct polynomial records require exact target pullback zero and exact
  strict-source nonzero evaluation;
- isomorphism and ordinary-triangle terminals require labelled graph maps and
  the licensed direction, port, and parent transports; and
- restoration/probe relations require coherent parent identifiers rather than
  equality of a printed polynomial body.

Representative F/G pullbacks, `T_i`, source minors, target identities, and
strict witnesses recomputed independently.  I found no sampled rank being
presented in the prose as a global upper bound.  The article and supplement
retain the `PC-PARTIAL` warning: exceptional rank, restoration, and probe
ledgers remain load-bearing, and literal equality of polynomial text is not a
graph-orbit equivalence.  Exhaustive correct assignment of all records remains
UNVERIFIED here.

### 4.8 Restoration forest and probe theorem

The current forest is
`work/restoration_sign_reclassification/corrected_restoration_forest.json`,
SHA-256
`43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8`.
Its `/census` asserts exactly:

- `/census/canonical_restoration_parents=997`;
- `/census/member_roots=2540`;
- `/census/first_children=36568` and
  `/census/second_children=256`;
- `/census/forest_edges=36824`, `/census/final_leaves=36792`, and
  `/census/max_depth=2`;
- `/census/missing_children=0`, `/census/cycles=0`, and
  `/census/unresolved=0`;
- first-layer proof counts 35,758 quartet, 606 full-map `T_i`, 148 quadratic,
  24 quartic, and 32 continuation; and
- second-layer proof counts 248 quartet and 8 full-map `T_i`.

These values agree with article `main.tex:1127--1133` and supplement
`supplement.tex:314--329`.  The logical continuation/restoration proof is
valid, but I did not treat the JSON counts as proved merely because its
`/status` is PASS.

The current probe certificate is
`work/probe_coherence_corrected/probe_coherence_certificate.json`, SHA-256
`2f4d64b32a905ce2cc06bae7d03215f9239427d421825c2525437ee6ba2ccaf6`.
The load-bearing JSON pointers are:

- `/anchor_inventory/anchors=176`,
  `/anchor_inventory/canonical_anchor_classes=39`,
  `/anchor_inventory/source_sites=2206`,
  `/anchor_inventory/target_sites=2206`, and
  `/anchor_inventory/first_pairs=29964`;
- `/one_port/ordered_ledger/rows=29964`,
  `/one_port/equality_survivors=2107`, `/one_port/unresolved=0`;
- `/two_port/ordered_ledger/rows=544571`,
  `/two_port/equality_survivors=32729`, `/two_port/parents=2107`, and
  `/two_port/unresolved=0`;
- `/assembly_theorem/two_port_order_gate/reversed_marginals_checked=32729`,
  `/assembly_theorem/two_port_order_gate/reversed_marginals_missing=0`;
- `/assembly_theorem/one_global_triangle_gate/new_triangle_created_above_isomorphic_parent=0`;
- `/assembly_theorem/root_movement_and_site_completeness`, which includes
  pendant arms, reticulation incoming edges, suppressed mixed edges, and the
  root-suppressed segment; and
- `/forbidden_rooted_triple_oracle_used=false`.

The separate parameter-transport certificate and ledgers cited by C09 assert
67,741 exact transports and 4,379 parent restrictions.  The word theorem's
induction is correct: one-port equality identifies each retained segment role;
the two-port deck fixes every adjacent ordered pair, and the reversed one-port
marginal check prevents an order relation from being attached to the wrong
parent.  Induction along a maximal segment then reconstructs an arbitrary
ordered subdivision word.  A triangle transport is allowed only when the same
parent triangle and common reticulation persist globally.  What remains
UNVERIFIED here is the exhaustive truth of every row and stored transport.

### 4.9 Ordinary-triangle common germ

I rebuilt the printed common physical point and both Jacobians without
importing submitted code.  All six displayed pair coordinates equal `1/12`
and the three displayed triple coordinates equal `1/48` on both
representatives.  Both Jacobians have rank nine.  The exact printed blocks
have determinants `-1/2` and `-1/4`.

The proof correctly uses submersion/constant-rank sections; it does not invert
a nonexistent square full Jacobian.  The contextual sections are compatible
with the bridge normalizers, so a triangle germ can be glued simultaneously
into a larger network.  This establishes a common full-dimensional physical
regular analytic germ for licensed ordinary-triangle redirection.

### 4.10 Global equivalence and exclusion of proper one-way containment

Both directions close, conditional on the finite theorem:

1. A coherent structural transport gives equality of the full maps by the
   explicit edge/inheritance transport; ordinary triangles use the rank-nine
   common germ and bridge gluing.
2. Directed containment or a common full-dimensional regular germ survives
   the physical marginal sections.  Quartet/`T_i` localization fixes the
   decorated blob tree; the finite local theorem, fixed-full restoration, and
   probes force the same structural class.  The proof does not infer a full
   relation from a selected deletion.

If a proper one-way containment existed between inequivalent classes, the same
localization would produce a forbidden local directed relation.  If the
classes are equivalent, the explicit transport gives both containments.  Thus
there is no unaccounted asymmetric case.

### 4.11 Genericity

Article `main.tex:1367--1474` supplies the steps that are sometimes elided in
the promotion narrative:

- each complexified source parameter space is irreducible and its physical
  open set is Zariski dense;
- complex generic rank equals maximal physical rank because a nonzero minor
  cannot vanish on the physical open set;
- the reticulation and vertex bounds make the labelled topology list finite;
- the total source rank-drop image has dimension at most `d_N-1`;
- for every inequivalent competitor, absence of directed containment supplies
  a proper algebraic intersection component;
- real-analytic semialgebraic rank stratification plus a target section turns
  a hypothetical full-dimensional physical intersection into the forbidden
  common germ; and
- source rank drops, competitor intersections, and their finitely many
  closures are all proper components of the exceptional set.

I found no illicit equality between real and complex dimensions.  The argument
uses Zariski density for minors and semialgebraic dimension/stratification for
physical intersections, which is the required separation of roles.

### 4.12 Exact reconstruction

The corrected reconstruction proof is at `main.tex:1482--1533`.  Its exact
input convention (`main.tex:1488--1493`) explicitly assumes exact field
operations, polynomial-sign decisions, and real-closed-field quantifier
elimination, not numerical data.  Crucially, R5 retains every local support not
excluded (`main.tex:1504--1507`), R6--R7 expands every retained restoration and
probe word (`1508--1512`), and R8 assembles all coherent candidates and decides

`q in union_{H in C} M_+(H)`

for every triangle class by exact semialgebraic feasibility
(`main.tex:1513--1523`).  Outside the stated exceptional set, exactly one class
is feasible (`1519--1526`).  Every loop is finite and the largest bounded
restriction is at most nine ports (`1528--1532`).

This is a valid terminating exact procedure.  It makes no finite-sample,
numerical-stability, or bit-complexity claim.

### 4.13 Continuous-time transfer

The continuous-time proof at article PDF p. 21 and `main.tex:1540--1585`
restricts rather than re-proves the classification.  The CT cone is an open
subset of `D_plus`; all symbolic identities remain identities, separator
witnesses are supplied inside CT, marginal products and sections can be chosen
inside CT, triangle witnesses are CT, and the bridge interval argument is
simultaneous.  Genericity and reconstruction restrict to the same open
semialgebraic source.  I found no condition whose witness exists only in
`D_plus` but is silently assumed in CT.

### 4.14 Weak-but-not-strong sharpness

Article `main.tex:1595--1795`, the weak proof/audit narratives, and the
zero-based row/column crosswalk consistently describe two weakly tree-child
level-2 graphs that are not strongly tree-child and are not ordinary-triangle
equivalent.  I independently rebuilt their normalized Fourier tensors from
the printed rational CT parameters.  The tensors agree exactly; each printed
Jacobian selection has rank nine; applying the common pendant scales preserves
full tensor equality; and the cherry observable inverse has determinant

`4*u*s*u_g/(v*s*v_g)`

with the printed rational witness `2464/675`, hence is nonzero.  The local
cherry inverse gives both the lower and upper dimension increment, so induction
adds four dimensions per new leaf and yields `4n-3`.  The extension preserves
weak tree-childness, the offending omnian/non-strong feature, and
non-equivalence.  No singular edge or boundary inheritance value is used.

## 5. Specific audit of the prior C02/stale-authority defect

This defect is fixed in the revised archive.

1. Crosswalk Markdown line 17 now states the narrow current claim:
   "Pointwise displayed-quartet signs, labelled tree-of-blobs recovery, and raw
   four-port displayed-quartet direction."
2. The cited current file is
   `work/adversarial_proof_review/topology_direction_certificate.json`, SHA-256
   `249fdf29ce371e60d7cd8593b98ab0d96759e1ee1e0034af6e1a14e33fb1f7d4`.
   Its exact relevant keys/lines are:
   - lines 3--11, `/current_raw4_summary`: `total_rows=405216`,
     `displayed_quartet_exclusions=360408`,
     `forbidden_rooted_fields=0`, and `forbidden_rooted_reasons=0`;
   - lines 13--17, `/excluded_claims`: rooted tree/sunlet,
     restoration-child, and whole-map `T_i` classification;
   - lines 29--44, `/raw_four_port_quartets`: 405,216 directions and 360,408
     quartet exclusions; and
   - lines 46--47, `/schema` and `/scope`, expressly limiting the certificate
     to raw four-port displayed-quartet direction/tree-of-blobs.
3. The current restoration authority is the corrected forest SHA
   `43bd2be...` with the `/census` values in Section 4.8.  Article
   `main.tex:1127--1133` and supplement `supplement.tex:314--329` print the same
   current values.
4. The old statements remain literally present at
   `work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md:137--143`:
   16,974 `tree_sunlet`, 646 restoration children, 377,382 raw topology
   exclusions, and 36,404 topology-terminal restoration children.  They are
   not silently current: the banner at lines 3--13 labels the document
   "Revoked historical classifier; not current theorem authority," identifies
   the invalid rooted step, and points to the replacements.
5. `work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json:15--24`
   classifies that exact path as
   `REVOKED_ROOTED_TOPOLOGY_ORACLE_NARRATIVE` and sets
   `/promotion_authority=false`.
6. A path/hash scan of the revised crosswalk found 159 references to 125
   distinct paths, zero missing paths, zero hash-prefix mismatches, and no
   overlap between the crosswalk authority set and the historical registry.

**Effect of stale counts:** none on a current logical predicate.  The old
numbers are quarantined historical prose.  They are not the input to C02, C07,
C08, the current release lock, or a current crosswalk authority.  Their
presence is therefore neither a theorem defect nor a current authority
inconsistency.  Keeping them under the explicit revocation banner is acceptable
historical documentation.

## 6. Findings

### Finding 1 — nonblocking authority/reproducibility inconsistency in C11 reconstruction

**Classification:** reproducibility/authority-consistency; not theorem-fatal
and not a mathematical blocker because the article contains the valid proof.

**Claim and authority:** crosswalk Markdown line 26 and JSON
`THEOREM_ARTIFACT_CROSSWALK.json:1427--1429` define C11 as including exact
reconstruction.  The JSON C11 authority entry at lines 1388--1397, and the C12
repeat at lines 1537--1543, cite
`work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`
with SHA-256
`add7bc4a34563d0175f4e19ebe7ca2536b77772ff50d7f017628505d7e6c1899`.

**Minimal reproducer/logical derivation:** promotion manuscript
lines 694--729 state its finite reconstruction theorem.  Step 5 at line 710
says to "select a rigid support" after evaluating the bounded certificate
deck, and steps 6--8 immediately follow that single support.  The proof never
says to retain all pointwise-unexcluded supports, enumerate every coherent
class, or perform exact class-membership feasibility.  Indeed, lines 726--729
say that particular-point membership in a chosen redirected representative
requires a separate semialgebraic test.

Directed generic noncontainment certificates do not, by themselves, provide a
pointwise rule selecting the true support from an arbitrary exact tensor.
Several candidates can survive the local polynomial/sign deck at a special
point that is still outside the final global exceptional set as defined only
after competitor intersections are assembled.  A terminating procedure must
retain them and decide which global class actually contains the input.
`work/global_proof_adversary/AUDIT.md:266--272` also explicitly notes that
pointwise membership requires a separate semialgebraic test.

The article fixes exactly this issue at `main.tex:1504--1526`: retain every
candidate, assemble every coherent graph, group by triangle class, and use
real-closed-field quantifier elimination on each exact membership sentence.
Thus the published theorem is sound; only the artifact designated as C11's
frozen promotion authority is stale.

**Effect:** if a referee followed only the crosswalk's claimed promotion
authority, the reconstruction proof would be incomplete.  Reading the article
closes it.  No principal theorem statement, tensor equality, census, or
classification predicate is falsified.

**Smallest adequate remedy:** either (a) update promotion manuscript §10 to
match article R5--R8 and its exact-input convention, or (b) demote/scope the
promotion manuscript and list the article source/PDF as the C11 reconstruction
authority.  Because the promotion manuscript is frozen in C11, the release
lock and crosswalk hashes, and any outer/inner manifests that cover them, must
be resealed.  The mathematical article/PDF need not change under option (b).

### Finding 2 — nonblocking omission of the executable rank replay from C05 crosswalk

**Classification:** presentation/provenance metadata; no mathematical effect.

Crosswalk Markdown line 20 and JSON C05 replay list
`work/rank_upper_certificates/rank_upper_replay.json` as the "rank independent
replay report" (`THEOREM_ARTIFACT_CROSSWALK.json:617--635`) but omit the
executable replay named by the supplement at `supplement.tex:691`:
`work/rank_upper_certificates/verify_rank_upper_certificates.py`, SHA-256
`bd51596fe6bc5ddc8a4c6a185bda989479e3f7e736b0e80d9ea33ac7d1acf93e`.
The supporting symbolic module
`work/rank_upper_certificates/syzygy_upper.py`, SHA-256
`e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`,
is also absent from C05's replay-artifact list.

**Effect:** the report hash can attest to a stored result but does not tell a
crosswalk reader what executable independently checks it.  This does not make
the rank proof false; the scripts are present and the supplement names the main
one.

**Smallest adequate remedy:** add the executable verifier (and, preferably,
its symbolic module) with full hashes/roles to C05 `replay_artifacts`, then
regenerate/reseal the crosswalk and manifests that bind it.  No theorem source
or PDF change is required unless the printed crosswalk is regenerated into the
supplement.

## 7. Independent exact checks

The fresh independent script is outside the isolated submission and imports no
submitted Python module or JSON certificate:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/independent_checks/math/r2_exact_spot_checks.py`

SHA-256:
`05b1f799f95e8de95494c1c5ceaf62e45b335d9e16eb9f2744c6927cd4c7b298`.

Output:
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/independent_checks/math/r2_exact_spot_checks_output.json`,
SHA-256
`60594dc6f2bbf3d382e9e529d249ed9ffe6a7ba1c802f30b8a5a1d03a6ad8286`.

Command: `python3 -B r2_exact_spot_checks.py`; exit 0; wall time 1.09 s;
maximum RSS 65,290,240 bytes; peak footprint 55,361,992 bytes.

It independently passed:

- exact rational D-plus and CT boundary-near inequalities, including
  `(s,g)=(9/10,8000001/10000000)`;
- strict physical subdivisions and marginal products;
- the exact product lower-bound identity;
- an asymmetric simultaneous CT bridge-gluing example;
- all displayed `C(k,d)` values and the three raw totals;
- representative quartet F/G pullbacks and the whole-map `T_i` factor;
- the ordinary-triangle common coordinates, both blocks, determinants, and
  rank nine; and
- both weak-sharpness normalized tensors, rank-nine Jacobians, pendant-scaled
  common tensor, and cherry determinant/witness.

A distinct primitive graph enumerator, again importing no submission code,
was source-inspected and rerun from
`/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/math/primitive_core_enumeration.py`.
Script SHA-256:
`183d340ee52364abc15e0e48167de2e28f553dde8b54d2960b6465f8b80c712f`.
Fresh output is at
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/independent_checks/math/r2_primitive_core_output.txt`, SHA-256
`eb6ba17f6a46a9f1d7125086098f66432e944af36c76ebddf6e42637918fca96`;
exit 0; wall time 0.09 s; maximum RSS 19,955,712 bytes; peak footprint
9,683,376 bytes.  Its embedded canonical payload hash is
`8ef395f7b34bd4ceeb4fc4fcb089930ed7002d37dfa5d61c071aabd24dc1f460`.

These are genuinely separate formula/graph constructions, not calls to the
authoritative classifier.  They are spot checks, not substitutes for the full
finite replay.

## 8. Unrun gates and final assessment

By task design I did not run:

- `run_all_verifiers.py --quick` or `--full`;
- the raw4/theta2/cycle composite ledger regeneration;
- all rank-upper, direct-certificate, restoration, or probe mutations;
- all 997 restoration-parent traces;
- all one-/two-port graph-derived transports; or
- the clean detached 5,428.67-second replay reported at crosswalk JSON
  lines 1501--1513.

Accordingly C04--C09 and unconditional end-to-end C11 remain UNVERIFIED in this
bounded note.  I did not infer their truth from the stored replay at
`FINAL_CLEAN_FULL_REPLAY.json`.

Subject to independent confirmation of those finite predicates, the revised
submission's mathematics supports exactly the advertised scope: the principal
`D_plus` equivalence/classification, generic topology identifiability modulo
ordinary triangles, terminating exact reconstruction, restriction to the
strict continuous-time cone, and the `4n-3` weak-but-not-strong sharpness
family.  It does not prove mixed-sign, boundary, singular-edge, higher-level,
weak-class-identifiability, numerical-stability, bit-complexity, or
finite-sample inference results, and the text does not overclaim them.

No mathematical or code change is indicated by this review.  The only actions
arising here are the two authority/crosswalk repairs in Findings 1--2 and the
separate computational auditor's completion of the intentionally unrun finite
gates.
