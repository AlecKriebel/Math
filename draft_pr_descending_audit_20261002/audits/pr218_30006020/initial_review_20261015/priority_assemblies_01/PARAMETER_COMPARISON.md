# Checkable comparison with logarithmic assembly theory

This is the auditor's derivation, not a claim that a located earlier paper states the geometric conclusion. Sources and theorem locations are pinned in SOURCE_PINS.json. The candidate was read only from the frozen `initial_review_20261015/submitted/.../30006020/CANDIDATE.md`.

## 1. The exact discrete law is already DGZZ's weighted permutation law

Let `a_j = ζ(2j)/(2j)`, `H(z)=exp(Σ a_j z^j)`, and `h_n=[z^n]H(z)`. If `c_j` counts parts of size `j`, the candidate's ordered composition law pushes forward to

`P(C=c) = 1{Σ j c_j=n} h_n^{-1} ∏ a_j^{c_j}/c_j!`.

The factor `k!/∏c_j!` counts the orderings of the composition and cancels the `k!` in the candidate. For independent `Z_j~Po(a_j)`, conditioning on `Σ_{j≤n}jZ_j=n` gives exactly this expression. No integer interpretation of the weights is required: the conditioning relation is a probabilistic identity.

DGZZ §1, equations (1.7)–(1.8), explicitly uses permutation cycle weights `θ_j=ζ(2j)/2`. Its Lemma 3.6, equations (3.20)–(3.23), gives ordered compositions of the same weights `∏ θ_{j_i}/j_i` divided by `k! W_n`. Thus `W_n=h_n`, and the candidate's composition law, before marking, is exactly `P_{n,∞,1/2}` of DGZZ. Sampling a permutation from this law and ordering its cycles uniformly gives the candidate composition. This is positive exact prior overlap.

## 2. ABT 2000 applies with parameter 1/2 and no mesoscopic rate loss

Write `A=ζ(2)/2`. Then `a_j≤A/j`,

`j E Z_j = ζ(2j)/2 → 1/2`,

`j P(Z_j=1) = (ζ(2j)/2) exp(-a_j) = 1/2+O(1/j)`.

For `ℓ≥2`,

`j P(Z_j=ℓ) ≤ A^ℓ/(ℓ! j^{ℓ-1}) ≤ j^{-1} A^ℓ/ℓ!`.

Consequently ABT's ULC holds with `θ=1/2`, `e(j)=C/j` and suitable summable `c_ℓ`, with `Σ ℓ c_ℓ<∞`. Also `Σ e(j)/j<∞`, so its stronger tail comparison is available. These checks are more specific than merely observing `a_j~1/(2j)`.

ABT Theorem 3.1 (Ann. Probab. 28 (2000), p.1630) gives

`d_TV(L(C_1,...,C_b), L(Z_1,...,Z_b)) → 0`

for **every** `b=b_n=o(n)`. Put `q_n=ns_g`. For any fixed compact union of windows with upper endpoint `B`, take `b=ceil(Bq_n)`. Since `q_n→∞` and `q_n=o(n)`, the theorem applies. The independent point process `Σ Z_j δ_{j/q_n}` has intensity `Σ a_j δ_{j/q_n}`, converging vaguely to `dx/(2x)` by Riemann sums. For disjoint windows the independent counts are exactly independent Poisson with means tending to `log(b_i/a_i)/2`. Thus the candidate's unmarked mesoscopic process is an immediate prior-theorem corollary, for arbitrary slow `q_n→∞` and arbitrary slow `n/q_n→∞`.

ABT Theorem 3.2 also compares the whole tail `(C_j)_{j>b_n}` to the `ESF_n(1/2)` tail in TV for every `b_n→∞`, `b_n=o(n)`, because `Σ e(j)/j<∞`. It is stronger than macroscopic coordinate convergence but does not identify cylinder areas.

## 3. The factorial-moment formula is an existing assembly identity

AT 1994, Lemma 5, equation (126), printed pp.136–137, becomes

`E∏ (C_j)_{r_j} = 1{R≤n} [h_{n-R}/h_n] ∏ a_j^{r_j}`, where `R=Σ j r_j`.

In its notation take the weighted assembly exponential coefficients `m_j/j! = a_j`, external tilt `1`, and `p(n)=n!h_n`. Equivalently, remove the distinguished parts directly from the preceding probability mass function; this verifies the extension to real positive weights without pretending `m_j` is an integer number of structures.

The candidate's coefficient estimate follows from

`H(z)=(1-z)^(-1/2) B(z)`, `B(z)=∏_{m≥2}(1-z/m²)^(-1/2)`,

where `B` is analytic on `|z|<4`, `B(1)=sqrt(2)`. Hence `h_n~sqrt(2/π)n^(-1/2)`, and

`h_{n-R}/h_n →1` uniformly for `R=o(n)`,

`h_{n-R}/h_n ≤ C sqrt((n+1)/(n-R+1))` for `0≤R≤n`.

