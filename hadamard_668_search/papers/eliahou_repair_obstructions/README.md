# Paper A: exact repair obstructions around Eliahou's order-668 seed

This folder contains the standalone manuscript
`eliahou_repair_obstructions.tex` and its compiled PDF.  The paper uses only
promoted exact results and explicitly omits the obsolete uncertified local
radius claim.

Immutable companion release:

<https://github.com/AlecKriebel/Math/releases/tag/h668-research-checkpoint-v1.0.0>

## Claim boundary

The manuscript establishes, in the scopes stated there:

1. an independent exhaustive certificate that `TU(41)` is empty and the
   resulting fixed-`q` obstruction;
2. a base-row distance lower bound of 80 and special-coordinate lower bound
   of 41 around Eliahou's published seed;
3. the complete `39 s-only + 2 q-only` classification at special distance
   41, followed by the 39-pair root frontier;
4. checked unsatisfiability of the canonical long boundary case `L0`;
5. complete exact exclusion of all nine canonical short cases; and
6. exact modulo-8/16/32 orientation reductions for the twenty open long
   cases, with the correction that the two 42-fold norms prove cyclic, not
   aperiodic, complementarity.

It does **not** exclude the other twenty long cases, all distance-41
repairs, `BS(84,83)`, a nonspecial Golay quadruple, or `H(668)`.

## Build the paper

From this folder:

```sh
tectonic --keep-logs --keep-intermediates \
  eliahou_repair_obstructions.tex
```

The expected output is `eliahou_repair_obstructions.pdf`.  The frozen draft
was built with Tectonic 0.16.9.  A successful build has no undefined
references, overfull boxes, or underfull boxes.

For a quick PDF metadata check:

```sh
pdfinfo eliahou_repair_obstructions.pdf
```

## Portable verification environment

The promoted requirements now pin the numerical stack used by this paper.
The primary tested environment was Python 3.11.8 with NumPy 2.4.6,
OR-Tools 9.14.6206, and python-sat 1.8.dev24.  From the repository root,
create an isolated environment with Python 3.11 or 3.12:

```sh
python3.11 -m venv .venv-h668-paper-a
. .venv-h668-paper-a/bin/activate
python -m pip install --upgrade pip
python -m pip install -r hadamard_668_search/requirements.txt
python -c 'import numpy; print(numpy.__version__)'
```

The final command should print `2.4.6`.  Set `H668_PYTHON` to
`.venv-h668-paper-a/bin/python` in the commands below.  The standard-library
checks do not require this environment.

## Quick exact verification

Start in the repository's `hadamard_668_search` directory.  The first group
uses only the Python standard library:

```sh
python3 verify_fixed_q_obstruction.py
python3 verify_eliahou_adjacent42_repair.py
python3 verify_eliahou_antifold42.py
python3 verify_eliahou_antifold_q0_proof.py
```

Verify the independent Turyn enumeration:

```sh
cd tu41_certificate
python3 verify_manifest.py
python3 verify_cube_cover.py cubes_depth5.txt
python3 test_regressions.py
cd ..
```

The remaining quick verifiers require the numerical Python environment used
by the research repository.  Set `H668_PYTHON` to a compatible interpreter;
the development machine currently uses
`/Users/alec/Documents/tmp/hadamard-env/bin/python`.

```sh
H668_PYTHON=/Users/alec/Documents/tmp/hadamard-env/bin/python

env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$H668_PYTHON" \
  eliahou_short_block_census/verify_nine_case_completion.py

PYTHONDONTWRITEBYTECODE=1 "$H668_PYTHON" \
  eliahou_long_orientation_cascade/audit_orientation_cascade.py

PYTHONDONTWRITEBYTECODE=1 "$H668_PYTHON" \
  eliahou_long_orientation_redteam/audit_exact_ternary_model.py

PYTHONDONTWRITEBYTECODE=1 "$H668_PYTHON" \
  eliahou_long_orientation_redteam/verify_pinned_root_survivor.py
```

