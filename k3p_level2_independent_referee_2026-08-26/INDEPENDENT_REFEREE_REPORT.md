# Independent referee report

**Manuscript:** *Triangle Hypersurfaces and a Sharp Identifiability Boundary for Level-2 K3P Networks*

**Materials reviewed:** article, reader supplement, LaTeX sources, active and historical proof artifacts, producer/verifier/mutation code, and the independent referee package

**Review date:** 26 August 2026 (America/Los_Angeles)

Unless stated otherwise, bare manuscript-section filenames are relative to
`package_copy/proof_package/manuscript/sections/`, other supplied-code paths
are relative to `package_copy/proof_package/`, run-evidence paths are relative
to `package_copy/`, and referee-authored check paths are relative to this audit
directory.

I read both supplied PDFs in full before consulting generated reports, then
inspected the active producers, verifiers, wrappers, and mutations before any
formal package execution.

## Recommendation

**Verdict: not fully assessable.** Confidence in this verdict: **0.91**.

This is not a finding that the theorem is false. I found no in-domain
counterexample, and substantial parts of the mathematics and computation are
strong: the physical-domain algebra, literal tree--sunlet separator, complete
three-leaf `H14` calculation, representative four-port polynomial and rank
obstructions, restoration replay, cut-obstruction algebra, rational Krawczyk
certificate, and all-`n` cherry inverse survived independent checks.

The present package nevertheless does not permit an independent conclusion on
the central classification theorem. Two computer-assisted completeness steps
remain conditional on producer/frozen data:

1. no active bundled command re-enumerates and classifies the full 405,216
   four-port relations, or even the 27,834 post-topology cases, to derive the
   asserted 40 post-filter records: 38 partitioned into fourteen orbits plus
   two pre-lock sink swaps; and
2. the purported independent probe verifier does not reconstruct the graph,
   marginal, quartet, or row-specific tree--sunlet semantics of the 574,535
   one-/two-port rows. It accepts a coherently self-hashed but semantically
   meaningless transport record.

Both steps are load-bearing for the passage from bounded primitive factors to
arbitrary labelled level-2 factors. A complete successful replay of the
current active graph cannot repair those scope limitations, because that graph
starts from the frozen four-port lock and uses the same semantically shallow
probe replay.

The required once-only 44-command regeneration did execute every mathematical
command successfully, but the outer runner ultimately returned failure because
the restoration producer embedded its absolute working directory in a Markdown
report, causing a one-file drift. This is a separate, repairable reproducibility
defect and does not change either major completeness limitation.

I also find a genuine omitted case in the handwritten necessity proof. Equal
bridge splits reconstruct the abstract component-incidence tree but do not
distinguish an ordinary trivalent component from a three-boundary cycle/sunlet.
The proof immediately applies a local theorem stated only for cycle/theta
factors. The manuscript already proves a strict pointwise tree--sunlet
separator that appears to give a short repair, so this is a major proof
omission rather than a counterexample.

If the missing exhaustive four-port producer/verifier and a genuinely
semantic probe replay are supplied, and the handwritten decoration step is
inserted, I would expect the result to become assessable without changing its
statement. The repair burden is major, but because correctness of a central
finite branch cannot presently be checked from the package, the sole verdict
is **not fully assessable**.

## 1. Exact claims and scope

### 1.1 Network and parameter hypotheses

The main theorem concerns two networks on the same finite labelled leaf set.
Each must be binary, level at most two, standard semi-directed, and strongly
tree-child. In every rooted presentation the binary root is the lowest stable
ancestor of all leaves (`manuscript/sections/03_conventions_model.tex:5-13`).
“Standard” means: mark the arcs entering reticulations, undirect
all other arcs, delete the binary root, and merge its two incident arcs exactly
once; the presentation is admitted only if that one suppression creates no
loop or parallel edge and loses no arrowhead. There is no later exhaustive
cleanup (`manuscript/sections/03_conventions_model.tex:5-24`). Strong
tree-childness means that an admissible rooting exists and every admissible
rooting is tree-child (`:40-64`).

Every inheritance probability is in `(0,1)`. Every edge has fixed, labelled
nontrivial K3P Fourier coordinates `(c,g,t)` in

`D_{3,+}={(c,g,t) in (0,1)^3: 1+c-g-t>0, 1-c+g-t>0, 1-c-g+t>0}`.

These inequalities are exactly strict positivity of the four inverse-Fourier
transition probabilities, together with positive nontrivial spectra
(`03_conventions_model.tex:85-135`). States and characters are identified with
the fixed Klein four group `{0,C,G,T}`, the root distribution is uniform, and
the network tensor is the inheritance-weighted sum of displayed-tree Fourier
monomials subject to total character zero; each switching weight is the product
of independent local `lambda_r` or `1-lambda_r` choices (`:87-122`). Zero spectra,
identity/boundary edges,
inheritance values `0` or `1`, nonbinary networks, higher level, nonreversible
models, and other semi-directed cleanup conventions are outside the theorem
(`12_continuous_time.tex:43-44`; `manuscript/sections/16_scope.tex:9-40`).

### 1.2 Observational relations

`N <= N'` is not ordinary image inclusion. It requires a regular source point,
a connected open neighborhood in the **full source parameter space** on which
the source map has maximal physical rank, and a physical real-analytic target
parameter section whose composition with the target map equals the source map
on that neighborhood. The target point need not be target-open or
target-regular (`03_conventions_model.tex:147-169`).

A common-germ relation requires a common analytic image germ that is regular
and full-dimensional relative to both images and has physical analytic
sections from both parameter spaces (`:160-163`). These notions are stronger
than a nonempty intersection and different from containment of complex
Zariski closures.

Ordinary-triangle equivalence requires the same labelled reduced component
tree; corresponding complete nontriangle factors must be labelled
mixed-graph isomorphic; each remaining ordinary three-cycle may redirect which
of its three vertices is reticulate, with coherent boundary transports
(`03_conventions_model.tex:67-83`). It does not assert equality of the complete
stochastic images of the representatives.

### 1.3 Principal-domain theorem

For networks in the stated class, the article claims equivalence of:

1. source-relative directed analytic containment;
2. ordinary-triangle equivalence; and
3. a common full-dimensional regular physical analytic germ.

Consequently it claims that no proper one-sided regular full-dimensional
containment occurs in this class (`02_main_theorems.tex:6-29`). Symmetry is at
the topology/germ level, not a claim that every parameter or tensor in one
representative is realized by every other representative (`:83-86`).

### 1.4 Generic identifiability and reconstruction

