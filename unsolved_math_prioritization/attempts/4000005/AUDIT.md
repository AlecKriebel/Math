# Mathematical audit of the nonreversible curvature counterexample

## Verdict

This is an AI-assisted mathematical assessment; it is not external human peer review or formal proof-assistant certification.

**PASS for the mathematical counterexample and its stated finite-approximation obstruction, with the scope clarifications below incorporated in PROOF.md.** This is an attributed reconstruction of a published counterexample, not a new solution claim. No fatal mathematical error was found in the frozen candidate.

The exact corpus target is problem 4000005, AMR-039-0005, “Non-reversible spectral gap,” row 1712. The frozen candidate was 5,051 bytes, SHA-256 `fe5cc54848e3a588db89092f14ef63531429881536ae3955eb507460a4842e04`. Its bytes and the three frozen source PDFs remained unchanged through final verification.

## Findings that matter

1. **Published prior counterexample verified.** Gong–Liu–Wen (2013), §3, printed p. 495, gives the same one-sided Bernoulli-prepending construction and credits Gong and Wu. The first source PDF includes a repository cover, so this is PDF page 6, zero-based page 5. The page was visually inspected, not just text-searched.
2. **Adjoint-order error verified against the actual definition.** The same printed paragraph defines its averaging operator by prepending before printing M* M = Id. Direct product integration gives M* f = f composed with the left shift and M M* = Id. The nonzero first-coordinate character is killed by M, so M* M = Id is impossible. Prefer “printed adjoint-order error under the explicit convention” to speculating about authorial intent or claiming an official erratum. The conclusion is independently correct.
3. **No hidden stationarity, topology, or moment failure.** The space is compact Polish, the kernel is Borel and Feller, the invariant product law has full support and is unique, the diameter is one, and the average squared diffusion quantity is 1/4. The curvature is exactly 1/2, not merely bounded below by it. The parameterized metric gives exactly 1−a for every 0<a<1.
4. **Irreducibility needs careful naming.** The infinite chain reaches every nonempty open set from every point, but it is not stationary-measure/Harris irreducible: a starting point has only countably many finite-time descendants. This added hypothesis is absent from Ollivier's general definition and Problem E. The construction must not be advertised as a counterexample in that stronger class. The finite truncations genuinely are irreducible and aperiodic.
5. **Norm, spectrum, coercivity, and convergence are distinct.** The complex mean-zero L2 spectrum is the closed unit disk, all power norms are one, and the spectral radius is one. However every fixed mean-zero L2 function converges strongly to zero under iteration. There is no unit-modulus eigenvalue. Lipschitz-norm contraction still holds. The proof states the Hilbert space, complexification, adjoint, domains, and quotient identification explicitly.
6. **All three energy calculations verified.** The ordinary jump energy is the real part of the quadratic form for I−P, equivalently the form for additive symmetrization. For the normalized N-coordinate sum its value is 1/N; the squared (I−P) norm is also 1/N. Conditional variance already vanishes for e1 while its stationary variance is one. All witnesses are Lipschitz cylinders.
7. **Finite approximation obstruction is stronger than mere weak resemblance.** Finite operators have exactly uniform L-step laws, hence mean-zero nilpotence; their consistent finite-rank extensions converge strongly on the common infinite Hilbert space. Nevertheless spectral radius jumps from zero to one. The convergence is not in operator norm: the difference norm is one at every size. Uniform curvature supplies no uniform L2 exponential-decay prefactor. This does not disprove approximation results with further uniform control.
8. **Exact finite ordinary Poincaré gap added and proved.** Walsh characters decompose the finite operator into nilpotent shift blocks. Additive symmetrization of the longest block has top eigenvalue cos(π/(L+1)), giving gap 1−cos(π/(L+1)) and Poincaré constant asymptotic to 2(L+1)^2/π². The frozen candidate's simpler lower bound C≥L is valid but not sharp.
9. **Imported citation mismatch confirmed.** Erbar–Fathi arXiv:1612.00514v1, p. 2 and §2.1 p. 4, imposes finite, irreducible, reversible, continuous-time hypotheses; its curvature is entropic. It does not support the imported assertion of a nonreversible coarse-curvature extension. No broader negative statement about all other literature follows from this citation check.
10. **Problem E is not wholly replaced by a universal “solved” label.** Its unrestricted positive-gap expectation receives this known negative answer, including the displayed local energies. Other hypotheses, sharper specialized bounds, nonlocal gradients, and quantitative approximation frameworks remain separate. The reversible spectral-gap result and Ollivier's nonlocal-gradient inequality are preserved.

