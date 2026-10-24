# Main two-input equality hardening audit

## 2026-10-24 — start (completion estimate: 20%)

User requested a fresh assessment of what would make the main two-input-per-party equality stronger. Inspect actual models and unconditional proof, commission independent mathematical and verifier reviews, and implement bounded validation improvements. Preserve the frozen September source/package/certificates and unrelated work. No external outreach or immutable release.

The actual repository-root workflow currently runs exact numerical artifacts and PDFs only. The nested bell_lean/.github/workflows/lean.yml is a standalone-project template, not an active monorepo workflow. Add an active root Lean job using the pinned existing verifier, full contracts and public dependency audit; retain receipts even on failure. Whether Lean --trust=0 really rechecks imported terms is under source inspection, not assumed from help text.

## 2026-10-24 — fresh CI exposed bootstrap gap (completion estimate: 60%)

Independent semantic review and an expanded actual-Born/source-projector contract passed. The initial protected-input comparison confirmed all 104 September inputs unchanged. First active Linux CI run 40104788823 then failed closed before proof compilation: online bootstrap attempted to interpret Cache/Main.lean before compiling its imports. September successful reproductions used a prepared dependency cache and remain valid, but they did not validate this online bootstrap path. Repair: build Cache.Main before interpretation and reject build errors; three new regression controls pass with all 53 runner tests. Only verifier scripts change, not mathematical declarations. The old initial source_identity.json predates these two verifier-script edits.

The imported-proof trust investigation confirmed --trust=0 does not replay all imported proof bodies in Lean 4.19. An explicit empty-environment dependency-closure replay is being tested; malformed-proof, retyped-axiom and changed-core controls reject correctly. Resource/stack failures in the large replay are preserved as failures, not mathematical counterexamples or successful verification. Frozen September artifacts remain unchanged.

A normal merge/push was blocked by unrelated dirty/untracked files overlapping newer remote work. Checked git merge-tree plus commit-tree integrated only this task’s paths into remote main by ordinary fast-forward push, without editing unrelated working files or the shared index.

## 2026-10-24T15:17:54.213334+00:00 — independent dependency replay passed (completion estimate: 90%)

Run 20261024T151139Z passed the complete empty-environment replay in 79 seconds: 33,644 declarations in 1,271 modules, all three required equality/simulation endpoints, four real kernel controls, unchanged source/checker/compiled-input hashes. Independent mathematical and verifier agents inspected the mechanism and final execution evidence; the root checked command log hashes and reran all nine mocked wrapper scenarios. These tests strengthen confidence in proof-object validity using the same pinned kernel. They do not claim an independent kernel implementation or a source rebuild of Mathlib. All Lean sources match the September certified snapshot; only the two intentional bootstrap verifier scripts differ.

The active CI now also includes the independent expanded Born contract, replay failure-control tests and full dependency replay after the fresh Lean build, with receipts uploaded even on failure. Fresh Linux CI for the bootstrap repair is still running; no successful Linux run is claimed yet. No new release or publication artifact is created.

## 2026-10-24T15:30:50.400656+00:00 — fresh Linux source build passed (completion estimate: 95%)

GitHub run 40105321824 completed successfully. Retained its actual run-specific receipt, commands and source/axiom/statement audits; all 104 protected hashes match the current repository and all 826 public audits use only allowed standard axioms. The exact/PDF job and independent expanded physical endpoint passed. This verifies the corrected online bootstrap on a clean Ubuntu runner using pinned downloaded dependency artifacts. The subsequent final CI run, which additionally executes the empty-environment replay, is still in progress. The quantitative branch bound was already formalized internally; only a specialized public physical-strategy corollary would be an optional API extension.

## 2026-10-24T15:42:49.097581+00:00 — complete Linux build and dependency replay passed (completion estimate: 100%)

Final combined CI 40106363370 at code snapshot 8aae12015e4fb470ce5a0970f5b792dc3ca7ad8f passed both jobs. Source run 20261024T151943Z-8d837c61 rebuilt all project proofs and passed all contracts and 826 axiom audits; its matching replay rechecked 33,644 declarations from 1,271 modules, with actual adversarial controls and unchanged protected inputs. Root verified all retained command log hashes, source/checker hashes and pre/post inventories; final independent CI review is recorded separately. No missing mathematical premise was found. The remaining full dependency source rebuild and distinct-kernel/human reviews are optional additional assurance, not claimed as completed. Final evidence/documentation checkpoint makes no further proof, verifier, checker or workflow changes. All work stays on main; no immutable release or external outreach.
