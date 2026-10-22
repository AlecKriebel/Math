# Independent priority audit: recent surveys and primary papers

Disposition: **BOUNDED_NO_FIND_FULL_TARGET**. No earlier full solution, set-only solution, proper-class solution, or fully checkable equivalent consequence was verified in this search family. This is a bounded no-find, not a novelty certificate or a claim that the question is currently open.

## Exact scope and independence

The source-first scope is in `SCOPE_AND_PLAN.md`; its SHA256 is recorded in `disposition.json`. The primary OWR 60/2016 Kaplan–Ehrlich contribution, pp. 3354–3356, and Ehrlich–Kaplan II §9, Q 9.1, agree: a discrete **initial ordered additive subgroup** of No is to be order-group-isomorphic onto a new **initial** subgroup lying in Oz. In EKII the background is NBG with global choice and classes include sets and proper classes (§1, p. 2). The trivial group is harmless and separate. Initiality is closure under sign prefixes, not convexity in the numerical order. Neither multiplicative closure nor preservation of the source simplicity relation is required.

Scope and plan were sealed before reading the candidate or any historical priority assertions. Only `inputs/PROOF.md` was subsequently read. Its internal-acceptance and historical-search assertions were disregarded; no root/sibling priority verdict was read. No external individual was contacted. No Git, index, PR, release, publication, or Sheets mutations were performed. All work is inside this family folder.

