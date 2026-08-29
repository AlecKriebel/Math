# Severity-ranked findings

Date: 2026-08-29
Package: `/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29`
Audit: `/Users/alec/Documents/Math/k3p_level2_third_revision_fresh_referee_2026-08-29`

## Executive assessment

I found **no remaining theorem-level counterexample, circularity, quantifier
shift, or physical-domain gap**. The handwritten chain passed independent
review, conditional on its finite premises; the subsequent isolated complete
regeneration ran all 55 mathematical command bodies successfully. The exact
failure is instead a deterministic file-mode drift in the portable referee
runner. A separate C1 certificate-fidelity vulnerability was confirmed, but it
does not make the current K3P cut proof false: the canonical producer supplies
the correct implication text and the handwritten proof supplies its semantics.

The appropriate disposition is therefore **minor revision / valid subject to
explicit software-and-attestation corrections**, not mathematical major
revision. The mode defect is release-blocking for an exact reproducibility
claim, while the C1 repair is needed to align the advertised semantic
verification boundary with what the code actually checks.

| Rank | Finding | Severity by layer | Theorem impact |
|---:|---|---|---|
| 1 | Portable `verify` and `regenerate` cannot finish because regenerated JSON modes drift from `0644` to `0600` | **Major/blocking reproducibility defect; mechanical repair** | None detected; bytes and SHA-256 values are unchanged and every mathematical command body passed |
| 2 | C1 implication verifiers accept payload-resealed false nonfinal claim text; the custom evidence can differ from the evidence bound by the global certificate | **Moderate certificate-fidelity defect** | None for the current frozen theorem; handwritten K3P proof and canonical full regeneration remain correct |
| 3 | Mutation/manifest descriptions are stale or overstate what was resealed and checked | **Minor metadata/editorial defect** | None |
| 4 | Source ZIPs are canonical, but the PDF-reproduction contract does not bind its resource bundle or seal current reports; fresh article build was inconclusive after a referee-sandbox failure | **Moderate reproducibility limitation** | None; no source/PDF mismatch observed |
| 5 | Theorem-level mathematics | **No adverse finding** | Handwritten PASS plus 55/55 regeneration bodies and independent spot checks |

## F1 — Exact reproducibility failure: deterministic mode drift

**Severity:** major for portable reproducibility and release completion;
low-complexity repair; no mathematical-content effect.

### Observed result

The complete isolated regeneration did what the mathematics requires before
the runner's final integrity check:

- package integrity passed at
  `logs/supervisor_regenerate_20260829T172724.243510Z.log:1-2`;
- every one of the 55 ordered mathematical commands reports `PASS` at `:3-57`;
  this includes K3P evidence construction, global cut construction, ordinary
  and optimized direct verification, adversarial verification/mutations,
  release binding, the hour-scale four-port/probe producers, restoration,
  sharpness, global infrastructure, primary rebinding, and the final integrated
  replay;
- the integrated replay itself reported `CERTIFIED_K3P_SAME` and its sentinel at
  `package_copy/review_runs/20260829T172726.410212Z/regenerate/transcript.log:1325-1329`;
- the final classification mutation suite rejected all 27 mutations at
  `:1331-1335`.

The runner then returned `K3P_REFEREE_ACTIVE_VERIFIERS_FAIL` solely because 11
pre-existing JSON files changed mode from sealed `0644` to `0600`, with the
same byte counts and SHA-256 values
(`logs/supervisor_regenerate_20260829T172724.243510Z.log:58`):

1. the eight `primary_exact_evidence.json` outputs under `model_domain`,
   `three_port`, `topology` (three files), `bridge_fibre`, `marginals`, and
   `four_port_atlas`;
2. `reproducibility/primary_gate_report.json`;
3. `reproducibility/strong_class_cut_transfer_gate_report.json`; and
4. `cut_recovery/strong_crossbridge/topology_regeneration/CUT_TOPOLOGY_REGENERATION_REPORT.json`.

The earlier four-command bounded replay exhibited the same defect on the first
ten files (the topology-regeneration report is not rewritten by that shorter
route): `RESEARCH_LOG.md:31-41`. Its four command bodies passed, and its fresh
integrated child report recorded 20/20 passing replays and status `CERTIFIED`
at `:33-37`. The repeated failure makes this a deterministic portability bug,
not a transient filesystem event.

