# Conformal first-positive Dirac infimum on a torus

Problem 30005600 / OWR-14297736-006. Author research packet, 7 October 2026.

## Scope and disposition

The full conjecture remains unresolved in this packet. No complete proof, counterexample, novelty, formal verification, or external peer-review claim is made. The partial results below distinguish credited prior theorems from direct elementary deductions and bounded numerical exploration.

Write Γ=Z(1,0)+Z(a,b), b>0, |a|≤1/2, a²+b²≥1, T=R²/Γ, and let g₀=dx²+dy² be its flat metric, of area b. Fix the trivial spin structure S₀, meaning spinors are periodic along both lattice generators in a parallel frame. It has two complex-dimensional harmonic-spinor kernel for every conformal metric. Let μ₁(g)>0 be the least *strictly positive* eigenvalue of the geometric Dirac operator, excluding this kernel. Spectrum symmetry makes it the least positive absolute value as well. Define

    Λ(a,b)=inf_{f∈C∞(T), f>0} μ₁(f²g₀) (∫_T f² dA₀)^(1/2).

Equivalently, impose ∫f²dA₀=1. This is an infimum over metrics in one fixed conformal class with one fixed spin structure. It is not over moduli, spin structures, or Laplace eigenvalues. The OWR conjecture is

    Λ(a,b) = min(2π/√b, 2√π).

The original split uses b>π and b≤π; both branches agree at π. Including zero as the first nonnegative eigenvalue would instead make that eigenvalue identically zero and would be the wrong problem.

### Primary-source status

The exact source is Antoine Métras, joint with Mikhail Karpukhin and Iosif Polterovich, “Optimisation of the first non-zero Dirac eigenvalue,” OWR 36/2023, printed pp. 2034--2036, Conjecture 3; the preceding talk specifies the conventions on p. 2033. The full report was published in 2024.

Karpukhin--Métras--Polterovich, *Dirac Eigenvalue Optimisation and Harmonic Maps to Complex Projective Spaces*, IMRN 2024(21), 13758--13784, DOI 10.1093/imrn/rnae216, Theorem 1.7 proves the formula for b>2π, and uniqueness among smooth minimizers up to scaling. Conjecture 1.8 states the stronger π threshold. Their Remark 3.7 yields the endpoint b=2π by comparison with the flat value. Thus b=2π is already an elementary consequence of the published results, not a claimed new resolution.

The April 2026 preprint by Pavel Martynyuk, arXiv:2604.14840v1, develops higher-eigenvalue existence criteria and the conformal spectrum of the sphere. Its introduction explicitly leaves the general strict spherical inequality open; its results do not supply this torus threshold. A bounded search of current primary sources and the authors' publication listings found no full solution. This is dated search evidence, not an exhaustive assertion of open status.

## Approach 1: harmonic-map energy and spin parity

### 1.1 Exact flat value

The dual lattice consists of

    η_(m,n)=(m,(n-am)/b),    m,n∈Z.

The constant-coefficient Dirac symbol has eigenvalues ±2π|η|. Fourier completeness gives the whole spectrum, with η=0 contributing only the kernel. Its least nonzero dual length is 1/b. To check this without suppressing the fundamental-domain assumption, multiply its square by b²:

    b²|η_(m,n)|²=b²m²+(n-am)².

For m=0, n≠0 this is at least 1, attained by n=±1. For |m|≥2 it is at least 4b²≥3 because b²≥1-a²≥3/4. For |m|=1 the smallest possible |n-am| is |a|, so the expression is at least a²+b²≥1. Hence

    μ₁(g₀)=2π/b,    μ₁(g₀)√Area(g₀)=2π/√b.

Together with the credited spinorial spherical-bubbling upper bound [KMP, Theorem 3.3 and its proof], this gives Λ≤min(2π/√b,2√π). It is only an upper bound.

### 1.2 The obstruction is an energy gap, not existence

We use the following precise prior inputs, all recorded and applied in KMP §§3.1--3.2:

