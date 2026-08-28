# R4 evidence registry — K2P principal-domain referee package

This registry covers the fresh review of the 27 August 2026 archive.  It is a
review-owned index, not an authoritative package artifact.  “Stored” means the
file was distributed in the ZIP; “fresh” means it was produced or checked in
this review; “independent” means the review-owned implementation did not call
the decisive submitted classifier or release verifier.  Hash agreement is
provenance evidence only.

## Immutable input and execution copies

| Item | Status | Bytes | SHA-256 / binding |
|---|---|---:|---|
| Distributed ZIP `/Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260827.zip` | immutable input | 214,944,591 | `51f502290434cd3415936ef69e3c5afe71438fa892d5b9e6998feecc47489278` |
| Pristine extraction `isolated/k2p_principal_d_plus_submission_referee` | fresh, read-only review copy | 491 archive files | byte equality to every archive member checked; zero extraction mismatches |
| Disposable execution copy `execution/k2p_principal_d_plus_submission_referee` | fresh working copy | 491 archive files plus `.venv` | post-run archive audit result `d0396f9a708294728f48f2c3d8ceb9e60d05a01af89880224157fbad900183e1`; archive/closure fields remained exact |

The ZIP has 491 regular entries, 483,653,934 uncompressed bytes, one fixed
prefix, lexicographic order, fixed `2026-08-27 00:00:00` timestamps, mode
`100644`, DEFLATE compression, and no unsafe name, duplicate path, case-fold
collision, directory entry, symlink, special file, encryption, or CRC failure.

## Frozen release and package ledgers

| Distributed artifact | Kind | Bytes | SHA-256 | Verified semantic binding |
|---|---|---:|---|---|
| `work/final_theorem_release/RELEASE_LOCK.json` | stored theorem authority | 79,989 | `30132af1b10f7aba6d49ababf14551f9f914a19dc6a0638517761b6b85cf4c8d` | payload `a32e7f04d5c979fc1f9e268ca8a791ae24ad99b296f3e3c72682a3beadadd653`; 230 direct files; promotion ready |
| Recursive release closure | independently recomputed | 479,327,565 | content root `3e01609b924a4e884f58916e852fa4e63eaa8ab1a1af3c932de1ecc3498efcd0` | 406 files; rank manifest 94, cycle manifest 17, direct lock 60, input lock 15 |
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | stored portable ledger | 76,995 | `6fd50449e450d45176346b47e19a06f667fd29a1c190f66032793df562eaec6f` | exactly equals the 406-file recursive closure |
| `proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json` | stored outer submission ledger | 99,328 | `6baf7448867bd3ed7968be9d98bbd9de2cab716937e7c631c054e211b059f3b0` | 406 frozen + 84 submission/support files; payload `e7d40183edc8878ec91ea3a3fc00039225afbcd136a0c5d7af3a20e6b60caa10`; combined root `5b7aa44ef814c3ba08eb6b6be86d9a11cf6595b236c5d33e3d7ecd4597b1aaba` |
| `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json` | stored theorem/artifact crosswalk | 87,596 | `2f4c1c53981efa3bd0c7efc31813398007b71c813570726cca596e3603b52990` | included and hash-bound; fresh producer `--check` passed 13 claims with payload `961102d2ff04d99100fc6f657cd83a02dc99b070279e24f84edfa0a961411553` |
| `proof_compression_submission/crosswalk/CROSSWALK_BUNDLE_MUTATION_REPORT.json` | stored mutation report | 7,200 | `883a3be0537010d3e435cb6c0dc953da8f4d8cb76f4fd33dd9cf9504d4f83749` | fresh 33-case comparison passed; payload `62a056e21c8a514fe2e7e96ab952464fcb0a1489d785ccde8ff390e5f5006fe2` |

## Stored execution evidence versus fresh controlling replay

