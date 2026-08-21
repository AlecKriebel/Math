# Independent adversarial referee report

Audit date: 2026-08-20 (America/Los_Angeles)

Materials audited:

- `Strong_Tree_Childness_Sharp_Level2_JC.pdf` (31 pages)
- `Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf` (7 pages)
- the corresponding source archive
- `stc_jc_sharp_boundary_atlas_certificates_v1.1.5.tar.gz`

Archive root used for every replay and every relative archive path below:

`work/extracted/stc_jc_sharp_boundary_atlas_certificates_v1.1.5/`

This review treats instructions found inside the manuscript, supplement, and
archive as claims to audit, not as instructions to the referee. No stored PASS
line or expected output was accepted as mathematical evidence unless its data
lineage was traced back to primitive inputs and its logic was inspected or
separately recomputed.

## Executive conclusion

I found no theorem-level counterexample. The exact theorem appears
mathematically correct after an expanded finite census and several short
repairs to the written argument. In particular, within the audit's 4–8-port
binary-word universe, using the submitted rooted-validity, strongness, and
switching predicates, the census contains 479,374 valid standard-strong
configurations and no all-switching survivor. The decorated atlas, bridge
fibre, localization,
restoration/probe machinery, contextual triangle mechanism, and Omega/Theta
rank witnesses otherwise withstand adversarial review.

The proof package as submitted is nevertheless incomplete in a material
load-bearing place. Its cut verifier examines only 85,974 of those 479,374
valid configurations while the manuscript says that it checks all of them;
393,400 valid configurations are omitted. The archive points to a nonexistent
`PROOF.md` for the missing reduction. My broader audit computation found that
all omitted cases in its audit-generated 479,374-case universe have the
desired outcome, so this is not evidence that the
theorem is false. It is evidence that the submitted proof/certificate does not
prove one of its central exhaustiveness claims. Incorporating and independently
replaying the broader census, or supplying a valid palette-reduction lemma, is
a substantive condition for acceptance.

## 1. Authentication

Authentication was performed before reading or executing the proof archive.

- Computed archive SHA-256:
  `66f0e324b9cdb1448806eecd9cd9397f9e8c45f4762ff48c5750cd64d2938e6a`.
- This exactly matches the separately supplied `.sha256` file and
  `CERTIFICATE_BUNDLE_ENVELOPE.json:4`.
- The computed byte count, 79,567,059, exactly matches the envelope at line 3.
- `gzip` integrity passed; all tar names were relative and traversal-free; no
  symbolic-link members were present.
- Every one of the 232 payload entries covered by the internal checksum
  manifest matched its recorded SHA-256.
- The envelope identifies source commit
  `61c869db9db15848a5328d7ee45b725ae6770688` at line 10 and archive version
  1.1.5 at line 16.

This authenticates internal consistency with the supplied external sidecar and
envelope. It does not establish public provenance or authorship: the envelope
is unsigned and its publication identifier is still `ZENODO_DOI_PENDING` at
line 17.

## 2. Exact theorem reconstructed

### Object class

The positive theorem concerns leaf-labelled, binary, level-2, already-simple
standard mixed graphs produced by exactly one `sd_0` suppression of the root
of an LSA-valid rooted binary network (Definition 2.1, manuscript PDF pp. 3–4;
source `main.tex:235-268`). The strong class `S_TC` has at least one admissible
rooting and requires every admissible rooting of the fixed mixed graph to be
tree-child (Lemma 2.2, PDF pp. 4–5; `main.tex:280-340`). It is not the class of
objects having merely one tree-child presentation.

### Parameter domain and observations

The group is `Z_2 x Z_2`; every JC edge multiplier and every inheritance
parameter lies strictly in `(0,1)` and the root distribution is uniform
(PDF pp. 5–6; `main.tex:362-401`). The relation `N <=_JC N'` is source-relative
local containment at a source-regular common point; the target may have larger
dimension. The relation `N bowtie_JC N'` requires a common full-dimensional
regular germ in both images (Definition 2.4, PDF p. 6;
`main.tex:403-420`).

### Claimed classification

