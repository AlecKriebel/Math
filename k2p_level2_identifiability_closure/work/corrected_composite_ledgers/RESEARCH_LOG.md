# Research log: corrected composite ledgers

All times are 2026-08-21 PDT.

## 11:55 — Contract and input audit

- Read the corrected finite-universe contract and its executable validator.
- Inventoried the raw-four and theta2 primitive ledgers, exact rank tables,
  full-map certificates, terminal records, and restoration forests.
- Detected a transient missing terminal-class-root return in the concurrently
  edited release validator.  The unified release owner corrected it before the
  package replay; a fresh invocation confirms the issue is resolved.
- Completion estimate for the bounded composite package: 10%.

## 12:21 — Terminal proof registry frozen

- Extracted all 934 non-restoration terminal proof payloads from the complete
  production records.
- Bound every registry row to its original record byte hash, semantic record
  hash, descriptor, source, and class identity.
- Replaced the 36 residual classes with the exact direct cubic, quartic, or
  quintic overlay certificate where applicable.
- Registry SHA-256:
  `0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d`.
- Completion estimate: 25%.

## 12:35 — Producer and independent replay implemented

- Implemented a streaming primitive producer and a separately written replay.
- Fixed gzip metadata, row ordering, canonical JSON, and streaming hash-root
  algorithms.
- Added direct graph-derived quartet witnesses and exact evidence bindings.
- Added optimized-Python refusal and source-tree fingerprint gates.
- Completion estimate: 50%.

## 12:40 — Adversarial rank and determinism correction

- Removed runtime from semantic summary payloads.
- Strengthened each directed rank exclusion to bind the exact source lower
  minor independently of the target lower/upper equality proof.
- A first theta2 run failed closed because an older Bernstein implementation
  differed only in its serialized domain-description string.  Switched to the
  frozen independent theta2 routine and required exact certificate-payload
  equality, not merely the same mathematical sign.
- Completion estimate: 60%.

## 12:51 — Theta2 authoritative ledger generated

- Generated all 2,946,240 rows with the exact required partition.
- Compressed ledger SHA-256:
  `4cbd7b774adccaafc81338ce9093e33f4abcae8d75664c9d4c9ecc582a80cc58`.
- Bound 56 restoration roots, 864 distinct one-parent descendants, and 832
  exact terminal leaves with zero gaps or cycles.
- Completion estimate: 72%.

## 12:55 — Raw-four authoritative ledger regenerated

- Waited for the corrected restoration forest to freeze, then regenerated
  against final forest SHA-256 `43bd2be5...`.
- Generated all 405,216 rows with the exact required partition.
- Compressed ledger SHA-256:
  `431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96`.
- Derived 934 terminal classes and 997 restoration parents with the exact
  required multiplicity histograms.
- Completion estimate: 80%.

## 13:01 — Mutation gates passed

- Raw-four rejected 14/14 mutations, including omission, duplicate raw ID,
  wrong permutation, false rank, wrong restoration parent, broken transport,
  forbidden rooted restriction, optimized mode, source drift, and reassigned
  cubic/quartic/quintic certificates.
- Theta2 rejected 12/12 mutations, including missing restoration child,
  reassigned quadratic certificate, and broken isomorphism transport.
- Zero survivors and zero source-tree drift.
- Completion estimate: 88%.

## 13:06 — Raw-four independent replay passed

- Recomputed every primitive coordinate and quartet witness.
- Rebound every rank, terminal, and restoration record.
- Recompressed the complete stream byte-for-byte to `431dac8898...`.
- Independently rebuilt all 16,974 exact whole-map pullbacks.
- Replay payload:
  `1a51d5ff1ab6b00fdb16259ac31a457d5d84fe9c272dbe1ea1c2ba70795e4bbe`.
- Completion estimate: 94%.

## 13:09 — Theta2 independent replay passed

- Recomputed every primitive coordinate and all 2,942,592 quartet witnesses.
- Rebound every rank, quadratic, isomorphism, and descendant record.
- Recompressed the complete stream byte-for-byte to `4cbd7b774a...`.
- Algebraically rediscovered the source-zero restriction and rebuilt all 2,528
  strict target pullbacks independently.
- Replay payload:
  `0e80f8c42cdaef062cc335c871b4daddd9e85592c3fad108903c634f448218a4`.
