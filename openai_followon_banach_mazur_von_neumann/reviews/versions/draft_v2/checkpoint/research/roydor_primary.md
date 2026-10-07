# Primary dependency audit: Roydor ordinary Banach–Mazur stability

Audit timestamp: 2026-10-06 22:14 PDT (2026-10-07 05:14 UTC).
Researcher: internal independent source-audit agent. No outside individual was contacted.

**Verdict:** The complete primary-author CIRM slides were retrieved directly, read, and their pivotal theorem and cochain definition visually checked. They state precisely the conditional ordinary Banach–Mazur conclusion for both the algebra and its canonical predual. The journal article's full text has **not** been obtained or read: publisher access is blocked and the legitimate EBSCO alternative requires institutional sign-in. Consequently this is a verified author-slide dependency statement, not a completed published-article audit. The user's mandatory article-read condition remains unsatisfied.

Subtask checkpoint estimate: 75% of the requested dependency audit; author-slide and cb-comparator statement checks complete, journal-text/proof check incomplete. This estimate does not measure or certify the upstream cohomology proof or overall project resolution.

## 1. Sources actually obtained

1. Jean Roydor, *Banach–Mazur stability of von Neumann algebras*, CIRM, October 2020, complete 87-page PDF with presentation overlays: [author slides](https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf). Direct ordinary HTTPS retrieval using Python `urllib.request` returned HTTP 200 although the web-reading tool returned HTTP 403. The local PDF is `sources/roydor/roydor_slides.pdf`, 459,832 bytes, SHA-256 `b9202a2b4b3b50efc84a3430c593823f8c15404e83a2987be80083dc9028c36a`. Page references below are **physical PDF pages**, starting at 1; overlays repeat content, and are not journal page numbers. Text extraction used installed Poppler `pdftotext -layout`; pages 28 and 32 were rendered and visually inspected.

