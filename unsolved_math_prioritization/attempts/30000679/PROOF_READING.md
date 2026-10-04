# Inspection of the existing proof

This is a reading record and dependency check, not an independent proof of the Ealy–Krupiński–Pillay theorem.

The complete rank-two argument was read in arXiv:0706.0486v1, Theorem 3.1, pp.18–25. Relevant background was read in Sections 0–2, including definitions of fsg and thorn rank, genericity, centralizer chain conditions, rank inequalities, and the rank-one argument. The paper's final Section 4 is unnecessary for this target and is not used.

The proof's checkpoints are:

- Initial reduction: centralizer-connected and centerless, after disposing of solvable cases.
- Claims 1–2: rank-one abelian Borels and intersection/normalizer properties.
- Claims 3–6: generic double cosets; relative connectedness and self-normalization in G^00.
- Claim 7: an involution exists in G^00.
- Claims 8–9: products of suitable involutions have finite centralizers; each Borel has finitely many involutions.
- Claims 10–11: elements with finite centralizers have odd order and unique square roots in G^00.
- Claim 12 and the next paragraph: a square-root map yields an involution in each relevant Borel coset.
- Claims 13–14: a conjugacy class of rank one would contain a family forcing rank two, a contradiction.
- Remark 3.3: the finite-index solvable witness is definable.

## Specific logical checks

1. NIP is not being used alone. Corollary 1.8 combines rosiness with NIP to give the centralizer intersection chain condition. Theorem 3.1 requires it also for definable sections. Those sections live in the same rosy imaginary setting. The paper explicitly derives Theorem 2 from these ingredients.
2. “Generic” and “thorn-generic” are different. A full-rank definable set need not be generic by finitely many translates. The proof separately obtains generic double cosets using fsg; the two notions were not silently identified in this application.
3. Claims 10–11 concern the set X of finite-centralizer elements inside G^00. If a∈X, then ⟨a⟩≤C(a) makes its order finite. The odd-order and square-root steps apply to that finite cyclic subgroup. They do not assert odd order or unique square roots for every element of G.
4. A useful algebraic justification at the end of Claim 14 is as follows. If c≠1 and C(c) is finite, put F=C(c). Conjugation embeds N_G(F)/C_G(F) into the finite group Aut(F). Since c∈F, C_G(F)≤C_G(c)=F is finite. Therefore N_G(F) is finite. Infinitely many elements normalizing F are indeed impossible. This check uses no classification theorem.
5. The final transfer to G=G^00 in RESULT.md uses the definable finite-index subgroup explicitly provided by Remark 3.3. An arbitrary nondefinable finite-index subgroup would not justify that transfer by definition alone.

These checks support a credited prior-resolution disposition. They are not a formal verification of the paper or of all foundational results it cites. The computational controls check only finite-group algebra and exact source fingerprints/locators; they cannot prove a theorem about all superrosy groups.
