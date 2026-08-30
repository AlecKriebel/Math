# K2P-SAME R6 evidence registry

Date: 2026-08-29 (America/Los_Angeles)

This registry separates mathematical evidence, computational evidence, and
byte/provenance evidence.  A digest agreement authenticates bytes; it is not
itself a proof.  All package paths below are relative to the pristine root
`isolated/k2p_principal_d_plus_submission_referee`.  No authoritative package
file was edited.

## Executive evidence disposition

- Fresh quick replay: **23/23 PASS**.
- Fresh full primitive replay: **41/41 PASS**.
- Crosswalk/revised-bundle suite: **37/37 attacks rejected**.
- Outer mutation suite: **25/25 rejected twice** in independently named clean
  relocations, with byte-identical reports and unchanged source inventories.
- Independent exact mathematics: **PASS** for tested identities, inequalities,
  counts, repair tables, triangle minors, and the complete weak-sharpness
  witness.
- Independent computational scan: **PASS**, zero unresolved checks; it
  reconstructed both primitive universes, streamed the large composite
  partitions, checked restoration/probe/transport joins, and audited complete
  verifier-facing mutation ledgers.
- Archive, recursive ledger, Git tag, PDF rebuild/layout, bibliography and
  generated-input omission gates: **PASS**.
- Sole fresh blocker: **R6-F1**, a current proof-to-artifact digest
  contradiction in C09.  It is a reproducibility/release blocker, not a
  demonstrated mathematical counterexample.

The fresh replay reports are SHA-256
`1cb8d359e2d12035d7c9c54b2495c523d67961d78c14098b277a55b90ed01c78`
(quick) and
`23c78f94072a993cad954d9e72615bd01acaf8f5842722ffecd133d631556b74`
(full).  Commands, wall times, RSS, stream hashes, all 64 layer rows, all 37
crosswalk attacks, and both 25-case relocation runs are in
`EXECUTION_LEDGER.md`.

## R6-F1 — current C09 proof narrative names obsolete coverage digests

**Classification:** reproducibility-blocking / current authoritative-proof
narrative inconsistency; not theorem-fatal on current evidence.

The authoritative C09 word-theorem narrative
`proof_compression_submission/probe/PROBE_WORD_THEOREM.md` (14,418 bytes,
SHA-256
`f45cd543b6cafbada2c9cd361b06f708f2bdebe112c596a774cd0ee7736a17e8`)
labels a section “Current coverage artifact” at lines 306--311 and prints:

- coverage file SHA-256
  `3791e4bb829976aa78289281b9998bfe0605ba4a20518f1e8dd660d7d1a91bb8`;
- logical payload
  `1d4248028b38f6b731f066960d9e584240de68a17323539fe5b47f119a8086f6`.

The actual sealed current certificate
`proof_compression_submission/probe/PROBE_WORD_COVERAGE.json` is 6,854 bytes,
schema `k2p-probe-word-theorem-coverage-v1`, status PASS, and has:

- file SHA-256
  `c2e32b37d32eda11470afc7f747cb2bca5fa58c78fd92793f8fa94309f3d3660`;
- declared and independently replayed payload
  `d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49`.

Both printed values are therefore wrong.  This is a current-object
contradiction: C09 in the theorem-artifact crosswalk and template row CBT-5
bind the theorem narrative together with the actual current JSON, while the
revised submission manifest and compression result also bind the actual JSON.
An independent scan found each obsolete digest exactly once, in this current
section; no historical registry classification applies.

Minimal reproducer:

1. read lines 306--311 of `PROBE_WORD_THEOREM.md`;
2. SHA-256 hash `PROBE_WORD_COVERAGE.json`; and
3. duplicate-aware parse and canonically replay its top-level
   `payload_sha256`.

The review-owned reproducer
`independent_checks/provenance/probe_narrative_binding_audit.py`, SHA-256
`364985fb5fb03b2d97a6d77696f8c9db9a09ab34662fcf21a8d548ff7248dc5f`,
imports no submitted module.  It exited 1 as intended with exactly two
mismatches.  Result
`evidence/provenance/PROBE_NARRATIVE_BINDING_AUDIT.json` has SHA-256
`bf4aea4e4905c2629441486855942c506a45880112a12d53a90572b91d7ec7f6`
and logical payload
`b80a7c40cc84be9de814f020a5a38076c933e684e326ebc80e852423790c0543`.

The current word verifier still passes and independently reports 176 anchors,
29,964 one-port rows, 544,571 two-port rows, and 67,741 exact transports.
That supports the artifact's computation but does not correct the false
present-tense binding in its proof narrative.

