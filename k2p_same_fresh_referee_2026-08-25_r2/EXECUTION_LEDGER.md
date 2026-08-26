# Fresh 2026-08-25 execution ledger

## Scope and evidence labels

This is a review-owned ledger for the fresh rereview of:

- read-only package: `isolated/k2p_principal_d_plus_submission_referee`;
- source archive: `source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip`;
- distributed ZIP SHA-256: `ca08a3f50154610c7297ca83f92f0c9517fa5422ac7acf53b89582e1e14edbde`.

No command recorded here wrote to the isolated package. Submitted writers and
mutation programs ran in disposable copies or wrote only caller-owned reports
outside the package.

Evidence labels used below:

- **S-FRESH** — submitted package code executed afresh in this review;
- **I-FRESH** — independently authored review code, or a direct third-party
  tool invocation, executed afresh;
- **A-FRESH** — an adversarial review invocation of submitted code;
- **STORED** — sealed telemetry shipped by the submission and not substituted
  for a fresh execution.

`stdout` and `stderr` hashes are hashes of the exact captured byte streams
when the review registry retained them. A report/artifact hash is separately
identified. `not retained` means precisely that: this ledger does not infer a
hash, argv, runtime, or RSS value that the preserved evidence did not record.
The full and quick reports retain a layer name rather than each child's argv;
those layer rows are therefore not presented as exact argv. RSS for the full,
quick, and mutation wrappers is the peak for the outer measured process tree;
the nested reports do not assign an RSS to each child.

The authoritative review execution registry is
`reports/ROOT_EXECUTION_REGISTRY.json`, file SHA-256
`da0c06ea1c318d78813c39c85c1679e29facecc9ae45ccdfcc2a41f1d06ffce5`,
canonical payload SHA-256
`7141636320d9221706ed96b22c49a2a13c7acced18c80ad50493b5739d06049c`.
This ledger covers every substantive fresh package/review execution whose
argv or normalized command, exit, and timing were preserved in that registry
or the three signed review notes. Untimed exploratory reads (`rg`, `jq`,
`shasum`, source inspection) are not misrepresented as metered executions.

## Environment

| Item | Fresh review value |
|---|---|
| OS | macOS 26.5.2, build 25F84; Darwin 25.5.0; arm64 |
| CPU | Apple M1 Pro; 10 logical cores |
| RAM | 17,179,869,184 bytes |
| qualified Python | CPython 3.14.6 |
| NetworkX | 3.5 |
| SymPy | 1.14.0 |
| Tectonic | 0.16.9 |
| Poppler/pdfinfo | 26.08.0 |
| Info-ZIP | 6.00 |
| Git | 2.38.2 |
| requirements file | 28 bytes; SHA-256 `c9716447ec239f2c91180609c0b1c972533605a387be73d001c7e6b7e9b01891` |

Path abbreviations used only to keep tables readable:

- `REVIEW` = `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2`;
- `ISOLATED` = `REVIEW/isolated/k2p_principal_d_plus_submission_referee`;
- `EXEC` = `REVIEW/tmp/execution/k2p_principal_d_plus_submission_referee`.

The dependency-qualified interpreter created for the root replay was
`EXEC/.venv/bin/python`. The independent provenance track also used the
already qualified interpreter explicitly named in its commands. Interpreters
are execution infrastructure, not submitted evidence.

## Root clean execution: exact outer commands

All commands in this table are verbatim from
`reports/ROOT_EXECUTION_REGISTRY.json`. Rows R01--R10 and R14--R15 ran in the
disposable `EXEC` copy. R11--R13 used `ISOLATED` as a read-only cwd and wrote
their reports outside it. Angle-bracket tokens in R12--R13 are retained
redactions from the registry, not reconstructed argv.

