# Adversarial release-engineering and archive audit

> **Evidentiary-status notice.** This delegated sub-audit's code inspection
> and static findings are retained, but its dynamic executions occurred
> outside the operating-system sandbox required by the referee mandate. Those
> executions are excluded from the final evidentiary record. The same mutation
> and double-archive-build claims were subsequently reproduced in the compliant
> sandbox and are documented in `release_reproduction_compliant.md`.

**Audit date:** 2026-08-27
**Delivered package:** `/Users/alec/Documents/Math/k3p_level2_identifiability_final/release/dist/K3P_Level2_Independent_Referee_Package`
**Sibling release artifacts:** `k3p_level2_compact_verifier.zip` and `k3p_level2_reproducibility.tar.gz` in the same `release/dist/` directory
**Scope:** the 32 release-engineering mutations, deterministic construction of both release archives, the extracted-archive gate, the 600-file handoff seal, and source commit `76a097fbc4ddadf23ba0119a371c5ac29f4802b1`. The delivered package was not modified. Expensive mathematical producers, the complete mathematical verifier/regeneration suite, and the hour-scale probe were not run.

## Verdict

**PASS with one moderate audit-trail defect and two minor wording/contract defects.** I found no false release-engineering result among the five claims tested. In fresh, clean, temporary checkouts I reproduced all 32 mutation rejections; rebuilt both current archives byte-for-byte; safely extracted both and reproduced their identical artifact-only classification-gate transcript; and rebuilt the entire 600-payload referee handoff byte-for-byte. I also independently confirmed that the originally delivered folder contains no symlink, cache, virtual environment, or runtime-output tree.

The principal defect is evidentiary rather than computational: the sealed handoff omits the final release ledger to which its README points, the archive build reports/transcripts, and the archive bytes themselves. Consequently the sealed folder **alone** does not demonstrate the claimed final double builds, extracted-gate executions, or remote push. Those claims became verified in this audit only through the separately delivered sibling archives and the available local Git object database. In addition, the archive's “extracted replay” is deliberately an **artifact-only cross-binding and logical validation with zero fresh mathematical replays**. Calling it an unqualified “theorem replay” overstates what that particular gate does.

## Severity-ranked findings

### RE-1 — Moderate: the sealed handoff cites but omits the final execution ledger and final archive-build evidence

`proof_package/README.md:64-78` reports the completed 54-command regeneration, 24/24 and 32/32 mutation rejection, PDF double builds, archive validity, and extracted gates. At lines 71-72 it directs the reader to `release/FINAL_RELEASE_ENGINEERING_REPORT.md`, but that path is absent from the delivered payload. The sealed `proof_package/reproducibility/RELEASE_WORK_LOG.md` is not a current substitute: its last checkpoint (`:170-203`) is for commit `0ddf4a…`, an older 45-command/18-mutation state with older archive hashes. The compact and full archive bytes, their second builds, and final build result objects also live outside the handoff.

Thus the sealed folder establishes manifest/code/report consistency, but only **asserts** that the final archive builds and their historical extracted gates were executed. It also cannot prove that a named commit was pushed to a live remote. This is a package auditability defect, not evidence that the executions failed: the independent executions below reproduce all current release results.

**Repair:** include a sanitized, sealed final ledger and compact JSON build records containing the exact commit, output hash, second-build equality, structural-verification result, extracted-gate mode/sentinel/transcript hash, environment identity, and before/after clean-tree status. Either include the archives or state unambiguously that they are sibling artifacts. Replace the broken README path if the ledger is intentionally excluded. State that “pushed” is externally checkable provenance, not a property authenticated by the package checksum.

### RE-2 — Minor: “extracted theorem replay” is an artifact-only promotion/integrity gate, not a fresh theorem recomputation

The archive builder invokes

```text
verify_k3p_same_classification.py --artifact-only --no-write-report
```

at `release/build_release.py:594-609`, from both archive paths at `:627-637` and `:687-705`. The gate itself says that `--artifact-only` performs cross-binding and logical checks “without executing the expensive replays” (`proof_package/reproducibility/verify_k3p_same_classification.py:4-8`), sets `fresh = []` at `:1459`, and reports `artifact_only: true` at `:1468`. My extracted executions for both archives reported `fresh_replays: 0`.

This gate is useful and did pass identically for both extracted archives, but it does not independently recompute the theorem artifacts. A phrase such as **“extracted artifact-integrity and theorem-promotion gate”** or **“artifact-only classification replay”** would be exact. Reserve “fresh theorem replay” for the ordinary non-`--artifact-only` gate.

### RE-3 — Minor: the standard integrity PASS does not itself prove absence of runtime trees

The delivered package claims 600 sealed payload files and no symlink, cache, virtual environment, or runtime output. The claim is true for the originally delivered directory by independent filesystem scan. However, `referee_tools/verify_package_integrity.py:44-63` deliberately excludes real top-level `.venv/` and `review_runs/` directories from its observed payload. Therefore an integrity-script PASS alone cannot substantiate the stronger “no virtual environment or runtime output” statement after a reviewer has run the package.

