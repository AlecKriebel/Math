# Bounded priority audit: broader theorem resolutions

Audit date: 2026-10-14 UTC / 2026-10-13 America/Los_Angeles. Frozen candidate commit: `5bee5139501a399da653f634147eab9433774ac7`.

**Finding:** no exact predecessor or broader theorem immediately proving the frozen claim was identified in the freshly inspected primary sources below. This is a bounded search result, not a certification that the claim is first, novel, or currently open. The candidate proof itself was not audited or developed in this lane.

The exact claim is existence of a dense G_delta subset of **Act(W)**, the Polish space of all continuous actions of the restricted wreath product W = Z wr Z on Cantor space, on which the **entire** Borel orbit relation is hyperfinite. A generic subset consisting of free actions can satisfy that claim; “all” specifies the ambient action space, not that every nonfree action must be hyperfinite. An invariant comeager subset of Cantor space or a measure-dependent conull subset is an insufficient replacement.

## Primary theorem comparison

| Primary source and locator | Relevant scope | Exact remaining mismatch |
|---|---|---|
| Iyer–Shinko, arXiv:2409.03078v1, pp. 2, 4–6, Theorems 3, 18, 19 | Generic whole-space hyperfiniteness for groups locally of finite asymptotic dimension; free actions form a dense G_delta (Proposition 8). | W is finitely generated and contains Z^d for every d, so has infinite asymptotic dimension. The final paragraph of p. 2 explicitly excludes the then-unresolved generic W case. [Primary paper](https://arxiv.org/pdf/2409.03078v1). |
| CJMST, freshly retrieved author PDF, pp. 3, 28–33, Theorems 1.3, 6.4, 7.1, 7.3 and Corollaries 7.4–7.5 | Certain normal series give finite Borel asymptotic dimension for free actions. The union theorem requires finite Borel asymptotic dimension of each metric and metric compatibility. | Finite Prüfer rank and finite Q-rank hypotheses exclude the infinite-rank lamp kernel. The designated lamplighter is Z_2 wr Z. Page 33 explicitly says W is not a union of finite-asymptotic-dimension groups. Finite-rank lamp pieces alone do not exhaust shift edges. [Author PDF](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf). |
| Grebík–Marks–Rozhoň–Shinko, arXiv:2608.22565v1, pp. 2–5, 13–18, Theorems A/C and 4.7/4.10 | A: decreasing metrics with pointwise growth exp(O(r^gamma)), gamma approximately 0.1523. C: quantitative dimension-growth criterion; polynomial form dim_B(s,C_m s^a)=O(s^b), ab <= 1/4. | Ordinary free W orbit metrics have exponential growth. No W-specific generic dimension bound or metric construction is supplied. Applying C to independently constructed compatible slabs would still require that construction. Page 5 retains W as a Weiss test problem; that addresses all Borel actions, not exact generic Cantor priority. [Primary paper](https://arxiv.org/pdf/2608.22565v1). |
| Naryshkin–Vaccaro, published Forum of Mathematics, Sigma 14:e29 (2026), pp. 2–3, 9, 15–17, Theorem 2, Corollary 3, Proposition 3.10, Corollaries 5.3–5.4 | Treeable hyper-u-amenable relations are hyperfinite; amenable group actions are hyper-u-amenable. | A Borel treeing of the entire generic W orbit relation remains an additional hypothesis. Neither metabelian structure nor amenability establishes it in this source. Freeness supplies treeability for virtually free groups, a different group class. [Published article](https://doi.org/10.1017/fms.2026.10171). |
| Shinko–Weilacher–Yu, arXiv:2608.18439v2, pp. 1–4, Theorems 1.5–1.7; Wang, arXiv:2609.17177v1, pp. 1–2, Theorem 1.1/Corollary 1.3 | Bounded-to-one actions of countable commutative monoids have hyperfinite relations. Wang removes freeness from the finite dimension statement for finitely generated commutative monoids. | W generators act bijectively but do not commute in free W actions. Lamp commutativity does not include the shift. These results cover lamp-only subrelations, not their semidirect extension. [SWY](https://arxiv.org/pdf/2608.18439v2), [Wang](https://arxiv.org/pdf/2609.17177v1). |
| Thornton, arXiv:2510.10882; current author PDF, pp. 23, 28–29, 37, Proposition 3.10/Corollary 3.11/Problem 4.2 | Generic and generic minimal hyperfiniteness remains proved under finite asymptotic dimension; the generic amenable/exact/residually finite case is posed as a problem. | No infinite-rank wreath-product extension appears in these relevant passages. [Current author PDF](https://borowiecki.dev/pdf/2510.10882), [version metadata](https://arxiv.org/abs/2510.10882). |

## Checkable scope exclusions (auditor deductions)

Write W = A semidirect Z, with A = direct sum over Z of Z, and let t shift lamp coordinates and a be the unit lamp at coordinate 0. For every d, lamps at d distinct coordinates generate a subgroup Z^d. Thus W has unbounded Prüfer rank and A has infinite Q-rank. This also explains the finite-asymptotic-dimension obstruction: standard asymptotic dimension is monotone for subgroups and asdim(Z^d)=d. CJMST p. 33 independently records that W is not a union of finite-asymptotic-dimension groups. Finite normal-series or finite-rank hypotheses cannot be satisfied merely by describing W as metabelian or abelian-by-cyclic.

For each binary vector epsilon of length n, the word

`(a^epsilon_0 t)(a^epsilon_1 t)...(a^epsilon_(n-1) t)t^(-n)`

has length at most 3n and produces a distinct lamp vector on coordinates 0 through n-1. Hence ordinary W word balls have at least 2^n elements at radius 3n. Every orbit of a free W action has the same lower bound. This contradicts exp(Cr^gamma) bounds for any fixed C and gamma < 1, including both the proved GMRS exponent and the announced approximately 0.1716 improvement. It excludes the direct word-metric growth application; it does **not** exclude a new construction of other Borel metrics satisfying Theorem C.

The lamp subrelation is covered by commutative-action theorems, and the shift alone is a Z-action. Their combination is not automatically covered by either theorem. Finite-rank lamp-subgroup exhaustion misses the shift unless additional slabs or metric structures are built. Their finite Borel asymptotic dimension and compatibility are exactly hypotheses needing proof, rather than consequences of a general arbitrary-union theorem.

## Additional dated boundary evidence and bibliography

Iyer's January 12–17, 2025 Oberwolfach workshop contribution, “Generic actions of countable groups,” printed pp. 114–115 (PDF pp. 40–41), explicitly asks the generic W question as Question 3. It is evidence of the source's 2025 status, not a statement about the whole world's literature on the audit date. [Report 2/2025, DOI 10.4171/OWR/2025/2](https://oa.tib.eu/renate/server/api/core/bitstreams/c9fee89b-4b9c-410d-be29-350e1a9ab305/content).

Iyer–Shinko's arXiv record exposes v1 only, submitted September 4, 2024. EMS reports the published paper under DOI 10.4171/GGD/896, accepted February 24, 2025 and published online May 6, 2025. The paper therefore should be cited as a published 2025 predecessor, with arXiv v1 identifying the content inspected here. [ArXiv record](https://arxiv.org/abs/2409.03078), [publisher record](https://ems.press/content/serial-article-files/50464?nt=1).

The authenticated arXiv PDF prints September 6, 2024; generated HTML displays August 24, 2026 despite carrying v1. No new version or mathematical revision is inferred from that generated date. The Berkeley author PDF URL returned 404 on direct fresh retrieval; indexed extracts from it were used only as discovery leads and were checked against the downloaded arXiv PDF.

## Inspection limits and provenance

The downloaded primary documents, SHA-256 hashes, retrieval timestamps and URLs are recorded in `download_manifest.json`; exact inspection scopes are in `inspection_ledger.md`; searches are in `query_ledger.md`. Most sources were inspected in the complete relevant theorem passages, definitions, applications and union proofs, not independently re-proved. Iyer–Shinko was read completely. No historical audit conclusions were imported, no candidate proof search was performed, and no Git/service/contact mutations occurred. Negative findings are limited to this stated corpus and search scope. Unindexed manuscripts, missed references, or new results could change them.

**Audit completion estimate: 100% of this assigned bounded broader-resolution audit.** This percentage is not a probability of novelty, priority, or correctness of the candidate result.
