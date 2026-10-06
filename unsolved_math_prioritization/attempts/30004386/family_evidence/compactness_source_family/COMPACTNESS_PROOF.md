# Independent verification of the limit-law set

This proof expands the route sealed in INITIAL_INDEPENDENT_SEAL.md before candidate exposure. It is a verification artifact, with no novelty claim. Subsequent source reading showed the same analytic mechanism already in Johnston–Kabluchko–Prochno. Their theorem supplies the full LDP; the argument here supplies the precise compactness and all-law attainability assertion independently.

Let U_j be independent uniform[-1,1], and Z independent standard normal. For any real a in l2 with s=Σa_j²≤1, let κ_a be the law of S_a+sqrt((1-s)/3)Z.

## 1. Series existence, signs and permutations

E U_j=0 and E U_j²=1/3. For q>p,
 E |Σ_{j=p+1}^q a_jU_j|²=(1/3)Σ_{j=p+1}^q a_j².
Thus the series is Cauchy in L2. For almost-sure convergence, choose n_k so that (1/3)Σ_{j>n_k}a_j²≤2^(-4k). The independent centered maximal inequality gives
 P(sup_{m>n_k}|S_m-S_{n_k}|>2^(-k))≤2^(-2k).
For the supremum over all m, first apply the finite inequality and increase its terminal index. Borel–Cantelli implies the partial sums are Cauchy almost surely: eventually every tail beyond n_k is within2^(-k) of S_{n_k}. The almost-sure and L2 limits agree by convergence in probability.

Symmetry removes any fixed pattern of signs. Rearrangement is legitimate in L2: the net of finite sums is Cauchy because the squared residual over indices outside any sufficiently long original prefix is bounded by its tail square sum. Every enumeration of the same nonzero terms tends to the same L2 net limit when variables are relabeled accordingly. Consequently the law depends only on the multiset of absolute coefficients. For an infinite nonzero l2 sequence there are only finitely many entries above every positive threshold; they can be listed in decreasing order. Discarding zero terms is harmless. If only finitely many positive magnitudes occur, append zeros.

The total variance of κ_a is s/3+(1-s)/3=1/3, including the endpoints.

## 2. Product compactness of the canonical coefficients

Write W={a_1≥a_2≥...≥0: Σa_j²≤1}. This equals the subset of [0,1]^N defined by the closed ordering constraints and all closed finite constraints Σ_{j≤m}a_j²≤1. It is compact in product topology. A compatible metric is d(a,b)=Σ_j2^(-j)|a_j-b_j|. Every a_j≤j^(-1/2).

This is not l2 norm compactness. The N equal coefficients N^(-1/2), zero-padded, converge coordinatewise to zero and all have norm1. Their Gaussian limit has parameter0; the norm discontinuity is essential, not an error to exclude.

## 3. An explicit uniform analytic remainder

Define sinc(0)=1. For real |x|≤1/2, put u=1-sinc(x). The alternating sine expansion gives 0≤u≤x²/6 and |u-x²/6|≤x⁴/120. Since u≤1/24,
 |log(sinc x)+x²/6|
 ≤ x⁴/120 + u²/(2(1-u))
 ≤ (1/120+1/69)x⁴
 = (21/920)x⁴ < x⁴/40.
The logarithm series estimate uses Σ_{k≥2}u^k/k≤u²/[2(1-u)]. The x=0 case follows by continuity.

For real t, the characteristic function is
 φ_a(t)=exp(-(1-Σa_j²)t²/6) Π_j sinc(a_jt).
L2 convergence justifies passage from finite characteristic functions, since |exp(itx)-exp(ity)|≤|t||x-y|. Fix m so |t|/sqrt(m+1)≤1/2. In the tail, all sinc factors are positive. Summing the explicit remainder yields
 R_m(a,t)=Σ_{j>m}[log sinc(a_jt)+(a_jt)²/6],
 |R_m(a,t)|≤t⁴/(40(m+1)),
since Σ_{j>m}a_j⁴≤a_{m+1}²Σ_{j>m}a_j²≤1/(m+1). Therefore
 φ_a(t)=H_m(a,t) exp(R_m(a,t)),
 H_m(a,t)=[Π_{j≤m}sinc(a_jt)] exp(-(1-Σ_{j≤m}a_j²)t²/6).
