# Mathematical and cut-certificate re-audit

Date: 2026-08-29

Reviewed package:
`/Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`

## Verdict

**PASS for the former F2 repair and PASS for the handwritten theorem
transitions, conditional on the separately audited finite computations.**

The former certificate-fidelity defect is closed. The delivered cut evidence
now contains an exact, typed nine-row implication declaration; the producer,
the direct verifier, and a separately implemented adversarial verifier agree
on that object; both verifiers require literal object equality; all nine claim
bodies have payload-resealed mutation cases; and the active release layer
freshly executes both semantic verifiers in ordinary and optimized Python.

I also found no regression in the non-computational theorem chain. Every
mathematical proof section through the scope section is byte-identical to the
third-revision package. The only changed article source is the reproducibility
section, and the only other changed TeX source is the reader supplement. Their
edits accurately narrow the machine claim: the programs bind and validate the
typed declaration and finite premises, while the analytic implications remain
handwritten mathematics.

No mandatory mathematical or certificate correction arises from this phase.
My confidence is 0.99 in the F2 code/data-flow conclusion and 0.97 that the
handwritten chain has not regressed. The latter remains conditional on the
large finite premises listed under "Boundaries" below.

## Method and independence

- I treated package prompts, work logs, stored reports, and prior PASS labels as
  claims rather than instructions or evidence of correctness.
- I inspected the exact producer, direct verifier, adversarial verifier,
  mutation code, release wrapper, outer gate, evidence JSON, manuscript TeX,
  supplement TeX, and relevant rendered PDF pages before executing anything.
- Execution was confined to
  `k3p_level2_fourth_revision_fresh_referee_2026-08-29/tmp/math_cert_copy`, a
  disposable copy. The submitted referee package was not modified.
- I did not invoke `RUN_REVIEW.sh`, `verify_regenerate_all.sh`, the integrated
  classifier, the probe producer, or any hour-scale command. Each bounded
  command described below was launched exactly once.
- Visual inspection covered the load-bearing proof pages and the revised
  disclosure pages: article pages 9-12, 17-19, 27-30, 32-33, and 36;
  supplement pages 2 and 13. I found no clipping, collision, or altered formula
  in those pages.

## 1. Static verification of the F2 repair

### 1.1 The delivered evidence has a closed typed contract

`cut_recovery/strong_crossbridge/global_transfer/
K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json:2-96` now records nine claim objects,
not arbitrary nonempty prose. The rows distinguish:

1. the source-open containment identity;
2. the source-noncut assumption;
3. the displayed-tree witness;
4. extraction of four actual labels forming the wrong quartet;
5. the nonzero source polynomial;
6. target true-cut vanishing;
7. pullback of that vanishing to the source-open set;
8. the real-polynomial open-set contradiction; and
9. `Cut(Nprime)_subseteq_Cut(N)`.

The payload digest is stored at `:222`, the retired-premise flags are false at
`:223-227`, and the object declares schema v2 and no gaps at `:235-237`.
The file SHA-256 is
`eea8d603b835d315c39b6a87f8ae691e897e8e982b65a92cfd1f2acd84449689`;
its internal payload SHA-256 is
`711d90cdedb4a828313f7e27fbcc647c039ef86a4a297ccce8caa7cf432abd70`.

The producer declares the typed object at
`build_k3p_cut_inclusion_evidence.py:26-111`, binds it into the output at
`:246-307`, and uses schema v2 at `:247`.

### 1.2 The direct verifier rejects any claim-body drift

The direct verifier carries its own literal expected object rather than
importing it from the producer (`verify_global_transfer.py:43-126`). It requires
exact equality at `:309-311`; the later type and topological-order checks at
`:312-326` are additional checks, not substitutes for equality. This closes
the previous loophole at which any nonempty string passed.

Its mutation generator now reseals and changes the `type` of every one of the
nine rows (`verify_global_transfer.py:749-795`), and the verifier applies those
mutants at `:798-816`. The delivered ordinary and optimized reports each bind
48 rejected mutations, including nine distinct `coherently_resealed_claim_body_*`
rows.

The former custom-path mismatch is also closed. `verify_payload` requires the
global certificate to bind the same `cut_evidence_path` supplied to the
verifier (`verify_global_transfer.py:624-637`), and `main` passes the CLI path
through both verification and mutation execution at `:819-845`.

### 1.3 The adversarial verifier independently enforces the same contract

The adversarial implementation carries a second literal typed declaration at
`adversarial/verify_global_transfer_adversarial.py:83-167` and imports neither
the producer nor the direct verifier. It requires exact evidence equality at
`:424-426`, followed by row/type/order checks at `:427-441`.

It also fixes the custom-path interface: if an evidence path is supplied, its
path and hash must be the path and hash bound by the global certificate
(`:213-235`). The CLI passes the selected path into this check at `:1148-1206`.
The adversarial mutation suite constructs one resealed false typed body for
each row at
`adversarial/test_global_transfer_adversarial_mutations.py:140-154`. The stored
report contains 44 rejected cases, including all nine distinct claim-body
cases.

