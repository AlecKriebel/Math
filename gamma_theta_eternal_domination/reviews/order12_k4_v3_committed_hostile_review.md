# Order-12, k=4 v3 committed hostile engineering review

Status: **ENGINEERING_NO_MATHEMATICAL_CLAIM**

Reviewed commit: `f4ccb1672e8e540bfe57f8472e44b4b3184a7b69` on
`main`.

## Verdict

The exact committed v3 runner and normalizer design is accepted for production
use. The final hostile review found no remaining proof-soundness, provenance,
schema, crash-recovery, or legacy-isolation blocker.

This is an engineering verdict only. No order-12 production solver was
launched, no retained leaf was promoted, and this review proves no finite or
universal mathematical claim.

## Exact committed bytes

The working files matched both their Git blobs at the reviewed commit and the
required SHA-256 values:

| File | Git blob | SHA-256 |
|---|---|---|
| `src/search/k4_production/runner.py` | `dd4a7b37c040dd70596d75ce9b51301c8cb0905d` | `39d690edc72d852b36b637497ef44463ebd80a51d3b13479d96e31becb939cfb` |
| `src/search/k4_production/normalize_bdrat.py` | `77a987d3c9c6d558b9d7185638cf2b9e6baccc65` | `07229fce9293a05fed3fa6ef3f96415eb48ea4b0cdd8e9a329620017d2bced99` |
| `tests/test_k4_production.py` | `999df7f3161e973589fec32c72e7100ddf3e0bb0` | `4f2fa849a60bc3acb4038e5dac0ee3d34fad997fd9de7c1e37922e88ee4fd7fc` |
| `README.md` | `fb2d9fd41e0ecaafe9658f098765af424dbd22f1` | `f571844872dd65b2cfe30b6b3c7229bbb13cc1eb8cc7271f41de45235c51066e` |
| `math/lemmas/order12_k4_partition_plan.md` | `8680df36ae90c6be335124cebf35a17d59bfbe78` | `f49a7ddfc3e7845b59fd9aa2f2938e0802f0d100241819b8b24953d8009b9ad4` |

The unmocked runtime source binding passed with source-set SHA-256
`4c8988b1e7967e2e4d59f73e0b6323900266c5b23fc94e0e19fc5a68fbc2921e`.

## Exact committed test replay

Command:

```text
PYTHONHASHSEED=0 PYTHONPATH=src /usr/bin/time -p python3 -m unittest tests.test_k4_production -v
```

Result:

```text
Ran 29 tests in 131.929s

OK
real 132.07
user 127.70
sys 2.26
```

Exit code: `0`.

The suite includes the real tiny six-stage proof chain, strict binary
normalization and hostile parser inputs, v2 refusal before lock or write,
both atomic pre-configuration recovery states, decisive provenance and schema
mutation, resource and log mutation, unclean verifier output, and unmocked Git
binding. Its solver invocation is the tiny regression fixture, not an order-12
production solve.

## Previously conditional findings now closed

The exact committed bytes close every issue raised during the moving-snapshot
review:

- the audit requires exact v3 outcome and certificate key sets;
- decisive outcome details are bound exactly to the certificate and all six
  child records;
- all six child commands, command hashes, executable hashes, exits, limits,
  logs, paths, hashes, timestamps, finite nonnegative accounting values, RSS
  units, and positive available-memory measurements are checked;
- all six resource reports receive semantic checks;
- the solver result is reparsed as strict UNSAT;
- the decisive artifact inventory and aggregate-status boundary are exact;
- normalization claims are independently checked against a full canonical
  binary-DRAT scan and the exact emitted addition stream;
- warning-bearing verifier output is rejected;
- v2 run and recovery entry points refuse before acquiring a lock or writing;
- runner-authored final files are atomically published;
- interruption before the case CNF or attempt configuration is published is
  deterministically reconstructed and sealed as a retryable nonclaim;
- interruption after normalization, certificate publication, or outcome
  publication is fail-closed and explicitly recoverable.

The decisive path cannot reach `UNSAT_LRAT_VERIFIED` without six successful
children: solver, raw forward verification, strict normalization, normalized
RUP-only forward verification, RUP-only LRAT conversion, and independent
`lrat-check` replay.

## Retained v2 case-1111 diagnostic

The retained v2 case-1111 CNF and raw binary proof were copied to a temporary
directory. Only the temporary copies were passed through:

1. raw binary-DRAT forward verification;
2. the strict v3 normalizer;
3. normalized `-U` forward verification;
4. normalized `-U` backward LRAT conversion;
5. fresh `lrat-check` replay.

All five commands exited `0`. The retained source files had identical hashes
and filesystem metadata before and after the diagnostic. Reproduced outputs:

- normalized proof:
  `f3401ad850f65db8808cd0949e6899ba6b6718902f83a289225c7f5b6390302d`,
  106318 bytes;
- converted LRAT:
  `90787a09742237e3c38c8b4f36916b2d0ccbd37be3920feb16ddb3306ec228d0`,
  692139 bytes.

The raw proof scan found 16646 records: 9690 additions, 6956 deletions, and
three post-empty deletions; the empty addition was record 16643. This
diagnostic did not mutate or promote the frozen v2 attempt.

## Mandatory claim boundary

`audit_run` is deliberately read-only. It validates retained execution
provenance but does not freshly replay retained LRAT semantics and returns no
mathematical claim.

Before any finite order-12 theorem can be stated, the separate aggregate
verifier must freshly replay every bound LRAT against its bound leaf CNF and
independently verify the Boolean partition coverage. This requirement remains
mandatory even after this engineering acceptance.
