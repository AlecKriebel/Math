# C1 re-audit: directed K3P cut-inclusion evidence

Date: 2026-08-29
Reviewed package: `/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29`
Method: read-only static inspection. I did **not** execute any package producer,
verifier, mutation suite, or stored command, and I do not credit any stored
`PASS`. I used only text inspection and an external SHA-256 utility. The four
checked current hashes agree with the strings stored in the package: the K3P
evidence is `6f3e37...b68d29`, the section-04 source is
`de19b7...81b27`, the direct verifier is `56dc79...ca47`, and the adversarial
verifier is `ff7c8d...7242`.

## Bottom line

There are two different conclusions, and they should not be conflated.

1. **Mathematical dependency (former C1): closed on static review, subject to
   replay of the finite computations.**  The current handwritten proof of
   \(\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)\) no longer invokes
   the companion JC pointwise cut theorem or the blocked legacy global-logic
   report. It supplies a K3P true-cut rank bound, a displayed-tree witness for a
   noncut, an explicit nonzero wrong-quartet minor, and the open-set
   contradiction. I found no circular use of cut equality in that chain.

2. **Certificate fidelity: not fully closed by the “fresh integrated” gate
   alone.**  The new evidence is genuinely load-bearing in the global proof
   DAG, and the dedicated direct and adversarial verifier functions reject a
   literal legacy-path substitution. However, both functions validate the
   nine-node analytic implication only as an ID/edge skeleton plus nonempty
   prose. The outer release/active/integrated path does not freshly execute
   those semantic functions; it rechecks stored reports and shallow summaries.
   Fixed hashes protect the delivered snapshot, but the existing “coherently
   resealed” test is not end-to-end coherent. Thus the supplied complete
   regeneration route is still essential evidence for C1, and the active gate
   should not be described as an independent semantic replay of the analytic
   implication.

My confidence is **0.93** that the former JC mathematical premise has been
removed, **0.98** in the static data-flow findings below, and only **0.60** in
the finite zero-survivor premises until they are executed in the required
isolated environment.

## 1. Handwritten mathematics: the JC premise has actually been replaced

The current proof chain is identifiable directly in
`proof_package/manuscript/sections/04_physical_topology.tex`:

- Pointwise true-cut rank is proved by four character blocks, each of rank one,
  at `:66-80`.
- The displayed-tree witness for a noncut is stated and proved at `:82-103`.
  The proof uses the two-color hull dichotomy in the abstract bridge-incidence
  tree. An edge in the hull intersection gives a crossing bridge split; a
  singleton component intersection reduces to the balanced cycle/theta case.
- Generic source-noncut recovery is proved at `:105-142`. It specializes to a
  displayed switching at inheritance endpoints, obtains a nonzero boundary
  evaluation, and moves back into the strict physical interior by continuity.
- The directed inclusion itself is derived by the open-set polynomial argument
  at `:144-159`.
- The same inclusion is then consumed noncircularly to exclude the crossing
  target-bridge alternative at `:288-303`; it is not inferred from a pre-existing
  common bridge tree.

The explicit determinant checks independently by hand. From the displayed
zero-character block at `04_physical_topology.tex:123-131`,

\[
1\cdot p_0p_1p_2p_3-(p_1p_3u)(p_0p_2u)
=p_0p_1p_2p_3(1-u^2),
\]

which is strictly positive for \(0<p_i,u<1\). Multiplication by one positive
entry \(p_0p_1\) in each of the other three blocks gives
\(p_0^4p_1^4p_2p_3(1-u^2)\), as recorded at
`K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json:82-155`. A nonzero evaluation at an
inheritance endpoint proves that the source minor is not the zero polynomial;
continuity supplies a strict physical evaluation. The target true-cut
proposition makes the same minor vanish after target composition, so vanishing
on a nonempty source-open set contradicts nonzeroness. This argument needs no
target regular point or target-open image.

The remaining substantive premise is the balanced-compression/finite handoff:
`04_physical_topology.tex:164-232` reduces the arbitrary complete component to
the finite palette, and `:234-272` states the 204 pointwise K3P obstruction.
Those are K3P/package premises, not a hidden JC theorem. Their reported
808,642-word and 379,742-presentation computations remain uncredited in this
static phase.

I found no JC or legacy-global-logic citation in section 04. The companion
manuscripts are discussed historically elsewhere, but they are not used in
this directed-inclusion proof.

## 2. The evidence is genuinely load-bearing

The evidence object is not parallel decoration:

- It records the nine-node implication at
  `K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json:2-61`, the exact minor at `:82-155`,
  the current K3P manuscript and standalone computational inputs at `:157-185`,
  and explicit false legacy/JC dependency flags at `:188-192`.
