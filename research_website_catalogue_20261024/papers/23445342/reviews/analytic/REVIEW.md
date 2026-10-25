# Independent analytic review — Zenodo 23445342, version 1.0

**Verdict: no mathematical defect identified in the checked central theorem.** The published argument supplies a coherent proof of the stated fixed-law, i.i.d. space-time, one-dimensional coarse endpoint concentration theorem. I independently reconstructed its analytic estimates and quantifiers, inspected the mathematical checker sources, replayed all nine published checkers, and added a separate exact polynomial-based control. This is an AI mathematical review, not conventional human peer review, formal verification, or a certificate of originality.

The strongest supported result is the actual all-diverging-scales theorem, including arbitrary deterministic real alignments and biased strictly elliptic environment laws. It is not limited to polynomially growing target cells. The proof uses a polynomial auxiliary cell size only in an intermediate step; the target scale enters through an expectation that tends to zero with no prescribed rate.

No central analytic gap was found. The remaining evidential boundaries are that this reconstruction is not a machine-checked proof or human expert review, and historical priority/novelty has not been established. The published manuscript explicitly acknowledges those priority limits. No defect was repaired, and no source, website, spreadsheet, Git state or Zenodo record was changed.

## 1. Exact reviewed object and independence

- Title: *Coarse endpoint concentration at every diverging scale for one-dimensional space-time random walks*.
- Author: Alec Kriebel; version 1.0; publication date 2026-10-18.
- Record: <https://zenodo.org/records/23445342>; DOI <https://doi.org/10.5281/zenodo.23445342>.
- Published PDF: `coarse_endpoint_concentration.pdf`, 121,461 bytes, **11 pages**.
- PDF SHA256: `7514e0e456811651fdfb4f2f890f3fe81646d0346789057b561e075ad553bbe6`.
- PDF MD5: `fde5d9bfaaa19009b99e19adf557b6b3`.
- Published ZIP: `coarse_endpoint_verification.zip`, 189,396 bytes.
- ZIP SHA256: `3a4ab05e434138db12d90dbfd1efebae0f101de36a5d674cc56ed04c8595236d`.
- ZIP MD5: `62731823f9cb81e78cc98b4f67426181`.
- Source `main.tex` SHA256: `cb9163437ab912588f8cdbcc10965badeb5a68aef6efb242884a61f4d4fbbfad`.

The first full read used the exact queue-bound local PDF while fresh acquisition was pending. The fresh Zenodo bytes subsequently matched that PDF SHA256, the acquisition receipt, the advertised MD5, the length and page count. `source_identity.json` records final fresh binding; the provisional identity is retained as process history.

I read every published page, the full 336-line authored `verification/submission/PROOF.md`, its complete 238-line `TURN_1.md` and 276-line `TURN_2.md` derivations, the relevant exact TeX formulas, the entire portable verifier and all nine selected mathematical checker sources. The authored support retains historical checkpoint language; its older integer-cell presentation is supplemented by its final real-cell section and the published full proof. Earlier partial checkpoint statuses are not the current theorem status.

I did not read archived reviewer reports/verdicts, the priority ledger, or sibling review opinions before arriving at this verdict. Incidental statements about historical review status embedded in the manuscript, authored proof, README and checker docstrings were disregarded as evidence of correctness. The portable verifier hashes archival files for integrity; this does not mean their verdicts were consulted. The historical `actual_replay_driver.py` was not executed. No other person was contacted.

## 2. Claim, assumptions, and success criterion

The coordinates `p_(s,x)`, for `s >= 0` and `x in Z`, are independent and identically distributed with a **fixed** law satisfying `0 < p < 1` almost surely. Given the environment, the walk starts at 0 and moves from x at time s to x+1 with probability p_(s,x), and to x−1 otherwise. Let

`mu_n^omega(x) = P^omega(X_n=x)`, `alpha_n(x) = E_env mu_n^omega(x)`.

For a deterministic partition P define the full L1 discrepancy

`L_(n,P) = sum_(I in P) |mu_n^omega(I) - alpha_n(I)|`.

This is twice the usual total variation distance. The random object being concentrated is a difference between two endpoint probability distributions; it is not the deviation probability of a single sampled walk.