| Evidence | Status | Result | File SHA-256 | Important binding |
|---|---|---|---|---|
| `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json` | stored, provenance-only until replayed | PASS, 41 layers, 5,880.415302 s internal | `5a5f62104bea1e88d725aa3cee0441c369d53905f71fe30bc20de82f4eadb35e` | replay commit `1ef5dd2737a50fd33bc3b15d63e0ba70b050e03f`; all 406 closure files and all five TeX/Bib sources byte-identical to tag/package |
| `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json` | stored provenance | telemetry PASS | `200b8f18dcd01c2f9fc4f3013b6963b3b8e8083b1acb6a591e28c6e42f7695e3` | wall 5,880.83 s; Python 3.14.6, NetworkX 3.5, SymPy 1.14.0; report hash above |
| `evidence/computation/quick_report.json` | **fresh controlling run** | PASS, 23/23, 282.231960 s internal | `3bf21791732e51341b8ce77c597d6343563eea5e847309721b666e2c909300c7` | lock payload `a32e7f…`; no blockers; unoptimized interpreter |
| `evidence/computation/full_report.json` | **fresh controlling run** | PASS, 41/41, 5,978.474062 s internal | `77ee2ee95d5c1d2a9816a1fa21bbdd78d776faf6fc3492d21b6ef5929c3b3de7` | all exhaustive layers completed, including primitive regeneration, restoration, probes, transports, rank, theta2, raw4, and unified mutations |
| `proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json` | stored report | PASS, 25/25 | `866cb66ffd5ad8fae159a487dc5f35a98d946fc2e5c363f9dfd5fea5a1591788` | payload `6e18ee2606ca765dbcbbd38bf86b0a4a247ecc104f3524e122160bc6d0748e7d` |
| `evidence/computation/release_mutations_report.json` | **fresh controlling run** | PASS, 25/25, zero survivors | `866cb66ffd5ad8fae159a487dc5f35a98d946fc2e5c363f9dfd5fea5a1591788` | byte-identical to stored stable report; output-contract preflight passed |

The equality of the fresh and stored mutation-report bytes is expected because
that report intentionally excludes runtime and temporary-path telemetry.  It
does not make the stored report a substitute for the fresh command.

## Exact finite evidence confirmed in the fresh full run

| Layer | Freshly reconciled counts |
|---|---|
| Four-port raw universe | 405,216 = 360,408 quartet + 16,974 whole-map sign + 23,822 symbolic rank + 1,472 direct terminal + 2,540 restoration member |
| Four-port direct terminals | 839 quadratic classes + 36 higher-degree direct classes + 4 hard bindings + 20 isomorphisms + 35 triangles; higher degree = 22 quintic + 12 quartic + 2 cubic |
| Theta2 five-port universe | 2,946,240 = 2,942,592 quartet + 2,528 whole-map sign + 800 rank + 240 quadratic + 80 isomorphism; forest 56 roots, 864 descendants, 832 leaves |
| Cycle layer | 13,440 bases, 536,364 children; base partition 5,964 restoration + 7,452 whole-map sign + 8 isomorphism + 16 triangle; child partition 535,920 quartet + 132 quadratic + 300 whole-map sign + 12 isomorphism |
| Restoration | 997 canonical parents, 2,540 roots, 36,568 first children, 256 second children, 36,824 edges, 36,792 leaves, depth two, zero duplicate/wrong/missing/cyclic rows in independent check |
| Probes | 176 anchors; 2,206 source and 2,206 target sites; 29,964 one-port rows; 2,107 one-port equality parents; 544,571 two-port rows; 67,741 exact transports; 4,379 restrictions |

## Article, supplement, exact source set, and PDF evidence

