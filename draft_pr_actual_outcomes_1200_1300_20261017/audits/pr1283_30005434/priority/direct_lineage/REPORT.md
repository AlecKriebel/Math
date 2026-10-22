# Initial independent seal: direct target and citation lineage

Audit date: 2026-10-18 UTC. Target: PR1283 / Problem 30005434 / OWR-12697693-005, Dietzel, *Some problems on L-algebras*, Problem 3, OWR 9/2023, printed p. 545.

## Finding and decision

**Priority remains unestablished. This audit does not clear novelty, first explicit statement, first mechanism, or current worldwide openness.** I found no body-verified prior source stating the full admitted classification or its meet-valued fallback formula. That is a bounded retrieval finding, not evidence that no prior result exists.

There are substantial, positively verified antecedents. Credit Rump for the L-algebra framework and closure constructions, and Dietzel for the stated problem. A stronger semibrace convention was present before the workshop, including in the paper coauthored by Dietzel. It cannot be framed as a later repair invented in response to this candidate.

The most important unresolved direct-priority gap is the full body of Rump's 2008 *Semidirect products in algebraic logic...*, which the target cites for Definition 2 and the enumeration paper cites for Definition 3 and Theorem 3. I inspected only its publisher-supplied first-page preview and bibliographic discovery records, not those definition/theorem pages. No outside contact was initiated or prepared.

## Claim audited

The admitted claim, supplied by the root, is taken as the claim whose priority is being tested, not as an assumption of novelty:

1. Under the four identities in the workshop's **printed** Definition 2, every nonempty meet-semilattice has a structure, at any chosen distinguished point, using right projection.
2. With the workshop's L-algebra axioms additionally imposed, the underlying meet-semilattice admits a structure exactly when it has a greatest element e. In every joint structure its meet order is the logical order x·y=e. One construction is x·y=e if x≤y, and x·y=x∧y otherwise.
3. Under the separately attested convention requiring (X,∧,e) to be a commutative monoid, restricted to meet-semilattices, a greatest e is required for both questions; the constructions still apply.

This concerns existence and order compatibility. It does not classify all products, imply self-similarity or cancellation, or resolve a stronger unpublished interpretation of the problem.

## Strongest direct findings

### The source and its dates

The original contribution's printed pp. 544–547 were read in the supplied read-only PDF/text. Definition 1, Definition 2, Problem 3, Problem 10, and the complete reference list were checked. The printed Definition 2 says meet-semilattice and distinguished point, without printing e as the meet identity. Its bibliographic pointer is [6], Rump 2008, DOI [10.1142/S0219498808002904](https://doi.org/10.1142/S0219498808002904).

