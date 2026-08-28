# R4 fresh execution ledger — 27 August 2026 package

This is the reviewer-owned execution record.  The status column reports the
observed process outcome; it is not, by itself, a mathematical verdict.

## Environment and path notation

| Field | Observed value |
|---|---|
| Host | Apple M1 Pro, arm64; 10 physical / 10 logical cores; 16 GiB RAM |
| OS | macOS 26.5.2 build 25F84; Darwin 25.5.0 |
| Python | 3.14.6 (source requirement: >=3.10) |
| Exact Python packages | NetworkX 3.5; SymPy 1.14.0; pip 26.2.1 |
| TeX | Tectonic 0.16.9 |
| PDF tooling | Poppler 26.08.0 |
| Review root `$R4` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-27_r4` |
| Source ZIP `$ZIP` | `/Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260827.zip` |
| Disposable project `$P` | `$R4/execution/k2p_principal_d_plus_submission_referee` |
| Pristine project `$I` | `$R4/isolated/k2p_principal_d_plus_submission_referee` |

Unless a row says otherwise, project commands ran with cwd `$P`.  Commands
with a timed stderr log were wrapped in `/usr/bin/time -l`; the table records
its `maximum resident set size`, while the raw log also preserves macOS’s
`peak memory footprint`.  `—` means the metric was not sampled or not retained,
not zero.  SHA-256 values in `output` are hashes of the named stdout/result
artifact; each retained timed stderr hash is also given.

## Fresh top-level execution

| # | Exact semantic command or operation | Exit | Wall s | Max RSS bytes | Result | Output/result SHA-256 | Timed stderr SHA-256 |
|---:|---|---:|---:|---:|---|---|---|
| 1 | `unzip -t "$ZIP"` | 0 | 2.47 | 2,752,512 | all 491 entries OK | stdout `139d5d6beaec224a3c41769bd9d1f51548bce533ff577e7975087cf0838d4ca8` | `172808b596b9f53ef88cb318b5d3cbd9cdfa0f7fccc0592945d851ade281ae1b` |
| 2 | `independent_checks/provenance/audit_zip.py "$ZIP" "$I" "$I/output/referee/REFEREE_BUNDLE_CONTENTS.json" evidence/provenance/zip_audit.json` | 0 | — | — | all archive members hashed; extraction exact; frozen ledger exact | result `83df2f44cede9ce3158d033133f4279d444fb35cedea7f0fb4b0044fb2b221e1` | — |
| 3 | `audit_archive_ledgers.py --archive "$ZIP" --project "$I" --output independent_checks/provenance/archive_and_closure_audit.json` | 0 | 3.08 | 376,619,008 | PASS | result `d0396f9a708294728f48f2c3d8ceb9e60d05a01af89880224157fbad900183e1`; stdout `2a8f7e15c9863e1b66a3b5f84895e7abdb98dd43cd08575eee36383fff41713e` | `982a8af4cf2d034d4b8b8bc3a76fd8b9385d78a46383ba930f20a4f9dbdb9fa5` |
| 4 | `audit_tag_binding.py --repository /Users/alec/Documents/Math/k2p_level2_identifiability_closure --project-path . --tag k2p-same-biorxiv-v1.0.3 --archive "$ZIP" --output independent_checks/provenance/tag_binding_audit.json` | 0 | 9.42 | 893,779,968 | 491/491 tag bytes exact; remote IDs agree | result `b68801bb5e1b1eba11bc5c7968c6952259eebff74c93c248805ae406ae52f69e`; stdout `c7591750ac6692e6cb102d36d73b3c5c0a0eee62c491af9a7181f25d44554c87` | `e9c01626bd5eebb0be6ef040f93b852d48fc768968e1a03d599270af303849e2` |
| 5 | `audit_replay_telemetry.py --project "$I" --repository /Users/alec/Documents/Math/k2p_level2_identifiability_closure --repository-project-path . --tag k2p-same-biorxiv-v1.0.3 --output independent_checks/provenance/replay_telemetry_audit.json` | 0 | 7.08 | 433,061,888 | stored replay ancestry/source/telemetry PASS | result `6e2f485219f32ee8f8b53077ff4d06dcd12e2e750a71cc6e7a210185723118a2`; stdout `f3cd1a216df938b33e11b49541f8a71bd8f5301e6dcfd81113c9457cbc123975` | `b996a8adebef3e9ba9f398beb619740558e3ed0f8e51cb951c4f9b07416e140f` |
| 6 | `audit_submission_documents.py --project "$I" --output independent_checks/provenance/submission_document_audit.json --source-archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_SAME_bioRxiv_Source_20260827.zip` | 0 | 0.18 | 25,526,272 | five sources/PDFs/logs/fonts PASS | result `0cb501bf747c66bd035b601e67774e57c59306365894b17aff60041414375be9`; stdout `23b27d321c34dfb7f76715ffd1b08c338ad1c264394c68f6873701a05322c0ba` | `eab132888dedc02ec745dc27b23652c06fe4d4a06e76818f82f255fbc7235b7e` |
| 7 | `audit_authority_partition.py --project "$I" --output independent_checks/provenance/authority_partition_audit.json` | 0 | — | — | historical/revoked partition PASS | result `bf5168e38a5f3e2ba184f0c668f6a656ba3ff9b45efb5428e003765920b43602`; stdout `924ebd232daa1c3823bddbe8c712b4ecee1fcfc029b8e6dd8675e35f1a011992` | — |
| 8 | `python3 -m venv .venv` | 0 | 2.16 | 97,058,816 | environment created | empty stdout `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `b2d098a10ec7e1b03aec6a3a756ce4fc76e5fe118819ecdba9158042f3ed0bb0` |
| 9 | `.venv/bin/python -m pip install --upgrade pip` | 0 | 1.06 | 94,191,616 | pip 26.2.1 | stdout `718706568de9b06a27c22283e3371ff13caf160182c8064a49b6f642545ea1c7` | `b1f5eec25d17b7e95a4057165391b1e5294dac23469ceb26e0bafdc387d58cdc` |
| 10 | `.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | 0 | 5.55 | 175,849,472 | NetworkX 3.5; SymPy 1.14.0 | stdout `b8cb8888e74efb13d53a13b09a6cf6e18e4df64a873dd861491a02bfca6cf7e8` | `71be5d6cfadaa87275a07e0464637115c3b91d54f947fd3836e40554c09c31d1` |
| 11 | `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.47 | 229,294,080 | 406 files/root PASS | stdout `734d2963a08ff58fa395001c1973c0153348a902e2c6a1f93085865563b8b217` | `c79e44cf166dd15137e1fa3790119a6df1b09530a2922ff7acf8343454f64f46` |
| 12 | same portable-ledger check, independent provenance invocation | 0 | 0.48 | 229,736,448 | identical PASS output | stdout `734d2963a08ff58fa395001c1973c0153348a902e2c6a1f93085865563b8b217` | `e065da8bb2fa13b4d09471b48aa2bc757cc21abc85274ec7bfd9dbe26d3d2d57` |
| 13 | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --require-ready` | 0 | 9.90 | 497,680,384 | regenerated bytes identical; PASS | stdout `be130e83dc7975cfc1f45d0c24c4bc6a6d7052864d62287d304ee494821ed675` | `21bf4112a27eb59c7bafa4d4d6db341e9a509eb665458568a173e5f0ba894207` |
| 14 | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 9.87 | 518,062,080 | PASS | stdout `512b42175588bb9d4c686b57ae122cf28c35619b05a9b364603b996783afa1f0` | `b393d153cebabe8994c134348febf1b59eedcc883cc994eb84af56c8e524d656` |
| 15 | same release-lock check, independent provenance invocation | 0 | 10.03 | 508,100,608 | identical PASS output | stdout `512b42175588bb9d4c686b57ae122cf28c35619b05a9b364603b996783afa1f0` | `56690f0427017ffe45ef7612a5ed6f1fb43570c432e5ede91df22096ddcf5e60` |
| 16 | `python3 -B proof_compression_submission/adversarial_review/audit_article_sources.py --check` before `.venv` existed | 1 | 0.19 | 41,451,520 | intended dependency rejection: `CROSSWALK_PATH_MISSING:.venv/bin/python` | stdout `3f793e0faa5a122f9b747dbaf95fe0bda96fc93ab0f22d47606377791e907207` | `3691c9b814b5fa78e9b1a75d14ea64b974a47885cbb7464a7dacadfb53ed7bdc` |
| 17 | same static article audit after environment setup | 0 | 0.19 | 41,500,672 | PASS, 26/26 bound rows | stdout `a1bd85a53462390549681d5d025a99ea7fb415e2ca5c97d986d3c11ffad2c966` | `e6b8bc04caebaaf49f86cf007d7efd3a90831028c5a49269703717807034eadc` |
| 18 | `python3 -B proof_compression_submission/adversarial_review/test_printed_authority_hash_gate.py` | 0 | 0.05 | 27,721,728 | 9/9 intended rejections | stdout `af7d96b25558d4a4bfeceea6e69967eba10ed8af612383576b4b508322b1f036` | `fbfc7c24616e4a62e7d70fabe7cd100b1b695ea18f084dd58151614f888e68b8` |
| 19 | `python3 -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.95 | 398,491,648 | PASS | stdout `3fbfd3996b43d536140b597478dd21500cd6e7ae199cce1d34855db086723074` | `cbc374836f8ebe50f09184dec2a6a42ecae9cd3b63388dfbc794cbd462470431` |
| 20 | same revised-manifest producer check, independent provenance invocation | 0 | 0.99 | 400,048,128 | identical PASS output | stdout `3fbfd3996b43d536140b597478dd21500cd6e7ae199cce1d34855db086723074` | `4d4b7ae18819a62b3c3eb98ae82c793ceea530c2114de6a5103659d3c05adb06` |
| 21 | `python3 -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 1.19 | 397,688,832 | independent checker PASS | stdout `3fbfd3996b43d536140b597478dd21500cd6e7ae199cce1d34855db086723074` | `a4c752ce8e9ba257fd6439eb772c0af443deb3e49c1c30ebe91151e85253cd95` |
| 22 | same revised-manifest checker, independent provenance invocation | 0 | 1.17 | 399,654,912 | identical PASS output | stdout `3fbfd3996b43d536140b597478dd21500cd6e7ae199cce1d34855db086723074` | `3a8eec74943ec3540a4a0ff60ac3f9292d7ac8d4862e1019b0ff250e5210f755` |
| 23 | `python3 -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 25.39 | 624,295,936 | 33/33 PASS; zero survivors | stdout `7269bbb13d381069b8ccb235d12c482a674a88c555bac7216f30dabf96a66cea` | `95502f39b26b6c9826ca22cf584be96437095fd96f3e12be0ef7ac9d1a938388` |
| 23a | `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.29 | 173,703,168 | PASS, 13 claims; payload `961102d2ff04d99100fc6f657cd83a02dc99b070279e24f84edfa0a961411553` | stdout `8579779f2ec3297a4ef0de28fa563aa07e720216672e3ed024c0453f91bae0a1` | `4b664315a27a8e237b6d3ed00847bb2cf24e2908e82c7bbf955800902fb37791` |
| 24 | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick --output "$R4/evidence/computation/quick_report.json"` | 0 | 282.68 | 1,399,980,032 | PASS 23/23 | report `3bf21791732e51341b8ce77c597d6343563eea5e847309721b666e2c909300c7`; stdout `835641ca0058875b9ee3adb05b3fc3ef8792a8d2bd3e6ddbf4e7bb091b05f553` | `5885bc087aeb21ab4906551b8cdcdd233e522a1e7ad43c7d2dbeb3cac83e688b` |
| 25 | `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --output "$R4/evidence/computation/release_mutations_report.json"` | 0 | 3,550.64 | 2,636,218,368 | PASS 25/25; zero survivors | report `866cb66ffd5ad8fae159a487dc5f35a98d946fc2e5c363f9dfd5fea5a1591788`; stdout `4f515b552df3afb70d7aa6f5d2b432661c4e5c55f1758bd044793811a19527bc` | `03d650c6729a01c963d01492785b2009523df65dbba309be566231aeaf50b0e1` |
| 26 | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --output "$R4/evidence/computation/full_report.json"` | 0 | 5,978.84 | 2,635,841,536 | PASS 41/41 | report `77ee2ee95d5c1d2a9816a1fa21bbdd78d776faf6fc3492d21b6ef5929c3b3de7`; stdout `9c04c70010663669efb52674636cd279f2ef2ba604fcf233a7e97794a80cde1a` | `786ad2f2c6dfa1e4f3ee7f070017acf574f0c8f8c6a03f2379f98bcb331b460c` |
| 27 | `.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check` | 0 | 0.10 | 34,013,184 | PASS, PC-PARTIAL, zero unresolved mathematical records | stdout `faa941ac0a3ed2b30ad8f66a8186607d7715a322956cdcae8cae51c448cf4981` | `e16e425c841dea46f1eec0a9058f853fa09672c089cecb2f056e92674837abe1` |
| 28 | `.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check` | 0 | 75.29 | 290,062,336 | PASS, 7 commands | stdout `6123850d1419bd5ffc1da5fcb20dc4c7e673fdda793670ad1e968d3cc5f38477` | `d79ae3acb7bffea9d990ce856543d43aaf4ade2ed2a9a34f0418fbf8c84a3242` |
| 29 | `.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check` | 0 | 0.39 | 40,239,104 | PASS, 11/11 | stdout `d240899c786e9f20999675ca74977b7479f18940f434560760d948b3e1bea1eb` | `b5f3b710e102fa57a46ecf8678854835297ac03d1fee9951ee30f275723f0a14` |
| 30 | `/Users/alec/Documents/Math/k2p_level2_identifiability_closure/.venv/bin/python -B independent_checks/math/independent_math_checks.py` | 0 | 0.54 | 64,274,432 | independent exact PASS, including cherry observable/inverse/Jacobian determinant `2464/675` and exact recovery of `(2/5,3/7,4/9,5/11)` | stdout `a32ff51961b00ba6f7912380270bcea37834fa516e788aeaa071f444eb5b4657` | `bb897056714e3b755bc3980462ae7797cfb1d968a622140813e64beaf3b23144` |
| 30a | `python3 -B independent_checks/math/boundary_rational_checks.py` | 0 | 0.04 | 21,086,208 | exact `Fraction`-only PASS: 5 `D_plus` faces, 4 CT faces, 2 inheritance faces, 5 subdivisions, 25 products, 20 surjective sections, 8 CT powers, 6 transformed bridge witnesses, 2 simultaneous CT gluing cases | result `6535ee1d2310a49da99729ab3fbe522af29a1ce49b35ce52cb8f7a15e168c069`; stdout `50047a8f1c2f31ad45c27cc3dba3571a6e7b490233bd5f87ab59bcd040f23964` | `f9ce145c6fc57d2e6a575aed928dccc405a8a24f48fffb6ab74f36304dcbe585` |
| 31 | `/Users/alec/Documents/Math/k2p_level2_identifiability_closure/.venv/bin/python -B independent_checks/computation/r4_independent_semantic_attack.py --project "$I" --output independent_checks/computation/r4_independent_semantic_attack_result.json` | 0 | 203.28 | 3,253,387,264 | independent clean census/graph/join PASS | result `35e56426ca918aa806e5cee66c91e4849168d4f587115562654e67ec66de730b` | — |
| 32 | same interpreter, `r4_probe_duplicate_jsonl_attack.py --project "$I" --output independent_checks/computation/r4_probe_duplicate_jsonl_attack_result.json --python /Users/alec/Documents/Math/k2p_level2_identifiability_closure/.venv/bin/python` | 0 | 17.05 | 70,025,216 | **mutant accepted by submitted probe verifier** | result `0b14d7dde85e323ed5ae4271e75f5f6f68d38a59f90e3c78931d828f552c7732` | — |
| 33 | `python3 -B independent_checks/computation/entrypoint_optimized/run_entrypoint_guard_matrix.py` | 0 | — | — | ten protected entry points reject `-O` | result `98ca64950a211af8eb743a6c55870b8595e48787e5a1f77ddb1f9687e47e6572` | — |
| 34 | `.venv/bin/python -O -B package/referee/k2p_offline_sweep_portable/verify_package.py --skip-smoke --skip-mutations --skip-prepared-audit` | 0 | 7.18 | 1,502,920,704 | **unexpected PASS** | stdout `2e05df25a73f535d10e7c3f2bf72f12db880b73471c524468d9f85afacccbaf0` | `5cf208a66aa4cb94533eabc17d6ddafa0123805c5533ed0c35f295550a7cb9a0` |
| 35 | `PYTHONOPTIMIZE=1 .venv/bin/python -B package/referee/k2p_offline_sweep_portable/verify_package.py --skip-smoke --skip-mutations --skip-prepared-audit` | 0 | 9.90 | 1,506,148,352 | **unexpected PASS**, same stdout | stdout `2e05df25a73f535d10e7c3f2bf72f12db880b73471c524468d9f85afacccbaf0` | `3d7dc738ac51327f56006a7aa9a7d449ae09bf02060fc3c260f7bbd85e96073b` |
| 36 | `.venv/bin/python -O -B package/referee/k2p_offline_sweep_portable/resumable_four_port_driver.py --package-root package/referee/k2p_offline_sweep_portable --list-sources` | 0 | 4.01 | 1,506,476,032 | unguarded substantive entry | stdout `f753451c5dc0c40be3bd6d8fa304a1e51df5ca0f2fe332385d10c57220c6010c` | `8f0bb3d720469c12dfc9cce28050fb27d6022b350a8a721453974124f93187e0` |
| 37 | same driver under `-O`, `--source-index 0 --start 0 --end 1 --output-root <review-owned disposable output>` | 0 | 5.44 | 1,505,984,512 | wrote pristine class 0 as `separated` | stdout `0d7b8ca4f4100edc6a706db1496a6f7b751094c6b3572fa51e62ec1d5c452708` | `648ea24930f5c20a587ca118555339d45a6a8cad6aaa863c289111726bfc9bb9` |
| 38 | mutated portable driver, normal `-B`, source 0/class 0 | 1 | — | — | intended target-zero `assert` rejection; no record | empty stdout `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | stderr `15e48cf3775283063993dadc9db6848a7231ecfa8500096df63daf880726a6a4` |
| 39 | same coherently relocked mutated driver with `-O -B` | 0 | — | — | **false `separated` record written** | record `ded971c15ce148fc2e4e0d6b259aa9a2fe4fc70cf47e9fd18f1d064d249d251d`; stdout `0168fc9d8f6ebd9044f9a8fa0bf83583e1bbdd60b3ffae25afd13b85bd1889d6` | empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 40 | `.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py` | 0 | 13.56 | 254,033,920 | two clean builds internally; `AWAITING_VISUAL_INSPECTION`; omission gates passed | stdout `e912b13384b15966994b1e9b15faf2e4e187b0f8566bbeda235deb18a68bbbd3` | `43379e409bdf30389cc3cb983a645e58e2b4e90ec691eb78caa76df540c7f723` |
| 41 | `pdftoppm` render of rebuilt 26-page article at 96 dpi | 0 | 0.40 | 17,743,872 | 26 page PNGs | empty stdout `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e1e8a45934bb11197648ce4556593a667564cb3d675509191da0abe0d785f146` |
| 42 | `pdftoppm` render of rebuilt 24-page supplement at 96 dpi | 0 | 0.29 | 17,530,880 | 24 page PNGs | empty stdout `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `a643111e8b4def032277fa748296fc05530da7c7ffbadf3ca5dd409f47bfa03b` |
| 43 | visual inspection of all 50 page renders/contact sheets | — | — | — | PASS: no clipping, overlap, malformed table, missing glyph, or layout defect | review observation; no output hash | — |
| 44 | `.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py --visual-pass` | 0 | 13.46 | 255,606,784 | PASS; published report in disposable copy | stdout `6d68bae40fe6527cd30363909c008f822c665fb35920b7947d22d960f75db534` | `839cfecbad963c80a87aed2355dcb48b5a3978ea8a8568934633ebabab690af9` |
| 45 | `.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 13.13 | 254,558,208 | PASS; exact report/source/PDF check | stdout `6d68bae40fe6527cd30363909c008f822c665fb35920b7947d22d960f75db534` | `ee4e2dfab79326f35084d7a692c254633b361c67bfdf80e739ee843eff918d03` |
| 46 | from `$P`: `python3 -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check --archive "$R4/tmp/archive_A/rebuild.zip"` | 0 | 20.55 | 418,775,040 | byte-reproducible ZIP | stdout `65a930d3035f1739a500586e0734096cb6fb1a9246c34f0792a75842c26f9736` | `16a709c3a7ee666d1b78ca087d84a90a64ceba22d877bce323686701e122f27c` |
| 47 | from `$I`: same builder, output `$R4/tmp/archive_B/rebuild.zip` | 0 | 21.26 | 561,364,992 | byte-reproducible ZIP | stdout `461cddb9ec748ac1f7ac92b1415c277e68390ca9638ab8cc46cbe71d363cf4f1` | `232f2e5966e4b46524fab7536c477e47ccc259f2eac8bc5d3ed6302a74737b4e` |
| 48 | byte comparison rebuilt A vs rebuilt B | 0 | — | — | identical | no output retained | — |
| 49 | byte comparison rebuilt archive vs `$ZIP` | 0 | — | — | identical | no output retained | — |
| 50 | post-run `audit_archive_ledgers.py --archive "$ZIP" --project "$P" --output evidence/provenance/postrun_execution_archive_audit.json` | 0 | 3.31 | 363,347,968 | closure/archive fields still exact | result `d0396f9a708294728f48f2c3d8ceb9e60d05a01af89880224157fbad900183e1`; stdout `2a8f7e15c9863e1b66a3b5f84895e7abdb98dd43cd08575eee36383fff41713e` | `b0a49062d7f0ee71805181401e3720e3f3109bfdf330c3d4027461d5bf6c7dd6` |

