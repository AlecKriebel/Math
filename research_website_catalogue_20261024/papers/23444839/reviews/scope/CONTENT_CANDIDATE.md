# Conditional page content — not approved for publication

Use only after the independent mathematical reviews clear this exact edition. This file is a draft content candidate, not a website change or a mathematical verdict.

## Proposed metadata

- Slug: `nevo-homology-sphere-decomposition`
- Page title: `Nevo’s homology-sphere decomposition question | Alec Kriebel`
- H1: `A negative answer to Nevo’s homology-sphere decomposition question`
- Description: `A finite two-dimensional complex is doubly Cohen–Macaulay in characteristic zero yet contains no homology-sphere subcomplex over any field.`
- Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X
- Published: 17 October 2026; version 1.0.0
- Status: Preprint · unrefereed
- Source: https://doi.org/10.5281/zenodo.23444839
- Keywords, used naturally: homology sphere; doubly Cohen–Macaulay complex; Nevo’s decomposition question; affine building; simplicial complex.
- Follow-up section: omit; `follow_up = null`.

## Proposed introduction

Eran Nevo asked whether every doubly Cohen–Macaulay simplicial complex could be assembled from homology spheres with specified overlaps. This paper gives a two-dimensional counterexample. It satisfies the required homology conditions even after any one vertex is removed, yet it contains no permitted sphere piece at all.

The example is doubly Cohen–Macaulay over every field of characteristic zero. The exclusion of homology-sphere subcomplexes holds over every field. Here, “homology sphere” includes the usual conditions on every face link, not just the homology of the whole complex.

## Proposed plain-language discussion

A simplicial complex is a shape described by vertices, edges, triangles and their higher-dimensional counterparts. The example here uses only vertices, edges and triangles. The Cohen–Macaulay conditions control its homology both globally and around each face; “doubly” adds the requirement that the conditions survive deleting any single vertex without lowering the dimension.

The surprising part is how strongly the sphere decomposition fails. The obstacle is not finding a clever order in which to join the pieces. There is no homology-sphere piece to start with.

The construction uses a finite quotient of an affine building. Every vertex has the same local pattern, given by point–line incidence in the projective plane of order eleven. Spectral estimates show that the necessary homology vanishing survives each vertex deletion. A short counting argument then rules out sphere subcomplexes: their local patterns would force an Euler characteristic at most zero, whereas a two-dimensional homology sphere has Euler characteristic two.

The building construction, congruence method, spectral criterion and curvature obstruction have established precedents. The paper brings these tools together for the specific decomposition question and checks the vertex-deletion requirements.

## Proposed scope note

The theorem concerns subcomplexes of the given finite complex. It does not claim the same Cohen–Macaulay conclusion in every positive characteristic, and it does not address spheres that might arise after changing or subdividing the complex. The paper is an unrefereed preprint developed with extensive AI assistance. Its publication date records this version; no claim of established firstness is made.

## Proposed paper and source links

- [Read the paper](https://zenodo.org/api/records/23444839/files/spherefree-doubly-cm.pdf/content)
- [Zenodo record and citation](https://zenodo.org/records/23444839)
- [Source and verification archive](https://zenodo.org/api/records/23444839/files/spherefree-doubly-cm-source-and-verification.zip/content)

Use the Zenodo PDF for the existing page template’s embedded reader, subject to the site’s usual rendering check. The exact complete abstract is in `abstract_original.txt`; do not replace it with the introduction above. No iframe compatibility test or website edit was performed in this scope.

## Proposed collaboration invitation

I welcome careful mathematical feedback from researchers in combinatorial topology, Cohen–Macaulay complexes and buildings. I would be particularly interested in collaborating on a substantive independent verification or a journal-ready development of the result. Any authorship would reflect the contributions made.

This is proposed public-page wording only. No outreach has been prepared or initiated.
