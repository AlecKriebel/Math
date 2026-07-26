# Independent referee addendum v4: deletion-agnostic raw RUP gate

## Verdict

**ACCEPT**

The v4 repair is sound and narrowly scoped.  Its only runner semantics change
is the new pipeline identifier and the raw-proof command

```text
drat-trim INSTANCE RAW -i -f -p -W -U -t LIMIT
```

The preserved attempt-1 production tree remains a v1
`RETRYABLE_NONCLAIM`; this review neither rewrites that tree nor promotes its
solver output.  Current v4 code deliberately refuses to load the old v1
manifest.

## Frozen target

| File | SHA-256 |
| --- | --- |
| `src/search/order13_k3/production.py` | `7223e9c789b50aa021371f07670af9ee1a2406fd649e1d84713ed4b566a7f11e` |
| `src/search/order13_k3/normalize_bdrat.py` | `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c` |
| `src/search/order13_k3/PRODUCTION_PROTOCOL.md` | `cec85e105e1372dc09de055f2b74bc80709b1a732c64541869c8106b6f2316a9` |
| `tests/test_order13_k3_production.py` | `51655e8764db2ad436e84041a8b81e83e07131bfdd88084158d6b8800052cc0a` |

The exact three-file worktree delta has SHA-256
`97a56d0ac649580480744766d56c58ad96f0a5a19c783245d85f4a10f0f19890`.
The normalizer is byte-identical to accepted v3.

## Why ignoring deletions is sound here

Let \(F\) be the original CNF.  Plain mode discards every deletion and checks
the additions in their original order.  Define

\[
G_0=F,\qquad G_i=G_{i-1}\land C_i.
\]

For each retained addition \(C_i\), `-U` permits success only when unit
propagation derives a contradiction from
\(G_{i-1}\land\neg C_i\).  Unit propagation is sound, so
\(G_{i-1}\models C_i\).  Therefore \(G_i\) and \(G_{i-1}\) have exactly the
same models.  Induction gives \(G_i\equiv F\) for every prefix.  A verified
root conflict or empty-clause conclusion consequently proves \(F\)
unsatisfiable.  No semantic property of a deletion record is used.

The pinned implementation matches this argument:

- `-p` sets `delete = 0`; deletion bodies are decoded but never inserted as
  proof steps (`drat-trim.c:1177-1195`, `1390-1414`);
- `-f` checks additions against the monotonically retained state
  (`drat-trim.c:769-850`);
- `-U` returns failure immediately after a failed RUP test, before the RAT
  path (`drat-trim.c:631-681`).

An exhaustive independent check covered every 2-variable formula over all
nontautological clauses and all possible added clauses: 2,304
formula/clause pairs, including 1,856 RUP pairs and 160 RUP-empty cases,
produced zero entailment counterexamples.

## Checker caveats and defenses

Hostile source review found that pinned drat-trim does not make every warning
process-fatal merely because `-W` is present.  In particular, its invalid
binary-prefix branch prints a warning and breaks before the hard-warning exit.
The final protocol now describes this accurately: `-W` requests
warning-fatal behavior, while the runner independently rejects a nonzero
exit, stderr, warning/error text, or a non-unique clean marker.

A tiny proof exercising that exact drat-trim branch returned exit zero with
both a warning and `s VERIFIED`.  The runner's `_strict_verified` rejected it,
and the mandatory normalizer independently rejected its invalid prefix and
left no output.  Other retained defenses are also essential:

- `-t` is not checked by drat-trim's forward loop, so the external bounded
  child deadline remains authoritative;
- operands must remain first because the checker opens `argv[1]` and
  `argv[2]`;
- the checker binary parser is permissive around some malformed varints, so
  the strict full-stream normalizer and second RUP replay remain mandatory.

These caveats do not create an acceptance path in the six-phase pipeline.

## Exact frozen attempt-1 replay

The referee ran the exact command against the live read-only instance and raw
proof:

```text
/Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination/tools/drat_trim_2023_05_22/drat-trim
/Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination/results/order13_k3_hole9_production/attempts/attempt-000001/instance.cnf
/Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination/results/order13_k3_hole9_production/attempts/attempt-000001/proof.raw.bdrat
-i -f -p -W -U -t 1800
```

It returned exit 0, empty stderr, exactly one clean `s VERIFIED`, and
reported zero RAT lemmas.  Bindings were:

| Object | Size | SHA-256 |
| --- | ---: | --- |
| instance | 1,168,197 | `3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea` |
| raw proof | 1,900,168 | `ecfb35ba56b5ce2a04437f381e357525581f3bcb6403290272984700d805dbeb` |
| stderr | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| timing-normalized stdout | — | `17016a876f1740f3c8730717fda157a189dec3877998348ab30c22afe589982b` |

Additional pinned-checker probes established:

- a RAT-only, non-RUP addition is rejected by `-U`;
- a bogus deletion hint is ignored in `-p` mode, while the deletion-aware
  warning-fatal control exits 80;
- the nonfatal `-W` warning path is rejected by both the runner output gate
  and strict normalizer.

## Preserved regression replay

Every v1-v3 synthetic hostile case was rerun against the current bytes:

- all six v1 malformed-metadata attacks;
- all four v2 adjacent producer/consumer substitutions;
- coherent formula, LRAT, phase-binding, certificate, and outcome mutations;
- four pre-`RUN_STARTED` crash windows;
- two opaque uncheckpointed-outcome cases;
- three orphan-quarantine and four outcome-quarantine crash prefixes;
- six malformed/symlink/extra orphan envelopes;
- positive phase, SAT semantics, resource, source/tool binding,
  normalization, interruption, and read-only audit controls.

All required rejection and safe-recovery counts matched accepted v3.  Three
coherently rehashed attempt-config mutations, each deleting one of `-p`,
`-W`, or `-U`, were also rejected.

The latest focused suite passed 25/25 independently: 24 tests ran against the
shared tree without writing source bytes, and the one deliberate
source-mutation test passed in a private full-source mirror.

## Live-tree and claim boundary

The complete live production-tree digest was identical before and after every
real checker and synthetic replay:

```text
4304e2546e40a63ac66e01e18dbb49c761f54b65ad25dc5d122129d1343afdd7
```

Its terminal checkpoint remains
`be3aa0a50f31a61ba7655c5795f21b4e88468eacd348183ada2f2a6e38c368d4`;
its outcome remains
`aa943916e4bb3e46cc2dd2d00f0593f959ad52e45c14202c497f968cd0ab915f`
with status `RETRYABLE_NONCLAIM`, claim status
`NO_SAT_OR_UNSAT_CLAIM`, and phase
`RAW_FORWARD_REJECTED_NONCLAIM`.

Acceptance is for the v4 runner engineering and full proof pipeline only.  A
future production tree must be initialized under pipeline v2 and independently
audited; the v1 attempt is not silently reinterpreted.

## Reproducible evidence

| Artifact | SHA-256 |
| --- | --- |
| `referee_regressions_v4.py` | `caf077fa9eb64ca368bf3c17c29e818cc8a36b72b3f4fa6a00e1f7d1382b24f3` |
| `run_readonly_upstream_tests_v4.py` | `b783a4e14a85ffa27ca95ad4cdf11026f4fbe6ce17f997a0acd4943d9562465d` |
| `evidence_v4.json` | `f9c05782d91321994d3841567df10f351b72d20326cf01f9764a729f265ab9d8` |

Two consecutive evidence generations were byte-identical.  The hostile
harness launched pinned drat-trim five times and no SAT solver.  The focused
suite's committed-certificate integration test supplied a separate exact
raw-proof replay.

Run from the campaign root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /opt/homebrew/opt/python@3.14/bin/python3.14 \
  reviews/order13_k3_production_referee/referee_regressions_v4.py \
  --output reviews/order13_k3_production_referee/evidence_v4.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /opt/homebrew/opt/python@3.14/bin/python3.14 \
  reviews/order13_k3_production_referee/run_readonly_upstream_tests_v4.py
```
