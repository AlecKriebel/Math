# Leung fixed-area lead: independent bounded priority supplement

Completed 2026-10-17 UTC. Source PR1136 head supplied as `cbbe7826cca914588018c840ba99c6b7a59fa7f5`, created 2026-10-10. This sibling audit does not modify the sealed `priority_classification_01` audit. Its public files were hashed at entry and checked again at exit.

## Result

**Two distinct Leung preliminary-report records are verified at title/bibliographic level, including an earlier 1990 record. The exact abstract pages have been located, but their mathematical contents remain unread here because the available scanned issue bodies are restricted. No subsequent primary paper was identified as a continuation. The lead remains substantively unresolved.**

This is neither an identified pre-PR full-target solution nor a verified exclusion of one. Do not promote the target as historically novel on the strength of this search. A public statement of bounded priority review should disclose that the two Leung abstract bodies were not inspected. The mathematical bridge already checked in the sealed audit is unaffected; this supplement concerns historical coverage.

## Verified records and distinct dates

| Record | Program evidence | Abstract pointer independently verified | Exact body location |
|---|---|---|---|
| 1990 | AMS Notices, February 1990, printed p. 159; Y. J. Leung, University of Delaware; abstract number 855-30-175 | AMS annual author index for Abstracts vol. 11 (1990), printed p. 546, rendered PDF p. 30: title entry points to p. 181 | Abstracts vol. 11, March 1990, issue 68, p. 181; scan leaf 28 |
| 1992 | AMS Notices, October 1992, printed p. 869; Yuk Leung, University of Delaware; abstract number 876-30-195 | AMS annual author index for Abstracts vol. 13 (1992), printed p. 566, rendered PDF p. 30: title entry points to p. 440 | Abstracts vol. 13, October 1992, issue 83, p. 440; scan leaf 27 |

The mapping from each program identifier to its annual-index page pointer is a match of author, title and year; it is not a direct reading of the identifier on the unread abstract body.

Both entries use the title *On a fixed area problem* and are labeled preliminary reports. These are distinct program identifiers and distinct dated index entries. Neither entry alone establishes whether the mathematics is the same in both talks, whether either concerns the target, or whether either claims a complete solution.

