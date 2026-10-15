# Independent RSK reconstruction — frozen before inherited verdicts

Timestamp: 2026-10-15T03:39:06.027832+00:00. Target input PROOF.md SHA256: c6e7d751931637e0f119cf6ba8adf71462adb321825be5df39f3f67f2ea61dc0. Reviewer role: exact combinatorial joint-law adversary, PR246 / AMR-096-0040. No files under submitted independent_review have been opened at this checkpoint. This file is frozen read-only; later comparisons and corrections belong in REPORT.md.

## Claim and boundary of this reconstruction

Let a unit-area-intensity Poisson process occupy (u,v)>0. At a fixed height 1 let L(x) be its strictly northeast chain length in (0,x] × (0,1], and define Z_r=inf{x:L(x)>=r}. Conditional on the separate dynamics/uniqueness identification Z being the stationary configuration, the claim is an explicit formula for every finite simultaneous event {Z_r>x}. The following counting proof does not assume a Markov property in r or a shape-process transition formula. Stationary existence, uniqueness, and historical adequacy of “fairly explicit” are outside this role.

For 0=x_0<x_1<...<x_m, r_j positive integers, Δ_j=x_j-x_{j-1}, b_j=r_j-1, define D_t(λ/μ)=det[t^(λ_i-μ_j-i+j)/(λ_i-μ_j-i+j)!], with negative entries replaced by 0, h_0(0)=1, zero if μ is not contained in λ, and sufficient zero padding. Then the proposed survival probability is

exp(-x_m) Σ_{∅=λ^0⊆λ^1⊆...⊆λ^m; λ^j_1≤b_j} D_1(λ^m/∅) ∏_{j=1}^m D_{Δ_j}(λ^j/λ^{j-1}).

An empty list of positive thresholds is assigned probability 1, separately from this displayed formula (which otherwise refers to x_m).

## Independent finite counting derivation

Disjoint u strips have independent Poisson counts d_j of means Δ_j. Given the counts, all n=Σd_j v marks are independent continuous uniforms; their relative ranks, in u order, are each of n! permutations with equal probability. The fact that u locations were conditioned to lie in strips does not bias the ranks: v is independent of all u data. The standard Schensted correspondence of a permutation gives standard tableaux (P,Q), of equal final shape λ^m. Its prefix shape after n_j=Σ_{i≤j}d_i is the shape of the entries 1,...,n_j of Q. Schensted's subsequence theorem identifies its first row with L(x_j).

Fix a nested shape chain of these sizes. Each block n_{j-1}+1,...,n_j occupies the skew difference λ^j/λ^{j-1}; standardizing its consecutive labels gives any one of f^(λ^j/λ^{j-1}) standard skew tableaux. Conversely, each tuple of block tableaux gives a standard Q: initial subshapes are order ideals, and all labels of a later block exceed all labels of an earlier one, so cross-block row/column inequalities hold. P remains any one of f^(λ^m) tableaux. Thus the number of permutations realizing the chain is f^(λ^m)∏_j f^(λ^j/λ^{j-1}), and the conditional probability is that count divided by n!.

Multiplying by exp(-x_m)∏ Δ_j^(d_j)/d_j! gives exp(-x_m)[f^(λ^m)/n!]∏[Δ_j^(d_j)f^(λ^j/λ^{j-1})/d_j!]. This contains BOTH the global n! from permutation ranks and each block d_j! from Poisson counts; there is no cancellation of either family. This is exactly the proposed determinant product once the next identity is established. Finally Z_r>x iff L(x)≤r-1, so imposing each first-row bound gives the claimed survival event.

## Determinant identity and independence from external limit heuristics

For any fixed skew shape with d boxes, specialize a Schur function to q identical variables t/q. Its semistandard tableaux with all d labels distinct contribute binomial(q,d) f^(λ/μ)(t/q)^d. Tableaux with fewer than d distinct labels are O(q^(d-1)) in number for fixed shape, so vanish after multiplication by q^-d. Therefore the limit is t^d f^(λ/μ)/d!. Meanwhile the generating function of the complete symmetric polynomials is (1-tz/q)^(-q); each fixed coefficient tends to t^r/r!. Finite skew Jacobi–Trudi passes to this limit and proves D_t(λ/μ)=t^d f^(λ/μ)/d!, including t=0 by polynomial continuity. This independently reconstructs the exponential specialization, rather than assuming a Plancherel parameter convention.

Every nonzero determinant monomial has the same t degree d because Σ_i(λ_i-μ_{σ(i)}-i+σ(i))=|λ|-|μ|; no missing degree factor arises. All D_t for t≥0 are nonnegative by the tableau interpretation. For λ=μ the skew tableau count is 1, d=0, so D_t=1 even at t=0. For t=0 and λ≠μ, D_0=0. If μ⊄λ, the skew weight is assigned 0, consistently with Jacobi–Trudi.

