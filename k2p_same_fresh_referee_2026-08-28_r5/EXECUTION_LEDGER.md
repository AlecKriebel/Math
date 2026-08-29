# R5 fresh execution ledger — 28 August 2026 package

This is the reviewer-owned execution record for the fresh review of the August
28 package. Process success is evidence, not a mathematical premise. The
integrated scientific status is mathematics **PASS**, computational evidence
**PASS**, byte reproducibility **PASS**, document/provenance consistency
**FAIL**, and overall recommendation **HOLD**.

## Environment and path notation

| Field | Observed value |
|---|---|
| Host | Apple M1 Pro, arm64; 10 physical/logical cores; 17,179,869,184 bytes RAM |
| OS | macOS 26.5.2 build 25F84; Darwin 25.5.0 |
| Python | CPython 3.14.6 |
| Packages | NetworkX 3.5; SymPy 1.14.0 |
| TeX / PDF | Tectonic 0.16.9; Poppler 26.08.0 |
| Review root `$R5` | `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5` |
| Pristine project `$I` | `$R5/isolated/k2p_principal_d_plus_submission_referee` |
| Disposable project `$P` | `$R5/execution/k2p_principal_d_plus_submission_referee` |
| Source ZIP `$ZIP` | `/Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260828.zip` |

The controlling rows below are reconstructed directly from the JSON execution
records. `max RSS` is the macOS child-process maximum resident set size in
bytes. An em dash means that a value was not sampled or retained, not zero.
All controlling stderr streams were empty and therefore have SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Controlling top-level commands

