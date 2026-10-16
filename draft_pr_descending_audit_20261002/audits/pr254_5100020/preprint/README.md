# Odd-period origin-pedal and antipedal area product

This kit accompanies the unrefereed note An odd-period pedal-antipedal area invariant in elliptic billiards, by Alec Kriebel, ORCID 0009-0001-9320-500X. It proves the k403,a observation of Reznik, Garcia and Koiller for the original orbit, a strict confocal elliptical caustic, primitive least odd period and every admitted coprime star. All areas are ordered signed shoelace areas; real intersections are finite. Circles are handled separately.

The written analytic proof establishes the universal theorem. Finite exact controls and high-precision diagnostics corroborate its algebra and construction domain; they are not proof-assistant formalization or interval certificates. The earlier campaign origin-pedal mechanism and classical canonical, Jacobi, cyclic-master-identity and Landen inputs are credited. Extensive bounded priority audits found no earlier covering result, without certifying worldwide firstness.

## Contents

- paper/odd_origin_area_product.tex is the standalone current source. The PDF is deposited separately.
- checks/, expected/ and CHECKSETS.json contain nine successful checksets and their complete reference receipts.
- run_verification.py verifies distributed hashes and executes programs in isolated temporary directories.
- audits/ contains authored mathematical/priority reports, derivations, source pins and root acceptance.
- proof/ORIGINAL_FROZEN_PROOF.md preserves the original proof bytes. Its historical candidate/pending-review labels refer to the 1 October packet; the current note and root acceptance govern the current result.
- provenance/ records immutable input identity and bibliographic hashes. Full third-party PDFs, archives, extracted text, images and raw web/API responses are excluded.
- MANIFEST.json hashes every distributed file except itself.

Historical audit manifests may mention original paths or excluded reading copies; they preserve provenance and are not runtime dependencies. Initially failed reviewer scripts remain in repository audit history and are excluded from executable PASS checksets. Fresh manuscript-review reports are recorded separately in the repository so adding a report cannot silently change a reviewed ZIP.

## Reproduce

Use Python 3.11 or newer, from the extracted package root:

~~~sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_verification.py
~~~

On Windows use the corresponding .venv/Scripts/python.exe. Dependencies are SymPy 1.14.0 and mpmath 1.3.0; NumPy/SciPy are not needed. The reference runtime was Python 3.14.6 on macOS. The runner checks hashes first, copies each script to its own temporary directory, and compares complete receipts ignoring only top-level generation UTC and elapsed time. It leaves this package unchanged.

Exact evidence includes named-line identities, Jacobi reductions, divisor coefficients, finite primitive lattice controls, and complete reflected strict-caustic constructions. Two distinct noncircular N3 trajectories have product 6860/81. An excluded same-caustic N4 pair has products 225/4 and 289/4, falsifying an all-parity extension. Diagnostics include Cartesian reflection, tangency, closing stars, reversal/repetition, extreme interior moduli, large odd periods and near-complex-pole phases. They do not replace the all-period proof.

Compile the standalone source with a modern LaTeX engine such as Tectonic if a PDF rebuild is desired; this is independent of the checksets.

AI tools were used extensively in derivation, verification, literature research, coding, writing and internal adversarial review. This is unrefereed, without external human peer review or formal proof-assistant verification.
