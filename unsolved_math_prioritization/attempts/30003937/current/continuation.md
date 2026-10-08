# Finite-time continuation: what the available estimates do and do not control

This is an authored audit of a continuation route for the beta=1 continuum DMK equation, not a global existence proof. The source Facca–Cardin–Putti, Theorem 1 and Proposition 1 of https://arxiv.org/abs/1610.06325v1 (associated publication https://doi.org/10.1137/16M1098383), reports a local Hölder-space theorem and bounded/Lipschitz elliptic and flux maps. The proof-level caveat below means local restart is an explicit assumption of the continuation implication in this note, rather than an independently certified consequence of that citation. The finite-time positivity estimate follows directly along any existing regular trajectory. No novelty claim is made.

Use the setting and energy S of `conditional_entropy.md`, and let T_max be the maximal classical existence time in C^δ. Write a₀=min μ₀>0 and S₀=S(μ₀).

## Continuation criterion, conditional on local restart

Assume that every strictly positive C^δ endpoint state under consideration admits a local regular solution in the same class, with enough time continuity to concatenate it with an existing trajectory. Then, if T_max<∞,

    limsup_{t↑T_max} ||μ(t)||_{C^δ}=∞.

Indeed, the mild equation gives μ(t)≥e^(−t)μ₀, hence μ(t)≥a₀e^(−T_max) for all t<T_max. If the Hölder norm were bounded by B, the trajectory would remain in one of the positive bounded sets D(a,b) from the local theorem, with fixed a>0 and b>B. Elliptic Hölder estimates bound ∇U(μ) on that set. The valid single-function inequality |||z|||_{C^δ}≤||z||_{C^δ} and the Banach-algebra product estimate therefore uniformly bound Q(μ)=μ|∇U(μ)|. Thus μ_t=Q(μ)−μ is uniformly bounded in C^δ, and μ has a C^δ limit at T_max. That limit remains strictly positive. The stated local-restart assumption then extends the solution, a contradiction. Endpoint convergence uses boundedness of Q, not Hölder compactness or C^δ-Lipschitz continuity of Q; extension still needs the restart assumption.

A direct sufficient estimate would be, for every finite T<T_max,

    ∫₀ᵀ || |∇u(t)| ||_{C^δ} dt < ∞

with a bound staying finite as T approaches any finite endpoint. The Banach-algebra product estimate and μ_t=μ(|∇u|−1) then give a Gronwall bound for ||μ||_{C^δ}. The existing elliptic estimates depend superlinearly on that same unknown norm; substituting them does not close this criterion.

## Imported proof caveat and what a weaker estimate does prove

In the inspected arXiv:1610.06325v1, printed p. 16, section 4.1, the final estimate for the C^δ Lipschitz bound of Q uses a generic comparison of the C^δ norm of |z₁|−|z₂| with that of z₁−z₂. That generic comparison is false, despite the valid pointwise reverse triangle inequality.

For 0<ε<1 on [-1,1], set z₁(x)=x and z₂(x)=x+ε. They are gradients of smooth scalar functions. The input difference has C^δ norm ε. At x=−ε and x=0 the output difference |z₁|−|z₂| takes values ε and −ε, so

    [|z₁|−|z₂|]_{C^δ} ≥ 2ε^(1−δ).

The ratio to ε diverges as ε→0. Thus no uniform Lipschitz constant for this generic composition step holds, even on a bounded smooth family. This is a counterexample to the proof step, not by itself a counterexample to Q on potentials arising from one fixed forcing. No claim is made here about whether another argument or the journal version repairs the reported local theorem.

There is a useful, narrower estimate. Suppose a≤μᵢ≤b, ||∇U(μᵢ)||∞≤G, and uᵢ=U(μᵢ), for i=1,2. Test the difference elliptic equation with u₁−u₂. Then

    ||∇(u₁−u₂)||₂ ≤ (G/a)||μ₁−μ₂||₂,
    ||Q(μ₁)−Q(μ₂)||₂ ≤ G(1+b/a)||μ₁−μ₂||₂.

The second line uses only the pointwise reverse triangle inequality. Gronwall therefore proves uniqueness among already existing regular trajectories whose conductivities and gradients obey these bounds on compact time intervals. It also justifies rotational symmetry of any such trajectory with radial data. It does not, on its own, establish existence or restart in C^δ. No new global construction is claimed.

## Bounds that do hold on finite intervals

Energy monotonicity and μ≥a₀e^(−t) give

    ||∇u(t)||²₂ ≤ 2S₀ e^t/a₀,
    ||u(t)||₂ ≤ C_P ||∇u(t)||₂,
    ||q(t)||₁=P(t)≤S₀,
    ||μ_t(t)||₁ ≤ P(t)+M(t)≤3S₀.

Here the second inequality uses the mean-zero gauge and the Poincaré constant of the connected domain. These are a finite-time H1 bound for the potential and a time-Lipschitz L1 bound for the density. They provide no spatial compactness of μ and no Hölder control of its time derivative.

## A static noncoercivity test

On Ω=(0,1), fix any nonzero smooth compactly supported, mean-zero f. Let

    F(x)=−∫₀ˣ f(s) ds,
    m_n(x)=2+cos(2πnx),     n=1,2,...,
    u_n'(x)=F(x)/m_n(x),    ∫₀¹u_n=0.

Then 1≤m_n≤3, ∫m_n=2, the flux is exactly m_nu_n'=F, and the Neumann conditions hold because F(0)=F(1)=0. Consequently

    A(m_n)=∫ F²/m_n ≤ ∫F²,
    S(m_n)≤1+(1/2)∫F².

But, taking x=0 and y=1/(2n),

    [m_n]_{C^δ} ≥ 2(2n)^δ →∞.

Thus even uniform upper and lower conductivity bounds, bounded energy, fixed forcing, and the exact elliptic equation do not control the norm required for continuation. These are static states, not states of one DMK trajectory. They do not establish finite-time blowup or disprove convergence.

## Exact gap

A genuinely new spatial regularity or compactness mechanism is needed. Replacing the missing Hölder estimate by energy monotonicity is invalid. The general multidimensional continuation problem remains unresolved in this work.
