# Research log and bounded disposition

Date: 2026-10-05. Problem: 30002753 / OWR-13359-003, rank 726.

## Intake and identity checks

The descriptor identified *Optimal Geodesic Curvature for Random Transpositions*, sourced to DOI 10.4171/OWR/2014/57. Its queued 0/5 field was treated only as a queue observation, not proof that no earlier work exists. The raw AI-solution and AI-progress corpora were not present in the available inputs and were not inspected. No claim about their contents is made.

The exact URL https://www.unsolvedmath.com/problems/30002753 failed in the web reader and returned HTTP 403 through an ordinary local retrieval. A search for that exact URL did not yield the statement. No exact website-statement match is claimed. The 2014 OWR source was obtained both from the publisher and the TIB repository, and its printed page 3229 was visually inspected. Its preceding definitions specify entropy convexity in the Markov-chain transport geometry. The model's exact rates were checked in the cited Erbar–Maas–Tetali paper. The source asks for asymptotic order; an exact optimal-constant problem would be stronger and remains unresolved as well.

## Repository history check

Read-only GitHub connector checks against AlecKriebel/Math:

- All-state PR searches for `30002753` and `OWR-13359-003`: no results.
- All-state PR search for `transposition`: one unrelated result, PR 431 about involution-color reconstruction and alternating double transpositions; it is not this entropy-curvature problem. A prior plural `transpositions` search returned no results.
- Branch-name searches for `30002753`, `transpos`, and `geodesic`: no results, with no continuation cursor.
- Commit-message searches for `30002753` and `transposition`: no results.
- Default-branch reads of `unsolved_math_prioritization/attempts/30002753` and its `README.md`: HTTP 404.
- Default-branch queue row 726 read: queued, 0/5.
- Local task-directory name scan before creating this investigation found no earlier task-specific directory. The provided workspace has no usable Git checkout history.

Conclusion: no prior task-specific attempt was found through these checks. Search coverage is bounded: this is not an exhaustive scan of every historical file on every deleted or differently named branch. The main queue alone would not support the conclusion.

## Literature pass

Inspected the OWR contribution and the Erbar–Maas–Tetali definitions, Hessian criterion, model normalization, lower-bound mechanism and S_3 obstruction. Inspected Fathi–Maas's published Section 4.4: the random-transposition theorem is **4.9 in the published paper**, but **4.8 in the earlier preprint**. Both use the same normalized generator and reproduce the existing lower bound.

Later primary-source scope checks included Pedrotti's arXiv v2 (2025 final accepted version), Münch–Wirth–Zhang's intertwining-curvature preprint, and Caputo–Salez's entropy-factorization preprint plus its 2026 publisher page and author bibliography. The latter uses W_1/W_∞ coupling conditions and proves entropy factorization; those statements are not a logarithmic-mean Hessian bound for this problem. The intertwining paper itself distinguishes several curvature notions. None of the inspected relevant statements resolved this problem's asymptotic order. Targeted web searches included random transposition with entropic Ricci, sharp/optimal/order, and 2025/2026 qualifiers. This is a bounded negative search, not a proof of global openness.

## Five substantive approaches

The approaches are counted by distinct mathematical strategy; source retrieval and tooling are not extra attempts.

1. **Uniform-density spectral/representation approach.** Derived the exact Hessian quotient at density one and the eigenfunction based on one card's position. Retained proof: κ_n≤2/(n−1). Gap: an all-density lower bound cannot follow from a density-one diagonalization. The proposed sharpness is contradicted by approach 2.
2. **Nonuniform one-card density quotient.** Derived the exact one-parameter formula R_n(t). Retained results: strict improvement on the spectral upper bound for n≥3 and limsup nκ_n≤1. Gap: this is an upper-bound family and does not supply the missing lower scale.
3. **Coarse-graining/conditional comparison.** Proved exact equality of forms on lifted equitable-quotient tests and the correct curvature inequality direction. Solved the parity-restricted variational problem and n=2 exactly. Gap: pulling a quotient lower bound back to the full chain is false; parity gives an explicit obstruction. Mixed directions remain uncontrolled.
4. **Local Bochner geometry.** Revisited the published square/S_3 strategy and evaluated its local obstruction completely. Retained formulas: the off-diagonal quotient tends to zero, while the full quotient diverges. Gap: neither a strictly positive local off-diagonal bound nor an upper-bound sequence for the full form is available from this construction.
5. **Full finite-density Hessian optimization and certification.** Derived the matrix form, explored n=3 and n=4 over all density coordinates, and replaced the n=3 numerical candidate by an explicit exact witness. Retained result: κ_3<9/10 by rational algebra and log 2>2/3. Gap: no global finite optimum or all-n asymptotic order is certified. The n=4 numerical value is explicitly exploratory.

## Checks and stop condition

The exact checker passed 113 arithmetic assertions and graph controls totaling 872 distinct permutation states across n=2,...,6. It verifies the one-card formula, parity formula, S_3 obstruction including both diagonal and full terms, the n=3 witness, and scaling. Deliberately omitting density derivatives, dropping the factor 1/2, misnormalizing time, identifying the spectral value with the full optimum, and confusing the off-diagonal sharpness with full sharpness are rejected.

No full proof, counterexample to the primary problem, or verified prior resolution resulted. Stop at the assigned five-approach limit with status **unsolved**, turns **5/5**. Preserve these results for an independent adversarial audit. No remote writes or publication took place.
