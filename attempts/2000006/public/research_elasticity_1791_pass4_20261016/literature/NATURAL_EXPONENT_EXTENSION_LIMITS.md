# Limits of arbitrary natural-exponent inverse additions

16 October 2026. The structured graph-transform theorem in the companion report is proved. The broader implication

v∈B_g, ζ∈W^{1,9/5} with compact support, ∫V(Dv+Dζ)<∞ ⇒ v+ζ∈B_g

has not been proved or disproved in this pass. The calculations below identify actual failures of proposed shortcuts; they are not counterexamples to that implication or to E-6322.

## 1. The generic polarization argument lacks an integrable mixed product

In dimension three,

cof(Dv+Dζ)=cof Dv+M(Dv,Dζ)+cof Dζ,

with M bilinear. If both gradients are only L^{9/5}, their product is controlled in L^{9/10}, which is below L¹. Strong W^{1,9/5} approximation therefore does not justify passing the mixed term to distributions by Hölder.

Finite V of the two endpoints gives their individual pointwise cofactors in L^{9/4}, but does not furnish a pointwise bound for the mixed terms. Here is an exact matrix test. For L≥1 set

H₁=diag(L,L^(−1/5),L^(−1/5)),
H₂=diag(L^(−1/5),L,L^(−1/5)).

Both determinants equal L^(3/5), both cofactor norms are comparable to L^(4/5), and V(H_i) is comparable to L^(9/5). Yet

[M(H₁,H₂)]₃₃=L²+L^(−2/5).

Consequently |M(H₁,H₂)|/(1+V(H₁)+V(H₂)) tends to infinity like L^(1/5). Choosing a scalar measurable L with L^{9/5} integrable but L² nonintegrable gives endpoint-energy-integrable matrix fields with a nonintegrable mixed polarization. No claim that these fields are compatible gradients is made. The test rules out this direct algebraic domination, not a compensated-compactness theorem using differential constraints.

## 2. High integrability of pointwise cofactors does not identify distributional minors by itself

Consider the cylinder C=B²_1×(−1,1) and the bounded map

q(x₁,x₂,x₃)=(x₁/r,x₂/r,0),  r=sqrt(x₁²+x₂²)>0,

with arbitrary values on the axis. It belongs to W^{1,p}(C) for every p<2, including p=9/5. Its derivative has rank one a.e., so every pointwise cofactor is zero, hence belongs to every L^q space.

Nevertheless its distributional (3,3) cofactor is not zero. With the standard distributional definition it is

∂₁(q₁∂₂q₂)−∂₂(q₁∂₁q₂)=π δ_{(0,0)}⊗Lebesgue_{x₃}.

For example the flux around a circle is ∮q₁ dq₂=∫₀^{2π}cos²θ dθ=π. The smooth regularizations

q_ε=(x₁/sqrt(r²+ε²),x₂/sqrt(r²+ε²),0)

converge strongly to q in W^{1,p}, p<2, while

[cof Dq_ε]₃₃=ε²/(r²+ε²)²

converges to the displayed line measure, rather than to the zero pointwise cofactor. Its L¹ mass on each cross-section tends to π. Thus strong low-exponent smoothing plus integrability of the limiting pointwise cofactors does not establish strong minor convergence or identification of the distributional minor.

This example has det Dq=0 and infinite V. It is deliberately not offered as a finite-V map, an inverse competitor, or a failure of the desired general extension. Also its distributional cofactor defect has zero row divergence in the interior, so it is not itself a counterexample to the weak Piola identity. Its sole role is to invalidate the stronger minor-identification shortcut.

## 3. What the checked primary calculus theorem licenses

Hajłasz–Schikorra–Tyson, *Homotopy groups of spheres and Lipschitz homotopy groups of Heisenberg groups*, arXiv:1301.4978v3, 28 November 2013, Lemma 4.1(3), pp.11–12, states the weak product rule for the two differentiated factors under p≥2. Part (2) uses p≥ℓ+1 for the pullback/exterior-derivative identity on ℓ-forms. The proof passes smooth approximations through the corresponding products. The full statement and proof were inspected, rather than reading the threshold from a secondary discussion.

https://arxiv.org/pdf/1301.4978v3

This theorem does not supply the generic p=9/5 step. Its thresholds are sufficient hypotheses; this inspection does not claim they exclude every possible theorem using the additional determinant/cofactor structure of V.

A valid conditional improvement is available: if v also belongs to W^{1,2}, then compactly supported W^{1,2} differences with finite resulting V are admissible. Both mixed gradient products are then L¹, the usual weak Piola passage works, and the new finite V provides the L^{9/4} cofactor pairing needed for transported identities. This additional W^{1,2} regularity is not part of the unconditional baseline.

## 4. Exact remaining criterion and why energy-bounded approximation would suffice

For an arbitrary finite-V candidate u agreeing with v in a collar, it suffices to prove weak Div(cof Du)=0. Conjugate pairing with Du∈L^{9/5} and cof Du∈L^{9/4} then gives its interior transported Piola identities; subtracting v's flux extends them to the full boundary, exactly as in pass 3. The reduced characterization yields u∈B_g.

An alternative sufficient condition is an approximation u_m∈B_g with u_m→u in L¹ and liminf∫V(Du_m)<∞. The established energy-bounded closure then gives u∈B_g. Merely smoothing u in W^{1,9/5} supplies neither these energy bounds nor the required minor convergence.

No primary theorem verifying either criterion for every arbitrary finite-V natural-exponent addition was found in this targeted check. No finite-V counterexample to it was verified. For smooth graph transformations of the actual inverse, the companion theorem bypasses these criteria by working with the W^{1,6} primal map, and covers the standard cutoff shape once its determinant and energy are controlled.
