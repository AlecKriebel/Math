# Kourovka 21.124: authoritative source contract

Prepared UTC: 2026-10-24T22:03:53.374817+00:00. This is candidate preparation only, with no claimed solution or publication.

## Authoritative statement and provenance

The current official homepage links the October 20, 2026 update-3 of the 21st edition. Problem 21.124 occurs on printed p.198 (PDF page index197), signed **I. Soroko**. It is not preceded by a solution star or an unverified-AI sharp. The original reference supplied is F. Haglund and D. T. Wise, *Special cube complexes*, Geom. Funct. Anal.17(5)(2008),1551–1620; cf. problem20.60.

Exact transcription:

> A group G is said to be virtually special if G has a finite-index subgroup isomorphic to the fundamental group of a special complex (in the sense of F. Haglund, D. T. Wise, Geom. Funct. Anal.,17,no.5(2008),1551–1620; cf20.60.) A group G is called a CAT(0) group if it acts properly discontinuously and cocompactly by isometries on a CAT(0) metric space.
>
> a) Is every CAT(0) free-by-cyclic group virtually special?
>
> b) A weaker question: does every CAT(0) free-by-cyclic group virtually embed into a right-angled Artin group?

Sources: [official homepage](https://kourovkanotebookorg.wordpress.com/), [official edition](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf). The corresponding local source is sources/notebook21_fresh.txt, lines9508–9515. Its source PDF SHA256 is f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118.

The live official [updates-only PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf) contains no exact21.124 match and no solution/correction notice located for this problem. It unexpectedly has a “November2026 update” cover even though the latest homepage post is dated October20 and today is October24. Record that observed mismatch; do not treat future-dated material as an independently authenticated future update. The source PDF hash is3371fa96766d35e18256af9eeac299785d95fb211b31d5e1b31bfab6da2beb71.

## Quantifiers and conventions to retain

The CAT(0) hypothesis asks for a geometric action of the group on some CAT(0) metric space. It is not merely a free action on a possibly infinite-dimensional CAT(0) cube complex; that much weaker cubical condition has known non-CAT(0) free-by-cyclic examples.

The infinite-cyclic case is an exact sequence1→F→G→Z→1, equivalently a semidirect product F⋊Z since Z is free. The printed statement does **not** explicitly require F to have finite rank. Keep both the commonly studied finite-rank case and the possible-infinite-rank reading in view. Wu–Ye2026 introduction and Linton2026 explicitly allow the latter terminology. Linton's Corollary1.5 already covers every hyperbolic free-by-cyclic group, including that broader reading. If “cyclic” includes a finite quotient, the free subgroup already has finite index and the desired virtual embedding follows from virtual freeness; those cases pose no new problem. Rank0 with quotientZ givesZ; rank1 givesZ² or a Klein-bottle group, both virtually abelian.

“Virtually embeds” means existence of a finite-index subgroup H≤G and an injective homomorphism H→A(Γ). A negative result must exclude every such H. Failure of G itself to embed does not suffice. For finitely generated H, any embedding into an infinite-graph RAAG uses finitely many vertex labels on a generating set, hence its image lies in a finite-graph induced RAAG.

## Special versus compact special: exact source warning

No compactness occurs in the21.124 definition. In contrast,20.60 explicitly defines **virtually compact special** using a compact complex (printedp166). The earlier Brady–Soroko2021 questions sheet distinguishes its Questions1.3 and1.4 as weaker/stronger and describes special subgroups as undistorted. This is a convention discrepancy to record, not authority to insert compactness into21.124 or to invent an undocumented proposer intention.

There is a second historical convention. In the corrected original Haglund–Wise text, Definition3.2 distinguishes A-special, which forbids one-sided hyperplanes, from special, which permits them. Their Theorem4.2 is a local-isometry characterization of **A-special** complexes. Proposition3.10 passes from special to A-special using finitely many walls; compactness is an example ensuring that hypothesis. Thus an arbitrary noncompact special complex is not directly covered by citing Proposition3.10 verbatim. Modern accounts often use “special” for A-special.

For the literal *virtual* group question, root has separately written a finite-generation parity-cover argument replacing the finite-walls assumption, in [TARGET_AND_HEIGHT_DELTA.md §1](../../21_125/root_controls/TARGET_AND_HEIGHT_DELTA.md). That is a supporting mathematical deduction subject to its own adversarial review, not a theorem misattributed to the printed HW proposition. Once accepted, it gives equivalence of(a) and(b) under the literal noncompact convention for finitely generated G. Independently of that extra direction, an embedding in a RAAG gives the corresponding Salvetti cover, an A-special complex, so an affirmative answer to(b) supplies an affirmative answer to literal(a). No compactness of that cover follows.

Primary definitions: [corrected Haglund–Wise](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/special%28corrected%29.pdf), Definition3.2, Corollary3.8, Proposition3.10, Theorem4.2.

## Success criteria for a later research attempt

A complete positive answer must construct or prove existence of an appropriate finite-index special model or injective RAAG map for every group under the actual CAT(0) free-by-cyclic hypotheses, including the stated rank convention. A complete negative answer needs an explicit eligible CAT(0) free-by-cyclic group and a proof that no finite-index subgroup embeds in a RAAG (or the exact stronger target if a separately documented compact formulation is being studied).

Rank-restricted results, one-vertex tubular results, special analogues of Hydra groups, free cubulations without the necessary finiteness, non-CAT(0) groups, and obstructions to cocompact cubulation are incomplete for the printed question. The next research target remains the unresolved general CAT(0) virtual-RAAG problem; no discovery claim is made here.
