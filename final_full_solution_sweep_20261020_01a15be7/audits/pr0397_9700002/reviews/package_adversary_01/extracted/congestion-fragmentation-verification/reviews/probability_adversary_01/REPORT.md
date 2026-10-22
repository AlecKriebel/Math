# Independent probability/concentration audit: PR397

Verdict: **PASS for the stated turn-2 probability theorem and outer-phase conclusions.** No material mathematical gap was found. **The historical replay wrapper does not pass unchanged in the available complete numerical environment** because it requires exact equality of floating diagnostics; this is a reproducibility qualification requiring documentation or repair before a package claims a clean replay. Novelty and the subjective adequacy of a conceptual toy model are separate judgments.

This review is independent of the other fresh families. I read no other fresh review output. Inputs are pinned to `3705c5102b58c48e29991c61771978bf756a62e7`; all 24 source files have verified byte lengths, SHA256 and Git blob identities in `INPUT_BINDING.json`. The exact diff contains these files and the corresponding QUEUE row. Frozen inputs were never modified.

## Exact claim and necessary assumptions

Let k=2^(H−1), H≥2. A complete binary tree has k left source leaves, k right destination leaves and N=4k−1 vertices. Every ordered left-to-right pair has initial demand one. Fixed topology, unique simple paths, positive linear prices and mandatory doubled baseline demand give capacity 2k k_e on every edge, where k_e counts descendant leaves. In particular terminal capacities are 2k, and top-edge capacities are 2k². This capacity scaling is essential, rather than a uniform bounded-capacity sparse-network theorem.

After capacities are fixed, the k² growth slopes X_ij are independent Exp(1) variables. Demand is 1+(t−1)X_ij for t≥1. Its mean is t and variance (t−1)². Put S_k=ΣX_ij>0 on the positive realization space. The marginal is the right derivative of optimal admitted throughput divided by this realized offered-demand slope, not by k² and not by total offered demand. The spare graph has all physical vertices and retains edges with load strictly below capacity. Statements about every optimizer occur only on the two proved outer phases.

The theorem uses δ_k=8√(log(k)/k)<1, which first occurs along this binary family at k=512 (H=10). With probability at least 1−ε_k, simultaneously at all t∈[1,2−δ_k] the marginal equals one and the whole tree is spare, while at every t≥2+δ_k the marginal equals zero and the spare graph has no edges, for **every** optimizer. The stated ε_k is

    2 k^−31 + 2 k^−2/(1−k^−2)² + (4/k²)^k.

This is an upper bound on an outer-phase window, not an exact scaling exponent, a lower bound on that window, a universal finite switch at two, a limit for r_k(2), or a component-size distribution at criticality.

## Independent analytic reconstruction

### 1. Deterministic reduction underlying the stochastic event

The terminal row and column constraints are Σ_j y_ij≤2k and Σ_i y_ij≤2k. Summing them over descendant terminals gives every other tree-edge constraint, with exactly the prescribed capacity. The converse is immediate from leaf edges. Thus the admitted-demand optimization is a capacitated bipartite transport problem.

For a cut with left source-side set A and right sink-side set D, let a=|A|, d=|D|. A full throughput of 2k² is feasible exactly when every cut satisfies

    Σ_(A×D) [1+(t−1)X_ij] ≥ 2k(a+d−k).

Cuts with a+d≤k need no stochastic estimate. This formulation explicitly includes mixed cuts; row and column offered totals alone would be insufficient. It makes no assertion of independence between distinct cuts.

If all offered terminal totals are strictly below 2k, full demand is feasible and is the unique admitted matrix maximizing its total: an individual deficit cannot be compensated by another entry exceeding its offered demand. Summing strict terminal inequalities makes every internal physical edge strictly spare. If throughput is 2k², all k row totals and all k column totals must instead equal 2k; therefore every internal physical edge is saturated under every optimizer. These facts prevent a favorable tie-break from entering the probability conclusion.

### 2. Tail rate from a separate Poisson route

For a positive integer n and Z∼Gamma(n,1),

    P(Z≤na) = P(Poisson(na)≥n),  0<a<1.

