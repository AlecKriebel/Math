# PR781 / 4600024: bounded priority audit

Audit cutoff: 16 October 2026. Eligible immutable head: `4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f`; exactly `claimed_solved 3/5`. This audit concerns priority and attribution only. The mathematical PASS is supplied by the separate closed mathematical gate; this document adds no proof-search turn.

**Finding: no full predecessor was located in the inspected primary bodies. Priority remains unestablished.** The evidence supports describing the candidate as an authored effective reduction with expressly credited prior inputs. It does not support “first solution,” an unconditional novelty claim, or certification that Problem 16.3 remained globally open until this work.

## Exact comparison target

Input: a finite labeled presentation of a nonempty two-sided irreducible sofic shift T, and a specified onto block self-map f with a finite local rule. Mixing is Boyle's original hypothesis; the candidate also covers periodic irreducible shifts. Its test constructs the regular bad ideal B, a common recognizing monoid M, and N = max(2, ell, 4(|M|+1)). It decides existence of an SFT neighborhood on which some extension of this particular f maps into T, by testing the chosen completion F on T[N]. Equality of the output with T uses onto-ness.

A full predecessor must supply this specified-map decision/extension characterization, or a checked reduction to a prior decidable property under these inputs and hypotheses. A criterion for the existence of some map, a restricted map class, or a different inverse/section property does not meet that comparison without the missing implication.

## Primary-body comparisons

