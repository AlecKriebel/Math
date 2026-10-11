# Independent reconstruction after proof release, before author-code exposure

The frozen initial direct-family derivation established the exact chain's nonexplosion and irreducibility for all fixed λ>0, recurrence for 0<λ<1, and affine/clipped-interface obstructions for λ≥1. The released TURN_4.md proposes a genuinely nonlinear state function that must be checked against those obstructions. Only the full exact author proof has now been read; no author checker, prior review, ROOT mathematical adjudication or sibling analysis has been read.

## Generator and rounded term

Let u=a(x+1)/D+b(y+1)/D and d=x(y+1)/D+y(x+1)/D. For W=2a+2b+x+y and Z=a+x−b−y, arrivals have W increments 2, conversions and departures −1. Conversions have Z increment zero; arrivals and departures have Z increments ±1. Consequently

    LW=2λ−u−d,  LZ=(y−x)/D,
    sum rate·(ΔZ)^2=λ+d.

The rounded absolute value has derivative clip(z/m,−1,1), continuous at both ±m, globally 1/m-Lipschitz. Integrating its derivative along any displacement gives h(z+v)−h(z)≤h'(z)v+v²/(2m), including jumps crossing a noninteger interface. Thus no unaccounted positive kink contribution occurs. With m=4c the bound for the core is β−u−(7/8)d+c h'(Z)(y−x)/D, where β=17λ/8. This is an upper bound, not an equality. Its last term is at most c in absolute value and at most −c/2 when Z≥m and x≥3(y+1).

## Corrector reconstructed from the reflecting endpoint

For fixed λ, θ=β+c+4, γ=(θ+1)/(θ+2) and η=(1+γ)/2 obey 0<γ<η<1. The finite reflected birth-death generator has detailed balance π_k γ(k+1)=π_{k+1}(k+1) with π_k proportional to γ^k. Its mean satisfies

    μ_R=γ/(1−γ)−(R+1)γ^(R+1)/(1−γ^(R+1)) → θ+1.

It increases strictly with R because adding the point R+1 raises the old truncated mean. Therefore the required strict μ_R>θ and q(R+1)>β+c+2 can simultaneously hold at finite R. R>μ_R, including at the reflecting endpoint.

Write t_k=g(k+1)−g(k), g(R)=0. Start at the endpoint with t_(R−1)=−(R−μ_R)/R. Backwards recursion from Qg(k)=k−μ_R is

    t_(k−1)=[γ(k+1)t_k−(k−μ_R)]/k,  1≤k<R.

This independently recovers the prefix-flux formula printed in the proof. Weighted telescoping gives Qg(0)=−μ_R and the endpoint identity Qg(R)=R g(R−1)=R−μ_R. The numerator of every printed t_k is negative because the conditional mean below k is strictly smaller than μ_R. Hence g is decreasing, nonnegative and bounded, with g(0)=G finite. Extending g(k)=0 above R preserves monotonicity and makes increments vanish for k>R, including the down-jump R+1→R.

For the actual y rates, birth coefficient b/D≥γ multiplies a nonpositive up-increment of g; death coefficient (x+1)/D≤1 multiplies a nonnegative down-increment. Therefore Lg(y)≤y−μ_R for 0≤y≤R under that ratio condition. At y=R the suppressed up-increment is exactly zero; its positive death contribution is bounded above by R−μ_R, not by a negative quantity. This endpoint is accounted for. No invariant law for the evolving original chain is assumed.

## Signed product errors and boundaries

Use the exact product increment with post-jump g on the cutoff increment. At either first download, D increases and both cutoff numerators weakly decrease. Both cutoff increments are nonpositive. Their factors g after the jump are nonnegative, so these errors are nonpositive regardless of queue magnitude. Discarding them in an upper bound is justified.

An arrival affects one cutoff and contributes at most ell G/D times its rate. At a departure D≥2. If w/D≥η, both cutoff values are 1 and their difference is zero. Otherwise w<ηD and the cutoff increase is at most ell w/[D(D−1)]≤2ell/D. Two terms contribute at most 4ell G/D per departure. This proves the global interface remainder ell G(λ+4d)/D. At D=1 there are no departures, so the formula still holds. Zero-coordinate transitions are omitted rather than evaluating g at a negative coordinate.

For the coarse small-visible-population bound, first downloads weakly decrease both products; arrivals can increase their sum by at most G, and departures by at most 2G. Thus LJ≤G(λ+2d). Both bounds are pointwise actual-state inequalities.

## Region coverage and constants for every real λ>0

All constants are finite for each real λ>0. The strict corrector conditions above give finite R. Since 1−η>0, every displayed lower bound on N, including the imbalance and interface bound, is finite; a sufficiently large integer satisfies them simultaneously. Integer ceiling does not reverse a weak inequality. There is no uniform-in-λ assertion.

For integers x,y the three regions are exhaustive: (I) min≥R+1; otherwise (II) max≥N; otherwise (III) min≤R and max<N. In I all successor g-values vanish, including visible departures at R+1. Also d≥min(x,y), so the core drift is below −2.

