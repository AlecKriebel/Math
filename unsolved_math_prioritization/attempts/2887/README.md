# Kirby Problem 4.11: corrected five-turn partial attempt

**UNSOLVED, 5/5. Neither existence question is resolved. No novelty claim.**

The controlling mathematical narrative is [corrected_release/FULL_PROOF.md](corrected_release/FULL_PROOF.md). The [independent audit](audit/AUDIT.md) accepts ONLY this corrected, scoped partial account. It does not give the original narrative an unqualified mathematical PASS.

Four corrections restore compactness assumptions to the Akbulut–Yasui and Kasprowski–Powell–Ray inputs while explicitly retaining the original problem's broad domain. No noncompact extension or exclusion of noncompact examples has been proved. These are corrections within verification, not a sixth solution attempt.

## Provenance layout

- corrected_release/: controlling narrative, corrected metadata and its own manifest
- submission/: byte-identical historical author freeze, retained solely as superseded audit input; its two missing compactness invocations must not be used uncorrected
- audit/: complete safe independent audit, exact four substitutions, corrected narrative, original diff, symbolic controls and audit manifest, all preserved byte-for-byte
- RELEASE_DIFF.patch: every difference between the original and corrected package content except the regenerated manifest
- RELEASE_SHA256SUMS.json: full publication-packet integrity, including all three subpackages

No source PDFs, extracted source texts, source screenshots, complete or selected corpus records, raw API responses, credentials or private coordination are included. Source hashes and bibliographic metadata support provenance without redistributing source material.

## Reproduce

Using Python 3.10+ standard library, from this folder:

    python3 submission/verify_manifest.py
    python3 corrected_release/verify_manifest.py
    python3 corrected_release/verify.py
    python3 audit/verify_audit.py
    python3 verify_release.py

The finite algebraic controls do not decide smooth topology or evaluate gauge invariants. External topology and gauge-theory theorems remain declared inputs. No full solution, formal proof verification, or exhaustive literature search is claimed.

The associated queue edit changes only this target's Status to unsolved and Turns to 5/5. Findings and every other queue byte are preserved.
