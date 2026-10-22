# Galois images in the Tautz--Top--Verberkmoes genus-two family

Problem 30001840 / OWR-11127-008. Status: unresolved here, with scoped partial results, after five mathematical approaches. No historical novelty is claimed. This is AI-assisted mathematical reconstruction, not a refereed paper or an independent acceptance report.

## Precise result

Let t be transcendental, C_t:y^2=x^5-5x^3+5x+t, J_t=Jac(C_t), K=Q(sqrt(5)), O=Z[(1+sqrt(5))/2]. The characteristic-zero smooth locus is t != +/-2. The O-action is defined over K; Galois over Q acts nontrivially on it.

- The generic mod-two image is the order-20 affine group AGL_1(F_5) over Q(t), and the order-10 dihedral group over K(t) and geometrically. Generic rational nonzero two-torsion is absent despite the Weierstrass section at infinity.
- The credited Darmon--Mestre residual theorem gives geometric projective A_5 at three. Its full linear inverse image has order 120, index six in SL_2(F_9).
- For every rational prime ell>=7, the generic geometric Tate image is SL_2(O tensor Z_ell). The proof includes the split-prime Goursat step and the full congruence-lifting argument.
- At those primes, the generic arithmetic image over K(t) is the O-linear group with determinant in Z_ell^*, and over Q(t) it is the normalizer of O tensor Z_ell in the polarized symplectic-similitude group.
- Takei's credited invariants show that the geometric moduli image has rational parameter t^2. The smooth rational fiber t=0 has mod-two image C_4, so the generic image is not a uniform fiber image.

## Sharp remaining scope

The original contribution is a broad question and does not specify a rational fiber or one exact maximal target. This packet does not determine the exact integral images at 2,3,5; the full cross-prime adelic image; or the arithmetic Tate images of every rational specialization. It does not classify all geometric or level structures of this curve in the Hilbert modular surface.

Those are gaps of this packet, not claims of global literature novelty or proof that each gap remains open in the literature. In particular Lang--Lang's later index formulas for H_5 make a generic integral-lattice identification a relevant potential route; their theorem is not silently transferred to a Jacobian lattice here. Cadoret--Moonen's open-image theorem does not on its own specify any exact finite-index subgroup for this family.

## Files and review order

1. Read PROOF.md, which contains the mathematical reconstruction and precise dependencies, before looking at finite code or output.
2. TURN_1.md through TURN_5.md and TURN_LEDGER.json preserve the successive mathematical attempts. Retrieval, source inspection, computation reruns, and packaging are not additional turns.
3. SOURCE_MANIFEST.json and SOURCE_AUDIT.md identify public scholarly inputs and exactly what was inspected. DATASET_VERIFICATION.json contains hashes and match metadata only.
4. checks.py and FINITE_CHECKS.json are reproducible finite controls, explicitly not substitutes for universal proofs or integral-lattice identification.
5. SELF_AUDIT.md records checks and limits. MANIFEST.json freezes the source-free packet, excluding itself.

No source PDFs, extracted source text, corpus contents, or private coordination/gate files are included in this directory.