The workshop itself ran 26 February–4 March 2023. The [MFO record](https://publications.mfo.de/handle/mfo/4027?show=full) records accession and availability at 2023-04-18T09:45:12Z. The [EMS article record](https://ems.press/journals/owr/articles/12697693) gives journal publication as 7 October 2023; Crossref records 6 October 2023. These are different metadata events. Neither accession metadata nor a present-day attachment establishes that the exact current bytes were publicly available on the accession date. The checked mathematical target is the current printed source, not an inferred authorial intention.

### The monoid convention is older than the workshop

I independently downloaded and visually checked [arXiv:2206.04955v1](https://arxiv.org/abs/2206.04955v1), whose version record gives 2022-06-10 09:06:03 UTC. Its printed p. 5, Definition 3.1, already requires a commutative monoid with neutral e and the same four identities. The immediately preceding text attributes the definition to Rump 2008, Definition 3. Theorem 3.2 attributes the unique ∧-closure construction to Rump 2008, Theorem 3. The version-pinned PDF is 409480 bytes, SHA256 19bc9879cd638e719c3817f3a50202427ca854c1b3d2956488e75d866cc1ed67.

This is the earliest independently downloaded, version-dated body attestation in this audit, **not the earliest appearance of the convention**. The search provider also exposed an actual primary publisher passage from [Rump 2020](https://doi.org/10.1016/j.jpaa.2020.106314), equations (21)–(22), defining semibraces using a commutative monoid and citing the 2008 semidirect-products paper. Direct page access returned 403, so this is limited indexed-primary-passage inspection, not a full-paper or pinned-PDF inspection.

The 2022 theorem starts with an L-algebra and builds its canonical closure. On its face it does not prescribe the meet-reduct of an arbitrary supplied semilattice or state the candidate's formula. Treating it as an exact antecedent would require a separate derivation, which this family has not established.

### The old poset construction is a different antecedent

In [Rump, *The category of L-algebras*](https://tac.mta.ca/tac/volumes/39/21/39-21.pdf), printed pp. 606–607, Example 4, equation (20), every poset with greatest element gets x·y=1 when x≤y and y otherwise. The continuation explicitly attributes it to [67], Rump 2008 *L-algebras, self-similarity, and l-groups*, Example 1. I checked pp. 604, 606–607 in extracted text and page renderings, and checked [67] in the references.

This is the fallback-y operation in the workshop's Problem 10. It is not the fallback-x∧y construction being audited. The distinction matters even on a four-element Boolean lattice. The root supplied that the old operation fails the required meet preservation there; I do not independently promote that supplied counterexample as a new computational result here.

The same workshop contribution already mentions right projection as a cycle-set trivialization in the paragraph before Problem 9. That is an attested prior formula/ingredient, not an explicit statement there of the first half of Problem 3.

### Self-similar and orthomodular antecedents have narrower hypotheses

The TAC paper, p. 604, equations (13)–(14), states the two meet identities for self-similar L-algebras and attributes them to Rump 2008, Proposition 4. Proposition 3.4 concerns an additional partial-multiplication/universal-meet-preservation characterization. It is not a theorem that every preassigned meet-semilattice carries the candidate operation.

[Zhao, Wang, Wu 2024](https://doi.org/10.3934/math.20241535), printed pp. 31956–31957, Definition 3.5 and equations (3.19)–(3.20), repeats the monoid convention with attribution to Rump 2008. Proposition 3.2 proves ∧-closedness for OM-L-algebras. This is useful convention and special-class context, not an exact resolution of the arbitrary semilattice existence claim. The source's use of canonical ∧-closure must not be silently identified with every possible printed-axiom semibrace structure.

The public enumeration poster also discusses canonical closure and lower semimodularity in its discrete-case discussion. Only indexed primary text was obtained; direct PDF download looped through redirects. It should not be used to impose an unexamined extra condition on the printed target or to infer an inconsistency from a different meaning of closure.

### Recent follow-ups and direct resolution searches

The primary bodies/scope passages inspected include Properzi–Qin, [arXiv:2512.08579v1](https://arxiv.org/abs/2512.08579v1), submitted 9 December 2025, and Facchini–Gran–Pompili, [arXiv:2305.19042v1](https://arxiv.org/abs/2305.19042v1). Their inspected introductions, definitions, and section scopes concern ideals, simple/linear L-algebras, semidirect products, and categorical properties. Complete extracted-body term scans did not expose semibrace or arbitrary-semilattice resolution passages. This is bounded screening, not a claim to have reverified all proofs or to have excluded every implicit consequence.

The author-maintained Dietzel publication/preprint list and Rump's institutional publication list were inspected for direct follow-up leads. Recent titles include Rump's *Decomposition of L-algebras* (publisher DOI [10.1007/s11083-025-09719-8](https://doi.org/10.1007/s11083-025-09719-8)); its accessible publisher/preview scope is decomposition and cancellation, with a poset example mentioned. I did not obtain its full body. No exact Problem 3 resolution was established from that abstract or title.

Searches covered the problem wording and aliases, the source title, semibrace terminology variants, the cited 2008/2015 sources, author-follow-up combinations, and recent preprints. Most narrow searches returned the original workshop, the enumeration paper/poster, or different notions of left/generalized semibraces. The 2026 Wang left-semibrace abstract explicitly assumes a multiplicative group, a different setting; it was not promoted as an answer to this target.

Zenodo REST searches were made directly for singular/plural semibrace, L-algebras, target ID/number, source title, and semilattice AND Dietzel. The exact singular/target/title/conjunction searches returned zero records; plural semibraces returned a 2017 semi-brace paper metadata record; exact L-algebras returned five records, including the authors' finite-L-algebra code release. These are metadata searches, not full-text searches of all Zenodo deposits. One exploratory unqualified query used OR-like semantics and returned 147 records with only 25 displayed; I did not treat it as complete coverage and replaced it with an explicit AND query.

OpenAlex's report citation graph returned two records. Their titles concern twisted Araki–Woods algebras and property-(s) skew braces, respectively, not a direct title-level match to Dietzel's L-semibrace problem. I inspected their metadata/abstract context only; report-level citation counts cannot exclude unindexed contribution-level follow-ups. The 65 citing records for the 2008 semidirect-products paper were screened at title/metadata level to identify the relevant convention, closure, and L-algebra follow-ups. This does not constitute full-body clearance of all 65.

## Exact remaining gaps

- Full Rump 2008 semidirect-products paper: Definition 3, Theorem 3, surrounding examples and proof have not been directly inspected. Institutional author pages, bibliographies, DOI search, public preview, and OpenAlex OA-location discovery did not provide a usable complete copy in this audit. Publisher access was 403; no access controls were bypassed.
- Full Rump 2008 self-similarity and Rump 2015 right-ℓ-group bodies were not inspected. Later primary sources give precise attributions, but cannot substitute for reading every earlier example or consequence.
- Dietzel's 2021 thesis was located in Stuttgart's repository, but access produced an Anubis denial/challenge page. This was retained as an access receipt, not mislabelled as a successfully read PDF.
- Recent decomposition and several other cited follow-up bodies remain uninspected. Author publication lists and citation indices are incomplete and may lag or aggregate workshop contributions.
- Exact formulas can be implicit, differently named, or absent from indexed metadata; searches over semibrace terminology cannot exclude the entire older implication-algebra literature.
- Unpublished, private, poorly indexed, non-English, and recently posted work is not covered. No outside input was requested; any further external communication belongs only to the human user.

## Recommended global framing

Retain the valid full mathematical statement as a precisely delimited result under the printed axioms and give a separate monoid-convention corollary. Describe the supplied proof as an explicit construction/verification answering the printed question, with **priority not established**. Credit the original question to Dietzel and the definitions/closure lineage to Rump. Cite the 2022v1 convention and the older fallback-y construction accurately. Do not use “first,” “new,” “previously open worldwide,” or “no prior solution exists” on the strength of this audit.

If an earlier exact statement or a direct derivation from an earlier theorem is located later, change paper, abstract, documentation, metadata, and problem-status records together to identify the original author/date and present this contribution as an independent derivation, clarification of the printed formulation, or exposition as appropriate. This audit authorizes no such edits or publication actions.

## Independence and artifacts

No sibling priority-family output was read and no sibling priority agent was contacted before this initial seal. Only root coordination occurred. Work was confined to this dedicated family directory. No repository, PR, index, sheet, release, or external-message mutation was performed.

QUERY_LEDGER.json records actual query strings and dates, batch result references, inspection paths, and findings. SOURCE_REGISTER.md distinguishes pinned bodies, indexed passages, metadata, and access gaps. PROVENANCE.json contains read-only input receipts, including absolute source paths as receipts only. Raw provider outputs, third-party PDFs, text extractions, and renders are private under _local and excluded from OUTPUT_MANIFEST.json. The manifest lists only explicit authored outputs and excludes itself and the seal.

Completion estimate at seal: 100% of this bounded family audit; no percentage confidence in novelty is assigned.

