# Source and prior-work gate

Problem 30006359 / OWR-14299511-008 / rank 556. Checked 2026-10-04 UTC.

## Primary record and exact scope

The requested catalogue URL, https://www.unsolvedmath.com/problems/30006359, was attempted directly. The browser fetch failed; an HTTP request returned 403 with a Vercel mitigation header. No login, restriction bypass, or access assumption was used.

The matching public UnsolvedMath dataset record was recovered from a locally available copy of the public `problems.json` distribution at https://huggingface.co/datasets/ulamai/UnsolvedMath. Its stable record ID is 30006359 and its secondary ID is OWR-14299511-008. The record points to DOI 10.4171/owr/2025/34. Its generated literature assessment and corrected statement were treated as discovery aids, not mathematical evidence. The full dataset is not included in this packet.

The primary source is Zhengwei Liu, joint with Fan Lu, “Construct Subfactors by Classical and Quantum Computers,” in *Subfactors and Applications*, Oberwolfach Report 34/2025, especially printed pp. 1854–1856 (the contribution continues on p.1857). Workshop dates: 27 July–1 August 2025. The catalogue uses a 2026 bibliographic publication year; the workshop/report is numbered 2025. The actual conjecture appears on printed p.1855.

- DOI: https://doi.org/10.4171/OWR/2025/34
- Publisher PDF: https://ems.press/content/serial-article-files/52239
- Report-PDF SHA-256: 659162d6517cfba3559ffadb8e70eb38cfd28f3230c078178e984b84b86d57f7

The claim concerns irreducible components of algebraic consistency loci indexed by forest fusion supports. It is not a graph-theoretic edge-decomposition problem, an assertion about arbitrary polynomial systems indexed by forests, or merely the forest/exchange-relation equivalence. Reflection positivity is a further condition and is excluded from the algebraic classification claim. The report's own low-rank algebraic counts are 7 for rank three and 24 for rank four. Those counts are credited, not claimed as new.

## Detailed equation source and complete relevant arguments inspected

Fan Lu and Zhengwei Liu, *Classification of exchange relation planar algebras through sieving forest fusion graphs*, arXiv:2412.17790v1, submitted 23 December 2024.

- Abstract/version history: https://arxiv.org/abs/2412.17790v1
- HTML: https://arxiv.org/html/2412.17790v1
- PDF: https://arxiv.org/pdf/2412.17790v1
- TeX source: https://arxiv.org/src/2412.17790v1
- Retrieved PDF SHA-256: 3a6049a839d093e14b319ec53f9d4d9e84baf88051503d271a0d268afc65079e

The actual version history inspected lists v1 only. The OWR contribution anticipates an updated manuscript, but such an update was not present on that arXiv record at this check. We do not claim access to unpublished definitions or code.

Inspected arguments and their use:

- Section 2.1 and Proposition 2.1: basis convention, trace, convolution, involution, Frobenius reciprocity and unit coefficients. Used to transcribe the polynomial model, retaining conjugate indices.
- Theorems 3.4, 3.5 and 3.7 with their proofs: reducing faces and comparing adjacent versus nonadjacent evaluation moves, and extending to exchange and identity moves. Read to establish what the polynomial presentation is intended to encode; this packet does not purport to reprove the full planar-algebra reconstruction theorem.
- Theorem 3.8, complete equation list and its proof: both shadings, the three expressions for W(i,j,k), two-face equations, and the remaining tangle comparisons. Used to define the exact equation family checked.
- Lemma 4.5 and Theorems 4.6, 4.9, 4.10 with their complete proofs: alternating tree-cut coefficients, the cycle obstruction, the explicit canonical conventions, and linear dependence of convolution coefficients on dimensions. The core incidence argument is also proved independently in RESULT.md.
- Example 4.8: finite-group examples with perfect-matching supports. Credited only for this established class.

The displayed equations (3.5) and (3.6) are literally identical in the v1 PDF and TeX. The proof displays three separate expansions in (3.12), (3.14), (3.16). The final verifier includes the displayed comparison and also compares (3.12) with (3.16), using the actual conjugate indices from the TeX. Thus the bounded result does not rest on ignoring the third expansion or guessing a replacement equation. RESULT.md states this additional equation explicitly. We do not assert that the duplicated display is, by itself, a mathematical error; it might be redundant under other equations.

## Later public update

Fan Lu, *Classification of exchange relation planar algebras through sieving forest fusion graphs*, presentation dated 19–23 January 2026, slide 20:

https://tsimf.tsinghua.edu.cn/__local/D/AF/4F/D6F859C069AF8BF0346AC84C7EA_C613B5B3_4DA53.pdf

PDF SHA-256: 2650fc950edf298517e11219bed6337b9483587c1d0a5edfdc240778c1a20cf1

The presentation again labels irreducibility as a conjecture. Its graph definition, degree reduction and algebraic-versus-unitary distinction agree with the report. Public author publication pages checked point to the same arXiv paper:

- https://www.bimsa.cn/detail/flu.html
- https://www.math.tsinghua.edu.cn/info/1125/1907.htm

Exact-phrase searches for the forest decomposition, irreducible decomposition, and the arXiv identifier found no later primary proof or counterexample. This is a bounded search statement, not proof that no resolution exists anywhere. No generated “solved” claim was accepted.

## Actual repository history checks

Repository: https://github.com/AlecKriebel/Math

The live default-branch queue showed rank 556 as `queued`, `0/5`. Queue blob ID returned by the connector: 59dba610d333684751e889818d21f66aba29cec9. That row alone was not treated as proof of a fresh problem.

Additional actual checks:

- Default-branch code search for `30006359`: no matches returned.
- Pull-request searches, with explicit `is:pull-request`, for `30006359`, `14299511-008`, `"exchange relation"`, and `"forest decomposition"`: each returned total_count=0 and no incomplete-results flag.
- Broader `forest` and `consistency` PR searches returned other mathematical investigations; none concerned this target after inspecting titles and descriptions.
- Branch search for `30006359`: no matching branches, no continuation cursor.
- Commit search for `30006359`: no matching commits.
- Contents lookup for `unsolved_math_prioritization/attempts/30006359`: 404.
- A recursive main-tree retrieval failed with a transport-closed error. It is not counted as a successful whole-repository scan.

No prior target attempt was located in the successful checks. Untagged or unindexed work cannot be ruled out. The source and branch/history checks are sufficient to avoid intentionally duplicating a known attempt, not to claim an exhaustive historical search.

The repository AGENTS.md was read (blob 9744d9b0ca61394e2ff9f23a1e6d24af1129a7ff). No outreach, remote write, merge, release or DOI action was performed for this packet. Publication and independent review remain separate steps.

## Scope gate and exclusions

The gate supports a scoped partial-results packet, with original disposition **unsolved**. It does not support a full-solution label.

Verified boundaries:

1. Exact nonzero supports are saturated before taking closures.
2. All dimension variables are required nonzero. Positivity is not assumed or inferred.
3. The canonical coefficient choice is explicitly specified; arbitrary raw exchange coefficients are not classified.
4. Circle/trace normalization is accounted for explicitly; no irreducibility-preserving assertion about a restored double cover is made.
5. The finite computation covers all involution types only for ranks two through four.
6. The source's low-rank counts and finite-group examples retain credit.
7. Complete third-party PDFs, extracted texts, the public source corpus, and private context remain outside the public packet.

The remaining all-rank primeness and ambient-coordinate questions are stated in RESULT.md. Independent adversarial review is required before publication; no review verdict is asserted here.
