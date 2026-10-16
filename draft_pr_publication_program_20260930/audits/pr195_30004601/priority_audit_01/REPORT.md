# PR195: bounded predecessor and priority audit

Audit date: 15 October 2026 (UTC). Subject: problem 30004601, original submission `e776a961293116775fed2cb2a3019d577b84c04a`. This report is research validation, not a paper, publication decision, or claim of historical firstness.

## 1. Disposition

**No complete predecessor was identified in the bounded corpus examined. Historical priority remains unresolved.** The evidence supports describing the verified calculation as an explicit counterexample to the correctly transcribed general-dimensional conjecture, with full attribution and an express limitation on the literature review. It does not support “first,” “previously unknown,” “independently discovered,” “the conjecture was open as of today,” or a claim that the arrangement construction or proof tools are new.

The closest explicit earlier Lefschetz counterexamples were checked mathematically, rather than excluded by title, ambient dimension, or a failed exact-text search. Their relevant pure-second-variable cutoffs are 9, 7, and 5; none supplies the strict early-third-variable violation at issue here. A 2026 rank-four counterexample to a different Jacobian-ideal conjecture was also inspected in full text and distinguished by its theorem and nine-factor example.

The arrangement belongs to a classical parallel-connection construction. The residual contribution under review is the concrete generic-sectional calculation `p=8` with a degree-7 generator whose largest variable is the third variable, and its application to the stated conjecture. Even this residual is not certified historically novel by this audit.

## 2. Claim and success criteria

Let `K` have characteristic zero, `S=K[x1,x2,x3,x4]`, and let `B` be the degree-reverse-lexicographic generic initial ideal of the ambient Jacobian ideal of

`Q = x y (x-y) (x-2y) z w (x+z+w)`.

The cleared claim is `min{d : x2^d in B}=8`, while `B` has a minimal generator of degree 7 using only the first three variables and involving the third. The arrangement is central and essential. The cutoff is the second variable. The first-variable formulation in the imported record is a transcription error and its correction is not a discovery.

The mathematical input is the separately authenticated Root gate `ROOT_MATHEMATICAL_GATE_01.json` (7,426 bytes; SHA-256 `c033bcd68a3ce4809ba40916b48a5c4ad9734fa3aad07f9e6e7c60d13e1306c0`). The gate excludes positive-characteristic, complete-gin, smallest-example, and historical-priority claims. This audit does not replace it.

A complete predecessor would be an earlier public proof or reproducible computation establishing the same example, a coordinate-equivalent example, any other example that already refutes the general conjecture, or a theorem that implies such a refutation under verified hypotheses. A shared tool, a different conjecture's counterexample, a generic initial ideal that is not known to be an arrangement Jacobian gin, or failure of WLP alone is insufficient.

## 3. Target lineage and credit

The following primary locations express the same second-variable target after index/notation changes:

