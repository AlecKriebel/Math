# Reproduce the candidate package

Python 3.10+ standard library is sufficient for all algebraic certificates. Run from this directory:

    python3 exact_kernel_certificate.py
    python3 rational_selection_certificate.py
    python3 verify_pair_identity.py

The first checks denominator-cleared universal polynomial identities and supplementary 292 exact rational inputs. The second checks exact selected-range rational inequalities. The third independently checks signed-pair polynomials. These are algebraic certificates, not PDE existence proofs. Read the manuscript and SUPPLEMENT files for the analytic proof and its dependencies.

Compile standalone main.tex with Tectonic 0.17.0 (or a compatible TeX engine with amsmath/amsthm/mathtools/mathrsfs/lmodern/hyperref). The reference bibliography is embedded in main.tex; references.bib records attribution but is not needed by the standalone build.

    tectonic -X compile --untrusted main.tex

The desktop editor's built-in compiler was used for authoring diagnostics. The same bundled Tectonic executable was invoked separately to produce an actual PDF file for inspection and eventual upload. PDF text/metadata and all page renders are checked separately. A clean temporary-directory build and all certificates must pass before publication.

Upstream proof input: https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a, family 362. PINNED_SOURCE.json lists exact source SHA256 hashes. Obtain sources from that public repository; third-party source/PDF copies are not included. No later source correction was observed in the intake remote check. Formalization scope is unit-mass positive-unit-charge one species only. Formal-scope audit and version receipt expressly record the failed build; no formal certification is claimed.

A full Lean reproduction requires Lean 4.34.1 and the Mathlib/package pins in the formal scope receipt, adequate disk, and the upstream repository instructions. We did not reproduce the final Main or comparator check and do not rely on that as validation.

All executed checks and final file SHA256 values are recorded with reviewed-version receipts. Computational outputs do not establish priority or eliminate mathematical assumptions.
