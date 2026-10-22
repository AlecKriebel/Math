# PR280 record URL repair

Completed local repair of P280-OPS-04 at 2026-10-21T14:37:03.262917+00:00. Publication readiness remains **false**. A NEW COMPLETE history-free whole-package reviewer05 and root decision are required. This report makes no scientific-clearance or actual-publication claim.

## Defect and preserved failure

The former record regex omitted singular trailing slash, default port, dot segment and export routes. With any of the four root-confirmed URL forms in any of the four sheet cells, the frozen actual collector found zero matching rows; the frozen gate accepted; the synthetic append added a row; and readback incorrectly declared uniqueness. A contradictory exact root non-target row digest did not stop this. `OLD_COUNTEREXAMPLES.json` and its optimized counterpart preserve all32 failing full-pipeline combinations per mode, with zero actual providers. These were reproduced before canonical edits from the exact frozen seven-helper binding.

The original122 artifacts plus manifest/checksum are reconstructible byte for byte in `pre_record_url_binding/` from `INPUT_PRESERVATION.json` (130 initial files including root finding, suspended clearance, historical true clearance and review04 report/verdict/manifest). `SUPPLEMENTAL_PRESERVATION.json` adds43 files to preserve the remaining complete44 review04 artifacts and checksum. Historical manifests and reviews were not rewritten. Review04's scoped pass predates the root finding and does not authorize this repaired binding.

## Mechanism and exact scope

Four helpers changed; `CURRENT_REPAIR.diff` is the complete diff against the frozen source. `ops_binding.py` now parses bounded URL candidates with the standard URL parser and embeds the shared conservative recognizer within the existing seven-helper contract. `record_url_parser.py` is a development code artifact, not an eighth operational helper.

The recognizer distinguishes exact ASCII official authorities from nearby alien hosts. It handles host ASCII case, bounded default ports, protocol-relative and bare official references, bounded dot segments, repeated/trailing slashes, unreserved percent octets, singular/plural/API record prefixes and subsequent subresources. It takes the whole ASCII numeric route segment as a record lead. Leading zeros in record URLs are conservative aliases; leading zeros and distinct extensions in DOI suffixes remain distinct. Query and fragment do not hide the record path. Nested combinations are exercised.

These are **conservative identity leads**, not assertions that every variant actually resolves or that different URLs are globally equivalent. Root/sibling evidence authenticates particular public routes on a known public record; this agent read the evidence JSON and test source, not the cached remote response bodies, and made no new HTTP requests. Root's296-case metamorphic benchmark is explicitly a finite lexical obligation set, not296 authenticated HTTP equivalences.

Recognized official URLs with unsupported or malformed ports/authority, userinfo, multiple terminal hostname dots, unsupported transport, ambiguous/reserved/nested path encodings, unknown route, absent or malformed ID, root escape or excessive numeric length require explicit identity review. A malformed single-slash official scheme and unreserved-encoded official authority also require review. Unknown recognized shortDOI/resolver aliases remain fail closed, including before a target ID exists. No arbitrary Unicode folding or digit coercion is introduced. Unknown/unrecognized external redirects and arbitrary disguised text remain outside this finite lexical recognizer; nothing here claims universal alias discovery. Official unknown routing can conservatively block an unrelated row until root reviews it.

`prepublication_check.gather` scans **all four cells of every full-sheet row before account search/allocation or a model-term shortcut**. After full account enumeration it compares the precomputed leads to exact target/concept/version-parent IDs. The gate independently scans each lead row before root digest filtering. `record_publication_ledger.matches` scans every cell before its model-pattern shortcut, and existing independent preappend and readback target checks use the same recognizer. A recognized ambiguity cannot be hidden by an earlier matching cell, an exact desired row, or a contradictory non-target digest. Exact literal desired-row idempotence is preserved; an alias-only row is a review conflict, not silently canonicalized into an idempotent result.

The exact path/hash/integer-ID/full account projection requirements for unrelated local state are unchanged; there is no broad new exemption. Directory inventory preservation, original parent/QUEUE row binding, source17 plus selected5 overlay and non-force protections remain unchanged. `repository_integration.py`, `publication_lifecycle.py` and `verify_published_files.py` are byte-identical to the frozen binding.

## Offline validation

Both normal and optimized Python pass **1,704 current controls per mode**:

| Suite | Controls per mode |
| --- | ---: |
| New actual collector/gate/independent append/readback controls | 994 |
| Complete prior regression suite | 404 |
| Root finite lexical benchmark (296 positive obligations and7 nearby negatives) | 303 |
| Already-pushed-head resume verification | 3 |