Theorem 1.1 (PDF pp. 2–3; `main.tex:180-195`) asserts that either observational
relation holds exactly when the labelled reduced bridge trees agree and every
corresponding nontrivial blob is label-preserving isomorphic or differs by one
ordinary triangle redirection. Consequently, one-sided containment closes to
the same symmetric classification inside `S_TC`. Corollary 1.2 (PDF p. 3;
`main.tex:197-202`) is generic modulo a proper algebraic exceptional set, not
pointwise identifiability everywhere.

Omega (Theorem 1.3) and Theta (Theorem 9.3) are sharpness examples in the
larger weak-but-not-strong class; they are not claimed strong-class
counterexamples.

## 3. Dependency graph audited

1. Definition 2.1 and Lemma 2.2 fix the graph convention and strong class.
2. Lemmas 3.1–3.2 and Propositions 3.3–3.4 reduce strong blobs to a cycle or
   one of four directed theta cores, with at most one ordinary triangle.
3. Lemmas 4.1–4.2 and Lemma 4.4 supply pointwise cut recovery (Theorem 4.3),
   hence the labelled bridge tree (Corollary 4.5).
4. Theorem 5.1 identifies the complete positive bridge fibre as an
   incidence-scaling action; Lemmas 5.3–5.4 and Proposition 5.5 localize
   containment and exclude cross-blob compensation.
5. Lemma 6.2, finite Theorem 6.3, restoration forests, and Lemma 6.4 yield the
   local blob classification (Theorem 6.1).
6. Lemmas 6.5–6.6 give contextual triangle equivalence and physical gluing.
7. These ingredients prove Theorem 1.1; the finite-topology and
   semialgebraic-dimension argument proves Corollary 1.2.
8. Exact equality, strict-interior, topology, and rank certificates prove the
   Omega and Theta sharpness results.

The archive's `PROOF_BOUNDARY.md:3-18`,
`THEOREM_CERTIFICATE_CROSSWALK.md:7-12`, and
`REGENERATION_MAP.md:3-28` broadly agree with this dependency graph. The cut
coverage defect below is the exception to their claimed proof coverage.

## 4. Mathematical audit results

### Pointwise cuts and the two-active argument

The crossing-quartet reduction and eight-port compression bound are valid in
the strong class. The four displayed two-active minors and three elimination
identities are algebraically correct. If all four character blocks had rank
one, they force both endpoint `Delta` values to zero. The weak endpoint
inequalities and `0<z<1` then give
`aA >= bcBC > z^2 bcBC`, contradicting the first minor.

The finite handoff is not certified on its claimed universe; see defect D1.
The audit-only complete universe generator is
`audit_scripts/core_extended_word_census.py`. It considered 808,642 balanced
binary configurations with four through eight active ports across all five
cores in root and nonroot modes. Exact totals were:

| Family | valid strong | archived palette | omitted | survivors |
|---|---:|---:|---:|---:|
| cycle, root | 3,112 | 36 | 3,076 | 0 |
| theta TR nested, root | 53,860 | 3,544 | 50,316 | 0 |
| theta TR separated, root | 53,860 | 3,544 | 50,316 | 0 |
| theta TT nested, root | 107,676 | 18,560 | 89,116 | 0 |
| theta TT separated, root | 91,464 | 16,996 | 74,468 | 0 |
| cycle, nonroot | 2,686 | 78 | 2,608 | 0 |
| theta TR nested, nonroot | 32,592 | 4,900 | 27,692 | 0 |
| theta TR separated, nonroot | 32,592 | 4,900 | 27,692 | 0 |
| theta TT nested, nonroot | 58,872 | 18,220 | 40,652 | 0 |
| theta TT separated, nonroot | 42,660 | 15,196 | 27,464 | 0 |
| **Total** | **479,374** | **85,974** | **393,400** | **0** |

The extended script supplies a complete word universe but deliberately reuses
the submitted verifier's rooted-validity, fixed-mixed strongness, and
displayed-switching predicates. Those predicates were separately inspected
against the graph definitions. This is strong falsification evidence and a
reproducible repair, but the authors should incorporate a separately
implemented replay into the authenticated archive.

