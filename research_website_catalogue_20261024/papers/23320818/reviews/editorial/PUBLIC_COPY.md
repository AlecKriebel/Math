# A regular zero-area singularity with a nonzero weak Bianchi defect

**Alec Kriebel** · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

12 October 2026 · Version 1.0 · [Zenodo DOI 10.5281/zenodo.23320818](https://doi.org/10.5281/zenodo.23320818)

Unrefereed research note; version 1.0. Developed with extensive AI assistance; no external human or journal peer review, journal acceptance or formal proof-assistant certification is claimed.

Authored paper and accompanying materials: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Original abstract

We apply a negative-mass member of the known Dadhich–Kar–Mukherjee–Visser metric family to the regular-zero-area-singularity conjecture in Burtscher's Oberwolfach report. Its natural static slices have harmonically regular zero-area singularities of mass −2a, but the homogeneous weak second Bianchi identity fails under the boundary-reaching vector-test convention of Burtscher–Kiessling–Tahvildar-Zadeh. We prove absolute convergence of the full scalar contraction for every such compactly supported smooth test and compute its exact boundary functional; a normalized radial test gives −8π. The metric and its Einstein tensor are classical, and the flux method is already present in the cited weak-identity work. The contribution is this explicit counterexample application and its convergence check. The example violates the null energy condition. The conclusion concerns the geometric implication in the cited static-foliation framework, with no specified matter model; it asserts neither regularity on every arbitrary tilted slice nor an identity for tests smooth after collapsing the boundary sphere to a point.

## The idea in plain English

The Bianchi identity is a geometric conservation identity for the Einstein tensor. It holds at every smooth interior point of the spacetime considered here. A weak version also asks what happens when one integrates against smooth test fields that reach a singular boundary.

A zero-area singularity is a boundary approached by surfaces whose physical areas shrink to zero. In this example, each natural static slice has a smooth harmonic resolution of that boundary and negative regular mass. The singular sphere is retained in the background smooth structure used to define the test fields.

Using a known negative-mass metric, the note shows that this slice geometry does not force the homogeneous weak identity under the stated retained-boundary convention. The complete scalar integral converges absolutely for every allowed vector test, but a normalized radial test gives the exact value −8π.

The example violates the null energy condition. It tests the geometric implication in the specified static framework; it does not supply a model of matter or settle variants that impose extra energy conditions or a different boundary-test convention.

## The precise result

Fix any a > 0. Let bar M = R_t × {x ∈ R³: ρ = |x| ≥ a}, M = int(bar M), S_a = {ρ = a}, φ = 1 − a/ρ, δ the Euclidean spatial metric and n = x/ρ. The smooth structure retains the entire boundary sphere S_a. Tests are every ψ ∈ C_c^∞(bar M; T bar M): compactly supported smooth contravariant vector fields on this manifold with boundary, with arbitrary time and angular dependence. Their normal boundary trace may be nonzero; a tangent-bundle section need not be tangent to the boundary.

Use signature (−+++), c = G_Newton = 1 and G_μν = Ric(g)_μν − (1/2)R_g g_μν, with the paper’s Ricci convention R_μν = ∂_λΓ^λ_μν − ∂_νΓ^λ_μλ + Γ^λ_μνΓ^κ_λκ − Γ^κ_μλΓ^λ_νκ. Define I_g(ψ) = ∫_M G^μ_ν ∇_μψ^ν dV_g as the integral of the complete scalar contraction.

For g = −φ^(−2)dt² + φ⁴(dρ² + ρ²dΩ²), the spacetime is static, spherically symmetric and asymptotically flat. Every slice of its natural static foliation is totally geodesic (K = 0) and has a harmonically regular zero-area singularity at S_a of regular mass −2a, including the full C¹ approaching-surface area condition.

For every test ψ in the stated class, ∫_M |G^μ_ν ∇_μψ^ν| dV_g is finite and I_g(ψ) = −(2/a²) ∫_(R × S_a) ⟨ψ_spatial,n⟩_δ dt dA_δ. Here dA_δ is Euclidean sphere area. Choose ψ = η(t)χ(ρ)∂_ρ with smooth compactly supported η, ∫η dt = 1, and smooth compactly supported χ on [a,∞) equal to 1 near a. This admissible normalized radial test gives I_g(ψ) = −8π.

The inner end is a genuine curvature singularity: Ric_μν Ric^μν = 6a²/(ρ⁶φ¹⁰) diverges as ρ decreases to a. Radial null geodesics reach it in finite affine length. It is timelike in the limiting radial conformal sense; no nondegenerate smooth extension of the physical four-metric to the boundary is asserted. The effective tensor T = G/(8π) violates the null energy condition.

The affine-lapse proposition covers every a > 0, A,B ≥ 0 with A + B > 0: set N = A + B(ρ + a)/(ρ − a) and g_N = −N²dt² + φ⁴δ. For every allowed ψ the complete scalar contraction is absolutely integrable and I_gN(ψ) = −(4A/a²) ∫_(R × S_a) ⟨ψ_spatial,n⟩_δ dt dA_δ. The homogeneous identity holds for every test in this family exactly when A = 0. The same radial test gives −16πA; A = B = 1/2 is the main metric and gives −8π. Both the vacuum endpoint A = 0, B > 0 and nonvacuum endpoint B = 0, A > 0 are included; A = B = 0 is excluded.

## Why the boundary functional is well-defined

The spatial metric is the classical negative-mass Schwarzschild zero-area-singularity example. The resolution (δ,φ) has a simple harmonic zero with inward-to-exterior normal derivative 1/a. For every family of boundary graphs approaching in C¹, bounded Euclidean areas and the vanishing φ⁴ factor force the physical areas to zero. The standard regular-mass formula gives −2a.

The classical affine-lapse tensor becomes especially simple after multiplication by the volume density: D^i_j = Nφ⁶G^i_j = (Aa/ρ³)(6n_i n_j − 2δ_ij). This tensor is smooth to the retained boundary, symmetric, tracefree and Euclidean divergence-free. Those properties cancel the entire singular connection contraction pointwise, leaving G^μ_ν∇_μψ^ν dV_gN = D^i_j∂_iψ^j dt d³x.

On compact support the resulting complete scalar density is bounded, so its absolute integral is finite for all the stated tests. Euclidean integration by parts has inner outward normal −n and gives the exact boundary flux. Individual connection summands can have divergent integrals; the proof combines the smooth interior summands before integration. It does not use a principal value or multiply tensor distributions.

The metric and Einstein tensor are due to Dadhich, Kar, Mukherjee and Visser, the spatial regular-ZAS example and mass framework are credited to Bray and Jauregui, and the boundary-flux method is already in Burtscher, Kiessling and Tahvildar-Zadeh. The contribution presented here is the explicit counterexample application and its all-test convergence check.

## Scope and limitations

The conclusion uses the natural static foliation and the retained-sphere smooth contravariant-vector test class. It is not a regularity assertion on every arbitrary tilted spacelike slice, an identity for independently smooth covectors, or an identity for fields smooth after collapsing S_a to a point. Lowering a vector with the singular metric or using the singular areal-radius collapse does not preserve the stipulated boundary smoothness.

Uniformly spacelike local tilts t = t₀ + q s(ρ), |q| < 1, have regular mass −2a/(1 − q²), but arbitrary nearly-null tilts can have a degenerate resolved radial metric. The paper expressly makes no all-arbitrary-tilted-slices claim. Its timelike-end statement concerns a limiting radial conformal causal structure, not a smooth physical extension.

Tests supported strictly inside the smooth interior obey the ordinary classical identity. The failed assertion is the homogeneous zero functional for all allowed boundary-reaching tests; the explicitly computed inhomogeneous boundary-flux identity remains valid. A zero normal boundary trace also gives zero flux.

The main example violates NEC. No specified electromagnetic or other matter system, energy-constrained version, or wider matter/evolution programme is resolved. The short report’s wording is interpreted in its cited static/BKTZ framework; the note does not claim to settle every stronger possible formalization.

BKTZ’s sufficient theorem assumes an improved bound O((ρ − a)^(−5+κ)) for some κ > 0. This example is genuinely borderline: (ρ − a)⁵G^ρ_ρ tends to 2a³. The sufficient theorem is neither contradicted nor invoked outside its hypotheses.

The metric, tensor, spatial ZAS example and boundary-flux method are classical. DKMV’s later wormhole classification takes positive mass; the negative-mass application here uses their displayed formula without attributing this ZAS/Bianchi conclusion to that classification. Bounded source comparison does not certify historical firstness, exhaustive originality or continued worldwide openness. Finite computations support consistency and do not prove the quantified all-test assertions.

## Credited prior work

[A. Burtscher, Matter particles, naked singularities, and a weak second Bianchi identity, Oberwolfach Report 40/2021, pp. 2231–2233](https://doi.org/10.4171/OWR/2021/40). The geometric conjecture and separate matter/evolution discussion. The workshop/volume year is 2021; the publisher lists publication on 26 November 2022.

[A. Burtscher, M. K.-H. Kiessling and A. S. Tahvildar-Zadeh, Weak second Bianchi identity for static, spherically symmetric spacetimes with timelike singularities (2021)](https://arxiv.org/abs/1901.00813v3). The exact cited vector-test and boundary-flux framework: Definition 2.1, boundary-support footnote and equation 2.5. Published in Classical and Quantum Gravity 38, 185001, DOI 10.1088/1361-6382/ac1853.

[N. Dadhich, S. Kar, S. Mukherjee and M. Visser, R = 0 spacetimes and self-dual Lorentzian wormholes](https://arxiv.org/abs/gr-qc/0109069). The classical metric and tensor in equations 9–15 of the original 2001 arXiv manuscript. Published in Physical Review D 65, 064004 on 7 February 2002, DOI 10.1103/PhysRevD.65.064004.

[H. L. Bray and J. L. Jauregui, A geometric theory of zero area singularities in general relativity](https://arxiv.org/abs/0909.0522v2). The exact cited regular/harmonic ZAS and mass definitions, time-symmetric setting and separate discussion of general spacelike extensions. Published in Asian Journal of Mathematics 17 (2013), 525–559.

## Publication and materials

The manuscript and Zenodo’s declared publication date are 12 October 2026, version 1.0. The record was created and updated on 12 October 2026 UTC. Those metadata timestamps do not establish historical priority.

Authored paper and accompanying materials are CC BY 4.0; third-party works retain their own rights.

Read the complete six-page published research note in the on-page PDF reader.

[Open the complete PDF](regular_zas_bianchi_defect.pdf) · [Download the complete PDF](regular_zas_bianchi_defect.pdf) · [Zenodo original PDF](https://zenodo.org/records/23320818/files/regular_zas_bianchi_defect.pdf)

[Download the complete verification ZIP](regular_zas_bianchi_verification_v1.zip) · [Zenodo original ZIP](https://zenodo.org/records/23320818/files/regular_zas_bianchi_verification_v1.zip)

The complete original ZIP contains the manuscript source, verification companions and preserved available historical inputs. The complete PDF is a separate native asset. The analytic proof establishes the quantified claims; finite exact computations provide supporting consistency and falsification evidence.

## Citation

Alec Kriebel. “A regular zero-area singularity with a nonzero weak Bianchi defect.” Version 1.0, 12 October 2026. Unrefereed research note. DOI: [10.5281/zenodo.23320818](https://doi.org/10.5281/zenodo.23320818).

[Download BibTeX](citation.bib)

```bibtex
@misc{Kriebel2026RegularZASBianchiDefect,
  author = {Kriebel, Alec},
  title = {A regular zero-area singularity with a nonzero weak Bianchi defect},
  year = {2026},
  month = oct,
  day = {12},
  version = {1.0},
  doi = {10.5281/zenodo.23320818},
  url = {https://doi.org/10.5281/zenodo.23320818},
  note = {Unrefereed research note, version 1.0, dated 12 October 2026. Developed with extensive AI assistance.}
}
```

## AI use and publication status

AI tools were used extensively in mathematical development, derivation, writing, coding, literature research and internal adversarial checking, including parallel AI-assisted reviews. This is an unrefereed research note. Internal AI review is not external human or journal peer review; no journal acceptance or formal proof-assistant certification is claimed. The named author is responsible for the claims, materials and citations.

## Substantive collaboration

Substantive collaboration on independent verification of the analytic argument, a meaningful mathematical extension, or development of a journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.
