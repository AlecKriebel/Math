# Independent proof audit: monotone absorbing IPS sharpness

Problem 30005233 / OWR-11101922-005. Audit date: 10 October 2026 (UTC).

## Verdict and scope

**The source-faithful Theorem 1.1 is accepted, with the explicit local repairs and technical completions below, relative to the published Poisson OSSS inequality specified in Section 5 and standard measure/probability foundations.** This is an independent verification of the argument of Bérard, Dembin and Marêché, not a claim of a new sharpness proof. The acceptance is of the intended translation-invariant, finite-range model after correcting the printed shift convention. It is not a claim that every printed formula is literally correct.

The accepted statement is this. Let L be a finite-rate, finite-range, translation-invariant, attractive binary single-site IPS generator on Z^d, with the all-zero state absorbing. If its occupied-origin probability from the all-one state tends to zero, then, for every ε > 0, the generator L + εD has exponentially decaying occupied-origin probability from all one. Here D resets each site to zero at rate one. Constants may depend on ε and L. The exact death-mixture parameter-ray consequence follows in Section 9.

This audit does not accept general finite-seed survival sharpness, arbitrary monotone parameter curves, critical-endpoint behavior, nonabsorbing ergodicity sharpness, infinite-range systems, simultaneous multiple-site updates, or the topological Corollary 1.2. In particular, the latter would require checking additional stability inputs; it is unnecessary for the accepted theorem and ray consequence.

The source remains a **prior preprint**: Jean Bérard, Barbara Dembin and Laure Marêché, *Sharpness for monotone absorbing Interacting Particle Systems*, arXiv:2510.11424v2, 24 November 2025, 18 pages. The current arXiv record and an author's publication list, checked again on 10 October 2026, supplied no journal reference for this item. This is bounded publication-status evidence, not proof that publication or acceptance has never occurred. Mathematical acceptance in this audit does not turn a preprint into a published theorem.

## 1. Sources and proof obligations

The exact preprint PDF inspected has 294,584 bytes and SHA-256

    ae1411968b797f149f050b553dd035225707d29a7739e003c26213b73878fd2d.

The published external input is Günter Last, Giovanni Peccati and D. Yogeshwaran, *Phase transitions and noise sensitivity on the Poisson space via stopping sets and decision trees*, Random Structures & Algorithms 63(2) (2023), 457-511, DOI 10.1002/rsa.21136. The inspected author-manuscript version is arXiv:2101.07180v3 (21 September 2022), 793,484 bytes, SHA-256

    dceb9e19a634d8cf93b55a6ec048346f69ee1654579bbbe35beaa81de0301269.

All theorem/equation page references for this input below are to that inspected author manuscript: Sections 2-4, assumptions (3.2)-(3.5), and Corollary 4.1, especially (4.2), p. 17. Publication status is independently confirmed by the publisher and KIT repository. The publisher's public full-text link returned its abstract/reference page, so this audit does not assert a byte-for-byte comparison with the publisher PDF or that its pagination matches the manuscript.

The previous applicability audit was used as a list of issues to verify, not as evidence that the omitted technical steps were already established. The entire v2 proof, pp. 5-17, was read; the theorem/conventions, influence, revealment and final calculus displays were also checked against PDF images where relevant. The audit independently discharges:

1. graphical construction, attractiveness and absorption;
2. finite dependence, localization and finite-box approximation;
3. the finite/infinite-volume Russo identity and needed derivative bounds;
4. comparison of absolute add-one influence with mark pivotality;
5. every hypothesis of the published continuous Poisson OSSS input;
6. revealment and finite-to-infinite-volume differential inequality;
7. the complete analytic lemma, including its corrected limsup display;
8. time-rescaling and the exact parameter-ray implication.

Standard dominated convergence, elementary Poisson conditioning/factorial moments, finite-state measurable recursion and scalar calculus are used below. To keep the dependency boundary clear, the finite-volume Russo identity and the localization estimate are supplied directly rather than leaving their essential content dependent on a second uninspected theorem. The substantial external theorem not reproved here is the stated published Poisson OSSS inequality.

## 2. Model, convention repair and graphical construction

Write N = Λ_R, K = |N|, and use the local view ξ_x(y) = ξ(x+y). The intended generator is

    Lf(ξ) = Σ_x {c_1(ξ_x)[f(ξ^{x,1})-f(ξ)]
                    + c_0(ξ_x)[f(ξ^{x,0})-f(ξ)]}.

