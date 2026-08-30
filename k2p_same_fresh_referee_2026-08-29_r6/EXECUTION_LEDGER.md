# K2P-SAME R6 fresh-referee execution ledger

Date: 2026-08-29 (America/Los_Angeles)

This ledger records the fresh R6 executions for
`K2P_Principal_D_Plus_Referee_Package_20260829.zip`.  The pristine package
root was
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/isolated/k2p_principal_d_plus_submission_referee`;
the ordinary disposable execution root was the sibling `execution/...` tree.
All nested Python runs were made with `PYTHONDONTWRITEBYTECODE=1`.  The two
outer-mutation relocations used an external virtual environment and external,
caller-owned reports.

## Environment

- macOS 26.5.2 (25F84), Darwin 25.5.0, arm64.
- Apple M1 Pro, 10 physical/logical cores, 17,179,869,184 bytes RAM.
- Python 3.14.6; NetworkX 3.5; SymPy 1.14.0.
- Tectonic 0.16.9; Poppler 26.08.0; Git 2.38.2.
- Empty-stream SHA-256, abbreviated `EMPTY` below:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- RSS is the maximum resident-set size reported by the command recorder.
  Per-layer and per-mutation RSS was not emitted by the submitted harness;
  the containing command's RSS is therefore the finest available measure.

The recorder metadata and all 82 corresponding stdout/stderr stream files
were independently rehashed; every recorded stream digest matched.

## Primary command ledger

Commands are shown exactly as recorded.  Relative commands ran from the
command record's `cwd`; the JSON record beside each stdout/stderr pair retains
that absolute working directory and start time.  `Output SHA-256` is the
recorder's ordered combined-output digest.

| Gate | Exact command | Exit | Wall s | Peak RSS bytes | Output SHA-256 |
|---|---|---:|---:|---:|---|
| `setup_venv` | `python3 -m venv /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv` | 0 | 1.936732 | 101,990,400 | `EMPTY` |
| `pip_upgrade` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -m pip install --upgrade pip` | 0 | 1.222152 | 95,911,936 | `5ee516c6c85d3b865b820e3bf6d4aebaab6d665ceba9b1d027f12f0ca14b202e` |
| `install_requirements` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | 0 | 6.404922 | 165,593,088 | `b8cb8888e74efb13d53a13b09a6cf6e18e4df64a873dd861491a02bfca6cf7e8` |
| `bundle_check` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.711803 | 185,516,032 | `e629be6db2848c9a83376f28c15bcb169af53c607167f27c761adbd37197699c` |
| `release_lock_check` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 15.908928 | 509,837,312 | `94e35b899bc88b934be42a11f470355f645b4fb1aaa35bd305574fbd5894350e` |
| `static_article_audit` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py --check` | 1 | 0.192495 | 45,383,680 | `3f793e0faa5a122f9b747dbaf95fe0bda96fc93ab0f22d47606377791e907207` |
| `setup_local_venv` | `python3 -m venv .venv` | 0 | 1.935755 | 97,435,648 | `EMPTY` |
| `install_local_requirements` | `.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | 0 | 6.255672 | 176,439,296 | `9045cb7d974405e9e5a5c9a264c198ba36461cc7cb79d884f3987eb647680714` |
| `static_article_audit_local` | `.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py --check` | 0 | 0.196195 | 44,220,416 | `df9582acafb22ad14c3283f3c8558258c91fd60cd9cc7ae29c68808574699cc9` |
| `pdf_build_visual_check` | `.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 42.294559 | 254,558,208 | `37d452846e17e734c72c499f57503a7363d02df145fcaf02ae49928a9d39975a` |
| `theorem_crosswalk_check` | `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.323174 | 176,963,584 | `26cc1c27c8d650495eb2d4bb328c7c1980653a5771c5f8faf6477b1855480c35` |
| `revised_bundle_builder_check` | `.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 121.005998 | 269,008,896 | `415373e5b9a0caca9351c8bcb0b9aeb9a2dad6d1993a2eab118fae01e08f3adb` |
| `revised_bundle_independent_check` | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 123.573363 | 270,548,992 | `415373e5b9a0caca9351c8bcb0b9aeb9a2dad6d1993a2eab118fae01e08f3adb` |
| `quick_replay` | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/evidence/quick_replay.json` | 0 | 420.921297 | 1,390,886,912 | `3ab84ab720afb2a12c8d578f89bbb909afb0352ad96d9de3fd3ded7deca20928` |
| `compressed_release_check` | `.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check` | 0 | 0.081397 | 35,700,736 | `1cc0a4e6da6e77164f0d87d049346fa06757aa599825020780ddfa8a39741c73` |
| `old_new_equivalence_check` | `.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check` | 0 | 123.963530 | 291,864,576 | `1380c65e64415f70fc856616bcbb958f9f436bea0856dda05f3c8a9fb6a94286` |
| `compression_mutations_check` | `.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check` | 0 | 0.416557 | 41,107,456 | `809c82f5fa2f601894ee5056daa7c01a3e3f51bfac3197eebc1c285e87f5a72a` |
| `telemetry_test` | `.venv/bin/python -B proof_compression_submission/test_clean_full_replay_telemetry.py` | 0 | 6.643744 | 27,951,104 | `6ed7a48d48f62034e3fc7bd088205366ee3c85b5a42041c26b3f733e65e2724a` |
| `probe_word_theorem_check` | `.venv/bin/python -B proof_compression_submission/probe/verify_probe_word_theorem.py --check` | 0 | 22.208678 | 79,118,336 | `46f31f70b5cfa50a15f2d3e7f883671b52083e4ac23e005234a6cddb25443ba3` |
| `crosswalk_bundle_mutations` | `.venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 3,768.434193 | 401,588,224 | `7be72305124618ad1739b165e5c62c23d818111a3d5e01a0d60cebb8caca2826` |
| `outer_mutations_alpha` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/evidence/outer_mutations_alpha.json` | 0 | 4,324.255900 | 2,547,793,920 | `c0cf6e69cec32f038aa7615aa9bc08a78b5e7990595c96c7159f1c53cb30586d` |
| `outer_mutations_beta` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/evidence/outer_mutations_beta.json` | 1 | 4,310.795162 | 2,548,252,672 | `aa3e6549d2c00810ed542c2ab82629ae41640fe3011983c3bfc5dec3abde5862` |
| `outer_mutations_beta_control` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/evidence/outer_mutations_beta.json` | 0 | 4,213.675648 | 2,624,995,328 | `c0cf6e69cec32f038aa7615aa9bc08a78b5e7990595c96c7159f1c53cb30586d` |
| `r6_exact_math_checks` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/independent_checks/math/r6_exact_math_checks.py --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/independent_checks/math/R6_EXACT_MATH_CHECKS.json` | 0 | 0.760939 | 70,090,752 | `d78957da49f82b79d739420ae6f1bba3f21162204885e12bd84898bdcb9acb08` |
| `full_replay` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/runtime/.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/evidence/full_replay.json` | 0 | 6,309.975749 | 2,548,711,424 | `f1cbb32309a920fa33559782f38d630dbf58d7dd6ded6c4814f7861b21d8e734` |