Since |H_m|≤1,
 |φ_a(t)-H_m(a,t)|≤exp(t⁴/[40(m+1)])-1.
This holds uniformly over W, including norm1 parameters. The expression never divides by a head factor, so head zeros create no gap.

If a^(n) tends coordinatewise to a, H_m(a^(n),t) tends to H_m(a,t) for fixed m. Letting m increase in the uniform error proves φ_{a^(n)}(t)→φ_a(t) for every real t. Lévy's continuity theorem gives κ_{a^(n)}⇒κ_a. Hence K={κ_a:a∈W} is compact in the weak topology and closed in the Hausdorff space P(R).

## 4. Canonical injectivity and completeness

For complex z in a fixed compact disk, sinc(a_jz)-1 is bounded by C_R a_j² for all sufficiently large j, from its power series. The sum of these bounds converges. Eventually these terms have modulus≤1/2, so the principal-log tail converges uniformly absolutely and its exponential is nonzero. Thus Π sinc(a_jz) is entire by locally uniform convergence, with zeros exactly the zeros of finite head factors; the Gaussian factor is nonzero. There are only finitely many factors vanishing at any fixed positive point because every such coefficient is at least π/z.

If a_1>0, the least positive real zero is π/a_1. Its multiplicity is exactly the number of coordinates equal to a_1, finite since Σa_j²≤1. No smaller coefficient vanishes there: 0<a_jπ/a_1<π. The parameter0 gives the zero-free function exp(-t²/6). Equal laws have equal characteristic functions; their entire extensions agree by the identity theorem. Recover the largest coefficient and its multiplicity from the first zero, divide out those finitely many sinc factors using removable analytic extensions, and repeat. If one list terminates, the remaining Gaussian is zero-free, forcing termination of the other list. If neither terminates, this recovers every fixed coordinate. Therefore a↦κ_a is injective on W. It is not injective on raw signed/permuted l2, nor is such injectivity needed.

A continuous bijection from compact W to Hausdorff K has continuous inverse. Thus it is a homeomorphism. K is complete for the Prohorov metric: that metric is complete on P(R), because R is complete separable, and K is closed. Alternatively compactness in this metric already implies completeness. In particular any sequence of E_N laws has a weakly convergent subsequence, and every actual limit lies in K.

## 5. Every proposed law is attained along all dimensions

Fix arbitrary unsorted real a∈l2 of norm≤1. For every N≥2 set r_N=floor√N and q_N=N-r_N. Retain the first r_N entries; append q_N equal coefficients
 c_N=sqrt((1-Σ_{j≤r_N}a_j²)/q_N).
The resulting vector has norm exactly1. Also c_N²≤1/q_N→0 and q_Nc_N²→1-||a||². Its retained sum tends in L2 to S_a. The independent filler characteristic function equals sinc(c_Nt)^(q_N); for sufficiently large N the preceding bound shows
 q_N log sinc(c_Nt) = -q_Nc_N²t²/6 + error,
 |error|≤t⁴q_Nc_N⁴/40≤t⁴/(40q_N)→0.
Thus the filler converges to normal variance(1-||a||²)/3, also when that variance is0. Independence of the two parts factors their characteristic functions, giving the law limit κ_a. Choose any unit vector at N=1.

For ordered a, the rearranged retained-plus-filler vector b^(N) also satisfies for every j≤r_N:
 a_j≤b_j^(N)≤max(a_j,c_N).
At least j retained entries are≥a_j, proving the lower bound; only the preceding j-1 retained entries can exceed max(a_j,c_N), proving the upper bound. Ties cause no problem. Fixed zero coordinates occur only after the finite positive support, and fillers tend0. Infinite positive support is controlled one fixed index at a time.

If a=0 this is the equal-coordinate Gaussian limit. If a has finite positive support, retained sums are eventually constant. If ||a||=1, filler variance tends0 and the infinite uniform series remains. No absolute summability or extra tail condition appears. Necessity from compact closed K and this all-N construction proves the original limit set exactly, in weak or equivalently Prohorov topology.

## 6. What this proves and what it imports

The preceding deductions prove the intermediate limit-law set and canonical parameterization. They do not derive the distribution of a random direction's coefficient statistics, so they do not prove the full LDP. The source's full LDP is settled by the exact primary published Theorem A, identified in SOURCE_MATCH_VERDICT.md. There is no mathematical gap in the limit-set verification and no new discovery claim.