The source's p. 3 definition τ_x ξ(y) = ξ(y-x), when substituted literally into its generator, looks around -x while updating x. That is inconsistent with the subsequent centered-neighborhood construction and the announced translation-invariant model. Replace it by ξ(y+x), or replace τ_x by τ_{-x} throughout the generator and update formulas. No reflection symmetry of the rates is required. This is a necessary convention correction, not a substantive enlargement of the theorem.

The nonnegative rates obey c_1 increasing, c_0 decreasing, and c_1(0)=0. They are bounded because N is finite. These reset-rate assumptions cover conventional attractive binary flip rates: extend the birth rate from configurations with central state 0 independently of that coordinate, and extend the death rate from central state 1 in the same manner. These extensions preserve monotonicity and leave the actual generator unchanged.

Set C_0 = c_0(0), C_1 = c_1(1). We may assume C_1 > 0. Indeed replace c_1(ζ) by c_1(ζ)+aζ(0), a>0 if necessary. The added term only resets an already-one central site to one, has no effect on the generator, remains increasing and vanishes at zero. Let M=C_0+C_1>0.

Use rate-M clocks at each site and an independent uniform u in [0,M]. For an A mark the local map is zero when u<c_0(ζ), unchanged when c_0(ζ)≤u<M-c_1(ζ), and one when u≥M-c_1(ζ). A B mark always outputs zero. A marks have probability 1-h and B marks probability h. The intensity, in a finite box and time interval, is

    λ_{h,m,T}(dx dt du dw)
      = counting(dx) dt du [(1-h)δ_A(dw)+hδ_B(dw)].

Thus total clock rate is M per site, and the generator is

    L_h = (1-h)L + MhD.                                      (2.1)

For a literal all-configuration definition, ignore A atoms with u=M; this null set otherwise makes the closed upper endpoint output one even at the zero neighborhood. Ignore time-zero atoms. This convention agrees with the random process almost surely. Equal-time and repeated atoms are handled measurably in Section 5.

Each A local map is increasing. Write α(ζ)=c_0(ζ) and β(ζ)=M-c_1(ζ); both thresholds are nonincreasing under increase of ζ and satisfy α≤β. If the output for a smaller configuration ζ is one, then either u≥β(ζ), so u≥β(η) for a larger configuration η, or ζ(0)=1 and u≥α(ζ), so η(0)=1 and u≥α(η). In either case the output for η is also one. These exhaust the ways the smaller output can be one. B is the constant zero map. Replacing A by B can only reduce the output. Consequently the common-clock coupling preserves initial-state order and is decreasing in h. The zero configuration is preserved because c_1(0)=0 and the null u=M endpoint has been removed.

### Well-defined infinite-volume process

Starting at (0,T), explore clocks backward, retaining every site already discovered and adjoining x+N whenever a clock at a discovered site x is met. With j sites, potential exploration events occur at rate Mj and each can add at most K-1 sites, because 0 belongs to N. A pure-birth population, with replacement of a particle by K particles at rate M, dominates the number of discovered sites. Its stopped first-moment estimate gives

    E Y_T ≤ exp[M(K-1)T].

The expected number of its events up to T is bounded by M∫_0^T exp[M(K-1)s] ds. Therefore there is no finite-time explosion, including K=1, where the population stays one and the event count is Poisson. This gives a finite backward dependency exploration. Read the finitely many relevant clocks in increasing time to define the desired spin for every initial configuration.

The countably many site/integer-horizon explorations suffice to obtain this construction simultaneously at every site and time and for every initial configuration. The exploration retains the starting site, so the exploration with terminal integer n includes all clocks needed for its starting site's state at earlier times t≤n. Almost surely all clock times in any relevant finite collection are distinct; globally this follows by a countable union over pairs of sites and bounded horizons. Independent increments give the Markov property, and the local one-clock calculation gives (2.1).

## 3. Localization, approximation and Russo differentiation

### 3.1 A direct exponential localization bound

Let I_0^T be the retained backward spatial cluster. If x is discovered and R≥1, some time-ordered sequence of n clocks follows neighborhood steps from 0 to x, where n≥ceil(||x||_∞/R). There are at most K^n spatial step sequences. For each prescribed sequence, the expected number of strictly ordered clock n-tuples is (MT)^n/n!, by the Poisson factorial-moment calculation, also when a site occurs more than once. Hence, with a=KMT and k=ceil(||x||_∞/R),

    P(x∈I_0^T) ≤ Σ_{n≥k} a^n/n!
                 ≤ exp(ae-k).                              (3.1)