The first static-audit exit 1 is **noncontrolling**: it was run against the
pristine tree with only the external environment and correctly failed with
`CROSSWALK_PATH_MISSING:.venv/bin/python`.  The documented setup requires a
project-local `.venv`; the same audit then passed in the disposable tree.

The first beta outer-mutation exit 1 is also **noncontrolling**.  It reached
the direct-terminal family and then raised `OSError: [Errno 28] No space left
on device` while copying `rank_certs_4.pkl` into the host temporary directory.
It was not a semantic survivor or verifier result.  Its stdout SHA-256 was
`bd948f0613112bb332982e09d55c905d42cc14aaa5aa492835eaf3331dace575`,
stderr SHA-256
`83772342cb1e9906d3bab3c5c12c1b64cb09257e80c3df21ec135cc51dcb3b6d`.
The unchanged beta tree was rerun serially once; the control passed and its
report is byte-identical to alpha.

## Independent provenance and document commands

These command records use a second recorder.  `Stream hashes` gives stdout
then stderr; `Record payload` is the command-record logical payload.  To keep
the table readable, `.../.venv/bin/python` abbreviates the absolute disposable
interpreter path printed in the command records; every other argument is
literal.  An exit 1 marked “expected finding” is controlling evidence for
R6-F1, not a crash.