**Smallest adequate remedy:** replace the two printed digests with the actual
current values; add a semantic gate plus targeted mutations that parse this
named current section and compare both declarations to duplicate-aware
certificate bytes and canonical payload; then regenerate and reseal all
byte-dependent objects, at least the compression result, theorem-artifact
crosswalk, revised submission manifest, referee archive/digest, commit, and
annotated tag.  The five TeX/Bib sources and PDFs do not consume this Markdown
file and need not change solely for this edit, but their gates should be rerun.

## Package, archive, ledger, and Git provenance

### Outer referee archive

- Source archive: `K2P_Principal_D_Plus_Referee_Package_20260829.zip`.
- 214,977,546 bytes; SHA-256
  `fef886379d9682586920a9f1112465dccab75267dbdd87a5b87b38dc4dbea513`.
- 495 unique regular members; 483,751,133 uncompressed member bytes;
  214,834,734 compressed member bytes.
- One safe root; lexicographic order; fixed 2026-08-27 timestamp; mode 100644;
  no duplicate names, traversal, encryption, symlinks, comments, or extra
  fields.  Every member is byte-identical to the pristine extraction.
- Two independent clean rebuilds and the distributed archive were byte
  identical.  Result
  `evidence/provenance/INDEPENDENT_ARCHIVE_REBUILDS.json`, SHA-256
  `a9816e541d52775b893d0e8498d376d6c56a575aea30504fb819833744427f99`,
  status PASS.

### Recursive frozen and combined ledgers

- `work/final_theorem_release/RELEASE_LOCK.json`: 80,180 bytes, SHA-256
  `bbb411dde4a13f001d9c2b5fac97722a54bb6ce604b6aff476de44f7ce4b8f53`,
  payload
  `3a0c89c4cedb7202161289eab7b3671c004ae638bcf90eba837e45e3e1890fc5`;
  promotion-ready, zero blockers.
- Recursive frozen closure: 231 outer rows plus nested 94 rank, 17 cycle,
  60 direct-closure, and 16 direct-input rows; 408 distinct files,
  479,383,009 bytes; content root
  `ed3beb4fca8338a3b97c7e5a0ff2bb58460ee7a244ea030bb7d3f837b5563d73`.
- Portable ledger `output/referee/REFEREE_BUNDLE_CONTENTS.json`: 77,354 bytes,
  SHA-256
  `b3af4bab82d9715841aed7f4c666309720f52fc78f6f560fd6325e26267b2753`.
- Submission layer: 86 files, 4,268,041 bytes, root
  `68c93bf97428d2f27064974f02cab5c1a0b3ac8ac863440adb96ebdc9ebad07c`.
- Combined layer excluding its manifest: 494 files, root
  `c63d27090e3598c45999db88db414de1fe20c654aa7bcec8cfa0508566bd06e7`.
- Revised manifest SHA-256
  `fe9125f446556664c7ca3c818ba816aa84709956c6426acbea33dd5d81f66610`,
  payload
  `2a871f6f69561ac7a02b7fb167d655b712ba00b352cb0a3b254df41419fc7b77`.
- Independent result
  `evidence/provenance/INDEPENDENT_PROVENANCE_AUDIT.json`, SHA-256
  `8b2224f9316f56b19709b8406ef3d3484f9d12227885106ffe5d733856347d97`,
  status PASS, payload
  `7bb498c2bde79a48338cabe009327bbd120ff0af79eb5b25975f572f480520c8`.

The current release declares three supplemental execution dependencies, all
present and bound: `output/referee/README.md`
(`76b8f7480e164d8667b4e4507e8662a897b9db22fc01cc3bda0410326f8bfc54`),
`output/referee/REFEREE_BUNDLE_CONTENTS.json` (hash above), and
`output/referee/build_referee_bundle.py`
(`b59301e07adbd232c45de820979a0f11aba88acb82bbcdb9456f4d886aa88207`).

### Git and stored-run provenance

- `k2p-same-biorxiv-v1.0.5` is an annotated tag peeling to
  `5628a08f6bf3e5573ebbbf3e2dd8636ad00b338e`.
- All 495 distributed members equal tagged blobs (491 mode 100644, four mode
  100755; ZIP mode normalization is declared).
- Stored telemetry commit
  `5d541c46969e1508596e62a21bc5647dd1f1ba3c` is an ancestor of the tag.
  Its five submission inputs and `RELEASE_LOCK.json` are unchanged through the
  tag.
- Stored clean-full report SHA-256
  `0d2fd0206181fe4c08ebff1367592809d0b8126d58aee3d91980941bfa55a95e`;
  telemetry SHA-256
  `eab3c1d6a096ef469b3db4844ea567a49e8e8ea6e62a6c8a2506814773cb6d50`.
  It records 41 PASS layers, 6,361.55 s real time, 2,543,091,712 bytes maximum
  resident set, and 487,932,720 bytes peak memory footprint.  These facts are
  provenance only; the fresh 41-layer replay was run separately.

## PDF and five-source consistency

