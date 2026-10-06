# PR292: ROOT mathematical adjudication

The submitted all-load result is mathematically accepted for the exact six-rate continuous-time chain below. Two independently initialized mathematical families reconstructed the complete argument and sealed their own derivations and controls before reading the author's checker. ROOT read the proof and both complete derivations, authenticated their closed evidence, and reproduced meaningful controls. No unresolved mathematical defect was identified. Worldwide priority and publication readiness remain unaccepted.

## Exact claim and original-problem scope

For each fixed real λ>0, take state (a,b,x,y) in the nonnegative integer lattice and D=x+y+1. The arrival increments (1,0,0,0) and (0,1,0,0) have rates λ/2 each. First downloads have increments (−1,0,1,0) and (0,−1,0,1), at rates a(x+1)/D and b(y+1)/D. Departures have increments (0,0,−1,0) and (0,0,0,−1), at rates x(y+1)/D and y(x+1)/D. A decrement at a zero coordinate has zero rate. This chain is nonexplosive, irreducible and positive recurrent, and therefore has a unique stationary probability.

The permanent seed, invisible empty waiting rooms and immediate complete-peer departure are essential model conventions. The inspected January 2011 author proof, Figure 2 and its denominator paragraph, agree with these rates. Its Conjecture 3.6 conjectures stability; every fixed positive λ is the explicit formalization of the unqualified parameterized conjecture and all-input-rate context, not a quotation of a literal universal quantifier. The earlier 2009 version conjectured the opposite outcome. The original 2010 workshop question selects this stochastic DFC model; its other open questions are outside the result. The final publisher PDF has not been authenticated, so identity with that unseen body is not asserted.

## Checkable all-state mechanism

Put W=2a+2b+x+y and Z=a+x−b−y. If u and d are respectively the total download and departure rates, then LW=2λ−u−d, LZ=(y−x)/D, and the total rate of unit Z jumps is λ+d. Define the rounded absolute value h_m(z)=z²/(2m)+m/2 for |z|≤m and |z| otherwise. Its clipped derivative is globally 1/m-Lipschitz. Thus its Taylor upper bound holds across noninteger rounding interfaces as well as at their endpoints.

Choose β=17λ/8, q=7/8, c=2(β+4), m=4c, θ=β+c+4, γ=(θ+1)/(θ+2), η=(1+γ)/2 and ℓ=1/(η−γ). The preceding exact identities give

    L(W+c h_m(Z)) ≤ β−u−qd+c h'_m(Z)(y−x)/D.

On {0,…,R}, reflect the birth–death chain with births γ(k+1) and deaths k. Its geometric weights give mean μ_R increasing to θ+1. Choose finite R with μ_R>θ and q(R+1)>β+c+2. The finite Poisson equation Qg=k−μ_R has a nonnegative decreasing solution with g(R)=0: use increments

    t_k = [Σ_{j=0}^k γ^j(j−μ_R)] / [γ^(k+1)(k+1)],
    g(k) = −Σ_{j=k}^{R−1} t_j.

The prefix conditional mean is strictly below μ_R, so every t_k is negative. The flux equations include both endpoints; Qg(R)=R g(R−1)=R−μ_R. Extend g by zero above R and write G=g(0). When b/D≥γ and y≤R, more births multiply nonpositive increments and fewer deaths multiply nonnegative increments, giving Lg(y)≤y−μ_R pointwise. This does not replace the evolving original coordinate by a stationary fast process.

Let f be zero up to γ, linear of slope ℓ between γ and η, and one above η. Set J=f(b/D)g(y)+f(a/D)g(x) and V=W+c h_m(Z)+J. In the exact product identity use the post-jump g factor on cutoff increments. First downloads increase D and do not increase the corresponding numerator, so their interface costs are nonpositive even for arbitrarily large empty populations. Arrivals cost at most ℓGλ/D. Departures have D≥2 and cost at most 4ℓGd/D, including saturation. Consequently

    LJ ≤ f(b/D)Lg(y)+f(a/D)Lg(x)+ℓG(λ+4d)/D,
    LJ ≤ G(λ+2d).

Choose a finite integer N satisfying N≥R+2, N≥3(R+1), (1−η)N−(1+η)R−η≥m, and N≥ℓG[λ+4(2R+1)]. Such an integer exists for every fixed positive real λ. Put

    B=(N+R+1){β+c+G[λ+2(N+R)]+1}.

If both visible counts exceed R, every current and successor correction vanishes and d≥min(x,y), giving drift below −2. If y≤R and x≥N, the other correction vanishes, d≤2R+1, qd≥y and the interface bound is at most one. For b/D≥η, the Poisson correction gives drift below −3. Otherwise Z≥m and (x−y)/D≥1/2, giving drift at most β−c/2+1−u=−3−u; the cutoff transition band is included. Exchange the two types for the symmetric case. In all remaining states x+y≤N+R, and u≥(a+b)/(N+R+1); the coarse bound gives drift at most −1 when a+b>B. These regions are exhaustive. Thus LV≤−1 outside the finite set F={x+y≤N+R,a+b≤B}, and V≥W≥a+b+x+y.

## Construction and recurrence inference

Arrivals are a Poisson process of rate λ. Internal events decrease W by one and arrivals increase it by two, so the total event count by time t is at most W(0)+3P_λ(t); no explosion is possible. Positive-rate finite drain and arrival/download paths give irreducibility. Also V has a linear upper bound in W and bounded single-jump increments. Localized Dynkin, stopped at F and at a finite population boundary, gives an expected stopped-time bound by V(s). Nonexplosion and monotone convergence/Fatou remove the localization and yield E_s τ_F≤V(s).

From finite F, fixed-duration drain trials have a uniform positive success probability. The Poisson bound and the linear upper bound on V give a uniform finite unconditional expected trial-plus-return duration. Strong Markov and a geometric trial tail therefore give finite mean hitting time of zero. At zero the mean holding time is 1/λ and there are only two exit neighbors, so the strict continuous-time return cycle has finite mean. Its normalized occupation law is stationary; irreducibility gives uniqueness. No invariant population moment, uniform-in-load bound, averaging hypothesis, simulation inference or embedded-chain holding-time assumption is used.

## Evidence and exact remaining gap

The original author checker reproduced 71,165 assertions over 5,200 states, and the older submitted independent checker reproduced 36,709 over 1,908 states. Fresh distinct families supplied 2,043 and 10,846 exact states with boundary, support, rounding and negative controls. ROOT separately replayed the first family's 2,043 states and the second family's 3,522 small-load states with complete exact data equality. These finite calculations corroborate the analytic proof; they do not prove its universal quantifiers.

Initial independent routes established low-load recurrence by distinct Foster and workload-coupling mechanisms and recorded their precise high-load gaps. Their affine obstruction and critical fast-process cautions remain valid method limitations; the verified nonlinear pointwise corrector closes those gaps for this chain. Historical capture qualifications and ROOT receipt-reader mistakes are retained in the acceptance records and logs; no failed metadata reader is relabelled a mathematical counterexample.

Mathematical validation100%; source correspondence100% within the stated edition limits; worldwide priority0% clearance; preprint/publication0%. No paper, DOI, tracker row, PR mutation or merge is authorized by this adjudication. The next required step is an extensive independent primary-source priority audit, including exact-protocol descendants and potentially equivalent general stability theorems. AI tools were used extensively; this is an unrefereed research audit and has not received formal human peer review.
