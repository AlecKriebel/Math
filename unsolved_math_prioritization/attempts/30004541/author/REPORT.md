# Extinction criteria for the continuous-time Derrida–Retaux process

Problem 30004541 · OWR-2654828-006 · rank 754  
Research date: 5 October 2026  
Disposition: **NO RESOLUTION of the bundled general problem.** Five substantive approaches are recorded below. The results proved here are partial controls and obstructions, not a new solution or a novelty claim. Independent audit remains required before publication.

## 1. Exact target and model

The original question is in Yueyun Hu's contribution, with Bastien Mallein and Michel Pain, to *Stochastic Processes under Constraints*, Oberwolfach Report 32/2020, printed page 1641, Question 2 and Conjecture 3. The PDF was both text-inspected and visually checked at that page. The task has two parts:

1. Characterize the initial probability laws on [0,∞) whose continuous-time free energy is zero.
2. Establish or refute convergence to zero in probability whenever that free energy is zero.

Let μ_t be the law of X_t. Between rate-one Poisson jump opportunities the state decreases at speed one until it reaches zero; at a jump an independent sample from μ_t is added. Equivalently, with a Poisson random measure N of intensity dt du and the right-continuous quantile Q_t of μ_t,

X_t = X_0 − ∫_0^t 1_{X_s>0} ds + ∫_(0,t]∫_(0,1) Q_s(u) N(ds,du).

The quantile may be defined by inf{x≥0: μ_t([0,x])>u}. Endpoint choices at u=0,1 are immaterial. The weak law equation, for bounded C¹ test functions with bounded derivative, is

d/dt ∫ f dμ_t = −∫_(0,∞) f'(x) μ_t(dx) + ∫∫ f(x+y) μ_t(dx)μ_t(dy) − ∫ f dμ_t.

Its tree representation uses binary splitting, with independent exponential holding times of mean one. Starting with one particle, the number of leaves at time t has probability e^(−t)(1−e^(−t))^(k−1), k≥1. Independent μ_0 amounts at the leaves flow toward the root, losing one unit per unit edge length and adding at mergers. Geometric leaf counts do **not** turn this into a discrete model with geometric offspring at every generation.

No finite moment is needed for existence of the law dynamics. The relevant free energy is F(μ_0)=lim_(t→∞) e^(−t) E[X_t], in the extended nonnegative reals. Infinite initial mean forces infinite mean at every finite time and hence infinite free energy in this sense. Thus a zero-free-energy law necessarily has finite mean. See Proposition 1 below for a direct argument.

In this problem, “extinction” means X_t→0 in probability, namely P(X_t>ε)→0 for each ε>0. It is not defined as P(X_t>0)→0, almost-sure convergence, or eventual permanent absorption. A sample path at zero can receive a positive jump while μ_t is nontrivial. The whole law δ_0 is absorbing.

For comparison only: the usual discrete binary recursion is Y_(n+1) = (Y_n^(1)+Y_n^(2)−1)_+ in distribution, with independent copies, and free energy lim 2^(−n)E[Y_n]. Its integer-valued criterion involves E[Y_0 2^Y_0]≤E[2^Y_0]<∞. The integer support and exact subtraction by one are essential. This is not an initial-law criterion for the continuous-time process here.

## 2. Source and prior-work review

- Hu–Mallein–Pain, *An exactly solvable continuous-time Derrida–Retaux model*, published in Communications in Mathematical Physics 375 (2020), 605–651; inspected arXiv:1811.08749v2. Definitions 1.4–1.7, Theorem 1.8, Section 3, and Section 6 establish the model and special cases. Conjecture 6.4 is the same extinction question. This source already contains the free-energy identity and the necessary moment inequalities used below; they are not claimed as new.
- Li–Zhang, arXiv:2411.12189v2, *Derrida–Retaux type models and related scaling limit theorems*: construction and finite-horizon scaling limits for generalized offspring. Its main statements do not supply the required uniform large-time extinction estimate.
- Li–Zhang, arXiv:2411.13068v3, *Asymptotic behavior of the generalized Derrida–Retaux recursive model*: geometric offspring and geometric-type initial laws. This restricted solvable family does not cover arbitrary μ_0 in the present process.
- Alsmeyer–Hu–Mallein, arXiv:2502.02991v2, revised 9 April 2026, *The Derrida–Retaux model on a geometric Galton–Watson tree*: exact critical curves and near-critical free energy for particular invariant two-parameter families. That result concerns a different recursion and restricted initial laws.
- Duquesne–Shi, arXiv:2609.11435, September 2026, *The continuous Derrida–Retaux branching process in the Brownian CRT*: a critical growth-fragmentation limit on [0,1). That “continuous” branching process is not the arbitrary-initial-law McKean–Vlasov process on [0,∞) posed here.

No full resolution of either general part was verified in this search. This is a dated, bounded search result, not proof that no later or unindexed result exists. Source versions, hashes, locations, and inspection limits are in SOURCE_VERIFICATION.json.

Both full cached public corpora were independently rehashed and matched the repository's immutable dataset manifest. There is exactly one numeric-ID match in the problem corpus; the exact problem-code key is absent from the full prior-report dictionary. Read-only GitHub searches for the exact ID and topic found no matching prior PR or commit. The pinned main attempts directory has no 30004541 entry. Related-target groups contain no entry for this ID. These checks do not cover deleted or unpublished work.

## 3. Results and five approaches

### Approach 1: mass balance, tail bounds, and moment hierarchy

Write m(t)=E[X_t] and q(t)=P(X_t>0). Proposition 1 proves

