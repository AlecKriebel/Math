# K2P-SAME theorem-layer evidence registry

This registry supplies the per-layer detail behind sections 3 and 5 of the
neutral referee report. Paths are relative to the isolated computational
project root. Every hexadecimal value is a complete SHA-256. Submitted
replays are evidence that the sealed computation reruns; they are not, by
themselves, mathematical validation. The crosswalk containing these bindings
has SHA-256
`918d9704469b016c7efc7c847dddb6ccc7da21c820d2259307729cf8c714d026`
and independently recomputed payload SHA-256
`ef596a50330766c126e7776c9fd8088260a42a129ca47ba16e50389e971f299b`.

## C01 — domain, subdivision, and rerooting

- Location: article source lines 300–413 (PDF pp. 4–6); supplement source
  lines 64–139 and crosswalk beginning at line 561.
- Status/evidence type: **PASS**; mathematical plus exact computational and
  provenance evidence.
- Authorities: `work/domain_rooting_closure/PROOF.md`
  `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
  `work/domain_rooting_closure/domain_rooting_certificate.json`
  `4e38beb68062deae8f83cd265daacbef8c5d3f6d73ce25ef47a54828b658d450`.
- Producer/replayer inspected: `work/domain_rooting_closure/verify_domain_rooting.py`
  `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b`.
- Observed command: final-release layer `domain_rooting`, exit 0, 0.057324 s,
  stdout SHA-256
  `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff`.
- Independent check: Fourier inverse, both strict domains, boundary-near
  rational points, serial closure, physical subdivision, and switching-wise
  root movement were derived exactly.

## C02 — quartet separation and topology direction

- Location: article source lines 414–461 (PDF p. 6); supplement source lines
  231–269 and 580–590.
- Status/evidence type: **FAIL** for the printed quartet body and its
  computational binding; structural direction evidence otherwise passes.
- Authorities: `work/quartet_separation_closure/PROOF.md`
  `629c58d44fbee452b2bf535821520354d4b2061a9f541a3543e741028eb4bd3a`;
  `work/quartet_separation_closure/quartet_logic_certificate.json`
  `e8d8542aacb672445777443712f1687a32c126eff070d342de9ae50e0aa24e29`;
  `work/adversarial_proof_review/topology_direction_certificate.json`
  `75ac5d4eebbde754f85e3cbf5de9d85e7e2f967bf72db02420e6637acf8087a9`.
- Producers/replayers inspected: `verify_quartet_logic.py`
  `edd0e42ffe14a4dbc30c685ad20dcb0d766547fe0dcefdd6a7ff51cc998c8ae1`;
  `verify_topology_direction.py`
  `299b88bae4f598ffa76fa5d83296c5578db01ba438277bcc40961a44c5c806d3`.
- Observed commands: `quartet_sign_logic`, exit 0, 0.033732 s, stdout
  `646d2e0a881888c2e9a63f8a8f724c85b74f535c2737ce858ed354a0ef46c066`;
  `topology_direction_structural_provenance`, exit 0, 13.932604 s, stdout
  `2cc12234d8b5f31fb40ce9a2164629261ca5dfd02778f0c2612a8abd2e3c4635`.
- Independent attack: the exact tree pullback disproves the printed `G/T`
  body at a strict continuous-time rational point; output
  `c6517e0659df6a13a970e94af6b238dec02afb95e417f61bd06ebaf94b649017`.
  Spectrum and coordinate-label mutations both survive the submitted gate;
  output `72a033e22826014cf260ae7e0d9766eb5feaab8406cf05fd2f1437dd9fbc76c0`.

## C03 — bridge fibre, marginals, and local product

- Location: article source lines 524–835 (PDF pp. 7–11); supplement source
  lines 397–425 and the crosswalk at 561–661.
- Status/evidence type: **PASS** for the bridge fibre and simultaneous physical
  gluing; exhaustive per-row transport semantics remain separately
  **UNVERIFIED**. Mathematical plus computational evidence.
- Authorities: `work/bridge_marginal_closure/PROOF.md`
  `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
  `certificate.json`
  `9231a7b78c13e54b745eba68926276a6551c6c3512d6a85746baba6613c1aacf`;
  `work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md`
  `b84af8f9f5a4c306e14f0d27e9fcd72dcce6608260ed6104e660734eb38b5d9b`.