**Theorem 1, PDF pp. 1–2:** for every deterministic real sequence `M_N > 0` with `M_N -> infinity`, every epsilon > 0 and K > 0, there are finite C and N0 such that, for N >= N0 and every deterministic real alignment b_N,

`P_env(L_(N,P_N) > epsilon) <= C N^(-K)`,

where P_N consists of the cells `[b_N+j M_N, b_N+(j+1) M_N) intersect Z`. Constants may depend on the environment law; the eventual threshold may depend on the chosen sequence. The bound is uniform in the deterministic alignment at each N.

The success criterion for this review was a valid derivation with those quantifiers, without replacing the arbitrary diverging target scale by a polynomial scale, introducing uniform ellipticity, treating the endpoint masses as independent, or applying an annealed statement as a pointwise quenched estimate.

Important scope restrictions:

1. No positive lower support bound for p or 1−p is assumed. Nevertheless the law is fixed and `delta=E[p(1-p)]>0`; constants can deteriorate as delta tends to zero.
2. Coordinates are i.i.d. in both space and time. Mere stationarity, temporal independence alone, static random environment, or general correlated environments are not covered.
3. The divergence of M_N may be arbitrarily slow and nonmonotone. No uniform rate over all diverging sequences is asserted.
4. The target cells may have real lengths; empty cells are harmless. M_N eventually exceeds 1, which is sufficient for intermediate estimates stated for M >= 1.
5. Alignment is deterministic. The theorem is not a simultaneous supremum over random, environment-selected partitions.
6. Nearest-neighbor parity is retained throughout. Coalescing comparison is used only for same-parity starting sites.
7. No fixed microscopic-cell or fine-site endpoint L1 convergence is claimed. Coarse averaging is essential to the statement under review.

## 3. Independent reconstruction of the analytic proof

### 3.1 Replica returns and conditional occupation moments

Set `q=E p`, `a=q(1-q)`, `delta=E[p(1-p)]`, `sigma^2=Var(p)=a-delta`, `v=2q-1`. Strict ellipticity gives `0<delta<=a<=1/4`. Annealed increments are independent signs of mean v because each new time layer is fresh, even when a spatial location is revisited.

Let F_s contain environment layers strictly before s, and `I_s=sum_x mu_s(x)^2`. Two walks independent conditional on the same environment have integral half-difference D. On averaging, D moves to each neighbor with probability a off zero, with probability delta at zero, and otherwise holds. Therefore `E I_t = g_t = P_0(D_t=0)`.

The published return generating function is

`G(z) = 1 / [(1-delta/a)(1-z) + (delta/a)*sqrt((1-z)(1-(1-4a)z))]`.

I reconstructed it using the bounded hitting-transform solution `rho(z)^d` of the off-zero recurrence and a first-return decomposition at zero. The positive square-root branch is required. Since delta <= a and `1-(1-4a)z >= 4a`,

`G(z) <= sqrt(a)/(2 delta sqrt(1-z))`, for 0<z<1.

A generating-function bound alone would not give the desired pointwise return bound. The manuscript supplies the missing coefficient control: reversibility with `pi(0)=a/delta`, `pi(d)=1` otherwise, and holding probabilities at least 1/2 make P a positive self-adjoint contraction on l2(pi). Consequently `g_t` is decreasing, as an integral of lambda^t over a positive measure on [0,1]. Combining this monotonicity with the generating function at `z=n/(n+1)` gives `g_n <= C/sqrt(n+1)`. The infinite reversible measure causes no problem: invariance and Jensen give the l2 contraction, and the origin indicator has finite norm.

For the backward profile `u_t(d)=P_d(D_t=0)`, set `b_t(d)=u_t(d)-u_t(d+1)`. At d=0,

`b_(t+1)(0)=(1-2delta-a)b_t(0)+a b_t(1)`;

off zero, the coefficients are a, 1−2a, a. They are nonnegative because `1-2delta-a>=1-3a>=1/4`. This gives a radial maximum at zero. Conditioning on F_s fixes only the initial replica distribution, so

`E[I_(s+t)|F_s] = sum_(x,y) mu_s(x)mu_s(y)u_t((x-y)/2) <= g_t`.

Ordering the k indices in an occupation-moment expansion, then successively conditioning at earlier selected times, yields

`E[(sum_(j<L) I_(s+j))^k | F_s] <= k! (sum_(j<L) g_j)^k <= k! C^k L^(k/2)`.

