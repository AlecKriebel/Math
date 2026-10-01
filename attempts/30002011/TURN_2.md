# Turn 2: full-data refitting, a delete-one stability criterion, and actual-family optimism

**Scoped partial, pending independent review; original question unresolved at 2/5.** This turn fixes the Rao–Blackwellized thinning-and-refit protocol and identifies its full-data risk correction exactly. The known coupled-bootstrap/Hudson limit is explicitly credited. The substantive increments are a uniform-in-h quantitative comparison for the actual Δ_h family, a full-refit oracle reduction to deletion stability, and an exact two-candidate example inside that family where adaptive unbiasedness fails.

## 1. Fixed protocol and credited prior input

Fix n≥1, a deterministic finite nonempty grid H⊂[0,∞), a fixed ordering to break ties, and α∈(0,1), with η=1−α. Let

F_h(y)_i=Δ_h^y(y_i)

be the entire source algorithm fitted on the full vector y of length n, using the separate h=0 convention from Turn1. For fixed data Y=y, generate coordinatewise U_i~Binomial(y_i,α), V=y−U. Define the exactly averaged score

barρ_(α,h)(y)=E[ n^(-1)||F_h(U)−αV/η||² | Y=y ].

Choose h_hat_α(y) to minimize this score on H, then **refit on the original data**, outputting

A_α(y)=F_(h_hat_α(y))(y).                         (1)

This is the source's conditional-average proposal with an explicit refit rule. Exact conditional averaging is assumed; a fixed finite Monte Carlo approximation is a different protocol and is not covered by the bounds below.

Oliveira–Lei–Tibshirani, *Unbiased test error estimation in the Poisson means problem via coupled bootstrap techniques*, Electronic Journal of Statistics19(1)(2025),361–396, DOI10.1214/24-EJS2336, already prove the fixed-algorithm small-noise limit to Hudson-based unbiased estimation. Their full26-page author version was read, especially Lemma1, Proposition1, Corollary1, Theorem1 and the variance discussion. Their noise probability is our η. Their squared-loss score differs from the centered score below only by terms independent of h. Hudson's Poisson identity and the existence of this limit are prior work, not new claims of this turn. The following calculations make the exact original-family/refit distinction and the missing adaptive control explicit.

## 2. Centering removes the singular validation-noise term

Subtract the h-independent quantity

A_α^0(y)=α²/(η² n) E[||V||² |Y=y]
        =α³/(η n)sum_i y_i + α²/n sum_i y_i².

This leaves the same minimizers. Write

C_(α,h)(y)=E[||F_h(U)||²/n |y]
          −2α/(η n)sum_i E[V_i F_h(U)_i |y].      (2)

For y_i>0, the elementary binomial identity is

E[V_i F_h(U)_i |y]
 =η y_i E[F_h(Bin(y−e_i,α))_i],                  (3)

where the binomial thinning on the right is independent in each coordinate and the data vector still has length n. This follows by reindexing v_i binom(y_i,v_i) as y_i binom(y_i−1,v_i−1). Terms with y_i=0 vanish and require no evaluation at a negative count.

Consequently

C_(α,h)(y)=E[||F_h(Bin(y,α))||²/n]
          −2α/n sum_i y_i E[F_h(Bin(y−e_i,α))_i]. (4)

For a fixed finite data vector, (4) is a finite sum with no division by η. Its limit as α increases to one is

C_(1,h)(y)=||F_h(y)||²/n−2/n sum_i y_i F_h(y−e_i)_i.                  (5)

Adding Q(y)=n^(-1)sum_i y_i(y_i−1) gives the usual unbiased **mean-risk** estimate

U_h(y)=C_(1,h)(y)+Q(y).                           (6)

For every fixed h and independent Y_i~Poisson(λ_i),

E_λ U_h(Y)=R_λ(F_h):=E_λ||F_h(Y)−λ||²/n.         (7)

