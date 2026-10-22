# Candidate proof package: corrected Function Theory Problem 5.38

This package proposes complete short proofs of both classical sharp inequalities:

- If F∈S, g=F∘φ, φ(0)=0 and φ′(0)∈[0,1], then |g(z)|≤|F(z)| for |z|≤(3−√5)/2
- Under the same hypotheses, |g′(z)|≤|F′(z)| for |z|≤3−√8

Both sharpness constructions are included. Subordinate g and φ need not be univalent.

## Verification reading order

1. SOURCE_SCOPE.md: exact source problem, corrected nonnegative-derivative hypothesis, and success criteria
2. TURN_1.md sections 2–4: attainable Schur-jet region, ordinary Koebe-transform derivative distortion, and sharpness
3. TURN_2.md sections 1–3: small-a derivative bound and full degree-two boundary calculation
4. TURN_3.md: exact interior-jet normalization and defect monotonicity, completing the derivative proof
5. TURN_4.md: standalone Grunsky phase-separation proof of the modulus half, with proof of the needed odd-function Grunsky consequence

The remaining sections preserve the development, failed mechanisms and limited source comparisons. No unpublished empirical assertion is used as a proof premise. Each file is a checkable mathematical argument rather than an execution transcript.

## Check commands

Run python verify_turn1.py, python verify_turn2.py, python verify_turn3.py, and python verify_turn4.py from this directory. Turn 1 uses the Python standard library. Turns 2–4 use SymPy (tested with 1.14.0). The scripts check exact algebra; they are not independent reviews or complete proof verifiers.

## Candidate and historical status

The complete proposed candidate was obtained in substantive author turn 4 of a five-turn budget on 2026-10-02. Independent mathematical review is pending. The qualitative request for simpler proofs requires assessment, not a theorem claim of novelty.

The derivative proof uses Schwarz–Pick, ordinary Koebe derivative distortion, a monotone interior-defect parameter, and a concavity certificate with two factorized endpoints. The modulus proof uses the classical Grunsky inequality, an odd-function transform, and phase separation established by two elementary factorizations. These are explicitly proposed simplifications of known results. The underlying two-point/Schur and odd-function mechanisms are credited to the classical literature.

Shah's original papers and full Campbell III were not recovered. Historical originality and superiority over every prior proof are not established. The false literal real-only normalization in the problem source is documented separately and is not being passed off as the intended solution.

## Primary references read

- W. K. Hayman and E. F. Lingham, Research Problems in Function Theory, arXiv:1809.07200v2, Problem 5.38 and update, PDF pp.99–100: https://arxiv.org/pdf/1809.07200v2
- D. M. Campbell, Majorization-subordination theorems for locally univalent functions II, Canadian J. Math. 25 (1973), 420–425, especially Theorem 3 normalization: https://doi.org/10.4153/CJM-1973-042-6
- R. W. Barnard and K. Pearce, A proof of Campbell’s subordination conjecture, author manuscript 2008, pp.1–5 for the prior proof structure: https://kjpearce100.github.io/mathwebsite/papers/bp1.pdf
- P. Duren, Subordination, Lecture Notes in Mathematics 599 (1977), 22–29; official reference https://doi.org/10.1007/BFb0096821; indexed copy and OCR limitation described in TURN_4.md
- P. L. Duren and M. M. Schiffer, Grunsky inequalities for univalent functions with prescribed Hayman index, Pacific J. Math. 131 (1988), 105–117; classical Grunsky statement at printed p.105 directly inspected: https://msp.org/pjm/1988/131-1/pjm-v131-n1-p06-p.pdf

Source PDFs remain local-only. No external researcher was contacted.
