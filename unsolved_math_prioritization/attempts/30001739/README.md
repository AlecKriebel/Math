# Unitary multiplicity: scoped five-segment counterexample

Status: **ACCEPTED_COMPLETE_COUNTEREXAMPLE** in the characteristic-zero p-adic smooth admissible complex model. This records AI-assisted independent mathematical audit acceptance, not conventional human peer review or journal acceptance. No historical priority or all-local-fields claim is made.

## Read the mathematics

- `current/PROOF.md`: complete corrected argument and exact published-theorem interfaces.
- `current/FULL_AUDIT.md`: complete independent adversarial audit, including noninducedness.
- `current/ANALYTIC_AUDIT.md`: separate independent audit of complete-Hom bases and analytic transport/specialization.
- `current/HALL_CERTIFICATES.md` and `.json`: all 15 exact noninduction certificates.
- `current/MODEL.json`: target category and interpretation.
- `ACCEPTANCE.md`, `ACCEPTANCE.json`, `STATUS.json`: exact accepted disposition and limits.
- `historical/PUBLIC_SOURCE_METADATA.json`: public citations, PDF hashes/sizes and source-inspection coverage; no source bodies.
- `historical/PRIORITY_REPORT.md`: bounded 50-query comparison, priority unestablished and Luo–Zha full-text comparison unresolved. The dated kernel-result announcement is May 13, 2025.

For F=Q_3 and its unramified quadratic extension E, the Langlands quotient of the GL_15(E) standard module with ordered segments [4,6], [2,5], [3,3], [1,4], [0,2] is tau-invariant and not itself an entire proper parabolic induction. For k=1 it has multiplicity zero for each Hermitian isometry class, giving total 0 instead of the proposed 2. The proof uses complete period bases, two invertible nested transports, five necessary linked-pair constraints forming an odd cycle, and the 15 Hall obstructions.

## Trust and replay

First authenticate the SHA-256 of `BOOTSTRAP.py` from an external reviewed source such as the reviewed PR body. Do not learn its trusted hash from the packet being checked. Copy that exact bootstrap outside the packet. It pins the complete manifest bytes, verifier and control harness. The manifest pins every other delivered file; it excludes itself and the bootstrap to avoid circularity. Final external replay receipts remain outside the delivery for the same reason.

This tested runtime uses Python 3.12, SymPy 1.14.0 and mpmath 1.3.0, already installed in the interpreter's trusted site-packages directory. The adapter adds only the explicit interpreter-prefix site-packages path and verifies module origins and versions. Site startup hooks are not run. Package code is not bundled. Dependency installation and integrity are part of the trusted runtime, not certified by these source-free receipts.

Run as genuine UID/EUID 1000, with packet files mode 0444 and every packet directory mode 0555. For each mode (ordinary, -O, -OO), run the externally authenticated bootstrap with `python -I -S -B [mode] EXTERNAL_BOOTSTRAP.py --controls PACKET`. Every case compares complete stdout and stderr bytes and recursively exact JSON identities, counts, types and failure reasons. There is no normalization, PASS-only acceptance, optional skipping, or success credited for expected-failure labels.

Four fresh positive checkers and six actual finite mathematical source mutants run per mode. Publication-integrity mutations, strict-schema controls, and direct output-comparator controls are reported separately. Read-only probes actually attempt writes as UID1000 and require errno13. Hostile-import runs must match the entire baseline output; before/after hashes cover the whole delivery. Repetition in integrity tests does not add mathematical coverage.

The code checks finite endpoint conditions, exact rational scalar functions, parity, and Hall obstructions. It does not compute invariant-functional spaces. Analytic vanishing uses the written proof and the published FLO, JPSS, and LM dependencies. Copied source PDFs/text, datasets, private coordination, excluded private-file identities, the superseded full provisional proof, and queue edits are absent. Original inputs remain unchanged.

The adapter records the exact captured inner stdout and stderr as verbatim UTF-8 JSON strings, with byte counts and SHA-256 values, beside the strictly interpreted result. Duplicate keys, nonfinite values, overflow, malformed JSON and trailing content are rejected. The verifier checks the entire raw adapter output and both inner streams against fixed references. Targeted controls reject whitespace-only changes and duplicate-key JSON that an ordinary decoder would map to the same object; these remain publication controls, not mathematical mutants.
