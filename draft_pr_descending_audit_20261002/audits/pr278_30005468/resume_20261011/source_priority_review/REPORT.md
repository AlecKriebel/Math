# PR278 resumed source and priority review

**Verdict: GO for merging the precisely scoped, credited application.** The result answers the literal printed fixed-polynomial question under the rational polynomial-square convention explicitly stated in the frozen preprint. It does not silently introduce a missing PSD assumption or strict minimum greater than one, and it does not claim an obstruction for every separator. No change to DOI 10.5281/zenodo.23196750 or its publication/tracker record is required by this review.

## Strongest verified claim and mechanism

Use Scheiderer's credited quartic

`f=x^4+xy^3+y^4-3x^2yz-4xy^2z+2x^2z^2+xz^3+yz^3+z^4`.

Let `g=1-x^2-y^2-z^2`, `K={g>=0}`, `p=1+f`, and give all 35 moments through total degree four by `m000=1`, `m400=-1`, every other entry zero. The data are rational. A nonnegative representing measure is impossible even on all of R^3 because its fourth x-moment would be negative. Direct coefficient evaluation gives `L_m(p)=0`. Scheiderer's real SOS theorem gives `p>=1`, and the origin gives `min_K p=1` and real membership `p in 1+Q_R(g)`.

Every rational ball-module identity for `p-1=f` would, at the origin, force the square factors' constants to vanish. Its zero quadratic part then forces every linear part to vanish. Its fourth-degree part would therefore write f as a sum of rational homogeneous quadratic squares: the product `(g-1)b_j^2` starts at degree six. Scheiderer's non-rational-SOS theorem excludes this. Thus `p not in 1+Q_Q(g)` for every finite multiplier degree. This proof permits higher-degree weighted cancellation; it never assumes such cancellation is impossible. I checked these deductions from the manuscript and primary passages; exact checker replay is outside this source-review remit.

The same moment vector has `q=1+x^4` with `L_m(q)=0` and rational factors. The vector is nonPSD because `M_2(m)[x^2,x^2]=-1`. The polynomial p itself, and `cp-1` for every rational `c>1`, are strictly positive on the ball; Powers' Theorem7 applies with the existing ball generator and provides rational factors. For `c<1`, the value of `cp-1` at the origin excludes even real membership.

## Exact source alignment