- Five sources:
  - `article/main.tex`: 85,978 bytes,
    `43278b63cc6d123fc8ec970178e886e9a57d02c879a2ff748887572f29eeb27d`;
  - `article/references.bib`: 6,960 bytes,
    `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6`;
  - `supplement/supplement.tex`: 46,724 bytes,
    `d5f79a95a7ec0aff2ce4e8e3f818dcf930435dcde2265ed23dc6bacede1fea33`;
  - `supplement/certificate_appendix.tex`: 22,405 bytes,
    `1f7590b2930f8ac1536724763d0b30e330f817fd3127edae0df3ee520180c649`;
  - `supplement/compression_tables.tex`: 3,269 bytes,
    `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81`.
- Article PDF: 194,542 bytes, 26 pages, SHA-256
  `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4`.
- Supplement PDF: 160,762 bytes, 24 pages, SHA-256
  `0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d`.
- Two clean builds were byte-identical to one another and to both sealed PDFs.
  Removing either generated supplement input was rejected.  Removing the
  bibliography was rejected with exit 1 and the intended named diagnostic.
- All 50 pages were rendered and inspected; all fonts embedded; zero clipping,
  overlap, broken tables, unreadable glyphs, or other layout defects.
- Result `evidence/documents/PDF_SOURCE_CONSISTENCY_AUDIT.json`, SHA-256
  `c222b6a5753df5f7b4743240acfaf3f4192adf5f9eee5422dc6df2a3a31dea2d`,
  status PASS.
- The independent five-file bioRxiv source ZIP was rebuilt twice; both and the
  distributed ZIP are 57,892 bytes with SHA-256
  `66527a3e3018b054f9e6b618a6c9e81a4ddbc6e2d0cced81542a0a7fe3eb3cd3`.

## R5 semantic-anchor repair

The prior 934-class registry/16,974-row overlay ambiguity is repaired:

- typed terminal registry:
  `work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz`,
  schema `k2p-raw4-terminal-certificate-registry-v1`, 934 classes, SHA-256
  `8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998`;
- distinct strict-sign overlay: schema
  `k2p-raw4-corrected-terminal-overlay-v2`, 16,974 corrected rows, SHA-256
  `5810ffb1d023e503eaa62d9705c28a85e9c724a6ad8357f49ebe61b2dde675dc`.

All three current narrative tables are explicitly typed as reader snapshots,
with `RELEASE_LOCK.json` as byte authority.  The 11-case printed-authority
mutation suite has zero survivors, including a coherent registry-to-overlay
swap rejected for schema drift and a 16,974-for-934 mutation rejected for
cardinality drift.  Independent repair result
`evidence/provenance/SEMANTIC_REPAIR_AUDIT.json`, SHA-256
`458d628ea21a32a2f915a468f8358254edef4161dcd5dc4bcf17dfd6ddcbb67f`,
status PASS.  R6-F1 is a separate C09 narrative edge not covered by this gate.

## Independent mathematical and computational evidence

### Exact mathematical attacks

Review program `independent_checks/math/r6_exact_math_checks.py`, SHA-256
`81b3fa05d004289ec9121946bbece00e334953f701fabfc873d6042a2ba16dc3`,
imports no submission code.  Result
`independent_checks/math/R6_EXACT_MATH_CHECKS.json`, SHA-256
`80e3a857c18a812d0e176c64a50109f41e98a998231ae0b7f1913c4e0aaab7f3`,
status PASS.  It independently obtained:

- four exact boundary-near `D_plus` points, three exact CT points, and an
  exact three-factor marginal section, all satisfying every strict inequality;
- zero remainder for a representative tree--sunlet identity;
- triangle determinants `-1/2`, `-1/4`, and combined rank-nine minor `1/8`;
- completion counts 831, 1,983, 1,983, 4,155 and the printed minimal-repair
  tables;
- partition totals 405,216 raw4, 2,946,240 theta2, 13,440 cycle bases,
  536,364 cycle completions, 36,824 restoration edges, 29,964 one-port and
  544,571 two-port rows;
- primitive weak-witness rooting triples `(5,2,3)` and `(7,2,5)`, no labelled
  mixed or triangle-forgotten isomorphism, exact common tensor equality,
  Jacobian determinants
  `10368019213741323/563981315074464023964442388464888915634290688`
  and `1435825/85002596691653613846528`, and cherry determinant `2464/675`.

### Independent computational scan

Review program `independent_checks/computation/r6_semantic_scan.py`, SHA-256
`9318c2927934aa3c944ed36f2d2e17dc1895ac72ec807440191219d5b31c6a84`,
result SHA-256
`3f9bd18cfa7d800a16e41280a4470a9bdf4c9cbee96c689bc06b344eca36f732`,
status PASS, zero unresolved.  It locally reimplemented primitive weak
compositions, repairs, sink masks, ordered words, graph degrees/DAG tests,
port permutations and raw-ID inversion, and independently streamed:

