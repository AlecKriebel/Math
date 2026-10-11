# Acceptance of the fixed-rank-block criterion

## Decision

Accept the restricted result without a substantive proof correction. The publication edition retains the complete general proofs of the fixed-rank complement reduction, the canonical indexed-incidence minimality statement, the tight-face minor extension, the polynomial maximal-tight-chain construction, and the KLS upper-only rounding lemma. The exact equality-case dependence and negative-cost invariant are retained.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

## Precise accepted guarantee

For explicit indexed degree sets of element incidence Δ, integer-normalized bounds, and a fixed-rank partition of block incidence κ, one basis simultaneously satisfies lower bounds minus κ−1 and upper bounds plus κ−1, with cost at most L. Here L is the degree-constrained basis-LP optimum after taking ceilings of lower bounds and floors of upper bounds. When κ≤Δ, the requested additive Δ−1 follows for that restricted class. The unpruned indexed system has κ≥Δ, so this test is equality there.

Canonical components minimize incidence only among the stated fixed-cardinality anchor-complement reductions retaining every original indexed upper row. The claim excludes pruning, duplicate merging, linear combinations, changing the matroid, restricting the face, and other algorithms.

A specified rational feasible point and a rank-tight chain yield a direct sum of successive matroid minors. The same reduction on that face returns a basis of the original matroid costing at most the supplied point. For an optimal point satisfying the face criterion, cost is at most L≤OPT, assuming original integral feasibility. The face lemma itself requires only LP feasibility. A maximal tight chain for the specified point is found through the tight-set implication preorder. No search guarantee over all optimal points is asserted.

The cited KLS upper-only rounding argument is established prior work and is reproduced completely for the needed LP-feasibility and initial-LP-cost guarantee. Finite rational costs may be negative. Polynomial-time submodular minimization and rational LP optimization/separation are standard accepted oracle dependencies; they are not re-proved or implemented here.

## Evidence and distribution boundary

The complete general mathematical proofs are retained, conditional on standard polynomial-time submodular-minimization and rational-LP oracle tools as accepted dependencies. Those tools are neither re-proved nor implemented here. This is not a computational reproduction package: executable code, raw certificates, numerical instance definitions, explicit finite witnesses and basis lists, matrices, and tables are omitted. The finite examples are separately checked supporting evidence; their omitted inputs cannot be recovered from this edition alone and are not premises of the general theorems.

The historical audit independently reconstructed the graphic and KLS examples and tested normalization, LP-only feasibility, negative costs, equality dependence, and boundary coordinates. Normal, -O, and -OO checks passed, including 36 negative and 6 positive controls. Omitted exemplars are not self-contained in this edition. The KLS stalled vertex does not refute the target; its checked relaxed-basis decomposition instead gives cost-preserving existence relative to that point for every linear objective.

The edition introduces no theorem change. Editorial changes remove finite witness inputs and private material, clarify the LP benchmark, delimit historical evidence, and state review status. Exact source identities and edition bindings appear in ACCEPTANCE.json; public-source provenance is in SOURCES.json. No source body, code, raw certificate, or private coordination material is distributed.

## Remaining question

The unrestricted simultaneous additive Δ−1 guarantee remains unresolved by this work when the relevant component-incidence criterion fails. No novelty, priority, or exhaustive current-literature-status claim is made.