The short-case verifier is output-independent by default: it regenerates the
models, checks the frozen completion certificate and tracked hashes, and
performs independent retained-witness replays.  Add `--live` to inspect all
2,304 retained production-range manifests when the ignored production
directories are present.  Without those manifests, the survivor-stream
digests are cryptographic commitments rather than inspectable survivor
lists.  The immutable companion release includes the production-manifest
archive needed by `--live`.

## Full proof and production replay

The case-0 DRAT proof can be replayed with `zstd` and `drat-trim`:

```sh
python3 verify_eliahou_antifold_q0_proof.py \
  --full --drat-trim /absolute/path/to/drat-trim
```

The original replay used about 471 MB peak resident memory and 75 seconds.

Regenerate the canonical case-0 CNF in memory and print its deterministic
dimensions and SHA-256 without solving:

```sh
"$H668_PYTHON" search_eliahou_antifold_sat.py \
  --ignore-profiles --start 0 --stop 1 \
  --modulus 42 --hensel-mod4 --list-instances
```

The output must report 39,580 variables, 127,589 clauses, and
`f3eb29b1ea9c386e53b03726349fe0c38577d7e187b56aa19f86412c8749755d`.
Check the released DIMACS file itself with:

```sh
shasum -a 256 output/antifold42_q0_proof/antifold_00.cnf
```

A complete fresh `TU(41)` enumeration and the complete nine-short-case
production census are substantially longer than the quick checks.  Their
exact resumable commands and resource limits are documented in:

- `tu41_certificate/README.md`
- `eliahou_short_block_census/README.md`

The nine-short-case production replay performs approximately 3.71 trillion
modular join rows.  Ordinary manuscript verification should use the frozen
certificate and bounded independent replays unless a complete independent
production rerun is specifically desired.  The companion release includes a
compact production-manifest archive for live validation; it does not replace
an independent full rerun.

## Promoted certificate anchors

| artifact | SHA-256 |
|---|---|
| `tu41_certificate/certificate.json` | `87f8853faedc5f63e44cd8f5d1bb263172a7e051956c29f7ea162fb421b67635` |
| `tu41_certificate/cubes_depth5.txt` | `3901ebe4291d881805cd59b9eec8636277d8750eb8ef893b24c2ff238c92f47b` |
| `output/antifold42_q0_proof/certificate.json` | `30712ff06cb9387f953e638b7c0388986fcab4a58c240e1df7c16b0a0ddb8dee` |
| `output/antifold42_q0_proof/antifold_00.cnf` | `f3eb29b1ea9c386e53b03726349fe0c38577d7e187b56aa19f86412c8749755d` |
| `output/antifold42_q0_proof/antifold_00.drat.zst` | `efd8abd9d80d50365822754f36345f368d7cff8f2740ca33b9cab7d5866aa519` |
| `eliahou_short_block_census/NINE_CASE_COMPLETION_CERTIFICATE.json` | `fdb06b6075883d3138814d7471cfbdc7d13ddaa2a650fa8a9efc3cca242e1556` |
| `eliahou_short_block_census/SHORT_BLOCK_CERTIFICATE.json` | `cd560390bfb1dbea1d0b23b0ea7fe1afff66f247d5c017aeee375f82f2af9fff` |
| `eliahou_long_orientation_cascade/EXPECTED_SAMPLE5_SUMMARY.json` | `c9e63cb04c38bfe3e5c55cab95523eda82faf7596e5869fcc4bc2efaec7f6218` |

These hashes anchor the promoted inputs used by the manuscript.

## Disclosure

The manuscript names Alec Kriebel as the human author and prominently
discloses substantial assistance from ChatGPT 5.6 Sol.  It is dated
25 July 2026, marked not peer reviewed, and includes a detailed verification
and responsibility disclaimer.
