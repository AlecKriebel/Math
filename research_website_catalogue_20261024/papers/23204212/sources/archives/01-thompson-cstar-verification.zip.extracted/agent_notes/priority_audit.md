# Independent priority and attribution audit

Audit checkpoint: 2026-10-06 22:14 PDT (2026-10-07 05:14 UTC). Scope: the proposed conclusion that the reduced group C*-algebras of F, T, Aut(F), and Comm(F) are simple and have their canonical traces as their unique tracial states. Source clone was read only; no outreach, Git mutation, or publication was performed. Best-guess completion: 100% of this bounded attribution audit. Public priority remains uncertain; no evidence establishes first publication of the combined unconditional consequence.

## Decision

The four-group conclusion is an immediate application of existing published conditional results to the claimed nonamenability input. It should be presented as an attributed consequence or dependency-checked exposition. This audit provides no basis to advertise a new C*-simplicity mechanism or first theorem for these groups. An absence of indexed recent hits is not evidence of novelty.

The strongest mathematical statement independently supported by this audit is conditional: **if Thompson's F is nonamenable, then all four named reduced group C*-algebras are simple and have unique canonical tracial states**. Independent validation of the new nonamenability input is outside this audit and remains a necessary dependency for promoting the consequence as established unconditionally.

## Primary public statements and attribution

