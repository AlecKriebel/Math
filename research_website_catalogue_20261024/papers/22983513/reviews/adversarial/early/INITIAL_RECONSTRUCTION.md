# Independent adversarial initial reconstruction — record22983513

## Independence and exact full claim

I personally read the complete actual three-page published PDF, all173controlling-TeX lines and allthreefresh individual page rasters before any foreign scientific body, supplied programme/result, inventory assessment or archived/current peer opinion. Earlier personal source-only acquisition exposure is fully disclosed in SOURCE_PINS.json: identity/API metadata, transport/header shapes, checksums/archive names and structural counts only. That exposure did not include scientific text or supplied code/results. The prior118packet is sealed and its findings remain withheld.

For every integer dimension n≥1, every nonempty bounded open Ω⊂Rⁿ (no connectedness or boundary regularity), and every integer J≥1, let E₁≤E₂≤… be the form-defined Dirichlet Laplacian eigenvalues, counted with multiplicity. Define A=J⁻¹Σ_(j≤J)E_j, B=J⁻¹Σ_(j≤J)E_j², M₁=(n+2)A/n and M₂²=(n+4)B/n. The exact target is

    D=M₁²−M₂² > (E_(J+1)−E_J)²/4.

The manuscript additionally claims the stronger strict Yang inequality at every finite real z>E₁:

    Σ_(E_j<z)(z−E_j)² < (4/n)Σ_(E_j<z)(z−E_j)E_j.

Its coordinate-times-eigenfunction lemma asserts infinite spectral support for every real normalized eigenfunction and every coordinate. These are universal analytic claims, not numerical conjectures restricted to boxes. The normalization uses M₂² and explicitly corrects a stated source typo; its actual primary meaning must be checked later. The claim is finite nonattainment, not a uniform positive deficit, a quantitative growth theorem, historical-firstness certification, Neumann/Robin/magnetic/PDE-with-potential theorem or unbounded-domain result.

Success means verifying the full quantified claim and all functional-analytic/spectral/algebraic reductions, with explicit boundary falsifiers. A substantive gap is to be recorded as such, without promoting a narrowed conditional theorem or inventing an extended repair. All119findings remain private until root119's explicit initial reading gate OPEN.

## Family 1 — attack the rough/disconnected-domain foundation

Let Q be an enclosing open box. Extension by zero embeds H₀¹(Ω) isometrically into H₀¹(Q): approximate by C_c∞(Ω), then regard those functions as C_c∞(Q). The box's Poincaré bound gives positive bottom energy. Compactness of H₀¹(Q)→L²(Q), restricted to these zero extensions, gives compact embedding for Ω. The associated closed nonnegative form therefore has compact resolvent and strictly positive eigenvalues, finite multiplicity and a complete orthonormal basis. Nonemptiness/openess supplies a ball and an infinite-dimensional L²space, so finite eigenvalue lists do not terminate.

For the form-defined operator, u∈Dom H iff u∈H₀¹(Ω) and the distribution −Δu is represented by an L²function. One implication comes from testing the form identity on C_c∞; the other extends the distribution identity to all H₀¹test functions by density. This avoids H²regularity and a pointwise boundary trace. The real form commutes with conjugation, so one may choose a real orthonormal eigenbasis, including all degeneracies. Connectedness is nowhere required by this construction.

Falsification targets: an unnoticed smooth-boundary theorem, replacement Dom H=H²∩H₀¹, infinite multiplicity below a finite threshold, or dependence on a strictly positive ground state on all components. None is needed by the reconstruction. After the seal, check the actual sources' stated domains rather than borrowing their regularity assumptions invisibly.

## Family 2 — attack multiplication, distributions and integration by parts

For a normalized real eigenfunction Hu=Eu, bounded coordinate xα and derivative1 imply multiplication maps H₀¹(Ω) into itself. More concretely, xαu_m→xαu in H¹ for smooth compactly supported approximants u_m, using boundedness of Ω. The distribution product rule gives

    −Δ(xαu)=E xαu−2∂αu ∈ L²,

hence w=xαu∈Dom H. No normal derivative of u or regular boundary is needed. Integrating ∂α(xαu_m²) over Rⁿ for the compactly supported extension gives −2∫xαu_m∂αu_m=∫u_m². Passing to the limit is legitimate by the L∞bound on xα and L²convergence of u_m and gradients. Thus

    v=(H−E)w=−2∂αu,     <w,v>=1.