Repeated indices are legitimate: they use `I_t<=1=g_0`, not a spurious independence claim. Markov's inequality at `N^eta sqrt(L)` gives `k! C^k N^(-k eta)`. A fixed k can be selected separately for any requested inverse-power exponent. These estimates concern deterministic intervals, which is exactly how later dyadic blocks are selected.

### 3.2 Environmental martingales and real-cell expectation

For deterministic bounded f, `M_s=mu_s(T_(n-s) f)` is the layer-exposure martingale. Its increment is

`sum_x mu_s(x)(p_(s,x)-q)[T_(n-s-1)f(x+1)-T_(n-s-1)f(x-1)]`.

Fresh within-layer independence gives conditional variance `sigma^2 sum_x mu_s(x)^2 h_s(x)^2`. A 1/r-Lipschitz test has increment bound 2/r and predictable variation at most `C r^(-2) sum_s I_s`.

The exponential-supermartingale argument establishes the joint-event inequality

`P(|sum D_s|>=u, Q<=w) <= 2 exp[-u^2/(4(w+bu))]`.

The chosen exponential parameter lies in the domain of the elementary bound `e^x<=1+x+x^2`. Crucially, the proof applies this to a joint event; it does not condition a martingale on a future good-variation event and assume its increments remain centered.

The independent centered increment maximum bound and independent-input bounded differences are also derived directly. The former controls the entire path segment, which is required when killing trajectories later. Its range bound is 2 for the centered sign increments, irrespective of bias.

Lemma 3 (PDF pp. 5–6) starts from the actual parity-lattice binomial kernel. Fourier estimates give a peak of order `(t+1)^(-1/2)` and adjacent-binomial-index difference of order `(t+1)^(-1)`. Unimodality gives total variation of the shift by two as exactly twice the peak. These are not aperiodic estimates inadvertently applied to a periodic walk.

For interval cells of real length M, each cell contains at most M+1 sites. The cell-gradient maximum and sum of absolute gradients imply

`sum_I h_I(x)^2 <= C min((t+1)^(-1), (M+1)(t+1)^(-3/2))`.

Orthogonality of martingale differences and the replica bound then give

`sum_I Var(mu_n(I)) <= C n^(-1/2)[1+log(1+min(M+1,sqrt(n)))]`.

The time sum is controlled by splitting at n/2 and, in the late part, at `(M+1)^2`. A deterministic window of radius B sqrt(n) around vn meets at most `2B sqrt(n)/M+2` cells. Cauchy–Schwarz inside, and annealed Chebyshev plus expectation outside, give

`E L_(n,P) <= C sqrt((B/M+n^(-1/2))*[1+log(1+min(M+1,sqrt(n)))]) + C/B^2`.

The square root covers the full product; this was checked in the exact TeX. Fix B, let n,M tend to infinity, and then let B tend to infinity. This constructs a deterministic bound `rho(n,M)<=2` tending to zero jointly as n,M diverge, uniformly in alignment. It supplies no fixed quantitative rate in M, and no such rate is used later.

### 3.3 Polynomial auxiliary scale without an illicit target-scale restriction

Proposition 4, PDF pp. 6–7, proves superpolynomial concentration for integer M >= n^gamma with fixed gamma>1/4. For gamma in (1/4,1/2), put

`d=gamma-1/4`, `beta=1/4+d/2`, `eta=d/4`, `r=n^beta`,
`h=floor(n^(2beta)/(log n)^2)`, `m=n-h`.

Average only the final h layers: `nu_n=mu_m T_h`. For bounded f, smoothing gives `b<=C/sqrt(h)` and `Q<=C sum_(s<m) I_s/(n-s)`. Deterministic dyadic time blocks and the occupation-moment lemma give one common superpolynomial-probability good event, on which `Q<=C n^eta/sqrt(h)`. The fixed-threshold tail exponent is of order `n^(beta-eta)/log n`.

The central window touches `J<=C n^(1/2-gamma) log n+2` cells, so its L1 discrepancy is the maximum of 2^J deterministic bounded sign tests. The exponent margin

`beta-eta-(1/2-gamma)=5d/4>0`

is sufficient to absorb this entropy. The exceptional overlap event is charged only once. Cells outside the window are handled by Markov's inequality applied to a superpolynomially small annealed tail.

