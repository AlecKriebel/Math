# Audit of the independent word equation partial result

## Decision

The two erasing-witness restrictions and the commutation-subsystem proposition are accepted as partial mathematical results. The accompanying clarification patch makes the introductory two-word criterion precise when the two images coincide and scopes the three-profile section heading explicitly to nonperiodic erasing morphisms. It changes no theorem, hypothesis, or proof inference.

Both reported finite searches have been independently reconstructed, including every bit of every solution signature. Their negative conclusions hold exactly on the stated finite witness pools. Problem 30001551 remains unresolved by this work. No novelty or improved general upper bound is claimed.

## Exact scope

The target has three distinct variables, no constants, and nonempty words on both sides of each equation. Solutions are morphisms into a finite-alphabet free monoid; variable images may be empty. Independence concerns complete solution sets. There must be one nonperiodic morphism satisfying all three equations.

These conventions agree with the definitions on printed page 2216 and the question on printed page 2217 of Karhumäki's contribution to [Oberwolfach Report 37/2010](https://ems.press/content/serial-article-files/46296). The entire contribution was read, and those two pages were visually inspected. The unrelated contributions in the workshop volume were not treated as mathematical dependencies.

## Balanced reduction

Saarela's [2024 manuscript](https://amsaar.gitlab.io/articles/sa24tocs.pdf), Lemma 4.4, applies to a nonperiodic morphism on precisely three variables into a free monoid. For an unbalanced equation that it satisfies, the lemma gives equivalence to the entire system of equations satisfied by that morphism. The statement includes erasing morphisms and periodic solutions of the equation; its proof explicitly handles the periodic case.

For the proposed application, the given finite system is contained in that entire system. An unbalanced member would therefore imply every member. Removing any other equation would leave the solution set unchanged, contradicting independence when the system has at least two members. The reduction is valid.

Every periodic morphism satisfies a balanced equation: both substituted sides are the same total power of a common word. Consequently every deletion witness of the balanced system is nonperiodic. This is a consequence of full-solution-set independence, not a replacement definition.

## Two-word criterion and erasing profiles

The precise criterion concerns the morphism from two distinct formal letters to two specified words: it is injective exactly when those images do not commute. Empty images and equal images make the morphism noninjective. If both images are nonempty and distinct, this is the usual two-element-code criterion.

The original opening sentence about two words forming a code is potentially ambiguous when the images are equal. For example, the set `{a,a}` is just the singleton code `{a}`, although the indexed substitution sending two distinct letters to `a` is not injective. The supplied patch resolves this terminology. It also adds the word “nonperiodic” to the three-profile heading, matching Lemma 1: unrestricted periodic erasing morphisms do not have just those three profiles. The proof only uses the valid indexed formulation: noncommuting images give injectivity, and a relation between distinct formal words forces commuting images.

A nonperiodic erasing three-variable morphism erases exactly one variable. Erasing two leaves at most one nonempty image, hence a periodic morphism. If the retained pair commuted, the entire morphism would again be periodic. Thus the retained pair gives an injective substitution, and equality of substituted equation sides is equivalent to equality of their deletion projections. Lemma 1 is correct, including all empty-image cases.

## Two deletion projections

For distinct erased variables `A,B`, the remaining letter `C` appears equally often and in corresponding positions in both deletion projections. Splitting the two equation sides at their `C` occurrences gives corresponding `{A,B}` blocks with identical counts of each letter. Their substituted lengths therefore agree for every morphism.

If the full substituted words agree, their equal-length prefixes give equality of the first pair of blocks. Cancelling these equal blocks and the common image of `C` repeats the argument. Cancellation is valid even when a block or the image of `C` is empty. If there are no `C` occurrences, there is simply one block.

Because the original equation is nontrivial, at least one block pair differs as formal words. Equality of that block pair forces the images of `A,B` to commute. Conversely, commutation and matching letter counts make every block pair equal. Thus Lemma 2 is an equivalence over the whole free monoid, not only over nonperiodic morphisms.

The assumption that the equation is nontrivial is necessary. A trivial equation has both deletion identities but imposes no commutation condition. The manuscript includes the assumption, and independence guarantees it in both theorem applications.

## Commutation-subsystem proposition

Replace the designated member by the equivalent equation `YZ=ZY`. Any nonperiodic solution has a representation `y=w^m,z=w^n`, where `w` is nonempty, `m,n` are nonnegative and not both zero, and `x,w` do not commute. Such a representation follows by taking the common primitive root of the nonempty members of `y,z`. If both were empty, or if `x` commuted with that root, the morphism would be periodic.

For each balanced equation, splitting at `X` occurrences gives equally many blocks on both sides. After substitution each block is a power of `w`. Injectivity of the substitution on the two formal letters representing `x,w` makes equality equivalent to equality of the corresponding exponents. This proves the stated homogeneous two-column matrix condition.

The common nonperiodic solution supplies a fixed nonzero exponent vector in every matrix kernel. A two-column matrix with such a kernel has rank zero or one. All rank-one matrices have exactly the same kernel line. Thus either every matrix is zero, or any one nonzero matrix imposes all the nonperiodic restrictions of the full system on the commutation slice. Periodic morphisms satisfy every balanced equation separately. These two cases exhaust all solutions, establishing equivalence to one or two original members.

