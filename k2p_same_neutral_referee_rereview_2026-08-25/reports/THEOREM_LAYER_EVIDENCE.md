# Theorem-layer evidence registry (fresh 2026-08-25 rereview)

This registry records the evidence actually checked for theorem-artifact claims
C01--C13. It does not treat a stored `PASS`, a matching hash, or a release lock
as a mathematical premise. Package paths below are relative to
`k2p_principal_d_plus_submission_referee/`.

## Evidence and location conventions

- Article source: `proof_compression_submission/article/main.tex`, SHA-256
  `ca6dd8d750768b0c47121c8bd60c5c9c3223af194139f5f578cb8bbf5fd5c3f1`.
- Article PDF: `proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf`,
  26 pages, SHA-256
  `2c4433d53c33c337d4ed028c2843cf0b5631263d7bf4a0a42106727985daa3a8`.
- Supplement source: `proof_compression_submission/supplement/supplement.tex`,
  SHA-256
  `57275e1e5e1058306607a98583ac31e98383952ef2284515fea01f1c47ce95bd`.
- Supplement PDF: `proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf`,
  24 pages, SHA-256
  `9b10797d7503e6940d80a95bc90302b3b32a9ea34cb9f63a54bee3f12f3c06e1`.
- Machine crosswalk: `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json`,
  SHA-256
  `7a137cf03bab6ddef7c5c9a798adcbb29942d69e988a375f4afb9c5a5c207ffd`;
  reader crosswalk SHA-256
  `7e85fd5009218d8561a990eb262e8b2d1554503d17ba0204cdc8ac7ebec79963`.
- **Mathematical** means a checked deduction or exact independent derivation.
  **Computational** means an executed exact finite/symbolic check.
  **Provenance** means only path/byte/hash/history agreement.
- “Independent” is used only when the check does not import the decisive
  package classifier/canonicalizer/model-map implementation. A package script
  whose name contains `independent` is not automatically independent of all
  upstream package code.

## Common fresh execution

The clean full suite was launched once from the second clean extraction as:

```text
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py \
  --full \
  --output /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/logs/release_full_report.json
```

It exited 0; all 40/40 layers passed; harness time was 5,465.840630 s,
shell wall time 5,466.17 s, and maximum RSS 2,547,630,080 bytes. The report
SHA-256 is
`7b5c7d2409db3ebf53784b7581ee4723c6aed05cd977a01f01124fa2006e7a6b`;
stdout SHA-256 is
`ec8c7b5b27cc212f4ffff0ab442572b14fd632e3649c8d7ca21e4ad75a47e21b`;
stderr was empty. The corresponding fresh quick run exited 0 with 23/23
layers in 382.72 s and maximum RSS 1,342,914,560 bytes; report SHA-256
`89ab068f59a3eafe9e556d8bfff3d9feaa3d1e03a9f9e3310b59ec33bb53525d`.

The report retains each child layer name, status, return code, elapsed time,
and stdout/stderr hashes. It does **not** retain child argv. Accordingly this
registry names the exact executed layer and its measured time but does not
invent argv; the immutable command constructors are in
`work/final_theorem_release/verify_final_theorem_release.py`, SHA-256
`f30cc4b26e45d0ed959786cf4504ae8974a3c3da5953a40072b8cc48bd82d95a`.

## Summary

| ID | Theorem-claim status | Evidence | Package-evidence qualification / exact gap |
|---|---|---|---|
| C01 | **PASS** | mathematical + computational | Package producer and replay are the same script; a separate exact boundary/subdivision attack closes the substantive gap. |
| C02 | **PASS** | mathematical + computational | **FAIL in authority consistency:** one named authority has stale restoration counts; the declared mutation gate is path-dependent. |
| C03 | **PASS** | mathematical + computational | Full transport regeneration passed; its dedicated frozen mutation report overstates independence. |
| C04 | **PASS** | mathematical + computational | Slow/fast canonicalizers share package graph objects; a separate incidence enumerator independently checks the primitive universe, not the full orbit code. |
| C05 | **PASS** | exact symbolic computational + independent census | No remaining rank/census gap found. |
| C06 | **PASS** | exact symbolic computational + representative independent pullback | Not every high-degree body was independently recomputed outside package code. |
| C07 | **PASS** | exhaustive computational + independent census/attacks | **FAIL in submitted mutation evidence:** the sealed composite mutation reports did not create mutant ledgers. |
| C08 | **PASS** | exhaustive computational + independent parent/hash attack | No current-forest gap; the stale C02 authority must not be used as current forest evidence. |
| C09 | **PASS** | exhaustive computational + separate graph audit | The package graph audit reconstructs primitives through the atlas, although its isomorphism/compiler and decisive classifications are separate. |
| C10 | **PASS** | mathematical + exact independent symbolic check | No remaining gap found. |
| C11 | **PASS** | mathematical + 40-layer computational replay | **FAIL in release reproducibility:** the documented ordinary mutation command exits 1 and rewrites a locked file. |
| C12 | **PASS** | mathematical + exact independent boundary checks | No remaining gap found. |
| C13 | **PASS** | mathematical + two package replays + independent literal-map check | Independent check establishes exact rank nine but does not duplicate the two specifically named minor values. |