To restore the last h quenched layers, a periodic 1/r-Lipschitz majorant bounds old mass within distance r of the boundary grid shifted by vh. The binomial-index residue class has modulus `M/gcd(2,M)`, so the physical residue mass bound is `2/M+2 max b_j`. Counting O(r+1) such residues gives expected boundary mass `C(r+1)/M+C(r+1)/sqrt(m)=o(1)` uniformly in real alignment. The martingale variance exponent has the strict margin

`2beta-1/2-eta=3d/4>0`.

The centered final displacement exceeds r with annealed probability `C exp[-c(log n)^2]`, and hence its quenched conditional probability exceeds any fixed threshold with superpolynomially small environment probability. Coupling through the real location `X_m+vh` then restores the actual coarse law. Half-open boundary coincidences are included in the boundary strip.

This proposition is a valid intermediate result. It does not alone settle arbitrary diverging M_N, and the manuscript does not treat it as doing so.

### 3.4 Conditional smoothing using coalescence

The final argument (PDF pp. 8–10) chooses

`ell=floor(N^(3/4))`, `m=N-ell`, `H=ceil(N^(5/16))`,
`r=N^(3/8)`, `R=ceil(N^(3/8) log N)`, `eta=kappa=1/32`.

Lemma 5 bounds the old mass of each member of a prescribed O(N)-sized family of intervals containing at most 10R+10 sites. A smooth majorant has mean `O(N^(-1/8)log N)=o(N^(-1/32))`. One common overlap event bounds its variation by `C N^(-7/32)`; the increment bound is `2N^(-3/8)`. At threshold proportional to `N^(-1/32)`, the joint-event martingale exponent is of order `N^(5/32)`. Union over O(N) intervals preserves a superpolynomial tail. The interval family later used is deterministic.

Lemma 6 couples two quenched walks independently until they meet and jointly afterward. Same parity and nearest-neighbor steps preserve their ordering until meeting. Before meeting, fresh environment variables are at different sites, so after environmental averaging the half-gap is the homogeneous lazy chain with neighbor probabilities a. This is different from the sticky common-environment two-replica chain at equality; the proof does not confuse their roles.

Reflection, including holding steps, gives survival from positive gap d as

`sum_(z>=1)[p_ell(z-d)-p_ell(z+d)] = sum_(j=1-d)^d p_ell(j)`.

The homogeneous peak bound therefore yields

`E_future ||K_ell^omega(x,.)-K_ell^omega(y,.)||_1 <= C|x-y|/sqrt(ell+1)`

for same-parity x,y, capped by 2. This is an averaged bound on quenched-kernel distance, not an assertion that fixed quenched environments are independent across paths.

Within each H-cell, replace the old quenched conditional distribution by the old annealed conditional distribution while keeping the cell mass. Call it mu'. Null annealed cells have zero quenched mass: both laws live on the same finite reachable parity support. The replacement coupling has displacement less than H, and

`E_future ||mu_m K_ell - mu' K_ell||_1 <= C H/sqrt(ell)`,
`||mu'-alpha_m||_1 = L_(m,P_H)`.

Markov-kernel contraction and convexity of L1, applied to the annealed mixture of starting sites, give

`E[F|F_m] <= L_(m,P_H)+C H/sqrt(ell)+rho(ell,M_N)`,

where `F=||mu_m K_ell(P_N)-alpha_N(P_N)||_1`.

The start shift changes only a deterministic target alignment, so Lemma 3's uniformity is exactly sufficient. There is no assumption that kernels from different starts are independent. The deterministic errors vanish: `H/sqrt(ell)=O(N^(-1/16))`, and `rho(ell,M_N)->0` for every diverging M_N. Proposition 4 applies only at the auxiliary scale H.

### 3.5 Independent moving strips and restoration of killed mass

Kill a last-segment path when it first leaves the tube `|X_(m+t)-x-vt|<=R`. The resulting K-dagger is a subprobability kernel. The maximal annealed inequality gives, uniformly in the start and old environment,

`E_future[1-K-dagger(x,Z)] <= d_N <= C exp[-c(log N)^2]`.

Partition fresh environment coordinates into deterministic disjoint strips

`S_k={(t,y): 0<=t<ell, kR<=y-vt<(k+1)R}`.