Padding by one extra zero appends a last row whose entries before the last are h_(j-ell-1-μ_j)=0 and whose final entry is h_0=1. Expansion in that row returns the original determinant, and induction proves padding invariance, including ∅/∅. Transpose of a standard skew tableau is a bijection preserving labels and standardness, so D_t(λ'/μ')=D_t(λ/μ). First-row bounds turn into length bounds; padding all transposed determinants to B=max b_j is valid. If B=0 all shapes are empty, all determinants are 1, giving exp(-x_m).

## Positivity, normalization, convergence

At a fixed strip-size vector d, summing f^(λ^m)∏ f^(λ^j/λ^{j-1}) over all nested chains with those sizes counts all n! permutations by the bijection. Hence the total raw unconstrained mass of terminal size n is Σ_{Σd=n} ∏Δ_j^(d_j)/d_j! = x_m^n/n!. Row constraints only remove nonnegative terms. Summing n gives exp(x_m), proving unit total mass after exp(-x_m), absolute convergence, and positivity of every finite survival query (the empty chain alone has raw weight 1). These are exact arguments for all finite m and all positive integer indices; finite tests below cannot replace them.

The Poisson tail x_m^(N+1)/(N+1)!/[1-x_m/(N+2)] for N+2>x_m bounds the discarded raw mass by successive term ratios. It tends to zero. For rational thresholds, the retained determinants and this bound are rational. This verifies the series is an effective finite expression to arbitrary requested tolerance, conditional on finite arithmetic and without a claimed efficient bound in the particle indices. The certificate's precise enclosure is delegated to another role.

## Arbitrary order, repeated thresholds, nonpositive thresholds

Sort distinct positive thresholds, keeping the associated index attached. At one threshold, {Z_a>x}∩{Z_b>x}={Z_min(a,b)>x}, because Z is increasing. Thresholds ≤0 impose no restriction because positions are strictly positive. Repeated particle indices at different thresholds may be retained; the formula automatically incorporates the redundancy of the strongest threshold. The b_j need not increase. If b decreases, nested shapes can satisfy the more stringent later bound, and the earlier bound can become redundant; the event is not impossible. No monotone-index assumption enters any preceding counting step. For all thresholds nonpositive, use probability 1. Inclusion–exclusion on complements {Z_r≤x} gives any finite joint distribution function. Right-continuity and the absence of deterministic-coordinate atoms follow from the continuous u marks, not from differentiating a possibly nonsmooth general joint law.

## Independent low-index derivative and gap check

For r=(1,2) and 0<x<y, the first shape must be empty and the final shape a column. Both straight/skew standard counts equal 1, so S(x,y)=exp(-y)F(y-x), F(z)=Σ_{n≥0} z^n/(n!)^2. This entire power series and all its derivatives converge uniformly on compact complex sets, justifying differentiation in x,y on compact subsets of 0<x<y. Its mixed derivative is exp(-y)[F'(y-x)-F''(y-x)] = exp(-y)Σ_{n≥0}(n+1)(y-x)^n/[n!(n+2)!]. This is positive. Under (x,y)↦(x,z=y-x) the Jacobian is 1 and it becomes exp(-x)a(z), a(z)=exp(-z)Σ(n+1)z^n/[n!(n+2)!]. Tonelli and ∫exp(-z)z^n dz=n! give ∫a=Σ(n+1)/(n+2)!=1 (telescoping 1/(n+1)!-1/(n+2)!). Thus this is the full normalized density on x,z>0 and proves independence of Z_1 and Z_2-Z_1. There is no general assertion of independent successive gaps or a particle-index Markov property.

## Primary input verification before inherited review

Opened the original URLs directly, including Okounkov–Reshetikhin arXiv math/0107056v3 (31 January 2003), section 2.2.4, equations (7)–(8); Betea et al., published author-hosted PDF, printed page 415, equation (6.6); Aldous–Diaconis 1999, section 2.1, RSK bijection and Proposition 4 on printed pages 418–419; Aldous–Diaconis 1993 notes, printed page 39, equations (46)–(48). Their conventions match the reconstructed determinant, exponential parameter, permutation normalizer, and gap density. PRIMARY_SOURCE_PINS.json records exact byte hashes and download outcomes; the primary source reading copies remain outside the public authored-file manifest. No historical novelty conclusion follows from these classical inputs.

## Falsifiable next checks and exact remaining gap

Reproduce author and inherited independent scripts in separate local directories, compare every receipt field, and test exact permutation prefix chains against independent skew-poset tableau enumeration and a separate determinant implementation. Explicitly include weak containment, noncontainment, zero parameters, oversized padding, transpose, B=0, all query orderings, and count conditioning. This reconstruction finds no mathematical gap in the conditional joint law. Its application to the unique invariant distribution still depends on the separately audited dynamics theorem; source adequacy and priority require separate review. This is an independent reconstruction, not a verdict about the complete PR.
