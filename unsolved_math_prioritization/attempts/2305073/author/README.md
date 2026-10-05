# Function Theory 5.73: five approaches and partial results

Target: 2305073 / AMR-022-5073, ranked campaign position 682.

**Disposition: unresolved after five substantive approaches.** This packet does not claim a complete characterization, a new solution, or novelty. It has not yet received the fresh independent audit required before remote publication.

The governing question is Korenblum's problem in Hayman and Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, printed p.111. For a fixed `0 < alpha < 1`, the kernel is exactly `|x-t|^(-alpha)` on the real line, with no normalization constant. The dominating measure must be a finite positive Borel measure. The question's domination is read pointwise: the adjacent Problem 5.74 explicitly says almost everywhere, while 5.73 does not.

## Established here

1. An exact smooth-test dual characterization, including attainment of the least mass, for **Lebesgue-almost-everywhere** domination. It also gives pointwise domination when the obstacle is lower semicontinuous.
2. Two equimeasurable, finite-valued, nonnegative Borel functions in weak `L^(1/alpha)` and `L^1`: one has a one-atom majorant, and the other has no finite-measure majorant, even almost everywhere. Thus rearrangement data alone cannot characterize this class.
3. A finite-valued Borel function supported on a compact Lebesgue-null Cantor set with no pointwise finite-measure majorant. This demonstrates that the almost-everywhere theorem is insufficient for the original measurable pointwise problem.
4. An explicit interval-cover sufficient condition, together with a majorizable function showing that condition is not necessary.
5. Arbitrarily small-mass repair on countable sets, and the consequent failure of finite-point/dense-countable-sample feasibility as a general characterization.

The remaining gap is a sufficient intrinsic criterion for arbitrary measurable pointwise obstacles, including singular exceptional sets. The all-bounded-potential-measure test is proved necessary only. Neither a capacitary duality theorem nor a polar-set repair theorem is assumed without proof.

## Files

- `PARTIAL_RESULTS.md`: self-contained proofs of the results and exact scope.
- `APPROACH_LOG.md`: five distinct approaches, their actual deductions, and why none settles the original problem.
- `SOURCE_VERIFICATION.json`: public source identity, inspection scope, live queue and bounded repository duplicate checks.
- `verify_controls.py`: portable exact-arithmetic algebraic, combinatorial, and scope controls.
- `CONTROL_RESULTS.json`: frozen deterministic output of those controls.
- `AUTHOR_MANIFEST.json`: byte sizes and SHA-256 hashes of the frozen authored packet.

Run `python3 verify_controls.py --check-manifest` from this directory. The 11,515 exact finite checks passed and their default output was reproduced byte-for-byte. The checks do not verify the infinite-dimensional separation argument or replace mathematical review. No source PDF, extracted source text, dataset corpus, or private coordination material belongs in this authored packet.

Primary source: https://arxiv.org/abs/1809.07200v2

