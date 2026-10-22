# The odd-period focal-pedal sum invariant

Alec Kriebel, ORCID 0009-0001-9320-500X. Attributed research note, version 1.0, 16 October 2026.

The paper verifies the k601 observation of Reznik–Garcia–Koiller for proper nested confocal ellipses and odd primitive physical period, including all admitted coprime star windings and either orientation. It concerns ordinary Euclidean distances from the foci to the COMPLETE original side supporting lines. Repeating an odd primitive orbit r times scales the product by r². It is not a theorem for every even primitive period, clipped segment distances, hyperbolic or collapsed caustics.

The full all-odd analytical lemma is a direct corollary of Khare–Sukhatme's classical generalized Landen formulas. The Fourier derivation in the paper makes the common argument, transformed parameter and unequal amplitudes checkable. Earlier focal support geometry, canonical billiard coordinates, original observation, cyclic identities and meromorphic methods are credited. No theorem/formula/method novelty, firstness, present-day openness, independent discovery or simultaneity is claimed. The bounded audit did not establish an earlier explicit full geometric k601 application and does not exclude one elsewhere.

The exact parity boundary uses one proper pair with primitive four-period products 8 and 9. The circle is treated separately by I=N²beta². The universal conclusion rests on the written proof.

## Reproduce the calibration

Use Python 3.10+ and the sole dependency mpmath 1.3.0 (verification/requirements.txt). From verification/ run:

    python3 -B verify.py > my_results_normal.json
    python3 -B -O verify.py > my_results_optimized.json

Both commands must exit zero and report PASS: 8 proper confocal configurations, 70 positive calibration traversals and 25 required rejection controls each. The default has 60 requested digits, 100 working digits, and an explicit 1e-40 residual tolerance. These are finite noninterval diagnostics, not certified error bounds or a universal computational proof. The included actual results used Python 3.14.6. No repository or private path is required by the portable verifier.

## Contents and historical evidence

The paper's LaTeX source is included. verification/ contains the current portable code, dependency declaration, usage and actual ordinary/optimized results. materials/ contains authored proofs, adversarial reports, bounded priority/source ledgers and all 17 immutable original submission files for auditability. No third-party full papers, page images, dependencies, credentials or operational tree caches are included.

The original submission scripts in materials/original_submitted_head are HISTORICAL EVIDENCE ONLY. Their favorable reports do not certify the final package. The old scripts use bare asserts that disappear under Python -O; the old candidate also permits a NaN to be masked inside max(). These vulnerabilities were reproduced and documented in the analytic audit. Use verification/verify.py, whose explicit real-finite exceptions and required rejection controls remain active under -O. The archived original bytes are preserved intentionally; they are not the current recommended verification program. Earlier audit code paths and reports describe their historical local environments.

The current attributed package was assembled after fresh mathematical/source/priority audits. Earlier mathematical, priority and operational audits are distinct from the later fresh whole-package reviews. Package review outcomes are recorded separately before publication; the archive does not claim human peer review or formal proof certification.

AI systems were used extensively for proof development, source comparison, software, drafting, computation and adversarial review. Unrefereed preprint; no conventional human peer review or proof-assistant formalization. The author remains responsible for the claims.

New authored materials are CC BY 4.0. Referenced external works retain their own rights.
