# Exact source and prior gate: 30004048 / OWR-16763-022

## The question and its universal quantifiers

The primary question is Paul Seymour's contribution *Concatenating bipartite graphs*, in OWR1/2019, printed46–47. [Official PDF](https://ems.press/content/serial-article-files/46780); [publisher record](https://ems.press/journals/owr/articles/16763), DOI10.4171/OWR/2019/1. The complete contribution was read, including the preceding definition of the one-direction function. The actual bidirectional symmetry question on printed47/PDF43 was visually checked.

Parameters are real x,y in **(0,1]**. The detailed primary paper specifies **finite simple graphs**, with a partition (A,B,C) into nonempty stable sets and no A–C edges. The four constraints are

 deg_B(a)>=x|B| for every a in A;
 deg_A(b)>=x|A| and deg_C(b)>=y|C| for every b in B;
 deg_B(c)>=y|B| for every c in C.

For c in C, N_A²(c) is the set of distinct A-vertices reachable through B. Multiplicity of paths is not counted. Define

 ψ(x,y)=inf_G max_(c in C) |N_A²(c)|/|A|,                         (1)

where the infimum ranges over **all** finite graphs and partitions satisfying those four constraints. Equivalently it is the largest universally guaranteed fraction: for every admissible graph there exists a suitable c. The graph attaining the infimum is not thereby asserted to exist. The exact question is whether ψ(x,y)=ψ(y,x) for every x,y in(0,1].

The imported expanded statement suppresses the universal-over-graphs clause in its last sentence; (1) restores the source's intended quantifiers. The source report initially speaks of disjoint subsets in a graph. Keeping only A–B and B–C edges gives the canonical tripartite formulation in the detailed paper. Deleting other vertices/edges cannot increase the number of reachable A-vertices and does not alter the four constraints, so this normalization is compatible with the universal guarantee. We do not extend the question to x=0 or to infinite graphs.

Reversing the parts converts an (x,y)-biconstrained graph into a (y,x)-biconstrained graph, but exchanges a maximum over C with a maximum over A of a different normalized reachability matrix. That observation alone is not the requested equality of the two infima.

## Detailed primary paper and already proved results

Chudnovsky, Hompe, Scott, Seymour and Spirkl, *Concatenating Bipartite Graphs*, Electronic Journal of Combinatorics29(2)(2022),P2.47, DOI10.37236/8451. [Published72-page PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/). The published paper was retrieved directly, including its definitions, §§2 and4, the final §12 and the symmetry discussion. Its earlier [arXiv1902.10878v3](https://arxiv.org/abs/1902.10878v3), posted7December2020 with a December8 revision date in its cover, is a distinct edition and is not substituted for the published numbering.

Known results to credit rather than count as new author turns:

- The one-direction function φ is symmetric by published Theorem2.3, printed10. Immediately afterward the authors explicitly say the corresponding biconstrained and exact questions are not proved and no counterexample is known. That page was visually checked. φ-symmetry does not establish ψ-symmetry.
- Weighted finite graphs are treated in Theorem2.1, with nonnegative vertex weights summing to1 on each part. All four degree conditions are required in the biconstrained case. Rational blow-ups and threshold/strictness issues must be handled explicitly in any new use; no attainment of the infimum in (1) is assumed here.
- max(x,y)<=ψ(x,y); the cyclic constructions give familiar upper bounds. Theorem4.3 evaluates the diagonal as ψ(x,x)=1/floor(1/x) for x in(0,1]. The source report's integer-threshold lower bounds are expanded in §4.
- Theorem12.2, printed72, already states symmetry in the minimal-value regime: ψ(x,y)=x iff ψ(y,x)=x, characterized by an x-regular weighted bipartite graph with minimum B-weight at least y. Its detailed proof is omitted there; this is a credited published statement, not a new general symmetry proof.
- The apparent asymmetric regions in the paper's plots are expressly described as different proven bounds, not a proof of asymmetry. A finite asymmetric graph or a failed reweighting route must not be labelled a counterexample to ψ-symmetry.

## Later work and retrieval limits

Patrick Hompe's [arXiv1908.07453v3](https://arxiv.org/abs/1908.07453) is **withdrawn as of23June2022**; the author comment says the results were edited and incorporated into1902.10878. The default PDF endpoint returns404 and the abstract page says no PDF is available for that version. It is not a separate later solution or an unexplained access failure. The2019 senior thesis with the girth/concatenation title is cited by the2022 paper, not treated as new postpublication evidence.

Current bounded searches with the exact title, biconstrained/symmetry terms and the current author publication list found the2022 paper and related work, but no primary result resolving the full ψ symmetry question. Scott's current publication list links the same paper. This is a dated source check, not exhaustive literature coverage or novelty certification. No external researcher was contacted.

The problem website returned an internal retrieval error, so the pinned catalogue record at revision37e53eabe540fb458758e198be61634bd02ee008 was checked against the full original contribution. Raw imports and PDFs are separate reading inputs and are not public artifacts.

## Prior-attempt gate and budget

Exact ID/alias/reference and related30004047/concatenation/biconstrained issue/PR and commit searches found no matching attempt. Both target attempt paths have empty histories.397 live branch names and443 mirrored refs were checked by branch, all-ref message and target-path history searches, with no exact attempt or invalidation located. Neighboring30004047 is the one-direction φ threshold problem; it does not replace this distinct bidirectional symmetry target.

Eligible for a distinct five-turn attempt. **Zero substantive author turns used by this source/review gate.** The objective remains a rigorous general proof or actual asymmetric pair of universal values; any finite-size, slackened, restricted-family or algorithmic result must retain its scope.
