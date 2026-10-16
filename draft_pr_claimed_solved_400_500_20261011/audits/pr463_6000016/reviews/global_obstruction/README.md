# Independent global obstruction verification

This authored mathematical review checks the global positive-definite Hessian obstruction for the classical shear family in PR #463, problem 6000016. REPORT.md proves the universal claim by Stokes' theorem and, independently, by affine potential cocycles on the cover. CLAIM_LEDGER.json distinguishes proved statements from excluded extensions and priority questions. RESULT.json is confined to this mathematical review.

For the exact controls, install the pinned dependencies from requirements.txt into a private environment and run:

```sh
python3 check_global_obstruction.py
python3 -O check_global_obstruction.py
python3 run_review_controls.py
python3 -O run_review_controls.py
```

The first two commands emit identical deterministic JSON, with 140 exact algebra checks each. The runner performs two valid runs and 16 expected false-claim rejections per invocation. It emits deterministic JSON and does not write fixtures or make network calls. All rejection guards remain active with Python optimization. The recorded runs used Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0.

The analytic argument, particularly positivity and Stokes' theorem, is the proof of universal exclusion. The exact computation checks formulae and catches intentional corruptions; finite parameter controls do not certify a universal claim by themselves. This is not a formal proof-assistant certificate.

PUBLIC_OUTPUT_WHITELIST.json is an explicit, nonrecursive list of authored public payloads with their sizes and SHA-256 hashes. The whitelist intentionally does not hash itself. All primary-source PDFs and source images are private, excluded, and must not be recursively added to a publication package. This review does not authorize external publication or merge and makes no novelty or first-priority assertion.
