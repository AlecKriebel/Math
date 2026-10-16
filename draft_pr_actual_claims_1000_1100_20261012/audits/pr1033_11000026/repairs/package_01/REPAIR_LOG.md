# PKG-01 repair log

## Claim, scope and success criteria

The assigned claim is that the sole P2 packaging finding in package_01 is repaired while every original, retained authored audit copy, private review artifact and historical pin remains unchanged. This is an integrity repair, not a fresh review or mathematical claim. Success requires the raw Farb extract absent from the current distribution, accurate inventories, deterministic safe archive bytes, unchanged paper/metadata/originals, valid current navigation and a pending NEW independent review 02.

## 2026-10-13T23:02:27.845309+00:00 — Baseline checkpoint; 10% of assigned repair

Pinned all 325 existing audit-folder files before mutation in BASELINE_FILE_PINS.json. Preserved byte-identical pre-repair current controls in before/. Did not copy any raw body into the repair folder. The reviewed old archive was 201814 bytes with SHA-256 0ec9d589631f5c645fb3130eb453cd1324b4c628cdd1e254446ce08a218ce9a7; its PACKAGE_MANIFEST was 10046 bytes with SHA-256 1604fa79a4b4e2c540b5276bf169adbb97018f4087863aed017c85a108f3fffb; its AUDIT_COPY_MANIFEST was 9862 bytes with SHA-256 7169196189abb3d93b648382176f74b57057ae26ff0b4d506c06b5faf8bc6369. Those prior pins remain unchanged stage records.

## 2026-10-13T23:03:22.055979+00:00 — Repair applied; 80% of assigned repair

Deleted only publication/evidence/metric_01/sources/farb_printed_24_25.txt, 6310 bytes, SHA-256 98acdd2674601eacd8247675cafbc8bb63bddf311a6ed51ccb48fa4f8e29e7f4. The corresponding reviews/metric_01/sources/farb_printed_24_25.txt remains private and byte-identical. The original ROOT_MATH_ACCEPTANCE authored_output_pins row and every historical manifest/report remain unchanged; their old path references are explicitly mapped to that private, previously inspected stage.

Added is_authored_review_record to prepare_package.py and included package_01 among potential authored families. The selector excludes raw/rawprivate/raw_private, extracted, render/renders/candidate_render, cache/.cache/__pycache__, .venv and tmp directories. It selects Markdown/JSON authored records and the retained .gitignore; text, HTML, PDF, image, archive and bytecode bodies are excluded. The one-shot prepare_package.main() was never executed. The selector was evaluated without bytecode via runpy.

Regenerated the current copy manifest by retaining its 39 valid prior rows unchanged and appending 15 byte-identical authored package_01 records, including the previous review's output pins. Excluded its candidate_render, extracted and rawprivate source trees. Added PACKAGE_01_REPAIR_STAGE_MAPPING.json with the old candidate identities, removed-body pin, historical-path meanings and appended-copy pins. Updated README, supplement, evidence index and current review state to state that PKG-01 is repaired and NEW review 02 is pending. Neither readiness nor final issue clearance is asserted.

Rebuilt PACKAGE_MANIFEST and ZIP with the existing unchanged build_package.py. The small stage-mapping key locator was corrected to the actual authored_output_pins key before the final rebuild. No other source or mathematical repair was needed. The rebuild reproduced zenodo-deposit.json byte-for-byte because metadata and deposit file names are unchanged.

## 2026-10-13T23:04:35.041461+00:00 — Verification checkpoint; 100% of assigned repair

Ran verify_repair.py with bytecode disabled. All assertions passed: 314 protected baseline files are unchanged, including all 242 private review files; all eight original snapshot/distribution copies and their pins agree; all 39 retained and 15 appended authored copies agree with their frozen sources; all 22 root historical output pins still match private files. The published metadata, wrapper, TeX, PDF, layout receipt and existing build script remain unchanged.

The current inventory exactly lists 72 included files; the ZIP contains those files plus the self-excluded PACKAGE_MANIFEST, totaling 73 entries. Checks passed for ASCII names, uniqueness and casefold uniqueness, single safe relative prefix, absence of traversal/backslashes, regular 0644 entries, fixed 2026-10-13 midnight timestamps, exact entry-to-current-file byte identity and CRC. Independent in-memory reconstruction reproduced all archive bytes. No raw third-party PDF/text/HTML/image body, candidate extraction, render or cache is included; the authored research_note.pdf is the only PDF. The removed raw-body SHA-256 occurs in no current inventory body. All 45 candidate JSON files parse; 53 README/supplement/index relative links resolve; the local deposit wrapper metadata equals unchanged metadata.json and its declared files exist.