- Producer/replayer inspected: `verify_bridge_marginal.py`
  `da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431`;
  `verify_adversarial.py`
  `0b8767b8b67200a977b49dae938be73ba829b7e89b51ce6a27d79205a08e3668`.
- Observed commands: `bridge_marginal_gluing`, 0.058313 s, stdout
  `554818967538c1ab104b693dead29a0da27a5d0fea1d711ac718d305993325d2`;
  `analytic_adversarial_audit`, 0.235693 s, stdout
  `18144e9db1caa747436777bd0f2ffbe18a10e27d5a6de73aeb74ed11c0582b48`;
  `global_component_scale_audit`, 0.156064 s, stdout
  `cedcbc2436f23dfced000232af0f777f9e42a52f7d88d134484215f7270cf344`;
  all exit 0. A fresh disposable 12-case analytic/domain mutation suite also
  exits 0 in 0.06 s with peak RSS 26,116,096 B and report
  `390976c38c6a1e00ca2490d5ef341f17cc9a13e72892dcb27a1d19cea315d172`.
- Independent check: exponent-incidence rank, analytic normalizers, absence of
  additional gauge/holonomy, exact marginal sections, and simultaneous strict
  `D_plus`/continuous-time gluing were derived separately.

## C04 — primitive grammar and completion counts

- Location: article source lines 837–1028 (PDF pp. 11–14); supplement source
  lines 141–229 and 275–339.
- Status/evidence type: **PASS** for the primitive domains and counts;
  mathematical counting plus independently streamed computation.
- Authorities: `FINITE_UNIVERSE_COMPLETENESS.md`
  `0604a331bc5112cae814aaae257296fa7f794bd1c3c7adc7f370ebc62e2a25bd`;
  `FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json`
  `66948b3d0f6c3c28e16ae7d70573ca78baa34c7173cd5d90264a5aed463fe7ef`;
  `corrected_universe_certificate.json`
  `c80c8781b968b21e1b001d51b6e71650ee74a326bb8b3f0aa56fc5997c224663`.
- Producer/replayers inspected: `derive_baseline_and_universe.py`
  `c14822a5f639b5cc0727980225dfaf359ccbbb5041ef7d0c747d200fe8de59a9`;
  `verify_family_coverage_equivalence.py`
  `d8630d17d5a2e0f843824b08bfc235944b31b07b40dea4c0cafbdd1410af87e7`;
  `verify_corrected_universe_independent.py`
  `ba916b95affd33a9121b72e6912e599be68d463838472e32fefc33c2177031ac`.
- Observed commands: top-level `family_coverage`, exit 0, 52.970895 s, log
  `65fc241b21530b35643b435177340adf2df56ead8b130d8765fe0b77f33ca936`;
  nested `corrected_universe_independent_replay`, exit 0, 9.512627 s, stdout
  `951b45954561825a1c2ff1ee6bd7242a6498d1c4e08a66c7c2bd99de204f3134`.
- Independent check: literal arc/repair index domains, minimal repair lists,
  ordered-word formula, raw-ID arithmetic and all requested censuses were
  rebuilt without importing the submitted generator or classifier; output
  `8f38e03b8caedabfaf738fd084a21ed73ec69efed33188bc8de593ce51672319`.

## C05 — raw-four exact-rank filter

- Location: article source lines 1030–1154 (PDF pp. 14–16); supplement source
  lines 231–338 and 662–698.
- Status/evidence type: **UNVERIFIED** globally; structural coverage passes and
  one exact representative passes. Computational and mathematical evidence.
- Authorities: `raw_ledger_summary.json`
  `07890bfb28e8aa3f3c6883e903911e7639264d86c9c99eef3acb2223b44217c0`;
  `rank_upper_coverage.json`
  `c52c5730494eb894360c17b6e54ae5c260fca3cddb8702d5c796750c7df874bc`;
  rank `manifest.json`
  `87068f8b0983d70c4ceef945d1b43165758e3f8f9949aa7d72af77a43aebc1bd`.
- Producer/replayers inspected: `generate_raw_ledger.py`
  `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44`;
  `verify_raw_ledger.py`
  `745ece3309128b0b0a5bb824e9811be946c40bee744cd99ebdc7d709f714e371`;
  `build_rank_upper_coverage.py`
  `b792efabbdf0d8a871bfb8a8526451b2f4c4e0f8209e75f654de6cc77b58d28f`;
  `rank_upper_replay.json`
  `c967917601f64803c96c1ba11cabc5fd3ea8d6021f9e55441c4210d9b886793d`.
