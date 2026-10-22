Portable mathematical excerpt of the initial scope review. Later r=2 coverage is recorded in the current README and full audit; this historical review predates that discovery. Administrative disposition instructions and nonportable receipt references are omitted.

# Independent applicability and scope audit

Target: rank 433, problem 30001895, OWR-11136-027, *Exact Transversals for Families with the (p,q)-Property*.

Audit date: 2026-10-03 UTC. Historical source/literature audit before the five author attempts; zero proof-attempt turns charged.

## Verdict

**PASS for the credited negative certificate for the hyperplane component. HOLD for a full-resolution designation of the bundled imported record.** The Keller–Smorodinsky theorem is directly applicable to Problem 8 part 2. It does not resolve part 2′. The imported record expressly retains that second question, and no directly established full prior resolution of it was located in this bounded review. That is an unresolved-by-this-audit status, not a certification that the question is currently open.

## 1. Imported and original scope

The statement, original_statement, and clean_statement fields of the frozen problem.json each ask two questions: the hyperplane assertion, followed by whether the analogous r-element-set assertion holds. This is not merely an explanatory mention of an unasked consequence.

I checked the original OWR 44/2011, printed pp. 2540–2541, PDF pages 82–83, by text extraction and fresh local rendering. Problem 8 contains:

- Definition 1: a t-transversal is a hitting set of cardinality at most t.
- Definition 2: every p chosen members contain q with a common point.
- Part 2: hyperplanes in R^d, d+1≤q≤p, and the p−q+1 upper bound.
- Separately numbered part 2′: r-element sets, r+1≤q≤p, and the same upper bound. The source calls 2′ a corollary of 2.

The last observation records an implication A⇒B. A negative answer to A does not imply a negative answer to B and does not make B disappear from an explicitly two-question imported record. A bare “No” is logically sufficient to reject the conjunction A∧B, but is not an adequate claim that both requested questions have been answered. A main-question-only negative answer is legitimate if it explicitly excludes 2′ and does not mark the full record solved.

The independent “Colored Grünbaum” part 1 of Problem 8 is not in this imported record and is not added to its scope.