2. Éric Ricard and Jean Roydor, *A noncommutative Amir–Cambern theorem for von Neumann algebras and nuclear C*-algebras*, [arXiv:1108.1970v2](https://arxiv.org/abs/1108.1970v2), version dated 24 June 2013, 11 pages. [Primary PDF](https://arxiv.org/pdf/1108.1970v2), [primary HTML](https://arxiv.org/html/1108.1970v2). Local PDF: `sources/roydor/ricard_roydor_1108.1970v2.pdf`, 193,449 bytes, SHA-256 `36eb3ae3204ff33c1e44f785358d743bbaf53b5671438e7e1a9a4fff66fb8a14`. Read the introduction, cohomology/proof mechanism in Section 3, and Remarks 3.3–3.7. The exact headline and predual comparator statements are checked below.

3. Publisher-deposited [Crossref DOI metadata](https://api.crossref.org/works/10.1142/S1793525321500151), downloaded directly as local `retrieval_metadata_1.json`, 6,646 bytes, SHA-256 `f95ac0c2b0de6b22bfa50e6e61f17756afb77a7b9d5646df3882565812929711`. This verifies the bibliographic identity, not the theorem text or proof.

4. Primary CIRM conference page [meeting 2169](https://conferences.cirm-math.fr/2169.html), establishing the conference dates 12–16 October 2020 and the author/talk identity; the title page of the actual slides independently gives CIRM, October 2020.

## 2. Published article identity and access limit

Publisher-deposited metadata verifies:

- Jean Roydor, *Banach–Mazur stability of von Neumann algebras*.
- *Journal of Topology and Analysis* **14**, issue **03**, pp. **767–792**.
- DOI [10.1142/S1793525321500151](https://doi.org/10.1142/S1793525321500151).
- Published online **11 December 2020**; print issue **September 2022**. Crossref's record creation date 22 October 2020 is not itself a publication date.
- Publisher's version-of-record PDF link: [World Scientific PDF](https://www.worldscientific.com/doi/pdf/10.1142/S1793525321500151).

The publisher article page and linked PDF returned HTTP 403 using direct HTTPS requests and the web tool. A normal browser visit to the article page remained at automatic security verification; no CAPTCHA, paywall, or browser-security bypass was attempted. The independently discovered licensed [EBSCO article record](https://openurl.ebsco.com/fulltext/gcd%3A159526972) identifies the same article but the actual browser offers institutional sign-in to obtain full text; no authenticated institutional access was available in that session.

Other legitimate discovery checks: HAL exact DOI search found zero records; HAL author search for Jean Roydor found twelve works, none the target article; the author's current [IMJ institutional profile](https://webusers.imj-prg.fr/~jean.roydor/) has no manuscript link; the public ORCID works response was empty; OpenAlex's metadata identifies only the closed publisher location and no repository full text. These failed searches do **not** prove that no accessible author manuscript exists. Search results or article abstracts were not promoted to verified journal theorem text.

Remaining access gap: obtain an authorized complete journal PDF or legitimate complete author manuscript and verify the actual theorem numbering, preliminary definitions, proof, general/nonseparable scope, and the handling of type-I summands. Until then do not say the published theorem has been read or its full proof independently audited.

## 3. Exact conditional theorem verified in the actual slides

PDF pp. 28–29 state Theorem 2; pp. 57–62 repeat the theorem before outlining its proof. The fixed algebra is a von Neumann algebra \(M\), and the slides explicitly identify \(L^1(M)\) as its predual. Assuming

\[
H^2(M,M)=H^3(M,M)=0,
\]

there is \(\varepsilon_M>0\) such that for **every von Neumann algebra** \(N\), the following five assertions are equivalent:

1. \(M\) and \(N\) are Jordan *-isomorphic;
2. their underlying Banach spaces are linearly isometric;
3. \(L^1(M)\) and \(L^1(N)\) are linearly isometric;
4. \(d(L^1(M),L^1(N))<1+\varepsilon_M\);
5. \(d(M,N)<1+\varepsilon_M\).

The slide uses \(\varepsilon_M\) in its existence quantifier and abbreviates it to \(\varepsilon\) in items 4–5; that shorthand does not give a universal threshold. No separability, factoriality, injectivity, finite-type, semifiniteness, faithful-state, or countability assumption appears in this theorem statement. The comparison object remains a von Neumann algebra; it is not an arbitrary Banach space.

The slides thus directly cover canonical preduals of arbitrary von Neumann algebras, including nonsemifinite and nonseparable cases **at the stated-theorem level**. The absence of a restriction in this author's theorem does not replace checking the published proof, especially where intermediate arguments have narrower hypotheses.

## 4. Cohomology convention

PDF pp. 30–32 define the cochain space \(\mathcal L^k(A,X)\) for a Banach algebra and Banach bimodule using the phrase “the space of all bounded k-linear maps” (p. 32). The coefficient in Theorem 2 is \(M\) itself, with its usual left and right multiplication. The group is specified as kernel of the Hochschild coboundary modulo the actual range of the preceding coboundary. The slides separately introduce \(H^k_{cb}(A,X)\) by restriction to completely bounded cochains.

Therefore the intended hypothesis is ordinary bounded/continuous Hochschild cohomology with coefficient module \(M\). It is not a cb-only group, not normal-only cochains, not coefficient \(B(H)\), not coefficient \(M_*\), and not reduced cohomology obtained by quotienting by a closure of the coboundaries. Vanishing means every bounded cocycle is an actual bounded coboundary.

**Detected slide typo, visually confirmed:** the displayed positive-degree coboundary formula on p. 32 sums interior terms only to \(k-1\) and gives the terminal sign \((-1)^k\), despite taking a \(k\)-cochain on \(k+1\) arguments. Taken literally that is not the Hochschild differential. For instance its \(k=1\) expression omits the middle product term. Do not copy that formula. The standard convention intended by the surrounding Hochschild terminology, kernel/range definition, and cited literature is

\[
(\delta^k f)(a_1,\ldots,a_{k+1})=
a_1 f(a_2,\ldots,a_{k+1})
+\sum_{i=1}^{k}(-1)^i f(a_1,\ldots,a_i a_{i+1},\ldots,a_{k+1})
+(-1)^{k+1}f(a_1,\ldots,a_k)a_{k+1}.
\]

This correction is a mathematical observation of the auditor, not a verified quotation from the unavailable journal article. The journal definition must still be checked against the upstream source. The typo does not change that the actual slides explicitly distinguish all bounded cochains from cb cochains, but it increases the importance of the journal-text check.

## 5. Field, norm, and distance conventions

PDF pp. 10–19 define the multiplicative Banach–Mazur distance as

\[
d(X,Y)=\inf_T\|T\|\,\|T^{-1}\|,
\]

where \(T:X\to Y\) ranges over linear isomorphisms. These are the ordinary operator norms on the underlying Banach spaces. The slides contrast this with \(d_{cb}\) and completely bounded norms. The slide presentation is in the usual complex C*-algebra/von Neumann algebra setting; it does not contain an explicit global declaration that every appearance of linear means complex-linear. Thus complex-linearity is the ordinary operator-algebra convention here, rather than a literal field declaration checked in the journal article. The project should state complex-linear maps explicitly and verify the journal preliminary convention when it is available.

The slides do not spell out the empty-infimum convention. Taking the distance to be \(+\infty\) when no bounded complex-linear isomorphism exists is a natural explicit extension and cannot affect any strict finite-threshold implication. Isomorphisms in this formula must be bounded bijections with bounded inverse; a hypothetical discontinuous algebraic bijection is not admissible.

The theorem's hypotheses do not require the small-distortion maps to be unital, *-preserving, multiplicative, completely bounded, or weak*-continuous. These extra properties are gained or approximated during the proof, not imposed on the definition of ordinary distance. The strict inequality matters: an infimum below the threshold yields an actual admissible map with norm product below it; the theorem does not assert a conclusion at equality.

Zero-algebra boundary, checked independently: if the project permits \(M=\{0\}\), then no nonzero \(N\) is linearly isomorphic to it, and the empty-infimum convention gives infinite distance in both algebra and predual cases. For \(N=\{0\}\) the conclusion is trivial. Under the literal norm-product definition \(d(0,0)=0\), since both zero operators have norm zero; the general claim \(d\ge1\) applies to nonzero Banach spaces. If the journal excludes the zero algebra by its unital convention, the project can cover it by this separate argument without any new input.

## 6. Jordan versus isometric structure

PDF pp. 23–26 give the Kadison description of a surjective linear isometry between unital C*-algebras as a unitary multiplier times a unital Jordan *-isomorphism. They then give Størmer's central-summand decomposition into a *-isomorphism and a *-anti-isomorphism, and explain the opposite-algebra obstruction using Connes's example. Thus Jordan *-isomorphism, not necessarily *-isomorphism, is the correct ordinary-distance conclusion. A raw surjective linear isometry need not itself be multiplicative or unital.

The equivalence of algebra and predual isometry is expressly part of Theorem 2 in the slides. Independent elementary check: a predual linear isometry has an adjoint surjective linear isometry of the von Neumann algebras, so Kadison recovers a Jordan *-isomorphism. Conversely a Jordan *-isomorphism of von Neumann algebras is a positive order isomorphism; as an order isomorphism it preserves existing suprema of bounded increasing selfadjoint nets, so it is normal. Its preadjoint is a surjective linear isometry. This explains why the predual in question is the canonical intrinsic predual, not an arbitrary predual chosen for the underlying Banach space. A surjective linear algebra isometry likewise factors as a unitary multiplier times such a normal Jordan map.

The independent explanation in this paragraph is not a claim that the journal's proof was examined.

## 7. Proof-outline limitations and quantitative boundaries

PDF p. 62 outlines three steps: normalize the unit, obtain approximate Jordan multiplicativity and approximate *-preservation, then use Banach-algebra multiplication stability coming from the two cohomology groups. PDF pp. 76–80 state the bounded multiplication-perturbation theorem attributed to Johnson and Raeburn–Taylor, and explicitly point out that the Jordan product is not associative; one cannot simply transfer an associative multiplication by a nearly Jordan-multiplicative map and apply the Banach-algebra theorem directly.

PDF pp. 81–83 give an approximate central Jordan decomposition lemma with an **intermediate type-I hypothesis**: the type-I part admits homogeneous subalgebras of even degree only. It also assumes a unital selfadjoint bounded isomorphism and specific small norm bounds. The all-von-Neumann headline does not impose this hypothesis. The slides alone do not present all details needed to verify removal of that intermediate restriction, so the missing journal proof is material to a full dependency audit.

The general theorem supplies a threshold depending on \(M\). Numerical constants stated elsewhere in the slides concern type decomposition or special families of algebras and must not be transplanted to all \(M\). In particular, even if upstream vanishing holds for all \(M\), the composition alone does not give a universal positive \(\varepsilon\), an optimal threshold, or quantitative control of a resulting Jordan map.

## 8. Exact completely bounded predecessor comparison

Ricard–Roydor [arXiv:1108.1970v2](https://arxiv.org/abs/1108.1970v2), PDF p. 1, Theorem A, proves unconditionally that if \(A\) is a von Neumann algebra and \(B\) is **any C*-algebra**, then

\[
d_{cb}(A,B)<1+4\cdot10^{-6}
\quad\Longrightarrow\quad
A\cong B\text{ as *-algebras}.
\]

Here \(d_{cb}\) is the infimum of \(\|T\|_{cb}\|T^{-1}\|_{cb}\) over completely bounded linear isomorphisms, not ordinary bounded maps. No separability restriction applies to the von Neumann algebra alternative in Theorem A. The separate separable-nuclear C*-algebra alternative has the bound \(3\cdot10^{-19}\).

PDF p. 2 explains that the proof uses \(H^2_{cb}\) and \(H^3_{cb}\) and the established vanishing of cb cohomology; it explicitly distinguishes the then-unknown bounded vanishing problem. PDF p. 8, Remark 3.4, states the canonical-predual comparator:

\[
d_{cb}(M_*,N_*)<1+4\cdot10^{-6}
\quad\Longrightarrow\quad
M_*\text{ and }N_*\text{ are completely isometric}.
\]

It uses the canonical operator-space predual structures. This is stronger structural output under a stronger metric hypothesis. Since ordinary operator norms are bounded by cb norms, \(d_{BM}\le d_{cb}\); closeness for ordinary distance alone does not imply the cb hypothesis. Therefore this unconditional predecessor does not settle the ordinary target.

Remark 3.7 (same page) also records an intermediate conditional result with \(H^2(A,A)=H^3(A,A)=0\) and a **2-level matrix distance** \(d_2\), giving *-isomorphism. This is not the ordinary distance. It should not be overlooked in attribution, but it cannot replace Roydor's later ordinary-distance reduction.

The 2020 slides p. 48 mention an older/smaller cb bound \(2\cdot10^{-7}\). The complete v2 paper's Theorem A and later estimate give \(4\cdot10^{-6}\). Cite the exact v2 theorem rather than promote the slide's comparison bound as the best predecessor threshold.

## 9. Safe dependency composition and what remains unverified

The checkable conditional composition is: **if** the upstream input proves ordinary bounded \(H^2(M,M)=H^3(M,M)=0\) for each complex von Neumann algebra, **and** Roydor's published theorem has the same scope as the retrieved author Theorem 2, then both requested ordinary algebra and canonical-predual local rigidity statements follow immediately, with one threshold \(\varepsilon_M\) for each fixed \(M\).

The new role of a valid upstream theorem would be to remove the vanishing hypotheses in an established reduction. It would not invent the reduction, and it would not constitute an independently new cb stability theorem. This report neither validates the upstream proof nor establishes current priority/novelty of the resulting unconditional consequence.

| Dependency item | Strongest checked evidence | Status / exact gap |
|---|---|---|
| Journal bibliographic identity | Publisher-deposited Crossref record | Verified |
| Ordinary H2/H3 coefficient M | Complete author slides pp. 28–32, visually checked | Verified as author statement; literal displayed differential has typo |
| Algebra + canonical-predual conclusion | Complete author slides pp. 28–29, 57–62 | Verified as author statement |
| No separability/type restriction in headline | Same theorem in actual PDF | Verified at slide-statement level; journal proof not inspected |
| Complex field / empty-infimum convention | Standard complex C*-setting; ordinary norm formula in actual slides | Complex convention inferred; exact journal preliminary declaration pending |
| Jordan/isometry equivalence | Theorem 2; Kadison/Størmer slides; independent order/adjoint explanation | Checked, subject to journal-text condition |
| Published ordinary proof and intermediate type-I reduction | Not obtained | **Unresolved source-access gap** |
| Unconditional cb predecessor, including predual | Complete arXiv v2 pp. 1–2, 8 | Verified |
| Upstream all-M bounded cohomology vanishing | Outside this source-audit subtask | Must be audited independently |
| Unconditional ordinary publication readiness | Requires all above and upstream validation | **Not established** |

## 10. Rights and reproducibility

Downloaded third-party PDFs, extracted text, rendered slide images, and full service responses are retained locally for verification only and are excluded from Git and the Zenodo payload by `sources/roydor/.gitignore`. No redistribution permission was identified for the CIRM slides. The cb preprint uses the [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html), which licenses arXiv to distribute and does not itself grant this project a general republication license. Public citation links, factual metadata, hashes, this audit's independently written analysis, and brief attributed excerpts may be retained in the project record; the source files should not be bundled in a publication kit.

To reproduce the local statement check, retrieve the two primary PDF links with ordinary authorized HTTPS access, verify the stated SHA-256 hashes, extract using `pdftotext -layout`, and inspect the cited physical PDF pages. Poppler version used here: `pdftotext 26.08.0`. A future change of downloaded bytes requires a new hash/version record. The unavailable journal PDF cannot presently be reproduced from this record without resolving its legitimate access condition.