**Repair:** retain the current runtime-tolerant mode for post-run checks, but add a `--pristine` mode (and a corresponding pre-run record) that rejects `.venv/`, `review_runs/`, bytecode, caches, and all unsealed paths.

## Claim-by-claim evidence boundary

| Claim | What the sealed folder itself establishes | What it only asserts or cannot authenticate | Independent result in this audit |
|---|---|---|---|
| **32 release-engineering mutations rejected** | A sealed PASS report lists 32 rejected, zero survived, and ten controls; its logical payload is internally canonical and its code-binding hashes match the sealed driver and release code. | A stored report is not proof that the driver was actually executed in the claimed historical clean checkout. The portable runner explicitly omits this Git-bound suite (`START_HERE.md:111-120`). | **Reproduced.** At detached exact commit `76a097f…`, a fresh run rejected 32/32 with zero survivors and ten passing controls. The generated JSON was byte-for-byte identical to the sealed report. |
| **Both archives rebuild byte-identically** | The inner manifest identifies a 573-member full archive and source commit `76a097f…`; the outer manifest records the canonical full-archive SHA-256. Deterministic builders and structural verifiers are sealed. | Neither archive nor a final two-build record is inside the handoff. Synthetic double-build controls in the mutation report do not prove that the two final release archives were each built twice. | **Reproduced.** Fresh exact-commit builds equal the delivered sibling archives byte-for-byte: compact `95e909f4…b955`, full `ab0c2b06…b9d8`. Each also equals its preserved second-build counterpart. |
| **Extracted theorem replay passed** | The sealed builder shows that archive construction is programmed to safe-extract and invoke the artifact-only gate, and the gate's contract is inspectable. | No final archive-gate transcript/build record is sealed. More importantly, this mode performs zero fresh producer/verifier replays. | **Reproduced with qualification.** Both delivered archives structurally verified, safely extracted, and passed the artifact-only gate with the same transcript SHA-256 `749d2b85d617eaa2138899636e13c0b7bcbfde0a1ccd200a8ecab174005957fc`; both reported `fresh_replays: 0`. |
| **600-payload seal; no symlinks/caches/venv/runtime output** | `PACKAGE_MANIFEST.json:3007-3009` declares 600 files, 158,848,430 bytes, and commit `76a097f…`; the manifest and `SHA256SUMS` bind all sealed payload bytes. The inner full archive has 573 members excluding its manifest (`proof_package/ARCHIVE_MANIFEST.json:8-9`). | The runtime-tolerant integrity script excludes `.venv/` and `review_runs/`, so its PASS cannot by itself establish their absence. The hash list also cannot authenticate itself or provenance external to the folder. | **Verified.** The integrity tool passed on the untouched original. Independent enumeration found 602 regular files (600 payload + manifest + checksum list), 58 directories, and zero symlinks/nonregular objects, `.git`, `.venv`, `review_runs`, caches, `.pyc`, or `.pyo`. A fresh exact-commit handoff build reproduced the complete path set and every byte, including manifest SHA-256 `fa2131e8…c676e`. |
| **Commit `76a097f…` is the final pushed source identity** | Outer and inner manifests, generated readme, and source-build records consistently name `76a097f…`. | These are fields in self-contained files; the package has no signature, Git object, or live-remote receipt. It cannot prove “pushed.” Different older hashes in historical provenance files have distinct roles but make the identity story harder to follow. | **Locally corroborated, not live-remote authenticated.** The local object is a commit dated 2026-08-27T03:25:39-07:00, parent `9cea20a…`, subject “Record final referee repair closure”; it is an ancestor of local `main` and the locally cached `origin/main`. All 588 direct commit-derived handoff members matched the `76a097f…` blobs. No network fetch or remote query was made. |

## Executed evidence

The following were executed. They are deliberately limited to release engineering, hashing, archive construction/extraction, and the artifact-only gate.

1. **Untouched delivered-package integrity and independent filesystem scan**

   ```text
   PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 referee_tools/verify_package_integrity.py
   find/lstat/hash enumeration over the original delivered directory
   ```

   Result: integrity sentinel PASS; 573 core members / 158,206,960 core bytes; 600 payload files / 158,848,430 payload bytes; exact package/proof commit `76a097f…`. Independent scan: 602 regular files, 58 directories, no symlink/nonregular file or forbidden runtime/cache path.

2. **Fresh replay of all release-engineering mutations**

   In a clean sparse shared clone at `/tmp/k3p-release-audit.wccfQn/repo`, detached at exactly `76a097f…`:

   ```text
   python3 reproducibility/test_release_engineering_mutations.py \
     --output /tmp/k3p-release-audit.wccfQn/replayed.json
   ```

   Result: PASS, 32/32 rejected, zero survived, ten controls. The replayed report is byte-identical to `proof_package/reproducibility/RELEASE_ENGINEERING_MUTATION_REPORT.json`; logical payload SHA-256 `bf5d121953f1859cd6174801bf3b73ce3cfd877618b1576b80319900b9ce2264`; report SHA-256 `de21482645a437066a405839eb9df2953327eeb1a08a62daadfdab05ab60363f`. The checkout remained clean. I also recomputed every code-binding hash recorded by the report; all matched.