- raw4: six sources, 2,814 targets, 405,216 rows, six equal 67,536-row source
  blocks, exact category partition
  `360408 + 16974 + 23822 + 1472 + 2540`;
- theta2: four sources, 6,138 targets, 2,946,240 rows, four equal 736,560-row
  source blocks, exact partition `2942592 + 2528 + 800 + 240 + 80`;
- direct terminal registry: 934 classes = 839 quadratic + 36 exact direct
  (22 quintic, 12 quartic, two cubic) + four hard + 20 isomorphism + 35
  triangle; 432 strict rational edge pairs checked;
- restoration: 997 canonical parents, 2,540 roots, 36,568 first children,
  256 second children, 36,824 edges, zero cycles/unresolved;
- probes: 29,964 one-port rows, 2,107 equality survivors, 544,571 two-port
  rows, 67,741 exact transport IDs, 4,379 parent restriction IDs;
- transport action scan: 230,232 identity, 47,157 complement, 277,389 affine,
  3,745 triangle-local, and zero illicit complements.

The scan forensically confirmed `main -> run_semantic_case ->
rewrite_complete_mutant + invoke_verifier`.  Raw4 has 12 distinct complete
mutant ledgers with 12 intended diagnostics, theta2 has 10; all reached the
production independent verifier, all mutant hashes were distinct, zero
survived, and source-tree drift was zero.  It also exercised 12 optimized-mode
entry points, each failing closed with its intended diagnostic.

Bounded attack program
`independent_checks/computation/r6_bounded_fail_closed_attacks.py`, SHA-256
`74255679840615ebc5dd752239ccb2939162373b89d7b001d801a547fee92815`,
result SHA-256
`e7c9a475a8da4f6b6f4462eda1356d20910d63be3e6b475217d83743e1542a8e`,
status PASS.  It rejected false atlas certificate families under normal,
`-O`, and environment optimization; checked all 4,379 rank-upper descriptors
(3,515 multilinear polynomial fields, 864 transported primitive log fields);
and confirmed that substituting sampled-rank evidence is rejected by the
production verifier with symbolic field-dimension failure.

### Reconciled finite census

| Layer | Reconciled exact result |
|---|---|
| Raw four-port | 405,216 = 360,408 quartet + 16,974 whole-map sign + 23,822 rank + 1,472 direct-terminal presentations + 2,540 restoration members |
| Direct terminal classes | 934 = 839 quadratic + 36 higher-degree + four hard + 20 isomorphism + 35 triangle; higher degree = 22 quintic + 12 quartic + two cubic |
| Five-port theta2 | 2,946,240 = 2,942,592 quartet + 2,528 whole-map sign + 800 rank + 240 quadratic + 80 isomorphism |
| Theta2 dummy forest | 56 roots, 864 one-parent descendants/edges, 832 leaves = 760 quartet + 72 isomorphism; zero missing, cyclic, or unresolved descendants |
| Cycle | 13,440 base directions; 5,964 restoration roots; 536,364 completions = 535,920 quartet + 300 whole-map sign + 132 quadratic + 12 isomorphism |
| Restoration | 997 canonical parents; 2,540 roots; 36,568 first + 256 second children = 36,824 edges; 36,792 separator leaves; depth two; zero missing, duplicated, cyclic, or unresolved obligations |
| Probes | 176 anchors; all 2,206 source and target attachment sites; 29,964 one-port rows; 2,107 equality survivors; 544,571 two-port rows; 67,741 exact transports; 4,379 parent restrictions |

The large raw4/theta2/restoration/probe values were freshly streamed or
regenerated, not inferred from a stored PASS.  Cycle and theta2 dummy-forest
partitions were checked by their full replay layers against the frozen exact
ledgers; the review-owned count/arithmetic program independently checked the
headline totals and repair/completion formulae.

## C01--C13 theorem-to-artifact bindings

Crosswalk:
`proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json`,
SHA-256
`43b8a284d1a5c2a3997d467f6d917eaaa00378f432ab434913bf7868151698c8`,
payload
`5392819dff6b208569bfd1d6ec30f498b847d243708a4d6d665acafbefe6dc6a`,
status `PASS_PC_PARTIAL`.  A review-owned pass rehashed all 173 path/SHA
occurrences inside the C01--C13 claim sections; mismatches: zero.  The broader
independent crosswalk audit resolved all 176 path/SHA occurrences, also with
zero byte mismatch.  This validates the bindings as byte facts only; R6-F1
shows why internal semantic consistency remains a separate question.

### C01 — domain, subdivision, and rooting

