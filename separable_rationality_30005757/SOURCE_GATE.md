# Source gate: Rationality of Separable Permutation Subclasses

Audit date: 2026-10-21 UTC. Ordered row 1848; problem 30005757; source key OWR-14298158-002.

## Decision

**SOURCE GATE PASSED; mathematical question remains unresolved in the literature located.** No proof, disproof, or completed classification is claimed. The dataset's “partially solved” label reflects an existing one-way theorem, not a solution to its converse. No queue or GitHub write was made.

## Exact target and logical scope

Let S = Av(2413,3142), and let C be a permutation class contained in S. For at least one p in {132,213,231,312}, suppose Av(p) is contained in C. Must the ordinary length generating function F_C(x) = sum_{n>=0}|C intersect S_n|x^n be nonrational?

This is the mathematical content of Vincent Vatter's Question 4, printed p.283 of [OWR 6/2024](https://doi.org/10.4171/owr/2024/6). The PDF page was also visually inspected. “Contains all” refers to every permutation in one of those four avoidance classes, not merely containing a pattern p or containing all four classes simultaneously. C need not be a proper subclass.

## Definitions and basis audit

A class is downward closed under classical permutation-pattern containment. It is not an arbitrary subset. Av(B) consists of permutations avoiding each member of B; the canonical basis is the antichain of minimal excluded permutations. In general that basis can be infinite. The four p above are the reversal/complement/inverse symmetry orbit of 231, as explicitly recorded in [Albert–Atkinson–Vatter, §1](https://arxiv.org/abs/1007.1014).

Neither sum closure nor skew closure is assumed for C. These are extra properties C⊕C⊆C and C⊖C⊆C respectively. The ambient S is generated from 1 using both operations. An arbitrary subclass does not inherit closure under either operation.

For this particular ambient class, finite basing and algebraicity are consequences, not omitted extra hypotheses: a separable permutation of length at least three is sum or skew decomposable and therefore not simple. Thus each C⊆S has only finitely many simple permutations. [Albert–Atkinson, Theorems 6 and 7 in the author technical report](https://cs.otago.ac.nz/research/publications/oucs-2003-08.pdf) then give a finite basis and algebraic generating function. The published paper is [Discrete Mathematics 300 (2005), 1–15](https://doi.org/10.1016/j.disc.2005.06.016). This argument does not identify countability with finite basing.

An alternative elementary basis argument uses that S is well-quasi-ordered: the minimal exclusions inside S form a finite antichain; adjoining 2413 and 3142 gives a finite avoidance description, whose redundant members can be removed. Countability of all permutations, by itself, would not justify this step.

## Already known versus conjectured

[Albert–Atkinson–Vatter, Theorem 4.1](https://arxiv.org/abs/1007.1014) proves that if none of those four avoidance classes is contained in C, then F_C is rational. This property passes to subclasses, so C is strongly rational. Conversely, a class containing a Catalan avoidance class cannot be strongly rational, because that subclass has nonrational generating function. What is missing is the implication from mere rationality of C to strong rationality of C, within S.

Equivalently, the proposed full characterization is:

F_C is rational iff Av(p) is not contained in C for every p in {132,213,231,312}.

The rational side is established; the nonrational side remains the target. Rationality of a superclass does not generally follow from, or rule out, irrationality of a subclass by inclusion alone.

The whole separable class has nonempty generating function (1-x-sqrt(1-6x+x^2))/2. Including the empty permutation adds 1. This is algebraic but not rational. Multiplying or dividing by x to shift Schröder indexing cannot change rationality, but should not be confused with the length-counting convention.

## Same-report structural route

The later Brignall report, pp.290–292, records an incomplete structural Conjecture 3: C is sum/skew closed or a finite union of such classes, or C⊆X[U] for U strictly smaller than C, with X=Av(2413,3142,2143,3412). X[U] denotes inflation. This is an auxiliary proposed structure theorem, not an established classification. Its related sufficient nonrationality condition is C⊕C⊆C together with 1⊖C⊆C. These hypotheses must not be substituted for the unrestricted target. [Report PDF](https://ems.press/content/serial-article-files/48646)

## Literature status and exclusions

The converse already appears in §5 of the 2010 preprint of Albert–Atkinson–Vatter and remains posed in the 2024 workshop report. Searches on 2026-10-21 covered exact title/statement terms, “separable permutations” with rational/nonrational and 2025/2026, and Brignall/Defant/Vatter combinations. No later resolution was located. This is a bounded negative search, not proof that no unpublished or unindexed resolution exists.

The nearby wqo/algebraicity counterexample is distinct: [Brignall–Vatter, Uncountably many enumerations of well-quasi-ordered permutation classes](https://arxiv.org/abs/2211.12397), revised September 2025 and now listed as Combinatorial Theory 6(1) (2026), #16. Its general classes do not overturn the finite-simple theorem for subclasses of S. The dataset's copied context runs into this separate false conjecture; that continuation is not part of the target.

The 2025/2026 flat-POP enumeration papers retrieved in the search provide special families, not a general resolution. No classification claim is inferred from their titles or abstracts. The current [Brignall page](https://www.rbrignall.org.uk/) was also checked; its publication contents were incompletely exposed on direct read, so absence there is weak evidence.

## Reproducibility and handling
Public full-corpus and PDF verification metadata are supplied separately. No dataset record, copied source, extracted text, screenshot, private-extract metadata or coordination material is included. The negative literature search is bounded as of 2026-10-21, not a novelty certification.
