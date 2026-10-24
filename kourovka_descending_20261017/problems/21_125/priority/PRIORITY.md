# Kourovka 21.125 — preliminary priority and source-scope audit

As of **October 24, 2026 UTC**. Literature audit completed; mathematical promotion of the newly recorded scope check awaits independent review. **The separate Hydra question is provisionally open for arbitrary rank, with small ranks already reported solved. The literal actual-word formulation of (a) has a counterexample by an elementary re-presentation of the established Gersten example.** Neither observation establishes an original complete resolution of both subquestions.

## Authoritative statement and official status

The [official main Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf), October 20, 2026, printed p.198, names M. Bridson and is signed I. Soroko. `SOURCE_CONTRACT.md` retains both subquestions, the absence of a CAT(0) hypothesis in (a), the actual word-length growth definition, and specialness without a compactness requirement.

The primary [official website](https://kourovkanotebookorg.wordpress.com/) was retrieved live. Its linked [update PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf) has no 21.125 entry. Both PDFs were freshly downloaded and match the earlier cache hashes. The updates cover says November 2026 despite being accessible October24; we preserve that anomaly and do not describe it as an authenticated future publication. Absence of a solution notice is corroboration only. Secondary “open” labels were not used as mathematical proof of unresolved status.

## A necessary distinction: actual growth versus outer growth

The [Brady–Soroko questions/comments sheet](https://sites.math.unt.edu/~soroko/questions1.pdf), dated July21,2021, asks the maximal-growth question as Question1.5, reports the small-rank Hydra work after Question1.6, and explicitly distinguishes actual and cyclic growth in §2. Its motivation uses the linearly growing rank-three Gersten example.

The [author copy of Brady–Soroko's 2019 paper](https://sites.math.unt.edu/~soroko/Dehn-functions-RAAGs.pdf), dated August28,2020, **Appendix10, Corollary10.3**, proves the exact Gersten group has no finite-index RAAG embedding. The result is identified there as folklore, based on Gersten1994, and a proof is supplied.

For the literal Notebook metric, set \(\alpha(a)=a,\alpha(b)=ba,\alpha(c)=ca^2\) and \(\varphi(x)=b\alpha(x)b^{-1}\). The exact calculation in `GROWTH_METRIC_SCOPE.md` proves
\[
n^2-n+3\le\max_x|\varphi^n(x)|\le n^2+3n+1.
\]
Changing the stable letter makes \(F_3\rtimes_\varphi\mathbb Z\) isomorphic to the established Gersten group. Thus the numerical degree hypothesis \(m-1=2\) holds for actual word length while the proposed conclusion fails. The outer/cyclic degree remains one. Direct free-word checks through n60 reproduce these formulae; the unbounded proof is symbolic and written out.

This is recorded as a **prior-theorem implication and statement-scope defect**, not an assertion that an original paper solving the full problem has been found. No claim of first discovery or formal official correction is supported. An alternative version asking for *outer* growth degree m−1 is different and was not resolved by this audit. A fresh independent adversarial checker should verify all conventions before this implication is promoted in the root ledger.

## What is known about the Hydra subquestion

The July2021 proposer sheet explicitly reports that Soroko established virtual specialness for Hydra ranks **m≤4**, with m≥5 then work in progress. This is an authoritative author announcement, but the sheet does not supply the complete rank3/4 proofs. We did not locate a separate public complete proof of those announced cases; that limitation prevents inventing verification details. They must nevertheless be excluded from an originality claim without resolving prior-art ownership. Rank1 is virtually abelian, and the general rank2 case is already established.

The current [Soroko publications page](https://ignatsoroko.com/publications/) was retrieved live, includes2026papers, and still links that questions sheet. No general Hydra virtual-specialness paper was located there. This is bounded corroboration, not evidence that unpublished work does not exist.

Most usefully, [Goswami–Verma, *Superexponential distortion of free groups in virtually special Groups*](https://arxiv.org/abs/2508.18223), v1 August25,2025, **§8**, explicitly calls the ordinary Hydra virtual-specialness question open. It distinguishes them from **hyperbolic Hydra** groups of Brady–Dison–Riley, whose virtual specialness follows from hyperbolic free-by-cyclic cubulation and Agol. The new distortion examples do not prove virtual specialness of the original ordinary groups. Its live arXiv history lists no later version at this audit.

[Dison–Riley, *Hydra groups*](https://doi.org/10.4171/CMH/294), Comment.Math.Helv.88(2013),507–540, Theorem1.3 and the following presentation/CAT(0) discussion, establishes the original family's CAT(0), biautomatic, free-by-cyclic structure and enormous free-subgroup distortion. These properties do not alone imply virtual specialness. Its correct arXiv identifier is **1002.1945**, not1002.1940.

[Bridson–Riley–Sale, *Conjugacy in a family of free-by-cyclic groups*](https://arxiv.org/abs/2506.01248), v1 June2,2025, studies exactly the same triangular Hydra presentation. Theorems1/2 prove linear conjugator length and polynomial-time conjugacy algorithms. No virtual-specialness theorem occurs; a positive algorithmic result is not the missing embedding theorem.

## Current cubulation results and their exact boundaries

| Primary source | Verified statement useful here | Boundary for 21.125 |
|---|---|---|
| [Wu–Ye, *Some questions related to free-by-cyclic groups and tubular groups*](https://arxiv.org/abs/2504.14192), **v2 October16,2026**, final version to appear in IMRN | Theorem4.5: a CAT(0) free-by-cyclic multiple HNN extension of one Z² vertex along cyclic groups is virtually special. Corollary4.6 gives equivalence with CAT(0) within that single-vertex tubular class. Theorem4.9 classifies a specified linear triangular family; Corollary4.10 separately treats compact specialness. | No theorem asserting that every maximal-growth automorphism or every ordinary Hydra group has the required one-vertex tubular presentation. No silent inference of that missing hypothesis. |
| [Woodhouse, *Classifying virtually special tubular groups*](https://doi.org/10.4171/GGD/452), GGD12(2018),679–702, Theorem1.1 | A tubular group is virtually special iff it acts freely on a finite-dimensional CAT(0) cube complex, equivalently on a locally finite one. | Requires tubular structure and the stated dimensional/local finiteness hypothesis, not just some free cubulation. |
| [Button, *Tubular free by cyclic groups act freely on CAT(0) cube complexes*](https://doi.org/10.4153/cmb-2016-074-0), CMB60(2017),54–62, Theorem2.4; accepted primary repository copy | Every tubular free-by-cyclic group has an equitable set and acts freely on a CAT(0) cube complex. The text explicitly says the complex need not be finite-dimensional or locally finite, and discusses Gersten as an infinite-dimensional example. | Combining this with Woodhouse does not make all tubular free-by-cyclic groups virtually special. One introductory sentence in Woodhouse attributes a stronger dimensional conclusion; the actual Button theorem does not contain it. We use theorem statements and checked hypotheses. |
| [Munro–Petyt, *Coarse obstructions to cocompact cubulation*](https://arxiv.org/abs/2407.09275), latestv3 June11,2025, TheoremsC/E | Rich linearity excludes coarse median/cocompact cubulation; tubular coarse-median groups are virtually compact special. | The problem asks virtual specialness without compactness. Failure of a cocompact cubulation alone is insufficient for a negative answer. |
| [Liu, *Virtual cubulation of nonpositively curved graph manifolds*](https://arxiv.org/abs/1110.1940), Theorem1.1; J.Topology6(2013),793–822 | Equivalence of NPC, virtual special cubulation, virtual RAAG embedding, virtual RFRS for compact aspherical graph manifolds. Wu–Ye introduction also records the known general rank2 free-by-cyclic conclusion. | Not every higher-rank mapping torus is a graph-manifold group. |
| [Brady–Soroko2019](https://sites.math.unt.edu/~soroko/Dehn-functions-RAAGs.pdf), TheoremA | Constructs particular virtually special free-by-cyclic Hydra analogues with polynomial degrees of arbitrary size. | The ranks/degrees are specified for their examples; existence for each degree is not a universal theorem about every rank-m maximal-growth automorphism and is not the original Hydra family. |

## Search coverage, limits, and research disposition

Searches included exact21.125wording; maximal-degree/polynomial/free-by-cyclic formulations; actual versus outer and inner-twist growth; Hydra/Soroko small ranks; current2025–2026cubulation; hyperbolic versus ordinary Hydra; author publication listings; and relevant bibliographies. Public indexed searches restricted to MathSciNet and zbMATH did not produce an accessible decisive review; no subscriber-only exhaustive database search is claimed. Aggregators and secondary summaries were leads only. Primary PDFs, author statements, and live arXiv histories support the recorded conclusions.

**Disposition:** do not present21.125as a wholly solved original problem. First independently review the literal(a) counterexample calculation. For genuinely unresolved work, the remaining eligible focus is ordinary Hydra(b), provisionally **m≥5**, and only an explicitly separated outer-growth variant if the root elects to study it as a related research program. No original investigation of those remaining targets, publication package, upload, or tracker entry was undertaken here.