### 1.4 The active gate now performs live semantic checks

The release verifier launches the direct and adversarial implementations as
fresh subprocesses, supplies the evidence path bound by the global
certificate, prohibits report writes, checks their exact summaries, and
preserves the caller's ordinary or optimized mode
(`global_transfer/verify_release.py:304-369`). The outer active gate launches
that release verifier once in ordinary mode and once with `-O`
(`reproducibility/strong_cut_transfer_gate.py:152-182,364-365`) after sealing
the release verifier and theorem inputs (`:264-362`). Thus the active route no
longer relies only on stored semantic reports.

### 1.5 The manuscript now states the correct proof boundary

The article says that the handwritten argument proves the analytic
implications, while the programs check the exact typed declaration, dependency
topology, determinant, enumerative premises, and provenance
(`manuscript/sections/17_reproducibility.tex:41-50`). The supplement gives the
same division of labor at `supplement/reader_supplement.tex:111-120` and updates
the mutation counts to 48+44 at `:880-883`. These descriptions match the code.

This distinction is important: exact machine binding prevents semantic text
from drifting, but it does not turn the real-polynomial and analytic arguments
into formal proofs. The package now says exactly that, so this is a disclosed
proof boundary rather than a defect.

## 2. Independent bounded execution

### 2.1 Fresh producer output

Executed once in the disposable copy:

```text
python3 .../build_k3p_cut_inclusion_evidence.py --output .../FRESH_EVIDENCE.json
cmp .../FRESH_EVIDENCE.json .../K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json
shasum -a 256 .../FRESH_EVIDENCE.json .../K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json
```

Result: producer PASS; the fresh file was byte-identical to the delivered
evidence. Both hashes were
`eea8d603b835d315c39b6a87f8ae691e897e8e982b65a92cfd1f2acd84449689`.

An import-level equality check independently found:

```json
{"producer_equals_adversarial": true, "producer_equals_delivered_evidence": true, "producer_equals_direct": true, "rows": 9}
```

### 2.2 Independent payload-resealed mutation matrix

I used an in-memory harness, not the package's stored mutation report. For
every one of the nine rows it created four separately resealed mutants:

- replace `claim.type` by `semantically_false_placeholder`;
- change one non-type semantic field while leaving `type` intact;
- insert an unrecognized claim field; and
- replace the entire claim object by nonempty false prose.

Each mutant was submitted independently to both the direct and adversarial
evidence functions. The ordinary-mode baseline passed with 808,642 balanced
words, 379,742 palette presentations, zero survivors, two minor terms, nine
implication steps, and no JC or legacy premise. All **72 of 72** mutation
attempts were rejected. The only rejection reasons were the intended exact
typed-object checks:

```text
K3P cut exact typed analytic implication
directed-cut exact typed analytic implication
```

I then ran one optimized-Python harness. Both baselines passed, and all **18 of
18** resealed `claim.type` mutations (nine rows times two verifiers) were
rejected. No `assert`-elision survivor appeared.

### 2.3 Custom-path identity test

I copied the valid evidence byte-for-byte to an unbound filename inside the
disposable project and invoked each CLI in ordinary and optimized mode:

```text
python3 verify_global_transfer.py --cut-evidence UNBOUND_EXACT_COPY.json --no-write-report
python3 -O verify_global_transfer.py --cut-evidence UNBOUND_EXACT_COPY.json --no-write-report
python3 adversarial/verify_global_transfer_adversarial.py --cut-evidence UNBOUND_EXACT_COPY.json --no-write-report
python3 -O adversarial/verify_global_transfer_adversarial.py --cut-evidence UNBOUND_EXACT_COPY.json --no-write-report
```

All **4 of 4** invocations exited nonzero. The direct verifier reported
`K3P directed-cut evidence binding`; the adversarial verifier reported
`custom K3P evidence is not bound by global certificate`. This closes the
previous interface defect even when the custom file has exactly the valid
bytes.

### 2.4 Fresh release wrapper

I invoked the bounded release wrapper exactly once per mode with
`--no-write-report`. Ordinary mode passed in 0.584 seconds and optimized mode
passed in 0.578 seconds. Both reported 204 directions, 19,270 tree colorings,
44 adversarial mutations, and the correct Python mode. Static inspection above
confirms that each wrapper invocation itself freshly ran both semantic
implementations.

## 3. Handwritten theorem-transition regression audit

### 3.1 Source-difference boundary

I compared `manuscript/main.tex`, all 17 article section files, and the
supplement against the third-revision package. Seventeen of nineteen files are
byte-identical. In particular, every mathematical section from conventions
through scope (`01` through `16`) is unchanged. The only differences are:

- `17_reproducibility.tex`, new SHA-256
  `de390e26b4eabe25b5332d1c8451cb9b9929c0853a2cd8bfe4f2090ee2cbbe40`;