The upper bound may be truncated at one. It is summable in x and independent of h, since the cluster ignores A/B and u marks. When R=0, I_0^T={0}; no spatial tail estimate is needed. This proves the required localization without the preprint's separate many-to-one citation.

A modification of the spin at (x,t) can only change the terminal spin if x lies in the unmodified retained backward cluster. This follows by chronological induction over its dependency graph: each relevant update's whole neighborhood is retained before it is evaluated. If x is absent, forced 0 and forced 1 versions coincide on every relevant site. In particular mark-pivotality is bounded by the right side of (3.1).

### 3.2 Finite boxes and a necessary enlargement for inserted points

In Λ_m use the same internal clocks, all-one internal initial state and zero external boundary. Denote its upper density by θ_T^m(h), and the infinite-volume density by θ_T(h). Once Λ_m contains the finite origin dependency cluster, the terminal spins agree. Consequently θ_T^m(h)→θ_T(h).

For an inserted point z=(x,t,u), define Piv_T(z) by the two conditions:

- the A update at z outputs one from the actual pre-update neighborhood;
- forcing the site at (x,t) to zero gives terminal zero, and forcing it to one gives terminal one.

These are exactly the conditions for exchanging the inserted A mark for B to change the terminal spin. A deterministic time t has no preexisting clock almost surely, so no tie issue occurs in these integrals.

For convergence and h-continuity of this event, the unmodified origin cluster alone need not contain the data in the first condition. Add the backward clusters of all sites y∈x+N at time t just before the insertion. Their union with the origin cluster is finite almost surely. It contains the information needed for the inserted update and both forced terminal trajectories. Under common unmarked clocks and auxiliary independent uniform marks v, set B precisely when v<h. The enlarged finite collection contains no mark v equal to a fixed h_0 almost surely. Thus the pivotal indicator is eventually constant as h→h_0, and eventually equal to its finite-box counterpart as m→∞. Dominated convergence proves continuity in h and convergence of pivotal probabilities. Endpoint h derivatives are understood one-sided.

This is a technical completion of the short proofs of source Lemmas 2.7 and 2.9. It is important to distinguish the finite collection needed to *evaluate* pivotality from the unmodified cluster needed to *bound the probability* of pivotality. The probability bound (3.1) still uses only the latter; the enlarged cluster is not inserted into that uniform bound.

### 3.3 Finite-volume Russo identity from elementary conditioning

The unmarked Poisson process in Λ_m×(0,T]×[0,M] has finite mean V=M|Λ_m|T. Conditional on its n points, the terminal Boolean value is a decreasing function of the n independent B indicators. Differentiating the finite Bernoulli product expectation gives minus the sum of the n mark-pivotal probabilities with all other marks held random. Its derivative has absolute value at most n. Since E n=V, differentiation under the Poisson expectation is justified uniformly on h∈[0,1].

The elementary identity nP(N=n)=VP(N=n-1), combined with integration over the locations of the n iid points, converts the sum over an existing point into an integral over one inserted point. Therefore

    -∂_h θ_T^m(h)
      = Σ_{x∈Λ_m}∫_0^T∫_0^M P_h(Piv_T^m(x,t,u)) du dt.       (3.2)

The derivative is continuous: conditional finite Bernoulli probabilities are continuous and bounded by n, which is integrable. This gives directly the finite-intensity result used by source Lemma 2.10; it does not require an unverified infinite-intensity differentiation formula.

### 3.4 Infinite-volume derivative and compact-time bound

Extend finite-box pivotal probabilities by zero outside Λ_m. They converge pointwise to the infinite-volume probability and are all bounded by (3.1). The same geometric cluster bounds the finite-box dependency graph. Thus dominated convergence gives convergence of the right side of (3.2), uniformly bounded in m and h by an integrable spatial majorant.

Write θ_T^m(h)=θ_T^m(0)+∫_0^h ∂_a θ_T^m(a) da and pass to the limit. The limiting integrand is continuous in h by the finite enlarged-cluster argument and the same majorant. The fundamental theorem of calculus now proves

    -∂_h θ_T(h)
      = J_T(h)
      := Σ_{x∈Z^d}∫_0^T∫_0^M P_h(Piv_T(x,t,u)) du dt,

    ∂_h θ_T^m(h) → ∂_h θ_T(h).                              (3.3)