| ID | Label | Command | Cwd | Exit | Wall (s) | Max RSS (bytes) | stdout SHA-256 | stderr SHA-256 | Report/result |
|---|---|---|---|---:|---:|---:|---|---|---|
| R01 | I-FRESH infrastructure | `python3 -m venv .venv` | `EXEC` | 0 | 2.08 | 98,123,776 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `d3b4242cafe438c16f28e8f6d43f5bfbbfe5008b8cde72fe9327ecc7f6087e05` | venv created |
| R02 | I-FRESH infrastructure | `.venv/bin/python -m pip install --upgrade pip` | `EXEC` | 0 | 1.30 | 98,369,536 | `718706568de9b06a27c22283e3371ff13caf160182c8064a49b6f642545ea1c7` | `bbd433a4afa71ee2f3969a48f541bbdd2f05dcd31cd2b61cda7ef55baadf55ac` | pip upgraded |
| R03 | I-FRESH infrastructure | `.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | `EXEC` | 0 | 6.05 | 177,586,176 | `b8cb8888e74efb13d53a13b09a6cf6e18e4df64a873dd861491a02bfca6cf7e8` | `db7ff0dd6dc77ff533a4391b82c1420010744ab66dc12cdaec735fe5ab978058` | NetworkX 3.5; SymPy 1.14.0 |
| R04 | S-FRESH | `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | `EXEC` | 0 | 0.60 | 230,195,200 | `234d8f3b43feaa2a0f2f3a0e94b457cea83161261977191cdbbda0ba8e927c24` | `ccebcd81afe1d1675df15fb8053e75be26b84545d2056998ac17c689bd90568f` | 403-file portable closure PASS |
| R05 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | `EXEC` | 0 | 10.07 | 468,516,864 | `4a6c02cc3744a15f4e8c97044db759760cf1796ac4968a2c97ed57b892f85547` | `953b032915b52b94bcdacc43f452dbe0f248cfb10c5f40a25265571e4a930acc` | lock payload `dcc15b8ae2bb46674344595809690657119e5271611bab8c3c47fccade0fa509` |
| R06 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick` | `EXEC` | 0 | 386.76 | 1,441,939,456 | `ee1ea2d6560df3a74fda6d8373b3be1b022b16999a23bf0ea20f08866d392f71` | `e60726c1d6848526c67f25953ba7dc154e78fe577d25ca46e5a6d4eb8206447a` | 23/23 PASS; report `logs/release_quick_report.json`, SHA-256 `c707481979868685cdaffbc20ced1c95d3b12f24eb892b2c6e9028c5a828b450` |
| R07 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/test_release_mutation_output_contract.py` | `EXEC` | 0 | 0.30 | 48,873,472 | `1f2f194e5d4249d6d2a713ec492dcb0a34c1b49ab5cabb85ec5552dca2127029` | `5891f50b702ddc8089e03ad79af49fa0b5d03064c9565c68a8e0d48a033360a6` | output contract PASS |
| R08 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/test_nested_mutation_output_contract.py` | `EXEC` | 0 | 0.29 | 25,329,664 | `bbe1d0401efaa645a1a02f6ac04792153e83185b68b4f899f1ea07d5de20700d` | `ae9b62318349c03528aebe3426a190d9092c04787538b4f9c04fa7a2fdc3315e` | nested output contract PASS |
| R09 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py` | `EXEC` | 0 | 971.54 | 1,423,196,160 | `2aae993baa3c626c0cb1aea54b6b246dc3a910339a3476acf0ff4249d8469037` | `5b0e5d2b3fc9434474219c83eee08816c37d00e2c0af5d384700bd5d46178c45` | 27/27 aggregate gates REJECTED, zero survivors; report SHA-256 `c60fdc2e5f70c702abbbc426f8e9595a1f64464b80a6bdccac13614ee5b2a28a`; payload `b7e1776e44ff5b50f92ed58f8b62d3c15ea49a358819bd8bc9dfac76ebd9df37` |
| R10 | S-FRESH | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full` | `EXEC` | 0 | 5,317.14 | 2,548,006,912 | `563e77a80c335284ac068c38bbdb4c1f94fde3bcad85636ee1ad61163b5a1a2b` | `c4ba9f170086627b0d981dd79107dce4e4d893b22f70395dffac9d5b6bc78661` | 40/40 PASS; report `logs/release_full_report.json`, SHA-256 `8ed37521c82830dc1f642d55faf1f5838fcd0ccbd0b90646e0eed184e65532ca` |
| R11 | A-FRESH | `/opt/homebrew/bin/python3 -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output <external-report>` | `ISOLATED` | 0 | 0.17 | 28,114,944 | `0e412e4c0c7ff8a12cf0f570a4890d874091b6bdabdfdaf8432184cab1999ba3` | `df389b59ba64df8f3a4e1dd0c35f814620021e5ac563e116dcdfc776c5241e10` | **false top-level PASS** on missing NetworkX; report SHA-256 `f4bf1d4eb8f9ef48213ab05cf8de2f48a2f368e2809a2f62474b931e135d32c9` |
| R12 | A-FRESH control | `<qualified-python> -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output <external-report>` | `ISOLATED` | 0 | 0.39 | 50,692,096 | `0e412e4c0c7ff8a12cf0f570a4890d874091b6bdabdfdaf8432184cab1999ba3` | `0ddccd76873fba3b3884d3ac18e3bf6790bfdbdf4f5131d4bd746e4a26078fb6` | intended diagnostics present; report SHA-256 `10b8eebaa739f3853434527bd6b55d90cdb28028345cb6285d687a8c3961dfdc` |
| R13 | A-FRESH | `<qualified-python> -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py --output <external-report>` | `ISOLATED` | 0 | 26.66 | 41,320,448 | `e156eb0a87a4a49e48891beedc70b3d926ca56bbf3f61f7f1f223928afe434f0` | `71357046163c3fbe2c8e61a1acaec0a6746137e4387d242343ff10c202c69f03` | wrapper PASS; 4/10 attacks rejected only by tautological row-hash inequality; report SHA-256 `893d1716040315a24191a1b05fee3aa5cfcf1900b780d3f283c0921de3e20634` |
| R14 | S-FRESH | `.venv/bin/python -B work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py` | `EXEC` | 0 | 33.61 | 524,255,232 | `fea309eafd5db60628a758dd57fed5ab4041ac113b8d6433156a98e68461055b` | `8e99936aad7324990526a65c76b3425c3a98acc6c38728bcb8d348795d6ae925` | 13/13 nonzero rejections; report SHA-256 `e5b3763c7fca333646e86462e0ca8af1332f98f650744f87c64c8a67f39b76ab` |
| R15 | S-FRESH | `.venv/bin/python -B work/probe_coherence_corrected/run_probe_coherence_mutations.py` | `EXEC` | 0 | 168.20 | 71,532,544 | `36e9a56591c9874877cc62c66742f0e2bd8d4c9aea9478263e1155287f14637b` | `8384fc51a887ac501586948c6b13b25e0321ca896256b9b56bf6c52335e74278` | 15/15 rejections plus clean nondefault-hash-seed control; report SHA-256 `4ba412df4e92ce696a10140e742e7aad82c3a0f685580f2ff33b8b638d566b64` |

Earlier fresh repetitions of three diagnostic commands are preserved in
`notes/computational_review.md`: the missing-dependency canonicalizer run
(0.20 s; 28,295,168-byte RSS), its qualified clean control (0.40 s;
50,413,568-byte RSS), and the parameter-transport mutation runner (28.65 s;
40,501,248-byte RSS). R11--R13 are the controlling exact-registry reruns and
supersede those timing-only repetitions. The earlier repetitions produced the
same semantic outcomes and no distinct evidence artifact.

The mutation run's independently computed 484-file source ledgers before and
after are byte-identical; both ledger files have SHA-256
`a995e62e73d2ef2d0f1c9455bec4acab5264cea1b2eeb59d2a178ab1637b3fe5`.
Successful qualified rejection does not cure the diagnostic-blind wrapper
defects documented for R11, R13, R14, and R15.

## Fresh independent mathematical and computational commands

| ID | Label | Recorded command / invocation | Cwd | Exit | Wall (s) | Max RSS (bytes) | Output/report SHA-256 | Result and independence boundary |
|---|---|---|---|---:|---:|---:|---|---|
| I01 | I-FRESH | `python3 -B r2_exact_spot_checks.py` | `REVIEW/independent_checks/math` | 0 | 1.09 | 65,290,240 | `60594dc6f2bbf3d382e9e529d249ed9ffe6a7ba1c802f30b8a5a1d03a6ad8286` | Independent exact rational/symbolic spot checks: domain, products, completion formula, quartet/sunlet/triangle formulas, weak-sharpness tensors/Jacobians. Script SHA-256 `05b1f799f95e8de95494c1c5ceaf62e45b335d9e16eb9f2744c6927cd4c7b298`; no submitted imports. |
| I02 | I-FRESH | independent `primitive_core_enumeration.py` rerun; exact argv was not retained | review scratch | 0 | 0.09 | 19,955,712 | `eb6ba17f6a46a9f1d7125086098f66432e944af36c76ebddf6e42637918fca96` | Independent primitive orientations/rootings/repair enumeration. Source script SHA-256 `183d340ee52364abc15e0e48167de2e28f553dde8b54d2960b6465f8b80c712f`; embedded payload `8ef395f7b34bd4ceeb4fc4fcb089930ed7002d37dfa5d61c071aabd24dc1f460`. |
| I03 | I-FRESH | `python3 -B tmp/fresh_census_audit.py --project isolated/k2p_principal_d_plus_submission_referee --output tmp/fresh_census_audit.json` | `REVIEW` | 0 | 51.79 | 318,570,496 | `844646caeadcf36885d722c85188b3f00fd29e0d6619ca7f5feb58006c791905` | Independent standard-library enumeration of primitive completion domains, raw IDs/order, counts/hashes, parent and transport-reference closure. It counts submitted analytic labels and is **not** an independent all-row classifier. Preserved script SHA-256 `933e2dac57fd09a409288576a5473ab5d7c54070fc8c82567793f3a099a0a163`. |
| I04 | I-FRESH | `python3 -B tmp/k2p_domain_boundary_audit.py` | `REVIEW` | 0 | 0.07 | 19,152,896 | `39e2101d0aacd7b4326b7f5795e1ac9ece32f2aa5f50d595fde7a63f562a3b25` | Exact `Fraction` audit of 136 domain points, 20 boundary-near witnesses, 10,404 products, and CT implication; no submitted imports. Preserved script SHA-256 `aad747d88462d2e205181932b724816ab79b407c0e9fc048fdd89b12569e9e0a`. |
| I05 | S-FRESH, shared submitted graph/model code | qualified Python invocation of `work/quartet_separation_closure/verify_quartet_logic.py` with an external `--output`; full argv was not retained | `ISOLATED` | 0 | 1.32 | 66,863,104 | `a49d8d7c02cd349f3db0df8d54d4887afa5953bfb9f16317eb5cbd43225984d1` | Six exact formulas, 288 transports, 21 displayed-set pairs; payload `20afb6da3e9acaf15db941cad782b8545893be260413119acc3bafdb0195a7ba`. Submitted replay, not an independent implementation. |
| I06 | A-FRESH, submitted mutation code | qualified Python invocation of `work/quartet_separation_closure/test_quartet_semantics_mutations.py --output <external-report>`; full argv was not retained | `ISOLATED` | 0 | 3.62 | 92,897,280 | `a1bf423637775b295fb1d6554401352834c59eab326798f7db4753a3855a4a9e` | 8/8 exact intended diagnostics; payload `4f7bef166b12b41058777cf17eb172605f1d50184fb449f4dd61565c6e48fc2e`. |
| I07 | I-FRESH driver around submitted verifier | `/usr/bin/time -p /usr/bin/python3 -B run_bounded_probe.py 2>&1 | tee bounded_probe_console.log` | `REVIEW/independent_checks/computation/composite_mutation_probe` | 0 | 85.23 | not separately recorded | report `1ea89890987b6b675da080bd38fe8bcedb409c9c40466ab275d7c116bbc3612a`; console `e4512969f368ff54066dd38b23e8804e6fcd29f232439af60330c36cf61a718d` | Four complete mutant ledgers sent to untouched production verifier: wrong port, wrong parent, reversed direction, missing theta2 child. All verifier children exited 1 at intended semantic gates before checksum; payload `055ef32f589d7ec941120d5bf8f60ea58ec23066ed3db6e9f4b36c2d0123ca60`. Driver SHA-256 `3eedd80fbeaa094b73a85e6a58dda03737d5e16b782cc960fe4c56aa87a4f941`. |
| I08 | S-FRESH unit fixtures | `/usr/bin/time -l python3 -B proof_compression_submission/test_clean_full_replay_telemetry.py` | disposable package copy | 0 | 4.62 | 27,394,048 | captured stderr/time log `2bead2304336a9e6fd1cb61158f744cac170030935fb421e0cf1190963865a39` | 9/9 telemetry fixture tests. A separately timed provenance rerun of the same submitted command was 4.67 s / 27,230,208 bytes, also 9/9 PASS. Submitted semantics with independent fixtures, not an independent telemetry implementation. |

For I07 the report retains the exact verifier argv for each child. The four
child exits and internal times were: raw4 wrong port, exit 1, 3.522315 s
verifier / 5.837550 s total; raw4 wrong parent, exit 1, 5.846434 / 8.187266 s;
raw4 reversed direction, exit 1, 6.242249 / 8.501306 s; theta2 missing child,
exit 1, 45.205449 / 62.456625 s. Their complete-mutant SHA-256 values were,
respectively,
`fcd2f649befe0175b30d47c87d421826e613f465a5a31dd22e6a97d1931ad66f`,
`fbf0ddf28ec78f8bf1b1a6d07c132f43ff98d774d8089f1a07e78520e6aec3fe`,
`7794d2642b93c3a23f7c9ddefdccbcf6f2fc592298ff5ab4a016558fdaeb3be2`,
and `37701995f32077958f7033f582e1750d07cea33bd3bbdd60daa9cedcfe5a7faf`.

## Fresh full replay: all retained child-layer records

R10's report records internal elapsed time 5,316.723762 s, mode `full`,
promotion-ready `true`, optimized mode `false`, no blockers, and lock payload
`dcc15b8ae2bb46674344595809690657119e5271611bab8c3c47fccade0fa509`.
The table below transcribes all 40 retained child records. These are
**S-FRESH** submitted producer/verifier executions. A layer name is not an
exact argv; the report does not serialize child argv or per-child RSS.

| Layer name | Retained return code | Status | Internal wall (s) | stdout SHA-256 | stderr SHA-256 |
|---|---:|---|---:|---|---|
| `promotion_manuscript_guard` | 0 | PASS | 0.283469 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `full_map_domain_reseal` | 0 | PASS | 0.100851 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_universe_independent_replay` | 0 | PASS | 9.758390 | `8936f3c441026b2f517d3d50e9682b52d9a42b762dddfab1cd19013037e7e07a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `three_port_no_assert` | 0 | PASS | 0.347759 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `domain_rooting` | 0 | PASS | 0.058798 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_sign_logic` | 0 | PASS | 1.199498 | `087c3c46ce4a89d45fa4ee88330d96f3f227f0ff0e91a6512a860388cc90b7a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_terminal_bindings` | 0 | PASS | 33.825649 | `3576aec35eedfd4948ba7a64e075fc87fdf12a408aae03a0f52504dd36a9a73d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw_displayed_quartet_direction` | 0 | PASS | 2.750220 | `f89b232160a7aa71d9631363d803792a968d2d93327938d960ed0d3781acbb0d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_structural` | 0 | PASS | 0.205138 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_structural` | 0 | PASS | 26.992403 | `f49d9714184268f295c50c886d5f21474a20c99d669d60e142eabbfc047d1da8` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge_marginal_gluing` | 0 | PASS | 0.065840 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `analytic_adversarial_audit` | 0 | PASS | 0.396906 | `a807c9cf973bc11068ba3be8e46c9a7084e72ad0b23c43a43ae5d74c9badb6b0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `global_component_scale_audit` | 0 | PASS | 0.206155 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_independent` | 0 | PASS | 84.969649 | `7c48be6ac5bbc4ce60bdd5bd045011b2a38eb4f6ec9f4f5a63e30327bdba6abf` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| `theta2_full_map_independent` | 0 | PASS | 45.211182 | `524e8691cab0ad4dbbe194454d851f842e67a756567106fd4ab40ed20d347395` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_raw_structural_provenance` | 0 | PASS | 1.498018 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36` | 0 | PASS | 14.344196 | `edd75a644d6e97b5bf627364ce6c6002936a83d28ab4a731095f7cc5867a59fc` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_structural_provenance` | 0 | PASS | 10.620298 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `cycle_three_port_structural_provenance` | 0 | PASS | 102.039005 | `4468b3cfb464fa0b671d2e85d46b0dad34bfd49911671e7d8849056e67b85764` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_streaming_replay` | 0 | PASS | 16.315536 | `d1a38229443c0e9264006566b4b35b9d8379099942f069c23826ca2a4fdc01a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_site_transport_partition` | 0 | PASS | 4.553175 | `5133b897d38244c39ce2078ec92b898378198421cec2779c5f6b0d53e3cbd8aa` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_primary` | 0 | PASS | 0.208244 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_independent` | 0 | PASS | 0.166302 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_full` | 0 | PASS | 98.361703 | `dde7a6df548d407df5cedb2810549aac0711269718ba203c9ddbd45461675188` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_full` | 0 | PASS | 286.780672 | `4c74c4e1be9f9faf7aedf31f87b64010b59aaa67e60e6a34625a55b2aa621e8d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_universe_cross_layer_mutations` | 0 | PASS | 186.124649 | `52575dbc4b488390b32f7aa9ed78d306e26ba623c9b354c26eef6cbe4416596c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_full_map_Ti_truth` | 0 | PASS | 18.182002 | `ec5d6f372abbefabcb41bdb042503e88238325bb4f71cb1850823d55057d684a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_full_map_Ti_truth` | 0 | PASS | 69.301281 | `fe586c75afe67b879a0c2f96d9520417a72572794b4f89ff337e7951ce1194e2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `composite_domain_reseal_diff` | 0 | PASS | 15.932886 | `7dc2a9797f79c0f4796b6a85e7389f8a3f0cac8149dde347de1015e05bc94cf0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_exact_rank_staged_atlas_omission_mutation` | not retained (`null`) | PASS | 0.332126 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `df8a1dbee081bf05f30d676f6766dedc32ad673614e78508c75e32b86383fccf` |
| `four_port_exact_rank_import_preflight` | 0 | PASS | 0.345420 | `c2314174ac47759fada9da52ed3e430f3c428404324e819427e94e48ab5cd268` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_exact_rank_full` | 0 | PASS | 117.295503 | `4301dfb05db393d8c3529daa92071a33af07e0a7a98153c3b8cf4557b23b80c2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_full_regeneration` | 0 | PASS | 59.022842 | `68ed4609b78c6c097a5e7f36d587767ba82e6ef6f7cf3f76706b43188689ba3b` | `de1f579aafe4aa7f4d84e6f47f6b6ca9aba263df850de2b6839abc89018dfb8c` |
| `four_port_raw_full_regeneration_provenance` | 0 | PASS | 304.265834 | `8eb91f720fe064d3007c5f2f4a65295b921c068285b1fad9db3d3710ae3f55c6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36_full` | 0 | PASS | 104.357135 | `f7b6acf61412a72457412b9961d962ac2e5c7217700ef229e421b3a0f84f5701` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_full_regeneration_provenance` | 0 | PASS | 461.361092 | `82c6917c4503a2cb7d3c42988100a58731dff13c8972a45b27ffbb5226bbd783` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_full_primitive_regeneration` | 0 | PASS | 2,798.101237 | `9f8e98a4a105b9d8bdf6a9f0221856732d5778c83bf7ced6e0f76390ba0f1300` | `b6626a6d3810c06aa95079bc2440639254ba769c7d0aa880b6c7388882de8bcd` |
| `corrected_probe_full_independent_replay` | 0 | PASS | 16.211847 | `d1a38229443c0e9264006566b4b35b9d8379099942f069c23826ca2a4fdc01a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_full_site_transport_partition` | 0 | PASS | 4.525099 | `5133b897d38244c39ce2078ec92b898378198421cec2779c5f6b0d53e3cbd8aa` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_primitive_graph_full` | 0 | PASS | 409.953645 | `cac286ee25754fb7ec694cda9de6763f82b347582a33b74fb3cd6a86b3228cb8` | `cbc56ffd93ed354a5cd9adfa22ebe130b83db6b8822b4fc1adc29c66e71e7602` |

The labels `independent` in submitted layer names describe the submission's
own replay architecture; they do not turn those rows into independently
authored review code. Several share the atlas, canonicalizer, or expected
classification and are explicitly treated as shared-code computational
evidence.

## Fresh quick replay: all retained child-layer records

R06's report records internal elapsed time 386.249763 s, mode `quick`, no
blockers, and the same release-lock payload. These 23 rows are separate fresh
executions of the quick subset, not aliases for the full-run rows. The child
argv and per-child RSS were not serialized.

| Layer name | Return code | Status | Internal wall (s) | stdout SHA-256 | stderr SHA-256 |
|---|---:|---|---:|---|---|
| `promotion_manuscript_guard` | 0 | PASS | 0.282028 | `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `full_map_domain_reseal` | 0 | PASS | 0.105163 | `e7a652c5493c5fec9d71e7cb208b978b412fc6a13cd22c1fe3a206c8a01765b2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_universe_independent_replay` | 0 | PASS | 9.581154 | `8936f3c441026b2f517d3d50e9682b52d9a42b762dddfab1cd19013037e7e07a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `three_port_no_assert` | 0 | PASS | 0.343245 | `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `domain_rooting` | 0 | PASS | 0.058759 | `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_sign_logic` | 0 | PASS | 1.197610 | `087c3c46ce4a89d45fa4ee88330d96f3f227f0ff0e91a6512a860388cc90b7a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_terminal_bindings` | 0 | PASS | 33.818863 | `3576aec35eedfd4948ba7a64e075fc87fdf12a408aae03a0f52504dd36a9a73d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw_displayed_quartet_direction` | 0 | PASS | 3.614059 | `f89b232160a7aa71d9631363d803792a968d2d93327938d960ed0d3781acbb0d` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_structural` | 0 | PASS | 0.212929 | `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_structural` | 0 | PASS | 27.850126 | `f49d9714184268f295c50c886d5f21474a20c99d669d60e142eabbfc047d1da8` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge_marginal_gluing` | 0 | PASS | 0.075773 | `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `analytic_adversarial_audit` | 0 | PASS | 0.433881 | `a807c9cf973bc11068ba3be8e46c9a7084e72ad0b23c43a43ae5d74c9badb6b0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `global_component_scale_audit` | 0 | PASS | 0.213649 | `84dc3508a497b8ff5529bc1e7c8bfbe52c74abce12ddfc90f7115a4328d844d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_independent` | 0 | PASS | 93.378479 | `a1df4b9a016b7bee24f3547ab5a5675acd9e1482cf600c0f5479eb04fc189a7a` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| `theta2_full_map_independent` | 0 | PASS | 48.010476 | `9e70431561f24fc3fdfe6929ea67e607216fc164094a9352a65e59a9eab661e3` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_raw_structural_provenance` | 0 | PASS | 1.557623 | `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36` | 0 | PASS | 15.684384 | `edd75a644d6e97b5bf627364ce6c6002936a83d28ab4a731095f7cc5867a59fc` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_structural_provenance` | 0 | PASS | 10.829791 | `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `cycle_three_port_structural_provenance` | 0 | PASS | 106.696247 | `4468b3cfb464fa0b671d2e85d46b0dad34bfd49911671e7d8849056e67b85764` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_streaming_replay` | 0 | PASS | 17.062304 | `d1a38229443c0e9264006566b4b35b9d8379099942f069c23826ca2a4fdc01a6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_site_transport_partition` | 0 | PASS | 4.651078 | `5133b897d38244c39ce2078ec92b898378198421cec2779c5f6b0d53e3cbd8aa` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_primary` | 0 | PASS | 0.234009 | `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_independent` | 0 | PASS | 0.181744 | `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Independent provenance, binding, and authority commands