| Record / exact command | Exit | Wall s | Peak RSS bytes | Stream hashes | Record payload |
|---|---:|---:|---:|---|---|
| `referee_bundle_check_only`: `.../.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.674669 | 231,473,152 | `e629be6db2848c9a83376f28c15bcb169af53c607167f27c761adbd37197699c` / `EMPTY` | `a2f9a7cd563648eb1a8355a28827b5b5c37950bce918cbbd3726e7c0adb3919d` |
| `release_lock_check`: `.../.venv/bin/python -B build_release_lock.py --check --require-ready` | 0 | 16.108591 | 491,061,248 | `94e35b899bc88b934be42a11f470355f645b4fb1aaa35bd305574fbd5894350e` / `EMPTY` | `d4699c93a66a36ac68ce75bc45b74ed23a93661caa8abb2616f7ff7864c6ec5b` |
| `static_article_audit_isolated_without_venv_expected_failure`: `.../.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py` | 1 | 0.208714 | 44,646,400 | `3f793e0faa5a122f9b747dbaf95fe0bda96fc93ab0f22d47606377791e907207` / `EMPTY` | `8a6e85aeee95d27d29ab5d1ec41f5b6529eb791f630bb01f8bcf6f92cb915bb8` |
| `static_article_audit_execution`: `.../.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py` | 0 | 0.242604 | 45,219,840 | `df9582acafb22ad14c3283f3c8558258c91fd60cd9cc7ae29c68808574699cc9` / `EMPTY` | `2fed9ce0a46a1f40da440a480846cbeb931e07318db870d99f20f968d8488d64` |
| `pdf_double_rebuild_and_omissions`: `.../.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 13.315202 | 256,344,064 | `37d452846e17e734c72c499f57503a7363d02df145fcaf02ae49928a9d39975a` / `EMPTY` | `11d309bda2784905613a5bf5df40d952496f87adf1ce3a3ae919528b9c1b11c4` |
| `bibliography_omission`: `python3 -B independent_checks/provenance/bibliography_omission_test.py --project isolated/k2p_principal_d_plus_submission_referee --python execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --scratch tmp --output evidence/documents/BIBLIOGRAPHY_OMISSION_TEST.json` | 0 | 120.749663 | 382,763,008 | `5036a493e1aa1e05bb0632dc465dda8e67a1450cb400ec4c567d0ee8067bc021` / `EMPTY` | `dbe3d8c6f767ebff8d2e4b2c68e7d44831d180dc6959d92c4b13ed2e8b384d57` |
| `pdf_source_consistency_audit`: `python3 -B independent_checks/provenance/build_pdf_evidence.py --project isolated/k2p_principal_d_plus_submission_referee --review-root . --output evidence/documents/PDF_SOURCE_CONSISTENCY_AUDIT.json` | 0 | 0.195544 | 24,952,832 | `b9f80fd194b94f3f57117874012edc1dfa3b32a5e6734a4ca0f359e9821dc831` / `EMPTY` | `3cd37e24d8b93203f52b6d0209b70224bb16852cb77c4c30ef3bf5e0c2ec2d60` |
| `theorem_crosswalk_check`: `.../.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.299272 | 178,733,056 | `26cc1c27c8d650495eb2d4bb328c7c1980653a5771c5f8faf6477b1855480c35` / `EMPTY` | `641ded5ef0224f421e86fcac3afb81ef4564665e3aa48ff16469bbc5a3ef0379` |
| `revised_bundle_producer_check`: `.../.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 122.143495 | 277,233,664 | `415373e5b9a0caca9351c8bcb0b9aeb9a2dad6d1993a2eab118fae01e08f3adb` / `EMPTY` | `9c21938a5de0c090d55924213a19381b225cd22a7f6d5213575023319f1ebfd0` |
| `revised_bundle_independent_check`: `.../.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json` | 0 | 127.083402 | 279,773,184 | `415373e5b9a0caca9351c8bcb0b9aeb9a2dad6d1993a2eab118fae01e08f3adb` / `EMPTY` | `24f78ece886dd0872f689587be7fb4f3bbcfcba943036772b86518fda8ca68ff` |
| `printed_authority_hash_mutations`: `python3 -B test_printed_authority_hash_gate.py` | 0 | 0.058697 | 28,098,560 | `f88d3b23d5be6348e13bc68ef9442cfb2809719a284db981198535c69b1b7246` / `EMPTY` | `d4030b400e679d9500f560c438bcbbff9ac45bf5c1d9db9ccc29e96838d179b9` |
| `semantic_repair_audit`: `python3 -B independent_checks/provenance/semantic_repair_audit.py --project isolated/k2p_principal_d_plus_submission_referee --output evidence/provenance/SEMANTIC_REPAIR_AUDIT.json` | 0 | 0.591940 | 218,431,488 | `c65563f0ce94c9fc6565fd448c6adcccdb5589e311f0ad26954b2c923f47688a` / `EMPTY` | `693da8e96f23dc8e45c0d55510c9de34a9b8a082d0ece0301493ee14571796bb` |
| `independent_provenance_audit`: `python3 -B independent_checks/provenance/independent_provenance_audit.py --project isolated/k2p_principal_d_plus_submission_referee --archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260829.zip --git-repo /Users/alec/Documents/Math/k2p_level2_identifiability_closure --output evidence/provenance/INDEPENDENT_PROVENANCE_AUDIT.json` | 0 | 2.188059 | 393,560,064 | `49de2115968b8251b7d9532be6e3fca3bafcf8ae624d334734f90699b92a412e` / `EMPTY` | `1898c4456ef1b1ce63b2f2494074fb5ddf7582b62fff6f9342366ddd21a8ec57` |
| `independent_archive_rebuild`: `python3 -B independent_checks/provenance/independent_archive_rebuild.py --project isolated/k2p_principal_d_plus_submission_referee --source-archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260829.zip --first tmp/archive_rebuild_1/K2P_Principal_D_Plus_Referee_Package_20260829.zip --second tmp/archive_rebuild_2/K2P_Principal_D_Plus_Referee_Package_20260829.zip --output evidence/provenance/INDEPENDENT_ARCHIVE_REBUILDS.json` | 0 | 41.879459 | 250,576,896 | `7088fc92c2c3ec19fa26aa06812b73a20d20b49e20451ed0477fe36e49ee96ae` / `EMPTY` | `b50f9bf8a6ded91fb0182c6be7cc1705c77b0358b52e2825050d2ec92c66136b` |
| `independent_biorxiv_source_rebuild`: `python3 -B independent_checks/provenance/independent_biorxiv_source_rebuild.py --source-root isolated/k2p_principal_d_plus_submission_referee/proof_compression_submission --archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_SAME_bioRxiv_Source_20260829.zip --first tmp/biorxiv_rebuild_1.zip --second tmp/biorxiv_rebuild_2.zip --output evidence/provenance/INDEPENDENT_BIORXIV_SOURCE_REBUILDS.json` | 0 | 0.075176 | 24,576,000 | `382e8adf23884276b597245e994edd1c91fd7b9c5d04085e551ae18ee8b6e2cb` / `EMPTY` | `af4c1edf6ddb6839294d7e6bebb9ea36fbfffd081653662ee202054a0b960eab` |
| `probe_narrative_binding_audit` (expected finding): `python3 -B independent_checks/provenance/probe_narrative_binding_audit.py --project isolated/k2p_principal_d_plus_submission_referee --output evidence/provenance/PROBE_NARRATIVE_BINDING_AUDIT.json` | 1 | 0.084670 | 34,635,776 | `c0eaac37c4077b0f5d1f1e58c720a60ba1dc37b750ba1d6cf643e22fda8fe62a` / `EMPTY` | `01e5ece21769759b51d832c97a2889486ccc6058adf6895c0166f74edf0ce330` |