For each fixed topology `N`, the article claims a proper complex
Zariski-closed exceptional set `E_N` in the complex image closure `V_N` such
that every exact physical tensor outside it determines the labelled standard
semi-directed topology uniquely modulo ordinary-triangle redirection
(`02_main_theorems.tex:31-36`; `11_genericity_reconstruction.tex:17-108`).

The reconstruction claim is only an exact-oracle termination claim. Input is
an exact-real representation supporting field operations, polynomial-sign
decisions, and real-closed-field quantifier elimination. No bit complexity,
conditioning, estimator, sample complexity, robustness, or finite-data
guarantee is claimed (`02_main_theorems.tex:38-45`;
`11_genericity_reconstruction.tex:115-152`). It returns a structural triangle
class, not all numerical parameters.

### 1.5 Strict continuous time

The same classification, genericity, and reconstruction conclusions are
claimed on

`D_{3,CT}={(c,g,t) in (0,1)^3: c>gt, g>ct, t>cg}`,

the open strict symmetric continuous-time K3P cone
(`02_main_theorems.tex:47-56`). The proof uses that this is a nonempty
full-dimensional open subset of `D_{3,+}` for necessity and supplies
continuous-time triangle/gluing constructions for sufficiency
(`12_continuous_time.tex:1-41`). It makes no boundary claim.

### 1.6 Triangle geometry

The three labelled orientations of an ordinary three-cycle are claimed to
have normalized generic rank 14 in the 15-dimensional normalized three-leaf
chart, to have the same irreducible eight-term quartic closure `H14`, and to
share a strict-CT smooth relative rank-14 germ. No ambient-open rank-15
triangle germ is claimed (`05_three_leaf_geometry.tex:104-187`). The contextual
lemma says the same relative ambiguity persists after insertion in an
otherwise fixed labelled context (`:189-211`).

### 1.7 Weak-class sharpness and outer obstruction

For every `n>=3`, the article constructs two labelled nonisomorphic,
non-triangle-equivalent networks in `W_TC \ S_TC` whose strict-CT images share
a regular common full-dimensional germ of dimension `6n-3`. At `n=3`, both
normalized maps have rank 15 throughout a rational Krawczyk box containing a
unique common equality-slice root (`02_main_theorems.tex:58-71`;
`13_sharpness.tex:1-195`). Uniqueness is only inside the selected 15-variable
slice, not global parameter identifiability (`13_sharpness.tex:119-121`).

A separate outer proposition puts a tree germ properly inside a double-theta
image outside `W_TC`, with normalized ranks 9 and 15 and a 23-dimensional
local target collision locus. It is expressly not the sharp weak/strong class
boundary (`02_main_theorems.tex:73-80`).

## 2. Claim-to-proof structure

The detailed dependency map is in `CLAIM_DEPENDENCY_MAP.md`. Its central flow
is:

`physical/domain and primitive topology`
→ `directed cut equality`
→ `bridge fibre and localization`
→ `four-port residue + restoration + one/two-port probes`
→ `complete local classification`
→ `global necessity`.

In the other direction, `H14 contextual equivalence + simultaneous physical
bridge gluing` gives global sufficiency. The classification is then consumed
by the semialgebraic/Zariski genericity and exact-reconstruction arguments.
The weak-class Krawczyk/cherry construction is logically independent of the
four-port atlas.

The active evidence is defined by `ACTIVE_MANIFEST.json`, but active status is
not synonymous with verified truth. The preserved rooted-DAG H21 verifier,
the withdrawn universal pointwise cut theorem, old broken cloud entrypoints,
and K2P algebra are historical/provenance-only. Model-independent graph,
parentage, and transport data imported from companion work remain inputs whose
meaning must still be replayed. The Git-bound release-engineering mutation
suite is a packaging audit, not theorem evidence.

## 3. Mathematical correctness of the stated theorems

### 3.1 Parts independently supported

I found no defect in the following handwritten transitions, and independent
exact checks agreed with the displayed formulas.

- The inverse Fourier formulas, strict principal domain, CT inclusion, and
  strict isotropic subdivision are correct. `D_{3,+}` is strictly larger than
  `D_{3,CT}`; for example `(2/5,2/5,1/10)` is principal-positive but has CT
  margin `-3/50`.
- The literal tree--sunlet six-circuit factorization is correct. Its paired
  contradiction and all-composition-margins-zero case prove strict positivity
  on the stated domain (`05_three_leaf_geometry.tex:53-99`). Identity edges
  and inheritance boundary values give zeros, as expected and excluded.
- All three transported sunlet maps annihilate the displayed eight-term
  quartic. At the common isotropic point, each has rank 14, the stated minor
  magnitude is `1/760840571584512`, and the gradient has six entries of
  magnitude `1/6912`. The linear-in-one-variable irreducibility argument is
  valid. These facts justify equality of the three irreducible closures and a
  common relative smooth germ.
- Positive rank-one bridge blocks yield one labelled scale per incidence and
  sector; on a tree there is no holonomy. The marked-anchor and unmarked
  degree-`d>=3` exponent matrices kill the stabilizer. The degree-two
  exclusion is essential: without it, `(tau,tau^{-1})` is a real stabilizer.
- The simultaneous bridge cap is correct. Exact algebra gives
  `epsilon/U - epsilon^2/L^2 >= 7 epsilon/(8U)` from
  `epsilon <= L^2/(8U)`, and the principal/CT margins remain strict on a
  common neighborhood (`10_global_classification.tex:22-70`).
- The finite semialgebraic genericity argument, source rank-drop estimate,
  full-rank incidence projection, and real-to-complex dimension passage are
  coherent once the classification theorem is available. The exact-oracle
  reconstruction terminates by finite enumeration and real-closed-field QE.
- The Krawczyk self-inclusion, contraction norm, uniform rank-15 bounds, and
  physical margins use exact rational interval endpoints and replay exactly.
  The all-`n` cherry observables have determinant
  `8 u_C u_G u_T/(v_C v_G v_T)` and value `176/25` at the stated point.

### 3.2 MATH-1 — omitted ordinary-component versus cycle decoration

**Severity:** major and load-bearing, but locally repairable.
**Location:** `manuscript/sections/04_physical_topology.tex:204-212` and
`:274-280`; `10_global_classification.tex:5-16`;
`09_restoration_words.tex:103-116`.
**Dependency:** necessity in the principal and CT classification; therefore
generic identifiability and reconstruction.
**Repairability:** high.

The cut theorem proves equality of bridge split sets and concludes “Hence the
labelled reduced trees of blobs agree.” Split sets reconstruct the abstract
tree, but not whether a trivalent internal component is ordinary or the
contraction of a three-boundary cycle blob. A three-leaf tree and an ordinary
three-sunlet have the same pendant cut splits.