| Artifact | Bytes/pages | SHA-256 | Evidence class |
|---|---:|---|---|
| `proof_compression_submission/article/main.tex` | 85,978 bytes | `d1344711d3d85ce5936574ccf54bcfbea1bf4164a0d2b6f5d25d5ecb483991bb` | stored source; freshly read and rebuilt |
| `proof_compression_submission/article/references.bib` | 6,960 bytes | `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6` | stored source; bibliography omission rejected |
| `proof_compression_submission/supplement/supplement.tex` | 46,305 bytes | `e0fe9e08c923a2946c282a3b19aa66c4c6aaa52e762639977024f538295de455` | stored source; freshly read and rebuilt |
| `supplement/compression_tables.tex` | 3,269 bytes | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` | generated input; omission build gate passed |
| `supplement/certificate_appendix.tex` | 22,405 bytes | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` | generated input; omission build gate passed |
| Article PDF | 194,574 bytes / 26 pages | `a6b91bc5d8864d1ce1a6eb352d00ecdf83712449b41fa4ad041e43a4c06e4858` | fresh rebuild byte-identical to stored PDF; all pages inspected |
| Supplement PDF | 160,272 bytes / 24 pages | `654f9150a2a22be18c651d9bd38864be2a080828dbcdad847d2b344e407ebdb2` | fresh rebuild byte-identical to stored PDF; all pages inspected |
| `PDF_BUILD_REPORT.json` | 2,102 bytes | `3e6b49cc14919ba582dc2b54d4222c16adc0bc333c5a6954c8a2f1aad3ddbee6` | payload `70394f0cb0a4b2947fb64c327431185c2fbd57df5f6c10fd1b5eecea221f0d89`; final status PASS |

All 50 rendered pages were visually checked.  All 22 article and 28 supplement
font rows are embedded.  The build logs have no fatal error, overfull box,
undefined citation/reference, or hyperref PDF-string warning; one underfull
supplement hbox is nonblocking.

## Proof-compression evidence

| Artifact/check | Status | SHA-256 or payload |
|---|---|---|
| `PROOF_COMPRESSION_RESULT.json` | stored PC-PARTIAL, zero unresolved mathematical records | file `7c485ed3f15dc74bcb9cbced60d43be7176b364502b88354e651b7e39b6dfe3f`; result payload `63a5808510a611b0bb6cf428e20a6b565d72393ec7fbbe65ed32a8b1b441f172` |
| `THEOREM_TO_TEMPLATE_CROSSWALK.json` | stored | `88aaa5dafd9be446eeefb899a1f67311269d0bfdbcfdfb810fc29f7347f2d96b` |
| Fresh compressed-release check | PASS | stdout `faa941ac0a3ed2b30ad8f66a8186607d7715a322956cdcae8cae51c448cf4981`; crosswalk payload `d2591c67eb5168b6601efa81b762e905239accd26acf69fe284f1b690de1d480` |
| Fresh old/new equivalence | PASS, 7 commands, 75.233 s internal | payload `db5ec5dde1b50382e163ca5b51a128c8506aac6e55632f76cb8474a473620b7b` |
| Fresh compression mutations | PASS, 11/11 | payload `eef0bba326d3e9dff0d26add67ec01717aa254a434f51f057333a39f21bbe075` |

## Review-owned independent evidence

