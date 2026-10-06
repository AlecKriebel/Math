# Ricci-flow Weyl/scalar cones: exact partial results

**Problem 30000789 / OWR-1588-003, rank 815. Outcome: UNSOLVED HERE after five substantive mathematical approaches.**

This package does not prove that the threshold is 12. It supplies a complete algebraic reduction, explicit obstructions below 12, and rigorously verified restricted tests at 12. No novelty, historical priority, exhaustive literature clearance, formal proof-assistant certification, or human peer review is claimed. Independent audit is pending.

## Main results

For the Hilbert–Schmidt curvature-operator norm, write

\[
R=aI+E(S)+W,\quad E(S)=\frac{2}{n-2}S\wedge\mathrm{id},\quad \operatorname{tr}S=0,
\quad N=\binom n2.
\]

Define

\[
\mu_n=\max_{S\ne0,\,\operatorname{tr}S=0}
 \frac{\|P_W(S\wedge S)\|}{|S|^2},\qquad
\beta_n=\max_{W\ne0,\,\operatorname{Ric}W=0}
 \frac{\langle Q(W),W\rangle}{\|W\|^3},\quad Q(R)=R^2+R^\#.
\]

The closed cone \(a\ge0,\ \|W\|^2\le cNa^2\) is ODE-invariant **if and only if**

\[
\frac{4N\mu_n^2}{(n-2)^2}\le c\le
\frac{(n-1)^2}{N\beta_n^2}.
\]

The proof includes the nonsmooth scalar-zero locus; differentiating the squared inequality alone would miss that obligation.

- For every even \(n\ge4\), invariance can occur only at \(c=n/(n-2)\). It occurs exactly when \(\beta_n^2\le 2(n-1)(n-2)/n^2\).
- No such cone is invariant in any dimension \(4\le n\le11\). In dimension 11, necessary bounds are \(c\ge2662/2187\) and \(c\le40/33\), with incompatible gap \(122/24057\).
- At dimension 12, the missing global bound is \(\beta_{12}^2\le55/36\). A four-dimensional self-dual Weyl tensor embedded in dimension 12 gives \(3/2=54/36\), so it falls just short of a counterexample.
- The balanced two-block Weyl tensor is a strict local maximum within the entire 54-dimensional **diagonal** Weyl subspace at dimension 12. The norm-sphere tangent space has dimension 53. This is not the 1,638-dimensional full Weyl space.
- Four explicitly specified two-dimensional spans of that balanced tensor and embedded self-dual tensors satisfy the target cubic inequality globally, by positive quartic certificates. This excludes those pencils, not all possible mixtures.

For odd \(n\), the Ricci endpoint lies strictly below \(n/(n-2)\). The desired nondegenerate interval around this center is equivalent to the strict global bound
\(\beta_n^2<2(n-1)(n-2)/n^2\). Thus proving only the dimension-12 inequality would still not prove the all-dimensions threshold assertion.

## Read in order

1. [Statement and literature boundaries](STATEMENT_AND_SOURCES.md)
2. [Approach 1: full tangency criterion](ATTEMPT_1.md)
3. [Approach 2: sharp Ricci-side estimate](ATTEMPT_2.md)
4. [Approach 3: global obstruction families](ATTEMPT_3.md)
5. [Approach 4: exact diagonal local maximum](ATTEMPT_4.md)
6. [Approach 5: exact mixed pencils and remaining gap](ATTEMPT_5.md)

## Reproducibility

Requires Python 3 and SymPy (author environment: 1.14.0). Run `python -B math_check.py`; its output must equal `results.json`. The exact diagnostics and mutation tests supplement the written proofs. They neither inspect all Weyl tensors nor certify the missing universal inequality.

Run `python -B verify_package.py --expected-manifest HASH`, substituting the externally supplied SHA-256 of `MANIFEST.json`. The same commands work under `python -O -B` and from unrelated working directories. The expected manifest hash must come from the independent handoff receipt, not be silently recomputed from a possibly altered package.

`VERIFICATION.md` records normal, optimized, relocated, and mutation outcomes. `PUBLIC_METADATA.json` records source provenance and full-record review hashes without distributing the underlying records. Only authored proof/code/results and public verification metadata are included. Source PDFs, extracts, images, full data corpora, and private coordination material are excluded.