- Authorities: `work/domain_rooting_closure/PROOF.md` @
  `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
  `work/domain_rooting_closure/domain_rooting_certificate.json` @
  `4e38beb68062deae8f83cd265daacbef8c5d3f6d73ce25ef47a54828b658d450`.
- Producer/replay: `work/domain_rooting_closure/verify_domain_rooting.py` @
  `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b`.
- Mutation orchestrator: `work/final_theorem_release/run_release_mutations.py`
  @ `becef7af22196affe559b253099b8e6aa68afe24cdcf9f6b122286e181b45275`.
- Evidence disposition: mathematical and fresh replay PASS.

### C02 — quartet signs and tree of blobs

- Authorities: `work/quartet_separation_closure/PROOF.md` @
  `a0f34c91c1a986412e6ae968015eaa38c09a9e2ee813b8d68b2c4655f0842744`;
  `QUARTET_SEMANTICS_SPEC.json` @
  `d193983da3322c708767a398fbe4c0e96543275d7ed769a7447aea5e893fb563`;
  `quartet_logic_certificate.json` @
  `71001499d619d5ba438e4dc0590459231eafef21217338a8f7ca7f0ad7e229de`;
  `quartet_terminal_binding_certificate.json` @
  `0cc64c71fdf455dce2eb0f541464047628cf8d47ff44ac5cec57d88ed64fc2af`;
  `work/adversarial_proof_review/topology_direction_certificate.json` @
  `2ec6f0ed415f1b1a2fb8b90de9364f00e33f365ed5e313ba755a6c74c183c9e8`.
- Producers/replayers: `verify_quartet_logic.py` @
  `5dd8cb283e513b0064d432f141561eb38fa0212bc7006303e86d49f97bd35aa9`;
  `verify_quartet_terminal_bindings.py` @
  `c23a985f1130f1e6288fe0ca8b4b27cd32a9f3db44b2cf96728911ef06d18abc`;
  `verify_topology_direction.py` @
  `a74b308a9936996d2ea87b75f6c56be185de7a2763857bd4f253068d20b9d083`.
- Mutations: quartet semantic script/certificate @
  `93de9c9170cd715f09ddef69f9622157151c3ba157bd8a4095b0f8e1409a38ee` /
  `f41255bc6e5ac78ce7c34956d284ebd4b0cb50a5727215cc420971b4542a0e0e`;
  terminal-binding script/certificate @
  `aa9ec3c1832146177876f6704a5bb2a978d969156f4c6474d2c88d48fd0e669d` /
  `3ddb49498f26762903c6d3a6676c82681e1f038bcff60bbfc3af5a498b405a49`.
- Evidence disposition: mathematical, computational and mutation PASS.

### C03 — bridge/marginal local product

- Authorities: `work/bridge_marginal_closure/PROOF.md` @
  `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
  `certificate.json` @
  `9231a7b78c13e54b745eba68926276a6551c6c3512d6a85746baba6613c1aacf`;
  `work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md` @
  `b84af8f9f5a4c306e14f0d27e9fcd72dcce6608260ed6104e660734eb38b5d9b`;
  parameter-transport certificate @
  `a706ebea37b9fbf338f1d8ae439e9d1a14cd14589f8b78699b657f039cd09a68`.
- Producer/replay: `verify_bridge_marginal.py` @
  `da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431`;
  parameter producer/verifier @
  `9058470d4e6f95106dc6d13de5399d88003aa90734dadb489e63f104e32788a8` /
  `fe065ed7e54a5a969e8578c3f72d347ac2248b47d9a2283a6f42d130932d26da`;
  adversarial verifier @
  `a523ece1e9a176f9f334532d8799e1637abf776b2981b17d9143208d4ac0f689`.
- Mutation reports: adversarial @
  `390976c38c6a1e00ca2490d5ef341f17cc9a13e72892dcb27a1d19cea315d172`;
  parameter transport @
  `b17711eda26cb31839dab842123529159f72ed2ddd755a04facfbbb9a17ffb66`.
- Evidence disposition: mathematical and fresh replay PASS.

### C04 — primitive grammar and completion count

- Authorities: `proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md`
  @ `1749e00bb1a1be5c482d596ed84a8394cf06951d0f704bb00a8502cecc64b902`;
  `FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json` @
  `1c3defb14a1465cb83c1e8e87ccb3090c540d14c6c22a36136a4b8205a0b402d`;
  corrected universe @
  `a67862fc6b7a529f34acbfd4e4817facdcad9cb279ddcfd96d6d7853010469b4`;
  canonicalizer proof/certificate @
  `7e0e7be28c5be309a67a9f7174858a2a3e356627acff233bbd97d0369a68ba2a` /
  `5522164471b06895f0388c8c2baad716e9e87344c3cf595c7d3075ac70e6e655`.