| Artifact | Independence/mechanism | Result | File SHA-256 |
|---|---|---|---|
| `independent_checks/math/independent_math_checks.py` | no submitted classifier, canonicalizer, graph builder, expected ledger, or certificate reader | completion counts; whole-map identity; triangle tensor/determinants; weak graphs/tensors/rank minors; exact cherry observable, inverse, and Jacobian determinant `2464/675`; recovered parameters `(2/5,3/7,4/9,5/11)`; all PASS | `5f771569695db63a14a3a9780293be51a27b58039076078c293b120a4885192e` |
| `independent_checks/math/boundary_rational_checks.py` | `fractions.Fraction` only; no floating-point comparison or submitted domain checker | PASS on 5 `D_plus` boundary-near faces, 4 strict-CT faces, both inheritance faces, 5 strict subdivisions, all 25 face-point products, 20 surjective sections, 8 CT powers, 6 transformed bridge witnesses, and 2 simultaneous CT gluing cases; payload `a265275e83f87c0226ab9982a3d2dff1eed0559445e9b16ae3ce50e6be410688` | script `642c07bbbeb315255945696c52191e3e10a455e0b0b91c25a3d78f3e8b38b1f8`; result `6535ee1d2310a49da99729ab3fbe522af29a1ce49b35ce52cb8f7a15e168c069` |
| `independent_checks/computation/r4_independent_semantic_attack.py` | standard-library decoding/hashing; direct raw-coordinate reconstruction and explicit graph predicates; no submitted classifier or release verifier | clean package PASS; all current compressed rows also required duplicate-free canonical decoding | `41760fb53167599e5ddf0258b628c189845141839653bf635af77f6943b13b4c` |
| `r4_independent_semantic_attack_result.json` | independent result | PASS; payload `6c54197b205886afc87a284e77e838467dfb8bb4a6b3c520920249019bfe2a62` | `35e56426ca918aa806e5cee66c91e4849168d4f587115562654e67ec66de730b` |
| `r4_probe_duplicate_jsonl_attack.py` | coherently resealed compressed-ledger mutation; does not rely on stale outer checksum | submitted independent probe verifier accepted a conflicting duplicate `parent_anchor_id` in row 0 | `70fd97d2937d27f394f89cf503d69a059da3ce37e9d8e9f000a8552ca5eca28c` |
| `r4_probe_duplicate_jsonl_attack_result.json` | finding evidence | verifier exit 0/PASS; mutant ledger `3ee36f…`; valid mutated layer seal `3a8692…`; payload `6a47dd…` | `0b14d7dde85e323ed5ae4271e75f5f6f68d38a59f90e3c78931d828f552c7732` |
| `entrypoint_optimized/entrypoint_guard_matrix.json` | ten current outer/direct entry points under `-O` | all ten intended protected entry points rejected | `98ca64950a211af8eb743a6c55870b8595e48787e5a1f77ddb1f9687e47e6572` |
| Portable `verify_package.py` under `-O` and `PYTHONOPTIMIZE=1` | direct documented portable qualification | both exit 0 and print `K2P_OFFLINE_SWEEP_PACKAGE_PASS` | stdout `2e05df25a73f535d10e7c3f2bf72f12db880b73471c524468d9f85afacccbaf0` |
| `driver_semantic_mutation/false_certificate_recheck.json` | non-kernel vector substituted, local input lock coherently updated, independent pullback recheck | normal mode rejects; `-O` writes false `separated` certificate; target pullback has 5 nonzero terms | `586d0fcd1ae00121a8051bc94139aa474a05ef38ae835d840709f76239f0ffaa` |

The clean compressed ledgers were independently found canonical and
duplicate-free.  The duplicate-JSONL and optimized-driver findings are
fail-closed interface/completeness defects, not evidence of an incorrect clean
row or a theorem counterexample.

The two failed cherry-check invocations preceding the controlling PASS were
reviewer-development diagnostics only: one used system Python without SymPy;
the other exposed the reviewer’s incorrect expected fraction `15/77`, which
was corrected to `20/99`.  Neither altered or failed submission code.  Full
runtime and output hashes are retained in `EXECUTION_LEDGER.md`.

## C01–C13 producer and replay registry

This table is extracted verbatim at the path/hash level from the distributed
`proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json`
(SHA-256
`2f4c1c53981efa3bd0c7efc31813398007b71c813570726cca596e3603b52990`,
payload
`961102d2ff04d99100fc6f657cd83a02dc99b070279e24f84edfa0a961411553`).
Every listed file is in the frozen/distributed closure and was hash-checked.
Mutation artifacts are referenced by claim ID and exact source-crosswalk row
to avoid duplicating the longer mutation inventory; the last column gives its
row count.

