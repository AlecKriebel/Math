# Exact two-point consequence of the audited certificate

For the Fourier convention exp(-2πi⟨x,ξ⟩), define L₂ as the infimum of g(0) over real Schwartz functions g on R² satisfying ĝ(0)=1, ĝ≥0 everywhere, and g(x)≤0 whenever |x|≥1.

Let Λ=Z(1,0)+Z(1/2,√3/2). Its determinant is b=√3/2. For the lattice point corresponding to integers j,k, the squared norm is j²+jk+k², a strictly positive integer when (j,k)≠(0,0). Hence every nonzero lattice point has norm at least one.

For any admissible g, Schwartz regularity makes both lattice sums absolutely convergent. Its sign constraint gives
Σλ∈Λ g(λ)≤g(0).
Poisson summation, with Λ*= {ξ:⟨ξ,Λ⟩⊂Z}, gives
Σλ∈Λ g(λ)=b⁻¹Σω∈Λ* ĝ(ω)≥b⁻¹ ĝ(0)=2/√3.
The inequality includes all sign-boundary points at norm exactly one and the unique origin term separately. No Fourier sign boundary is omitted, because the Fourier constraint holds everywhere. It follows that every admissible g has g(0)≥2/√3, so L₂≥2/√3.

OpenAI family 090 Theorem 1.1, whose construction is reconstructed in CERTIFICATE_AUDIT.md and whose finite gates are covered by the recorded validated computations, supplies an admissible f with f(0)=2/√3. Once its fresh adversarial dependency review is accepted, this yields L₂≤2/√3 and therefore L₂=2/√3. It also witnesses attainment of the two-point infimum. This proof makes no claim of attainment for the triangle infimum.

The quantity 2/√3 is the number of lattice points per unit area. A disk of radius 1/2 has area π/4, so the associated covered-area density is π/(2√3). Substituting the area density as the objective would be a normalization error.

This is the standard Poisson lower-bound deduction from an explicitly credited imported upper certificate. It is not claimed as an independently discovered breakthrough. The triangle product-program theorem remains a separate dependency; this file does not establish P₂=4/3 or solve the all-dimensional problem in PR #487.