No exchange of an infinite-volume derivative with a limit has been assumed.

For any finite H, the same backward construction with horizon H dominates in law every shorter horizon, or one can use its first-moment bound directly. For 0≤t≤H,

    |∂_h θ_t(h)| ≤ Mt E|I_0^t|
                   ≤ MH exp[M(K-1)H].                      (3.4)

This is uniform in h, and at t=0 the derivative is zero. It supplies the exact compact-time uniform derivative hypothesis of source Lemma 3.3.

Finally, |θ_{t+s}(h)-θ_t(h)|≤1-exp(-Ms) by the chance of an origin clock, so θ is continuous in time. Attractiveness and the Markov property, starting from the maximum state, make θ nonincreasing in time. The h-coupling makes it nonincreasing in h. The lower bound θ_T(h)≥exp(-MT)>0 comes from no origin clock.

## 4. Absolute add-one influence versus mark pivotality

This is source Lemma 3.2. All differences below are **absolute values**. The PDF has them, even where text extraction loses vertical bars.

Let f be the finite-box terminal Boolean observable and define

    I = ∫ E_h|f(η+δ_z)-f(η)| λ_{h,m,T}(dz),
    J = Σ_x∫_0^T∫_0^M P_h(Piv_T^m(x,t,u)) du dt.

For a deterministic x,t, let a be the pre-update spin, b the event that forced 0 and forced 1 at that point give different terminal outcomes, and A_u the event that the inserted A update outputs one. The event b does not depend on inserted u or inserted A/B choice.

If a=0 and inserting a point changes f, that point must set the site to one. Therefore A_u and b both occur. If a=1 and inserting a point changes f, at least b occurs. Integrating these two inclusions gives I≤I_1+I_2, where

    I_1 = Σ_x∫dt∫du P(a=0,A_u,b),
    I_2 = M Σ_x∫dt P(a=1,b).

For a=1, every A mark with u∈[C_0,M), an interval of length C_1, preserves or resets the site to one: the death threshold never exceeds C_0. Hence

    I_2 = (M/C_1) Σ_x∫dt∫_{C_0}^M du P(a=1,A_u,b)
         ≤ (M/C_1) Σ_x∫dt∫_0^M du P(a=1,A_u,b).

Since M/C_1≥1 and the a=0 and a=1 cases partition the sample space,

    I ≤ (M/C_1) J.                                          (4.1)

This proof requires no independence of a and b. It is an integrated comparison, not an assertion that point influence and mark pivotality coincide. The harmless u=M endpoint convention has zero effect on all integrals. Combining (3.2) with (4.1) gives I≤(M/C_1)(-∂_hθ_T^m).

## 5. Published Poisson OSSS input and its applicability

The accepted input is LPY Corollary 4.1, variance form (4.2): for a measurable f:N→[-1,1] determined by a randomized continuous-time decision tree,

    Var(f(η)) ≤ 2∫ P(z∈Z_∞) E|f(η+δ_z)-f(η)| λ(dz).        (5.1)

The hypotheses are not merely that Z_∞ informally reveals enough information. They are:

- X is a Borel space and λ is locally finite and diffuse;
- for each auxiliary randomization, Z_r is graph-measurable and a stopping set, meaning Z_r(μ)=Z_r(μ restricted to Z_r(μ) + ν restricted to its complement) for all μ,ν;
- Z_r is increasing and right-continuous in r, each Z_r lies in a finite localizing set, and Eλ(Z_0)=0;
- λ(Z_r(μ)\Z_{r-}(μ))=0 for every μ,r;
- almost surely the Poisson measure has at most one atom in every instantaneous increment, simultaneously for all r;
- f(μ)=f(μ restricted to Z_∞(μ)) for every μ;
- the LPY mixed configuration ζ_r converges under f in probability to f(η′), with η′ an independent copy;
- the auxiliary randomization is independent and the exploration is jointly measurable in that randomization, the point and μ.

Here X=Λ_m×[0,T]×[0,M]×{A,B}, a finite product of standard Borel spaces, and λ(X)=M|Λ_m|T<∞. It is diffuse even at h=0 or h=1 because its time coordinate is Lebesgue. We may take every localizing B_n=X; thus N is the space of finite integer-valued measures. The observable takes values in {0,1}.