| Claim | Exact producer artifacts | Exact replay/verifier artifacts | Mutation rows |
|---|---|---|---:|
| `C01-domain-rooting-subdivision` | `work/domain_rooting_closure/verify_domain_rooting.py` — `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b` (certificate producer/replayer) | same path/hash (exact replay) | 1 |
| `C02-quartet-tree-of-blobs` | `work/quartet_separation_closure/verify_quartet_logic.py` — `6f653169942b61d3b2c9d13ab9f3a08afc4c9dbd2bdae13a6ce0c42ee245c529` (quartet producer)<br>`work/quartet_separation_closure/verify_quartet_terminal_bindings.py` — `081512f7f9186e2aca310aaf689f85b7de4d6e810f2f5ccff018138273c0b600` (terminal-binding producer/replayer)<br>`work/adversarial_proof_review/verify_topology_direction.py` — `8fb87cb9bd0bb99efb8281780b76d20c4970d24d8c471f33e885fe17077428c2` (raw graph-direction producer) | the same three paths/hashes: exact quartet replay; 4,414,710-row terminal-binding replay; independent raw-direction replay | 5 |
| `C03-bridge-marginal-local-product` | `work/bridge_marginal_closure/verify_bridge_marginal.py` — `da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431` (certificate producer)<br>`work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py` — `a980f3c96206a1fcd8849676bfc54a773b512f2878e322d3b78ddf2a9e9cb9cb` (transport producer) | `work/adversarial_proof_review/verify_adversarial.py` — `1429bca080e6cffe591ad7455a54dbbe16db3b41a806c8a7a14d5848d4ec4380` (adversarial replay)<br>`work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` — `01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160` (graph-derived transport replay) | 5 |
| `C04-primitive-grammar-and-completion-count` | `proof_compression_submission/analysis/derive_baseline_and_universe.py` — `040876b520919780105df4eb51b8edcf17115a485c56e3d41ed1f6ec16a72204` (independent grammar/counter)<br>`work/canonicalizer_completeness/canonicalizer_audit.py` — `3df120b4e5d36e1222fc5766346e18b79623debbdaa04236cabf5132415cf3e4` (slow canonicalizer/strict relation) | `proof_compression_submission/analysis/verify_family_coverage_equivalence.py` — `980e66de5bc3b7bbd8a0508f1c89bfa925130b0565679ac2280d8adf7b7e7044` (direction-safe equivalence)<br>`work/final_theorem_release/verify_corrected_universe_independent.py` — `b42d3aed0edfab7cdf6b70c8efa1cf6c5ea32715b8eead10a7df31eb329ee9df` (independent universe replay)<br>`work/canonicalizer_completeness/verify_canonicalizer_completeness.py` — `76c24d9784a49460dff1ed2175c6b05d593f51ce404b11420096ba942397391b` (full canonicalizer replay) | 5 |
| `C05-raw-four-rank-filter` | `work/raw_ledger_audit/generate_raw_ledger.py` — `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44` (raw generator)<br>`work/rank_upper_certificates/build_rank_upper_coverage.py` — `b792efabbdf0d8a871bfb8a8526451b2f4c4e0f8209e75f654de6cc77b58d28f` (rank-coverage producer) | `work/raw_ledger_audit/verify_raw_ledger.py` — `745ece3309128b0b0a5bb824e9811be946c40bee744cd99ebdc7d709f714e371`<br>`work/rank_upper_certificates/verify_rank_upper_certificates.py` — `7cc30cc31d80d999e899c4372bc0991d057fa02e847bd8167d8e33ca4a6cb0a6`<br>`work/rank_upper_certificates/syzygy_upper.py` — `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`<br>`work/rank_upper_certificates/rank_upper_replay.json` — `c967917601f64803c96c1ba11cabc5fd3ea8d6021f9e55441c4210d9b886793d` (replay report) | 3 |
| `C06-direct-separator-families` | `proof_compression_submission/templates/derive_direct_templates.py` — `ff987bd136ac9e2fe59ae27c4e5a6344916086f8347b9928019e12d2656eb904` (body/orbit grouper)<br>`proof_compression_submission/templates/build_printed_certificate_appendix.py` — `7c366606b15661ce30f6f88f8e195f139f7d1f37e5378b79df0c19254018a0f8` (appendix producer/checker) | `package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py` — `08a188809833bc429053b01a2243542ab4a25e8b50a14409f82649e29160243a` (direct closure replay)<br>`proof_compression_submission/templates/verify_printed_certificate_appendix.py` — `79d8e7dc59c9934987d13480fab1b36212abb269b6e2a8333bf36918945dbd6c` (formula/example regression) | 4 |
| `C07-corrected-full-map-finite-universe` | `work/corrected_composite_ledgers/generate_corrected_composites.py` — `a117923e7b5cf90f0a13630fd21a6c454139f7e6e9c3c7bf84276229351a58ce`<br>`work/adversarial_proof_review/build_corrected_cycle_promotion.py` — `bd6967db370d5f1f584538136abf5461037d1c9d9ce36a5009687c05c47528d8`<br>`work/final_theorem_release/verify_full_map_reseal.py` — `3463db8199bb8a6068c732742085fbfdb3ab0722eec9fe8dd3e133dbb523aca3`<br>`work/final_theorem_release/verify_composite_reseal_diff.py` — `8806d7470910c999fc3b3d83cbb0f9785cf0ca39d8f2d9ed839d8a4564d39e2c`<br>`proof_compression_submission/analysis/verify_family_coverage_equivalence.py` — `980e66de5bc3b7bbd8a0508f1c89bfa925130b0565679ac2280d8adf7b7e7044` | `work/corrected_composite_ledgers/verify_corrected_composites_independent.py` — `67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690`<br>`work/corrected_composite_ledgers/artifacts/release_contract_replay.json` — `88f7532b9ad05e44c89ca067e4d3e2fefe95806e577d6115636c40a8890bc095`<br>`work/adversarial_proof_review/verify_corrected_cycle_promotion.py` — `01eb7c31402b3ce562f634422eed4491d9d2c499f18eee5dd6c7fd68ba3abca5`<br>`work/adversarial_proof_review/cycle_promotion_independent_verification.json` — `085f8d7b16ef3146853b6296b34bc9d994b8004a5ccc1bdfa6355dfebf79a4eb`<br>`work/final_theorem_release/verify_full_map_reseal.py` — `3463db8199bb8a6068c732742085fbfdb3ab0722eec9fe8dd3e133dbb523aca3`<br>`work/final_theorem_release/verify_composite_reseal_diff.py` — `8806d7470910c999fc3b3d83cbb0f9785cf0ca39d8f2d9ed839d8a4564d39e2c` | 7 |
| `C08-restoration-forest` | `work/restoration_sign_reclassification/build_corrected_restoration_forest.py` — `55e7196b840b98334327e81b2583ab2105a8107ee9be308781b41187c9c7de6d`<br>`proof_compression_submission/restoration/analyze_restoration_archetypes.py` — `f1142b921ce92423c5fd25d4fd5ae2872bc486f2c3839090028b4069d3f549fb` | `work/restoration_sign_reclassification/verify_corrected_restoration_forest.py` — `e4cef28f156e1c300ed7b7cc48bb1a96f3a7686d92e2c748ec8dfa156d236f9e`<br>`work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json` — `42be6b0c4d85aa58b336caebbdefd10a0af0ce4234a0482e65c7b5a68d1e6430`<br>`work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` — `01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160`<br>`proof_compression_submission/restoration/verify_restoration_archetypes.py` — `5e6eba5d2f2a941b8ece98e4a75ff784286d3d5acecf136ce0a658a74c97b0df` | 4 |
| `C09-coherent-probe-word-reconstruction` | `work/probe_coherence_corrected/build_probe_coherence_corrected.py` — `f0176e1759771a01ffa3da9e8d2b8967fc9189d3f93b30c6d06554bba9a77ddf` | `work/probe_coherence_corrected/verify_probe_coherence_corrected.py` — `3facc1b51c133aa953f4a0cba86782672c86e78990d72ef2fc2aaa16a6f2a1bd`<br>`work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py` — `9d1cdf0a219aeffb82b2f8e0d09d7cbfdbbfe28f11da1d46ff37a34d5fa4d4e8`<br>`work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` — `01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160`<br>`proof_compression_submission/probe/verify_probe_word_theorem.py` — `0ccb2c8813dbf7d060481ecc41f1318bebae813ac5eb423debda9e4f0430c28e` | 5 |
| `C10-three-port-triangle-and-genericity` | `work/final_theorem_release/no_assert_triangle_sunlet.py` — `c4a529336a0d409de30cf1c55f283e64628099424bd4191cfb7b31ec8995d7a1` | `package/original/checkpoint_2/continuation_2/verify_triangle_and_sunlet.py` — `3b6c69caf6e72818fe5d931b1c30beabb7860c0c3686d300aff998c48741ccd6` (legacy independent arithmetic)<br>`work/final_theorem_release/no_assert_triangle_sunlet.py` — `c4a529336a0d409de30cf1c55f283e64628099424bd4191cfb7b31ec8995d7a1` (promotion-grade replay) | 1 |
| `C11-global-K2P-SAME-and-reconstruction` | `work/final_theorem_release/build_release_lock.py` — `a49add912050dad8e11f16897010feae6269ff4405ae3ad019d02cf32437f683` | `work/final_theorem_release/verify_final_theorem_release.py` — `700c5d43aaf83ee504498ad61fb38f0b9df5271cc537cb24216bcc5b1d0bbb46`<br>`work/final_theorem_release/corrected_universe_independent_replay.json` — `d33a02829a0892b370f4bcee6b202e71a0b15c57222f9fb094b0aec8f5e9a7c8`<br>`work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py` — `40aed29c86fc8e6019fc9202cdd2e27225b2084a2332d7ecb99c14b33830fca1`<br>`proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json` — `5a5f62104bea1e88d725aa3cee0441c369d53905f71fe30bc20de82f4eadb35e`<br>`proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json` — `200b8f18dcd01c2f9fc4f3013b6963b3b8e8083b1acb6a591e28c6e42f7695e3` | 1 |
| `C12-strict-continuous-time-corollary` | `work/domain_rooting_closure/verify_domain_rooting.py` — `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b` | `work/bridge_marginal_closure/verify_bridge_marginal.py` — `da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431` | 1 |
| `C13-weak-class-sharpness` | `work/weak_sharpness_closure/verify_weak_sharpness.py` — `f0cab684609a89e2ab331643e15f6d516576b063f5acdff0f1cb134b5af8a3e2`<br>`proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py` — `4e764b5e6cc6a67de4381fc7c3c3994437eead134ed576004f8fe218b53e897d` | `work/weak_sharpness_audit/PROOF_AUDIT.md` — `d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa`<br>`work/weak_sharpness_audit/audit_weak_sharpness.py` — `e737fe3c0f0878c0284b0a55ebac1bfd3a7915b33278ab2916ed56bdf2200e5d`<br>`work/weak_sharpness_audit/audit_certificate.json` — `cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52`<br>`proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py` — `4de6be83448ff79b3a3677926e4fea75709ff6e8dafc6ec4baed55fa8bc969a1` | 4 |

