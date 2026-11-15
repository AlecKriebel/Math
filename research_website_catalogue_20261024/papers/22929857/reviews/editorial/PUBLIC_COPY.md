# A Lipschitz-nonincreasing deformation of small unitary-valued maps

**Alec Kriebel** · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

23 September 2026 · Version 1.1 · [Zenodo DOI 10.5281/zenodo.22929857](https://doi.org/10.5281/zenodo.22929857)

Unrefereed preprint; version 1.1. Developed with extensive AI assistance; no external human or journal peer review, journal acceptance or formal proof-assistant certification is claimed.

Paper and prose: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: MIT.

## Original abstract

For the unit-round sphere and either the unnormalized Hilbert–Schmidt or operator-norm length metric on U(N), we give an explicit strong deformation retraction of the maps with Lipschitz constant at most 1/2 onto the constant maps. At time t ∈ [0,1], the Lipschitz constant is at most (1 − t²)/(1 + t²) times its original value. The formula depends continuously on the entire map and stays in the original U(N). In particular, it answers the literal question [?24](i) in Gromov's 2017 scalar-curvature problem list, with the stronger requirement that the Lipschitz bound be preserved throughout. The proof uses a classical matrix fractional transformation and an elementary resolvent identity.

## The idea in plain English

A map can assign a unitary matrix to each point of a sphere. A small Lipschitz constant means nearby points receive nearby matrices, measured by a specified intrinsic distance on the unitary group.

This note gives an explicit way to deform every such map with Lipschitz constant at most one half into a constant map. At each time the Lipschitz constant is bounded by a known factor times its original value, so the deformation stays inside the same small-map space.

Choose one point on the sphere. The final constant is the matrix originally assigned to that point. Maps that were already constant remain fixed throughout, and the construction uses the original U(N) without enlarging the matrices.

## The precise result

For every finite n ≥ 2 and N ≥ 1, equip the unit-round sphere S^(n−1) with geodesic distance and U(N) with the induced length metric of either the unnormalized Hilbert–Schmidt norm ||X||HS = sqrt(tr(X*X)) or the operator norm ||X||op. Give the space of maps the uniform topology. Fix p ∈ S^(n−1). For every map Φ with intrinsic Lipschitz constant L ≤ 1/2, put A = Φ(p) and WΦ(x) = A*Φ(x).

For every t ∈ [0,1], Ht(Φ)(x) = A(WΦ(x) + tI)(I + tWΦ(x))^(−1) is well-defined in U(N) and satisfies Lip(Ht(Φ)) ≤ ((1 − t²)/(1 + t²)) L. It starts at Φ when t = 0 and ends at the constant Φ(p) when t = 1.

This is a jointly continuous strong deformation retraction of the closed L ≤ 1/2 sublevel onto the constant maps, and it restricts to one of the strict L < 1/2 sublevel. Every constant map is fixed at every time. Thus the based subspace Φ(p) = I is contractible; the unbased space retracts onto a copy of U(N). The theorem includes nonsmooth Lipschitz inputs.

The same conclusion holds on the two-point sphere S⁰ when its two points are assigned angular distance π. It does not use the disconnected sphere’s intrinsic path metric.

For any topological parameter space Y, a continuous family Φ: Y × S^(n−1) → U(N) whose slices satisfy the bound gives a continuous family of these deformations. For constant Q,R ∈ U(N), Ht(QΦR) = QHt(Φ)R.

## Why the deformation works

After normalizing by the value at p, the sphere’s diameter and the Lipschitz bound place all image eigenangles in the closed interval [−π/2, π/2]. This keeps the fractional transformation’s inverse uniformly well-defined, including at the terminal time.

A resolvent identity gives the same quantitative differential bound for both stated matrix norms, without assuming that the matrices commute. Integrating that bound along the actual image of a shortest sphere geodesic controls intrinsic curve length and proves the Lipschitz estimate, including for nonsmooth maps.

The construction is a classical Cayley-coordinate scaling. The contribution presented here is the explicit quantitative map-space deformation and its estimate for the two specified length metrics; the Cayley transform, logarithm chart and ordinary local contractibility are classical.

## Scope and classical background

The sphere is unit-round, and the target norms are exactly the unnormalized Hilbert–Schmidt norm or operator norm with their induced length metrics. Dividing the Hilbert–Schmidt norm by sqrt(N), changing the source geometry, or specifying only a shortest-geodesic normalization does not give the stated theorem for an arbitrary metric.

A fixed domain basepoint is chosen. The endpoint constant depends on the input map; the construction does not contract the constant-map copy of U(N) to one prescribed point. No nontrivial sphere-fibration, domain-rotation-equivariant or infinite-dimensional result is claimed.

The result addresses the literal small-map assertion in Gromov’s 2017 question [?24](i). The nearby discussion of the larger Lip < 1 bound and the separate sphere-fibration question are different statements. Ordinary deformation for Lip < 1 already follows from a principal logarithm chart without the same sublevel-preservation assertion.

The method’s classical ingredients are credited below. A bounded primary-source comparison does not establish first-publication priority, exhaustive novelty or continued worldwide openness. Exact algebra and numerical diagnostics in the package supplement the analytic proof; finite tests do not prove its all-dimensional or mapping-space assertions.

## Credited prior work

[M. Gromov, 101 Questions, Problems and Conjectures around Scalar Curvature (2017), printed pages 35–36](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf). The original metric context and question [?24](i), asking for deformation of maps with Lip < 1/2 to constants continuously in the input map.

[Y. A. Neretin, Lectures on Gaussian Integral Operators and Classical Groups (2011), §1.7.9, Theorem 7.5, page 42](https://www.mat.univie.ac.at/~neretin/lectures/ems.pdf). The classical Cayley chart for unitary and self-adjoint matrices. The displayed deformation scales that coordinate by (1 − t)/(1 + t).

## Publication and materials

The manuscript and Zenodo’s declared publication date are 23 September 2026, version 1.1. Zenodo created the record on 24 September 2026 UTC and updated its metadata on 10 October 2026. Those dates do not replace the original edition date or establish historical priority.

Paper, LaTeX, research notes, review reports and prose: CC BY 4.0. Python scripts and website code: MIT. Third-party works retain their own rights.

Read the complete four-page published preprint in the on-page PDF reader.

[Open the complete PDF](paper.pdf) · [Download the complete PDF](paper.pdf) · [Zenodo original PDF](https://zenodo.org/records/22929857/files/paper.pdf)

[Download the complete reproducibility ZIP](reproducibility.zip) · [Zenodo original ZIP](https://zenodo.org/records/22929857/files/reproducibility.zip)

The complete ZIP includes the editable manuscript, verification companions and internal AI-assisted review materials. Exact algebra and ordinary numerical diagnostics are supporting checks; the analytic proof carries the theorem.

## Citation

Alec Kriebel. “A Lipschitz-nonincreasing deformation of small unitary-valued maps.” Version 1.1, 23 September 2026. Unrefereed preprint. DOI: [10.5281/zenodo.22929857](https://doi.org/10.5281/zenodo.22929857).

[Download BibTeX](citation.bib)

```bibtex
@misc{Kriebel2026SmallUnitaryDeformation,
  author = {Kriebel, Alec},
  title = {A Lipschitz-nonincreasing deformation of small unitary-valued maps},
  year = {2026},
  month = sep,
  day = {23},
  version = {1.1},
  doi = {10.5281/zenodo.22929857},
  url = {https://doi.org/10.5281/zenodo.22929857},
  note = {Unrefereed preprint, version 1.1, dated 23 September 2026. Zenodo record created 24 September 2026 UTC. Developed with extensive AI assistance.}
}
```

## AI use and publication status

OpenAI tools were used extensively in mathematical development, derivation, writing, coding, literature research and internal adversarial checking. This is an unrefereed preprint. Internal AI-assisted reviews are not external human or journal peer review, and no journal acceptance or formal proof-assistant certification is claimed. The named author is responsible for the claims, materials and citations.

## Substantive collaboration

Substantive collaboration on independent verification, a meaningful mathematical extension, or development of a journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.