## Claim-by-claim decision on the frozen candidate

- Construction and curvature lower bound: accepted; exact curvature proved.
- Invariant measure and Feller property: accepted; uniqueness/full support added.
- Mean-zero power norms and radius: accepted.
- Entire closed unit disk as complex L2 spectrum: accepted; complex convention added.
- Adjoint formula and order discrepancy: accepted; source visually checked and wording made precise.
- Nonreversibility: accepted.
- Ordinary Poincaré, conditional-variance, and residual inequalities: accepted; exact energies and complex real-part convention supplied.
- Finite nilpotence, norm, and degenerating energy: accepted; L=1 edge case and irreducibility verified.
- Finite approximation warning: accepted within its stated scope; common-space strong convergence and absence of norm convergence made explicit.
- Erbar–Fathi citation correction: accepted for the inspected source and claim.
- Historical novelty or contradiction of reversible theory: neither claimed nor justified.

## Reproducibility and inspection

The retained numerical verification performs exact integer checks on finite chains for L=1,…,7: stochasticity, uniform stationarity, exactly uniform L-step transitions, self-loops, orthogonality, backward-shift action, energy witnesses, and nonreversibility. Exact rational two-point transport computations inspect every distinct pair for L=1,…,5, for a=1/2, 1/3, and 3/4 (1,953 pair/metric cases). Small floating-point symmetric eigendecompositions independently diagnose the exact Poincaré-gap formula; the proof of that formula is symbolic, not numerical.

The final script passed all 110 checks under ordinary Python, `-O`, and `-OO`. It does not use `assert`, so optimization does not disable its checks. An exact negative control rejects the printed adjoint identity through its norm implication on e0. Frozen hashes are checked, not silently regenerated.

The infinite-dimensional spectral result, strong convergence, irreducibility distinctions, and full exact finite gap are mathematical arguments in PROOF.md. The numerical work is supporting evidence only.

The original-problem and Gong pages were locally rendered and visually inspected. The web tool corroborated Gong's PDF and Erbar–Fathi's PDF; it encountered a redirect-loop error on the original-problem URL, so that item's frozen local PDF, rather than a claimed fresh web fetch, supplies the inspected evidence. An independent public JFA PDF was retrieved and pinned, and the relevant definitions and propositions were checked. Detailed inspection locators and hashes are in SOURCE_PINS.json. Source PDFs and page images are retained only as private inspection material, not included in the authored proof deliverables.

## Proposed record correction

Suggested bounded status text:

“Known negative answer to the unrestricted nonreversible L2-gap extension: the Gong–Wu Bernoulli-prepending counterexample, published in Gong–Liu–Wen (2013), has positive coarse Ricci curvature but L2 spectral radius and norm one. Its ordinary local Poincaré and one-step conditional-variance bounds fail. Consistent positively curved finite truncations do not transfer their spectral-radius bounds without further uniform analytic control. Nonlocal-gradient bounds and estimates under additional hypotheses are separate.”

This report supplies a bounded mathematical recommendation. It does not claim to settle all questions in Problem E. The accepted candidate and inspected source bytes remain unchanged. Source documents, source extracts, datasets, scripts, and coordination materials are excluded from this authored report package.