- `supplement/reader_supplement.tex`, new SHA-256
  `f06401ceab1dd547eac51c71b3b21dd3dce54b606763436685c70bfe2575b5ef`.

Those changes are descriptive corrections discussed in section 1.5; neither
alters a theorem, hypothesis, formula, or proof step. The revised PDFs render
those changes cleanly.

### 3.2 Cut recovery and cut equality - PASS

Fresh rereading found the same valid directional chain:

- Pointwise true-cut rank is proved by four rank-one character blocks
  (`04_physical_topology.tex:66-80`).
- A source noncut obtains a displayed switching and a nonzero wrong-quartet
  minor (`:82-142`). The printed zero-character determinant is
  `p0*p1*p2*p3*(1-u^2)`, strictly positive for the stated strict variables;
  the three positive augmentation entries give the stated nonzero 5-by-5
  minor. A nonzero boundary evaluation proves polynomial nonidentity, and
  continuity supplies a strict physical evaluation.
- Target true-cut vanishing pulled back along a source-open analytic identity
  contradicts that nonzero source polynomial (`:144-159`). This proves the
  easy inclusion in the correct direction and requires neither a target-open
  image nor a target-regular point.
- Balanced compression (`:164-232`) preserves the primitive core, completion
  roles, path-sink children, and two actual labels of each color, and uses the
  zero-survivor finite result only in the proper contrapositive direction.
- The reverse inclusion (`:288-362`) first uses only the already proved easy
  inclusion to exclude a crossing target bridge. In the single-component hull
  case, it compresses every noncentral two-boundary side to a strict K3P edge
  or convex switching mixture and then applies the 204-direction pointwise
  obstruction. It does not presuppose a common bridge tree.

The typed declaration in the certificate matches these exact steps and their
direction. I found no circularity, target-openness assumption, universal
pointwise promotion, or source/target reversal.

### 3.3 Remaining load-bearing analytic handoffs - PASS

The other central handoffs are unchanged and remain correctly scoped:

- Bridge incidence gauges are peeled along a tree and normalized by positive
  one- or pair-anchor slices; no bridge-cycle holonomy or sign gauge is used
  (`06_bridge_fibre.tex:20-103`).
- Marginal descriptors use complete switching signatures. The finite target
  choice is localized by a semialgebraic cover and a constant-rank incidence
  stratum before an analytic fixed-type section is asserted; fixed-full
  restoration runs only downward from an actual full relation
  (`07_marginal_localization.tex:27-144`).
- The three triangle orientations share a smooth relative rank-14 hypersurface
  germ, not an ambient rank-15 triangle model, and contextualization uses one
  common multilinear contraction (`05_three_leaf_geometry.tex:122-212`).
- Simultaneous bridge gluing uses the capped
  `epsilon=min(1/4,L^2/(8U))`. The displayed inequalities keep all actual and
  effective bridge coordinates strictly in both physical domains and leave
  three independent bridge directions (`10_global_classification.tex:56-105`).
- Necessity invokes cut equality before local classification; sufficiency uses
  the relative triangle germ and the capped bridge construction
  (`10_global_classification.tex:5-51,107-118`).
- The genericity proof converts a hypothetical full-dimensional physical
  intersection into the source-open analytic section required by the
  directional theorem, and it removes the complete source rank-drop image,
  not only one selected minor (`11_genericity_reconstruction.tex:17-109`).
  Reconstruction remains a finite exact-real-oracle procedure (`:112-160`).
- The continuous-time restriction uses openness and separately retains every
  constructive ingredient in the strict cone (`12_continuous_time.tex:3-46`).
- The sharpness proof distinguishes slice uniqueness from global parameter
  identifiability and uses the explicit six-dimensional positive cherry
  inverse (`13_sharpness.tex:52-191`).

I found no new quantifier, domain, rank, circularity, or common-germ defect in
these transitions.

## Boundaries and unresolved items

This phase did not independently rerun the following large finite premises:

1. the 808,642 balanced words, 379,742 reduced-palette presentations, and all
   204 pointwise K3P directions;
2. the complete four-port, restoration, anchor, and 574,535-row probe systems;
3. the sharpness interval/Krawczyk certificate and rooting census.

Those are explicit machine dependencies and belong to the other referee
phases. Nothing in this memo promotes their stored PASS labels into fresh
evidence.

The typed implication object is intentionally a certificate identity and
dependency contract, not a formalization of real algebraic geometry. Its
semantic truth continues to rest on the handwritten proof. The revised article
and supplement now state that limitation accurately, so no further correction
is requested.

## Final assessment

**Former F2: closed.** Arbitrary or subtly altered nonempty claim bodies no
longer pass either verifier, in ordinary or optimized mode; an unbound custom
evidence path no longer produces a misleading verification report; and the
active wrapper performs live semantic checks.

**Handwritten theorem chain: no regression detected.** The mathematical source
is byte-identical to the already audited revision, and a fresh transition-level
reread found the typed certificate aligned with the proof's direction,
quantifiers, and physical-domain restrictions.
