# Independent audit of nonabelian torsors and parabolic bundles

Problem 30003771, OWR-16158-014, rank 871. Review date: 2026-10-06 UTC.

## Verdict and exact scope

**Accept the corrected packet as a bounded, unresolved partial audit with a verified prior local obstruction. Reject any designation as a full solution, a global counterexample, or a new obstruction theorem.** Both authored elementary proofs are valid. Two source-precision qualifications have been added in a separate derivative: the final paper's corrected joint-weight definition, and its correction from representability to faithfulness for maps into nonalgebraic fundamental gerbes. Neither changes the mathematical outcome or the count of two approaches out of five.

The original author archive remains unchanged: 8,319 bytes, SHA-256 d55c2141a1d6d85aa159ea425bd928fac155f0cf8942fb89051ea51e6db29664. The reviewed derivative is NONABELIAN_TORSORS_30003771_CORRECTED_SAFE.zip: 9,243 bytes, SHA-256 01ba8bd5104b12ea8a8cb7d8adc93dbeb56176af24c527fbdd3e27aeda63df65.

This review concerns the two existing approaches and their dependencies. It does not introduce a third solution approach, independently classify all possible nonabelian torsors, or establish the absence of later results. All checks of mathematical statements below are deductive or source-based. File hashing, JSON parsing, and archive inspection establish identity and packaging only; they are not computer proofs.

## 1. Input identity and the prior-attempt gate

The supplied archive was pinned before extraction. Its exact five-member allowlist, byte counts, SHA-256 values, regular-file types, and ZIP CRCs agree with the external manifest. Its members are APPROACHES.md, CITATIONS.md, MATHEMATICAL_AUDIT.md, STATUS.md, and VERIFICATION_METADATA.json. There are no executable mathematical checkers.

Each complete supplied dataset was read and hashed, rather than hashing a selected excerpt. The resulting metadata is:

- Catalog: 21,735,099 bytes; SHA-256 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566.
- Problems: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- Research results: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b.
- Statement UTF-8 hash: 01c8cfd399a2216489f461d95492a0be09ec41baa07cb5369af76fb3c52d47ed.
- Complete problem/report pair: 58de3fba4f0a9abc76d946d05c9188131062caf0123ee21fd43e63aebd085580, using default json.dumps([full_problem, reports.get(problem_number,{})], sort_keys=True).encode().

The selected catalog entry and complete problem agree on ID, number, title, rank, and fingerprints. The report lookup is the empty object. That is an absence of an inherited report in this supplied corpus, not evidence that no mathematician or repository branch has considered the problem. The catalog suggestion is preliminary triage, not an inherited proof attempt. The author's historical indexed GitHub-search claims are retained as bounded historical search metadata; this independent audit did not rerun those searches and does not certify exhaustive repository-history absence.

## 2. Original question and necessary source correction

The OWR contribution by Niels Borne, joint work with Indranil Biswas, occupies printed pages 1069–1071 of Report 17/2018 [S1]. The report states an existence equivalence with G allowed to vary. The base X is proper, finite type, geometrically connected, and geometrically reduced over k; D is a simple normal-crossings divisor, and its components carry positive integer indices. A rational point is not assumed. The workshop dates are 15–21 April 2018.

On the cover side, Y is a scheme with a G-action and a finite flat invariant map to X. At every closed point, after a field extension and an fppf neighborhood of the coarse base, the map must be induced from the corresponding Kummer cover along a monomorphism from the full product of local roots-of-unity group schemes into G. On the other side, the abelian theorem requires all allowed local weights to occur in essentially finite parabolic bundles with abelian monodromy. The proposed extension removes the abelian restriction on both sides. It is not a bijection between a single vector bundle and an individual torsor for a prescribed G.

**Weight-definition repair.** The 2018 report tests a simultaneous diagonal step of the multi-index. The final manuscript instead uses the sum of the coordinate-step images, and Definition 2.5 footnote 1 explicitly credits Ahlqvist with correcting the earlier definition [S2]. The distinction matters at intersections: a nonzero cokernel of one simultaneous step does not imply a nonzero cokernel after summing all individual-step images. The reviewed mathematics uses the corrected joint-weight definition. The derivative now says so explicitly, rather than describing that corrected convention as the literal formula printed in 2018.

