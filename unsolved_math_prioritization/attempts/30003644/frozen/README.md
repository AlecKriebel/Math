# Zero-free Dirichlet polynomial on Re(s)=1

Problem 30003644 / OWR-15956-010. Research disposition: **unsolved, 5/5**.
The exact target is `D(1+it) != 0` for every real `t`, where
`D(s) = 1 + 2^(-s) + 3^(-s) + 5^(-s)`.

Start with `PROOF.md`. It separates five substantive approaches and their
remaining gaps. Full nonvanishing is proved only conditionally on Schanuel's
conjecture. The unconditional conclusions are partial and include a
transcendence obstruction, the impossibility of a positive uniform gap on
the line, and the classical sharp boundary for the real parts of zeros.
This is an AI-assisted, unrefereed research note; it makes no novelty claim.

## Replay

Requires Python 3.12 and mpmath 1.3.0. No network, source PDFs, or source
corpus is needed to run the checks.

```sh
python verify_controls.py > replay.json
cmp replay.json control_results.json
sha256sum -c SHA256SUMS
```

The script uses exact `fractions.Fraction` arithmetic for the algebraic
torus witness and `mpmath.iv` at 35 decimal digits for directed interval
enclosures. It verifies:

1. Unit norms, exact cancellation, and rejection of three sign mutants
2. The real rightmost-zero-boundary bracket `(1.032, 1.033)`
3. A derivative lower bound at hypothetical line zeros
4. A Rouché disk containing a zero strictly to the right of the line
5. Nonvanishing on the entire finite interval `|t| <= 10000`
6. Failure to certify an interval that actually contains a zero of a
   deliberately modified polynomial

The finite-height test is not sampling: a leaf is accepted only if an
interval enclosure of the real or imaginary component excludes zero.
Every subdivided parent is the union of its two closed children. The input
endpoints and midpoints are exact binary rationals: heights are at most
10000 and subdivision depth is at most 30, well inside the 53-bit mantissa
range for the integer numerators in this particular dyadic tree. Any
unresolved leaf is an explicit failure. The accepted-leaf endpoint digest
binds the traversal, while the verifier reconstructs the enclosures.

These are computer-assisted interval certificates, dependent on mpmath's
outward-rounding elementary-function implementation; they are not a
machine-checked formal proof. Its `libmpi` implementation uses downward and
upward rounded endpoint logarithms, includes trigonometric extrema inside
intervals, and outward-rounds the resulting trigonometric bounds. A fresh
independent audit should check this dependency as well as rerun the script.
No finite-height result is extrapolated to unbounded height.

## Files

- `PROOF.md`: complete deductions and five exact gaps
- `SOURCES.md`: primary-source locations and bounded literature check
- `RESEARCH_LOG.md`: dated checkpoints, approach accounting, corrections
- `RESULT.json`: machine-readable scope and disposition
- `verify_controls.py`, `control_results.json`: executable controls and output
- `SHA256SUMS`: hashes of the seven authored artifacts above

Only authored text, code, and small computed outputs belong to this packet.
No third-party PDFs, OCR, full-text copies, imported datasets, account
information, or private coordination records are included.