| Source | Exact location | Relation |
|---|---|---|
| Bigatti–Palezzato–Torielli, *New characterizations of freeness for hyperplane arrangements* | Conjecture 5.7 | Uses cutoff `d0+1`. [arXiv](https://arxiv.org/abs/1801.09868), [publisher](https://doi.org/10.1007/s10801-019-00876-9). |
| Bigatti–Palezzato–Torielli, Zaragoza 2018 | Conjecture 3.4, printed p.61 | Same target. [Primary PDF](https://eventos.unizar.es/_files/_event/_15634/_editorFiles/file/Speakers/Palezzato.pdf). |
| Bigatti–Palezzato–Torielli, RIMS Kôkyûroku 2138 (2019) | Conjecture 4.16, manuscript p.5 / proceedings p.123 | Same target; all five scanned pages rendered and read. [Primary PDF](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/2138-17.pdf). |
| Palezzato–Torielli, J. Algebra 555 (2020), 289–304 | Conjecture 7.9 | Same cutoff `d0`. [arXiv](https://arxiv.org/abs/1911.04083). |
| Palezzato–Torielli, J. Algebra 590 (2022), 215–233 | Conjecture 7.9 | Repeats target; source-record link checked in full manuscript context. [Accepted manuscript](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/91057/J.%20Algebra%20590_215-233.pdf), [DOI](https://doi.org/10.1016/j.jalgebra.2021.10.014). |
| OWR Report 5/2021 | Conjecture 7, printed p.234 | Official target, explicitly second variable. [Primary PDF](https://ems.press/content/serial-article-files/46883). |
| Torielli–Palezzato, ACA 2021 abstract | Conjecture 2.2; Theorem 2.5 | Also announces the valid three-variable case. [Primary abstract book](https://aca2021.sba-research.org/data/ACA_2021_Book_of_Abstracts.pdf). |
| Marchesi–Palezzato–Torielli, Port. Math.83 (2026), 1–18 | Conjecture 4.6; Theorem 4.7 | Zero-based variables: cutoff `x1`, witness variable `x2`; theorem covers arrangements in `K^3`. [Final PDF](https://ems.press/content/serial-article-files/52275?nt=1), [article](https://ems.press/journals/pm/articles/14299324). |

Required tool credit is broader than that target list. Galligo supplies characteristic-zero strong stability; Hilbert–Burch supplies binary syzygy-degree constraints; the generic-section identity is classical, including Conca's Lemma 1.2 and the sectional-matrix lineage of Bigatti–Robbiano, the 2017 BPT paper, and BPT Theorem 6.2. The kernel/sectional-matrix translation is existing machinery, not a new theorem. When using BPT Theorem 6.6, retain the truncation/largest-variable precision established by the separate source audit; do not apply its whole-ring divisibility wording literally to arbitrary later-variable generators.

The scalar proportionality calculation is a standard logarithmic-derivation/polar argument. Tohaneanu's discussion of linear logarithmic derivations explicitly traces the decomposition mechanism to Orlik–Terao, Proposition 4.29(3). Denham–Steiner also treats logarithmic derivations through syzygies and matroid components. These overlaps preclude presenting the basic method as independently novel. [Tohaneanu](https://arxiv.org/abs/1405.2122), [Denham–Steiner](https://arxiv.org/abs/2112.13462), [Conca](https://arxiv.org/abs/math/0210064).

## 4. Exact exclusion of the closest earlier examples

The executable `compare_known_examples.py` uses only Python's standard library, integer polynomial arithmetic, and exact rational elimination. It differentiates before sectioning and produces explicit nonzero minors. `KNOWN_EXAMPLE_CERTIFICATES.json` is deterministic and contains no timestamp. Run:

`python3 -E -S -B -P compare_known_examples.py --verify KNOWN_EXAMPLE_CERTIFICATES.json`

This performs no writes. Default execution prints the reconstructed certificate to stdout. The stored ranks below are exact specializations. The generic conclusions use the stated absolute rank bounds and nonvanishing minors, rather than treating a sample as a genericity proof.

| Prior example | Ambient rank / factors | Exact binary quotient values | Generic cutoff | Why it does not settle this conjecture |
|---|---:|---|---:|---|
| PT2020 Example 8.2 = PT2022 Example 8.4 | 4 / 8 | `H2(7,8,9)=(4,1,0)` | 9 | No third-variable minimal generator below 9. Published degree-10 WLP witness is later than the cutoff. |
| PT2020 Example 8.11 | 5 / 7 | `H2(6,7,8)=(2,0,0)` | 7 | All degree-6 gin elements lie in the first two variables; displayed `y^6 z w` has degree 8. |
| PT2020 Example 8.6 | 4 / 5 | `H2(4,5,6)=(1,0,0)` | 5 | All degree-4 gin elements lie in the first two variables; no earlier witness. |

For the eight-factor example,

`Q8=xyzw(x-y+z)(y+z-3w)(x+z+w)(x-5w)`.

The four degree-7 ambient polars are independent. At the binary flag their degree-8 multiples have rank 8 (the maximum), so generically there are no linear syzygies. Pairwise distinct restricted factors and Euler's identity imply no common projective zero of all polars, hence the binary ideal has height two. Hilbert–Burch gives three positive coefficient shifts summing to 7; with none equal to 1, they must be `(2,2,3)`. Thus the binary Hilbert values and cutoff 9 hold generically, not merely at the flag.

In three variables, degree-7 and degree-8 ranks are respectively 4 and 12, both absolute maxima. Therefore `H3(6)=28`, `H3(7)=32`, `H3(8)=33`. The multiplication kernels in the first two relevant degrees are `28-32+4=0` and `32-33+1=0`. There is no largest-third-variable generator before degree 9. Strong stability extends this exclusion to minimal generators involving later variables in these degrees: replacing later variables by the third would otherwise give an element whose minimal divisor either contains the third variable or already divides the original generator. The known WLP failure in degree 9→10 consequently does not imply an early-third-variable bound violation.

For the seven-factor rank-five example,

`Q7'=xyw(x-y+z+w)(x+v)(x+y+w+v)(z-w-v)`.

The normal matrix has rank 5, so the five degree-6 polars are independent after the displayed sections. The binary degree-7 rank is 8, the whole binary space. An 8-by-8 nonzero minor proves this remains true generically. Binary degree 6 has dimension 2, so the cutoff is exactly 7. The binary degree-6 rank equals the entire five-dimensional space of degree-6 generators of the ambient gin. Thus every such gin element lies in the first two variables, and no generator involving the third can precede degree 7. The ternary flag has one linear syzygy and `H3(6,7,8)=(23,22,21)`; this report does not infer its exact generic linear-syzygy dimension from that flag, since that inference is unnecessary for the exclusion. Rank five alone would not have excluded a predecessor to the general-dimensional conjecture.

The five-factor example is handled by the same maximum-rank reasoning: binary degree 4 has dimension 1, binary degree 5 is zero, and all four initial polars survive independently in the binary section.

**Fourteen rigid octic examples.** Janasz–Pokora's full arXiv v4 was read, including Proposition 4.1, all fourteen rigid equations/degree sequences in Section 5, Theorem 5.1 and the one-parameter discussion in Section 6. The main theorems concern nonfreeness and derivation-module type. Their defining Cynk–Szemberg class permits only double/triple intersection lines, whereas the candidate has a fourfold line. That distinguishes the candidate but does not by itself exclude an earlier refutation by a different arrangement.

The fourteen listed rigid examples were therefore checked directly. `octic_scalar_check.py` and `OCTIC_CERTIFICATES.json` give full-column-rank scalar linear-syzygy systems at a coherent ternary/binary flag for each example. The ranks are 20 and 16, so both linear-syzygy spaces vanish generically. Each pair of restricted factors has a recorded nonzero minor. The certificate uses exact arithmetic modulo 1009: the rational examples reduce directly, and the three quadratic-field examples use roots `260^2=-3` and `244^2=5` modulo 1009. A nonzero reduced minor proves the original algebraic-integer minor is nonzero in characteristic zero; the modular calculation is not an assertion about a positive-characteristic gin.

Consequently the same Hilbert–Burch argument gives binary shifts `(2,2,3)` and cutoff 9 for all fourteen. Ternary degree-7/8 ranks are maximal, giving `H3(6,7,8)=(28,32,33)` and zero kernels before degree 9. None supplies an early-third-variable counterexample. The published derivation degree sequences alone would not have justified that exclusion. Replay with:

`python3 -E -S -B -P octic_scalar_check.py --verify OCTIC_CERTIFICATES.json`

This is a bounded check of the fourteen rigid equations. It does not classify the paper's 63 one-parameter families, all values in the displayed family 266, or all possible degenerations. The displayed free degeneration is covered by the prior theorem for free arrangements. [Primary arXiv v4](https://arxiv.org/abs/2502.17031v4), [journal DOI](https://doi.org/10.4134/JKMS.j250358).

## 5. Broader constructions and current literature

**Classical family overlap.** The candidate is the parallel connection along the shared normal `x` of the four-factor pencil `{x,y,x-y,x-2y}` and the four-factor rank-three circuit `{x,z,w,x+z+w}`. Falk–Proudfoot's Section 4, especially Theorem 4.1, explicitly constructs this type of realization by identifying shared coordinates. The construction and the associated family are prior mathematics. Their bundle results do not compute the candidate's finite gin cutoff. [Primary paper](https://arxiv.org/abs/math/0002094).

**Applicable 2025 family theorem.** Migliore–Nagel's Theorem 8.11 and Corollary 8.12 apply to the candidate's unmixed Jacobian part `J^top`: there is one multiplicity-four codimension-two flat and three hyperplanes outside that pencil. Their result gives `0 → S(-7)^3 ⊕ S(-9) → S(-6)^5 → J^top → 0`. This is substantive prior family information and must be credited. It is not the four-generated ambient polar ideal `J`. Their Section 3 explicitly distinguishes the ambient Jacobian ideal after restriction from the Jacobian ideal of the restricted arrangement; Example 3.5 shows the distinction even for four general planes. Neither that resolution nor the line-arrangement reconstruction theorem 9.1 has been verified to imply the candidate's successive ambient-polar section ranks. Sections 3, 8.2, relevant examples in Section 8, and the statements of Section 9 were inspected in the full 62-page primary text; the other liaison proofs were not independently checked. [arXiv:2508.12113](https://arxiv.org/abs/2508.12113).

**Ilardi lineage and an access gap.** Ilardi's 2018 article, *Jacobian ideals, arrangements and the Lefschetz properties*, J. Algebra 508, 418–430, is a material earlier lead cited by PT2020. Its publisher abstract describes low-degree injectivity under a singular-locus dimension hypothesis, reflection line-arrangement SLP failures, and an infinite family. The full article was not obtained: the official IRIS record labels its postprint private/restricted; OpenAlex marks the publisher PDF bronze open access, but PDF requests failed and a direct browser visit reached a CAPTCHA, which was not solved. Public-copy, filename, title-variant and author searches found no accessible copy through the routes reached. Thus this audit does not claim to have excluded every theorem or family in that article. Its abstract alone cannot settle whether an implicit predecessor occurs there. Ilardi's accessible CIRM 2019 slides were inspected as a separate primary talk source, but do not substitute for the article. [Publisher](https://doi.org/10.1016/j.jalgebra.2018.04.029), [restricted institutional record](https://www.iris.unina.it/handle/11588/726226), [CIRM slides](https://www.cirm-math.fr/RepOrga/2073/Slides/Slide_Luminy.pdf).

The full accessible Dimca–Ilardi preprint and the June 2026 Ilardi–Nasrollah Nejad–Tafazolian preprint were also followed up. Their central hyperplane-section criteria assume smooth hypersurfaces or isolated singularities. The candidate arrangement in projective three-space has singular lines, and these criteria govern multiplication on a hypersurface's Milnor algebra, rather than prove the needed WLP failure after a further generic section. Main hypotheses, criteria and examples were read; the unrelated moduli/GIT arguments were not independently verified. [Dimca–Ilardi](https://arxiv.org/abs/2202.02233), [2026 variation paper](https://arxiv.org/abs/2606.22587).

**Kuzmanovski 2026.** The full PDF was retrieved; the introduction, Sections 3–4, principal structural theorem statements in Section 7, and Section 11 were inspected. Theorems 1.1–1.2/7.3 concern sufficiently large initial degree with prescribed generator/regular-sequence data. Theorems 1.10/11.3 require complete intersections; Theorem 11.4 adds a sharp EGH-bound hypothesis. The candidate is a four-generated height-two Jacobian ideal of initial degree 6, so the complete-intersection hypotheses fail, and no verified large-degree threshold or EGH-sharpness premise turns those results into this finite counterexample. Lemma 4.2 and Corollary 4.3 explicitly credit Conca and Wiebe. This is related structural work, not an identified complete predecessor. The remaining proofs of unrelated EGH/shadow/Betti assertions were not independently audited. [arXiv:2608.17281](https://arxiv.org/abs/2608.17281).

**Nasrollah Nejad–Simis 2026.** Full text was retrieved and the main claims, counterexample, extension, and final historical note read. Their target is the minimal-reduction/linear-type conjectures of Burity–Simis–Tohaneanu. Example 3.4 has nine factors and a cubic-syzygy/Pfaffian obstruction; Theorem 3.5 extends that linear-type obstruction with Boolean factors. These conclusions do not supply the section ranks or the early-third-variable conclusion here. Walther's earlier non-tame nine-factor bracelet example and the tameness-dependent linear-type result were followed up in the original full text. A full computation of the nine-factor example's gin was not performed, so it is not declared to satisfy or fail the target bound. [2026 preprint](https://arxiv.org/abs/2606.18693), [Walther](https://arxiv.org/abs/1504.07164).

**Dimca–Pokora 2026.** The full plane-arrangement preprint was retrieved and its main results, coning formulas, generic-section construction, and examples inspected. It compares Hilbert functions/polynomials, Jacobian syzygies, and Betti data of Ziegler pairs; its formulas for cones require the displayed cone/product structure. They do not establish this candidate's generic ambient-polar sections. The separate nine-line mdr counterexample concerns a rank-three Generalized Terao claim; its exact claim/construction was checked in full text. Neither has been identified as a complete predecessor to the gin bound refutation. [Plane arrangements](https://arxiv.org/abs/2604.25637), [nine-line mdr example](https://arxiv.org/abs/2607.01985).

**Other citers and method sources.** Full accessible texts were retrieved for CoCoA arrangements, combinatorial equivalence under reduction, localization of plus-one generated arrangements, freeness over arbitrary fields and of multiarrangements, and Falk-invariant formulas. Their introductions, theorem statements, and relevant examples were checked; the matrix states the limits of each inspection. The 2017 thesis's sectional-matrix chapters were available through the author's public PDF in the browser, though direct local download failed. They provide earlier general tools, not an identified arrangement counterexample. The full Cioffi–Franco–Ilardi 2026 paper was retrieved and its general rational/elliptic curve hypotheses checked; those hypotheses do not identify a singular arrangement Jacobian scheme. Its separate publisher correction concerns publishing workflow, and supplies no target result.

## 6. Public chronology, with date types kept distinct

| Public record | Supported date and type |
|---|---|
| BPT original conjecture | arXiv v1 submitted **30 January 2018, 07:02:26 UTC**. |
| Zaragoza abstract | Proceedings citation **2018**; exact first-public day not established. |
| RIMS short paper | Proceedings citation **2019**, workshop **17–20 December 2018**; the current contents page labels the linked files “unissued version.” No invented first-public day. |
| BPT journal | Publisher version of record / online **26 March 2019**; issue **March 2020**. |
| PT Lefschetz paper | arXiv v1 **11 November 2019, 05:26:36 UTC**; v2 **2 April 2020, 02:29:30 UTC**; journal issue **1 August 2020**. |
| PT k-Lefschetz paper | arXiv v1 **12 March 2020, 09:27:20 UTC**; issue **15 January 2022**. Crossref record created **12 October 2021** is a metadata-deposit date, not verified first-publication timing. |
| OWR | Workshop **24–30 January 2021**; report/volume year **2021**; official EMS article page says published **15 March 2022**. Crossref has **14 March 2022**; discrepancy retained, not harmonized by assumption. |
| ACA abstract | Conference dates **23–27 July 2021** printed in abstract book; exact posting date not established. |
| MPT | arXiv v1 **26 October 2023, 21:49:45 UTC**; publisher accepted **19 September 2025**, online **27 November 2025**; Port. Math.83 issue published **17 February 2026**, pp.1–18. |
| Migliore–Nagel | arXiv v1 **16 August 2025, 17:54:23 UTC**. |
| Janasz–Pokora | arXiv v1 **24 February 2025, 10:31:16 UTC**; v4 **14 January 2026, 12:18:53 UTC**; journal citation J. Korean Math. Soc.63(4) (2026), 753–771. Internal title-page dates are not used as public disclosure dates. |
| Dimca–Pokora planes | arXiv v1 **28 April 2026**, v2 **23 June 2026**. |
| Nasrollah Nejad–Simis | arXiv v1 **17 June 2026, 05:16:18 UTC**, v2 **21 June 2026, 02:33:44 UTC**. |
| Ilardi–Nasrollah Nejad–Tafazolian | arXiv v1 **21 June 2026, 16:49:57 UTC**. |
| Cioffi–Franco–Ilardi | Publisher **6 June 2026**; workflow correction **23 July 2026**. |
| Dimca–Pokora mdr | arXiv v1 **2 July 2026**, v2 **20 August 2026**. |
| Kuzmanovski | arXiv v1 **18 August 2026, 02:24:09 UTC**. |

ArXiv histories, publisher pages, and primary PDFs were checked during this audit. Source records appear in the evidence matrix; downloaded metadata is private. The original candidate's local research log records 1 October 2026 work and expressly preserves unknown earlier interrupted effort. Those local records do not establish a first public disclosure date or independent discovery. This audit did not authenticate an external publication timestamp for PR195 or compare deleted/private sources.

## 7. Coverage, access gaps, and limitations

The query log records the exact batched queries and UTC times. Searches covered the exact polynomial and sign variants, invariant descriptions (pencil/circuit/parallel connection, rank/factor counts, degree thresholds), target numbers 5.7/4.6/7.9 and OWR 7, authors' current lists, arXiv, publishers, repositories, thesis/conference/code leads, errata terms, and citation discovery. No failed negative query is treated as a mathematical or worldwide-priority proof.

OpenAlex's returned citation lists are demonstrably incomplete: MPT2026, Kuzmanovski2026, and Cioffi–Franco–Ilardi2026 visibly cite PT2022 but were absent from its returned one-item citer list. A null-title record in BPT's list has a JSAG DOI ending `2019.9-1` that appears issue-level; its identity remains unresolved after the endpoint failed, and it is not counted as an excluded research article. The returned PT2022 citer, a 2024 Heliyon stochastic-modeling paper, was opened in full primary HTML: its reference 33 does cite PT2022, but the surrounding passages concern Shannon entropy and data models rather than a hyperplane-arrangement theorem. Database counts are discovery aids only. Indexed GitHub/code queries are not an exhaustive audit of all historical source archives, private code, or unindexed computation logs.

BPT's final publisher article is subscription-preview only in this session; its arXiv and explicitly post-peer-review/pre-copyedit Hokkaido manuscripts were inspected, while official OWR and the final MPT PDF independently state the target. The PT2020/PT2022 Hokkaido PDFs are author/accepted manuscripts, not falsely labeled final publisher PDFs; the publisher's final PT2022 endpoint returned 403. The thesis direct download returned 403, but the browser tool accessed the public 92-page PDF; selected sectional chapters were inspected there. RIMS text extraction was empty, so all five pages were rendered and read instead of silently skipped.

No exhaustive search over all coordinate transformations, all parameter families, or every theorem in arrangement theory was performed. Ilardi2018 remains a material full-text gap, and the RIMS/OIST2021 abstract link returned HTML instead of a usable PDF on local retrieval; an indexed abstract was seen but is not treated as a full paper. Janasz–Pokora's fourteen rigid examples were checked, but their 63 one-parameter families were not exhaustively checked. Their retrieved v4 PDF has an internal title date of 15 January 2026; Root observed 24 August 2026 in the HTML rendering. The arXiv history supplies the separate v4 revision timestamp; this metadata discrepancy is not resolved by reconstructing a date from either title page. Related nine-factor gin computations were not supplied by the papers inspected and were not undertaken. External specialist assessment could improve the historical audit; the project's independent-research policy reserves all communication to the human user. No outreach or outreach draft was prepared.

## 8. Exactly supported wording

Suitable factual description, subject to Root's separate package review:

> We give an explicit seven-hyperplane counterexample to the second-variable degree bound formulated by Bigatti–Palezzato–Torielli and repeated in OWR Report 5/2021. For the displayed characteristic-zero arrangement, the pure-second-variable cutoff is 8, while a minimal generic-initial generator whose largest variable is the third has degree 7. The proof applies classical logarithmic-derivation, Hilbert–Burch, and generic-section methods.

Suitable priority qualification:

> A bounded literature audit completed on 15 October 2026 did not identify an earlier complete predecessor for this specific calculation or an earlier refutation of the same general bound. This does not establish historical firstness or independent discovery. The arrangement is an instance of the classical parallel-connection construction, and the valid three-variable theorem is prior work.

Do not replace that qualification with a current-openness claim. If a complete predecessor is later found, record its exact overlap and retain only the genuinely residual verified result; publication is not automatic.

## 9. Artifact boundary

All authored outputs are confined to `priority_audit_01`. Downloaded PDFs, extracted text, page renders, citation-API responses, and publisher metadata are in ignored `private_sources/` and excluded from the public-safe allowlist. Safe metadata records URLs, versions, inspection scopes, hashes, and failures without redistributing article text. No Git/index/branch/ref operations, remote writes, releases, messages to people, publication edits, or modifications to other audit/paper folders were performed.
