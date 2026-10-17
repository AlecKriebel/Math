# Conditional admissibility of additive inverse comparisons

16 October 2026. Let B_g be the exact inverse class characterized by the full-boundary transported Piola identities in `TRANSPORT_PIOLA_CHARACTERIZATION.md`.

**Lemma.** If v∈B_g, ζ∈C_c∞(D;R³), and t∈R satisfies

∫_D V(Dv+tDζ)<∞,

then v_t=v+tζ also belongs to B_g. Consequently, for an inverse of a primal global minimizer,

∫_D V(Dv)≤∫_D V(Dv+tDζ)

for every such t. The finite-energy condition includes det(Dv+tDζ)>0 a.e. For all other t the inequality holds trivially with an infinite right side, so this is genuine minimality against every compact smooth additive comparison.

This does not assert the existence of a nonzero admissible t, an admissible interval about zero, or an integrable ordinary dual Piola stress. Those facts remain necessary for unrestricted additive Euler–Lagrange differentiation.

## Proof

### 1. Weak Piola holds for v and is preserved by a smooth addition

The exact inverse v is bounded, with Dv∈L^{9/5} and cof Dv∈L^{9/4}. In its transported Piola identity take a target vector field that is constant on a neighborhood of Ωbar, and take a compactly supported scalar test in D. This gives

Div(cof Dv)=0

in distributions, with divergence taken row by row.

For 3×3 matrices the cofactor is quadratic. Therefore

cof(Dv+tDζ)=cof Dv+t M(Dv,Dζ)+t² cof Dζ,

where M is the symmetric bilinear polarization of the cofactor. The mixed tensor has distributional divergence zero. Indeed, approximate v locally by smooth v_m strongly in W^{1,9/5}. For smooth v_m and ζ, expand the usual Piola identity for v_m+sζ in powers of s. Its linear coefficient gives Div M(Dv_m,Dζ)=0. Since Dζ is smooth and bounded, M(Dv_m,Dζ)→M(Dv,Dζ) strongly in L^{9/5} on compact sets. Passing to distributions proves the assertion. The last tensor cof Dζ also satisfies Piola. Hence Div(cof Dv_t)=0.

### 2. The conjugate exponents justify the transported chain rule

The assumed finite V gives cof Dv_t∈L^{9/4} and K_t=det Dv_t∈L³. The exponents 9/5 and 9/4 are conjugate. Thus the weak Piola equation can be tested against each component of

ψ·φ(v_t),

where ψ∈C_c∞(D) and φ∈C_c∞(R³;R³), by density in W_0^{1,9/5}. The Sobolev chain rule and the identity (cof H)Hᵀ=(det H)I give

∫_D [ψ K_t div φ(v_t)+φ(v_t)·(cof Dv_t)Dψ]=0.

These are the interior transported Piola identities. The same argument applies to v.

### 3. The full boundary flux is unchanged

Because ζ has compact support in D, v_t=v and Dv_t=Dv a.e. on a neighborhood of ∂D. For a fixed target test φ, the flux difference

B=(cof Dv_t)ᵀφ(v_t)−(cof Dv)ᵀφ(v)

is supported in a compact subset of D and belongs to L^{9/4}. The interior identities give

div B=K_t divφ(v_t)−K divφ(v)

in distributions. Multiply by any ψ smooth near Dbar and integrate. A compact cutoff equal to one on the support of B and its divergence justifies the same test, so the integral of div(ψB) is zero. Consequently the difference of the two full transported Piola expressions is zero. The expression for v already has the prescribed boundary term, so v_t has that same boundary term.

It follows that v_t satisfies the reduced intrinsic characterization. Therefore v_t∈B_g, as claimed. No direct injectivity theorem at exponent 9/5 and no assumed weak derivative of its primal inverse were used.

## Extension to compactly supported W^{1,9/4} differences

The lemma remains true for ζ∈W^{1,9/4}(D;R³) with compact essential support. In particular, it applies to every compactly supported Lipschitz difference. The finite-energy condition on v+ζ is unchanged.

To check this, approximate v strongly in W^{1,9/5} locally and ζ strongly in W^{1,9/4}, using compactly supported smooth approximations for ζ. The mixed cofactor terms converge strongly in L¹ because 9/5 and 9/4 are conjugate. The pure cof Dζ terms converge strongly in L^{9/8}. Thus their distributional Piola identities pass to the limit. If v+ζ has finite V, its cofactor belongs to L^{9/4}, so the transported chain-rule test is again justified exactly as above.

Boundedness of ζ is unnecessary: the target test φ and its derivative are bounded. Compact essential support makes ζ and Dζ vanish in a collar, so the full-boundary flux argument is unchanged. The reduced class theorem itself recovers the bounded range of v+ζ and its actual primal inverse.

## Scope

Therefore an inverse minimizer is a local minimizer against every compactly supported W^{1,9/4} additive difference: finite-energy comparisons belong to the exact class, and infinite-energy comparisons satisfy the inequality trivially.

This does not yet permit every W^{1,9/5} difference. In particular, the ordinary cutoff expression ζ=η(v−an affine map) is only known to be W^{1,9/5}; its membership in W^{1,9/4} cannot be assumed. The argument also does not identify an arbitrary finite-V map with the correct ordinary boundary trace as a genuine inverse.

All hypotheses and the compact W^{1,9/4} extension were independently checked in the pass 3 audit.
