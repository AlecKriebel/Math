# Problem 30002167: disk tour counterexample

**Partial resolution only:** the proposed squared-edge Hamiltonian-cycle bound 8 is false, even for six distinct rational points strictly inside the Euclidean unit disk. The separate perfect-matching bound 4 and other-convex-body questions are not settled here.

`PROOF.md` contains the complete analytic counterexample and a lower bound 9 on any possible universal replacement constant. `exact_checks.py` replays the optional exhaustive six-point certificate with exact arithmetic. `verify_manifest.py` checks the frozen file set and hashes. `negative_controls.py` checks rejection of four deliberately false mathematical claims and four manifest mutations.

Run from any directory:

    python3 exact_checks.py
    python3 -O exact_checks.py
    python3 verify_manifest.py
    python3 negative_controls.py

All scripts resolve local files relative to themselves. They use only the Python standard library, make no network calls, and require no source documents or external datasets.

The primary OWR page was downloaded, text-inspected, rendered, and visually checked. The exact aggregator URL returned HTTP 403, so its page text was not independently inspected. The raw AI corpora were unavailable and uninspected. `SOURCE_VERIFICATION.json` and `RESEARCH_LOG.md` record the limitations and search scope. No global-openness or novelty claim is made.

This authored packet contains no source PDF, source extraction, source image, raw dataset record, or private coordination material. It is an unrefereed candidate awaiting independent review.