1. Below 2√π, a smooth conformal minimizer exists on a torus (Ammann; KMP Theorem 1.1).
2. It determines a quaternionic harmonic map Ψ:T→CP¹=S² with the given induced spin structure, and its antiholomorphic energy is E⁽⁰,¹⁾(Ψ)=Λ².
3. In this subthreshold torus situation the map has degree zero, and therefore E(Ψ)=2Λ². Here E=(1/2)∫|dΨ|² and the target is the round unit sphere. The holomorphic and antiholomorphic energies differ by 4π deg Ψ. A nonzero-degree harmonic torus-to-sphere map is holomorphic or antiholomorphic; the first possibility would produce zero eigenvalue, and the second has antiholomorphic energy at least 8π.
4. A harmonic torus-to-unit-sphere map with E<4π takes values in a great circle (Ferus--Leschke--Pedit--Pinkall, Corollary 6.6).

The last theorem only supplies 4π, whereas the spherical threshold for the minimizer corresponds to total harmonic energy 8π. Replacing one constant by the other without an additional theorem would be a factor-two error.

For completeness, harmonic circle maps have a simple explicit form. Lift Ψ=e^{iθ} to the universal cover. Harmonicity says Δθ=0 and the increments of θ along lattice translations are integral multiples of 2π. Subtract the associated linear function 2π⟨ξ,z⟩, ξ∈Γ*, obtaining a periodic harmonic function; integration by parts makes it constant. Thus

    Ψ(z)=e^{iθ₀}e^{2πi⟨ξ,z⟩},    E(Ψ)=2π² b |ξ|².

The induced spin character is χ(γ)=ξ(γ) mod 2. Indeed a spinor lift uses half the phase, e^{±πi⟨ξ,z⟩}; its monodromy is (-1)^{ξ(γ)}. Equivalently a periodic plane-wave eigenspinor with frequency η gives projective phase frequency ξ=2η. Consequently, for S₀ the nonconstant circle maps have ξ∈2Γ*, and

    E(Ψ)≥8π²/b.

This explicitly retains the spin restriction; allowing every ξ∈Γ* would give the nontrivial-spin scale and an incorrect bound.

### 1.3 Consequences and exact gap

Suppose Λ<min(2π/√b,√(2π)). Then Λ<2√π, so the smooth minimizer above exists and E=2Λ²<4π. It must be a circle map with induced trivial spin, so E≥8π²/b, contradicting Λ<2π/√b. Therefore

    min(2π/√b,√(2π)) ≤ Λ(a,b) ≤ min(2π/√b,2√π).        (1)

This recovers the known b>2π region and proves equality at b=2π from the credited energy-gap theorem. It does not prove endpoint uniqueness: E=4π is outside the strict circle theorem.

The exact missing lower bound, in the harmonic-map formulation, is

    E(Ψ) ≥ min(8π²/b,8π)

for the admissible nonholomorphic quaternionic harmonic maps inducing S₀. A stronger sufficient statement would say that every such map not contained in an equator has energy at least 8π. We have not proved either statement. Ordinary degree estimates and the 4π circle theorem cannot bridge the interval 4π≤E<8π. This route is blocked at that explicit analytic/geometric classification problem; invoking it is not a proof.

## Approach 2: a kernel-corrected weighted chiral inequality

Fix Pauli matrices σ₁,σ₂ and the flat operator D₀=-i(σ₁∂x+σ₂∂y), unitarily equivalent to the preceding geometric convention. The conformal covariance formula in the norm-preserving bundle identification is

    D_(f²g₀)(f^(-1/2)v)=f^(-3/2)D₀v.

After also making the L² measure unitary, the operator on flat L² is

    A_f=f^(-1/2)D₀f^(-1/2),    ker A_f={f^(1/2)c:c∈C²}.

The square has least nonzero eigenvalue μ₁². Set u=f^(1/2)v. Its Rayleigh quotient and orthogonality condition are

    ||A_fu||²/||u||² = (∫|D₀v|²/f)/(∫f|v|²),    ∫f v=0.

The square preserves chirality, and conjugation exchanges the two chiral scalar forms. Thus it suffices to minimize over complex scalar v:

    μ₁(f²g₀)² = inf_{v≠0, ∫fv=0}
                   [∫|Lv|²/f]/[∫f|v|²],
    L=∂x+i∂y.                                             (2)

All integrals are with dA₀. Smooth test functions are dense in the form domain. For smooth positive f ellipticity and the compact-resolvent min--max principle justify (2). The opposite sign in L yields the same infimum by complex conjugation. Zero-mean with respect to dA₀ is not the required constraint; the weight f cannot be omitted.

