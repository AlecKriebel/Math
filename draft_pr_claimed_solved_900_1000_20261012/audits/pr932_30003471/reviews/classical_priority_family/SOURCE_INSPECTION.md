# Inspection receipts and exact source scope

Primary source URLs, version-specific bytes and retrieval UTC are in SOURCE_PINS.json. This record describes inspection actually performed, rather than treating successful retrieval as review or acceptance.

| Source | Text actually inspected | Complete PDF pages viewed from pixels (one-based) |
|---|---|---|
| OWR19/2017, MFO original bytes | Problem4 and full printed p1198 | 64 (printed1198) |
| AK1505.05263v2 | Complete six-page text, especially Theorem3.2, Conjecture5.1 and reference10 | 5 |
| Winter finite note, author-hosted, September4,2026 | Complete two-page statement, proof and references | 1,2 |
| Winter finite note, blog-hosted, September3,2026 | Complete two-page statement, proof and references | 1,2 |
| Same note, Git commit766c313 | Complete text; bytes equal current author note | Same exact PDF bytes as author note |
| Winter metric paper, institutional typeset journal PDF | Theorem3.2, complete proof and equality characterization, Theorem3.3, Remark3.7, Lemma4.3 and proof, section4.4 | 5,6,8,9,10,12,13,15 |
| Winter2302.14194v2 | Corresponding sections3,4.1,4.4,4.5 and references; compared exact theorem numbering and metric hypotheses | Journal copy viewed at corresponding statements above |
| Izmestiev0704.0349v3 | Theorem2.4 and proof, section2.3, AppendixA.3 and spectral proof; nonsimple C2 volume assertion | 7,8,15,16 |
| Winter2609.14645v1 | Complete six-page text; Theorem1, setup, full proof and finite-priority pointers | 1,2,5 |
| Mazzeo-Montcouquiol0908.2981v3 | Complete introduction/statement pages1-2; no full50-page analytic audit | 1,2 |
| Schlenker2000 official PDF | Intro and main theorem statements; spherical/deSitter and hyperbolic scope checked | 1,2,3 (printed409-411) |
| Schlenker-Souam2003 official PDF | Classical Schläfli formula and surrounding hypotheses, intro pages1-2 | 1,2 |
| Bobenko-Izmestiev2008 publisher PDF | Abstract, Theorem1.1, metric definition and uniqueness scope on printed448 | 3 (printed448) |

All29 rendered complete pages were opened and actually viewed. Raw render receipts and pixels are private. Source extraction preserves full pages; no crop hid hypotheses, footnotes, equation signs, references or dates. The MFO copy's SHA matches the original selected packet metadata. The current EMS PDF has different bytes and is separately pinned; no byte equality was assumed.

Version metadata: AKv2 April6,2016; Winter metricv2 January8,2024; Izmestievv3 July25,2008; Mazzeo-Montcouquiolv3 April5,2011; Winter infinitesimalv1 submittedSeptember13,2026 (PDF internal dateSeptember15). Current arXiv metadata for each was retrieved. The finite note is an author-hosted note, not an arXiv article or a verified journal publication. Its first note-file Git history entry records September4,2026 and retrieves the same bytes; the earlier blog attachment internally records September3. Crossref verifies the metric article's onlineDecember21,2023 and printMay7,2024 dates and IMRN2024(9),7721-7747.

Inputs required by the task were read in full before old verdicts: charter, complete cached source record, full selected original proof, SOURCE_STATUS.md and SOURCE_METADATA.json. No sibling reports or original audit verdicts were read. Original byte authentication itself did not read their mathematical content.
