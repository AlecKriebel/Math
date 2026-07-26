# Independent verifier B: order-13, k=3, `hole9` certificate

**Verifier verdict:**  
`VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_PENDING_HOSTILE_ACCEPTANCE`

**Exact verifier:**  
`src/verifier_b/order13_k3_hole9_certificate.py`, 39,193 bytes, SHA-256
`4adf3691f438c03b230ff323ea5f7c180db9b5c8cd895b6f31327f5e154a97ee`.

**Canonical evidence:**  
`evidence.json`, 15,105 bytes, SHA-256
`3de45d16b906e52c3960e4b2e75604908c8cacf356b84d7337db721f4fa49af8`.

## Scope

This is a clean-room certificate verifier.  It imports no constructor,
search, production-runner, normalizer, or candidate-manifest logic.  The
candidate manifest is retained and hash-bound as provenance, but none of its
claims is used to reach the verdict.

The verdict certifies UNSAT only for the exact formula with SHA-256
`3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea`.
It does not by itself exclude all order-13 graphs and makes no universal
gamma-theta claim.  The exact C-055 mathematical theorem, its hostile review,
the constructor acceptance, and the live `hole9` package preflight are
byte-bound so a separate integration audit can decide the template-level
claim.

## Independent checks

The verifier:

1. reads every decisive path without following a final symlink and checks
   exact size and SHA-256;
2. requires the certificate formula to equal the accepted constructor
   formula byte for byte;
3. independently parses DIMACS and obtains 9,802 variables, 32,108 clauses,
   281,028 literals, maximum clause size 286, no comments, and no empty
   clauses;
4. independently parses the normalized binary stream using canonical
   unsigned LEB128 records and obtains 45,281 additions total, comprising
   45,280 nonempty additions and one unique final empty addition, 410,400
   literals, maximum clause size 284, maximum variable 9,802, zero deletions,
   and no post-empty bytes;
5. checks that the corrected candidate README states that same census;
6. copies the formula, both proofs, and both pinned checkers into a fresh
   private directory;
7. runs pinned `drat-trim` with `-i -f -W -U`, requiring exit 0, empty stderr,
   an exact unique `s VERIFIED` transcript shape, and zero RAT lemmas in the
   core;
8. runs pinned `lrat-check`, requiring exit 0, empty stderr, an exact unique
   `c VERIFIED` transcript shape, and the expected LRAT clause totals;
9. confirms that all frozen inputs and private copies are unchanged; and
10. rejects 24 representative corruptions, including malformed DIMACS,
    deletions, early/post-empty records, noncanonical/truncated varints,
    variables above 9,802, checker failures, nonempty stderr, missing markers,
    a RAT core, and bit flips in both proofs, both tools, C-055, and constructor
    evidence.

Seven focused parser/transcript tests pass.  Two complete verifier runs
produced byte-identical evidence.  A complete run took about 4.2 seconds and
peaked below 71 MB resident memory on the campaign Mac.

## Exact-byte adversarial code audit

A separate exact-byte audit returned `ACCEPT_WITH_CAVEATS` for verifier SHA
`4adf3691...` and focused-test SHA `2ca00e46...`; it independently reproduced
the DIMACS and binary-proof censuses, replayed both retained checkers, rebuilt
both checker executables from their retained C sources and obtained
`VERIFIED`, and found no soundness blocker.

The nonblocking caveats are:

- the focused unit test covers the 18 base mutations, while the six decisive
  artifact bit-flips and full checker integration are exercised by the
  complete verifier replay rather than by that unit test;
- the verifier's self-hash is explicitly only provenance for a source file
  stable across the run, not authentication of already-loaded interpreter
  state, so the external hostile review must bind exact verifier bytes; and
- publication packaging should retain checker C-source hashes and build
  provenance in addition to the already bound executable hashes.

The last portability item is now retained in
`tool-source-provenance.json`: it binds both checker C sources and the
Makefile, records the compiler and exact clean-build commands, hashes the
freshly rebuilt executables, and records successful DRAT and LRAT replays.
Those clean-build hashes are supporting provenance; the verifier continues
to rely decisively on the separately frozen executable hashes.

## Reproduction

From the campaign root:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -W error \
  src/verifier_b/order13_k3_hole9_certificate.py > /tmp/evidence.json
cmp /tmp/evidence.json \
  reviews/order13_k3_hole9_certificate_verifier_b/evidence.json
PYTHONDONTWRITEBYTECODE=1 python3 -W error -m unittest -v \
  tests.test_order13_k3_hole9_certificate_verifier_b
```

The retained evidence remains candidate-only pending the campaign's separate
hostile acceptance and claim-integration review.
