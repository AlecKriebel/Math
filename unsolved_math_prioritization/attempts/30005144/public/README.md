# CMC min–max width under nonnegative scalar curvature

**Problem:** 30005144 / OWR-10252937-007, queue rank 484.  
**Disposition:** complete literature-based affirmative reduction, pending fresh independent audit.  
**Research budget:** 1/5 substantive attempt; stopped at the complete candidate.  
**Date:** 3 October 2026.

For a connected complete boundary-free asymptotically flat three-manifold of nonnegative scalar curvature, other than Euclidean space, the proposed inequality is

\[
\omega_c(M)<\frac{16\pi}{3c^2}\qquad(c>0).
\]

The decisive prior work is Liam Mazurowski and Jintian Zhu, *Existence of Constant Mean Curvature Surfaces in Asymptotically Flat and Asymptotically Hyperbolic Manifolds*, arXiv:2502.18455v1 (25 February 2025). Its Proposition 2.1 and the proof of Theorem 4.3 establish the strict-width conclusion with the authors' weighted-C³ asymptotic convention. This is a literature finding, not a new solution or priority claim. A journal publication of this joint paper was not verified.

The original 2022 source uses less explicit asymptotic terminology. The cited 2022 preprint prints weaker derivative conditions than the 2025 paper. `PROOF.md` therefore supplies an explicit local-transplantation reduction rather than silently identifying these conditions. This reduction, including its use of the published preprint's local flow estimates, requires independent review before the broad original formulation is declared closed.

## Files

- `PROOF.md`: exact hypotheses, source-dependent affirmative argument, and checks of strictness and the Euclidean normalization
- `SOURCE_AUDIT.md`: original provenance, current primary literature, hypothesis comparison, and duplicate/prior-attempt checks
- `RESEARCH_LOG.md`: substantive attempt, checkpoint, outcome, and limits
- `verify_algebra.py`: small exact algebra checks; these do not verify geometric analysis
- `verification.json`: recorded execution of those checks

No numerical experiment is used to establish a geometric theorem. Source PDFs, raw catalogue data, prior-report corpora, and private operational records are excluded from this packet. AI tools were used extensively. These notes and the reduction are unrefereed.