The Poisson exponential moment bound with exponential parameter −log(a)>0 gives exp[−n(a−1−log(a))]. This independently recovers the lower Gamma tail used in the proof. The usual exponential moment calculation also gives the upper tail with the same rate I(a)=a−1−log(a), a>1.

For 0<δ<1, exact derivatives/integrals give

    I(1/(1−δ)) = ∫₀^δ u/(1−u)² du ≥ δ²/2,
    I(1/(1+δ)) = ∫₀^δ u/(1+u)² du ≥ δ²/[2(1+δ)²] ≥ δ²/8.

In particular the lower-tail constant cannot simply be replaced by 1/2; a δ=1/2 control rejects that tempting mutation.

### 3. Uniform subcritical event

At 2−δ, each offered row total is k+(1−δ)Γ_k; a violation of strict slack requires Γ_k≥k/(1−δ). The same marginal estimate holds for every column. A union bound over 2k dependent row/column events gives

    P(any terminal reaches capacity) ≤ 2k exp(−kδ²/2).

At δ=δ_k this is 2k^−31. On the complementary event, positivity of growth slopes gives strict slack simultaneously at every earlier t≥1. Strict slack at the endpoint persists in a realization-dependent right neighborhood, so the **right** derivative at the endpoint still equals S_k. No uncountable-time union bound is needed.

### 4. Full supercritical all-cuts estimate

For a+d>k the rectangle has n=ad independent exponential entries, and

    ad−k(a+d−k)=(k−a)(k−d)≥0.

At 2+δ, failure of this cut implies Γ_ad<ad/(1+δ). Some actual cut thresholds may be nonpositive, making failure impossible; replacing them by ad/(1+δ) remains a safe upper bound. Hence each cut fails with probability at most exp(−c ad), where c=I(1/(1+δ))≥δ²/8.

I independently enumerated cuts using q=min(a,d) and ℓ=k−max(a,d). Positivity gives 0≤ℓ<q and area ad=q(k−ℓ). For q≤k/2, each ℓ has at most 2 binom(k,q)binom(k,ℓ) realizations. Summing ℓ gives at most 2q k^(2q), and area is at least qk/2. For q>k/2, area is greater than k²/4 and there are at most 4^k subset pairs. These cases cover every positive cut, including all asymmetric sizes and duplicated interchange counts safely.

Using c≥8log(k)/k at the specified δ_k, the first contribution is at most

    Σ_(q≥1) 2q k^−2q = 2 k^−2/(1−k^−2)²,

and the second is at most (4/k²)^k. No independence among rectangles is invoked. A crude 4^k multiplier at the smallest area k would not yield a useful bound; the size split is necessary to this proof.

When all cuts pass, one full-capacity admitted matrix remains feasible at every later time because every demand bound increases. The global terminal bound prevents more than 2k² throughput. Thus the zero right derivative and all-optimizer edge saturation hold on the whole supercritical half-line, with no union over times.

### 5. Limits and edge cases

Adding the two failure estimates proves the advertised simultaneous event. The failure series is summable along k=2^(H−1): its main term is O(k^−2), and the remaining terms are smaller and summable. Under any common coupling, first Borel–Cantelli therefore gives eventual outer-phase conclusions; independence between network sizes is unnecessary.

For any fixed t<2 or t>2, δ_k→0 places it eventually in the appropriate phase. Whole-tree and edgeless spare graphs have largest component sizes N and one, so the displayed normalized limits follow. At t=2, the proof uses only monotonicity:

    k²+(1−δ_k)S_k ≤ F_k(2) ≤ 2k²

on the good event, together with Var(S_k/k²)=1/k². This establishes F_k(2)/k²→2 in probability without interchanging a derivative and a limit. No inference about r_k(2) follows. With all positive slopes equal to x, the finite kink occurs at 1+1/x, which differs from two when x≠1. The candidate correctly avoids claiming universal finite criticality.

The rate normalization excludes the null-probability all-zero rate vector. A sample space (0,∞)^(k²) realizes the stated Exp(1) model with S_k>0 everywhere; no additional probabilistic assumption is needed. The H≥2 restriction excludes k=1 from the theorem although some code tests that harmless extension. Natural logarithms are used. A bound exceeding one at small inadmissible sizes is not promoted to a probability theorem there.

## Computation and reproducibility

