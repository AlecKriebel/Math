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