For complex eigenfunctions the displayed unsymmetrized real identity requires care; the manuscript explicitly chooses real functions and a real basis, so this is a model choice available without restricting the theorem. A domain translation changes w by a multiple of u, leaves (H−E)w unchanged, and preserves the identity because <u,v>=0.

Falsifiers: attempting the same proof for Neumann or periodic boundary conditions can fail at coordinate multiplication preserving Dom H. Neumann ground energy0 also immediately destroys the claimed gap inequality at J1. A confining harmonic oscillator on R can have x times its ground state in a finite spectral subspace; the differentiated eigen-equation then has a potential-derivative term. Such operators are outside the claim and expose which hypotheses carry the obstruction.

## Family 3 — two distinct infinite-support mechanisms

Range/kernel mechanism: if w belonged to a finite spectral subspace then w∈Dom H² and v=(H−E)w∈Dom H. Differentiating the interior distribution equation commutes constant-coefficient derivatives, so (−Δ−E)v=0. The form-domain characterization yields (H−E)v=0. Self-adjointness gives ||v||²=< (H−E)w,v>=<w,(H−E)v>=0, contradicting <w,v>=1. No assertion that ∂αu normally satisfies the Dirichlet boundary condition was made: it enters Dom H solely under the finite-support hypothesis.

An independent polynomial/orthogonality mechanism avoids even that domain inference for v. In distributions, (−Δ−E)²(xαu)=0. If w=Σ_(k in finite K)c_k u_k, this implies the L²identity Σ( E_k−E )² c_k u_k=0. Orthonormality forces c_k=0 outside the E-eigenspace, hence (H−E)w=0, contradicting the same identity1. Differentiation here is distributional; no elliptic H²up-to-boundary regularity is assumed. This separates a finite-dimensional polynomial annihilator from the self-adjoint range/kernel argument.

As a third diagnostic, on (0,π) the normalized sine basis has, for j≠k of opposite parity,

    <u_k,xu_j>=−8jk/[π(j²−k²)²],

and zero off-diagonal coefficients for equal parity. There are infinitely many nonzero opposite-parity coefficients for each j. This provides a directly computable Fourier mechanism on an explicit subclass, not a proof for arbitrary Ω. A proposed finite-spectral truncation cannot be treated as exact evidence against the universal lemma: it loses the full commutator sum rule.

## Family 4 — attack infinite sums, signs and the exact remainder

Write a_jk^α=<u_k,xαu_j>, δ=E_k−E_j and t_j=z−E_j. Parseval and w∈Dom H give Σδ²|a|²=4||∂αu_j||²; the scalar identity gives Σδ|a|²=1. Absolute convergence of the first-order series follows from Cauchy–Schwarz applied to δa and a. The combination t_j²δ−t_jδ² is therefore absolutely summable. Summing coordinates uses Σ||∂αu_j||²=E_j by the form eigenvalue identity.

The fixed-j expression is n t_j²−4t_jE_j=Σ_(α,k)t_j(E_k−E_j)(z−E_k)|a|². For j,k both in finite L={E_j<z}, t_k=z−E_k gives paired factors t_j(E_k−E_j)t_k and t_k(E_j−E_k)t_j, which cancel exactly. Terms E_k=z vanish. Flipping the remaining sign yields

    R(z)=4Σ_L t_jE_j−nΣ_Lt_j²
        =Σ_(α,j in L,E_k>z)t_j(E_k−E_j)(E_k−z)|a_jk^α|² ≥0.

Each rearrangement is controlled by the two absolute series for a fixed j, and L is finite. There is no unlicensed cancellation of conditionally convergent double sums. Hermitian symmetry would suffice at the level of absolute squares; reality makes the manuscript's simpler symmetry literal.

If R(z)=0, positivity of every coefficient for j=1 and E_k>z forces all such a_1k^α=0. Compact resolvent makes the remaining spectral space E_k≤z finite, contradicting Family3 for any coordinate. Thus R(z)>0 for every finite z>E₁. At z≤E₁ the displayed sums are empty and strictness fails, explaining the sharp threshold domain. Spectral multiplicity does not defeat the j=1choice.

## Family 5 — attack the quadratic and all repeated-threshold cases

Expanding the Jterm polynomial gives

    Q(t)=t²−(2+4/n)At+(1+4/n)B=(t−M₁)²−D.

