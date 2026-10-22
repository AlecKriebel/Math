# The BMP quasi-locality bridge: a positive implication and an unresolved source ambiguity

## Source status and the range discrepancy

The complete BMP1999 original was not obtained. The indexed primary BMP2007 survey, printed p680, §1.4.3, was exposed by a targeted primary-domain search on 2026-10-15. Its actual-file link is
https://www.mathnet.ru/links/a9699e240be5a8ff3e2617cf62aceb2c/rm6849_eng.pdf ; its DOI is 10.1070/RM2007v062n04ABEH004428. Direct retrieval failed. This is partial primary passage access, not complete-source clearance.

The passage has two apparently inconsistent range statements. It first defines u_T=(X_T−bT)/√T and discusses |u_T|=o(T^(1/6)), which corresponds algebraically to |X_T−bT|=o(T^(2/3)) and includes every fixed diffusive bulk. Its final displayed condition instead reads literally |x̄_T−bT|=o(T^(1/6)), without the normalization. Dunlap–Gu's inspected May27,2021 and Dec8,2021 sources describe BMP1999 Theorem2 using a third expression, |x|≪t^(1/3).

These statements are not reconciled by the simple substitution u_T=(X_T−bT)/√T. The original is required to identify a typo, convention, different scaling, or amended theorem. **No exclusion of BMP1999 on the ground that its window misses the diffusive bulk is justified by this audit.** The tail gap described below remains even if the largest plausible window is granted.

The indexed survey defines a finite-state field functional Φ to be quasi-concentrated through uniform cylinder oscillation:

    osc_R(Φ)=sup{|Φ(η1)−Φ(η2)| : η1,η2 in Ω̃,
                      η1 and η2 agree in the finite cube O_R} →0.

Here Ω̃ is a full-measure domain of finite Φ. It asserts a weighted local asymptotic with a terminal shift of Φ and EΦ=1. Its associated main CLT (Theorem1.1.1, printedp669) specifies a.s. and L2 convergence, and the local paragraph writes an o(1) term without specifying a deterministic environmental-tail rate. We do not silently interpret that o(1) as uniform over η.

## A. Uniform quasi-locality does supply strong concentration of the stationary factor

This original deduction tests the strongest reasonable reading of the definition. It is not attributed as a theorem stated in BMP1999 or BMP2007.

Let η be an iid field taking values in a finite set, and let Φ be a real finite functional on a full-measure set Ω̃ with osc_R(Φ)→0. Fix R large enough that osc_R≤1. There are only finitely many field patterns in O_R. Choose one representative in Ω̃ from each nonempty cylinder. Every Φ value differs by at most1 from the representative value in its cylinder, so Φ is uniformly bounded on Ω̃. This uses finiteness of the local alphabet.

For any δ>0 choose a fixed finite R=R(δ) with osc_R≤δ. The representative construction gives a cylinder function Φ_R with sup_(Ω̃)|Φ−Φ_R|≤δ. Since EΦ=1, its recentered version Ψ_R=Φ_R+1−EΦ_R satisfies EΨ_R=1 and sup|Φ−Ψ_R|≤2δ. Its bound B_R is finite.

Work in parity-sheared coordinates so the deterministic terminal weights b_N(x) are Binomial(N,q). Define

    H_N(Ψ)=Σ_(I in partition)|Σ_(x∈I)b_N(x)(Ψ(shift_(x,N)η)−1)|.

Changing Ψ by at most2δ changes H_N by at most2δ, because Σb_N=1. The finite-radius field Ψ_R(shift_(x,N)η) is finite-range dependent in x. If its dependence cubes have spatial radius R, distinct coordinates separated by more than2R use disjoint iid inputs. Its variance/covariance are bounded by constants depending on R and B_R. Consequently

    Var[Σ_(x∈I)b_N(x)(Ψ_R(shift_xη)−1)]
        ≤ C_R Σ_(x∈I)b_N(x)²,

where 2ab≤a²+b² handles adjacent covariance terms. For clarity, use a separate central-window radius A≥1, keeping the cylinder radius R fixed. The central-window/truncation proof gives

    EH_N(Ψ_R)≤C_R√(A/M+N^(−1/2))+C(B_R+1)/A².

Here Ψ_R may have either sign after recentering, so tail cells use

    E|Σ_(x∈J)b_N(x)(Ψ_R(shift_xη)−1)|≤(B_R+1)b_N(J),

not a positivity argument. First fix A, let N,M_N→∞, and then let A→∞. This proves EH_N(Ψ_R)→0 uniformly over deterministic alignments. No rate of divergence of M_N is needed.

