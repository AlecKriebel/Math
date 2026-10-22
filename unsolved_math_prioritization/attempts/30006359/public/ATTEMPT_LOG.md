# Five-approach research log

Problem 30006359, 2026-10-04 UTC. These are substantive mathematical approaches within one investigation, not claims that five user conversations occurred. The general target remains unresolved. Progress percentages are rough subjective estimates toward the original all-rank research goal, not probabilities of correctness and not percentages of ranks covered.

## 1. Incidence-matrix mechanism

Checkpoint: 06:24 UTC. Estimated progress: 5%.

Mechanism: replace exchange-coefficient identities on each fixed nonzero support by a bipartite vertex-to-edge incidence map. Compute its exact kernel and rank, and construct edge delta vectors by signed tree cuts.

Result: a full proof of the forest criterion at the incidence-equation stage, together with the componentwise coefficient freedom. This recovers the source's mechanism and explains why a canonical representative is needed. It does not show irreducibility after imposing higher consistency equations. The attempted inference that the kernel supplies a free factor of the full variety was rejected because the other equations can restrict it.

Artifact: RESULT.md, Lemma 1.

## 2. Degeneration and counterexample stress test

Checkpoint: 06:26 UTC. Estimated progress: 7%.

Mechanism: search for a smallest-rank contradiction by allowing a nonzero fusion edge to vanish in a family. Compute both rank-two supports exactly and compare their closures with their actual support loci and canonical exchange coefficients.

Result: the large-support chart is the line minus two points, and the group-like point is a boundary in dimension/convolution coordinates. This defeats an overly literal identification of exact support strata with closed components. It does not refute the intended conjecture because the canonical A,B coordinates and the ambient variety have to be specified. The tempting target counterexample was explicitly rejected.

Artifact: RESULT.md, Proposition 2.

## 3. Localized ideals and unit-division elimination

Checkpoint: 06:30 UTC. Estimated progress: 10%.

Mechanism: replace graph-support constraints by saturation, identify the correct radical-prime criterion, and design an exact elimination step that divides only by required nonzero linear forms. Examine whether forest sparsity alone forces all residual quadratics to be removable.

Result: a rigorous saturation/closure criterion and a sound conditional affine-chart certificate procedure. The general induction stalls at potentially nonlinear residual equations; the elementary system uv=0 on D(u+v) illustrates the logical gap but is not a target counterexample. No unsupported claim that many low-degree equations imply primeness survives.

Artifact: RESULT.md, Lemma 3 and the localized-elimination proof; verify.py.

## 4. All-rank permutation-support rigidity

Checkpoint: 06:34 UTC. Estimated progress: 12%.

Mechanism: take the extremal class in which every fusion graph is a perfect matching. Use associativity of singleton supports to recover a group law, then use inverse products, trace equations and nonzero dimensions to eliminate every parameter.

Result: any nonempty normalized chart of this kind is one reduced point, with all dimensions and nonzero coefficients equal to one. This gives a complete argument for a general class of supports, while crediting known finite-group examples. The proof does not extend to branching forests.

Artifact: RESULT.md, Proposition 4.

## 5. Exhaustive exact small-rank algebra

Checkpoint: final packet preparation, 06:42 UTC. Estimated progress: 15%.

Mechanism: enumerate every reciprocity support and duality type through rank four, build the actual canonical coefficients and consistency polynomials, and run exact affine elimination with division only by declared nonzero forms. Initial Gröbner-basis exploration was used locally as a cross-check; the final public certificate does not depend on a Gröbner-basis oracle. It includes both comparisons obtained from the three W-expansions in the source proof.

Result: all 426 forest patterns are decided; 91 nonempty labelled charts have affine-linear saturated ideals. Quotienting only by permitted label permutations yields the source's 7 rank-three and 24 rank-four algebraic types. The rank-three nonpositive point has dimension sum −1. An explicit hand-checkable rank-three table supplements the exhaustive finite certificate. Source-reported counts are not claimed as novel.

Artifact: RESULT.md, Proposition 5; verify.py; verification.json; verification_summary.json. The exact final receipt must replay byte-for-byte before the author packet is frozen.

## Stopping condition and disposition

Five substantive approaches have produced rigorously scoped partials and exact bounded computations. No proof of the all-rank primeness assertion, no proof identifying components in every intended ambient convention, and no genuine target counterexample has been established. The honest queue recommendation is `unsolved`, `5/5`, changing only this target's Status and Turns cells. The target is not marked exhausted, and no queue utility or other row is changed.

No remote changes or third-party communications occurred. A fresh independent reviewer must assess the frozen packet before any proposed draft pull request.
