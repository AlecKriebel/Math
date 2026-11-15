# Nonattainment in the Harrell–Stubbe Dirichlet gap inequality

By Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X)

Version 1.0.1, 23 September 2026

Unrefereed preprint; version 1.0.1. Developed with extensive AI assistance; no external human or journal peer review, journal acceptance or formal proof-assistant certification is claimed.

[Read the complete preprint (PDF, 3 pages)](paper.pdf) · [Complete source and verification package (ZIP)](source-and-verification.zip) · [Original checksums](SHA256SUMS.txt) · [Zenodo record](https://doi.org/10.5281/zenodo.22983513) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Original abstract

The universal Harrell–Stubbe bound for a gap between consecutive Dirichlet eigenvalues is never attained on a nonempty bounded open subset of Euclidean space at a finite index. This answers negatively the corrected saturation question recorded in the 2009 Oberwolfach report on low eigenvalues. We prove the stronger statement that Yang’s first inequality is strict at every real threshold above the lowest eigenvalue. The proof uses the classical spectral remainder and a short obstruction to finite spectral support of a coordinate times an eigenfunction. No boundary regularity or connectedness assumption is needed.

## The idea in plain English

For a membrane fixed along its edge, Dirichlet eigenvalues are proportional to squared vibration frequencies. More generally, they describe the Laplacian on a bounded region in any positive dimension.

A classical inequality bounds the gap between consecutive eigenvalues using averages of earlier eigenvalues. This note proves that equality never occurs at a finite index for the Dirichlet Laplacian.

The proof also makes Yang’s first inequality strict at every real threshold above the lowest eigenvalue. It includes disconnected regions, rough boundaries and repeated eigenvalues.

## The precise result

Let n ≥ 1 be an integer and let Ω be any nonempty bounded open subset of Rⁿ. Use the Dirichlet Laplacian defined by the energy form on H₀¹(Ω), and list its eigenvalues 0 < E₁ ≤ E₂ ≤ ⋯ with multiplicity. No boundary regularity or connectedness is assumed.

For every integer J ≥ 1, define A_J = (1/J) Σ_{j=1}^J E_j, B_J = (1/J) Σ_{j=1}^J E_j², M₁ = ((n + 2)/n) A_J and M₂² = ((n + 4)/n) B_J. Then M₁² − M₂² > (E_{J+1} − E_J)²/4. Thus the classical gap bound cannot be attained at any finite index.

More strongly, for every real z > E₁, Σ_{E_j<z} (z − E_j)² < (4/n) Σ_{E_j<z} (z − E_j)E_j. These are finite sums over the eigenvalues strictly below z.

Repeated eigenvalues and zero gaps are included. The proof also covers an index ending inside a repeated eigenspace, including the case E_{J+1} = E₁.

## Why the inequality is strict

The classical commutator trace identity expresses the difference between the two sides of Yang’s inequality as a nonnegative sum over higher spectral modes.

The equality obstruction is short: multiplying a real Dirichlet eigenfunction by a coordinate cannot produce a finite sum of eigenfunctions. If it did, the differentiated eigenvalue equation and self-adjointness would force a derivative vector to vanish, contradicting an integration-by-parts identity. The argument uses the form-defined operator and distributions, so it does not require a smooth boundary.

The high-mode remainder therefore cannot vanish above the lowest eigenvalue. Completing the square in the resulting quadratic inequality then gives the strict gap bound, with multiplicities handled explicitly.

## Scope, normalization and classical background

The theorem concerns the form-defined Dirichlet Laplacian on nonempty bounded open Euclidean sets. Neumann or periodic boundary conditions, unbounded sets and operators with added potentials are different models.

The 2009 Oberwolfach report defines rooted moments M_p but prints M₁² − M₂ in its gap displays. This paper explicitly uses the corrected expression M₁² − M₂², which matches Harrell and Stubbe’s original inequality and scales homogeneously. The negative answer concerns that corrected saturation question.

Finite nonattainment is compatible with sharp leading Weyl asymptotics. It supplies no uniform positive deficit and does not resolve the adjacent quantitative growth question or the separate question about E_J ≤ M_p.

The trace identities and non-strict inequalities are classical and are credited below. The contribution presented here is the explicit nonattainment conclusion and its short equality argument. A bounded source comparison does not certify historical firstness, exhaustive novelty or continued worldwide openness.

Exact algebra and certified box-spectrum checks in the package supplement the analytic proof. They do not machine-prove the theorem for arbitrary domains or provide proof-assistant certification.

## Publication and materials

The manuscript and Zenodo’s declared publication date are 23 September 2026, version 1.0.1. Zenodo created this record on 26 September 2026 UTC and updated it on 10 October 2026. Those record dates do not replace the original edition date or establish historical priority.

The original manuscript, audits, metadata and website prose are CC BY 4.0. Software and website code are MIT licensed. Third-party works retain their own rights; attribution and provenance must be retained.

## AI use and publication status

OpenAI tools were used extensively in mathematical development, derivation, writing, coding, literature research and internal adversarial checking. This is an unrefereed preprint. Internal AI-assisted review is not external human or journal peer review, and no journal acceptance or formal proof-assistant certification is claimed. The named author is responsible for the claims, materials and citations.

## Substantive collaboration

Substantive collaboration on independent verification of the analytic argument, a mathematically meaningful extension, or development of a journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.

## Background and sources

- [E. M. Harrell II and J. Stubbe, On trace identities and universal eigenvalue estimates for some partial differential operators (1997), Proposition 6, printed page 1802](https://doi.org/10.1090/S0002-9947-97-01846-1) — The classical trace framework and squared-moment gap bound. Its free Dirichlet specialization has kinetic parameter σ = 1.
- [M. Levitin and L. Parnovski, Commutators, spectral trace identities, and universal estimates for eigenvalues (2002)](https://doi.org/10.1006/jfan.2001.3913) — A credited classical source on commutator spectral trace identities.
- [E. M. Harrell II and J. Stubbe, Universal bounds and semiclassical estimates for eigenvalues of abstract Schrödinger operators (2010); author preprint arXiv:0808.1133](https://arxiv.org/abs/0808.1133) — The credited general spectral remainder and semiclassical context.
- [Low Eigenvalues of Laplace and Schrödinger Operators, Oberwolfach Reports 6 (2009), printed pages 414–416](https://doi.org/10.4171/OWR/2009/06) — Harrell and Stubbe’s saturation question appears on page 415. The manuscript discloses the missing square there and distinguishes the neighboring questions.
- [M. S. Ashbaugh, The universal eigenvalue bounds of Payne–Pólya–Weinberger, Hile–Protter, and H C Yang (2002), printed page 12](https://doi.org/10.1007/BF02829638) — The historical discussion left strictness of Yang’s first inequality undecided there. This is historical context, not a current worldwide-open-status claim.

## Read the complete paper

Read the complete three-page published preprint in the on-page PDF reader. The reader contains the unchanged full PDF. [Open the PDF](paper.pdf) or [download it](paper.pdf). [Original Zenodo PDF](https://zenodo.org/records/22983513/files/paper.pdf).

[Download the complete original ZIP](source-and-verification.zip) · [Original Zenodo ZIP](https://zenodo.org/records/22983513/files/source-and-verification.zip) · [Original PDF/ZIP SHA-256 checksums](SHA256SUMS.txt) · [Download BibTeX](citation.bib).

## Cite this preprint

```bibtex
@misc{Kriebel2026StrictDirichletGap,
  author = {Kriebel, Alec},
  title = {Nonattainment in the {Harrell--Stubbe} {Dirichlet} gap inequality},
  year = {2026},
  month = sep,
  day = {23},
  version = {1.0.1},
  doi = {10.5281/zenodo.22983513},
  url = {https://doi.org/10.5281/zenodo.22983513},
  note = {Unrefereed preprint, version 1.0.1, dated 23 September 2026. Zenodo record created 26 September 2026 UTC and updated 10 October 2026. Developed with extensive AI assistance.}
}
```
