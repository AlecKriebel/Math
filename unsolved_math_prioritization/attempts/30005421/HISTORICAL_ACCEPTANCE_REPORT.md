# Prior-result verification: ACCEPT

Target: **30005421 / OWR-12697690-001**, uniform expansion stability for wild quivers.

The original question is answered affirmatively by **Markus Reineke**, *Expander representations of quivers*, Theorem 2.4, [Forum of Mathematics, Sigma 14 (2026), e132](https://doi.org/10.1017/fms.2026.10284). Publication was verified on the publisher's website and in its PDF. The result is prior work, not a new solution by this project.

## What was established

The original [Oberwolfach Report 7/2023](https://ems.press/content/serial-article-files/47001), printed pp.405–406, and the full relevant forward proof in the [author's v2 paper](https://arxiv.org/abs/2411.15609v2) and published article were inspected.

- **Field:** the same algebraically closed field throughout; no characteristic restriction was introduced.
- **Quiver:** finite and acyclic; wildness is the usual path-algebra/underlying-graph condition. Disconnected quivers reduce to a wild connected component by zero extension.
- **Slope:** one fixed rational slope with an everywhere-positive denominator. Integral coefficients are obtained by choosing an integral dimension vector near the positive Perron eigenvector.
- **Uniformity:** a single representation sequence works for every cutoff. The positive gap depends only on the fixed quiver/slope and the cutoff, not on sequence index or subrepresentation.
- **Growth:** dimensions are exactly positive integer multiples of a fixed nonzero dimension vector, hence tend to infinity.
- **Expansion/stability:** the exact subrepresentation inequality is proved. A factor of one-half in the chosen gap accommodates both the original weak inequality and the published strict inequality.
- **Completeness:** the source question asks for the existence direction, which is fully reconstructed in PROOF_APPLICATION.md. The converse is not needed and is not independently audited here.

## Presentation details checked explicitly

The verification does not merely quote the theorem statement.

1. The restricted Rayleigh *minimum*, rather than every Rayleigh quotient, approaches the second Cartan eigenvalue. This supplies a lower bound uniform over all relevant subrepresentations.
2. The weighted coordinate-square estimate uses a linear term whose sum is zero. The sign variation in the displayed source calculation therefore does not affect the conclusion; the derivation in this packet uses the direct coordinate inequality consistently.
3. For each dimension vector, all negative-Euler subrepresentation loci are excluded in one finite operation. This makes the family independent of the cutoff and avoids an unjustified interchange of family/cutoff quantifiers.
4. The proved weak bound is converted into a strict positive gap by shrinking the constant. Claims about an attained largest strict expansion coefficient are unnecessary.

These details close the proof application's bookkeeping and inequality conventions. No unresolved bridge remains for the stated target. No extension to nonclosed fields, cyclic quivers, arbitrary prescribed stability conditions, or explicit expanders is claimed.

## Exact supporting tests

Run: python verification_test.py > TEST_RESULTS.json

The tests use integer/rational arithmetic and exact symbolic positive-definiteness certificates. They check the weighted-box bound, Euler/skew identity, incidence-dimension identity, scale normalization, and strict-gap choice:

- Three-arrow Kronecker quiver: scales 1 through 16; 1,784 dimension vectors enumerated; 698 eligible nonzero proper vectors; 3,171 strict-cutoff checks.
- Four-vertex acyclic chain with arrow multiplicities 3, 1, 3: scales 1 through 8; 15,332 vectors enumerated; 881 eligible vectors; 3,979 strict-cutoff checks. This exercises the branch with a negative restricted Rayleigh lower bound.
- Combined: **17,116 enumerated vectors, 17,068 weighted-box checks, 1,579 eligible vectors, and 7,150 strict-cutoff checks; all passed.**

These finite tests are supporting checks. The universal conclusion follows from the written proof, not enumeration.

## Publication and attribution boundary

This authored packet contains the proof application, this verification report, a reproducible checking script, its results, and public bibliographic/hash metadata. Third-party PDFs, extracted source text, dataset records, and private coordination material are excluded.

Recommended mathematical disposition: **already solved by prior published result**. This verification uses **zero substantive new proof-search turns** and makes **no novelty claim**.