No C01--C13 theorem claim is left `UNVERIFIED` on its merits. The obsolete
filenames `START_HERE.md`, `verify_handoff.py`, `test_handoff_mutations.py`,
`setup_environment.sh`, `run_all_verifiers.py`, and `SUBMISSION_BINDING.json`
do not exist in this revised ZIP; those legacy protocol gates are separately
**UNVERIFIED**, not silently mapped to any C-row.

## C01 — domain, rooting, subdivision

**Claim and status.** Principal stochastic/continuous-time K2P domains, edge
subdivision, and rerooting invariance: **PASS**.

**Printed locations.** Article source lines 202--413 (definitions and K2P map,
PDF pp. 4--6); the strict continuous-time specialization is at lines
1540--1588 (PDF p. 21).

**Authoritative artifacts.** `work/domain_rooting_closure/PROOF.md` —
`f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
`work/domain_rooting_closure/domain_rooting_certificate.json` —
`4e38beb68062deae8f83cd265daacbef8c5d3f6d73ce25ef47a54828b658d450`.

**Inspected producer/replayer.** `work/domain_rooting_closure/verify_domain_rooting.py`
— `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b`.

**Fresh result and attack.** Full layer `domain_rooting` passed in 0.058649 s
(stdout `0deca40553e32ec02cea5a3dcdd824c20372abc8b111c36118247f2ed96d7bff`).
The genuinely separate `independent_checks/math/fresh_exact_checks.py`
(`6e31a7a28e59921d874eece125ae980b80ef50b373433d2463f5a7b0315667a5`)
checked three representative exact rational points near the strict `D_plus`
and continuous-time boundaries and their inverse-transition-probability signs;
output
`aedc640f928ecd0b2336289c19a743bbf09b88a0ca55345e6505d8e6ec6f8a1f`.
The separate hand proof audit established the general subdivision choice
`r > max{s,g,2s-g,0}` and checked the reticulation-adjacent rerooting argument.

**Evidence/gap.** Mathematical plus exact computational. The package's
producer and replay are shared code; the independent rational derivation is
the non-shared check. No mathematical gap remains.

## C02 — quartet signs and labelled tree of blobs

**Claim and status.** Pointwise quartet signs, labelled tree-of-blobs recovery,
and source-to-target topology direction: **PASS**, with an authority-consistency
defect.

**Printed locations.** Article lines 415--527 (PDF pp. 6--7), especially the
corrected C/T sector at 415--461; supplement lines 398--414 (tree--sunlet exact
calculation, supplement PDF pp. 8--9). Current restoration partitions are at
article 1127--1133 (PDF p. 15) and supplement 310--326 (PDF p. 6).

**Authoritative artifacts.** `work/quartet_separation_closure/PROOF.md` —
`a0f34c91c1a986412e6ae968015eaa38c09a9e2ee813b8d68b2c4655f0842744`;
`work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json` —
`d193983da3322c708767a398fbe4c0e96543275d7ed769a7447aea5e893fb563`;
`work/quartet_separation_closure/quartet_logic_certificate.json` —
`d7974dc2b57276f12a4fa827f42ddcd4b9fa95f89880032c65c085e54d7f7276`;
`work/quartet_separation_closure/quartet_terminal_binding_certificate.json` —
`fdbd41bfcb07e4884b0eedfdde223d63fffd5462187d6972e8a6d9bd326b531c`;
`work/adversarial_proof_review/topology_direction_certificate.json` —
`3a2cf7c15be8dcb4c307e1f2547af6ffb93596a4a7de5245242882a565fd033d`.

**Inspected code.** `work/quartet_separation_closure/verify_quartet_logic.py` —
`783cc522c8669eb1cd89928246b998ed09b222a9e9931d4c22d7fd03b5e05ec8`;
`work/quartet_separation_closure/verify_quartet_terminal_bindings.py` —
`b97cdf9ce0ce01a6d5ccd6843fb22b64a9b872e6dcae69de2adc9735da095b3b`;
`work/adversarial_proof_review/verify_topology_direction.py` —
`03d6ec9a7b84cdce9179967a720bbfae4410681d4bdfc07cbb3a54588da7bcc8`.

**Fresh result and attack.** `quartet_sign_logic` passed in 1.081811 s,
`quartet_terminal_bindings` in 33.544317 s, and
`topology_direction_structural_provenance` in 13.727806 s. The separate exact
script above regenerated the three quartet-tree pullbacks and the whole-map
`T_i` factor without importing package model-map code. It obtained precisely
the printed corrected C/T-sector signs.

**Evidence/gap.** Mathematical and computational. The exhaustive terminal
replay shares upstream graph-derived split sets; the algebraic mapping from
those sets and the representative primitive graph checks are independent.
The exact package gap is that the last named authority still says 35,758
restoration quartet plus 646 tree/sunlet children (36,404 topology terminals),
where the current forest gives first layer 35,758 quartet + 606 `T_i` + 148
quadratic + 24 quartic + 32 continuation and second layer 248 quartet + 8
`T_i`, hence 36,620 topology-sign leaves. Regenerate or narrow that authority
and reseal. Separately, its semantics mutation report is path-dependent as
described under C11.

## C03 — bridge fibre, marginals, local product, gluing

**Claim and status.** Complete two-sector bridge fibre, paired marginal
submersions, physical local product, and simultaneous gluing: **PASS**.

**Printed locations.** Article lines 535--846 (PDF pp. 8--11) and contextual
simultaneous gluing at 1277--1330 (PDF pp. 17--18); supplement bridge
normalizer lines 415--427 (PDF p. 9).

**Authoritative artifacts.** `work/bridge_marginal_closure/PROOF.md` —
`0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
`work/bridge_marginal_closure/certificate.json` —
`9231a7b78c13e54b745eba68926276a6551c6c3512d6a85746baba6613c1aacf`;
`work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md` —
`b84af8f9f5a4c306e14f0d27e9fcd72dcce6608260ed6104e660734eb38b5d9b`;
`work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json`
— `4a97b7d2ffb61e1f1ab094cbe3486c9801bfcd64f8fa783411fa45b343d601be`.