Two additional review-owned computational programs were recorded in the
computational review note rather than the common command recorder:

- `python3 -B independent_checks/computation/r6_semantic_scan.py --project isolated/k2p_principal_d_plus_submission_referee --runtime-python /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --output independent_checks/computation/r6_semantic_scan_result.json`: exit 0, 98.596991 s internal time; peak RSS/output-stream hashes not recorded; result SHA-256 `3f9bd18cfa7d800a16e41280a4470a9bdf4c9cbee96c689bc06b344eca36f732`.
- `python3 -B independent_checks/computation/r6_bounded_fail_closed_attacks.py --project isolated/k2p_principal_d_plus_submission_referee --python /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --output independent_checks/computation/r6_bounded_fail_closed_attacks_result.json`: exit 0, approximately 6.3 s; peak RSS/output-stream hashes not recorded; result SHA-256 `e7c9a475a8da4f6b6f4462eda1356d20910d63be3e6b475217d83743e1542a8e`.

## Quick replay: 23/23 layers

The quick report is `evidence/quick_replay.json`, 7,856 bytes, SHA-256
`1cb8d359e2d12035d7c9c54b2495c523d67961d78c14098b277a55b90ed01c78`.
It records status PASS, promotion-ready, zero blockers, 420.387981 s internal
time, and release-lock payload
`3a0c89c4cedb7202161289eab7b3671c004ae638bcf90eba837e45e3e1890fc5`.
`Err` is `EMPTY` unless shown explicitly.

| # | Layer | Status / exit | Wall s | Stdout SHA-256 | Err |
|---:|---|---|---:|---|---|
| 1 | `promotion_manuscript_guard` | PASS / 0 | 0.327230 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `EMPTY` |
| 2 | `full_map_domain_reseal` | PASS / 0 | 0.118368 | `f54c4a337184e36575f82ac1af9a89fde7a2b60fe73db1d4d907c22561b313a4` | `EMPTY` |
| 3 | `corrected_universe_independent_replay` | PASS / 0 | 16.329436 | `a44b144b69e9b01b570bbbb3ccad2c650f1e243e0f3678a13d172565c96fa2f1` | `EMPTY` |
| 4 | `three_port_no_assert` | PASS / 0 | 0.392070 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `EMPTY` |
| 5 | `domain_rooting` | PASS / 0 | 0.066017 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `EMPTY` |
| 6 | `quartet_sign_logic` | PASS / 0 | 1.151748 | `b73a2b520963b97789f0a9123d8cb5c09b72e90885f20cb0c5f4eda4a92a5dd4` | `EMPTY` |
| 7 | `quartet_terminal_bindings` | PASS / 0 | 81.709103 | `9218991b427b64fc74247021fed9a232fa1d32e4878d53bca5f95c86518f2a8e` | `EMPTY` |
| 8 | `raw_displayed_quartet_direction` | PASS / 0 | 3.080568 | `9127ddc5dc420396827fa228265879838e9284bbe7461368cc77472bf0e734fe` | `EMPTY` |
| 9 | `canonicalizer_completeness_structural` | PASS / 0 | 0.234389 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `EMPTY` |
| 10 | `graph_derived_parameter_transports_structural` | PASS / 0 | 29.826856 | `fcc72354add0c6a5154978663980f89fee98ada714d420f866769ad3a12711d6` | `EMPTY` |
| 11 | `bridge_marginal_gluing` | PASS / 0 | 0.059955 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `EMPTY` |
| 12 | `analytic_adversarial_audit` | PASS / 0 | 0.429537 | `2a2e22c51ac89be87e3b026fcd8079faf5f7eadd422397da68a81d810b9d525f` | `EMPTY` |
| 13 | `global_component_scale_audit` | PASS / 0 | 0.218416 | `a8433fa855d987a6d7bda3036014479ffb8a63b4825363ee42f6e73bbf726418` | `EMPTY` |
| 14 | `raw4_corrected_overlay_independent` | PASS / 0 | 92.735497 | `72fb7ecc18cc32cb97018955b5e47ce640c83931742976e80c5802635e297e12` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| 15 | `theta2_full_map_independent` | PASS / 0 | 64.203082 | `d6936adfebc21718c84bf67a4b5ec1065ef2955cbabf29a2d892381d798c03d4` | `EMPTY` |
| 16 | `four_port_raw_structural_provenance` | PASS / 0 | 3.953972 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `EMPTY` |
| 17 | `four_port_direct36` | PASS / 0 | 17.326065 | `b792ab5f5eca3737c2f92f0cd251dc25685d100524141cac8ecbee6e25a8d800` | `EMPTY` |
| 18 | `theta2_structural_provenance` | PASS / 0 | 28.971239 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `EMPTY` |
| 19 | `cycle_three_port_authoritative_promotion` | PASS / 0 | 25.599331 | `254d8dae0e19636f20cb1718007725e6e484711a828633b22d31e4b3090e2781` | `EMPTY` |
| 20 | `corrected_probe_independent_streaming_replay` | PASS / 0 | 24.627137 | `e10c878db794c7c296c4dc08bd735f82dfbd0267564b4ccf8631b4081dd96439` | `EMPTY` |
| 21 | `corrected_probe_site_transport_partition` | PASS / 0 | 12.040171 | `fed2eea6ec9162c3fa4302a1603e164abf9e940c0635bb582accf179a84a38ed` | `EMPTY` |
| 22 | `weak_sharpness_primary` | PASS / 0 | 0.213494 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `EMPTY` |
| 23 | `weak_sharpness_independent` | PASS / 0 | 0.178693 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `EMPTY` |

