# Independent audit of Jiang–Su perturbation stability

Problem 30002218 / OWR-12175-007. Review date: 2026-10-06 UTC.

## Decision

Accept the corrected derivative as a scoped mathematical investigation with five completed approaches and the original problem unresolved. Do not accept the frozen original unchanged. Two corrections are required and have been applied:

1. The integer arithmetic behind the printed Cuntz-transfer radius is correct, but the original audit missed a factor discrepancy in the cited proof chain. The published radius 1/6422957 remains attributed to the source and is not independently certified here. A conservative radius 1/16000000 survives the retained-factor calculation in the common-unit unital subcase.
2. The conditional central-sequence proof needs an intermediate parameter γ₁ greater than γ, but below the same threshold, to satisfy the cited paper's strict uniform near-inclusion convention. Its conclusion and stated hypotheses are unchanged.

The corrected derivative supplies an actual seven-file patch, not an annotation attached to an unchanged overclaim. The initial ten-entry archive and its external manifest were preserved byte-for-byte.

## Identity and source match

The initial archive has SHA-256 9e45e7a3e3c64c4324b86bf4037ac849e4dc59dec54bd41b4208e98775dbf279 and length 14470 bytes. Its external manifest has SHA-256 73ca5ca1c5294dffc0d71d81655b25348a1b005e14d09b93ba951f3eac7fc0fe and length 1956 bytes. All ten entry digests, lengths, UTF-8 decodings, JSON parses, regular-file types, and CRCs match. The extracted authored files equal the archive entries.

The complete supplied problem and its associated complete review object were independently serialized by the specified default json.dumps(..., sort_keys=True).encode() procedure, with neither truncation nor key selection. The resulting digest is a0632c9b45dd19b05cc78fd58d78efc86fec82db2ceef433d80d638e8d8172b1. The statement digest is 17eb1673fa897711167d80bbcc260f5dd9ad1f597447c834fa6f45dcf5014ccb. The catalog's identifier is a string while the complete problem's identifier is numeric; both identify the same selected problem. The catalog's historical queue state is not evidence that the current five approaches were absent. No raw corpus records are included.

The original source is Stuart White's contribution to the Oberwolfach report, pp. 3140–3143. The metric on p. 3140 is two-sided Hausdorff distance between closed norm unit balls in a common B(H). The question on p. 3143 assumes separability and Z-absorption of A. It does not assume nuclearity, simplicity, unitality, separability of H, or a separately stated separability hypothesis on B. It asks for a uniform positive radius over such pairs. Ordinary distance cannot be replaced by complete distance without proof.

Schafhauser–Tikuisis–White, arXiv:2506.10902v2, §27, pp. 82–83, repeats the same question as Problem XCIX. The live arXiv metadata independently confirms revision date 8 May 2026 and the publicly stated forthcoming journal status. This is dated evidence of an open question, not an exhaustive assertion about every subsequent manuscript. Bounded independent searches did not locate a later matching resolution. A 2026 paper on centrally pure algebras concerns central sequence algebras and does not, by its abstract, bridge ordinary closeness to their pureness; it was not used to infer a solution. The source's bounded repository-search history and failed problem-page retrieval are retained as author reports, not relabeled as independently reproduced searches.

## Verification of each route

### Separability transfer

The direct argument is valid. For d(A,B)<γ<1/2, a countable dense subset of A's unit ball and chosen γ-close contractions in B give a q-net of B's unit ball with q=2γ+ε<1. Approximate a nonzero residual r by ||r|| times a chosen contraction with error at most q||r||; iterating gives a convergent geometric series in the countable closed linear span. Hence that span is B. No completeness or separability of the ambient Hilbert space is used. This is also covered by CSSWW Proposition 2.10. It works for nonunital algebras and does not change the source's hypotheses.

### Nuclear isomorphism subcase

CSSWW Theorem 4.3 gives an abstract isomorphism when A is nuclear and separable and d(A,B)<1/420000. The statement has no common-unit or separable-H condition. B's separability and nuclearity are transferred in the cited argument. Transporting an isomorphism A≅A⊗Z across A≅B is valid for spatial tensor products, including nonunital algebras. The proposed composite is correctly typed. This is an existing additional-nuclearity subcase; Z being nuclear does not make an arbitrary Z-stable algebra nuclear.

### Embedding transfer and the commutator estimate

