# Complete local rings from their quotients: the source already gives a negative answer

**The unrestricted question in 30000671 / OWR-1453-004 is already answered negatively by examples credited to Ofer Gabber.** The original 2007 report states this immediately after posing the question. This package corrects the imported open status; it makes no new-discovery claim. Separate adversarial source review passed; see [the report](review/REVIEW.md).

## Exact question

For complete local Noetherian rings $A,B$ with maximal ideals $\mathfrak m,\mathfrak n$, assume
$$
A/\mathfrak m^r\cong B/\mathfrak n^r\qquad\text{for every }r\geq1.
$$
The question is whether $A\cong B$. It does not require the displayed isomorphisms to commute with the reduction maps. It does not assume a finite residue field, a fixed coefficient field, or that the rings are integral domains. The usual commutative-algebra setting of the source is retained; no noncommutative generalization is asserted.

“Finite quotients” in the imported title refers to finite-order, Artinian quotients. They need not have finitely many elements: already the quotient at $r=1$ is the possibly infinite residue field.

## What the original source actually says

Lou van den Dries's contribution, “Isomorphism of Complete Local Noetherian Rings and Strong Approximation,” is on printed **p.106** of [Oberwolfach Report 2/2007](https://publications.mfo.de/bitstream/handle/mfo/2988/OWR_2007_02.pdf?isAllowed=y&sequence=1), *Model Theory and Groups*, pp.83–138, DOI [10.4171/OWR/2007/02](https://doi.org/10.4171/OWR/2007/02). The entire contribution and its references were read, and the page was inspected visually.

After attributing the question to Angus Macintyre, the report states:

- Van den Dries obtained an affirmative answer when the residue field is algebraic over its prime field
- Gabber gave counterexamples in equicharacteristic zero with residue-field transcendence degree one over $\mathbb Q$, and in positive equicharacteristic with infinite transcendence degree over $\mathbb F_p$
- Those counterexamples are not integral domains; the report then identifies the domain restriction as a remaining question at that time

The supplied dataset preserved the initial question but omitted these decisive qualifications and the already stated negative answer. This is a source-status error, not merely a later theorem missing from a recent literature search.

## Published corroboration and access limit

Van den Dries subsequently published **“Isomorphism of complete local Noetherian rings and strong approximation,” Proceedings of the American Mathematical Society 136(10) (2008), 3435–3448**, DOI [10.1090/S0002-9939-08-09401-X](https://doi.org/10.1090/S0002-9939-08-09401-X).

The author's [University of Illinois publication record](https://experts.illinois.edu/en/publications/isomorphism-of-complete-local-noetherian-rings-and-strong-approxi) provides the complete abstract and journal metadata. Its abstract repeats both the algebraic-residue-field affirmative theorem and Gabber's negative answer in general. The [Celebratio Mathematica bibliography, item 90](https://celebratio.org/vandenDries_LP/article/788/) independently confirms that publication identity.

The full 2008 article was **not retrieved**: the publisher page returned 403 and the PDF was inaccessible through the available web tool. Accordingly, this package does not claim to have reconstructed or independently verified Gabber's examples, or to have read the full proof of the positive theorem. The classification as previously answered is supported directly by the full original report, and corroborated by the published article's institutional abstract.

## Compatibility is a substantive extra assumption

If one instead assumes a compatible family of quotient isomorphisms, taking inverse limits immediately gives an isomorphism
$$
A\cong\varprojlim_r A/\mathfrak m^r
\cong\varprojlim_r B/\mathfrak n^r\cong B.
$$
The middle map is induced by the compatible isomorphisms; their inverses are compatible as well. Completeness gives the outer identifications. This elementary observation does not answer the original question, because levelwise existence does not assert that such a compatible family can be chosen.

Similarly, imposing integral-domain or residue-field assumptions would change the target. We make no claim here about the current status of the separate domain-restricted problem mentioned in 2007.

## Disposition

Recommend **already_solved**, meaning that the unrestricted yes/no question has a prior negative answer. Credit for the counterexamples belongs to Gabber, as reported by van den Dries. Zero new substantive proof attempts were used. There is no new counterexample, numerical proof, or historical-priority claim in this package.