verify_repair.py checks that the preparation selector's current selected sets exactly equal each distributed family set and rejects 18 synthetic raw/extracted/render/cache/body probes. These probes check the actual exclusion boundary; they are not mathematical experiments or a new reviewer. The three-page count is preserved from the prior byte-pinned layout receipt; the unchanged PDF was not rerendered during this repair.

CANDIDATE_INTEGRITY.json is explicitly an integrity-only PASS, with immutable-publication readiness false. Its prior bytes are preserved at before/CANDIDATE_INTEGRITY.json. REPAIR_VERIFICATION.json preserves check details and every checked included/copy hash; REPAIRED_CANDIDATE_PINS.json pins the complete new publication tree plus preparation/build scripts. CHANGED_PATHS.json records every added/modified/deleted path and before/after hashes. OUTPUT_PINS.json pins repair outputs, including this log and the change inventory, with its own hash excluded.

No Git command, index mutation, PR update, service call, publishing action, release, deposit or outreach was performed. Work stayed inside the assigned audit folder; no agents were spawned or contacted. The required NEW independent adversarial whole-package reviewer will be assigned by the parent after this repair output is inspected. This repair's 100% completion estimate does not claim completion of the larger PR or publication workflow.

## Exact final key pins

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `publication/teichmuller_original_ball_paths_source_audits_v1.zip` | 252060 | `b709d01b1d9bed974c7c2ca04810921c41ccccb5846450600f12c0822d3a19f8` |
| `publication/PACKAGE_MANIFEST.json` | 12684 | `af52328ff5cf255f6d48e79f8b67b5553786bab726f6a98c03005a2e4aa5bd46` |
| `publication/evidence/AUDIT_COPY_MANIFEST.json` | 13479 | `f7f74a77685e0b4aa5f4a7d6fa205f32da7697d92cb6760a20f99f92c4acf605` |
| `publication/evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json` | 6937 | `db6b46bf37a30ca9eef91b620a28a4cb10af52f2560bb0ed9488d15419cf5352` |
| `publication/evidence/CURRENT_REVIEW_STATE.json` | 1175 | `3e90cd336ceb48f5a4d1882f65b110aec713277065904140941a1e0beceb6bab` |
| `publication/research_note.tex` | 8657 | `7f8c22e2bb55569fac85c330d45eb4510d8eaba8fbdff2d0b6fd92db30aa70e1` |
| `publication/research_note.pdf` | 81135 | `9d10b9dbfd7540cdd6e5dd298c079c6834bc3c404d3494dd4e485dd654ca1e56` |
| `publication/metadata.json` | 3506 | `a05444ab0ae43e818e5efca5f8c4d5e022035b712450b57e636486283f9fb002` |
| `publication/zenodo-deposit.json` | 3810 | `7116648a539544cd8dbfcbc4f2cc5deefbeb389ad0286845d0758e7fbdf6c9bf` |
| `prepare_package.py` | 16342 | `6628c9fa8e37610aa143d177ee3c752d605be8e7dddfeadd92f4645cf123ef50` |
| `build_package.py` | 2291 | `04b2de934db137d6a3258e015595246cff7fbce6de3e1c1aceb6c0982e00b860` |
| `CANDIDATE_INTEGRITY.json` | 1915 | `7a7357f3c5ac9955d11f169b1e6bdafeabdce2820cc134e1e832e805706ba8f0` |
| `repairs/package_01/REPAIRED_CANDIDATE_PINS.json` | 14986 | `abc61719d51a2af1d0ac561d36c90913ed6bea80f90e2db9732f54defa49072c` |
| `repairs/package_01/BASELINE_FILE_PINS.json` | 63044 | `89410d29da4cd4e367c72b9c04c751231d3c8c1c5b0672d95a8907d9f534986e` |
| `reviews/package_01/VERDICT.json` | 3134 | `858aa165badfbc6374c6f2e0388d88f19c9f76f4dad99cd830282a0f299a4037` |
| `reviews/package_01/FULL_REVIEW.md` | 17890 | `ef387d7beb3cc94f53b315b7bc605f18a08f0c1296687d29bbb973aecc48f993` |
| `reviews/package_01/OUTPUT_PINS.json` | 2401 | `d14df2a0eb249224fb335f33484833230f436b622020479f64492280bdfa2f26` |
