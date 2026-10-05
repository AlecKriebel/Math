# Critical Dirac potentials: verified candidates and a fixed-potential angular theorem

Problem 30005664 / OWR-14297742-004, queue rank 779.

**Disposition: the original global optimization question remains unresolved after five substantive approaches.** This is an AI-assisted, unrefereed research note. No novelty, human peer review, journal acceptance, or full solution is claimed. A fresh independent review is still required.

The Aubin–Talenti candidate and its norm bound in dimensions two and three are already in Dolbeault, Gontier, Pizzichillo and Van Den Bosch, §5.4. This package credits that construction and proves the following limited statements with explicit hypotheses:

1. A Clifford-algebra construction of the threshold candidate for every integer d≥2 and finite p>d, including the mass normalization and an H¹ eigenstate.
2. Exact minimization within one explicitly specified one-parameter family of threshold bubble potentials. This is not minimization among all potentials of rational shape.
3. A Pohozaev identity and p=d nonexistence in a stated dilation-differentiable H¹ stationary class.
4. The concentrating p=d boundary of the explicit bubble family.
5. In d=2, an exact factorization of the threshold Schur form of the fixed candidate in every angular Fourier mode. Its kernel is radial, and its nonradial part has a lower bound 4m/p times its L² mass. This does not compare the candidate with other potentials. A weighted modulus shortcut is also disproved.

See `PROOF.md` for all proofs and the exact remaining gap, `APPROACHES.md` for the five attempts, and `SOURCE_VERIFICATION.json` for bounded source and provenance checks.

Reproduce from this directory with Python 3 and SymPy 1.14.0:

    python check.py > /tmp/critical_dirac_results.json
    cmp /tmp/critical_dirac_results.json RESULTS.json
    python verify_manifest.py

The finite checks are algebraic controls, not replacements for the analytic proofs. No source PDFs, source extracts, images, raw dataset records, private correspondence, or coordination material are included.
