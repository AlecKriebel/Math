# Independent Picard and descent falsification audit

Checkpoint: 2026-10-06 22:18 America/Los_Angeles (2026-10-07 05:18 UTC).
Completion estimate: 100% of the assigned Section 05/06 subaudit; this is not an estimate of completion of the overall discovery goal or verification of the complete theorem.

## Scope and disposition

Read the upstream `build/sections/05-curves.tex` and `06-descent.tex` without editing them. Audited Picard freeness, character maps, matrix transport, scalar cancellation, generic-module extension, derived rank extraction, the mixed Picard determinant pairing, and the finite-torsor Euler argument. The construction and high-connectivity geometry of X and the comparison of its Euler polynomial with the fiber integral are outside this subaudit.

**Disposition:** no explicit counterexample or missing hypothesis was found in these assigned arguments. This is a scoped mathematical audit, not certification of the division theorem or its application to EGH. Below are independent reconstructions of the potentially delicate steps and the precise dependencies retained.

## 1. Picard freeness

Source: `05-curves.tex`, lines 350–367.

Fix a nonidentity element g of order r. If a degree-one line V is fixed as an isomorphism class, choose t:g_*V→V. The composite t·g_*t·…·g_*^(r−1)t is scalar c, because the curve is connected and projective. Multiplying t by λ with λ^r=c^−1 makes that composite the identity. The resulting cyclic linearization is genuine. Since the cyclic subgroup acts freely on C, the quotient q:C→C/⟨g⟩ is an étale cover of degree r and the linearized line descends. Thus deg V=r deg V₀, impossible for deg V=1 and r>1.

The argument does not need a linearization under the entire possibly noncyclic G. Attempting to object using a Schur multiplier is therefore inapplicable. Over the complex numbers the required root λ exists. Freeness persists after extension of the constant field, since each geometric fixed-point scheme is already empty over the algebraically closed original field.

Boundary check: for b=2 the source curve has genus one and the free deck action is by translations; the same degree divisibility proves the result. It does not incorrectly infer freeness on Pic⁰, where translations can act trivially.

## 2. Character maps

Source: `05-curves.tex`, lines 369–430.

For ξ:G→μ_b, the character of covering monodromy is an element ᾱ∈Hom(H₁(T,Z),Z/b). Because H₁(T,Z) is free, choose an integral homomorphism α reducing to ᾱ. For every loop γ in C, qγ has monodromy identity; therefore α(qγ)∈bZ. Hence q*α/b is an integral H¹(C,Z) class. The harmonic representative ω of this class is G-invariant, because it is pulled back from T. Its integral gives f_C:C→R/Z, and along a path c→gc the increment is the covering character ξ(g), after fixing the left/right monodromy convention.

The Abel map a:C→Pic¹(C), c↦O(c), is equivariant. The integral H¹ isomorphism induced by a identifies the class of ω with an integral class of the Picard torsor. On the underlying real torus there is a unique translation-invariant real form ω̃ pulling back to the harmonic form ω. Integrate ω̃ to a circle map and normalize it at one Abel point. Since the induced action on the torsor is affine, g*ω̃−ω̃ is translation-invariant. Its pullback vanishes, so it is zero. Consequently f(g_*A)/f(A) is constant on the connected torsor. On the Abel image its value is ξ(g), proving the required equivariance everywhere.

The hypotheses that matter here are the connected étale cover, the surface H₁ torsion-freeness, and the Abel integral H¹ isomorphism. These are present. There is no need for the whole nonabelian monodromy to lift to an integral homomorphism; only its abelian character is lifted. The construction also works for characters of order properly dividing b.

## 3. Matrix transport and scalar ambiguity

Source: `05-curves.tex`, lines 252–340; `06-descent.tex`, lines 81–98 and 148–177.

