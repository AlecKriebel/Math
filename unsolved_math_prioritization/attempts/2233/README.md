# Erdős Problem 653: unresolved after two attempts

The original question asks whether n planar points can have n−o(n) different pinned-distance counts. This package does not prove or refute that claim.

[PARTIAL.md](PARTIAL.md) proves that generic gluing preserves the seed deficit spectrum, so a hierarchy of small seeds cannot amplify the spectrum to the required size. It also proves a one-half barrier for points on a line or circle, including a sublinear number of exceptional points, and recalls the classical Erdős–Saldanha two-pin estimate. These are elementary route obstructions with no novelty claim.

[SOURCE_AUDIT.md](SOURCE_AUDIT.md) recovers the exact question from a full 1995 primary source and records access limitations and newer external preprint claims. Those claims are not used in the proof and have not been independently certified here.

Run `python check_spectra.py`. It uses exact integer and rational squared distances and passes 18,306 finite assertions, including generic gluing, a nongeneric negative control, restricted-support examples and small-grid subsets. It cannot establish an asymptotic result.

Separate adversarial review is pending. The model used was gpt-6-astra at xhigh reasoning.
