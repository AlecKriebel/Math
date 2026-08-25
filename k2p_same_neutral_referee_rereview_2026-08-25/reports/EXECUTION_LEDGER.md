# Fresh execution ledger

Review date: 2026-08-25. All package paths below refer to a disposable
extraction. No submitted file was repaired. Writers were redirected to audit
storage or run in disposable copies except for the defective release-mutation
command, whose in-place write is itself preserved as evidence.

Path abbreviations:

- `A=/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25`
- `P=$A/tmp/clean_full/k2p_principal_d_plus_submission_referee`
- `P0=$A/isolated/k2p_principal_d_plus_submission_referee`
- `PY=$P/.venv/bin/python`
- `S=$A/independent_checks/provenance`
- `TMP` denotes the randomized disposable directory created by the inspected
  release harness. The harness report did not retain those random path strings;
  its exact constructors are in `verify_final_theorem_release.py`, SHA-256
  `f30cc4b26e45d0ed959786cf4504ae8974a3c3da5953a40072b8cc48bd82d95a`.

The ledger below accounts for every primary command used as scientific
evidence. Read-only exploratory commands (`rg`, `sed`, `jq`, `shasum`,
`pdffonts`, and page-image inspection) are not theorem gates. Instrumentation
(`/usr/bin/time -l`) and redirections to named audit logs are omitted where the
row displays the core argv only. A small set of subsidiary omission/optimized
invocations did not retain exact argv; those are inventoried explicitly as
command-metadata UNVERIFIED rather than reconstructed from guesswork.

## Environment

| Item | Observed value |
|---|---|
| OS | macOS 26.5.2, build 25F84 |
| Kernel / architecture | Darwin 25.5 / arm64 |
| CPU | Apple M1 Pro, 10 physical and 10 logical cores |
| Memory | 17,179,869,184 bytes |
| Python | 3.14.6, assertions enabled (`-B`, not `-O`) |
| NetworkX | 3.5 |
| SymPy | 1.14.0 |
| Tectonic | 0.16.9 |
| Poppler | 26.08.0 |

## Directly invoked commands

Peak RSS is shown when `/usr/bin/time -l` recorded it. “Output hash” means
SHA-256 of the principal report or stdout/stderr named in the row.