The complete Naldi contribution, printed pp.802–804 in [OWR14/2023](https://ems.press/content/serial-article-files/47007), defines every moment through degree d and nonnegative Borel representing measures. It asks about positivity certificates of the membership of a supplied rational p in `1+Q(g)`. There is no PSD restriction or demand that all separators fail. Its explicit p803 ball example is `1+(8/9)(1-x^2-y^2)`, with minimum exactly one. The argument therefore remains within the literal report's allowed normalization. I read the full operative contribution and visually inspected full pp.803–804.

The imported record 30005468 / OWR-12697710-015 similarly asks for one rational separating p whose every SOS membership certificate requires irrational coefficients. Its dated catalogue assertion of openness is not used as contemporary status or novelty evidence.

The [companion v1](https://arxiv.org/abs/2302.06927v1), p9, Definition3 requires positivity of p and `L_m(p)=0`. Corollary2 separately constructs `min_K p>1`, and Remark2 discusses that stronger construction. Its rational-certificate discussion explicitly contrasts sums of squares in R[x] with those in Q[x]. The OWR statement does not itself formally define a Q-module. The preprint is consequently correct to define rational square factors explicitly and to disclose that this is a context-supported convention, not a formal definition attributed to OWR. I visually inspected the complete companion p9 in addition to reading it.

Under the weaker convention of rational coefficients in real-SOS multiplier polynomials, the list `sigma0=f, sigma1=0` already is rational. The result would fail that different target. This limitation is prominent in the frozen manuscript, CLAIM_SCOPE, README and metadata, so no silent target substitution occurs. An unqualified claim that every rational multiplier list is impossible would be false.

## Attribution and bounded priority

I independently inspected the following operative primary passages, without upgrading those partial reads into whole-body audits:

- Scheiderer2016 Theorem2.1, its quartic construction and Example2.8: the exact quartic, Galois obstruction and real-SOS identity are classical.
- Scheiderer2000 Lemma1.1 and Proposition6.1/proof: leading forms and completion with positive generators are classical mechanisms.
- Benoist2022 Remark2.7: the rational formal-ring obstruction for the same quartic is explicit prior work.
- Nie2011 author manuscript, complete Example5.3: the homogeneous Motzkin form is excluded at every degree from the ball preordering by the same mechanism over the reals.
- Henrion–Naldi–Safey El Din2016, whole §6.2: irrational Gram points of this quartic were already examined.
- Naldi–Sinn2021, Example3.8 and immediate §3.2 setup: the same quartic already gives rational SDP data without a rational PSD separating certificate. This precludes marketing a new general irrational infeasibility phenomenon.
- Powers2011 Theorem7/Remark8 and Gram Spectrahedra v1 Lemma1.6: strict-positive rational ball certificates and rational Gram/rational square equivalence are established.

The frozen manuscript and priority note credit all these ingredients and describe an explicit fixed normalized-moment application plus scope clarification. That framing is defensible. No newly discovered quartic, new irrationality mechanism, new all-degree method, algorithm or worldwide-first result is supported.

The 11October2026 primary refresh found that the [moment arXiv metadata](https://arxiv.org/abs/2302.06927) and [descent arXiv metadata](https://arxiv.org/abs/2508.07060) each still expose only v1. This does not certify absence of a later publication. Direct current author-listing access produced HTTP200 bot-challenge HTML; it is not a publication-list read. A search presentation appeared to associate the moment title with a 2020 citation, but the [actual journal metadata](https://www.aimsciences.org/article/doi/10.3934/mcrf.2019032) identify those pages as the separate Marx–Weisser–Henrion–Lasserre PDE paper, resolving that specific apparent lead.

The [2026 corrected descent paper](https://www.sciencedirect.com/science/article/pii/S0019357726000716) still returned403 for a complete-body request. Its current primary introduction/section preview describes univariate saturation, strictly positive multivariate descent and zero-dimensional-support Archimedeanity descent, and refers to a generalization in TheoremB.1. I did not recover that theorem or the unexamined remainder. The inspected scopes do not conflict with the example: f vanishes at the origin; K has interior, so the module support ideal is zero and its support quotient has dimension three; and the ball module is already rationally Archimedean. Archimedeanity descent alone cannot establish this boundary membership. I did not infer non-overlap for unknown statements.

No exact earlier normalized-moment application was verified in the bounded primary scopes checked. Search absence, inaccessible bodies, catalogue openness and version metadata do not prove historical novelty. The preprint's dated priority note correctly preserves these distinctions, including unknown AppendixB.1 and other unexamined final/duplicate bodies. The refresh creates no material hold for the modest application claim.

## Exact remaining gap

There is no unresolved source mismatch or proof gap in the stated literal fixed-p/rational-square claim found by this review. The actual final PR bytes and resumed merge need their own integration check.

Historical firstness remains unproved: unexamined bodies, unavailable corrected AppendixB.1, unindexed and unpublished work may contain an exact predecessor. The originating authors' unstated intended restriction is unknown. A verified exact predecessor or stronger intended target would reopen the decision. These uncertainties are disclosed and prevent broad novelty or current-openness claims; they do not turn this precise application into an incomplete result. The PSD-input, strict-margin, all-separator and general Archimedean-descent variants are outside this theorem.

Outside author input could clarify unpublished intention, but this project forbids external communication; no outreach was drafted or initiated.

## Recommended final PR wording

Title: **30005468: fixed rational separator without a rational normalized SOS certificate**

Body:

> Applies Scheiderer's classical rational quartic to the literal fixed-polynomial question in OWR14/2023 p804. On the three-variable rational unit ball, p=1+f annihilates an explicit rational degree-four moment vector of mass one and belongs to 1+Q_R(g), but has no certificate with rational polynomial square factors at any finite multiplier degree. The contribution is this explicit normalized-moment application and clarification of its minimum-one boundary; the quartic and local obstruction are credited classical results.
>
> The input moment matrix is not PSD. The same vector has a rationally certifiable alternative separator, and every rational rescaling cp with c>1 has a rational normalized certificate. Merely rational coefficients in real-SOS multiplier polynomials already suffice here; the obstruction is to rational square factors, equivalently rational PSD Gram data. The result does not address the companion preprint's strict-margin regime, a PSD-input restriction, all separators, or general Archimedean descent.
>
> Written Galois and local leading-form proofs establish the all-degree conclusion; the portable supplement provides 2,059 exact finite controls. The unrefereed AI-assisted preprint and verification archive are preserved at https://doi.org/10.5281/zenodo.23196750. Its bounded priority note credits the older quartic, formal-ring, ball, Gram and SDP applications and records inaccessible or unexamined literature. No worldwide-firstness, current-openness, originating-author endorsement, human peer review or proof-assistant certification is claimed.

This wording is a recommendation, not a provider edit. Preserve the existing DOI, published v1 package and sheet record.