- Producers/replayers: derivation @
  `072700b140a5d6a8ef8baf41a8b21d84955c5f808c24f4b9f83f7f6634ac39d4`;
  family replay @
  `7897197a604527c3944406f20098174bdf937e5563fd004397460ed33c48d37f`;
  corrected-universe replay @
  `b42d3aed0edfab7cdf6b70c8efa1cf6c5ea32715b8eead10a7df31eb329ee9df`;
  canonicalizer producer/replay @
  `0e4f2315d836053d1f50742af163668d243b086afda84515d197a2da09756bda` /
  `d6f6d7e05b700675055409229f0115e568bda1fcdeafc463e7d417ffdbe3706d`.
- Mutation reports: corrected universe @
  `4eb5ddbd407d64a83a7b6362fae1910bdac725f04c374de0da2f88256c1d0418`;
  canonicalizer @
  `d18b54d319d5fae95a193f9597339dca4e7f648b929f088d492207bce24ae674`.
- Evidence disposition: exact independent counts and fresh full replay PASS;
  the submission retains a declared PC-PARTIAL finite residue.

### C05 — raw-four rank filter

- Authorities: `work/raw_ledger_audit/artifacts/raw_ledger_summary.json` @
  `59212034aca49b29d2e0dd0e312cd5e7e76957b48e8eb312f74ce277e0843f43`;
  `work/rank_upper_certificates/rank_upper_coverage.json` @
  `c52c5730494eb894360c17b6e54ae5c260fca3cddb8702d5c796750c7df874bc`;
  rank manifest @
  `1ec69ef02c4ef511534952a9258a9cce5c3b40c33590b1383ee9219e95602913`.
- Generator/replayers: raw generator @
  `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44`;
  raw verifier @
  `615ae57fac469f9e6243c3295ef5121c0927873444e346696a05b12eb34e3d15`;
  rank verifier @
  `f5a72dcdf390252c1d5003e56a9fb097fc2624a18ce34b05e79abc9c1e50f86a`;
  symbolic engine @
  `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`.
- Rank mutation report @
  `a591d0e910d2fae3ee11664a591b485c474327f74b05711143e5c11d4a77f524`.
- Evidence disposition: fresh full generation/replay, independent raw-ID
  reconstruction and symbolic-vs-sampled attack PASS.

### C06 — direct separator families

- Authorities: template table @
  `b6c63c7818c54ac0bae1e4d3f64047cbcaa531f83ad0b16e6a4ec92f134f7698`;
  printed appendix JSON @
  `9990bb807323e1ceda93cb520b58692129fbdc8f41ea8ca66a1684a48f18ce08`;
  generated TeX @
  `1f7590b2930f8ac1536724763d0b30e330f817fd3127edae0df3ee520180c649`;
  direct-36 certificate @
  `8f0760543d0b69937c24785288ee26f58db86f34bb3446d686e0422eb2fa7af7`;
  direct lock @
  `dca3e0a76879336b0f4482417c7409275db205b3e1a769e48057cde46b6c1946`.
- Producers: template/appendix @
  `ff987bd136ac9e2fe59ae27c4e5a6344916086f8347b9928019e12d2656eb904` /
  `6d410af24a8864d57cbc3cdcbe5a7ab265cbdde241631280a712cf71cd95c710`.
- Replayers: direct closure @
  `87f274d6624ad67703306197d5b063f4b120e013125ac35e1af45df648bdee78`;
  printed appendix @
  `78ae3468b37818aff54c649401ce5fa47bd9ab9b33112d81b68752e7670defb5`.
- Mutation reports/scripts: direct @
  `26face7a232348830b6afaaff571e3fdc7e82bd611baf7be910241e1d9961e58` /
  `3b0672266c2dcec4ba7eaeeccee0c47b1f0a848dcd4bec0418de00233679d0cc`;
  printed appendix mutations @
  `7b0bb68a6d8f32e0df5a21bde11cba97795d22fa89d1af2f990fadd3ce45770b`.
- Evidence disposition: fresh direct-36/full replay, registry scan and family
  reassignment mutations PASS.

### C07 — corrected whole-map finite universe

- Authorities: corrected universe @
  `a67862fc6b7a529f34acbfd4e4817facdcad9cb279ddcfd96d6d7853010469b4`;
  raw4/theta2 summaries @
  `7fe22084b0037bd29674baa72683be2673a7f247f300422432c9857f47ad3da1` /
  `a714cf5b96591832eca83405daec42557bf7da787bf4b6656c19584b726f7973`;
  cycle base/full ledgers @
  `7bfb6c99ffff43993fe12c7f2625be83dbeb590faac5178961398331368d69a2` /
  `6e170c814b95fa7900e9cf24bcb6594a72f8399456614e9da7c0e5a1593d3506`;
  cycle certificate @
  `126ad1dd1aa753b578779fe01c12d26df2f5939abc1e02b5c4b8ccc275867adc`;
  full-map/differential audits @
  `b1eda458ede322a272f0306a58bb87def243295ba52abc52361bcea4a5ea7fcc` /
  `a3dcb06f44f4085f386ca37bfd29809536b79d10c2c6e920b28144f97a894a68`.