**Inspected code.** `work/bridge_marginal_closure/verify_bridge_marginal.py` —
`da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431`;
`work/adversarial_proof_review/verify_adversarial.py` —
`0b8767b8b67200a977b49dae938be73ba829b7e89b51ce6a27d79205a08e3668`;
`work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py` —
`1a3395c89b08a213b192039018b68ed1925632dedea5e3b68c9dc35a086d8af2`;
`work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` —
`01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160`.

**Fresh result and attack.** `bridge_marginal_gluing`,
`analytic_adversarial_audit`, and `global_component_scale_audit` passed in
0.053222, 0.232722, and 0.147406 s. The full graph-derived transport
rederivation passed in 296.095941 s (stdout
`4515e9e9f3d49e88f1b3c349a39680607834657ac36eb32482d34c2f0060dfe7`).
Fresh hand checking established the all-zero normalizer, equality of C/T
scales, independent G scale, degree-two obstruction exclusion, pair-anchor
determinant `-2`, lack of tree holonomy, marginal surjectivity, and physical
simultaneous bridge inequalities.

**Evidence/gap.** Mathematical plus exact computational. Full regeneration is
stronger than the dedicated transport mutation report, which only treats a
changed exact-row hash as rejection and is not an independent installed-ledger
attack. That report should be relabelled; no theorem gap remains because the
fresh full rederivation passed.

## C04 — primitive grammar, completion counts, canonicalizer action

**Claim and status.** Complete cycle/theta primitive grammar, licensed
canonicalizer action, ordinary-triangle semantics, and counts 831, 1,983,
4,155 / 405,216 / 2,946,240 / 13,440: **PASS**.

**Printed locations.** Article lines 848--1040 (PDF pp. 11--14); supplement
primitive grammar and raw schema lines 142--231 (PDF pp. 3--5).

**Authoritative artifacts.** `proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md` —
`4dbb41879114bb2dd61b8b9f5daa84c0f561f4d88918d3c5359a276913bacbd1`;
`proof_compression_submission/analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json` —
`e47c9d11f13c7a8527767149ecff87bc9905d49579d12a736bdce88539852cc2`;
`work/final_theorem_release/corrected_universe_certificate.json` —
`cd5803dcee8da7f0cd6cddda6b17c2a1303336657ddacfa147b004c40f79a450`;
`work/canonicalizer_completeness/PROOF.md` —
`7e0e7be28c5be309a67a9f7174858a2a3e356627acff233bbd97d0369a68ba2a`;
`work/canonicalizer_completeness/canonicalizer_completeness_certificate.json`
— `dd1eca849a992a14ef7b4942e2e4e864052f210c23b132fc8dfc9cbd5f513afa`.

**Inspected code.** `proof_compression_submission/analysis/derive_baseline_and_universe.py` —
`74623c169ad8589de52ad75394629d0c9b6087eacb032bac68b5b5da61b1b317`;
`proof_compression_submission/analysis/verify_family_coverage_equivalence.py` —
`f35a6e13a2b703ed9337f75b027727922e3563023c85520186df1049cbc561c9`;
`work/final_theorem_release/verify_corrected_universe_independent.py` —
`ba916b95affd33a9121b72e6912e599be68d463838472e32fefc33c2177031ac`;
`work/canonicalizer_completeness/canonicalizer_audit.py` —
`3df120b4e5d36e1222fc5766346e18b79623debbdaa04236cabf5132415cf3e4`;
`work/canonicalizer_completeness/verify_canonicalizer_completeness.py` —
`c9f5acd64f1cc0f1fa344b95ebe6f96d401839325380ac22338f9c1081c2641f`.

**Fresh result and attack.** `corrected_universe_independent_replay` passed in
9.791420 s and `canonicalizer_completeness_full` in 100.115231 s. A separate
standard-library primitive/census program,
`independent_checks/computation/independent_primitive_and_census.py`, SHA-256
`f6ad6a8161fb8f8cea41fb187180e6947a72960b21b13ce66fca83f71f1c19df`,
enumerated and graph-checked all 10,084 archetypes and independently derived
the completion formula and all three raw totals; its report SHA-256 is
`7fe83d590f90cdf03dc0c88c7eff72902b040fb9019b825f254538a50cd1613d`.
A second graph attack from three abstract pole paths,
`independent_checks/math/primitive_core_enumeration.py`, script SHA-256
`183d340ee52364abc15e0e48167de2e28f553dde8b54d2960b6465f8b80c712f`,
found exactly theta0--theta3, the printed repairs, zero two-reticulate-pole
cases, and the 25/0 admissible/tree-child census for the exceptional `K4-e`.

**Evidence/gap.** Mathematical plus computational. The package slow and fast
canonicalizers share submitted primitive graph objects; the separate incidence
enumerator verifies their universe and graph axioms but does not independently
reimplement every licensed orbit comparison. No collision or split was found.

