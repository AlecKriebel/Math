# Fresh 2026-08-26 execution and evidence ledger

## Scope and evidence labels

This review-owned ledger covers only the fresh adversarial review of
`K2P_Principal_D_Plus_Referee_Package_20260826.zip`. The distributed archive
has 214,930,375 bytes and SHA-256
`86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`.

The review used these path abbreviations:

- `REVIEW` = `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3`;
- `EXEC` = `REVIEW/execution/k2p_principal_d_plus_submission_referee`;
- `ISOLATED` = `REVIEW/isolated/k2p_principal_d_plus_submission_referee`.

Submitted writers and mutation programs ran only in `EXEC` or a disposable
copy. `ISOLATED` was treated as read-only evidence and, after all executions,
was replaced from the distributed ZIP. The final replacement contains exactly
the 489 archive files and no Python cache or symbolic-link byproducts.

Evidence labels:

- **S-FRESH** — submitted package code executed afresh;
- **I-FRESH** — review-authored code or a direct third-party tool executed
  afresh;
- **A-FRESH** — an adversarial mutation or negative-control invocation;
- **STORED** — sealed package evidence, never substituted for a fresh run.

Stream hashes below are SHA-256 hashes of exact captured stdout/stderr bytes.
Report hashes are identified separately. The BSD `/usr/bin/time -l` output is
part of captured stderr where such a log is named. A missing child argv, RSS,
or stream capture is explicitly marked rather than reconstructed. Full/quick
replay reports retain child layer names, return codes, runtimes, and stream
hashes, but not each child's complete argv or RSS.

## Environment

| Item | Fresh-review value |
|---|---|
| OS | macOS 26.5.2, build 25F84; Darwin 25.5.0; arm64 |
| CPU | Apple M1 Pro; 10 cores |
| RAM | 17,179,869,184 bytes |
| Python | CPython 3.14.6 |
| NetworkX | 3.5 |
| SymPy | 1.14.0 |
| Tectonic | 0.16.9 |
| Poppler | 26.08.0 |
| requirements | 28 bytes; SHA-256 `c9716447ec239f2c91180609c0b1c972533605a387be73d001c7e6b7e9b01891` |

## Fresh top-level package commands

All rows ran from `EXEC`. Redirection to the named `logs/` files and the
outer `/usr/bin/time -l` wrapper are omitted from the command cell; those are
capture mechanics, not child argv. Every row with a report path wrote outside
the authoritative package bytes or in the disposable execution copy.

