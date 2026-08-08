# Replacement-manuscript plan

Date: 2026-08-08 (America/Los_Angeles)

## Editorial decision

The central statement is now the strict improvement

\[
R_{\rm sim}\ge 1.5028569127905696\ldots>3/2,
\]

not an exact `3/2` phase transition. The former endpoint-impossibility
candidate is false. The fixed-affine-separator program is also closed:
an exact endpoint witness violates the only coefficient not already excluded
by clique--pendant sharpness.

The previous lower-bound paper remains correct as a theorem about its own
center--triangle family, but this manuscript supersedes it.

## Proof architecture

1. Define the model, complete-graph baselines, and the quantifiers in
   `R_sim`.
2. Display the dilute hybrid: a large clique with hub pendants and weakly
   coupled internally heavy `K_2` satellites.
3. Prove exact orbit lumpability and the finite weak-cut Schur trace.
4. Prove the center singleton estimates, including the path from a
   mesoscopic core seed to full fixation.
5. Derive the two pair-gate odds and prove the post-gate sweep.
6. Obtain the normalized coefficients
   \[
   B={2(\sigma-1)\over1+\sigma(r^2-1)}
     +{\lambda\over r-1},\qquad
   D={2(r(2-r)-\sigma)\over\sigma+2r(r-1)}-\lambda.
   \]
7. Optimize the feasible interval `L<lambda<U`, producing the sextic and
   its isolated root `R_hyb`.
8. State both fitness-independent diagonals: the transparent `C=t^4`
   count scale and the independent least-integer iterated diagonal.
9. Separate exact proof, exact computation, numerical hostile audit, and
   open problems.

## Evidence map

| Claim | Analytic source | Independent replay |
|---|---|---|
| finite orbit lumping | labelled event aggregation | `verify_hybrid_lumping.py` |
| pair and leaf coefficients | trace equations | `verify_hybrid_coefficients.py` |
| sextic/tangency | quadratic optimization | `verify_leading_algebra.py` |
| center error at strict scale | logarithmic cutoff and cleanup blocks | `HYBRID_CONSTRUCTION_AUDIT.md` |
| effective iterated diagonal | compact-uniform two-step limit | `DILUTE_HYBRID_THEOREM.md` |
| novelty context | narrow post-proof audit | `LITERATURE_AUDIT.md` |

## Before release

- Complete a line-by-line hostile proof audit of `main.tex`.
- Compile and visually inspect the PDF.
- Add equation-level cross-references to every verifier.
- Generate a deterministic manifest and archive.
- Update the project claims ledger without overwriting parallel work.
- Do not reuse the previous title suggesting that `3/2` is the boundary.
- Do not claim the exact value of `R_sim`.