Let M=max f and F=∫f. Write v=w+c with ∫w=0. The constraint gives c=-(∫fw)/F, and direct expansion gives

    ∫f|v|²=∫f|w|²-|∫fw|²/F ≤ M∫|w|².

Also Lc=0. Parseval and the exact dual-lattice calculation show

    ∫|Lw|²≥(2π/b)²∫|w|².

It follows that

    μ₁(f²g₀)² ≥ (2π/b)²/M²,
    μ₁(f²g₀)√Area(f²g₀) ≥ (2π/b) ||f||₂/M.                (3)

This holds for every smooth positive f and treats the harmonic kernel exactly. It becomes equality for constant f. But ||f||₂/M may approach zero for concentrating positive factors, so it does not yield a uniform sharp conformal lower bound. The tempting substitution M≤||f||₂/√b reverses the actual inequality. This identifies precisely why an elementary unweighted Poincaré argument fails.

Equivalently, the full conjecture would follow from the sharp weighted inequality

    (∫f²)(∫|Lv|²/f) ≥ min(4π²/b,4π) ∫f|v|²,
    f>0,  ∫fv=0.                                          (4)

We have derived this exact reformulation, not proved (4). The concentration-sensitive sharp constant is the remaining gap for this route.

## Approach 3: an exact nonconstant metric family

Here f=f(y) is a smooth positive b-periodic function on T. Define

    F=∫₀ᵇ f(y)dy,    Q=∫₀ᵇ f(y)²dy,    M=max_y f(y).

Assume M≤F. Then the *full* first-positive Dirac eigenvalue, not just one trial branch, is

    μ₁(f²g₀)=2π/F,
    μ₁(f²g₀)√Area(f²g₀)=2π√Q/F ≥ 2π/√b.                 (5)

Equality on the right occurs exactly for constant f.

Proof. In the generalized flat equation D₀v=λ f v, split into x-Fourier sectors v=e^{2πinx}w(y). The skew-lattice condition is w(y+b)=e^{-2πina}w(y). For n=0, diagonalize σ₂. The scalar equations have solutions exp(±iλ∫₀ʸf), and b-periodicity is equivalent to λF∈2πZ. Hence the positive n=0 spectrum starts at 2π/F; zero gives exactly the constants.

For n≠0, D_n=2πnσ₁-iσ₂ d/dy. Since the Pauli matrices anticommute, integration by parts under the quasiperiodic boundary condition gives

    ||D_n w||₂²=(2πn)²||w||₂²+||w'||₂².

If D_nw=λfw, then |λ|²M²||w||₂²≥||D_nw||₂², so

    |λ|≥2π|n|/M≥2π/F.

Thus no other sector undercuts the explicit n=0 branch. Translation symmetry decomposes the compact-resolvent operator into these sectors, so this covers the full spectrum. The area is Q because x has period one. Finally F²≤bQ by Cauchy--Schwarz, with equality only for constant f. This proves (5).

A concrete family is f(y)=1+εcos(2πy/b), |ε|<1, 1+|ε|≤b. Then

    μ₁√Area=(2π/√b)√(1+ε²/2).

This excludes a counterexample from this entire explicitly bounded-contrast one-variable family, including many conformal classes in the unresolved range π<b<2π. It says nothing about arbitrary two-variable factors or f(y) with M>F. For those factors the n≠0 sectors might be lower and must not be discarded. When b<1, M≤F is impossible, so the theorem has no examples there. When b=1 it forces f constant.

## Approach 4: pullback from a nontrivial spin structure

The literature supplies low-energy non-equatorial harmonic maps and non-flat critical metrics for nontrivial torus spin structures, including Gauss maps of Delaunay unduloids [KMP, Remark 3.8]. A natural candidate counterexample mechanism is to trivialize their spin character by a double cover and hope to keep the energy below the spherical value.