| ID | CWD | Recorded command or core argv, with abbreviations above | Exit | Wall / peak RSS | Output hash and result |
|---|---|---|---:|---|---|
| E01 | `$P0` | `python3 -m venv .venv` | 0 | not retained | environment created only in isolated copy |
| E02 | `$P0` | `.venv/bin/python -m pip install --upgrade pip` | 0 | not retained | stdout `718706568de9b06a27c22283e3371ff13caf160182c8064a49b6f642545ea1c7` |
| E03 | `$P0` | `.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | 0 | not retained | stdout `b8cb8888e74efb13d53a13b09a6cf6e18e4df64a873dd861491a02bfca6cf7e8` |
| E04 | `$P0` | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick --output $A/logs/release_quick_report.json` | 0 | 382.72 s / 1,342,914,560 B | 23/23 PASS; report `89ab068f59a3eafe9e556d8bfff3d9feaa3d1e03a9f9e3310b59ec33bb53525d`; stdout `b75daf70796a90f6f525e1b15bba5fecd3baed6b9bdc1ab32c799d334c021978` |
| E05 | `$P` | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --output $A/logs/release_full_report.json` | 0 | 5,466.17 s / 2,547,630,080 B | 40/40 PASS; report `7b5c7d2409db3ebf53784b7581ee4723c6aed05cd977a01f01124fa2006e7a6b`; stdout `ec8c7b5b27cc212f4ffff0ab442572b14fd632e3649c8d7ca21e4ad75a47e21b` |
| E06 | `$P0` | `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py` | **1** | 4.25 s / 99,565,568 B | **FAIL** `MUTATION_SOURCE_TREE_FINGERPRINT_DRIFT`; stdout `b947c165a7cbeab18f3dfba742f89b660e4b57d4bf828f7641878ef47108d0c9`; stderr `1813199cee48724e6498e030800c525360944040ab35868f7373da79027df782` |
| E07 | `$P` | `.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check` | 0 | 0.08 s / 33,734,656 B | stdout `288e941110a86339ae1b70239a0976229cb4bc7091650be624456f236f95226c` |
| E08 | `$P` | `.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check` | 0 | 0.37 s / 38,420,480 B | stdout `4e895b23a9ff06c7a6d77f5149a0bc33125713f194d7cfbb2cfbb61d8c70dcce`; summary/certificate mutations only |
| E09 | `$P` | `.venv/bin/python -B proof_compression_submission/test_clean_full_replay_telemetry.py` | 0 | 4.42 s / 27,181,056 B | 9 tests PASS; stderr `b470e90ea36649eda232609f9b7bc7b0a88ddf4384cfccef473b7fdb317c9fdf` |
| E10 | `$P` | `.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check` | 0 | 72.80 s / 294,273,024 B | stdout `bfe3612b031ac0cc1d17acfbae060f6ff8cc20cccaec74d041a899dc7482b7a1` |
| E11 | `$P` | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check` | 0 | 10.09 s / 491,290,624 B | stdout `03dede61ff3ace480e7996cbcced6c9b46a2aef1e22e6700090b21a59ea4a29d`; 223/223 locked files matched after full replay |
| E12 | `$P` | `.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py --check` | 0 | 0.10 s / 38,797,312 B | stdout `17326ba2eabc8287bf1a5738a3bb104bada6095841c50ff77be2c07599e27f68` |
| E13 | `$P` | `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.27 s / 158,875,648 B | stdout `ed36872368a68a59032501458efc0f46488f2e28784f4db5b2663b85d44c140f` |
| E14 | `$P` | `.venv/bin/python -B work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family raw4 --report $A/logs/raw4_composite_independent_report.json` | 0 | 230.39 s / 335,036,416 B | 405,216 rows PASS; report `1ae9505c553d174d36bc8c3701fea3b9b7f2cfe5059d4a1fc58bd8571ab4e348`; stdout `fb6b5ca3d708bc94fefb4b9011451b57c0a647429b14055b801b4ca0ccc6da7c` |
| E15 | `$P` | `.venv/bin/python -B work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family theta2 --report $A/logs/theta2_composite_independent_report.json` | 0 | 333.37 s / 308,838,400 B | 2,946,240 rows PASS; report `937cde59ff65317ef003e4d8728a95b40a7849f9c673c80b69d5e3c61273adca`; stdout `2e8737e2a527749dd3cb56116efc9a989d1d9c359c552616e7c8cab270ea48bd` |
| E16 | `$A` | `$P0/.venv/bin/python -B independent_checks/math/fresh_exact_checks.py` | 0 | 1.19 s / 84,934,656 B | report `aedc640f928ecd0b2336289c19a743bbf09b88a0ca55345e6505d8e6ec6f8a1f` |
| E17 | `$A` | `$P0/.venv/bin/python -B independent_checks/math/primitive_core_enumeration.py` | 0 | 0.08 s / 20,086,784 B | output `eb6ba17f6a46a9f1d7125086098f66432e944af36c76ebddf6e42637918fca96` |
| E18 | `$A` | `$P0/.venv/bin/python -B independent_checks/math/direct_certificate_check.py` | 0 | 0.34 s / 64,897,024 B | output `ec59f819aa93536e20c8e06f53b92358e7f8f63faae0a889e7762f3708c14994` |
| E19 | `$A` | `/usr/bin/time -l python3 -B independent_checks/computation/independent_primitive_and_census.py --project isolated/k2p_principal_d_plus_submission_referee --output independent_checks/computation/independent_primitive_and_census_report.json` | 0 | 26.59 s / 159,891,456 B | report `7fe83d590f90cdf03dc0c88c7eff72902b040fb9019b825f254538a50cd1613d` |
| E20 | `$A` | `/usr/bin/time -l $P0/.venv/bin/python -B independent_checks/computation/composite_mutations/run_real_composite_mutations.py --project isolated/k2p_principal_d_plus_submission_referee --output-root independent_checks/computation/composite_mutations/final_cases` | 0 | 413.97 s / 1,104,183,296 B | 12/12 intended semantic rejections; report `8bf09b30f9be51ebb48b8523cafe4eae767f0972f9c32cd4682c88d23c2d4086` |
| E21 | `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_archive.py --project isolated/k2p_principal_d_plus_submission_referee --archive source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip --checksum source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip.sha256 --result independent_checks/provenance/archive_audit.json --rebuild independent_checks/provenance/rebuilt_archives/rebuild_1.zip --rebuild independent_checks/provenance/rebuilt_archives/rebuild_2.zip` | 0 | 42.02 s / 777,011,200 B | report `fd7ae2e9e4dc9424221669228b43c9c7b7b7c61d59106c4c01bce64ee0f8a49d`; both ZIPs byte-identical |
| E22 | `$P0` | `/usr/bin/time -l .venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.45 s / 229,507,072 B | stdout `3bdc629a55de599eda014ed5fc8b0cf033692ad9bd27da6175cd97ebed5fcb91` |
| E23 | `$P0` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.44 s / 231,768,064 B | stdout `c5118bede592ee62ecdcbaf4f68684ff53012afb942b0179030e2ab9290e2b4b` |
| E24 | `$P0` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 0.51 s / 292,225,024 B | stdout `c5118bede592ee62ecdcbaf4f68684ff53012afb942b0179030e2ab9290e2b4b` |
| E25 | `$P0` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 6.69 s / 604,422,144 B | 27/27 rejected; stdout `5567ad8ff3ef51d275390b8e859f733b8bc9b92666446286b5283fe83287de89` |
| E26 | `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_git_binding.py --repo /Users/alec/Documents/Math --project isolated/k2p_principal_d_plus_submission_referee --project-in-repo k2p_level2_identifiability_closure --revision 1877985d20132fb186d21a5985e8c5f760a656af --revision k2p-same-biorxiv-v1.0.0 --result independent_checks/provenance/git_binding_audit.json` | 0 | 3.12 s / 791,429,120 B | report `99d587fefd1df1a660e9872bec95b50eb69c91d856085bcdb8981acb68442cff` |
| E27 | `$S/pdf_rebuild/project` | `/usr/bin/time -l python3 -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 19.44 s / 255,836,160 B | stdout `33e3306416c0279a999db2c1e244318ea5d68df0e3232ce6754af63940e9a177` |
| E28 | `$S/pdf_rebuild/direct/article` | `/usr/bin/time -l env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates main.tex` | 0 | 4.02 s / 252,854,272 B | PDF `2c4433d53c33c337d4ed028c2843cf0b5631263d7bf4a0a42106727985daa3a8` |
| E29 | `$S/pdf_rebuild/direct/supplement` | `/usr/bin/time -l env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates supplement.tex` | 0 | 3.51 s / 250,593,280 B | PDF `9b10797d7503e6940d80a95bc90302b3b32a9ea34cb9f63a54bee3f12f3c06e1` |
| E30 | `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_artifact_consistency.py --project independent_checks/provenance/pristine_archive_extract/k2p_principal_d_plus_submission_referee --result independent_checks/provenance/artifact_consistency_audit.json` | 0 | 0.51 s / 162,529,280 B | 19/19 PASS; report `2f35d56cc27c789a75b48e2e48bf42e4be0bdc59ee40ca017513656a5aac5396` |
| E31 | `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_dependency_binding.py --project isolated/k2p_principal_d_plus_submission_referee --git-audit independent_checks/provenance/git_binding_audit.json --interpreter isolated/k2p_principal_d_plus_submission_referee/.venv/bin/python --result independent_checks/provenance/dependency_binding_audit.json` | 0 | 0.84 s / 77,463,552 B | report `9a4ea338aba4654c167f5f494ebfc8722f4d37822efdcbdb478ae573af61a5f4` |
| E32 | `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/reproduce_quartet_path_dependence.py --archive source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip --interpreter isolated/k2p_principal_d_plus_submission_referee/.venv/bin/python --project independent_checks/provenance/quartet_path_reproducer/extraction_alpha --project independent_checks/provenance/quartet_path_reproducer/extraction_beta_with_different_length --log-dir independent_checks/provenance/logs --result independent_checks/provenance/quartet_path_dependence_reproducer.json` | 0 | 0.63 s driver; children 3.49/3.51 s | path dependence confirmed; report `13c27197e78b7c260e4d6e964a5bbdd2a56fc8af5433d0b1aa1ea3b596e03bb7` |
| E33 | `$S/pristine_archive_extract/k2p_principal_d_plus_submission_referee` | `/usr/bin/time -l $P0/.venv/bin/python -B work/final_theorem_release/run_release_mutations.py` | **1** | 3.02 s / 99,418,112 B | same intended reproducer FAIL; stdout `b947c165a7cbeab18f3dfba742f89b660e4b57d4bf828f7641878ef47108d0c9`; stderr/time `5c80e5c76b52168e02752ba191f6d4e1db32d153c42664392b5a8db922c67c6c` |
| E34 | `$P0` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/test_clean_full_replay_telemetry.py` | 0 | 4.61 s / 27,394,048 B | independent duplicate 9-test run PASS; stderr/time `67e12274ea10cf470288b13e1f5dc325a08673dacca28e484215e86b125831db` |
| E35 | `$S/pdf_rebuild/omissions/missing_compression_table/supplement` | core `tectonic supplement.tex`; exact wrapper/remaining argv not retained | 1 | 2.48 s / 216,776,704 B | intended missing `compression_tables.tex`; stdout `0a6161b17697bef0fe63029b6fb97254c30e75f8fa3dd33206a614f3077f84e3`; stderr `c45468c04331bfae0306413ed0798b337a6643a763549425f3119cec9f5a6f5d` |
| E36 | `$S/pdf_rebuild/omissions/missing_certificate_appendix/supplement` | core `tectonic supplement.tex`; exact wrapper/remaining argv not retained | 1 | 0.91 s / 216,547,328 B | intended missing `certificate_appendix.tex`; stdout `8a7697e69297f0a5b5b8868c72de130422c77617dc9befe9532e0c7d95f3e241`; stderr `ad9f02229491f59cb3f89e0156c00072b16a68df860ade6c7134bdc2be280c80` |
| E37 | `$S/pdf_rebuild/omissions/missing_bibliography/article` | core `tectonic main.tex`; exact wrapper/remaining argv not retained | 0 | 3.39 s / 253,952,000 B | BibTeX warning, demonstrating raw Tectonic alone is not the bibliography gate; stdout `e27f14c38b7b798e5eb08b045aad12470962e0bb9e06c7eff66c11ca4a43a67a`; stderr `2c95d4262cd65186a62dff5c0f34b3ac2c4da65a7c933558d2b34729ab773183` |
| E38 | `$A` | `python3 -B independent_checks/provenance/make_manifest_mutations.py --source isolated/k2p_principal_d_plus_submission_referee/proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json --output-dir independent_checks/provenance/manifest_mutations` | 0 | not retained | four coherently resealed mutants created; stdout `08c467b491d79301a0fa9182f1a307ac781a9a3e281085861a40e31dae210dc9` |
| E39 | `$P0` | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest $S/manifest_mutations/omit_bibliography.json` | 1 | 0.64 s / 180,977,664 B | intended missing bibliography; stderr/time `0f1b99901cf7ca0ab8dd39dc9f706831192453a33b25775ec08a93c2e8a27cba` |
| E40 | `$P0` | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest $S/manifest_mutations/omit_portable_ledger.json` | 1 | 0.61 s / 202,342,400 B | intended missing content ledger; stderr/time `d28ec9453b00031063106996e786ed16bf86a89cdc882edbd77bf0a2016c32de` |
| E41 | `$P0` | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest $S/manifest_mutations/stale_article_pdf.json` | 1 | 0.57 s / 209,125,376 B | intended stale article digest; stderr/time `21e583cb923cdf972fbddb9c058ff3534b4b2449af582c3fb19784e8524eed19` |
| E42 | `$P0` | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest $S/manifest_mutations/stale_full_replay.json` | 1 | 0.54 s / 196,231,168 B | intended stale replay digest; stderr/time `ef6472b7453494af53b295cda4a125a5c56f9c51ef4cfe818ff5b70cf0480a7b` |
| E43 | `$P0` | core `.venv/bin/python -O proof_compression_submission/crosswalk/check_revised_referee_bundle.py`; exact remaining argv not retained | 1 | 0.04 s / 23,527,424 B | intended optimized-mode rejection; stderr/time `fc1e9597addf8dbec954ecae385de968a6ce134042224a75561fc849c2f9cc30` |
| E44 | disposable PDF project | core `python3 -O proof_compression_submission/build_submission_pdfs.py`; exact remaining argv not retained | 1 | 0.05 s / 23,855,104 B | intended optimized-mode rejection; stderr/time `32d1ade153dbe7f0e06543bc9fbd0833fddba721ba8d0b9bab6853b15e793d86` |
| E45 | disposable telemetry project | core `python3 -O proof_compression_submission/build_clean_full_replay_telemetry.py`; exact remaining argv not retained | 1 | 0.04 s / 23,543,808 B | intended optimized-mode rejection; stderr/time `7799ac1117bd4a2e1013f3ca0a3d7b0dadeabbb9ee18a461978cabaa2eee0016` |