| ID | Evidence | Exact child command | Exit | Wall (s) | Max RSS (bytes) | stdout SHA-256 | stderr SHA-256 | Result/report |
|---|---|---|---:|---:|---:|---|---|---|
| R01 | I-FRESH infrastructure | `python3 -m venv .venv` | 0 | 1.93 | 97,288,192 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `5c025f9b48fa4f734797caf9140f64b988808cddafb60d658154c11e123aa185` | qualified venv created |
| R02 | I-FRESH infrastructure | `.venv/bin/python -m pip install --upgrade pip` | 0 | 1.20 | 96,534,528 | `718706568de9b06a27c22283e3371ff13caf160182c8064a49b6f642545ea1c7` | `b426e12aba5813282dc045e5e7d980e2f90aa407fec0af9b01dbde96e4b081a0` | pip 26.2.1 |
| R03 | I-FRESH infrastructure | `.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | 0 | 6.31 | 179,273,728 | `b8cb8888e74efb13d53a13b09a6cf6e18e4df64a873dd861491a02bfca6cf7e8` | `3044fa57c52a0e563c5035e97d8da0c68219cee18e76dd66ef5b5c6430134e8d` | NetworkX 3.5; SymPy 1.14.0 |
| R04 | S-FRESH | `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.46 | 231,636,992 | `468aedd20bce6c1e99b4fbc7a0ec87bd227786c7d531e2341692da680a4cbcef` | `2bbc8b83cd0670001e64de22b48fb020444132c562bc85c23cdfcfc73418a624` | 406 files, 479,324,605 bytes, root `d4385855fd9d8387080a8e789613114f047fd93aaad9a78e86924d1a29b25c3e` |
| R05 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 9.93 | 516,947,968 | `20b3a276c444b271006edef1fb3b7a923a7cfc6d1d13b6a379c3ec615d04244c` | `95920959ebb7dad73ec9db6d3f61ab2022874275d83a9c132040ec75ed309155` | 230 files, ready, payload `b5eb26e953fbb76de671a4caa0db3068932af1e23b4fffdb0d118b5939f81756` |
| R06 | S-FRESH writer control | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py` | 0 | 9.89 | 518,209,536 | `771f5cd491db2d3b0903f5dee8d9722cccfb74ab0d3806bbd15d93fa3a4b883f` | `122ba3a7a04024905f893bcfeae261ff291e6ee1ba42dbc4cbbfc25889a13c93` | rebuilt lock byte-identical in `EXEC` |
| R07 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick --output REVIEW/logs/release_quick_report.json` | 0 | 286.48 | 1,463,189,504 | `a8b55d93480814fb3ec45e4523b0a6d06539ff41840ab4e1442fd5246bd50a3e` | `e4bd6c1f60c4c1cac90a1bcd11d3c3a0134d8a7d796fff135c8735b67b77b5b9` | 23/23 PASS; report SHA-256 `309d2b341a9ab8626ab1982000b43d0d015824885f9887d98f8323277c5a29aa` |
| R08 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --timeout-seconds 7200 --output REVIEW/logs/release_full_report.json` | 0 | 6,083.36 | 2,544,648,192 | `51da276e8e40527152104720191ff418aae1363e5eacfd96c2c76c28ec73389f` | `50bb7ef5960e48ae10d67f3e97bbf39a3299fecc050d428b50930f1e887c17c6` | 41/41 PASS; internal 6,082.872989 s; report SHA-256 `d5e6642eda6c4fa721cdde8a7cb9cf5da240b3784d27f6d99b1084c48ed79cab`; peak footprint 508,658,456 B |
| R09 | A-FRESH | normalized retained invocation of `work/final_theorem_release/run_corrected_universe_mutations.py` with external output `REVIEW/logs/corrected_universe_mutations_report.json`; complete argv was not retained | 0 | 218.10 | 461,307,904 | `14ad6897e7e53cf4b95ceeb055876fe00c0e709269d363af3a9a16f4dfcf2a15` | `371e23fd7c709a95f6168a1694de8b2eecea3b2f499742ec28d7f79c18fdef` | 22/22 PASS; report SHA-256 `596bb5a47c5cc662568a0e432ac2c544177d973dea12005b44b8ee7f46bc89c8`, payload `a67ce800ef355bd32d4e20aeadd6c1f8c2c285e70616a95c6999ca8d670cf0cb` |
| R10 | A-FRESH, concurrent heavy-run; cause unresolved | normalized retained invocation of `work/final_theorem_release/run_release_mutations.py`; complete argv was not retained | 1 | 718.33 | 2,545,827,840 | `befaf0d5e081844cbae526ed57629d8ca2ac5dc39b9d1bf6fbc887ce0830034d` | `96997dca4d59f4b5830eb1710d23ceec5b274d27006742ad5e330c7181dc8166` | stopped in `parameter_transport_mutations`: `triangle_edge_false_product_map:1:None`; no report. It overlapped the full replay, is diagnostically unqualified, and is not treated as a controlling semantic failure. |
| R11 | A-FRESH control | `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --timeout-seconds 7200 --output REVIEW/logs/release_mutations_control_report.json` | 0 | 3,519.10 | 2,635,235,328 | `7dbb43e2428d3d6c74923d956c1c9741315893be328341b65a276979b14ce5e4` | `349f87ac666959d4f7bf7898f4200fdc0e707aecdd92fb54359e6a641710f0ab` | low-contention control PASS: 25/25 aggregate mutation gates PASS, zero survivors/blockers; report SHA-256 `f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`; payload `05475591f00c75f2f0c2ee2e92c23bc869a8ed5000d28b40455ab7481870d30b`; peak footprint 483,410,736 B |

R10 had already rejected the optimized-mode, quartet-semantics,
quartet-terminal-binding, and canonicalizer-completeness gates before the
parameter-transport child stopped. Its observed failure is preserved as
evidence; it is not overwritten by a later control.

### R11 aggregate mutation gates

The controlling report retains stable semantic evidence but deliberately
excludes per-gate elapsed time, temporary paths, raw child output, and
raw-output hashes. Therefore the table does not invent per-gate argv, timing,
or RSS. R11's exact outer argv, timing, RSS, streams, report, and payload are
in the top-level command table.

| Gate | Status | Nested case count when declared | Nested payload SHA-256 when declared | Scope/expected mechanism |
|---|---|---:|---|---|
| `optimized_mode` | REJECTED | — | — | FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN |
| `quartet_semantics_mutations` | REJECTED | 8 | `aa7c5bb024441e9e620e8cc40154dc866ab0fa06169eea2366c5c2336e3709aa` | 8/8 literal spectrum, coordinate, domain, document, and optimized-mode attacks |
| `quartet_terminal_binding_mutations` | REJECTED | 12 | `73d6f6594bcd24cbb1d737d4837be4b3469396249d0cb2ae256e903d93092aac` | 12/12 resealed algebra, split, reference, reassignment, reversal, and optimized-mode attacks |
| `canonicalizer_completeness_mutations` | REJECTED | 2 | `6a86dd657f3240a072df59df358fe93f475bb9a262edd52b83cd6dade7e7a73c` | 2/2 nonordinary-triangle and selected-triangle marker attacks |
| `parameter_transport_mutations` | REJECTED | 10 | `93741cbeb50b2e2fde5d2c144de5d9943d1879fb61faf64115cf44ec5608b044` | 10/10 paired-edge, parent-flip, triangle-local, restriction, root-suppression, and reversal attacks |
| `rank_upper_mutations` | REJECTED | 7 | `2fae9aab6167a060abbce5544b1ae7180a29ac3ddcbf33ae2aff1d5485b46110` | 7/7 rank coverage, syzygy, orbit, port-transport, false-rank, and complete production-verifier attacks |
| `corrected_raw4_overlay_mutations` | REJECTED | — | `3bac7bccf763bf5d2e476607751fb6b9971c002bfaff171a693855ec3677befa` | authoritative v2 full-map overlay, 9/9 mutations |
| `theta2_full_map_mutations` | REJECTED | — | `9d4a1753c7b51b868e20fb828fc418c8ba75ad5b956f04664b239ab7fd73c688` | independent whole-map theta2 suite, 10/10 mutations |
| `corrected_primitive_composite_mutations` | REJECTED | 26 | — | fresh verifier-facing raw4 14/14 and theta2 12/12 suites: 22 complete disposable-ledger attacks plus optimized-mode and aggregate source-immutability guards |
| `corrected_restoration_v3_mutations` | REJECTED | — | `9f31f9688a587d79d35c24114d4a0693463486f254f0ee4892b99494d707c909` | fresh clean-forest suite, 13/13: omitted child, wrong parent, broken transport, reassigned quartet/T_i/quartic |
| `corrected_two_stage_probe_mutations` | REJECTED | 15 | `14f0364d516330017f0e73d904ad3d6ff5825f299d3fa2f00dcac5720a6f6e74` | fresh 15/15 suite plus nondefault hash-seed replay: omitted one-/two-port rows and parent, wrong parents, reversed order, global triangle, exact transport/restriction, T_i/Bernstein, classifier precedence, and optimized mode |
| `promotion_theorem_status` | REJECTED | — | — | promotion package exact byte-binding gate |
| `promotion_quantifier_checklist` | REJECTED | — | — | promotion package exact byte-binding gate |
| `promotion_pass_gate` | REJECTED | — | — | promotion package exact byte-binding gate |
| `promotion_zero_gate` | REJECTED | — | — | promotion package exact byte-binding gate |
| `promotion_ledger_path` | REJECTED | — | — | promotion package exact byte-binding gate |
| `promotion_combined_root` | REJECTED | — | — | promotion package exact byte-binding gate |
| `historical_artifact_promoted` | REJECTED | — | — | historical artifact quarantine registry exact binding |
| `historical_authoritative_replacement_removed` | REJECTED | — | — | historical artifact quarantine registry exact binding |
| `historical_scanner_record_omitted` | REJECTED | — | — | historical artifact quarantine registry exact binding |
| `weak_sharpness_mutations` | REJECTED | 21 | `946cc5706d5cb60e2a818461f7ac2d02409b8722e19f6334f2f51eb3db166edf` | 21/21 exact typed graph, tensor, rank, cherry, and optimized-mode attacks |
| `reassigned_cubic_certificate` | REJECTED | — | `75f07d311c6e0a24ac00b575649e94c53d40c2ea4b231666ca1ca9dc925ab80e` | DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH |
| `reassigned_quartic_certificate` | REJECTED | — | `75f07d311c6e0a24ac00b575649e94c53d40c2ea4b231666ca1ca9dc925ab80e` | DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH |
| `reassigned_quintic_certificate` | REJECTED | — | `75f07d311c6e0a24ac00b575649e94c53d40c2ea4b231666ca1ca9dc925ab80e` | DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH |
| `raw4424_false_tree_sunlet_reintroduction` | REJECTED | — | — | frozen unified corrected-universe mutation suite |

All 25 aggregate gates are unique and REJECTED; the report has zero survivors
and zero blockers. The 25 aggregate rows encapsulate more than 25 primitive
mutants (for example, 10 parameter transports, 7 rank attacks, 26 corrected
composite cases, 13 restoration cases, 15 probe cases, and 21 weak-sharpness
cases).

## Input-copy identity and immutability boundary

Before execution, independent 489-row relative-path SHA-256 inventories of
`EXEC` and `ISOLATED` were byte-identical. Each inventory file has SHA-256
`c689844a8f0b2b241fc2d1c88d99c826b70c20619b9558be9938ba03bd00f6b3`.
The broader initial `EXEC` inventory (490 rows, including its review-owned
copy metadata) has file SHA-256
`b6b48179bc1494cb33e887912d765191d7f0bde1e16cc225175dfba5968d7f94`.
The initial `ISOLATED` inventory has file SHA-256
`283920cf0486a30b167082ecc407ed9b6329412fec9bea429a1f2834d5b9510f`.

The full and mutation harnesses fingerprint their locked inputs and reject
drift. After R11, a direct `shasum -a 256 -c` check against the original
489-row submitted-file inventory returned 0 with 489/489 `OK`; its stdout has
SHA-256
`f58c22d4d32b76efd907d6e40725c6094bb329a95c3539d9db20e75d2f5a1cc2`.
The child processes had created exactly three unsealed Python-cache files in
disposable `EXEC` (`compression_common`, `verify_final_theorem_release`, and
`k2p_atlas_core`); the 489 submitted files themselves remained byte-exact.
Unsealed `.venv` and `__pycache__` files are execution/reviewer infrastructure
and are never treated as archive members.

The ZIP-derived path/size/hash ledger is
`evidence/provenance/final_archive_member_ledger.tsv`: 489 member rows plus
one header, 87,015 bytes, SHA-256
`d6584f46587e1c2c29f40e924edd28579b2a29acfb7a3b0b878bca0d8850a36c`.
It was generated by a review-owned standard-library ZIP stream and did not
import submitted code.

The exact post-R11 submitted-file check was:

```sh
# cwd: /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/execution/k2p_principal_d_plus_submission_referee
shasum -a 256 -c ../../logs/execution_source_before.sha256 > ../../logs/execution_source_check.stdout
```

Its wall time, RSS, and separately captured stderr were not measured; none is
inferred.

The final `ISOLATED` tree was newly re-extracted from the distributed ZIP and
compared independently with that complete ledger. The comparison returned 0
in 0.32 s with maximum RSS 274,989,056 bytes and peak footprint 264,749,656
bytes: 489/489 paths, 483,608,160/483,608,160 bytes, zero hash/size/path
mismatches, zero symbolic links, and zero `__pycache__`/`.pyc` objects. Its
stdout SHA-256 is
`fc54f242fcaa4dd7b8eb147d3f90dc7c514641211d2d7a264641a85f81699cdf`;
the stderr/time SHA-256 is
`bb937dce3ecd0a8fc5d698ca0068841568d3e21a812a7cd62df041d08545d2e5`.
The exact comparison command was:

```sh
# cwd: /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3
/usr/bin/time -l python3 -B -c 'import csv,hashlib,pathlib,sys; root=pathlib.Path("isolated"); rows=list(csv.DictReader(open("evidence/provenance/final_archive_member_ledger.tsv", newline=""), delimiter="\t")); expected={r["archive_path"]:(int(r["bytes"]),r["sha256"]) for r in rows}; actual={str(p.relative_to(root)):(p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()) for p in root.rglob("*") if p.is_file()}; bad={k:(expected.get(k),actual.get(k)) for k in sorted(set(expected)|set(actual)) if expected.get(k)!=actual.get(k)}; pyc=[str(p) for p in root.rglob("*") if p.name=="__pycache__" or p.suffix==".pyc"]; result={"expected_files":len(expected),"actual_files":len(actual),"expected_bytes":sum(v[0] for v in expected.values()),"actual_bytes":sum(v[0] for v in actual.values()),"mismatches":len(bad),"pycache_or_pyc":len(pyc),"symlinks":sum(1 for p in root.rglob("*") if p.is_symlink())}; print(result); sys.exit(1 if bad or pyc else 0)' > logs/final_pristine_extraction_check.stdout 2> logs/final_pristine_extraction_check.stderr
```

The re-extraction step itself was recorded as an action and target, but its
complete argv was not retained; no argv is reconstructed for it.

## Fresh quick replay: all retained child layers

R07 reports internal elapsed time 286.044108 s, mode `quick`, optimized mode
false, no blockers, and lock payload
`b5eb26e953fbb76de671a4caa0db3068932af1e23b4fffdb0d118b5939f81756`.
These are submitted replays. A layer name is not represented as exact argv.

| Layer | Return code | Status | Internal wall (s) | stdout SHA-256 | stderr SHA-256 |
|---|---:|---|---:|---|---|
| `promotion_manuscript_guard` | 0 | PASS | 0.289730 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `full_map_domain_reseal` | 0 | PASS | 0.125607 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_universe_independent_replay` | 0 | PASS | 9.790216 | `f7e9a523cda71bb0908f0525ac0e861d43242f336ae17fdfdf9441fe968b503c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `three_port_no_assert` | 0 | PASS | 0.553348 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `domain_rooting` | 0 | PASS | 0.066650 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_sign_logic` | 0 | PASS | 1.208884 | `61649d9e82422f1a536ac4751f3bda84561e7cd5c51290d0137eb7b59bf66e49` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_terminal_bindings` | 0 | PASS | 35.205896 | `9a82fef0325a5057a0ef27b0f7cc6d56e89c9a9adefa4ac38de5800e5d88e0bd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw_displayed_quartet_direction` | 0 | PASS | 2.758828 | `91fc95ea11887e6007cf59e760a26e0f1757753a833bf313ac18d8e623620a35` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_structural` | 0 | PASS | 0.208332 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_structural` | 0 | PASS | 27.566608 | `ec2483b3a0172dc14121cbf498bac3a3f607779d06dfdd17e21c84e665ce5817` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge_marginal_gluing` | 0 | PASS | 0.059508 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `analytic_adversarial_audit` | 0 | PASS | 0.400632 | `4884773924959ae0c0ce29953487165662b2efceeca8b572a2ea67fd01fb6bb2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `global_component_scale_audit` | 0 | PASS | 0.180061 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_independent` | 0 | PASS | 86.739647 | `3d602477a9c751b2a7fafaf0a9d4579009fd604b1fa22d456595093b4e49da42` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| `theta2_full_map_independent` | 0 | PASS | 45.194594 | `9b7e1a550f461d05e0c46f6edca192d8b8b268387fea261f49a49543c38b7aa0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_raw_structural_provenance` | 0 | PASS | 1.576595 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36` | 0 | PASS | 14.466909 | `8d53ffac2b3823abda37eb3dc40cde2e50d1a0a703ac3b4a2bbbd394bb9b113d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_structural_provenance` | 0 | PASS | 10.694532 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `cycle_three_port_authoritative_promotion` | 0 | PASS | 17.019381 | `a3270f6dddef4b40ce8772ff9ad3c872b8010418039bdc95e0c7ce65ddd1cc93` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_streaming_replay` | 0 | PASS | 16.913120 | `ce27e8a17795548a178568a7198635c9ebe6bef03932c7dae89f3c5a637591e1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_site_transport_partition` | 0 | PASS | 4.623463 | `57603f796ecbed71b4a24a09297d7f9d0fa019d1436556d7a6f14beb59fe0deb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_primary` | 0 | PASS | 0.225042 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_independent` | 0 | PASS | 0.181306 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Fresh full replay: all retained child layers

R08 reports internal elapsed time 6,082.872989 s, mode `full`,
promotion-ready true, optimized mode false, no blockers, and lock payload
`b5eb26e953fbb76de671a4caa0db3068932af1e23b4fffdb0d118b5939f81756`.
All 41 layers passed. These are **S-FRESH** submitted producer/verifier
executions. A layer name is not an exact argv; the report does not serialize
each child's complete argv or per-child RSS.

| Layer | Retained return code | Status | Internal wall (s) | stdout SHA-256 | stderr SHA-256 |
|---|---:|---|---:|---|---|
| `promotion_manuscript_guard` | 0 | PASS | 0.287794 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `full_map_domain_reseal` | 0 | PASS | 0.132572 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_universe_independent_replay` | 0 | PASS | 9.727799 | `f7e9a523cda71bb0908f0525ac0e861d43242f336ae17fdfdf9441fe968b503c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `three_port_no_assert` | 0 | PASS | 0.383773 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `domain_rooting` | 0 | PASS | 0.060815 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_sign_logic` | 0 | PASS | 1.112613 | `61649d9e82422f1a536ac4751f3bda84561e7cd5c51290d0137eb7b59bf66e49` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_terminal_bindings` | 0 | PASS | 34.663271 | `9a82fef0325a5057a0ef27b0f7cc6d56e89c9a9adefa4ac38de5800e5d88e0bd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw_displayed_quartet_direction` | 0 | PASS | 2.889306 | `91fc95ea11887e6007cf59e760a26e0f1757753a833bf313ac18d8e623620a35` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_structural` | 0 | PASS | 0.232101 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_structural` | 0 | PASS | 28.256358 | `ec2483b3a0172dc14121cbf498bac3a3f607779d06dfdd17e21c84e665ce5817` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge_marginal_gluing` | 0 | PASS | 0.059431 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `analytic_adversarial_audit` | 0 | PASS | 0.436018 | `4884773924959ae0c0ce29953487165662b2efceeca8b572a2ea67fd01fb6bb2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `global_component_scale_audit` | 0 | PASS | 0.194767 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_independent` | 0 | PASS | 90.389094 | `54d2380008ee12800429fa4a88252aea03c9171a78fde4da0a37788a1d74b02e` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| `theta2_full_map_independent` | 0 | PASS | 47.522629 | `ee9925d3e4521913dfb3afb12a0d50d2857f73cfd69e5c6bac9a7e3225fa530a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_raw_structural_provenance` | 0 | PASS | 1.595623 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36` | 0 | PASS | 15.116768 | `8d53ffac2b3823abda37eb3dc40cde2e50d1a0a703ac3b4a2bbbd394bb9b113d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_structural_provenance` | 0 | PASS | 10.991173 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `cycle_three_port_authoritative_promotion` | 0 | PASS | 17.224705 | `a3270f6dddef4b40ce8772ff9ad3c872b8010418039bdc95e0c7ce65ddd1cc93` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_streaming_replay` | 0 | PASS | 17.374663 | `ce27e8a17795548a178568a7198635c9ebe6bef03932c7dae89f3c5a637591e1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_site_transport_partition` | 0 | PASS | 4.702544 | `57603f796ecbed71b4a24a09297d7f9d0fa019d1436556d7a6f14beb59fe0deb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_primary` | 0 | PASS | 0.237439 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_independent` | 0 | PASS | 0.194531 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_full` | 0 | PASS | 124.295653 | `dde7a6df548d407df5cedb2810549aac0711269718ba203c9ddbd45461675188` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_full` | 0 | PASS | 343.663765 | `9d3414eb83163a3e831444b7d7efb7b18c5e2d8d43ed7e82552445be766399fe` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_restoration_independent_full_replay` | 0 | PASS | 500.200541 | `9b3cb53e5d67418f2202cb49ff85dfb949358decdab4740d5a1550965a608f23` | `7bb69d81f6d45d866e3030dda574eb3b5056c637319c017fc12ee4b3c10fb1da` |
| `corrected_universe_cross_layer_mutations` | 0 | PASS | 203.066543 | `14ad6897e7e53cf4b95ceeb055876fe00c0e709269d363af3a9a16f4dfcf2a15` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_full_map_Ti_truth` | 0 | PASS | 19.441422 | `ec5d6f372abbefabcb41bdb042503e88238325bb4f71cb1850823d55057d684a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_full_map_Ti_truth` | 0 | PASS | 73.179267 | `fe586c75afe67b879a0c2f96d9520417a72572794b4f89ff337e7951ce1194e2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `composite_domain_reseal_diff` | 0 | PASS | 16.234802 | `0c9290e7142fc4f3dc0a89408015b806385b48e507d6a2eebe0e2fca8e3fcfca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_exact_rank_staged_atlas_omission_mutation` | 1 (expected nonzero) | PASS | 0.350104 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `5fdba7abc0ce4f73880541bfaec271b8320df09b8686456f210359cad951eeca` |
| `four_port_exact_rank_import_preflight` | 0 | PASS | 0.38749 | `79d039353c2a88425952fe6ffd8e67653c512de65e89b2ab6f22b46e5ee72212` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_exact_rank_full` | 0 | PASS | 122.764512 | `a670c37ecc2fa8cde0575c640be5d3af7ffb841648bc8f4464785d4332bb1362` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_full_regeneration` | 0 | PASS | 61.732527 | `b62bf1aa1efc498e83e9054af1bb5228a9213f4c03ff07fcbfc01d6001059870` | `de1f579aafe4aa7f4d84e6f47f6b6ca9aba263df850de2b6839abc89018dfb8c` |
| `four_port_raw_full_regeneration_provenance` | 0 | PASS | 318.629357 | `8eb91f720fe064d3007c5f2f4a65295b921c068285b1fad9db3d3710ae3f55c6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36_full` | 0 | PASS | 107.401629 | `770af48343668f93633451072582efb477294a88da4046b88d2eac91508c2727` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_full_regeneration_provenance` | 0 | PASS | 477.192379 | `82c6917c4503a2cb7d3c42988100a58731dff13c8972a45b27ffbb5226bbd783` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_full_primitive_regeneration` | 0 | PASS | 2992.736053 | `129a45db66a6e1a9b4e733ce4a87c6be61e678031bd62b09a8246e5945036a55` | `24548d12907df3b2d4c09684f334439f33ff5ed238106a7f03e5979c45a57dfb` |
| `corrected_probe_full_independent_replay` | 0 | PASS | 16.677781 | `ce27e8a17795548a178568a7198635c9ebe6bef03932c7dae89f3c5a637591e1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_full_site_transport_partition` | 0 | PASS | 4.628138 | `57603f796ecbed71b4a24a09297d7f9d0fa019d1436556d7a6f14beb59fe0deb` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_primitive_graph_full` | 0 | PASS | 405.886596 | `d17da6517e02a00e522c57e3cf76a7e484036e565aa23249aebbd73b268aea58` | `cbc56ffd93ed354a5cd9adfa22ebe130b83db6b8822b4fc1adc29c66e71e7602` |

The rank staged-atlas omission row is an intended negative test: its child
returned 1 and emitted the required missing-module diagnostic, so the layer
status is PASS. The restoration replay additionally binds command SHA-256
`dc76b9eeaf7acc19780810ca9f631fb615c51ad2a3c404cfdbb0a91692998b3e`
and exact source hashes for the forest
`bcf91bf433c71056d1e27871dd15fe532f9ae1cc4ad79eb2373eae57071ee427`,
historical crosswalk
`42155ffb322f493d2e4b2971c71b26a5b2d4156e23fc2ae971a9a50dc96c8223`,
and verifier
`e4cef28f156e1c300ed7b7cc48bb1a96f3a7686d92e2c748ec8dfa156d236f9e`.

## Additional submitted checks

All rows ran in a disposable qualified copy. Commands listed as exact were
recovered from the preserved review notes and logs; a `normalized invocation`
means the complete argv was not retained.

| ID | Evidence | Command | Exit | Wall (s) | Max RSS (bytes) | stdout / result SHA-256 | stderr SHA-256 | Result |
|---|---|---|---:|---:|---:|---|---|---|
| S01 | S-FRESH | `.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py --check` | 0 | 0.19 | 42,434,560 | stdout `59f401307c0cce25ff2d7570789fd89da78e5d642814d870589b965549a272a5` | `19c8f5556631aa65a2e5ee3941646fc703f4e320cc549e692419113781ffede8` | static source audit PASS |
| S02 | S-FRESH | `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.41 | 170,786,816 | stdout `298114b75c2a2198f8bc67e9666845a88dbab55285d4e4b241e8341335402b32` | `1c160c36cd661a0bbd052b64a5284206ff517d948cf248618d5f7a39527da7a3` | 13 claims PASS |
| S03 | S-FRESH | `.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.81 | 229,539,840 | stdout `b52b015e43b75dd3d99c11024afa601b8a8a91a15cfa0fe705ad497b5cf1db0b` | `0a07dc83a2d000b5d4a6b10d13df8cffd240fd0681f89b309aa9c6d407a2c4c4` | 406 frozen + 82 submission files PASS |
| S04 | S-FRESH | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 0.69 | 292,454,400 | stdout `b52b015e43b75dd3d99c11024afa601b8a8a91a15cfa0fe705ad497b5cf1db0b` | `93acfaaed1d2841fbb15db9093b3cc9c9b001a43286bc9583763a05f6351c587` | outer checker PASS |
| S05 | S-FRESH | `.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check` | 0 | 0.08 | 34,603,008 | stdout `470286fe31274571acc258ef9f752cc676292cf15bb9c81741adb98e239623e9` | `548fb140feee32222fbaa6a222ac818aaf0e2a71c318d239aa1b0039853b0293` | `PC-PARTIAL`, zero unresolved records |
| S06 | S-FRESH | `.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check` | 0 | 78.69 | 294,551,552 | stdout `900d6404ce4025b8f78773985dd22f146bf073449e82d5deb3a298c5944d007a` | `24c734295510a2444ea6da2db133029b5ef6992a1240289287be7af2100e2df6` | seven commands PASS; internal 78.396 s |
| S07 | A-FRESH | `.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check` | 0 | 0.42 | 40,189,952 | stdout `c222d94339f83ada7faf9c9564d160a326e4af182da76c69ebc513fbc8ec0f84` | `c9305586b2d45360a063787a29c18aa593ab2261b7cfceb18baad92e39b54f3a` | 11/11 PASS |
| S08 | A-FRESH | `.venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 11.79 | 505,249,792 | stdout `bd92ab6565a2a75317d7b83aa07fd7d0096ea13697b1f6457d1ac999125afd29` | `24df915e1e4c47e34dbdce43580c7782447edbcb3103546bcaf100bbe6d60ea1` | 31/31 PASS; later independent timing-only repeat: 10.05 s, same stdout hash |
| S09 | S-FRESH fixtures | `.venv/bin/python -B proof_compression_submission/test_clean_full_replay_telemetry.py` | 0 | 7.65 | 27,885,568 | stdout empty; stderr/time log `f29b96c768470a3224c131e37d986624a58aa69438fd7c5bf5ba0b25c3ac2408` | same capture | 12 tests PASS |
| S10 | S-FRESH | `.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 26.94 | not retained in the compact provenance timing log | stdout `6617d0c7d4e5e6c9ad6a63dbc65be5729271c81894cb2eeec3aeb3d1c7a304f0` | `c382723d7b3a8b3e4625549df4e28e2af530cc5ab92f5017aed2ba1826fa77ad` | double rebuild and omission gates PASS; report payload `d3b3095fb009e0b10870cd8afd04e7948a16c0d2c225c1ecd0989f61beceadaf` |
| S11 | S-FRESH fixture | `.venv/bin/python -B work/final_theorem_release/test_release_mutation_output_contract.py` | 0 | 0.37 | not retained | stdout `4988dbe96b51dbe099727ea52b8474e94cabf68dd5c429b54aa0520740e0c4af` | timing `554141f57dac254d7f1b519af0e853d22cbea0bf5dd9b7823862c609a82f1339` | output-safety controls PASS |

The seven S06 subcommands and each S08/S09 test name are retained in the
submitted outputs, but their per-child RSS values are not. They are not
expanded into invented command rows here.

## Independent mathematical and finite checks

| ID | Evidence | Exact command | Cwd | Exit | Wall (s) | Max RSS (bytes) | Result SHA-256 | Independence boundary and result |
|---|---|---|---|---:|---:|---:|---|---|
| I01 | I-FRESH | `python3 -B independent_checks/computation/fresh_census_audit.py --project ISOLATED --output independent_checks/computation/fresh_census_audit.json` | `REVIEW` | 0 | 54.74 | 274,153,472 | `602924d7481b4132bc17323c27299e1e904db15c673ce7a252d0d0e759cf51e0` | no submitted imports; independently enumerates primitive completion grammar/raw IDs and checks parent/reference closure, but counts submitted analytic labels rather than reclassifying every row; payload `0a60795802e1e40a38590ae251cc09f3ac77331fa240f61c4162b9565ae1dd88` |
| I02 | I-FRESH | `python3 -B independent_checks/computation/k2p_domain_boundary_audit.py` | `REVIEW` | 0 | 0.09 | 18,989,056 | `39e2101d0aacd7b4326b7f5795e1ac9ece32f2aa5f50d595fde7a63f562a3b25` | exact `Fraction` check: 136 grid points, 20 boundary witnesses, 10,404 D-plus products; no submitted imports |
| I03 | I-FRESH | normalized retained invocation of `independent_checks/math/exact_spot_checks.py`; complete interpreter argv was not retained | `REVIEW` | 0 | 1.85 | 65,699,840 | `60594dc6f2bbf3d382e9e529d249ed9ffe6a7ba1c802f30b8a5a1d03a6ad8286` | no submitted imports; exact completion counts, quartet/Ti formulas, rank-nine blocks, both weak tensors/Jacobians, cherry determinant |

Preserved checker source hashes are, respectively,
`933e2dac57fd09a409288576a5473ab5d7c54070fc8c82567793f3a099a0a163`,
`aad747d88462d2e205181932b724816ab79b407c0e9fc048fdd89b12569e9e0a`,
and
`05b1f799f95e8de95494c1c5ceaf62e45b335d9e16eb9f2744c6927cd4c7b298`.

## Additional computational-adversary executions

These executions were performed independently in
`REVIEW/execution/r3_computational_adversary/package`, a second disposable
copy. Raw stream captures were not retained, so no stream hash is inferred.

| ID | Evidence | Exact or normalized command | Exit | Wall (s) | Max RSS (bytes) | Result artifact / observation |
|---|---|---|---:|---:|---:|---|
| C01 | S-FRESH repeat | `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.60 | 231,669,760 | PASS, same 406-file root as R04 |
| C02 | S-FRESH repeat | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 10.03 | 518,602,752 | PASS, same lock/payload as R05 |
| C03 | S-FRESH fixtures | `.venv/bin/python -B work/final_theorem_release/test_semantic_mutation_diagnostic_contracts.py` | 0 | 0.52 | 64,913,408 | nine qualified forms and 49 negative controls PASS |
| C04 | A-FRESH | `.venv/bin/python -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output REVIEW/execution/r3_computational_adversary/canonicalizer_mutations.json` | 0 | 0.52 | 50,626,560 | 2/2 intended rejections; report SHA-256 `48c35a2c6a2abe2327a3921dffbaecfd1ddc829d16e6478991f85dd6fb07b158`, payload `6a86dd657f3240a072df59df358fe93f475bb9a262edd52b83cd6dade7e7a73c` |
| C05 | A-FRESH | independent missing-`networkx` plus stale-PASS canonicalizer attack; complete wrapper argv/timing was not retained | 0 expected catcher | under 1 | not sampled | baseline child exit 1; wrapper created no output and emitted no PASS |
| C06 | A-FRESH | `.venv/bin/python -B work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py --output REVIEW/execution/r3_computational_adversary/restoration_mutations.json` | 0 | 586.20 | 574,898,176 | 13/13 intended rejections; report SHA-256 `3fc427a415fa4cdb2cb31007913afdd6422a0f9833387a7f6876e0cc3a34b9b4`, payload `9f31f9688a587d79d35c24114d4a0693463486f254f0ee4892b99494d707c909` |
| C07 | A-FRESH | `.venv/bin/python -B work/probe_coherence_corrected/run_probe_coherence_mutations.py --output REVIEW/execution/r3_computational_adversary/probe_mutations.json` | 0 | 195.28 | 69,386,240 | 15/15 intended rejections; report SHA-256 `eec59bb49db580828cdded73ca36fc01a6b0442d826c3a24fcba966e30755dd7`, payload `14f0364d516330017f0e73d904ad3d6ff5825f299d3fa2f00dcac5720a6f6e74` |
| C08 | A-FRESH, separate concurrent heavy-run; cause unresolved | `.venv/bin/python -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py --output <reviewer-output>` | 1 | 515.92 | 2,548,809,728 | fail closed on first mutant with `unqualified production rejection:triangle_edge_false_product_map:1:None`; exact stdout SHA-256 `85f60ec7977b889a6021fb9d356aa587229ea1dcc5bf511836197df88abcc744`; no report; separate concurrent invocation of the same submitted mechanism as R10 |
| C09 | I-FRESH driver around untouched submitted verifier | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/execution/r3_computational_adversary/package/.venv/bin/python -B REVIEW/execution/r3_computational_adversary/diagnose_parameter_triangle.py` | 0 expected catcher; production child 1 | 360.45 total; 313.643751 verifier | 2,546,106,368 | exact production stdout `PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:parameter_transport_certificate.json`, SHA-256 `c725b0eb845fc7acf11ee3c4751a3dde3de4299188c65a75d83bfac7807332ce`; empty production stderr; driver stdout `bdae9106b2fd1886fe69f2624ac39e4d4d2f7bb3d8c68dac96d6fe51509e1c89`; result `ce0684e2676e381683a04f9650deb10d52f2015ee7633474eb66a71c87aa2f63` |
| C10 | I-FRESH | direct in-memory sampled-rank semantic substitution attack; complete argv not retained | 0 expected catcher | 0.45 | not sampled | exact `RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6` |
| C11 | I-FRESH repeat | `.venv/bin/python -B /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/independent_checks/computation/fresh_census_audit.py --project REVIEW/execution/r3_computational_adversary/package --output REVIEW/execution/r3_computational_adversary/fresh_census_audit.json` | 0 | 52.09 | 341,934,080 | report SHA-256 `602924d7481b4132bc17323c27299e1e904db15c673ce7a252d0d0e759cf51e0`; same payload as I01 |
| C12 | A-FRESH | each of the four supported commands under `python -O`; individual argv/time streams not retained | 1 each | under 1 each | not sampled | each exact optimized-mode marker observed; no success artifact |

C09's review driver has SHA-256
`16ca0b22b347143c53ba897d393b75df2ba2093191376db4c980ccb994ba72ee`.
It independently builds and reseals the complete first mutant, then calls the
unchanged production verifier; it does not call the mutation wrapper's
decisive classifier. C09 establishes the intended rejection path for the
first mutant but does not substitute for R11's complete ten-mutant/25-gate
orchestration.

## Independent provenance, archive, PDF, and fail-closed checks

The principal disposable provenance root was
`REVIEW/tmp/provenance_r3/extract_a/k2p_principal_d_plus_submission_referee`.
It was removed after results and hashes were retained. The commands below use
`PROV` for that exact former path.

| ID | Evidence | Command or exact retained operation | Exit | Wall (s) | Max RSS (bytes) | Result / output SHA-256 | Result |
|---|---|---|---:|---:|---:|---|---|
| P01 | I-FRESH | `python3 -B independent_checks/provenance/independent_bundle_audit.py PROV /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260826.zip` | 0 | 2.22 | not retained | preserved result `evidence/provenance/independent_bundle_audit.json`, SHA-256 `39a46ef34d93d0801d763c98055dac823aa4fde512005a2281f96085853eda2e` | independently checked all 489 archive members, every outer/inner ledger row, counts, bytes, and roots |
| P02 | I-FRESH direct tool | `unzip -t K2P_Principal_D_Plus_Referee_Package_20260826.zip` | 0 | 2.70 | not retained | stdout `dcb909a56fc4976aa8baa7786a5d5f8be88653ff2f978c0b724e31f089c22476`; timing/stderr `3a517883c2353a5556125f7a324f2cb6ba2f14396da656b8fd6d1f6ecf2aa194` | archive structure PASS |
| P03 | I-FRESH | normalized retained invocation of `git_binding_audit.py PROV /Users/alec/Documents/Math k2p_level2_identifiability_closure cb7559e0ba5fd72f94bce5941208be0838be878d`; output redirection not part of argv | 0 | 19.85 | not retained | preserved `evidence/provenance/git_binding_audit.json`, SHA-256 `edef15443c29109824e94ac9d6b0eeecf1379c74a060ba72d4731fef25775332` | 489/489 tag blobs and 411/411 replay-commit inputs exact |
| P04 | I-FRESH | `python3 -B independent_checks/provenance/strict_json_inventory.py PROV` | 0 | 0.62 | not retained | stdout `1de65445d03a64f1aa2c6e1f3f3769688fdcccfb04613f39feb40344b26faa93` | 233 current JSON files; zero duplicate-name or syntax failures |
| P05 | I-FRESH negative finding | `python3 -B independent_checks/provenance/check_printed_supplement_hashes.py --project PROV --output <reviewer-output>` | 1 | 0.24 | not retained | preserved `evidence/provenance/printed_supplement_hash_audit_fresh.json`, SHA-256 `3d5ec99f0b2de74518e67e0d53ee50821dc2d4aa4e8806c5a4291d7619492e02` | 23 rows checked; exactly two stale presentations of one artifact hash; payload `03bff60b02496d5d7ebe63caeeefc7c8260c5893ebfd10e5a1fd24c42c7072ae` |
| P06 | A-FRESH negative finding | `PROV/.venv/bin/python -B REVIEW/independent_checks/provenance/test_outer_fail_closed.py PROV` (result written by redirection) | 0 | 3.71 | not retained | preserved `evidence/provenance/outer_fail_closed.json`, SHA-256 `6fbc82361dbf0e3ffc274e8f730d1dd0e99082ec14661129b4b7aa173a49443d` | intended symlink/missing/syntax controls reject, but a legitimately resealed same-valued duplicate JSON key is accepted by both outer checkers |
| P07 | S-FRESH PDF wrapper | same exact command as S10 | 0 | 26.94 | not retained | article PDF `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9`; supplement `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621` | rebuilt both twice from exactly five sources; outputs byte-identical |
| P08 | I-FRESH direct Tectonic omission | clean five-source build with `compression_tables.tex` physically absent | 1 | 3.69 | not retained | log `b5438bbab8a6434f0d6ecfd83740ec5f2dd3e12047eabedcab532d72602a87d5` | intended missing input at `supplement.tex:319` |
| P09 | I-FRESH direct Tectonic omission | clean five-source build with `certificate_appendix.tex` physically absent | 1 | 3.19 | not retained | log `d01a43d7fe0dbf743e3f7a92a339138ce7cc6e40f45f40624271d7b07689d52f` | intended missing input at `supplement.tex:453` |
| P10 | A-FRESH outer omission | outer builder after physically omitting `article/references.bib` | 1 | not retained | not retained | diagnostic: `required submission source missing` |

P05's checker source SHA-256 is
`d9fd06c302fa1d3e3d0fb233296adea009eaa3346e0edd87bbc148d7be3227c7`;
P06's is
`d6f636dd6b3087d32512aacae4e3f1ec76e0547e96b702cd1cb6ee4bb1308756`.
The duplicate-key acceptance is a present checker defect, not evidence that a
current distributed JSON is ambiguous.

The exact five-source/PDF binding checked by P07 is:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `proof_compression_submission/article/main.tex` | 85,827 | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` |
| `proof_compression_submission/article/references.bib` | 6,992 | `d1b3b50f6e276cc147471dcab9f30ed3a9b629fddc19ffb7fea58d427ee5de6b` |
| `proof_compression_submission/supplement/supplement.tex` | 46,057 | `7b28e0ff620b24256f4eebe61fc233dc21df8ffd7b4b552b51eb579712358bc4` |
| `proof_compression_submission/supplement/compression_tables.tex` | 3,269 | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `proof_compression_submission/supplement/certificate_appendix.tex` | 22,405 | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` |
| article PDF, 26 pages | 194,327 | `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9` |
| reader supplement PDF, 24 pages | 160,133 | `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621` |

All 50 rendered pages were visually inspected. The renderer's exact shell
argv and RSS were not retained, so that inspection is visual artifact evidence
rather than an invented execution row.

## Deterministic archive rebuild

The inspected outer builder was run with `--check --archive` three times to
three new disposable output paths. Each rebuilt archive was exactly
214,930,375 bytes with SHA-256
`86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`;
byte comparisons with the source and between rebuilds returned zero.

| Rebuild | Exit | Wall (s) | Artifact SHA-256 | Note |
|---|---:|---:|---|---|
| A | 0 | 20.65 | `86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba` | measured |
| B | 0 | approximately 21 | same | runtime stream was not retained after an intermediate yield |
| C | 0 | 20.92 | same | measured |

The large disposable rebuilds were deleted after hashing. Their retained
metadata file is `evidence/provenance/rebuild_metadata.md`, SHA-256
`0c03dd62ffcbc8f367e8ab960559e09e4220b638a0853a5735cb94c5d35ccacb`.

## Requested legacy names and current semantic replacements

The exact requested legacy filenames are not distributed. They were invoked
once to establish absence; each semantic replacement is separately executed
above. This is an interface change explicitly documented by the package's
`output/referee/README.md`, not a claim that the legacy files ran.

| Requested command | Exit | Wall (s) | Max RSS (bytes) | stderr SHA-256 | Current semantic replacement and fresh status |
|---|---:|---:|---:|---|---|
| `python3 -B verify_handoff.py` | 2 | 0.02 | 15,089,664 | `5b44713773c0ffa4426bcb92e79227e818d475fe1bd8f58e1b3182cca472bd07` | R04 + R05 + R07, all PASS |
| `python3 -B test_handoff_mutations.py` | 2 | 0.02 | 14,991,360 | `fca5bff9ea0a7bf9094a7dee50dd352be2b1d39e6504014e4ce9dcc9071335bf` | R11 current release-mutation authority: 25/25 aggregate gates PASS, zero survivors |
| `./setup_environment.sh` | 127 | 0.00 | 966,656 | `e8ba04514a756a992712f3a99e4ed89c767dda76add06ddc75dc7c4475a4c7b2` | explicit R01--R03 environment commands PASS |
| `.venv/bin/python -B run_all_verifiers.py --quick` | 2 | 0.02 | 15,073,280 | `f9178d10c101bf7ee2ed52ea927f6882b6395330a3f5931d016737acfe108f89` | R07 current quick authority PASS |
| `.venv/bin/python -B run_all_verifiers.py --full` | 2 | 0.02 | 15,220,736 | `eb665b2daa45cd021a5af7c05b6574b80e3d4666207c4cd1c43b294db45793c1` | R08 current full authority: 41/41 PASS |

The old `SUBMISSION_BINDING.json` interface is likewise intentionally
replaced by `work/final_theorem_release/RELEASE_LOCK.json` plus
`output/referee/REFEREE_BUNDLE_CONTENTS.json`.

## Stored evidence, explicitly not fresh execution

For comparison only, the package ships a 41-layer stored full replay report
with SHA-256
`2489643d65c50f662d027bf5002b9f398c8fa2999d7a17fcf43a5334cb04e86e`
and source-bound telemetry SHA-256
`b0f379d5e9d7e3acfd4c9812711964c4f7894dfd15e28045eab8077a9e6bd18f`.
It reports 5,696.744942 internal seconds, 5,697.15 wall seconds, and
2,552,119,296-byte maximum RSS. Those stored values are provenance evidence
only and are not substituted for R08.

The shipped 25-gate mutation report has SHA-256
`f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`
and reports 25/25 aggregate mutation gates PASS. It likewise is not
substituted for R11.

## Registry completion state

R08, R11, the post-run source check, and the final pristine-extraction/member-
ledger comparison are complete. This execution ledger is **COMPLETE**. The
separate review-wide artifact index is intentionally generated only after this
ledger and all report files are frozen; its file hash is therefore not embedded
recursively in this ledger.