m'(t)=m(t)−q(t),
F=e^(−t)m(t)−∫_t^∞e^(−s)q(s)ds,
F=0 ⇔ m(t)≤1 for every t≥0.

This last condition is an exact trajectory characterization, not the requested effective condition on μ_0 alone. It gives a finite-time certificate of positive free energy whenever m(t)>1. Under F=0, Proposition 2 gives the uniform bounds

P(X_t≥x)≤min(1,e^(1−x)),   E[X_t²]≤1/2.

The bounds imply tightness and uniform integrability. They do not imply that the first moment tends to zero. The hierarchy remains unclosed because m' depends on the atom at zero.

Status: useful exact controls; the general criterion and decay remain open.

### Approach 2: solvable family and a false-criterion obstruction

For μ_0=pδ_0+(1−p)Exp(λ), the family is invariant. Its parameters solve

p'=(1−p)(λ−p),   λ'=−λ(1−p),   H=p/λ+log λ=constant.

Proposition 3 derives the phase classification. Apart from p=1, zero free energy holds exactly when λ>1 and p≥λ(1−log λ). On the nontrivial critical curve, λ(t)−1∼2/t and 1−p(t)∼2/t². These are special-family statements only.

A particularly useful control is μ_0=Exp(5/2). Proposition 4 proves F>(2/5)e^(−40)>0, while the initial law simultaneously satisfies:

- P(X_0≥x)≤e^(1−x)
- E[X_0²]=8/25<1/2
- E[X_0e^X_0]=10/9<5/3=E[e^X_0]
- E[(1−θX_0−2(1−θ)X_0²)e^(θX_0)]>0 for every 0<θ<1

Consequently, even the conjunction of these known necessary inequalities at time zero is not sufficient. This is a counterexample to that proposed shortcut, **not** a counterexample to extinction under F=0.

Stochastic domination by a member of the zero-free-energy solvable family proves extinction for additional initial laws, but no argument places every zero-free-energy law under such an envelope.

Status: sharp obstruction to a natural moment criterion; general domination route incomplete.

### Approach 3: exponential Lyapunov region

Proposition 5 proves a sufficient condition without a finite-dimensional family assumption. If, for some θ>1,

M_0(θ)=E[e^(θX_0)]<θ,

then for c=θ−M_0(θ)>0,

E[e^(θX_t)]−1 ≤ (M_0(θ)−1)e^(−ct).

In particular E[X_t] and P(X_t>ε) decay exponentially. The proof uses capped tree dynamics to justify the exponential-moment differential inequality without assuming beforehand that the moment remains finite. For deterministic X_0=a this gives extinction whenever 0≤a<1/e.

This is only a sufficient region. It does not reach the nontrivial critical exponential mixtures, whose decay is polynomial. A criterion that forced this exponential bound for every F=0 law would already contradict those critical examples.

Status: complete partial theorem, insufficient for the general target; no optimality or novelty asserted.

### Approach 4: Laplace transforms and stationary-limit exclusion

For L_t(s)=E[e^(−sX_t)] and p_t=P(X_t=0),

∂_t L_t(s)=L_t(s)²+(s−1)L_t(s)−sp_t.

The unknown boundary mass p_t prevents scalar closure. Proposition 6 nevertheless proves that δ_0 is the only stationary probability law with finite mean. The proof uses the stationary quadratic equation, the exponential tail control from Approach 1, and an elementary positive-coefficient power-series argument.

Consequently, if a zero-free-energy trajectory has a weak limit, that limit must be δ_0. Uniform tail bounds and continuity of the nonlinear semigroup justify this conditional implication. Tightness alone supplies subsequential limits, which need not be stationary. No Lyapunov functional excluding recurrent or nonconvergent law trajectories was obtained.

Status: a rigorous reduction; the missing convergence step is the core extinction difficulty, not a technicality to suppress.

### Approach 5: discrete approximation and transfer

Rare binary splitting approximations use offspring 1 with probability 1−1/K and offspring 2 with probability 1/K, time step 1/K, and erosion 1/K. This is different from simply sampling the fixed-binary integer-valued recursion. Finite-horizon convergence of the approximants cannot exchange K→∞ with t→∞. For example, the elementary functions f_K(t)=exp(−t/K) tend to zero for each K as t→∞ but tend to one for each fixed t as K→∞.

This is a logical control on a limit-interchange argument, not a DR counterexample. No uniform-in-K extinction estimate suitable for all initial laws was proved or located.

Status: blocked at a precise uniformity requirement.

## 4. Final disposition

The exact two-part target remains unresolved in this attempt. Five approaches were used; no sixth search route is proposed. Completion toward the full requested general resolution is estimated at 10%, a subjective planning estimate reflecting clarification and partial controls, not a probability or theorem. The strongest retained deliverables are the explicit false-criterion example, the exponential Lyapunov region, and stationary-law exclusion, each with a self-contained proof below.

No simulation is used as proof. The code performs exact symbolic checks and exact rational certificates only; it does not independently validate the analysis. No claim of new mathematics or global literature priority is made. No remote mutation was performed. Publication requires a fresh, uninvolved audit of the frozen artifact.

## References

1. Original problem: https://doi.org/10.4171/owr/2020/32
2. HMP: https://arxiv.org/abs/1811.08749v2
3. Li–Zhang scaling: https://arxiv.org/abs/2411.12189v2
4. Li–Zhang asymptotics: https://arxiv.org/abs/2411.13068v3
5. Alsmeyer–Hu–Mallein: https://arxiv.org/abs/2502.02991v2
6. Duquesne–Shi: https://arxiv.org/abs/2609.11435
