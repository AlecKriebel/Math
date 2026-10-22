# Portable reproduction

Run commands below from this package's directory. Scripts that read or write saved artifacts resolve those paths relative to their own file, not the caller's working directory. The core certificate checks need only Python 3.10+ and its standard library. The two C++ programs need a C++17 compiler supporting the GNU/Clang `__builtin_popcountll` intrinsic (tested with g++). No SymPy is needed.

## First step: reconstruct the transported certificate

```
python computation/reconstruct_certificates.py
```

The largest certificate, `finite_certificate_d3_n5.json.gz`, is not shipped as a binary file. Its original gzip bytes are transported losslessly as 47 numbered base64 text files under `computation/certificate_parts/`. Each file has at most 32,768 ASCII characters, including its final newline. No gzip decompression or recompression occurs during transport or reconstruction. The other eleven gzip certificates are shipped directly and unchanged.

The standard-library reconstructor requires the exact part roster, verifies each part's byte count and SHA-256, strictly decodes base64, and verifies the complete original length and hash before an atomic write:

- Original gzip byte count: 1,146,536.
- Original gzip SHA-256: `25835b71af17eb7eab18d817b1f65d9aceb380d169a7b5ab317ee82388a4c716`.

Missing, extra, or corrupted parts cause failure without writing the output. An existing identical output is verified and retained; an existing different output is rejected. Checks are explicit exceptions and remain active under `-O` and `-OO`. The reconstruction script resolves every path relative to itself, so the command can also be invoked by absolute path from outside the package.

## Recommended independent replay

```
python computation/reconstruct_certificates.py
python computation/check_repairs_independent.py
python -O computation/check_repairs_independent.py
python -OO computation/check_repairs_independent.py
python computation/audit_finite_independent.py
python -O computation/audit_finite_independent.py
python -OO computation/audit_finite_independent.py
python -OO computation/audit_compression_independent.py
python -OO computation/audit_boundary_independent.py
python -OO computation/audit_boundary_counts.py
python -OO computation/audit_trades_independent.py
python -OO computation/verify_upset_bound.py
g++ -std=c++17 -O2 computation/enumerate_upsets.cpp -o /tmp/sumfree-enumerate
/tmp/sumfree-enumerate
g++ -std=c++17 -O2 computation/audit_upsets_independent.cpp -o /tmp/sumfree-independent
/tmp/sumfree-independent
```

These checks use explicit exceptions rather than assertions. The repair checker consumes only the rational brackets from EXACT_SLICE_RESULTS.json, disregards saved pass flags and decimal displays, checks exactly dimensions 4–200, and independently certifies fresh transition brackets, tail constants, recurrence tests, and hub tests. The finite checker reconstructs every forbidden edge including repeated summands, checks all 12 certificate files against an explicit roster, validates lower witnesses, and rejects corrupted certificates. Absence of certificates is a failure, not an empty success.

The two C++ implementations independently enumerate all upsets through dimension six. Their 64-bit representation does not support dimension seven without redesign. The Python checker proves the dimension-six upper bound through actual union witnesses and exhaustive comparable pairs. Timings and search-node counts are implementation observations, not mathematical quality comparisons.

The pre-transport package replay was performed from an isolated copied directory, with a working directory outside the package. `computation/PACKAGE_REPLAY.json` records those checks and is preserved unchanged. After the transport-only change, reconstruction and all twelve finite certificate checks were rerun in an isolated copy in normal, `-O`, and `-OO` modes; missing and corrupted parts were also tested for fail-closed behavior. The reconstructed gzip bytes match the pre-transport certificate exactly.

The final manifest covers the files actually shipped: the 47 text parts, the reconstructor, the other eleven original gzip files, and the remaining package files. It excludes itself and the reconstructed gzip, which is absent until reconstruction. The original size and hash of that reconstructed gzip are pinned above and in the reconstructor. Reconstruction adds the derived gzip locally but does not modify any manifest-covered file.

## Optional generation and construction checks

```
python computation/exact_finite_search.py 2,5
python computation/certify_finite.py 2,5,18
python computation/isolated_completion.py
python computation/boundary_completion.py
python -OO computation/search_boundary_trades.py
```

Certificate generation overwrites the named sibling certificate and may change gzip metadata; it is not needed for replay. Use a disposable copy if preserving manifest hashes. The exhaustive search script's final assertion is an optional self-check that optimization removes; it is not the independent acceptance mechanism. Candidate numerical bracket generation with `python computation/verify_slice_exact.py` additionally requires SciPy (and its NumPy dependency), overwrites EXACT_SLICE_RESULTS.json and ANALYTIC_CONSTANTS_RESULTS.json, and must be run without -O/-OO. SciPy proposes candidates only; exact rational arithmetic controls acceptance. Prefer the standard-library-only independent checker above for verification of saved data.

Exploratory floating-point MILP logs and scripts are intentionally omitted. Neither solver termination nor its objective bound is accepted as an exact upper certificate. Additional exploratory integer runs without exported upper certificates are omitted from the published finite result log.

## Operational packaging changes

The publication copy replaces workspace-relative paths with sibling paths, adds the exact 12-certificate roster guard, and points the chronological first attempt to the later proof of 706. A later transport-only step replaces the largest shipped binary with base64 parts and a verified reconstruction script. No mathematical algorithm, certificate bytes, result, or existing checker is changed by that transport step. The result log is restricted to the twelve certified instances; redundant exploratory runs are omitted. Source manuscripts, third-party copied scripts, dataset contents, private evidence and coordination files are excluded. The manifest excludes itself to avoid a circular hash definition.
