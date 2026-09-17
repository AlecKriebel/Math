# Equal-sum–product matrices: general nonexistence

**Result:** No globally distinct positive-integer matrix with three or more
rows can have every row sum and every column product equal to one common
number. The proof covers all allowed dimensions and all common values; it
is not a finite-search conclusion.

The source's two-row construction is valid. The equal-value conjecture is
therefore true under the stated positive-integer, global-distinctness, and
at-least-two-column conventions.

## Read the proof

`notes/equal_sum_product_note.pdf` is the self-contained mathematical note.
Its editable source is `notes/equal_sum_product_note.tex`. A plain-text
mathematical checkpoint is `notes/proof_checkpoint.md`.

The key chain selects any three rows and writes their entries as x_j,y_j,z_j:

    3 = sum_j (x_j+y_j+z_j)/N
      <= sum_j (1/(x_j*y_j) + 1/(x_j*z_j) + 1/(y_j*z_j))
      <= sum_j (1/x_j^2 + 1/y_j^2 + 1/z_j^2)
      < 2.

The first bound holds for any total number of rows, since all omitted
integer factors in each column are at least 1. The second is an exact
sum-of-squares inequality. The third uses global distinctness and the finite
telescoping bound sum_{k=1}^M 1/k^2 <= 2-1/M < 2.

## Reproduce all executed checks

Python 3.10 or newer; no third-party packages, network, solver, or paid service.
Executed here with Python 3.13.5 on Linux x86_64.

```sh
python3 src/reproduce.py
```

This runs 33 checker tests, an exact symbolic identity comparison, all
64,000 ordered positive-integer triples through 40, all 4,095 nonempty
subsets of {1,...,12}, 512 telescoping checks, 360 higher-row array tests,
and a 101-digit rational probe. Exact scopes and logs are included.

The checker is deliberately independent of the proof audit and does not
reject inputs merely by invoking the theorem. It recomputes every required
condition from the entries with arbitrary-precision integers. To test the
source's two-row control:

```sh
python3 src/verify_matrix.py certificates/source_two_rows.json --min-rows 2
```

To check a proposed target matrix, omit the two-row override:

```sh
python3 src/verify_matrix.py path/to/candidate.json
```

Input is either a JSON array of rows or an object with `matrix` and an
optional positive integer `N`. The checker exits with status 0 for valid,
1 for a rejected matrix, and 2 for malformed input or a command/input error.
It accepts `-` instead of a filename to read standard input. Integers must
be JSON integers; bools, floats, and numeric strings are rejected.

## Files and integrity

- `notes/`: proof, stronger ordinary-SP bound, controls, and research log.
- `src/`: independent matrix checker, exact audit, one-command reproducer.
- `tests/`: executed checker regression suite.
- `certificates/`: source matrix, negative controls, symbolic certificate.
- `references/`: primary sources and the exact later-result queries.
- `logs/`: inspected outputs, command return codes, environment, PDF build log.
- `progress.json`: completion status and exact reproduction command.
- `SHA256SUMS`: SHA-256 integrity manifest for the delivered files.

On macOS, validate the archive's initial file contents before rerunning tests:

```sh
shasum -a 256 -c SHA256SUMS
```

Rerunning tests refreshes files in `logs/`, so their hashes may then change.
No font files are included. The PDF can be rebuilt with a LaTeX installation:

```sh
cd notes
pdflatex -interaction=nonstopmode -halt-on-error equal_sum_product_note.tex
pdflatex -interaction=nonstopmode -halt-on-error equal_sum_product_note.tex
```

## Completion and provenance

No mathematical case remains unresolved. No factorization or matrix search
was needed. The tests are diagnostics; the written argument proves the
unrestricted theorem. No proof-assistant or external-review claim is made.
Targeted web queries did not locate a later resolution, but historical
priority is not exhaustively established. The public source still displayed
the statement as a conjecture when inspected on 14 September 2026.

No contact, publication, spending, or asynchronous work was undertaken.