The Git and artifact-consistency programs identified below were reusable,
source-inspected independent implementations from the preceding review
workspace. They were executed afresh against this 20260825 package; no prior
output was used as a premise. The archive, dependency-v2, and C02 programs are
preserved under this review's `independent_checks/provenance/` directory.

| ID | Label | Exact command | Cwd | Exit | Wall (s) | Max RSS (bytes) | Output SHA-256 | Result |
|---|---|---|---|---:|---:|---:|---|---|
| P01 | I-FRESH | `python3 -B independent_checks/provenance/audit_archive_v2.py --project isolated/k2p_principal_d_plus_submission_referee --archive source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip --output reports/provenance_archive_registry_timed.json --rebuild tmp/provenance/rebuilds/rebuild_c.zip --rebuild tmp/provenance/rebuilds/rebuild_d.zip` | `REVIEW` | 0 | 42.59 | 632,242,176 | registry `55be5239a28ccfd3546ed42175fea768ad0db1b15e4b6d74cce6f07dbc39eba1`; each rebuilt ZIP `ca08a3f50154610c7297ca83f92f0c9517fa5422ac7acf53b89582e1e14edbde` | Independently reconstructed every ledger path/hash/byte count and rebuilt the 484-file ZIP twice, byte-identical to distribution. Script SHA-256 `81235c09044d4a9596440fc3464bfa0a659642fe592882145a9119e97d0754b1`. |
| P02 | I-FRESH direct tool | `unzip -tq source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip` | `REVIEW` | 0 | 2.52 | 2,768,896 | no output artifact | Info-ZIP structural test PASS. |
| P03 | I-FRESH, reused/source-inspected checker | `python3 -B /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/audit_git_binding.py --repo /Users/alec/Documents/Math --project isolated/k2p_principal_d_plus_submission_referee --project-in-repo k2p_level2_identifiability_closure --revision 83821850e02bc6b6a0383dbc9d3d42ab24a261f5 --revision k2p-same-biorxiv-v1.0.1 --result reports/provenance_git_registry_rerun.json` | `REVIEW` | 0 | 4.88 | 723,894,272 | `d0381229893306b83abca4ddf92e82b5ebff46ff9716ef0c0c72f3573a3fe0b9` | 484/484 package files exact at final annotated tag; 473/484 exact at replay commit, with 11 later sealed differences enumerated. |
| P04 | I-FRESH | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_dependency_binding_v2.py --project isolated/k2p_principal_d_plus_submission_referee --git-audit reports/provenance_git_registry.json --interpreter tmp/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --output reports/provenance_dependency_registry_current_timed.json` | `REVIEW` | 0 | 0.53 | 77,201,408 | `b1dcce8dd2a9f45e2868215d31c5ebf447389583159589c625d46d357954e6ce` | Fresh current-venv probe: Python 3.14.6, NetworkX 3.5, SymPy 1.14.0; three dependencies exact; final tag exact. Stdout/stderr hashes not retained. |
| P05 | I-FRESH, reused/source-inspected checker | `python3 -B /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/audit_artifact_consistency.py --project isolated/k2p_principal_d_plus_submission_referee --result reports/provenance_artifact_consistency_raw_rerun.json` | `REVIEW` | 0 | 0.93 | 161,071,104 | raw `e78b3199656ac3502c239ffc7a699b60dbac0a86ac2c093705ca5af3663c6d3f`; normalized review registry `ad255e97a0ece3864c4bedfd3ee31f83ffed9f959426b559636097575d896c86` | 19 consistency groups and all 483 declared rows PASS. Normalization changed only the stale human-readable count label 479 to the dynamically checked 483. |
| P06 | I-FRESH | `python3 -B independent_checks/provenance/audit_c02_authority_v2.py --project isolated/k2p_principal_d_plus_submission_referee --output reports/provenance_c02_authority_registry.json` | `REVIEW` | 0 | 0.18 | 151,650,304 | `d132ebe102ec66719efb100e39724b864d0ca1b910de6aa59fc815555c835205` | 17/17 current-v2 scope, hash, lock, forest-census, and supplement-source checks PASS. Script SHA-256 `4d5d1b3d235c87d4563fb65d7a7b1b2f881f90d1b67e5030d5f1c4c0f2a31f91`. |

The earlier dependency rerun that explicitly named the preceding review's
qualified interpreter also exited 0 in 1.01 s with maximum RSS 76,300,288
bytes and produced the identical registry hash
`b1dcce8dd2a9f45e2868215d31c5ebf447389583159589c625d46d357954e6ce`.
P04 is the controlling current-workspace rerun. The review-owned aggregate
provenance registry is
`reports/provenance_reproducibility_registry.json`, SHA-256
`15a0808f42745d9233e028a3aa5e2ec6a0d72b240f6f9540ee10d763b776063e`.

## Fresh submitted package, crosswalk, build, and mutation entry points

These **S-FRESH** commands ran in a disposable extraction. Where no byte
capture or output file was preserved, the output-hash field says so rather
than substituting a payload hash for a raw stream hash.

| Command | Exit | Wall (s) | Max RSS (bytes) | Retained result/hash |
|---|---:|---:|---:|---|
| `python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.87 | 225,329,152 | 403 files / 478,865,262 bytes / frozen root PASS; this is a separate repetition of R04, raw stream hash not retained |
| `python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 10.56 | 502,988,800 | 227 rows, promotion ready, lock payload `dcc15b8ae2bb46674344595809690657119e5271611bab8c3c47fccade0fa509` |
| `python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 0.97 | 286,425,088 | 403 frozen + 80 submission files; combined root prefix `ab13…`; raw stream hash not retained |
| `python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.77 | 232,439,808 | manifest payload `1a4b0999d6c7c2cc6f4ff9cb322ab3189f90aa9b4cdf020464d666aa78148c81` |
| `python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.49 | 159,186,944 | 13 claims; payload prefix `c57a…`; raw stream hash not retained |
| `python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 7.26 | 597,491,712 | 31/31 resealed semantic attacks PASS; payload `0492a14d8efc310b4bed1e0d0217f4408ea5e3c827372be366582e7bc047efae` |
| `python3 -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 19.77 | 255,983,616 | both PDFs and both missing-generated-input gates PASS; payload `556ba6792d8dd1e27a3e35d52e306d74d835c1f8d35a49f698039127964dc94d` |
| `python3 -B proof_compression_submission/test_clean_full_replay_telemetry.py` | 0 | 4.67 | 27,230,208 | 9/9 fixture tests PASS; no report artifact |

