# Independent source target and initial mechanism seal

Sealed UTC: 2026-10-02T23:17:03.932302+00:00. Completion estimate for this source/math audit: 35%.
Inputs to this seal: immutable `source_snapshot/source_record.json`; publisher original report PDF DOI 10.4171/OWR/2020/6, pp. 411–413 (download and text extraction in own foreign/captures directories). No candidate, review, README, SOURCE_STATUS, helper, result, sibling family, or snapshot manifest has been read. Web search result titles/abstracts identified possible literature; no such proof has yet been read.

## Literal target
For independent U_i uniform on [-1,1] and independent standard normal Z, define

    μ_θ = law(Σ_{i=1}^N θ_i U_i), θ∈S^{N−1};
    ν_N = μ_{Θ^(N)}, Θ^(N) uniform on S^{N−1};
    κ_α = law(Σ_{i≥1} α_i U_i + sqrt((1−||α||₂²)/3) Z), ||α||₂≤1.

The series converges in L² (and almost surely by the independent centered variance-summable theorem). Every κ_α has variance 1/3. κ_0=N(0,1/3), the proposed unique zero of the rate. The target is the distribution **of the random probability measure** ν_N, with speed N and rate I(κ_α)=−(1/2)log(1−||α||₂²) for ||α||₂<1 and I=∞ otherwise. It is not an LDP for a scalar sample from μ_Θ, either conditional on Θ or averaged over Θ. The natural state space is P(R) with weak convergence, metrized by Prohorov; the original report explicitly names Prohorov for its limit lemma. The literal conjecture paragraph does not separately spell out a topology for the LDP, so this standard interpretation must be made explicit, not falsely quoted as part of that paragraph.

The intermediate target is the sequential limit set K={κ_α:||α||₂≤1} of μ_θ with N→∞. The closed ball is required here; the strict inequality belongs to the finite-rate domain only. Boundary measures ||α||₂=1 have infinite rate, yet lie in K. They need not have bounded support when α∉ℓ¹. 'Compact support' for K means compactness of the set of probability measures, not bounded support of every scalar law.

## Independent checkable mechanism (deduction, not a source claim)
Signs and permutations of α leave κ_α unchanged. Use canonical parameters A={a₁≥a₂≥…≥0:Σaᵢ²≤1}, with coordinatewise/product topology. A is compact by diagonal subsequences and Fatou; a_{m+1}≤1/sqrt(m+1). For fixed t the characteristic function is

    exp(−(1−Σaᵢ²)t²/6) Π sinc(aᵢt).

For m large enough that |t|/sqrt(m+1) is small, log sinc(x)=−x²/6+O(x⁴), uniformly for the remaining coordinates. Since Σ_{i>m}aᵢ⁴≤a_{m+1}²Σ_{i>m}aᵢ²≤1/(m+1), the tail plus Gaussian differs from exp(−(1−Σ_{i≤m}aᵢ²)t²/6) by O_t(1/m). This uniform bound proves continuity a↦κ_a from A to weak P(R). K is compact. A diagonal limit of sorted |θ^(N)| gives every possible limit in K. Conversely keep an increasing finite prefix of a and fill remaining mass with many equal small coefficients: take m(N)→∞ with m(N)=o(N) and prefix length m(N), and fill N−m(N) entries by sqrt((1−Σ_{i≤m(N)}aᵢ²)/(N−m(N))). Prefix truncation plus the same tail estimate yields κ_a. Ordering afterward does not change the law.

Injectivity on A is checkable by real zeros: for nonzero a, the smallest positive zero of the characteristic function is π/a₁. Its multiplicity is exactly the finite number of indices with aᵢ=a₁. The Gaussian factor has no zeros; a nonzero infinite sinc product remains nonzero at every t avoiding individual zeros, because its tail logarithms are absolutely summable. Divide out the recovered maximal factors and repeat to recover every positive coefficient. If there are no zeros then a=0. Thus κ_a=κ_b implies a=b, and ||a||₂² is intrinsic. The unqualified map on the whole ℓ² ball is not injective because of signs/permutations; the proposed rate nevertheless is well defined.

Sorted sphere coordinates plausibly give the LDP on A: any fixed m-coordinate constraint has exponential cost −(1/2)log(1−Σ_{i≤m}aᵢ²), and choosing its positions multiplies probabilities by at most N^m, which has zero exponential cost at speed N. A full rigorous lower bound must ensure the remaining coordinates are smaller than the last specified positive coordinate and handle zero ties. Compactness of A would promote projective/local bounds to a full LDP with good rate J(a)=sup_m[−(1/2)log(1−Σ_{i≤m}aᵢ²)]. The homeomorphism A↔K and contraction then transfer it to P(R). This is an independently reconstructed route, not yet a complete audited proof of the sorted-coordinate LDP.

## Source caution
The original report labels the measure LDP a conjecture and the limit-set assertion a lemma being investigated. It labels a sorted-coordinate assertion a theorem, but the short report supplies motivation rather than a full proof. Its displayed finite-coordinate sphere density and normalized log-density contain apparent typographical omissions/errors in the extracted version; those displays must be checked visually before being used. The standard density exponent is (N−m−2)/2, and its normalized log limit is +(1/2)log(1−||t||²), the negative of the proposed cost. These observations are mathematical deductions and do not yet establish the later literature status.

Strongest verified result at this seal: exact literal normalization/object, compact canonical parameter image and complete limit-set mechanism with explicit uniform tail bound, and an injectivity argument adequate to make the proposed rate single-valued. Remaining gap: source chronology and published proof identification; rigorous projective LDP details; exact candidate audit after this initial seal.