This simple mechanism cannot work. Let χ:Γ→Z/2 be nonzero, and let Γ'⊂Γ be a finite-index subgroup on which χ vanishes. The covering π:R²/Γ'→R²/Γ has degree d=[Γ:Γ']≥2 because Γ'⊂ker χ and [Γ:ker χ]=2. Pulling back the induced spin structure trivializes it; this follows directly from restricting its monodromy character. For any harmonic map Ψ into the unit sphere, its pullback is harmonic and

    E(Ψ∘π)=d E(Ψ).

Indeed the covering is conformal, energy is conformally invariant in dimension two, and integration over a fundamental domain for Γ' sums d copies of a domain for Γ.

If Ψ is not contained in a great circle, the credited FLPP gap gives E(Ψ)≥4π. Consequently every such spin-trivializing lift has

    E(Ψ∘π)≥8π,    E⁽⁰,¹⁾(Ψ∘π)≥4π

when the degree is zero, as in the relevant low-energy torus candidates. Thus the pulled-back harmonic map and its associated eigenpair cannot themselves supply a sub-spherical energy witness. This does not give a lower bound for the first positive eigenvalue of the pulled-back metric: the cover may introduce additional, lower eigenmodes. In particular, an associated eigenvalue satisfying λ²Area≥4π is compatible with μ₁²Area<4π. If the base map is equatorial, its lift is equatorial too, and Approach 1 computes the allowable trivial-spin map energies exactly.

This is an obstruction only to the low-energy harmonic-map witness obtained by direct finite-cover pullback. It does not exclude a counterexample found through a different eigenmode of the literal pullback metric, does not classify intrinsically trivial-spin maps, and does not exclude deformations of a cover map. In particular, an equality-energy lift might conceivably deform to lower energy while changing its induced metric. No spectral-ordering or stability theorem of the needed strength was obtained here. The direct low-energy map construction is obstructed; a general covering-based metric search and the full conjecture remain unresolved.

## Approach 5: two-variable variational counterexample search

Equation (2), rather than an indefinite Dirac truncation, provides a positive variational search. Use u=x-ay/b and v=y/b, so 0≤u,v<1 and dA₀=b du dv. Let e_k=exp(2πi(mu+nv)), k=(m,n), and q_k=m+i(n-am)/b. For Fourier coefficients ĉ_h(w)=∫_[0,1]² w e^(-2πi⟨h,(u,v)⟩), choose finitely many nonzero frequencies. Eliminating the constant coefficient by ∫f v=0 gives the matrices

    A_ij=4π² conjugate(q_i) q_j ĉ_(i-j)(1/f),
    B_ij=ĉ_(i-j)(f)-ĉ_i(f)ĉ_(-j)(f)/ĉ_0(f).                (6)

Here B is a positive-definite weighted covariance matrix and A is positive definite. The lowest generalized eigenvalue A c=ρ B c is a trial upper bound for μ₁², provided its entries are evaluated as exact integrals. The overall factors b cancel in ρ, and area normalization multiplies ρ by b∫_[0,1]² f². This constant-mode Schur complement is essential: projecting out the unweighted constant would be the wrong variational space.

The script search_conformal.py searches

    f=exp(c₁cos2πu+c₂cos2πv+c₃cos2π(u+v)
          +c₄cos2π(u-v)+c₅cos4πv+c₆sin2π(u+v)).

It normalizes mean(f²)=1, uses |m|,|n|≤3 excluding zero, and 96×96 FFT trapezoidal quadrature. Seven conformal classes are tested: (a,b)=(0,1), (1/2,√3/2), (1/4,2), (0,π), (1/2,π), (1/4,4), (0,6). At each class there are 41 initial factors (including the flat one), followed by two bounded six-variable L-BFGS-B minimizations from the best nonconstant initial factors. The random seed is 30005600. Best factors and the best initially sampled nonconstant factors are re-evaluated at Fourier cutoffs 4 and 6 and quadrature sizes 128 and 192. Six flat-spectrum and three exact one-variable metric controls are run first.

Results: no computed value fell below the conjectured target. For the square and equilateral classes, the optimized cutoff-3 values fell below their flat values, as they should be allowed to do, but the cutoff-6 re-evaluations were approximately 4.9250 and 4.9641, respectively, still above 2√π≈3.5449. In the other five classes the best search factor was flat. This does not establish that flat is minimizing there: at b=2 the established spherical-bubbling upper bound 2√π is strictly below the flat value 2π/√2, so smooth sub-flat competitors exist. This finite search failed to capture that known comparison. No necessity of concentration or nonexistence of a smooth minimizer is inferred. The distinction is an important negative control on overinterpreting the optimization.

The actual FFT quadrature and dense generalized eigenvalue computations use floating-point arithmetic. Their outputs are not certified integral enclosures, rigorous spectral bounds, or a global optimization certificate. A candidate strict counterexample would require a new certified test-function inequality with explicit quadrature and rounding bounds. None was found. The finite Fourier space also poorly resolves concentrating bubbles; optimization convergence messages certify neither local nor global mathematical minimality.

This fifth approach ends without a counterexample or proof. Its useful deliverable is the explicit kernel-corrected variational formulation, reproducible search parameters and negative controls, with the discretization limitations stated.

## Final remaining problem and review challenges

The full target remains open in this work after five substantive approaches. The established comparison (1) settles b≥2π by credited prior theory; the exact family (5), the weighted bound (3), and the harmonic-map energy obstruction for covers are scoped partial results. The unresolved ranges are π<b<2π for the flat-value lower bound and b≤π for the spherical-value lower bound, including b=π itself.

The following checks were applied to the written arguments:

- Zero modes are excluded, and the weighted kernel projection appears explicitly in both (2) and (6).
- The two spin characters cannot be exchanged: periodic frequencies give 2π/b, whereas an antiperiodic generator can give π/b.
- The conformal class is fixed; no modulus optimization or cover is silently identified with the original class.
- Area is b for the reference torus and ∫f² for the conformal metric. Every displayed normalized quantity is invariant under f↦cf.
- Harmonic-map energy is E=(1/2)∫|dΨ|² with unit target sphere. The relation E=2Λ² is why 4π rigidity only yields b>2π.
- At b=π the two conjectured formulas coincide, but equality has not been proved. At b=2π the value follows from the credited comparison; uniqueness is deliberately not asserted there.
- The one-variable theorem controls every x-Fourier sector, including skew-lattice quasiperiodicity. Without M≤F it supplies an explicit spectral branch, not the whole first eigenvalue.
- The covering estimate concerns the energy of the literal pulled-back harmonic map and its associated eigenpair. Lower eigenmodes of the pullback metric, perturbations, and intrinsically trivial-spin harmonic maps remain uncontrolled.
- Numerical Ritz tests cannot prove a lower bound. The established spherical-bubbling comparison supplies sub-flat competitors at b=2, behavior not recovered by the low-order search. Neither necessity of concentration nor nonexistence of a smooth minimizer is established.

At the author freeze, no independent review had yet been performed. The accompanying audit accepts the scoped partial results with the cover and numerical-scope corrections incorporated in this reading copy. The analytic steps are elementary deductions plus explicitly named prior theorems; the computational controls are finite arithmetic/numerical checks, not formal verification. In particular, neither the missing harmonic energy estimate nor the sharp weighted inequality (4) is assumed in any proved partial result.

## References

[OWR] *Geometric Spectral Theory*, Oberwolfach Reports 20 (2023), report 36, published 2024, pp. 2017--2106. Relevant contributions pp. 2031--2036; exact Conjecture 3 at p. 2036. DOI: https://doi.org/10.4171/owr/2023/36 . Official PDF: https://ems.press/content/serial-article-files/47475 .

[KMP] Mikhail Karpukhin, Antoine Métras and Iosif Polterovich, *Dirac Eigenvalue Optimisation and Harmonic Maps to Complex Projective Spaces*, International Mathematics Research Notices 2024(21), 13758--13784. https://doi.org/10.1093/imrn/rnae216 . Primary article: https://academic.oup.com/imrn/article/2024/21/13758/7810213 . Author preprint: https://arxiv.org/abs/2308.07875 and https://dms.umontreal.ca/~iossif/dirac.pdf . Particularly Theorems 1.1, 1.7, 3.3, 3.5--3.6, Conjecture 1.8, and Remarks 3.7--3.8.

[FLPP] Dirk Ferus, Katrin Leschke, Franz Pedit and Ulrich Pinkall, *Quaternionic holomorphic geometry: Plücker formula, Dirac eigenvalue estimates and energy estimates of harmonic 2-tori*, Inventiones Mathematicae 146 (2001), 507--593. Corollary 6.6. https://arxiv.org/abs/math/0012238 .

[Mar26] Pavel Martynyuk, *Conformally critical metrics and optimal bounds for Dirac eigenvalues on spin surfaces*, arXiv:2604.14840v1, 16 April 2026, preprint. https://arxiv.org/abs/2604.14840 . Used only for current literature scope; no unverified generalization from its higher-eigenvalue/sphere results is invoked.