CSSWW Corollaries 4.5 and 4.7 use threshold 1/12600000 and finite-set norm control 152√γ. The source algebra to which the theorem is applied is the separable strongly self-absorbing copy of Z. The target need not be separable or nuclear. For ordinary d(A,B)<γ there is uniform slack, so the paper's strict near-inclusion hypothesis is satisfied.

For nonzero common-unit unital A and B, the tail-factor argument genuinely gives approximately central unital copies of Z in A. Strong self-absorption identifies the infinite tensor power with Z, and finite tensors are dense. Including 1 among the controlled elements makes the transferred homomorphism unital because a projection p≠1 has ||p−1||=1. The numerical bound is adequate: 152²=23104<12600000.

Each summand of the displayed commutator expansion has the asserted norm bound: 2||ψ(y)−φ(y)||, 2||x−a_x||, and ε, respectively, since x and φ(y) are contractions. Thus ε+2γ+304√γ is correct. It is a remaining upper allowance for a fixed distance, not a positive lower bound on achievable commutators. The M₂⊗Z example is exact: [e₁₁,e₁₂]=e₁₂ and ||e₁₂||=1, while 1−γe₁₁ is a contraction. It refutes arbitrary fixed-error representative selection, not absorption stability.

### Cuntz transfer and the source discrepancy

PTWW Theorem 3.10 gives an isomorphism including the natural scale at complete distance below 1/42. PTWW Corollary 4.15 states a Z-stable ordinary-distance result at 1/6422957 without nuclearity, simplicity, unitality, or separability hypotheses beyond the shared representation. Its use does not produce an algebra isomorphism or Z-absorption of B.

The original arithmetic exactly follows the smaller β printed in Proposition 4.13. For k=5/2 it obtains β=1585056γ, η=3203122γ+52306848000γ², and the integer remainder 3427616. Those computations are correct, including the rational bound √2<3/2.

The source proof chain does not support discarding k: Lemma 4.11 has β=96kα(600k+1); its substitution α=11γ and Lemma 4.12 both give β=1056k(600kγ+γ). Proposition 4.13 prints β without that leading k while invoking Lemma 4.12. Both arXiv v2 and the published PDF contain the discrepancy. The printed pages 944–945 were visually inspected to exclude a text-extraction artifact. The antecedent CSSW argument, Lemma 4.3 and Theorem 4.4, was additionally inspected: a commutant-distance estimate η produces denominator 1−2η−2kγ. The PTWW proof correctly uses this denominator, but the larger η must be carried into it.

Retaining k gives β_*=3962640γ and η_*=7958290γ+130767120000γ². The corrected derivative supplies the full monotonic-polynomial argument at M=16000000:

    M²−15917005M−261534240000=1066385760000>0.

Together with 1344·2200<M, this proves both smallness hypotheses and 1−2η_*−5γ>420γ. For common-unit unital pairs the source's proof scheme then gives d_cb<1/42. Here is the analytic justification of that scope. Restrict the given representation to the common support of the unit, so both algebras act nondegenerately. For an arbitrary unital representation of B, use a unital representation of C*(A,B) extending it as a summand. Its image of A inherits property D_k by quotient permanence. Lemma 4.12 bounds the commutant distance by η_*. The argument of CSSW Lemma 4.3 then gives the local derivation-distance bound k/(1−2η_*−2kγ) for the image of B. Compression to the given summand preserves that bound. Thus B has the required property D, and PTWW Proposition 4.2 applies to both original near inclusions. Converting unrestricted approximation to unit-ball approximation incurs the displayed factor 2, giving 4kγ/(1−2η_*−2kγ). This verifies the conservative quantitative deduction without suppressing Proposition 4.2's nondegeneracy hypothesis. The 1/16000000 radius is deliberately conservative. It neither improves the larger published radius nor asserts novelty. At γ=1/7000000 the retained positivity condition fails, since 2η_*+5γ=2791940731/1225000000>1. This witnesses a failure of that estimate, not a counterexample to the theorem's conclusion.

The nonunital bridge deserves attention. PTWW Corollary 4.9 explicitly gives property D₅/₂ for Z-stable C*-algebras. One must not argue that 1_A⊗Z lies inside nonunital A⊗Z. In a nondegenerate representation of A⊗Z, use multiplier extensions of A and Z, and adjoin the unit to the A factor. These commuting unital subalgebras generate a C*-algebra E with E''=(A⊗Z)'', because approximate units put both multiplier factors in that von Neumann closure. PTWW Proposition 4.8 applies to E. Kaplansky density gives the same derivation norm on E as on A⊗Z, and their commutants agree. Thus the D₅/₂ estimate applies to the original nonunital representation as well. This is exactly the nondegenerate-representation convention in PTWW Definition 4.1. It does not by itself dispose of all common-ambient degeneracy issues in a quantitative comparison of two algebras. The source-stated Corollary 4.15 has no nondegeneracy hypothesis, but the independently retained-parameter deduction here is expressly restricted to the common-unit unital subcase. No arbitrary-support or arbitrary-nonunital quantitative reconstruction is claimed.

