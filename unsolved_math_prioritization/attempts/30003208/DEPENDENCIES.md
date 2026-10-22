# Scope and proof dependencies

## Exact objects

A is an arbitrary unital C*-algebra. The state ψ on 𝔄=*_{j≥1}A_j is invariant under every finite permutation. All operators act in its original GNS representation (π,H,ξ). Let

T=⋂_{N≥1}C_N'', with C_N=C*(π_j(A):j>N),
B_N=C*(π_j(A):1≤j≤N), H_N=closure(B_Nξ),
and Q=C*(T∪π(𝔄)).

F:Q→T is the canonical expectation of DKW Theorem 5.1.10. D is the least unital C*-subalgebra of T closed under every alternating F-valued copyword operation in DKW Definition 5.3.1, with arbitrary inserted D-elements and repeated copy indices allowed. It is not defined to be merely the set of first moments.

## Dependency chain

1. Finite-permutation invariance gives the GNS unitaries fixing ξ and the induced concrete automorphisms. This uses invariance of the GNS seminorm, not faithfulness. DKW Definition 5.1.2 provides this framework.
2. DKW Lemma 5.1.9 and Theorem 5.1.10 provide the isometric shift on Q and F(x)=WOT-lim α^k(x). Lemma 5.1.8 and Remark 5.1.11 provide prior coefficient-stabilization technique.
3. A finite partial bijection i↦i+k on the support of a future polynomial extends to a finite permutation fixing all indices at most N. This remains valid with overlapping supports and repeated indices.
4. Consequently P_N F(x)P_N=P_N xP_N for x∈C_N, where P_N projects onto H_N. Contractivity extends the polynomial identity in norm. P_N need not belong to M, commute with T, or reduce C_N.
5. Cyclicity gives P_N→I strongly. This does not require a separable H; the individual H_N may be nonseparable.
6. For t∈T⊂C_N'', exact-radius Kaplansky density provides an x∈C_N within each required finite WOT test, with ||x||≤||t||. Nonselfadjoint inputs use the standard 2×2 selfadjoint reduction. A net is used, not an unjustified sequence.
7. Compression and ||F(x)−t||≤2||t|| extend approximation from H_N to the arbitrary test vectors. This proves bounded WOT density of F(π(𝔄)) in T without passing a weak limit through F.
8. Unitality and the full ordinary-word operations give F(π(𝔄))⊂D by norm density and continuity. The bicommutant theorem then gives T⊂D''⊂T.

[The proof](PROOF.md) supplies the quantitative estimate and all details. [The acceptance](ACCEPTANCE.md) independently reconstructs the argument, including the exact-radius Kaplansky step.

## Conclusions that do not follow

- No normal extension of F to M is produced. Liu's compact-plus-scalar example in DKW Example 5.2.1 satisfies the conclusion despite nonnormality.
- No equality between T and the finite-permutation fixed-point algebra is asserted.
- No general inclusion D⊂π(𝔄) is proved. DKW Proposition 6.7 establishes that separate inclusion in the quantum-symmetric case only.
- Neither equality of F(x) with x nor an operator-algebra conclusion from equality on ξ alone is used.
- There is no claim that only one-letter moments suffice. Quadratic moments are essential even in the displayed nonnormality example.
- No finite computation proves the arbitrary infinite-dimensional theorem. The controls in [the certificate](VERIFICATION.json) test specified mechanisms and reject false shortcuts.

Liu's arXiv:1505.02215v1 Lemma 6.8 is method prior art; the present proof does not depend on reducing its bilateral setting to the exact DKW setting. Source provenance and novelty limits appear in [Sources](SOURCES.md).
