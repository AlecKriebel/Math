# Categorical phase-free invariants: scope clarification

This separate addendum accompanies the unchanged eleven-file author freeze and the [full independent audit](audit/INDEPENDENT_AUDIT.md). The accepted disposition is **partial analysis, unsolved after five approaches**. The frozen author-stage references to a pending audit are historical; the separate audit passes only that partial/unsolved disposition.

Two different categorical results must not be conflated.

1. **Geer–Kashaev–Turaev**, *Tetrahedral forms in monoidal categories and 3-manifold invariants*, [arXiv:1008.3103v2](https://arxiv.org/abs/1008.3103v2), Theorems 29 and 50. The first theorem permits powers of a scalar anomaly. In its Borel example that scalar is

       q̃ = (−1)^((N−1)/2) ζ^(−(N²−1)/8),    ζ=exp(2πi/N).

   For odd N>1, this scalar has order N when N≡1 modulo 4 and order 2N when N≡3 modulo 4. The categorical construction in this example is therefore not a theorem selecting an exact phase. The independent audit checks the order formula and its source scope.

2. **Geer–Patureau-Mirand**, *Topological invariants from non-restricted quantum groups*, [arXiv:1009.4120v3](https://arxiv.org/abs/1009.4120v3), §3.6, Theorems 20–21. For the Ψ-system obtained from the specified relative G-spherical category and its basic data, the relevant operator q is the identity. Its generalized Kashaev invariant equals the modified Turaev–Viro invariant and loses the charge-class ambiguity. This is a genuine phase-free result under those hypotheses.

The latter theorem does not, by itself, identify its scalar with the original B-valued Baseilhac–Benedetti state sum H(T_N), including the original cocycle-edge normalization, or prove that its Nth power equals the original K_N(W,L,ρ). Establishing that comparison is a separate requirement for Problem 7.21. Accordingly, references in this package to retained phase ambiguities concern the specified BB families, not every related categorical invariant. No general nonexistence of phase-free invariants is claimed.

The complete source discussion, normalization warning, mathematical review, and reproducible controls are preserved in the accompanying audit. This addendum introduces no new solution or novelty claim and changes none of the frozen author proofs.
