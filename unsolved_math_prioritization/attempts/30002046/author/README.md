# 30002046 / OWR-11784-003: fixed-point investigation

Outcome: unresolved after five substantive approaches. This is an unrefereed AI-assisted partial-results packet, not a solution, a novelty claim, or a claim that the question is globally open as of today.

For the standard Minkowski question-mark function on [0,1], the retained proofs establish exactly three rational fixed points, no quadratic-irrational fixed points, at least two additional symmetric fixed points, and a complete exact enclosure of every lower-half nontrivial fixed point in an interval of width about 1.23e-47. A separate rational bisection computes one such point. Neither computation proves uniqueness.

The five approaches and their exact gaps are in PROOFS.md and APPROACH_LOG.md. Source verification and repository-history search limits are in SOURCE_VERIFICATION.json. The original OWR report was retrieved and its relevant page visually inspected. The exact UnsolvedMath page was inaccessible; its wording was not recovered. The original raw AI-corpus records were unavailable, and this packet does not claim to reproduce or verify their content or hashes.

Run with Python 3, without third-party packages or network:

    python3 verify.py --check

The command regenerates the exact rational certificate and controls and compares them byte-for-byte with EXACT_RESULTS.json. The controls include all reduced rationals below 1/2 through denominator 1500 (342090 inputs), 128 levels of adaptive Stern-Brocot subdivision, 160 rational bisections, and explicit failures of tempting shortcuts. Finite tests are not a proof of the original count.

All source PDFs, extracted source text, rendered source pages, raw catalogue records and private coordination are excluded. MANIFEST.json contains hashes and sizes of the authored files. No remote repository change or publication was performed by this investigation. Independent review remains pending.