- Completion estimate: 98%.

## 13:10 — Outer release contract accepted both packages

- Invoked the current final-theorem release validator directly.
- Both composite summaries, ledgers, generators, independent reports, mutation
  reports, forest/registry/truth inputs, hash roots, censuses, class roots, and
  descendant roots passed.
- Contract replay payload:
  `df840ff7962386c224edb9320d8f86dc184feaaa67256f8e56f0f65e83ab194f`.
- Zero unresolved composite records.
- Completion estimate for this bounded goal: **100%**.

## 2026-08-22 — Full-map domain prose resealed and replayed

- A clean full replay exposed an original byte-reproducibility defect: the
  raw-four and theta2 full-map producers emitted the precise open-unit-cube
  domain statement, while their frozen certificates retained an older
  ambiguous sentence.
- Regenerated and resealed both truth certificates.  An independent audit
  proves that the old and new raw-four certificates differ in exactly 8
  domain leaves, 8 dependent nested seals, and the top seal; theta2 differs in
  exactly 85 domain leaves, 85 dependent nested seals, and the top seal.  No
  mathematical field changed.
- Regenerated both composite ledgers from primitive inputs.  Raw-four remained
  byte-identical at `431dac8898ad...`.  Theta2 now has SHA-256
  `805fc7f5a3de...`; all and only its 2,528 `full_map_Ti_strict_sign` rows
  changed, at the single leaf
  `evidence_binding.coefficient_certificate_sha256`.
- Reconstructed the prior theta2 gzip byte-for-byte from the new package by
  reversing those 2,528 seals, then independently regenerated the new ledger
  byte-for-byte.  Both composite mutation suites again had zero survivors.
- Updated outer composite-contract replay payload:
  `5fd774fb9335a7ce1900dd80226c79fab8459f8fa3738c5274237c131113cde7`.
- Completion estimate for the bounded composite layer: **100%**; completion
  estimate for the final clean submission/release package: **94%**.

## 2026-08-25 — verifier-facing mutation qualification repaired

- Replaced every synthetic sampled-dictionary composite check with a complete
  deterministic disposable gzip-ledger attack against the production
  independent verifier.
- Raw-four now has 12 semantic ledger attacks plus optimized-mode and aggregate
  source-immutability guards; all 14/14 reject at their intended diagnostics.
  Report payload: `dc265e02da504666197320fcab90226fa44cfc5c5906bb4ef5b6f1ab35d44f02`.
- Theta2 now has 10 semantic ledger attacks plus the two separate guards; all
  12/12 reject at their intended diagnostics. Report payload:
  `5663b87d3f09eaac5e89db69ac5a1cf6069b308abf9bc4242650d0897ded1ff7`.
- Independent A/B executions to differently named outputs were byte-identical:
  raw-four report SHA-256 `83196bc33504fd1e17c8784d2c7530f358e85cff8161c8e5f14ba04a60c42d76`;
  theta2 report SHA-256 `ec2c6ec092539048b4e7ab9d9cfea01caa985d0f35cae74ca56732dc4cfe4c84`.
- Output safety now uses atomic same-directory replacement and rejects project
  symlink aliases and source hardlinks. Focused hardlink, late-symlink,
  authoritative-alias, and optimized-mode regressions pass without changing a
  locked source.
- The rich v2 report validator independently accepted both reports. No
  authoritative composite ledger, classification, census, rank, separator,
  restoration forest, or transport changed.
- Completion estimate for the corrected-composite mutation qualification:
  **100%**. Completion estimate for the final resealed submission package:
  **96%** pending global locator/lock/crosswalk/PDF/archive replay.

## 2026-08-25 — corrected-composite contract rebound

- Replayed the strengthened live release contract against both v2 mutation
  reports and their exact producer/verifier bindings.  The contract passed
  with zero unresolved records and payload
  `e4b7e754bab7d9dbb7f39b5749725ca3585c4bdd79764f69dd6851a12cd2185b`.
- Added the focused output-safety regression to the package manifest and
  corrected two stale reader-table fields so that the printed summary and
  independent-replay payloads equal the current artifacts.
- Completion estimate for this bounded package remains **100%**; the outer
  submission bundle remains pending its ordered reseal.

## 2026-08-26 — raw-four restoration-provenance rebind

