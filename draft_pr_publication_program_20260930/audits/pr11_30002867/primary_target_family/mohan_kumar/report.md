# PR11 primary theorem source audit: N. Mohan Kumar (1978)

Final checkpoint: 2026-10-01 05:07 UTC. Completion estimate: **100% of this bounded theorem-source audit**. This is not a completion estimate for PR11's research program or a full priority audit.

## Verdict and exact checked proposition

**The original primary theorem is directly accessible and its statement is verified.** The scan of N. Mohan Kumar, *On two conjectures about polynomial rings*, *Inventiones mathematicae* **46** (1978), 225–236, contains Theorem 5 on printed page 234, with its proof continuing on page 235. The DOI is [10.1007/BF01390276](https://doi.org/10.1007/BF01390276). The [publisher record](https://link.springer.com/article/10.1007/BF01390276) verifies the bibliographic identity; the [Göttingen institutional scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0046/LOG_0020.pdf) supplies the full text.

The exact mathematical content checked, with the generator count renamed to avoid collision with the number of variables, is:

\[
R=S[X_1,\ldots,X_d],\quad S\text{ a field or a principal ideal domain},\quad
r=\mu_R(I/I^2)\geq\dim(R/I)+2
\quad\Longrightarrow\quad\mu_R(I)=r.
\]

The source prints “any ideal”; applications here should use a proper ideal with nonzero quotient, so no convention for the dimension of the zero ring is required. Printed page 226 defines \(\mu(M)\) as the global minimum number of generators of the \(R\)-module \(M\) and dimension as Krull dimension. Since \(I/I^2\) is annihilated by \(I\), its generator count over \(R\) equals its generator count over \(R/I\).

There is **no infinite-field, algebraic-closure, perfection, or characteristic restriction** in Theorem 5. The threshold is inclusive. The statement has no smoothness, radicality, or local-complete-intersection assumption. The field case requested by the audit is a specialization of the source's field/PID statement. It establishes existence of a generating set of size \(r\); it does not state that every prescribed conormal generating tuple lifts to a generating tuple of \(I\).

## Provenance and exact bytes

The GDZ catalog [METS record](https://gdz.sub.uni-goettingen.de/mets/PPN356556735_0046.mets.xml) identifies article `LOG_0020`, author N. Mohan Kumar, title *On Two Conjectures About Polynomial Rings*, extent 12 pages, and older article identifier `GDZPPN002094266`. Its structural links map the article to printed pages 225–236. The downloaded PDF has an archive cover followed by these twelve scanned pages: Theorem 5 is PDF page 11 (zero-based index 10), and its continuation is PDF page 12 (index 11). The [older resolver](https://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002094266) redirects to the same volume viewer.

| Fetched item | Bytes | SHA-256 | Fetch time, UTC |
| --- | ---: | --- | --- |
| Original GDZ article PDF | 1,264,895 | `801159ec9a1ce67d6c193cde82554453dacde8d1b670cecdda2b346eb53a75fd` | 2026-10-01 05:03:09 |
| GDZ volume 46 METS XML | 503,676 | `3c6d73a7f479516a836f4237c2a0163e91730be58630cf660247747b9333804a` | 2026-10-01 05:02:03 |
| Das arXiv v4 PDF | 297,608 | `5774f5d199468e1428455ec9be1ba79c4e7559d70115a0ee6bbba5499605e06f` | 2026-10-01 04:59:59 |
| Das arXiv v4 source gzip | 27,330 | `4554707ee150abc8ac8b7bc4b2419e3390c2a2900a7c3837affe4ffb614ce92e` | 2026-10-01 05:02:01 |

[source_manifest.json](source_manifest.json) records requested/resolved URLs, HTTP statuses, MIME types, sizes, hashes, and timestamps for the successful key fetches and failed initial access paths. Full PDFs, extracted text, TeX, catalog XML, and rendered pages remain only under the assigned ignored scratch directory `../../tmp/primary/mohan_kumar/`; none is included in this report folder.

## Visible proof dependencies and bounded verification

The entire printed proof on pages 234–235 was visually inspected. Its direct internal dependencies were also inspected in the original scan:

| Dependency | Primary locator | Role and verification limit |
| --- | --- | --- |
| UFD height-one reduction | p. 234, first proof paragraph | Removes principal height-one components. The printed assertion was checked; this audit does not separately reconstruct that reduction for all ideals. |
| Bass, reference [1], §4, Lemma 3 | p. 234; bibliography p. 235 | Supplies a coordinate change giving a monic polynomial after the height reduction. The citation is visible; the external result is not independently reproved here. |
| Internal Lemma 4 and Corollary 3(i),(ii), with \(t=0\) | Lemma 4, pp. 230–231; Corollary 3, p. 231 | Controls conormal generators and unwanted primes in the quotient modulo \(J^2\). The statements and prime-avoidance proof of Lemma 4 were visually checked. |
| Internal Theorem 2 patching argument | pp. 232–233 | Supplies the local-generation, module-patching, and extension-localization mechanism referred to by “as before” in Theorem 5. These exact pages were visually checked. |
| Quillen–Suslin, reference [7], Theorem 3 | p. 235; antecedent use p. 233 | Gives freeness of the kernel of a unimodular row having a monic entry on the overlap. The external theorem is a retained classical dependency. |
| Quillen–Suslin, reference [7], Theorem 4 | p. 235 | Makes the final rank-\(r\) projective module free over the polynomial ring. The external theorem is a retained classical dependency. |

Reference [7] is D. Quillen, *Projective modules over polynomial rings*, *Inventiones mathematicae* **36** (1976), as printed on p. 236. This audit checks the explicit dependency chain, not every cited foundational proof.

On the \(\operatorname{ht}(I)\geq2\) branch, I independently replayed the last patching step conditional on the stated monic-row and polynomial-projective-freeness results. Set \(J=I\cap A\). The construction produces \(g\in1+J\) and an exact sequence over \(R_g\) with free middle module of rank \(r\). Because \(g-1\in I\), one has \(I_{g-1}=R_{g-1}\). The kernel on the overlap is free of rank \(r-1\), so it can be patched with a free module on \(D(g-1)\). The extension-localization map is an isomorphism: it is an isomorphism on \(D(g)\) and both extension modules vanish on \(D(g-1)\), since the localized ideal is the ring. The resulting middle module is locally free of rank \(r\) on the covering \(D(g)\cup D(g-1)\). The cited global freeness theorem therefore yields \(R^r\twoheadrightarrow I\), and the universal inequality \(\mu(I/I^2)\leq\mu(I)\) yields equality. This checks the proof's relevant mechanism without asserting an independent reproof of Bass or Quillen–Suslin.

The peer `pr11_homology_global_adversary` independently viewed printed pages 234–235 and confirmed the field/PID hypothesis, inclusive threshold, absence of field restrictions, and patching dependencies. No mismatch was reported.

## Das restatement, versions, and date discrepancy

[Mrinal Kanti Das, arXiv:1710.04281v4](https://arxiv.org/abs/1710.04281) independently corroborates the field specialization. Its [PDF](https://arxiv.org/pdf/1710.04281v4), printed p. 1, Theorem 1.2, gives the exact field case above; the preceding paragraph identifies Mohan Kumar [23, Theorem 5]. Reference [23], printed p. 24, is the 1978 paper. This is a **statement restatement and attribution**, not a new proof of Theorem 5.

The current arXiv record reports v1 submitted 11 October 2017, v2 on 24 October, v3 on 7 November, and v4 on 14 December 2017. Its comments direct readers to ignore v1; describe v2 as revised and expanded; identify Example 3.6 as the v3 addition; and report typo/slip fixes in v4. The PDF banner and versioned URL both identify v4, 14 December 2017.

The fetched PDF nevertheless prints `Date: November 11, 2021` on p. 1. Its PDF metadata gives creation/modification time 11 November 2021 at 02:22:18 UTC. The current [HTML rendering](https://arxiv.org/html/1710.04281v4) instead prints `Date: August 24, 2026`. The fetched [v4 TeX source](https://export.arxiv.org/e-print/1710.04281v4) contains `\date{\today}`. Thus the internal date is generated at compilation; it is **not** evidence of an arXiv revision in 2021 or 2026. The precise source identifier should be v4 (14 December 2017), optionally accompanied by the fetched-byte hash. “PDF internally dated November 11, 2021” is accurate only as a description of these fetched PDF bytes.

Targeted searches for a correction/erratum to the 1978 title and to Das's title/arXiv identifier found no specifically matching correction of this theorem statement. That is a bounded search result, not an exhaustive claim that no correction exists. The better-known errata on later Murthy-conjecture claims are outside this bounded source path and do not alter what this original scan states.

## Remaining limits and research log

The original-source-access and statement-verification gaps are closed. This audit does not verify the candidate's numerical inputs \(r\) and \(\dim(R/I)\), reconstruct every classical external theorem, audit all later stronger claims, or certify novelty. Those tasks belong to the other assigned routes. There is no source blocker to citing the original Theorem 5 accurately with the exact hypotheses above.

- 2026-10-01 04:59 UTC — 35%: publisher identity and Das v4 located; original publisher access was subscription-only.
- 2026-10-01 05:01 UTC — 55%: Das theorem page visually verified; compile-date discrepancy isolated; original archive search continued.
- 2026-10-01 05:03 UTC — 80%: GDZ METS resolved the correct article; original 12-page scan fetched and hashed.
- 2026-10-01 05:05 UTC — 95%: original Theorem 5 and proof pages inspected; internal Corollary 3/Lemma 4 and Theorem 2 dependencies mapped.
- 2026-10-01 05:07 UTC — 100%: peer source reading corroborated the statement; date source, limits, manifest, and report recorded.

No snapshot edits, Git operations, publication, or external communication were performed. An attempted subagent delegation was unavailable because all team slots were occupied; the separate active homology adversary supplied the independent corroborating check.