Primary question sources:
- [OWR report](https://ems.press/content/serial-article-files/46663), DOI10.4171/OWR/2016/60, report 2016; publisher records publication21Dec 2017.
- [EKII author manuscript](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf), JSL83(2018)617–633, DOI10.1017/jsl.2017.9. The fetched author PDF has 16 pages and no publication-date line; search-cache versions can have different pagination. The local byte pin controls this audit.

## Strongest verified partial priority

EKII Proposition 5.2 and its full proof (§5.1, p. 10 in the fetched PDF) already characterize the least positive element in the required form 2^(-n)·omega^(-alpha). Combined with Theorem 5.1 and Lemma 5.1, the bottom-exponent/coefficient reduction used in candidate Lemma 1 is therefore established input or an elementary consequence. That reduction should not be promoted as the principal new discovery.

A second explicit precursor is [Aschenbrenner–van den Dries–van der Hoeven, The surreal numbers as a universal H-field](https://arxiv.org/abs/1512.02267), arXiv v3 11Aug 2016, JEMS21(2019)1179–1199. Lemma 3.2, p. 11, proves that a least element of an initial exponent subset is a negative ordinal. Its complete short proof was read. The surrounding construction concerns real-coefficient initial Hahn groups and associated fields; it does not normalize arbitrary discrete initial groups into Oz. The lemma is formulated for an initial **subset** I. Its elementary reasoning is relevant beyond that setting, but no stronger class statement is being attributed to its wording.

## Strongest recent leads and exact gaps

**Tree/substructure route.** [Bagayoko–van der Hoeven, Surreal substructures](https://arxiv.org/abs/2305.02001), arXiv v1 3May 2023, published FM266(2024)25–96, online1July 2024. Read the complete relevant proofs of Propositions 4.6–4.7 and Theorem 6.7, with Remarks 4.8/6.8 and the Oz partition example. These results give order/simplicity parametrizations and simplest representatives of convex partitions. They do not assert preservation of addition or the required one-sided ancestor condition for arbitrary exponent re-embedding. Their generic initial-copy statement alone supplies no such compatibility. The 2022 author version and the corresponding 2022 thesis contexts were also screened. Published-paper metadata was verified at [the publisher](https://www.impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/266/1/115480/surreal-substructures); the publisher full text was not authenticated.

**Hahn lift route.** [Kaplan–Krapp–Serra, Decomposing the automorphism group of the surreal numbers](https://arxiv.org/abs/2509.22374), v3 23Apr 2026 (v2 2Jan 2026 also acquired). Proposition 3.9, pp. 6–7, was read with its full proof and conventions. It explicitly describes order-preserving external additive automorphisms via exponent order automorphisms and positive coefficient scalings. The outstanding issue is the image subgroup's initiality. The theorem does not provide a choice of exponent map satisfying the candidate's normalization and one-sided ancestor control.

The following independent checks prevent conflation of these routes with a full solution:

1. An arbitrary exponent order relabeling need not preserve initiality: exponent translation y↦y+1 lifts to an ordered additive automorphism of the full Hahn group, but sends the initial subgroup Z to omega·Z. The latter omits 1 although 1 is a simplicity predecessor of omega. The example is a deduction in this audit, not a claim that the cited theorem contains it.
2. A literal order-and-simplicity isomorphism between initial exponent trees fixes their root 0. If a source tree has minimum m<0, that kind of isomorphism cannot put every exponent at or above 0. The candidate permits the source tree structure to change; the required weaker right-predecessor implication needs its own argument.
3. An arbitrary order-class realization theorem does not control new right ancestors. EKII's remark following Corollary 5.1 explicitly warns about the dyadic coefficient obstruction when changing exponent realizations.
4. EKII Theorem 6.2, whose full proof was read, assumes an initial **subdomain**. Its least positive element is 1. The original question follows precisely because discrete initial additive groups need not be contained in Oz. The dense-group/model obstruction in §8 also has different hypotheses and conclusion.

The candidate-specific central step that this family did not find earlier is an exponent re-rooting from minimum −alpha to 0 whose initial image introduces no new right ancestors, followed by scaling only the bottom coefficient group and transporting the source supports. Ordinary Hahn transport is established machinery; no source examined here was verified to package those steps into the full target.

## Coverage and limits

The exact query log contains **48 query inputs in 12 search batches**, including exact question searches, variants concerning omnific/initial/Hahn groups, re-rooting and right ancestors, current author bibliographies, and post 2018 survey/monograph/preprint leads. Repeated URLs and versions are deduplicated by work: **16 unique primary works assessed**, **15 with full text acquired**. Reading was selective, not cover-to-cover. There are 17 PDF acquisitions because two works have multiple versions. Bibliography pages and publisher landing pages are navigation evidence, not extra mathematical works. The work-by-work scope, dates, set/class scope, and assessment are in `work_catalog.json` and `reading_scopes.jsonl`.

Recent survey/expository contexts examined additionally include Berarducci 2020; Ehrlich 2018/2021; the Ehrlich subsection in the AMS 2022 Conway retrospective; Ehrlich–Kaplan 2021 exponential fields; Berenbeim 2022 and Bagayoko 2022 theses; Bagayoko–van der Hoeven 2023 hyperseries; Bertram 2025; and Pąk–Kaliszyk 2024 formalization. None was verified to contain the target result within the recorded reading scope. Fulltext keyword screening, especially of long theses, can miss alternate wording and is not itself a proof of absence.

Material access/unread limits:

- [Ehrlich's 2024 handbook chapter](https://doi.org/10.1007/978-3-031-40846-5_54) is directly relevant. The public abstract and references were read, but the PDF endpoint returned HTML/access content. Full chapter remains unread. An earlier living-entry 2021/2022 version is separately identified in search results and was not obtained. This gap precludes an exhaustive priority claim.
- IMPAN's published 2024 Substructures text requires institutional access; the audit relies on pinned primary author manuscripts 2022/2023 for proof content.
- The Bertram author PDF failed certificate validation; arXiv v2 succeeded. AMS web tool returned403, but direct primary PDF acquisition succeeded. The Westlake mirror returned403. Berarducci's bibliography direct download failed DNS; web search returned its indexed primary author listing. A guessed Bagayoko research directory failed in the web tool; the actual linked research page succeeded.
- Recent omnific factorization/refinement claims and other weak search leads were not fully audited because their stated conclusion is multiplicative refinement, not this additive initial-copy problem. No human input was sought or prepared.
- No exhaustive citation index, non-English corpus, inaccessible or unpublished literature search was completed. A different proof could have appeared under terminology not reached by these queries.

The proper-class component is explicitly retained in the target and in classification. No set-only theorem has silently been promoted to a class theorem. Source scope, bytes, SHA256 pins, access failures, and all retained evidence are recorded in `sources.jsonl` and `ALL_EVIDENCE_PIN_RECEIPT.json`. Third-party bodies and extracts are confined to ignored `private/`; public files contain authored analysis and metadata.
