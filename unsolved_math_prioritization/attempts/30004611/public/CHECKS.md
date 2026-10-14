# Reproducing the bounded checks

These authored Python programs repeat the finite controls already described in the mathematical audits. They do not perform a new search or establish statements beyond their listed test cases. Their source programs are not downloaded third-party code.

## Safe execution

Run from the reader's root directory with Python 3. Each reader program writes its complete result as JSON to stdout and writes no result files. For example:

    python checks/tangency.py
    python -O checks/tangency.py
    python -OO checks/tangency.py

To save output, choose a **new directory**, rather than redirecting into the included frozen results. For example:

    mkdir my_new_check_run
    python checks/tangency.py > my_new_check_run/tangency.json

The `mkdir` must succeed; do not proceed with an existing directory. The program predicates remain active under both `-O` and `-OO`: optimization-removable assertions have been replaced by explicit `if not ...: raise RuntimeError(...)` checks, preserving their predicates and lazy diagnostics.

The graded-rigidity, ungraded, and transport checkers require SymPy. Other included checkers use only the standard library. The recorded replay environment and comparisons are in [REPLAY.json](REPLAY.json). No automatic package installation is part of these scripts.

## Included checks

- `checks/tangency.py`: 55 example/field/degree controls, degrees 0–4, for ordinary and Ziegler maps, correction kernels/Tor, and repeated-row distinctions. Expected aggregate: `results/tangency.json`.
- `checks/product_cochains.py`: 20 full stalk/cochain controls for the four-plane factor and its rank-four product; degrees 0–3 over F₂ and 0–1 over F₃, F₅, F₇. Expected aggregate: `results/product_cochains.json`.
- `checks/minimal_cover.py`: eight independent degree-zero minimal-open-cover controls over Q, F₂, F₃, F₅. Expected aggregate: `results/minimal_cover.json`.
- `checks/prism_signs.py`: 546 formal strict-chain prism identities with integer coefficients. Expected aggregate: `results/prism_signs.json`.
- `checks/graded_rigidity_author.py`: exact Gröbner/Hilbert identities and 21 degree/field controls, degrees 0–6 over F₃, F₅, F₇. Expected aggregate: `results/graded_rigidity_author.json`.
- `checks/graded_rigidity_audit.py`: independent Smith-form, Gröbner, Hilbert-series, and endomorphism controls. Expected aggregate: `results/graded_rigidity_audit.json`.
- `checks/transports_author.py`: exact rational flat-incidence, local-rank, and cochain controls for the marked-hyperplane and open-transport examples. Expected aggregate: `results/transports_author.json`.
- `checks/transports_audit.py`: independently implemented exact rational incidence and cochain controls for those examples. Expected aggregate: `results/transports_audit.json`.

- `checks/ungraded_local_author.py`: exact tangent-generator, presentation, stalk-epimorphism, and Ext-length controls over Q, F₃, F₅, F₇, F₁₁. Expected aggregate: `results/ungraded_local_author.json`.
- `checks/ungraded_audit.py`: independent exact polynomial checks of ungraded map and module arguments, including the ordinary nonunit-matrix counterexample to an invalid shortcut. Expected aggregate: `results/ungraded_audit.json`.

The original pass-1 audit also records matrix-rank controls; no separate executable for those historical controls was present in the accepted files. The later checks cover the same credited arrangements but are not represented as exact replays of a missing pass-1 program.

The preserved results are authored verification outputs, not source datasets. Output objects may be compared after JSON parsing; whitespace differences alone do not change a result.

## What changed from the accepted program versions

[EDITIONS.json](EDITIONS.json) records original program sizes/hashes, exact reader-output hashes, replaced assertion locations, and output-only changes. Full unified code diffs are in `code_changes/`. The calculation expressions, loops, fields, degrees, and expected predicates were not changed. AST reserialization changes formatting and removes ordinary comments; two docstrings replace a researcher-role label with “author”; this is recorded separately and changes no calculation.

Programs that formerly wrote beside themselves now print the same full JSON aggregate. Redundant progress/summary printing was removed only when needed to produce one JSON object. These executable editorial changes received [independent packaging review](PACKAGING_ACCEPTANCE.md); the earlier mathematical audit alone did not certify the changed program bytes.

The mathematical proofs remain the authority for all-field/all-degree assertions. Successful normal, `-O`, and `-OO` replays verify agreement on the **same bounded controls**, not unrestricted correctness.
