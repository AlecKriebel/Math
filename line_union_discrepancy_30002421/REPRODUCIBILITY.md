# Reproducibility and numerical limits

## What is mathematical, and what is diagnostic

The proofs in Attempts 1–5, the weighted-square note, and the independent audit are the mathematical deliverables. The axis-parallel counterexample sequence follows from the cited Borda theorem and exact full-chord identities. It does not rely on a finite computation, a value of Borda's constant, or a machine-certified finite counterexample.

The numerical experiment is an optional deterministic-seed floating-point diagnostic. It forms approximate chord lists for the three cyclic permutations of (sqrt(2),sqrt(3),1), and samples 1,920 contained cubes for each n in {8,16,32,64,128,256}. There are four special frames (ambient axes plus one aligned with each direction) with 180 samples each, and 24 random orthonormal frames with 50 samples each. The generator seed is 182530002421.

An exactly evaluated maximum on finitely many valid cubes would be a lower bound on the full supremum, never an upper bound. These floating-point values are not asserted to be certified lower bounds either. Event sorting, irrational crossing positions, QR frames, containment, clipping, and numerical roundoff are not protected by exact or interval arithmetic. The clipping code treats directional coordinates of magnitude below 1e-12 as zero. No certified numerical counterexample or asymptotic inference is claimed.

## Dependencies

Recorded replay environment:

- CPython 3.12.14.
- NumPy 2.3.5, pinned in requirements.txt.
- Linux x86_64.
- Python standard library: pathlib, json, math, hashlib, platform, shutil, subprocess, sys, tempfile.

No network, external dataset, source PDF, credential, repository checkout, or files outside this package are required. A compatible Python installation with the listed dependency is sufficient. Different numerical libraries, CPUs, or NumPy versions can change floating-point results and QR frame signs. An exact parsed match is reported only for the recorded replay; it is not promised universally.

## Recommended isolated replay

From the package directory:

```sh
python verify_replay.py
```

The checker copies test_direction_mixtures.py into a fresh temporary artifact directory and runs it with a different, empty working directory. It confirms that the output JSON is written beside the copied script, not into the working directory. It compares the generated JSON to the included baseline, preserves that baseline, cleans the temporary directory, and writes REPLAY_VERIFICATION.json beside the checker.

The comparison recursively excludes only the declared timing-key names. No timing fields are present in the current diagnostic data. Integers and nonnumeric metadata are compared exactly. Floating values are checked for finiteness and compared with relative tolerance 1e-11 and absolute tolerance 1e-12. The report separately records whether every parsed field, excluding timing, agrees exactly. These tolerances are reproducibility tolerances, not mathematical error bounds.

Recorded result: **PASS; all 271 numeric fields compared, exact parsed output match, maximum absolute and relative differences both zero.** The script SHA-256, baseline SHA-256, replay-output SHA-256, environment, comparison details, and six output summary lines are in REPLAY_VERIFICATION.json. Timing is neither recorded nor compared. A successful replay establishes consistency of this diagnostic computation, not the correctness of the mathematical theorems.

## Direct experiment run

```sh
python test_direction_mixtures.py
```

This writes DIRECTION_MIXTURE_EXPERIMENT.json beside the script, regardless of the current working directory. It replaces that sibling file. Prefer the isolated checker if the included baseline must remain unchanged. The main script prints n and the sampled values of L times discrepancy for the single-family and three-family cases.

The JSON records the seed, numerical warning, n, chord counts, approximate length sums and maximal piece length, sample count, and the maximizing sampled cube's frame, center, side, and discrepancy statistics. All numerical fields are authored experimental output, not copied dataset contents.

## Integrity manifest

MANIFEST.json lists the relative path, byte count, and SHA-256 of every public package file except MANIFEST.json itself, which is excluded to avoid self-reference. It also records the intended public directory and the status split. Re-running a script can update a recorded output or report; refresh the manifest only after any intentional content change has been reviewed.

Verify the included bytes with Python from this directory:

```sh
python - <<'PY'
from pathlib import Path
import hashlib, json
root = Path('.')
manifest = json.loads((root / 'MANIFEST.json').read_text())
listed = {entry['path'] for entry in manifest['files']}
actual = {p.as_posix() for p in root.rglob('*') if p.is_file() and p.name != 'MANIFEST.json'}
assert actual == listed, (actual - listed, listed - actual)
for entry in manifest['files']:
    data = (root / entry['path']).read_bytes()
    assert len(data) == entry['bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
print('Manifest verified.')
PY
```

The independent mathematical audit accepted the weighted transfer and Attempts 3–5 within their stated restrictions before the package manifest was frozen. Numerical reproducibility and byte integrity are separate checks from that audit.