- Observed submitted umbrella: `final_theorem_quick`, exit 0, 321.007619 s,
  log `28cbca4059deb3a43f1d8265cfefafd73164487a678f3d82ee49deb77faea492`.
- Independent check: raw ID 97 was reconstructed from literal graph edges;
  a separate Fourier map/Jacobian gave source rank 13, target rank 10 and both
  exact stored minors, exit 0 in 0.22 s, output
  `647b330b985fd635dce772162e4686fea092f59cd8f638d9ae79a3d1866a6370`.
  A complete alternative derivation of every symbolic upper body was not run.

## C06 — direct separator families

- Location: article source lines 1030–1154 (PDF pp. 14–16); supplement source
  lines 231–308, 427–441, 561–698, plus generated certificate appendix.
- Status/evidence type: **UNVERIFIED** globally; exact direct-family machinery
  and representative bodies pass, but quartet-bound terminals fail separately.
- Authorities: `DIRECT_CERTIFICATE_TEMPLATE_TABLE.json`
  `febc5e36c07e17dec1ba3dffb70dd0e4f4030dd796225d37dd0e7cc267485fe1`;
  `PRINTED_CERTIFICATE_APPENDIX.json`
  `7a24443f1583f1fc2ef57734c7845bc8377dc7da124265d1588f2d41e9555afa`;
  `certificate_appendix.tex`
  `ef878c24ff3f6b28d70b6c3dbf90c6d1e7d3c85a2bece621c96f47c409ca0ffa`;
  direct-36 certificate
  `d39ef18b8a58383c4f35aa9cc8fffc69d87928c77a27ddeb60c39b067e24fe21`;
  direct lock
  `89ebf377aa30fd27cd6480382fedcdd895519905f5accb51537a584b5dd8bc92`.
- Producer/replayers inspected: `derive_direct_templates.py`
  `0e53bcc6cfecf67c7d49d9e4f4b57deb1867537f969fd7812a22b8bbbb13fb02`;
  `build_printed_certificate_appendix.py`
  `a28fe156292f2af21092fe4a7d68ba983fe75e36dc95fcdf7332010b6f784bb9`;
  `verify_direct_closure_release.py`
  `08a188809833bc429053b01a2243542ab4a25e8b50a14409f82649e29160243a`;
  `verify_printed_certificate_appendix.py`
  `0bad09463df61ee235c523900caec35c952bf77b840a939615484268f1df835e`.
- Observed commands: top-level `printed_appendix`, exit 0, 4.213066 s, log
  `f9e4055cbed58fa8aef606155006aed29367fb592b9e4f027eb28ca78a31a7b8`;
  nested `four_port_direct36`, exit 0, 14.250650 s, stdout
  `6287724472f06313f24430de3a73782dc67d5cbdcc41501f7ea6aeac7a7c93a1`.
- Independent check: all 196 feasible direct equality/triangle presentations
  were reconstructed by a fresh incidence-graph implementation; output
  `a431ac1627b00dce9808333ca69037e603bc60e74d52224fdf41f0dd279f194e`.
  This is not an all-record alternative symbolic replay.

## C07 — corrected finite universe and terminal classification

- Location: article source lines 1030–1154 (PDF pp. 14–16); supplement source
  lines 214–338 and crosswalk 561–698.
- Status/evidence type: **FAIL** for quartet-terminal algebra; **PASS** for the
  independently rebuilt index/count contracts; complete alternative category
  and canonicalizer decisions remain **UNVERIFIED**.
- Authorities: `corrected_universe_certificate.json`
  `c80c8781b968b21e1b001d51b6e71650ee74a326bb8b3f0aa56fc5997c224663`;
  raw4 summary `515d6fea22d8388ab13c68066d0a57164b96baa684bf24b8f6da7da21bf6726c`;
  theta2 summary `5c0c7c091982b3ce235f0380eeb6e4531419bf7d3dcbfe44b9535f1b0e122086`;
  truth reseal audit `8ec6b987422b0dd27a12d590e8aad4f2c34817e341024f0881000013baffc3df`;
  composite reseal audit `bc91fee3b7541fcae72c4db2e66776fbfc69c43890718239f0eea41bb2cc0654`;
  family certificate
  `66948b3d0f6c3c28e16ae7d70573ca78baa34c7173cd5d90264a5aed463fe7ef`.
