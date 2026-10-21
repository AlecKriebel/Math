# Conditional hardness of dimension-parameterized zonotope containment

**Credited prior applicability accepted for exact binary-rational input.** Canonical problem 30006105 / OWR-14298804-007; duplicate 30006106 / OWR-14298804-008.

For total binary input length N and ambient dimension d, non-containment is W[1]-hard and containment is co-W[1]-hard. Thus a deterministic dimension-FPT containment algorithm would imply FPT=W[1]. ETH excludes deterministic rho(d) N^o(d) algorithms for either decision direction. These are conditional conclusions in the stated model.

The result is due to **Vincent Froese, Moritz Grillo, Christoph Hertrich, and Moritz Stargalla**, *Parameterized Hardness of Zonotope Containment and Neural Network Verification*, [arXiv:2509.22849v3](https://arxiv.org/abs/2509.22849v3), 3 September 2026, Section 6, Theorem 6.1, p.20. Both the theorem and [Skutella's OWR question](https://ems.press/content/serial-article-files/50767) use the exact convention Z(A)=sum_i[0,a_i]. No independent recentering is allowed.

- [APPLICABILITY_CERTIFICATE.md](APPLICABILITY_CERTIFICATE.md): complete accepted mathematical audit, including the source match, support functions, explicit integer reduction, all homogenization cases, encoding and size bounds, complement logic, and dependency limits.
- [ACCEPTANCE.md](ACCEPTANCE.md): precise accepted scope and the distributed certificate's identity.
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public-source PDF identity, original retrieval/inspection history, version and status.
- [STATUS.json](STATUS.json): conditional disposition and zero new proof-search turns.
- [PROVENANCE.md](PROVENANCE.md): credit and editorial boundary.
- [MANIFEST.json](MANIFEST.json): exact edition membership and file identities.

The v3 p.11 rising piecewise branch has a minus-1/4 typo; the correct plus-1/4 term already appears in the displayed ReLU implementation. The audit preserves and explains that local correction.

Expanded v3 extends a preliminary [ICLR 2026 conference publication](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4db5ca5ff61529e9bebe2089bf466ca8-Abstract-Conference.html); separate journal review of v3 is not verified. The audit is AI-assisted and makes no novelty, human-peer-review or proof-assistant claim. An unrestricted real-RAM lower bound, approximation hardness and an unconditional complexity separation are not asserted.