New files under `release/work/**` were separately classified as permitted
runtime drift; they were not the reason for failure. The trusted external
supervisor records return code 1 and status `FAIL`, but also records both the
outer package payload and venv unchanged
(`execution/supervisor_regenerate_20260829T172724.243510Z.json:12-22`). Thus the
failure was the copied workspace's undeclared mode drift, not source-package or
dependency-environment mutation.

### Exact cause

The runner correctly inventories modes as well as content:

- `referee_tools/run_active_verifiers.py:45-83` records type, mode, bytes, and
  SHA-256;
- `:86-98` treats a mode change as a changed record;
- only `release/work/**` drift is declared runtime output, and any other change
  is rejected at `:593-605`.

The producers replace sealed public JSON files using `NamedTemporaryFile`,
whose newly created file is mode `0600`, without restoring the target's mode:

- the primary producer: `proof_package/reproducibility/verify_primary.py:79-88`;
  it writes the eight primary evidence files at `:514-528` and the primary gate
  report at `:687`;
- the strong cut gate: `proof_package/reproducibility/strong_cut_transfer_gate.py:373-381,398-399`;
- the topology regeneration verifier:
  `proof_package/cut_recovery/strong_crossbridge/topology_regeneration/verify_cut_topology_regeneration.py:185-194,250-254`.

The runner's location-dependent primary-report restoration writes the canonical
bytes back to the already replaced path but does not restore its original mode
(`referee_tools/run_active_verifiers.py:436-455`). Thus byte restoration cannot
repair the `0600` inode mode.

This behavior is independent of the documented `0022` child umask because
secure temporary-file creation deliberately starts at `0600`.

### Required repair and acceptance test

Do not weaken the runner's mode-integrity gate. Instead, centralize atomic JSON
writing so that an overwrite preserves `stat.S_IMODE(existing.stat().st_mode)`;
for a new public report, select and document an explicit mode, normally `0644`.
Apply that helper to the three writers above and make
`preserve_and_restore_primary_report` restore both canonical bytes and canonical
mode. A safe pattern is to `chmod` the temporary file to the intended mode
before `os.replace`.

Acceptance requires:

1. a unit test that overwriting a `0644` target preserves `0644`;
2. the four-command portable `verify` route ending with its runner-level PASS,
   not merely four child PASS records;
3. one clean complete regeneration ending with runner-level PASS, zero
   undeclared workspace drift, and zero venv drift.

The existing 55/55 run need not be interpreted as a mathematical failure; it
is evidence that the content-producing computations reproduced even though the
wrapper correctly refused to certify the filesystem endpoint.

## F2 — C1 certificate fidelity: false implication prose is accepted

**Severity:** moderate certificate/attestation defect; no detected theorem
error.

### Confirmed behavior

The independent mutation changed all eight nonfinal rows of
`analytic_implication` to the same semantically false but nonempty placeholder,
left the final `Cut(Nprime)_subseteq_Cut(N)` claim exact, and recomputed the
evidence payload digest
(`independent_checks/check_cut_claim_fidelity.py:34-47`). It then invoked the
current direct verifier in ordinary and optimized modes with the mutant as
`--cut-evidence`, with built-in mutations enabled (`:49-69`).

Both executions returned exit code 0 and reported `PASS`, 15 proof steps, and 39
rejected built-in mutations
(`independent_checks/results/c1_claim_fidelity/REPORT.json:42-70`). The report's
verdict is `VULNERABILITY_CONFIRMED` at `:73-74`, and it records that the global
certificate continued to bind the unmodified default evidence at `:36-41`.

That behavior follows directly from the verifier:

- it requires exact implication IDs and dependencies, but each nonfinal claim
  only has to be a nonempty string at
  `proof_package/cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py:223-251`, especially `:247-248`;
- the independently implemented adversarial verifier has the same check at
  `.../adversarial/verify_global_transfer_adversarial.py:323-351`, especially
  `:347-348` (this second function was established statically here; the
  independent executed mutation above exercised the direct verifier);
- the command-line verifier loads an arbitrary `--cut-evidence` object at
  `verify_global_transfer.py:735-747` and reports its hash at `:749-755`, while
  the global certificate is always checked against the fixed default evidence
  at `:557-562`.

