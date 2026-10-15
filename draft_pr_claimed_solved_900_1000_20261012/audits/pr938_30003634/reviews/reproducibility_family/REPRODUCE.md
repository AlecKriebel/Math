# Reproduce this family

Obtain the immutable PR938 packet and independently supplied current-guard and original-manifest pins. Verify the current guard digest before running it. It is standard-library Python; full audit recovery additionally needs SymPy1.14.0 in the selected trusted interpreter.

Check a baseline 0644/0755 packet:

```sh
python -I -B /trusted/guarded_replay.py --packet /path/to/30003634 --check-only
```

Run the original author verifier through the fixed 44-file guard:

```sh
python -I -B /trusted/guarded_replay.py --packet /path/to/30003634 --python /path/to/trusted/python --script original/verify.py --mode normal
```

Repeat with modes O, OO and env2. env2 deliberately omits isolated startup for its worker so inherited PYTHONOPTIMIZE=2 actually reaches it. Add --readonly only when all packet files are 0444 and all directories 0555. Exact original mode and inventory requirements are retained.

For full original BOOTSTRAP replay, keep its original fixed pin and pass its normal arguments after --:

```sh
python -I -B /trusted/guarded_replay.py --packet /path/to/30003634 --python /path/to/trusted/python --script BOOTSTRAP.py -- --packet /path/to/30003634 --expected-manifest 149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30
```

The guard enforces the original44 bytes, so intentional packet mutation tests use the separately supplied hostile-controls driver and fresh disposable copies. run_replays.py and hostile_controls.py document the exact local runs and trust the already existing Python path recorded in RESULT.json. Set that driver constant to an equivalent trusted interpreter if reproducing elsewhere. They create tmp and raw only under this family. Do not copy those scratch outputs into a public package.

Independent leading-minor arithmetic is portable standard-library Python:

```sh
python -I -B /path/to/independent_finite_check.py --packet /path/to/30003634/original
```

Keep the packet quiescent during a run. This is finite verification, not a sandbox, formal topology verification, primary-source verification or a novelty certificate.
