# Fresh independent priority and scope audit

Initial checkpoint: 2026-10-17 20:26 UTC (13:26 America/Los_Angeles).

Updated checkpoint: 2026-10-17 20:28:34 UTC (13:28:34 America/Los_Angeles), after independently reproducing the primary p. 542 passage.

This reviewer searched independently before reading `CANDIDATE_PROOF.md` and `priority_independent.md`. No outside individuals were contacted; no other chats, queues, PRs, or Git state were inspected or changed. Completion estimate: 100% of this requested audit, with the literature-access limitations below. This is not completion of full mathematical/package review.

## Verdict

I found no duplicate of the candidate's all-rank, arbitrary-embedding theorem, and no known general theorem that immediately supplies it. I found no mathematical counterexample to the theorem under its **explicit** definitions of A_I and A_R. After the follow-up reproduction below, I regard the master-group coverage of the standard real interval and extended-real families as established by the accessible primary text. This is not an exhaustive certification of originality.

The strongest defensible characterization is presently: an apparently new strengthening of Gong--Yang--Zeng's September result, with standard real-family scope supported and full proof/package reviews still required. It would be inaccurate to announce either the infinite-bump normalizer idea or the six rank-one cases as new. It would also be inaccurate to claim that I independently read the complete 1999 paper: direct PDF access failed.

## Recent primary priority source