Indeed E[Y_i F_h(Y−e_i)_i]=λ_i E[F_h(Y)_i] by Hudson's identity, and E[Y_i(Y_i−1)]=λ_i². Turn1 gives 0≤F_h(y)_i≤max_j y_j, so all required first and second moments are finite. One can also prove the identity by direct reindexing of the Poisson series. Equation (7) is for fixed h; it does not continue to hold after inserting a data-selected h into both places without accounting for the selection change on Y−e_i.

## 3. A quantitative comparison uniform over the original family

Let S=sum_i y_i and m=max_i y_i. From Turn1, for every h≥0 and every u≤y coordinatewise, all coordinates of F_h(u) lie in [0,m]. The chance that Bin(y,α) differs from y is 1−α^S≤ηS. For y_i>0, the analogous probability for y−e_i is at most η(S−1).

It follows from (4)–(5), uniformly over **all** h≥0, that

|C_(α,h)(y)−C_(1,h)(y)| ≤ D_α(y),

D_α(y):=η[m² S + 2mS²/n].                        (8)

For the first term, the two mean squares lie in [0,m²] and coincide when U=y. For the cross term,

|α E F_h(Bin(y−e_i,α))_i−F_h(y−e_i)_i|
 ≤ηm+αmη(S−1)≤ηmS.

Multiplying by 2y_i/n and summing proves (8). If S=0, both sides are zero. This argument needs neither continuity in h nor samplewise continuity of the fitted algorithm under a count deletion.

For 0≤λ_i≤M, S~Poisson(Λ) with Λ=sum_iλ_i≤nM. Since m≤S,

sup_(λ∈[0,M]^n) E_λ D_α(Y)
 ≤η(1+2/n)[(nM)³+3(nM)²+nM].                    (9)

Thus, for example, the purely theoretical choice η_n=n^(−5), n≥2, makes this expectation O_M(n^(−2)), smaller than the bounded-prior regret scale (log n/log log n)²/n. This concerns the exactly averaged centered criterion. It provides no computational claim about taking extremely few validation counts and estimating their expectation by a fixed number of random splits.

## 4. Exact full-refit risk correction

Let h_hat(y) be any measurable selector into H, and let A(y)=F_(h_hat(y))(y). Define

Ω_λ(h_hat)=(2/n)E_λ sum_i Y_i[
 F_(h_hat(Y))(Y−e_i)_i−F_(h_hat(Y−e_i))(Y−e_i)_i].                   (10)

Again terms with Y_i=0 vanish. The full-data fitted rule A satisfies the exact identity

R_λ(A)=E_λ U_(h_hat(Y))(Y)+Ω_λ(h_hat).              (11)

To prove it, apply Hudson's identity to the **whole selected-and-refitted algorithm** A. Its unbiased risk expression contains A(Y−e_i)_i=F_(h_hat(Y−e_i))(Y−e_i)_i. The plug-in expression U_(h_hat(Y))(Y) instead holds the original selected h fixed during the deletion. Subtracting the two formulas gives (10)–(11). All moments are finite by the same sample-maximum envelope. The correction need not be assigned a sign for arbitrary selectors.

For the fixed protocol (1), minimization of C_α and (8) give pointwise

U_(h_hat_α(y))(y)≤min_(h∈H)U_h(y)+2D_α(y).

Combining with (7) and (11) proves the **full-refit oracle reduction**

R_λ(A_α)≤min_(h∈H)R_λ(F_h)+2E_λD_α(Y)+Ω_λ(h_hat_α).                (12)

This is a statement about the actual output refitted on Y. It does not replace that output by the U-trained estimator.

The remaining adaptive term has a concrete sufficient stability bound. Let m_i(y)=max_j(y−e_i)_j for y_i>0. Then

|Ω_λ(h_hat)| ≤ (2/n)E_λ sum_i Y_i m_i(Y)
                          1{h_hat(Y)≠h_hat(Y−e_i)}.                (13)

