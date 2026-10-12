# Finite verification supplement

For Alec Kriebel, *Missing faces and topological embeddings of sphere skeleta*.
Version 1.0, 12 October 2026. The note is unrefereed and its AI-assisted
reviews are preserved as bounded audit evidence.

The accompanying manuscript proves the mathematical statement. The programs
in this supplement check specified finite examples and chain calculations;
they are not a formal proof verifier and do not establish the universal
theorem, generic algebraic conclusions, topological sphere recognition,
contractibility, exotic PL structure, or priority.

Use Python 3.10 or newer, with its standard library only. From this folder run:

    python3 reproduce.py

The driver verifies the current program and expected-output SHA256 hashes,
runs all three programs in normal and optimized modes, and requires every
output to match its recorded bytes. It prints a JSON receipt. The driver and
current checkers use explicit runtime checks that remain active under `-O`.
Checks can also be run separately, for example:

    python3 checks/check_exact.py
    python3 checks/check_independent.py
    python3 checks/check_bitmask_controls.py

The first two are hardened derivatives of the frozen author and prior audit
programs. The third was independently formulated with bitmask faces, dense
modular ranks, rational affine circuits, and a separately seeded bistellar
sequence. Random choices are seeded. Seeded choices use Python's floating-point
selection routine; byte reproducibility across every future Python version
or platform is not claimed. The recorded runtime appears in the receipt.

`CONTROL_MANIFEST.json` records each current program and expected output.
`patches/` records the replacement of removable assertions in the original
programs and the current author output’s reference to the accompanying
manuscript. Numerical results are unchanged; the historical stdout is preserved. `audit_evidence/reproduction/INDEPENDENT_VERDICT.md` describes the
scope and the actual fault tests. The intentionally incorrect mutation
programs are excluded. The fault-test logs in that folder are evidence about
negative controls, not additional successful mathematical computations.

The author controls check four stellar examples, quotient dimensions at
particular finite primes, four Flores cycles, and a flag-subdivision example.
The first audit controls check 100 bistellar moves, 3,542 complement homology
calculations, 824 persistent missing triangles, 28 middle-move identities,
and 70 new-face witnesses. The independent bitmask controls additionally
check 24 quotient ranks over three primes and a different 100-move sequence,
with 3,548 complement calculations, 580 persistent missing triangles,
30 middle-move identities, and 52 new-face witnesses. These counts describe
finite test coverage, not a quantitative probability that the theorem is true.

`historical/` preserves all 15 original files from reviewed PR head
`8527ccdba064bca52035fc6c8d96caa750ac9c00`. Their original manifests remain
unchanged. These are historical inputs: their checker assertions disappear
under optimized Python and some prose preserves the earlier pending-review
status. Use `checks/` for current computations and the accompanying manuscript
for the current proof and its clarifications. Historical audit references to
`hardened/` correspond to the present `checks/` and `patches/` folders.

The mathematical reviews in `audit_evidence/` cover separate algebraic and
topological dependencies. They are AI-assisted reviews, with early independent
assessments, and are neither independent human peer review nor formal
certification. Source publications are cited rather than redistributed.
The paper and package are unrefereed. AI tools were used extensively in
solving, drafting, checking, and preparing these materials.

License: CC BY 4.0; see `LICENSE.txt`.