The two rebuilt ZIPs and their directories were deleted after their hashes and
byte comparisons were recorded because reviewer disk space was constrained.
The immutable distributed ZIP, pristine/execution source trees, reports, and
logs were retained.

### Superseded reviewer-development diagnostics

Two intermediate cherry-check diagnostics are recorded for transparency but
are not controlling package operations and are excluded from the numbered
ledger above:

- A first review-script rerun accidentally used system Python and exited 1 in
  0.05 s with maximum RSS 20,365,312 bytes solely because SymPy was absent.
  Stdout was empty (SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`);
  stderr SHA-256 was
  `922f1e90d2cbfc06adb23f78381923f6232882e314dc35857cb72e4e52d4ce93`.
- The next review-owned venv run exited 1 in 0.62 s with maximum RSS
  64,913,408 bytes because the reviewer had entered the wrong expected
  arithmetic value `P_g=15/77`.  Stdout SHA-256 was
  `528173a9b368eb3c1f17af1f0fc692c302d3d04380cc57004d4635593abe0e15`;
  stderr SHA-256 was
  `7954a968b8bee7f3d16d6e5343fcc2eecb849220915d2e31e4a3e672af435805`.
  After correcting the review expectation to `P_g=20/99`, numbered row 30
  passed and independently recovered the complete input tuple.

Neither diagnostic touched submission source, exercised a failing package
claim, or counts as a package failure.

## Fresh quick-harness child ledger (23 commands)

The harness’s JSON report records stable layer names, elapsed times, return
codes, and raw child stdout/stderr hashes, but intentionally does not serialize
raw argv.  Exact argv remain defined in the inspected
`verify_final_theorem_release.py` (SHA-256
`700c5d43aaf83ee504498ad61fb38f0b9df5271cc537cb24216bcc5b1d0bbb46`).

| # | Layer | Exit | Elapsed s | Child stdout SHA-256 | Child stderr SHA-256 |
|---:|---|---:|---:|---|---|
| 1 | `promotion_manuscript_guard` | 0 | 0.268993 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `full_map_domain_reseal` | 0 | 0.099632 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `corrected_universe_independent_replay` | 0 | 9.818439 | `f7e9a523cda71bb0908f0525ac0e861d43242f336ae17fdfdf9441fe968b503c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `three_port_no_assert` | 0 | 0.425285 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `domain_rooting` | 0 | 0.059819 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 6 | `quartet_sign_logic` | 0 | 1.077513 | `83132d46011458b6ee2a262c05ff80ec38702c86e4345340724dd32083a588ab` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 7 | `quartet_terminal_bindings` | 0 | 33.290108 | `8eb23b2e09472d77d63e9bd47dd389752f98f0817889fdbc057f097f7212fc2b` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 8 | `raw_displayed_quartet_direction` | 0 | 2.686945 | `91fc95ea11887e6007cf59e760a26e0f1757753a833bf313ac18d8e623620a35` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 9 | `canonicalizer_completeness_structural` | 0 | 0.200660 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 10 | `graph_derived_parameter_transports_structural` | 0 | 26.841793 | `4b3646ec38d0ef52964beb12721c7f2a2be6cb0620fa89aaef36f6e9f8639908` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 11 | `bridge_marginal_gluing` | 0 | 0.057397 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 12 | `analytic_adversarial_audit` | 0 | 0.399472 | `4884773924959ae0c0ce29953487165662b2efceeca8b572a2ea67fd01fb6bb2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 13 | `global_component_scale_audit` | 0 | 0.166369 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 14 | `raw4_corrected_overlay_independent` | 0 | 87.096077 | `f388968a3d1a6cf39091a0a9af7e88de08d3a23ad45a186b5dd57e0f4ad06b46` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| 15 | `theta2_full_map_independent` | 0 | 45.119012 | `29309e25f599eeec7a510ed0a0dd71c4c07919b93250902532ba4f6f5e13f361` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 16 | `four_port_raw_structural_provenance` | 0 | 1.494257 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 17 | `four_port_direct36` | 0 | 14.128482 | `8d53ffac2b3823abda37eb3dc40cde2e50d1a0a703ac3b4a2bbbd394bb9b113d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 18 | `theta2_structural_provenance` | 0 | 10.791929 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 19 | `cycle_three_port_authoritative_promotion` | 0 | 16.903612 | `a3270f6dddef4b40ce8772ff9ad3c872b8010418039bdc95e0c7ce65ddd1cc93` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 20 | `corrected_probe_independent_streaming_replay` | 0 | 16.783607 | `ce27e8a17795548a178568a7198635c9ebe6bef03932c7dae89f3c5a637591e1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 21 | `corrected_probe_site_transport_partition` | 0 | 4.609037 | `57603f796ecbed71b4a24a09297d7f9d0fa019d1436556d7a6f14beb59fe0deb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 22 | `weak_sharpness_primary` | 0 | 0.167419 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 23 | `weak_sharpness_independent` | 0 | 0.174535 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Fresh full-harness child ledger (41 commands)

| # | Layer | Exit | Elapsed s | Child stdout SHA-256 | Child stderr SHA-256 |
|---:|---|---:|---:|---|---|
| 1 | `promotion_manuscript_guard` | 0 | 0.293818 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `full_map_domain_reseal` | 0 | 0.104733 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `corrected_universe_independent_replay` | 0 | 9.641853 | `f7e9a523cda71bb0908f0525ac0e861d43242f336ae17fdfdf9441fe968b503c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `three_port_no_assert` | 0 | 0.255514 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `domain_rooting` | 0 | 0.058212 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 6 | `quartet_sign_logic` | 0 | 1.078555 | `83132d46011458b6ee2a262c05ff80ec38702c86e4345340724dd32083a588ab` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 7 | `quartet_terminal_bindings` | 0 | 34.145969 | `8eb23b2e09472d77d63e9bd47dd389752f98f0817889fdbc057f097f7212fc2b` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 8 | `raw_displayed_quartet_direction` | 0 | 2.709245 | `91fc95ea11887e6007cf59e760a26e0f1757753a833bf313ac18d8e623620a35` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 9 | `canonicalizer_completeness_structural` | 0 | 0.194363 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 10 | `graph_derived_parameter_transports_structural` | 0 | 27.355144 | `4b3646ec38d0ef52964beb12721c7f2a2be6cb0620fa89aaef36f6e9f8639908` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 11 | `bridge_marginal_gluing` | 0 | 0.055810 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 12 | `analytic_adversarial_audit` | 0 | 0.401067 | `4884773924959ae0c0ce29953487165662b2efceeca8b572a2ea67fd01fb6bb2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 13 | `global_component_scale_audit` | 0 | 0.154538 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 14 | `raw4_corrected_overlay_independent` | 0 | 86.317780 | `11f08fcd1718edb58531043ee2cf94a2db3c336cb9b0fab1530ee5a2b74bcd04` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| 15 | `theta2_full_map_independent` | 0 | 44.800551 | `5df361929cd2c4db73ac58ae93db979f48f0e39fc6bc11a5ec60a17317cec895` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 16 | `four_port_raw_structural_provenance` | 0 | 1.478982 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 17 | `four_port_direct36` | 0 | 13.623406 | `8d53ffac2b3823abda37eb3dc40cde2e50d1a0a703ac3b4a2bbbd394bb9b113d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 18 | `theta2_structural_provenance` | 0 | 10.790940 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 19 | `cycle_three_port_authoritative_promotion` | 0 | 16.722257 | `a3270f6dddef4b40ce8772ff9ad3c872b8010418039bdc95e0c7ce65ddd1cc93` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 20 | `corrected_probe_independent_streaming_replay` | 0 | 16.697578 | `ce27e8a17795548a178568a7198635c9ebe6bef03932c7dae89f3c5a637591e1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 21 | `corrected_probe_site_transport_partition` | 0 | 4.570021 | `57603f796ecbed71b4a24a09297d7f9d0fa019d1436556d7a6f14beb59fe0deb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 22 | `weak_sharpness_primary` | 0 | 0.152913 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 23 | `weak_sharpness_independent` | 0 | 0.174492 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 24 | `canonicalizer_completeness_full` | 0 | 100.780871 | `dde7a6df548d407df5cedb2810549aac0711269718ba203c9ddbd45461675188` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 25 | `graph_derived_parameter_transports_full` | 0 | 289.974424 | `bd213d981376cd17a04c4d2813916092a79a41541b1c8ece01fb9882496d72f8` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 26 | `corrected_restoration_independent_full_replay` | 0 | 466.221573 | `7e3e631312333780b77c77af977d013d02e89646d75927b76e4a973e92ea74df` | `7bb69d81f6d45d866e3030dda574eb3b5056c637319c017fc12ee4b3c10fb1da` |
| 27 | `corrected_universe_cross_layer_mutations` | 0 | 199.021098 | `14ad6897e7e53cf4b95ceeb055876fe00c0e709269d363af3a9a16f4dfcf2a15` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 28 | `raw4_full_map_Ti_truth` | 0 | 18.703678 | `ec5d6f372abbefabcb41bdb042503e88238325bb4f71cb1850823d55057d684a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 29 | `theta2_full_map_Ti_truth` | 0 | 70.954285 | `fe586c75afe67b879a0c2f96d9520417a72572794b4f89ff337e7951ce1194e2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 30 | `composite_domain_reseal_diff` | 0 | 16.043564 | `0c9290e7142fc4f3dc0a89408015b806385b48e507d6a2eebe0e2fca8e3fcfca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 31 | `four_port_exact_rank_staged_atlas_omission_mutation` | expected 1 | 0.318827 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `a67ee902d7853b76b85815a6723be3439bbb3bcdae6b5fc14d817f942502b856` |
| 32 | `four_port_exact_rank_import_preflight` | 0 | 0.305261 | `79d039353c2a88425952fe6ffd8e67653c512de65e89b2ab6f22b46e5ee72212` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 33 | `four_port_exact_rank_full` | 0 | 119.862162 | `f3370e890b15aaa7643a808baaa41ee1c38d6383f102462dbabffae45d471c06` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 34 | `raw4_corrected_overlay_full_regeneration` | 0 | 60.187880 | `b62bf1aa1efc498e83e9054af1bb5228a9213f4c03ff07fcbfc01d6001059870` | `de1f579aafe4aa7f4d84e6f47f6b6ca9aba263df850de2b6839abc89018dfb8c` |
| 35 | `four_port_raw_full_regeneration_provenance` | 0 | 310.493651 | `8eb91f720fe064d3007c5f2f4a65295b921c068285b1fad9db3d3710ae3f55c6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 36 | `four_port_direct36_full` | 0 | 104.972465 | `770af48343668f93633451072582efb477294a88da4046b88d2eac91508c2727` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 37 | `theta2_full_regeneration_provenance` | 0 | 469.919709 | `82c6917c4503a2cb7d3c42988100a58731dff13c8972a45b27ffbb5226bbd783` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 38 | `corrected_probe_full_primitive_regeneration` | 0 | 3004.717560 | `129a45db66a6e1a9b4e733ce4a87c6be61e678031bd62b09a8246e5945036a55` | `c2415184e691fb40195027d8c6daa36ea5500e88c107f837d898862760fa194c` |
| 39 | `corrected_probe_full_independent_replay` | 0 | 17.487351 | `ce27e8a17795548a178568a7198635c9ebe6bef03932c7dae89f3c5a637591e1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 40 | `corrected_probe_full_site_transport_partition` | 0 | 4.995406 | `57603f796ecbed71b4a24a09297d7f9d0fa019d1436556d7a6f14beb59fe0deb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 41 | `corrected_probe_independent_primitive_graph_full` | 0 | 441.427862 | `d17da6517e02a00e522c57e3cf76a7e484036e565aa23249aebbd73b268aea58` | `cbc56ffd93ed354a5cd9adfa22ebe130b83db6b8822b4fc1adc29c66e71e7602` |

## Current-command coverage and unrun gates

| Documented current command | Coverage |
|---|---|
| Three venv/pip commands | separately run, exits 0 |
| `build_release_lock.py --require-ready` and `--check --require-ready` | separately run, exits 0 |
| `verify_final_theorem_release.py --quick` | separately run with caller-owned report, exit 0 |
| `run_release_mutations.py` | separately run with caller-owned report, exit 0; its mandatory preflight invoked all three focused output-contract tests |
| `run_corrected_universe_mutations.py --output …` | not separately logged at top level; invoked by full layer 27, exit 0, and compared against the bound result |
| `verify_final_theorem_release.py --full` | separately run with caller-owned report, exit 0 |
| Three proof-compression commands | separately run, exits 0 |
| Static article audit, revised-bundle producer/checker, crosswalk mutations | separately run, exits 0 after setup |
| `build_theorem_artifact_crosswalk.py --check` | separately run, exit 0, 13 claims PASS |
| Archive builder with `--check --archive` | twice in separate clean locations, exits 0; byte comparisons pass |

Optional resealing/write forms (`build_referee_bundle.py --ledger …`, the
crosswalk `--write` commands, and `--allow-authoritative-output`) were
deliberately not run against the pristine authority.  Their corresponding
check paths were run; the only writing producer used for qualification wrote
inside the disposable execution copy, and archive/report outputs used
reviewer-owned paths.  These write modes are maintenance operations, not unrun
scientific gates.

The literal legacy names `verify_handoff.py`, `test_handoff_mutations.py`,
`setup_environment.sh`, and `run_all_verifiers.py` are absent and were not run
by name; their documented current mappings above were run.  `START_HERE.md` and
`SUBMISSION_BINDING.json` are likewise absent and map to the two READMEs and
the release/content ledgers.  No command was inferred to have passed merely
from a stored report.  The corrected-universe and three output-contract scripts
were executed as named child/preflight commands; their lack of separate
top-level logs is not an unrun theorem gate.