| # | Exact command | cwd | Exit | Wall s | Max RSS bytes | Observed coverage/result | Stdout SHA-256 | Report/result | Execution-record SHA-256 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `python3 -m venv .venv` | `$P` | 0 | 1.855579 | 97,550,336 | venv created | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | — | `302954571f377ec21af7f1ea510253fbb1212e77094abf2fe317d35d29cbd84f` |
| 2 | `.venv/bin/python -m pip install --upgrade pip` | `$P` | 0 | 1.091841 | 94,289,920 | pip upgraded | `718706568de9b06a27c22283e3371ff13caf160182c8064a49b6f642545ea1c7` | — | `9eb602f1b732385f7ddda75befa5dc8149aaef3333b90ac995817c8aad7dd18e` |
| 3 | `.venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt` | `$P` | 0 | 5.727744 | 176,111,616 | NetworkX 3.5 / SymPy 1.14.0 installed | `b8cb8888e74efb13d53a13b09a6cf6e18e4df64a873dd861491a02bfca6cf7e8` | — | `f885564fddcf23dafeb4735bddc51811784227b1d0411b41ea47df5365042159` |
| 4 | `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | `$P` | 0 | 0.611204 | 230,522,880 | 408-file portable closure PASS | `dc6c0926ed937e24ceb37058eb76ac13d92766a8bec912bf5ab0dcfb66b302dd` | — | `9979baa9f960040b49fa294bd84b0fd57fc31a90c4ef8100e05ac865511b41ec` |
| 5 | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --require-ready` | `$P` | 0 | 15.69213 | 516,063,232 | writing producer in disposable clone; rebuilt lock byte-identically | `bb9d6b5bf21a43180005985a86b450a882e3c9560fed05228ee16d049fc84032` | — | `971fe37b63efa13ca649289117e24b7ed24a43b0fcfd736f8254cc548e39751e` |
| 6 | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | `$P` | 0 | 17.158591 | 503,283,712 | release lock PASS / promotion ready | `58fb9da56b6d1d045d3b0df9a1899f76d67be2e8022bb12f230fc39d51b636d6` | — | `2dfaef2c04ed61bfd2493a866c1abb2a7e7e4c98134a5d4934dd40bb0310ea11` |
| 7 | `.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | `$P` | 0 | 118.470232 | 355,008,512 | revised bundle producer check PASS | `1fc00d24feab80f4d8a86ab240df1be8d652cf8f611156f5bb4cca61b94d327d` | — | `7fb0f2825bdba3b652ad37c821072eeb1848dc61ca27beb7c8e4604b985de4ee` |
| 8 | `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | `$P` | 0 | 121.019853 | 353,583,104 | separate revised-bundle checker PASS | `1fc00d24feab80f4d8a86ab240df1be8d652cf8f611156f5bb4cca61b94d327d` | — | `003f5c7d8c0edc281c1d28af800d2d4517dcd910eda55a15b6a93a68da08bba3` |
| 9 | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick --output $R5/evidence/computation/quick_report.json` | `$P` | 0 | 435.083181 | 1,457,586,176 | 23/23 PASS | `cbb9b0657dbaf8357b5d5a12a000ffea88310d4d41acd84819f37531ba7e98ce` | report `6dff8c349158986462af8566da548cb2bfb32e4159951af63d9a150d7e850234` | `93c8dbcd57432d56ebcad10e43a41dad8359161347ecfd4c46cbe65058776839` |
| 10 | `.venv/bin/python -B work/final_theorem_release/run_release_mutations.py --output $R5/evidence/computation/release_mutations_report.json` | `$P` | 0 | 4,367.74117 | 2,548,629,504 | 25/25 rejected; zero survivors | `704277209dd09d96ad164175a7525092570fdbca8411d0d5f1e598d5f032b728` | report `c14d30290eab72b07b4ff791550a42e5d71d083a860e93a482908e28c7c2ca38`; payload `5a1e8cc440d36e9da4c634e0c52a65a88f589e4e7abaad195f18fc7616ce4212` | `3ea9127ad6bd73f447fc49a5551ee12ed412910d5ecfa1b8c877c8094d518ce3` |
| 11 | `.venv/bin/python -B proof_compression_submission/crosswalk/test_strict_json.py` | `$P` | 0 | 0.037141 | 19,185,664 | 2 clean / 17 mutations PASS | `5efaf2b222f7ecaed14101d4a552a2320591b9faf89eeccf4ac424b3d60ec344` | — | `560813855693bd8c9bf39613e07813d78327495db63b3bc42f08afc66f8485ce` |
| 12 | `.venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | `$P` | 0 | 3,911.047525 | 385,236,992 | 37/37 rejected; duplicate-name repairs covered | `7be72305124618ad1739b165e5c62c23d818111a3d5e01a0d60cebb8caca2826` | shipped report `a49415da9daa15079b6e0528027826196e6f5a314728fdbfb8b8314df7447b80`; payload `0217ccc3cfdcb9f3142257aadf1ea0725f532e2389085b1df211c99cc031dfeb` | `6356b26e6da81e7bbc3cef8868928cb8a399b90df89123f5f73026d3aa2f864f` |
| 13 | `.venv/bin/python -B proof_compression_submission/verify_compressed_release.py --check` | `$P` | 0 | 0.079652 | 33,587,200 | compressed PC-PARTIAL release PASS | `02b2df45c8525bb21bde5f7f35ce65ce16fff4642a59abca61afd3c34b0213e2` | — | `ec84e66ca2fd0cda58a41ea74fecdcfa4cd3552ec123077575c93ad16e7d7c2a` |
| 14 | `.venv/bin/python -B proof_compression_submission/run_compression_mutations.py --check` | `$P` | 0 | 0.378017 | 39,124,992 | compression mutations PASS | `4e895b23a9ff06c7a6d77f5149a0bc33125713f194d7cfbb2cfbb61d8c70dcce` | — | `a1f1465e811d6ee2b390aea51d0cdb2daae7c82e96a6192fd16c8187c9317c4a` |
| 15 | `.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py --check` | `$P` | 0 | 124.548939 | 291,307,520 | old/new equivalence PASS | `b51274dc66bb655f50e2faf3315747400e4efbe2451999e9df31ec855bf5078e` | — | `73f9df94943458054e07940b91df8c3626d06adaf2eff8d0593573da1e87bc36` |
| 16 | `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | `$P` | 0 | 0.312538 | 174,669,824 | 13-claim crosswalk PASS_PC_PARTIAL | `998285a0dc40880457565f2bc8316aa6910a8205992a46899de702b601061ff5` | — | `db5efc83170ad1cef74415196de4a2de82010b206feea71aa55144e5f47e892f` |
| 17 | `.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py --check` | `$P` | 0 | 0.205209 | 41,762,816 | submitted static audit PASS byte map (semantic limitation separately found) | `b90f4d3ecd74284e58f77ecdc9b10260126ad8a80381eef00ada0bedaffd0022` | — | `1eb254f8e3679ec132f7340a44f8cf5640add8f85cdfe0a9cd88a5e27399d513` |
| 18 | `../../../.venv/bin/python -B verify_package.py` | `$P/package/referee/k2p_offline_sweep_portable` | 0 | 99.68701 | 1,503,150,080 | portable package PASS | `97ff420ab12479098ffd0903cd05ad70c4bed89ab9f0bbfd2544540a1544ddac` | — | `3a8559b7e7dfb5286798bab7bc4fea1c532791ae1bc746261b8ef2a07c0a35b1` |
| 19 | `.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full --output $R5/evidence/computation/full_report.json` | `$P` | 0 | 6,294.501465 | 2,548,678,656 | 41/41 PASS | `6c967f01d23d942b42c3eb6b4485f1731a8da529c780dd317fbd15292306bd68` | report `2f4fce76613bfe3f985ffdce37171854220e67330144e1705780d656211c4e9e` | `b3833be56e200bb1034a93181e6f939c1dc03cc5f508f8624b3f80f9126128d7` |
| 20 | `$P/.venv/bin/python -B independent_checks/math/r5_exact_math_checks.py` | `$R5` | 0 | 0.510515 | 66,895,872 | independent exact completion/domain/triangle/weak-sharpness mathematics PASS | `7784bfc8bd30f393794acbe9c588c5f1b060807bc6dc4c1356869823e010b68d` | result `5cf3cecf911e6464821b6417f3a04313cbd7feb635e5c82b051b7ddcf5842ca6`; payload `cd4fc393575618cdd4ca627413d140408d48dd75d6047b98b3d45f9fde9a9a87` | `f6304dfaf3b20c43ff728a1b916c652356e7c4164c6c3c0e498da29414e84023` |

## Quick/full child-layer reconciliation

The top-level harness actually executed every layer listed below. The submitted
report schema retains a stable layer name, exit/status, elapsed time, and child
stdout/stderr hashes; it does not serialize the child argv. The exact argv map
therefore remains inspectable in
`work/final_theorem_release/verify_final_theorem_release.py` (SHA-256
`6c2a6142e5a7c4fc092f16d5c3e52d0a4a00215f445d9facb199d557f7502ba0`).
Quick report SHA-256:
`6dff8c349158986462af8566da548cb2bfb32e4159951af63d9a150d7e850234`;
full report SHA-256:
`2f4fce76613bfe3f985ffdce37171854220e67330144e1705780d656211c4e9e`.
Both bind release-lock payload
`2a8d58662a45c1cb08973b7755a93259e091c0dab4a064891652883cabbf9a0b`.

| Layer | Quick status / s / stdout | Full status / s / stdout | Child stderr SHA-256 |
|---|---|---|---|
| `promotion_manuscript_guard` | PASS / 0.368201 / `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | PASS / 0.299482 / `8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `full_map_domain_reseal` | PASS / 0.124272 / `f54c4a337184e36575f82ac1af9a89fde7a2b60fe73db1d4d907c22561b313a4` | PASS / 0.110789 / `f54c4a337184e36575f82ac1af9a89fde7a2b60fe73db1d4d907c22561b313a4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_universe_independent_replay` | PASS / 15.923669 / `7cfd3f2eb796da8a64df24a7a79a4a328ed15abc1ef954e2803c5351d945bc56` | PASS / 15.424181 / `7cfd3f2eb796da8a64df24a7a79a4a328ed15abc1ef954e2803c5351d945bc56` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `three_port_no_assert` | PASS / 0.401108 / `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | PASS / 0.326975 / `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `domain_rooting` | PASS / 0.062869 / `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | PASS / 0.058264 / `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_sign_logic` | PASS / 1.116487 / `3d775e324c6c01fc66a5a62f99cd0bd0708b00b63095c54094a816db4c0f12a5` | PASS / 1.08367 / `3d775e324c6c01fc66a5a62f99cd0bd0708b00b63095c54094a816db4c0f12a5` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `quartet_terminal_bindings` | PASS / 81.236247 / `dde863b34b386440cf4cccb27c77150f3999ade5388bad67dea3173f92f143db` | PASS / 77.295511 / `dde863b34b386440cf4cccb27c77150f3999ade5388bad67dea3173f92f143db` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw_displayed_quartet_direction` | PASS / 3.137494 / `9127ddc5dc420396827fa228265879838e9284bbe7461368cc77472bf0e734fe` | PASS / 2.784805 / `9127ddc5dc420396827fa228265879838e9284bbe7461368cc77472bf0e734fe` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_structural` | PASS / 0.425958 / `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | PASS / 0.21161 / `7515bd2fc232683553554eda3867ce20df3b80a7ac6f4fab8dfd63f7ae8a38dd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_structural` | PASS / 31.428366 / `fcc72354add0c6a5154978663980f89fee98ada714d420f866769ad3a12711d6` | PASS / 29.002003 / `fcc72354add0c6a5154978663980f89fee98ada714d420f866769ad3a12711d6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge_marginal_gluing` | PASS / 0.084827 / `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | PASS / 0.062352 / `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `analytic_adversarial_audit` | PASS / 0.462716 / `2a2e22c51ac89be87e3b026fcd8079faf5f7eadd422397da68a81d810b9d525f` | PASS / 0.435975 / `2a2e22c51ac89be87e3b026fcd8079faf5f7eadd422397da68a81d810b9d525f` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `global_component_scale_audit` | PASS / 0.228048 / `a8433fa855d987a6d7bda3036014479ffb8a63b4825363ee42f6e73bbf726418` | PASS / 0.20121 / `a8433fa855d987a6d7bda3036014479ffb8a63b4825363ee42f6e73bbf726418` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_independent` | PASS / 95.321271 / `83bf82db6c8cddc5bc13ae9f4dca52f2a00a0bdb572d5d7c96c9672f4fab2411` | PASS / 89.71254 / `1a0b6e8eab94ca2ed12dd884a934daefb094bf5a6b0ded373eee03b851a7f0cf` | `e6e3956dc79c5b4fd93d3cd9178b3e8617dc54b0f43f1ab0ac209a3f9fa0c083` |
| `theta2_full_map_independent` | PASS / 66.670364 / `0ef4fdef4ffe9059ddc346e53996ba29f861938d5a8514dfb3f7ce4c8e2b9fd9` | PASS / 63.915761 / `65b01ac8a630ddc306af70ea82b8b37a518c5dcc06d0e4f35c20f9a3eeebec28` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_raw_structural_provenance` | PASS / 4.113981 / `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | PASS / 3.96909 / `d7475cfbfbbb911b3acb2685703ae995a43a52046c4702b89993203c1d1a3706` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36` | PASS / 18.618986 / `b792ab5f5eca3737c2f92f0cd251dc25685d100524141cac8ecbee6e25a8d800` | PASS / 16.97243 / `b792ab5f5eca3737c2f92f0cd251dc25685d100524141cac8ecbee6e25a8d800` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_structural_provenance` | PASS / 30.327924 / `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | PASS / 29.722199 / `0b59cde4ce11aa5dc6cc44b7b58d66b2d6a1b48e6b06f856c84e3a5a84eb8bc4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `cycle_three_port_authoritative_promotion` | PASS / 26.933569 / `254d8dae0e19636f20cb1718007725e6e484711a828633b22d31e4b3090e2781` | PASS / 25.494439 / `254d8dae0e19636f20cb1718007725e6e484711a828633b22d31e4b3090e2781` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_streaming_replay` | PASS / 26.216995 / `e10c878db794c7c296c4dc08bd735f82dfbd0267564b4ccf8631b4081dd96439` | PASS / 24.701273 / `e10c878db794c7c296c4dc08bd735f82dfbd0267564b4ccf8631b4081dd96439` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_site_transport_partition` | PASS / 12.778886 / `fed2eea6ec9162c3fa4302a1603e164abf9e940c0635bb582accf179a84a38ed` | PASS / 12.194012 / `fed2eea6ec9162c3fa4302a1603e164abf9e940c0635bb582accf179a84a38ed` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_primary` | PASS / 0.246095 / `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | PASS / 0.209162 / `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `weak_sharpness_independent` | PASS / 0.217998 / `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | PASS / 0.171789 / `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `canonicalizer_completeness_full` | — | PASS / 105.16221 / `dde7a6df548d407df5cedb2810549aac0711269718ba203c9ddbd45461675188` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `graph_derived_parameter_transports_full` | — | PASS / 310.08085 / `4e9007b2086809e76cb00c31a68e13a8c8998a9a1d968f82dfaf7621a1e75363` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_restoration_independent_full_replay` | — | PASS / 466.395262 / `bcb143e46f2f57c6a90e921f387b3b59ec6e5bd8795e1fcb3bc8eb4f288649c1` | `7bb69d81f6d45d866e3030dda574eb3b5056c637319c017fc12ee4b3c10fb1da` |
| `corrected_universe_cross_layer_mutations` | — | PASS / 316.062604 / `ff0d551c9ea9f78568f495d4f0b9fc01d5afaeca979174cce4a69ccb89382ff7` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_full_map_Ti_truth` | — | PASS / 21.146282 / `f95c1e2d59974d8a3faf42ee63d3fe389de3c3baffef9b374b8939812ab50423` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_full_map_Ti_truth` | — | PASS / 89.331729 / `cec14bbbe0712b53c033610d754b101c6ccce0c98d4e42536121083d86fa5ebd` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `composite_domain_reseal_diff` | — | PASS / 77.44642 / `d214d2df286b6ca780476fe40372eb88eefde13b1ab0d78f82b0af629d4dd0ca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_exact_rank_staged_atlas_omission_mutation` | — | PASS / 0.317321 / `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `b7aec20635849f1cd1ccd4881875d00a97bda898d04bab0a2523c0f521943770` |
| `four_port_exact_rank_import_preflight` | — | PASS / 0.348709 / `79d039353c2a88425952fe6ffd8e67653c512de65e89b2ab6f22b46e5ee72212` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_exact_rank_full` | — | PASS / 120.181701 / `8139abc270327787b8f8afb39ff566fd88805c24ba53995166ba71c79692e784` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `raw4_corrected_overlay_full_regeneration` | — | PASS / 62.527349 / `4c51979cd98bd4e8835b170780982e7541948c1a2cf8d96e63801dcf242ce1f3` | `de1f579aafe4aa7f4d84e6f47f6b6ca9aba263df850de2b6839abc89018dfb8c` |
| `four_port_raw_full_regeneration_provenance` | — | PASS / 314.275196 / `8eb91f720fe064d3007c5f2f4a65295b921c068285b1fad9db3d3710ae3f55c6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `four_port_direct36_full` | — | PASS / 110.098491 / `a3758962638af6df263c9fa40dab3e26bf41881761c9f94ae129345609ec7f65` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `theta2_full_regeneration_provenance` | — | PASS / 492.756508 / `82c6917c4503a2cb7d3c42988100a58731dff13c8972a45b27ffbb5226bbd783` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_full_primitive_regeneration` | — | PASS / 2,919.442297 / `1664163725018b35688415340a3f9c1e1d14964680ad7bd94cdb9a84142fe902` | `484f841e7a07d0f80daa0e26ae38ad7b1cda1bae6ca9508e3fef8e86a7ce80ac` |
| `corrected_probe_full_independent_replay` | — | PASS / 23.749864 / `e10c878db794c7c296c4dc08bd735f82dfbd0267564b4ccf8631b4081dd96439` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_full_site_transport_partition` | — | PASS / 11.843967 / `fed2eea6ec9162c3fa4302a1603e164abf9e940c0635bb582accf179a84a38ed` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `corrected_probe_independent_primitive_graph_full` | — | PASS / 442.270397 / `42a7fe23231c17994c3aa4c83a11e0289cee00039ba61fac255069c0f4791891` | `cbc56ffd93ed354a5cd9adfa22ebe130b83db6b8822b4fc1adc29c66e71e7602` |

Quick: 23/23 PASS, internal 434.524088 s, wrapper 435.083181 s,
wrapper max RSS 1,457,586,176 bytes. Full: 41/41 PASS, internal
6,294.018177 s, wrapper 6,294.501465 s, wrapper max RSS 2,548,678,656
bytes. The full job was launched once and awaited without repeated invocation.

## Additional independent and duplicated checks

These rows were preserved by the provenance/computational subreviews. They are
separate from the controlling JSON-wrapped executions above. Commands shown
with `/usr/bin/time -l` have retained timing logs; commands timed with
`time -p` did not collect peak RSS.

| # | Command / cwd | Exit | Wall s | Max RSS bytes | Result | Stdout SHA-256 | Stderr SHA-256 | Result SHA-256 / payload |
|---:|---|---:|---:|---:|---|---|---|---|
| A1 | `python3 -B independent_checks/provenance/independent_provenance_audit.py --project $I --archive $ZIP --git-repo /Users/alec/Documents/Math/k2p_level2_identifiability_closure --output evidence/provenance/INDEPENDENT_PROVENANCE_AUDIT.json`; cwd `$R5` | 0 | 146.07 | 445,562,880 | archive/ledgers/tag/telemetry/strict JSON/PDF report PASS | `ac7f45d6b16ff0f76205456ff29f8d4acae6bd17211935f48684550b7aa4b7a7` | `ee7f2565e52e8e4798f51f8869ea09a41675f35ba545628e538edfd4cae1237a` | file `da8178e13da9fa24843c99d7fc06d9dbc4e3932e539157a6a2b6088b5ddef931`; payload `e481e0a51550e11627c416d327dd6ce8e060800349cd4ac29537bc870738f0aa` |
| A2 | `python3 -B independent_archive_rebuild.py --project $I --output tmp/archive_rebuild_a/referee.zip`; cwd `$R5` | 0 | 21.08 | 273,842,176 | 495-file ZIP equals source | `765d8846e0b4d666aa0929f6f3f435801e0988a1d2c0c014be76dfbd25db557b` | `0accffed551cf3daa1378e7f7711c79fe243a73489f53b9af602c187f2ab9a59` | combined rebuild record `eabcf286a49e2d9072e57403894c33662beafc88416e0a30e34946da22286b22`; payload `139c840c9b1e260ee8bb196217e13b1d0d410cbbed36b51a4f073bae8ae57f69` |
| A3 | same builder, output `tmp/archive_rebuild_b/referee.zip` | 0 | 21.07 | 272,596,992 | equals A and source | `26db20dfcfb1cfa2e83358f40697092d2a8c8da801988e0836a30e7b8d4f1a93` | `ca194cf19a053df1e9fc09aed14b7e92f2cdbd40a72ff4e56dde237c1f2dc264` | same combined record |
| A4 | `python3 -B independent_checks/provenance/semantic_anchor_audit.py --project $I --output evidence/provenance/SEMANTIC_ANCHOR_AUDIT.json`; cwd `$R5` | 1 (expected finding) | 0.54 | 222,593,024 | **FAIL: 37 semantic/current-hash mismatches** | not retained | not retained | file `a96b8549a5f77176ba638170c9e549a099c525387a0d3ec6226a69e33cf77de9`; payload `7966d7b885e32486f3599df05d544d57961e6a1253c8c066736bcf3a8020aa6a` |
| A5 | `python3 -B output/referee/build_referee_bundle.py --check-only`; cwd `$I` | 0 | 0.64 | 230,703,104 | independent duplicate invocation PASS | `dc6c0926ed937e24ceb37058eb76ac13d92766a8bec912bf5ab0dcfb66b302dd` | `a801cf4dee013384548496957996012515d59a5058a571393f5c10ef7fd8712a` | — |
| A6 | `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready`; cwd `$P` | 0 | 16.91 | 509,837,312 | independent duplicate invocation PASS | `58fb9da56b6d1d045d3b0df9a1899f76d67be2e8022bb12f230fc39d51b636d6` | `c8325cd10e481e97469dcdcc877ecdf5cb7046407b5628602f9b439a0b9f04cd` | — |
| A7 | `python3 -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check`; cwd `$I` | 0 | 127.67 | 272,596,992 | producer check PASS | `1fc00d24feab80f4d8a86ab240df1be8d652cf8f611156f5bb4cca61b94d327d` | `0f142f4c60e79446b63b0a5820b8f3eaed04d375470b8f2eb13f9215ed5ad661` | — |
| A8 | `python3 -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json`; cwd `$I` | 0 | 129.37 | 268,173,312 | separate checker PASS | `1fc00d24feab80f4d8a86ab240df1be8d652cf8f611156f5bb4cca61b94d327d` | `5912b456e2a9c03367b47e1e70fc0783a25b63c287a1651515e387c0324d397f` | — |
| A9 | `.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py --check`; cwd `$P` | 0 | 0.74 | 42,631,168 | byte-map/static audit PASS; does not catch A4 | `b90f4d3ecd74284e58f77ecdc9b10260126ad8a80381eef00ada0bedaffd0022` | `91696dce86d484eb855a77df4576abb44808f9527c8bb7d4d2750180b4ecd660` | — |
| A10 | `.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check`; cwd `$P` | 0 | 0.43 | 176,734,208 | 13 claims / 173 rows PASS_PC_PARTIAL | `998285a0dc40880457565f2bc8316aa6910a8205992a46899de702b601061ff5` | not separately retained | crosswalk `1430e065692c0c40d6fbd319daf913701ca9fb8bfd6faaaade3457ce5e4b75c5`; payload `ed8c4ebbdaf76e20774653801930dff6e6ea50a847bbf11a53718965f91d1f55` |
| A11 | `.venv/bin/python -B proof_compression_submission/templates/verify_printed_certificate_appendix.py`; cwd `$P` | 0 | 12.31 | 162,889,728 | 23 quadratics, 5 bases, 36 transports, 3 examples PASS | `74c2e8f13a3cd35b4a6556826388ae87c416a382812f0e048579843fe9729c61` | `3dd06c7e61b3d13d9da6e829f9ee87f4882333fff45b6deba2198cae086f4a91` | payload `e2df6cefd697d5bd28277f8760808444620ccf281ecac3f84a8892372f24de54` |
| A12 | `.venv/bin/python -B proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py`; cwd `$P` | 0 | 0.31 | 44,695,552 | exact named columns PASS | `08119dce7f8892abd89c1a3ca73da91f8e3d1c83c3da76b4424eb9332ce3f550` | `565d6b96196d5c866981e85fd0d8cb6fd3c0187193e7bbd88abea01e00fda986` | authority `a6629eba036b93170d27cbb72ba04cd30b9b8c0b221f81ec4f450ca9ee6eb058` |
| A13 | `.venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check`; cwd `$I` | 0 | 3,884.99 | 391,577,600 | independent 37/37 PASS invocation | `7be72305124618ad1739b165e5c62c23d818111a3d5e01a0d60cebb8caca2826` | `a1e91ee7e6ee5a98efa5d86892527b8852ed5ecb93f6634eeadef5b4d4341125` (reported; timed log not retained) | report `a49415da9daa15079b6e0528027826196e6f5a314728fdbfb8b8314df7447b80`; payload `0217ccc3cfdcb9f3142257aadf1ea0725f532e2389085b1df211c99cc031dfeb` |
| A14 | `.venv/bin/python -B package/referee/k2p_offline_sweep_portable/test_optimized_entrypoints.py`; cwd `$P` | 0 | 2.86 | 151,076,864 | all 18 entrypoints reject `-O` and `PYTHONOPTIMIZE=1` | `4b25654b34ece9abe5f14dfca1da1a45bde74507d37c88b21e8a59c6a9593e46` | `7f3c3335ded4f01a9b119a2239b6b62a762bc9651916ef3745ffb0e10a4dd8a5` | — |

## Reviewer-owned computational attacks

| # | Exact command / cwd | Exit | Wall s | Max RSS | Result | Stdout SHA-256 | Result SHA-256 / payload |
|---:|---|---:|---:|---:|---|---|---|
| C1 | `python3 -B proof_compression_submission/crosswalk/test_strict_json.py`; cwd `$I` | 0 | 0.04 | not sampled | 2 clean / 17 mutations PASS | `5efaf2b222f7ecaed14101d4a552a2320591b9faf89eeccf4ac424b3d60ec344` | — |
| C2 | system Python optimized-entrypoint matrix; cwd `$I` | 1 | 1.86 | not sampled | environment-only `networkx` absence; no package conclusion | not retained | — |
| C3 | R4 review venv Python, `r5_fail_closed_attacks.py --project $I --python <same venv> --output ...`; cwd `$R5` | 0 | 25.45 | not sampled | duplicate names, optimization guards, false-kernel invariants PASS | `2d036d0241a944b0939e21ec9e2f0a5e2438245641abc3216ac209e745625404` | file `3dbaa595b7a2e1c711f98821f5c187f57f2ac385bf64f0166fca9a5e0da3e50d`; payload `b7403bf7b5076a8645fa1777d8ab0e80eec0a31a705bfa996c38e739be7e2559` |
| C4 | R4 review venv Python, `r4_independent_semantic_attack.py --project $I --output r5_independent_semantic_scan_result.json`; cwd `$R5` | 0 | 221.73 | not sampled | primitive/raw/cycle/restoration/probe joins and counts PASS | `84ef04d16f75743a1a77a0c852d59e11e3aa450d2bb7fa04994abec4c7925b9d` | file `22ef5fcd2197d791fc5a4c6cff61672978f50cfd93e11ca405cbda7e46214cd3`; payload `ce04ed741461d9f193be7df96fee9ca0b5c160217c1c6b57e59f859a1836431d` |
| C5 | `python3 -B r5_compressed_json_audit.py --project $I --output ...`; cwd `$R5` | 0 | 157.39 | not sampled | every compressed JSON/JSONL object unique and canonical | `fe913b41f29bc0650cfa0d816ebde36f30069192f048ec82142cebbbaab78817` | file `dda6fd9c283a53e9a08fe8ca961051ef89bf927f571554e6c82f8d0a1507c37e`; payload `0ae7ebaf67ab86923fe8d522a0b1ccd2d2b261a273772b84bed776d91d61e42c` |
| C6 | `python3 -B r5_manifest_projection_compare.py --baseline <R4 complete results> --candidate <R5 complete results> --output ...`; cwd `$R5` | 0 | 0.28 | not sampled | all 1,931 semantic projections equal | `b48e6043d2663db20e11e8a7c7b44984a85022e780885c40097e39ba93cf8baf` | file `d04ffce1d5597e75fce7616780aa6fbd0cf8515992fdebca47a9fd1cbf51c4cc`; payload `a57ce847db833cd8df3902211152da5135dd2fe0864ef4639f126c45df6d4594` |
| C7 | submitted `compare_semantic_runs.py` without `--allow-partial`; cwd `$I` | 1 | — | — | intended rejection: 36 records are not complete 1,931 sweep | not retained | — |
| C8 | same comparator with `--allow-partial` | 0 | — | — | 36 shipped complete direct records equal on all 19 fields; root `201a616e...` | `f02c2695f246df709e464d8e4aa03586164c2961b6c0322f27e8d16b2a94f445` | — |

The broad graph scan reuses a review-owned R4 method (script SHA-256
`41760fb53167599e5ddf0258b628c189845141839653bf635af77f6943b13b4c`)
on the R5 project. It does not call the submitted classifier or release
harness, but it shares the submitted primitive grammar/serialized graph
conventions where reconstructing the same finite universe necessarily requires
them. No submitted second symbolic engine independently re-expanded every
high-degree polynomial body.

The mathematical subreview combined retained hand/symbolic derivations in
`notes/mathematical_review.md` with controlling row 20. The latter imports no
submitted code, classifier, graph generator, ledger, or expected file and
independently checks exact completion/raw counts, boundary-near domain and
section arithmetic, the triangle blocks, both weak-sharpness determinants,
and the cherry determinant `2464/675`.

## PDF/source/build commands

All four successful builds staged exactly the five declared source files into
separate review-owned scratch trees and used
`SOURCE_DATE_EPOCH=1787788800 tectonic --keep-logs <document>.tex`.

| Operation | Exit | Wall s | Max RSS bytes | Stdout SHA-256 | Stderr SHA-256 | Result |
|---|---:|---:|---:|---|---|---|
| Independent PDF/source consistency audit | 0 | 0.38 | 26,509,312 | `45ab50f93b9be3197d54f09d6d8e5458a8abb5de0a0a38f1e0c80276b29533ca` | `07e364d213c83e59d3ebd449e882792a3b8452fadaae79d6f44fc66b10e83512` | result `48ed02d95f19631f4e2562f3da795eba775bc284d8357562d9134af1675ba81b` |
| Submitted PDF builder `--visual-pass --check` | 0 | 13.93 | 254,476,288 | `f60d5968b6f14c8a2e6bd2da28bc6ff9588d91048cca9ffb3dde488d0bc60898` | `1501e3b25d18afa18b22869427162d18e1bbe1902b1ef70ed7af65eba0eec729` | exact report payload reproduced |
| Rebuild A article | 0 | 3.15 | 249,020,416 | `e4035dc240c361e6ce3a46ef261c893cd5b77e44a4c94eda89ed0cb12313c400` | `176fee8a730187e3a294f29f308de08517c2f7c7d53c7adca2843b328dfc4526` | byte-identical |
| Rebuild A supplement | 0 | 2.51 | 245,596,160 | `71f35246f611e7a1d8983ec3674bafded6bfa394b03a97b2c173d0198ac0c0d7` | `c8bdbd6f0976835cb9e981d1b7e95717e82097bf734a8516325d014548930434` | byte-identical |
| Rebuild B article | 0 | 3.09 | 250,249,216 | `382bf1687d080125e76a2ba599a6bbeff22aa7b0e5e18d18bbb86bad7d271989` | `55b10040463a5a5224a9afd936deaf99204540b3f5e264315fb78a559d123b25` | byte-identical |
| Rebuild B supplement | 0 | 2.46 | 250,003,456 | `a2aaff4eda6ce45bd20d321e8569c606ea4b635ef79b0f0061697cbfe7efcabd` | `77d5763d77d6b0d0390519f955dbaadf9624941e63a24ffbdeff8083c802476c` | byte-identical |
| Omit `compression_tables.tex` | 1 | 1.43 | 217,006,080 | `0a6161b17697bef0fe63029b6fb97254c30e75f8fa3dd33206a614f3077f84e3` | `28a8e62f11c8f5c96e352b7424e6b0c885f990ac583524384eb5138129add85e` | intended missing-file diagnostic |
| Omit `certificate_appendix.tex` | 1 | 1.39 | 217,317,376 | `8a7697e69297f0a5b5b8868c72de130422c77617dc9befe9532e0c7d95f3e241` | `1f7c71a13cbd7fd5c4e843f7a1935ecadfc0b54337216e23d60ebcf1abd51774` | intended missing-file diagnostic |
| Render article 26 pages | 0 | 4.30 | 17,661,952 | empty SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `ffcfca90b12873d2893156ad717473ad3f6862195085abcb2170353c7c4a8158` | all pages inspected |
| Render supplement 24 pages | 0 | 3.42 | 17,350,656 | empty SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `d7db151d08b750bae1bbc027b02cca761de37c45718bf90f90617a3137892406` | all pages inspected |

Document result SHA-256
`65ac9f6add5f99a1bc6d5800acc8e3cbaadbaa1b94774ffdb598d1613aed59d5`,
payload
`b17a7da731bf595e7cad406f9422a538bcb17d6b579a664c5b555e964ddae4ef`.
The source/output build report itself is
`6bd098c65d59a889dcdda28342c0a5954c1fea53d7e3521809ee9bfefb30afd4`
(payload
`a3c6b81b053be86811d56bb763a8a139c4d5e03cdf78a06da36887b2aa982d46`).

## Mutation report reconciliation

- Final release suite: 25 required/observed, 25 rejected, zero survivors;
  report SHA-256
  `c14d30290eab72b07b4ff791550a42e5d71d083a860e93a482908e28c7c2ca38`;
  payload
  `5a1e8cc440d36e9da4c634e0c52a65a88f589e4e7abaad195f18fc7616ce4212`.
- Crosswalk/bundle suite: 37 required/observed, 37 rejected, including
  same-valued/conflicting duplicate plain JSON and compressed JSONL,
  noncanonical compressed JSONL, and omitted bibliography/dependencies;
  report SHA-256
  `a49415da9daa15079b6e0528027826196e6f5a314728fdbfb8b8314df7447b80`;
  payload
  `0217ccc3cfdcb9f3142257aadf1ea0725f532e2389085b1df211c99cc031dfeb`.

## Unrun gates and exact mappings

The following legacy names are absent from this package; the current mappings
were executed:

| Absent legacy name | Current mapping | Fresh disposition |
|---|---|---|
| `START_HERE.md` | `output/referee/README.md` and release README | read |
| `setup_environment.sh` | the three explicit venv/pip rows above | all exit 0 |
| `verify_handoff.py` | bundle check, release-lock check, quick harness | all exit 0 |
| `test_handoff_mutations.py` | final release and crosswalk mutation harnesses | 25/25 and 37/37 PASS |
| `run_all_verifiers.py` | full harness | 41/41 PASS |
| `SUBMISSION_BINDING.json` | `RELEASE_LOCK.json`, bundle contents, revised manifest | independently reconstructed |

No required current scientific gate remains unrun. Deliberately unrun actions:

- authoritative write/reseal modes in the pristine copy; check modes and
  disposable writing producers were used;
- any external message, remote mutation, publication, release, DOI, or Zenodo
  action;
- signed-tag and remote-host availability claims (the local annotated tag,
  tree, blobs, and ancestry were checked);
- unclaimed second all-family orbit implementation independent of both the
  atlas and its grammar, and unclaimed second symbolic expansion of every
  high-degree polynomial body.

The two rebuilt ZIPs and transient TeX/PDF scratch outputs were deleted only
after byte comparisons and evidence hashes were recorded. No isolated package
file was edited.