The global proof then invokes the complete local factor classification for
every corresponding factor, although that theorem is explicitly stated only
for complete ported cycle/theta factors. The missing ordinary-versus-cycle
case is therefore not discharged by the cited theorem.

The existing six-circuit separator appears to repair the proof: it vanishes on
the three-leaf tree and is pointwise positive on every strict sunlet, and its
zero/nonzero distinction survives positive incidence scaling. Indeed, under
`q_xyz -> A_x B_y C_z q_xyz`, the two cubic monomials in each circuit have the
same character multiset at each port, so that circuit is multiplied by one
strictly positive monomial. The strong
repair table gives at least four boundaries for a theta, leaving the cycle as
the only nontrivial degree-three blob alternative
(`08_primitive_bounded.tex:45-73`). The revision should insert this decoration
test after recovery of the abstract split tree and bridge-orbit extraction,
before applying the cycle/theta local theorem, and should weaken the premature
conclusion at `04_physical_topology.tex:212` accordingly. The reconstruction
algorithm already performs this missing distinction as step R3
(`11_genericity_reconstruction.tex:119-131`).

### 3.3 MATH-2 — analytic section in finite-type localization is not explicit

**Severity:** moderate, repairable proof-detail gap.
**Location:** `manuscript/sections/07_marginal_localization.tex:68-91`, with
the needed model at `11_genericity_reconstruction.tex:62-81`.
**Dependency:** localization into a fixed target completion type, hence local
classification under directed containment.
**Repairability:** high.

The finite-cover lemma shows that one semialgebraic realization set contains a
relative open source subgerm. By itself, that set-theoretic statement does not
supply the regular source germ and physical real-analytic target parameter
section required by the local directed relation (`06_bridge_fibre.tex:105-110`).
The argument likely follows from existing hypotheses: intersect with the
focal maximal-minor locus and restrict the original global analytic target
section and analytic marginal descriptor; or stratify the fixed-type incidence
correspondence and take a full-rank projection stratum as in the later
genericity proof. The manuscript should state one of these arguments.

### 3.4 MATH-3 — primitive directed grammar is too compressed

**Severity:** minor-to-moderate auditability issue; no omitted case found.
**Location:** `manuscript/sections/08_primitive_bounded.tex:11-38` and
`supplement/reader_supplement.tex:87-93`.
**Dependency:** all finite primitive universes.
**Repairability:** high.

The excess-degree argument correctly reduces one reticulation to a cycle and
two to a theta, but “separating the cases” into exactly four directed theta
types is a load-bearing enumeration compressed to two sentences and a frozen
topology replay. The bundled companion JC source contains a coherent
pole/source/sink case split; I found no missing directed case there. The K3P
article should reproduce or directly cite that lemma at the point of use.

### 3.5 Minor mathematical precision

The root-movement lemma says the K3P map is “unchanged”
(`04_physical_topology.tex:38-51`). Its proof establishes equality of physical
images/local germs after reversible root movement and physical edge
subdivision/merging, not literal identity of parameter maps. That is sufficient
for later arguments, but the statement should say “unchanged up to analytic
physical reparameterization.” This is a minor, locally repairable wording issue;
it affects only the formulation of the root-movement dependency used throughout
the topology reductions, not the image/germ conclusion actually needed.

## 4. Fidelity of code and certificates to the mathematics

### 4.1 Positive findings

- Exact polynomial/rank code uses integers or `Fraction`; the Krawczyk and
  Neumann decisions use rational interval endpoints, so there is no hidden
  floating-point outward-rounding assumption.
- The clean-room four-port verifier genuinely reconstructs the selected
  literal maps, root-suppressed mixed automorphism groups, displayed-frame
  conjugation, double cosets, Fourier transports, separator pullbacks, source
  minors, and target generator upper bounds. The problem is selection of the
  records, not the representative algebra.
- The restoration verifier is materially producer-independent. It imports
  neither producer nor producer support, reconstructs every row, rechecks
  fixed-full parent restrictions and graph hashes, recompiles K3P descriptors,
  checks target-zero/source-nonzero direction, and evaluates strict witnesses.
- The cut verifiers exactly re-expand switching polynomials, minors, Bernstein
  coefficients, signed pairs, and cyclic certificates within the frozen
  direction universe. Source/target direction is explicit.
- The literal tree--sunlet verifier starts from the printed map rather than a
  stored Boolean.

### 4.2 CODE-1 — four-port exhaustiveness is never regenerated

**Severity:** major, load-bearing.
**Location:** `input_frozen/k3p_cloud_artifacts/descriptor_report_4(1).json:2-18`;
`input_frozen/k3p_cloud_artifacts/K3P_14_ORBIT_LOCK.json:69-71,928-929`;
`manuscript/sections/08_primitive_bounded.tex:90-211`;
`reproducibility/exact_four_port.py:560-626,830-843`;
`clean_room/verify_h21_transport_and_fourteen_orbits.py:71-120,328-407,1683-1719`;
`reproducibility/verify_k3p_same_classification.py:182-250`;
`reproducibility/run_release_suite.py:116-240`.
**Dependency:** fourteen-orbit theorem, complete local classification, main
necessity, generic identifiability, and reconstruction.
**Repairability:** yes, but requires a missing producer/verifier boundary.

The underlying raw space is `6 * 2814 * 24 = 405,216`. The bundled compressed
companion ledger has all 405,216 rows, partitioned as 377,382
`topology_excluded`, 23,822 `rank_excluded`, 2,540
`restoration_obligation`, and 1,472 `retained_terminal`; the last three total
the reported 27,834 post-topology relations. The dependency lock expressly
limits imported K2P algebra to reference-only use
(`COMPANION_DEPENDENCY_LOCK.md:3-17`).

The K3P descriptor report records a 142,589,253-byte corpus and hashes, but the
corpus itself is absent, and `LOCAL_INPUT_INVENTORY.json:34-46` classifies the
lock as `frozen_input_unverified`. The active lock stores the final 40/14/2
answer.
`exact_four_port.py` and the clean-room code then loop only over records loaded
from that lock. The clean-room target census proves that its handwritten
grammar constructs 2,814 targets, but it never compares all sources, targets,
and 24 port permutations through the full filters. Its only exhaustive orbit
step is the 24-permutation double-coset partition of one H21 base relation.

The 44-command “complete regeneration” contains no four-port universe or lock
producer. The integrated gate verifies only the stored 14/38/2 census and 9+5
separator partition. Exact certificates for the selected rows cannot rule out
an omitted relation. In particular, the primary module returns
`accounting_classification_certified_by_this_module=True` after checking that
same stored selection (`reproducibility/exact_four_port.py:1043-1059`), and the
later gate consumes that Boolean (`reproducibility/verify_primary.py:579-599`);
this is not independent evidence of exhaustive selection.

