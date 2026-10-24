# Independent priority check: Kourovka 21.136

Check date: 2026-10-24. Scope: bounded literature/status verification; no target proof attempted. Only primary sources support conclusions below. No outreach was prepared or initiated.

## Exact problem and priority status

The latest editor-maintained arXiv version is **1401.0300v49**, submitted **2026-10-20 09:15:18 UTC**. Its printed page 199 (zero-based PDF page index 198), Problem 21.136, asks whether a profinite group with fewer than continuum many conjugacy classes of infinite-order elements must be torsion. Its only recorded positive case is finite generation; it has no solution marker or additional qualification. This is strong current primary evidence that the general problem remains open, not a guarantee that every recent/unindexed work has been found. [Editor version](https://arxiv.org/abs/1401.0300v49).

## Wilson scope, including a source trap

John S. Wilson, *Profinite groups with few conjugacy classes of elements of infinite order*, **Archiv der Mathematik 120(6) (2023), 557–563**, DOI **10.1007/s00013-023-01851-4**, published 2023-04-19; preprint **arXiv:2209.14753v1**, 2022-09-29.

Theorem A assumes finite generation and concludes finiteness. Theorem B assumes an odd prime and a finitely generated Sylow subgroup; a bound on conjugacy classes of infinite-order p-elements makes that Sylow subgroup finite. The introduction describes the unrestricted locally finite conclusion as conjectural and discusses non-finitely generated, countably based pro-p groups. It supplies no theorem for every metrizable/countably based profinite group.

**Corollary 3.1 has an evident omitted hypothesis:** its printed statement lacks finite generation, but the preceding sentence restricts to that case, and its proof invokes Theorem C, which requires it. Both published PDF and arXiv v1 contain this omission. The literal unrestricted finite conclusion fails for the infinite product of copies of C_p (zero infinite-order elements). Interpret the corollary with finite generation; this is a contextual diagnosis, not an author-confirmed erratum. [Published paper](https://doi.org/10.1007/s00013-023-01851-4), [preprint](https://arxiv.org/abs/2209.14753).

## Other primary sources checked

- Wilson's **2024-04-16 MPI seminar abstract** still highlights the finitely generated result. It announces no general or metrizable extension. [Author talk](https://www.mis.mpg.de/de/events/event/profinite-groups-with-few-conjugacy-classes).
- Barnea–Camina–Ershov–Lewis, *On groups that can be covered by conjugates of finitely many cyclic or procyclic subgroups*, **Mathematische Annalen 392 (2025), 1747–1779**, DOI **10.1007/s00208-025-03119-4**, published 2025-03-29, cites Wilson as related work. It studies coverage by conjugates of procyclic subgroups, a different hypothesis, and is not a solution of 21.136. [Publisher](https://doi.org/10.1007/s00208-025-03119-4), [author PDF](https://m-ershov.github.io/Research/ncc_final2025.pdf).
- Wilson's earlier **Proc. AMS 150 (2022), 3297–3305**, *Profinite groups with few conjugacy classes of p-elements*, arXiv:2204.09936v2 (corrected 2022-09-29), bounds **all** p-element classes, including finite-order ones; for odd p it is equivalent to Sylow finiteness. It does not remove finite generation from the infinite-order-only question. [Corrected preprint metadata](https://arxiv.org/abs/2204.09936).

## Exact remaining gap and confidence

The verified target gap is the implication for **arbitrary profinite groups**, including non-finitely generated ones, from fewer than continuum many infinite-order conjugacy classes to absence of infinite-order elements. No resolution of the entire countably based/metrizable subclass was verified in this bounded search. Finite generation must not be silently replaced with countable basing, and fewer than continuum must not be silently replaced with countability. The full problem's torsion conclusion is weaker than finiteness: infinite profinite torsion groups already satisfy the hypothesis vacuously.

Priority assessment: **eligible as apparently open**, with high confidence from the 2026-10-20 primary problem list; the negative search result remains bounded evidence. No claim of a novel contribution is made.

## Reproducibility

Saved original primary PDFs/HTML and local plain-text extraction accompany this note. `source_receipts.json` records requested/resolved URLs, UTC retrieval times, byte counts, HTTP metadata and SHA-256 values. Direct alglog.org requests failed because its TLS certificate was expired; the versioned arXiv editor source was retrieved successfully without bypassing TLS checks.