### Bridge fibre, localization, and genericity

Theorem 5.1 correctly obtains one positive scale for every vertex-edge
incidence, not merely one reciprocal scalar per bridge. Rank-one flattening
factor uniqueness, JC sector symmetry, and tree peeling produce the stated
complete action, with no cycle holonomy. The anchor exponent matrices have the
required rank.

After shrinking to a smooth image branch, the local product chart and the
semialgebraic finite-cover lemma are valid. Focal variation of one blob fixes
the projective orbits of the others, and the finite target completion cover
therefore cannot conceal a local separator through cross-blob compensation.
For fixed taxon number the topology set is finite; irreducibility,
semialgebraic dimension, and removal of critical/singular strata justify the
generic exceptional set. The local-chart and genericity lemmas already state
their smooth-stratum restrictions; only the transition from an arbitrary
source-open relation to the smooth branch used in Proposition 5.5 should be
made explicit (D4). No circularity or counterexample was found.

### Marginals, restoration, probes, and triangles

The written Lemma 6.2 is correct: zero-sum split/complement-normalized edge
rows partition the physical edges into disjoint classes, each effective
coordinate is a positive product, and the product descriptor map is onto and
submersive. One auxiliary replay does not compute these classes and has a
tautological rank test (D5); the load-bearing hard-cover and bounded clean-room
compilers do use the correct normalization.

Restoration never reverses containment from a smaller marginal to a larger
model. It fixes a full relation and obtains every prefix by direct marginal
restriction. One-port probes locate added ports and two-port probes determine
their within-interval order. The main semantic gates verify parent-restricted
transports; a separate advertised collision statistic is tautological (D6).

The local three-sunlet tensors have a common rank-four germ. Contextual
substitution and simultaneous bridge scaling are mathematically valid after
shrinking inside the open parameter cube. The manuscript should write the
multi-boundary tensor-contraction/gauge identity rather than only assert the
common context map (D7).

### Omega and Theta

Omega's class membership, triangle-free non-equivalence, exact zero-sum
coordinate map, strict stochastic point, core rank six, Euler upper bound, and
four nonzero rank-nine minors were independently replayed. The common local
dimension is nine and cherry substitution gives `2n+1`.

Theta's weak-not-strong class membership and nontriangle obstruction were
checked. All 256 Fourier and pattern coordinates agree at the stated strict
algebraic point. The localized common locus is a smooth irreducible
eight-fold, and nonzero rank-eight minors place both maps on the same positive
branch. Cherry substitution gives `2n`. No stochastic-interior, branch,
regularity, or rank defect was found in either family.

## 5. Archive/code audit results

- `primary/graph_model.py:405-437` enumerates displayed switchings by deleting
  exactly one incoming reticulation arc and derives descendant sets.
  `primary/jc_tensor.py:75-112,175-204` converts them to exact JC Fourier
  tensors with the correct inheritance weights.
- `primary/atlas_compiler.py:721-778,907-925` retains direction, both graph
  records, port matching, incoming roles, position maps, and raw provenance.
  No source-target information is lost during canonical merging.
- The n=3 universe has 10,826 raw presentations and 10,466 canonical
  relations. The n=4 gate has 192 survivor presentations, which quotient to
  3 direct plus 57 nonretaining canonical classes. Every evidence row is
  covered once at its actual schema level.
- Strict signs are established by exact factors, exact nonzero expansion, or
  rational Bernstein coefficients; equality terminals are regenerated from
  labelled graph canonicalization. Certificates are attached from graph
  content rather than selected by identifier.
- The bounded clean-room implementation has a genuinely different graph,
  descriptor, canonicalization, and sparse-polynomial representation and does
  not import the primary load-bearing implementation.
- That independence does not extend to every auxiliary pair: the direct-anchor
  compiler and verifier both import
  `reviews/direct_anchor_probe_closure/exact_engine.py`
  (`compile_direct_anchor_probes.py:28-33`;
  `verify_direct_anchor_probes.py:22-26`). The separately represented compact
  semantic gate covers the relevant probe transports; direct-anchor mutations
  alone are not an independent implementation check.