Required evidence is an active independently implemented driver that derives
the primitive universe, visits all 405,216 cases, recomputes topology and K3P
rank/polynomial filters, and deterministically derives the 40 records and their
14-orbit/two-sink quotient. If a large descriptor corpus is the intended
certificate, it must be bundled and every row semantically verified. Mutations
must include coherent omission/reclassification cases.

### 4.3 CODE-2 — probe replay is structural/hash replay, not semantic replay

**Severity:** major, load-bearing.
**Location:** `probes/verify_k3p_probes.py:2-8,80-135,154-222,280-355,357-494`;
`probes/test_k3p_probe_mutations.py:82-180,323-349`;
`reproducibility/verify_k3p_same_classification.py:932-943`;
`manuscript/sections/09_restoration_words.tex:65-124`;
`independent_checks/check_probe_semantic_samples.py:707-739`.
**Dependency:** arbitrary one-/two-port word recovery and coherent triangle
assembly, hence complete local classification and main necessity.
**Repairability:** yes, with a genuinely separate semantic verifier.

The verifier claims to validate every exact map/marginal and recompute every
stored Bernstein certificate. The hour-scale producer itself does perform
semantic graph construction, classifications, restrictions, and the full
one-/two-port Cartesian enumeration
(`probes/regenerate_k3p_probes.py:199-263,409-432,992-1003,1222-1315,1337-1429,1516-1646`).
The defect is the lack of a separately implemented semantic replay. In the
advertised verifier:

- `validate_transport` checks a self-hash, enum values, injectivity, and shallow
  triangle-list properties. It never reconstructs source or target graphs or
  proves that the vertex/edge map preserves vertices, labels, incidence, and
  arrowheads.
- `validate_restriction` checks only a self-hash, a relation string, an integer,
  and hash-string lengths; it performs no marginal restriction.
- `sparse_from_payload` and `bernstein_replay` are defined but have no call
  sites.
- a quartet record is accepted when two stored split lists differ; neither list
  is generated from a graph;
- a row-specific tree--sunlet record is accepted from stored circuit hashes and
  a nonzero-count field. The general six-circuit theorem is independently
  replayed, but its application to the row's actual restricted graphs is not.

A direct test supplied a coherently self-hashed “isomorphism” whose vertex map
sends `source_a` and `source_b` to `target_a` and `target_b`, but whose claimed
edge maps to `target_a--target_not_in_vertex_map` rather than the induced edge
`target_a--target_b`. `validate_transport` accepted record
`bfc9e39ce0fddae47e137321086466b90e22dc3c4aaa333afbb1147b477339e4`.
The mutation suite's “broken transport”
changes a vertex string without recomputing the inner self-hash, so rejection
shows hash sensitivity, not semantic sensitivity. The tree-circuit mutation is
similar.

The repair is to reconstruct each referenced anchor and inserted source/target
graph independently, derive the mixed graphs and restrictions, verify labelled
incidence/arrowheads, compile the actual restricted Fourier maps, recompute
quartet splits and all six row-specific circuit pullbacks, and invoke the
Bernstein routine where sign certificates are claimed. Mutations must be
coherently resealed so that only the semantic error remains.

### 4.4 CODE-3 — other fidelity limitations

1. **Cut topology boundary (moderate).** The exact 204-direction algebra begins
   from frozen JC switching masks; the five primitive templates, 72 records,
   and masks are not graph-generated on the active path
   (`cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py:72-132`;
   `cut_recovery/strong_crossbridge/final_certificate/verify_final_certificate.py:28,174-214`).
   The article nevertheless says the verifier rebuilds the “entire labelled
   universe” (`manuscript/sections/04_physical_topology.tex:196-201`). This is a
   conditional topology input, not algebraic circularity. It affects directed
   cut transfer and hence global necessity. An active graph generator deriving
   the five templates, 72 records, and switching masks would resolve it; absent
   that, the dependency should be disclosed as conditional.
2. **Hardened H21 audit not active (moderate).** `ACTIVE_MANIFEST.json:123-125`
   attributes 10 gate and 25 adversarial mutations to
   `clean_room/verify_clean_room.sh`, but that wrapper runs the 10-mutation
   suite and optimized rejection only (`clean_room/verify_clean_room.sh:12-29`).
   It never runs `clean_room/adversarial/hardened_cleanroom_reaudit.py`, and the
   44-command plan omits it. The integrated gate reads the stored hardened
   report rather than freshly producing it. I separately ran that script in a
   fresh copied workspace: its baseline, three optimized-mode controls, five
   input hashes, all 25 coherently exercised mutations, five directional rank
   inequalities, and historical-failure replay passed. This confirms the fixed
   audit but does not make it part of the claimed active wrapper.
   This affects reproducibility of the claimed hardening, rather than the
   mathematical conclusion by itself. Repair by adding the hardened script and
   a sentinel to the active wrapper/44-command plan, or relabel the stored audit
   as non-fresh evidence.
3. **Vacuous H14 hardening check (minor).** The global verifier computes the
   purported exponent gcd as the gcd of a list of ones
   (`global_infrastructure/verify_global_infrastructure.py:526-554`). The fixed
   coefficient is genuinely primitive, so the mathematics survives. Compute
   the actual exponent-difference vector and add an `x^3-y^3` mutation.
4. **Standalone optimized-mode weakness (minor).** `exact_primary.py`,
   `exact_four_port.py`, and `verify_primary.py` use load-bearing `assert`s and
   do not themselves refuse `-O`; representative four-port assertions are at
   `reproducibility/exact_four_port.py:830-1043`. The primary rank replay also
   does not require the stored rank to equal both selected minor dimensions
   (`:895-909,953-988`), although every delivered record has matching sizes and
   the clean-room check supplies this condition
   (`clean_room/verify_h21_transport_and_fourteen_orbits.py:1436-1475`).
   The official integrated gate refuses
   optimized mode, mitigating the delivered path. The standalone primary
   entrypoint should also fail closed and bind rank labels to minor dimensions.
   This affects only the standalone primary assurance path, not the official
   integrated result for these fixed records.
5. **Blocked cut certificate exits zero (minor).** The standalone final cut
   verifier can emit `PASS_BLOCKED` and return zero
   (`cut_recovery/strong_crossbridge/final_certificate/verify_final_certificate.py:571-588,631-664`). Later
   global transfer requires true `PASS`, so the complete chain eventually
   fails, but the standalone command should return nonzero or have a strict
   runner sentinel. This affects standalone fail-closed reporting, not the
   later global-transfer theorem dependency when the whole chain is run.

