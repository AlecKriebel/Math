# Problem 30003221: prior spherical-flocking theorem

**Reviewed disposition: already_solved, 0/5.** Frank–Lieb's published 2021 Theorem 1.1 answers the original question affirmatively for every alpha>0: take dimension N=3 and repulsive exponent lambda=1. For every sufficiently large mass, all minimizers among capped densities are ball indicators, up to null sets and translation. [Published result](https://doi.org/10.2422/2036-2145.201909_007).

- [Exact source and theorem alignment](SOURCE_STATUS.md)
- [Main proof-chain and external dependency audit](DEPENDENCY_AUDIT.md)
- [Independent source-resolution review: PASS](final_review/REVIEW.md)
- [Frozen author/source packet integrity](FINAL_FROZEN_MANIFEST.json) and [review integrity](final_review/REVIEW_MANIFEST.json)

The frozen packet records its pending-review history; this additive wrapper records the accepted final disposition. The result is credited prior mathematics. Neither the packet nor its review claims a new theorem or an independent foundational recertification of all classical rearrangement/spectral/compactness inputs. The full-density domain, cap, mass, both coefficient-1 kernels and common factor 1/2 match exactly. The catalog's perimeter/integrable-kernel citation describes a different model.

## Replay

Both checkers use Python 3 standard library only:

    python verify_source_alignment.py > /tmp/nonlocal-author.json
    cmp SOURCE_CHECKS.json /tmp/nonlocal-author.json
    python final_review/run_portable.py --math-only

The author replay gives 157 exact algebra/scope controls. The source-free independent replay gives 30 controls, explicitly excluding eight source PDF hashes. To reproduce the full historical 38-control receipt, obtain the eight PDFs listed in SOURCE_MANIFEST.json with the listed local filenames and run:

    python final_review/run_portable.py --sources /path/to/source-pdfs > /tmp/nonlocal-review.json
    cmp final_review/INDEPENDENT_CHECKS.json /tmp/nonlocal-review.json

The original independent script and receipt are preserved byte-for-byte; the wrapper adapts paths and the explicit source-hash mode. These controls cannot establish the analytic variational theorem. Source PDFs and imported records are not redistributed.

No optimal or alpha-uniform threshold, all-mass ball claim, uncapped-measure result or general quantitative gap for non-minimizers is asserted.