## Independent provenance result files

| Result | SHA-256 | Principal conclusion |
|---|---|---|
| `independent_checks/provenance/archive_and_closure_audit.json` | `d0396f9a708294728f48f2c3d8ceb9e60d05a01af89880224157fbad900183e1` | archive metadata, revised manifest, 406-file recursive closure, and portable ledger exact |
| `tag_binding_audit.json` | `b68801bb5e1b1eba11bc5c7968c6952259eebff74c93c248805ae406ae52f69e` | all 491 bytes equal annotated tag object `83ffef7455ea2e43b887e12d9fb5ade5a867039f`, peeled commit `79e33706a5563d5c8620b988e27e98119da3487c` |
| `replay_telemetry_audit.json` | `6e2f485219f32ee8f8b53077ff4d06dcd12e2e750a71cc6e7a210185723118a2` | replay commit ancestry and exact 406-file/five-source equality; stored report/telemetry consistency |
| `submission_document_audit.json` | `0cb501bf747c66bd035b601e67774e57c59306365894b17aff60041414375be9` | five-source archive, PDFs, build report/logs, page/font facts consistent |
| `authority_partition_audit.json` | `bf5168e38a5f3e2ba184f0c668f6a656ba3ff9b45efb5428e003765920b43602` | historical/revoked inventory exact and non-authoritative; no crosswalk promotion |
| `evidence/provenance/zip_audit.json` | `83df2f44cede9ce3158d033133f4279d444fb35cedea7f0fb4b0044fb2b221e1` | all 491 ZIP members hashed; exact extraction; frozen-ledger comparison has the expected 85 non-frozen entries |