## C05 — raw four-port coverage and symbolic rank filter

**Claim and status.** Every raw4 direction occurs once; all rank exclusions use
symbolic global target upper bounds and exact source lower witnesses, including
75 exceptional orbits: **PASS**.

**Printed locations.** Article lines 1041--1165 (PDF pp. 14--16); supplement
certificate decision tree and census lines 232--309 (PDF pp. 5--6).

**Authoritative artifacts.** `work/raw_ledger_audit/artifacts/raw_ledger_summary.json`
— `b14591da6604aa77712a5121bb88f7d2a4731ebdc0b68bd2634771e3bc7ed56f`;
`work/rank_upper_certificates/rank_upper_coverage.json` —
`c52c5730494eb894360c17b6e54ae5c260fca3cddb8702d5c796750c7df874bc`;
`work/rank_upper_certificates/manifest.json` —
`ea1f37d1d6dbc33735eae532de970d659b152cd76c758cbbd601c3970856ced5`.

**Inspected code/replay.** `work/raw_ledger_audit/generate_raw_ledger.py` —
`91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44`;
`work/raw_ledger_audit/verify_raw_ledger.py` —
`745ece3309128b0b0a5bb824e9811be946c40bee744cd99ebdc7d709f714e371`;
`work/rank_upper_certificates/build_rank_upper_coverage.py` —
`b792efabbdf0d8a871bfb8a8526451b2f4c4e0f8209e75f654de6cc77b58d28f`;
`work/rank_upper_certificates/syzygy_upper.py` —
`e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`;
`work/rank_upper_certificates/verify_rank_upper_certificates.py` —
`bd51596fe6bc5ddc8a4c6a185bda989479e3f7e736b0e80d9ea33ac7d1acf93e`.
Exact output artifact (not executable code):
`work/rank_upper_certificates/rank_upper_replay.json` —
`c967917601f64803c96c1ba11cabc5fd3ea8d6021f9e55441c4210d9b886793d`.

**Fresh result and attack.** `four_port_raw_full_regeneration_provenance`
passed in 304.989545 s and `four_port_exact_rank_full` in 117.163632 s;
the staged-atlas-omission expected-failure layer also passed its intended
nonzero-return check. The independent stream audit required raw ID to equal
stream ordinal for every one of 405,216 rows and reproduced all partitions.
A real complete-ledger mutation that made a source rank equal the target rank
was rejected at `RAW4_RANK_EVIDENCE:97`, not at a checksum guard.

**Evidence/gap.** Exact symbolic computational plus independent census and
mutation. Package rank upper certificates are checked coefficientwise, not by
sampling. No remaining gap was found.

## C06 — direct separator families

**Claim and status.** All direct terminals are exhausted by exact
isomorphism/triangle terminals and direction-safe quadratic, cubic, quartic,
quintic, or F2/F3/F4 certificates: **PASS**.

**Printed locations.** Article lines 1041--1165 (PDF pp. 14--16); supplement
lines 232--309 and generated
`proof_compression_submission/supplement/certificate_appendix.tex` lines
1--285 (printed exact-certificate appendix).

**Authoritative artifacts.**
`proof_compression_submission/templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json`
— `f2f99e77e91fa97a747156ef032aeec5fd9406babea6b7887bb58506da14caf4`;
`proof_compression_submission/templates/PRINTED_CERTIFICATE_APPENDIX.json` —
`4a4b58f486769fe03fc199d5914d854d8f03e89538284b51b9a375a96fa5920e`;
`proof_compression_submission/supplement/certificate_appendix.tex` —
`f2444f0308ab2dcccc45dec0704e98b147fffe4bb11fef9ef19cb7f34e688af5`;
`package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json`
— `e333b0420c22c8a80aa2b0bbe8553500a5c0734b78e90b35c08d857a302c963c`;
`package/referee/k2p_offline_sweep_portable/DIRECT_CLOSURE_LOCK.json` —
`6c9052e14a5a551a6b928c7ecb244dd16f8cce7a5078baa79f1bc1c956c9fc35`.

**Inspected code.**
`package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py` —
`08a188809833bc429053b01a2243542ab4a25e8b50a14409f82649e29160243a`;
`proof_compression_submission/templates/derive_direct_templates.py` —
`ff987bd136ac9e2fe59ae27c4e5a6344916086f8347b9928019e12d2656eb904`;
`proof_compression_submission/templates/build_printed_certificate_appendix.py` —
`7c366606b15661ce30f6f88f8e195f139f7d1f37e5378b79df0c19254018a0f8`;
`proof_compression_submission/templates/verify_printed_certificate_appendix.py` —
`79d8e7dc59c9934987d13480fab1b36212abb269b6e2a8333bf36918945dbd6c`.

**Fresh result and attack.** `four_port_direct36` passed in 13.618133 s and
`four_port_direct36_full` in 106.380986 s. The independent stream split 1,472
presentations into 839 quadratics, 36 higher-degree (2 cubics, 12 quartics, 22
quintics), four hard bindings, 20 isomorphisms, and 35 triangles. A separate
four-switch symbolic expansion for raw row 1849 / R4Q-03,
`independent_checks/math/direct_certificate_check.py`, script SHA-256
`b85fd57b863ea3ffdc8684d1615b30619ca1e39ce3606f73c9f08a86dc928014`,
obtained target pullback zero and a nonzero 44-term source pullback; output
`ec59f819aa93536e20c8e06f53b92358e7f8f63faae0a889e7762f3708c14994`.