## Full replay: 41/41 layers

The full report is `evidence/full_replay.json`, SHA-256
`23c78f94072a993cad954d9e72615bd01acaf8f5842722ffecd133d631556b74`.
It records status PASS, promotion-ready, zero blockers, 6,309.453324 s
internal time, and the same release-lock payload.  The containing command's
peak RSS was 2,548,711,424 bytes.

| # | Layer | Status / exit | Wall s | Stdout SHA-256 | Err |
|---:|---|---|---:|---|---|
| 1 | `promotion_manuscript_guard` | PASS / 0 | 0.309525 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `EMPTY` |
| 2 | `full_map_domain_reseal` | PASS / 0 | 0.116474 | `f54c4a337184e36575f82ac1af9a89fde7a2b60fe73db1d4d907c22561b313a4` | `EMPTY` |
| 3 | `corrected_universe_independent_replay` | PASS / 0 | 15.312237 | `a44b144b69e9b01b570bbbb3ccad2c650f1e243e0f3678a13d172565c96fa2f1` | `EMPTY` |
| 4 | `three_port_no_assert` | PASS / 0 | 0.337899 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `EMPTY` |
| 5 | `domain_rooting` | PASS / 0 | 0.061795 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `EMPTY` |
| 6 | `quartet_sign_logic` | PASS / 0 | 1.083666 | `b73a2b520963b97789f0a9123d8cb5c09b72e90885f20cb0c5f4eda4a92a5dd4` | `EMPTY` |
| 7 | `quartet_terminal_bindings` | PASS / 0 | 78.074757 | `9218991b427b64fc74247021fed9a232fa1d32e4878d53bca5f95c86518f2a8e` | `EMPTY` |
| 8 | `raw_displayed_quartet_direction` | PASS / 0 | 2.813877 | `9127ddc5dc420396827fa228265879838e9284bbe7461368cc77472bf0e734fe` | `EMPTY` |
| 9 | `canonicalizer_completeness_structural` | PASS / 0 | 0.235710 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `EMPTY` |
| 10 | `graph_derived_parameter_transports_structural` | PASS / 0 | 28.999950 | `fcc72354add0c6a5154978663980f89fee98ada714d420f866769ad3a12711d6` | `EMPTY` |
| 11 | `bridge_marginal_gluing` | PASS / 0 | 0.065036 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `EMPTY` |
| 12 | `analytic_adversarial_audit` | PASS / 0 | 0.435024 | `2a2e22c51ac89be87e3b026fcd8079faf5f7eadd422397da68a81d810b9d525f` | `EMPTY` |
| 13 | `global_component_scale_audit` | PASS / 0 | 0.216402 | `a8433fa855d987a6d7bda3036014479ffb8a63b4825363ee42f6e73bbf726418` | `EMPTY` |
| 14 | `raw4_corrected_overlay_independent` | PASS / 0 | 89.086723 | `c5e7d09364878232385d6c6f805801030ca6a00d2bc22892dc4017c00f51d8d0` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| 15 | `theta2_full_map_independent` | PASS / 0 | 63.455550 | `fcae5bb7a583631a96c15680bde1cb5834ad81d379259ca7a09efb4888f0f1f1` | `EMPTY` |
| 16 | `four_port_raw_structural_provenance` | PASS / 0 | 3.955387 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `EMPTY` |
| 17 | `four_port_direct36` | PASS / 0 | 16.704948 | `b792ab5f5eca3737c2f92f0cd251dc25685d100524141cac8ecbee6e25a8d800` | `EMPTY` |
| 18 | `theta2_structural_provenance` | PASS / 0 | 29.150473 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `EMPTY` |
| 19 | `cycle_three_port_authoritative_promotion` | PASS / 0 | 25.590880 | `254d8dae0e19636f20cb1718007725e6e484711a828633b22d31e4b3090e2781` | `EMPTY` |
| 20 | `corrected_probe_independent_streaming_replay` | PASS / 0 | 24.827037 | `e10c878db794c7c296c4dc08bd735f82dfbd0267564b4ccf8631b4081dd96439` | `EMPTY` |
| 21 | `corrected_probe_site_transport_partition` | PASS / 0 | 12.160549 | `fed2eea6ec9162c3fa4302a1603e164abf9e940c0635bb582accf179a84a38ed` | `EMPTY` |
| 22 | `weak_sharpness_primary` | PASS / 0 | 0.219988 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `EMPTY` |
| 23 | `weak_sharpness_independent` | PASS / 0 | 0.173091 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `EMPTY` |
| 24 | `canonicalizer_completeness_full` | PASS / 0 | 107.117779 | `dde7a6df548d407df5cedb2810549aac0711269718ba203c9ddbd45461675188` | `EMPTY` |
| 25 | `graph_derived_parameter_transports_full` | PASS / 0 | 307.831196 | `4e9007b2086809e76cb00c31a68e13a8c8998a9a1d968f82dfaf7621a1e75363` | `EMPTY` |
| 26 | `corrected_restoration_independent_full_replay` | PASS / 0 | 463.890221 | `3b9d4c8d7b6136906855b5c20c0aad88e3fa90826fe082f1848817109ce095e8` | `7bb69d81f6d45d866e3030dda574eb3b5056c637319c017fc12ee4b3c10fb1da` |
| 27 | `corrected_universe_cross_layer_mutations` | PASS / 0 | 316.194419 | `80bda05ae0652db668258d7383231e637233644b559098fdb786f4c5e0bcb3f0` | `EMPTY` |
| 28 | `raw4_full_map_Ti_truth` | PASS / 0 | 21.151375 | `f95c1e2d59974d8a3faf42ee63d3fe389de3c3baffef9b374b8939812ab50423` | `EMPTY` |
| 29 | `theta2_full_map_Ti_truth` | PASS / 0 | 89.004961 | `cec14bbbe0712b53c033610d754b101c6ccce0c98d4e42536121083d86fa5ebd` | `EMPTY` |
| 30 | `composite_domain_reseal_diff` | PASS / 0 | 77.251806 | `d214d2df286b6ca780476fe40372eb88eefde13b1ab0d78f82b0af629d4dd0ca` | `EMPTY` |
| 31 | `four_port_exact_rank_staged_atlas_omission_mutation` | PASS / expected nonzero child | 0.462563 | `EMPTY` | `46747fbb6a1a7a4b597168371f731e5c46731f007a4eefabe8e4543f351980b0` |
| 32 | `four_port_exact_rank_import_preflight` | PASS / 0 | 0.462949 | `79d039353c2a88425952fe6ffd8e67653c512de65e89b2ab6f22b46e5ee72212` | `EMPTY` |
| 33 | `four_port_exact_rank_full` | PASS / 0 | 120.922544 | `19ae94237493e6fec9e0fc952d8c36b236cee3c13a9b8acc2f8cda1a11e70e17` | `EMPTY` |
| 34 | `raw4_corrected_overlay_full_regeneration` | PASS / 0 | 61.985446 | `4c51979cd98bd4e8835b170780982e7541948c1a2cf8d96e63801dcf242ce1f3` | `de1f579aafe4aa7f4d84e6f47f6b6ca9aba263df850de2b6839abc89018dfb8c` |
| 35 | `four_port_raw_full_regeneration_provenance` | PASS / 0 | 312.575690 | `8eb91f720fe064d3007c5f2f4a65295b921c068285b1fad9db3d3710ae3f55c6` | `EMPTY` |
| 36 | `four_port_direct36_full` | PASS / 0 | 109.804688 | `a3758962638af6df263c9fa40dab3e26bf41881761c9f94ae129345609ec7f65` | `EMPTY` |
| 37 | `theta2_full_regeneration_provenance` | PASS / 0 | 490.317503 | `82c6917c4503a2cb7d3c42988100a58731dff13c8972a45b27ffbb5226bbd783` | `EMPTY` |
| 38 | `corrected_probe_full_primitive_regeneration` | PASS / 0 | 2,927.639456 | `1664163725018b35688415340a3f9c1e1d14964680ad7bd94cdb9a84142fe902` | `a4690a0abf2b599894e5a32de5a3053344d15b8da7dd45686a143d301801b92b` |
| 39 | `corrected_probe_full_independent_replay` | PASS / 0 | 24.666928 | `e10c878db794c7c296c4dc08bd735f82dfbd0267564b4ccf8631b4081dd96439` | `EMPTY` |
| 40 | `corrected_probe_full_site_transport_partition` | PASS / 0 | 12.253910 | `fed2eea6ec9162c3fa4302a1603e164abf9e940c0635bb582accf179a84a38ed` | `EMPTY` |
| 41 | `corrected_probe_independent_primitive_graph_full` | PASS / 0 | 456.051485 | `42a7fe23231c17994c3aa4c83a11e0289cee00039ba61fac255069c0f4791891` | `cbc56ffd93ed354a5cd9adfa22ebe130b83db6b8822b4fc1adc29c66e71e7602` |