### Conditional central-sequence criterion

For unital A, the multiplier algebra M(A) in TW Theorem 2.2 is A. Hence its exact criterion gives the claimed unital embedding of Z into Q(A)∩A′. Simplicity of Z gives injectivity. The maps from Q(A) and Q(B) into Q(C) are isometric: their quotient norm is limsup of coordinate norms, unchanged by inclusion. The target central-sequence algebra is a C*-algebra and can be represented faithfully even when nonseparable.

One repair is necessary. A pointwise error strictly below γ for every contraction gives a supremum at most γ, not necessarily below γ. CSSWW's ⊂γ convention requires a uniformly smaller parameter. Choosing γ<γ₁<1/12600000 establishes the required ⊂γ₁ relation and preserves the projection estimate 152√γ₁<1. No premise or conclusion of the conditional theorem changes. B must still be separable for the final TW criterion, as assumed.

This remains conditional. Coordinatewise approximation supplies closeness to Q(B), not to its intersection with B′. The nonunital version requires the multiplier/annihilator formulation and is not established by this common-unit argument.

### Relative commutants and the vanishing-distance route

The rotating-MASA example is correct. For 0<t<π/2 a diagonal matrix commuting with the rotated rank-one projection is scalar. The distance of diag(1,−1) to scalar contractions is 1, while scalars are contained in D, so the Hausdorff unit-ball distance is exactly 1. On the other hand conjugation gives d(U_tDU_t*,D)≤2||U_t−1||→0. This refutes an unrestricted continuity rule for intersections without purporting to compare the special F_A,F_B of the original problem.

For γ_n→0, the diagonal sequence of honest coordinate embeddings is multiplicative and unital without a lifting theorem. Dense finite sets and the contraction bound extend asymptotic commutation to every pair. Ignoring or filling finitely many coordinates does not affect the quotient. The resulting central embedding invokes TW Theorem 2.2 and reproves the Z-case of CSSWW Corollary 4.6. Its common-unit unital assumptions are explicit. Closedness at a fixed B is not uniform openness, and a single positive distance cannot be replaced by a vanishing sequence without an additional construction.

## Scope and acceptance limits

No proof or counterexample to the original perturbation-stability question is supplied. All five approaches retain their explicit stopping points. Acceptance means the corrected arguments and cautions are sound at their stated scope, using the cited established results as inputs. It is not an independent reconstruction of every theorem in the references. Arithmetic and integrity tests are supplementary; neither certifies the analytic mathematics.

There is no packaged executable program, importable module, source PDF, copied third-party source text, raw dataset, private coordination file, symlink, or cache. A separate receipt records isolated private validation of exact archive inventories, hashes, patch replay, and adverse mutations. No publication was performed by this audit.

## Public references

- White's contribution in C*-Algebras, Dynamics, and Classification, Oberwolfach Reports 9 (2012), pp. 3140–3143: https://doi.org/10.4171/owr/2012/52 and https://ems.press/content/serial-article-files/46423
- Christensen–Sinclair–Smith–White–Winter, Perturbations of nuclear C*-algebras: https://arxiv.org/abs/0910.4953 and https://doi.org/10.1007/s11511-012-0075-5
- Perera–Toms–White–Winter, The Cuntz semigroup and stability of close C*-algebras: https://arxiv.org/abs/1210.4533 and https://eprints.gla.ac.uk/90387/1/90387.pdf
- Toms–Winter, Strongly self-absorbing C*-algebras, Theorem 2.2: https://arxiv.org/abs/math/0502211
- Schafhauser–Tikuisis–White, Nuclear C*-algebras: 99 problems, §27, Problem XCIX: https://arxiv.org/abs/2506.10902v2
- Christensen–Sinclair–Smith–White, Perturbations of C*-algebraic invariants, Lemma 4.3 and Theorem 4.4: https://arxiv.org/abs/0910.1368 and https://eprints.gla.ac.uk/25426/1/25426.pdf