- Its producer binds the current manuscript, minor verifier, two finite
  producers/certificates, and replay script at
  `build_k3p_cut_inclusion_evidence.py:12-23,158-178`. It validates the stored
  finite-certificate schemas, scopes, counts, family sums, and zero-survivor
  facts at `:61-142`, constructs the determinant terms at `:145-209`, and emits
  the nine-node implication and provenance policy at `:210-271`.
- `build_global_transfer.py:11` imports that builder. On the default route it
  reads the evidence, freshly reconstructs the expected object, and requires
  exact object equality at `:259-288`.
- The global proof contains an explicit K3P node `K0`, and `D1` depends on both
  `H0` and `K0`, at `build_global_transfer.py:179-188`. The evidence file is an
  exact load-bearing input of the global certificate at `:317-326`, and the
  resulting evidence-pass assertion is at `:400-404`.
- The direct verifier requires the global certificate to bind the default
  evidence at `verify_global_transfer.py:557-562`, semantically inspects the
  supplied evidence at `:580-582`, and independently requires the `K0 -> D1`
  dependency and orientation at `:460-493`.
- The adversarial verifier independently hard-codes the current producer,
  verifier, evidence, manuscript, and finite-input hashes at
  `adversarial/verify_global_transfer_adversarial.py:57-80` and checks them at
  `:109-117`. It separately requires `D1` to consume `K0` at `:842-904`.
- The theorem manifest names the K3P mechanism at
  `global_transfer/THEOREM_MANIFEST.json:2-8`, makes the evidence load-bearing
  at `:66-74`, and declares the legacy/JC inputs unused at `:100-110`.
- The package-wide active manifest includes the K3P evidence as an active proof
  artifact at `proof_package/ACTIVE_MANIFEST.json:131-153`, while the old
  `CUT_GLOBAL_LOGIC_REPORT.json` occurs only under historical claim-correction
  evidence at `:491-501`.

Therefore the old defect—`D1` consuming a three-field legacy report while the
K3P material sat on a parallel branch—is not present in the current default
producer DAG.

## 3. What is independently checked, and what is not

The two verifier implementations do meaningful independent work:

- The direct verifier does not import the producer
  (`verify_global_transfer.py:1-9`). It requires the exact seven source names,
  paths, and current hashes at `:103-116`; checks balanced and palette schemas,
  scopes, totals, family sums, mutation flags, and zero survivors at `:130-194`;
  rederives the two determinant terms at `:196-221`; and checks the implication
  topology at `:223-251`.
- The adversarial verifier likewise imports neither producer nor direct
  verifier (`adversarial/verify_global_transfer_adversarial.py:1-15,126-132`).
  It rejects source paths containing `global_logic` or
  `referenced_chat_manuscripts` at `:156-175`, checks the current manuscript and
  exact-minor source at `:177-200`, independently audits the two finite
  certificate summaries at `:201-278`, rederives the determinant at `:280-321`,
  and checks the implication topology at `:323-351`.
- The finite inputs can be freshly reproduced by
  `palette_independent/verify_cut_combinatorics.py:25-55`, which runs the two
  producer implementations into temporary outputs and byte-compares them.

But neither evidence verifier proves or semantically reconstructs the complete
analytic implication. The exact gap is visible in the code:

- `target_cut_vanishing` is an axiom node with no dependency in the evidence at
  `K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json:34-38` and in the producer at
  `build_k3p_cut_inclusion_evidence.py:243-246`.
- Both validators require exact IDs and dependency edges, but require every
  intermediate `claim` only to be a nonempty string:
  `verify_global_transfer.py:223-251`, especially `:247-248`, and
  `adversarial/verify_global_transfer_adversarial.py:323-351`, especially
  `:347-348`. Only the final conclusion text is exact.
- The manuscript snippet lists do not even require the true-cut proposition or
  its proof. They check selected headings/formulas and include the directed
  conclusion itself: `build_k3p_cut_inclusion_evidence.py:61-76`,
  `verify_global_transfer.py:118-128`, and
  `adversarial/verify_global_transfer_adversarial.py:177-190`. This establishes
  source identity/presence, not proof semantics.
- The current semantic mutation lists test legacy-path substitution, removal of
  the minor, and removal of an implication edge, but not alteration of an
  intermediate claim body: `verify_global_transfer.py:678-711` and
  `adversarial/test_global_transfer_adversarial_mutations.py:110-143`.

Consequently a payload-resealed evidence object can replace, for example,
`source_noncut_nonzero.claim`, `target_cut_vanishing.claim`, or
`composition_pullback.claim` by arbitrary or circular nonempty prose and still
pass both `verify_cut_inclusion_evidence` functions. This is a **certificate-
fidelity defect**, not a counterexample to the current handwritten proof. The
default full producer route protects the frozen artifact because
`build_global_transfer.py:259-288` reconstructs and exact-compares the
producer's hard-coded correct object.

