# Research log: order-13 k=3 production referee v4

## 2026-07-26T18:32:00Z — failure localized

- Bound live attempt 1 as a terminal `RETRYABLE_NONCLAIM`; no solver,
  checker, or resource failure was promoted.
- Verbose private replay localized exit 80 to drat-trim's hard-warning path
  for a pseudo-unit propagation-reason deletion.  Raw record 4,694 adds unit
  `-954`; record 4,695 deletes `-954 -1 -13 -20`.
- A warning-permissive diagnostic found 2,604 warnings, all of that deletion
  class, then verified.  No tautology, RAT, or other warning occurred.
- Strict normalization accepted 117,926 canonical records, including 45,281
  additions, 72,645 deletions, and one final empty addition.  The normalized
  RUP replay and independent LRAT conversion/check succeeded privately.

## 2026-07-26T18:40:00Z — v4 semantic review

- Isolated the implementation delta to pipeline identifier v2 plus
  `-p -U` in the raw forward command; the normalizer remained byte-identical
  to accepted v3.
- Proved soundness from RUP entailment: with every deletion ignored, each
  retained addition is an entailed clause in a monotone sequence, so the
  model set remains exactly that of the original formula.
- Exhaustively checked 2,304 two-variable formula/clause pairs, including
  1,856 RUP cases, without a counterexample.
- Source inspection confirmed `-p` discards deletion steps, `-f` checks
  additions forward, and `-U` blocks entry to the RAT path after failed RUP.

## 2026-07-26T18:47:00Z — warning-path caveat repaired

- Found that pinned drat-trim's invalid-prefix warning can return exit zero
  despite `-W`; its source breaks before the nominal hard-warning exit.
- Confirmed the production output gate rejects that output because it
  contains `WARNING`, and the strict normalizer independently rejects the
  malformed prefix without leaving outputs.
- The protocol was updated to distinguish requested warning-fatal mode from
  the runner's authoritative clean-output policy.  Rebound the final protocol
  hash after that repair.

## 2026-07-26T19:01:07Z — final hostile replay accepted

- Exact live attempt-1 raw command `-i -f -p -W -U -t 1800` exited 0 with
  empty stderr, one clean `s VERIFIED`, and zero RAT lemmas.
- RAT-only, bogus-deletion, deletion-aware, and nonfatal-warning controls all
  had the required fail-closed behavior.
- Replayed every v1-v3 provenance, crash, mutation, recovery, and positive
  control against the final v4 bytes; all decisive counts matched.
- Independently passed all 25 focused tests.  Twenty-four ran read-only on
  shared bytes; the deliberate source-writing test passed in a private mirror.
- The complete live production-tree digest was identical before and after:
  `4304e2546e40a63ac66e01e18dbb49c761f54b65ad25dc5d122129d1343afdd7`.
- Generated `evidence_v4.json` twice with identical SHA-256
  `f9c05782d91321994d3841567df10f351b72d20326cf01f9764a729f265ab9d8`.
- Verdict: **ACCEPT** v4 runner engineering.  Live attempt 1 remains an
  unmodified v1 nonclaim and cannot be loaded as a v2 run.