- Producer/independent verifier: corrected composites @
  `41f9f15f83fc860b15994c4369ca3b8b7c6b424bdc76e5377bf11d45c76c88e3` /
  `0c9bf77a1af47d2eedf424c825703b23c6753f2ed26defb5107db7f50da6666d`;
  cycle producer/verifier @
  `22d8193ee489895ed2390e5fb1e9067e195f046c9acf5656f8c2ff26f8bd7cc3` /
  `90bbcc7c2326ac15a8eb6fd8ea7d5a8334f6a047ae4a20d7c98fb70c334d6146`.
- Mutations: runner @
  `f15c3d49ed94c626943c9a568b48d29c1cedde8d2904b2aa3d9a28da19c7d7f3`;
  raw4/theta2 reports @
  `6475e37d2ec15eafc3650f387d8d4543268963c6794e3dfd90376d01741f23db` /
  `07f51fe0d5a28cd673cf782478c4a024e38ff7c729cf7a1e5cdafa4b53a4fac5`;
  cycle report @
  `7a5467eb57def74313a2db60ca2e1cfafc041d3236c289673c0907a34cf8ae23`.
- Evidence disposition: fresh full regeneration plus independent streaming and
  complete-ledger attacks PASS; finite residue remains declared PC-PARTIAL.

### C08 — restoration forest

- Authorities: forest @
  `396d1970af17b5e90c3f1b00ceab1b810816e93ec68a566bd0479f05c722793f`;
  parameter certificate @
  `a706ebea37b9fbf338f1d8ae439e9d1a14cd14589f8b78699b657f039cd09a68`;
  restoration transport ledger @
  `eda4157580c611fcc22eb760e99b3c61bd207cb7b5688bba33482a62a4b5df39`;
  archetypes/verification @
  `03b30ed654228833b159e533eb419ca2efc2f64b01a58a88027b212aca5152b7` /
  `a9e44df19cc0ec3207d4de95b64c59fa975d752f48e73da337c6ed37fb3c8074`.
- Producer/replayers: forest builder/verifier @
  `fa60f13409ac8b364b70fb4fb6ffd65634f1ddbf4ded4c4325205b44e383a7e2` /
  `99f8a373d1bbb924cc312777733a38d663cfc7e58f14d47b431357b222171f3b`;
  independent replay @
  `d74cc01341f405732c6ff62558ca3afff705c15cdf9a6f16dcc6ccd7636749c4`.
- Mutation certificate @
  `10e74ca5dd50da8b9597b0640181615012816f96eeb9c64153f3eadc1b395a3b`.
- Evidence disposition: 997/2,540/36,824 exact counts, zero unresolved/cycles,
  fresh full replay and parent/child mutations PASS.

### C09 — coherent probe-word reconstruction

- Authorities: probe certificate @
  `6edd4097d0ce6cc0938e1a7eaee8d01c7e9daac814e72422250f1dbdea04bdd3`;
  parameter certificate @
  `a706ebea37b9fbf338f1d8ae439e9d1a14cd14589f8b78699b657f039cd09a68`;
  relation/restriction ledgers @
  `67bd9dcf5d466b5b281f90b87d50d96d8e2992ab48977ec4eaf8a0809ecff8fb` /
  `1aff01aea4b854bf88cfd7ff684bf633ffe71f5c50391a8d79362dec38a44ab9`;
  word theorem @
  `f45cd543b6cafbada2c9cd361b06f708f2bdebe112c596a774cd0ee7736a17e8`;
  coverage JSON @
  `c2e32b37d32eda11470afc7f747cb2bca5fa58c78fd92793f8fa94309f3d3660`.
- Producer/replayers: probe builder @
  `db4e6b33cf552278d9ade1ae16941187777d44f4754f53cd1af92bdfde684cdd`;
  primary/independent graph replayers @
  `a101909cc492594d635752882a476ac4694314fa3b0be306857fb5a5dfd76053` /
  `ed6dccf6273fa1ba60a34c201d9ea4b0774eed2548055ddee5f90fd4282621c5`;
  word verifier @
  `8dcc191cc3af59a5b4f5950d6b15202823c943015be30cdd5ee21db62482ed28`.
- Mutation reports: probe @
  `6a0c037a5dbdd4f36713ea77202625beff11f70d60222af84f15648c30980455`;
  independent probe @
  `7224b26a0eead1aa39ccb0092b14b24990cdf5c455e15d040bd8d9181fd6463b`;
  parameter transport @
  `b17711eda26cb31839dab842123529159f72ed2ddd755a04facfbbb9a17ffb66`.
- Evidence disposition: computational census/replay/mutations PASS; **HOLD on
  current proof-to-artifact consistency because of R6-F1**.

### C10 — three-port signs and ordinary-triangle germ