The article and supplement currently overstate this boundary. The assertion
that the two verifiers validate “analytic dependence” at
`manuscript/sections/17_reproducibility.tex:41-46`, and “the full analytic
implication” at `supplement/reader_supplement.tex:112-117`, is not supported by
the verifier logic. They validate source hashes, selected finite semantics, the
minor, and the implication graph shape; the non-computational implications
remain handwritten mathematics.

**Severity:** moderate, repairable certificate-fidelity/presentation defect;
no direct adverse theorem dependency because the current source proof supplies
the missing semantics and the full default producer fixes the intended text.

## 4. The outer active/integrated route is report-replay, not a fresh semantic C1 replay

This distinction is load-bearing for an independent referee:

- `verify_release.py:82-159` loads the global certificate, evidence, and stored
  ordinary/optimized direct reports and checks their hashes and summaries. Its
  adversarial layer similarly loads the stored audit/report/mutation artifacts
  at `:183-300`. It does not execute either semantic verifier.
- `strong_cut_transfer_gate.py:151-175` freshly invokes only
  `verify_release.py`. Its own direct evidence check is limited to
  schema/status/`remaining_gaps` and the four provenance flags at `:280-293`.
- The integrated consumer binds the evidence and checks its payload, conclusion,
  counts, factorization string, provenance flags, and `len(analytic_implication)
  == 9` at `verify_k3p_same_classification.py:1213-1255`; it does not check the
  seven internal source bindings or exact intermediate claims.
- Its “fresh” phase invokes the outer strong gate and mutation suite and then
  separately replays the word combinatorics and displayed minor at
  `verify_k3p_same_classification.py:1967-1993`. It does not freshly run the
  evidence builder, global builder, direct verifier, or adversarial verifier.
- By contrast, the complete regeneration plan explicitly orders evidence
  construction, global construction, ordinary and optimized direct verification,
  adversarial verification/mutations, release verification, and manifest build
  at `referee_tools/ACTIVE_VERIFIER_PLAN.json:46-83` and
  `reproducibility/run_release_suite.py:180-214`.

The referee prompt itself correctly requires **both** the fresh integrated
replay and the complete producer/verifier regeneration
(`REFEREE_PROMPT.md:83-91`). Thus this layering is not fatal if that full route
is actually run and credited separately. It does mean that an integrated-gate
`PASS` alone does not independently establish C1.

The current outer mutation does not establish end-to-end coherent-substitution
resistance. `reproducibility/test_cut_transfer_gate_mutations.py:108-153`:

1. changes the evidence provenance flag;
2. updates that evidence's payload digest and its two theorem-manifest hashes;
3. patches the copied gate's hard-coded theorem-manifest hash; and
4. labels the result `all_affected_hashes_resealed: True` at `:152`.

It does **not** rebind the changed evidence through the global certificate,
ordinary/optimized direct reports, adversarial audit/report/mutation manifest,
or release reports. Moreover it is rejected early by the outer gate's explicit
provenance check at `strong_cut_transfer_gate.py:288-293`, before the fresh
release invocation at `:342-343`. The test usefully proves that one Boolean is
checked, but its “all affected hashes” description is false and it does not
test a semantically disguised legacy-source substitution.

Static data flow predicts that a more coherent fixture can pass the outer cut
gate if it changes the evidence's `displayed_tree_lemma` binding to the legacy
report while dishonestly retaining all four provenance flags as `False`, then
updates the downstream stored hashes/reports and repins the copied theorem-root
constant. The live direct and adversarial semantic functions would reject that
fixture because they require the exact current source map; the outer gate never
calls them. This prediction must be tested, not reported as an executed result.

**Severity:** load-bearing for certificate fidelity. It is major if the
four-command active/integrated plan is presented as sufficient semantic
validation by itself; it is a moderate, repairable workflow condition in the
documented referee process because the separately required complete
regeneration executes the missing producer and verifiers. The mathematical
theorem is not invalidated.

## 5. Additional verifier-interface defect

`verify_global_transfer.py` accepts a custom `--cut-evidence` path at
`:735-746`, semantically checks the object loaded from that path at `:580`, and
records that custom file's hash at `:749-755`. But the global certificate is
always required to bind the fixed default `CUT_EVIDENCE`, not the supplied
argument, at `:557-562`.

Thus a standalone verification report can describe a custom evidence object
while certifying a global artifact bound to a different evidence object. The
active default route and release manifest require the default hash, so this is
not an active C1 bypass. It is a **low-severity verifier-interface defect**.
Either remove the custom argument, require it to resolve to the default path,
or pass its actual path into `verify_payload` and require the global binding to
match that same file.

## 6. Active-manifest metadata inconsistency

