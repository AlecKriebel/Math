# Shell-two structured action closure

## Result

The authoritative v2 certificate exhausts four bounded phase families on
all 84 distinct labelled action images of the five exact shell-two profile
orbits.  It finds five digit-two survivor occurrences, all in
`opposite_helical_c4`.  They remain five distinct classes after exact
deduplication by the common `C6` class-rotation action.  Their next-digit
defects are respectively 5, 6, 7, 8, and 12 of the 20 displayed equations.
Every one is fixed by minimal proper multiplier supergroup `8`; none is
proper-supergroup-free.  There is no survivor through lambda digit three.

Consequently this computation **does not pass the consecutive-lift gate**.
The five digit-two points are useful scope corrections and exact negative
data, but are not evidence of convergence to a Legendre pair.

The pinned certificate is
`ACTION_CLOSURE_CERTIFICATE_V2.json`, with semantic SHA-256
`e5a27d107a5e2f140feabb3a69a02c16044980a05baaa1523fafff3ef9d0d802`.

## Exact scope

The five source-orbit image counts are:

| Source profile orbit | Distinct labelled images |
|---|---:|
| `h2-222222-0` | 24 |
| `h2-422220-0` | 12 |
| `h2-422220-1` | 12 |
| `h2-422220-2` | 12 |
| `h2-422220-3` | 24 |
| **Total** | **84** |

The action manifest is derived from all 24 elements used by the frozen
shell-two classifier, deduplicated separately inside each source orbit, and
sorted lexicographically by the two identifier words.  Every image is
replayed as an exact physical profile before it enters a family audit.

The four bounded families and exact v2 totals are:

| Family | First-digit placements | Digit-two survivors | Best zero rows at digit two |
|---|---:|---:|---:|
| `opposite_planar_c3_envelope` | 72,900 | 0 | 18/20 |
| `opposite_twisted_c6` | 3,542,940 | 0 | 18/20 |
| `opposite_helical_c4` | 2,278,854 | 5 | 20/20 |
| F27 minimal submodules | 5,325 | 0 | 19/20 |
| **Total** | **5,900,019** | **5** | — |

For the F27 family, each image tests all `56^2 = 3,136`
channel-asymmetric minimal-submodule pairs, hence 263,424 pair tests over
the action closure.

This is an exhaustive result only for these four finite ansatz families.
It is not an exclusion of the full 36-dimensional first-digit solution
space, and it does not construct a Legendre pair or an `H(668)`.

## Survivor replay and equivalence accounting

Every digit-two survivor is retained explicitly and independently replayed
through:

1. the symbolic and direct first placement digit;
2. the symbolic and direct second placement digit;
3. exact Eisenstein values and lambda digits three through five;
4. all five tested minimal proper multiplier-supergroup constraints.

The common `C6` class rotation has an explicit labelled-placement action.
For each survivor the verifier constructs all six rotations and checks that
each still has zero first and second digits and the same digit-three defect.
The lexicographically least rotated pair of normalized mask words defines
the recorded equivalence hash.  The five observed survivor occurrences
have five different hashes.

The independent channel-star actions are included when producing the 84
profile images, but are **not** used to deduplicate lifted placements:
their action on the fixed labelled zero-column slice has not been proved in
this certificate.  This deliberate boundary prevents an unjustified
collapse of potentially distinct witnesses.

## Reproducibility and resumption

The production runner writes one atomic result per image.  On restart it
skips a result only after validating its complete semantic hash, the exact
image record, the action-manifest hash, all 22 transitive local source
hashes, histogram coverage, and every retained survivor.

Run or resume the authoritative computation:

```bash
python3 run_action_closure.py --output output/production-v2 --write-certificate
```

Verify the tracked certificate without relying on ignored output:

```bash
python3 verify_action_closure.py
```

Also compare the exact 84-file live output set:

```bash
python3 verify_action_closure.py --live
```

Rerun every enumeration from the frozen source and compare every semantic
record:

```bash
python3 verify_action_closure.py --full
```

All three verification modes passed on the authoritative v2 artifact.

The original `output/production` partial run used the superseded v1 schema.
It is retained only as an ignored diagnostic.  Only `production-v2` and
`ACTION_CLOSURE_CERTIFICATE_V2.json` are authoritative.

The completed v2 production run used one process, 555.84 summed image
seconds, and approximately 36.4 MB peak resident memory.  No parallel
workers or external services are used.

## Files

- `action_closure_common.py`: manifest derivation, exact family calls,
  survivor replay, C6 equivalence accounting, validation, and aggregation.
- `run_action_closure.py`: atomic resumable per-image production runner.
- `verify_action_closure.py`: strict pinned, live-output, and full-recompute
  verifier.
- `ACTION_CLOSURE_CERTIFICATE_V2.json`: complete tracked semantic
  certificate, including all 84 image records.
- `RESEARCH_LOG.md`: dated decisions and findings.
- `ARTIFACT_SHA256.txt`: detached file digests.