A fully specified all-configuration construction and proof are supplied in the companion CTDT review. The following gives the complete essential verification rather than relying on the preprint's assertion alone.

### 5.1 Measurable dynamics and single-phase exploration

For any finite μ, ignore atoms at time zero and A atoms with u=M. At a fixed site and time with multiple eligible marks, choose the smallest pair under a fixed Borel lexicographic order on [0,M]×{A,B}, ignoring multiplicity. At a time with marks at multiple sites, apply all selected updates simultaneously, using the common pre-time configuration. These are measurable finite operations. They agree with the Poisson dynamics almost surely. Simultaneous updates also preserve order, and an update at a site whose whole pre-time neighborhood is zero has no effect.

Given a starting time s and all-one initial configuration, explore forward only the site fibres x whose neighborhood contains a one in the evolving configuration. While that active set is E, reveal E×(a,b]×[0,M]×{A,B} up to the next eligible active atom time or the specified exploration cutoff. At an event, apply all eligible marks at active sites at that time, simultaneously. An inactive site's ignored event has no effect even when a neighbor becomes one at the same time, because simultaneous updates use the pre-time state. All full mark fibres at queried site-times are included, whether or not an atom on that fibre was eligible. Continue with the updated active set. If it is empty, reveal no further region.

For every finite μ this finite recursion recovers exactly the trajectory of the all-configuration dynamics: between queried events, unqueried sites have zero pre-time neighborhoods and their updates do nothing. Measurability follows by finite sorting/selection and recursion on finite counting measures; the membership graph is a finite union of sets whose interval endpoints and active-site indicators are measurable. The same construction is jointly measurable in s and the cutoff.

The stopping-set property follows by replay. Hold μ fixed and keep μ unchanged on the region revealed up to the cutoff, replacing the complement arbitrarily. The first active set is deterministic. Its revealed time interval contains every mark and absence query responsible for choosing the first queried event before the cutoff. No replacement can introduce an earlier eligible active event because the entire corresponding fibre segment is fixed. At that event, all raw mark fibres at active sites are fixed, so the tie choice and simultaneous updated state are unchanged. Induction repeats this argument through every queried event. Inserted events at inactive sites are ineffective. Hence the same revealed region and trajectory are obtained. This proves the identity for every finite pair μ,ν, rather than just almost surely.

### 5.2 Two-phase randomized tree

Choose S uniformly on [0,T], independently of η. Run the single-phase exploration from S to T, starting from all one at S. Denote this auxiliary upper trajectory by U. If U_T(0)=0, stop. Otherwise run the single-phase exploration from time zero to T for the actual all-one initial state, retaining the already revealed first-phase region. Parameterize the two phases consecutively, each at unit physical-time speed. The tree is constant by exploration time 2T (indeed by 2T-S).

For any fixed S, the first-stage stopping identity follows from replay. Its terminal answer is determined by its revealed region. Therefore the decision whether to run stage two is invariant under a replacement outside the union. If stage two runs, apply the same replay argument to its revealed part; its region may overlap the first stage, which is harmless. This proves the stopping identity for the union at every exploration time.

The regions increase. Intervals are open at their starting time and closed at their currently revealed ending time, so they are right-continuous as sets, including event times and the concatenation point. The initial region is empty, and no positive-volume region is inserted at the second-stage start. Each instantaneous increment lies in a single physical-time slice of one phase, and therefore has λ measure zero for every μ. At a phase boundary there is no new positive-length interval.

Almost surely all Poisson atoms on this finite X have distinct physical times. At any exploration time only one phase is advancing; a boundary adds no second time slice. Thus each instantaneous increment contains at most one Poisson atom simultaneously for all exploration times. Previously revealed overlaps add none. Possible coincident or multiple atoms in arbitrary μ do not violate this requirement, which is specifically almost sure, while their intensity-zero increment property has already been proved for every μ.

For determination on all μ: if stage two runs, its replayed actual trajectory determines f and is unchanged after deleting all unqueried atoms. If stage one stops with zero, its computed upper trajectory is unchanged by that deletion; the actual configuration at S is at most all one, and attractiveness using the same post-S retained graph gives terminal origin zero for both the original and restricted μ. Thus f(μ)=f(μ restricted to Z_∞(μ)) in both cases.

