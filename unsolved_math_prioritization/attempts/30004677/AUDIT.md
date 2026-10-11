# Editorial audit: hyperarithmetical common lower cone

This is an AI-assisted, unrefereed mathematical draft. Acceptance records one internal AI mathematical reconstruction of a credited prior result, with explicit foundational imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Scope of this record

This record checks the organization, logical dependencies and exact boundaries of the single accepted reconstruction in PROOF.md. It is not a second independent mathematical audit. The original authored proof/audit is 22,131 bytes with SHA-256 9dbf5ab2864a7b958fe272c17c8a7e136f1a0fdaa26a1e3ff7d555cbbf6fc440. All mathematical arguments are preserved; only review/distribution wording is adapted for this edition.

The accepted equivalence is quantified over every enumeration degree b and every double-skip fixed degree a. A cycle includes both a and its skip: both satisfy the double-skip equality. Replacing “every” by “some” is false, since a nonhyperarithmetical cycle degree lies below itself. The result is credited to Goh for the converse and AGKLMSS for the lower bound and cycle existence.

## 1. Three distinctions that the proof preserves

Enumeration operators use positive finite oracle information. K_A is enumeration equivalent to A, and S(A) is the complement of K_A. Complementing a computable column is valid; complementing an arbitrary enumeration reduction is not. S is antitone for set inclusion but monotone and invariant for enumeration degrees. The diagonal argument excludes S(A) <=_e A.

A total degree contains T(B) = B join complement(B). A cototal degree contains a C enumeration reducible to its complement. Totality implies cototality, but the two notions are not identified. T(B) <=_e T(C) is equivalent to B <=_T C, and T(B) <=_e A implies B <=_T A by waiting for one of the two tagged answers. These facts are essential both for the transfinite lower bound and for proving that cycle degrees cannot be hyperarithmetical.

Exact set equality S(S(A)) = A is used only for a nonempty arithmetical test class P. The accepted theorem concerns degree equality. No claim is made that every degree cycle has an exactly fixed set representative, and the converse does not need such a claim.

## 2. Existence without a hidden effectiveness premise

S composed with S is monotone on the complete inclusion lattice of subsets of the natural numbers. Intersect all pre-fixed points B with F(B) contained in B. Monotonicity first gives F(L) contained in L and then makes F(L) itself pre-fixed; the intersection definition gives the reverse inclusion. Thus F(L) = L.

The class P of exact fixed points is arithmetical in its free set variable, hence lightface effective analytic. Its definition uses no selected real or noncomputable ordinal notation. The fixed point construction itself is not claimed effective. Nonemptiness is proved before the analytic basis theorem is applied, avoiding a vacuous universal characterization.

## 3. Uniform ordinal-notation reduction