The 27 R09 aggregate gate names were: `optimized_mode`,
`quartet_semantics_mutations`, `quartet_terminal_binding_mutations`,
`canonicalizer_completeness_mutations`, `parameter_transport_mutations`,
`omitted_raw_row`, `false_rank_exclusion`,
`corrected_raw4_overlay_mutations`, `theta2_full_map_mutations`,
`reassigned_quadratic_certificate`, `missing_theta2_seven_port_child`,
`corrected_primitive_composite_mutations`,
`corrected_restoration_v3_mutations`, `corrected_two_stage_probe_mutations`,
`promotion_theorem_status`, `promotion_quantifier_checklist`,
`promotion_pass_gate`, `promotion_zero_gate`, `promotion_ledger_path`,
`promotion_combined_root`, `historical_artifact_promoted`,
`historical_authoritative_replacement_removed`,
`historical_scanner_record_omitted`, `reassigned_cubic_certificate`,
`reassigned_quartic_certificate`, `reassigned_quintic_certificate`, and
`raw4424_false_tree_sunlet_reintroduction`. The portable report deliberately
omits child elapsed times, temporary paths, raw child output, and raw-output
hashes. It therefore supports the aggregate semantic markers and statuses,
not an invented per-gate argv/timing ledger.

## Independent PDF rebuilds and omission attacks