The generating-function identity and analyticity are explicitly DL Lemma 6.7 (and DGZZ's earlier related lemma). For each fixed factorial-moment order, windows at scale `q_n` have `R=O(q_n)=o(n)`. Summing the AT formula therefore proves all unmarked joint factorial moments converge to the independent Poisson moments. TV convergence alone would not justify this moment statement.

## 4. Gamma marking has a short rigorous extension, but this is an auditor deduction

Mark each independent Poisson part of index `j` with an independent `Y~Gamma(2j,1)`. Poisson marking/superposition gives the continuous intensity

`ρ(y) = Σ_{j≥1} a_j e^{-y} y^(2j-1)/(2j-1)!`

`     = (e^{-y}/y) Σ_{j≥1} ζ(2j) y^(2j)/(2j)!`

`     = (e^{-y}/y) Σ_{m≥1} (cosh(y/m)-1)`.

This is exactly the functional expression printed in OWR's microscopic statement. It is not legitimate to infer a moving-window geometric theorem from that microscopic weak limit alone.

For `m≥2`, `cosh(y/m)-1 ≤ y² cosh(y/2)/(2m²)`. Separating `m=1` yields

`ρ(y) = 1/(2y) + O(y e^{-y/2})` as `y→∞`.

Thus the independently marked process rescaled by `2q_n` has intensity `2q_n ρ(2q_n x) dx → dx/(2x)` in total variation on every fixed compact subset of `(0,∞)`.

To pass from conditioned to independent marks without a hidden logarithmic restriction, choose

`b_n = floor(sqrt(n q_n))`.

Then `b_n=o(n)` and `b_n/q_n→∞`. ABT Theorem 3.1 plus contraction under a common marking kernel couples all marks of parts `j≤b_n`. Marks from `j>b_n` enter a fixed compact rescaled window only through a Gamma lower tail. For any fixed upper endpoint `B`, eventually

`P(Gamma(2j,1) ≤ 2Bq_n) ≤ exp(-c j)`, `j>b_n`.

The preceding bound on `h_{n-j}/h_n` bounds the expected number of such conditioned intrusions by `C sqrt(n) exp(-c b_n)`, which tends to zero. The independent intrusion tail also vanishes. This proves local TV approximation for the unnormalized marked compact-window process at every permitted rate.

For marked count factorial moments, set `w_j=a_j P(Y_j/(2q_n)∈I)`. The intensity calculation gives `Σw_j=O(1)` and its limit. Independent marking in the AT identity gives the `r`th factorial moment as

`Σ_{j_1+...+j_r≤n} [h_{n-Σj_i}/h_n] ∏ w_{j_i}`.

If all `j_i≤b_n`, the ratio tends uniformly to one because `r b_n=o(n)`. If one index exceeds `b_n`, its exponentially small Gamma tail controls the entire contribution by `C_r sqrt(n)exp(-c_r b_n)`. This proves every fixed joint marked count moment, including arbitrarily slow `q_n→∞`.

Finally, conditional on any composition, `T=ΣY_i~Gamma(2n,1)`. Therefore `T/(2n)→1`. Dilating the marked process by `2n/T` gives the candidate normalized Dirichlet model and preserves its vague limit. Its normalized compact-window count is bounded by the unnormalized count in `[a/2,2b]` on `1/2≤T/(2n)≤2`; the complement has exponentially small probability, and total number of parts is at most `n`. The already proved higher moment bounds imply all normalized count moments converge too.

Conclusion of this calculation: the whole analytic portion of Theorem B is an elementary extension of verified older assembly results. No located primary theorem was found stating this exact Gamma/Dirichlet mixture result. The distinction between a checked deduction and an already published statement must be retained in the priority decision.

## 5. Exact remaining geometric gap

Neither ABT nor AT identifies the random variables with geometric cylinders. To solve the original problem one must still prove the full-area mixture approximation, and enough uniform integrability for geometric counts. DL's exact simplex polynomial mixture, its one-vertex restriction, and the uniform correlator coefficients are unusually close to supplying this bridge. The candidate supplies the latent density comparison and polynomial exceptional-event/moment transfer. A citation to a theorem about Ewens cycles does not replace those steps.

Two falsifiable non-implications help delimit the gap:

- Microscopic and macroscopic limits together do not force mesoscopic behavior. Insert one additional component of mass `s_g` and subtract `s_g` from a macroscopic component. At `gs_g→∞`, `s_g→0`, this alteration is invisible to both fixed-scale endpoint limits but adds one atom at rescaled mesoscopic location `1`.
- Whole-law TV convergence alone does not transfer unbounded moments. A variable equal to `n` with probability `1/n` and zero otherwise is TV-close to zero while its expectation is `1`. The candidate's quantitative bad-event bound and logarithmic total-count moments address a real extra requirement.

The source's requested scale has `q_n=(3g-3)/sqrt(g)~3sqrt(g)` and maps to Poisson mean `log(2)/2`. The factor `2n=6g-6` is the Gamma total parameter. This lane makes no identification of the OWR microscopic printed `4g-4` with `6g-6`; scale invariance makes the mesoscopic intensity insensitive to a fixed dilation, but the microscopic laws must remain distinguished.