In II take y≤R,x≥N by symmetry. The other correction and all its successors vanish. Direct algebra gives d≤2R+1, x/D≥3/4, (x−y)/D≥1/2 and qd≥y. The remainder is at most 1. When b/D≥η the full corrector gives an upper bound β+c−μ_R+1<−3. When b/D<η, b<ηD and a≥0 imply Z≥(1−η)x−(1+η)y−η≥m. The rounded derivative equals 1 there, and f(b/D)(y−μ_R)≤y. The upper bound is β−c/2+1−u=−3−u. This includes both endpoints of the cutoff band; no switching rule is used.

In III, x+y≤N+R and u≥(a+b)/(N+R+1). The coarse bound proves drift at most −1 once a+b exceeds the stated finite B. Hence the stated finite F contains every remaining possible bad state. Some states in I or II lie inside F; that only enlarges F and does not spoil the outside-F bound.

## Foster/stopping assumptions reconstructed explicitly

The earlier direct nonexplosion and irreducibility proofs remain applicable. Here V≥W≥N, and h_m(Z)≤|Z|+m/2 with |Z|≤N; J≤2G. Therefore

    0≤V≤(2+c)N+c m/2+2G,
    |ΔV|≤2+c+2G.

Total rate q≤λ+N and N(t)≤N(0)+Π_λ(t) give finite-time generator and stopped-value integrability. The localized Dynkin argument is legitimate. Nonnegative stopped V gives the expected stopped-time bound; nonexplosion and Fatou remove the localization. Alternatively bounded jumps and the displayed linear upper bound yield uniform integrability and the direct stopped Dynkin identity. Thus E_s τ_F≤V(s) outside F.

To obtain a finite-mean origin return, start fixed-duration trials from the finite F. Each state has a positive-rate finite path to the origin; the minimum probability to complete such a path in time 1 is positive. After failed trials, the hitting bound and the Poisson/linear upper bound on expected V at time 1 give a uniform finite expected cost to return to F. Strong Markov conditioning gives a geometric trial tail and finite expected origin hitting time. The origin has mean holding time 1/λ and two possible first-jump neighbors. Its strict return cycle has finite mean. Regeneration yields an invariant probability; irreducibility makes it unique. This fills the abbreviated alternative Foster explanation with actual integrability and return hypotheses.

The nonlinear corrector directly addresses the frozen clipped-deficit failure: at the B≈X,Y=0 interface it pays for births of Y through a negative g increment, rather than introducing an uncontrolled positive clipping increment. Its bounded magnitude does not prevent a large fixed negative drift because G and μ_R may depend on λ.

**Provisional analytic conclusion before author-code inspection:** the displayed all-state proof appears sound for the exact six-rate chain, including real λ and zero/reflecting/interface cases. Exact rational controls will test correspondence to this reconstruction. Final mathematical acceptance remains conditional on final external source/model correspondence; no priority or publication judgment is made.


## Post-reconstruction reproducibility and the frozen failure families

The pre-code reconstruction seal was completed at 2026-10-05T18:36:29.449441 UTC before the original checker was read. Original checker pin: 6,964 bytes, SHA256 53aab7ce990f4b70d6d1ea3a3665e8e8375685407589e021f50a4695f075acae. Only an unchanged copy inside this review's own folder was executed. It reproduced PASS with 71,165 exact assertions over 5,200 states. The reported floats are display-only, and no floating-point quantity appears in an assertion. The checker uses the same six rates, suppresses zero-rate negative-coordinate successors, implements g(R)=0 correctly and calculates the same cutoffs/constants. It is finite corroboration, not the universal proof. For lambda=1 its R=89 and N=37,844,441 agree with the independent backward-endpoint construction.

The frozen initial proof's affine obstruction remains correct. It does not apply to the present piecewise core/corrector, whose local slopes need not be a globally coercive affine function. The previous clipped-deficit interface failure is specifically remedied. At a=y=0,b=x=n sufficiently large that all relevant cutoff values are 1 and g(x) and its successors vanish, put σ=n/(n+1). Here Z=0, u=d=σ and the rounded part is quadratic for every one-step Z change. The exact core drift is

    L(W+c h_m(Z))=β−(1+q)σ.

The minority correction has exact drift

    LJ_X=σ[g(1)−g(0)]=−σ μ_R/γ,

so LV=β−σ(1+q+μ_R/γ). Since μ_R>θ=3β+12, γ<1 and σ≥1/2, this is strictly negative. The first-download ratio can remain saturated once n≥(1+2η)/(1−η); all these are finite fixed-load thresholds. This concrete check links the candidate's mechanism to the previous unbounded interface counterexample. No frozen-rate mean is used.

The exact coefficient archives store the full g array. Their t field is empty; increments are recovered exactly as g(k+1)−g(k). The independent control script uses a backward endpoint recursion and separately compares it with the prefix-flux formula, without importing the author code.

The formerly open all-load direct-family gap is closed by this nonlinear pointwise mechanism for the exact chain. The source/model correspondence gate is independently owned by ROOT and was authenticated here by its complete source-only acceptance record. It accepts the 2011 author proof and OWR scope with explicit edition limits: the final publisher body is uninspected, the source conjecture does not literally print the universal quantifier, and all fixed positive loads formalize its unqualified parameterized setting. These source qualifications do not weaken the exact-chain mathematical theorem proved here. No worldwide priority or preprint/publication judgment follows from this mathematical review.
