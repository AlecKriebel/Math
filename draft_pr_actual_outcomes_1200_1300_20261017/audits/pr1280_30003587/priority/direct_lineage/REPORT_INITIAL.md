# Independent direct-lineage priority audit: PR1280 / 30003587

Initial independent report. The UTC report/verdict/seal times are recorded in INITIAL_VERDICT.json and INITIAL_SEAL.md. This family did not read other families' or root mathematical/priority reports before sealing. It read the original submitted PROOF.md and its SOURCE_METADATA.json and SOURCE_VERIFICATION.md as unverified leads.

## Verdict and exact scope

**Priority remains uncleared.** No primary body inspected here explicitly states the entire target with both extra hypotheses removed. This is a bounded negative observation, not a novelty certificate. There are substantial positive predecessors, including a later general theorem that already implies the entire **outer** case without aperiodicity. A claim of a new explicit combined statement, a new theorem consequence, and a new mechanism must therefore be evaluated separately.

The target remains the original full admission claim: for every essential finite 0-1 matrix M with simple purely infinite O_M, every finite abelian diagonal quasi-free action is strongly approximately inner. For each g the implementers must belong exactly to the fixed algebra of the **whole** action. No approximate group representation is required. The present priority findings do not retroactively narrow that admission target.

## Question identity and chronology