- Authorities: tree--sunlet sign proof @
  `f2feaaec71194a794b8b8b6b24a66866803a10fe12ce59a04e7688917b100cc4`;
  exact triangle proof @
  `25593e90d87286d7092b68ba5ac9bc176afba56d98b39becefafb1fe3becbc07`;
  certificate @
  `b81a6cf8da1380f6a682ba6042f6f429ce5d6a47ba0cf62e9c9d8de1b4158885`.
- Original/no-assert replayers @
  `3b6c69caf6e72818fe5d931b1c30beabb7860c0c3686d300aff998c48741ccd6` /
  `c4a529336a0d409de30cf1c55f283e64628099424bd4191cfb7b31ec8995d7a1`.
- Evidence disposition: independent symbolic determinants and fresh replay
  PASS.

### C11 — global K2P-SAME, genericity, and reconstruction

- Authorities: article source/PDF @
  `43278b63cc6d123fc8ec970178e886e9a57d02c879a2ff748887572f29eeb27d` /
  `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4`;
  promotion manuscript @
  `fcf5ecd8321ccc68691736f6d522deb58cbb880e8bc8aa75d190807cec268331`;
  promotion placeholder @
  `fabd1dd919bc443d818b07b27ea8d4c73c78d0ee557a18a9f01abd0cc50d6569`;
  `LICENSES.md` @
  `9f8d28b470f185905d0469d45168d72d56d0152a1667a299328a3af00041465e`;
  release lock @
  `bbb411dde4a13f001d9c2b5fac97722a54bb6ce604b6aff476de44f7ce4b8f53`.
- Producer/replayers: lock builder @
  `a49add912050dad8e11f16897010feae6269ff4405ae3ad019d02cf32437f683`;
  final verifier @
  `6c2a6142e5a7c4fc092f16d5c3e52d0a4a00215f445d9facb199d557f7502ba0`;
  corrected-universe replay @
  `24547ab143ee78661f5e178da4afbe5d52e6cb500db4a56d588019ac47e31d6c`;
  promotion gate @
  `7c1bf4ecf5381af0b117029ce68dcaeb4cc1b8837e2ee36c19819b7a5533a847`;
  stored report/telemetry hashes as above.
- Evidence disposition: global hand argument and fresh 41-layer premises
  otherwise support PASS, but release status is **HOLD downstream of R6-F1**.

### C12 — strict continuous-time corollary

- Authorities: article source/PDF hashes as in C11; domain proof @
  `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d`;
  bridge proof @
  `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc`;
  promotion manuscript @
  `fcf5ecd8321ccc68691736f6d522deb58cbb880e8bc8aa75d190807cec268331`.
- Replayers: domain @
  `6c57043a801cba338ef90a68279bc078bda11d3ff25c40a3a53777aa9fd83f7b`;
  bridge @
  `da9c56d0057b90ccf63588c4a8ce90ca4fd3ab8764013f2c44ffc66411079431`.
- Evidence disposition: exact boundary/CT checks and hand corollary PASS,
  conditional on the C11 release closure.

### C13 — weak-class sharpness

- Authorities: proof/certificate @
  `dcc36e0ae4299e3f0415d31e73522f224c91506f90062d0a13791af5746e9369` /
  `e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd`;
  column crosswalk @
  `a6629eba036b93170d27cbb72ba04cd30b9b8c0b221f81ec4f450ca9ee6eb058`.
- Producer/replayers: primary @
  `f0cab684609a89e2ab331643e15f6d516576b063f5acdff0f1cb134b5af8a3e2`;
  independent proof/verifier/certificate @
  `d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa` /
  `28ecbd3c3b40dfd19af573cd9546b9c206817fad36b73240a485e2333f3a0fda` /
  `cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52`.
- Mutation reports/scripts: weak audit @
  `5f0037511f84e9c990e95cc995ce1542a0d92f9aaf5b424c2e56f4eb7c001310` /
  `4155765fd016072e46921c3843ca24f7de6b3b3e10d3fea95d32685b9c5a8b48`;
  crosswalk mutation script @
  `e30fbac168817480d092d107cfca41456504816be403bbd54493046e6941fc57`.
- Evidence disposition: two submitted replayers plus fully independent exact
  graph/tensor/Jacobian/cherry reconstruction PASS.

## Evidence-type boundary and remaining action

- Mathematical evidence establishes the checked hand derivations and exact
  independent identities; computational evidence establishes the finite
  generations and certificate checks actually rerun; provenance evidence
  establishes only identity, custody, and reproducibility of bytes.
- The submission's `PC-PARTIAL` boundary remains explicit: equality of
  polynomial bodies is not treated as graph-orbit equivalence, and the rank,
  restoration, and probe ledgers remain load-bearing.
- No advertised gate remains unrun.  The two environmental exit-1 attempts
  have successful controls.  R6-F1 remains unresolved and requires correction,
  a new semantic gate/mutations, and resealing before submission.
