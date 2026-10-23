# Independent geometry and measure audit of the centroid counterexample

## Conclusion and scope

The construction underlying Theorem 3 of Myroshnychenko, Tatarko and Yaskin (MTY) is valid in every dimension n ≥ 5. It gives a compact convex body with nonempty interior, ordinary volume centroid exactly zero, and exactly one unoriented hyperplane section with centroid zero. Consequently it disproves the universal assertion that every convex body in every dimension n ≥ 3 has at least n+1 such hyperplanes.

This is a verification of the authors' prior result, not a new counterexample or novelty claim. This audit reconstructs the measure, convexity, regularity, parameter selection, and counting arguments directly. Two minor statements in the inspected author manuscript need correction; both repairs are supplied below and leave the construction intact.

Source: Sergii Myroshnychenko, Kateryna Tatarko and Vladyslav Yaskin, *Answers to questions of Grünbaum and Loewner*, [arXiv:2404.15188v2](https://arxiv.org/abs/2404.15188v2), revised November 7, 2024, especially pp. 3–8. Publication: *Advances in Mathematics* 461 (2025), 110081, [DOI 10.1016/j.aim.2024.110081](https://doi.org/10.1016/j.aim.2024.110081). The inspected PDF is the arXiv author manuscript, not publisher PDF bytes; no byte equivalence is claimed.

## 1 Measure and notation

Write S = S^(n−1), t(u) = u_n, and dσ for ordinary unnormalized surface measure. For a positive smooth radial function r, let

    K_r = {s u : u ∈ S, 0 ≤ s ≤ r(u)}.

Ordinary Euclidean polar coordinates give

    vol_n(K_r) = (1/n) ∫_S r(u)^n dσ(u),
    ∫_{K_r} x dx = (1/(n+1)) ∫_S u r(u)^(n+1) dσ(u).

For a unit normal ξ, polar coordinates in the Euclidean space ξ^⊥, of dimension n−1, give

    ∫_{K_r ∩ ξ^⊥} x dvol_(n−1)(x)
      = (1/n) ∫_{S ∩ ξ^⊥} u r(u)^n dσ_(n−2)(u).

Thus the powers n+1 and n, and the denominators n+1 and n, concern genuinely different dimensional measures. None is a probability-weighted or ambient n-dimensional measure on a section. A positive lower bound on r puts a Euclidean ball around zero inside K_r, so all these central sections have strictly positive (n−1)-volume.

## 2 An explicit convex seed in every dimension at least five

Set a = 1/100 and, on S, define

    β = a^(−2) − 1,
    q(t) = (1 + β t²)^(−1/2),
    r_M(u) = 1 − 2 a^(n−2) q(t(u)).

This is smooth, positive, even, and invariant under rotations fixing the last coordinate axis. Since 0 < q ≤ 1,

    r_M ≥ 1 − 2 a^(n−2) ≥ 0.999998  for n ≥ 5.

The elementary derivative bounds

    |q′| ≤ √β < a^(−1),
    |q″| ≤ 4β < 4a^(−2)

follow by setting z = √β t in the explicit derivatives. On the unit sphere, |∇t| ≤ 1 and ∇²t = −t times the spherical metric. Therefore

    ||∇²_S r_M|| ≤ 8 a^(n−4) + 2 a^(n−3) ≤ 0.0802.

In particular, ||∇²_S r_M|| < min r_M. These are inequalities proved from exact expressions, not sampled curvature estimates.

Here is a direct global convexity check. Put s = 1/r_M and extend the gauge by F(x) = |x|s(x/|x|), with F(0)=0. At a unit vector, its Hessian has zero radial and mixed terms; on tangent vectors it is

    ∇²_S s + s I
      = r_M^(−3) [r_M² I + 2 dr_M ⊗ dr_M − r_M ∇²_S r_M].

The bracket is positive definite by the displayed bound. Consequently F is convex along every line not passing through zero. On a line through zero its left and right slopes are −F(−v) and F(v); positivity of F makes the required slope inequality automatic. Hence F is globally convex and {F≤1}=M is a convex body. The same positive bracket gives positive definite second fundamental form, so M is smooth and strictly convex.

This argument establishes global convexity rather than merely asserting that a locally curved radial graph bounds a convex body.

### The dimension threshold is real for this seed

At t=0 the meridional derivative vanishes, and the relevant curvature sign is the sign of

    r_M(0) − r_M″(0) = 1 − 2 a^(n−4).

For n=4 this equals −1, independently of a. For n=3 it is negative for 0<a<1. Thus this particular seed does not establish the lower-dimensional claims by simply taking a smaller parameter. The n≥5 conclusion is exactly the sufficient range needed for the universal target.

## 3 The transform identities and a repaired preliminary statement

Use the Fourier convention with kernel exp(−i x·y). If f is a smooth even function on S, let Qf denote the restriction to S of the Fourier transform of its homogeneous degree −1 extension. Standard homogeneous Fourier transformation gives a smooth even function, with the transformed extension having degree 1−n. Fourier inversion and the equatorial formula give

    R Q f = c f,       Q R f = c f,       c = (2π)^n/π,

where

    R h(ξ) = ∫_{S ∩ ξ^⊥} h(u) dσ_(n−2)(u).

The equatorial formula is the Fourier transform of the degree 1−n extension, namely πRh. Its factor π can also be obtained by integrating the polar radial variable: the even part of the one-dimensional half-ray Fourier integral is π times the Dirac delta, which restricts angular integration to the equator.

The Radon transform R is self-adjoint: integrating a function of two orthogonal unit vectors in either order gives the same invariant incidence measure, with the same fiber measure |S^(n−2)|. Taking h=Qf and k=Qg in this identity yields

    ∫_S (Qf) g dσ = ∫_S f (Qg) dσ.                 (A)

This establishes exactly the same-degree spherical Fourier identity needed below, independently of the misstated preliminary identity in the manuscript. All functions used here are smooth and even; Fourier inversion is applied to their tempered homogeneous extensions, whose degrees lie strictly between −n and 0. There is no discarded singular term at the origin in these identities.

### Correction to the inspected equation (5)

On p.3, MTY v2 states the displayed identity ∫ f̂g = ∫ fĝ while assigning f and g the complementary homogeneities −k and −n+k. That statement is false as written. For example, in R^5 take f(x)=|x|^(−1) and g(x)=|x|^(−4). Their Fourier transforms restrict to the distinct constants 16π² and 2π³, so the two spherical integrals differ.

The applications in the main proof involve degree −1 extensions on both sides, and (A) proves the required identity in that case. Alternatively, the usual complementary-degree Parseval identity has both Fourier transforms on one side and the factor (2π)^n on the other. The present audit uses (A), so this source-level defect does not create a gap in the counterexample.

## 4 The two endpoint functions have genuinely opposite moment signs

The Gaussian integral formula for the Fourier transform of |x|^(−1), followed by an invertible linear change of variables, gives

    c_n = 2^(n−1) π^((n−1)/2) Γ((n−1)/2) > 0,

    Qr_M(u) = c_n [1 − 2a^(n−1)(|u′|²+a²u_n²)^((1−n)/2)].

At u=±e_n this is −c_n. Continuity therefore provides two open polar caps on which Qr_M<0. Choose a smooth even axial function G that vanishes at the two poles and off these caps and is positive in the punctured caps. Such a function is elementary: if the caps are {0≤1−t²<δ}, use

    G(u) = (1−t²) exp(−1/[δ−(1−t²)])

inside the caps and zero outside. Smoothness at the cap boundary follows from flat exponential decay; at the poles it is a smooth function of 1−t². Its positivity set has positive surface measure. Hence

    ∫_S (Qr_M)G dσ < 0.                            (B)

Define another even axial function

    H(u) = 1 − (4|u′|²+u_n²)^(−1/2).

It vanishes exactly at ±e_n and is strictly positive everywhere else. The same elementary transform calculation yields

    QH(u) = c_n [1 − (|u′|²+4u_n²)^((1−n)/2)].

This is nonnegative everywhere and strictly positive whenever u_n≠0. Since r_M is positive,

    ∫_S (Qr_M)H dσ = ∫_S r_M QH dσ > 0.           (C)

The strictness in (B) and (C) comes from open sets of positive measure; neither is an endpoint sign inferred from numerical approximation.

For 0≤λ≤1 let g_λ=(1−λ)G+λH. It is smooth, even and axial. For every λ>0 it is strictly positive at every point of S except the two poles, where it vanishes.

### Correction to a positivity sentence on p.5

The manuscript's comparison between |x|^(−1) and (|x′|²+x_n²/a²)^(−1/2) is non-strict when x_n=0. The positivity needed for the seed follows from the non-strict comparison and 2a^(n−2)<1, as established in Section 2. No strict comparison at the equator is needed.

## 5 Equatorial division is smooth for the actual symmetric family

Let q_λ=Qg_λ. Rotational covariance of Fourier transformation preserves axial invariance. Thus q_λ is constant on the equator. By the transform identity and g_λ(e_n)=0,

    |S^(n−2)| q_λ|_(equator) = Rq_λ(e_n) = c g_λ(e_n) = 0.

Near the equator q_λ can be expressed as a smooth one-variable function b_λ(t). Axial invariance combined with antipodal evenness implies b_λ(−t)=b_λ(t). Therefore b_λ(0)=b′_λ(0)=0 and b_λ(t)=t² d_λ(t) with d_λ smooth and even. It follows that

    φ_λ(u) = q_λ(u)/u_n  when u_n≠0,
    φ_λ(u) = 0          when u_n=0

is smooth, odd and axial on the whole sphere. Away from the equator the quotient is plainly smooth, including at the poles. The dependence on λ is affine, so all C^k norms are uniformly bounded for λ∈[0,1].

The axial assumption is important here: antipodal evenness alone, plus vanishing on the equator, would not justify defining this quotient to be zero there. The actual construction supplies the stronger reflection symmetry needed for the second-order vanishing.

## 6 Uniform convexity and exact section signs

Define

    r_(λ,ε) = (r_M^n + εφ_λ)^(1/n).

The positive minimum of r_M and the uniform C² bounds on φ_λ imply that, for all sufficiently small |ε|, this is positive and uniformly C²-close to r_M for every λ∈[0,1]. The gauge-Hessian criterion in Section 2 is open in the C² topology. Compactness of S×[0,1] therefore gives one positive ε bound under which every K_(λ,ε) is a smooth strictly convex body with nonempty interior. No convexity assertion depends on the later, unknown λ chosen by the centering argument.

For a unit normal ξ, the last coordinate of the section's unnormalized first moment is exactly

    ∫_{K_(λ,ε) ∩ ξ^⊥} x_n dvol_(n−1)(x)
      = (1/n) ∫_{S ∩ ξ^⊥} u_n [r_M(u)^n+εφ_λ(u)] dσ
      = (ε/n) Rq_λ(ξ)
      = ε(2π)^n/(π n) g_λ(ξ).

The seed term vanishes by the oddness of u_n r_M^n on every central equator. If ε>0 and λ>0, the final expression is strictly positive for every ξ≠±e_n. This is an exact identity, not a first-order estimate. Consequently it remains valid for normals arbitrarily close to ±e_n; no uniform positive lower bound away from zero is being presumed.

For ξ=±e_n, the hyperplane is x_n=0. On its unit sphere φ_λ=0 and r_M is the constant 1−2a^(n−2). Thus this section is an origin-centered Euclidean (n−1)-ball. Its entire centroid vector is zero, not merely its last coordinate.

## 7 Exact body centering without a transformed remainder

Axial symmetry forces the first n−1 coordinates of the body's first moment to vanish. Define the remaining coordinate

    J(λ,ε) = (1/(n+1)) ∫_S u_n
                   [r_M(u)^n+εφ_λ(u)]^((n+1)/n) dσ(u).

For ε=0 this is zero by symmetry. The fundamental theorem of calculus gives the exact integral expression

    J(λ,ε)/ε
      = (1/n) ∫_0^1 ∫_S u_n φ_λ(u)
                   [r_M(u)^n+sεφ_λ(u)]^(1/n) dσ(u) ds.

The right side extends continuously, indeed smoothly, to ε=0, uniformly in λ on its compact interval. At ε=0 it is

    L(λ,0) = (1/n) ∫_S r_M q_λ dσ
           = (1/n) ∫_S (Qr_M)g_λ dσ.

By (B) and (C), L(0,0)<0<L(1,0). These strict endpoint signs persist for all sufficiently small fixed positive ε. Choose one such ε also inside the uniform convexity range. Continuity in λ and the intermediate value theorem then give λ_ε∈(0,1) with J(λ_ε,ε)=0 exactly.

The resulting body has first-moment vector exactly zero and positive volume, hence ordinary centroid exactly zero. It has not been translated after constructing its central sections. Its section signs remain strict because λ_ε>0 and ε>0. The argument does not require uniqueness of the centering parameter or a numerical root computation.

## 8 Hyperplane counting and target matching

Every affine hyperplane whose section centroid is zero must itself contain zero: applying its affine defining functional to the section mean proves this immediately. Thus it is enough to count central hyperplanes ξ^⊥.

The exceptional normals +e_n and −e_n specify the same geometric hyperplane. Every other normal gives a section with strictly positive last centroid coordinate, so no other section can have centroid zero. The exceptional section does have full centroid zero, as checked in Section 6. There is therefore exactly one distinct unoriented barycentric hyperplane.

All target hypotheses are satisfied: finite-dimensional Euclidean body, compactness, convexity, nonempty interior, ordinary volume centroid, induced section measure, and geometric rather than oriented hyperplane count. A counterexample already in dimension five refutes the assertion universally quantified over n≥3. No assertion about a specially chosen interior point, maximum Tukey-depth point, volume bisection, or lower-dimensional section is substituted for that target.

## Audit disposition

Accepted as a credited prior negative resolution of the universal centroid question. The geometric proof is stronger in regularity than the target requires. The manuscript's preliminary Parseval formulation and one strict comparison require the explicit repairs above; neither defeats the result. This audit does not assert publisher/manuscript byte identity or claim to resolve a different interior-point question.