## Review narratives

| Review-owned report | SHA-256 | Status contributed |
|---|---|---|
| `notes/mathematical_review.md` | `f549d80633daa08c6c0d94c74c5f479fb6936ed2187036a21a5c2007a287c8ce` | hand/analytic mathematics PASS; finite lemma conditional on computation; includes the controlling exact cherry observable/inverse/Jacobian and rational boundary/CT checks indexed above |
| `notes/computational_review.md` | `5127c375df158fe7f569bb3f11cbd63726bce2e22ae6d9a27f57d36ad47f7fd8` | clean census PASS; compressed duplicate-name defect gives HOLD |
| `notes/entrypoint_optimized_audit.md` | `05bdb35f4b4ecb18782f713549ae39553bfbd6cb0aecf40d2cdf39575019f9d3` | official harness guarded; documented portable production surface fail-open under `-O` |
| `notes/provenance_reproducibility.md` | `2db62d7d98b52a6017889796c32c52c2145c2457b659b5b7141c7a88d07e4175` | archive/tag/telemetry/PDF/source provenance PASS before integration of new fail-closed findings |
| `notes/literature_scope_review.md` | `49e1c39a44edb573b9bd20c529f64615202413fabcfc7410ac7cf21b527ff33c` | 16/16 bibliography records and 21 citations checked; scope/attribution PASS; novelty search non-exhaustive |