Only the five declared TeX/Bib inputs were copied into each clean build
directory. These are **I-FRESH direct-tool** executions; `SOURCE_DATE_EPOCH`
was 1787529600.

| Command | Cwd | Exit | Wall (s) | Max RSS (bytes) | Output artifact hashes |
|---|---|---:|---:|---:|---|
| `env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates main.tex` | `tmp/provenance/pdf_direct/run_a/article` | 0 | 2.54 | 253,247,488 | PDF `9934a92091d069c8764cf8c3aba6b496d482e4e0d5d0a526586f5a0d133f0411`; log `d243446067dd462d90921ddbb0b5891c1ae4509e3b710f6361f8b5f819dbe5e3` |
| same exact command | `tmp/provenance/pdf_direct/run_b/article` | 0 | 3.99 | 255,541,248 | byte-identical PDF/log with the same hashes |
| `env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates supplement.tex` | `tmp/provenance/pdf_direct/run_a/supplement` | 0 | 1.98 | 250,396,672 | PDF `66161998ec9b30355ac3f6f6467462e8be32230ee52ebf4fbfcaff77fe663866`; log `8859def133582903cd3f036af1145c1711581bb41ad9f33b2d6ef77f8a1f722d` |
| same exact command | `tmp/provenance/pdf_direct/run_b/supplement` | 0 | 3.36 | 251,035,648 | byte-identical PDF/log with the same hashes |
| supplement command after omitting `compression_tables.tex` | `tmp/provenance/pdf_direct/omit_compression/supplement` | 1 | 2.38 | 216,809,472 | diagnostic named the missing file; Tectonic log `301f5bf6ad7047dbe086972b7aaee080395ef5c939041f5173f7c8b3a30a1cd3` |
| supplement command after omitting `certificate_appendix.tex` | `tmp/provenance/pdf_direct/omit_appendix/supplement` | 1 | 0.85 | 216,842,240 | diagnostic named the missing file; Tectonic log `08ff533bbab3790a61916e92195dddd0e53d1c08c2e4a24bb356efe446bfa553` |
| article command after omitting `references.bib` | `tmp/provenance/pdf_direct/omit_bibliography/article` | 0 | 3.35 | 255,213,568 | Tectonic only warned; PDF `39ed798a74c29619d9ee5ffabecc980f75605e27e747c44e3fc8f370076f896c`, log `76a9e116bb49d4961321a9f5bfaad4f7bc800a4e95caf70f87cec44559673974` |