- Regenerated raw-four first into an external scratch directory after the
  corrected restoration forest was independently replayed and resealed.
  Comparing all 405,216 old and new rows found the same category, class,
  parent, transport, and certificate data.  Exactly the 2,540 restoration
  presentations changed, and each changed only at
  `evidence_binding.forest_payload_sha256`, from the superseded forest payload
  `0a3df52751ba38d7e6d4d118ee7068a98b7be7897d0aa732e96a74d7523a88bf`
  to `be81d13f8f51dc49030e569bf31939a7c3bb915c3dff1f91455416761eeeb772`.
- Repeated the official producer into the authoritative artifact directory;
  its ledger and summary were byte-identical to the prior scratch generation.
  The producer completed in 235.82 seconds with 348,536,832 bytes maximum RSS.
  The resulting ledger SHA-256 is
  `c6cd9d6b5b09371565fd3e58ff9ab3cd7266b6231b153d43f9d1e886af8eae27`
  and the summary payload is
  `3fdfdfb46d8c23e89979ce5794f8b5b11176946278ae70ebc75d54d6e2ad1d44`.
- The independent primitive, byte, classification, and whole-map algebra
  replay passed all 405,216 rows in 368.29 seconds with 337,379,328 bytes
  maximum RSS.  Replay payload:
  `1cb227b8430d86fc74dfce7f94bc3ec9c01adad1be8c9156c118d15812e85c7c`.
- The production-verifier-facing suite rejected all 12 complete semantic
  ledger attacks and passed its optimized-mode and source-immutability guards,
  for 14/14 total tests and zero survivors.  It completed in 522.27 seconds
  with 343,932,928 bytes maximum RSS.  Mutation payload:
  `c1d55c7624a2cfd508681a5b18529e0760384d66c3ed1b534c17b9eb4e747d46`.
  The separate atomic-output, hardlink, symlink, authoritative-alias, and
  optimized-mode safety test also passed.
- Completion estimate for the corrected raw-four composite layer remains
  **100%**.  No mathematical census, classification, relation, parent, child,
  or transport changed; only provenance seals were rebound.  The outer finite
  universe locator and release lock remain to be resealed by the global release
  workflow.

## 2026-08-26 — final raw-rank and full-map provenance rebind

- Regenerated the authoritative raw-four composite after the final raw-rank
  and full-map-overlay provenance reseals.  The 405,216-row gzip ledger was
  byte-identical to its predecessor, with unchanged SHA-256
  `c6cd9d6b5b09371565fd3e58ff9ab3cd7266b6231b153d43f9d1e886af8eae27`.
  A recursive summary comparison found exactly three changed leaves: the
  `rank_upper` input SHA-256, the `whole_map_overlay` input SHA-256, and the
  derived payload seal.  Every classification, exact rank, terminal,
  restoration member and parent, polynomial witness, ordered root, stream
  hash, and census was unchanged.  The producer completed in 228.60 seconds
  with 346,963,968 bytes maximum RSS.  The final summary has file SHA-256
  `31bb6cf9e363fa4435e1d5a5e4d6d589440b926afd049844eb010b59f04c1436`
  and payload
  `3a49bfeeb244cba84cf2e42e2acf296f112d1586c5e17f40e2d2872722c3c988`.
- The independent primitive, exact-algebra, and canonical-byte replay passed
  all 405,216 rows in 353.19 seconds with 342,441,984 bytes maximum RSS.  Its
  file SHA-256 is
  `1a4ac5c5ab5f86228f9e59c62a9021547907a9d6238e1171a7074f49506a8c66`
  and payload is
  `dfed35eab33dcc9983b38c8cedb79ed90b12c8a5cf04b58d251637b3fb2f1191`.
- The verifier-facing v2 mutation suite rejected all 12 complete semantic
  ledger attacks and passed its optimized-mode and source-immutability guards,
  for 14/14 total tests and zero survivors.  It completed in 509.48 seconds
  with 344,195,072 bytes maximum RSS.  Its file SHA-256 is
  `db6d4e6c8986db20ca623724981d2d4f39f6ff0ccf5d70e708190c1e09a86d4a`
  and payload is
  `eec4a56b20faa3239044db49796fa724d60a5412a8d6e89a92db5d81e9656385`.
- Completion remains **100%**.  No theorem, classification, relation, rank,
  parent, child, transport, or finite census changed.