These are independent input vectors, including for irrational drift v. Only finitely many reachable coordinates are relevant. Before killing, every used site has `y-vt` in `[x-R,x+R]`. Therefore changing strip k can affect the killed row only if its starting point belongs to

`J_k=[kR-R-1,(k+1)R+R+1] intersect Z`.

This influence claim holds for every alternative value of the strip input, not just along a previously sampled path. Killing at the first exit is essential: merely checking the endpoint would not localize the variables read.

Set `w_k=mu_m(J_k)`. At most O(N) strips are relevant, each J_k satisfies the old-mass lemma, and every old point lies in at most six influence intervals. Thus `sum w_k<=6` and `sum w_k^2<=6 max w_k`. Changing one strip changes the mixed killed endpoint subprobability measure in L1 by at most 2w_k, hence changes its L1 distance from the target by at most 2w_k. Conditional bounded differences yields

`P(F-dagger-E[F-dagger|F_m]>t | F_m) <= exp[-t^2/(12 max w_k)]`.

No independence of overlapping start cones or endpoint masses is required. The independent objects are the disjoint environment strips. Lemma 5 gives `max w_k<=N^(-1/32)` outside a superpolynomially small event, producing `exp[-c_t N^(1/32)]` fixed-deviation tails.

Finally let `D=1-mu_m K-dagger(Z)`. Positivity of the lost subkernel gives

`|F-F-dagger|<=D`, `E[D|F_m]<=d_N`,
`E[F-dagger|F_m]<=E[F|F_m]+d_N`, `P(D>t|F_m)<=d_N/t`.

For sufficiently large N, the conditional mean is at most epsilon/4 outside the old coarse-scale bad event. If D<=epsilon/4 and F>epsilon, the killed norm exceeds its conditional mean by more than epsilon/2. The resulting bound is

`P(F>epsilon) <= O(N^(-K)) + exp[-c_epsilon N^(1/32)] + 4d_N/epsilon`.

Both explicit remainders are superpolynomial. This proves the actual target theorem, with the threshold dependence on M_N coming only through the vanishing deterministic expectation. I found no hidden exchange of limits, adaptive-partition step, lost factor of parity, or law-uniform claim in this closure.

## 4. Primary-source and import audit

No specialized outside result is imported as a missing analytic lemma: the manuscript gives its return estimate, occupation moments, martingale bound, maximal inequality, bounded differences, binomial estimates, coalescence estimate and final concentration argument. The spectral theorem is used in its standard self-adjoint contraction form, with the required positivity and reversible measure verified in the text.

