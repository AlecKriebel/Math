# Off-interval spectral convergence for geometrically consistent discrete dipoles

By [Alec Kriebel](https://orcid.org/0009-0001-9320-500X), independent researcher.

Manuscript and declared publication date: 15 October 2026 · Version 1.0 · Unrefereed preprint

Canonical URL: https://aleckriebel.com/research/off-interval-spectral-convergence-discrete-dipoles/

Search description: Fixed-frequency convergence of zero-diagonal cubic discrete dipoles outside the exact static lattice interval, under convergence of the selected voxels in volume.

[Research home](https://aleckriebel.com/research/) · [Zenodo record](https://zenodo.org/records/23390551) · [DOI](https://doi.org/10.5281/zenodo.23390551) · [CC BY4.0](https://creativecommons.org/licenses/by/4.0/)

## Original abstract

Costabel’s 2022 Oberwolfach report asks for a precise description and proof of the observed approximation of nonreal eigenvalues by the discrete dipole approximation away from a real lattice interval. We give an independent proof for bounded particles whose center-selected cubic voxels converge in volume. This includes every bounded Lipschitz particle, with arbitrary grid translations. At each fixed complex frequency, the actual zero-diagonal matrices have no spectral pollution outside the exact static lattice interval; isolated eigenvalues are approximated with algebraic multiplicity and norm-convergent embedded Riesz projections. The proof combines the established static lattice bound of Costabel–Dauge–Nedaiasl with strong static consistency, Hilbert–Schmidt convergence of the sampled dynamic correction and classical spectral approximation. A separate compact, positive-volume, empty-interior support has a nonreal continuum eigenvalue at frequency 10⁻⁴ while every matrix on the grids n⁻¹ℤ³ is 3 × 3 zero. This example clarifies the geometric hypothesis. The classical ingredients and previously announced dynamic work are explicitly credited; first priority is not certified. AI tools were used extensively, and no external human peer review is asserted.

## The idea in plain English

The discrete dipole approximation replaces a three-dimensional scattering volume by dipoles on a cubic grid. This paper asks when matrix eigenvalues outside a certain real lattice interval track the continuum volume operator as the grid is refined.

The geometric requirement is that the union of cubes whose centers lie in the particle approaches the particle in volume. Bounded Lipschitz particles satisfy it, even when the grid is translated. The actual matrices keep every diagonal block zero.

At each fixed complex frequency, the result gives stable inverses away from the interval and convergence of isolated eigenvalue clusters with their total algebraic multiplicity. A separate irregular compact support shows why arbitrary point-membership sets cannot be included without a geometric qualification.

## The precise result

Let Ω⊂ℝ³ be bounded and measurable, with a chosen representative for deciding center membership. Fix κ∈ℂ throughout the mesh limit. For h>0 choose arbitrary translations a_h, centers x_m=a_h+hm, cells Q_m^h=x_m+h[−1/2,1/2)³ and occupied indices I_h={m∈ℤ³:x_m∈Ω}. Let Ω_h be the union of the occupied cells and assume (G): |Ω_h△Ω|→0.

The matrix is exactly (T_κ^h u)_m=∑_{n∈I_h,n≠m}h³K_κ(x_m−x_n)u_n, with every 3×3 diagonal block zero. Its continuum comparison is S_κ=A_κ−I/3, using the distributional operator and kernel convention in the paper. This shift is part of the statement, rather than a material-contrast conversion.

Let J_lat=cl W(T)=[Λ_−,Λ_+] be the exact closed numerical range of the bounded selfadjoint full static cubic lattice operator. It contains [−1/3,2/3]. Every compact L⊂(ℂ∖J_lat)∩ρ(S_κ) has uniformly bounded discrete inverses for all z∈L and all sufficiently small h. No sequence of matrix eigenvalues can converge to an off-interval point of the continuum resolvent set.

Every continuum spectral point outside J_lat is isolated with finite algebraic multiplicity. For each closed isolating disk whose closure misses J_lat and whose only continuum spectral point is that eigenvalue, the embedded discrete Riesz projections converge in operator norm to the continuum projection. Ranks eventually agree, and enclosed eigenvalues converge with total algebraic multiplicity. Both gap directions for the total generalized spectral subspaces converge, and the matrix norms stay uniformly bounded.

The value-preserving embeddings and continuum projections are extended by zero to the common space L²(ℝ³;ℂ³). The discrete squared norm is h³∑_m|u_m|², making the cell embedding an isometry. An empty occupied set uses the zero-dimensional matrix convention. Bounded sets with boundary of volume zero, including bounded Lipschitz particles, satisfy (G) for arbitrary translations.

Separately, there exists one fixed compact positive-volume support with empty interior for which S_κ has an isolated nonreal eigenvalue at κ=1/10000, while every grid h=1/n, a_h=0 selects only one isolated volume-zero anchor and gives the 3×3 zero matrix. The support is selected at a sufficiently large existential finite index; no effective index or numerical eigenvalue location is claimed.

## Why the result holds

Exact finite radial-shell cancellation, a smooth-core near/far split and uniform whole-space tails establish strong consistency of the static cubic lattice operators. Condition (G) gives strong convergence of the membership masks. The static lattice bound itself is established prior work of Costabel, Dauge and Nedaiasl.

For the actual sampled dynamic correction R_κ=K_κ−K_0, the near-diagonal squared-kernel mass is O(δ+h), including the omitted same-cell block. Uniform continuity away from the diagonal and volume control of the changing masks give Hilbert–Schmidt convergence. No integrated-cell replacement or inserted self interaction is used.

Factoring out the selfadjoint static resolvent turns compact multiplication into norm convergence of the compact family. On isolating contours the analytic static term integrates to zero. Strong convergence of adjoint resolvents, obtained at the conjugate spectral parameter, supplies the remaining left-compact product. Norm-close Riesz projections then give equal finite ranks, total algebraic multiplicity and both subspace gaps.

For the obstruction, the intrinsic ball has exactly three constant-field zero modes for S_0, with spectral gap 1/15. An explicit perturbation estimate gives Im tr H_κ≤−2κ³/3+1446κ⁴=−(7831/15000)κ³<0 at κ=1/10000, forcing at least one nonreal eigenvalue. Rational holes in the closed ball yield nested compact empty-interior supports; continuum mask convergence retains a nonreal cluster on one sufficiently large fixed support. Restoring the isolated null anchor makes every rational-grid matrix zero.

## Scope and limitations

The affirmative theorem requires the specified center-selected cubic voxels, zero diagonal blocks, a fixed complex frequency and (G). The membership representative matters. The theorem does not classify all irregular compact particles or show that (G) is necessary for every spectral question.

No spectral correctness inside J_lat, convergence rate, mesh-dependent-frequency limit, full operator-norm convergence of the singular static operators or full norm-resolvent convergence is asserted. Individual Jordan block sizes, diagonalizability and individual eigenvector convergence are not promised.

J_lat is the exact closed static lattice interval. Numerically suggested endpoint extrema are not substituted for its definition. Contours and compact resolvent sets must stay outside it.

The irregular support in the separate example fails (G). Its support index and nonreal eigenvalue location remain existential. It neither contradicts the Lipschitz-particle theorem nor proves a necessary geometry condition.

Static lattice bounds, earlier DDA consistency, classical compact spectral approximation, continuum pole theory and sphere perturbation are credited prior work. No new general spectral principle, first DDA consistency analysis or new mechanism for nonreal continuum poles is claimed.

The full announced 2022/2023 time-harmonic DDA manuscript and Rahola’s full article remain outside the bounded source coverage. Their possible overlap and historical priority are unverified; no firstness, exhaustive novelty or worldwide current-open claim is made.

The infinite-dimensional conclusions rest on the analytic proof and credited classical foundations. Finite symbolic, rational and numerical controls are supplementary evidence. This is an unrefereed preprint prepared with extensive AI assistance, without independent human or journal peer review or formal proof-assistant certification.

## Status and AI use

AI tools were used extensively in development, derivation, computation, literature research, writing and internal adversarial checking. Internal AI-assisted reviews are not independent human or journal peer review. This is an unrefereed preprint without formal proof-assistant certification. The named author is responsible for its claims, materials and citations.

The manuscript and Zenodo’s declared publication date are 15 October 2026, version 1.0. Zenodo created the record on 15 October 2026 UTC. These edition dates do not establish historical priority.

## Read the paper

Read the complete 11-page paper in the on-page PDF reader.

[Open the PDF](https://aleckriebel.com/research/off-interval-spectral-convergence-discrete-dipoles/dipole_spectrum.pdf) · [Download the PDF](https://aleckriebel.com/research/off-interval-spectral-convergence-discrete-dipoles/dipole_spectrum.pdf) · [Zenodo original PDF](https://zenodo.org/records/23390551/files/dipole_spectrum.pdf)

## Supporting materials

[Complete source and verification materials (ZIP)](https://aleckriebel.com/research/off-interval-spectral-convergence-discrete-dipoles/dipole_spectrum_verification.zip) · [Zenodo original ZIP](https://zenodo.org/records/23390551/files/dipole_spectrum_verification.zip)

## Collaborate on this result

Substantive collaboration on independent verification of the operator limits and spectral argument, a meaningful mathematical extension, or development toward journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.

## Cite this paper

Kriebel, Alec. (2026). Off-interval spectral convergence for geometrically consistent discrete dipoles (Version 1.0, 15 October 2026) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.23390551

[Download BibTeX](https://aleckriebel.com/research/off-interval-spectral-convergence-discrete-dipoles/citation.bib)

```bibtex
@misc{kriebel2026_23390551,
  author = {Kriebel, Alec},
  title = {Off-interval spectral convergence for geometrically consistent discrete dipoles},
  year = {2026},
  month = oct,
  doi = {10.5281/zenodo.23390551},
  url = {https://aleckriebel.com/research/off-interval-spectral-convergence-discrete-dipoles/},
  version = {1.0},
  publisher = {Zenodo},
  note = {Unrefereed preprint; version 1.0, dated 15 October 2026. Zenodo record created 15 October 2026 UTC. Prepared with extensive AI assistance.}
}
```

## Background and prior work

- [Costabel, Stability analysis of the DDA for Dielectric Scattering, OWR43/2022](https://doi.org/10.4171/owr/2022/43): The original contribution, pp2580–2582, records prior dynamic stability and the off-interval eigenvalue-approximation question. It does not state the present volume condition or certify present-day openness.

- [Costabel, Dauge and Nedaiasl, Stability analysis of a simple discretization method for strongly singular integral equations](https://arxiv.org/abs/2302.13159v3): The controlling arXiv v3 supplies the homogeneous-kernel, matrix-valued lattice bound and exact interval framework, including Proposition3.15. Its numerical endpoint discussion is qualified.

- [Yurkin, Maltsev and Hoekstra, Convergence of the discrete dipole approximation. I. Theoretical analysis](https://doi.org/10.1364/JOSAA.23.002578): Prior cubic cancellation and smooth-field DDA consistency/error estimates, with explicit inverse-control assumptions; read together with the 2015 erratum, DOI10.1364/JOSAA.32.002407.

- [Anselone and Palmer, Spectral analysis of collectively compact, strongly convergent operator sequences](https://msp.org/pjm/1968/25-3/pjm-v25-n3-p02-p.pdf): Classical compact spectral approximation. Its compactness hypotheses are substantive, rather than automatic from ordinary strong convergence.

- [Anselone and Treuden, Regular operator approximation theory](https://msp.org/pjm/1985/120-2/pjm-v120-n2-p01-p.pdf): Classical stability and regular-approximation machinery, credited with its required hypotheses.

- [Descloux, Nassif and Rappaz, On spectral approximation. Part1. The problem of convergence](https://www.numdam.org/article/M2AN_1978__12_2_97_0.pdf): Classical spectral-projection, multiplicity and subspace approximation framework.

- [Budko and Samokhin, Spectrum of the volume integral operator of electromagnetic scattering](https://arxiv.org/abs/math-ph/0505013): Prior continuum electromagnetic volume-operator spectral structure and static-plus-compact context.

- [Zhou, Spectral structure of electromagnetic scattering on arbitrarily shaped dielectrics](https://arxiv.org/abs/0911.4540v5): Prior continuum spectral and nonreal-pole theory. The cited edition is arXiv v5.

- [Rahola, On the eigenvalues of the volume integral operator of electromagnetic scattering](https://doi.org/10.1137/S1064827598338962): Historical sphere-spectrum credit is retained. The complete article was unavailable in the bounded review, so its full coverage and priority implications are not narrowed from its abstract.

- [Ammari and Millien, Shape and size dependence of dipolar plasmonic resonance of nanoparticles](https://doi.org/10.1016/j.matpur.2018.12.001): Prior sphere and dipolar perturbation context; the note does not claim a new general radiation or nonreal-pole mechanism.

- [Yurkin and Mishchenko, Volume integral equation for electromagnetic scattering](https://doi.org/10.1103/PhysRevA.97.043824): SectionIX and footnote22 discuss center-value dependence and the associated continuity issue. Geometry sensitivity itself is credited prior work.