## Crosswalk and revised-bundle mutations: 37/37 rejected

The controlling command passed in 3,768.434193 s.  Frozen report:
`proof_compression_submission/crosswalk/CROSSWALK_BUNDLE_MUTATION_REPORT.json`,
SHA-256
`a49415da9daa15079b6e0528027826196e6f5a314728fdbfb8b8314df7447b80`,
logical payload
`0217ccc3cfdcb9f3142257aadf1ea0725f532e2389085b1df211c99cc031dfeb`.
The report does not record per-case runtime/RSS, so those fields are
unavailable rather than inferred.

| # | Mutation | Observed intended rejection |
|---:|---|---|
| 1 | `overbroad_c02_topology_authority` | `C02 claim scope drift` |
| 2 | `erased_c02_exclusion_boundary` | `C02 narrowed artifact role drift: authoritative_artifacts:work/adversarial_proof_review/topology_direction_certificate.json` |
| 3 | `omitted_frozen_evidence_file` | missing `LICENSES.md` from frozen ledger |
| 4 | `omitted_quartet_terminal_binding` | missing quartet terminal-binding certificate |
| 5 | `omitted_canonicalizer_completeness_certificate` | missing canonicalizer certificate |
| 6 | `omitted_graph_parameter_transport_ledger` | missing parameter-transport ledger |
| 7 | `omitted_shared_strict_json_parser` | missing `strict_json.py` |
| 8 | `omitted_approved_license_terms` | missing `LICENSES.md` |
| 9 | `false_frozen_evidence_hash` | frozen evidence ledger mismatch |
| 10 | `omitted_submission_source` | missing article `main.tex` |
| 11 | `omitted_compression_table` | missing `compression_tables.tex` |
| 12 | `omitted_bibliography` | missing `references.bib` |
| 13 | `omitted_certificate_appendix` | missing `certificate_appendix.tex` |
| 14 | `unsafe_source_path` | unsafe `../outside` path |
| 15 | `stale_pending_human_status` | manifest status mismatch |
| 16 | `unapproved_corresponding_email` | submission metadata mismatch |
| 17 | `false_doi_claim` | submission metadata mismatch |
| 18 | `wrong_versioned_source_tag` | submission metadata mismatch |
| 19 | `false_external_release_claim` | submission metadata mismatch |
| 20 | `false_combined_content_root` | combined content-root mismatch |
| 21 | `false_crosswalk_binding` | submission-source ledger mismatch |
| 22 | `false_clean_full_runtime` | runtime-boundary mismatch |
| 23 | `false_clean_full_layer_count` | runtime-boundary mismatch |
| 24 | `false_telemetry_submission_source_binding` | builder/checker/crosswalk telemetry source-binding mismatch |
| 25 | `false_telemetry_release_lock_binding` | builder/checker/crosswalk telemetry lock-binding mismatch |
| 26 | `omitted_article_pdf` | missing article PDF |
| 27 | `omitted_static_article_audit` | missing static audit result |
| 28 | `omitted_neutral_referee_prompt` | missing referee prompt |
| 29 | `omitted_portable_content_ledger` | missing portable content ledger |
| 30 | `omitted_portable_bundle_checker` | missing portable checker |
| 31 | `omitted_portable_bundle_readme` | missing portable README |
| 32 | `false_supplement_pdf_hash` | submission-source ledger mismatch |
| 33 | `same_valued_duplicate_json_name_after_reseal` | producer and checker `STRICT_JSON_DUPLICATE_NAME` in `PDF_BUILD_REPORT.json` |
| 34 | `same_valued_duplicate_compressed_jsonl_after_reseal` | producer and checker duplicate `parent_anchor_id` |
| 35 | `conflicting_duplicate_compressed_jsonl_after_reseal` | producer and checker duplicate `parent_anchor_id` |
| 36 | `noncanonical_compressed_jsonl_after_reseal` | producer and checker `STRICT_JSON_NONCANONICAL_BYTES` |
| 37 | `conflicting_valued_duplicate_json_name_after_reseal` | producer and checker `STRICT_JSON_DUPLICATE_NAME` in `PDF_BUILD_REPORT.json` |

