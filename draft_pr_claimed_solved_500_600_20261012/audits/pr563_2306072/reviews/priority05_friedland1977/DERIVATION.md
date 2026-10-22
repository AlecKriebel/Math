# Exact bridges to Friedland–Schiffer 1977

This audit compares the full original paper *On coefficient regions of univalent functions*, Journal d'Analyse Mathématique31(1977),125–168, DOI10.1007/BF02813301. Its notation is reused below only when stated. All44pages were read in text and visual renderings; the report distinguishes scope reading from independent proof verification.

## 1. Recover the explicit global degree-four family

Let a=(a₁,a₂,a₃,a₄)ᵀ with a₁=1. From source(3.6),

    B₄=[[0,0,0,0],
        [2,1,0,0],
        [2,4,2,0],
        [2,4,6,3]],
    D₄=diag(1,−1,1,−1).

The Koebe Loewner control is κ=−1, so source(4.69) is

    dΛ/dt=−D₄ B₄ᵀ D₄ Λ,  Λ(0)=(0,0,0,1)ᵀ.

Putting x=exp(−t), the unique solution is

    Λ₁=4−20x+30x²−14x³,
    Λ₂=10x−24x²+14x³=2x(7x²−12x+5),
    Λ₃=6x²−6x³=6x²(1−x),
    Λ₄=x³.

The script checks each polynomial component against −xΛ′=−D₄B₄ᵀD₄Λ and the exact initial condition. It also checks Λ·(1,2,3,4)=4 for every x. Thus source Theorem4.2, started from the classical global inequality Re a₄≤4, yields Re(Λ·a)≤4 throughout all S. After removing the constant Λ₁a₁ and dividing by x>0, this is precisely source Corollary4.2(4.74):

    Re[x²a₄+6x(1−x)a₃+2(7x²−12x+5)a₂]
        ≤14x²−30x+20,  0<x≤1.

The x→0 endpoint follows continuously. For5/7<x<1 the a₂coefficient is negative; this is a nontrivial mixed coefficient inequality. The source displays an actual global maximizer: k(z)=z/(1−z)², whose normalized Loewner family stays k and whose omitted arc is the ray (−∞,−1/4]. That arc has constant polar argument and radial angle0.

This is not a claim that arbitrary necessary extremal trajectories are sufficient. The crucial transfer proof on pp141–145 establishes W(T)⁻¹𝒜ₙ⊆𝒜ₙ using the reversed Loewner flow, then pulls a competing vector back to the original global extremal problem. For an unconstrained support problem take m=1, where only a₁=1 is fixed. Given a∈𝒜ₙ, the inequality F(W⁻¹a)≤F(a*) becomes an inequality on all of𝒜ₙ for the transformed functional. The source proves this global preservation; the algebra script alone does not.

## 2. Exclude exact matching to that explicit family, including rotations

Write L=λ₂a₂+λ₃a₃+λ₄a₄. Under a normalized rotation g(z)=exp(−iα)f(exp(iα)z), coefficients are multiplied by exp(i(n−1)α). The functional coefficients therefore acquire powers q,q²,q³ with |q|=1, up to choosing the inverse rotation convention. The quotient

    I(L)=λ₃²/(λ₂λ₄)

is invariant under these rotations and under any common nonzero scalar, even a complex phase. Every real-coefficient member of Corollary4.2 has real I whenever λ₂λ₄≠0. For the candidate,

    λ₂=1,  λ₃=−3iε,  λ₄=iε,  ε=10⁻²⁴,
    I(L)=9iε≠real.

Hence the candidate cannot be exactly one of those explicit functionals, even after normalized rotation and phase scaling. If a prior-family coefficient vanishes, it still cannot match the candidate, whose three coefficients are nonzero. This is a functional-matching certificate only: it does not prove that every possible implicit extremal covered by the general paper has different geometry, nor does it supply any historical-firstness claim.