## 5. Computational reproducibility and toolchain limitations

### 5.1 Isolation and environment

The formal supplied-package runs were made in `package_copy`, not the delivered
original. A macOS sandbox denied all network operations and confined writes to
that copy (plus `/dev/null`). The caller environment was rebuilt from empty, so
no credential-bearing environment variables were inherited. A connection
attempt to `127.0.0.1` failed with `EPERM`.

There is an important procedural limitation: `logs/offline_referee.sb` allowed
unrestricted host file reads for runtime compatibility. It therefore was **not**
a complete filesystem-level no-credentials sandbox; supplied code could in
principle have read a host credential file even though it could neither use the
network nor write outside the copy. Pre-execution static inspection found no
explicit credential-store, keychain, browser-profile, or network-client access
in the active command graph, and a live `lsof` snapshot during the probe stage
showed only package-copy files open, but neither check proves the absence of an
earlier transient read. This limitation applies to the formal regeneration and
cannot be repaired by relaunching it under the prompt's exact-once rule.

The first executions of the referee-authored spot scripts, one read-only
integrity preflight, and the isolated fake-transport validator probe occurred
before that final confinement protocol. All six spot scripts, including the
actual validator call, were subsequently rerun inside `package_copy` with an
empty environment, network denial, write confinement, and a follow-up overlay
that explicitly denied common SSH/cloud/keychain/browser credential locations.
Every result was byte-identical to the preserved evidence. The overlay itself
does not claim to enumerate every possible credential location; its SHA-256 is
`39dbe755d63423558dc3416b8351927b6f26a8512754515e09cf7f874d8187d6`.
Commands, control probes, and result hashes are recorded in
`results/strict_independent_replay.md`.

The documented dependencies were supplied offline by copying the source
project's exact local `.venv` into the isolated package, avoiding package-index
access. The environment was Python 3.14.6, mpmath 1.3.0, networkx 3.5, numpy
2.5.2, and sympy 1.14.0. The successful run report records module-file and
interpreter hashes.

Initial and formal-run integrity checks found 574 outer payload files totaling
153,326,366 bytes and 548 proof-core members totaling 152,714,245 bytes
hash/size consistent. The mutually consistent manifest fields name proof and
package-builder commit
`983086779dab08f6a0d76d0a10c614b7cee4affe`; no Git-tree or remote-authenticity
binding was reproduced from this extracted package. The successful
release-input command used its documented `--allow-uncommitted-sources` mode.

### 5.2 Executions

The later isolated `./RUN_REVIEW.sh plan` passed and reconstructed the declared
44 mathematical regeneration commands. No second probe producer was launched.

Three failed harness/preflight attempts are retained and explained:

- a subordinate static-audit invocation of `./RUN_REVIEW.sh plan` raced the
  parent-owned verification workspace, so its integrity scan saw a temporary
  path disappear. It launched no mathematical command. A later isolated plan
  run passed. One earlier read-only JSON inspection also raised a corrected
  `KeyError` after a guessed field name; no conclusion or execution depended on
  it (`results/code_audit.md:131-142`).

- `review_runs/20260827T005735Z`: substantive clean-room checks passed, then
  BSD `mktemp -t` ignored the phase `TMPDIR` and attempted a denied system-temp
  write (`clean_room/verify_clean_room.sh:17`). Transcript SHA-256:
  `122664812e228d61e78bc5d6e36288ed72e6328d7cd1104c107c812cad187189`.
  The all-path diff has one authorized addition (`.venv`), one changed
  location-dependent `primary_gate_report.json`, and no removal; evidence hash
  `1a9b66539760f341392b43fc62041dc4b6a8788182cb1462ae768ec897aea131`.
- `review_runs/20260827T005931Z`: the ten-child integrated replay passed in
  190.80 seconds, but the outer runner rejected a primary-report platform
  string changed by sandbox denial of writes to `/dev/null`. Transcript
  SHA-256:
  `cc1c11b9758e6818a2365154c7651bc08281ad1c818f4cfdb3794cf13edb63c3`.
  Its all-path diff has two additions (`.venv` and the generated fresh report),
  the same location-dependent primary-report change, and no removal; evidence
  hash
  `05c3f07d247fe2ad270a8ced8f9d93077a848105186e4e9ea8b3ffdcec2452a7`.

A local execution shim rewrote only `mktemp -t TEMPLATE` to the explicit
phase-local `TMPDIR`; allowing `/dev/null` writes restored the standard
read-only platform probe. These adjustments did not modify the sealed package
or relax the enforced network/write scope. The original sandbox-profile and
shim SHA-256 values are respectively
`7e217ae3951973d49d0f37a7088d7b7542c6722a9490967b3e828d46ebb2e142`
and `b2d5e9ac9b71f60e0d65bf53028b86cfb57319abdf8baf0d36a548c75f767403`.

The clean verification session `review_runs/20260827T010421Z` passed:

| Command | Result | Seconds | stdout SHA-256 |
|---|---:|---:|---|
| release-input semantic bindings | PASS | 0.151 | `1607b33014ff29f0fb8986268686d0994a46451c25fce3033c426dcaddd385b8` |
| integrated artifact binding | PASS | 0.090 | `901cb49a6f0a89bda02130b003c7e828d76c41d5eae9cac8fd868b45f8fb532b` |
| integrated ten-child fresh replay | PASS | 187.911 | `e9a2a4aa6f48d162492afcba14589ff22c70d95203cdede144e18e47e42c79ee` |
| integrated classification mutations | PASS | 5.411 | `37386eed3c13b4e6f1cb6897671ed9e8bc85001a81851d3ad2fe1c8a94af627a` |

Total phase time was 193.749 seconds; the runner's declared sealed-payload
drift was empty. That field deliberately excludes the `.venv` symlink and
`release/work/`. A separate all-path byte/symlink comparison against the
delivered proof source found zero changed files, zero removals, and exactly two
authorized additions: `.venv` and
`release/work/referee_integrated_fresh_report.json` (29,679 bytes, SHA-256
`a0672f420e273c5560ed00fda92b8c26dcd985521b6c731b3bd142e0db5bcf83`).
The complete diff is `results/verify_full_workspace_diff.json`, SHA-256
`22cd7b89ea1044a409ee55b41023116ee5ea2e867fdb7367d791a487c2a9e03a`.
Report SHA-256:
`da448cca65c7787d48a7e537ea707d6f032b019434a7c1688ba062833c5b4afa`.
Transcript SHA-256:
`04404b9c5959c2fbb33db33b13d7757686a958125ff48e764418818125b83db2`.