The additional LPY convergence condition is especially simple here. For exploration r≥2T, Z_r=Z_∞, so

    ζ_r = η restricted to (Z_∞\Z_r)
          + η′ restricted to Z_r + η′ restricted to X\Z_∞
        = η′

identically. Hence f(ζ_r)=f(η′) eventually, not just in probability. Independence and joint measurability of the uniform S were established by the construction.

This verifies every input of (5.1). The preprint's footnote 9 is not by itself a full all-configuration specification: a fixed Borel mark order and a convention for distinct sites at the same time must be supplied. The above completion changes no Poisson-almost-sure trajectory, influence integral or revealment estimate.

## 6. Revealment estimate and translated-box correction

Fix z=(x,t,u,w). For a cut S=s, first-stage revelation at time t can occur only if t>s and at least one site y∈(x+N)∩Λ_m is one in the auxiliary upper process at time t-. Second-stage revelation requires its trigger U_T(0)=1. Therefore the union bound gives

    P(z∈Z_∞) ≤ (1/T)∫_0^T [θ^m_{T-s}(h)
       + 1_{s<t} Σ_{y∈(x+N)∩Λ_m} P(X^m_{t-s}(y)=1)] ds.

Time homogeneity was used here, and deterministic-time Poisson atoms have probability zero, so t- and t have the same spin distribution. One can also bound stage-two activity after s by the upper trajectory's activity using attractiveness, but that stronger inclusion is not needed for this displayed union bound. It follows that

    P(z∈Z_∞) ≤ (K+1)/T ∫_0^T max_{y∈Λ_m}P(X^m_r(y)=1) dr.  (6.1)

For y∈Λ_m, Λ_m⊂y+Λ_{2m}. Put the dominating finite-box process on y+Λ_{2m}, initially **one on y+Λ_{2m}**, and zero outside. Share all common clocks. Its boundary and initial states dominate those of the Λ_m process. Translation invariance gives

    P(X^m_r(y)=1) ≤ P(X^{2m,y}_r(y)=1) = θ^{2m}_r(h).

This proves

    P(z∈Z_∞) ≤ (K+1)/T ∫_0^T θ^{2m}_r(h) dr.                (6.2)

The p. 15 printed initial state 1 restricted to Λ_{2m} must be replaced by 1 restricted to y+Λ_{2m} (or explicitly stated in coordinates centered at y). Without that correction the displayed equality to θ^{2m} is not justified. The corrected comparison follows directly from inclusion of boxes and needs no spatial reflection assumption.

## 7. Differential inequality with all constants controlled

Apply (5.1), use (6.2), then (4.1) and (3.2). For T>0,

    θ_T^m(1-θ_T^m)
      ≤ 2(M/C_1)(K+1)(-∂_hθ_T^m) (1/T)∫_0^T θ_s^{2m} ds.

Let m→∞. Section 3 proves convergence of both densities and derivatives, and bounded convergence applies to the time integral since its integrand is at most one. Thus

    θ_T(1-θ_T)
      ≤ 2(M/C_1)(K+1)(-∂_hθ_T) (1/T)Σ_T,
    Σ_T(h) := ∫_0^T θ_s(h) ds.                              (7.1)

Ergodicity of L implies c_0(1)>0. If c_0(1)=0, no update could move the all-one initial state away from all one; this would contradict θ_T(0)→0. Moreover θ_1(0)<1 quantitatively: the event of exactly one origin clock in [0,1], with u<c_0(1), has probability c_0(1)e^{-M}; it forces death regardless of the neighbors and has no later origin update. Therefore

    b := 1-θ_1(0) ≥ c_0(1)e^{-M}>0.

Time and h monotonicity give 1-θ_T(h)≥b for T≥1. Positivity of θ_T and Σ_T allows division in (7.1), yielding

    -∂_h θ_T(h) ≥ c T θ_T(h)/Σ_T(h),  T≥1, h∈[0,1],        (7.2)
    c = b C_1/[2M(K+1)] > 0.

The constant is independent of T,h,m. This is exactly the differential inequality needed; there is no unproved strictly positive factor near h=0.

## 8. Complete calculus argument and precise p. 17 correction

We verify source Lemma 3.3 in its stated generality. Let 0<f_T(h)≤1, with h↦f_T nonincreasing and differentiable, T↦f_T(h) continuous, f(h)=lim_{T→∞}f_T(h) existing, and

    -f_T′(h) ≥ c T f_T(h)/Σ_T(h),  T≥1,
    Σ_T(h)=∫_0^T f_t(h)dt.

