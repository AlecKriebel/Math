# Primary statement validation

Retrieved 2026-10-21 UTC using the browser reader and direct PDF downloads. Hashes and byte counts are in `sources/SOURCES.json`; the PDFs and selected page extracts are preserved in the same directory.

1. **Mike Janssen, On the Fattening of Lines in P3, arXiv:1306.4387v2 (29 June 2013).** [Primary PDF](https://arxiv.org/pdf/1306.4387). PDF page 1 establishes that the base field is algebraically closed with arbitrary characteristic. Definition 1.1 defines symbolic powers by localization at associated primes and notes ordinary/symbolic agreement for a linear complete intersection. On PDF page 2, type `(d-t,d)` means `alpha(I)=d-t`, `alpha(I^(2))=d`. Definition 2.1 on page 4 defines a pseudostar by all pair intersections of finitely many hyperplanes, with no three containing a line. It explicitly allows more than three planes through a point. Theorem 2.13 on page 7 classifies ACM line unions and gives the converse.

   Question 3.1, PDF page 8, is the existence question for a non-ACM configuration of type `(d-1,d)`. Its ambient projective space and field are inherited from the surrounding paper, not restricted to characteristic zero. A negative answer would remove the ACM assumption in Theorem 2.13, as the next sentence explains. Question 3.2 on PDF page 9 separately concerns arbitrary reduced curves, so that broader curve question must not be substituted for the line-configuration target.

2. **Michael Janssen, On the fattening of lines in P3, Oberwolfach Report 9/2015, pp. 513–515.** [Primary PDF](https://ems.press/content/serial-article-files/46557). Printed page 514 is PDF page 26 (one-based), not PDF page 25. It asks whether there exists a non-ACM line configuration `L` in `P3`, with `I=I(L)` and `alpha(I^(2))-alpha(I)=1`. The same printed page defines a pseudostar as the `binomial(d,2)` pair intersections of `d` planes with no triple containing a line. The preceding theorem has an ACM hypothesis only in its forward direction.

   This short Oberwolfach contribution does not itself repeat the explicit arbitrary-characteristic convention. The candidate's arbitrary-characteristic target is supported by the original Janssen paper's convention. The line-configuration question is distinct from the reduced-curve question at printed page 515.

## Recovered quantifiers

- **Universal proposed theorem:** for every algebraically closed field k, and every nonempty finite reduced union of distinct projective lines in `P3_k`, the initial-degree gap one forces coplanarity or a complete plane-pair pseudostar, hence ACM.
- **Original existence question:** whether any non-ACM finite line configuration of the stated gap exists, in the above ambient and field setting. Establishing the universal proposed theorem would answer this existence question negatively.
- There is no requirement of real realizability, general position at points, pairwise disjointness, connectedness, a degree bound, or an ACM hypothesis on the sought counterexample.
- Empty unions cannot satisfy the stated gap when their unit ideal is assigned initial degree zero; the nonempty convention simply avoids irrelevant boundary ambiguity. Repeated line components are not part of the reduced configuration target.

This source check authenticates scope. It makes no claim about novelty, priority, or the current literature status.