**Evidence/gap.** Exact symbolic computational plus an independent
representative polynomial route. The fresh review did not independently
recompute every high-degree body outside package code; package exact replay
remains load-bearing for those bodies.

## C07 — corrected full-map finite universe

**Claim and status.** Corrected raw4/theta2/cycle ledgers, whole-map `T_i`
directions, terminal classifications, and exact composite coverage are
mutually consistent: **PASS**. The submitted mutation evidence for this claim
is **FAIL**.

**Printed locations.** Article lines 1041--1203 (PDF pp. 14--17); supplement
lines 232--340 (certificate decision tree, censuses, restoration; PDF pp.
5--7).

**Authoritative artifacts.**
`work/final_theorem_release/corrected_universe_certificate.json` —
`cd5803dcee8da7f0cd6cddda6b17c2a1303336657ddacfa147b004c40f79a450`;
`work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json` —
`9a2b340eb10e73abf0ea7c7aba5ae7c69942eea0f75402408f52277d960d648e`;
`work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json` —
`cf4ee4c23068cbc644474ad0161510a99106d3235f28e722fd3340b5bbbb3fdb`;
`work/final_theorem_release/full_map_reseal_audit.json` —
`945c957f0b73ab01d9c5bd6942ccb881f86e22fc47d8e4cc1fff5da8f4a64f40`;
`work/final_theorem_release/composite_reseal_diff_audit.json` —
`bc91fee3b7541fcae72c4db2e66776fbfc69c43890718239f0eea41bb2cc0654`;
`proof_compression_submission/analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json` —
`e47c9d11f13c7a8527767149ecff87bc9905d49579d12a736bdce88539852cc2`.

**Inspected code/replay.**
`work/corrected_composite_ledgers/generate_corrected_composites.py` —
`a117923e7b5cf90f0a13630fd21a6c454139f7e6e9c3c7bf84276229351a58ce`;
`work/corrected_composite_ledgers/verify_corrected_composites_independent.py` —
`67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690`;
`work/corrected_composite_ledgers/artifacts/release_contract_replay.json` —
`a9c863627250de79d52b8c2501c8c2865d768f58146e91406b17e7a4dc854125`;
`work/final_theorem_release/verify_full_map_reseal.py` —
`9d7b2b148e8a2b14e57fa4f8ed2acca9f21874cf46df667d8c225bc9b0625ff5`;
`work/final_theorem_release/verify_composite_reseal_diff.py` —
`238ffcea402fa74ab955df9fc73500e98d3c64f3d0ecb77441d1a081c2d997b3`;
`proof_compression_submission/analysis/verify_family_coverage_equivalence.py` —
`f35a6e13a2b703ed9337f75b027727922e3563023c85520186df1049cbc561c9`.

**Fresh result.** The full suite passed raw4 `T_i` truth (18.935887 s),
theta2 `T_i` truth (70.556143 s), raw4 full regeneration (59.123858 s),
theta2 full regeneration (471.029543 s), cycle structural replay
(104.363563 s), and composite reseal differential (15.364630 s).
Additionally, the composite verifier was invoked directly, outside the
umbrella, with reports redirected outside the package:

```text
.venv/bin/python -B work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family raw4 --report <audit>/logs/raw4_composite_independent_report.json
.venv/bin/python -B work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family theta2 --report <audit>/logs/theta2_composite_independent_report.json
```

Raw4 exited 0 in 230.39 s, 405,216/405,216 rows, report SHA-256
`1ae9505c553d174d36bc8c3701fea3b9b7f2cfe5059d4a1fc58bd8571ab4e348`;
theta2 exited 0 in 333.37 s, 2,946,240/2,946,240 rows, report SHA-256
`937cde59ff65317ef003e4d8728a95b40a7849f9c673c80b69d5e3c61273adca`.
These are fresh exhaustive package-code replays, not independent model-map
implementations.

**Independent attack and exact gap.** The standard-library census independently
streamed every row and reproduced all raw4, theta2, and cycle partitions. A
separate driver
`independent_checks/computation/composite_mutations/run_real_composite_mutations.py`
(`7ca72d10eacf8f2d25d931db855b7e36430356cbbd85ae548f6350723c790378`)
made 12 real complete raw4 gzip-ledger mutations; all were rejected by the
actual verifier at their intended semantic markers. Report SHA-256:
`8bf09b30f9be51ebb48b8523cafe4eae767f0972f9c32cd4682c88d23c2d4086`.
In contrast, authoritative
`work/corrected_composite_ledgers/run_composite_mutations.py` SHA-256
`0786f265b01fdf93a8fb90a79ff01a18f59113f197f4ca9f2a1e9e1eaa0c7c8e`
never creates a mutant ledger; its sealed raw4/theta2 reports
`13492986e8bb366a26fa3ba2278905696165c4deeeb5c2e808fa051fd6a34568`
and `bd3c50d48da744897b073afa2416b6a91b4d264f65ca7d23942b336352b0b3c5`
therefore do not evidence their claimed attacks. Replace them with real
raw4 **and theta2** disposable-ledger tests and reseal. This is computational
evidence/reproducibility blocking, not a classification counterexample.

## C08 — restoration forest

**Claim and status.** All 997 obligations form a transport-coherent,
depth-two, 36,824-edge forest with zero unresolved records: **PASS**.

