# 30001893: dimension of convex partition spaces

**Partial, 5/5 approaches. The full source question is not solved.**

The primary OWR question asks for the maximal dimension of the realization spaces of partitions of R^3 into n>3 convex pieces. Its printed regular-family count 4n-1 differs from the inspected 2015 Leon-Ziegler theorem, which gives 4n-5 and conjectures that this is also the dimension of the full space. These statements are kept separate.

Read `PROOF.md` for complete retained proofs, scope, and exact obstructions. The strongest global interval retained here is

    4n-5 <= dim C(R^3,n) <= 3*binomial(n,2), n>=4.

Five routes:

1. Supporting-plane coordinates give the rigorous global quadratic upper bound.
2. Affine-function gauges and exact fiber propagation recover the prior 4n-5 regular-family theorem.
3. Spherical graphs give the exact dimensions 4n-8 and 4n-5 for pointed central fans with fixed and moving apex, respectively.
4. Cylindrical partitions yield a 4n-5-dimensional family, with explicit nonregular examples.
5. A five-region incidence calculation has 20 variables and six written equations but Jacobian rank five. Its local dimension is 15, disproving the independent-equation count 14 for that example.

The remaining issue is an upper bound for every arbitrary affine realization stratum. No new full solution, novelty, or global current-openness claim is made.

## Replay

From this directory:

    python3 -B verify.py --selftest
    python3 -O -B verify.py --selftest
    python3 -B verify.py --selftest --verify-freeze
    python3 -O -B verify.py --selftest --verify-freeze

The verifier uses only the Python standard library and exact rational arithmetic. `EXACT_RESULTS.json` is the retained scientific/control output without the optional freeze checks; rerunning that command with ordinary and optimized Python gives identical output. The optional freeze test validates all payload bytes and rejects eight additional file/manifest corruptions. No floating-point rank estimate is used. These tests supplement the proofs; they do not certify the universal conjecture.

## Source and history limits

`SOURCE_VERIFICATION.json` and `RESEARCH_LOG.md` identify retrieved primary sources, their byte counts and hashes, inspected locations, unsuccessful exact-page retrievals, and bounded literature/prior-attempt searches. The 2015 arXiv preprint and thesis were inspected. The 2018 chapter is bibliographically verified only. The exact live UnsolvedMath page and raw upstream AI corpora remain uninspected. No exact prior repository attempt was found in the bounded searches; this is not exhaustive semantic-history coverage.

`MANIFEST.json` freezes only authored mathematics, code, status, logs, and verification metadata. It excludes all source PDFs, source text extraction, screenshots, raw catalog records, and private coordination. This package has not been remotely written or published and awaits a fresh independent audit.