[Gong, Yang and Zeng, arXiv:2609.18630](https://arxiv.org/abs/2609.18630), submitted September 16, 2026, still displays only v1. Its [Theorem 1.1 and Remark 2.4](https://arxiv.org/html/2609.18630v1) explicitly impose rank one on the ambient slope group and restrict the theorem to six named families. The introduction expressly omits D_*H on the extended real line. The witness uses infinitely many support components descending to zero; well-ordered target support is the obstruction. Its arbitrary order-preserving embedding argument uses the first-slope description of target orders. Those restrictions are substantive.

The candidate proposes a different route around them: perfect centralizers force disjoint local supports, least local components have a uniform orientation, and bumps at both source endpoints defeat either orientation. I did not locate this combination in a primary source. It eliminates reliance on the target order entirely, so it is stronger than merely extending the September paper's order classification.

Searches specifically bounded to September 16--October 17, 2026 for Dlab group / Kourovka 21.149 / automorphism / larger conjugation returned that preprint and the known earlier formalization, not a subsequent extension. This is a search-coverage statement, not a guarantee that no unindexed or differently titled manuscript exists.

## Standard definitions: established and unestablished

[Dlab, *On a family of simple ordered groups* (1968)](https://doi.org/10.1017/S1446788700006261), [primary PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2FC98980CF8D6CE6001298088EC1E5FA/S1446788700006261a.pdf/div-class-title-on-a-family-of-simple-ordered-groups-div.pdf), treats subgroups of the positive **real** multiplicative group, without a rank-one restriction in the initial definition. Its interval elements have an affine right germ at each point below one. Thus its four interval families lie in A_I. The introduction explicitly defers generalizations to other ordered fields. I found no primary evidence that the Notebook silently quantifies over such generalizations. A manuscript should say “standard real interval and extended-real Dlab groups,” rather than suggesting a theorem over arbitrary ordered fields.

[Zenkov--Medvedev, *On Dlab groups* (1999)](https://www.mathnet.ru/rus/al2480), DOI [10.1007/BF02671746](https://doi.org/10.1007/BF02671746), is accessible here through indexed primary-PDF text. Page 538 defines D_H* by affine pieces on a well-ordered breakpoint sequence and identity on an initial ray; D_H is its bounded-support subgroup. Page 543 places the bounded-above-support D_*H inside full bar D_H. Page 542 explicitly writes every full-group element as g=U_r T_alpha d, where d belongs to D_H*, and identifies the affine germ at minus infinity for elements outside D_H*. Thus every full-group element, and each named real subgroup, lies in A_R. This conclusion follows from the factorization even without obtaining the definition's opening paragraph. I independently reproduced the complete relevant p. 542 paragraph, rather than inferring its content from a secondary source.

**Updated scope verdict:** the former left-tail gate is closed for the standard real families. The abstract all-slope master-group theorem also covers the analogous real groups with unrestricted H whenever their defining one-sided affine conditions are retained. This is a structural deduction; no extension of the rank-one order-classification theorems is being asserted.

The [2001 primary abstract](https://www.mathnet.ru/eng/al213), also [indexed by Mathdoc](https://geodesic.mathdoc.fr/item/AL_2001_40_2_a1/), lists only the six families used in the September theorem and restricts its order-classification assertions to rank one. It is not a definition or completeness certificate for all possible Dlab targets.

Exact search queries that exposed useful primary excerpts were `"Длаба" "538" "носитель"`, `"Длаба" "T_H" "2.2"`, and `"О группах Длаба" "543"`. For p. 542 I independently ran the exact three-query batch recorded in [primary_left_germ_evidence.md](../primary_left_germ_evidence.md), receiving the same mathematical paragraph and page heading. These point to [the primary PDF URL](https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=2480&what=fullt). Direct web opening and ordinary HTTP requests to MathNet timed out; Springer redirected the PDF request to the article/paywall page. No access control was bypassed. PDF-byte acquisition and visual authentication remain unavailable; this evidentiary limitation should be reported accurately, but does not create a remaining mathematical ambiguity in the returned paragraph.

## Equivalent known mechanisms checked

The candidate's slope-and-propagation centralizer argument has substantial classical antecedents. [Kassabov--Matucci, *The simultaneous conjugacy problem in groups of PL-functions*](https://arxiv.org/abs/math/0607167), [published primary PDF](https://ems.press/content/serial-article-files/29621?nt=1), discusses the initial-slope injection and Brin--Squier centralizer results. Its finite-piece PL setting is narrower than the locally right-affine master groups. It does not immediately settle arbitrary embeddings of the present uncountable Dlab group or the two-tail obstruction. The elementary centralizer fact should be presented as an adaptation of a standard mechanism, without a priority claim for that fact itself.

[McCleary (1978), *Some simple homeomorphism groups having nonsolvable outer automorphism groups*](https://doi.org/10.1080/00927877808822255), concerns bounded-support homeomorphisms and related simple groups. Its primary abstract establishes outer automorphism phenomena, but does not state the ambient-Dlab nonimplementation assertion. I did not have the full paper and cannot certify that every relevant lemma in it was excluded. An outer automorphism alone is logically insufficient here: the corrected problem expressly allows a larger target.

Queries for Dlab plus Rubin / McCleary / embeddings, and for perfect centralizers, PL diagonal embeddings, and locally right-linear homomorphisms, did not reveal a theorem implying the whole candidate. Reconstruction results about isomorphisms or normalizers would still require justification for **arbitrary** embeddings; they cannot be silently substituted.

## Mathematical scope checks made while auditing

The explicit theorem does not require a target slope-rank condition: the slope at a finite fixed endpoint maps a perfect centralizer to an abelian group regardless of rank. The source local group G(L) is perfect, so the germ is trivial and the commuting bump propagates the identity through its whole component. This is the key reason the target order is dispensable.

The two-tail modification matters. If least local components reverse interval order, a sequence accumulating only at the left source endpoint would no longer give a descending target sequence. The second tail supplies one. Any manuscript that drops that tail must replace the uniform-orientation argument with a separate proof excluding reversal.

The initial-ray condition in A_R is essential to the proof, not editorial decoration. Without it, perfect subgroups can have nontrivial action arbitrarily far left and support components need not be well ordered. The candidate itself records a twisted-diagonal obstruction in that larger category. Therefore an uncertain Dlab definition cannot be resolved merely by enlarging A_R to all finite-point locally right-affine maps.

I found no defect in these points, but did not perform the requested fresh full-package proof review or reproduce a compiled manuscript in this scope audit.

## Access and promotion limitations

Direct zbMATH access to 0937.06016 was unavailable; MathSciNet full reviews were not available. Public indexed queries to those domains yielded no additional relevant result, which must not be described as having searched their full subscription databases. General search results produced considerable unrelated “D-Lab” material. The audit is therefore stronger on the identified primary articles and their exact stated restrictions than on proving exhaustive absence.

Before using `solved_verified` for the full Notebook problem, enumerate all included standard target families; preserve the higher-rank/all-embedding quantifiers in the theorem; credit the September paper prominently; and complete fresh independent proof/package reviews. The primary-text follow-up now supports the Kourovka scope implication for the standard real groups. The lack of an accessible exhaustive database search remains an originality limitation, separate from that scope verdict.
