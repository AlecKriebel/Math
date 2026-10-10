# A precise obstruction to zero extension

## Scope

Let Ω be a bounded open subset of R^n, n ≥ 2, and y ∈ ∂Ω. The question is whether B regularity at y implies B regularity for Ω ∩ B(y,r_m) along some sequence r_m ↓ 0. B regularity here concerns all finite PWB solutions with resolutive boundary data bounded near y. No connectedness, smoothness, Lipschitz boundary, cone condition, or ordinary Dirichlet regularity is assumed in the question.

We do not settle this implication. We prove that one natural step in a localization argument is false, even for a disk cut by a ball centered at the boundary point.

## Conditional transfer lemma

Put D = Ω ∩ B(y,r), Γ = ∂D ∩ ∂Ω, and Σ = ∂D ∩ Ω. These two sets partition ∂D. Suppose f ≥ 0 is resolutive on ∂D and bounded near y. Suppose also that:

1. f ≤ M on Σ for a finite constant M ≥ 0;
2. the function g on ∂Ω equal to f on Γ and zero on ∂Ω \ Γ is resolutive for Ω.

If y is B regular for Ω, then H_f^D is bounded near y.

Proof. The PWB restriction theorem says that H_g^Ω restricted to D is the PWB solution with data g on Γ and H_g^Ω on Σ. Call those data F. Positivity gives F ≥ 0 on Σ. On Γ we have F = f, and on Σ we have f ≤ M ≤ M + F. Thus f ≤ M + F on ∂D, and PWB monotonicity gives

0 ≤ H_f^D ≤ M + H_F^D = M + H_g^Ω.

For a sufficiently small neighborhood of y, the original and cut boundaries agree. Therefore g is bounded near y. B regularity of Ω makes the right-hand side bounded in a possibly smaller neighborhood. This proves the lemma.

The PWB restriction theorem is the standard restriction property used in Sadi's equation (6.2), [S, p. 116]. The argument works componentwise and does not require D to be connected. The extra assumptions above are not consequences of the problem's hypotheses.

## Proposition on nonpreservation of resolutivity

Let Ω = {z ∈ C : |z| < 1}, let y = 1, and set

D = {z : |z| < 1 and |z - 1| < 1}.

There is a nonnegative Borel function f on ∂D, vanishing near y and identically zero on Σ = ∂D ∩ Ω, such that f is resolutive for D but its zero extension g from Γ = ∂D ∩ ∂Ω to ∂Ω is not resolutive for Ω.

### Geometry and conformal map

The corners are a = 1/2 + i√3/2 and b = 1/2 - i√3/2. Both lie on the two boundary circles. The interior angle of the lens at each corner is 2π/3.

Define

T(z) = (z-a)/(z-b),
W(z) = exp(-2πi/3) T(z),
F(z) = W(z)^(3/2).

Choose the branch with 0 < arg W < 2π/3. To verify the domain of this branch, note that T maps both boundary circles through a and b to lines through 0. The original-circle arc has arg T = 4π/3; the artificial-circle arc has arg T = 2π/3. The interior point z_0 = 1/2 has T(z_0) = -1, with argument π. Consequently W maps the lens bijectively onto the sector 0 < arg w < 2π/3, and F maps it conformally onto the upper half-plane. Moreover F(z_0) = i. The point a corresponds to 0, b to infinity, and y to -1.

These facts follow directly from the Möbius map: its boundary rays enclose the sector containing W(z_0) = exp(iπ/3). No numerical approximation is used in this identification.

### Exact harmonic measure density

Write s = |z-a| and d = |z-b| for z on the original-circle arc Γ, away from its endpoints. Conformal invariance of harmonic measure and the Poisson density at i in the upper half-plane give, with respect to arclength,

q_D(z) = |F'(z)| / [π(1 + |F(z)|^2)].

We have |W(z)| = s/d and |W'(z)| = √3/d^2, so

