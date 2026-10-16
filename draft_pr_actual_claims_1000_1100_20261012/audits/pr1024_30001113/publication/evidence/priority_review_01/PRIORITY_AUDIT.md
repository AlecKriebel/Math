# Independent adversarial priority audit: PR #1024

Audit performed 12 October 2026 PDT (13 October UTC). This report concerns the exact theorem in `submitted/current/COUNTEREXAMPLE.md`. It is independent of root searches and other reviewers' findings. It does not replace the mathematical audits.

## Disposition

**No matching prior negative answer was identified in the primary-source bodies inspected. The bounded audit supports proceeding with a short note, after the credit and scope corrections below. It does not certify exhaustive novelty.**

The theorem under comparison is specific: over k=F4, with G=(F4,+), N=(F2,+), and rho(a)(t)=t/(1+at), there is no prorepresentable F, with any tangent dimension, for which restriction–induction is formally smooth into D_N^(G/N) x_F D_(G/N). This gives a negative instance of the unrestricted question in OWR54/2008 p.3039 and arXiv:1112.0352v1 Question 4.4. It does not address a variant assuming D_N and D_(G/N) prorepresentable.

The defensible contribution is the application of known involution pathology, together with the restriction-kernel calculation, to exclude the proposed factorization. The additive action, involution nonprorepresentability, parameter-shift conjugacy, and foundational tangent-cohomology framework should not be promoted as independent new discoveries.

## Exact source comparison

The source URLs, downloaded hashes, bibliographic/version dates, and precise body-inspection levels are in `SOURCE_INSPECTION_MANIFEST.json`. PDFs were inspected as mathematical bodies, not merely as metadata. Three decisive original pages were also rendered and visually checked.

| Source inspected | Exact relevant claim and hypothesis comparison |
|---|---|
| Byszewski, OWR54/2008, pp.3038–3040 | The question on p.3039 requires prorepresentable F but does not require prorepresentable D_N or D_(G/N). Theorem 3 on p.3040 adds both assumptions separately. This is an exact target match for the unrestricted question, not a previously proved negative answer. |
| Byszewski, thesis, 18 May 2009, pp.59–60,73–80 | Question 6.4.4 and introductory formulation are unrestricted. Remark 6.4.5 adds assumptions conditionally for a ring formula; Theorem 6.4.7 separately assumes both component functors prorepresentable. Its proof constructs an obstruction class, verifies choices and completeness; it neither constructs the desired F nor excludes F in the exceptional example. |
| Byszewski, arXiv:1112.0352v1, 1 December 2011 | Definitions1.1–1.2 admit this perfect residue field and identity-reducing conjugacy category. Question 4.4 is unrestricted. Remark 4.5 and Theorem 4.9 impose additional assumptions explicitly. Current arXiv history has only v1; its record has no journal reference. No 2013 publication or later version was verified by this audit. |
| Byszewski–Cornelissen, AIF59(2009), pp.895–901 | Proposition 4.1 gives the exact parameter shift. Proposition 6.1 supplies a stronger antecedent of tangent collapse, explained below. These inspected statements concern universality and quotient descriptions, not the restriction–induction no-F assertion. |
| Same work, arXiv:0708.3279v3, 2 April 2008 | Relevant proofs occur under earlier proposition numbers, including Proposition 5.5 for failure to preserve injections. The inspected bodies add no matching factorization assertion. Use published numbering in the note. |
| Dokchitser, arXiv:math/0511514v1, 21 November 2005, all 4 pages | The theorem characterizes quotients by constant groups; the concluding question concerns formally smooth group-functor quotients of hulls. Neither is the local subgroup/quotient fibre-product question. The proof bodies were read. |
| Byszewski–Cornelissen–Kato, published2012, pp.25–27 | Proves universality for an order5 automorphism in characteristic5 with conductor2. Different group and characteristic; the entire proof was inspected. Its references still call the 2011 local-action paper a preprint. |
| Obus, arXiv:1703.01191v2, pp.34–38, 2017; book publication2019 per arXiv | Proposition 7.16 repeats universality classification. Theorem 7.17 gives restriction isomorphism when the quotient order is prime to p and subgroup functor universal. The candidate has quotient order p=2, so this theorem does not apply. Tower/lifting questions in these sections are distinct. |
| Dang, Algebraic Geometry13(3)(2026), pp.305–308,314–316 | Studies cyclic covers in towers and cites Byszewski for induction. Question 2.16/Conjecture 2.17 concern cyclic extension deformation rings. Noncyclic Klein-four G and arbitrary prorepresentable recipients are not their claim. Bibliographic acceptance is 26 September 2024; publication2026. |
| Byszewski–Cornelissen–Tijsma, published2022, pp.486,526–528 | Proposition 8.1.1 explicitly proves the familiar additive Klein-four family over fields larger than F2. Other Section8 results construct higher-depth series over F2; their proofs were inspected. They do not discuss the proposed deformation-functor factorization. The journal version, as well as the 2020 arXiv version, was recovered. |
| Kontogeorgis–Terezakis, arXiv:2304.08377v4, 22 May 2025, pp.1–4 | Screened by explicit theorem hypotheses: cyclic p-Sylow metacyclic groups and lifting to characteristic zero. The candidate's p-Sylow is noncyclic and its assertion is functor factorization. No full audit of this different theorem is claimed. |