## 3. The candidate's quadratic differential is the classical source mechanism

Let F=Re L. Use standard Wirtinger derivatives, treating aₙand its conjugate independently: ∂F/∂aₙ=λₙ/2. Source(5.6)–(5.7) defines

    P_FS(x)=Σᵥ₌₂⁴Aᵥx^(v−1),
    Aᵥ=Σₙ₌ᵥ⁴(∂F/∂aₙ)[zⁿ]f(z)ᵛ=L(fᵛ)/2.

Independent finite power multiplication gives

    L(f²)=1+iε(2a₃+a₂²−6a₂)=a,
    L(f³)=iε(3a₂−3)=b,
    L(f⁴)=iε=c.

Thus

    P_FS(1/w)/w² = (a/2)w⁻³+(b/2)w⁻⁴+(c/2)w⁻⁵
                  = −Q_candidate(w)/2.

Source(5.9) uses [P_FS(1/w)/w²]dw²≤0; the candidate uses Q_candidate dw²>0 along regular arcs. The signs agree after multiplication by−1/2 in the stated Wirtinger normalization. The paper's linear-functional endpoint formulas (5.41)/(5.50) can absorb the common factor2 into the coefficient vector; that convention would give−Q_candidate instead. An overall positive factor does not change a trajectory or the sign comparison. The source's polynomial P_FS(x) must not be confused with its earlier exterior rational P(w) in Section4, nor with the candidate's polynomial after the double-cover substitution.

This verifies substantive classical method overlap. Finite coefficient extraction, variational slit differentials and their relation to Loewner/control equations are prior methods and require credit. The candidate's specific functional, uniform estimates across all actual global maximizers, certified reversals and actual-tip identification are additional concrete work; this comparison alone cannot establish their novelty.

## 4. Boundary equations and local coefficient expansions do not certify the target

On p139 the source separately defines the full coefficient-body boundary ℬₙ and supporting set ℛₙ⊆ℬₙ by existence of a globally supporting hyperplane. On p140, Teichmüller's sufficiency assertion optimizes aₙ with a₂,…,aₙ₋₁ fixed. That is a constrained cross-section result; it is not automatically a global linear support problem with no fixed lower coefficients.

The arbitrary initial-parameter discussion on p155 follows curves on ℬₙ. It then gives extra properties enjoyed by points ofℛₙ, including the unique double zero. One must not reverse these necessary implications or simply rename an arbitrary boundary curve a support point. The explicit global propagation of Section4 starts with an already solved extremal function, a genuine stronger premise.

Theorem5.1(pp156–157) reduces a linear extremal problem to a nonlinear boundary-value system with endpoint conditions containing unknown coefficients of the solution. It does not work out a mixed complex degree-four instance or any polar/radial sign reversal. Invoking the general reduction as though it were a solved counterexample transfers the central difficulty to an equivalent unsupported instance. That shortcut is blocked absent a solved instance with actual support/slit and geometric signs.

Finally, (5.92)–(5.94) and Theorem5.4 concern coefficients of the changing normalized functions as s=exp(−t)→0. For ν≥2,

    aν(s)=ν+[ik(ν²−1)/3]s
          +[−k²ν(ν²−1)/18+iβν]s²+O(s³),
    |aν(s)|²=ν²−[k²(ν²−1)/9]s²+O(s³).

The script independently verifies the second identity from the first. This local coefficient estimate is neither θ′=Im(w′/w) nor β=arg(w′/w) on an omitted arc. The source's φ(s), defining the Loewner control κ=−exp(iφ), is also a boundary-preimage/control angle, not arg w or arg w′. Recovering the physical slit still requires the actual conformal mapping and its tip/subarc; no angle reversal follows just from Im A₃≠0 or non-Koebe departure.

The full source contains no worked actual S-support slit whose polar argument or radial angle is shown nonmonotone. This is a source-specific scope finding after full inspection, not an assertion that no later result or unpublished consequence exists.