Both fits in (10) lie in [0,m_i(Y)], and their difference is zero when the selectors agree. This proves (13). A finer bound could use the actual fitted-value difference rather than the switch indicator.

For an iid prior G supported on [0,M], integrate these identities over λ~G^n. If a grid has a comparator with Bayes regret O(r_n), and the expectation of the right side of (13) is O(r_n), then (9), with η_n=n^(−5), and (12) give the corresponding O(r_n) regret for the refitted selector. The comparator guarantee and the deletion-stability bound are separate hypotheses. A credited monotone-Robbins endpoint bound can serve as comparator when h=0 is allowed and the same risk convention is used; a positive-only grid needs its own approximation guarantee. The deletion-stability bound is **not proved** for the source selector. Credited endpoint/alternative estimator results alone do not supply it.

## 5. Exact optimism inside the actual source family

A concrete example shows why the correction cannot simply be set to zero, even after averaging over all splits. It is a finite-sample countercontrol to adaptive unbiasedness, not an asymptotic lower bound for the original question.

Take n=1 and the actual candidate grid

H={0, log 2},

with ties resolved in favor of h=0. If the one observed count is y, then its empirical histogram is the point mass at y. Directly from the source formulas,

a_h(y+j)=hy/(j+1),

F_h(y)=hy E[1/(Poisson(h)+1)]=y(1−e^(−h)).          (14)

Isotonic projection does nothing for a one-point domain. The separately defined h=0 fit is also zero. Thus the two candidates are exactly F_0(y)=0 and F_(log2)(y)=y/2.

For a linear fit F_c(y)=cy, formula (4) gives

C_(α,c)(y)=c²[αηy+α²y²]−2cα²y(y−1).

With c=1/2, its difference from c=0 is

C_(α,1/2)(y)−C_(α,0)(y)
   = (αy/4)[1−3α(y−1)].                          (15)

For every α>1/3, the exactly averaged thinning selector therefore chooses 0 when y=0 or 1, and log2 when y≥2. The full-data refitted estimator is

A_α(y)=(y/2)1{y≥2}.                              (16)

There is a deletion switch only at y=2. Substituting in (10) yields, for Y~Poisson(λ),

Ω_λ(h_hat_α)=2P_λ(Y=2)=λ²e^(−λ)>0, λ>0.          (17)

This is an exact positive bias correction within the original Δ_h family and the specified finite-grid Rao–Blackwellized CV/refit protocol. It persists as α→1.

For an independent risk check,

R_λ(A_α)=(λ²+λ)/4+(λ²−λ/4)e^(−λ),

E_λ U_(h_hat_α(Y))(Y)=(λ²+λ−λe^(−λ))/4.

Their difference is exactly (17). At λ=1 the refitted rule has risk 1/2+3/(4e), exceeding the better fixed candidate's risk 1/2. This does not prove a failure of any large-n optimal-regret claim. In particular, the n=1 construction cannot be tensorized into a source counterexample by applying separate fits to coordinates: the source uses one common empirical histogram and one globally selected h.

## 6. Checkpoint and precise remaining gap

The fixed protocol now has a full-data risk identity and a quantitative route from its averaged thinning score to a classical unbiased risk criterion. The existence of the limiting criterion is credited known work; the uniform bound (8), the actual-family envelope it uses, the refit correction (10) and the exact original-family countercontrol sharpen the current research reduction.

The original optimal-regret requirement remains open here. A uniform bound on the refit selection correction is still missing. For a positive-only grid, an adequate comparator also remains to be proved; inclusion of the separately defined h=0 endpoint changes that comparator issue, but not the adaptive correction. The n=1 optimism calculation only rejects the shortcut from fixed-h unbiasedness to adaptive unbiasedness. The exact-averaging convention also leaves finite Monte Carlo error as a separate issue. No automatic transfer from the known coupled-bootstrap limit or from criterion convergence to regret optimality is asserted.

This completes substantive turn2; three turns remain. All partial claims await independent review before publication as results, and no novelty is asserted.