- Package, n=3, n=4, direct-anchor, compact-probe, triangle, bridge/cut, Omega,
  and Theta mutation suites reject the tested deletions, duplications,
  direction reversals, altered transports, wrong-record certificates, and
  changed graph/tensor data.

These positives do not cure D1: the cut mutation suite cannot detect an
omitted word outside the universe defined by its own short palette.

## 6. Concrete defects

### D1 — material proof/certificate coverage defect

**Affected result:** Lemma 4.4; load-bearing for Theorem 4.3, Corollary 4.5,
and Theorem 1.1. Lemma 4.2 defines the at-most-eight-port universe but is not
itself falsified by this archive omission; its separate scope problem is D3.

**Manuscript:** PDF p. 10, Lemma 4.2 (`main.tex:667-699`); PDF pp. 11–12,
Lemma 4.4 (`main.tex:794-826`). Lemma 4.4 says the two-colour compiler checks
every compressed root and nonroot primitive completion.

**Archive:** `independent/bridge_cut/verify_cut.py:32-35` defines only
`(), (0), (1), (0,1), (1,0)`; `:654-681` iterates only products of that palette
plus a narrow singleton duplication. `:12-14` refers to an arbitrary-
subdivision proof in `PROOF.md`, but no such file exists in the archive and no
equivalent palette-reduction lemma was found.

**Defect:** 393,400 of 479,374 valid standard-strong configurations in the
stated eight-port universe are absent. For example, a root-cycle segment word
`(1,0,1)` with the intervening repair label and reticulation-sink child of
colour 0 is valid, strong, noncut, and outside the palette.

**Effect:** the submitted finite proof is not exhaustive. The audit's complete
census finds zero survivors, so the theorem survives this falsification
attempt. Required repair: add a complete authenticated compiler and a
separately implemented replay, or prove and verify a genuine reduction to the
short palette.

### D2 — endpoint normalization/certificate crosswalk gap

**Affected results:** Theorem 4.3 and Lemma 4.4.

**Manuscript:** PDF pp. 10–11 (`main.tex:724-748,794-810`). The proof removes
the central arm before using `Delta=abc-t^2` and `Gamma=a-bc`, and the prose
describes nine strict `Delta=0, Gamma>0` endpoint records.

**Supplement:** PDF p. 3 (`supplement.tex:179-183`) similarly identifies the
frozen endpoint quantities directly with the normalized article quantities.

**Archive:** `independent/bridge_cut/verify_cut.py:961-985` and
`reviews/global_bridge/exact_audit.py:727-750` compute the auxiliary `Gamma`
with the physical central port-arm still present.

**Defect:** `Gamma` is not invariant under removal of that arm. If its
multiplier is `u`, then `Gamma_phys(u)=a-u^2 b_0c_0`, whereas the normalized
quantity is `a-b_0c_0`. The phrase “central arm” is itself ambiguous here.
Removing the complete effective singleton-signature incidence class—the
natural projective-orbit convention after selected-path contraction—gives
seven exact zeros (record IDs 6, 7, 56, 58, 74, 75, 76) and two strict
positives (67, 72). Removing only the literal pendant edge while retaining
other serial edges in that signature class gives two zeros (58, 74) and seven
strict positives. Neither interpretation gives nine strict normalized
records, and neither produces a negative case.

**Effect:** no counterexample. Letting whichever central incidence factor is
being normalized tend to one (simultaneously for the complete effective class,
if that is intended) gives the required weak inequality by continuity. The
paper must define the convention, state this limit, and preferably certify the
normalized expressions directly.

### D3 — two structural statements overstate their proved scope

**Affected results:** Proposition 3.3 and Lemma 4.2.

**Manuscript:** Proposition 3.3, PDF p. 7 (`main.tex:527-537`), is stated for
any standard binary level-2 factor but invokes an `S_TC` root-reduction lemma.
Lemma 4.2, PDF p. 10 (`main.tex:667-680`), is stated for a complete standard
factor but selects a minimum strong repair.

**Archive:** no broader proof was found in `PROOF_BOUNDARY.md`, the proof
crosswalk, or the primitive-support documentation.