**Printed locations.** Fixed-full lemma at article lines 827--846; forest
census at 1127--1164 (PDF p. 15); supplement lines 310--340 (PDF pp. 6--7).

**Authoritative artifacts.**
`work/restoration_sign_reclassification/corrected_restoration_forest.json` —
`43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8`;
`work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json` —
`4a97b7d2ffb61e1f1ab094cbe3486c9801bfcd64f8fa783411fa45b343d601be`;
`work/canonicalizer_completeness/inheritance_transport/restoration_restriction_parameter_transports.jsonl.gz` —
`eda4157580c611fcc22eb760e99b3c61bd207cb7b5688bba33482a62a4b5df39`;
`proof_compression_submission/restoration/RESTORATION_ARCHETYPES.json` —
`127f3920c1a882e07c7d424eeb43d696067ffe0c068a820a34ee5394b49d0ba4`;
`proof_compression_submission/restoration/RESTORATION_ARCHETYPE_VERIFICATION.json` —
`2c18ea9271fe260a404d7d239c81d7f5f79af8363cc324135325b33ab61a6c1e`.

**Inspected code/replay.**
`work/restoration_sign_reclassification/build_corrected_restoration_forest.py` —
`55e7196b840b98334327e81b2583ab2105a8107ee9be308781b41187c9c7de6d`;
`work/restoration_sign_reclassification/verify_corrected_restoration_forest.py` —
`e4cef28f156e1c300ed7b7cc48bb1a96f3a7686d92e2c748ec8dfa156d236f9e`;
`work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json` —
`24fa2e61f60610a8b24c4107ec7f866278f0cc671ca203d7aaa40a37bea291dd`;
`proof_compression_submission/restoration/analyze_restoration_archetypes.py` —
`2e9256f6d61b73b19cd92d4242918af22a851d398993360dd59b8a54d439978e`;
`proof_compression_submission/restoration/verify_restoration_archetypes.py` —
`5e6eba5d2f2a941b8ece98e4a75ff784286d3d5acecf136ce0a658a74c97b0df`;
`work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` —
`01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160`.

**Fresh result and attack.** Full parameter rederivation passed in 296.095941
s. The independent stream audit verified every one of 36,568 first rows and
256 second rows against row hashes, every second-row parent index/hash/root ID,
and the continuation-parent set. It derived 997 parents, 2,540 roots, 36,824
edges, 36,792 leaves, depth two, and zero missing/duplicate/cyclic/unresolved
obligations. Real raw4 mutations of parent and presentation transport both
failed at `RAW4_RESTORATION_EVIDENCE:2185`.

**Evidence/gap.** Exact computational plus independent hash/parent traversal.
No forest gap remains. The stale C02 topology certificate is not valid current
restoration-census evidence and must be repaired separately.

## C09 — coherent probes and arbitrary subdivision words

**Claim and status.** Exact one-/two-port probes determine arbitrary attachment
words, all site types, automorphisms, and triangle transports: **PASS**.

**Printed locations.** Article localization lines 693--846, PC-PARTIAL boundary
1166--1202, reconstruction 1480--1538; supplement probe theorem 341--397
(PDF pp. 7--8).

**Authoritative artifacts.**
`work/probe_coherence_corrected/probe_coherence_certificate.json` —
`2f4d64b32a905ce2cc06bae7d03215f9239427d421825c2525437ee6ba2ccaf6`;
`work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json` —
`4a97b7d2ffb61e1f1ab094cbe3486c9801bfcd64f8fa783411fa45b343d601be`;
`work/canonicalizer_completeness/inheritance_transport/probe_relation_parameter_transports.jsonl.gz` —
`67bd9dcf5d466b5b281f90b87d50d96d8e2992ab48977ec4eaf8a0809ecff8fb`;
`work/canonicalizer_completeness/inheritance_transport/probe_restriction_parameter_transports.jsonl.gz` —
`1aff01aea4b854bf88cfd7ff684bf633ffe71f5c50391a8d79362dec38a44ab9`;
`proof_compression_submission/probe/PROBE_WORD_THEOREM.md` —
`cd4e16a50622a1584d16a4a90b08a55f95c1dfe16849e47eedae11d77b57b56f`;
`proof_compression_submission/probe/PROBE_WORD_COVERAGE.json` —
`4a38372635ba617268cfc921baf3a7b397c9beb639dde31bf26b3d2dc7673414`.

**Inspected code.** `work/probe_coherence_corrected/build_probe_coherence_corrected.py` —
`f0176e1759771a01ffa3da9e8d2b8967fc9189d3f93b30c6d06554bba9a77ddf`;
`work/probe_coherence_corrected/verify_probe_coherence_corrected.py` —
`3facc1b51c133aa953f4a0cba86782672c86e78990d72ef2fc2aaa16a6f2a1bd`;
`work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py` —
`51e2de1e8b1fe753a5b0605b3995ea02cfc7db4c3f83d7a3d39da51a116bba44`;
`work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` —
`01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160`;
`proof_compression_submission/probe/verify_probe_word_theorem.py` —
`58405a121c607ff3039e569977af4a50481e687e9308c02cb7491e8781ab8de7`.