| Existing result | Primary source and locator | Attribution consequence |
|---|---|---|
| F nonamenable iff F is C*-simple iff T is C*-simple | [Le Boudec–Matte Bon, arXiv HTML](https://arxiv.org/html/1605.01651), Corollary 4.2 | The implication for F and T is already explicit. |
| F nonamenable iff Aut(F) is C*-simple iff Comm(F) is C*-simple | Same source, Corollary 4.4 | The implication for both automorphism and abstract commensurator groups is already explicit. |
| Any C*-simple discrete group has the unique trace property; this property is equivalent to trivial amenable radical | [Breuillard–Kalantar–Kennedy–Ozawa](https://arxiv.org/html/1410.2518), Theorem 1.3 / Corollary 4.3 | Uniqueness is a general established theorem, not an added new mechanism. |
| T already has a unique tracial state | [Haagerup–Olesen](https://arxiv.org/html/1609.05086), paragraph following Theorem 4.5 | This part of the target is unconditional and predates the proposed input; the authors credit Dudko–Medynets. |
| F nonamenable iff its reduced algebra has a unique tracial state | Same arXiv source, Remark 4.6 (journal Remark 5.6) | Even the conditional trace consequence for F is explicitly in the older literature. |

Publication metadata checked at the publishers' or archival primary pages:

- Adrien Le Boudec and Nicolás Matte Bon, *Subgroup dynamics and C*-simplicity of groups of homeomorphisms*, Annales scientifiques de l'École Normale Supérieure (4) **51** (2018), no. 3, 557–602, [DOI 10.24033/asens.2361](https://www.numdam.org/articles/10.24033/asens.2361/). arXiv:1605.01651 was submitted 2016-05-05, last revised 2016-12-23 (v3).
- Emmanuel Breuillard, Mehrdad Kalantar, Matthew Kennedy, and Narutaka Ozawa, *C*-simplicity and the unique trace property for discrete groups*, Publications Mathématiques de l'IHÉS **126** (2017), 35–71, [DOI 10.1007/s10240-017-0091-2](https://www.numdam.org/articles/10.1007/s10240-017-0091-2/).
- Uffe Haagerup and Kristian Knudsen Olesen, *Non-inner amenability of the Thompson groups T and V*, Journal of Functional Analysis **272** (2017), no. 11, 4838–4852, [DOI 10.1016/j.jfa.2017.02.003](https://doi.org/10.1016/j.jfa.2017.02.003).
- Artem Dudko and Konstantin Medynets, *Finite factor representations of Higman–Thompson groups*, Groups, Geometry, and Dynamics **8** (2014), no. 2, 375–389, [DOI 10.4171/GGD/230](https://ems.press/journals/ggd/articles/12665). The preprint is [arXiv:1212.1230](https://arxiv.org/abs/1212.1230), December 2012. For the explicit T unique-trace statement and attribution, cite Haagerup–Olesen directly rather than treating the title of the Dudko–Medynets paper alone as its locator.

The Haagerup–Olesen arXiv HTML introduction has a sentence saying “amenable” where the later Remark 4.6 correctly says “non-amenable.” Do not repeat that introduction sentence; the remark gives the supported implication and a proof via the amenable radical. This is a source-reading caution, not a proposed new correction to the source.

## Pinned corpus audit and dates

Read-only source: `/Users/alec/Desktop/math`, verified HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

- `CONTENTS.md:6162` identifies family 248 and `lean/docs/248.md` describes only nonamenability of the standard dyadic PL group, with no explicit boundary constant or prescribed generating set.
- `preprints/Thompsons-group-F-is-nonamenable-September-23-2026/README.md` gives the author as **OpenAI**, title *Thompson's group F is nonamenable*, year 2026, and the manuscript date as September 23, 2026. Use this metadata; do not attribute the input to this follow-on researcher.
- In that manuscript, `build/sections/consequences.tex` states two companion applications: nonunitarizability and percolation. It contains no C*-simplicity or unique-trace application. `build/sections/introduction.tex:61–63` recalls the older Haagerup–Olesen implication from simplicity for T to nonamenability for F. Its bibliography does not cite Le Boudec–Matte Bon.
- A corpus-wide lexical scan of `.tex`, `.md`, and `.bib` files for Thompson, Le Boudec/Matte Bon, DOI/asens.2361, arXiv/1605.01651, Aut(F), Comm(F), and relevant simplicity terms did not locate another named-group C*-simplicity consequence. Files mentioning Thompson together with “simple” concern unrelated group-theoretic applications or the family-248 introduction. This is a bounded file-content observation, not an assertion about all PDFs or all public statements.

**Manuscript date is not an established announcement date.** Public GitHub API reads during this audit returned exactly one path-specific commit and the same current main commit, both `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, committer date **2026-10-06T21:58:50Z** (October 6, 14:58:50 PDT), message `Initial commit`. The repository evidence therefore establishes this commit date; it does not establish public availability on September 23. No earlier independent announcement was verified.

Read URLs:

- [Pinned family README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Thompsons-group-F-is-nonamenable-September-23-2026/README.md)
- [Current family consequences source](https://raw.githubusercontent.com/openai/math/main/preprints/Thompsons-group-F-is-nonamenable-September-23-2026/build/sections/consequences.tex)
- [Current repository README](https://raw.githubusercontent.com/openai/math/main/README.md)
- [Path commit-history API](https://api.github.com/repos/openai/math/commits?path=preprints/Thompsons-group-F-is-nonamenable-September-23-2026&per_page=100)
- [Current main commit API](https://api.github.com/repos/openai/math/commits/main)
- [Read-only issue search API](https://api.github.com/search/issues?q=repo%3Aopenai%2Fmath+Thompson)

The issue search returned `total_count: 0`, `incomplete_results: false` for the word Thompson. This does not exclude unindexed commentary, different wording, private review, or a correction posted elsewhere. The current README describes materials at differing verification stages; a formalization listing does not by itself establish independent verification of the intended group semantics.

## Current public search record

The dedicated repeat batch began **2026-10-07 05:14:21 UTC** and ended **05:14:22 UTC** (October 6, 22:14:21–22:14:22 PDT). Searches used the web tool; it does not disclose an underlying search-engine result-page URL. Exact queries, filters, and accessed primary source URLs are recorded here and in `priority_searches.json`.

| Query | Filters | Observed outcome |
|---|---|---|
| `"Thompson" "nonamenable" "OpenAI"` | domains arxiv.org, github.com, openai.com | No mathematical announcement or correction located in returned indexed hits. |
| `"Thompson" "C*-simple" "OpenAI"` | same domains | No relevant named-group follow-on result located in returned hits. |
| `"Thompson" "C*-simplicity" after:2026-09-23` | recency 15 days | Returned the older Le Boudec–Matte Bon primary article and older seminar/publication pages; crawl freshness did not make them new publications. |
| `"Thompson" "OpenAI" correction` | above domains, recency 20 days | No relevant mathematical correction located in returned hits. |

Earlier probes in the same audit included `site:openai.com "Thompson" "nonamenable"`, `"Thompson’s group F" "C*-simple" 2026`, `"Thompson's group F" "unique trace" "2026"`, `"OpenAI" "Thompson" "September 23" "2026"`, `site:arxiv.org "Thompson" "nonamenable" "2026"`, and named-group trace searches. No search result was treated as proof of absence. One current author page and a June 2026 preprint still called the problem open, but those statements may precede the repository publication and are not corrections to it.

## Nearby established strengthening

[Kang Li and Eduardo Scarparo, *C*-irreducibility of commensurated subgroups*](https://arxiv.org/html/2210.00827), Pacific Journal of Mathematics **322** (2023), no. 2, 369–380, [DOI 10.2140/pjm.2023.322.369](https://msp.org/pjm/2023/322-2/pjm-v322-n2-p07-p.pdf), already proves that a C*-simple group embeds C*-irreducibly in its abstract commensurator (Corollary 3.14). Its Remark 3.15 explicitly identifies Le Boudec–Matte Bon's Comm(F) conclusion as the earlier special case. Moving from simplicity to the inclusion's C*-irreducibility would therefore also activate an existing general theorem and requires attribution. These exact locators were independently read in the primary arXiv v3 HTML.

## Exact uncertainty and recommendation

There is no demonstrated new implication among the four original C*-simplicity conclusions, and T's trace conclusion is already unconditional. The only changed input would be the claimed proof of F's nonamenability. Whether somebody has already explicitly combined that input with the older theorems is unresolved by this bounded public search, especially given the source repository's October 6 initial commit and index delays. That uncertainty does not justify a “first,” “new proof,” or “novel C*-simplicity result” claim.

A defensible note should name OpenAI for the nonamenability input, Le Boudec–Matte Bon for the four simplicity implications, Breuillard–Kalantar–Kennedy–Ozawa for the trace implication, and the earlier unique-trace literature for T/F as appropriate. It should pin the OpenAI commit, separate the manuscript date from verified availability, and make the new nonamenability input's validation status explicit.
