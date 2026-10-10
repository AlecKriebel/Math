# Clarifying supplement: explicit gluing constants and CK jets

This separately authored supplement leaves the original freeze unchanged. It supplies detail to an accepted argument, rather than repairs a false theorem. Assume n ≥ 4, d > 0, Δ = div grad, and a_n = 4(n−1)/(n−2).

## Fixed choices before ε

Choose a fixed normal chart B_(r_0) on which the germ exists and F_d(g) ≥ 0. Shrink r_0 to lie in a round normal chart and ensure all metric eigenvalues lie in [1/2,2]. Choose smooth 0 ≤ χ ≤ 1 with χ = 1 on [0,2] and χ = 0 on [3,∞). Choose smooth φ ≥ 0 supported in [1,4], positive on (1,4), and φ ≥ 1 on [2,3]. Choose smooth 0 ≤ η ≤ 1 equal to 1 for r ≤ r_0/2 and equal to 0 on a neighborhood of r ≥ r_0.

For all sufficiently small ε, normal-coordinate cutoff estimates give constants A ≥ 0 and B ≥ 0, independent of ε, with

Δ_(g_ε) r ≥ (n−1)/r − Ar,

F_d(g_ε) ≥ −B on [2ε,3ε].

One direct derivation of the first bound uses radial gauge: ∇r = ∂_r, and

Δr = (n−1)/r + (1/2) tr(g_ε^−1 ∂_r g_ε).

The Cartesian metric derivative is O(r), uniformly in ε. Thus the trace correction is O(r), including on the cutoff shell. The curvature bound follows from uniform control through two metric derivatives and the inverse-metric bound. Fix M > B/a_n. Every subsequent smallness condition is on ε; there is no circular choice making M or the cutoffs depend on ε.

## Quantitative bound on the barrier

Set L = exp(A r_0²/2), Φ = sup φ, and C_I = Φ·4^n/n. For ε ≤ r ≤ r_0,

I_ε(r) = ∫_ε^r s^(n−1) exp(−As²/2) φ(s/ε) ds

obeys 0 ≤ I_ε(r) ≤ C_I ε^n. Also I_ε(r) ≤ Φ r^n/n. With v′ = −M r^(1−n) exp(Ar²/2) I_ε(r), these give

|v′(r)| ≤ MLΦ r/n for ε ≤ r ≤ 4ε,

|v′(r)| ≤ MLC_I ε^n r^(1−n) for 4ε ≤ r ≤ r_0.

After integrating, one may take

C_0 = L [15Φ/(2n) + C_I·4^(2−n)/(n−2)]

to obtain 0 ≤ 1−v(r) ≤ M C_0 ε². Choose ε with 4ε < r_0/2 and M C_0 ε² ≤ 1/2. This gives 1/2 ≤ v ≤ 1.

Since v′ ≤ 0 and Δr ≥ α := (n−1)/r−Ar,

Δv = v″ + (Δr)v′ ≤ v″ + αv′ = −Mφ(r/ε).

Where F_d(g_ε) ≥ 0, the conformal numerator is nonnegative. In the cutoff shell, it is at least a_nM−B because v ≤ 1. This verifies the whole inner region, not only a boundary sphere.

## The fixed outer annulus

On A_0 = {r_0/2 ≤ r ≤ r_0}, I_ε is constant, and r is bounded away from 0. Thus there is C_1 independent of ε with |v′| + |v″| ≤ C_1 M ε^n. The radial Laplacian of the round metric has bounded coefficients there. Product differentiation of v_tilde = 1 + η(v−1) therefore yields

‖v_tilde−1‖_(C²(A_0)) ≤ C_2 M ε²

for 0 < ε ≤ 1; C_2 depends only on the fixed data. Consequently, for another fixed C_3,

−a_n Δ_b v_tilde + n(n−1)v_tilde ≥ n(n−1) − C_3 M ε².

Take ε still smaller so that C_3 M ε² ≤ n(n−1)/2. The numerator is then strictly positive on A_0. This permits Δ_b v_tilde to have either sign in the outer transition. The construction does not require a globally superharmonic nonconstant conformal factor.

The inner constant factor and flat cutoffs ensure smoothness at the center and both seams. Outside the chart the metric is round. Smooth positive definiteness on S^n gives compactness, completeness, and the standard short-time Ricci-flow existence setting.

## The CK jet in coordinate detail

Write the analytic equation as h^{ij}v_ij + b^jv_j = f v, where f = F_d(h)/a_n. At 0, h^{ij} = δ_ij, ∂h^{ij} = 0, b^j = 0, f = 0, and ∂f = 0. Cauchy data v(x′,0) = 1 and v_n(x′,0) = 0 annihilate every tangential derivative and every derivative with exactly one normal index on the initial hypersurface.

The undifferentiated equation at 0 yields v_nn = 0. Differentiating in x_k gives

h^{ij}v_ijk + (∂_k h^{ij})v_ij + b^jv_jk + (∂_k b^j)v_j = f_k v + f v_k.

All lower-jet terms vanish. Thus Σ_i v_iik = 0. Each i < n term is zero by the Cauchy data, including when k = n. Therefore v_nnk = 0 for every k. This proves the full 3-jet claim without specifying fourth derivatives or imposing a false condition ΔR = 0.

Finally, ∇R = 0 kills the norm-Hessian contribution to ΔF. The local equality F = 0 then kills only DF[ΔR], exactly the normal component needed for the PDE counterexample.
