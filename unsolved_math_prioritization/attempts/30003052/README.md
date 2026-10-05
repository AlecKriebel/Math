# 30003052: linear-map Koopman spectra

The complete classification candidate is in [CLASSIFICATION.md](CLASSIFICATION.md). Its exact setting is the complex Banach space C(U), where U is the closed unit ball of any complex norm on finite-dimensional space and A is a contraction.

The central step forces every unimodular Koopman eigenfunction to factor through the peripheral spectral projection. Combined with credited known cases and a nilpotent splitting, this gives both point and full spectra, including all zero-eigenvalue cases. Separate adversarial AI review passed; see [the independent report](review/REVIEW.md). The frozen proof retains its submission-time status header. Historical priority has not been established; the work is not human-peer-reviewed.

- One substantive proof family, within the five-family ceiling
- 473 exact submitted controls and 907 independent exact controls pass
- Reproduce with Python3 and SymPy: run verify.py from this directory; its JSON receipt is printed to stdout
- The controls support finite algebraic identities; the written proof supplies compactness, continuity, recurrence, Stone–Weierstrass density and spectral closure
- Full source provenance: SOURCES.md and source_manifest.json
- The coordinating task owns queue updates
