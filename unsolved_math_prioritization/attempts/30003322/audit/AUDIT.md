# Independent adversarial audit: initial surreal set models

Problem 30003322 / OWR-15181-014, rank 664. Audit date: 2026-10-04 UTC.

## Verdict

PASS for the intended partial mathematical results, with one required standalone wording clarification in CORRECTIONS.md. Preserve the disposition **unresolved / exhausted, 5 of 5 approaches**. Neither universal set-model converse has been proved or refuted, and no independence or novelty conclusion is established.

This audit is bound to the original MANIFEST.json with SHA-256 `4a0a5cece35d143c2ebdf3683f0a7a115588f2a42b5730af77ac21aee7a84a54`. Every listed payload's byte count and hash match. The original files were not changed. The supplied checker was independently executed and its output matches the recorded result. Additional controls use separate representations and algorithms; their scope is deliberately finite.

## Source alignment and dependencies

Fresh retrievals of the official Oberwolfach PDF and author-hosted Ehrlich--Kaplan PDF match the original PDF hashes and byte counts exactly. The relevant primary statements, definitions, and proofs were inspected in extracted text; the group criterion and both problem statements were also visually inspected in rendered original pages.

The original report's printed pages 3357--3358 state the canonical field criterion, the group criterion, and the exact distinction between class models and set-universe models. The author paper's Sections 2--5 fix simplicity, normal forms, truncation, cross-sections and coefficient groups. Its Section 8 has the class-model theorem and the set-model question. These support the target interpretation and the criterion applications used here. The qualification to consistent theories considered up to deductive equivalence is appropriate.

For model theory, C. Ward Henson's *Class Notes for Mathematics 571* (Spring 2010), Definition 4.1 and Theorem 13.3, were separately inspected to check the parameter-cardinality saturation convention and the partial-type version of Omitting Types. Source metadata and URLs are in SOURCE_CHECK.json. Published surreal embedding criteria and the ordinary first-order completeness/omitting-types results are accepted external theorems here; this audit checks their precise hypotheses and every authored application, rather than claiming a new foundational proof of those theorems.

The stored exponential-field and Rangel--Mariano PDFs also match their recorded hashes. Their introductions and relevant model/initiality passages do not supply the missing converse. The search is bounded and is not a certification of worldwide current openness. The older simplicity-hierarchy corrigendum was located bibliographically, but its text was not used as an independent theorem source. The required canonical criteria are explicitly restated in the later primary sources actually inspected.

## Approach 1: saturation and birthdays

Proposition 1 is correct for every infinite cardinal kappa under the package's stated cut property. At a stage alpha < kappa, the set of proper sign-sequence prefixes has cardinality |alpha| < kappa, including for singular kappa. No regularity assumption is necessary. L and R together still have size less than kappa. If y meets every strict prefix inequality, it cannot first disagree before alpha, nor terminate there: either event violates a particular required bound. Consequently the sequence s is an initial segment of y, and initiality supplies s. The empty sequence causes no exception.

The saturation application is correct for the ordered groups and ordered fields in this problem. They have dense orders without endpoints. Thus the associated inequalities are finitely satisfiable, and a complete extension of the partial one-variable type is realized over fewer than kappa parameters. The standalone phrase “a densely ordered structure” should explicitly include “without endpoints”; otherwise one-sided cuts at endpoints are not finitely satisfiable. This is the only required statement clarification.

The obstruction is accurately located. A set image has a set of birthdays and hence an ordinal bound, but no bound tied to a previously chosen saturation cardinal is obtained. Containment of all shorter sequences does not assert equality, and a larger saturation degree does not give compatible embeddings. The finite tree controls prove neither a transfinite saturation claim nor independence.

## Approach 2: dyadics and the omitted type

The proof that a nontrivial dense initial subgroup contains the canonical dyadic subgroup is sound. Every positive surreal starts with +, giving 1. A positive surreal below the sign sequence + followed by n minuses must extend the corresponding sequence with one more minus. Density and initiality therefore supply the whole compatible halving tower. Additive closure supplies every dyadic rational. Order-group embeddings preserve its unique division equations because ordered abelian groups are torsion free.

For odd p, Z[1/p] is dense and cannot contain a nonzero element divisible by all powers of 2. Clearing odd denominators forces unbounded powers of 2 to divide one fixed nonzero numerator. Thus the corollary is valid and correctly not presented as novel.

The conditional Omitting Types argument is valid with “nonprincipal” understood in the partial-type sense: no U-consistent formula implies every formula of the partial type. For a countable complete U, this is the local omission hypothesis of the standard theorem. Omitting p_2 prevents an initial copy. The same model is a countermodel to a weaker theory T contained in U.

A harmless unused branch can be removed: p_2 is always consistent with a consistent theory of nontrivial ordered abelian groups. Every finite fragment is realized by a positive sufficiently large power-of-two multiple of any positive element, and compactness applies. Its nonprincipality, however, is not automatic. In a 2-divisible theory positivity isolates this partial type. The claimed reduction remains conditional and does not resolve theories failing divisibility at a different prime.

## Approach 3: infinite tails and group initiality

For G_A = R[t] + A/(1-t), t = omega^(-1), the eventual-coefficient description is exact. The zero-tail series are precisely the finite polynomials. A nonzero tail has infinitely many nonzero terms after a finite stage, so every proper support truncation is finite. Finite-support members cause no exceptional truncation.

All three hypotheses of the canonical group criterion are met:

- The exponent set consists of 0, -1, -2, ... and is closed under simplicity predecessors.
- Each exponent's coefficient group is all of R, an initial real subgroup.
- Every dyadic requirement for right simplicity predecessors is met, since those coefficient groups are R.

The group is also cross-sectional. Thus the conclusion concerns this actual canonical subgroup of No, not just an unrelated isomorphic copy. No exponent-addition closure is required for an additive Hahn group, and none was silently assumed.

If g has positive leading coefficient c at t^k, then g - (c/2)t^k has positive leading coefficient c/2, regardless of lower terms. The proposed midpoint is therefore positive and below g. This establishes density. Set size follows directly from the finite-polynomial representation and A being a subset of R.

The tail map is a surjective additive homomorphism to A with kernel R[t]. Hence G_A/R[t] is isomorphic to A as an abstract additive quotient; no convexity is needed. Division in the ambient characteristic-zero group is unique. For G_Z the tail of x/2 is 1/2 and excludes membership; for G_D all halves remain allowed but the tail of x/3 does not. Full monomial coefficient groups cannot repair the missing infinite tail.

A stronger boundary is available: none of these groups has the aleph_1-cut property. The countable cut with left side {0} and right side {t^n : n >= 0} is finitely satisfiable. Every positive group member has a leading term c t^k for a finite k, and t^n is smaller once n > k. No group member realizes the full cut. This confirms, rather than weakens, the original disclaimer that saturation is not being claimed.

## Approach 4: the field and its integer part

The family R(omega^(1/n)) is directed by divisibility of n, so its union F is a field. Every omega^q for q rational occurs in one member. For a rational function in u = omega^(-1/n), the usual Laurent expansion at zero has powers of u bounded below; in surreal exponent order its support is finite or has order type omega. All proper truncations are finite Laurent polynomials and lie in the same field. Cancellations can remove terms but cannot introduce another support order type.

The rational exponent group is initial: rational numbers are canonical real surreals, and proper predecessors of a non-dyadic real are dyadic; the dyadic case has finite birthday. Coefficients are all real. Canonical initiality follows either from the canonical field criterion explicitly given on printed page 3357 of the original report, or directly from Theorem 5.1 applied to F's additive group with exponent set Q and coefficient groups R. Thus the abstractly worded criterion in the later paper's introduction does not leave an actual-versus-isomorphic-copy gap in this example.

The non-real-closure proof is correct for every n >= 1. The identity

    (1 + u^n) - (u/n)(n u^(n-1)) = 1

shows squarefreeness. Any irreducible factor has odd multiplicity one, incompatible with the even valuation of a square in R(u). Since 1 + omega^(-1) is positive and a hypothetical square root in the union must lie in a single member, F cannot be real closed. This argument includes n = 1 and does not confuse the directed union of rational-function fields with the full real Puiseux-series field.

The proposed I is an integer part. Finite positive rational exponents are closed under multiplication and addition of monomials; constants multiply and add in Z. A positive nonconstant member has positive leading coefficient at a positive surreal exponent, and exceeds all ordinary integers. Thus 1 is least positive. A field member has only finitely many positive surreal exponents, so its polynomial part belongs to I. For the remaining real constant and infinitesimal, each of the three floor branches in Proposition 4.1 gives z <= a < z+1, including negative constants and a negative infinitesimal at an integral constant. Arbitrarily large finite coefficients do not change these order arguments.

The field thus refutes the suggested sufficiency of residue/coefficient data, rational value group and integer part for a *particular* initial field to be real closed. It does not refute the universal assertion about all models of one theory.

## Approach 5: initial hulls and theory preservation

The iterative set closure construction is valid. Each element has a set of predecessors, the algebraic operations are set-indexed, and the increasing omega union is closed under all operations and predecessors. For any two members, some common finite stage contains both. The construction yields a set-sized initial field containing S, not a representation of a specified field with the same theory.

The canonical initial additive hull of Z[1/3] is indeed Z[1/6]. A fully explicit justification for the dyadic step is to intersect any initial overgroup with R: this intersection is initial, contains Z[1/3], and is dense as a subgroup of R. Proposition 2 applies to that intersection. Then Bezout's identity gives D + Z[1/3] = Z[1/6]; conversely this real subgroup contains D and is initial. This clarification avoids relying on the false general heuristic that an ordered supergroup of a dense group must be dense. The package's conclusion itself is correct.

The hull has the first-order halving axiom and the original localization does not, proving failure of theory preservation. Compatible embeddings of an elementary chain do give an embedding of the union and an initial image. Separate existence does not establish that compatibility. At a class index the availability of the chain and maps as classes must also be accounted for. The compactness warning is correctly limited to external well-foundedness: finite systems of strict descent can live in finite well-orders, while their infinite union demands an infinite descending chain.

## Verification and publication boundary

The original checker reproduces the 3,000 localization cases, 1,000 eventually-constant group trials, 64 squarefree cases and finite tree counts. The independent checker exhaustively verifies the finite prefix-cut equivalence and tests generating-function tail membership, squarefreeness by a different Bezout certificate, all integer-part branches, integer-part ring closure, and localization-hull decompositions. Counts are recorded in ADVERSARIAL_RESULTS.json.

No remote write, repository helper, or other auditor was used. No original source PDF, source extraction, dataset contents, or coordination material is included in this audit folder. Current remote queue state and raw public-dataset bytes were not independently rechecked in this audit; those remain publication-time provenance gates. Mathematical acceptance is restricted to the partial-results scope above and the frozen package, with CORRECTIONS.md applied or carried alongside it.