## Important antecedent: recipient tangent collapse

AIF Proposition 6.1, p.899, exhibits an injection A=k[e]/(e²) -> B=k[w]/(w³), e -> w², for which the nontrivial involution class v over A and the basepoint become equal over B. Let eta:D_(G/N) -> h_R be natural. Naturality gives

h_R(A -> B)(eta_A(v)) = h_R(A -> B)(eta_A(0)).

The map on Hom-sets is injective because A -> B is injective. Thus eta_A(v)=eta_A(0). The candidate's conclusion that every prorepresentable recipient kills v is therefore an elementary consequence of an already published fact. Its direct proof using e -> e+e² remains useful and checkable, but it should be presented with this antecedent explicitly credited.

This observation does not itself settle the subgroup/quotient question: the obstruction also needs a group action whose restriction tangent map is injective, the identified quotient involution, and the final smoothness contradiction. No inspected source stated or proved that assembled assertion. This is the exact distinction on which the bounded priority conclusion rests.

## Search and retrieval record

`QUERY_LEDGER.json` records **65 independent search queries**, covering title/author/version searches, devissage and dévissage, fiber/fibre/fibre-product, factorization/factorisation, counterexample/negative answer, nonrepresentability/prorepresentability, Klein-four and involution terminology, and recipient/tangent mechanisms. Earlier batches have an explicitly bounded session timestamp because a finer timestamp was not captured; later batches have invocation timestamps. Search results and indexed snippets were discovery leads, not substitutes for body inspection.

OpenAlex title/DOI/citation endpoints supplied leads for the 2011 article and AIF paper. Retrieved citing works were followed into primary bodies. Crossref title search supplied no verified matching journal edition; this is only a search outcome. Semantic Scholar returned429 and was not repeatedly polled. No citation service is assumed complete, and source metadata cannot establish absence of a solution.

The Utrecht research-portal PDF returned403; the old igitur hostname did not resolve. Those failures were recorded, then the thesis was recovered via the supervisor's exact DSpace handle and its advertised bitstream content endpoint. The 2012 and 2022 published PDFs were likewise recovered from repository records after other endpoints failed. Retrieval records preserve status, URL, local path, and hashes. An accidental unrelated OpenAlex work endpoint was corrected and labeled as unused evidence.

## Required paper and global-credit corrections

1. Add explicit credit to AIF Proposition 6.1 alongside Proposition 4.1 in the discussion of the recipient-collapse lemma. Explain its elementary consequence above; do not present that lemma as an unprecedented detection phenomenon.
2. Cite the thesis Question 6.4.4 as an earlier full formulation, with OWR p.3039 and arXiv Question 4.4 as the other documented formulations. They are one question, not three discoveries.
3. State at the beginning, in theorem wording and publication metadata, that the answer is negative for the **unrestricted** formulation. Repeat that the prorepresentable-component variant is untouched. The inspected texts support this scope distinction directly.
4. Credit the additive weakly ramified family as standard. If a modern explicit source is desired, the published2022 Proposition 8.1.1 has exactly the family; AIF's normalization is already sufficient historical context.
5. Remove or avoid claims such as first counterexample, previously unknown involution pathology, full solution of the prorepresentable-case dévissage problem, or proof that the question remained open through2026. The audit did not verify those stronger historical assertions.
6. Use a title such as *A characteristic-two counterexample to dévissage for local deformation functors*. A short research note is proportionate to the verified scope.

Suggested introduction wording:

> We give a negative answer to the unrestricted fibre-product question posed by Byszewski. For a weakly ramified Klein-four action over F4, restriction–induction cannot be formally smooth over any prorepresentable recipient. The argument uses the known failure of the involution deformation functor to preserve injections and an explicit calculation of the restriction kernel. The variant imposing prorepresentability on the subgroup and quotient deformation functors is not addressed.

This is publication framing, not a claim that the independent priority search is exhaustive. Add the requested AI-use and unrefereed-status disclosures elsewhere in the note; they should not be conflated with priority verification.

## Strongest verified conclusion and remaining gap

The primary formulations inspected really do permit this exceptional nonprorepresentable-involution instance. The most important candidate ingredients are established antecedents, and the exact negative factorization assertion was not found in the inspected sources or returned focused leads. Consequently this audit supplies no basis for an `already_solved` disposition.

The remaining priority gap is possible unindexed work, differently worded statements, inaccessible or uncaptured proceedings, unpublished arguments, and omitted citation-database records. No independent audit of absolute absence is possible from these searches. A human-led specialist literature review could increase confidence; no communication or outreach was prepared or initiated. This residual gap should constrain novelty wording, not be replaced by an unwarranted claim of guaranteed priority.

Completion of the documented bounded priority audit: **100%**. Guarantee of exhaustive novelty: **not asserted**. No GitHub mutation, merge, comment, deposit, release, or external communication was performed.