## Archive reproducibility

Two clean-location builds produced 214,944,591-byte ZIPs with SHA-256
`51f502290434cd3415936ef69e3c5afe71438fa892d5b9e6998feecc47489278`,
exactly equal to each other and the distributed ZIP.  The disposable rebuilt
ZIP files were removed after `cmp` and hashing; their stdout/time logs remain.

## Legacy-name mapping and exact unrun disclosure

The archive intentionally does not contain the following literal legacy
filenames.  They were therefore not runnable or run *by those names*:

| Absent name | Current mapping | Fresh disposition |
|---|---|---|
| `START_HERE.md` | `output/referee/README.md`, then release README | both read |
| `setup_environment.sh` | three explicit venv/pip commands | all three exit 0 |
| `verify_handoff.py` | portable bundle check, release-lock check, quick harness | all mapped commands exit 0 |
| `test_handoff_mutations.py` | `run_release_mutations.py` | exit 0, 25/25 |
| `run_all_verifiers.py` | full harness | exit 0, 41/41 |
| `SUBMISSION_BINDING.json` | `RELEASE_LOCK.json` + `REFEREE_BUNDLE_CONTENTS.json` | both independently reconstructed |

The current README’s standalone
`build_theorem_artifact_crosswalk.py --check` command was separately run and
passed (exit 0, 0.29 s, maximum RSS 173,703,168 bytes, stdout SHA-256
`8579779f2ec3297a4ef0de28fa563aa07e720216672e3ed024c0453f91bae0a1`).
`run_corrected_universe_mutations.py --output …` was not separately invoked at
top level; the full harness invoked that same script as
`corrected_universe_cross_layer_mutations` (exit 0, 199.021098 s) and compared
its result.  The three focused output-contract scripts ran as the mandatory
preflight of `run_release_mutations.py`, not as separately logged normal-mode
top-level commands.  These nested executions are coverage distinctions, not
unrun gates.

The package also expressly does not claim a second all-family orbit partition
independent of both its atlas and canonicalizer, or a second symbolic engine
re-expanding every higher-degree polynomial body.  Those are independent-audit
boundaries, not silently passed gates.

Optional authoritative resealing/write modes were not run in the pristine
copy.  Equivalent check modes were run, and writing producers were confined
to the disposable execution copy or reviewer-owned output paths.  Those
maintenance modes are not scientific execution gates.