Omission tests were additionally run from disposable five-source PDF trees.
Removing `compression_tables.tex` and `certificate_appendix.tex` made Tectonic
exit 1 at the named missing file; raw Tectonic without the bibliography exited
0 with a BibTeX warning, while a coherently resealed outer manifest without
`references.bib` was rejected at the intended missing-path check. Exact hashes
and resource figures are in `notes/provenance_reproducibility.md` §PDF rebuild.

## Fresh full-suite child ledger

The exact umbrella invocation is E05. It constructed and invoked each child
below once. All 40 statuses are fresh; none is copied from the stored replay.
Random `TMP` path components were not serialized, so the table records the
logical name plus output hashes rather than pretending to retain nonexistent
absolute argv. The normalized argv constructors are at
`verify_final_theorem_release.py:52-1011`; quick children are at lines
`505-711`, full-only children at lines `712-1011`. Individual child peak RSS
was not recorded; the E05 peak is the available measurement.

| # | Layer | Status / child exit | Seconds | stdout SHA-256 | stderr SHA-256 |
|---:|---|---|---:|---|---|
| 1 | `promotion_manuscript_guard` | PASS / 0 | 0.292038 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `full_map_domain_reseal` | PASS / 0 | 0.104281 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `corrected_universe_independent_replay` | PASS / 0 | 9.791420 | `145f5add52b6d2692f3546b48bf122a1b82fa2477f1eaade1726f06186d94c9f` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `three_port_no_assert` | PASS / 0 | 0.314900 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `domain_rooting` | PASS / 0 | 0.058649 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 6 | `quartet_sign_logic` | PASS / 0 | 1.081811 | `288d1cd435c47a541f8a368ca3f5b5e4a4b1137cbb5f0f01d996b700df2eeb4e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 7 | `quartet_terminal_bindings` | PASS / 0 | 33.544317 | `77b343bdee5718bec7a6c3e7d0c832bfe0ec06df31661efd358440bcb795fa29` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 8 | `topology_direction_structural_provenance` | PASS / 0 | 13.727806 | `59511e1c15b842829c98a531d6f9ca8079e3be9e729f2235df5b01f40e1063b9` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 9 | `canonicalizer_completeness_structural` | PASS / 0 | 0.187295 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 10 | `graph_derived_parameter_transports_structural` | PASS / 0 | 26.486776 | `dee36148bc1457950a06626a5bda9ffcadeb2815d8d2d054cbedb87301888117` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 11 | `bridge_marginal_gluing` | PASS / 0 | 0.053222 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 12 | `analytic_adversarial_audit` | PASS / 0 | 0.232722 | `8c7051ca698239a0deaa464b4741d800e9cfa7a6142ea784d741f9c7c882e8bb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 13 | `global_component_scale_audit` | PASS / 0 | 0.147406 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 14 | `raw4_corrected_overlay_independent` | PASS / 0 | 84.130647 | `f56f98ec7fd75f760f17cb22f6e8d5712d1b35611f9ca8e1f7add5f44928f557` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| 15 | `theta2_full_map_independent` | PASS / 0 | 44.338287 | `b2e3b2bb1fc20cca7330c51f4a702778af7bda9cef64ed4d53bf3917cc5abbd8` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 16 | `four_port_raw_structural_provenance` | PASS / 0 | 1.470809 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 17 | `four_port_direct36` | PASS / 0 | 13.618133 | `edd75a644d6e97b5bf627364ce6c6002936a83d28ab4a731095f7cc5867a59fc` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 18 | `theta2_structural_provenance` | PASS / 0 | 10.603933 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 19 | `cycle_three_port_structural_provenance` | PASS / 0 | 104.363563 | `4468b3cfb464fa0b671d2e85d46b0dad34bfd49911671e7d8849056e67b85764` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 20 | `corrected_probe_independent_streaming_replay` | PASS / 0 | 16.250745 | `d1a38229443c0e9264006566b4b35b9d8379099942f069c23826ca2a4fdc01a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 21 | `corrected_probe_site_transport_partition` | PASS / 0 | 4.551172 | `5133b897d38244c39ce2078ec92b898378198421cec2779c5f6b0d53e3cbd8aa` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 22 | `weak_sharpness_primary` | PASS / 0 | 0.148404 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 23 | `weak_sharpness_independent` | PASS / 0 | 0.166278 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 24 | `canonicalizer_completeness_full` | PASS / 0 | 100.115231 | `dde7a6df548d407df5cedb2810549aac0711269718ba203c9ddbd45461675188` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 25 | `graph_derived_parameter_transports_full` | PASS / 0 | 296.095941 | `4515e9e9f3d49e88f1b3c349a39680607834657ac36eb32482d34c2f0060dfe7` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 26 | `corrected_universe_cross_layer_mutations` | PASS / 0 | 191.169428 | `5d2f402530eab01d8c50a9f625bd0041701accaa63130a8a2361fa808eb590f5` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 27 | `raw4_full_map_Ti_truth` | PASS / 0 | 18.935887 | `ec5d6f372abbefabcb41bdb042503e88238325bb4f71cb1850823d55057d684a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 28 | `theta2_full_map_Ti_truth` | PASS / 0 | 70.556143 | `fe586c75afe67b879a0c2f96d9520417a72572794b4f89ff337e7951ce1194e2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 29 | `composite_domain_reseal_diff` | PASS / 0 | 15.364630 | `7dc2a9797f79c0f4796b6a85e7389f8a3f0cac8149dde347de1015e05bc94cf0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 30 | `four_port_exact_rank_staged_atlas_omission_mutation` | PASS / expected nonzero | 0.296121 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `93ad7c1ca85ffa49f1c3e8ac487cfdbc567c41fcbea030fa22d3bc00196e9a08` |
| 31 | `four_port_exact_rank_import_preflight` | PASS / 0 | 0.328006 | `c2314174ac47759fada9da52ed3e430f3c428404324e819427e94e48ab5cd268` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 32 | `four_port_exact_rank_full` | PASS / 0 | 117.163632 | `04c346affe668b0d917b8233628d62a1a855edbb6d8bad182c34aee3770e6b5f` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 33 | `raw4_corrected_overlay_full_regeneration` | PASS / 0 | 59.123858 | `68ed4609b78c6c097a5e7f36d587767ba82e6ef6f7cf3f76706b43188689ba3b` | `de1f579aafe4aa7f4d84e6f47f6b6ca9aba263df850de2b6839abc89018dfb8c` |
| 34 | `four_port_raw_full_regeneration_provenance` | PASS / 0 | 304.989545 | `8eb91f720fe064d3007c5f2f4a65295b921c068285b1fad9db3d3710ae3f55c6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 35 | `four_port_direct36_full` | PASS / 0 | 106.380986 | `f7b6acf61412a72457412b9961d962ac2e5c7217700ef229e421b3a0f84f5701` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 36 | `theta2_full_regeneration_provenance` | PASS / 0 | 471.029543 | `82c6917c4503a2cb7d3c42988100a58731dff13c8972a45b27ffbb5226bbd783` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 37 | `corrected_probe_full_primitive_regeneration` | PASS / 0 | 2907.058666 | `9f8e98a4a105b9d8bdf6a9f0221856732d5778c83bf7ced6e0f76390ba0f1300` | `9fbe7bcdb1f9ba961666c6d5f974699e40664387ccd5d90dd9fbbe4953446c8e` |
| 38 | `corrected_probe_full_independent_replay` | PASS / 0 | 16.768294 | `d1a38229443c0e9264006566b4b35b9d8379099942f069c23826ca2a4fdc01a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 39 | `corrected_probe_full_site_transport_partition` | PASS / 0 | 4.777194 | `5133b897d38244c39ce2078ec92b898378198421cec2779c5f6b0d53e3cbd8aa` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 40 | `corrected_probe_independent_primitive_graph_full` | PASS / 0 | 409.836254 | `cac286ee25754fb7ec694cda9de6763f82b347582a33b74fb3cd6a86b3228cb8` | `cbc56ffd93ed354a5cd9adfa22ebe130b83db6b8822b4fc1adc29c66e71e7602` |

