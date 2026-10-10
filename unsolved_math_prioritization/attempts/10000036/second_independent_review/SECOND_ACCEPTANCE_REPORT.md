# Separate acceptance report

Problem 10000036 / AMR-099-0036, rank 875. Date: 6 October 2026.

## Decision

**ACCEPT: the frozen author manuscript proves its stated mathematical theorem.** No correction patch is required. The second audit reached this assessment independently, without reading the first auditor's conclusions. The complete reasoning is in SECOND_ADVERSARIAL_AUDIT.md.

## Exact accepted result

For every fixed integer d >= 2, the nearest-neighbor lattice Z^d admits a bond-percolation law which:

1. is invariant under its full graph-automorphism group;
2. is mixing, and hence ergodic, under translations;
3. gives both states of every edge strictly positive conditional probability given all other output edge states;
4. has exactly one infinite component almost surely; and
5. has quenched internal Bernoulli bond critical probability one, both for the complete output graph and for its unique infinite component.

The internal Bernoulli site critical probability is also one. The energy condition is the ordinary, nonuniform positivity convention. No uniform finite-energy, finitary-coding, positive-association, or finite-dependence conclusion is accepted or inferred.

## Decisive checks

The connected one-ended spanning-tree input is supported in all dimensions by Timár's established factor-of-iid theorem. The perturbation is measurable and equivariant. Along every starting ray, finite-side sizes strictly increase; the total conditional probability of a deleted ray edge or inserted bypass is summable. Countable Borel-Cantelli gives genuine singleton boundaries in the final graph at every vertex. Those same deterministic boundaries force the quenched p^k thinning bound for every p<1. Retained coalescing tails give existence and uniqueness. Conditional expectation transfers strict finite energy from the hidden-tree kernel to the observable marginal.

The exact question and its finite-energy convention were checked against BHS Question 1.1, BT Question 1, and the archived Saint-Flour item 8.15. The original catalog does not explicitly require the manuscript's stronger all-dimensions formulation. The manuscript supplies it for d>=2.

## Provenance and limitations

Accepted input: INTERNAL_THRESHOLD_10000036_AUTHOR_SAFE_FREEZE.zip, 13,793 bytes, SHA-256 266debc377c66c6813e9db2b6abc704454ead9cdec47024f5d15338329b2fe05. Its external manifest and all six members were independently checked before use.

This acceptance certifies the written mathematical argument within its stated assumptions and scope. It does not certify novelty, priority, live catalog status, journal acceptance, or a proof-assistant derivation. Established tree-existence theorems remain cited external inputs. The credited earlier summable-flip method is a close antecedent; bounded literature searching did not settle whether an exact prior resolution exists. Three substantive approaches remain recorded; no additional construction was attempted in this review.

The author freeze is preserved unchanged. The separate acceptance report supersedes no historical bytes. No publication or external upload was carried out by this review.