The historically consequential reference was freshly checked against [the original EMS/Oberwolfach report](https://ems.press/content/serial-article-files/46239), DOI [10.4171/OWR/2009/38](https://doi.org/10.4171/OWR/2009/38). Printed pp. 2151–2152 were read, and p. 2151 was also visually inspected. Its Theorem 1 gives the analogous coarse endpoint comparison with faster-than-any-polynomial environment probability for i.i.d. nearest-neighbor elliptic space-time walks in transverse dimension at least two; the immediately following Conjecture 1 asserts failure in transverse dimension one. Thus the manuscript's claimed relationship to that historical statement is accurate in the specified model. The report's later martingale lemma is not silently imported in place of the manuscript's own argument.

The 64-page source PDF has SHA256 `4642f579215a28b58adb465e3eb3f1512b6dde596505df5a64b3eaae69b86847`; its retrieval receipt is retained separately. The source's apparent Z versus Z^d typographical shorthand does not affect the one-dimensional comparison.

This is **not an exhaustive priority audit**. I did not independently clear every cited historical paper, certify that an old conjecture remained open in 2026, or verify the historical circumstances of earlier AI reviews. The paper itself explicitly leaves four earlier full-text anticipation questions unresolved and disclaims firstness. Those unresolved literature questions do not invalidate a self-contained proof, but they prevent a claim here that this is the first solution or a novel method. Method-credit and background references are not treated as independently verified theorem dependencies by this verdict.

## 5. Reproducibility and separate exact controls

The published portable runner was read before execution. It verifies the whole 92-file payload manifest, including 32 preserved native Git-blob pins, then isolates selected checker sources in temporary directories. It installs nothing and makes no network calls. Its fresh replay passed:

| Published checker | Exact finite assertions |
|---|---:|
| `submission/check_turn2.py` | 50,324 |
| `submission/check_turn3.py` | 17,148 |
| `submission/independent_review/independent_check.py` | 31,888 |
| `audits/math_replica_family_01/independent_exact_checks.py` | 37,140 |
| `audits/math_replica_family_01/excluded_boundary_checks.py` | 197 |
| `audits/math_martingale_family_01/independent_exact_controls.py` | 197,758 |
| `audits/math_coalescence_family_01/independent_exact_checks.py` | 22,225 |
| `audits/reproduction_history_family_01/independent_finite_check.py` | 19,340 |
| Optional `submission/check_turn1.py`, SymPy 1.14.0 | 486 |
| **Total** | **376,506** |

The first eight ran under the published portable verifier with Python 3.12.14. The optional source was then copied to an isolated temporary directory and executed directly with an existing read-only SymPy 1.14.0 dependency path. It was not silently counted as part of the default runner. Both result receipts record the distinction. All scripts were run with assertions enabled; archived outputs were not substituted for actual execution.

These counts are parameter instances, not independent theorems. They corroborate replica transitions, exact conditional moments, martingale variance, parity residues, killed coalescence, real-cell handling, strip sensitivity and exponent arithmetic. They do not supply the infinite-time theorem.

I separately wrote `independent_controls.py`, without importing any published checker. Its mechanism is **exact multiaffine polynomial expansion in the environment variables**, followed by integration using first and second moments, rather than complete enumeration of environmental assignments. It passed **3,090 exact assertions in 17 families**, including:

- normalization and annealed means as polynomial identities;
- replica overlap and 429 real-cell variance identities checked against an independently evaluated martingale decomposition;
- formal dependency sets of killed-kernel polynomials, checking that every surviving variable lies inside the live tube and has its start in the associated strip influence interval;
- near-arrow and biased laws, deterministic strictly elliptic laws, rational noninteger cell widths and alignments, and drift close to ±1;
- exact exponent margins for gamma approaching 1/4;
- explicit omitted-hypothesis controls: an arrow law with delta=0 has a large coarse discrepancy; a single globally selected p gives an almost-unit coarse discrepancy despite strict ellipticity; opposite-parity shifted endpoint laws have L1 distance exactly 2.

The last two controls explain why i.i.d. coordinates and same-parity coupling are substantive assumptions. They are excluded models, not counterexamples to the theorem. Finite controls at N=256 also do not by themselves prove an asymptotic countertheorem. The analytic arrow boundary is independently transparent: quenched endpoint mass is a point mass while annealed cells with M_N=o(sqrt(N)) have vanishing mass.

## 6. Disposition, strongest claim, and exact remaining gap

**Strongest mathematically supported claim:** for every fixed i.i.d. strictly elliptic nearest-neighbor space-time environment law in one transverse dimension, the full L1 discrepancy between quenched and annealed endpoint laws, grouped into deterministic intervals of any real lengths M_N tending to infinity, exceeds any fixed epsilon with probability O(N^(-K)) for every fixed K, uniformly in deterministic alignment. Biased laws, parity and arbitrarily slow nonmonotone divergence are covered. The asymptotic proof, not the finite assertion count, supports this conclusion.

**Exact defect status:** none identified in the central theorem, its supporting lemmas, their quantifier linkage, or the fresh mathematical replays. There is no requested repair and no deferred correctness defect from this review.

**Exact remaining gap:** this is not a human expert or formal proof certificate, and it does not settle novelty, first resolution, independent discovery, literature completeness, or journal suitability. The complete original historical anticipation question remains unresolved by this review. Additional source access or expert mathematical scrutiny would be recorded as research needs; no outreach was prepared or initiated.

**Public description boundary:** it is accurate to describe the published note as an unrefereed, AI-assisted theorem with a self-contained argument supporting all diverging deterministic coarse scales, subject to its i.i.d. fixed-law assumptions. It would overstate this review to call it a human-verified breakthrough, the first disproof of a still-open conjecture, a fine-site local limit theorem, or a result uniform over degenerating/correlated environments.

The PDF, proof sources and raw exact results were left unchanged. Downloaded reference PDFs/rendered images and other transient caches are excluded by this review folder's `.gitignore`; receipts, hashes, code, result JSON, this report and research log are retained.
