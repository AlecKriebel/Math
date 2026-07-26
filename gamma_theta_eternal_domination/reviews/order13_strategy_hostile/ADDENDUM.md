# Addendum: revised order-13 strategy bytes

**Audit date:** 2026-07-26  
**Revised strategy:** 14,924 bytes, SHA-256
`5b59d8c9fcbf1eb2a3e20157fcef02b4faa02a48e62c6fbda7b9c1fc12e7d6c6`  
**Final revised pilot JSON:** 3,927 bytes, SHA-256
`4383dec046945223a7bd3d6b642996fdd5cfc6da4d03b041b2b1cd351369ed64`

## Verdict

**`ACCEPT_REVISED_DOCUMENTATION_AND_UNCHANGED_STRATEGY_CONTENT`**

This is an addendum to the historical audit of strategy
`eca21b54...e6b5c8` and pilot record `331630a5...b7148c`; it does not
rewrite that audit.

The revised strategy repairs both prose defects:

- its Proposition 1 dependency ledger now names C-003, C-006, C-036,
  C-049, and C-050, and no longer names the unused C-051;
- both pilot-time occurrences now say `0.0202` seconds, consistently
  rounding the recorded `0.020179042010568082`.

The revised strict JSON has schema/version
`gamma-theta-order13-strategy-k3-template-pilot-v2` / `2`.  Its
protocol-compliance block explicitly records that exact argv, CPU time, and
stdout/stderr were not retained and that the historical invocation is not
replayable.  The corresponding values are `null`, not reconstructed
surrogates.  Solver version `3.0.1` is labeled accurately as a post-hoc query
of the exact hash-bound binary, not as historical run metadata.  The pilot
remains `OBSERVED` and `UNSAT_UNCERTIFIED`.

The final pilot revision changes exactly one JSON string relative to the
previously audited 3,822-byte v2 record: its `claim_boundary`.  Bytewise
replacement of the new string by the old string reproduces SHA-256
`36d964a4741772a8f8c7783a852765623bd7b441d230cc7cf1da9bcdd7ab7d2d`
exactly.  The new wording distinguishes what was unaudited at run time from
the later hostile reconstruction and coverage audit, while again refusing
to promote the proofless UNSAT return.  This resolves the prior
present-tense contradiction without changing any formula or census field.

I reran the standard-library reconstruction from `audit.py`.  All four
formula byte streams retain exactly the previously audited hashes and sizes;
all template, coloring-bank, signature-breaker, and generic \(k=3,4,5\)
censuses are unchanged.  No mathematical, formula, coverage, or solver
claim was added, and no solver was run on a formula.

The current revised bytes therefore satisfy the historical review after
discharging its documentation corrections.  They remain a bounded strategy
and exploratory record, not a certified order-13 exclusion.

## Final-byte replay

The final bytes are replayed with:

```text
python3 reviews/order13_strategy_hostile/audit_final.py |
  cmp - reviews/order13_strategy_hostile/evidence_final.json
```

The command exits successfully and reproduces the retained evidence byte for
byte.  Its new artifacts are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `audit_final.py` | 14,572 | `ec4a6ef5ace6f35c2822ee41da754f2b04f58802e5466cf11984b7b5c6656c66` |
| `evidence_final.json` | 6,099 | `3457ada027bcf2887c7cf59d837992dc481fb0ea552c48cfb3122fc69a0a1548` |

The replay binds the final strategy and pilot, strict v2 semantics, the
unchanged historical auditor, all four reconstructed formula byte streams,
and the generic and signature-breaker censuses.  The historical
`audit.py`/`evidence.json` pair remains unchanged.
