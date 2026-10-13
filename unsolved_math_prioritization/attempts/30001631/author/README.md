# 30001631: curvature of the Takhtajan–Zograf metric

**NO RESOLUTION. Five attempted approaches with rigorous partial lemmas.**

The source leaves the curvature convention unspecified. This package distinguishes real sectional, holomorphic sectional, holomorphic bisectional, and Ricci curvature, and does not claim a sign theorem for any of them on the actual finite-type TZ metric.

- `RESEARCH.md`: full definitions, five approaches, proofs, and exact gaps.
- `APPROACH_LOG.md`: ordered research checkpoints and completion estimates.
- `STATUS.json`: machine-readable scope and outcome.
- `SOURCE_VERIFICATION.json`: public source links, byte counts, hashes, inspection scope, and provenance limitations.
- `check_controls.py` and `CONTROL_OUTPUT.json`: eleven exact symbolic/algebraic controls, none evaluating the curvature of an actual Riemann surface.
- `MANIFEST.json` and `verify_manifest.py`: frozen-byte verification.

Run from this directory:

    python verify_manifest.py
    python check_controls.py > /tmp/tz-controls.json
    cmp CONTROL_OUTPUT.json /tmp/tz-controls.json

The control output was generated with Python 3.12.14 and SymPy 1.14.0. Other versions may change presentation strings; equality of the output bytes is a replay check for the recorded environment. Mathematical proofs do not depend on SymPy.

The exact primary OWR question and surrounding context were inspected. The live UnsolvedMath page could not be retrieved, and the complete raw upstream statement/AI-report corpus was unavailable. The compact catalog's recorded statement hash was not recomputed from that missing source. These limitations remain explicit.

Primary source: [Obitsu in OWR 53/2010, printed p. 3130](https://ems.press/content/serial-article-files/46312). The packet contains no source PDFs, text extracts, screenshots, raw dataset records, or private coordination materials. Source copyrights and terms remain with their respective rights holders. This is a research note with elementary partial deductions, not a solved-problem manuscript or a novelty claim.