For concentration, expose each iid space-time input z in the union of dependence cubes. Its modification changes at most the Ψ_R coordinates whose centers are within R of its spatial coordinate. Therefore its bounded-differences oscillation for H_N is at most

    c_z≤2 B_R Σ_(|x−z_space|≤R)b_N(x).

There are only a fixed number (depending on R) of relevant time layers. Young's convolution inequality, or Cauchy–Schwarz followed by summing x, gives

    Σ_z c_z² ≤ C_R Σ_x b_N(x)² ≤ C_R/√N.

This argument sums actual weights; the cruder count of all N support sites would lose the useful power. Independent-input bounded differences now gives

    P(H_N(Ψ_R)−EH_N(Ψ_R)>s)≤exp(−c_R s²√N).

For fixed ε choose δ<ε/16 and then fixed R(δ). Eventually the mean is below ε/4. Sup approximation transfers the same fixed-ε bound to H_N(Φ), after changing constants. **Thus a bounded uniformly quasi-local stationary corrector itself has the requested all-diverging-scale superpolynomial coarse concentration.** A quantitative decay rate of osc_R is unnecessary because ε is fixed and R may depend on ε.

This positive deduction prevents an overbroad objection that every stationary-corrector route needs a polynomially growing approximation radius or high moments. Uniform quasi-locality is strong enough by itself for this part.

## B. The missing local-limit residual is a separate random object

Suppose a source also supplies μ_N(x)=b_N(x)Φ(shift_(x,N)η)+r_N(x). To transfer A to the full endpoint discrepancy, one still needs

    P(Σ_x |r_N(x)|>ε)=O(N^(−K)) for every K,

or a sufficient weaker control after coarse summation, uniformly over the relevant diffusive region. A qualitative a.s. o(1), an L2 o(1), or one-point asymptotics along a deterministic sequence does not supply this. The adversary's normalized binomial example proves the nonimplication from these summaries even when Φ≡1.

If the original result proves a deterministic uniformly-in-η residual on a growing window containing the bulk, then A and elementary annealed tail control would be a promising exact finite-state implication. If it proves only a.s./L2 convergence, the all-K residual failure probability remains an unsupported bridge. The unavailable original prevents deciding that fork. No source claim is promoted past it.

## C. A bounded corrector cannot automatically be identified with the generic JRS density

The following independently checked lemma concerns the JRS invariant density, not the validity of an unread BMP theorem.

Take a fixed target law giving positive probability to each of p=r and p=1−r, with0<r<1/2. Define a deterministic comparison birth–death walk on Z by

    p_x=1−r for x≤0,   p_x=r for x≥1.

It drifts toward the edge {0,1}. Write P for its transition matrix, d=1−2r>0, ρ=r/(1−r)<1, and π0=π1=(1−ρ)/2. A reversible stationary probability has π_(−k)=π0ρ^k and π_(1+k)=π1ρ^k for k≥0.

The column sum of P at y is1+d for y=0,1 and1 elsewhere. Starting from counting measure, iteration therefore gives

    u_T(0):=Σ_x P^T(x,0)
           =1+d Σ_(s=0)^(T−1)[P^s(0,0)+P^s(1,0)].

Reversibility and Cauchy–Schwarz imply

    P^(2n)(0,0)=π0 Σ_z P^n(0,z)²/π_z ≥π0.

Hence u_T(0)≥1+dπ0 ceil(T/2), which diverges. All sites that can reach0 in T nearest-neighbor steps lie in a finite backward cone. Enforce the deterministic comparison p values on that cone during the last T time layers. This event has positive probability under the fixed two-atom iid law, and the finite-past column sum f_T at the origin equals u_T(0) there. Opposite-parity starts contribute zero, so the exact shear to {0,1} preserves this column sum and puts it within JRS's span-one hypotheses.

JRS's L2 martingale construction gives f_T=E[f | last T layers]. If f were essentially bounded by B, all f_T would be bounded by B. The preceding positive cylinder events contradict that for large T. **Thus f has unbounded support even for this fixed finite-state uniformly elliptic law.**

Part A showed that literal uniform finite-state quasi-locality implies bounded Φ. It follows that Φ cannot automatically be equated with this generic JRS f. This is a warning that the source's precise assumptions, definition, and limiting object must be resolved. It is not a claim that BMP1999 is false: identifying their Φ with JRS f under the original hypotheses is an additional statement that this audit has not proved from the inaccessible original.

## Audit status

The quasi-local stationary-factor bridge is established conditionally on the explicit uniform definition. The BMP source region, actual local-limit residual mode/rate, and precise corrector identification remain unresolved. Therefore this family does not currently establish older exact coverage of the PR239 full claim, and does not establish novelty either.
