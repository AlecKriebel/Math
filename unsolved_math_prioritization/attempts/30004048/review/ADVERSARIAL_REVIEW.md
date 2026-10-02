# Independent AI-assisted full review: 30004048

## Verdict and precise conclusion

**PASS: complete negative answer to the exact source symmetry question, claimed_solved3/5.** No mandatory mathematical correction was found. This is an independent AI-assisted mathematical/source audit, not human peer review or historical-priority certification.

The proved assertion is

    |psi(13/27,14/27) − psi(14/27,13/27)| ≥ 1/108.

It concerns the universal biconstrained function on all finite simple graphs. The actual two values and their ordering are not computed. The two explicit162-vertex examples supply upper bounds only; their unequal bounds are not themselves the counterexample proof.

## Frozen binding and reproducibility

The complete30-file author packet at [commit06726651](https://github.com/AlecKriebel/Math/tree/067266518aca8b427edd926a68a311e538ad45dd/unsolved_math_prioritization/attempts/30004048) is bound by FINAL_AUTHOR_MANIFEST.json, SHA256 `15fb5403c1d0aebc44bc406c5d0f20c0ca0a303e61423418abb918d19a8e7243`. TURN_3.md has SHA256 `cf1c7a7078a8bc29ef775fe0bf9298fe052017e25b1da363c1dd20643b1ff3b4`.

All30 raw Git blob hashes and lengths match the frozen local files. All88 nested artifact entries and three source PDF bindings verify. All three author checkers were read and replayed:29,175 +12,749 +1,831 =43,755 assertions, complete stdout byte-exact. The independent standard-library verifier passes2,552 separate assertions. Its small census includes108 nonfull boundary cases with repeated C-neighborhoods and extra A vertices, as well as both explicit ordinary blow-ups and all16 possible integer-gap comparisons. Finite controls supplement the universal proof; they do not substitute for it.

## Source audit

Seymour's complete contribution in [OWR1/2019](https://ems.press/content/serial-article-files/46780), printed46–47, was read; printed47 was visually checked. It adds the B→A and C→B constraints to the preceding A→B and B→C requirements and asks symmetry of the resulting universal function. The [publisher](https://ems.press/journals/owr/articles/16763) identifies the volume year2019 and publication27February2020.

The detailed [published2022 paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/) by Chudnovsky, Hompe, Scott, Seymour and Spirkl explicitly uses finite simple graphs and distinct reachable vertices. Its definitions, symmetry discussion onp10, Figure1 onp6, and regularity discussion onp71 were checked. Figure1 was visually transcribed independently. The seed matrix, weights and complement agree exactly with the packet. The seven-type regular matrix is credited prior work, not an original construction here.

The source's proved symmetry is for phi; it explicitly leaves the analogous psi assertion unproved. The published minimal-value and diagonal results are different statements and do not supply or contradict the present rational-boundary argument. No invocation of an omitted proof of Theorem12.2 is required. Removing nonconsecutive edges and irrelevant vertices justifies the canonical tripartite formulation without strengthening the universal lower-bound problem; tripartite examples suffice for upper bounds.

## Turn1 audit

For a finite admissible graph, the two actual minimum bidirectional degree fractions are rational and dominate the requested parameters. This proves the cofinal rational-infimum formula in both directions using monotonicity and a near-minimizer, without assuming attainment or continuity. The asymmetric-real-pair reduction preserves the direction of both inequalities after swapping the rational coordinates.

The sampling lemma conditions separately on each sampled endpoint. All4n degree events and2n original-reach-set domination events have the stated Bernoulli bound. Repeated vertices become distinct twins, so no multigraph is introduced. Independence across these6n events is unnecessary for the union bound. The elementary exponential-moment argument and ceiling estimate give a failure probability strictly below1. The finite optimization sandwich retains degree slack; it does not remove it at rational jumps. The proposed finite asymmetry certificate requires a reversed global finite-table lower bound, not a sample graph's upper bound. All these scope distinctions are mathematically correct.

## Turn2 audit

The three feasibility polytopes encode all four constraints, including the two conditions on the middle weight vector. The Boolean reach matrix is kept fixed only for a retained incidence pattern. Positive feasible points can be mixed with optimizers; for rational parameters, rational affine solutions and rational near-optima preserve strictly positive support. Ordinary blow-ups then preserve reachability because every middle type remains present. Zero-weight deletion is not treated as an innocuous operation.

Both dual inequalities have the correct sign and orientation. The displayed family has forward optimum1/2 and reverse fixed-pattern optimum2y; feasible weights and matching elementary lower certificates establish both. The120-vertex instance and the support-deletion repair check. The universal values at these parameters are both1/2 by the credited lower bound and the two-component construction. Thus the packet correctly records a method obstruction, not an earlier counterexample.

## Turn3: universal boundary formula

For rational theta in(0,1), the finite-template class is nonempty by cyclic incidence matrices. The unweighted maximum row degree is a positive integer, so its minimum is genuinely attained by a finite positive rational template. This uses well-ordering, not extremal attainment of psi. Positive real feasible weights can be approximated inside their rational affine solution spaces while retaining strict positivity; this observation is also valid as stated.

For an arbitrary finite boundary graph, F=1 is handled separately. If F<1, each C vertex misses at least one A vertex. Their disjoint B-neighborhoods have lower size bounds summing to|B|, so both bounds are exact. This forces every C neighborhood to have the same exact size. Summing edges and using every B→C lower bound then forces exact regularity in the other direction too. This is a universal conclusion for every admissible graph in the nonfull case.

Identical C neighborhoods are grouped with their positive rational class weights. Rows may repeat; they are not discarded. The missed A set for each distinct C type is exactly the class whose neighborhood is its complement. These missed classes are nonempty and pairwise disjoint. Any A vertices outside their union remain in the graph and can only strengthen the bound on nonneighbors of a B vertex. Thus t times the maximum distinct-column incidence degree is at most theta, giving the universal lower bound1−theta/d(theta).

For the upper bound, equal positive b-weight and distinct columns imply incomparable column supports. This is essential: no positive row can hide a strict inclusion at equal weight. Setting every special A weight to theta/d and adding the universal residual weight gives nonnegative residual mass because the b-average row degree equals n theta and is at most d. If the residual is zero, that vertex is omitted. Every retained weight is strictly positive and rational. All four constraints hold; each C type misses exactly its own special A type and reaches all the others. The rational blow-up preserves all degrees and two-step reach sets, proving the matching upper bound with an ordinary finite graph. Therefore

    psi(1−theta,theta)=1−theta/d(theta)

holds exactly, and rational-boundary attainment is a conclusion rather than an assumption. The irrational-boundary observation is also correct but is not needed for the asymmetric pair.

## Matrix and final gap

The transcribed7×7 matrix with b=(5,5,3,3,3,4,4)/27 and q=(4,4,3,3,3,5,5)/27 has both weighted degrees13/27, distinct columns, and maximum unweighted row degree4. Its complement has both weighted degrees14/27 and maximum row degree4. Consequently the two invariant minima are positive integers at most4, regardless of whether either displayed matrix minimizes them.

Equality of the two universal values would require13e=14d, impossible for integers1≤d,e≤4. The exact16-case gap check agrees with the analytic argument: the minimum permitted absolute difference is1/108. The denominator bound used for unequal d,e is valid because de≤12 in that case. No value or ordering of d,e, and hence of the two psi values, is inferred.

The two162-vertex blow-ups satisfy the four directed degree requirements and give reach counts95 and94 out of108. These remain explicitly upper bounds95/108 and47/54. The universal quantization formula, not their inequality, establishes the negative answer.

## Disposition and limits

All three turns pass in their stated scopes, with no frozen-file revision required. The complete exact original symmetry question has a negative answer. Credit the earlier source matrix and elementary prior framework, retain real-parameter/finite-graph scope, and do not claim computed psi values, a specific order of them, or novelty. No source PDFs, private material or large generated artifacts are needed in the public review packet.