The article/supplement consequently overstate the machine boundary when they
say the verifiers validate “analytic dependence” or the “full analytic
implication” (`manuscript/sections/17_reproducibility.tex:41-46`;
`supplement/reader_supplement.tex:111-117`). They validate the source hashes,
finite summaries, exact minor, and DAG shape; they do not validate the truth of
the prose implications.

### Why this is not a theorem-level C1 failure

The current handwritten K3P proof independently supplies the missing semantics:

- true-cut rank: `manuscript/sections/04_physical_topology.tex:66-80`;
- displayed-tree noncut witness: `:82-103`;
- generic noncut polynomial/minor: `:105-142`;
- directed inclusion: `:144-159`;
- noncircular downstream use: `:288-303`.

The global producer also imports the canonical evidence builder and requires
exact object equality at
`global_transfer/build_global_transfer.py:11,259-288`; `D1` explicitly depends
on the K3P node `K0` at `:179-188`. In the fresh complete regeneration, the
canonical evidence builder, global builder, ordinary/optimized direct
verifiers, adversarial verifier/mutations, and release/manifest steps all
passed (`supervisor_regenerate...log:20-29`). Thus the delivered default route
did not consume the false mutant.

The former external JC premise is therefore removed. What remains is an
attestation weakness: the direct verifier can certify a supplied auxiliary
object different from the object bound by its global certificate, and both
semantic functions undercheck the meaning of the implication rows.

The outer cut/integrated gate also deserves precise wording. It freshly invokes
the release wrapper, which validates stored direct/adversarial reports, rather
than freshly executing those semantic verifiers
(`verify_release.py:82-159,183-300`;
`strong_cut_transfer_gate.py:151-175,280-293`;
`verify_k3p_same_classification.py:1213-1255,1967-1993`). The complete
regeneration does execute the missing chain, so the full referee route is
stronger than the integrated gate alone.

### Required repair

1. Require the exact intended nine-row implication object (or typed exact
   predicates) in both verifier implementations, including every claim body.
2. Bind the evidence path passed on the command line to the same evidence file
   named by the global certificate, or remove the custom argument.
3. Add claim-body mutations for at least `target_cut_vanishing`,
   `source_noncut_nonzero`, and `composition_pullback`, in ordinary and
   optimized modes.
4. Make the active cut gate freshly invoke the direct and adversarial semantic
   checks, or state explicitly that only the complete regeneration supplies
   that replay.
5. Narrow the article/supplement language: the analytic implications are
   handwritten proof obligations; the programs bind them and verify their
   finite/algebraic premises and dependency topology.

## F3 — Stale and inaccurate metadata

**Severity:** minor editorial/certificate-description defect; no theorem
impact.

Three concrete inconsistencies should be corrected:

1. `proof_package/ACTIVE_MANIFEST.json:319-321` says the cut-transfer gate suite
   passed 12 of 12, while the same manifest binds a 16-rejection report at
   `:395-397`. The report itself says `mutation_count = rejected_count = 16` at
   `proof_package/reproducibility/CUT_TRANSFER_GATE_MUTATION_REPORT.json:20-29,152-155`.
2. The active manifest's version string still says
   `0.9.0-second-referee-certificate-dag-repaired` in this third-revision package
   (`ACTIVE_MANIFEST.json:382`).
3. The mutation report says `all_affected_hashes_resealed: true`
   (`CUT_TRANSFER_GATE_MUTATION_REPORT.json:20-29`), but the test changes only
   the evidence payload, the evidence hashes in the theorem manifest, and the
   copied gate's theorem-root constant
   (`reproducibility/test_cut_transfer_gate_mutations.py:108-153`). It does not
   rebind the global certificate, direct reports, adversarial audit/report/
   manifest, or release reports. The test validly proves sensitivity to the
   explicit provenance Boolean, but it is not an end-to-end coherent-reseal
   test.

These are straightforward textual/report-generation repairs. The third item
should be fixed either by implementing a genuinely downstream-resealed mutation
or by renaming the field to describe the narrower hashes actually updated.

## F4 — Source reproduction contract is incomplete

