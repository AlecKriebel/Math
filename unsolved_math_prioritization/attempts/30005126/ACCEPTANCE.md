# Acceptance of the symmetric degeneration source correction

Problem 30005126. Assessment dated 11 October 2026.

## Accepted result

Accept the source-target correction in CORRECTED_TARGET.md together with the qualifications and complete arguments in AUDIT_REPORT.md. The accepted result is a correction of the question and its bibliographic scope. The general representation-directed symmetric-degeneration implication remains unresolved by this work.

The source compares two geometric orbit-closure orders on the same fixed-form symmetric representation variety: the order for the graded general-linear group G and the order for its full graded isometry subgroup H. The imported Hom-order substitution changes the question. Ordinary Ext, degeneration, and Hom-order equivalence for representation-directed algebras is attributed to the established literature, with Bongartz DOI 10.1006/aima.1996.0053. It is not presented as a new proof or a solution of the symmetric question.

## Required mathematical qualifications

1. The precise self-dual formulation is over C and assumes both the stated admissible σ-stable relation ideal and its preservation by the signed path anti-involution ρ(eᵢ)=eσ(i), ρ(α)=−σ(α), with reversal of products. This makes the twisted duality on A-modules well-defined. The weaker source-literal arrowwise formulation remains separately meaningful; equivalence of the two classes of presentations is not asserted.
2. The graded vector space and nondegenerate ε-symmetric form B are fixed. The arrow equation is B(Mαv,w)+B(v,Mσ(α)w)=0 for both values of ε. Fixed vertices in the alternating case have even dimension.
3. The ordinary group is the product of the graded GL factors. The symmetric group is the full graded isometry group. Replacing full O factors by SO or by identity components is not accepted.
4. The convention M≤deg N means that N lies in the closure of G·M. The analogous symmetric order uses H·M. Since H⊆G and the symmetric locus is closed, symmetric degeneration always implies ordinary degeneration. The converse is the intended general conjecture. Equality of isomorphism classes on the symmetric locus alone does not establish the corresponding orbit-closure equality.
5. “Symmetric” here refers to the quiver involution and compatible representation theory; no identification with symmetric Frobenius algebras is made.

## Accepted published scope and restriction argument

The published 2025 Theorem 7.1, p.107, concerns symmetric type-A quivers and their complex path algebras. It proves equivalence of ordinary degeneration, symmetric degeneration, and symmetric Ext-order in that setting. Its representation-directed extension remains a conjecture on p.69. The proof is not replaced by the ordinary Bongartz theorem, because ordinary extensions need not preserve the fixed form or involve isotropic submodules.

The audit's bounded consequence for a closed invariant relation locus is accepted. Let X be the ambient representation variety for a symmetric type-A quiver covered by the theorem, and let Y=R(CQ/I,V) be a closed G-invariant relation locus. For M∈Y, invariance gives G·M⊆Y, and closedness gives closure_X(G·M)⊆Y. Since H⊆G, the same reasoning gives closure_X(H·M)⊆Y. For either orbit, its closure computed in Y is therefore the same as its ambient closure. Applying the published equality to M,N in Y∩Rε(CQ,V,B) proves equality of the two degeneration orders on this locus. The fixed-form symmetric locus is closed as well, so the corresponding symmetric closure is unchanged by this restriction.

This is an elementary consequence of the cited theorem, not a new general theorem. It neither changes the ambient type-A hypothesis nor establishes symmetric Ext-order equivalence for every relation presentation. In a self-dual module interpretation, the signed-compatibility requirement continues to apply.

The finite-representation-type seesaw counterexample is not a counterexample within the representation-directed target. Its orthogonal type-D terminology must not be mistaken for an extension of the type-A quiver theorem to all Dynkin diagrams.

## Evidence and limits

The authored target is preserved byte for byte. The audit retains its mathematical arguments and source hypotheses, with only exact editorial removal of internal identifiers, local file references, and coordination material. Public scholarly metadata preserve the source versions, byte counts, digests, and inspection limits. The seven source PDFs and the frozen correction input were checked against their recorded pins; the full audit-manifest payload was checked as well.

The prior audit inspected the relevant source definitions, theorem and conjecture statements, attribution passages, and selected pages visually. Preparation rechecked the pinned PDFs and freshly inspected OWR pp.1300–1302, Arkiv pp.69 and 107, and the ordinary-order and counterexample passages in the published 2022 paper. OWR p.1302 and Arkiv pp.69 and 107 were freshly rendered and visually inspected. The full Bongartz PDF was not obtained, and no complete independent reconstruction of the cited proofs is claimed.

Fresh explicit integrity and preservation checks were run in normal Python, -O, and -OO modes, together with deliberate mutation controls. The aggregate results are in VERIFICATION.json. These checks do not prove unbounded mathematical assertions or exhaust the literature.

The remaining task is a valid argument or counterexample for the general representation-directed symmetric setting. Neither the accepted correction nor this acceptance report supplies it. No new solution, general disproof, novelty certification, or exhaustive current-status claim is made.
