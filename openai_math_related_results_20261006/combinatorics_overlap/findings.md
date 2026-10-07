# Combinatorics, finite geometry, probability, and reaction-network comparison

Snapshot: OpenAI `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (372 families, 722 manuscripts); our `sources/open_prs.json` (781 open PRs, 780 drafts). Authoritative comparison inputs are the family map, selected complete OpenAI PDFs, selected current local project README files, and pinned draft bodies/proofs. Full source PDFs/extractions are local comparison inputs under `sources/`, not authored findings for publication. All actions were read-only with respect to the external services; no individual was contacted.

“Claims” below describe manuscript statements. The comparison checks the relation between statements, not the correctness of the full new OpenAI proofs. No result is promoted as independently established on the strength of this matching exercise.

## Strongest actionable match: a concrete new partial consequence

### 1. Family 090 → our draft #487: the dimension-two triangle-program equality

- OpenAI paper: [A sharp Fourier certificate for planar circle packing](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/paper.pdf), Theorem 1.1, PDF p.3.
- Our draft: [#487, Partial: AIM lattice three-point bound, symmetry and restriction obstructions (20001754)](https://github.com/AlecKriebel/Math/pull/487), head `d33ec2f43aa7c59519f0b004202b8cd653ce4fd8`, `unsolved_math_prioritization/attempts/20001754/public/PROOF.md`, §§1,3.
- Exact relation: their claimed real radial Schwartz auxiliary function has `fhat(0)=1`, `f(0)=2/√3`, `fhat≥0`, and `f≤0` for distances at least one. These match our raw `L_n` convention exactly. Combined with the lattice Poisson lower bound and the product-program inequality already in our draft, it gives `P(C_△)=4/3` and `sqrt(P(C_△))=L_2=2/√3`. Our draft currently records this equality only in sharp dimensions 1,8,24, so this would add dimension two.
- Scope: a direct advance on a subcase of our exact question, conditional on validation of the OpenAI theorem. It does not resolve general-dimensional equality or the universal optimizer conversion.
- Checkable derivation: `planar_triangle_bound_derivation.md`. The new interval/analytic certificate itself has not been replayed or independently reconstructed.

## Material neighboring work

### 2. Family 149 → our stochastic bimolecular positive-recurrence theorem

- OpenAI: [Uniform Permanence in Weakly Reversible Mass-Action Systems](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/permanence.pdf), Theorem 1.1, PDF p.2. Companion [Boundedness and persistence of weakly reversible mass-action systems](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Boundedness-and-persistence-of-weakly-reversible-mass-action-systems-September-25-2026/paper.pdf).
- Our canonical local release candidate: `/Users/alec/Documents/Math/bimolecular_positive_recurrence_submission_v1_2_4/README.md`; earlier program `/Users/alec/Documents/Math/bimolecular_positive_recurrence/README.md`.
- Exact relation: same finite weakly reversible mass-action reaction graphs and arbitrary fixed positive rates. OpenAI claims deterministic ODE permanence for all finite weakly reversible networks, any molecularity and any linkage count: one compact convex positive absorbing set per positive stoichiometric class. Our theorem concerns the population CTMC, restricted to one linkage class and molecularity at most two, including boundary/lattice communicating classes, and proves nonexplosion plus positive recurrence and a stationary law on each reachable class.
- Scope: complementary deterministic/stochastic sides of the weak-reversibility conjecture landscape. Deterministic positive concentration bounds do not imply stochastic positive recurrence. In particular the OpenAI theorem does not supply a stationary population law, boundary-class treatment, a falling-factorial Foster argument, or mixing rates. It does not supersede our claim.
- Verification: exact formulations checked in both readmes and OpenAI theorem; no independent reconstruction of either universal proof in this comparison.

### 3. Family 149 → our deterministic reversible realizations and Turing design programs

- OpenAI paper and theorem as above.
- Our projects: `/Users/alec/Documents/Math/reversible_mass_action_realization_theory/README.md`; `/Users/alec/Documents/Math/qbio_mass_action_turing_topology_phase3/README.md`; `/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/README.md`.
- Exact relation: our reversible one-linkage positive equilibrium-continuum constructions and binary-complex diffusion-design networks are weakly reversible ODE systems, hence lie within the claimed permanence theorem before spatial diffusion is added. This supplies a proposed global positive compact trapping framework alongside our equilibrium-component/Jacobian/diffusion analysis.
- Scope: permanence does not imply uniqueness of equilibria, convergence to an equilibrium, homogeneous linear stability, exclusion of a continuum of equilibria, or Turing instability/stable spatial patterns. The manuscript explicitly distinguishes weak reversibility from complex balance. Our diffusion claims concern additional spatial operators not covered by the ODE theorem.
- Strongest impact: potentially relevant background citation for future deterministic papers after validation; no claim replacement or contradiction found.

### 4. Family 156 → our Borsuk dimension-four program

- OpenAI: [A nine-dimensional counterexample to Borsuk's covering assertion](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-nine-dimensional-counterexample-to-Borsuks-covering-assertion-September-23-2026/paper.pdf), Theorem 1.1, PDF p.2.
- Ours: `/Users/alec/Documents/Math/borsuk_dimension4/README.md`, target every bounded subset of `R^4` partitionable into five smaller-diameter sets, with finite-coordinate/diameter-graph proof requirements for a counterexample.
- Exact relation: same Borsuk covering/partition question, different ambient dimension. OpenAI claims the full compact rank-one-projector image `{uuᵀ:u∈S^3}` cannot be covered by ten smaller-diameter sets.
- Essential caveat: the `u∈R^4` notation does NOT make this a four-dimensional Borsuk counterexample. The projector image lies in the trace-one affine hyperplane of `Sym_4(R)`, whose ambient Euclidean dimension is nine. Theorem1.1 explicitly says it does not determine the smallest failure dimension. Their compact topological witness differs from our finite exact configuration approach.
- Impact: a major neighboring claimed reduction of the known failure dimension, leaving our four-dimensional target unresolved.

### 5. Family 170 → our `R(5,5)` search

- OpenAI: [The sharp logarithmic exponent of r(5,t)](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Sharp-Logarithmic-Exponent-of-r-5-t-September-24-2026/paper.pdf), Theorem1.1, PDF p.2; companion for fixed `s≥6` in family170.
- Ours: `/Users/alec/Documents/Math/ramsey55/README.md` and `/Users/alec/Documents/Math/ramsey55_endpoint_capacity/README.md`.
- Exact relation: both ask for graphs avoiding a five-clique and a large independent set. OpenAI claims `r(5,t)=t^4/(log t)^(3+o(1))` as `t→∞`, via projective-flag constructions and entropy compression. Our finite certificate-first work seeks the exact diagonal `r(5,5)`, with Exoo42 verification, fixed-core extension exclusions and an unrestricted order43 CNF that has not been solved globally.
- Caveat: their sufficiently-large-`t` threshold depends on an accuracy exponent. Substituting `t=5` into the asymptotic formula is invalid; it yields no order43/44/45/46 decision or improvement of our finite bound. Same question family, no finite-target resolution.

### 6. Family 179 → our Hadamard order668 program

- OpenAI: [The circulant Hadamard conjecture](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-circulant-Hadamard-conjecture-September-23-2026/paper.pdf), Theorem1.1, PDF p.1.
- Ours: `/Users/alec/Documents/Math/hadamard_668_search/README.md`.
- Exact relation: same orthogonality equation `HHᵀ=nI` for sign matrices, with cyclic autocorrelation/difference-set/cyclotomic methods shared by several of our restricted construction lanes. OpenAI claims that a FULL circulant Hadamard exists only in orders1,4 and deduces Barker length classification.
- Caveat: our target is an arbitrary order668 Hadamard; using circulant blocks, cyclic SDS, Legendre pairs, or group-developed conference cores does not make the full668 matrix circulant. Indeed a full circulant668 was already excluded by the elementary necessary form `n=4u²`, since668=4·167. The new circulant theorem gives no general order668 nonexistence or construction.
- Impact: related exact-autocorrelation methods, while our headline construction remains unresolved.

### 7. Family 188 → our draft #754 triangle-removal spread question

- OpenAI: [The sharp terminal leave in random triangle removal](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026.pdf), Theorem1.1, PDF p.2.
- Ours: [#754, Triangle-removal spread: audited partial bounds; 30005114 unsolved (5/5)](https://github.com/AlecKriebel/Math/pull/754), head `bb0dc486831107a7abd6b3442eff41b42c670c3e`.
- Exact relation: EXACT SAME stochastic process—start from `K_n`, repeatedly remove a uniformly chosen remaining triangle. OpenAI claims the terminal edge count divided by `n^(3/2)` converges in `L²` to `1/(2√2)`. Our question is a conditioned `C/n` spread bound for prescribed families of triangles at the earlier horizon `m=floor(n²/6-n^1.99)`.
- Caveat: terminal leave size/first two moments do not control every prescribed-family inclusion probability. Our current all-family base is `O(n^-0.98)`, with `(4/n)^k` only under an edge-shadow degree hypothesis. Nothing in the checked statement closes this gap. The OpenAI paper uses the same Bohman–Frieze–Lubetzky prefix concentration, followed by independent-unfolding/chronological-query continuation; this is a substantial neighboring paper to inspect, not a substitute solution.

### 8. Family 167 → our draft #738 low-multiplicity distances

- OpenAI: [A power saving for planar unit distances](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-power-saving-for-planar-unit-distances-September-23-2026/paper.pdf), Theorem1.1, PDF p.1; [The weak pinned planar distance theorem](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-weak-pinned-planar-distance-theorem-September-23-2026/paper.pdf).
- Ours: [#738, Audit scoped partials for two low-multiplicity distances (30006556)](https://github.com/AlecKriebel/Math/pull/738), target two distinct occurring distances each of unordered-pair multiplicity at most `n`; accepted partial when at least `n−1` points are cocircular.
- Exact relation: same planar repeated-distance multiplicities. By rescaling, OpenAI's `u(n)≤Cn^β`, `1≤β<4/3`, bounds every one-distance multiplicity in every configuration. Its pinned theorem concerns the number of distinct distances observed from most points.
- Caveat: a superlinear bound `Cn^β` does not force TWO distances of multiplicity≤n. Pinned diversity does not directly impose this exact multiplicity cutoff. These are neighboring uniform bounds, not the target theorem; our special cocircular result is not superseded by the stated exponents.

### 9. Family 167 → our draft #725 diameter with distance gaps

- OpenAI family167 papers as above.
- Ours: [#725, Erdős100 (1929): audited diameter partials, unsolved5/5](https://github.com/AlecKriebel/Math/pull/725), minimum positive distance and gaps between unequal positive distance values at least1; target linear diameter.
- Exact relation: distinct-distance counts translate into diameter lower bounds for our gapped-distance configurations. The pinned `n^(1−ε)` diversity statement would give a corresponding near-linear-power diameter lower bound by counting separated distance values.
- Caveat: our packet already imports the stronger `n/log n` consequence of Guth–Katz. A bound of `n^(1−ε)` for fixedε does not improve it. The unit-distance power bound gives no linear diameter theorem. This is relevant geometry literature, without a newly closed gap from the checked statements.

### 10. Family125 → our draft #88 metric-clustering LP stability

- OpenAI: [The approximation threshold for metric k-median](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Approximation-Threshold-for-Metric-k-Median-September-24-2026/main.pdf), Theorem1.1 and Corollary1.2, PDF pp.1–2; companion [Single-exponential recovery and bounded-price strictness for metric k-median](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Single-Exponential-Recovery-and-Bounded-Price-Strictness-for-Metric-k-Median-September-24-2026/paper.pdf).
- Ours: [#88, Clustering: reviewed metric LP-gap example and dual-margin certificate](https://github.com/AlecKriebel/Math/pull/88), head`a6c913e7992011104708e731349f0876e500a48c`, `PARTIAL_RESULT.md` §§1–4.
- Exact relation: the same finite rational metric k-median assignment relaxation and facility budget. OpenAI claims deterministic `(1+2/e+ε)` approximation with specified candidate facilities and uses LP preparation/dependent rounding/recovery. Our packet constructs an exact weakly1.001 perturbation-resilient F=J instance with a fractional LP gap and proves a strict dual-margin certificate for unique integral LP optimality.
- Caveat: approximation algorithms do not prove the LP integral; “recovery” here is anchor/proxy repair, not a theorem that source-style objective-gap stability implies LP/SDP integrality. Our candidate facilities equal clients; their hardness statement explicitly distinguishes F=J from the general disjoint candidate/client model. No general integrality-threshold or k-means SDP resolution follows.

## Explicit boundaries and nonmatches worth preserving

### Family145 does not settle draft #578

[OpenAI, Rokhlin's multiple-mixing problem for one transformation](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Rokhlins-multiple-mixing-problem-for-one-transformation-September-23-2026/paper.pdf), Theorem1.1 (PDFp.2), concerns a single invertible Z-action and also mixing endomorphisms/flows. [Our #578](https://github.com/AlecKriebel/Math/pull/578) concerns the mixing order of a specific algebraic Z²-action dual to `F_p[x±,y±]/(f)`, with `5≤M_p≤6`, `M_2=6`, and an odd-prime six-term relation gap. The OpenAI introduction explicitly calls one versus several time generators essential and cites Ledrappier's mixing Z² counterexample. No contradiction or closure of the odd-prime gap follows.

### Family213 does not settle our dependent percolation drafts

[OpenAI, No percolation at criticality on quasi-transitive graphs](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/No-percolation-at-criticality-on-quasi-transitive-graphs-September-24-2026/paper.pdf), Theorem1.1 (PDFp.2), assumes independent Bernoulli bonds on a deterministic locally finite quasi-transitive graph and `p_c<1`. [Our #838](https://github.com/AlecKriebel/Math/pull/838) constructs dependent invariant finite-energy laws with an infinite random cluster whose internal Bernoulli threshold equals1. This lacks the theorem's threshold hypothesis, and the realized cluster need not be quasi-transitive. [#837](https://github.com/AlecKriebel/Math/pull/837) is a dependent FKG half-plane existence question; [#755](https://github.com/AlecKriebel/Math/pull/755) concerns GFF maxima on supercritical random clusters; [#112](https://github.com/AlecKriebel/Math/pull/112) is a long-range inverse-square end-count question. No one of these is answered by critical quasi-transitive Bernoulli percolation. Topic adjacency alone should not become an exact match.

### Family231 shares a construction setting with #838 but supplies a different random law

[OpenAI, The free uniform spanning forest is a factor of IID](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-free-uniform-spanning-forest-is-a-factor-of-IID-September-25-2026/paper.pdf), Theorem1.1 (PDFp.2), claims a root-free equivariant construction of the FUSF on every infinite connected locally finite simple unweighted graph. Our [#838](https://github.com/AlecKriebel/Math/pull/838) uses Timár's known one-ended FIID spanning TREE on Z^d as a structural input. Being an FIID forest does not supply one connected one-ended spanning tree or the required thinning bottlenecks. This may be useful background on equivariant sampling, but it is not replacement of the specific tree theorem used in our proof.

### No direct headline match located for kissing number five or eternal domination

The contents/abstract map has no family claiming `τ(5)=A(5,1/2)`, the gamma–theta eternal-domination conjecture, or our negative inequality `gamma∞≥Lovasz theta`. The exact local targets are `/Users/alec/Documents/Math/kissing_number_5/README.md`, `/Users/alec/Documents/Math/gamma_theta_eternal_domination/README.md`, and `/Users/alec/Documents/Math/eternal_domination_lovasz_theta/README.md`. Family090 planar packing/universal optimality and family157 fractional-coloring/minor invariants are related subject areas but have different ambient dimensions, feasible sets, and graph invariants; they should not be presented as having solved these projects. The same applies to dimension-six COMPLEX Hadamard/MUB family266 versus our REAL order668 search.

## Evidence and audit limits

- OpenAI PDFs are pinned, downloaded and extracted with local checksums in `sources/manifest.json`. Introductory definitions and main theorem statements were inspected; selected supporting statements were checked for the PR487 deduction.
- Current pinned PR proofs additionally read for #487 (exact normalized sign set/product comparison), #88 (stability/LP definition and gap) and #578 (Z² action). Other selected draft relations use complete captured PR bodies.
- No full OpenAI proof reconstruction, Lean artifact audit, numerical certificate replay, or literature-priority assessment was performed. These are exact statement comparisons and one conditional mathematical deduction.
- No external contact, outreach, PR comment, branch change, git commit or push was performed by this subtask.
