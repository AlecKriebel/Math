# Independent audit: rank-two NIP groups

## Verdict

**Accept as a credited prior resolution of both assertions, with no mathematical blocker.** The appropriate reviewed disposition is `already_solved`, with the recorded investigation count `1/5`. This is an independent automated source-and-argument audit, not a new proof, formal verification, or human peer review.

The frozen author packet was not changed. Its nine-file boundary and all manifest entries were verified. The reviewed manifest has SHA-256 `231dd7a3c9756ab04bf57992a6c869867cd5ce26dc1d82b3ad4b9dda4be3e28f`; RESULT.md has SHA-256 `79327d157683e678863c42de835bf1c5c3239c13310d83b81a7c37e82e1f349d`.

There is one nonblocking publication-status discrepancy: the frozen ATTEMPT_LOG.md suggests `claimed_solved`, whereas this is an existing-literature resolution. A separate publication-status statement should supersede that suggested label with `already_solved`. This does not require changing the frozen mathematics or inventing additional attempts.

## Source scope and identification

The audit used the three hash-bound reference PDFs identified in SOURCE_BINDINGS.json. Their cached text was independently compared with fresh `pdftotext -layout` extraction and matched exactly. The complete rank-two proof, its initial reductions, all fourteen claims, its concluding paragraph and Remark 3.3 were read, together with the necessary definitions and results in Sections 0–2. The original OWR contribution on printed pp.132–133 was read. OWR p.132 and EKP pp.19, 23–25 were additionally inspected visually.