`probability_controls.py` is independently authored and imports no author or historical reviewer program. Its retained output records 2,796,678 passing assertions across 695,520 positive cut-size pairs for k=1,…,160. It also directly counts subset pairs for k≤6, checks the independent q/ℓ multiplicity formula, tests high-precision tail rates down to δ=10^−12, reconstructs the rate via Gamma–Poisson identities and positive Poisson-tail sums, verifies window exponents and the first admissible binary family member, and rejects the false finite-k switch-at-two and wrong lower-tail constant. Counts measure finite control coverage, not independent proofs. Decimal and float probability diagnostics are not claimed as validated interval certificates.

I inspected the actual author turn2 checker and historical portable independent checker. A fresh disposable copy was used for each standalone reproduction, leaving all original bytes unchanged. Available complete runtime: Python3.9.6, NumPy2.0.2, SciPy1.13.1 in the repository `.venv`; this review installed or changed no packages.

- Turn2 `CHECKS.json` reproduced **byte-for-byte**, SHA256 `c98e5388c9496b25ce37b966a59bdd29ff25325940f72dee789dc2d72b94c1d9`.
- Turn1's preserved illustrative-partial checker passed every assertion, but 37 floating diagnostics differ by at most 4.440892098500626e−16. The original `REPLAY_ALL.py` stops at its strict SHA comparison for this old output.
- The portable independent checker passed every assertion on fresh frozen inputs. Its expected public-input control uses eight files rather than the 25-file original review binding, as already documented. Runtime metadata differs. Three Gamma-CDF diagnostic sums also differ by ordinary final-bit amounts, largest absolute change 2.2737367544323206e−13 on a sum around1841; their relative differences are about10^−16. No pass/fail or discrete mathematical control changed. The wrapper's exact `checks[1:]` equality would reject these floating variations too.

`REPLAY_DETAIL.json` retains every exact difference, environment and output hash. `REPLAY_DETAIL_INITIAL.json` preserves an initial harness sequencing mistake: it reused a disposable copy after turn1 rewrote a CHECKS file, causing the next frozen-input guard to reject. The revised harness restores all frozen inputs before **each** standalone run. This mistake was mine; it established no defect in the candidate's portable input binding.

Default Python lacks NumPy; bundled Python has NumPy but lacks SciPy. Both unsuccessful attempts ended before mathematical controls. These are environment limitations, not mathematical counterexamples. A publication package should retain immutable historical receipts, provide a tolerant semantic comparison for declared floating diagnostics or pin a genuinely reproducible environment, and disclose that its historical exact wrapper did not pass in the available runtime. It must not silently describe this review as a byte-identical replay of the entire packet.

## Source fidelity and limits of this family

I independently retrieved and read the complete primary Aldous congestion page and its index. The request seeks an analytically tractable model linking a sharp loss of marginal absorption with fragmentation of spare capacity. Fixed-topology doubled-demand capacity design is one suggested mechanism; the page's linear-variance random-growth example is illustrative. The index places this problem on its conceptual end of the spectrum. The present physical tree and dense traffic model is a precise HOT example within that broad request, with quadratic variance explicitly disclosed. It does not solve a prescribed linear-variance process, SOC variant, universal network theorem or canonical unique modeling program. Whether it is the intended “right” model cannot itself be established by its concentration proof.

Sources: [Aldous congestion problem](https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html), [problem-list interpretation](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html). `SOURCE_CUSTODY.json` binds complete actual HTML downloads kept only in ignored private storage; no third-party full text is redistributed here. No individual was contacted. This family conducted no comprehensive priority audit and makes no historical originality or firstness judgment. Classical transport or concentration ingredients alone do not establish duplication of their exact application.

## Required disposition from this review

No proof repair is required for the stated turn2 probability theorem. The strongest verified result is exactly the explicit uniform outer-phase theorem, its fixed-time marginal/connectivity limits, and critical throughput limit under the model above. No stronger critical conclusion is certified. The replay portability defect is a substantive package concern if the package asserts that its unmodified clean wrapper works across the available documented runtime; it can be repaired without changing the theorem. Publication readiness remains subject to that repair/documentation, the other mathematical family, source-scope and priority judgments, and fresh whole-package adversarial reviews.