The original local Kummer requirement and the proper-base existential quantifiers are preserved. This source correction is not a replacement of the open problem with unrestricted stack uniformization.

## 3. Root-stack reduction and its precise endpoint

Let S be the root stack of (X,D,r). At a closed point on components indexed by J, its residual gerbe is noncanonically neutral and banded by H = product over j in J of mu_(r_j). Characters are indexed by the entire product of the cyclic character groups. They are not independently chosen one-divisor weight lists.

The character argument in the author packet is correct. A representation of a diagonalizable group is a character-graded vector space, including in characteristic dividing some r_j. This statement concerns comodules of the group scheme; it does not identify the group scheme with the abstract group of its geometric points. Graded subobjects and quotients cannot introduce a missing character. Conversely, if each character occurs in the restriction of some essentially finite bundle, finitely many such bundles, repeated as necessary, supply all multiplicities in any given representation. Direct sums stay essentially finite under the stated Tannakian hypotheses.

Biswas–Borne's earlier uniformization theorem [S3, Theorem 4.11 and Proposition 4.5] is already nonabelian. Its residual-representation criterion yields a finite-group-scheme torsor over S with algebraic-space total space. Properness, finite type, finite inertia, geometric connectedness and geometric reducedness of the root stack are established in the final torsor paper's proof of Theorem 2.8; the latter two give inflexibility, and properness gives the required pseudo-proper setting [S2, Section 4]. Thus these are available dependencies under the source hypotheses, rather than missing new conjectures. For a root stack over a scheme, the uniformizing total space is a scheme, as noted in [S2, Remark 3.6(2)].

The finite-flat aspect must also be separated from the missing local model. Locally the Kummer algebra is free over the base, with its standard monomial basis. Root-stack projection is flat, as can be checked after the faithfully flat Kummer chart. A finite-group-scheme torsor is finite flat over the stack. The resulting scheme cover of X is flat; its finite nature is the conclusion used in Remark 3.6(2). Flatness alone does not produce an isomorphism with the required induced Kummer model.

**Dependency repair.** The earlier paper uses representability terminology for morphisms to the generally nonalgebraic Nori gerbe. The final paper explicitly corrects this in Remark 3.21: use faithfulness, meaning injectivity on automorphism sheaves, when the target fundamental gerbe is nonalgebraic. Lemma 3.20 passes to a finite algebraic gerbe stage, where representability is appropriate. The character criterion and nonabelian uniformization endpoint remain valid with this qualification. The derivative now carries that warning.

To reconstruct a torsor for a fixed G, one needs the whole exact strong symmetric monoidal functor from Rep_k(G), with its coherence and unit data. An essentially finite object or an unstructured list of character spaces does not substitute for it. Likewise, no rational basepoint or neutralization of the global fundamental gerbe may be inserted without justification.

## 4. What the published obstruction actually disproves

The complete 18-page final arXiv manuscript was read, including both appendices and the published corrections to earlier dependencies. Remark 2.9(3) expresses doubt about the unrestricted theorem with the existing torsor definition; it does not announce a proved proper-base counterexample. Proposition 3.13 proves extension of an isomorphism on a closed residual gerbe to an fppf neighborhood of the coarse point for abelian G. Remark 3.14 and Appendix B give Rydh's counterexamples to the nonabelian version of that local proposition [S2].

The exact failure point in the abelian proof is identifiable. For abelian G, the isomorphism sheaf of two G-torsors is itself a G-torsor. In the nonabelian setting it is naturally a torsor under a twisted inner form, and the required descent statement cannot simply be reused. Proposition 3.15, which concerns a torsor that is trivial on a residual gerbe, does not by itself imply Proposition 3.13 for arbitrary G.

