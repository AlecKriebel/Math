# Random Galois groups: five scoped approaches

Problem ID 30005647; queue row 1852. Status: **UNSOLVED**, five approaches. No novelty claim.

This package contains authored mathematical analysis, an independent audit, finite exact checks, and public-source verification metadata. It contains no source PDFs, dataset contents, extracted source text or fingerprints, or private coordination material. The source gate and audit documents record their original investigation stages; historical statements that no publication occurred refer to those stages.

For fixed n>=10 the square-event and full-A_n probabilities differ by additive O_n(H^-2), not necessarily by a relatively negligible error. Nonseparable polynomials have probability Theta_n(H^-2) for n>=3. The composition discriminant requires the sign (-1)^m. The CRT argument uses 0<c<1; the free-coefficient composition argument uses m>=2. Plugging the conjectural Malle exponent into the quoted bound does not resolve the target. None of the five routes proves the needed little-o bound.

Read FIVE_APPROACHES.md, INDEPENDENT_AUDIT.md, SOURCE_GATE.md and SOURCE_PRIORITY_AUDIT.md for proofs, scope and citations. Exact Wiley publication/acceptance dates are reported metadata, not independently replicated by the auditor. Literature checks are bounded, not exhaustive. The separate recent Odlyzko–Poonen manuscript is a posted theorem claim, not a proof audited here.

## Reproduction

Requires Python 3 and SymPy. Tested with Python 3.12.14 and SymPy 1.14.0. From this directory:

```sh
python verify_manifest.py
python -O verify_manifest.py
python verify_identities.py
python -O verify_identities.py
python test_package.py
```

The identity output must match IDENTITY_CHECKS.json byte for byte. test_package.py verifies full output in normal and optimized Python; mutates the actual square-count, parity and composition-sign mathematics; and checks strict manifest rejection of missing, changed, extra, nested-manifest, symlink, empty-directory, duplicate-record and unsafe-path cases. It does not mutate the delivered package. Tests are finite supplements, not mathematical proofs or asymptotic evidence.

PROVENANCE.json identifies accepted inputs and the assertion-to-explicit-guard transformation. Conditions and their control-flow placement were checked by reversing the transformation and comparing complete ASTs. Explicit guards remain active under -O. All files except the root MANIFEST.json are included in the closed manifest, including the verifier and tests themselves. Nested manifests are not exempt. The manifest is an integrity inventory, not a signature or proof of origin; an independent trusted manifest hash is needed to anchor it.
