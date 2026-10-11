# Functional inequalities and coarse Ricci curvature

Research package for **4000010 / AMR-039-0010**, Ollivier's Problem J, rank 553.

**Status: partial results; the full exploratory question is not claimed solved. No novelty claim.**

The main useful distinction is between a quadratic-then-linear function of the Wasserstein distance and an optimal transportation cost with that function inside the integral. The first follows from a finite Laplace window. The correction-free second formulation fails even for a reversible two-point curvature-one chain. A weak defective cost bound and exact two-point optimal defect are also proved.

- [Proof and precise remaining scope](PROOF.md)
- [Primary-source, literature, and previous-attempt checks](SOURCE_GATE.md)
- [Five substantive approaches](ATTEMPT_LOG.md)
- [Machine-readable claim boundary](CLAIMS.json)
- [Verification code](verify.py) and [recorded results](verification_results.json)
- [Frozen SHA-256 manifest](FROZEN_MANIFEST.json)

## Reproduce

Run `python3 verify.py` with Python 3.11 or newer. The code uses only the standard library and writes `verification_results.json`. Exact rational controls and high-precision numerical regressions are explicitly separated. It needs no network, source PDFs, or dataset.

The proofs use the standard Kantorovich--Rubinstein duality theorem, and otherwise include the needed analytic arguments. No finite test is offered as proof of an infinite or universal assertion. The source PDFs used for local checking are not redistributed.
