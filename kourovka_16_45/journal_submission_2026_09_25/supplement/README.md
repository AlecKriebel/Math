# Exact verification supplement

**A counterexample to Kourovka Notebook Problem 16.45 — Alec Kriebel**

These exact programs corroborate the finite inputs and explicit witnesses in
the paper. The paper proves the upper bounds for all permutation actions
structurally; they do not depend on enumerating all subgroups of the affine
group or on the reader running software. See `verification_note.pdf` (source:
`verification_note.tex`) for the mathematical scope and a characteristic-11
boundary case.

## Requirements and one-command verification

Use Python 3 (version 3.9 or later), a C++17 compiler, and Make. Python uses
only its standard library. No group catalogue, optimizer, saved multiplication
table, network access, or third-party Python package is required.

From this directory run:

```sh
make verify
```

All generated files go in `build/`. Files in `expected/` are never modified.
Every verifier exits unsuccessfully if a required check fails. The comparison
stage prints `PASS` only when the fresh mathematical results and complete
subgroup sets agree with the bundled expected outputs. The Python summary's
`seconds` field is elapsed-time metadata and is excluded from comparison.

The independent checker reads no input certificate. Its optional
`--subgroups-output PATH` argument names only an output file, so it works after
extracting the supplement anywhere. All verification sources are included.

## Commands without Make

Run the following from this directory in an ordinary shell:

```sh
mkdir -p build
python3 src/verify_counterexample.py --outdir build > build/verification_python.log
c++ -O2 -std=c++17 -Wall -Wextra -pedantic src/verify_counterexample.cpp -o build/verify_counterexample_cpp
./build/verify_counterexample_cpp build/subgroups_cpp.txt > build/verification_cpp.log
python3 src/compare_certificates.py build/finite_certificate.json build/subgroups_cpp.txt
python3 independent_exact.py --subgroups-output build/independent_subgroups.json > build/independent_exact.json
python3 src/compare_results.py
```

If only Python is available, create `build/` and run the two checker commands
(`src/verify_counterexample.py` and `independent_exact.py`) independently.
The full comparison command also requires the C++
export. On systems where the Python command is `python` instead of `python3`,
substitute that name, or run `make verify PYTHON=python`.

## Exact expected results

| Quantity | Expected value |
|---|---:|
| Complement order | 120 |
| Actual complement subgroups | 76 |
| Proper-subgroup four-families tested | 1215450 |
| Irredundant four-families | 0 |
| Proper-subgroup three-families tested | 67525 |
| Faithful minimal three-families | 0 |
| Independent complement triple omission orders | 8, 12, 20 |
| Lines over the field of order 29 | 30; each stabilizer cyclic of order 4 |
| Affine group order | 100920 |
| Independent affine four-set omission orders | 120, 6728, 10092, 16820 |
| Four omission subgroups' total intersection | Order 2, not normal |
| Faithful three-family subgroup orders | 58, 58, 58 |
| Faithful three-family pair-intersection orders | 2, 2, 2 |
| Faithful three-family total intersection | Order 1 |
| Corresponding coset action degree | 5220 |
| Characteristic-11 four-family subgroup orders | 110, 110, 242, 605 |
| Characteristic-11 deletion-intersection orders | 11, 11, 5, 2 |
| Characteristic-11 total intersection | Order 1 |

The additional independent checker tests all 14400 products for the specified
isomorphism with `SL₂(5)` and quotient onto `A₅`, verifies all displayed affine intersections
element-for-element, and enumerates all 62 subgroups of the scalar group
`F₂₉ ⋊ C₄`: there are no irredundant triples. Across the implementations the
subgroups are compared as sets of actual matrices, not by their orders or
labels. A digest comparison additionally verifies agreement on all 100920
sorted affine elements. The upper bounds for all permutation actions remain
the mathematical proof in the paper.

## Files

- `src/verify_counterexample.py`: first standalone exact checker.
- `src/verify_counterexample.cpp`: separate C++17 implementation.
- `src/compare_certificates.py`: exact subgroup-set comparison for those two.
- `independent_exact.py`: additional checker independently reconstructed from
  the displayed manuscript inputs before the supplied implementations were read.
- `src/compare_results.py`: comparison with fresh and expected certificates.
- `expected/`: fresh verified outputs supplied for comparison; not inputs to
  the reconstruction algorithms.
- `verification_note.tex` and `verification_note.pdf`: mathematical explanation
  of coverage, the explicit isomorphism, and the boundary case.
- `LICENSES.md`: existing rights position; no new reuse license is granted.

The programs were prepared and checked with AI assistance. Separate
implementations do not constitute external human peer review or formal
verification. No compiled executable, exploratory optimization result, review
history, or third-party paper is part of this supplement.
