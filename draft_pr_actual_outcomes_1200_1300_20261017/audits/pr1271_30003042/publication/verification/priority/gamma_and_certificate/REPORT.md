# Independent priority audit: gamma filtration and finite certificate

This initial report was completed without reading the new lineage family or new root priority findings. The mathematical gate is an input premise, not something this priority audit independently reproves. Search cutoff is 17 October 2026 in the project timezone; the observed UTC retrieval date is 18 October. No outside person was contacted.

## Target and decision

The exact claim is the existence of a nondegenerate 17-dimensional quadratic form phi over F with ind C0(phi)=256, K=F(SB(C0(phi))), X=OG8(phi), and e8 in gamma^5 K(X_K). This contradicts OWR 2016 Conjecture 3 and A Conjecture 4.7. It does not assert an exact gamma depth, every n>=8, or an index theorem newly proved by this project.

**Priority is not cleared.** The underlying index result and the pointwise passage from index failure to gamma membership are published. No later primary text explicitly restating this exact n=8 negative membership was located in this audit. That is a scoped search result, not a proof of firstness or of current openness. The proper description is a literature-derived negative corollary, accompanied by independent verification artifacts whose exact priority remains unknown.

## Positive prior art that controls the wording

| Component | Verified earlier source and scope | Consequence |
|---|---|---|
| Original nonmembership and pointwise implication | [A](https://sites.ualberta.ca/~karpenko/publ/a16i5.pdf), pp. 11–12 | The transfer/incidence argument already explains how a failure at dimension 18 gives the prohibited membership at n=8. This is more specific than a universal contrapositive. |
| Index 8 input and finite computation | [K](https://sites.ualberta.ca/~karpenko/publ/spindI15.pdf), §§4–6, Appendix A; [published record](https://mat.uab.cat/pubmat/articles/view_doi/10.5565/PUBLMAT6722310) | Credit Karpenko for the Spin17/18 indices and original computation. |
| Analytic proof replacing the critical computation | [I](https://sites.ualberta.ca/~karpenko/publ/spind18-04.pdf), Theorem 4.1 and Corollary 4.4 | The computer-free critical bound was already supplied by Karpenko in the28 August 2023 preprint, published in 2024 with 2025 English translation. It is not a project contribution. |
| Pairing and degree framework | [D](https://sites.ualberta.ca/~karpenko/publ/duality14.pdf), pp. 1–5 | Integral duality and the symplectic comparison, including degree normalization, are prior machinery. |

The analytic paper's full author preprint was read. It identifies the earlier computational dependence, supplies a distinct argument, and gives the dimension 18 exponent list. It cites A, but I did not find an explicit statement there that the original gamma conjecture is false. A itself prints the conditional pointwise counterexample mechanism. Combining these published ingredients needs accurate field/genericity bookkeeping, already accepted by the supplied gate; the combination cannot be marketed as a new Spin theorem or a novel proof of that bound. Whether this exact corollary was printed elsewhere first remains unresolved.

## Certificate provenance

The proposed verification certificate uses Y=IG(5,16)=Sp16/P5, x=x1+...+x5 and the product a of the eight factors x±y1±y2±y3. Its correct relation is a=2^8*ztilde. For b=a/128 the supplied certificate gives

    integral_Y a^3 c2(T*)^9 c3(T*) = 14668659594398531584
                                 = 2^22 * 3497280977821,
    integral_Y b^3 c2(T*)^9 c3(T*) = 6994561955642.

The proposed odd-orthogonal rational zero-cycle has degree 27978247822568=8*3497280977821. These values and the explicit b^2-even identity are accepted from the supplied mathematical validation; this audit independently checked only the displayed integer ratios and dimension count45=24+18+3, not the integral from scratch.

K Appendix A already specifies this same product a, the typeC8 parabolic with fifth vertex deleted in ordinary numbering, the eight-term Schubert expansion divisible by 128, and the nonzero reduction of b^3/2 modulo2. Thus the precise class valuation 22 is already published. The inspected journal Appendix A, printed pp. 753–754, agrees. Both versions have an apparent prose normalization 2^3*ztilde beside the eight-factor formula; the formula has2^8. No official erratum or first identification of that discrepancy is established here.

What differs in the supplied certificate is an explicit Chern-monomial complementary pairing and integer degree witness, plus an independently executed, inspectable calculation and explicit lower-divisibility identity. The pairing witnesses a suitable complement in the existing duality proof. Reproducing a known valuation with different computation can improve reproducibility, while supplying no automatic theorem novelty. I found no exact integer or exact matching pairing in the retrieved sources or indexed searches. The eight-factor construction and its normalization should never be presented as invented here. A claim that the explicit b^2 identity is new would also require further priority evidence.

## Standard methods and a remaining specificity issue

[BKT](https://www.math.umd.edu/~harryt/papers/qprig3.pdf), §§1.1–1.3, gives established integral symplectic Schubert/Pieri rules and a ring presentation. Its distinction between quotient-bundle special classes and Chern classes of the dual tautological subbundle matters when describing c2(T*) and c3(T*). Calling every one of these classes a one-row special class would obscure that distinction. [GPS](https://www.math.lmu.de/~geldhauser/publ/shell.pdf), §5, gives established equivariant restriction and multiplication algorithms, and is explicitly cited in K for the original software. Neither integral Pieri recurrence nor localization/root enumeration is a novel mechanism merely because independently implemented here.

The exact complementary monomial, its pairing value and the resulting specific zero-cycle are more specific than these general algorithms. Their occurrence elsewhere is **unknown**. Searches for the four full decimal integers, selected integer fragments, normalized forms, IG(5,16), Sp16/P5, and Chern-degree variants produced no verified earlier match. These results do not search every symbolic presentation or software output. The strongest defensible certificate claim is independent verification of a previously published mathematical fact with the displayed witness.

## Adversarial exclusions and current literature

Yagita's [Y](https://arxiv.org/abs/1811.08288), Karpenko's [Y0](https://sites.ualberta.ca/~karpenko/publ/yagita06.pdf), Baek–Karpenko [BK](https://sites.ualberta.ca/~karpenko/publ/yagita2-05.pdf), and Baek–Devyatov [BD](https://aif.centre-mersenne.org/articles/10.5802/aif.3725/) concern injectivity/isomorphism of CH to the graded ring of the topological filtration. Their Spin17 labels and e8 symbols are insufficient to identify the present target. The checked Y section 10 witnesses involve products of Chern classes and a different motivic notation, rather than the single special K-class of the original conjecture.

The official BD page now gives final issue 76(3)(2026), 907–943, published 10 July 2026, after its 1 August 2025 online-first appearance. The 2026 [PWZ preprint](https://arxiv.org/abs/2602.07965), submitted8 February 2026, also addresses the CH-to-graded conjecture; it supplies new cases including Spin15, not an identified resolution of the exact target here. These distinctions prevent borrowing their priority claims or their former open-case lists for this problem.

The current author [publication index](https://sites.ualberta.ca/~karpenko/publ/) displays 14 September 2026 as its update. Its 2026 subcritical-exponent paper was followed to the24 May 2026 final preprint. That introduction studies a different deviation beginning at dimension 33. Other scoped checks covered the author's representation-ring filtration paper, notes on spin Grassmannians, special Clifford characteristic classes, characteristic classes modulo torsion, and the 2022 index paper. None yielded a verified explicit restatement of the exact negative gamma conclusion in the inspected passages/full-text searches. These are access-scoped findings, not universal absence assertions.

## Search and evidence limits

QUERY_LEDGER contains 72 actual, distinct literal queries in 18 four-query calls. Returned URLs are batch unions because the provider combines results; no per-query attribution, number of papers read, or exhaustive-result count is inferred. Query wording includes English, French and Russian terms, gamma/lambda/Schubert/K-theory variants, direct conjecture numbers, dimension-specific variants and exact certificate values. Raw provider responses, downloaded PDFs, extracted text, source HTML and page images are ignored local evidence and are excluded from the public manifest.

SOURCE_LEDGER records 20 selected primary sources with manually verified metadata, byte identities, actual inspection scopes and limitations. The proposed source path filtrations14.pdf returned 404; the correct br15.pdf was then obtained from the author's actual link. The software-page download returned 502; the software was not run. Relevant paper bodies were successfully obtained. This audit did not exhaustively traverse citation databases, inspect Russian full texts, audit every proof of every adjacent paper, or prove the absence of unpublished/unindexed prior work.

## Recommended publication language and exact remaining gap

Describe the work as an explicit, independently verified derivation of the n=8 negative corollary from Karpenko's published results, with new-to-this-package finite verification witnesses. Attribute the bound and its analytic proof to their actual sources. Do not say the conjecture was open until this work, that this is its first disproof, that valuation 22 is new, or that the witness is the first computation of its kind.

The remaining priority gap is evidence establishing whether an earlier text already states the exact gamma membership, and whether an earlier computation contains this particular integral pairing/zero-cycle or the b^2-even identity. The search found no verified exact match but cannot close either gap. Mathematical validity and firstness are separate outcomes.
