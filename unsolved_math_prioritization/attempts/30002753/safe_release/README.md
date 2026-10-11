# 30002753: random-transposition entropic curvature

**Unsolved in this investigation; 5/5 approaches used. Independent audit pending.**

The original source asks for the correct order of the optimal logarithmic-mean entropy-geodesic-convexity constant for the total-rate-one continuous-time transposition chain on S_n. This is not ordinary Ollivier curvature. The exact website statement could not be read; the catalog-to-primary-source correspondence and this limitation are recorded.

Retained proved results include an explicit one-card upper-bound family with limsup nκ_n≤1, the exact value κ_2=2, a rationally certified κ_3<9/10 witness, and explicit formulas showing why the published local off-diagonal obstruction does not prove sharpness of the full curvature bound. These do not determine the asymptotic order. No novelty claim is made.

- `PROOF.md`: definitions, five substantive approaches, complete retained partial proofs, and exact unresolved gaps
- `RESEARCH_LOG.md`: attempt accounting, source scope, and repository checks
- `SOURCE_VERIFICATION.json`: public-source titles, URLs, byte counts, hashes and inspection scope
- `STATUS.json`: bounded disposition and limitations
- `verify.py`: portable exact rational/Laurent-polynomial checks and negative controls
- `VERIFICATION.json`: arithmetic output from the author run
- `explore.py`, `EXPLORATORY_RESULTS.json`: optional numerical search provenance, not a mathematical certificate
- `MANIFEST.json`: exact safe-file inventory and hashes

Run `python3 verify.py` from this directory or any working directory. Python's standard library suffices for all certified controls. The exploratory script separately requires NumPy and SciPy; it is not required for verification.

The 113 exact arithmetic assertions check formulas, finite graph controls for n=2 through 6, rate scaling, and deliberate errors. They do not certify an all-density optimum or the infinite sequence of optimal constants. The analytic arguments and established Hessian criterion remain mathematical proof obligations for independent review.

Only authored mathematics, code and public verification metadata are included. No scholarly PDFs, text extracts, screenshots, raw problem records or private coordination files are part of this packet. No publication, repository mutation or remote write was performed for this investigation.
