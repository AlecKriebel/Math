# Outer-pedal area centroid: reproducibility package

Alec Kriebel, version 1.0, 13 October 2026.
ORCID: https://orcid.org/0009-0001-9320-500X
Problem 5100017 / AMR-050-0017, invariant k307.

The standalone research note gives the proof, explicit centroid, and exact
zero-area domain. The claim assumes a noncircular ellipse, a strict confocal
elliptic caustic, and least even period; primitive stars use signed moments.
It does not concern unsigned region centroids or the arithmetic vertex mean.

AI tools were used extensively throughout. This is unrefereed and has not
received external human peer review or proof-assistant formalization.
Bounded primary-source audits found no earlier covering proof; they do not
certify historical firstness. Original observation: Reznik--Garcia--Koiller,
doi:10.1007/s40598-021-00174-y, Table 4, k307.

## Run the checkable evidence

Use Python 3.12 or newer and a disposable environment:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_verification.py
~~~

The default run checks the integrity manifest, the exact independent rational
controls (4355 assertions), the real Cartesian symbolic coefficient certificate,
and exact winding. Each program runs in a fresh temporary working directory
with a copied script, so its outputs do not alter the evidence files. New output
and process receipts are saved under replay-output/.

For the longer, independently generated numerical controls:

~~~sh
.venv/bin/python run_verification.py --full
~~~

This additionally runs the author controls, the original independent 85-digit
controls, the new Laurent algebra and 90-digit tangent-generated controls,
and the new 110-digit physical-reflection controls. It can take several
minutes. Numerical reports contain environment details and timestamps, so
byte identity is not expected. Published tolerances, exact assertions and
scope are the checks; floating maxima can vary by platform.

The proof itself, including the four-period converse, is in proof/PROOF.md.
The paper source is standalone LaTeX in paper/outer_pedal_centroid.tex, with
inline bibliography. It compiles with Tectonic 0.16.9 or a modern LaTeX
installation. The accompanying PDF is supplied separately in the deposit.

## Evidence and limitations

The algebraic and geometric audit folders contain independent derivations,
checkers and their original successful outputs. The Laurent checker evaluates
the exact unrestricted symbolic-M star polynomials and the complete edge
coboundaries; the real-coordinate checker supplies separate endpoint
potentials. The winding certificate checks the exact eight-period star.

Initial double-precision generator failures were repaired using high precision.
DOUBLE_PRECISION_FAILURE_HISTORY.md explains that the original full failing
scripts were not retained; its minimal failure reproducer is reconstructed,
not an authenticated original. Geometric audit reports also explain the
spurious four-period zero circle caused by floating sign noise. No surviving
mathematical counterexample was found under the stated hypotheses.

Root reproduction reports and independent audit reports describe the prior
checkpoints, some before manuscript preparation. Their earlier pending-stage
statements are historical, not current publication clearance. Primary-source
manifests identify the literature read; private copyrighted PDFs and bulk
search receipts are intentionally excluded from this archive.

MANIFEST.json lists the authored package files and SHA-256 hashes. It provides
integrity checking, not mathematical proof. CC BY 4.0 terms are in LICENSE.
