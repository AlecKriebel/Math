# Portable PR204 finite scientific verification

`verify_portable.py` is a standard-library-only driver. It authenticates the142
material files in INPUT_PINS.json, copies the live verifiers into disposable
layouts, and runs28 required cases:14 valid executions and14 genuine false
identity/NaN controls. Every case runs with `-B`, and both ordinary and `-O`
modes are tested. Correct outcomes are required; merely returning an error is
insufficient for a negative control.

The external packages must already be SymPy1.14.0 and mpmath1.3.0. Nothing is
installed, downloaded, or copied from those dependencies. To select an existing
read-only package directory, set PR204_RUNTIME_PACKAGES; an existing PYTHONPATH
also works. Otherwise normally installed packages are used. All subprocesses
have PYTHONDONTWRITEBYTECODE=1 and PYTHONHASHSEED=0. The driver also disables
its own bytecode before importing the standard library.

From a publication package with the A204 relative paths mirrored in materials:

```sh
python3 -B portable_verification_01/verify_portable.py \
  --materials materials --work-dir verification-work \
  --output verification-receipt.json
```

An optional existing dependency location can be supplied without changing code:

```sh
PR204_RUNTIME_PACKAGES=/path/to/existing/runtime_packages \
  python3 -B portable_verification_01/verify_portable.py \
  --materials materials --work-dir verification-work \
  --output verification-receipt.json
```

`--materials` is recommended. Without it, the driver tries sibling materials,
parent materials, then its parent A204 directory, in that documented order; the
selected root is recorded. There is no hardcoded home directory. `--output -`
(the default) emits a JSON receipt with the compressed raw evidence embedded as
base64. A named output creates that new JSON file plus its
`.raw.json.gz` companion. Existing output files are not overwritten. Each temporary case
layout is removed immediately after capture, including on setup failure. `--jobs` selects1-4 workers (default2), and
`--timeout` sets the per-process timeout in seconds (default900).

Writes into any pinned material family are refused. Choose a work directory
and receipt location outside those immutable family directories. For the
original A204 layout, portable_verification_01 itself is a permitted writable
location. Author verification.json writes occur only inside its disposable
layout. No source wrapper with historical fixed runtime/output paths is run.

The live cases are:

- Physical shooting: valid and actual product-plus-one rejection in both modes.
- Exact low periods:209 valid checks and actual product-plus-one rejection in
  both modes.
- Source-analytic controls:187 active checks, including their internal false
  sentinel, in both modes.
- Direct geometry: valid exact/physical controls and their internal false
  identity rejection in both modes.
- Hardened complex-v2: valid runs plus genuine false symbolic identity,
  doubled numerical identity, and NaN residual rejection in both modes.
- Repaired original author/reviewer controls: valid output byte-for-byte equal
  to the archived JSON, and actual false chord/product rejection, in both modes.

Historical bare-assert verifiers and historical audit wrappers are records,
not live validation entrypoints. The complex-v2 fixture preserves its sealed
six-file parent layout and the exact parent manifest pin. Its standalone
verifier is run directly. The repaired author receives only an unchanged copy
of the historical original PROOF.md for its legacy hash calculation. That file
is explicitly historical and is not a new manuscript.

Valid outputs must match their pinned expected baselines and contain finite
numeric data. Only these fields normalize for baseline/mode comparison:
source optimization_flag; direct optimized_mode; complex utc, optimized and
runtime.method. Complex versions and bytecode-disabled status remain checked.
Repaired original output receives no normalization and must match raw bytes.
No mathematical result, count, residual, or predicate is discarded.

Receipts pin each executed code file and every raw stdout/stderr byte stream.
The gzip evidence preserves exact UTF-8 streams (base64 fallback for non-UTF-8), argv and working
directories, all input snapshots before/after including SHA256,size,mtime and
ctime, and dependency-cache inventory records. The receipt records exact
relevant environment overrides and software locations/versions without
dumping unrelated secrets. Any cache or immutable input change fails the run.
To inspect the raw evidence, decompress the companion with Python's gzip
module and parse the JSON. Encode stdout_utf8/stderr_utf8 as UTF-8, or decode
the stdout_b64/stderr_b64 fallback. Identical after-snapshots use an explicit
identical_to reference to the full before-snapshot, with both digests recorded.

These are finite exact controls and noninterval diagnostics. A PASS does not
establish universal phase constancy, validate historical execution flags, or
certify novelty or priority. The original historical defects remain recorded;
the portable driver does not rewrite that audit.
