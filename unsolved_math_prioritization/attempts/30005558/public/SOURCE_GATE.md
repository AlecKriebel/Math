# Source and scope record

Checked 3 October 2026.

## Exact question

Rahul Pandharipande, “Maps to a moving elliptic curve,” in *Recent Trends in Algebraic Geometry*, Oberwolfach Reports 20 (2023), report 27, printed pp. 1491–1493. Question 2 and its degree-two normalization are on printed p. 1492 (PDF p. 8).

- [Publisher landing page](https://ems.press/journals/owr/articles/13750339)
- [Official report PDF](https://ems.press/content/serial-article-files/47021)
- [Author's report](https://people.math.ethz.ch/~rahul/MFO-RP-23.pdf)
- DOI: 10.4171/OWR/2023/27

The question asks for the higher-degree counterpart of the generating series integrating λ_{n+1}λ_{n−1} over admissible covers of a moving genus-one target, with 2n simple branch points and denominator (2n−1)!. The expected dependence is rational in q=−e^{iu}. The source's degree-two series fixes the branch-label and stack normalization.

The catalogue page [problem 30005558](https://www.unsolvedmath.com/problems/30005558) could not be retrieved: direct HTTP request returned 403. Its cached record was used only to identify the original report. No cached generated mathematical claim is used in the proof.

## Decisive update

A. Iribar López, R. Pandharipande, H.-H. Tseng, *Gromov–Witten theory of Hilb^n(C²) and Noether–Lefschetz theory of A_g*, [arXiv:2506.12438v2](https://arxiv.org/abs/2506.12438v2), submitted 14 June 2025 and revised 30 August 2025.

Read and used:

- Section 0.5.1, Theorem 1, and equation (0.5): exact, unconditional divisor-insertion formula and partition trace
- Sections 2.1–2.6: complete proof of the families Hodge-integral calculation, including the target Hodge-line injection and the fixed-elliptic-target calculation
- Sections 3.1–3.5: complete proof of Theorem 1, including connected/disconnected calculus, the partition identity, and the relative/descendent correction

The open nondegeneracy conjecture for general-insertion reconstruction is not used. In particular it does not qualify Theorem 1.

A later report independently points to this update: Aitor Iribar López, “Counting maps to an elliptic curve in several ways,” [Oberwolfach report 28/2025](https://ems.press/content/serial-article-files/51852), printed pp. 1492–1495, especially Theorem 1 on p. 1494. It is corroboration, not a substitute for the complete proof in the preprint.

## Correspondence and conventions

R. Pandharipande, H.-H. Tseng, *Higher genus Gromov–Witten theory of Hilb^n(C²) and CohFTs associated to local curves*, Forum of Mathematics, Pi 7 (2019), e4, [DOI 10.1017/fmp.2019.4](https://doi.org/10.1017/fmp.2019.4). Use the [author's August 2025 revision](https://people.math.ethz.ch/~rahul/HilbC2-2025-August.pdf).

Read and used:

- Section 0.6, Theorem 4 and the degree-two example: phase, branch labels, and normalization
- Section 3.2, including equation (3.1): the b! convention for b free branch points
- Section 11.1: complete proof of the Hilb/Sym correspondence; the pre-existing genus-zero and R-matrix results cited there are treated as established theorems
- Section 12: records the subsequent divisor calculation

The August 2025 revision repairs a rationality gap in the original paper. Footnote 7 of arXiv:2506.12438v2 explicitly says the analytic-continuation correspondence was unaffected. The present proof requires that correspondence and the explicit rational formula from the newer Theorem 1.

For compactified-cover conventions, Y. Len, S. Molcho, N. Nabijou, [arXiv:2609.17703v1](https://arxiv.org/abs/2609.17703v1), Section 0.5.2 and Section 1, explain the normalization by maps to BS_d and the decomposition by global monodromy type. This September 2026 paper was also checked as a recent related development; its computational Prym-class algorithm is not a dependency of the formula here.

## Scope and source caution

The answer in PROOF.md is for connected source curves with ordered branch points, unmarked unramified sheets, and stack automorphism weights, matching the degree-two source convention. It distinguishes the desired integral from both a relative stable-map integral and the disconnected symmetric-product invariant. Its Section 3 proves the extraction rather than asserting those three are identical.

The displayed d=5 example immediately following Theorem 1 in arXiv:2506.12438v2 has a sign inconsistency: the trace formula and Theorem 1 give −136/3 at q=0 for the normalized bracket, whereas that example prints +136/3. The argument and verifier use the trace theorem itself, not that displayed example. The displayed d=3 and d=4 examples agree exactly with the theorem and verifier.

## Dependency boundary

This is a deduction from established geometric theorems, with a detailed connected-cover extraction and an elementary evaluation of the resulting trace. It does not reprove orbifold Gromov–Witten theory, virtual localization, Mumford's Chern relation, or the Hilb/Sym correspondence from foundations. The arithmetic checks are independent exact checks of the deduction's algebra; they do not certify the geometric input.

No claim of a new solution or of first priority is made. The 2025 result supplies the decisive existing solution input.