The official [OWR report](https://ems.press/content/serial-article-files/46706), printed p2621/PDF21, was text- and visually inspected. Barlak's Question 1 has no outerness or aperiodicity assumption; its preceding paragraph requires no zero rows or columns. Its range-projection definition gives the narrower, generator-eigenvector notion. Its adjacent Theorem 2 adds both extra assumptions. The report explicitly credits Izumi for standard Cuntz algebras. This distinguishes a question from the restricted positive result printed beside it.

The [official landing page](https://ems.press/journals/owr/articles/15585) identifies volume 14 (2017), no. 3, pp2601-2629, DOI 10.4171/OWR/2017/42. The workshop was 17-23 September 2017; the report's displayed publication date is **5 July 2018**. Thus “2017 question/report” and “online publication July 2018” describe different events. An internal ISO timestamp on the EMS page is 2018-07-04T23:30:03Z; it does not change the displayed calendar date or report year.

## Barlak-Szabo version and locator reconciliation

All three arXiv bodies and the final journal body were freshly acquired. The current [arXiv history](https://arxiv.org/abs/1708.08258) lists v1 28 August 2017, v2 18 February 2018, v3 3 October 2018. The final PDF records received 14 November 2017 and accepted 4 June 2018; the [current publisher page](https://journals.msp.org/mscand/article/view/221) displays 19 October 2019. A secondary date of 7 November 2019 is not substituted for this primary date.

| Body | Title family | Relevant result labels and pages |
|---|---|---|
| [v1](https://arxiv.org/pdf/1708.08258v1), 16 pages | Purely infinite simple graph C*-algebras | Definition 2.5 p10; graph Corollary 2.7 pp13-14; classification Corollary 2.8 p14 |
| [v2](https://arxiv.org/pdf/1708.08258v2), 16 pages | Same graph title | Same relevant labels/locators |
| [v3 accepted](https://arxiv.org/pdf/1708.08258v3), 17 pages | Simple Cuntz-Krieger algebras | Definition 2.5 p10; matrix Corollary 2.7 pp13-14; graph Corollary 2.8 pp14-15 |
| [Final journal PDF](https://journals.msp.org/mscand/article/download/221/220), 17 pages | Same CK title | Matrix **Theorem 1**, graph **Theorem 2**, both p212/PDF3; their proofs pp222-224/PDF13-15; Definition 2.5 p219/PDF10 |

The old three-component mscand PDF address returned 404. The DOI landing page migrates to MSP; its displayed PDF leads to the successful endpoint above. This is the actual final typeset body, not a renamed accepted manuscript.

Every checked version retains pointwise outerness and primitivity/strong connectedness plus aperiodicity. The technical Theorem 2.6 also retains these restrictions. The v1-v2 extracted-text comparison shows support/contact and layout changes, without changing the relevant theorem. V3 reorganizes the argument around matrices. Final numbering must not be cited as “Corollary 2.7/2.8.” The accepted version cites Cartan/UCT II as reference 1; final reference 1 is Cartan/UCT I. These are genuinely different bibliographic bodies.

## Hypothesis inheritance

The final Definition 1.7/Proposition 1.8, pp214-216/PDF5-7, uses fixed **domain** projections and permits more actions than the OWR range-projection definition. Proposition 1.8(2) conjugates an abelian action to a generator-eigenvector action. The OWR actions are already of the latter form, so there is no missing definition bridge. Definition 2.5 has separate g-dependent implementing sequences in the whole fixed algebra; it does not impose representation relations.

For the candidate's return graph, applying final Theorem 2 requires independently proving the finite return graph is strongly connected aperiodic, has at least two edges, carries a diagonal quasi-free action, and has an outer restricted action. The published theorem does not supply those reductions. In particular, simplicity of the original CK algebra is not a replacement for matrix aperiodicity, and faithfulness is not a replacement for outerness.

## Positive predecessors and their exact limits

**Izumi.** [Kyoto's 2002 preprint index](https://www.math.kyoto-u.ac.jp/preprint/preprint2002.html) links the original [PostScript preprint](https://www.math.kyoto-u.ac.jp/preprint/2002/4.ps). It was acquired, rendered with a local document converter, and inspected at preprint pp13,15,27-29, including visual checks of pp13 and28. Definition 3.6 separates strong approximate innerness from approximate representability. Proposition 5.6(2), p28, and its proof p29 give strong approximate innerness for finite abelian quasi-free actions on O_n, n finite, without an outer assumption. The proof uses whole-action fixed UHF unitaries. This is a positive standard-presentation Cuntz predecessor, not every graph presentation of an abstractly isomorphic algebra. The 2004 final article DOI is [10.1215/S0012-7094-04-12221-3](https://doi.org/10.1215/S0012-7094-04-12221-3); its final PDF was not acquired, and no final printed-page identity is asserted.

**An older innerness mechanism.** Katayama-Takehana's [1997 RIMS report](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1003-6.pdf), Proposition 1.2 pp81-82/PDF1-2 and Proposition 2.6 p89/PDF9, was read (p89 also visually). For finite dimensional abelian coefficient algebra, X-aperiodicity is matrix primitivity; under that condition inner quasi-free automorphisms come from the coefficient-algebra formula Ux=uxu*. For graph edge eigenvectors this is the same type of vertex-coboundary mechanism. Its primitive assumption matters. The [1998 journal DOI](https://doi.org/10.1142/S0129167X9800021X) was located, but publisher access returned 403. I do not claim complete identity between report and final body, or that this report proves the arbitrary-period inner-kernel reduction.

**General equivariant uniqueness.** The separate [KNOWN_CONSEQUENCE.md](KNOWN_CONSEQUENCE.md) gives a checkable deduction from Gabe-Szabo, [arXiv:2205.04933v1](https://arxiv.org/pdf/2205.04933v1), Theorem 5.8 pp45-46 and Proposition 3.14 p29; compare [v3](https://arxiv.org/pdf/2205.04933v3), Theorem 5.8 p46 and Proposition 3.15 p29. The v1 timestamp is 10 May 2022, not an aggregator's 11 May announcement date. This general theorem plus an elementary equivariant path and finite averaging establishes the **outer arbitrary-period** target. It is a positive theorem consequence with a mechanism different from the candidate's return corner. It does not by itself remove a nontrivial inner kernel. Bibliographic final publication: Acta Math. 232 (2024), 1-77; this audit uses the pinned arXiv bodies for theorem locators.

**Cartan/UCT I and II.** [I, arXiv v3](https://arxiv.org/pdf/1511.02697v3), Theorems 1.7/1.8 pp3-4 and5.7/5.8 p16, and [II final](https://link.springer.com/content/pdf/10.1007/s00208-020-02022-4.pdf), Theorem 1.2 p258/PDF4, Definition 4.13 p283/PDF29, Remark 4.14/Corollary 4.15 p284/PDF30, were read. II v1 Theorem1.2 pp2-3 was also compared. These statements assume approximate representability or strong approximate innerness and add cyclic/UHF/crossed-product conditions. Their homogeneous inverse-semigroup conclusion cannot be reversed into the full CK target by dropping those assumptions. The general O_2 involution question in II Remark4.14(2) is broader than diagonal quasi-free actions; its 2020 historical open-status statement is not a current-status certificate.

**Later works checked.** Gabe, [2407.12059v2](https://arxiv.org/pdf/2407.12059v2), entire three-page body, classifies faithful standard quasi-free compact actions on O_n using representation-ring data; it cites Izumi and the dynamical KP theorem, not an extension to arbitrary CK presentations. Christensen-Neagu-Szabo, [2504.12730v2](https://arxiv.org/pdf/2504.12730v2), Definition3.1/Remark3.2 p11 and Corollary3.8 p16, checks the finite-abelian meaning while proving duality, not universal CK membership. Neagu, [2509.00829v1](https://arxiv.org/pdf/2509.00829v1), pp1-3 and Theorem3.9 pp14-16, concerns R-flows with parameter restrictions and generic conclusions. It is not the full finite-group CK theorem.

Conti-Hong-Szymanski, [1101.4210v3](https://arxiv.org/pdf/1101.4210v3), selected pp5-6,8-11,15,20, supplies diagonal/quasi-free background and outerness criteria, not an inspected full-target result. Hayashi-Hong-Szymanski, [2201.08009v2](https://arxiv.org/pdf/2201.08009v2), pp1-2 and Theorem3.3 p9, concerns non-inner conjugacy of images of diagonals, not strong approximate innerness. These statements have different quantifiers and conclusions.

## Citation tracing, theses, talks, and coverage limits

Reverse tracing followed the report's references to Izumi, Evans, Zacharias, and the early Barlak-Szabo preprint; the latter's references led to Cartan/UCT and graph endomorphisms. Evans's [official 1980 body](https://ems.press/content/serial-article-files/42034), pp915-917/PDF1-3, defines standard quasi-free automorphisms and discusses outerness and crossed-product simplicity. It does not itself supply the inspected full target. A guessed RIMS address was an unrelated 1981 item and was discarded as evidence.

Forward tracing used literal title/DOI/arXiv queries, spelling and formulation variations, an actual later graph-MASA paper, 2024-2025 classification/duality/flow papers, author publication metadata, and two citation APIs. OpenAlex and Semantic Scholar each returned zero incoming indexed records for the Barlak-Szabo record. That is demonstrably not a complete citation census: the original OWR report cites the preprint and was read here. No proof or priority conclusion is based on those zero counts.

Barlak's [2014 thesis](https://noah.nrw/ulbmshsnoah/download/pdf/4291748) was acquired; its abstract, contents and introduction were read and exact-term fulltext searches run. The inspected scope is Z^n crossed-product K-theory; no matching target terminology was found. This is not a full theorem-by-theorem thesis exclusion. Szabo's 2015 thesis was located only through author-list metadata; its body was not authenticated here. The 2017 OWR talk itself is authenticated. No separate later talk giving a complete solution was located. Exact-title/DOI erratum searches located no correction; the official arXiv page still ends at v3. This does not assert that no erratum or unindexed result exists.

The full Zacharias 2000 chapter remains a material body gap: the attempted full PDF redirected to a subscription page. The official [two-page preview](https://page-one.springer.com/pdf/preview/10.1007/978-3-642-57288-3_15), pp262-263, was actually read. Its introduction concerns generalized quasi-free definitions, crossed-product simplicity/pure infiniteness and KMS states. The uninspected remaining pages are not excluded by inference from that introduction.

## What this does and does not clear

1. **Explicit full combined statement:** not located in inspected primary bodies; novelty not certified.
2. **Theorem consequences:** the outer arbitrary-period case is already a consequence of 2022 equivariant uniqueness. Its periodic extension must not be presented as newly unavailable mathematics.
3. **Distinct mechanism:** the candidate gives a graph-return-corner route; coefficient-algebra inner implementations have an older primitive predecessor. No first-in-literature certification of the combined corner/kernel/pinch route follows from this audit.
4. **Remaining exact priority gap:** prior literature establishing the arbitrary-period inner-kernel normalization and its transfer to exact whole-action fixed implementers, or another published consequence covering that full non-outer scope, has not been ruled out. Completing the missing older bodies and a separate consequence/mechanism challenge remains necessary before promotion.

The literal query record contains 67 executed searches, with URLs and authored statuses, plus source acquisition metadata. Private PDFs, converted source documents, provider responses, extracts, differences and page images remain under _local and are excluded from the output manifest. No individual was contacted; no outreach was prepared; no git index, commit, push, release or root/current-edition file was changed.
