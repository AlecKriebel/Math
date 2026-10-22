# PR1151 / problem30003321: independent priority-lineage audit

Decision: **BOUNDED_NO_PRIOR_FULL_FOUND**. No previously recorded theorem or explicitly recorded consequence fully answering the exact group target was identified in this lineage search. This is neither a novelty certificate nor a certificate that the question remains open globally or currently. Mathematical correctness was assigned separately and is not re-decided here.

The audit covers the original question, Kaplan's thesis and author publication lineage, Ehrlich's accessible author writings, available forward-citation leads, and the strongest nearby statements. It was conducted without reading any root/sibling/previous priority verdict. The plan was sealed before the candidate mathematical text was opened; the seal is in `plan_seal.json`. Only candidate lines9-88 were read, excluding review-status and scope/novelty sections. No external communications or repository/publication changes were made.

## Exact target and original-source distinction

The target is: every discrete initial ordered additive subgroup G of No has an order-group isomorphism onto a subgroup H contained in Oz that is initial in No. Sets and proper classes are included, in NBG with global choice. Initiality is closure under simplicity predecessors. The isomorphism need not preserve simplicity, and no multiplicative closure is assumed. Zero is a harmless separate boundary case; the sources define a discrete group as nontrivial with a least positive element.

The exact question is present in these independently inspected versions:

| Work/version | Verified location | Role |
|---|---|---|
| Kaplan, honors thesis, cover April2015 | printed47 / PDF49, Question1 | Earliest explicit occurrence located in this audit; full surrounding proof and open-problem context inspected |
| Ehrlich–Kaplan, arXiv1512.04001v1, submitted2015-12-13 | printed18 / PDF18, Question2 | Same target, different numbering |
| Kaplan (joint Ehrlich), supplied EMS report60/2016 | printed3356 / PDF44, Question1 | Original requested locator; visually verified |
| Official MFO report mirror | printed3358 / PDF44, Question1 | Same question, shifted printed pagination; not an independent work |
| Current author-hosted sequel manuscript | printed15 / PDF15, Question9.1 | Same target and explicit NBG/class convention on p2 |
| Published sequel | JSL83(2018),617–633; online2018-02-05 | Publisher metadata independently checked; publisher PDF endpoint did not supply the article body |

