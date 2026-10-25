# K2P-SAME reproducibility package

This archive accompanies *Generic Identifiability and Directed Containment for
Strongly Tree-Child Level-2 Networks under Positive-Fourier K2P: The Principal
Positive Domain and Strict Continuous Time*.

It is the publication reproducibility package, not a referee-process record.
It contains the exact article and supplement sources, rendered PDFs, theorem
crosswalk, generated certificate tables, verifier code, locked finite
certificates, replay reports, and mutation evidence needed to audit the
computer-assisted part of the result. Standalone AI-referee prompts and
reports, and submission-review dispositions, are deliberately absent. Sealed
technical research and audit records remain where the accepted evidence lock
requires their exact paths and bytes.

## Scope and authority

The mathematical theorem is stated in
`proof_compression_submission/article/main.tex`. The finite evidence authority
is `work/final_theorem_release/RELEASE_LOCK.json`. Its recursive 408-file
closure is recorded by `output/referee/REFEREE_BUNDLE_CONTENTS.json` and has
content-ledger root

```text
ed3beb4fca8338a3b97c7e5a0ff2bb58460ee7a244ea030bb7d3f837b5563d73
```

The word `referee` remains in a few historical paths because those exact path
names are part of the sealed computational evidence. It does not indicate that
private referee correspondence or reports are included.

The release proves the classification on

```text
D_plus = {0 < s < 1, 0 < g < 1, g > 2s - 1},
```

its strict continuous-time corollary `0 < s < 1, s^2 < g < 1`, and the
`4n-3` weak-class sharpness theorem. It makes no mixed-sign claim.

## Integrity check

From the extracted archive root, run:

```sh
python3 -B proof_compression_submission/zenodo/verify_zenodo_reproducibility_package.py \
  --root .
python3 -B output/referee/build_referee_bundle.py --check-only
```

The first command checks the publication archive manifest, exact allowlist,
every byte hash and size, the frozen content root and lock, the source/PDF
bindings, the successful 41-layer replay, theorem crosswalk, and mutation
censuses. The second independently reconstructs the recursive frozen ledger.

The packaging-specific regression suite is:

```sh
python3 -B proof_compression_submission/zenodo/test_zenodo_reproducibility_mutations.py
```

## Environment

The package does not contain a machine-specific virtual environment. Python
3.11 or newer is required. To reproduce the qualified environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install \
  -r work/final_theorem_release/requirements.txt
```

The release was qualified with Python 3.14.6, NetworkX 3.5, and SymPy 1.14.0.

## Verification paths

The compact, minutes-scale qualification is:

```sh
.venv/bin/python -B work/final_theorem_release/build_release_lock.py \
  --check --require-ready
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py \
  --quick
.venv/bin/python -B proof_compression_submission/verify_compressed_release.py \
  --check
.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py \
  --check
```

The release-level and proof-compression mutation suites are:

```sh
.venv/bin/python -B work/final_theorem_release/run_release_mutations.py
.venv/bin/python -B proof_compression_submission/run_compression_mutations.py \
  --check
```

For complete primitive regeneration, run the long path once and wait for it to
finish:

```sh
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py \
  --full
```

The accepted clean detached replay passed all 41 layers. Its exact report and
resource telemetry are included at
`proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json` and
`proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json`.

## Deterministic rebuild

To rebuild the publication archive from an extracted copy:

```sh
python3 -B proof_compression_submission/zenodo/build_zenodo_reproducibility_package.py \
  --output /tmp/K2P_SAME_Reproducibility_Package_v1.0.5-r1.zip
python3 -B proof_compression_submission/zenodo/verify_zenodo_reproducibility_package.py \
  --archive /tmp/K2P_SAME_Reproducibility_Package_v1.0.5-r1.zip
```

All archive members have a fixed timestamp, mode, order, and compression
policy. The archive's external SHA-256 appears in the Zenodo upload-set
manifest and `SHA256SUMS`; it is not embedded in the archive itself.

## Licenses

Article, supplement, figures, tables, and mathematical certificate data are
CC BY 4.0. Verifier and build code are MIT licensed. See `LICENSES.md`.
