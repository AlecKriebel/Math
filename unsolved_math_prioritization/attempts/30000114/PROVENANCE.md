# Provenance and editorial boundary

## Mathematical scope and attribution

Problem 30000114, rank 1217, source alias OWR-741-008, asks for a fixed-dimension bound with both leading intrinsic-volume coefficients exactly 1. The unrestricted question remains unresolved by this work. The outcome is accepted rigorous restricted progress, Approach 1 of the five-approach budget.

The slicing argument uses the established general-lattice surface estimate of [Henk and Wills](https://arxiv.org/abs/0705.2088v1), Blichfeldt's lattice-point bound and the classical flatness theorem, with the flatness input checked in [Banaszczyk, Litvak, Pajor and Szarek](https://www.math.ualberta.ca/~alexandr/papers/wwBLPS2503.pdf). The prior Ehrhart and asymptotic results of [Betke and Böröczky](https://doi.org/10.4153/CJM-1999-012-9) are credited and their scope limits retained. No historical novelty, exhaustive literature coverage or complete solution is claimed.

The proof note and independent audit are AI-assisted and unrefereed. The audit's acceptance is not external human peer review or proof-assistant certification.

## Exact distributed reports

- APPROACH1.md: 15614 bytes; SHA-256 `ecc9d520fd579549e8ee6bf095dc3044de6312fdb0f98497e89e5a582b3e27f9`.
- AUDIT.md: 12418 bytes; SHA-256 `7245d1f210eb4c7998c766d846540e4bf8f6b5ebb900deb60e45c36dbf951c49`.

The full mathematical proof in Sections 1-6 is preserved verbatim. The mathematical audit, accepted scope, boundary cases, precision repairs, source applicability and final unresolved disposition are preserved verbatim. Editorial changes do not introduce a new mathematical correction.

The retained mathematics includes the complete lattice-hull reduction; induced-lattice determinant checks; lower-rank slice estimates; endpoint-aware quadrature; the sharper surface coefficient for degenerate bodies; the flatness-to-hollow-body passage; the exact large-width necessary condition; every Ehrhart and height-one-pyramid formula; the surface-deficit compensation; and the exact unimodular-shear example separating large lattice width from large Euclidean inradius.

## Editorial changes and publication boundary

The proof's final verification-and-administration section and the audit's finite-verification paragraph are removed in full. References to nondistributed input identities and administrative material are removed or adapted. The audit's final heading is adjusted and its mathematical precision repairs are retained. The source ledger retains public bibliographic details, public PDF hashes and sizes, and retrieval/inspection history while removing local artifact paths. No omitted computation is converted into replacement prose.

Exactly seven files are distributed. No third-party source documents, source extracts, source images, datasets, scripts, computation outputs, logs or private coordination material are included. Hashes in the edition identify only its distributed files or the six cited public PDFs. The manifest lists the seven distributed members and binds the six non-manifest members; the pull-request body independently pins the manifest.

## Accepted result and remaining gap

For every n>=2, a dimension-only A_n bounds every compact convex K and every primitive integer normal a by

    G(K) <= V_n(K) + V_(n-1)(K)/||a||
            + A_n (floor(w_a(K))+1) sum_(i=0)^(n-2) V_i(K).

Consequently each fixed bounded-lattice-width class and the hollow-body class satisfy the requested form, and all lower-dimensional lattice hulls are controlled. Any sequence with divergent normalized target residual must have lattice width tending to infinity. Its Euclidean inradius need not tend to infinity. The pyramid example disproves only an auxiliary coefficientwise Ehrhart bound; its surface deficit compensates the large lower coefficient.

The remaining gap is a shape-uniform lower-Ehrhart-sum bound in each fixed dimension over full-dimensional lattice polytopes of unbounded lattice width, retaining Delta(P)=V_(n-1)(P)-g_(n-1)(P). This edition changes no queue entry or historical accounting and adds no proof-search approach.