The child elapsed sum need not equal the umbrella wall time because several
children run internal parallel work and the harness also performs byte/logical
comparisons. The report's internal elapsed time is 5,465.840630 s.

## Legacy gates not runnable from this revised package

The following prior-protocol entry points are absent from the 480-member ZIP
and therefore were not silently mapped to current PASS commands:

| Requested legacy gate | Status | Current-package observation |
|---|---|---|
| `START_HERE.md` | UNVERIFIED / absent | current entry is `output/referee/README.md` |
| `python3 -B verify_handoff.py` | UNVERIFIED / absent | outer bundle checker is E24 |
| `python3 -B test_handoff_mutations.py` | UNVERIFIED / absent | current crosswalk mutation suite is E25; final release mutation gate E06 fails |
| `./setup_environment.sh` | UNVERIFIED / absent | environment was constructed explicitly in E01–E03 |
| `run_all_verifiers.py --quick` | UNVERIFIED / absent | current release quick gate is E04 |
| `run_all_verifiers.py --full` | UNVERIFIED / absent | current release full gate is E05 |
| `SUBMISSION_BINDING.json` five-dependency audit | UNVERIFIED / superseded | current manifest v2 binds three supplemental dependencies, all checked in E31 |

These absences are a protocol/entry-point incompatibility, not evidence that
the corresponding current theorem layers failed.