Given a witnessed T(B) <=_e C, a finite halting B-computation can be certified by positive information in C. Its complement is a column of S(C). The complement of T(B), also a column, gives back T(B) by tag swapping, which enumerates the positive halting set. Combining the two halves yields T(B') <=_e S(C), uniformly in the original index.

For a degree cycle, fix a witnessed S(S(A)) <=_e A. This witness may depend on A. The recursion theorem constructs one enumeration operator Phi(Z,p), not a nonuniform family of unrelated reductions. On a valid zero notation it enumerates T(empty set). On a successor-shaped notation it transports the lower column through two skips, projects from the second Turing jump to the first, and composes with the fixed double-skip witness. At a valid limit it dovetails the effective fundamental sequence and copies both tagged answers into the effective join.

Only the integer’s syntactic notation shape is tested. Membership in Kleene’s O is never queried or decided. No correctness claim is made on invalid notations. Transfinite induction on valid notations verifies Phi(A,p) = T(H(p)); validity is a correctness premise, not an effective input test. This single index supplies the simultaneous uniformity required at limit joins. Separate reducibility of each earlier H(q_i) would be insufficient.

Hierarchy completeness then puts every hyperarithmetical X below some H(p), so its totalization and therefore X lie below every cycle. This explicitly covers nontotal hyperarithmetical enumeration degrees, even though the cited prior lower-bound proposition is worded for total hyperarithmetical degrees.

## 4. The analytic basis argument and witness fusion

The HSS theorem permits the relative analytic definition of X to vary with Z in a nonempty lightface analytic class. Its countable list of relative formulas is not replaced by one uniform formula. The reconstruction proceeds by choosing nonempty effective analytic subclasses that force a disagreement with successive candidate definitions of X.

Every chosen analytic class is represented by a recursive tree. At each stage finite prefixes of the real and all current membership witnesses are retained and lengthened compatibly. If the construction never stops, their limits satisfy every finite tree requirement, yielding a member of the original class and all selected subclasses. This real defeats every relative definition, contradicting the hypothesis. Nested nonempty analytic classes alone would not justify a common member; the retained witnesses are indispensable.

If a stage stops, membership n in X is equivalent to the existence of a class member satisfying that stage’s relative analytic formula. A witness on the wrong side would create the excluded nonempty subclass; a missing witness for n in X would make the whole current class such a subclass. Effective analytic closure establishes the unrelativized definition. The choices need not be effective in X. Finite strings and integer indices introduce no real parameter. This is a reconstruction of HSS Theorem 2.1, not a new basis theorem.

## 5. Converse and the unresolved arithmetic boundary

If X lies in a degree below every cycle degree, then X <=_e A for every exact fixed point A in P. Consequently X is c.e. in the ordinary Turing oracle A and its complement is co-c.e. in A. Both are arithmetical, hence analytic relative to A. This does not assert an enumeration reduction of the complement. Two separate applications of the HSS lemma make X and its complement lightface analytic, so X is Delta^1_1, or hyperarithmetical.

For any degree c, c <= c^ is equivalent to cototality, and that comparison makes c^ total because the enumeration jump is c join c^. A total degree is cototal. Accordingly, the universal condition that no finite skip is below the next is equivalent to the universal condition that every finite skip is nontotal. This equivalence uses a one-step shift and does not identify pointwise nontotality with failure of cototality.

The two members of a skip cycle are incomparable: one comparison violates diagonalization immediately and the other, after applying monotonicity, forces the forbidden comparison. Thus all finite skips of a cycle are nontotal. Nevertheless, if its representative A were hyperarithmetical, then A' would be hyperarithmetical, and the lower-bound theorem would imply T(A') <=_e A, hence A' <=_T A. Jump strictness rules this out. Therefore no cycle is an arithmetic example for the residual target.

## 6. Foundational imports and source boundaries

The proof explicitly imports acceptable numberings and effective operator composition; the ordinary recursion theorem; the Kleene ordinal-notation hierarchy, transfinite induction and the Delta^1_1 hierarchy completeness theorem; effective analytic recursive-tree normal forms, relativization and closure; countable dependent choice; and ordinary Turing-jump strictness. These are substantive standard foundations, not results certified by finite checking. No unsupplied research lemma specific to skip cycles remains as an import.

The OWR contribution supplies the exact selected questions and Goh attribution. AGKLMSS supplies the prior lower bound, cycle existence and arithmetic conjecture. Soskova’s slides independently corroborate the attribution but are not a second proof. HSS supplies the analytic theorem and normal forms. Generic-set constructions, skip inversion and definability results elsewhere in those sources are not dependencies audited here. The sources’ complete contents are not claimed reviewed.

The original source ledger records four completely retrieved PDFs and selective page inspection. HSS is an author manuscript dated 11 July 2016; an author bibliography lists a 2017 publication, but the publisher edition was not inspected. AGKLMSS is an undated 39-page author-hosted version with no asserted publisher byte identity or pagination equivalence. Bounded searching found no later arithmetic resolution; it is not an exhaustive current-status certificate.

## 7. Editorial and integrity acceptance

The public PROOF.md is generated from the complete original proof/audit with exactly three editorial substitutions: the added transparent status paragraph, the qualification of mathematical acceptance as internal AI review, and the clarification that finite-check code is not distributed. Mathematical Sections 1–6 and all references are retained verbatim; Section 7’s sole change is that distribution clarification. No theorem, quantifier, proof step, import or residual boundary is removed.

The original closed audit has 84 listed members plus its manifest. Its 37-member input manifest and the 233-member input-screen manifest are separately authenticated by externally fixed hashes; no closed-directory claim is made for those larger input locations. Exact target and related-record joins against both full original corpora are replayed. Hashes and native Git identities authenticate bytes, not mathematics.

The original finite checker exercises all 8,000 antitone maps on the three-atom Boolean lattice and three known-wrong alternatives. Its checks are rerun privately in normal, -O and -OO modes. They cannot prove a theorem quantified over reals or all ordinal notations. Editorial acceptance requires exact replay of every public file’s provenance map, strict additions-only patch replay, all eight native Git blobs and seven complete native trees, preserving all existing siblings and QUEUE. Code, raw outputs, copied source documents, datasets and private coordination are excluded from distribution.