`proof_package/ACTIVE_MANIFEST.json:319-321` says the cut-transfer gate mutation
suite passed “12 of 12,” while the bound report is described as 16 rejected
mutations at `:395-397`, and the actual JSON declares `mutation_count` and
`rejected_count` equal to 16. This is editorial/stale metadata, not a theorem
defect. The manifest version string still says “second-referee” at `:382`, also
suggesting a stale revision label.

## 7. Bounded isolated mutation plan (not executed)

All execution must occur later in a disposable copy under a real default-deny
isolation boundary with no network or credential/sibling reads, as required by
the referee prompt. Preserve the clean package and full transcripts.

### A. Exact-claim semantic test

1. Copy the evidence and replace
   `analytic_implication[target_cut_vanishing].claim` with a circular nonempty
   sentence such as “this follows from directed cut inclusion.” Leave IDs,
   edges, final conclusion, source bindings, and provenance flags untouched.
2. Recompute only `payload_sha256`.
3. Feed the mutant to the direct `verify_cut_inclusion_evidence` function and
   to the adversarial function's evidence argument. Static prediction: both
   accept it.
4. Repeat for `source_noncut_nonzero` and `composition_pullback`.
5. Control: a full evidence/global producer run should overwrite or reject the
   mutant because it exact-reconstructs the intended object.

### B. Coherent legacy-source substitution through the outer cut gate

1. Establish a clean outer-gate baseline in the isolated copy.
2. Change only the evidence's `displayed_tree_lemma` path/hash to
   `cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json`; keep the provenance
   flags falsely `False`, and recompute the evidence payload hash.
3. Propagate the new evidence/global-certificate hashes through both direct
   reports, the adversarial audit and report, its mutation report and manifest,
   both release reports, and the theorem manifest. Do not alter either semantic
   verifier's logic.
4. Repin only the copied outer gate's theorem-root hash, matching the attack
   model already used at `test_cut_transfer_gate_mutations.py:130-140`.
5. Run the copied outer cut gate. Static prediction: it passes because its live
   execution reaches only the release wrapper and its evidence semantics stop
   at the false provenance flags.
6. Controls: directly run the direct and adversarial semantic verifiers on the
   same fixture; both should fail at the exact source-map check. Run complete
   regeneration; the evidence builder should restore the K3P source and the
   mutated downstream chain should cease to reproduce.

### C. Integrated-root extension

After phase B, inventory the additional theorem/evidence hashes sealed by
`global_infrastructure` and the integrated report. Propagate the fixture only
through data artifacts, repinning copied top-level root constants exactly once,
then test artifact-only and fresh integrated modes. This phase must be reported
separately: a failure at an unchanged outer hash proves identity locking, while
a pass after coherent repinning tests semantic resistance. Do not call either
outcome evidence about the handwritten theorem.

### D. Custom-path identity test

Invoke `verify_global_transfer.py --cut-evidence <mutant> --no-write-report`
with the default global certificate and evidence left untouched. Use an
otherwise semantically accepted mutant with one nonfinal claim changed and a
valid payload digest. Static prediction: it passes while reporting the mutant
hash even though the global certificate binds the default evidence.

## 8. Minimal repair

For a fail-closed certificate claim, the minimum repair is:

1. Make both evidence verifiers require the exact nine-row implication object,
   including every claim, or replace prose claims by typed predicates with
   exact values. Add exact checks/bindings for the true-cut proposition and
   generic-noncut proof environment.
2. Add payload-resealed claim-body mutations for `target_cut_vanishing`,
   `source_noncut_nonzero`, and `composition_pullback`.
3. Make the active cut gate freshly execute the direct and adversarial semantic
   verifiers (ordinary and optimized where relevant), rather than only the
   report-checking release wrapper. A temporary fresh rebuild and byte
   comparison of the K3P evidence should also be part of that gate.
4. Replace the current outer legacy mutation by a truly downstream-resealed
   fixture, or remove the inaccurate `all_affected_hashes_resealed: True`
   assertion.
5. Bind the direct verifier's custom evidence argument to the same file as the
   global certificate, and correct the two stale active-manifest strings.

The code should not claim to machine-validate the non-computational analytic
proof. A precise and defensible description is: the package binds the current
handwritten K3P proof, independently checks its exact displayed-tree minor and
finite combinatorial premises, and verifies the intended dependency topology;
the analytic implications themselves are subject to human proof review.

## Independent C1 verdict

**Former theorem condition C1:** closed on the present handwritten proof; no
active JC cut theorem or legacy global-logic premise remains. Final acceptance
still requires isolated replay of the finite K3P computations.

**Certificate condition C1:** valid only subject to a named minor-to-moderate
repair or to explicit reliance on the separately executed complete regeneration
route. The integrated/release gate alone is not a fresh semantic validation,
and the package currently overstates what its two implication verifiers check.
