# Provenance and reproducibility

## Inherited material

The starting package contained an exact quartic-field K3P collision, a short paper draft, a technical summary, a JSON certificate, and a dependency-free verifier. The inherited core data were the rooted theta-network topology, the vectors `K,U,V,S,T`, the comparison-tree vectors `alpha,beta,gamma`, the relation `5h^4=1`, and the factorization `M[y,z]=P[y+z]B[y]B[z].` The original package was preserved unchanged outside this directory.

## Calculations rerun independently

The revised package reconstructs and checks the following from definitions rather than importing the inherited outputs:

- rooted acyclicity and binary vertex types;
- suppression of the degree-two root and composition of the two `K` edges;
- the theta core, three incident leaf components, and strict level two;
- every edge eigenvalue and inverse-Fourier transition probability;
- all four displayed-tree contributions;
- all sixteen core factorization identities;
- all sixty-four network and tree Fourier coordinates;
- all sixty-four inverse-Fourier leaf-pattern probabilities, positivity, and normalization;
- the complete selected 15x15 Jacobian matrix and its determinant;
- the continuous-time rate inequalities, exact fixed-output tangent identity, and positive derivatives of the formerly saturated margins.

The main verifier uses exact arithmetic in the quartic number field `Q(h)`, represented in the basis `1,h,h^2,h^3`, with rational coefficients and rational interval sign bounds from `2/3<h<7/10`. It uses only the Python standard library and reads `certificate.json`; it does not import the certificate-generation code or the LaTeX sources.

## New claims added in this revision

Two claims were added after independent exact audit:

1. the fixed theta-trinet K3P map has rank fifteen at the collision and is locally surjective in the 15-dimensional affine space of consistent three-leaf group-based Fourier coordinates with `q_AAA=1`;
2. the same fixed tree distribution has a nearby theta-network preimage in which every edge has three strictly positive continuous-time K3P substitution rates.

The semi-directed root-suppression formulation, the effective `K odot K` edge, the corrected continuous-time interpretation of the closed-form witness, and the convention-independent topology statement are also new to the revised exposition.

## Software and files

- Python 3 standard library: exact certificate generation and final independent verification.
- SymPy: optional, separate symbolic audits of the Jacobian and fixed-output tangent identity in `src/`; not needed by `verify.py`.
- pdfLaTeX and TikZ: document and figure production.
- Standard SHA-256 utilities: distribution manifest.

The complete verifier transcript is stored in `verification_report.txt`. The archive was unpacked into a fresh directory and `python3 verify.py` was rerun there before release.

## AI-assisted work

AI-assisted mathematical and editorial tools were used in discovery, algebraic checking, software drafting, and exposition. The package does not treat model output as evidence. Every computationally derived identity, stochastic inequality, and determinant used in the paper is reduced to explicit exact checks. The continuous-time extension is then deduced from the standard real-analytic implicit-function theorem after exact verification of the invertible Jacobian, fixed-output tangent identity, strict slack, and margin signs. No hidden reasoning transcript or internal work instructions are included.

## Literature and priority scope

A narrow post-discovery search was performed for the exact strict level-two theta topology, the quartic relation `5h^4=1`, the displayed factorization, three-leaf K3P tree/network collisions, and full-dimensional overlap for this topology. No exact match was found. This was not an exhaustive historical search, so the paper makes no absolute priority claim and requests an expert literature audit.
