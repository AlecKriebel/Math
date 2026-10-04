# 30002200 / OWR-12172-003: credited prior positive answer

**Proposed disposition: already solved, 0/5 author turns.** The sharp nonfree syzygy bound is realized for every requested torus rank by Matthias Franz's big polygon spaces. This packet verifies the source match and reconstructs the relevant published construction; it is not a new solution or novelty claim.

## Exact question

The complete Franz contribution, “Equivariant cohomology, syzygies and orbit structure,” is on OWR49/2012 pp2954–2956 (report published 7 August 2013). It fixes T=(S¹)^r and rational Borel equivariant cohomology over R=Q[t_1,...,t_r]. For rational Poincaré duality spaces, nonfree equivariant cohomology has syzygy order at most floor((r−1)/2). The text asks whether this is sharp for r>=5.

The original displays on pp2955–2956 contain an undeclared n; the surrounding torus-rank notation is r. This is not interpreted as the manifold dimension. The primary Allday–Franz–Puppe Corollary1.4 and Proposition5.12 explicitly use r/2, resolving that typographical mismatch. The “mild” topological hypotheses are recovered from their Sections3.1,3.2 and Assumption4.1. They are satisfied by the compact smooth algebraic examples below, including their orbit skeletons.

The requested numeric UnsolvedMath page failed direct retrieval. Its pinned record was checked against these primary pages, including visual inspection of pp2955–2956. No additional free-action, almost-free-action, fixed dimension, integral-coefficient or positive-characteristic requirement appears in the question.

## Prior answer and every rank

Use Franz, *Big polygon spaces*, IMRN2015, 13379–13405, DOI10.1093/imrn/rnv090. The checked author version is arXiv:1403.4485v4 (12June2023), which corrects degree shifts in Proposition5.1. Its characteristic-zero convention includes Q.

Set a=b=1. For odd r=2m+1 take the equal length vector (1,...,1); for even r=2m+2 take (0,1,...,1). In both cases define

    X(ell)={ (u,z) in (C×C)^r :
             |u_j|²+|z_j|²=1 for every j,
             sum_j ell_j u_j=0 }.

T acts by coordinatewise multiplication on z. These are compact connected orientable smooth manifolds of dimension 3r−2. Proposition5.1 and Corollary5.3 give syzygy order exactly m=floor((r−1)/2), so the module is nonfree and attains the bound. The even example is S³ times the odd example with the additional circle acting on its sphere factor.

The relevant construction and proof chain, including its algebraic and geometric checks, is recorded in CREDITED_PROOF_GUIDE.md. The later Franz–Huang paper in AGT20(2020),2657–2675, Theorem1.2, determines the order for all generic length vectors and corroborates these cases. Its introduction uses real coefficients, but Section2 explicitly permits every characteristic-zero field. No coefficient-extension inference is needed for the rational result.

## Scope of this gate

The supplied dated “open” triage is superseded by this direct primary answer. Current literature and repository checks are bounded, not an exhaustive novelty certification. Minimal possible dimension for realizing maximal syzygy order is a different question and is not resolved here. No new author proof turn was opened: source retrieval, verification, reconstruction, finite controls and packaging remain at zero turns.

Primary links:
- https://ems.press/journals/owr/articles/12172
- https://arxiv.org/pdf/1111.0957v2
- https://arxiv.org/pdf/1403.4485v4
- https://doi.org/10.1093/imrn/rnv090
- https://msp.org/agt/2020/20-5/agt-v20-n5-p12-s.pdf
