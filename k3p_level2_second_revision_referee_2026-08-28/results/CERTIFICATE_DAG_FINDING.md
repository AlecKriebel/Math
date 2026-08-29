# Mandatory finding: the active cut certificate still depends on the retired JC route

## Severity and scope

**High certificate-fidelity defect; repairable without changing the revised
theorem proof.** The manuscript's new K3P cut argument is sound, but the active
machine-readable dependency graph does not consume it at the step where it is
needed.

## Exact evidence

All paths are relative to the reviewed package's `proof_package` directory.

1. The alleged load-bearing input is explicitly unresolved.

   - `cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json:1-22` has verdict
     `B-PRECISE-UNRESOLVED-IMPLICATION` and status
     `BLOCKED_BY_DIRECTED_CUT_REVERSE_INCLUSION`.
   - `cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.md:63-103` derives the
     easy directed inclusion using corrected JC and states the former reverse
     gap.
   - Its input hashes at JSON lines 67-77 bind `jc_level2_source.tex` and the
     former cut reports.

2. The active producer promotes that object without validating it.

   - `cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py:177-181`
     states proof step D1 by “isotropic-JC generic recovery.”
   - Lines 252-271 read the old report but require only
     `proved_inclusion == Cut(N_prime)_subseteq_Cut(N)` and
     `target_regular_not_assumed == true`.
   - Lines 300-328 label the report a load-bearing input and issue a `PASS`
     certificate whenever the separate 204-direction layer passes.

3. The active verifier checks the assertion, not its proof.

   - `verify_global_transfer.py:345-370` checks the legacy file hash and three
     stored values: the inclusion orientation,
     `reverse_inclusion_proved == false`, and target regularity. It never checks
     the report schema, blocked status, or a K3P derivation.
   - Its 30 mutations at lines 414-448 mutate the generated certificate, not
     the semantic premise in the legacy report.

4. The nominally independent adversary has the same premise.

   - `global_transfer/adversarial/verify_global_transfer_adversarial.py:32-65`
     hard-binds the old report and the complete JC manuscript.
   - Lines 593-651 trust the same report booleans and text-mine JC topology
     snippets.
   - Lines 677-682 require only nonempty reason strings for the logical steps.
   - `ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json:110-114` still identifies D1 as
     `generic_isotropic_JC_noncut_minor...`.

5. Downstream seals preserve rather than repair this dataflow.

   - `global_transfer/THEOREM_MANIFEST.json:63-70` calls the legacy report
     load-bearing.
   - `reproducibility/strong_cut_transfer_gate.py:70-79,221-290` requires that
     exact load-bearing set and a hard-coded theorem-manifest hash.
   - `reproducibility/verify_k3p_same_classification.py:1103-1141` validates the
     new balanced-word and displayed-tree-minor evidence, while lines
     1144-1196 independently validate the old transfer gate. No logical edge
     makes the former the premise of D1.
   - `ACTIVE_MANIFEST.json:143-146` promotes the transfer theorem while lines
     479-488 call the same legacy report historical. It also retains the JC
     manuscript as an active input, despite its inventory status
     `frozen_input_unverified`.

## Adversarial semantic test

The producer and its direct verifier accept an otherwise proof-free replacement
of the legacy report after local rebinding, provided these three values remain:

```text
proved_inclusion = Cut(N_prime)_subseteq_Cut(N)
reverse_inclusion_proved = false
target_regular_not_assumed = true
```

Naive byte changes are caught by hashes. That is not semantic independence:
after coherent resealing of the adversarial bindings and downstream constants,
no active consumer rederives D1. The historical
`global_logic/verify_global_logic.py` would reject such a replacement, but it
is not in the current 54-command mathematical plan.

## Mathematical impact

This is not a counterexample to the paper. The revised proof at
`manuscript/sections/04_physical_topology.tex:82-159` independently supplies:

- a displayed-tree witness for every noncut;
- an explicit K3P boundary determinant
  `p0*p1*p2*p3*(1-u^2)`;
- a strict five-by-five wrong-flattening minor; and
- the correct nonzero-polynomial/open-set argument for the easy inclusion.

The reverse inclusion at lines 274-356 then uses the separately certified 204
pointwise K3P directions without circularity. Thus theorem correctness is
supported, while the package's claim of a self-contained active certificate
graph is false as delivered.

## Required repair

1. Replace `directed_cut_inclusion_audit` with a K3P D1 evidence object bound
   to the revised displayed-tree lemma, the exact five-by-five minor, the
   balanced-word certificate, and the clean-room palette replay.
2. Rewrite D1 in the global producer and both independent/adversarial
   verifiers; validate the implication, not a stored inclusion string.
3. Remove the JC manuscript and old blocked report from all active/load-bearing
   sets; preserve them only as historical provenance.
4. Add a coherent premise-removal/provenance-substitution mutation.
5. Rebuild and reseal the transfer certificate, adversarial layer, theorem
   manifest, primary/global/integrated reports, release artifacts, and referee
   package; then rerun the full plan.
