# Final verification transcript

Status: **VERIFIED**.

Definitions lock SHA-256:

```text
c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09
```

Active manifest body hash:

```text
fea4e1876d422234c7c25a7cc39a8e50a3e2a29eadac5b1d9fc4a4dc0f3c8f2a
```

## Commands and exact outcomes

```sh
python3 build_atlas.py --ports 4 5 6 7 --output certificates
```

Outcome: `EXACTLY_COMPUTED_PRIMITIVE_UNIVERSE`.

```sh
python3 verify_contract.py certificates
```

Outcome: `VERIFIED`; totals were 317 role classes, 148,479 labelled
primitives, 153,258 raw-to-labelled transports, and 19,290 decorated
ordinary-`T` relations.

```sh
python3 mutation_tests.py certificates --fixture-port-count 4 \
  --output mutation_transcript_p4.json
python3 mutation_tests.py certificates --fixture-port-count 7 \
  --output mutation_transcript_p7.json
```

Outcome: `ALL_MUTATIONS_REJECTED` in both fixtures, 17 of 17 each.

```sh
python3 verify_contract.py certificates --regenerate
```

Outcome: `VERIFIED`; `BYTE_IDENTICAL_REGENERATION`, 24 files.

Mutation transcript SHA-256 values:

```text
p4  309610eb5a845daf4466a2027641a78f3ea06585a48f2149d5c49bea04012211
p7  848bd1462f3a18b056b6c4f34166b9430a31e8bebde719dc83d8bf861b5f5b83
```

## Selected-core correction

The active audit certifies only `selected_retains_strong_core`. It explicitly
sets `intrinsic_selected_STC_membership_classified` to `false`. Both the
dummy-rule false-negative witness and the sink-omission intrinsic-`S_TC`
counterexample are manifest-bound.