**Severity:** moderate reproducibility limitation; no mathematical effect and
no observed source/PDF mismatch.

Both delivered source ZIPs were independently reconstructed byte-identically
from the exact Git blobs at `738b662...9d6`, with zero source-member mismatch.
The supplement's one isolated offline command completed its two internal builds
and matched the delivered PDF twice. The article's sole allowed invocation
stopped before a completed build because the initial referee Seatbelt profile
omitted a SystemConfiguration Mach lookup required during Tectonic
initialization; it was not relaunched. This is an inconclusive fresh check, not
an archive or PDF failure (`results/SOURCE_ARCHIVE_REPRODUCTION.md`).

Static inspection nevertheless found that the release contract pins the
Tectonic executable but not its resource bundle/cache, inherits the caller's
full environment (`release/verify_source_reproduction.py:211-220`), and does
not seal final-commit source-reproduction reports or transcripts in the
package. The article is strongly corroborated by an earlier two-build report
using the same 23 source bytes, delivered PDF, and pinned executable, but that
report is ignored live-work evidence at an earlier bookkeeping commit and was
not promoted to a fresh final-commit PASS.

The release should bind or vendor the bundle, force offline/only-cached
operation under a minimal environment, and seal current reports/transcripts.
A final article two-build run under that contract closes the one unexecuted
fresh check.

## F5 — Theorem-level status after the fresh evidence

**Finding:** no theorem-level issue remains from the reviewed transitions.

The independent handwritten report concludes PASS for the full
non-computational proof chain, conditional only on the disclosed finite exact
premises (`results/HANDWRITTEN_PROOF_REAUDIT.md:3-16`). Its transition-by-
transition audit finds the cut proof noncircular (`:36-98`), then clears bridge
fibre, localization/restoration, triangle contextualization, gluing,
genericity/reconstruction, continuous-time restriction, and all-\(n\) sharpness
(`:100-273`). Its final conclusion identifies certificate fidelity—not a hidden
quantifier/domain/circularity flaw—as the remaining risk (`:296-304`).

The finite evidence was then materially replayed:

- all 55 complete-regeneration command bodies passed, including the hour-scale
  producers and all active mathematical mutation suites
  (`logs/supervisor_regenerate_20260829T172724.243510Z.log:3-57`);
- seven independent spot-check families passed in 40.46 seconds without
  changing the package seal
  (`independent_checks/results/fresh_spots_20260829/SUITE_REPORT.json:1-84`);
- the independent revised-cut check rederived the 808,642 closed-form count and
  exact displayed-tree determinant without package imports or stored
  certificates
  (`independent_checks/results/fresh_spots_20260829/revised_cut.json:106-170`);
- the separately staged exact-checkout release-engineering suite rejected all
  32 mutations with 11 controls, left the self-contained checkout clean, and
  reproduced the sealed report
  (`results/RELEASE_ENGINEERING_REPLAY.json:1-23`).

These facts do not turn hashes or successful programs into a formal human proof
of their own correctness, but together with the static producer/verifier audits
they discharge the concrete finite premises to the standard normally expected
for this computer-assisted theorem. The mode failure does not alter any
mathematical payload; the C1 false-claim mutant was a verifier-boundary test and
was not used by the canonical regeneration.

## Recommended overall wording

> The stated K3P classification theorem is supported by a complete handwritten
> argument and a successful fresh replay of every mathematical command body. No
> theorem-level defect was found. The delivered portable runner nevertheless
> fails its own final exact-reproducibility gate because several atomic JSON
> writers change sealed public-file modes from `0644` to `0600`. In addition,
> the C1 evidence verifiers undercheck nonfinal analytic claim text and allow a
> custom evidence object to differ from the evidence bound by the global
> certificate. Both defects are repairable without changing the theorem or its
> mathematical artifacts. Acceptance should be conditional on preserving file
> modes, obtaining clean runner-level PASS for both verify and regeneration,
> tightening the C1 evidence binding/claim checks, and correcting stale
> mutation metadata and explanatory language. The PDF-source contract should
> also bind its Tectonic bundle, force a minimal offline environment, seal
> current build evidence, and close the inconclusive fresh article build.

On the evidence presently available, this supports **minor revision / valid
subject to the named corrections**, with high confidence that no theorem-level
repair is required.