- Producer/replayers inspected: `generate_corrected_composites.py`
  `a117923e7b5cf90f0a13630fd21a6c454139f7e6e9c3c7bf84276229351a58ce`;
  independent composite verifier
  `67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690`;
  reseal verifiers
  `93f386c5ddb6dd355c6e510d0668f30fde3df5219fee70665c56e0c2135dd05d`
  and `238ffcea402fa74ab955df9fc73500e98d3c64f3d0ecb77441d1a081c2d997b3`;
  release-contract replay
  `c3166bf4127c5442b4fd842efcd39b63e6828ef36271514306f712306940479c`.
- Observed commands: `raw4_corrected_overlay_independent`, exit 0,
  87.035605 s, stdout
  `39b8b8ac590e4d8fe97d036d8a1e7ef3684015b5fe668b730e7de5338e0c0d09`;
  `theta2_full_map_independent`, 45.033877 s,
  `67554d8b2b254b986e03a711377bdc1f04ef97c9ce3468d8f28d992dd9cd49fb`;
  `cycle_three_port_structural_provenance`, 105.335744 s,
  `4468b3cfb464fa0b671d2e85d46b0dad34bfd49911671e7d8849056e67b85764`;
  all exit 0.
- Independent attack: all census/index contracts pass, but 360,408 raw4,
  2,942,592 theta2, and 535,920 cycle quartet bodies inherit C02's false
  algebraic binding.

## C08 — restoration forest

- Location: article source lines 769–835 and 1030–1154 (PDF pp. 10–16);
  supplement source lines 309–339 and 699–705.
- Status/evidence type: **UNVERIFIED** semantically; structural forest and fresh
  mutation behavior **PASS**. Computational evidence.
- Authorities: `corrected_restoration_forest.json`
  `43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8`;
  `RESTORATION_ARCHETYPES.json`
  `fa112b6bc051b3853f85f4156807252cac44f980f19bf2ed77d36f74a455eecd`;
  archetype report
  `1c110189118568cb80cce2b0fcc141cac43606c90324cb532ae6c463eaba2fc5`.
- Producer/replayers inspected: forest builder
  `55e7196b840b98334327e81b2583ab2105a8107ee9be308781b41187c9c7de6d`;
  forest verifier
  `e4cef28f156e1c300ed7b7cc48bb1a96f3a7686d92e2c748ec8dfa156d236f9e`;
  replay certificate
  `24fa2e61f60610a8b24c4107ec7f866278f0cc671ca203d7aaa40a37bea291dd`;
  archetype producer
  `8eacd74e892916f7cc7c17864c3ecfb5c2d19345caf63249ce162212d5c38073`;
  archetype verifier
  `7d3eed52f069c33af37c30e4d0f0eaed7616385247ffcd07dcb367a799a23281`.
- Observed commands: top-level `restoration_archetypes`, exit 0, 1.889020 s,
  log `6b04d764eefb26c5996cefcdf2cd30ff76e145eb99edbf8fd3641baf96f23673`;
  fresh 13-case disposable mutation suite, exit 0, 66.46 s, peak RSS
  569,540,608 B, report
  `79645c56cc0b4689eafcd7abc5f78f7854dac694e32a5915c905f557e7f1e6c0`.
- Independent check: all 997 parents, 2,540 roots, 36,824 edges, cartesian
  children, parent references, acyclicity, depth and terminal references were
  streamed. Graph-semantic reconstruction of every equality/transport was not
  performed, and quartet-labelled leaves remain affected by C02.

## C09 — coherent probes and reconstruction words

- Location: article source lines 1030–1154 and 1469–1528 (PDF pp. 14–20);
  supplement source lines 340–395 and 706–712.
- Status/evidence type: **UNVERIFIED** semantically; structural probe contracts
  **PASS**. Computational evidence.
- Authorities: `probe_coherence_certificate.json`
  `93de7b0dd3aa581bdf12288eae8cb9ac42f20a9d9bb3eab35eee8ef9a759d390`;
  `PROBE_WORD_THEOREM.md`
  `ab55aae4e0d0bba65927519d5970ba11f49e9ce211a051d40dfbf114a45d36ec`;
  `PROBE_WORD_COVERAGE.json`
  `a18410c360554426f0290ed9b85ce90f72fbdc76b8a4af67187971dd7ef067e6`.