## Dual clean-relocation outer mutations: 25/25 twice

Alpha ran under
`.../relocations/alpha_parent/referee_alpha`; beta ran under
`.../relocations/distinct_beta_parent/referee_beta_relocated`.  Both used the
same external environment and external reports.  The two completed reports
are byte-identical: 9,146 bytes, SHA-256
`0bc92a5f1f8328b6ce51945233a5152f5a28e96a99f538568bf9d057f92a8a55`,
logical payload
`a12b19d10abde01fc1f51c17aad5d5e9b35550ec8f019f7ba3a11f4fca65b81a`.
Each records 25 required/observed mutations, zero survivors, no crash text,
and a passing output-contract preflight.  The stable report deliberately
omits temporary paths, elapsed times, and raw child output; per-case runtime
and RSS are therefore unavailable.

| # | Outer family | Semantic evidence | Alpha | Beta control |
|---:|---|---|---|---|
| 1 | `optimized_mode` | exact `FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN`, exit 1, no success artifact | REJECTED | REJECTED |
| 2 | `quartet_semantics_mutations` | 8/8 spectrum, coordinate, domain, document, optimized attacks | REJECTED | REJECTED |
| 3 | `quartet_terminal_binding_mutations` | 12/12 algebra, split, reference, reassignment, reversal, optimized attacks | REJECTED | REJECTED |
| 4 | `canonicalizer_completeness_mutations` | 2/2 nonordinary/selected-triangle marker attacks | REJECTED | REJECTED |
| 5 | `parameter_transport_mutations` | 10/10 paired-edge, parent-flip, triangle, restriction, root and reversal attacks | REJECTED | REJECTED |
| 6 | `rank_upper_mutations` | 7/7 coverage, syzygy, orbit, port, false-rank and complete-verifier attacks | REJECTED | REJECTED |
| 7 | `corrected_raw4_overlay_mutations` | authoritative v2 9/9 | REJECTED | REJECTED |
| 8 | `theta2_full_map_mutations` | independent whole-map 10/10 | REJECTED | REJECTED |
| 9 | `corrected_primitive_composite_mutations` | raw4 14/14 + theta2 12/12; 22 complete-ledger attacks; payloads `94b2f2...` / `6395c6...` | REJECTED | REJECTED |
| 10 | `corrected_restoration_v3_mutations` | 13/13 omitted child, wrong parent/transport, reassigned certificate | REJECTED | REJECTED |
| 11 | `corrected_two_stage_probe_mutations` | 18/18 plus nondefault hash seed; omission/order/parent/transport/JSON/optimized attacks | REJECTED | REJECTED |
| 12 | `promotion_theorem_status` | promotion-manuscript byte drift | REJECTED | REJECTED |
| 13 | `promotion_quantifier_checklist` | promotion-manuscript byte drift | REJECTED | REJECTED |
| 14 | `promotion_pass_gate` | promotion placeholder byte drift | REJECTED | REJECTED |
| 15 | `promotion_zero_gate` | promotion placeholder byte drift | REJECTED | REJECTED |
| 16 | `promotion_ledger_path` | promotion placeholder byte drift | REJECTED | REJECTED |
| 17 | `promotion_combined_root` | promotion placeholder byte drift | REJECTED | REJECTED |
| 18 | `historical_artifact_promoted` | historical-registry authority fail | REJECTED | REJECTED |
| 19 | `historical_authoritative_replacement_removed` | historical-registry replacement fail | REJECTED | REJECTED |
| 20 | `historical_scanner_record_omitted` | historical-registry scanner coverage fail | REJECTED | REJECTED |
| 21 | `weak_sharpness_mutations` | 21/21 typed graph/tensor/rank/cherry/optimized attacks | REJECTED | REJECTED |
| 22 | `reassigned_cubic_certificate` | `DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH` | REJECTED | REJECTED |
| 23 | `reassigned_quartic_certificate` | `DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH` | REJECTED | REJECTED |
| 24 | `reassigned_quintic_certificate` | `DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH` | REJECTED | REJECTED |
| 25 | `raw4424_false_tree_sunlet_reintroduction` | frozen unified corrected-universe suite | REJECTED | REJECTED |