The first family has positive characteristic p, root index p, and G = alpha_p semidirect mu_p. The second has odd characteristic, root index two, and G = mu_p semidirect C_2, with C_2 acting by inversion. Both structure groups are finite, flat over the field, nonreduced, and nonconstant; both are genuinely nonabelian as group schemes. Testing only their geometric points would lose the nonreduced part. The second root stack is Deligne–Mumford, with prime-to-characteristic inertia. It still has a nonétale structure group.

The counterexamples are therefore not removed by requiring the root denominator to be prime to p or by requiring the root stack to be tame. In fact, the second structure group is itself linearly reductive: taking invariants first by diagonalizable mu_p and then by C_2 is exact when p is odd. This additional observation follows from the displayed semidirect product and exactness of those two invariant functors; it is not a new counterexample construction. Neither family is an example for finite étale G or in characteristic zero.

## 5. Independent check of the first authored lemma

Let R = k[u,v] localized at (u,v), where char(k)=p>0. For a faithfully flat R-algebra B, extension and contraction preserve the ideal (u). Equivalently, faithful flatness gives an injection R/(u) into B/uB. Since R/(u) is k[v] localized at (v), the class of v is nonzero. Hence v is not in uB, and a fortiori cannot equal u b^p for any b in B. Its closed-point specialization is zero.

Every fppf neighborhood containing a point over the chosen closed point reduces to this situation by localizing at that point: the resulting flat local ring map is faithfully flat. Local finite presentation need not survive the final localization; it is not needed for the ideal-contraction argument. Additional field extension does not evade the argument, since the composed local flat map is again faithfully flat. Thus the proof covers the neighborhood operation at issue, rather than only a single chosen cover.

In the published first family, the relevant Frobenius map on global sections is b mapped to u b^p after factoring out the tautological root coordinate. The associated boundary class therefore remains nonzero after these base neighborhoods, while restricting to zero on the chosen residual gerbe. The authored lemma correctly proves this algebraic obstruction. It does not claim to rederive every cohomological construction of Appendix B from elementary algebra.

## 6. Independent check of the second authored lemma

Assume p is odd and let R be the localization of k[u,v,a]/(a^2-1-u v^2) at (u,v,a-1). Set C = R[t]/(t^2-u) and e=a+v t.

The defining polynomial of C is monic, so C is free of rank two over R with basis 1,t. The involution t mapped to -t gives e its inverse a-vt, since their product is a^2-u v^2=1. Thus e is a unit of norm one.

The coefficient 2a is a unit at the chosen point. The local equation consequently defines an étale local extension of the regular local ring k[u,v]_(u,v). In particular u is a nonzerodivisor, as required for the Cartier divisor in the source construction. Modulo u, a+1 is a unit and (a-1)(a+1)=0 forces a=1. Therefore R/(u) is exactly k[v]_(v), with v nonzero.

For any faithfully flat R-algebra B, the basis 1,t survives base change. Every candidate p-th root of e is uniquely c+dt. Characteristic p gives

(c+dt)^p = c^p + d^p u^((p-1)/2) t.

Equality to e forces v=d^p u^((p-1)/2). Since p is odd, the exponent is at least one, contradicting the injection R/(u) into B/uB. This rules out every p-th root in C tensor_R B, even without a norm-one restriction. At the closed point, a=1 and v=0, so e specializes to one.

Every hypothesis used by this proof is necessary to its stated form: commutative characteristic-p algebras for Frobenius additivity, p odd for the involution and positive exponent, faithful flatness for ideal contraction, the chosen localization for a+1 invertible, and monicity for coefficient comparison. The case p=2 is not included. The proof does not assume that Frobenius is surjective or that B is reduced or perfect.

This local algebra is an essentially finite-type realization of the norm-one obstruction in Appendix B.2, whose illustrative base is a power-series ring. The local realization is legitimate and remains nonproper; it does not turn the example into one satisfying the global existence theorem's proper-base hypothesis.

## 7. Lifting, representability, and flatness in the counterexamples

The passage from these calculations to torsors uses the source's two split extensions N semidirect H and their twisted forms K of N. Lifts of the canonical H-torsor Q to a G-torsor, together with the quotient identification, are K-torsors. In the first family the boundary comes from the relative Frobenius sequence of a line bundle; in the second it comes from the twisted Kummer sequence of the norm-one group. The elementary calculations show nonmembership in the image of the map on global sections. Exactness then gives a nonzero boundary class. The specializations zero and one have the indicated roots, so their boundary classes on the residual gerbe vanish.