Assume derivatives are uniformly bounded for (t,h) in [0,H]×[0,h_0] for each finite H. Define

    A={h∈[0,h_0]: limsup_{T→∞} log Σ_T(h)/log T = 1},
    h_1=sup A, with h_1=0 when A is empty.

This agrees with the source's ≥1 definition because Σ_T≤T. The set A is downward closed: Σ_T is nonincreasing in h. Consequently every h′<h_1 lies in A. This last statement follows from the supremum property by choosing an element of A strictly above h′; it does not presume that the supremum is attained.

### Above h_1

For h>h_1 choose h′∈(h_1,h), set h″=(h′+h)/2, and δ=(h-h′)/2. Since h′∉A, there exist α>0,T_0>1 with Σ_T(h′)≤T^{1-α} for T≥T_0. The same holds for parameters at least h′. Integrating the logarithmic differential inequality between h′ and h″ gives

    f_T(h″)≤exp(-cδ T^α),  T≥T_0.

Thus B=∫_0^∞ f_t(h″)dt<∞; the integral on [0,T_0] is bounded by T_0. For every parameter between h″ and h, Σ_T≤B. A second integration gives

    f_T(h)≤exp[-(cδ/B)T],  T≥1.

This proves pointwise-parameter exponential decay.

### Below h_1

For T>1 put F_T(h)=(log T)^{-1}∫_1^T f_t(h)dt/t. Logarithmic Cesàro averaging gives F_T(h)→f(h): split the integral at a fixed large A, bound the first part by a constant divided by log T, and use |f_t(h)-f(h)|≤ε beyond A.

The compact-time derivative bound justifies differentiation of F_T. Indeed the difference quotients are bounded by the derivative supremum using the mean value theorem; pointwise convergence and dominated convergence apply on [1,T]. Hence

    -F_T′(a) ≥ c/(log T) ∫_1^T f_t(a)/Σ_t(a) dt
             = c/(log T)[log Σ_T(a)-log Σ_1(a)].

For h<h′<h_1 and a∈[h,h′], monotonicity gives

    log Σ_T(a)-log Σ_1(a)
      ≥ log Σ_T(h′)-log Σ_1(h).

Integrating in a gives the valid retained bound

    F_T(h)-F_T(h′)
      ≥ c(h′-h)[log Σ_T(h′)-log Σ_1(h)]/log T.                (8.1)

The first displayed bound on source p. 17 already has exactly these correct parameter positions. The next displayed limsup in the source swaps them. Its corrected continuation is

    f(h)-f(h′)
      ≥ c(h′-h) limsup_{T→∞}
          [log Σ_T(h′)-log Σ_1(h)]/log T
      = c(h′-h),                                            (8.2)

because h′∈A and Σ_1(h)>0 is fixed. Since f(h′)≥0, let h′ increase to h_1 to obtain f(h)≥c(h_1-h). No continuity of f at h_1 is required.

Thus the first p. 17 display should be retained, and only the swapped arguments in the following limsup must be corrected. This explicitly supersedes the earlier applicability report's overbroad wording about the two displayed logarithmic bounds: the first displayed argument was already correct. The earlier report remains unchanged as a historical artifact. Both the inequality direction and the limiting threshold argument are now fully justified.

### Application and time change

Apply this lemma to f_T=θ_T, h_0=1. Every regularity assumption was proved in Section 3, and (7.2) is its differential inequality. Ergodicity says f(0)=0. If h_1>0, the below-threshold conclusion at h=0 would give f(0)≥ch_1>0, a contradiction. Therefore h_1=0 and θ_T(h) decays exponentially for every h>0. An enlarged multiplicative constant covers the bounded initial time interval, so the estimate has the form C_h exp(-c_hT) for all T≥0.

For a given ε>0 choose h=ε/(M+ε), so 0<h<1 and

    L_h=(1-h)(L+εD).

If θ^{ε} is the upper density for L+εD, then

    θ^{ε}(t)=θ^h(t/(1-h)).

This positive time change proves the stated exponential bound for every ε>0. Attractiveness and absorption also give exponential convergence of each fixed finite set's marginal to all zero from any initial state, by a union bound. No total-variation convergence on the entire infinite product space at finite time is being asserted.

## 9. Exact death-mixture ray consequence