Primary source: [OWR 44/2011 publisher PDF](https://ems.press/content/serial-article-files/46358), printed pp. 2540–2541. The source year is 2011; the imported citation's 2012 label is not used to change the identity of the question.

## 2. Quantifiers and conventions

The 2011 paragraphs do not explicitly qualify the cardinality of F. Chelnokov–Dol’nikov's 2013 preprint, Definition 7 and the definition of P(p,q;m) on PDF p. 3, explicitly use |F|≥p and finite hyperplane families. Its conjecture P(p,q;m)=p−q+1 cites Oberwolfach September 2011. This directly supports the finite, nonvacuous reading of the hyperplane question used in this review.

The counterexample already belongs to that finite, nonvacuous class, so no argument about infinite families or vacuous |F|<p instances is needed. “Exact transversals” means the proposed upper bound, not a requirement that every individual family attain equality. Hyperplanes are affine hyperplanes; in d=2 the relevant objects are whole affine lines. There is no restriction in the target to central hyperplanes, parallel classes, compact convex bodies, or general position.

For part 2′, preserve the primary's unspecified family cardinality. The 2013 general definition supports |F|≥p as the nonvacuous convention, but its finite definition of P is specifically about hyperplanes; it is not evidence that the 2011 r-set paragraph was expressly finite-only. A later positive resolution must state its cardinality scope or justify any extension. A finite r-uniform counterexample, if independently established, would suffice to refute either scope.

Source: [Chelnokov–Dol’nikov, arXiv:1312.4110v1](https://arxiv.org/abs/1312.4110v1), p. 3; published in *Journal of Combinatorial Theory A* 125 (2014), 194–213, [DOI](https://doi.org/10.1016/j.jcta.2014.03.002).

## 3. Exact negative certificate

Credit: Chaya Keller and Shakhar Smorodinsky, *A new lower bound on Hadwiger–Debrunner numbers in the plane*, [arXiv:1809.06451v2](https://arxiv.org/abs/1809.06451v2), Theorem 1.1, PDF p. 3. Version 2 is dated 5 November 2018. The [journal publication](https://doi.org/10.1007/s11856-021-2185-2) is *Israel Journal of Mathematics* 244 (2021), 649–680, published 21 August 2021. Exact constants here are version-specific to the checked preprint; the journal landing page independently confirms authorship and line-family scope.

For 0<η<1/2 and integer parameters p,q≥3 satisfying

`q ≤ 0.01 η (ln p / ln ln p)^(1/3)`,

the theorem gives a planar line family with the (p,q)-property and

`τ(F) ≥ p^(1 + (1−η)/(4q−7))`.

There is no multiplicative constant C hidden in this displayed bound. The theorem's statement contains no separate threshold p₀. The proof uses asymptotic estimates; the audit's conservative specialization is to sufficiently large integer p satisfying the displayed relation. This is a safe choice within the stated domain, not an additional threshold claimed to have been printed in the theorem. No smallest p is claimed.

With d=2, q=3 and η=1/4, the relation is

`ln p / ln ln p ≥ 1200^3 = 1,728,000,000`,

and the lower bound is

`τ(F) ≥ p^(23/20) > p > p−2 = p−q+1`.

Such integer p exist because ln p/ln ln p tends to infinity. Thus d+1=q≤p and every substantive hypothesis of part 2 is met, while its conclusion fails. A published existential family suffices to negate this universal assertion; an explicit coordinate list is not required.

### Family type, finiteness and nonvacuity

The first clause of Theorem 1.1 itself names lines in R². The separate consequence about general Hadwiger–Debrunner numbers is not being used as a substitute for this stronger, directly applicable clause.

Proposition 3.1, PDF pp. 8–9, starts with a subset of a finite grid. It uses incidence-preserving planar projection and point–line duality to obtain |S| actual lines. The construction of that finite S is provided in the same paper. Its collinearity and cardinality conditions give the stated piercing bound. Hence this is a finite line-family theorem, not only an abstract hypergraph or an arbitrary-convex-body lower bound. Nonvacuity is also forced by |F|≥τ(F)>p; a finite family of nonempty lines can always be hit with at most one point per member.

The q=3 argument is credited in the paper to the point-configuration construction of Balogh and Solymosi, *On the number of points in general position in the plane*, *Discrete Analysis* 2018:16. Keller–Smorodinsky supply the line-family theorem and duality application used here. No new construction, proof of the container theorem, or independent theorem claim is made by this audit.

## 4. Remaining explicit question

The exact remaining mathematical question is:

For positive integer r and integers r+1≤q≤p, let F be a family of r-element subsets of a ground set, with at least p distinct members, such that every p distinct members include q with nonempty common intersection. Must there be a set T of at most p−q+1 elements intersecting every member of F?

Family cardinality should be kept unspecified when quoting the original; its finite, nonvacuous specialization may be separately identified. Do not add linearity, bounded degree, representability, pairwise intersection, or an asymptotically large-|F| condition to obtain a different task.

Keller–Smorodinsky do not provide this conclusion or its negation. Replacing each line by a selected finite set of incidence points would require separate verification of uniform cardinality r, q≥r+1, the common-intersection condition, and the piercing lower bound. None of those requirements is discharged by the hyperplane certificate, and no such transfer was attempted.

## 5. Prior-coverage check and exclusions

The bounded source check found no direct full resolution of the r-element assertion. Its source/coverage log and preserved additional query strings are in R_SET_LITERATURE_CHECK.md; the exact strings from a separate 23-query pass were not retained. The following exclusions are important:

- Chelnokov–Dol’nikov Theorem 4 gives an exact bound for linear families, with an additional explicit lower bound on |F|. It is not an all-cardinalities theorem for arbitrary r-uniform families.
- Their Helly–Gallai-number theorems concern how local t-transversals imply global t-transversals. They are not stated as the requested exact (p,q) theorem.
- OWR follow-ups about planar lines, or hypergraph (p,q)-coloring defined using independent vertex subsets, do not directly cover the present condition on common intersections of member sets.
- General convex-family finiteness, asymptotic bounds, and exact results in restricted parameter regimes do not answer the all-parameter r-element question.
- Search results mentioning uniform linear systems, finite projective planes, chain-intersecting families, and generic hypergraph transversal bounds were not promoted to coverage without matching hypotheses and conclusion.

“No full resolution located” remains a bounded-search finding. It is not an affirmative claim that none exists or that new proof work would be novel.

