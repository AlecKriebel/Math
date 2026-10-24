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
