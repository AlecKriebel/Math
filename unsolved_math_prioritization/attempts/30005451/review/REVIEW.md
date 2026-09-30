# Independent review: affine Bernoulli/Poisson preferential attachment

**Verdict: PASS for the complete stated affine comparison theorem and its explicit limit tree. The broad source target remains unsolved, 1/5.** No mathematical correction to the frozen candidate is required. The original question introduces general concave attachment rules; the affine theorem is a substantial, explicitly bounded subcase. The dataset's fixed-outdegree equality is a separate source-extraction error.

This review covers `CANDIDATE.md` SHA-256 `2cda05be8133f5176c34ade68a859c8b7d14ec8e2586ca64ca7a63f590a64b74`. The mathematical snapshot was not edited. Review completed on 30 September 2026, using GPT-6 Astra at xhigh reasoning. This is independent adversarial AI review, not human peer review. Priority remains unestablished.

## 1. Primary source and classification

I read the complete preferential-attachment contribution in OWR 12/2023, printed pp. 646–651, and visually inspected p. 650. The report's paragraph (b) defines the Bernoulli model for concave positive functions with increments less than one, then asks for the relation to a random-outdegree model adapted to indegree weights and i.i.d. Poisson outdegrees. It does not ask for equality with the original fixed-outdegree model. Paragraph (c)'s separate nonlinear fixed-outdegree question does not remove the general-function wording in paragraph (b). [Official report](https://ems.press/content/serial-article-files/47008)

Consequently, the safe queue classification is **unsolved, 1/5**, with a complete affine theorem recorded as the partial result. The source's open-ended adaptation also does not specify every convention; the candidate makes its two no-new-self-loop conventions precise instead of claiming to cover all interpretations. Its own final section already preserves the nonlinear gap.

The complete Dereich–Mörters primary paper was checked at its model definition, the idealized neighborhood construction, its explicit weak-local-limit statement on reprint p. 9, and the neighborhood exploration couplings in Sections 5–6. The model requires f(0)≤1, uses an isolated initial vertex, and has independent incoming columns. These exactly support the restored affine range 0≤a<1, 0<b≤1 and the credited limiting tree. The displayed component-size propositions alone would be insufficient, but the paper expressly identifies the tree as the weak local limit and develops the structure-preserving exploration. [Dereich–Mörters](https://arxiv.org/abs/1007.0899)

The current Garavaglia–Hazra–van der Hofstad–Ray v4 was independently checked, including its 2 March 2026 revision, models (D)/(E), and p. 13's extension discussion. Its weights use total degree, and its convergence theorem is not being applied to indegree weights. The candidate borrows only the updating conventions and proves its adapted models independently. That distinction is correct. [Current primary preprint](https://arxiv.org/abs/2212.05551v4)

## 2. Definitions, admissibility and finite seeds

For the Bernoulli graph, every vertex can receive at most one edge from each later arrival, so its indegree at time n is at most n−1. The proposed probability (a d+b)/n is therefore in [0,1], including the boundary b=1. The affine slope a<1 is indispensable later; the theorem does not cover a=1. The case a=0 is not silently divided by a.

Both Poisson definitions are valid even when an arrival has zero outdegree. The normalizing sum is at least bn>0; there is no conditioning on a positive Poisson count. Frozen targets allow repetitions. Sequential targets update only the old receiving vertex, giving denominator S+aj after j choices. The arriving vertex is never eligible as a target in its own row. These choices are consistently retained in the coupling and tree description.

A fixed alternative Poisson seed contributes a finite initial discrepancy. Its edge count later is a fixed integer plus an independent Poisson sum, so its normalization error acquires only an additional O(1/n) bias. The proof handles this directly, including a seed with loops or parallel edges. It does not require an unproved seed-universality theorem. Loops count twice in undirected degree and once in indegree/edge count, which is compatible with the estimates used.

## 3. Moment bounds and the crucial normalization

The conditional row mean and variance are valid because the Bernoulli indicators are conditionally independent. The mean edge-count recursion gives E T_n≤λn with λ=b/(1−a), and hence E S_n≤λn. Updating each weight by a times its Bernoulli indicator yields the displayed exact squared-weight recursion. Iteration gives O(n), O(n log n), or O(n^(2a)) according to 2a<1, =1, or >1. In every case E F_n/n²→0.

The total-edge second-moment inequality is also correct: conditioning on T_n and adding the row variance bound gives precisely the displayed coefficient (1+a/n)² and the O(n) forcing. Since a<1, a sufficiently large multiple of n² is a supersolution. Consequently the birth-row second moments are uniformly bounded.

For a>0, choose 1<q≤2 with aq<1. Taylor's remainder in (w+a)^q is bounded uniformly for w≥b>0, because q−2≤0. Thus the qth-weight recursion has multiplier 1+aq/n and bounded forcing, and its expected sum is O(n). The outdegree is fixed at birth, so its averaged qth moment follows from the row second moment. For a=0 the separately written indegree-square recursion is exact. This proves the needed uniform averaged undirected-degree moment of some order strictly greater than one; it does not assume finite degree variance when a>1/2.

The decisive normalization estimate uses the **Poisson graph's own** total weight:

    Σ_v |w_v/n − λw′_v/S′_n|
      ≤ aD_n/n + |S′_n/n − λ|.

The first term comes from indegree discrepancies. The second follows exactly by summing w′_v times the scalar normalization difference. Since T′_n is a Poisson sum and aλ+b=λ, its expected normalization error is O(n^(−1/2)), with a possible O(1/n) seed bias. No missing concentration result for a general nonlinear weight sum is being assumed.

## 4. Couplings and error recursion

The Bernoulli/Poisson count coupling is legitimate on the whole interval 0≤p≤1. The extra Bernoulli success probability on the event N=0 is between zero and one, since 0≤p−1+exp(−p)≤exp(−p). Its expected absolute discrepancy is 2(p−1+exp(−p))≤p². Adding or thinning a Poisson variable gives the further |p−z| term.

Independent targetwise application preserves the complete conditional Bernoulli row law and the vector of independent Poisson counts. Poisson splitting makes the latter precisely the frozen-weight row. Its total is Poisson(λ) conditionally on the entire coupled past, because its total mean is the fixed constant λ. Thus the outdegrees remain independent across arrivals, even though the two graphs are coupled.

For sequential updating, after j choices the target law is a convex mixture of the frozen law and the empirical distribution of past sequential targets. Its distance from the frozen law is at most aj/(S′+aj). One can maximally couple at each step while keeping the next frozen target's conditional marginal fixed given the full joint history; its draws therefore remain independent. A target disagreement changes the count vector by at most two. Summing and using E[M(M−1)]=λ² gives aλ²/(bn), including M=0 and a=0.

The two row couplings can be glued through the intermediate frozen row. Conditional on its counts, a uniformly random ordering recovers its independent-target representation; regular conditional laws on these countable spaces then supply the sequential coupling. There is no requirement that a Bernoulli row have the same count as a Poisson row.

The resulting recursion is

    d_(n+1) ≤ (1+a/n)d_n + r_n,      r_n→0.

For n beyond a fixed cutoff, replace r_n by ε. The affine function εn/(1−a) is an exact particular solution, and the homogeneous factor grows only as n^a. Dividing by n, taking the limit, then ε↓0 proves d_n=o(n). Every error term used tends to zero, including the squared-weight term and sequential-update term.

## 5. Local stability, boundary edges and empirical total variation

Let H be the union multigraph and W₀ the endpoints of discrepant edges. The estimates |W₀|≤2D, deg_H≤2deg_B+|deg_P−deg_B| and Σ|deg_P−deg_B|≤2D are valid, including multiplicities and seed loops.

Hölder's inequality must be applied on the product of probability space and vertex counting measure because the exceptional vertex set is random and depends on the graph. That application gives exactly equation (15). Iterating the resulting scalar bound over a fixed number of neighborhood expansions sends an o(n) expected exceptional set to another o(n) expected set.

A root whose union-graph radius-r ball avoids W₀ has the same vertices, all its induced edges, their directions and multiplicities in both graphs. In particular, this does check edges between boundary vertices; it is stronger than checking only the exploration's spanning tree or vertex degrees. Identical deterministic labels/marks are automatically preserved by the identity map. Pairing the same root label gives the empirical total-variation bound, not merely convergence of an annealed one-root marginal.

## 6. Independent-column pruning and concentration

The Bernoulli model has a stronger independence property than conditional independence of a single row: all indicators pointing to a fixed receiver are a function of that receiver's own uniforms and deterministic times. Different incoming columns are independent. A global random normalization would destroy this argument, but that normalization is absent in the Bernoulli rule.

The first pruning deletes a whole column if it contains more than K edges. The second uses degrees in that intermediate graph, not iteratively recomputed degrees, and deletes every edge incident to a vertex of degree greater than K. Every removed edge meets a vertex whose original degree exceeds K. The qth-degree bound therefore gives an expected removed-edge fraction O(K^(1−q)), uniformly in n. The same Hölder neighborhood argument turns this into a uniform error ε_(K,r)→0 for bounded radius-r statistics.

For a resampled column, the intermediate graphs differ by at most 2K edges. At most 4K endpoint vertices can change threshold status. A vertex whose threshold status changes has degree at most 3K in either intermediate graph, because the degree difference is at most 2K and one side is at most K. Thus at most 2K+12K² edges can differ in the final pruned graphs, a concrete bound sufficient for the candidate's unspecified C_K. Both final graphs have degree at most K, so their union has degree at most 2K. Only a bounded number, depending on K and r, of roots can detect those edits.

Accordingly the empirical bounded local statistic has coordinate oscillation O_(K,r,h)(1/n). The martingale bounded-difference calculation yields variance O_(K,r,h)(1/n). Comparing original and pruned empirical means costs at most a constant times ε_(K,r), including their expectations. Taking n→∞ first and K→∞ second proves L¹ concentration around the mean. This supplies the source's empirical local-in-probability conclusion rather than treating annealed convergence as sufficient by itself.

## 7. Gamma–Poisson tree and Palm conditioning

The affine birth-process representation is valid as a process, not just a match of one-time means. Put ν=b/a. Conditional on Γ~Gamma(ν,1), the point process has intensity aΓ exp(at)dt. Given its complete history through t with k points, its Gamma likelihood depends on that history through k and exp(at)−1; the posterior is Gamma(ν+k,exp(at)). Its conditional jump intensity is therefore a(ν+k)=b+ak, identifying the stated pure-birth process.

An equivalent direct check uses ordered event times 0<t₁<⋯<t_k<t. Integrating the Poisson likelihood gives a density proportional to

    a^k (ν)_k exp(aΣt_i) exp(−(b+ak)t),

which equals the product of successive affine birth rates times the pure-birth waiting-time survival factors. The independent checker additionally compares exact two-time distributions after the common nonrational power is canceled.

Palm conditioning on a prescribed incoming point multiplies the mixing density by Γ. It therefore changes the shape from ν to ν+1 while retaining rate one; the deterministic intensity factor at that time cancels on normalization. Conditional on Γ, removing the Palm point leaves the original Poisson process. Thus the +1 shift is required exactly when the parent is younger. When the parent is older, it belongs to the independent older-child Poisson process, whose Palm remainder has its original law, so the incoming strength remains unshifted. Conditioning on an ordinary zero-probability point event has not been used.

Using E f(Z_t)=b exp(at), the transformations v=u exp(s) for older children and v=u exp(t) for younger children give the candidate's two age intensities. Their masses are λ and Γ(u^(−a)−1), finite for every u>0. Every fixed generation is therefore finite almost surely. The constant-rule case uses ordinary Poisson processes and is correctly treated separately.

For the root, U is uniform, the older-child count is Poisson(λ), and the conditional probability of no younger child is u^b. Their independence gives isolated-root probability exp(−λ)/(1+b)>0. A fixed positive outdegree gives no isolated non-seed vertex; the finite seed fraction vanishes. This rigorously diagnoses the dataset's unmarked fixed-outdegree comparison as false, while leaving the actual Poisson comparison distinct.

## 8. Reproduction and limitations

All **35,349 author assertions** replayed byte for byte from the isolated snapshot. The author verifier hash is `4ec5048e1053e9634c02a9a90040daf065b2a37a91183eca2766e943a845ed5f`; its receipt hash is `42e68e9c561d3173ae9b380f2b1e9ecab7b6c3ec55f21d2c239381512ca29656`.

The independently written standard-library checker passes **98,943 exact assertions**, including:

- 1,350 two-time Cox/affine-birth identities and separate Palm shape checks
- 252 complete finite target-sequence models, including Dirichlet–multinomial count laws and path-to-count total-variation contraction
- 4,374 loop/parallel-edge graph-edit pairs, testing degrees and induced balls
- 4,096 five-vertex column-replacement pairs, testing an explicit pruning influence bound and threshold locality
- Independent rational normalization, second-moment and recursion checks

These calculations challenge the local formulas and finite mechanisms; they are not numerical proofs of convergence, Hölder uniform integrability, or priority. Those conclusions depend on the written argument and the explicitly credited Bernoulli limit.

Reproduce from this review directory:

```sh
python3 author_replay/verify.py
python3 independent_checks.py
```

The first command uses SymPy in addition to Python's standard library; the second uses only the standard library. Source PDFs/page images and incidental replay stdout are not publication files.

**Final scope recommendation:** publish the reviewed affine theorem as a partial result, with the repaired source formulation and **unsolved, 1/5** broad status. General nonlinear concave rules, alternative unspecified adaptation conventions and a no-parallel-edge model remain outside the proof. Do not promote the isolated-root correction to a solution of the original Poisson comparison, or the affine comparison to a theorem for all concave rules.
