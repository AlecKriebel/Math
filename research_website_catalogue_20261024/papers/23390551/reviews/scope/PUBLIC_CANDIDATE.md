# Off-interval spectral convergence for geometrically consistent discrete dipoles

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)  
15 October 2026 · Version 1.0 · Unrefereed preprint

[Zenodo record and DOI](https://doi.org/10.5281/zenodo.23390551) · [Open PDF](https://zenodo.org/records/23390551/files/dipole_spectrum.pdf) · [Download PDF](https://zenodo.org/records/23390551/files/dipole_spectrum.pdf?download=1) · [Source and verification archive](https://zenodo.org/records/23390551/files/dipole_spectrum_verification.zip)

## Abstract

Costabel’s 2022 Oberwolfach report asks for a precise description and proof of the observed approximation of nonreal eigenvalues by the discrete dipole approximation away from a real lattice interval. We give an independent proof for bounded particles whose center-selected cubic voxels converge in volume. This includes every bounded Lipschitz particle, with arbitrary grid translations. At each fixed complex frequency, the actual zero-diagonal matrices have no spectral pollution outside the exact static lattice interval; isolated eigenvalues are approximated with algebraic multiplicity and norm-convergent embedded Riesz projections. The proof combines the established static lattice bound of Costabel–Dauge–Nedaiasl with strong static consistency, Hilbert–Schmidt convergence of the sampled dynamic correction and classical spectral approximation. A separate compact, positive-volume, empty-interior support has a nonreal continuum eigenvalue at frequency 10⁻⁴ while every matrix on the grids n⁻¹ℤ³ is 3 × 3 zero. This example clarifies the geometric hypothesis. The classical ingredients and previously announced dynamic work are explicitly credited; first priority is not certified. AI tools were used extensively, and no external human peer review is asserted.

## What the paper studies

The discrete dipole approximation replaces a three-dimensional scattering volume with dipoles on a cubic grid. Some matrix eigenvalues collect near a real interval determined by the infinite static lattice. This note studies how eigenvalues outside that interval approximate the continuum volume operator as the grid is refined.

The geometric requirement is concrete: the union of cubes whose centers lie in the particle must approach the particle in volume. Bounded Lipschitz particles meet this condition, including translated grids. The paper compares the actual center-sampled matrices with zero diagonal blocks to the shifted continuum operator Sκ=Aκ−I/3.

## Central result

At each fixed complex frequency, the main theorem states that compact parts of the continuum resolvent set outside the exact static lattice interval have uniformly stable discrete inverses for sufficiently fine meshes. It also states that isolated eigenvalues there are approximated with total algebraic multiplicity, and that the corresponding embedded Riesz projections converge in operator norm. The total generalized spectral subspaces converge in both gap directions.

The proof combines a prior static lattice bound with strong static consistency and Hilbert–Schmidt convergence of the sampled dynamic correction, followed by a classical compact spectral argument.

## Scope and limitations

The result assumes volume convergence of the center-selected cubes. It does not establish spectral correctness inside the lattice interval, a convergence rate, a limit with changing frequency, or preservation of individual Jordan block sizes. The exact lattice interval is used without treating numerical endpoint estimates as proved extrema.

A separate construction gives an irregular compact particle of positive volume and empty interior that is invisible to every rational mesh except for one null anchor. At frequency 1/10000 its continuum operator has a nonreal eigenvalue, while those sampled matrices are 3×3 zero. The support is selected through an existential index. This construction does not contradict convergence for Lipschitz particles or establish a necessary geometric condition.

## Prior work

The motivating question and earlier dynamic stability results are due to Martin Costabel, Monique Dauge and Khadijeh Nedaiasl; see [Oberwolfach Report 43/2022](https://doi.org/10.4171/owr/2022/43). Their [static lattice analysis](https://arxiv.org/abs/2302.13159v3) supplies the lattice interval. Earlier DDA consistency analysis by Yurkin, Maltsev and Hoekstra, classical spectral approximation by Anselone, Palmer, Treuden, Descloux, Nassif and Rappaz, and prior continuum/sphere-spectrum work are credited in the manuscript. The full contents of previously announced time-harmonic work and Rahola's article were not established by the manuscript's source audit, so first priority is not certified.

## Research status and collaboration

This is an unrefereed preprint. AI tools were used extensively in development, derivation, computation, literature research, writing and internal adversarial checking. No external human peer review or proof-assistant certification is asserted.

Independent verification of the operator limits and spectral argument, a substantive mathematical extension, or development of a journal submission would be useful contributions. Authorship should reflect actual scholarly contributions and be discussed in that context.

## Citation

Alec Kriebel. *Off-interval spectral convergence for geometrically consistent discrete dipoles*. Version 1.0, 15 October 2026. Zenodo. https://doi.org/10.5281/zenodo.23390551.