| Source and actual locator | Verified scope and comparison |
| --- | --- |
| [Boyle 2008](https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf), printed p. 17, Section 16 | Problem 16.3 specifies a surjective self-code on a mixing sofic shift, with no receptive-fixed-point hypothesis. Adjacent 16.2 quantifies over f and assumes a receptive fixed point; 16.1 concerns stable CA limit sets. The candidate addresses the former specified-map question. Historical open wording is not current-status evidence. |
| [Dykstra 2007 dissertation](https://drum.lib.umd.edu/items/66faa056-fc9f-4423-a340-1311e1a4ed6b), printed pp. 47–48, Remark 3.6.7/Problem 3.6.8 | The same neighborhood image property is called steadiness, and necessary/sufficient conditions for a homomorphism on a sofic shift are posed as a problem. This predates Boyle's survey and must be credited as earlier formulation, not mistaken for an earlier solution. The institutional record dates the thesis 2007-04-25. |
| [Ballier, arXiv1301.3790v1](https://arxiv.org/abs/1301.3790), printed pp. 9–13 | The steady-map definition is the same extension property. Theorem 2.2 assumes equal entropy and characterizes existence of a right-closing-a.e. steady factor through a right-continuing map to the minimal right-resolving cover. Theorem 3.2 characterizes existence of a right-continuing-a.e. steady factor through factoring onto that cover. Theorem 4.2 adds two-sided continuation and an AFT range. These are restricted existence results. In the continuing definition the retract condition is imposed on the ambient SFT extension, not merely on the original sofic-domain map. Lemma 2.1 is a restricted decomposition theorem, not a general recognition algorithm. |
| [Dastjerdi–Shaldehi, arXiv1505.00395v1](https://arxiv.org/abs/1505.00395), printed pp. 10–12, Theorems 4.15/4.16 | Theorem 4.15 promotes a right-continuing-a.e. factor with a specified retract to everywhere continuation when its range is an irreducible SFT. The nearby semi-open-code result supplies a.e. continuation without the missing general neighborhood extension. This does not give the target criterion. |
| [Jung, arXiv0810.4632](https://arxiv.org/abs/0810.4632), printed pp. 13,18, Theorems 4.5/5.5 | These prescribed-code extension results have an SFT target, an entropy gap, and additional ambient hypotheses (plus a cyclic condition in the irreducible case). They do not decide extension into a general strictly sofic T. |
| [Salo–Törmä, arXiv1309.2456v2](https://arxiv.org/abs/1309.2456), pp. 17–19, Theorem 1; p. 21, Proposition 6 | A specified morphism between sofic shifts has decidable split epicness: existence of a block-map section. This is a substantial nearby algorithm under comparable finite descriptions, but a section is a different property. No equivalence to the candidate's steadiness condition was found or established. The inspected version is dated 2018, while the journal bibliographic record is 2015; its statements are not silently backdated. |
| [Salo, arXiv2209.13373](https://arxiv.org/abs/2209.13373), pp. 4–5, Theorems 5/7 | Von Neumann regularity of a CA on a mixing SFT is equivalent to split epicness onto its image, and is decidable. This concerns generalized inverses of a given SFT-domain map. It supplies no inspected full predecessor for arbitrary sofic-domain steadiness. |

Ballier's publication identity is verified at [DOI10.1017/etds.2013.72](https://doi.org/10.1017/etds.2013.72): online 9 October 2013, issue May 2015, pp. 673–690. The theorem comparison above is to the actual arXiv body. The publisher PDF redirects to abstract HTML, so identity of all manuscript/VOR statements is an explicit gap.

## Prior theorem versus candidate reduction

[Place–van Rooijen–Zeitoun 2014, Theorem 4.2](https://lmcs.episciences.org/1163/pdf), printed p. 8, already supplies the LT-separation cutoff 4(|M|+1) for regular languages recognized by a common finite monoid. That theorem, its decidability, and its bound belong to those authors.

The candidate's claimed contribution is the symbolic-dynamics reduction: constructing B from the specified rule and using irreducible-language saturation to turn bounded LT separation into a canonical SFT witness. Calling this reduction “authored” identifies where its proof appears in the audited packet; it does not establish historical novelty. Standard finite automata, neighborhood approximations, and graph reachability should not be presented as new general machinery.

The terminology is older still: Ballier explicitly attributes steady maps to Barth–Dykstra 2007, [DOI10.1016/S0019-3577(07)80058-9](https://doi.org/10.1016/S0019-3577(07)80058-9). That journal body was unavailable; the independently read dissertation is evidence for the earlier definition/problem, without an asserted byte or theorem-number correspondence to the article.

## Search boundary, dates, and remaining gaps

The audit executed 52 exact web queries in 14 batches, retained in QUERY_LEDGER.json. It also followed the actual Ballier bibliography, Boyle's update page, publisher citation list, Crossref, and OpenAlex. Crossref and OpenAlex each returned 2 citations; the OpenAlex cited-by query returned the 2017 Ruivo–de Oliveira paper and the 2019/2020 Dastjerdi–Shaldehi paper. Those are catalog results, not a claim that exactly 2 later papers exist. Semantic Scholar returned 429. Boyle's update page is last revised 2016; missing 16.3 from its solved list has no 2026 certification value.

The 2017 citing paper's full body is unread (publisher 403). Published full bodies of Barth–Dykstra and Dastjerdi–Shaldehi also returned 403; Ballier's published PDF was unavailable by redirect. Additional discovered but unread bodies include Ashley 1993, Maass 1995, a 2026 rule-18 paper, deterministic-presentation complexity work, and profinite symbolic-dynamics work. Their titles or abstracts were not used to declare them non-predecessors. The separate MacDonald lead is outside this report's independent body comparison. These gaps are reasons for bounded language, not evidence of novelty.

The original proof/provenance/status packet is dated 6 October 2026 and explicitly disclaims novelty and original-solution credit. Its publication acceptance log also preserves that limitation. This audit records that documentary chronology only; it does not establish the earliest creation, disclosure, or priority date. Original triage and a finite search finding no source do not prove present-day openness.

## Disposition and custody

**Bounded priority review complete; novelty/firstness unestablished; no inspected full predecessor identified.** The mathematical scope can retain its separately verified effective-criterion wording. Preserve the explicit credit and exclusions of existential-over-f and arbitrary CA-stability claims. No Git mutation, posting, release, outreach, or external communication was performed by this audit.

Actual completed artifacts are staged in this audit's dedicated temporary workspace because canonical APFS allocation failed even for a 13-byte probe. The original canonical priority folder retains only the earlier partial checkpoint. The frozen staging manifest and caller-supplied external pin establish byte custody; they do not provide durable storage or publication. The coordinator must preserve these exact authored bytes before detaching temporary storage.

Source PDFs, text extracts, screenshots, and full HTML bodies are absent from the frozen folder. SOURCE_REVIEW_LEDGER.json and fetch/access receipts distinguish actual body reads from metadata-only and unread leads. INPUT_RECEIPTS.json pins the original packet and selected record. The custody verifier rejects changed inputs, undeclared files, links, special files, pin mismatch, and altered artifacts using explicit exceptions rather than assert statements. It must pass in ordinary and optimized Python.