**Fresh result and attack.** Full primitive probe regeneration passed in
2,907.058666 s; the full independent package replay in 16.768294 s; site and
transport partition in 4.777194 s; and independent primitive graph audit in
409.836254 s. The separate standard-library stream audit checked all 176
anchors, 2,206 source and target sites, 29,964 one-port rows, 2,107 equality
survivors, 544,571 two-port rows, 67,741 unique transports, and 4,379 unique
restrictions, including independently recomputed site-count formula and site
types.

**Evidence/gap.** Exhaustive computational plus an independently written
census. The package “independent” graph audit imports the atlas for primitive
reconstruction, but uses its own labelled isomorphism, polynomial compiler,
transport derivation, and does not import the decisive expected probe
classification. This shared-input qualification remains; no missing site or
transport was found.

## C10 — three-port separation, triangle germ, genericity

**Claim and status.** The three-port tree/sunlet separator and rank-nine
ordinary-triangle common germ close the local alternatives used in global
genericity: **PASS**.

**Printed locations.** Tree/sunlet at article lines 474--527 (PDF p. 7);
triangle germ and contextual gluing 1204--1330 (PDF pp. 17--18); genericity
1365--1478 (PDF pp. 19--20); supplement exact calculations 398--443.

**Authoritative artifacts.**
`package/original/checkpoint_2/continuation_2/K2P_TREE_SUNLET_SIGN_CERTIFICATE.md` —
`f2feaaec71194a794b8b8b6b24a66866803a10fe12ce59a04e7688917b100cc4`;
`package/original/checkpoint_2/continuation_2/K2P_TRIANGLE_GERM_EXACT.md` —
`25593e90d87286d7092b68ba5ac9bc176afba56d98b39becefafb1fe3becbc07`;
`work/final_theorem_release/triangle_sunlet_certificate.json` —
`b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885`.

**Inspected code.** The first path is a historical arithmetic replay retained
from checkpoint 2; it is not a current independent implementation of the
entire final package.
`package/original/checkpoint_2/continuation_2/verify_triangle_and_sunlet.py` —
`3b6c69caf6e72818fe5d931b1c30beabb7860c0c3686d300aff998c48741ccd6`;
`work/final_theorem_release/no_assert_triangle_sunlet.py` —
`c4a529336a0d409de30cf1c55f283e64628099424bd4191cfb7b31ec8995d7a1`.

**Fresh result and attack.** `three_port_no_assert` passed in 0.314900 s. The
separate symbolic route factored the `T_i` polynomial exactly, rebuilt the
ordinary-triangle map, obtained its six `1/12` and three `1/48` nonconstant
coordinates, rank nine, and exact block determinants `-1/2` and `-1/4`.
Fresh proof checking confirmed that the article uses submersion/constant-rank
sections, not a false square inverse, and that the complex/real dimension
argument makes every generic exceptional component proper.

**Evidence/gap.** Mathematical plus exact independent symbolic computational.
No remaining gap found.

## C11 — global K2P-SAME, genericity, reconstruction

**Claim and status.** Unconditional principal-domain directed-containment
classification, generic identifiability, and exact terminating reconstruction:
**PASS**. Release reproducibility is **FAIL**.

**Printed locations.** Main equivalence theorem article lines 1332--1363
(PDF p. 18), genericity 1365--1478 (pp. 19--20), reconstruction 1480--1538
(pp. 20--21); supplement crosswalk/replay/mutations lines 562--869.

**Authoritative artifacts.**
`work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md` —
`bff0a4e6ddfa123aff0f560795d3f90dc6d60a6da768690f1f8e39db0fddcc9f`;
`work/global_theorem_closure/promotion_manuscript/PROBE_PROMOTION_PLACEHOLDER.json` —
`79a9949f5a5598a83c7e2bfc60d669dfe4b8b7d3417d8d8673e2fc4c634efaaa`;
`LICENSES.md` —
`9f8d28b470f185905d0469d45168d72d56d0152a1667a299328a3af00041465e`;
`work/final_theorem_release/RELEASE_LOCK.json` —
`7113b1c52d577858ec20ef83cd87c870242c8ddc96018036b5c073229821eec9`.

**Inspected executable producers/replayers.**
`work/final_theorem_release/build_release_lock.py` —
`a49add912050dad8e11f16897010feae6269ff4405ae3ad019d02cf32437f683`;
`work/final_theorem_release/verify_final_theorem_release.py` —
`f30cc4b26e45d0ed959786cf4504ae8974a3c3da5953a40072b8cc48bd82d95a`;
`work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py` —
`464bf0823283e93175e350fefcb5fce3fd2bce2cd137dfe833b4722e24943ccd`.

**Inspected JSON output artifacts (not executable code).**
`work/final_theorem_release/corrected_universe_independent_replay.json` —
`dec57350681e175ac4f27b6c809ff540769ef78d318c0c856d26725915cf77e5`.
Stored full report `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json`
`ec5fefc3c1ab2210e9c53792240ebe008603da6abd004d093e2b95e15ff5c10b`
and telemetry
`proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json`
`415bf36a59e6006603e4382085c784ffc4e1a1744f1e4c920cd5f0d313fb9df5`
were checked only as provenance, not fresh validation.

**Fresh result and attack.** The fresh 40-layer execution above passed; its
`promotion_manuscript_guard` layer passed in 0.292038 s. Independent proof
checking verified both directions, no proper one-way containment, all
finite-choice/localization quantifiers, full-dimensional competitor-section
argument, and exact reconstruction termination. The exact algebra, primitive
universe, censuses, restoration, probe, transport, and real mutation attacks
listed under C01--C10 supply the non-umbrella attacks.