Let a be an increasing local probability a:{0,1}^N→[0,1], with a(0)=0. Its rate-one asynchronous death-mixture family is

    G_p = pG_1+(1-p)D, 0≤p≤1,

where each update outputs one with probability p a(local state). Its birth and zero-reset rates are p a and 1-p a, so it belongs to the accepted class. Write ρ(p)=lim_{t→∞}θ_p(t). The limit exists by monotonicity in time and is nondecreasing in p under common clocks/uniform marks. Let E={p:ρ(p)=0} and p_c=sup E. E is downward closed and contains 0, where θ_0(t)=e^{-t}.

For p>p_c, ρ(p)>0 by definition. For 0<p<p_c, choose q∈E with p<q≤1. There is the exact identity

    G_p=(p/q)[G_q+εD],  ε=(q-p)/p>0.

The theorem applies to G_q because q∈E. Therefore θ_p(t) is bounded by C exp[-c(p/q)t]. This proves exponential decay throughout the strict subcritical ray, directly covers p=0, and requires no assertion at p_c. Empty phases and p_c=0 or p_c=1 are allowed. The constants are not asserted uniform as p approaches p_c.

This is a statement about upper-invariant density from the all-one initial state. General attractive systems need not identify it with survival from a single occupied site. Contact-process duality provides that identification in that special model only. An arbitrary parameterized curve has not been shown to admit this generator identity or a suitable comparison and is not covered merely because it is monotone.

The original OWR source and Hartarsky's published formulation supply the reason to use this restricted observable and ray. If one additionally permits a(0)>0, the upper-density dichotomy is the elementary degenerate case p_c=0: for p>0, θ_p′(t)=pE[a(X_t)]-θ_p(t)≥pa(0)-θ_p(t), whence ρ(p)≥pa(0)>0. That observation is not an extension of the accepted perturbative ergodicity theorem to nonabsorbing systems.

## 10. Repair ledger and final acceptance boundary

The audit's necessary corrections/completions are local to the existing proof:

1. **p. 3, centered shift:** use ξ(x+y), or τ_{-x} with the printed minus convention, consistently. The literal mismatched convention is not accepted.
2. **pp. 8-10, pivotal finite dependence:** include backward ancestors of the inserted update's whole local neighborhood when proving continuity and finite-box convergence. Keep the original origin cluster for the uniform pivotal-probability majorant.
3. **p. 14, footnote 9 and CTDT assertion:** specify a Borel tie order and simultaneous pre-time updates at equal times; prove the all-configuration stopping and determining properties by replay. These completions alter only null-case conventions and supply omitted measurability arguments.
4. **p. 15, translated box:** start the comparison process from one on y+Λ_{2m}. This restores the stated translation-law equality.
5. **p. 17, calculus:** retain the first correct bound, correct the following swapped-parameter limsup, and state downward closure of the threshold set.

Items 1, 4 and 5 correct actual printed convention/display errors. Items 2 and 3 supply omitted technical justification or explicit null-configuration conventions. The first p. 17 logarithmic bound is already correct and is not classified as an error.

No counterexample or unresolved substantive implication remains for the scoped theorem once these completions are installed. Every use of the substantial published dependency has its hypotheses verified. This is ordinary mathematical proof acceptance, not machine-checked formal verification and not a referee/journal decision.

The main conclusion is therefore stronger than the previous applicability-only audit but no broader in model scope: **independently accepted prior-preprint proof, with explicit local repairs, for the absorbing attractive finite-range translation-invariant binary single-site death perturbation and its upper-density death-mixture ray.** The broader cleaned record remains unclosed by this result.

## Public references

- Bérard, Dembin and Marêché, v2: https://arxiv.org/abs/2510.11424v2 ; current record: https://arxiv.org/abs/2510.11424
- Author publication record: https://irma.math.unistra.fr/~mareche/page_anglais.html
- Last, Peccati and Yogeshwaran, published article: https://doi.org/10.1002/rsa.21136
- Inspected LPY author manuscript: https://arxiv.org/abs/2101.07180v3
- Independent publication metadata: https://publikationen.bibliothek.kit.edu/1000160403
- Original workshop report: https://doi.org/10.4171/owr/2022/41
- Hartarsky, *Bootstrap percolation, probabilistic cellular automata and sharpness*: https://doi.org/10.1007/s10955-022-02922-6 ; author manuscript https://arxiv.org/abs/2112.01778v2
