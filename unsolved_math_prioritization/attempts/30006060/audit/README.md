# Independent audit of positive three-braid concordance

Problem 30006060, OWR-14298592-014. All five scoped mathematical approaches pass independent review. The original smooth-concordance problem remains **unsolved, 5/5**.

The required correction concerns verification under optimized Python, not the mathematics. The original author freeze is preserved. `corrections/verify.py` is a separately supplied hardened derivative; `VERIFY_HARDENING.patch` describes its only change.

## Portable replay

Python 3.10 or later, standard library only:

    python3 verify_manifest.py
    python3 independent_verify.py > /tmp/positive-braid-replay.json
    python3 -O independent_verify.py > /tmp/positive-braid-optimized.json
    cmp /tmp/positive-braid-replay.json independent_results.json
    cmp /tmp/positive-braid-optimized.json independent_results.json
    python3 run_controls.py > /tmp/positive-braid-controls.json
    cmp /tmp/positive-braid-controls.json CONTROL_RESULTS.json

`run_controls.py` automatically repeats clean runs in a temporary relocated directory, rejects five independent corruptions in both modes, replays the hardened author checker, and demonstrates why the original assertion implementation needed correction. It requires no network, author directory, external corpus, or third-party packages.

The independent verifier uses 163 explicit checks. All 20 subprocess controls passed. See `AUDIT.md` for the geometric identification, exact claims and source hypotheses; `SOURCE_REVIEW.md` and `PUBLIC_METADATA.json` for bounded identity/source/prior-artifact verification; and `ACCEPTANCE.json` for the machine-readable disposition.

Only authored audit prose/code/corrections, calculated results and public verification metadata are included. Source PDFs, text extracts, page images, dataset contents, private sources and private coordination are excluded. This is an independent agent audit, not human peer review.
