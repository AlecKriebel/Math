# Independent boundary and invalid-shortcut controls

These controls deliberately challenge conclusions stronger than the final manuscript. None falsifies the stated final theorem. They explain why its uniformity, normalization, moment, and endpoint conditions are necessary.

## 1. A direct marked-intensity calculation

For an unconditioned Poisson assembly with independent Gamma(2j,1) marks divided by 2q, the intensity density at x>0 is

    ρ_q(x) = Σ_(j≥1) [ζ(2j)/(2j)]
                        [2q e^(−2qx)(2qx)^(2j−1)/(2j−1)!]
           = e^(−u)/x Σ_(m≥1) [cosh(u/m)−1],   u=2qx.

Every summand is nonnegative, so Tonelli justifies both exchanges of sums. This identity is independently derived here; it was not read from a supplied audit or verification program.

The m=1 contribution to xρ_q(x) is exactly (1+e^(−2u))/2−e^(−u). For m≥2, Taylor's theorem gives

    cosh(u/m)−1 ≤ (u²/(2m²)) cosh(u/2).

Therefore

    |xρ_q(x)−1/2|
       ≤ e^(−u)+(1/2)e^(−2u)
         +(u²/2)e^(−u)cosh(u/2) Σ_(m≥2)m^(−2).

For each fixed 0<a<b<∞ this tends uniformly to zero for x∈[a,b] as q→∞. It independently confirms the factor 1/(2x), the disappearance of the all-multiplicity zeta correction at intermediate scale, and the uniform boundedness of the unconditioned marked mass on compact windows.

It also gives another direct proof route for marked factorial moments: in the exact conditional-assembly selected-component sum, restrict each selected size to j≤Lq for fixed L>2b. There the coefficient ratio is uniformly 1+o(1) for each fixed moment order. For the omitted tuples whose total size is ≤n/2, the coefficient ratio is bounded and the Gamma tails give an error O(e^(−cLq)). For the tuples with total size >n/2, at least one j≥n/(2r), and its mark has probability e^(−c_r n); the C√n ratio and logarithmic weight sums are negligible. The remaining products of marked masses converge by the explicit density formula above. This obtains the marked Poisson factorial moments directly, corroborating the manuscript's Lipschitz smoothing route. Normalization and uniform integrability still require the manuscript's concentrated-total and higher-moment arguments.

## 2. Fixed microscopic q cannot use the intermediate intensity

The same exact density displays the boundary obstruction. For u≥0,

    cosh(u/m)−1 ≤ (u²/(2m²))cosh(u).

For the window [1,2], this implies

    ∫_1^2 ρ_q(x)dx ≤ 3ζ(2)q²cosh(4q).

Set q=1/100. The elementary inequalities ζ(2)<2 and cosh(1/25)≤1/(1−(1/25)²/2)=1250/1249 give

    ∫_1^2 ρ_(1/100)(x)dx < 3/4996 < 1/1000,

whereas (log2)/2≥1/4. Thus the 1/(2x) claim cannot be extended to q fixed. In the conditional model, the h-ratio tends to one for fixed selected sizes; Gamma tails control the remaining sizes, so this is a genuine microscopic limiting intensity, not merely a finite-n observation. It is consistent with the final theorem excluding gs_g=O(1).

## 3. Macroscopic s cannot give the claimed Poisson count

Fix s=1/10 and use the rescaled window [1,2]. Since the normalized areas sum to one, at most ten cylinders have area in [1/10,1/5], deterministically at every genus. Any weak limiting count is supported on {0,...,10}. Poisson((log2)/2) has positive probability above ten. Therefore extending the same conclusion to constant s is impossible. The manuscript excludes this regime.

## 4. Normalized Gamma marks are dependent

Condition on the two-component composition (1,1), so (X_1,X_2)~Dirichlet(2,2). Direct beta integration gives

    P(X_1∈[1/10,1/5])
       = ∫_(1/10)^(1/5) 6x(1−x)dx = 19/250 > 0.

But the two coordinates sum to one, while two values in this interval sum to at most 2/5. Hence

    P(X_1,X_2∈[1/10,1/5]) = 0,

which differs from (19/250)². Applying independent Bernoulli marking to normalized areas would be false. The final proof applies it to independent unnormalized Y_i and only afterward divides by T. The exact controls include normalized Dirichlet second and cross count moments to guard this distinction.

Nor is T independent of the unnormalized marked point process: in a one-component composition, Y_1=T. The final argument needs only the deterministic probability limit T/(2n)→1 and does not assume the false independence.

## 5. Weak macroscopic convergence does not determine moving windows

Take any s_n→0. The partition (1) and the partition

    (1−(3/2)k_n s_n, (3/2)s_n,...,(3/2)s_n)

with k_n appended small parts both converge to (1) in ℓ¹ whenever k_n s_n→0. Yet their counts in [s_n,2s_n] are zero and k_n for all sufficiently large n. Taking k_n=floor(s_n^(−1/2)) makes the latter diverge. Thus even strong macroscopic ℓ¹ convergence can coexist with arbitrarily different moving-window counts. Random macroscopic partitions admit analogous small-mass perturbations. A macroscopic Poisson–Dirichlet limit cannot supply the theorem without additional uniform information. The manuscript supplies that information through total variation of the entire multiset and the exact assembly calculation.

## 6. Total variation does not by itself transfer expectations

Let P_n=δ_0 and Q_n=(1−1/n)δ_0+(1/n)δ_n. Their total variation distance is 1/n→0, but E_(P_n)X=0 and E_(Q_n)X=1. Also E_(Q_n)X²=n, so there is no uniform integrability. A maximum count ≤n does not fix this. The final proof instead combines a polynomial bad-event bound with E K^(2r)=O((log n)^(2r)) and Cauchy–Schwarz. That makes each bad-event r-th moment o(1), exactly the extra control needed.

## 7. Finite checks versus asymptotic proof

`independent_exact_controls.py` uses Euler's even-zeta formula to remove the common π^(2n) factor, leaving rational weights. It independently compares ordered compositions, integer-partition count weights, coefficient recurrences, selected-component sums, direct Bernoulli count generating polynomials, and normalized integer-Dirichlet polynomial integrals. These controls catch the 1/k! and repeated-size factors, the h-ratio, Gamma/Dirichlet shape conventions, and first/second/cross-count algebra. Finite agreement alone cannot verify all q_n or geometric asymptotics. Those rely on the explicit estimates in `INDEPENDENT_DERIVATION.md` and the specified published inputs.