**Evidence/gap.** Mathematical plus exhaustive computational. The umbrella is
orchestration, not independent mathematical evidence. The documented ordinary
command
` .venv/bin/python -B work/final_theorem_release/run_release_mutations.py `
exited 1 in a pristine relocated extraction after rewriting locked
`work/quartet_separation_closure/quartet_semantics_mutation_certificate.json`
from sealed SHA-256
`51aca097b5a4ed7e699206d58b6e61ebc899372057ea733e83ac148e86231eb1`.
Its trace hashes absolute extraction paths; a two-directory reproducer report,
SHA-256
`13c27197e78b7c260e4d6e964a5bbdd2a56fc8af5433d0b1aa1ea3b596e03bb7`,
proved path dependence. This blocks reproducibility/fresh mutation
qualification, not the theorem implication. Add disposable output and
path-normalized semantic diagnostics, rerun, and reseal.

## C12 — strict continuous-time corollary

**Claim and status.** Classification and reconstruction restrict to
`0<s<1, s^2<g<1`: **PASS**.

**Printed locations.** Article lines 1540--1588 (PDF p. 21), with domain and
subdivision inputs at 303--413 and bridge inputs at 642--728.

**Authoritative artifacts.** `work/domain_rooting_closure/PROOF.md` —
`f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
`work/bridge_marginal_closure/PROOF.md` —
`0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
`work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md` —
`bff0a4e6ddfa123aff0f560795d3f90dc6d60a6da768690f1f8e39db0fddcc9f`.

**Inspected code.** `work/domain_rooting_closure/verify_domain_rooting.py` —
`6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b`;
`work/bridge_marginal_closure/verify_bridge_marginal.py` —
`da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431`.

**Fresh result and attack.** The C01/C03 layers passed. The separate exact
script checked representative rational points near `s^2=g` and the strict-CT
triangle witness without floating point. The independent hand proof audit,
rather than that script, checked positive-root marginal sections and the
explicit simultaneous bridge `L,U` inequalities.

**Evidence/gap.** Mathematical plus exact independent computational. No
remaining gap found.

## C13 — weak-class sharpness

**Claim and status.** A full-dimensional `4n-3` weakly-but-not-strongly
tree-child ambiguity establishes sharpness: **PASS**.

**Printed locations.** Article lines 1590--1799 (PDF pp. 21--24); supplement
full weak certificate lines 444--561 (PDF pp. 9--12).

**Authoritative artifacts.** `work/weak_sharpness_closure/PROOF.md` —
`dcc36e0ae4299e3f0415d31e73522f224c91506f90062d0a13791af5746e9369`;
`work/weak_sharpness_closure/weak_sharpness_certificate.json` —
`e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd`;
`proof_compression_submission/analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json` —
`c3b302c37744fa33834c75ca5b22da9d374d5def4f1e6f4650e3b2b3b4166437`.

**Inspected code/replays.**
`work/weak_sharpness_closure/verify_weak_sharpness.py` —
`f0cab684609a89e2ab331643e15f6d516576b063f5acdff0f1cb134b5af8a3e2`;
`proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py` —
`4e764b5e6cc6a67de4381fc7c3c3994437eead134ed576004f8fe218b53e897d`;
`proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py` —
`4de6be83448ff79b3a3677926e4fea75709ff6e8dafc6ec4baed55fa8bc969a1`;
`work/weak_sharpness_audit/PROOF_AUDIT.md` —
`d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa`;
`work/weak_sharpness_audit/audit_weak_sharpness.py` —
`e737fe3c0f0878c0284b0a55ebac1bfd3a7915b33278ab2916ed56bdf2200e5d`;
`work/weak_sharpness_audit/audit_certificate.json` —
`cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52`.

**Fresh result and attack.** `weak_sharpness_primary` passed in 0.148404 s
and `weak_sharpness_independent` in 0.166278 s. The separate literal-arc script
reconstructed both maps, exact common normalized tensor, rank nine for each,
admissible/tree-child/non-tree-child rooting censuses `(5,2,3)` and `(7,2,5)`,
nonisomorphism even after forgetting triangle head flags, cherry determinant
`2464/675`, and the four-dimension-per-cherry induction.

**Evidence/gap.** Mathematical plus exact computational with a genuinely
separate literal-map check. That check establishes the theorem-relevant exact
rank nine but does not duplicate the package's two specifically named 9-by-9
minor values; this is a stated equivalence-level qualification, not an
unverified rank claim.

## Cross-cutting evidence failures and reseal boundary

1. **C02 authority consistency — FAIL.** Regenerate or narrow the stale
   topology-direction certificate/narrative and reseal every binding manifest;
   rebuild PDFs only if a printed source/hash changes.
2. **C07 submitted composite mutation evidence — FAIL.** Replace in-memory
   comparisons with real disposable raw4 and theta2 ledgers passed to the
   actual verifier, require intended semantic diagnostics, correct release
   prose, and reseal reports/lock/crosswalk/archive.
3. **C11 ordinary release mutation gate — FAIL.** Write only to caller-owned
   scratch, normalize path-dependent diagnostics, add a two-location/no-write
   regression, rerun the ordinary gate, and reseal.

These defects justify scientific **HOLD** at the package/reproducibility level.
They do not supply a counterexample or invalidate any C01--C13 mathematical
implication established above.
