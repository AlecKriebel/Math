# Independent audit of the frozen TZ curvature investigation

Verdict: **PASS WITH CONTROLLING CLARIFICATIONS for unsolved 5/5 only. NO RESOLUTION.**

`AUDIT.md` gives the complete proof/source review, exact input binding, and the two controlling Approach 1 wording clarifications. `SOURCE_AUDIT.json` records independent public-source retrieval and inspection. `INDEPENDENT_RESULTS.json` records 23 passing check groups, including the separately labeled original 11-control replay and eight deliberate-error rejections. None computes actual finite-type TZ curvature.

Run, with the paths to the preserved original public directory and ZIP:

    python independent_controls.py /path/to/original/public /path/to/original.zip > /tmp/tz-independent-results.json
    cmp INDEPENDENT_RESULTS.json /tmp/tz-independent-results.json
    python verify_audit_manifest.py

Recorded environment: Python 3.12.14, SymPy 1.14.0, mpmath 1.3.0. Output-byte equality is an environment-specific replay check; the written mathematics does not depend on presentation strings or high-precision quadrature.

The audit manifest excludes its own bytes and binds every other allowlisted audit file. The audit ZIP hash and manifest hash are delivered separately in a receipt. The original manifest and ZIP digests are hardcoded in the independent checks. All original bytes remain unchanged. This separate audit does not mutate the original pending-audit status field.

No source PDFs, text extracts, screenshots, raw dataset records, or private coordination files are distributed here. Public scholarly metadata and links are included. All source rights remain with their holders. This is an audit of an unsuccessful investigation, not a solved-problem manuscript or a novelty claim.
