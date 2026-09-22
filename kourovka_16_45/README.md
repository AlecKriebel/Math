# Kourovka Notebook 16.45: a counterexample

## Result

For the explicitly specified group

    G = F_29^2 semidirect H,
    H = < [[0,28],[1,0]], [[2,7],[12,28]] > <= SL(2,29),

with the natural column-vector action, the manuscript proves

    |G| = 100920,
    b_f(G) = b(G) = 3 < 4 = mu'(G).

Here b(G) is the maximum size of an **inclusion-minimal** base over **all**
permutation representations, including nonfaithful and intransitive ones.
Bases are for the permutation image. The auxiliary b_f restricts only this
maximum to faithful actions. The invariant mu' allows independent subsets
that need not generate the entire group. All three invariants of the trivial
group are zero.

This is a negative answer under the user's conventions and Cameron's original
all-representations conventions. It is not a minimum-order claim.

## Read first

- `proof.pdf`: eight-page mathematical proof, including the all-actions bound.
- `proof.tex`: editable LaTeX source.
- `data/group_spec.json`: portable group, multiplication, and witness specification.
- `progress.json`: exact checkpoint and next verification action.
- `references/source_audit.md`: source and notation audit, with priority limitations.
- `research_log.md`: discovery steps, adversarial tests, and actual verification.

The crucial upper bound is **structural**. Every subgroup K not containing
V = F_29^2 has b_f(K) <= 2. Restricting a faithful irredundant intersection
family to such a K gives b_f(G) <= 3. Every nontrivial normal subgroup of G
contains V, so every nonfaithful action factors through H; b(H) = 3. This
covers all actions without enumerating the subgroup lattice of G.

## Reproduce the exact certificates

Requirements: Python 3.10 or later (standard library only), and optionally a
C++17 compiler. No GAP, Sage, numerical optimizer, network access, or group
catalogue is required for the final verification. On macOS, `c++` may be
used instead of `g++`.

From this directory:

```sh
mkdir -p build/certified
python3 src/verify_counterexample.py --outdir build/certified

g++ -O2 -std=c++17 -Wall -Wextra -pedantic \
    src/verify_counterexample.cpp -o build/verify_counterexample_cpp
./build/verify_counterexample_cpp build/certified/subgroups_cpp.txt

python3 src/compare_certificates.py \
    build/certified/finite_certificate.json \
    build/certified/subgroups_cpp.txt
```

All three commands that perform verification should report PASS. Python uses
explicit checks, not statements that disappear under `python -O`. The saved
logs are in `logs/verification_python.log`, `logs/verification_cpp.log`, and
`logs/cross_verification.log`. The final C++ build completed without warnings.
The earlier formatting warnings, subsequently corrected, are retained in
`logs/cpp_compile_initial_warnings.log`.

Each final verifier reconstructs H from matrices, separately enumerates all
76 **actual subgroups**, and checks all 1,215,450 four-member families of
proper subgroups and all 67,525 three-member families. The comparison script
compares sets of actual matrices, not subgroup sizes, conjugacy classes, or
implementation-specific indices. Closure under adjoining all outside elements
proves subgroup-enumeration coverage.

The verifiers also generate the 100,920 affine elements, certify the explicit
independent 4-set, and check a faithful minimal 3-base family. The Python
verifier additionally certifies the quotient map H -> A5, the normal cores
of the four omission subgroups, and the characteristic-11 adversarial example.
The C++ verifier checks its SL(2,5) isomorphism on every pair of elements.
Both use exact integer arithmetic but were written in the same research
session; this is not a claim of independent external peer review.

## Certificate layout

`data/certified/finite_certificate.json` contains the 120 matrices, all 76
subgroups (element indices and generating indices), the 30 line stabilizers,
the explicit SL(2,5) isomorphism, the map onto A5, and the faithful-base data.
Indices in that file are zero-based and refer to its `matrices` array.
Matrices are row-major `[a,b,c,d]`. Affine elements are `[x,y,a,b,c,d]`.
All entries are residues in 0,...,28 unless a field of order 5 or 11 is
explicitly named. `subgroups_cpp.txt` instead encodes a matrix by
`((a*29+b)*29+c)*29+d`; its first line is the number of subgroups.

`verification_python.json` gives the concrete checks and witnesses. Its
runtime field will vary between runs. The sorted affine-element list has
SHA-256

    2f4c3b8353a9a5cd7d2cbbeb8a0d48dd0e203f4371652fd25c5ca2936fff5efc

using the canonical compact JSON encoding implemented in the verifier.

## Discovery material, not proof premises

The other files in `data/` preserve the small-group exploratory tables,
subgroup lattices, and optimization outputs. `src/groups.py`,
`src/enumerate_subgroups.cpp`, `src/lattice_opt.py`, `src/run_examples.py`, and
`src/discover_affine.py` preserve the discovery code. That exploratory path
uses NumPy and SciPy MILP; it is unnecessary for the final proof or verifiers.
Floating-point optimization results are not used as certified upper bounds.
No arbitrary catalogue or order cutoff supports the final theorem.

To rerun the exploratory examples, install NumPy and SciPy, compile
`src/enumerate_subgroups.cpp` to `src/enumerate_subgroups`, then run
`python3 src/run_examples.py` followed by the selected case names, such as
`Q8 SL2_5 A5`. The code has some unrun optional case names; the presence of a
name in the script is not evidence that it was tested. The research log
lists the cases actually run.

## Manuscript and integrity

The PDF was compiled successfully with `pdflatex` twice and all eight rendered
pages were visually inspected. To rebuild:

```sh
pdflatex -interaction=nonstopmode -halt-on-error proof.tex
pdflatex -interaction=nonstopmode -halt-on-error proof.tex
```

`SHA256SUMS` records the bundle files at delivery. Check it before running
commands that overwrite saved output, using `sha256sum -c SHA256SUMS` on Linux
or `shasum -a 256 -c SHA256SUMS` on macOS. The reproduction commands above
write to `build/`, leaving the delivered certificates unchanged.

## Limits of the certification

The mathematical argument and explicit witnesses are complete for the stated
counterexample. No Lean formalization was compiled; no proof assistant, human
referee, or external researcher has certified it in this session. No contact,
submission, publication, purchase, or modification of any external resource
was performed. The source audit found the question still listed in the
September 2026 notebook and found no earlier resolution in a focused search;
this does not guarantee bibliographic priority.
