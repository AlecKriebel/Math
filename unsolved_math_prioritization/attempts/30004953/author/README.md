# 30004953: negative-p Aleksandrov concentration

OWR-8415364-011; rank 785. Five substantive approaches completed on 5 October 2026.

## Result and status

**Original full target unresolved. Candidate scoped theorems, not independently audited yet.**

The separately identified planar endpoint p = -1 has candidate sharp threshold pi/(pi+2), approximately 0.611015. Every even finite nonzero measure with all antipodal-pair mass ratios strictly below this number has an origin-symmetric solution. An explicit four-atom measure at equality has no solution, even among nonsymmetric bodies. Thus the supremum for a condition of the form ratio <= c is pi/(pi+2), but that endpoint is not admissible with <=. This would improve the cited planar bound of 1/2.

An all-dimensional p=-1 theorem gives existence under nonconcentration in proper subspaces and line masses below

    1 / [1 + 2 Gamma(n/2)/(sqrt(pi) Gamma((n-1)/2))].

Other proved claims are a compactified variational argument, exclusion of collapse dimensions k > -p, exact two-pair constructions for p < -1, and a concrete solution that is not a maximizing critical point. The optimal all-dimensional p<-1 bound and higher-dimensional p=-1 sharpness remain open in this packet.

Read [PROOFS.md](PROOFS.md) for the full arguments, including the distinction between an actual solution and a global maximizer. [RESEARCH_LOG.md](RESEARCH_LOG.md) records the five approaches and their stopping points. [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) and [PRIOR_WORK_CHECK.json](PRIOR_WORK_CHECK.json) identify the source and search limits.

## Source and attribution limits

The official OWR pages and the 2022 Mui article were inspected. The imported question omits evenness; this packet restores the primary hypotheses. A 2025 primary survey and a March 2026 publisher abstract were checked. The latter already announces p=-1 nonexistence and p<-1 nonuniqueness examples; its full text was unavailable in the inspected route, so overlap with examples here is unresolved. No novelty, priority, human verification, or editorial acceptance is claimed. A separate 2026 bibliographic lead could not be authenticated and is not relied on.

The mathematical argument here is written out, including the first-variation calculation. Standard foundational inputs are Blaschke selection, almost-everywhere differentiability of Lipschitz support functions, basic measure convergence, and beta/gamma identities. Numerical controls do not establish the continuous theorems.

## Reproduction

Requires Python 3 and mpmath 1.3.0 for mathematical controls:

    python3 verify_math.py
    python3 verify_manifest.py

The first replays finite high-precision controls and compares the deterministic saved result. The second verifies the exact frozen authored file set, byte lengths, and SHA-256 hashes using the standard library. Neither labels the full problem solved. Default replay is read-only. Running Python with -O does not disable checks.

Only authored mathematics/code/results and public source/repository verification metadata are included. Third-party PDFs, excerpts, images, raw datasets, and private coordination are excluded. No remote writes were performed by this investigation.