The bibliography result proves that Tectonic alone is not the bibliography
gate; the outer manifest rejection below is load-bearing. All 26 article and
24 supplement pages were also rendered and inspected. The complete contact
sheets have SHA-256
`a08bed0941f58e66cb743750f5302d0e1e5b01d96a333515caf8b4dd5c6752a8`
and `44b77ff53d9b2ff4a3fd03eb9c0ad8c9336cbf3a8f2d4d5ce9b86acd6fcac5bc`.
The renderer's precise shell argv/RSS were not retained, so this is recorded
as visual artifact evidence rather than a fabricated command row.

## Independent manifest, stale-input, and optimized-mode attacks

The manifest mutation generator was run as:

`python3 -B /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/make_manifest_mutations.py --source isolated/k2p_principal_d_plus_submission_referee/REVISED_REFEREE_BUNDLE_MANIFEST.json --output-dir tmp/provenance/manifest_mutations_v2`

It is a reused, source-inspected independent implementation executed afresh,
not prior output. It exited 0 in 0.07 s with maximum RSS 24,985,600 bytes.
Each current-checker command had the form
`python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest <absolute-mutant-path>`
from a disposable clean project.

| Resealed mutation | Mutant SHA-256 | Checker exit | Wall (s) | Max RSS (bytes) | Intended observed diagnostic |
|---|---|---:|---:|---:|---|
| omit bibliography | `76c1c834bc33523024f84e3b948c67f3e393a3b65e92b08521cdcd7633dc5e80` | 1 | 0.70 | 183,435,264 | submission ledger missing `proof_compression_submission/article/references.bib` |
| omit portable content ledger | `acba2ca5520a8f87d4afc2468f5c82e1287324db51a9fa0c8de73fa5f4c159d3` | 1 | 0.62 | 217,432,064 | submission ledger missing portable content ledger |
| stale article-PDF hash | `aaa9b7f36630af7340b91be511218d78df6c42cbeb73dca46a8dede9a497705d` | 1 | 0.66 | 213,696,512 | submission-ledger mismatch |
| stale full-replay hash | `5037df5143d564d9c13f74ffee74d8518c38b5beccb79dea79fd6680f10d0abe` | 1 | 0.59 | 213,401,600 | submission-ledger mismatch |