At t=E_J, all eigenvalues strictly below the threshold occur among the first J; repeated top eigenvalues contribute zero. Thus the complete Jterm sum agrees with the strict-threshold sum. Q(E_J)≤0, strictly if E_J>E₁ and zero if all first J energies equal E₁. At z=E_(J+1)>E₁ the same equality of truncated expressions holds even when J cuts inside a repeated eigenspace, giving Q(z)<0. Then D>0, E_J≥M₁−sqrt D and z<M₁+sqrt D. The nonnegative gap is strictly less than2sqrt D, so squaring preserves strictness.

If E_(J+1)=E₁, all first J+1energies equal positive E₁. Directly D=4E₁²/n²>0 while the gap is0. This covers disconnected identical components and arbitrary finite ground-state multiplicity. A repeated higher eigenvalue also has gap0 and is covered by the strict Q(z) branch. No simplicity or connected ground state was smuggled in.

Falsifier for the strength needed: the synthetic list E₁=1,E₂=5,n1,J1 saturates D=4=(gap)²/4 and only gives Q(E₂)=0. Non-strict Yang alone cannot exclude it; the actual strict remainder is essential. It is not an interval spectrum and is not claimed as a domain counterexample.

## Family 6 — exact interval, disconnected and box diagnostics

On Ω=(0,L), E_k=c k² with c=π²/L². Direct finite power sums, without invoking any commutator theorem, give

    A/c=(J+1)(2J+1)/6,
    B/c²=(J+1)(2J+1)(3J²+3J−1)/30,
    D/c²=(J+1)(2J+1)(3J+5)/12,
    [D−(gap)²/4]/c²=(2J+1)(3J²+2J+2)/12>0.

This independently checks the constants, sign and quadratic inference for every J in dimension1. Union of r equal disjoint intervals repeats every level r times and tests thresholds/multiplicity without connectedness. For rational squared inverse side lengths, rectangle/box spectra are exact rational sums of positive integer squares after factoring π². Sorted shell enumeration must certify that no unenumerated multiindex can fall below the first J+1 levels; merely sorting a finite box of indices is not a valid spectrum check.

After the early seal, own diagnostics should use these explicit families, exact rational arithmetic, genuine high/low repeated thresholds, translations/scalings, the quadratic expansion and synthetic cancellation identities. They supplement rather than prove the analytic universal theorem. A distinct Fourier check can use explicit nonzero couplings and a rigorous tail estimate, without treating a truncated infinite sum as exact equality.

## Family 7 — attack normalization, scaling and unsupported quantitative promises

Scaling Ω by s>0 sends E→s⁻²E; the squared expression D and squared gap scale s⁻⁴. The literal unsquared M₁²−M₂ mixes orders s⁻⁴ and s⁻². An interval of length3π has E₁=1/9 and E₂=4/9, n1,J1; the unsquared left side is (1−sqrt5)/9<0 while (gap)²/4=1/36>0. Thus that literal formula is not a universal bound. The target explicitly discloses the normalization change; the actual original source must be read to authenticate the corrected problem rather than treating an inventory label as authority.

There is no uniform absolute positive deficit over all bounded domains: take any fixed domain and dilate by arbitrarily large finite s. Each domain remains bounded while any strictly positive deficit scales to0. Nor does finite nonattainment conflict with leading Weyl cancellation; in the exact interval formula the deficit divided by E_J² tends to0 as J→∞. None of this supplies the separate quantitative growth bounds that the paper expressly declines to claim.

## Family 8 — source/provenance falsification frontier and stopping rule

The manuscript presents its analytic proof self-containedly, so primary sources are needed to verify the exact original corrected saturation statement, classical trace identities and claimed historical status rather than to import unexamined strictness. Critical later readings: actual Harrell–Stubbe Proposition6 and its definitions; actual OWR2009printed415 and nearby context/attribution; actual Ashbaugh2002printed12 and the exact strictness caveat; applicable commutator source domains. Website/inventory statements must not substitute for those bodies. Priority remains bounded to inspected sources; a website's present status cannot establish an unresolved mathematical question worldwide.

No source programme, result record, archived AI audit, current sibling review or foreign paper has yet been read. The initial proof reconstruction above is substantial and independent but source/history claims remain an explicit frontier. A substantive contradiction would stop promotion of the complete claim, without a long repair project. The next work, after this seal, is direct primary inspection plus own exact distinct diagnostics and bounded source reproducibility. Root119initialgate is still CLOSED and every scientific finding remains withheld.