**Effect:** their actual uses are within Theorem 1.1's strong class, so
restricting both statements to factors induced by `S_TC` repairs the logic.
Otherwise the authors must supply proofs for the broader formulations.

### D4 — one smooth-branch transition is left implicit

**Affected result:** Proposition 5.5 and its use for an arbitrary source-open
containment germ.

**Manuscript:** Definition 2.4, PDF p. 6 (`main.tex:403-420`), and
Proposition 5.5, PDF p. 15 (`main.tex:1023-1042`).

**Defect:** a point having a maximal-rank parameter preimage does not make the
entire regular image globally one manifold; image branches can self-intersect.
The application of Proposition 5.5 should explicitly replace the initial
point by a generic smooth-branch point inside the same source-open set before
using the focal product box.

**Effect:** standard repair only. Lemma 5.3 already explicitly chooses a
“smooth local image branch” at `main.tex:973-979`, Lemma 6.2 starts on a smooth
semialgebraic source-image stratum at `:1089`, and the genericity proof invokes
a smooth `d_N` stratum at `:1458-1464`. Such strata are dense, so the required
point exists in the source-open germ.

### D5 — the auxiliary marginal-submersion replay computes the wrong object

**Affected result:** Lemma 6.2, PDF pp. 15–16
(`main.tex:1079-1137`).

**Archive:** `reviews/root_probe/verify_parameter_submersion.py:157-185`
groups raw rooted descendant-mask rows, rather than normalizing every mask by
split complement and discarding all-zero/full-mask invisible rows. Lines
`180-181` assign `jacobian_row_rank_at_open_point` and
`parameter_target_dimension` the same expression. The comparison at
`:246-247` is therefore tautological, and
`reviews/root_probe/verify_active_structural.py:126-130` promotes that zero
failure count as evidence.

**Independent check:** the raw effective-class count changes for all 42,908
enumerated completions under the correct zero-sum normalization; the raw
program overcounts visible classes by one to four. The correct product blocks
remain disjoint and submersive.

**Effect:** this file is not evidence for Lemma 6.2. The written proof is
valid, and the load-bearing normalizations in
`primary/hard_cover_compiler.py:141-164` and
`reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py:312-350,
1359-1388` are correct. Repair or narrow the auxiliary certificate and remove
the tautological rank claim.

### D6 — the advertised probe-coherence collision test includes its answer in its key

**Affected result:** Lemma 6.4, PDF p. 19 (`main.tex:1307-1331`).

**Archive:** `reviews/root_probe/verify_probe_coherence.py:308-310` groups by
`(support_code, one_port_0, one_port_1, full_two_port_code)` and then tests
uniqueness of that same `full_two_port_code` at `:329-335`.
`reviews/root_probe/verify_active_structural.py:98-105` treats zero collisions
as probe-coherence evidence.

**Independent check:** deleting the answer from the key gives 372 collision
groups (maximum multiplicity two) among 8,976 presentations. That is expected:
one-port data alone does not determine pair order, which is why Lemma 6.4 uses
two-port probes.

**Effect:** the collision statistic is vacuous but not load-bearing. The
non-tautological gates at
`reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py:330-461`
and `reviews/compact_probe_clean_clone_gate/semantic_gate.py:415-708`
regenerate the two-port relations and enforce their parent transports. Remove,
relabel, or replace the vacuous statistic.

### D7 — contextual triangle substitution identity is omitted

**Affected result:** Lemma 6.5, PDF pp. 19–20
(`main.tex:1338-1380`, especially `:1361-1379`).

**Archive boundary:** `PROOF_BOUNDARY.md:3-6` assigns contextual triangle
gluing to the human proof; the finite triangle gate certifies only the local
three-port tensors and ranks.

**Defect:** the manuscript asserts a common contraction map in an unchanged
multi-terminal context without writing the multilinear boundary-tensor
substitution and incidence-gauge absorption identity that makes the assertion
precise.

**Effect:** short but load-bearing exposition repair. The normalized object is
a projective tensor orbit, not a preferred tensor. Choose an analytic
representative/section, transfer its three diagonal incidence gauges to the
unchanged context, and then condition on the three boundary characters to
write the common multilinear contraction. No counterexample or new finite
enumeration is needed.