Primary publisher program URLs: [February 1990 Notices](https://www.ams.org/journals/notices/199002/199002FullIssue.pdf) and [October 1992 Notices](https://www.ams.org/journals/notices/199210/199210FullIssue.pdf). In this supplement the displayed program passages were available only through indexed search excerpts at these primary URLs; direct opens and downloads returned HTTP 403. I therefore do **not** claim to have freshly read their entire pages or downloaded publisher originals.

Publicly downloadable scans of the primary annual indexes were obtained from the Internet Archive's microfilm collection: [1990 volume 11 index](https://archive.org/details/sim_abstracts-of-papers-american-mathematical-society_1990_11_index) and [1992 volume 13 index](https://archive.org/details/sim_abstracts-of-papers-american-mathematical-society_1992_13_index). Both index PDF pages were rendered and visually checked; OCR alone was not used to authenticate the page references.

Issue identity and leaf positions were determined from public item metadata and its explicitly non-private `scandata.xml`: [March 1990 issue metadata](https://archive.org/metadata/sim_abstracts-of-papers-american-mathematical-society_1990-03_11_68) and [October 1992 issue metadata](https://archive.org/metadata/sim_abstracts-of-papers-american-mathematical-society_1992-10_13_83). The March 1990 scan's numbered range is 156-239 and includes 181; the October 1992 scan's range is 415-517 and includes 440. The annual-index references and issue metadata support the exact locations, not the contents of the abstract text.

## Read scope and access boundary

For each target issue, Internet Archive metadata explicitly sets `access-restricted-item` to `true`; both its PDF and full OCR files have `private` set to `true`. No restricted PDF/OCR was requested or downloaded. Public item metadata, public page-number metadata, and unrestricted annual-index bodies were inspected. Direct web opens of the issue landing pages also failed in this environment. No credential, account, borrowing action, outreach, or alternate aggregate scan was used to obtain restricted text.

The precise unresolved checks are therefore these two short primary texts:

1. Y. J. Leung, preliminary report, abstract 855-30-175, *Abstracts of Papers Presented to the American Mathematical Society* 11 (March 1990), p. 181.
2. Y. J. Leung, preliminary report, abstract 876-30-195, the same journal 13 (October 1992), p. 440.

These are usable bibliographic retrieval targets for future authorized access. They are not proposed outreach, and no request to any person has been prepared or sent.

## Exact-target comparison

The target is

\[
\exists C<\infty\ \forall\bigl(g(z)=\sum_{j=1}^{n}\lambda_j(z-z_j)^{-2}\bigr)
\ \exists S(g),\ |S(g)|=\pi\ \forall R>1:
\quad\int_{D_R\setminus S(g)}|g|\,dA\le2\pi\log R+C,
\]

where the list is arbitrary finite, every weight is positive, their sum is one, and the complex poles may repeat. The constant must be absolute and the same set must serve every real radius.

| Required content | 1990 abstract | 1992 abstract |
|---|---|---|
| Positive normalized arbitrary weights | Unknown: text unread | Unknown: text unread |
| Squared complex poles, arbitrary/repeated locations | Unknown | Unknown |
| Exceptional set of exact area π | Unknown | Unknown |
| One set independent of R | Unknown | Unknown |
| Every real R>1 | Unknown | Unknown |
| Leading coefficient 2π and absolute additive constant | Unknown | Unknown |
| Claimed theorem versus partial progress/question | Unknown | Unknown |

The title words do not fill any of these cells. Similarity of title warrants retaining the lead; it supplies no theorem to bridge. Consequently no prior-full proof or counterproof is presented for these abstracts.

## Search for a subsequent primary paper

The actual ledger contains 65 web queries plus structured discovery requests. It covers exact title and abstract numbers; author-name variants; connections to univalent functions, Baernstein, Hayman, rational functions, Beurling, Gehring/Reich; page 181/page 440; and possible subsequent dates. General-web and alternate search-tool results mostly repeated the two programs or were irrelevant. No source was identified as a published continuation of either title.

Additional discovery coverage, with raw responses privately pinned:

- Crossref author query and an older-date author query, plus exact-title/bibliographic and fixed-area title searches. These are incomplete discovery indexes and can mix names; their absence of a continuation proves no historical absence.
- The public ORCID works endpoint for the ORCID attached to a current Leung publisher record returned an empty works list. This is not evidence that he published nothing.
- OpenAlex's ORCID-associated author record and its 33 work-title records were inspected. None was identified as the continuation. This is not a complete author bibliography or content audit, and author-cluster errors remain possible.
- Semantic Scholar author discovery returned possible identities, but paper-list requests returned HTTP 429; no full citation audit is claimed.
- Legacy University of Delaware author-page opens were inaccessible. No reliable complete author CV was obtained.

One accessible primary article was investigated as a chronological/author lead: Y. J. Leung and G. Schober, [*Some coefficient problems and applications*, Pacific J. Math. 145 (1990), 71-96](https://msp.org/pjm/1990/145-1/pjm-v145-n1-p04-p.pdf). The publisher PDF was downloaded and pinned. Its abstract/introduction, section structure and all eleven named theorem statements were inspected, with full-body text searches for target terms. It treats univalent-function coefficient variations, support-point geometry and the Nth-diameter problem; it supplies no identified full-target assertion. This excludes that inspected article as a recorded statement of the exact target. **No evidence was obtained linking that article to either fixed-area abstract**, so excluding it does not dispose of the talks.

A 2007 Leung isoperimetric-conformal-mapping title appeared in discovery metadata; its primary publisher body was inaccessible here. It was not inspected or treated as an exclusion. No theorem claim in this report relies on a third-party synopsis of it.

## Correction/supplement to the sealed earlier report

The earlier audit's 1992 title hit was correctly dated: the 1992 program and index entry both exist. The earlier report was nevertheless incomplete about the earliest located title evidence, because a separate 1990 record is now established. The separate `CORRECTION_NOTICE.md` states this coverage correction and the unresolved abstract-body gap. No silent edit was made to the earlier report or its receipt.

## Recommendation and remaining gap

At the priority gate, use **unresolved Leung primary-abstract lead, located exactly but text inaccessible**. Do not turn it into either `prior_full` or `unrelated` without the bodies. The earlier bounded finding that no full-target witness was identified remains literally true, but any presentation of that finding must now make this concrete coverage gap visible. It must not be used to certify first priority.

A sufficient disclosure is: “The bounded priority search did not identify a verified earlier full-target solution. It located Leung preliminary reports in AMS Abstracts 11 (1990), p. 181, and 13 (1992), p. 440; their mathematical text was not accessible in this audit, so their relevance remains unresolved.”

Strongest verified result of this supplement: both records and exact abstract locations, supported by visually checked primary annual-index scans and pinned public issue metadata. Remaining substantive gap: the two abstract texts and any identified continuation. Scoped goal of resolving **or honestly bounding** this lead: 100% complete. Historical relevance itself remains unresolved; this percentage does not measure resolution of priority.
