# Consolidated execution ledger

This ledger records the requested package commands and every substantive
producer, verifier, build, replay, and falsification invocation whose exact
command form was retained. Any invocation not retained exactly is identified
as such rather than reconstructed from memory. Read-only
shell inspections (`rg`, `sed`, `jq`, `shasum`, process inspection) are not
scientific gates and are not enumerated as executions. The exact absolute
`argv`, working directory, per-stage log name, return code, runtime and log
hash for the submitted harness are preserved in the bound JSON ledgers below.

## Bound machine-readable ledgers

| Ledger | Scope | SHA-256 |
|---|---|---|
| `reports/provenance/execution_ledger.json` | integrity, archives, builds, omissions, cross-bindings, optimized-mode and PDF checks | `8001f09b7f3952ce96d55707fd8889cee77c868c9d4b8acbd75461dcc7c9dd80` |
| `logs/raw/quick-20260824T045021Z/EXECUTION_LEDGER.json` | exact `argv` and results for all 21 quick stages | `76236eebb4900c2aa3b616470d5a15fd9de9228c3fe0a5cdc43bd472bc9ef2cd` |
| `reports/FULL_EXECUTION_LEDGER.json` | exact `argv` and results for all 22 full stages | `7146e52b0708ba7f459d27a9125203a973aab614668486eb985c908f16bf64cf` |

Environment: macOS 26.5.2 / Darwin 25.5.0, arm64 Apple M1 Pro, 10 logical
CPUs, 17,179,869,184 B physical memory; Python 3.14.6, NetworkX 3.5, SymPy
1.14.0, Tectonic 0.16.9, Poppler 26.08.0. Python package gates used `-B` and
explicitly rejected optimized mode.

## Required top-level commands

| Exact command | CWD | Exit | Wall | Peak RSS | Result/binding |
|---|---|---:|---:|---:|---|
| `python3 -B verify_handoff.py` | isolated handoff | 0 | 0.90 s | 283,279,360 B | 492 outer; 374 frozen + 73 submission inner rows |
| `python3 -B test_handoff_mutations.py` | isolated handoff | 0 | 2.63 s | 280,723,456 B | five outer mutations and optimized mode rejected |
| `./setup_environment.sh` | isolated handoff | 0 | not retained | not retained | first required invocation succeeded; environment then moved aside for a clean repeat |
| `./setup_environment.sh` | isolated handoff | 0 | 10.33 s | 165,773,312 B | clean environment: Python 3.14.6, NetworkX 3.5, SymPy 1.14.0 |
| `/usr/bin/time -l materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --quick` | isolated handoff | 0 | 778.96 s | 1,460,994,048 B | 21/21; ledger `76236eebb4900c2aa3b616470d5a15fd9de9228c3fe0a5cdc43bd472bc9ef2cd` |
| `/usr/bin/time -l materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --full` | isolated handoff | 0 | 5,684.81 s | 2,034,221,056 B | 22/22; ledger `7146e52b0708ba7f459d27a9125203a973aab614668486eb985c908f16bf64cf` |

## Quick harness: all 21 exact stage commands

`HANDOFF/` below denotes the isolated handoff root; all other paths are
relative to the computational project root. Each output binding is the full
SHA-256 of that stage's combined log.

