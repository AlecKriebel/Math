# Local complexity of functional estimation

Problem 30005248 · OWR-11695855-001 · catalogue rank 486

**Status: partial progress; no full resolution.** Five substantive approaches are recorded. The elementary examples and reductions below are not claimed to be new. Important parts of the broad question were already treated in the literature, including before the original report.

## What is established here

- A self-contained multinomial example proves that the minimax squared error for estimating L1 distance from a known reference can depend polynomially on that reference. A cited sharp theorem gives a risk ratio of order S/log S between the uniform and point-mass references at n=S.
- A group-invariance argument proves exact reference-independence for unrestricted Gaussian location models with translation-invariant discrepancies.
- Explicit neighborhood-local Bernoulli risks differ at the boundary and in the interior. This is a different minimax convention and is labelled accordingly.
- A family of tolerant tests yields an estimator, with an explicit confidence-amplification cost. A single-threshold result is insufficient for that reduction.
- In the Bernoulli boundary example, the tolerant-testing sample complexity is of order (nu+delta)/delta^2, or a critical gap of order sqrt(nu/n)+1/n within the admissible range.

## Files

1. [Paired-sign lower bound](turn_01.md)
2. [Sharp prior discrete theory and its regime restrictions](turn_02.md)
3. [Symmetry and local-neighborhood distinctions](turn_03.md)
4. [Testing–estimation reductions](turn_04.md)
5. [A complete Bernoulli transition calculation](turn_05.md)

[Source and scope audit](SOURCE_AUDIT.md) records authorship, literature, and why the general research direction remains unclosed. [Research log](RESEARCH_LOG.md) records the outcome of each route.

Run `python verify_exact.py` to reproduce 16,459 exact rational checks; [verification.json](verification.json) records their output. These finite checks do not prove the asymptotic theorems or replace independent review.

No general classification, novel full solution, or first-priority claim is made. Prepared 3 October 2026; external mathematical review is still needed.
