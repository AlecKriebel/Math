# Optimization-safe verification copy

These four scripts are separately repaired copies of the frozen PR 436 verifiers. `REPAIR_PROVENANCE.json` identifies every original/repaired script hash and every unchanged mathematical-input hash. Frozen author bytes were not edited.

For a standalone replay, make an isolated copy of the frozen 2569 attempt at head `c7805ab0804f50c6f4b0d1dda99e433dbb702ae2`, then overlay only the four repaired scripts at the same relative paths. Keep the original proof and `independent_audit/a5_idempotents.json` as inputs. Run:

```sh
python verify_counterexample.py
python verify_controls.py
python contributor_checks/check_character_data.py
python independent_audit/independent_audit.py
```

Repeat with `python -O` to check the optimization-safe mode. Both modes should produce the frozen JSON byte for byte. All 82 validation checks use explicit failure branches, so optimization does not disable them. The source manifest refers to the frozen originals; use this repair's provenance to identify overlaid code.

The exact validated versions are Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0. The first two scripts need only Python's standard library; the latter two require SymPy. `requirements.txt` records the tested symbolic dependencies.

Within the complete audit case, run the parent `repair_replay.py --python PATH` to reproduce all baseline and fault tests in private fixtures. Use a fresh private fixture directory; the runner refuses to overwrite existing records. No successful finite replay alone certifies the general semiperfectness theorem.