The separately manifest-claimed hardened H21 re-audit also passed once. An
initial shell setup attempt failed before Python launch because the copy-target
parent directory did not yet exist; after creating that parent, the single
actual audit run rejected all 25 mutations and passed its controls. Transcript
SHA-256:
`c751a1b00de068175ef63b68fa99fa67beead11cf353fd0f63a6410d2b098b4a`.
An all-path comparison of its fresh workspace found no file or symlink
difference from the delivered proof source; diff-report SHA-256:
`e87f1b2d261520832da3ed5f0178608f54e0982f5311289bfc153340c0d1f660`.

**Complete regeneration:** the once-only session
`review_runs/20260827T010753Z` returned
`FAIL_OUTER_DRIFT_AFTER_ALL_COMMANDS_PASS`. All 44 declared mathematical
commands ran in the prescribed order, exited zero, emitted their sentinels, and
were recorded as `PASS`. Their elapsed-time sum was 4,202.194 seconds; the
transcript's filesystem wall interval was 4,202.237 seconds (70m02s). The
hour-scale probe producer took 2,863.367 seconds and was launched exactly once.
The restoration producer/replay took 609.710/75.095 seconds, and the final
integrated replay took 182.635 seconds.

Selected regenerated outputs were:

| Command | Seconds | stdout SHA-256 |
|---|---:|---|
| restoration full producer | 609.710 | `9c142efab431690578e0b0d8dceb0fb8644636282a54ad8ff6129ad9efd8f279` |
| restoration independent replay | 75.095 | `3be91a42e8f8a2e63a4057f6ea472ea5f272e287d294c2be7a8d49eb903cb2a6` |
| probe hour-scale producer | 2,863.367 | `1182fb269397621299e18b281344ccca5a3cf67853f6c4a89a12593a88300b37` |
| probe advertised replay | 16.432 | `40bc14354f04991c885ab453fd7eea467acd0d92f5b2bf1e154a2376c7102cc0` |
| probe mutations | 169.650 | `7ebeb51cf2fbd5f9be6b057337bef4725fbfccfc53c26733940031f737eac99e` |
| integrated fresh replay | 182.635 | `2c7a45f0666cc16420556c2cd8abeed18ab9f036e693936eeddabec79b2f751f` |
| integrated mutations | 5.158 | `37386eed3c13b4e6f1cb6897671ed9e8bc85001a81851d3ad2fe1c8a94af627a` |

The complete transcript is 76,098 bytes, SHA-256
`fbf05586be101315a4e2434c83b3c8ae50c9fd3c487f0c73d16928d98e4403d8`.
All 44 records and stdout hashes are preserved in
`results/regeneration_failure_summary.json`, SHA-256
`e3956277d80a33dbaa0b42e790c607b664088b51c04f611416ec144ee5043535`.
The preserved primary and integrated supplemental reports have SHA-256
`5ce054ecddd6c4bf14c57b01c02c00efcd03edea1645c8e83491774413bb128c`
and `8413bd460776ff8696a05b63b85a407b52a3c035b8457f1ebdf3cf899ae1760b`.
Because the outer drift check failed, the runner created neither `report.json`
nor `summary.json`; I do not describe the complete regeneration as a passing
run and did not rerun it.

### 5.3 REPRO-1 — location-dependent restoration report defeats drift gate

**Severity:** moderate reproducibility defect; no mathematical certificate
failed.

**Location:** `restoration/regenerate_k3p_restoration.py:569-628,829`;
`referee_tools/run_active_verifiers.py:366-422`.

**Dependency:** the outer claim of deterministic, zero-drift portable
regeneration; not the restoration theorem's algebra or the main theorem by
itself.

**Repairability:** high.

The only changed sealed-payload file was
`restoration/K3P_RESTORATION_THEOREM_REPORT.md`. Its reproduction block embeds
`cd {HERE}`. The delivered report contains the source-project absolute path;
the regenerated report contains the isolated-workspace absolute path. No other
text differs. Its size/hash changed from 2,401 bytes /
`9c3ea74acdc5dc4eff24d50c9f2db845215bde6b8276c72faf0a6d150f4bf7f0`
to 2,473 bytes /
`26392bbdfdeb363b4440f960d0814fb07c9d76c410de8d6f2f35bb126629dbfb`.

The complete all-path comparison found no removal, that one change, and three
authorized additions: `.venv`, the integrated fresh report (29,695 bytes,
SHA-256 `8413bd460776ff8696a05b63b85a407b52a3c035b8457f1ebdf3cf899ae1760b`),
and the ephemeral probe-verification report (1,132 bytes, SHA-256
`1bd4a010a306ff887247cb1fd19516c504e766155f41f47ff117efaf137bffe6`).
The full diff is `results/regeneration_full_workspace_diff.json`, SHA-256
`f86b84a9e528cb40fddc1dbaf73d2ae09f971a4622708846c985ad639ff4919f`.
Render a relative reproduction command, normalize this report as is already
done for `primary_gate_report.json`, or restore the canonical bytes before the
drift comparison; then add a relocated-workspace regression.

### 5.4 Explicitly unexecuted packaging/toolchain checks

I inspected all 932 lines of
`reproducibility/test_release_engineering_mutations.py`. It tests Git-index
selection, dirty-tree policy, deterministic archives, path traversal, source
build identity, journal package structure, timeouts, and release envelopes. I
did **not** execute it: the extracted referee package is not the exact clean
Git checkout it requires, and the prompt correctly excludes it as
nonmathematical packaging evidence.

I did not reproduce the PDFs byte-for-byte. The package does not bundle the
required exact Tectonic 0.16.9 arm64 executable. I did extract and render every
page of both supplied PDFs and found no material visual defect. PDF identity is
covered by package integrity, not a fresh typesetting build.

### 5.5 What the executions do and do not show

The clean verification establishes replay of the declared arithmetic,
hash/schema bindings, and listed mutations with zero sealed-payload drift. The
complete regeneration establishes that all 44 command-level checks can pass,
but REPRO-1 prevents a claim of end-to-end zero-drift determinism. Neither
execution establishes completeness of untested
mutations or correctness of prose analytic arguments. Specifically, they do
not resolve CODE-1 or CODE-2 because those are omissions from the active
verification graph itself.

## 6. Independent spot derivations and counterexample search

Fresh scripts and exact output hashes are under `independent_checks/`. Their
scope was deliberately different from accepting stored `PASS` flags.