Forgetting the chosen quotient identification does not make the nontrivial lift isomorphic to the canonical lift: any automorphism of Q induces an automorphism of its canonical induced G-torsor. An isomorphism of unframed lifts could therefore be adjusted to preserve the quotient identification, contradicting the nonzero K-class.

The finite-flat hypotheses are genuine, not inferred from the number of geometric points. The group schemes alpha_p and mu_p have rank p. Their torsors are finite flat; the H-Kummer chart is finite flat of rank p or two. A lift Y has quotient Q by N, so Y to Q is an N-torsor. Consequently these total spaces are schemes and their composite maps to the affine/local base are finite flat of ranks p^2 and 2p, respectively. Failure of flatness is not the mechanism of the examples.

These checks justify the obstruction to the residual-gerbe-to-base-neighborhood step used by the existing strategy. They do not classify every possible embedding of inertia into every possible structure group, nor do they assert a proper global nonexistence theorem.

## 8. Logical variants that must remain separate

1. The unrestricted local rigidity assertion for all pairs of nonabelian torsors is false, by the published examples.
2. The root-stack representation/uniformization criterion is known in the nonabelian setting, subject to its hypotheses and the faithfulness correction.
3. The proper-base existence criterion with the original Kummer-local torsor condition, using the corrected definition of joint weights and allowing G to vary, is not proved or disproved by this work.
4. Even an existential problem for a fixed G is not refuted by finding one bad G-torsor. The displayed split groups already admit a canonical good induced G-torsor on the same affine/local base. There is also the Kummer cover itself under H. This makes the quantifier gap concrete.
5. A criterion with G prescribed needs G-compatible tensor data. The original theorem does not have that quantifier order.
6. Characteristic zero, finite étale structure groups, additional global restrictions, and alternative definitions of a ramified torsor are different variants. No outcome for them is claimed here.

Ahlqvist's 2024 paper is not a solution of item 3. Its Proposition 9.6, Definition 9.8 and Theorem 9.18 retain finite abelian group schemes [S4]. The inspected theorem enlarges the building-data setting, not the structure-group scope. Its later date does not change the obstruction analysis.

## 9. Acceptance and stopping condition

The algebraic statements pass. The prior local obstruction is correctly attributed. The original global question remains unresolved by this packet. The author correctly declines to turn a local counterexample into a universal global nonexistence claim and correctly stops after two bounded approaches.

The corrected derivative supplies two necessary source-provenance warnings. No further mathematical repair is required for acceptance at the stated partial scope. This audit and its accompanying explicit acceptance are not certification of a full solution. No repository mutation or publication was performed.

## References

[S1] Niels Borne, joint work with Indranil Biswas, Tamely Ramified Torsors and Parabolic Bundles, Oberwolfach Report 17/2018, pp. 1069–1071. https://doi.org/10.4171/OWR/2018/17 and https://ems.press/content/serial-article-files/46740

[S2] Indranil Biswas and Niels Borne, Tamely ramified torsors and parabolic bundles, final manuscript arXiv:1706.06733v4, 5 November 2020; published in Annali della Scuola Normale Superiore di Pisa 23(1), 293–314, 2022. https://arxiv.org/abs/1706.06733v4 and https://journals.sns.it/index.php/annaliscienze/article/view/894

[S3] Indranil Biswas and Niels Borne, The Nori fundamental gerbe of tame stacks, arXiv:1502.07023v3; Transformation Groups 22 (2017), 91–104. https://arxiv.org/abs/1502.07023v3 and https://doi.org/10.1007/s00031-017-9419-8. Use the correction in [S2, Remark 3.21] for nonalgebraic gerbes.

[S4] Eric Ahlqvist, Building data for stacky covers, Selecta Mathematica 30, article 50 (2024), published 9 May 2024. https://link.springer.com/article/10.1007/s00029-024-00939-1