The original source is Krzysztof Krupiński, joint work with Clifton Ealy and Anand Pillay, “Superrosy Groups and Fields with NIP and FSG,” in [Oberwolfach Report 2/2007](https://publications.mfo.de/bitstream/handle/mfo/2988/OWR_2007_02.pdf?isAllowed=y&sequence=1), printed pp.132–133. Conjecture 2 asks for solvable-by-finite; Conjecture 3 adds G=G^00 and asks for solvability. The report explicitly places these questions in its rosy/superrosy setting. The adjacent Proposition 4 is only a partial result and is not used as a complete resolution.

The resolution is Ealy–Krupiński–Pillay, [arXiv:0706.0486v1](https://arxiv.org/abs/0706.0486v1), *Superrosy dependent groups having finitely satisfiable generics*, Theorem 2 (pp.2 and 19), proved through Theorem 3.1 (pp.18–25), together with Remark 3.3 (p.25). The packet gives the journal citation APAL 151(1) (2008), 1–21, DOI [10.1016/j.apal.2007.09.004](https://doi.org/10.1016/j.apal.2007.09.004). The proof audit is anchored to the inspected arXiv bytes, not to an assumption that journal pagination agrees. The Modnet PDF is a second hosted copy of the same work, not a second independent proof.

No network requests or remote writes were made in this audit. Therefore it does not independently certify the author’s earlier repository-search coverage, publisher-page access, or any exhaustive current-literature search. Those ancillary limits do not prevent matching the exact original questions to the inspected affirmative theorem.

## Hypothesis and convention checks

- **Definability and parameters.** EKP p.2 works with a definable group in a sufficiently saturated monster model. Unqualified definability and type-definability allow parameters. The result is not being extended here to arbitrary abstract groups or arbitrary type-definable groups.
- **Rosiness and rank.** The original report’s context is retained. The rank is thorn U-rank, as defined from thorn independence; it is not dp-rank. Definitions 0.10–0.13, Remark 1.20, Proposition 1.22 and the group Lascar inequalities in Proposition 1.27 support the rank steps used in Section 3. The audit does not infer a theorem for arbitrary non-rosy NIP theories from an abbreviated theorem statement.
- **Hereditary fsg.** Definition 0.21 means every parameter-definable subgroup, including G itself, has fsg. Ordinary fsg alone is not substituted. Definable quotients inherit fsg (Remark 0.22); hereditary fsg for a quotient follows by taking the definable preimage of each definable subgroup. This supports the subgroup and quotient reductions.
- **Centralizer chain condition.** Proposition 1.7 and Corollary 1.8 use both rosiness and NIP. Their application to definable sections occurs in the imaginary setting used by the paper. The stronger hypothesis of Theorem 3.1 is therefore available for Theorem 2.
- **Two kinds of genericity.** A full-rank definable set need not be generic under finitely many translates. The proof obtains the relevant generic double cosets using fsg, rather than conflating full thorn rank with ordinary genericity. Fact 0.24 provides the generic ideal and the common stabilizer G^00.
- **Connected components.** Centralizer-connectedness, G^0, and G^00 are not identified. The centralizer-connected component used in reductions is definable of finite index by the chain condition. G^00 can remain type-definable throughout the main proof.

## Complete rank-two proof review

The following records the checks made on the proof, rather than reproducing it.

1. **Initial reductions and Claim 1.** Passing to the centralizer-connected component preserves the relevant hypotheses and finite-index conclusion. An infinite center is disposed of using the rank-one theorem on the remaining quotient. When the center is finite, an element central modulo the center has finite-index centralizer; centralizer-connectedness therefore makes the central quotient centerless. Minimal infinite intersections of centralizers exist and are definable. The rank-one theorem, minimality and rank inequalities give abelian Borels, trivial intersections between distinct Borels, finite-index normalizers, and the unique Borel attached to a nontrivial element with infinite centralizer.
2. **Claim 2.** The two intersection assertions follow from uniqueness in Claim 1 and the finite indices in the normalizers. They concern distinct Borels; no connected-component equivalence is assumed.
3. **Claim 3.** Outside the normalizer, the double-coset multiplication map from B×B is injective and its image has rank two. The definable double-coset equivalence relation has finitely many classes. Extending an ordinary generic type using the fsg generic ideal then gives the required generic double coset. Merely being rank two is not used as a substitute for that last step.
4. **Claim 4.** B^00 is contained in B∩G^00 by bounded index and type-definability. The reverse inclusion is proved using a global generic type and its stabilizer, together with the double-coset injection. The proof does not assume that B^00 is definable.
5. **Claim 5.** A noncentral normalizer element has an infinite conjugacy family in the normalizer. Distinct conjugate normalizers intersect finitely. Applying Lemma 0.15 to this parameterized family gives rank two for the conjugacy class and hence a finite centralizer. Equality of two conjugate normalizers would force their finite-index Borels to meet infinitely and therefore coincide, so the coset parameterization introduces no extra identification problem.
6. **Claim 6.** The extension of the injection to N(B)×B uses Claim 5 and the trivial centralizer intersection of distinct Borels. The generic-stabilizer argument then proves relative self-normalization inside G^00. This is a conclusion of the proof, not an assumption about all definable subgroups.
7. **Claim 7.** The comparison of a double coset with its inverse uses a global generic and compactness over definable neighborhoods of B^00. It produces an element i outside B with i² in B. If i² were nontrivial, uniqueness of the Borel of i² would force i, and hence the original generic element, into N(B). Thus i is an involution in G^00.
8. **Claim 8.** An involution with finite centralizer would give a full-rank involution, contradicting Corollary 2.3 in the centerless centralizer-connected setting. If a product of involutions from distinct Borels had infinite centralizer, both involutions would centralize its Borel by Claim 5, contradicting Claim 2.
9. **Claim 9.** Infinitely many involutions in a Borel, varied over its conjugates, would give the almost-disjoint family required by Lemma 0.15 and produce a full-rank involution. Only finiteness of pairwise intersections is required.
10. **Claim 10.** X consists only of elements of G^00 with finite centralizer. For a in X, its cyclic subgroup lies in its finite centralizer, so a has finite order. A nonidentity power lying outside X would force a into a Borel by relative self-normalization. The absence of finite-centralizer involutions then makes that finite order odd. This makes no odd-order assertion about every element of G.
11. **Claim 11.** Squaring is bijective in the finite odd cyclic group generated by a. Any other square root b has C(b) contained in C(a), hence belongs to X and has odd order. Its square has the same cyclic subgroup, so uniqueness holds even among roots in G^00.
12. **Claim 12 and its consequence.** For x=i·i^g and its unique square root r in the cyclic subgroup generated by x, conjugation by i sends r to its inverse. Thus r·g^-1 centralizes i and lies in B^00. The identity f(bg)=f(g)b^-1 gives surjectivity onto B^00. The subsequent algebra indeed supplies an involution in every B^00-coset in G^00, including the identity coset because B^00 already contains i.
13. **Claim 13.** The chosen nonalgebraic element g has infinite centralizer and is thorn-independent of the nonalgebraic Borel name. Such a choice is available from an infinite Borel component after omitting its finitely many involutions and taking an independent extension. Lemma 0.15 prevents that chosen g from lying in B. Its full conjugacy class has rank one, while its B-conjugacy orbit is infinite.
14. **Claim 14 and final contradiction.** Automorphisms are taken after naming g, so the conjugate Borels preserve the necessary decompositions of that same g. An infinite overlap gives infinitely many products of involutions equal to a fixed nonidentity element c. Claim 9 forces one pair to come from distinct Borels; Claim 8 then makes C(c) finite. Every corresponding involution normalizes C(c), an impossibility: for F=C(c), conjugation embeds N(F)/C_G(F) in the finite group Aut(F), and C_G(F) is contained in C_G(c)=F. Thus N(F) is finite. Lemma 0.15 now forces rank at least two within the rank-one conjugacy class, giving the stated contradiction.

Two harmless typographical slips were checked against the source image on p.23: in Claim 10(i), a^-1 a^n a equals a^n, rather than the printed a; and in Claim 9, if involution means order exactly two, the intersection with the singleton identity is empty, rather than that singleton. The first uses only that an element commutes with its powers; the second uses only finiteness. Neither changes the argument or the frozen result.

## Definable finite-index witness and the second question

Remark 3.3 explicitly supplies a **definable solvable subgroup H of finite index**. This is stronger than merely an abstract finite-index subgroup, and it is the required bridge to the second assertion. The rank-one witness and the reductions above also preserve definability, consistent with that remark.

Since H is definable, it is type-definable, and its finite index is bounded. By the defining minimality of G^00,

G^00 <= H <= G.

If G=G^00, these inclusions give H=G, so G is solvable. No assertion that every abstract finite-index subgroup is definable or contains G^00 is used.

If solvable-by-finite is taken to require a normal solvable subgroup, take the normal core of H. It is the intersection of finitely many conjugates, hence is definable, normal, solvable, and finite-index. This removes the convention issue without strengthening any hypothesis.

## Replay and publication boundary

CONTROL_REPLAY.json records:

- Exact equality with the frozen author’s successful source-and-algebra control output, with exit code 0.
- A source-omitted replay with exit code 2 and `NOT_RUN_MISSING_SOURCES`.
- A deliberately changed source PDF with exit code 1 and `FAIL_SOURCE_HASH`.
- Correct byte counts and SHA-256 digests for every frozen author file.

The 82 finite normalizer checks and 48 dihedral square-root-map checks are finite algebra controls only. They cannot prove the model-theoretic theorem. Likewise, hash and locator checks identify documents and selected statements; they do not certify mathematical correctness. The substantive source-and-argument reading above is separate from those controls.

The audit artifacts contain authored review text, machine-readable findings, replay results, and hashes only. They do not include reference PDFs, extracted source text, screenshots, datasets, or unrelated materials. No frozen file, queue record, branch, commit, or remote repository was modified by this audit.
