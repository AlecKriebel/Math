# A physical-clock constraint on the proposed condensation profile

**Target:** 30002926 / OWR-13856-002.  
**Status:** a source-qualified counterexample to the printed physical-time normalization; the clock-corrected Gamma-profile existence problem remains unresolved. Separate adversarial review pending. One substantive approach. No priority or human peer-review claim.

## 1. Exact model, source and unresolved scope

The [complete Oberwolfach report](https://ems.press/content/serial-article-files/46582), Mörters' contribution, printed pp. 1997–1999, defines a continuous-time population model as follows. Initially one individual has fitness sampled from a probability measure μ on (0,1), with essential supremum one. Individuals live forever. An individual of fitness f gives birth to one new individual at rate f. A birth is a mutation with probability β; a mutant's fitness is sampled independently from μ. Otherwise the offspring inherits its parent's fitness. We retain this physical clock, including its specified birth rates.

Write N(t) for population size and Ξ_t for the **normalized** empirical fitness measure. The source defines Ξ_t(A) by dividing the number of individuals in A by N(t) on p. 1997. A later family-sum display on p. 1998 omits that factor; throughout this argument we use the explicit normalized definition, not the inconsistent unnormalized display.

Put

    c=1−β,       I=∫_(0,1) (1−f)^−1 μ(df),
    ρ=1−β I.

We work with 0<β<1 and strict condensation β I<1, so I is finite, c>0 and ρ>0. The notation ρ is the source's γ(β), the condensate mass; it must not be confused with the clonal birth-rate coefficient c.

The source assumes μ(1−ε,1)=ε^α ℓ(ε) and prints

    Ξ_t(1−x/t,1) → ρ/Γ(α) ∫₀ˣ e^−y y^(α−1) dy.          (1)

No change from physical time is announced between its model definition and this formula. We show that (1) cannot hold in probability in a genuine positive-mutation condensation example. Stronger convergence to the same deterministic limit is therefore also impossible.

The distinction is substantive but limited: on the scale t(1−f), a possible Gamma limit must have **rate c**, rather than rate one. Equivalently a unit-rate expression would use the clone clock s=ct, and the window 1−x/(ct). We do not prove that this repaired profile exists or determine its shape parameter.

The later [Dereich–Mailler–Mörters paper](https://arxiv.org/abs/1601.08128) defines a larger reinforced-branching family. Its Example 1 identifies this model by setting its clonal parameter γ=1−β, and its physical birth clocks remain explicit. Its conjecture on p. 20 prints shape α+1, whereas the OWR formula prints shape α; its regular-variation assumption on p. 5 still uses tail exponent α. These distinct printed conjectures are not silently equated. Its theorem about the fitness of the **largest family** concerns a different observable, not the normalized collective condensate. Neither that theorem nor the deterministic Kingman model is used to claim collective convergence here.

## 2. Necessary clock condition

Let G_(k,λ) be the Gamma cumulative distribution function with shape k>0 and rate λ>0:

    G_(k,λ)(x)=λ^k/Γ(k) ∫₀ˣ y^(k−1)e^(−λy) dy.

**Theorem.** In the physical-time model above, assume I<∞ and ρ>0. If, for some m>0, k>0 and λ>0,

    Ξ_t(1−x/t,1) → m G_(k,λ)(x)

in probability for every x>0, then necessarily λ=c. In that case, for every q>1,

    N(qt) / [N(t)e^(c(q−1)t)] → q^(−k)                  (2)

in probability. The theorem assumes the proposed profile convergence to obtain a necessary condition; it does not assert that such convergence occurs.

The proof uses only the actual branching process, a uniform first-moment bound, and negligible late mutations in a shrinking fitness band. In particular, no precise polynomial correction to N(t), no independence of N(t) from the empirical fitness distribution, and no unproved mean-field replacement is assumed.

## 3. Uniform expected growth from any starting fitness

Let m_f(h) be the expected population at time h, starting from one individual of fixed fitness f∈(0,1), including all its descendants. Let m_μ(h)=∫m_f(h)μ(df). Birth rates are at most one per individual, so the process is dominated by the rate-one Yule process and is nonexplosive; these expectations are finite at every finite h.

The descendants without mutation of the initial individual form a Yule family of rate cf. Its expected size at age s is e^(cfs). Mutants are born from that family at mean rate βf e^(cfs), and each starts an independent full population with mean m_μ. Decomposition by the first mutant ancestor gives the exact renewal identity

    m_f(h)=e^(cfh)+βf∫₀ʰ e^(cfs)m_μ(h−s) ds.

Define u_f(h)=e^(−ch)m_f(h), u(h)=∫u_f(h)μ(df), and

    a(h)=∫ e^(−c(1−f)h) μ(df),
    K(h)=β∫ f e^(−c(1−f)h) μ(df).

Then u=a+K*u. The nonnegative renewal series u=∑_(j>=0)K^{*j}*a follows by classifying individuals by the number of mutant ancestors. Every individual at finite time has a finite genealogy, so Tonelli's theorem justifies this series without a hidden integrability assumption.

Direct integration gives

    ||a||₁=I/c,
    ||K||₁=(β/c)(I−1)<1,
    ||u||₁=(I/c)/[1−(β/c)(I−1)]=I/ρ.

The fixed-fitness identity, after discounting, is

    u_f(h)=e^(−c(1−f)h)
              +βf∫₀ʰ e^(−c(1−f)s)u(h−s) ds.

Thus u_f(h)<=1+β||u||₁=1/ρ, uniformly in f and h. We have proved

    m_f(h)<=ρ^−1 e^(ch).                                 (3)

Let F_t denote the complete population history up to t. The branching property now gives, with no distributional assumption on the current fitnesses,

    E[N(t+h)|F_t] <= ρ^−1 N(t)e^(ch).                     (4)

## 4. Old clones and late high-fitness mutants

Fix q>1 and x>0, put h=(q−1)t, and define the deterministic band

    B_t=(1−x/(qt),1).

At time qt every individual with fitness in B_t is either a mutation-free descendant of an individual already present at t, or belongs to a clonal family whose mutant founder was born after t with fitness in B_t. These alternatives give an exact partition by the most recent mutation after t; if there is none, use the ancestral individual present at t.

### Old clone fluctuations

Conditional on F_t, start one independent clonal Yule process from each of the N(t) individuals. Mutation branches are excluded. Existing genealogical relations among the individuals do not interfere: their future birth clocks and future clonal descendants form independent subtrees when the population is cut at time t.

If C_t(x) is the number of old-clone individuals in B_t at qt, then

    E[C_t(x)|F_t]
      = sum_(v alive at t) 1_{F_v∈B_t} e^(cF_v h),
    Var(C_t(x)|F_t)<=N(t)e^(2ch).

The variance bound is the Yule variance e^(2cF_vh)−e^(cF_vh) and conditional independence. Moreover N(t)→∞ almost surely: the original immortal individual has strictly positive fitness and continues producing births forever. Since 0<1/N(t)<=1, conditional Chebyshev and dominated convergence imply

    C_t(x)/[N(t)e^(ch)]
      − E[C_t(x)|F_t]/[N(t)e^(ch)] → 0                   (5)

in probability.

### Late mutations

Let L_t(x) be the remaining population in B_t at qt. A mutant founder at time s and fitness f has expected clonal size e^(cf(qt−s)) at qt. The marked mutation-birth compensator is

    β [sum_(v alive at s) F_v] μ(df) ds.

Its total-fitness factor is at most N(s). Taking conditional expectations, applying (4), and using f<=1 gives

    E[L_t(x)|F_t]
      <= β μ(B_t) ∫_t^(qt) E[N(s)|F_t] e^(c(qt−s)) ds
      <= (β/ρ) h μ(B_t) N(t)e^(ch).                     (6)

This bound neither assumes independence between mutation intensity and population size nor replaces a random normalization by its expectation.

Finite I implies μ(1−ε,1)=o(ε), because

    μ(1−ε,1)/ε <= ∫_(1−ε,1) (1−f)^−1 μ(df) → 0.

Consequently t μ(B_t)→0. Conditional Markov's inequality applied to (6) proves

    L_t(x)/[N(t)e^(ch)] → 0                              (7)

in probability. No regular-variation theorem is needed for this step; strict condensation with positive β already provides the required integrability.

## 5. The random-normalization consistency equation

Let ν_t be the normalized measure obtained from Ξ_t by the map f↦t(1−f), and write H_t(x)=ν_t((0,x)). Define the random quantity

    R_t(q)=N(qt)/[N(t)e^(ch)].

Combining the exact count partition with (5)–(7) yields, for each fixed x>0,

    R_t(q) H_(qt)(x)
      = ∫_(0,x/q) e^(−c(q−1)y) ν_t(dy)+o_P(1).           (8)

Assume the profile in the theorem, so H_t(x)→H(x)=mG_(k,λ)(x) in probability for every x>0. The right side of (8) converges to

    J_q(x)=∫₀^(x/q) e^(−c(q−1)y) dH(y).

For completeness, this passage does not require uniform-in-x convergence: for L=x/q and a=c(q−1), integration by parts expresses the integral as

    e^(−aL)H_t(L)+a∫₀ᴸ e^(−ay)H_t(y)dy.

The bounds 0<=H_t<=1 and pointwise convergence in probability imply convergence in L¹ of each H_t(y); dominated convergence and Fubini control the integral. The Gamma limit is continuous and has no mass at zero, so the open-interval convention causes no endpoint term or ambiguity.

Since H_(qt)(x)→H(x)>0, division in (8) proves

    R_t(q) → J_q(x)/H(x).                                (9)

The left side is the **same random variable for every x**. Uniqueness of a limit in probability therefore forces the ratio on the right to be a constant r(q)>0, independent of x. This is where the random population normalization is controlled; no prior growth-ratio limit is inserted.

Differentiate the resulting deterministic identity r(q)H(x)=J_q(x). The positive Gamma density h=H' gives

    r(q)h(x)=q^−1 e^(−c(q−1)x/q) h(x/q),

and hence

    r(q)=q^(−k) exp[(λ−c)(q−1)x/q].                     (10)

It is independent of x only if λ=c. Substitution into (10) gives r(q)=q^(−k), proving the theorem and (2). QED.

## 6. Explicit counterexample to the displayed normalization

Choose

    μ(df)=2(1−f)df on (0,1),        β=1/4.

Then μ(1−ε,1)=ε², so the source regular-variation condition holds with α=2 and ℓ=1. Also I=2, ρ=1/2 and c=3/4. This is a positive-mutation strict-condensation example, not the degenerate β=0 boundary.

The printed OWR limit is m=1/2 times a Gamma distribution of shape two and rate one. The theorem requires rate 3/4, so the printed physical-time assertion cannot hold.

A direct version of the contradiction uses q=2 and G(x)=1−(1+x)e^−x. In (9) the proposed limit would force

    R_t(2) → (16/49) G(7x/8)/G(x), for every x>0.

This ratio tends to 1/4 as x decreases to zero and to 16/49 as x increases without bound, so it is not constant. These are limits of a deterministic candidate ratio **after** (9) has been established for each fixed x; no interchange of the population limit with x→0 or x→∞ is assumed.

## 7. The precise remaining problem

If physical time is rescaled to s=ct, then a Gamma law with rate c on t(1−f) becomes a unit-rate Gamma law on s(1−f). A unit-rate version consistent with the necessary clock condition would therefore examine Ξ_t(1−x/(ct),1). This is a change of the printed normalization, not a proof of its corrected version.

The argument does not prove convergence of ν_t, identify the actual shape parameter, establish a precise population-growth asymptotic, or resolve the intended universality of Gamma condensate waves. The source and later paper print different shape parameters, and this work does not choose between them. Existing deterministic Kingman results and largest-family limit theorems remain credited, distinct results.

Recommended conservative disposition: **unsolved, with a proved physical-clock obstruction to the exact printed formula, 1/5 approaches**. Priority for the clock constraint has not been established. The exact checker supplies algebraic and normalization controls; the probabilistic proof is Sections 3–5 and requires separate adversarial review before publication.