- Producer/replayers inspected: probe builder
  `f0176e1759771a01ffa3da9e8d2b8967fc9189d3f93b30c6d06554bba9a77ddf`;
  main verifier
  `3facc1b51c133aa953f4a0cba86782672c86e78990d72ef2fc2aaa16a6f2a1bd`;
  submitted graph replay
  `51e2de1e8b1fe753a5b0605b3995ea02cfc7db4c3f83d7a3d39da51a116bba44`;
  word verifier
  `e4e76a2baa44804747997a1c68412d1ab10a9d2e4fb25532eb4eb50e4eb52d13`.
- Observed commands: top-level `probe_word_theorem`, exit 0, 13.598143 s,
  log `448fe21601314ed67705da883b2c07f4b9ea7e0b8ac1be22a472ac2699a2c707`;
  nested independent streaming replay, exit 0, 16.739453 s, stdout
  `0eb5a5fd0e1d6f6ad839619ffa21eece680d76f57033fe0825af6766ac544baa`;
  site/transport partition, exit 0, 4.749701 s, stdout
  `5133b897d38244c39ce2078ec92b898378198421cec2779c5f6b0d53e3cbd8aa`.
  A fresh disposable 15-case probe suite exits 0 in 172.97 s with peak RSS
  72,531,968 B and report
  `517138a25e210faa33caaef2dec6ae6b9a4b27ec5b61c268f4589181a86541b5`.
- Independent check: all anchor/site/row/transport/restriction domains and
  references were counted. Every graph transport was not independently
  reconstructed, and quartet-labelled probe rows remain affected by C02.

## C10 — tree/sunlet separation, triangle germ, and genericity input

- Location: article source lines 463–523, 1193–1319, and 1354–1468 (PDF
  pp. 6–7 and 16–20); supplement source lines 397–425.
- Status/evidence type: tree/sunlet and triangle germ **PASS**; the global
  genericity conclusion remains **UNVERIFIED** through C02/C11. Mathematical
  plus exact computational evidence.
- Authorities: tree/sunlet proof
  `f2feaaec71194a794b8b8b6b24a66866803a10fe12ce59a04e7688917b100cc4`;
  triangle-germ proof
  `25593e90d87286d7092b68ba5ac9bc176afba56d98b39becefafb1fe3becbc07`;
  no-assert certificate
  `b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885`.
- Producer/replayers inspected: `no_assert_triangle_sunlet.py`
  `c4a529336a0d409de30cf1c55f283e64628099424bd4191cfb7b31ec8995d7a1`;
  `verify_triangle_and_sunlet.py`
  `3b6c69caf6e72818fe5d931b1c30beabb7860c0c3686d300aff998c48741ccd6`.
- Observed command: `three_port_no_assert`, exit 0, 0.336323 s, stdout
  `c0f37ed9a0abdc26b229110ba56470883eda85e82eae5bb13578d675c54eef41`.
- Independent check: exact `T_i` factorization, rank-nine Jacobian, 4x4
  determinant `-1/2`, 5x5 determinant `-1/4`, contextual constant-rank
  sections and simultaneous physical gluing; output
  `4801dabb3f602761da9450560e9baae62c9061973c3365fafb809a9d17008e88`.

## C11 — global classification, genericity, and reconstruction

- Location: article source lines 1321–1528 (PDF pp. 17–20); supplement
  crosswalk and replay protocol at lines 561–833.
- Status/evidence type: **UNVERIFIED** because the load-bearing C02 premise and
  its terminal binding fail. The stored replay is computational/provenance
  evidence, not a cure for that failure.
- Authorities: promotion manuscript
  `d5e33c0ded1a8ae3ec3b7738e3166cb6d6afb7faff76c6bad0b759a0671a38cd`;
  completed probe binding
  `5e316301a53c6f437a3f6ad5f971e67846aaa13de67fd01978bbbc6f9efb9285`;
  release lock
  `58e32bd29f7a039e3da4e47398e32ee8277ad46cf62271a7ed80bf41688b18fb`.