The boundary cases are covered:

- If one of `m,n` is zero, the common kernel is a coordinate axis; the same rank argument applies.
- If an equation contains no `X`, its sole block has zero count differences because the equation is balanced.
- Zero blocks do not disrupt the formal-word comparison; zero consecutive powers remain well-defined.
- The chosen root representation need not be unique. Scaling a root representation scales the exponent vector, and the homogeneous condition is unchanged.
- A periodic morphism is never subjected to the injective two-word argument.

The common nonperiodic hypothesis is indispensable. The three pairwise commutation equations are independent, have erasing deletion witnesses, and have only periodic common solutions. They are an explicit adverse control against deleting this hypothesis.

## The two restrictions

If two different equations of an independent triple had erasing deletion witnesses, those witnesses would be nonperiodic and would have to erase different variables. Otherwise their equation profiles would coincide, which is incompatible with failing different designated equations while satisfying the others. The third equation has both deletion identities, is nontrivial, and is therefore equivalent to commutation. The proposition makes the triple redundant, a contradiction.

If a common nonperiodic solution erases `A` and a deletion witness erases `B`, their profiles force `A` and `B` to differ. Any equation other than the failed one is satisfied by both morphisms. Applying the same two-projection argument and proposition again contradicts independence. Hence no equation admits an erasing deletion witness in this case.

The conclusion does not exclude an erasing common nonperiodic solution. Such a hypothetical triple would need nonerasing deletion witnesses for all three equations.

## Prior attribution and theorem scope

The full [Holub–Žemlička 2015 article](https://www.karlin.mff.cuni.cz/~holub/soubory/AlgebraicProperties.pdf) was read. Its Lemmas 15–16 contain the erasure/projection and block-commutation mechanism; their rank hypotheses must not be silently replaced by nonperiodicity. For example, `[ab,ba,epsilon]` is nonperiodic but its letter-count vectors span a one-dimensional space. The audited argument avoids that issue by proving the three-variable statement directly with injectivity. It also explicitly retains nontriviality when invoking commutation equivalence. There is no novelty claim.

The full [Nowotka–Saarela 2022 manuscript](https://amsaar.gitlab.io/articles/nosa22sicomp.pdf) was read. Theorem 7.2 supplies the bound 17 with a common nonperiodic solution. The bound 18 omits that condition. Neither proves that an independent triple is impossible. The full 2024 manuscript was also read; its entire-system classification does not by itself imply redundancy of an arbitrary balanced finite subsystem. The audited proposition supplies its own restricted-class proof.

This audit does not certify an exhaustive literature search or the absence of a later resolution.

## Exact computational acceptance

For each side length `n`, a common deletion skeleton of length `r` has `2^r` possibilities. Choosing its positions in a length-`n` side gives `binomial(n,r)` distinct insertions. The number of unordered nontrivial equations of length `n` is therefore

`sum over r=0,...,n of 2^r * binomial(binomial(n,r),2)`.

For lengths 1 through 8, the counts are `0, 2, 18, 120, 720, 4130, 23226, 129584`. The family is balanced: equal deletion skeletons fix the `X,Y` counts, and equal side length fixes the `Z` count. Every equation has the common nonperiodic solution `[a,b,epsilon]`.

An audit-only C++ reconstruction generated every skeleton and subset of insertion positions. It evaluated substitutions with exact binary integers carrying a leading length delimiter. The longest encoded output has 21 letters in the second scope and 16 in the first, so the unsigned 64-bit representation cannot overflow. It enumerated all finite signatures and all triples without the original searcher's pair-pruning step. An independent Python comparison checked the combinatorial counts, every signature bit, and direct string evaluations of every representative from both implementations.

- Side length at most 8, binary image lengths 1–2: 157,800 equations, 216 morphisms, 5 signatures, 10 signature triples, zero independent triples.
- Side length at most 7, binary image lengths 1–3: 28,216 equations, 2,744 morphisms, 15 signatures, 455 signature triples, zero independent triples.

For signatures `A,B,C`, independence on the pool means all three sets `(B intersect C) minus A`, `(A intersect C) minus B`, and `(A intersect B) minus C` are nonempty. This condition was rechecked as set differences. Repeated signatures cannot provide all three witnesses, so distinct-signature triples suffice.

The Python comparison and nine deliberately corrupted-result controls passed under normal Python, `-O`, and `-OO`. The original two mathematical sanity checkers were separately rerun in a preserved copy, reproducing 98,441 two-erasure tests, 57,798 erasing-profile tests, and 1,617,840 commuting-slice tests. Seven additional logical controls cover equal images, empties, linear-rank mismatch, nontriviality, necessity of the common solution, boundary kernels, and empty block delimiters. Finite controls corroborate the proof; they do not replace it.

No conclusion is accepted about longer or nonbinary witnesses, longer equations, or systems with only nonerasing common nonperiodic solutions. The finite absence results are not universal nonexistence proofs.