- **Domains and three-leaf geometry:** exact inverse Fourier inversion, CT
  inclusion, all six tree--sunlet pullbacks, all six leaf transports of `H14`,
  three rank-14 Jacobians, smoothness, gcd/irreducibility, and the cherry
  determinant. Result hash:
  `26ebfacdd91bf97e5673758c600b8c8a4622cec4e1e0a93cef91d58513e5a29d`.
- **Bridge/gluing:** marked/unmarked exponent matrices through degree 12,
  the degree-two stabilizer, exact normalizers/cancellation, cap inequality,
  and 1,000 exact-rational adversarial samples. Result hash:
  `86a2abf63d7a992a19d550438cb0c5dfef45c80d2e8fc8a80ffdb2f05f8f11f6`.
- **Four-port representative checks:** exact target-zero/source-nonzero
  quartics for H21-01, L20-01, and L23-02; exact rank gaps and target generator
  bounds for H21-02, L20-02, and L21a-02, including the H21 saturation factors.
  Result hash:
  `be9b87a9295fc4d00ea9d23cac8ba51e4605e609f430fa6e5e5337a099ce2eea`.
  This was expressly sampling, not orbit completeness.
- **Restoration/probe census:** every stored row was streamed; canonical
  self-hashes, ordered roots, references, counts, and stored transport endpoint
  consistency were checked. Result hash:
  `6142f542695325d96b718fc5a2ec373c1f04599e4f943ffaecf3a2f55de42db4`.
  This does not regenerate the producer semantics; a follow-up semantic sample
  is recorded separately.
- **Probe semantics:** five rows were reconstructed independently without the
  producer/atlas: one-port isomorphism, triangle, quartet, tree--sunlet, and a
  two-port parent/inventory restriction. Their graph, transport, restriction,
  quartet, and literal-circuit semantics all matched. The same script supplied
  the coherently resealed impossible transport described in CODE-2, which the
  actual validator accepted. Result hash:
  `2b8e43da7f7e7269ba621f6e67f548303363df8cb8e7545bade3742196bedf2d`.
  Five positive samples do not establish semantic correctness of 574,535 rows.
- **Krawczyk:** literal DAG maps, point and interval Jacobians, rational
  inverse, self-inclusion, contraction, rank bounds, and every physical margin
  were rebuilt. Result hash:
  `8e34365ecf992234a9e8c21f1efe3bb8a3f57b8624f469654f505284fcfe6598`.

No in-domain counterexample was found. The strongest boundary/adversarial
findings were expected: tree--sunlet separation fails at an identity edge or
inheritance 0; an unmarked degree-two bridge factor has a stabilizer; and the
principal-positive domain contains non-CT points. No sampled separator
reversed source and target, no Krawczyk interval touched a forbidden boundary,
and no tested triangle orientation acquired ambient rank 15.

## 7. Scope, novelty, and literature positioning