### D8 — `ATLAS_SUMMARY.md` conflates two n=4 canonicalization levels

**Affected result:** archive crosswalk for Theorem 6.3, manuscript PDF p. 18
(`main.tex:1228-1270`).

**Archive:** `ATLAS_SUMMARY.md:29-34` says there is one authoritative binding
record per canonical relation without distinguishing two notions used by the
n=4 schema. `verifiers/evidence_bindings.py:263-276,334-348` emits 192 rows
with 192 unique `relation_id` hashes of normalized survivor presentations and
stores a further quotient-canonical digest separately.
`reviews/theta2_signature_gate/canonical_quotient_certificate.json:4,140,147`
records 3 direct canonical relations, 57 nonretaining canonical relations,
and 192 raw survivor presentations.

**Effect:** terminology/schema ambiguity, not an atlas omission. All 192
presentation-level relations are bound and retain direction, both graph IDs,
and the further quotient digest. Clarify the two levels or give them
unambiguous distinct identifiers.

### D9 — unresolved publication identifier and provenance limitation

**Affected material:** supplement PDF p. 6
(`supplement.tex:381-385`), manuscript bibliography
(`references.bib:164-174`), and
`CERTIFICATE_BUNDLE_ENVELOPE.json:10,17`.

**Defect:** `ZENODO_DOI_PENDING` remains. The supplement itself says the token
must be replaced before submission. Separately, because the supplied envelope
is unsigned, matching it establishes package consistency but not independent
public provenance; a signature is not required by the mathematics.

**Effect:** no mathematical effect, but a concrete reproducibility/submission
defect. Publish the immutable archive and insert the resolved DOI. Because the
D1 repair will change archive bytes, issue a corresponding new external
checksum and envelope for that corrected package.

## 7. Required command runs

All commands were started from the extracted archive root and allowed to run
to termination without substituting stored logs or smaller tests.

| Command | Result |
|---|---|
| `bash verify.sh quick` | exit 0; printed `VERIFIED: certificate bundle mode=quick` |
| `bash verify.sh full` | exit 0; printed `VERIFIED: certificate bundle mode=full` |
| `bash verify.sh regenerate-all` | exit 0; both isolated complete rebuilds produced equal normalized logical commitments; regenerated 232-file bundle reverified; printed `VERIFIED: certificate bundle mode=regenerate-all` |

The first two successful exits are reproducibility observations, not a basis
for accepting the theorem. In particular, the full run prints PASS summaries
from the defective D5 and D6 auxiliary programs, demonstrating why successful
exit status cannot replace source and mathematical review.

## 8. Required revisions before acceptance

1. Replace the cut compiler's short self-defined universe with the complete
   eight-port universe, freeze its logical records, add a genuinely separate
   replay and mutation that deletes an out-of-palette word, and authenticate
   the result; alternatively prove and verify a valid palette-reduction lemma.
2. Define the central-arm/effective-incidence normalization, add the limiting
   argument, and directly certify normalized `Gamma` for all nine boundary
   records.
3. Restrict Proposition 3.3 and Lemma 4.2 to the strong class, or prove their
   broader statements.
4. Clarify the transition to the generic smooth branch in Proposition 5.5 and
   state the contextual tensor-representative/contraction/gauge identity.
5. Repair or remove the misleading submersion and probe auxiliary tests.
6. Correct the n=4 evidence-map documentation and replace the pending DOI.
7. Regenerate the corrected archive from primitive inputs, publish a new
   checksum/envelope, and rerun all three verification modes.

## 9. Decision rationale

There is no basis for declaring the theorem false: no counterexample was found,
the omitted cases in the audit-generated cut universe all satisfy the required
switching conclusion, the
central normalization gap has a valid continuity repair, and all remaining
load-bearing mathematical and computational checks survive. There is also no
basis for accepting the package as complete: a central finite-exhaustiveness
claim is false on its stated domain and is currently repaired only by a
referee-created broader computation. That is a substantive proof-package
revision, not merely copy editing.