| # | Stage / exact relative `argv` | Exit | Wall s | Log SHA-256 |
|---:|---|---:|---:|---|
| 1 | `outer_handoff_integrity` — `.venv/bin/python -B HANDOFF/verify_handoff.py` | 0 | 1.200696 | `20d6179cedc60f27d25cc25123d6d57783e5cdd9aa3445b18e8bfd5d6dfc2239` |
| 2 | `outer_handoff_mutations` — `.venv/bin/python -B HANDOFF/test_handoff_mutations.py` | 0 | 2.200118 | `91e339c5c56a0933000bbaee7ce43faccd330f93c9ba9555e49a7374da428e1b` |
| 3 | `five_source_manuscript_build` — `.venv/bin/python -B HANDOFF/check_manuscript_build.py` | 0 | 12.617060 | `dc7b81e4e2ba6c09ace4f45e53def80193e9fec96f6370c397b23a53a7183b49` |
| 4 | `article_static_audit` — `.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py` | 0 | 0.048410 | `91ff21d73983c08c5e56b4d46936c45db55b5caa26e2b87a4142d5e6f452ebec` |
| 5 | `theorem_artifact_crosswalk` — `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.216289 | `78ed41fc89e37aadba26d4df271a200ff10023e5d8a285f3cd9125023f11db4a` |
| 6 | `revised_bundle_primary` — `.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.672103 | `184d26d639c0ae130b772c0b82ed7ea012462eb77d189ef7922905d7f0cb5d3e` |
| 7 | `revised_bundle_independent` — `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 0.479713 | `184d26d639c0ae130b772c0b82ed7ea012462eb77d189ef7922905d7f0cb5d3e` |
| 8 | `revised_bundle_mutations` — `.venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 3.612642 | `c7a39b234015db4e768c6c29645b2db01854dd773926269afe233e2ea2a30ec8` |
| 9 | `compressed_release` — `.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check` | 0 | 0.079683 | `c7c386ac05fc07917ad9f426517a95c0a9c9acf142944f5e4453e35e434fd097` |
| 10 | `old_new_equivalence` — `.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check` | 0 | 75.017184 | `1235688ff25f25bee8131beb33d4415dd9ae6d082f1c888d70ccf58bd222e6dc` |
| 11 | `compression_mutations` — `.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check` | 0 | 0.378367 | `5073bef9e6b533c6045eb91c6b319a78ce95a5c1143f6b43e40877424a569575` |
| 12 | `family_coverage` — `.venv/bin/python -B proof_compression_submission/analysis/verify_family_coverage_equivalence.py --check` | 0 | 52.970895 | `65fc241b21530b35643b435177340adf2df56ead8b130d8765fe0b77f33ca936` |
| 13 | `printed_appendix` — `.venv/bin/python -B proof_compression_submission/templates/verify_printed_certificate_appendix.py` | 0 | 4.213066 | `f9e4055cbed58fa8aef606155006aed29367fb592b9e4f027eb28ca78a31a7b8` |
| 14 | `printed_appendix_mutations` — `.venv/bin/python -B proof_compression_submission/templates/test_printed_certificate_appendix_mutations.py` | 0 | 16.661608 | `e93cd4ccf51e5c4a2fcb6fb3cb34386ec42b7f272b3e3e63e6bfb43c7c7d9d3a` |
| 15 | `restoration_archetypes` — `.venv/bin/python -B proof_compression_submission/restoration/verify_restoration_archetypes.py --check` | 0 | 1.889020 | `6b04d764eefb26c5996cefcdf2cd30ff76e145eb99edbf8fd3641baf96f23673` |
| 16 | `probe_word_theorem` — `.venv/bin/python -B proof_compression_submission/probe/verify_probe_word_theorem.py --check` | 0 | 13.598143 | `448fe21601314ed67705da883b2c07f4b9ea7e0b8ac1be22a472ac2699a2c707` |
| 17 | `weak_sharpness_crosswalk` — `.venv/bin/python -B proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py` | 0 | 0.158058 | `5cb48aebf2c432c53af31b1c5555d23fbebe29b703c808c41bd7352a69035a7b` |
| 18 | `weak_sharpness_mutations` — `.venv/bin/python -B proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py` | 0 | 0.892480 | `ff1ccb2c233a152c8f490803a7ae01fafa49d0c16c84c977b323e7d600389bf4` |
| 19 | `release_lock` — `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 10.178362 | `39c57fbf7829e70cabc8016bf891725d9b8fe1a2da31dcd9ab4dcf513cc5ccfd` |
| 20 | `final_theorem_quick` — `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick --timeout-seconds 7200` | 0 | 321.007619 | `28cbca4059deb3a43f1d8265cfefafd73164487a678f3d82ee49deb77faea492` |
| 21 | `release_mutations` — `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --timeout-seconds 7200` | 0 | 260.436709 | `3a16770932344e955d634ecb18d3dc10c64ed8990574badaa134d2adaf2385be` |

The stage-20 log contains all 20 nested theorem-layer command names with
individual return codes, runtimes and stdout/stderr hashes; its binding is
given above. Sixteen layer values are reproduced in the theorem-layer
registry. The remaining four are: `promotion_manuscript_guard`, exit 0,
0.278211 s, stdout
`8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c`;
`full_map_domain_reseal`, exit 0, 0.098934 s, stdout
`7680711b434bd93bc7a001995225259f3e8e855a4b304dc2edfce648be41a139`;
`four_port_raw_structural_provenance`, exit 0, 1.473628 s, stdout
`d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706`;
and `theta2_structural_provenance`, exit 0, 10.947466 s, stdout
`0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4`.

## Full harness: all 22 stage commands

Stages 1–21 use the same exact `argv` as the table above and are recorded
again, with fresh runtimes and log hashes, in the full ledger. Stage 22 is:

| # | Stage / exact relative `argv` | Exit | Wall s | Log SHA-256 |
|---:|---|---:|---:|---|
| 22 | `final_theorem_full_primitive_regeneration` — `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --timeout-seconds 7200` | 0 | 4,911.443992 | `ba6a7f291fab27c5772cd15e9ceadfcf5fd36e751cd017635f901128c085ea92` |

## Independent and fresh falsification commands

All were run from the audit root or a disposable project copy; none edited the
isolated handoff. `PROJECT` denotes
`isolated_handoff/materials/k2p_principal_d_plus_submission_referee`.

| Exact command / check | Exit | Wall | Peak RSS | Output SHA-256 |
|---|---:|---:|---:|---|
| `python3 -B scripts/computational/check_quartet_coordinate_semantics.py --project PROJECT --output outputs/computational/quartet_coordinate_audit.json` | 0 | 0.43 s | 81,543,168 B | `c6517e0659df6a13a970e94af6b238dec02afb95e417f61bd06ebaf94b649017` |
| `python3 -B scripts/computational/test_quartet_gate_blindness.py --project PROJECT --output outputs/computational/quartet_gate_mutation` | 0 | 0.13 s | 24,510,464 B | `72a033e22826014cf260ae7e0d9766eb5feaab8406cf05fd2f1437dd9fbc76c0` |
| `python3 -B scripts/computational/independent_finite_census_audit.py --project PROJECT --output outputs/computational/independent_finite_census_audit.json` | 0 | 30.45 s | 172,212,224 B | `8f38e03b8caedabfaf738fd084a21ed73ec69efed33188bc8de593ce51672319` |
| `python3 -B scripts/computational/independent_graph_relation_audit.py --project PROJECT --primitive-engine scripts/computational/independent_finite_census_audit.py --output outputs/computational/independent_graph_relation_audit.json` | 0 | 6.19 s | 125,763,584 B | `a431ac1627b00dce9808333ca69037e603bc60e74d52224fdf41f0dd279f194e` |
| `python3 -B scripts/computational/independent_rank_replay.py --project PROJECT --output outputs/computational/independent_rank_replay.json` | 0 | 0.22 s | 52,330,496 B | `647b330b985fd635dce772162e4686fea092f59cd8f638d9ae79a3d1866a6370` |
| `.venv/bin/python -B work/weak_sharpness_audit/audit_weak_sharpness.py` in disposable copy | 0 | 0.25 s | 43,302,912 B | `cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52` |
| `.venv/bin/python -B work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py` in disposable copy | 0 | 66.46 s | 569,540,608 B | `79645c56cc0b4689eafcd7abc5f78f7854dac694e32a5915c905f557e7f1e6c0` |
| `.venv/bin/python -B work/probe_coherence_corrected/run_probe_coherence_mutations.py` in disposable copy | 0 | 172.97 s | 72,531,968 B | `517138a25e210faa33caaef2dec6ae6b9a4b27ec5b61c268f4589181a86541b5` |
| `.venv/bin/python -B work/adversarial_proof_review/test_mutations.py` in disposable copy | 0 | 0.06 s | 26,116,096 B | `390976c38c6a1e00ca2490d5ef341f17cc9a13e72892dcb27a1d19cea315d172` |
| `python3 -B scripts/mathematical/verify_quartet_convention_independent.py --output outputs/mathematical/quartet_convention_independent.json` | 0 | about 0.39 s | not retained | `07af30a348f67a1449044ef5f2024f80e833b9cc682698ccd52969fe39bcc9bf` |
| `python3 -B scripts/mathematical/verify_triangle_germ_independent.py --output outputs/mathematical/triangle_germ_independent.json` | 0 | about 0.36 s | not retained | `4801dabb3f602761da9450560e9baae62c9061973c3365fafb809a9d17008e88` |
| `python3 -B scripts/mathematical/verify_weak_sharpness_independent.py --output outputs/mathematical/weak_sharpness_independent.json` | 0 | about 0.57 s | not retained | `a18d67fd9858d217578df413714f3b9e9da88e0f39635f37003574806a3319d3` |

## Provenance/build/archive command ledger

The provenance JSON bound at the top records 29 command/event entries with
exact commands where retained, working directories, exit statuses, retained
runtimes, peak RSS where available, and output hashes. A few multi-command PDF
render comparisons and archive/Git retention searches are recorded as explicit
command lists or prose rather than a single exact `argv`. The ledger includes
two clean archive
rebuilds, independent ledger/archive audits, clean and fixed-epoch article and
supplement builds, two generated-input omissions, physical and crosswalk
bibliography omissions, artifact cross-binding, final integrity/manifest
checks, PDF render/font checks, historical/current literature-PDF comparison,
and optimized-mode checks. The full details are not duplicated here because
the complete machine-readable ledger is itself SHA-bound above.

## Reviewer process events and command errors

- The initial `./setup_environment.sh` succeeded, but its wrapper timing was
  not retained; a clean repeated invocation is fully measured above.
- `python3 -B verify_handoff.py` was once invoked from the audit root rather
  than the isolated handoff and exited 2 because the script path was absent.
  This was a reviewer working-directory error, not a package result.
- A reviewer-generated PNG temporarily produced the intended 493-vs-492
  outer-manifest failure. It was moved recoverably outside the isolated copy;
  final verifier, manifest `--check`, and independent-ledger commands all pass.
- The full suite was launched once. No long-running verifier was reinvoked
  while it was running. It completed 22/22 PASS in 5,684.81 s with maximum
  resident set size 2,034,221,056 B.
