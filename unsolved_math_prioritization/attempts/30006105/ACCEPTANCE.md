# Scoped acceptance: dimension-parameterized zonotope containment

Canonical problem **30006105 / OWR-14298804-007**, with duplicate **30006106 / OWR-14298804-008**. Mathematical applicability audit: 10 October 2026 UTC.

**Verdict: accepted as a credited conditional negative answer for exact binary-rational input.** This acceptance concerns the mathematical applicability audit in [APPLICABILITY_CERTIFICATE.md](APPLICABILITY_CERTIFICATE.md). It does not present a new hardness result, a new independent audit, an unconditional complexity separation, or a resolution in an unrestricted real-RAM model.

## Exact distributed certificate

- APPLICABILITY_CERTIFICATE.md: 16494 bytes; SHA-256 `f7c51dd30aa421d7cc4e60cae58cb5c32283843eaac468a97487ad4bfc8b594c`.

The complete substantive mathematical content of the accepted certificate is preserved byte for byte. [PROVENANCE.md](PROVENANCE.md) states the editorial boundary. This acceptance binds the distributed edition identified above; later substantive mathematical edits need their own review.

## Accepted conclusion and credit

For generator matrices defining Z(A)=sum_i[0,a_i], with signed binary-rational entries and total binary input length N, the dimension-d non-containment language is W[1]-hard and the containment language is co-W[1]-hard. Therefore a deterministic f(d) N^O(1) containment algorithm would imply FPT=W[1]. Under ETH, neither exact decision direction has a deterministic rho(d) N^o(d) algorithm. These are conditional exclusions; no completeness claim is made.

The result is credited to **Vincent Froese, Moritz Grillo, Christoph Hertrich, and Moritz Stargalla**, *Parameterized Hardness of Zonotope Containment and Neural Network Verification*, [arXiv:2509.22849v3](https://arxiv.org/abs/2509.22849v3), 3 September 2026, Section 6, Theorem 6.1, p.20. The inspected expanded manuscript describes itself as extending a preliminary [ICLR 2026 conference publication](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4db5ca5ff61529e9bebe2089bf466ca8-Abstract-Conference.html). Separate journal review of v3 is not verified.

The target is Martin Skutella's question in [Oberwolfach Report 50/2024](https://ems.press/content/serial-article-files/50767), printed pp.2988–2989, PDF pp.40–41. Both sources use segments [0,a_i]. The original question suppresses entry encoding; this acceptance states the rigorous binary-rational specialization and does not silently infer a unit-cost arbitrary-real lower bound.

## Accepted mathematical scope

The certificate proves and retains:

1. The exact support-function formula and both directions of the containment equivalence, including the strict positive witness, lower-dimensional cases, signs, and absorption of rational output coefficients by their absolute magnitudes.
2. The translation identity, the requirement to retain the difference of centers, and the one-dimensional counterexample to independent recentering.
3. The prior's Multicolored Clique triangle-gadget reconstruction, its Sidon-label dependencies, disjoint-support arguments, positive-point equivalence, and all threshold and scale choices.
4. The explicit integer generator columns in dimension d=k+1, with n+m=3(q+e)+2; the positive, zero, and negative homogenizing-coordinate cases; and the absence of spurious witnesses.
5. Equal centers and full-dimensionality of the constructed nontrivial instances, without imposing those as hidden target assumptions.
6. O(log(q+1)) entry bit-length, N=O((k+1)(q+e) log(q+1))=O(q^3 log(q+1)), fixed-degree polynomial construction, and preservation of the ETH exponent scale.
7. Complement closure of deterministic FPT and of the stated running-time bound, giving co-W[1]-hardness for containment from W[1]-hardness for non-containment.

The source's v3 p.11 rising branch prints minus 1/4 where plus 1/4 is required. The displayed ReLU implementation on the same page already has the correct plus sign. The certificate follows that implementation and explains why this is a local nonblocking exposition typo, not a gap in the specified reduction.

## Dependency and assurance boundary

The external foundations remain standard Multicolored Clique W[1]-hardness and its ETH consequence, and the cited polynomial-time greedy Sidon construction with labels O(q^3). Their underlying theories and original literature are not independently re-proved. No approximation hardness, unrestricted real-RAM lower bound, W[1]-completeness, or co-W[1]-completeness is inferred.

This is an AI-assisted mathematical applicability audit. No original discovery, external human peer review, proof-assistant certification, or exhaustive present-day literature certification is asserted. It reconstructs an existing credited result and adds **zero new substantive proof-search turns**; it does not reset any historical accounting. Source and edition checksums establish identity, not mathematical truth.