Optimized-mode probes in a disposable copy produced the following fresh
results. Exact stdout/stderr hashes were not retained. All commands used the
same ordinary argv as their named entry point with `python -O -B` substituted.

| Submitted entry point | Exit | Wall (s) | Max RSS (bytes) | Result |
|---|---:|---:|---:|---|
| `output/referee/build_referee_bundle.py --check-only` | 0 | 0.63 | 231,620,608 | accepted valid optimized run; nonblocking documentation defect because README says every entry point explicitly rejects `-O` |
| `work/final_theorem_release/build_release_lock.py --check --require-ready` | 1 | 0.09 | 44,630,016 | explicit optimized-mode rejection |
| `work/final_theorem_release/verify_final_theorem_release.py --quick` | 1 | 0.11 | 47,497,216 | explicit optimized-mode rejection |
| `work/final_theorem_release/run_release_mutations.py` | 1 | 0.11 | 48,873,472 | explicit optimized-mode rejection |
| `proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 1 | 0.05 | 23,887,872 | explicit optimized-mode rejection |
| `proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 1 | 0.04 | 24,150,016 | explicit optimized-mode rejection |
| `proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 1 | 0.07 | 29,573,120 | explicit optimized-mode rejection |
| `proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 1 | 0.05 | 23,789,568 | explicit optimized-mode rejection |
| `proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 1 | 0.04 | 22,970,368 | explicit optimized-mode rejection |
| `proof_compression_submission/build_clean_full_replay_telemetry.py` | 1 | 0.04 | 23,248,896 | explicit optimized-mode rejection |

On a disposable copy with a bound proof file changed, ordinary and optimized
portable-bundle checker invocations both exited 1 with the identical semantic
diagnostic `outer lock mismatch: work/domain_rooting_closure/PROOF.md`.
Ordinary: 0.50 s / 164,233,216 bytes RSS; optimized: 0.47 s / 164,577,280
bytes RSS. Thus the accepted clean `-O` run is a literal documentation defect,
but the tested corruption did not fail open.

## Direct retest of the former path-dependent source-writing defect

All rows are fresh; the extraction and test destinations were disposable.

| Command / attack | Exit | Wall (s) | Max RSS (bytes) | Retained result |
|---|---:|---:|---:|---|
| `unzip -q source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip -d tmp/provenance/disposable/relocation_alpha` | 0 | 5.50 | 2,981,888 | clean extraction |
| same command with destination `relocation_beta_with_a_much_longer_name` | 0 | 5.46 | 2,965,504 | clean extraction |
| `python3 -B work/quartet_separation_closure/test_quartet_semantics_mutations.py` with no `--output` | 2 | 0.06 | 25,985,024 | argparse rejection; wrote nothing |
| same runner with routine output inside its project | 1 | not retained | not retained | `QUARTET_MUTATION_OUTPUT_POLICY_FAIL`; wrote nothing |
| runner in alpha with caller-owned external `--output` | 0 | 2.32 | 70,385,664 | 8/8; report `reports/quartet_semantics_alpha.json`, SHA-256 `a1bf423637775b295fb1d6554401352834c59eab326798f7db4753a3855a4a9e` |
| runner in beta with caller-owned external `--output` | 0 | 2.30 | 70,287,360 | byte-identical report `reports/quartet_semantics_beta.json`, same SHA-256 |
| `python -B work/quartet_separation_closure/test_quartet_semantics_relocation.py` | 0 | 10.30 | 70,041,600 | eight relocation/output/collision/symlink/hardlink cases PASS |
| `python -B work/final_theorem_release/test_release_mutation_output_contract.py` | 0 | 0.33 | 48,922,624 | output report hash `a1f01d2ad623d09ca393e0b4e7bfc6b7c80600d4d4d973b948b00e6d7e695cff` |
| `python -B work/final_theorem_release/test_nested_mutation_output_contract.py` | 0 | 0.32 | 25,280,512 | nested writer output contracts PASS |

Fresh post-test source manifests for alpha, beta, and `ISOLATED` each contain
484 files and 483,053,523 bytes with the same review-format root
`4cf4cae6057aaae433ca768df531424d7ba0faa5719acffb645283ecb7bfc9a2`;
there were zero missing, extra, or changed files. This is direct evidence that
the previously reported source-writing/path-length defect is fixed.

## Additional fresh provenance actions without complete metering

These actions are recorded for completeness but are not assigned invented
runtime/RSS values:

- `sha256sum -c` on the external archive sidecar exited 0. The sidecar file
  SHA-256 is
  `021115cbca75aad96555256203147e05f3eb5ef5f3bb841394e69882413038db`;
  it names the distributed ZIP hash.
- The author's source-location ZIP and `source_archive/` copy compared
  byte-identical. `REFEREE_ARCHIVE_REPORT.json`, SHA-256
  `527e22e66c38539241f20f2448933e458bddbdcaee79552e56aea18a95a6c823`,
  agrees on size, member count, hash, second-build hash, and roots.
- Independent file/content reconciliation obtained: 403 recursively frozen
  files / 478,865,262 bytes / root
  `de6c2f7162164bb460bc608bffefb96b0494965c734c1063f304530a0cc36b82`;
  80 submission files / 4,090,352 bytes / root
  `923e8e0741557a013af2b480e4735894833ea4ff792c1e62aefe4f24dd2e0953`;
  484 complete files / 483,053,523 bytes; outer manifest file SHA-256
  `bebf82e4d0a406c129d38ceb2433583720bb24f5fea1f6f6ba5a1f05478ef0ce`.
- The final annotated tag `k2p-same-biorxiv-v1.0.1`, object
  `40980e2be87e3d5fcba8ce414f18f821492b099b`, resolves to
  `57f50ab46cde634b9450c5a01be4b3a12ba5a864` and binds all package bytes.
  This is provenance evidence only.

## STORED submission telemetry — provenance only, not fresh execution

The package ships a prior clean detached replay. It was inspected and
hash-bound, but its PASS was never used in place of R10.

| Field | Stored submitted value |
|---|---|
| command | `/usr/bin/time -l .venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --timeout-seconds 7200 --output <external-report-path>` |
| commit | `83821850e02bc6b6a0383dbc9d3d42ab24a261f5` |
| checkout | clean, detached (as asserted by sealed telemetry and checked against Git bytes) |
| stored status | PASS; 40 layers; zero blockers; promotion ready |
| internal elapsed | 5,428.031056 s |
| outer real/user/system | 5,428.67 / 5,923.09 / 31.66 s |
| max RSS | 2,548,498,432 bytes |
| peak memory footprint | 505,070,384 bytes |
| stored report | `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json`; SHA-256 `d26ce0841a50ebdc50a5e5d75a25ac2e12d9b647759051c8ceea29d803bd799e` |
| stored telemetry | `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json`; SHA-256 `dc4bd8faafef195a1fd7879b2c8ac7197ebb56cf8fee46c799ab0415b1e3ec08` |
| stored release lock | file SHA-256 `c319977f350923ab900a883235e32ec945d55a864338c14a08ce266ed3a1c78a`; payload `dcc15b8ae2bb46674344595809690657119e5271611bab8c3c47fccade0fa509` |

The scientific distinction is essential: R10 establishes fresh
reproducibility of the submitted 40-layer harness; I01--I07 and P01--P06 add
independent or adversarial checks with the stated boundaries; the STORED row
establishes only sealed provenance for an earlier execution. Neither hash
agreement nor a submitted verifier's PASS is, by itself, a mathematical
proof.

## Execution-level exceptions and limits

- The fresh outer full and quick runs passed. The computational-evidence HOLD
  arises from mutation semantics and independence gaps, not from an unrun
  package gate.
- R11 demonstrates a real false PASS in the canonicalizer mutation wrapper
  under missing NetworkX. R13 demonstrates that four transport mutants receive
  no structural diagnostic and are counted rejected only by changed bytes.
  R14/R15 invoke real production verifiers, but their wrappers still accept
  arbitrary nonzero child exits rather than binding exact diagnostics.
- The independent census proves the generated coordinate domains, ordering,
  counts, hashes, and referential closure. It does not independently recompute
  every analytic category or every all-family graph orbit.
- The submitted full replay's layers named `independent` remain submitted-code
  evidence and may share the atlas/canonicalizer. They are not relabelled as
  independently authored referee implementations.
- No substantive fresh execution documented in the preserved registries or
  review notes is omitted merely because it failed. Unknown argv, stream
  hashes, child RSS, or timings are explicitly marked unretained.
