# Independent check of the only imported stochastic limit

The pinned preprint is arXiv:0902.0497v1, submitted 3 February 2009, with front-page typesetting date March 22, 2022. Fresh bytes are 424,962 and SHA-256 `de4d91bff1cde45c02298d9f7f49f34790b6c4043232eb6ef5da999af3128ebf`. I read its definitions and complete critical proof body, not only Theorem 1.1 or the abstract. Source pages 3, 11 and 12 were also visually inspected.

## Needed consequence and exact convention

Equations (4)–(5), p.3, are exactly ∫B¹dB² and its left Euler rule. Section 2.2, pp.6–7, defines the analytic-approximation second-level integral; Proposition 2.3 supplies its Lᵖ convergence and Chen relation for H>1/4. The finite decomposition at Section 3, p.9, expresses the Euler error as the sum of the cell iterated integrals. That decomposition follows also by applying Chen's relation finitely many times. No lower bound for optimal approximation is used.

Let I_j=∫_j^(j+1)(B¹_s−B¹_j)dB²_s and c_r=E[I_0 I_r]. The source's scaling identity (21) and stationarity imply exactly

\[
E|X_T-L_m|^2=T^{4H}m^{-4H}\left[mc_0+2(m-1)c_1+2\sum_{r=2}^{m-1}(m-r)c_r\right].
\]

All cell areas are L² by Proposition 2.3, so c_0<∞ and |c_1|≤c_0 by Cauchy–Schwarz. The source's regularized covariance calculation, (26), p.11, is nonsingular for r≥2 and gives

\[
c_r=H^2(2H-1)^2
\int_0^1\int_r^{r+1}\int_0^{s_1}\int_r^{s_2}
|u_1-u_2|^{2H-2}|s_1-s_2|^{2H-2}\,du_2du_1ds_2ds_1.
\]

Since both distances are at least r−1, each integrand is at most (r−1)^(4H−4), and the integration domain has volume 1/4. Thus

\[
0\le c_r\le \tfrac14H^2(2H-1)^2(r-1)^{4H-4}\quad(r\ge2).
\]

Consequently the variance is bounded by

\[
T^{4H}m^{-4H}\left[3mc_0+\tfrac12H^2(2H-1)^2m\sum_{q=1}^{m-2}q^{4H-4}\right].
\]

An empty sum means zero, so this includes m=1,2. When H<3/4 the sum is bounded by 1+1/(3−4H), using the decreasing-series integral bound. At H=3/4 it is at most 1+log m. When H>3/4 it is at most 1+(m^(4H−3)−1)/(4H−3). Hence

\[
E|X_T-L_m|^2\le C_HT^{4H}
\begin{cases}
m^{1-4H},&1/4<H<3/4,\\
m^{-2}(1+\log m),&H=3/4,\\
m^{-2},&3/4<H<1.
\end{cases}
\]

Every bound tends to zero. At H=1/2 the direct Brownian computation is T²/(2m). This provides the entire required Euler L² convergence while retaining the legitimate analytic-area construction input. It does not depend on the preprint's unnecessary exact asymptotic coefficients.

## A source-body defect that must not be promoted

Equation (27), p.12, declares the sum over all |i−j|>1 to be little-o of m^(1−4H) for H<1/2. This is false. From (26), c_2>0 whenever H≠1/2: the coefficient and integrand are strictly positive. In fact the distances are at most 3 for lag two, giving the explicit lower bound

\[
c_2\ge\tfrac14H^2(2H-1)^2 3^{4H-4}>0.
\]

The two lag-two diagonals alone yield

\[
m^{4H-1}T^{-4H}\sum_{|i-j|>1}|E[J_i^{(m)}J_j^{(m)}]|\ge2(1-2/m)c_2,
\]

whose liminf is positive. The source's claimed sum of all off-diagonal lag powers also confuses a summable single-lag sequence with the double sum, which contains m−r copies of lag r. The displayed v1 rough coefficient omits strictly positive distant-lag contributions; its smooth coefficient derivation also makes unjustified O(1) replacements of double sums. I do not accept those displayed exact coefficients from that version.

This defect is in the external preprint. The submitted proof never uses the coefficient, a rate lower bound for Euler, or a limiting law. Its needed convergence remains independently justified by the valid calculation above. A source-scope note should distinguish those facts rather than give the faulty exact-coefficient presentation an unqualified source-proof endorsement. No statement is made here about journal-identical bytes: the journal body could not be fully retrieved in this audit.

## Identification with the canonical polygonal area

For the actual polygonal iterated integral P_m, direct integration gives

\[
P_m-L_m=Q_m=\tfrac12\sum_{k=0}^{m-1}\Delta_kB^1\Delta_kB^2.
\]

Independence of the components, with Δ=T/m and ρ_H(r)=((r+1)^(2H)+|r−1|^(2H)−2r^(2H))/2, gives exactly

\[
E[Q_m]=0,\qquad E[Q_m^2]=\tfrac14\Delta^{4H}\left[m+2\sum_{r=1}^{m-1}(m-r)\rho_H(r)^2\right].
\]

For r≥2, the integral second-difference formula gives

\[
|\rho_H(r)|\le H|2H-1|(r-1)^{2H-2}
\le H|2H-1|2^{2-2H}r^{2H-2}.
\]

Squaring and using the same power-sum regimes proves Q_m→0 in L² throughout H>1/4. Lag one is finite, including m=1; at Brownian H all nonzero lags vanish. Thus the analytic Euler limit equals the polygonal limit, in particular along dyadics defining the canonical lift. The bridge in AREA_CONVENTION_CHECK.md is correct.

At H=1/4, E[Q_m²]≥T/4 from the diagonal term, so this bridge does not extend to that endpoint. At H=1, Q_m does vanish (variance T⁴/(4m²)); the witness proof instead fails because D_H diverges and the canonical area is recoverable from endpoints. These are different endpoint mechanisms.

## Prior smooth result and boundaries

The freshly read author-uploaded Neuenkirch–Shalaiko preprint is dated July 14, 2015, uploaded July 23, 2015. Its complete mathematical body has been read online: Theorem 1, p.3; Brownian Remark 5, p.4; Theorems 2–3, pp.4–5; conditional expectation construction, pp.6–7; entire main proof, pp.7–10. Theorem 1 assumes H>1/2 and yields positive scaled liminf and finite limsup; it does not prove an exact normalized-error limit. The main mechanism is a lower covariance bound for increments plus strong local nondeterminism. Theorem 2's following paragraph explains the impossibility of that increment lower bound for H<1/2 by taking all coefficients equal to one. The submitted localized upper-Gram proof does not import this false rough-range extension.

Fresh Elsevier API metadata confirms journal DOI `10.1016/j.jco.2015.09.008`, Journal of Complexity, April 2016. Current author-university bibliography confirms volume 33, pp.107–117. The actual journal PDF/full body was not obtained; no journal-byte or visual-PDF inspection is claimed. Retained web response text is private and hash-pinned as tool-extracted author text, not as original PDF/HTML bytes.