The failed concurrent beta attempt stopped during the twenty-fourth/direct
family setup because of host storage exhaustion; it did not produce a
complete semantic report and is not counted as the beta control.  Its source
inventory after failure was byte-identical to beta's pre-run inventory.

## Source-tree custody and inventories

| Tree/checkpoint | Files | Bytes | Symlinks | Inventory logical payload | Result |
|---|---:|---:|---:|---|---|
| pristine before review | 495 | 483,751,133 | 0 | `fa20f31760755fcf619212d638748d3928e162e9b650e84a12b56495c3708446` | baseline |
| pristine after full replay | 495 | 483,751,133 | 0 | `fa20f31760755fcf619212d638748d3928e162e9b650e84a12b56495c3708446` | no drift; no bytecode |
| disposable before setup | 495 | 483,751,133 | 0 | `fa20f31760755fcf619212d638748d3928e162e9b650e84a12b56495c3708446` | matched pristine |
| disposable after setup | 5,823 | 588,495,430 | 4 | `f27294708c3aad430ff46e635ab5b9a3ffc39e86fd63e84ffec9c5df3e643024` | only documented local `.venv` addition |
| disposable after compact gates | 5,823 | 588,495,430 | 4 | `f27294708c3aad430ff46e635ab5b9a3ffc39e86fd63e84ffec9c5df3e643024` | no post-setup drift |
| alpha before / after | 495 | 483,751,133 | 0 | `6264a43d4991caef06fe5107ac17a1a18cf17e273f310698698c41768b99f942` | exact equality; no bytecode |
| beta before / after failed / after control | 495 | 483,751,133 | 0 | `e03bba7279ec99ae6ec90071d780f023bd85cf5b314e4740ee00adc5de4e67a1` | exact equality; no bytecode |

The alpha/beta logical payloads differ only because the inventory schema binds
the different project-root labels.  Canonical `.files` maps have the same
SHA-256 `cc9d272d1f96ed0c3739a4489e8dd285376d2e718aa15ffefbda7f9469231082`.

## Controlling outcomes

- Package, source/PDF, provenance, quick, full, compact, mutation, and dual
  relocation execution gates: **PASS**.
- Expected negative tests (rank-atlas omission, bibliography omission,
  optimized execution, mutation rejection): **PASS when the intended failure
  occurred**.
- Noncontrolling environmental failures: initial missing local `.venv`; first
  simultaneous beta temporary-disk exhaustion.  Both have successful controls.
- Controlling semantic finding: the independent C09 narrative-binding audit
  exited 1 with exactly two mismatches.  This is R6-F1 and is detailed in
  `EVIDENCE_REGISTRY.md`; no later PASS erases it.
