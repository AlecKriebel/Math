# Core geodesics in a one-handle compression body

Problem **30001048 / OWR-2089-004**. Edition date: 2026-10-10 UTC.

**UNRESOLVED, Approach 1 of 5.** This is a proof-only checkpoint of an accepted partial reduction. The authored note, mathematical audit, precision ledger, and acceptance report are **AI-assisted and unrefereed**. No proof or disproof of the conjecture, novelty claim, or proof-assistant certification is asserted.

## Exact target

For the compression body obtained by attaching one 1-handle to T² × [0,1], is its specified core tunnel isotopic to a geodesic in every geometrically finite complete hyperbolic structure on the interior? Endpoints run out the rank-two cusp, or move on the cusp torus after truncation. The question is Purcell's Conjecture 2.1 in [Oberwolfach Report 43/2008](https://ems.press/journals/owr/articles/2089), printed pp. 2435–2436.

## Accepted partial mathematics

For the marked discrete faithful group P * ⟨γ⟩, P ≅ Z², normalize γ to g=[[s,−1],[1,0]] and the homotopic core geodesic to the projection of L={(0,t):t>0}.

- An element h=[[a,b],[c,d]] witnesses an interior collision exactly when bc∈(−1,0), with stabilizer and zero-entry exceptions fully treated.
- Peripheral elements, all pγq and pγ⁻¹q with p,q∈P, and every nonzero power of pγ are excluded as witnesses.
- The audit explicitly establishes the rank-two parabolic lattice, full cusp stabilizer, properness from g(0,t)=(s,1/t), and the marking/endpoint interpretation even when γ is accidentally parabolic.
- The conditional path-to-isotopy statement requires a marking-compatible family of proper embeddings throughout the entire parameter interval.

The properness and accidentally parabolic extensions are supplied by the audit, rather than attributed to the loxodromic-generator wording of Lackenby–Purcell Lemma 4.8. The Shimizu–Leutbecher input is credited to Burton–Purcell Lemma 4.3. The Chebyshev level-set proof and all exact illustrative matrices are retained in full.

## Remaining obligations

Arbitrary reduced mixed words are not controlled. Embeddedness alone does not identify the specified core isotopy class. Any future minimally parabolic path proof must justify the full geometrically finite endpoint scope. The displayed loxodromic matrix h₀ is solely an algebraic illustration, not a geometric counterexample. Published multi-handle counterexamples require at least two handles and do not settle this one-handle case.

## Reading order

1. [PROOF_ATTEMPT.md](PROOF_ATTEMPT.md): complete partial proof and exact gaps.
2. [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md): complete mathematical audit and supplied cusp, endpoint, properness, and marking arguments.
3. [CORRECTION_PRECISION_LEDGER.md](CORRECTION_PRECISION_LEDGER.md): incorporated correction and additional audit precisions.
4. [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md): exact accepted and unaccepted scope.
5. [SOURCE_LEDGER.md](SOURCE_LEDGER.md): public citations, PDF identities, retrieval/inspection history, and literature-search limits.
6. [PROVENANCE.md](PROVENANCE.md), [STATUS.json](STATUS.json), and [MANIFEST.json](MANIFEST.json): edition provenance, machine-readable status, and public edition identities.

This edition records the existing first approach; it adds no new proof-search turn. The bounded literature review found no later primary-source resolution, which is not a certification that no such result exists.
