# Simultaneous nonorientable obstructions: structural reductions

Status: unsolved. Problem 3327 / OPG-172. First newly documented substantive investigation, 12 October 2026; lifetime attempt count unknown. This edition does not assert that no earlier attempts occurred and does not reset any investigation budget.

## Exact target

Find a finite ordinary simple graph G and h ≥ 1 such that G does not embed in the closed nonorientable surface N_(h+1), while every proper minor embeds in N_h. Both edge deletion and edge contraction are required, with isolated-vertex deletion handled explicitly. No connectedness assumption is imposed on the original problem. The invariant ν(G)=min{h≥1:G embeds in N_h} is one on planar graphs and forests; it is distinct from Euler genus E(G).

## Accepted partial results

- The target exists if and only if there is a positive orientably simple Euler-critical ordinary graph or an ordinary positive-Euler-genus hopper. The all-proper-minor condition is essential.
- A suitable non-orientably-simple hopper can be doubled to remove the exceptional orientability correction. This construction is conditional; no suitable hopper is exhibited.
- Every target is triangle-free, has minimum degree at least four, has h ≥ 2, and has at least nine vertices. Triangle augmentation is credited to Campbell (2017); the contraction argument and exact K4,4 certificate provide the additional reductions.
- At h=2, every target is 3-connected, 4-regular, triangle-free and K_(2,3)-free, has at least 12 vertices, and has every edge in two or three squares, with at least one edge in three squares. The 3-connected conclusion uses the credited low-connectivity classification. The mixed two/three-square case has no proved compatible global face selection.
- The exact co-Heawood square certificate rules out an Euler-genus-two embedding of that graph. It does not establish its N_3 embeddability, Euler genus four, or minor-minimality.

No target graph, universal nonexistence proof, novelty claim, or certification of the entire current literature is supplied. Restricting the search to h=2 cannot settle the arbitrary-genus problem.

## Reading order and complete evidence

1. [Structural proofs](STRUCTURAL_REPORT.md), including the equivalence, minimum-degree argument, density and square restrictions.
2. [Independent mathematical audit](INDEPENDENT_AUDIT.md), including corrected conventions and the finite verification boundary.
3. [Bounded source audit](SOURCE_AUDIT.md), identifying the 2024 publications and the exact inspected source scope.
4. [K4,4 embedding proof](K44_N2_PROOF.md) and [complete signed rotation](K44_N2_CERTIFICATE.json).
5. [Complete co-Heawood certificate](COHEAWOOD_SQUARE_CERTIFICATE.json) and [independent checking guide](CERTIFICATE_GUIDE.md).
6. [Integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md), [public source identities](SOURCE_IDENTITIES.json), and [public byte manifest](PUBLIC_MANIFEST.json).

These are authored proofs, audits and small mathematical certificates. No copied third-party source document or executable program is included. The independent audit is a separate mathematical and computational review, not human peer review. Standard genus facts and the cited computer-assisted classifications retain their stated source dependencies.