The994 controls comprise176 complete alias pipelines,176 independent append checks with upstream approval bypassed synthetically,280 ambiguous-route independent append checks,280 collector/gate checks before allocation,57 readback-introduced alias/ambiguity checks,15 nearby distinct identities,7 recognized rejection controls, literal idempotence, genuine absence with one synthetic append, and a later-cell short-circuit check. Every alias/cell check is exercised with and without a contradictory exact root digest exemption. Full pipelines retain actual account-search/gather/reconcile/append/readback bodies; only provider interfaces and specified clearance preconditions are synthetic. Provider/socket/subprocess mutation traps record zero actual attempts.

The404 replay is120+53+73+158. Fixture adapters redirect output/scratch locations and load the current canonical recognizer rather than the old development prototype; prior truthful directory fixtures remain unchanged. No production guard or expected outcome was weakened. Frozen previous DOI/directory failure reproductions inside the old suites remain historical counterexamples. Root benchmark outcomes are295 target leads,1 explicit ambiguity rejection, zero silent misses, and all7 nearby negatives distinct. These finite overlapping checks are evidence, not exhaustive correctness proof.

`resume_path_controls.py` invokes actual `verify-test-merge` at the parent-reported already-pushed head `8aebb819bfac9c12340d2f1469408943549ab530` with synthetic GET-only responses and actual leaf/directory/QUEUE/source guards. It accepts the correct resume, rejects a wrong expected head and rejects a stale merge parent. An initial test-fixture omission lacked the source snapshot after relocating the receipt root; `HARNESS_NOTES.json` preserves that failure and its correction by copying the exact17-file approved snapshot. The actual production snapshot guard was retained.

## Preservation and operational handoff

`PRESERVATION_FINAL.json` verifies all initial130 frozen files, reconstruction of old122, complete44 review04 preservation, all unselected initial inputs, original17, five scientific payloads plus RELEASE, root lead, suspended clearance and prior true clearance history. The complete314-file `.zenodo-state` inventory remains byte-identical, aggregate SHA256 `1d241f0c6e2450ec0df942bf36bfe438f937d5ad530414028b3b47fcf827010b`. No state file was deleted. No Git/index/ref, GitHub/PR, Zenodo, GWS or actual lifecycle operation was performed by this repair agent.

The parent already pushed the branch once. After fresh whole-package review and any newly bound root clearance, resume with `repository_integration.py verify-test-merge --expected-pr-head 8aebb819bfac9c12340d2f1469408943549ab530`; do not rerun `commit` or create a second integration commit. Recheck fresh provider/ledger/account/public-byte gates at every later lifecycle transition using the reviewed workflow. Do not blindly retry a mutation after an uncertain outcome. This is a descriptive future handoff, not execution or permission.

Reproduce from this folder with normal Python and `-O`: `reproduce_old.py`, `current_controls.py`, `replay_404.py`, `resume_path_controls.py`; run the root-owned `private/record_url_metamorphic_controls.py` against this audit's canonical `ops_binding.py` and retain its JSON outside historical sealed folders. Use `PYTHONDONTWRITEBYTECODE=1`. `seal_current.py --verify` checks the final inventory and immutable inputs without provider access. The new manifest binds every authored repair artifact and all seven canonical helpers; previous seals remain historical inputs.

## Current seven-helper binding

| Helper | Bytes | SHA256 |
| --- | ---: | --- |
| ops_binding.py | 19889 | `99998518adb4c6ec8bfcf948284d661fa75d1c0a9f6896d06ad9881a6df431a1` |
| prepublication_check.py | 8077 | `8910f36f5a15c977fb9854eb6a8d9e083031ef96a4f8f28800acf468e827f4df` |
| publication_live_gates.py | 8911 | `6cff8fc49839afee22020e25e2342144e02d8dc489c898b1d483ff4f75707122` |
| repository_integration.py | 12873 | `c6c45427d051dc4e133894652da0bf667d41fb0c903659519d78d5b935d41e7b` |
| publication_lifecycle.py | 3195 | `174181d3b04281f999336d4aad52cbab21b1f5cdec496b70a0903b17ea317344` |
| record_publication_ledger.py | 8589 | `588d9f75233a8329360eefe1611252c687ff690e883f79ce90a70b8a1a02b49f` |
| verify_published_files.py | 5000 | `17bc2d7b2ac2c98cffb9797daeffdf7e1eb4ead31472d4fccb23b2dcc5d5431b` |

Local repair preparation is100% complete. Publication is pending reviewer05/root decision. Remaining limitations are finite lexical coverage and conservative false blocks on unreviewed recognized routes; no live record has been allocated for PR280 and no live publication/ledger outcome is asserted here.
