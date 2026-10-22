# Fresh primary-source and repair review: PR833 / 30003711

Date: 2026-10-21 UTC. Frozen PR head: `0e6e23213494ecb4a7208f920d25d7b49502a5cb`.

**Result: no checkable replacement lower bound was recovered. Exact equality eight remains uncertified by the submitted proof packet. The verified eight-domain upper-bound construction remains a partial result; this source review does not undermine it.** The inspected arXiv lower-bound detector fails, but that is not a conclusion that the genus is smaller or that the unseen final journal theorem is false.

## Exact problem and invariant

The frozen author's PROOF.md explicitly claims ordinary unnormalized section-based Schwarz genus g(Y -> X)=8, equivalently normalized sectional category seven. Here X=CP^9 minus the cubic discriminant: smooth ternary homogeneous cubic equations modulo nonzero scalar. It is not the quotient by PGL(3,C). A point of Y is a pair (F,p) with p one of F's nine flexes. Each open domain only needs one continuous flex; domains may be disconnected.

The primary [2018 Oberwolfach report, Question 5, printed pp. 114-115](https://ems.press/content/serial-article-files/46724) uses connected open domains on which the entire cover is trivial, and records historical bounds three to nine. For this nonregular cover that literal wording imposes a stronger requirement. The frozen manuscript expressly separates it from ordinary section genus. Neither normalization nor the workshop's stronger definition removes the missing lower-bound justification for the manuscript's own exact claim.

## Version evidence

| Primary artifact | Verified content and limits |
|---|---|
| Official arXiv v1, 29 June 2023, ten pages | The same cover and section-genus convention; Theorem 1.2 states 8 <= g <= 9, Conjecture 1.3 states g=8. Its lower-bound section uses the degree-seven constant-F3 classifying-map detector. |
| Official arXiv v2, 21 July 2023, ten pages | The introduction and references are expanded. The exact lower-bound mechanism, Proposition 4.2, and proposed degree-seven detector remain the same. Theorem 1.2 and Conjecture 1.3 are unchanged. |
| Official current arXiv record | Latest is still v2 dated 21 July 2023. The 2025 revision date shown by arxiv.gg is not an official arXiv version. |
| Official AMS journal record | Proc. Amer. Math. Soc. 153(5) (2025), 2255-2267, DOI 10.1090/proc/17184; received 23 May 2024, revised 29 September and 15 October 2024, online 5 March 2025. These dates establish a later editorial version. The thirteen-page body was not obtained. |

Source links: [v1](https://arxiv.org/pdf/2306.17303v1), [v2](https://arxiv.org/pdf/2306.17303v2), [official version history](https://arxiv.org/abs/2306.17303), [AMS final metadata](https://pubs.ams.org/journals/proc/2025-153-05/S0002-9939-2025-17184-2), [Crossref's publisher deposit](https://api.crossref.org/works/10.1090/proc/17184).

The journal article is treated as a published scholarly result with its stated subject and bibliographic identity. A defect in the 2023 preprint cannot be assigned to the later proof without inspecting it. Conversely, later dates, publication, and citations do not constitute an independent check of that proof, and the abstract does not provide a replacement derivation.

## Retrieval and repair attempts

1. The official DOI resolves to the May issue and identifier `S0002-9939-2025-17184-2`. My initial guessed `-X` URL gave a 404; that error was corrected from primary metadata. The correct publisher PDF and the article's linked MathViewer both redirect to LibLynx access-selection HTML. HTTP 200 from those endpoints is not a PDF or proof-body receipt. The earlier integrated audit already had the correct identifier.
2. The [author's maintained research page](https://www.weiyanc.com/research) links the arXiv text and journal DOI, with no separate final manuscript. The [coauthor's institutional publication page](https://www.bimsa.cn/detail/zheyanwan.html) confirms the publication but supplies no final full text. The linked personal page yielded no relevant full-text copy. No login, payment, access-control bypass, or outreach was attempted.
3. Bounded searches of exact title, authors, publisher, author/institutional domains, and correction/erratum terms yielded no verified replacement lower proof or correction. That is not an exhaustive absence claim. Search snippets and third-party publication records were discovery aids only; they were not used to certify mathematical content.
4. The primary [Leary text, Theorem 2, pp. 2-3](https://arxiv.org/pdf/0711.4831) confirms that the primed relation uses x-prime squared; the Chen-Wan display has an unprimed x there, while its later calculation uses the primed version. Correcting that transcription is insufficient: the independent duality proof in DUALITY_DETECTOR_PROOF.md shows the entire H^7(BK;F3) -> H^7(PU(3)/K;F3) map is zero.
5. The newer [Chen-Gu primary preprint](https://arxiv.org/pdf/2411.00497), linked by the author's current research page to its 2026 journal article, concerns cubic surfaces and quartic bitangent/flex covers with simultaneous labeling. Its inspected theorems do not provide the missing lower bound for one flex of a cubic plane curve over this X. The normal Wiley PDF request returned 403; no final-body proof claim is made.
6. Replacing the failed detector with unspecified twisted coefficients or an unspecified other test space is a proposal, not a repair. It transfers the central difficulty to another unsupported nonvanishing assertion. This route remains blocked unless a materially new construction or verified source is supplied.

The direct duality proof was reconstructed before reading the dated integrated audit at Git `98ee5482ef3352b81758c1590a7685947eec3725`. Reading that specifically identified document afterward confirmed agreement, and it was not used as a substitute for primary inspection. The finite algebra supporting the fresh derivation is independently reproducible with check_heisenberg_extension.py and the saved result HEISENBERG_EXTENSION_CHECK.json.

## Strongest verified scope and exact gap

The strongest positive submitted result carried forward is g(Y -> X)<=8 for ordinary section genus, with the corresponding eightfold join primary obstruction vanishing, as established by the separate geometric construction and review. This family verifies the exact source identity, invariant boundary, official version history, current lawful retrieval limits, and failure of the inspected constant-F3 degree-seven lower detector.

The exact gap is a correct, checkable proof that g(Y -> X)>=8 for the same base and invariant. A legitimately available final proof or a valid independent lower-bound construction could fill it. This review does not establish genus<8, does not adjudicate the uninspected final article's truth, does not solve the stronger literal workshop invariant, and makes no novelty, priority, or exhaustive-literature claim. No solved-result acceptance is justified from this packet alone.

No individuals were contacted, no outreach draft was prepared, no unrelated project chat was read, no frozen original was changed or executed, and no PR, Git, tracker, or publication state was mutated. Source bodies, text extractions, and page renders are private and excluded by the local .gitignore. Exact retrieval hashes and read extents are in the private receipts; SHA256/size manifests seal the complete review.