The vanishing H*(C,A L^(g_T−1))=0 gives H*(P¹,V(−1))=0 for V=π*(A L^g_T). For every geometric q∈P¹, the evaluation sequence identifies H⁰(V) with the rank-e fiber V_q. Consequently V is canonically trivialized by evaluation, and the section module is E_A⊗κ[U,V]. Multiplication by a line-bundle section has degree one and commutes with multiplication by every other section.

To check the direction of the character factors, write

    m_a(e) = A_a(e) u + B_a(e) v.

After transport, the right side becomes (g_coeff A_a)(g e) χ(g)u + (g_coeff B_a)(g e) ψ(g)v. Thus the source's substitution χ(g)U,ψ(g)V is correct for its definition of g_coeff. No inverse character is missing.

If a transported universal A is identified with the universal A at the transported parameter in a different way, the identifying map is multiplied by a scalar. It multiplies both source and target section spaces by the same scalar, so conjugation on End(E_A) is unchanged. The scalar projective cocycle is central and disappears on End(E_A), giving a genuine algebra action. This does **not** provide a genuine action on E_A itself; Section 06 correctly treats that action as twisted.

The source also correctly distinguishes commuting matrix polynomials from commuting individual coefficient matrices. The latter, stronger assertion would generally be false and is not used in these audited claims.

## 4. Twisted extension and determinant cancellation

Source: `06-descent.tex`, lines 148–267.

Morita tensoring a right module of reduced rank r over the degree-e₀e₁ algebra with the standard left End(E)-module divides its K-vector-space dimension by e₁, giving e₀r. Changing the line identification for one A_m by a scalar λ changes E and this Morita module by λ. Thus its line weight is +1.

For simultaneous curve/parameter transport, g_*A and A represent the same relative Picard point. Their relative Hom is pulled back from a line J_g on the parameter scheme. Its evaluation map is an isomorphism: on each connected curve fiber the Hom line is trivial, with h⁰=1, and the normalized universal family supplies the usual see-saw identification. Associative composition gives J_g⊗g_*J_h≅J_gh. Summing the finitely many corrected transports of any coherent rational lattice preserves both that twisted law and the constant Δ₀-action. This provides the claimed global coherent extension without requiring the section bundle to be defined on the effectiveness locus.

For one degree-zero/degree-one pair (A,V), the determinant correction is

    D = det RΓ(A⊗V)^−1 ⊗ det RΓ(A) ⊗ det RΓ(V).

Scalar action on a determinant of cohomology has exponent χ. Riemann–Roch gives χ(A)=1−g and χ(A⊗V)=χ(V)=2−g, so the weights of D are (−1,0). Hence the A scalar ambiguity is canceled exactly and the V ambiguity has no residual weight. This checks arbitrary invertible-function changes of local identifications, not only constant scalars. Determinant functoriality preserves composition, and each discrepancy between composed line identifications is precisely such a scalar. Therefore the local corrected transports glue and obey the actual group law.

The origin in the representation R is fixed. Its inclusion is a regular immersion even if X is singular: coordinates of the affine-space factor form a regular sequence in a polynomial algebra over any base ring. Its finite equivariant Koszul complex yields a bounded coherent Tor class. Thus restriction to R=0 is legitimate without flatness of the lattice over R.

## 5. Mixed Picard determinant pairing

Source: `06-descent.tex`, lines 289–344.

There is no hidden factor of two in this pairing. Let a=c₁(A) and v=c₁(V) on J_A×J_V×C. GRR in degree two of the base gives c₁(D)=−q*(av): the signed exponential −exp(a+v)+exp(a)+exp(v) has no degree-two term and its degree-four term is −av. The possible constant term multiplies only the degree-two Todd term of the curve, producing rank rather than c₁.

Normalization at c₀ excludes pure base classes. The degree-zero A has no pure curve class; V's pure curve class cannot multiply the mixed a to contribute the degree-two curve term required by integration. Hence c₁(D) is purely H¹(J_A)⊗H¹(J_V).

