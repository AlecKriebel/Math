# Computation/combinatorics follow-on triage, batch 2

Checkpoint: 2026-10-06 America/Los_Angeles. Triage estimate 95%; no upstream theorem verified. Separate from the first ten, including their optional bundled targets.

## A. Binary-weight nonnegative hafnian FPRAS — recommend, impact 8.2

**Precise claim.** A uniform FPRAS for the hafnian of every even-order symmetric nonnegative rational matrix, with arbitrary zero support and entries in binary. Exact detection of zero; runtime polynomial in full encoded input length, inverse relative accuracy and log inverse failure probability. Include total-variation approximate sampling from the weighted perfect-matching law. Weighted prescribed-degree factors may be bundled after checking the exact Tutte reduction.

**New input.** Family 113, `A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex`, main theorem around line 132. The existing applications explicitly exclude weights and compressed multiplicities at lines 3126–3127. Corpus searches found only approximate weighted hafnian background, not this new FPRAS.

**Previously unresolved gate now has explicit mechanism.** For integer W≥1, build a directed acyclic graph D with distinct source s and terminal t and exactly W directed s–t paths. Begin with s→t for W=1. Read each subsequent binary digit b. Add fresh a,z and arcs t→z, t→a, a→z; add s→z iff b=1; replace t by z. Path count is 2W+b, and the DAG has 2+2 floor(log2 W) vertices. Split every internal vertex i into L_i,R_i with identity edge L_i–R_i. Keep only L_s and R_t as terminals. Each directed arc i→j becomes undirected edge L_i–R_j. This is a simple bipartite graph. A perfect matching of the full gadget corresponds to exactly one s–t path plus identity edges off the path; a matching with both terminals removed consists uniquely of all identity edges, since DAG cycles are impossible. A gadget with only one terminal removed has odd order. Thus its signature (both present, neither, first only, second only) is (W,1,0,0), with 2+4 floor(log2 W) vertices.

Replace each edge uv of the original graph by its gadget, identifying terminals with u,v, orienting each original edge arbitrarily. Parity forces either both endpoints or neither to be used inside each gadget. Global matching counts therefore equal the weighted hafnian exactly. For rational weights clear denominators using their product D (polynomial bit length); dividing the result by D^(n/2) preserves relative error. No numeric-multiplicity blowup occurs.

**Sanity check.** Exact recursive perfect-matching enumeration for W=1,...,64 returned signature (W,1,0,0) throughout; largest gadget had 26 vertices. This checks finite examples, not an upstream FPRAS.

**Research work remaining.** Write the short bijection rigorously, total input-size and bit bounds, robust self-reduction sampler and exact-zero branch. Publish as a precisely attributed consequence/application package, not as a new matching-chain mechanism. Very high tractability; high simultaneous-discovery risk.

**Primary comparison.** Rudelson–Samorodnitsky–Zeitouni, https://arxiv.org/abs/1409.3905, subexponential-error estimator under structural conditions; Barvinok, https://arxiv.org/abs/1601.07518, restricted-matrix hafnian approximation. Do not imply unrestricted complex Gaussian-boson sampling becomes easy.

## B. Exponential SDP extension complexity of traveling-salesman polytopes — recommend, impact 8.3

**Precise claim.** For the symmetric TSP polytope on N cities, every exact real positive-semidefinite extended formulation has matrix dimension 2^{Omega(N)}. With the standard dynamic-programming extended formulation upper bound, its exact SDP extension complexity is 2^{Theta(N)}. Bundle a lower bound 2^{Omega(sqrt M)} for stable-set polytopes of explicit M-vertex line graphs, if worthwhile.

**New input.** Family 126, `Exponential-PSD-rank-of-positively-shifted-matching-matrices-October-5-2026/build/source/sections/introduction.tex`: exponential PSD lift size for perfect matching. Targeted whole-corpus searches found no TSP-PSD corollary; the manuscript discusses matching and its shifted slack matrices.

**Bridge.** Yannakakis's classical reduction makes the perfect-matching polytope on n vertices a linear projection of a face of a TSP polytope on O(n) vertices. Rothvoss https://arxiv.org/pdf/1311.2369, pp.3–4, states this exact linear-size reduction explicitly immediately before Corollary 2. PSD lift size, just like LP extension complexity, cannot increase under taking a face then a linear image: lift the face by an affine equality and compose the projection. This transfers 2^{Omega(n)} without an exponent loss.

For stable sets, the matching polytope of K_n is precisely the stable-set polytope of its line graph; perfect matchings form the maximum-cardinality face. M=binom(n,2), so the guaranteed lower exponent is sqrt M, not M.

**Prior literature.** Lee–Raghavendra–Steurer https://arxiv.org/abs/1411.6317 gives 2^{N^c} lower bounds for TSP and related explicit polytopes, with c<1. This candidate strengthens the exponent to linear in city count. Targeted current searches did not locate an intervening full-exponential exact SDP bound, but a publication-priority audit is mandatory.

**Remaining work / limits.** Reproduce the linear-size face projection, prove monotonicity with correct PSD-size conventions, cite a 2^{O(N)} DP lift for matching upper order if claiming Theta. No approximation-factor hardness follows automatically. The shifted matching bound might yield robust TSP relaxations but that requires a separate affine-slack calculation and is not part of the safe target. Very high tractability; limited independent technique.

## C. Smooth pure Lebesgue spectrum of every finite multiplicity — lower-priority alternative, impact 7.5–8

**Precise claim.** For every positive integer m, a C-infinity standard-volume-preserving diffeomorphism of T^3 has homogeneous Lebesgue spectrum of multiplicity exactly m on its entire mean-zero L2 space. It has zero entropy and all Lyapunov exponents zero; all-order mixing follows from family 145 or the already stated dynamical profile.

**Mechanism.** If T is the simple-Lebesgue transformation from 144, take T^m. Under its spectral representation U_T=M_z, U_(T^m)=M_(z^m), unitarily equivalent to m copies of M_z. Equivalently partition the orthonormal orbit basis by residues modulo m. No new smooth construction is necessary.

**Nonduplication and priority.** The source's `sections/06-consequences.tex` contains mixing, entropy and Lyapunov conclusions but no prescribed multiplicity theorem. The general homogeneous *singular* spectrum realization problem has extensive prior solutions; do not confuse it with pure Lebesgue spectrum. Ageev's primary article https://www.mathnet.ru/links/d7626fabc9605959725c2ecc301307a7/sm1743_eng.pdf discusses finite even Lebesgue *components* and explicitly asks whether the entire complement of constants can have finite Lebesgue multiplicity. The distinction matters. The result is mathematically meaningful but so immediate from the new Banach solution that a standalone paper may be thin; reserve behind A and B unless packaged with a genuinely useful realization theorem.

## Other exclusions checked

- Simple stochastic reachability quasipolynomial algorithms already appear explicitly in #104's October5 stochastic introduction; reject as duplicate.
- Positive equilibria for weakly reversible mass action are already proved by Boros (2019), https://arxiv.org/abs/1710.04732; reject.
- Arbitrary time-dependent reaction rates need a uniform trapping-region argument absent from fixed-rate permanence; not automatic.
- Conjectural matroid-secretary consequences of the one-sample prophet theorem are not established: per-item independent samples do not automatically transfer to secretary random ordering.
- General/parabolic Kazhdan–Lusztig claims require marked-interval scope; no unmarked-poset upgrade assumed.
