# Supplementary audit of the all dimensional centroid construction

## Conclusion and source status

The geometric, measure-theoretic, and perturbative parts of the Wang–Xiong–Yang construction check out in every n≥3, including n=3 and n=4. The short transform and critical-point checks below also support the required analytic inputs. No substantive obstruction was found in this construction.

This is a supplementary audit of an existing submitted preprint: Shouda Wang, Ge Xiong and Kaiwen Yang, *A complete solution to the Grünbaum–Loewner centroid problems*, [arXiv:2606.19865v2](https://arxiv.org/abs/2606.19865v2), July 31, 2026. The proof inspected is Theorem 1.1 and its supporting lemmas in that version. Mathematical verification does not change its manuscript status; this audit does not label it a verified journal publication. The published MTY result in dimensions at least five already suffices for the universal question, independently of this supplement.

## 1 The twisted height function has the required exact moment

Let

    w(t)=(1−t²)^((n−1)/2),    W=∫_0^1 w(t)dt,
    s(t)=W^(−1)∫_0^t w(τ)dτ,    0≤t≤1.

Choose a smooth function a on [0,1], constant near 0, 1/2 and 1, with endpoint values 0, π and 2π, and with a(r+1/2)=a(r)+π. One explicit existence prescription is to choose a smooth increasing transition from 0 to π on [0,1/2], constant near both ends, then extend by this rule. The flat endpoint regions make the extension smooth at 1/2.

Define α(t)=a(s(|t|)). The absolute value causes no nonsmoothness at zero because a∘s is identically zero near zero. The possibly noninteger exponent in w causes no problem at ±1 because a∘s is constant on neighborhoods of those endpoints. Hence α is a smooth even function on the closed interval, with a smooth extension to a neighborhood. The exact change of variables gives

    ∫_(−1)^1 w(t)e^(iα(t))dt
      =2W∫_0^1 e^(ia(r))dr=0.

For u=(x₁,x₂,y,t)∈S^(n−1), where y has n−3 coordinates, rotate (x₁,x₂) through α(t), leaving y,t fixed. The resulting map Φ is a globally smooth diffeomorphism of the sphere; the inverse rotates by −α(t). It is odd because α is even. Thus

    f(u)=x₁ cosα(t)−x₂ sinα(t)

is smooth and odd and is a height function composed with a diffeomorphism. It has precisely two nondegenerate critical points. Since α is zero near t=0, these are in fact ±e₁ and the function is the ordinary height function on neighborhoods of them.

The latitude parametrization is

    u=(√(1−t²)v,t),    v∈S^(n−2),
    dσ_(n−1)(u)=(1−t²)^((n−3)/2)dσ_(n−2)(v)dt.

To verify the Jacobian, the fiber directions scale by √(1−t²), whereas the altitude tangent has length (1−t²)^(−1/2). Their product is the displayed power. The two endpoint points have surface measure zero.

For i<n, the product u_i f adds the factor 1−t², so its t weight is exactly w(t). Both the cosine and sine weighted integrals vanish by the complex identity above. For i=n, the integrand is odd in t, or alternatively has zero fiber mean. Therefore

    ∫_S u f(u)dσ(u)=0

exactly, in every component. This is a statement about the standard surface measure; no change-of-variables Jacobian for Φ is silently omitted, since no substitution by Φ is used in this moment calculation.

The construction works at n=3, where y is absent and the fibers are circles. It also works at n=4 despite the half-integer latitude exponent. The two rotating coordinates plus one altitude coordinate explain the genuine n≥3 threshold of this method.

## 2 The hemisphere transform preserves the needed smoothness and moment condition

Let

    Th(u)=∫_{θ·u≥0} h(θ)dσ(θ).

For odd h this is again odd. Rotational covariance makes each spherical-harmonic space invariant. For odd degree m its eigenvalue is

    λ_m=π^((n−2)/2)(−1)^((m−1)/2)
                     Γ(m/2)/Γ((m+n)/2).

A direct check uses the zonal Gegenbauer polynomial C_m^α, α=(n−2)/2: the eigenvalue is |S^(n−2)|/C_m^α(1) times its integral on [0,1] against (1−t²)^(α−1/2). Integrating the Gegenbauer differential equation gives that integral as C_m^α′(0)/[m(m+2α)]. The derivative at zero is nonzero for every odd m, and the gamma expression follows from the values of these polynomials at zero and one. As a normalization check, λ₁=|S^(n−2)|/(n−1), equal to the direct integral of a coordinate over a hemisphere.

Thus all odd eigenvalues are nonzero. Their reciprocals grow only polynomially, of order m^(n/2). Smooth functions have spherical-harmonic coefficients decaying faster than every power, so dividing their odd coefficients by λ_m again defines a smooth odd function. Consequently h=T^(−1)f exists and is smooth and odd. Since λ₁ is nonzero and the first harmonic component of f vanishes, the first harmonic component of h vanishes as well:

    ∫_S u h(u)dσ(u)=0.

The required C² boundedness of T does not rely on treating the indicator kernel as smooth. T commutes with rotations; differentiating this covariance along rotational vector fields moves derivatives onto h. Integration is then over a fixed hemisphere and is bounded by its area times the corresponding supremum norm of derivatives of h. Finitely many rotational vector fields span every tangent space; their derivatives through order two control an equivalent C² norm on the compact sphere. Hence ||Th||_(C²)≤C_n||h||_(C²).

## 3 The body is globally convex and exactly centered

For sufficiently small positive ε define

    ρ_ε(u)=(1+εh(u))^(1/(n+1)),
    K_ε={r u : u∈S, 0≤r≤ρ_ε(u)}.

Choose ε||h||_∞<1/2. This gives a smooth positive radius bounded above and away from zero. In particular K_ε is compact and contains a ball around zero. The ordinary chain rule on the compact sphere gives

    ρ_ε=1+εh/(n+1)+O_(C²)(ε²).

Global convexity follows directly from the homogeneous gauge F(x)=|x|/ρ_ε(x/|x|). Its tangent Hessian at a unit vector is ∇²_S(1/ρ_ε)+(1/ρ_ε)I, which converges uniformly to I. For small ε this is positive definite; radial and mixed terms are zero. Line convexity, including the slope condition across zero, proves that {F≤1}=K_ε is globally convex. Its smooth boundary has positive definite second fundamental form and is strictly convex. This supplies the global conclusion rather than relying only on a pointwise curvature assertion.

The volume centroid calculation is exact:

    ∫_{K_ε} x dx
      =(1/(n+1))∫_S uρ_ε(u)^(n+1)dσ(u)
      =(1/(n+1))∫_S u(1+εh(u))dσ(u)=0.

No asymptotic remainder, recentering translation, or replacement of volume by spherical measure is involved. The positive volume makes the centroid well-defined and equal to zero.

## 4 Hemisphere derivatives are precisely section moments

The half-space volume function through zero is

    A_ε(u)=vol_n(K_ε∩{x:x·u≥0})=(1/n)T(ρ_ε^n)(u).

For v tangent to S at u, differentiating the moving hemisphere boundary gives

    D_v A_ε(u)
      =(1/n)∫_{S∩u^⊥}(θ·v)ρ_ε(θ)^n dσ_(n−2)(θ)
      =∫_{K_ε∩u^⊥} x·v dvol_(n−1)(x).

The sign is positive for the hemisphere defined by x·u≥0. The boundary speed is θ·v because the spherical gradient of θ↦θ·u has unit length on the equator. The second equality is polar integration in u^⊥, with the correct exponent n and factor 1/n.

The section moment vector lies in u^⊥. Therefore vanishing of every tangential derivative is equivalent to vanishing of its full vector, and, since section volume is positive, equivalent to section centroid zero. This proves the critical-point correspondence for the smooth bodies actually constructed, without needing a regularity theorem for arbitrary nonsmooth convex bodies.

## 5 No additional critical directions can appear

The chain rule gives

    ρ_ε^n=1+[n/(n+1)]εh+O_(C²)(ε²).

Using the C² bound for T yields

    A_ε=|S^(n−1)|/(2n)+εf/(n+1)+O_(C²)(ε²).

Hence the function obtained by subtracting the first constant and multiplying by (n+1)/ε tends to f in C².

For this particular f, exact stability of the number of critical points can be proved without a general Morse-theory theorem. Take disjoint small coordinate balls around ±e₁. In one f is strictly concave and in the other strictly convex; the Hessian definiteness persists for sufficiently small C² perturbations. A positive gap between the center value and the boundary values ensures a maximum or minimum in the interior under small C⁰ perturbations. Strict Hessian definiteness gives uniqueness there. On the compact complement of these two balls, |df| has a strictly positive minimum, so a sufficiently small C¹ perturbation has no critical point there. Thus the rescaled A_ε, and therefore A_ε itself, has exactly two critical points.

Because

    A_ε(−u)=vol_n(K_ε)−A_ε(u),

these two critical points form one antipodal pair. Both normals define the same geometric hyperplane. The derivative identity shows that its section centroid is zero and that no other central section has centroid zero. An affine hyperplane with section centroid zero must itself contain zero, so this also excludes every noncentral affine hyperplane.

## Supplementary disposition

The all-dimensional geometric reconstruction is accepted for the specified arXiv v2 proof. The result remains attributed to Wang, Xiong and Yang and described as a submitted preprint rather than a verified journal publication. It gives smooth strictly convex examples in all n≥3. Its lower-dimensional conclusion is supplementary to the sufficient published MTY counterexample, and is not needed to negate the original universal assertion.