Under the Abel integral H¹ identification, the mixed component of a is the mixed diagonal class. In a symplectic integral basis x_i,y_i of H¹(C,Z), one may take its expression as

    a = Σ_i (b_{y_i} ∧ x_i − b_{x_i} ∧ y_i),

and the analogous expression for v with p in place of b. Integrating their product gives, up to the transport convention, the mixed class

    θ = Σ_i (b_{x_i} ∧ p_{y_i} − b_{y_i} ∧ p_{x_i}).

Its matrix consists of unimodular symplectic blocks. For d=2g, θ^d/d! integrates to ±1; in the usual complex orientation the sign is (−1)^g. Thus genus one already gives a unit, rather than 2 or 4. In the product of curve factors the blocks are independent, retaining a unit top integral.

Because each θ term uses degree one from B and degree one from P, saturating the P degree simultaneously saturates the B degree. Every positive-degree term of ch(γ) therefore integrates to zero. Picard tangent bundles are trivial, so td(Z)=1. The result is exactly ±rank γ for every K⁰ class γ, including differences of bundles.

## 6. Rank extraction and arithmetic Euler divisibility

Source: `06-descent.tex`, lines 271–287 and 353–415.

On the smooth connected locus B×X_sm×R a coherent sheaf is perfect, so its virtual rank is locally constant and equals its generic rank e₀r. Derived restriction preserves virtual rank even at fibers where the lattice is not flat. A primitive matrix idempotent after complex splitting divides ranks by e₀ and preserves H-equivariance because H fixes Δ₀ pointwise. Thus each fiber class has the required form pr_B*γ_x⊗D with rank γ_x=r.

The torsor Euler lemma survives singular Q. Write V=δ_*O_{T′} and d=[V]−a in K⁰(Q). A rank-zero virtual vector bundle lowers the support-dimension filtration of G₀(Q), hence d is nilpotent as an operator. Triviality of δ^*V implies δ^*d=0. For every α∈G₀(Q), the projection formula yields (a+d)dα=0. Over the rationals, a+d is invertible by a finite nilpotent expansion, so dα is torsion. The integer-valued Euler homomorphism kills it, giving χ(T′,δ^*α)=aχ(Q,α). This proof needs finite dimension and projectivity for Euler characteristics, both available.

H acts freely on P and hence on Z×X. The finite quotient is a scheme and its map is an étale torsor. Equivariant coherent classes with commuting Δ₀-actions descend. Their cohomology over k is a finite right Δ₀-module and therefore has dimension divisible by e₀², because Δ₀ is division over k. Torsor pullback multiplies Euler characteristic by e₁, giving χ upstairs∈e₀²e₁Z. Subsequent complex splitting/idempotent reduction divides dimensions by e₀, exactly as asserted. This argument does not assume Δ₀ remains division after complex base change.

## Exact remaining gap

No gap was identified in the scoped statements after the reconstructions above. Their strongest verified conclusion is conditional: **given** the geometrically integral X and the curve/pencil data stipulated in Sections 05/06, the rank-to-Euler proposition supplies the claimed unit fiber index and arithmetic divisibility of every twist. It does not by itself prove e₀e₁ divides r, because the fiber index and the global twisted Euler values are different numerical quantities. The comparison in Section 07 and the prior connectivity theorem remain essential and were not certified by this subaudit.

Primary reference checks: [Stacks 07S7](https://stacks.math.columbia.edu/tag/07S7) confirms that a free finite locally free action on a projective scheme has a scheme quotient and an fppf torsor; the constant group here is étale. [Stacks 0FJI](https://stacks.math.columbia.edu/tag/0FJI) supplies determinant functoriality and composition. The cited Milne PDF could not be fetched through the browser during this audit; the Abel H¹ assertion was used through its standard period-lattice construction and independently reconstructed above, rather than treating the inaccessible citation as evidence.

No outside communication, source edits, commits, or pushes were performed by this subagent.
