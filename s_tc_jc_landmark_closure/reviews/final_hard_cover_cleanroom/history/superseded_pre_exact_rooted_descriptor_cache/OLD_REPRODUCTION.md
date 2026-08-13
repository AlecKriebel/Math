# Reproduction

Run from the repository root.

## Scoped release entry point

```bash
bash reviews/final_hard_cover_cleanroom/verify_all.sh
```

This first verifies `MANIFEST.sha256`, performs the complete independent
schema-3 n=4 theta-2 base and probe regeneration, reruns the supporting
universe, conditional p/q-enumeration, and mutation checks, and verifies the
manifest again.  Use `--quick` to replace the full algebra regeneration by
the certificate-integrity and actual-stream mutation replay:

```bash
bash reviews/final_hard_cover_cleanroom/verify_all.sh --quick
```

Both modes deliberately stop at this scoped n=4 theta-2 verdict.  Neither is
an n=3 or global-classification verifier.

## Fast integrity and mutation replay

```bash
bash reviews/final_hard_cover_cleanroom/verify_schema3_n4_quick.sh
```

Expected final hashes:

- base full audit:
  `245321c8e17c6b27fc2c5230b4074459d106a3c37454c90e1ff84f902954a1a4`;
- probe structure:
  `e586e17213a37d075cca714d597b0d03a9fa0aa5fb8ed91a5567da3095c8425c`;
- probe algebra:
  `d954013945e74c99dc28c2ab55541531cf491e413473ada8931c45e74758f3a8`;
- base mutation suite:
  `875d13e64f4cceb8c9d4be46457d72a3a14ad6927929c5f80dc1211f2d7e97e1`;
- probe mutation suite:
  `93ed47297ec22b3ac8c50921c05ef6bfdc1f125992e1ca0508970d857bed4e18`.

## Full clean-room regeneration

```bash
bash reviews/final_hard_cover_cleanroom/verify_schema3_n4_full.sh
```

This reruns the base graph/path/terminal audit, both mutation suites, the full
23,400-graph probe structure audit, and exact algebra for all 168,582 probe
states.  On the reference Apple M1 Pro it takes roughly fifteen minutes and
uses one CPU core with modest memory.

The scripts default to `/opt/homebrew/bin/python3`.  The exact algebra imports
SymPy 1.14 from
`/Users/alec/Library/Python/3.9/lib/python/site-packages`.  Override
`PYTHON_BIN` and `SYMPY_SITE` if an equivalent clean environment exposes the
same dependencies elsewhere.

## Broader clean-room component checks

```bash
PYTHONPATH=reviews/final_hard_cover_cleanroom:/Users/alec/Library/Python/3.9/lib/python/site-packages \
  /opt/homebrew/bin/python3 reviews/final_hard_cover_cleanroom/verify_universes.py
PYTHONPATH=reviews/final_hard_cover_cleanroom:/Users/alec/Library/Python/3.9/lib/python/site-packages \
  /opt/homebrew/bin/python3 reviews/final_hard_cover_cleanroom/verify_pq_extension.py
PYTHONPATH=reviews/final_hard_cover_cleanroom:/Users/alec/Library/Python/3.9/lib/python/site-packages \
  /opt/homebrew/bin/python3 reviews/final_hard_cover_cleanroom/mutation_tests.py
```

These produce, respectively:

- `1f2d76f387c87f75b8ebc9a3b4752cd09d76df2fdcf4d3107e0c1c4a2aa9b0d5`;
- `667dc415462b5f0b520e20f26d4e5c725190fdccb38e960d8d013c7f544ec308`;
- `5fea627f35ba851ee5b14dbf90eb6814f1c9f3c267ca6a6a082ec429d4a6adb9`.

The historical `verify_quick.sh` intentionally includes the quarantined n=3
schema-2 audit and therefore remains fail-closed.  It is not the verification
entry point for the corrected n=4 schema-3 subgate.