Primary links: [2015 thesis](https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=ouhonors1429615758&disposition=inline), [arXivv1](https://arxiv.org/abs/1512.04001v1), [supplied EMS report](https://ems.press/content/serial-article-files/46663), [official MFO mirror](https://publications.mfo.de/bitstream/handle/mfo/3563/OWR_2016_60.pdf?isAllowed=y&sequence=1), [author manuscript](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf), [publisher record](https://doi.org/10.1017/jsl.2017.9).

The thesis uses the example Z/2, whereas the sequel gives D+Z/omega and its map onto omega D+Z. These are examples of the required phenomenon, not universal solutions. The established subdomain statement concerns groups with additional ring closure. The dense-theory set-model question, called Question8.1 in the later manuscript and Question2 in the workshop contribution, is also separate. None of these distinctions is merely terminological: each changes the hypotheses or desired conclusion.

The author-hosted PDFs were recompiled in September2026 according to embedded PDF metadata. That does not make their mathematics newly published in2026, or make an old retained question a current-open-status announcement. arXiv version histories and journal metadata supply the historical dates; exact retrieved bytes are separately pinned.

## Strongest prior statements and exact gaps

### 1. The original work supplies substantial machinery, not the full answer

The author manuscript's Lemma5.1, Theorem5.1 with its complete pp7-9 proof, and Proposition5.2 with its p10 proof were checked. In particular, the least positive element already has the form 2^(-n)omega^(-alpha). The initial-group characterization includes the dyadic requirement attached to right simplicity predecessors. Theorem6.2 and its complete pp11-12 proof cover initial subdomains. The paper nevertheless explicitly proceeds to the general group question in Section9. **Classification: PARTIAL_PRIOR**, with exact target expressly posed rather than settled.

Relative to the candidate, the prior work already accounts for the bottom-element form and the general characterization. What was not located as a prior recorded full conclusion is the universal sign-sequence rerooting with suitable right-predecessor control, followed by the specific normalization of the actual subgroup image. This assessment identifies an exact missing priority witness; it does not certify that the missing statement is new.

### 2. Later author paper explicitly records series transport

Kaplan–Krapp–Serra, *Decomposing the automorphism group of the surreal numbers*, was first submitted2025-09-26; arXivv3 is dated2026-04-23. Author-hosted pp4-8 were read with the full proof of Proposition3.9 and Construction3.10; the corresponding arXivv3 construction on p7 was checked. Definition2.8 and Construction3.10 explicitly combine exponent order automorphisms and positive real coefficient scalings. This is real overlap with the candidate's transport step. [Primary paper and version history](https://arxiv.org/abs/2509.22374).

The stated theorem decomposes automorphisms of the whole surreal field/group. It does not state that every discrete initial subgroup can be sent to an initial subgroup of Oz, nor provide a minimum-to-zero exponent construction with the required right-predecessor property. An order automorphism of the full exponent class is not a recorded guarantee that an arbitrary initial subclass has an initial image. **Classification: PARTIAL_PRIOR_TRANSPORT_MACHINERY**, not PRIOR_FULL. Earlier general Hahn-group automorphism references cited in that paper were not separately read; this audit does not assign the first date for the transport machinery itself.

### 3. Surreal-substructure and convex-partition results are in a different signature

Bagayoko–van der Hoeven, *Surreal substructures*, arXiv2023-05-03, is a strong search hit because its p34 discusses Oz and isomorphisms onto initial subclasses. Proposition4.6, Remark4.8, the complete Theorem6.7 proof, and the surrounding pp32-35 were read, with p34 visually checked. The maps concern the order and simplicity structure. The Oz convex-partition example does not assert additive compatibility for an arbitrary source group. **Classification: NEAR_MISS_ORDER_AND_SIMPLICITY**. [Primary paper](https://arxiv.org/abs/2305.02001).

### 4. Canonical integer parts do not already normalize every discrete initial group

Ehrlich2011, pp3-4 footnote2, records initiality of the omnific integer part of an s-hierarchical group/field. Ehrlich2012, pp22-24, gives the corresponding initial-subfield theorem and addendum. Berenbeim's dated2020 notes summarize an integer-part statement on p5. These were inspected where they might appear to furnish a stronger universal consequence. None of the read statements identifies every given discrete initial group, with arbitrary least positive element, with an initial subgroup of the canonical Oz. **Classification: PARTIAL_PRIOR_INTEGER_PART**. [2011 journal article mirror](https://upload.wikimedia.org/wikipedia/commons/6/61/Conway_names%2C_the_simplicity_hierarchy_and_the_surreal_number_tree.pdf), [2012 article copy](https://norvaisa.lt/wp-content/uploads/2012/08/Ehrlich-unification-2012.pdf), [2020 notes](https://www.berenbeim.com/_files/ugd/4185a9_48e6549b46e44b6186c90bc11b13b26a.pdf).

### 5. The2021 exponential followup resolves other issues

Ehrlich–Kaplan, *Surreal ordered exponential fields*, was checked at the abstract, dense-group counterexample, and full initial-integer-part lemma/proof. Lemma11.1 concerns Oz intersect an initial field. Example8.1 uses a densely ordered group with no initial embedding into No. These do not settle the target discrete-initial-group question. Other screened author/citing works concern integration, hyperseries, differential fields, or SUR-algebras. **Classification: PARTIAL_PRIOR or SCREENED_NOT_TARGET**, with individual read scopes in the ledger. [Primary2021 version history](https://arxiv.org/abs/2002.07739).

## Search scope, counts, and evidence quality

- **52 distinct search-query inputs**, in13 four-query batches; all strings and timestamps appear in `SEARCH_LOG.json`. They cover the exact question, wording variants, author/thesis/publication searches, dates, author-attributed recorded discussions, and explicit answer/solution variants. There were12 logged follow-up primary-page/link/find inputs, in addition to the two supplied originals opened at the outset. HTTP catalog/download requests are counted separately in `fetch_manifest.json` and are not research-work counts.
- **16 distinct mathematical works had bodies acquired and text screened**. This is not a claim that every page was mathematically read. Three further works had only primary abstract/metadata access. Versions and mirrors are grouped by work in `EVIDENCE_LEDGER.json`. Author pages, the CV, catalog records, and one unrelated arXiv identifier checked because of a bad bibliography link are not counted as mathematical works with bodies.
- Kaplan's current author list and CV were inspected; the CV is explicitly updated2026-09-27. The relevant exponential and automorphism followups received deeper reading. The2021 dissertation was distinguished from the2015 honors thesis. [Author list](https://elliotakaplan.github.io/).
- OpenAlex's DOI record for the sequel returned32 citing records but visibly merged in pre2015 citations belonging to the2001 predecessor. The separate arXiv record returned one citation. Semantic Scholar's DOI result had8 citations but year2001; its arXiv request returned429. These are discovery leads, not32 or8 verified forward citations to the sequel. Cambridge exposed no usable CrossRef citing list. Google Scholar access was forbidden through the web tool; an exploratory numerical cites request was not a valid article identifier and was discarded as citation evidence.
- Every acquired body, extraction, rendering, and raw web-response record is confined to ignored `private/`. Public artifacts contain authored analysis, acquisition metadata, reading scopes, and hashes. Receipt pins include the candidate, AGENTS instructions, PDF skill, sealed plan, reports, and all local evidence. A future re-fetch at the same URL is not assumed byte-identical.

## Access failures, unread leads, and limits

Material fulltext gaps are the2001 predecessor and Ehrlich's2024 chapter *The Absolute Arithmetic Continuum and Its Geometric Counterpart*. The2024 primary preview includes abstract and exposed references, including the2018 sequel, but the full chapter and relevant proofs were not accessible. It remains an explicit unread author-lineage lead, with no asserted result inferred from its title. [2024 publisher chapter](https://doi.org/10.1007/978-3-031-40846-5_54).

Ehrlich's old author homepage/PDF routes returned404, his official faculty URL redirected to the generic directory, and DBLP supplied anti-bot pages. The original JLA endpoint timed out; its matching journal PDF was obtained from a mirror. The2012 Euclid PDF request supplied a challenge page; the article copy was used instead. The JMM2015 abstract was readable in search output but download returned403. Publisher PDF endpoints for the sequel and2024 chapter returned subscription-preview HTML. These failures are recorded rather than counted as fulltext access.

No exhaustive citation graph, complete current Ehrlich bibliography, non-English literature census, unpublished-record census, or global current-open-status check was obtained. The weakest screened works were checked by whole-text keyword searches plus abstracts and relevant contexts, not full proof-by-proof reading. General Hahn-automorphism antecedents cited by the2025 paper and the broad2024 chapter remain potential further checks. No outside input was sought, and no outreach was prepared.

## Result of this family

**PRIOR_FULL witness: none found.** Strongest verified prior overlap consists of the explicit least-positive-element description, the complete initial-group characterization, the subdomain result, canonical initial integer parts, and explicit coefficient/exponent transport machinery. The exact remaining priority question is whether an earlier recorded theorem or consequence already supplies the full discrete-group normalization, including initial image and proper classes. The search did not locate one within its stated accessible scope.
