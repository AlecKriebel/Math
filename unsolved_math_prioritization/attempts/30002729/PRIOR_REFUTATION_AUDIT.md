# Ring loading: audit of a credited prior refutation

**Target:** the proposed universal additive bound `L <= L* + 11D/10` for finite undirected rings, where `L` and `L*` are the optimum unsplittable and splittable maximum edge loads and `D` is the maximum complete demand.

**Decision:** accepted as a **prior refutation**, with **zero new proof turns**. The construction is credited to Georgiev, Gómez-Serrano, Tao, and Wagner's AlphaEvolve work. The transfer from split-relative discrepancy to an optimum-value gap is credited to Däubel. This audit verifies the applicability of that prior result; it makes no new-discovery or sharp-constant claim.

**Review status and reliance:** AI-assisted and unrefereed. Acceptance here is a scoped mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. The complete transfer proof is supplied below. The finite witness and its exact computational verification remain external to this proof-only edition; the edition records the completed audit rather than distributing a self-contained computational certificate.

## Evidence and precise scope

Skutella states the target as Conjecture 1 in the [Oberwolfach report](https://doi.org/10.4171/owr/2014/51), printed page 2917. His preceding definitions specify the same two optima and the maximum full pair-demand.

Section 41 of [Mathematical exploration and discovery at scale](https://arxiv.org/abs/2511.02864) reports a 15-pair construction with discrepancy at least 1.119. The [pinned official notebook](https://github.com/google-deepmind/alphaevolve_repository_of_problems/blob/8f447457957deac61e28bf1676746f0753b3b2f8/experiments/ring_loading_problem/ring_loading_problem.ipynb) supplies the witness. The latest available arXiv version checked, v3, retains this claim in [Section 41](https://arxiv.org/html/2511.02864v3).

This discrepancy is relative to a particular split routing. It is not, by itself, a gap between optimum values. The necessary transfer is [Däubel, Lemma 7](https://arxiv.org/abs/1904.02119), PDF pages 15–16. The finite construction and proof below verify that transfer in precisely the case needed here.

The notebook's exhaustive routine uses floating-point arithmetic and omits the two endpoint cuts. The audit instead used exact decimal rationalization and integer arithmetic, checked all 32,768 binary choices with and without endpoint cuts, and independently checked actual edge loads. The exact minimum, divided by the actual maximum demand, is strictly greater than 1.119 and hence than 11/10. A tiny excess of a printed pair-total over one was handled by common rescaling by the actual maximum demand, not by a floating-point tolerance. The original routing has strictly positive split parts, and its required edge padding is less than twice its maximum demand.

## Discrepancy has the required ring interpretation

For `m` demands, use a `2m`-vertex ring and join vertex `i` to vertex `i+m`. Write the clockwise and counterclockwise split amounts as `u_i` and `v_i`, so the complete demand is `u_i+v_i` and `D=max_i(u_i+v_i)`.

An unsplit choice replaces the clockwise amount by either the entire demand or zero. Its change is therefore `z_i=v_i` or `z_i=-u_i`. If `S_k` is the sum of the first `k` changes and `T` their total, the edge-load changes along one semicircle are `2S_k-T`; antipodal edges have the opposite changes. Thus the largest increase on any edge is the maximum of `|2S_k-T|`, with the appropriate endpoint cuts included. A lower bound obtained from interior cuts remains valid when endpoint cuts are added.

Let `A` be the minimum such maximum increase. The exact source-witness audit establishes `A>1.119D`. This is the quantity that must survive the transfer.

## Finite demand-capped load equalization

Let `l_e` be the chosen split load on original edge `e`, `C=max_e l_e`, and `h_e=C-l_e`. Here `0<=h_e<2D` for every edge. Retain all original demands and replace each original edge by the following block:

1. For `h_e<=D`, use two consecutive edges and put a demand of size `h_e` on each edge's endpoints. Omit zero demands.
2. For `D<h_e<2D`, use four consecutive edges. Put two demands of size `D` on the endpoint pairs of the two two-edge halves. Also put a demand of size `h_e-D` on every adjacent pair.

The intended routing takes each new demand along its indicated local subpath. It adds exactly `h_e` to every edge in that block. All added demands are at most `D`; the original demands remain unchanged, so the new maximum demand is exactly `D`. Original demands have no endpoints inside a block. The resulting finite instance retains the permitted undirected-cycle and nonnegative pair-demand conventions, with distinct endpoint pairs for its nonzero demands.

The intended split routing has constant load `C` on every new edge.

## Normalizing every auxiliary routing

Consider two equal demands of size `q` whose intended paths are consecutive disjoint subpaths. Suppose all other demands contribute a common load `B` across their union.

- When both demands use their intended paths, no change is needed.
- When both use the complements, switching both to their intended paths leaves the internal contributions unchanged and reduces all outside contributions.
- When exactly one uses its complement, their internal contributions are `0` and `2q`. Switching it to its intended path changes both to `q`. The internal maximum decreases from `B+2q` to `B+q`, while outside contributions decrease.

Therefore the operation never increases the maximum load. It can increase an individual previously lighter edge. The stronger blanket componentwise claim in the source proof is unnecessary; the maximum-load statement is what its case analysis establishes and what the transfer requires.

In a two-edge block, apply this operation to the two local demands. In a four-edge block, first normalize the equal adjacent-demand pair in each half. All other contributions are constant within that half. The four adjacent demands then contribute the same amount throughout the whole block, so the equal pair of outer demands can be normalized as well. Demands belonging to other blocks have no endpoints inside the current block and contribute uniformly there. Consequently this bottom-up normalization applies to every global unsplit routing without increasing its maximum load.

Once all new demands are normalized, an original choice with maximum increase `a` has maximum load `C+a`. Thus the new unsplit optimum is `C+A`.

## Certifying the split optimum

Equal edge loads alone are not a sufficient optimality argument. A direct weighted-load certificate supplies the missing justification.

Assign weight 2 to every edge in a two-edge block and weight 1 to every edge in a four-edge block. Every original block has total weight 4. Both complementary paths of each original antipodal demand have the same weight. Every new demand's intended local path has weight 1 or 2, strictly smaller than its complement.

For any split routing, the weighted sum of edge loads is at least the sum, over all demands, of demand times its smaller path weight. The intended split routing attains this lower bound and has constant edge load `C`. Hence every routing has maximum edge load at least `C`, and the split optimum is exactly `C`.

Combining the two optima gives

`L-L*=A>1.119D>11D/10`.

This refutes the exact universal target. It does not determine the optimal additive constant.

## Verification extent

The explicit specialization has 84 vertices and 119 nonzero demands. Exact checks covered all 32,768 original choices in the discrepancy, original-ring-load, and expanded-ring-load formulations; the split weighted-load certificate; uniqueness of demand endpoint pairs; exact preservation of the maximum demand; and all 832 applicable local gadget orientation assignments. No floating-point optimizer or third-party solver was used as a proof certificate, and the source notebook was not executed.

The authors' notebook, source-derived demand data, enumeration programs, and raw computational outputs are not reproduced in this proof-only audit. The public source and its authentication metadata identify the witness being audited. Reproducing the finite witness check requires obtaining that public source and performing an independent exact verification; the reported checks cannot be rerun solely from this packet. The source retrieval, inspection, and version/status information in [VERIFICATION_METADATA.json](VERIFICATION_METADATA.json) records the earlier audit. Edition preparation makes no new source-retrieval, source-rehash, source-inspection, or literature-search claim.