- Producer/replayers inspected: release-lock builder
  `a49add912050dad8e11f16897010feae6269ff4405ae3ad019d02cf32437f683`;
  final verifier
  `1f197bf6e5d3704e6a9d25832f21454125a0fa5d4d0898fbc42db317dab8dd2d`;
  promotion gate
  `48f5522a70c4c0c5896c2d38382d0abb5ef2a93370bb217fac487fdbf6138136`;
  universe replay `09a445c725caee1d7447382ea261869c91f4ae5ff6b8a995ab2e8a4cf3047325`;
  stored full replay `7939b389880de80b7d8abd69022e0b69d2dc4188815854b294d3384fa24c9e18`;
  telemetry `8779854633d9a52ba3d7bc9278ccbcc3918e51987bb4c30204c0adcd9771ce16`.
- Observed command: `final_theorem_quick`, exit 0, 321.007619 s, log
  `28cbca4059deb3a43f1d8265cfefafd73164487a678f3d82ee49deb77faea492`;
  the one full command is recorded in the main report when complete.
- Independent check: both global implications, irreducibility/dimension chain,
  finite topology bounds, exceptional components, exact reconstruction loops
  and scope were reviewed. They remain conditional on a corrected/rebound C02
  and the explicit finite-evidence gaps.

## C12 — strict continuous-time transfer

- Location: article source lines 1529–1578 (PDF pp. 21–22); supplement guide
  and convention crosswalk at lines 64–139.
- Status/evidence type: **UNVERIFIED** globally; all local continuous-time
  domain, root, openness, separator, rank, triangle and bridge conditions that
  were independently checked pass mathematically.
- Authorities: domain proof
  `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
  gluing proof
  `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
  corollary manuscript
  `d5e33c0ded1a8ae3ec3b7738e3166cb6d6afb7faff76c6bad0b759a0671a38cd`.
- Producer/replayers inspected: domain verifier
  `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b`;
  bridge verifier
  `da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431`.
- Observed commands: the C01 and C03 commands above, all exit 0 with their
  stated runtimes and hashes.
- Independent check: strict rational continuous-time points, including the C02
  counterexample, were checked without floating-point inference. The transfer
  awaits repair of the principal-domain classification.

## C13 — weak-class sharpness

- Location: article source lines 1579–1789 (PDF pp. 22–24); supplement source
  lines 443–559 and 646–653.
- Status/evidence type: **PASS**; mathematical and two-route exact computational
  evidence.
- Authorities: sharpness proof
  `dcc36e0ae4299e3f0415d31e73522f224c91506f90062d0a13791af5746e9369`;
  certificate
  `e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd`;
  named-column crosswalk
  `827fc4a81b27da05916040e76e4de5b512c7a71e38577e495860a2cf63ee1af5`.
- Producer/replayers inspected: primary verifier
  `f0cab684609a89e2ab331643e15f6d516576b063f5acdff0f1cb134b5af8a3e2`;
  crosswalk producer
  `d8f82f03fbccb9426e3d1f9856e91c1bece58d6a4b24b882027657648a80c006`;
  independent audit proof
  `d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa`;
  audit script
  `e737fe3c0f0878c0284b0a55ebac1bfd3a7915b33278ab2916ed56bdf2200e5d`;
  audit certificate
  `cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52`;
  crosswalk verifier
  `e63b549ebf81046e0691d72b8eaf764b3289fecf387551ee2ee174f223e33afe`.
- Observed commands: `weak_sharpness_primary`, exit 0, 0.213568 s, stdout
  `9cf40181d0706f0c28b9d03bea0b151c9ac840b417e1c7059454dbdff1650ba1`;
  `weak_sharpness_independent`, exit 0, 0.184746 s, stdout
  `650dbdd6ca3d53ffef02e8dce76498edefe7415882068590e27de1e1ba74fe2c`.
- Independent check: both labelled graphs and admissible rootings, weak/not
  strong properties, non-equivalence, exact common tensors, named zero-based
  Jacobian rows/columns, determinant values, cherry inverse and `4n-3`
  extension were rebuilt; output
  `a18d67fd9858d217578df413714f3b9e9da88e0f39635f37003574806a3319d3`.

## Shared execution bindings

- Quick top-level suite: 21/21, exit 0, 778.96 s, peak RSS 1,460,994,048 B;
  ledger SHA-256
  `76236eebb4900c2aa3b616470d5a15fd9de9228c3fe0a5cdc43bd472bc9ef2cd`.
- The quick nested release log cited above is
  `28cbca4059deb3a43f1d8265cfefafd73164487a678f3d82ee49deb77faea492`.
- Full-suite values are intentionally deferred to the main report and
  consolidated execution ledger until the single uninterrupted command exits.
