# Independent audit of Hamiltonian prior resolution attribution

## Decision

Approve `already_solved` as a **published prior-resolution attribution**, with the existing full-theorem and full-proof limitations retained. Do not label this a newly solved problem, a verified published proof, or a complete candidate proof. No blocking mathematical correction to the frozen literature-status note was found.

The decisive evidence is the authors' explicit identification of Gasull's Problem 12 as answered positively in the primary publisher abstract. It is not an inference from the abstract's separate simple-critical-period wording. [Zhuang and Liu, 2023](https://link.springer.com/article/10.1007/s12346-023-00786-z).

This judgment is bound to the original `SHA256SUMS.json` hash `78c55db696e21f0c0d2d071d0b80e7745810a54fe43cdb5f7e373ee4a61cf5ad` and `LITERATURE_STATUS.md` hash `a23c188e00ad2e42f6a8294ec9fc79f7e64eaa771d40e9e13245bd430cb79f7c`. The frozen submission was not edited.

## Original question and counting convention

I independently inspected page 13 of Gasull's [arXiv v1 paper](https://arxiv.org/pdf/2012.02524v1), including its rendered page. Problem 12 matches the selected numeric record 4700012 / AMR-046-0012: two nonzero homogeneous Hamiltonian terms of respective degrees 2n and m, m greater than 2n, with a center at the origin. The surrounding definition counts zeros of the derivative of the minimal-period function on its open parameter interval. It does not restrict the question to simple zeros or to limit cycles.

The historical sufficient range and first remaining pair in the packet match that page. Its restatement adds no positivity, nondegeneracy, even-m, or global-annulus hypothesis. The center and boundary levels are outside the interior count. Reading n as a positive integer and retaining exact nonzero degrees is the intended ordinary-degree formulation; the zero-polynomial linear-oscillator extension is not part of the recorded problem.

The [2021 publisher entry](https://link.springer.com/article/10.1007/s40324-021-00244-3) and [author-university catalogue](https://portalrecerca.uab.cat/en/publications/some-open-problems-in-low-dimensional-dynamical-systems/) establish the journal identity corresponding to the 2023 citation. I did not inspect the 2021 version of record's complete text. Its university accepted-manuscript record was located, but retrieval failed; no unseen-version equivalence beyond this bibliographic link is asserted.

## Family mapping

This is an elementary scope check, not a proof of a period bound. Write an arbitrary ordinary homogeneous polynomial as a sum of monomials x^i y^j with i+j=d. Substitution of (lambda*x, lambda*y) multiplies each term by lambda^d, hence the whole polynomial has weights (1,1) and weighted degree d. Every nonzero first partial derivative has degree d-1. Consequently the two Hamiltonian vector fields have quasi-degrees 2n-1 and m-1, which remain distinct.

The [publisher-supplied first-page preview](https://www.researchgate.net/publication/370226829_Critical_Periods_of_the_Sum_of_Two_Quasi-Homogeneous_Hamiltonian_Vector_Fields) exposes the polynomial and vector-field definitions. Their degree convention agrees with this calculation: with unit weights, each vector-field component has degree equal to the vector field's quasi-degree. Both allowed weights are positive integers. This directly checks the advertised specialization against an inspected definition, without assigning a number to an unread theorem.

The specialization leaves the vector field, center, periodic trajectories, time parameter, and period annulus unchanged. It imposes no parity condition on m. The period function is therefore the same function under the same regular-energy parameter. Any detailed extra hypotheses of the inaccessible full theorem remain unverified.

## What the publication does and does not establish here

The primary publisher confirms Ziwei Zhuang and Changjian Liu, the matching title, Qualitative Theory of Dynamical Systems 22, article 90, DOI 10.1007/s12346-023-00786-z, and publication/version-of-record date 24 April 2023. Its abstract concerns an origin-center period annulus and Hamiltonians with two common-weight terms of different quasi-degrees. It expressly attributes an affirmative resolution to the exact numbered problem. That is sufficient evidence for a qualified bibliographic status in this audit.

A bound on simple zeros alone does not bound all zeros. Even analytic functions can have many nonsimple derivative zeros while having no simple ones. Neither finite arithmetic controls nor the family map closes that gap. This audit does not decide how the paper treats multiplicity, isochrony, hidden theorem assumptions, or its global analytic argument. No theorem number, proof reconstruction, or independent proof validation is supplied. A workflow requiring theorem-level certification must keep that separate verification gate open.

## Bounded public-source search

Fresh searches covered the exact title, DOI, author/title combinations, manuscript/PDF terms, arXiv, HAL, the authors' institutional domain, and correction/erratum terms. The public publisher entry and its legitimate opening-page preview were inspected. The institutional author-profile result did not provide the target manuscript. No readable full theorem or author manuscript was located through these bounded routes, and no relevant correction was found. No author was contacted, paid access attempted, credential used, or access restriction bypassed.

Fresh Crossref retrieval matches the frozen metadata bytes and reports no `update-to` entry and an empty `relation` object. Fresh OpenAlex reports closed access, no repository full text, no best open-access location, and no retraction flag. Its parsed response equals the earlier one although byte serialization differs. These are scoped metadata observations, not proof that no correction or manuscript exists. No current Crossmark status was independently established.

The frozen report of a failed publisher PDF retrieval remains historical evidence. This auditor did not download a full 2023 article PDF and does not assign one a hash. Source PDFs, extracted full text, raw API responses, and private coordination material are excluded from the audit publication allowlist.

## Portable checks and limitations

All ten content files match the frozen manifest's hashes and sizes, and the submission has its expected eleven-file allowlist including that manifest. Both pinned complete upstream corpora were independently rehashed; the selected problem is unique and exactly matches the supplied selection, and the complete AMR-046-0012 prior report matches its corpus entry. The older report's failure to locate a proof is superseded as a literature-search conclusion by the explicit 2023 publication attribution.

The supplied verifier passes normally and under Python optimization with 6085 checks, 858 monomials, and 500 degree pairs. Independent recount: monomial/scaling/derivative checks contribute 5070; degree-pair inequalities contribute 1000; remaining arithmetic and declared-metadata checks contribute 15. They do not numerically evaluate period functions and cannot certify the analytic theorem. In particular, checking that a status field says `already_solved` is a metadata-consistency check, not evidence for that status.

## Exact addendum and accounting recommendations

1. Preserve all original files and historical assessments. Record this audit as an additive assessment bound to the frozen hashes, changing only the latest interpretation of the pending-audit state.
2. Preserve historical `turns_used=0` and empty proof-attempt history. Add separate fields `campaign_turns_used=1`, `campaign_turn_limit=5`, `campaign_turn_kind=literature_verification`, and `new_proof_search_turns=0`. Do not rewrite the frozen zero to make it mean the broader campaign count.
3. Keep `full_published_proof_inspected=false`, `complete_candidate_proof=false`, and `new_mathematical_result=false`. Use `independent_audit=passed_attribution_only` in the new assessment, not an unqualified proof-verification label.
4. Optional source improvement: cite the inspected first-page preview specifically for the quasi-homogeneous vector-field degree convention. This strengthens the family map without pretending that the theorem statement was available.

Suggested public status sentence: Published prior resolution attributed to Zhuang and Liu (2023), whose primary abstract expressly identifies Gasull Problem 12; exact original-question and family-map checks pass, while the full theorem and proof remain uninspected.

This completes the requested source/classification audit. No new proof search or remote write was performed.