q_D(z) = (3√3/(2π)) s^(1/2) / [d^(5/2)(1 + (s/d)^3)].

In particular, as z approaches a along Γ,

q_D(z) / s^(1/2) → 3^(1/4)/(2π),

because d → √3. This is a positive finite limit. Therefore q_D(z) is bounded above and below by positive constant multiples of s^(1/2) on a sufficiently short arc ending at a.

### Choice of boundary data

Let A be the part of Γ with 0 < |z-a| < 1/4. Define f(z) = |z-a|^(-5/4) on A and f(z) = 0 on the rest of ∂D, including the endpoints a and b. It is Borel measurable. Since |a-y| = 1 and |z-a| < 1/4 on A, the triangle inequality gives |z-y| > 3/4 there. Thus f vanishes near y and on the entire artificial open arc Σ.

On a circle, arclength distance to a and chord distance s are comparable near a; more explicitly s = 2 sin(t/2), where t is arclength from a. Hence local integrability is decided by the powers of s. For the cut domain,

f q_D ≍ s^(-5/4) s^(1/2) = s^(-3/4),

whose integral at 0 is finite. Away from a the data are bounded. Consequently f is integrable with respect to harmonic measure at z_0. The elementary Poisson/PWB representation on this Jordan domain then gives a finite harmonic solution, and f is resolutive. Finiteness at other interior poles follows either from the half-plane Poisson formula or Harnack comparison of harmonic measures. Values assigned at a and b do not matter because individual boundary points have zero harmonic measure here.

For Ω, harmonic measure at 0 is normalized arclength, q_Ω = 1/(2π). The zero extension g therefore has

∫_(∂Ω) g dω_Ω^0 = (1/(2π)) ∫_A s^(-5/4) dσ = +∞.

For every other interior pole the disk Poisson density is bounded below by a positive constant on this arc, so the same divergence holds. Thus g has no finite PWB solution and is not resolutive in the convention of Problem 3.33. This proves the proposition.

### Why this does not answer the original question

The disk is B regular at y. For example, split any resolutive data into a bounded part near y and an integrable part supported away from y; the disk Poisson kernels are uniformly bounded on the latter support when the interior point stays sufficiently close to y. Also the cut lens is a Lipschitz domain, a known locally B regular class [S, §6]. In this particular example H_f^D even tends to zero at y: F(z) tends to -1, while F(A) lies on a short interval ending at 0, away from -1. The Poisson kernels on F(A) therefore tend uniformly to zero and are bounded by a constant multiple of the kernel at i, which integrates f.

The example invalidates the assertion that resolutive cut-boundary data can simply be extended by zero to resolutive original-boundary data. It does not invalidate B regular localization itself. Importantly, the failure already occurs with zero artificial-boundary data, so the artificial spherical boundary is not the only gap in this proposed proof strategy.

## Remaining analytic step

A successful localization proof must control every resolutive f on the cut boundary, not merely restrictions of globally resolutive data. For connected Green domains, Sadi's harmonic-measure criterion [S, Corollary 3.3] gives one possible target: uniformly dominate harmonic measures near y on boundary pieces separated from y by a reference harmonic measure. The corresponding estimate for cut domains has not been derived here from the estimate for Ω. Artificial boundary pieces are new, and the proposition shows an integrability mismatch even on the inherited boundary. Cut domains may also have infinitely many components, so one cannot silently choose a single reference pole or use componentwise constants without a uniform argument.

## References

[S] A. Sadi, Some types of regularity for the Dirichlet problem, Nagoya Mathematical Journal 126 (1992), 103–124. https://doi.org/10.1017/S0027763000004013

Standard dependencies used explicitly: conformal invariance of harmonic measure; the half-plane Poisson kernel; the PWB/harmonic-measure integrability characterization on Jordan domains; the PWB restriction and comparison properties. The elementary lens construction and all its calculations are supplied above. No claim of novelty is made for this obstruction.