3. **Sibling archive structure and sidecars**

   `release/archive_tools.py` verified both delivered sibling artifacts. Results:

   - compact: 361 total members (360 excluding its manifest), SHA-256 `95e909f433b2a7cb1975f34324dc84cbe94e1ac0e76d43352cfccd69db18b955`, source `76a097f…`;
   - full: 574 total members (573 excluding its manifest), SHA-256 `ab0c2b068a6a0e7c80767000c29b1375591ac14a77b8fcb359818a73e167b9d8`, source `76a097f…`.

   Both `.sha256` sidecars matched. The full hash equals `PACKAGE_MANIFEST.json:2`.

4. **Safe extraction and artifact-only classification gate**

   After safe extraction of each delivered archive:

   ```text
   python3 reproducibility/verify_k3p_same_classification.py \
     --artifact-only --no-write-report
   ```

   Both exited zero with `K3P_SAME_CLASSIFICATION_GATE_PASS`; both produced transcript SHA-256 `749d2b85d617eaa2138899636e13c0b7bcbfde0a1ccd200a8ecab174005957fc`, reported 59 bindings, `fresh_replays: 0`, and identical logical payload `646b8004…`.

5. **Independent exact-commit archive builds**

   In the clean detached checkout:

   ```text
   python3 release/build_release.py compact \
     --output release/work/audit_rebuild/k3p_level2_compact_verifier.zip
   python3 release/build_release.py full \
     --output release/work/audit_rebuild/k3p_level2_reproducibility.tar.gz
   ```

   Both builders passed their structural and extracted artifact-only gates. The compact rebuild was 13,081,162 bytes with SHA-256 `95e909f4…b955`; the full rebuild was 89,740,617 bytes with SHA-256 `ab0c2b06…b9d8`. Each was byte-for-byte equal to the corresponding delivered sibling archive and to the preserved second build (`release/work/final_compact_second.zip` and `release/work/final_full_second.tar.gz`).

6. **Independent handoff-package rebuild**

   `referee_handoff/build_referee_package.py` was run from the same exact-commit checkout against the verified full archive, writing only to temporary output. It emitted its PASS sentinel and reproduced all 602 delivered files, paths and bytes. The rebuilt `PACKAGE_MANIFEST.json` SHA-256 is `fa2131e8a64f0caa40b95f67dbc2d635b12f45f33de50e5665a5a722fd5c676e`, exactly matching the delivered manifest.

7. **Commit/blob provenance checks**

   Read-only Git checks (`cat-file`, `show`, `merge-base --is-ancestor`, and streamed `git archive`) established the local commit metadata above and exact equality for 588 directly commit-derived handoff members. The remaining twelve handoff payload members are generated archive/handoff material or duplicate PDF placements and were covered by the exact package rebuild.

## Inspected, but not treated as executed evidence

- The sealed mutation JSON and all hashes to which it binds.
- `release/build_release.py`, `release/archive_tools.py`, `reproducibility/release_common.py`, the package builder, the package integrity verifier, and the artifact-only integrated gate.
- The omitted repository copy of `release/FINAL_RELEASE_ENGINEERING_REPORT.md` and `RESEARCH_LOG.md`. They narrate the final runs, but because they were not sealed into the handoff they are corroborating author records, not self-authenticating execution evidence.
- Historical provenance/log entries naming earlier proof or packaging commits. They are not treated as evidence for the current final build unless their role is explicitly historical.

## Explicitly not run or verified

- No mathematical producer was regenerated, including the 405,216 four-port enumeration and 574,535-row probe production/replay.
- No ordinary integrated classification gate with its fresh child replays was run.
- No complete 54-command or portable 53-command mathematical suite was run.
- No hour-scale probe, TeX/PDF rebuild, page rendering, or source-reproduction build was run in this sub-audit.
- No network fetch, Git-host API query, signature verification, or other live-remote check was performed; therefore “pushed to `main`” is locally corroborated only.

## Final assessment and confidence

The release implementation is unusually strong under adversarial replay: mutation behavior, canonical archives, extracted artifact validation, the handoff builder, and the package seal all reproduced exactly. **Confidence: high (0.98)** that the current delivered archives and handoff are deterministic products of the locally available exact commit and that the 32 release mutations reject as reported. **Confidence: high (0.99)** that the untouched delivered folder satisfies the 600-payload/no-symlink/no-runtime-state claim. **Confidence: limited (0.75)** on the word “pushed,” because this audit used the local object database and cached `origin/main`, not a live remote or cryptographic publication receipt.

The exact repair priority is documentation/provenance: seal the final ledger and build records, qualify the archive gate as artifact-only, and provide a pristine-integrity mode. No theorem statement depends on these corrections.
