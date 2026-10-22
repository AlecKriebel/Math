# Attempt 1: full-path formulation and an explicit non-TV example

Date: 2026-10-20. Target: AMR-098-0006, Thorisson Problem 3.2. Publication status: accepted partial result. The SC necessity question raised below was subsequently answered negatively in [Attempt 2](ATTEMPT_2.md); the positive general auxiliary-copy criterion is in [Attempt 3](ATTEMPT_3.md). See [SCOPE](SCOPE.md) for the final disposition.

## Source and exact problem

The entire Section 3 of Hermann Thorisson, *Some Open Probability Problems*, pp. 3–4, was read, not only the problem sentence. Public source: https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf . The state space is an arbitrary measurable space (E,ℰ). Write S=E^{N₀}, Σ=ℰ^{⊗N₀}, θ(x)=(x₁,x₂,…), μ=Law(X), and ν=Law(X′). The question asks for a coupling characterization of

μ(θ^{-n}A) → ν(A) for every A∈Σ.

These are fixed measurable sets of entire paths, not merely cylinders. The implication to total variation is the separate Problem 3.1; the desired characterization is Problem 3.2. The limiting law is stationary, since applying convergence to A and θ^{-1}A shows ν(θ^{-1}A)=ν(A). Corollary 3.1 already gives distributional shift coupling and Cesàro-TV convergence; neither answers the nonaveraged question.

## A self-contained negative answer to the antecedent Problem 3.1

Let E={0,1}^ℤ with its product σ-algebra, and let ρ be fair independent Bernoulli product measure. Put (Tz)_j=z_{j+1}; T is a measurable bijection preserving ρ. Let η be ρ conditioned on z₀=1, so dη/dρ=f(z)=2·1_{z₀=1}. Define the measurable orbit embedding Φ:E→S by Φ(z)_k=T^kz. Its zeroth-coordinate projection is its measurable left inverse. Set μ=Φ_*η and ν=Φ_*ρ. Thus ν is the law of a stationary process; μ is the law of the same deterministic dynamics from a biased initial state.

For any A∈Σ set B=Φ^{-1}A. Then

μ(θ^{-n}A)=η(T^{-n}B)=∫ 2·1_{w_{-n}=1}·1_B(w) dρ(w).

This tends to ρ(B)=ν(A). To prove this for every measurable B, fix ε>0 and approximate B in ρ-symmetric difference by a finite-coordinate cylinder C with ρ(B△C)<ε. For all sufficiently large n, the coordinate −n is outside those defining C, so independence gives ∫2·1_{w_{-n}=1}·1_C dρ=ρ(C). The difference for B is bounded by 2ρ(B△C)+ρ(B△C)<3ε. Finite-coordinate cylinder approximation holds by the usual monotone-class approximation of the product σ-algebra. No finite-dimensional-to-full-path inference is being made without this approximation step.

Nevertheless the total variation distance, normalized as sup over measurable events, is exactly 1/2 for every n. Indeed the shifted initial-state distribution has density 2·1_{w_{-n}=1}, and hence TV distance 1/2 from ρ. Pushforward cannot increase TV, giving the upper bound for the path laws; the path event A_n={x:(x₀)_{−n}=1} attains difference 1/2, giving the lower bound. A_n depends on n, whereas the setwise assertion fixes A before taking n→∞.

Consequently Problem 3.1 has a negative answer under precisely the source's stated assumptions, independently of any uninspected 2026 manuscript. This example alone does NOT characterize the convergence and therefore does NOT solve Problem 3.2. No literature-priority claim is made.

## A genuine single-coupling property in this example

Construct Z∼η and Z′∼ρ on one probability space as follows. All coordinates other than zero are identical fair independent bits in Z and Z′. Set Z₀=1 and choose Z′₀ as an independent fair bit. Let X=Φ(Z), X′=Φ(Z′). This preserves both whole-process laws, and the second process is stationary. Under this ONE coupling, for EVERY A∈Σ,

P(1_A(θ^nX) ≠ 1_A(θ^nX′)) → 0.                 (SC)

For proof, again pull A back to B⊂E and approximate B by a finite-coordinate C. The variables T^nZ and T^nZ′ differ only at coordinate −n. For large n their indicators of C coincide exactly. The mismatch probability for B is at most P(T^nZ∈B△C)+P(T^nZ′∈B△C), bounded by 2ρ(B△C)+ρ(B△C)<3ε. The same coupling works for all B; only the proof's approximation and threshold depend on B. Almost-sure eventual equality of indicators is NOT asserted for every B.

This proves that (SC) can hold even when total variation convergence and distributional exact coupling fail: our example satisfies (SC) but fails TV convergence. No reverse implication is asserted here. Plainly (SC) is sufficient for setwise convergence whenever X′ is stationary, since the absolute difference of the event probabilities is bounded by the mismatch probability.

## Necessity question tested in the subsequent attempt

This attempt alone does not establish that full-path setwise convergence always permits a single whole-process coupling satisfying (SC). Attempt 2 subsequently disproves that necessity. The distinction is substantive:

- A separate maximal coupling for each n and each finite measurable partition supplies neither a single original X nor an orbit θ^nX′ of one stationary X′.
- Even separately recoupling the entire shifted laws at every n does not preserve their deterministic consistency as successive shifts.
- A countable generating algebra cannot simply replace all measurable tests under arbitrary marginals without a common approximation/control argument. The Bernoulli proof works because every shifted first marginal is bounded above by 2ν; that domination has not been proved in general.
- The source allows general measurable state spaces. Conditional-distribution or compactness constructions require explicit additional justification if they assume standard Borel structure.

Thus (SC) is a substantive candidate answer form, validated on this counterexample but disproved as a necessary condition in Attempt 2. The completed contribution here is an explicit full-path negative answer to the antecedent and a nontrivial single-coupling property. It is not a substitute for the characterization requested by Problem 3.2. The final named-problem disposition remains partial/unresolved for the reasons in SCOPE.md.
