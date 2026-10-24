# Bounded general recognition priority search

Checkpoint: 2026-10-24 18:17 UTC. Completion estimate: 100% of this bounded screening pass; no estimate of the mathematical discovery goal is inferred from that percentage.

## Exact target and outcome

Target: a published or preprint theorem asserting, for every finite nonabelian simple group S and every n >= 1, that any finite group G satisfying C[G] ~= C[S^n] is isomorphic to S^n; or a sufficient general theorem covering S = A7 and every n. The equivalent input is the **multiset** of degrees of irreducible complex characters, including multiplicities.

**Outcome:** no theorem with that scope was located in this bounded pass. This is a search result, not a proof of absence, an assertion that the target is open, or a novelty certification. Exact A7-specific searches and the older Azad–Khosravi papers were assigned elsewhere and are not duplicated here.

## Primary theorem whose scope was checked exactly

Bessenrodt, Nguyen, Olsson, Tong-Viet, *Complex group algebras of the double covers of the symmetric and alternating groups*, Algebra & Number Theory 9 (2015), 601–628, DOI [10.2140/ant.2015.9.601](https://doi.org/10.2140/ant.2015.9.601). Primary [arXiv v2 PDF](https://arxiv.org/pdf/1308.4388), p. 2, Theorem B:

> Let G be a finite group and H a quasi-simple group. Then G ≅ H if and only if CG ≅ CH.

The primary text on p. 3 explicitly identifies complex group algebra isomorphism with equality of character degrees counting multiplicities, and distinguishes cd from cd* on pp. 3–4. Thus the invariant matches the target. **The hypothesis does not:** A7 is covered, whereas A7^n for n > 1 is not quasisimple. This theorem is not an all-direct-powers result. The PDF metadata and journal reference are also confirmed by the [arXiv record](https://arxiv.org/abs/1308.4388).

## Later direct-power result: bounded Suzuki powers

Rashidi and Oftadeh, *Recognition of the direct products of Suzuki groups by their complex group algebras*, Journal of Mahani Mathematical Research Center 12(1) (2023), 127–135, DOI [10.22103/jmmr.2022.19218.1226](https://doi.org/10.22103/jmmr.2022.19218.1226). The DOI resolves to the primary [journal article](https://jmmrc.uk.ac.ir/article_3333.html), whose citation metadata and abstract were successfully retrieved directly. It links the [publisher PDF](https://jmmrc.uk.ac.ir/article_3333_2be9bd7a3434f7038ca27d1918de58bd.pdf).

The journal abstract states that, for q = 2^(2n+1) >= 8, recognition is proved only for exponents alpha <= p_hat(n), where p_hat(n) is the largest primitive prime divisor occurring for 2^(2n+1)-1 or 2^(2(4n+2))-1. The [author-uploaded primary full text](https://www.researchgate.net/publication/368282733_RECOGNITION_OF_THE_DIRECT_PRODUCTS_OF_SUZUKI_GROUPS_BY_THEIR_COMPLEX_GROUP_ALGEBRAS), Corollary 2.8, gives the same bounded implication C[G] ~= C[Sz(q)^alpha] iff G ~= Sz(q)^alpha. The web reader could not open the publisher PDF, so the corollary's exact location was checked in the indexed author-uploaded text. This covers neither arbitrary exponents for a fixed Suzuki group nor A7.

## Recent and equivalent-formulation checks

- Hung and Moretó, *The codegree isomorphism problem for finite simple groups*, Quarterly Journal of Mathematics 75(3) (2024), 1157–1179, DOI [10.1093/qmath/haae039](https://doi.org/10.1093/qmath/haae039). The [publisher abstract/introduction](https://academic.oup.com/qjmath/article/75/3/1157/7712335?guestAccessKey=4d5e7dd3-520c-40ab-aa3b-3f386a6d2bfa) recognizes finite simple groups by character **codegrees** counting multiplicity. Its introductory comparison confirms the known degree-multiset/quasisimple result; its target theorem has a different invariant and simple, not direct-power, comparison group. It supplies no general degree-multiset recognition theorem for S^n.
- Tong-Viet, *Huppert's conjecture for finite simple exceptional groups of Lie type*, Journal of Algebra 665 (2025), 48–71, DOI [10.1016/j.jalgebra.2024.10.042](https://doi.org/10.1016/j.jalgebra.2024.10.042). The [publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0021869324006021) uses the degree **set** and a simple exceptional comparison group. It therefore does not furnish the required direct-power statement. No extension from its simple-group hypothesis is assumed.
- Larsen, *Determining a semisimple group from its representation degrees*, [arXiv:math/0308033](https://arxiv.org/abs/math/0308033). This title is a search false positive: the primary abstract concerns **compact semisimple Lie groups**, and recovery of their Lie algebra, not the finite-group recognition target.
- Searches also found graph-and-order recognition results and direct products of non-isomorphic Suzuki groups. Those titles cannot be read as all direct powers of all simple groups. The older characteristically simple results are being checked separately by the parent.

## Exact unresolved priority gap

Hawkes, *On groups with isomorphic complex group algebras*, Journal of Algebra 167 (1994), 557–577, DOI [10.1006/jabr.1994.1202](https://doi.org/10.1006/jabr.1994.1202), was supplied by the parent as an older potentially structural source. **Its text was not accessed in this pass.** Parent reports Warwick metadata without a PDF and publisher access failure. Do not exclude this paper as irrelevant without reading its statements. It remains a priority gap and prevents any claim that all older structural recognition results have been screened.

## Search coverage and limits

Public web searches were run on 2026-10-24 in the families: “direct powers” + “complex group algebra”; “characteristically simple” + “character degrees/algebras”; “direct products of simple groups” + “character degrees/group algebras”; “finite semisimple” + “representation degrees”; degree multiset / degrees with multiplicities / degree pattern; Huppert + direct products / semisimple; recent 2021–2026 variants; and arXiv-restricted variants. Searches predominantly returned the known quasisimple theorem and bounded/product-family results above. Primary manuscripts, publisher abstracts, and publisher metadata were used for scope; third-party indexes were only leads. No proof audit, citation-complete database search, external communication, git operation, or publication occurred.

Strongest verified conclusion for the requested priority decision: the fully checked general quasisimple theorem only disposes of n = 1; the located later Suzuki-power theorem is explicitly bounded; **the all-A7-powers prior-art question remains unresolved by this search**.