The principal novelty is plausible. I found no prior primary source claiming a
complete K3P containment classification for binary standard semi-directed
strongly tree-child level-2 networks. The immediately preceding level-1 K3P
paper explicitly lists lifting level-2 identifiability to K2P/K3P as open
([Brits et al., arXiv:2607.12919v3](https://arxiv.org/abs/2607.12919v3)). The
explicit `H14` quartic, equality of three K3P orientation closures, and common
strict relative rank-14 germ also appear new. This is a priority inference,
not a proof that no uncatalogued work exists.

The cited comparisons to group-based Fourier work, level-1 identifiability,
three-sunlet dimension calculations, multigraded implicitization, and recent
JC level-2 work are materially accurate. The literature discussion still
needs minor revision:

1. **LIT-1 — omitted JC triangle geometry.** Location:
   `manuscript/sections/01_introduction.tex:31-50`,
   `15_kimura_perspective.tex:17-29`, and absent from
   `manuscript/references.bib`. Severity: minor revision. Dependency: novelty
   and presentation only. Currie et al., *Semialgebraic Conditions for
   Identifying Triangles in Phylogenetic Networks*
   ([arXiv:2606.26673](https://arxiv.org/abs/2606.26673)), is the closest JC
   analogue to a common triangle germ without equality of full stochastic
   images. Cite it and contrast its ambient JC geometry with the relative K3P
   `H14` germ; that citation resolves the issue.
2. **LIT-2 — practical invariant landscape.** Location:
   `01_introduction.tex:39-43` and absent from `manuscript/references.bib`.
   Severity: minor. Dependency: motivation/literature completeness only.
   Martin et al., *Algebraic Invariants for Inferring 4-Leaf Semi-Directed
   Phylogenetic Networks*,
   [DOI 10.1093/sysbio/syaf071](https://doi.org/10.1093/sysbio/syaf071), should
   be cited with one sentence distinguishing practical four-cycle inference
   from this exact local-to-global classification.
3. **LIT-3 — incomplete higher-level context.** Location:
   `01_introduction.tex:52-59` and absent from `manuscript/references.bib`.
   Severity: minor. Dependency: breadth of novelty comparison only. Allman et
   al., *Beyond Level-1: Identifiability of a Class of Galled Tree-Child
   Networks*,
   [DOI 10.1007/s11538-025-01545-8](https://doi.org/10.1007/s11538-025-01545-8),
   should be cited as complementary higher-level identifiability under
   different data and models, explicitly noting that it does not subsume K3P
   displayed-tree site-pattern containment.
4. **LIT-4 — same-author companion status.** Location:
   `01_introduction.tex:61-64`, `15_kimura_perspective.tex:3-21`, and
   `manuscript/references.bib:199-237`. Severity: minor revision/confidence
   limitation. Dependency: the JC/K2P comparison columns and proposed common
   sharp boundary, not the internal K3P proof. Label the JC, K2P, and
   tree--theta items as same-author companion manuscripts/reproducibility
   packages, avoid implying independent consensus, and give the K2P/tree--theta
   items durable archives rather than only Git commits.
5. **LIT-5 — convention translation.** Location:
   `01_introduction.tex:48-50` versus `03_conventions_model.tex:16-24`.
   Severity: minor clarity issue. Dependency: only the claim that the two
   topology quotients agree. Brits et al. perform later exhaustive cleanup,
   whereas this article uses one-step root suppression. Qualify agreement as
   holding after translation and restriction to standard-admissible
   presentations, or supply a short equivalence lemma.

These are literature/presentation issues, not discovered mathematical
counterexamples.

The weak-class `6n-3` construction is also plausibly new but only moderately
externally corroborated; the closest precedents are same-author companions.
The exact-real reconstruction theorem appears new in this network class, but
its novelty is inseparable from the unassessed classification and it is not a
practical inference algorithm (`02_main_theorems.tex:38-44`;
`16_scope.tex:30-36`).

## 8. Presentation and editorial assessment

The article is unusually careful about scope: it distinguishes local germs
from full images, relative rank 14 from ambient rank 15, generic topology from
numerical parameter identifiability, strict interiors from boundaries, and
exact-oracle reconstruction from practical inference. The article and
supplement rendered cleanly, and the supplement is useful for coordinate and
certificate lookup.

Required presentation repairs are:

- correct the global necessity chain for ordinary/blob decoration (MATH-1);
- expand the analytic-section step in localization (MATH-2);
- disclose that four-port exhaustiveness is not regenerated by the active
  package and either supply the missing producer or weaken the certification
  language (CODE-1);
- correct the probe verifier docstring and “independent replay” claims unless
  semantic reconstruction is implemented (CODE-2);
- correct `ACTIVE_MANIFEST.json` so that the active wrapper is not credited
  with 25 adversarial mutations it does not execute;
- distinguish active, stored-only, companion, and historical dependencies at
  the theorem boundary rather than only in package metadata;
- make the root-movement reparameterization wording precise; and
- add/qualify the recent literature described above.

**PRES-1 (moderate, repairable disclosure defect).** The claim at
`manuscript/sections/17_reproducibility.tex:18-25` that
load-bearing replays rebuild literal graphs, switching masks, Fourier tensors,
coordinate transports, and exact witnesses is too broad for the four-port and
probe boundaries and for the frozen cut-topology masks. The more specific claim
that a verifier rebuilds the “entire labelled universe” at
`manuscript/sections/04_physical_topology.tex:196-201` is likewise not supported
by the active cut path. This affects the publication-level interpretation of
computer assistance, rather than adding a new mathematical dependency beyond
CODE-1, CODE-2, and CODE-3. Repair by naming the frozen/producer-only boundaries
at those theorem steps; an active independent regeneration of each boundary
would permit the stronger language.

## 9. Required evidence for reassessment

1. A bundled, active, deterministic, independently verified full four-port
   universe regeneration deriving the 40/14/2 residue from all 405,216 cases.
2. A separately implemented semantic probe verifier, with coherently resealed
   mutations, covering graph construction, restriction, transport,
   row-specific quartet/tree--sunlet observables, and any Bernstein signs.
3. A revised proof inserting ordinary-tree versus three-boundary-cycle
   separation before the cycle/theta local theorem.
4. An explicit analytic-section argument for the fixed target completion type.
5. Add the now-separately-replayed hardened 25-mutation audit to the active
   wrapper with a sentinel, or correct the manifest language.
6. Updated dependency disclosure and literature/convention comparison.

After these repairs, rerun the integrated verification and the complete
regeneration in a clean offline copy and preserve the same runtime/hash/drift
evidence.

## 10. Unresolved and unexecuted checks

| Check or concern | Location; severity and dependency | Status; repair or resolving evidence |
|---|---|---|
| Ordinary/tree versus three-boundary-cycle decoration (MATH-1) | `04_physical_topology.tex:204-212,274-280`; `10_global_classification.tex:5-16`; major in the necessity dependency | Unresolved in the text. Insert the strict tree--sunlet marginal test before the cycle/theta local theorem; the existing proposition appears sufficient. |
| Fixed-type analytic section (MATH-2) | `07_marginal_localization.tex:68-91`; moderate; localization and local classification | Unresolved proof detail. Restrict the original analytic section/descriptor on a regular subgerm or supply the incidence-stratification argument. |
| Full four-port reclassification (CODE-1) | `08_primitive_bounded.tex:90-211`; `input_frozen/k3p_cloud_artifacts/K3P_14_ORBIT_LOCK.json:69-71,928-929`; major; complete local classification and main necessity | Unexecuted and impossible with the active package as supplied. Bundle and independently verify a producer over all 405,216 relations that derives `40=38+2` and the fourteen orbits. |
| Semantic replay of all probe rows (CODE-2) | `09_restoration_words.tex:65-124`; `probes/verify_k3p_probes.py:96-222,302-494`; major; arbitrary-word recovery and main necessity | The semantic producer ran, but a separate semantic replay of all 574,535 rows remains absent. Supply independent graph/restriction/transport/observable reconstruction and coherently resealed mutations. |
| Primitive/cut topology and degree-two exclusion | `08_primitive_bounded.tex:3-88`; `cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py:72-132`; `06_bridge_fibre.tex:51-81`; moderate conditional dependencies | Five templates, 72 cut records/masks, and the full strong-class exclusion of unmarked degree two were not independently graph-enumerated. An independent graph generator or a complete handwritten enumeration would resolve them. |
| Complete portable regeneration / REPRO-1 | `review_runs/20260827T010753Z`; `restoration/regenerate_k3p_restoration.py:569-628`; moderate reproducibility dependency | Executed exactly once: all 44 mathematical commands passed, then the outer gate failed on one location-dependent Markdown path. It was not rerun. Use relative/normalized report text and test relocation. |
| Filesystem-level credential isolation | `logs/offline_referee.sb:1-15`; major procedural/reproducibility limitation, not a mathematical dependency | Network denial, write confinement, and an empty environment were enforced, but host reads were unrestricted. The exact-once regeneration will not be relaunched. Future reassessment should use a reviewed allowlist or credential-free VM; the smaller referee checks did rerun identically under a common-credential deny overlay. |
| Claimed hardened 25-mutation H21 audit | `ACTIVE_MANIFEST.json:123-125`; `clean_room/verify_clean_room.sh:12-29`; `reproducibility/run_release_suite.py:116-240`; moderate active-boundary issue | Separately executed once and passed all 25 mutations, but remains absent from the wrapper/44-command plan. Add it with a sentinel or relabel the report stored-only. |
| Git-bound release-engineering suite | `reproducibility/test_release_engineering_mutations.py:1-932`; nonmathematical packaging scope | Source inspected; not executed in the exact clean checkout it requires. Reproduce only from the named clean Git tree if packaging assurance is desired. |
| Exact PDF rebuild | `START_HERE.md:115-117`; `release/ENVIRONMENT.md:15-18`; editorial/toolchain only | Not executed because the exact Tectonic 0.16.9 arm64 binary is not bundled. Both supplied PDFs were fully read, rendered, and visually inspected. |
| Literature repairs LIT-1--LIT-5 | Locations and minor dependencies are enumerated in section 7 | Unresolved editorial work; add the sources, status labels, durable archives, and convention qualification specified there. |
| Finite-data practicality | `02_main_theorems.tex:38-45`; `16_scope.tex:30-36`; outside theorem scope, not a defect | No finite-sample, conditioning, bit-complexity, or practical-inference assessment was attempted because none is claimed. |

Subject to those explicit limits, my single independent verdict remains:
**not fully assessable**.
