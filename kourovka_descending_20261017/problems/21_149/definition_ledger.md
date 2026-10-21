# Dlab definition ledger and priority refresh

Checkpoint: 2026-10-17T20:23:26.836192+00:00 (file write time; root corrected an erroneous future timestamp supplied by the subagent).
Completion estimate: 70% of endpoint-definition audit, 95% of preliminary priority refresh. No mathematical solution status is assigned by this ledger.

## Evidence provenance

**Full primary text read:** V. Dlab (1968), Section 2 and Theorems 4.1–4.3, original Cambridge PDF, [DOI](https://doi.org/10.1017/S1446788700006261). This directly establishes the locally right affine definition at every a in [0,1), including a=0, and allows arbitrary positive-real slope subgroups H. Compact support and the one-sided interval subgroups use identity on endpoint neighborhoods. Hence right affine behavior at the finite left endpoint is not optional.

**Full primary text read:** [Gong–Yang–Zeng v1, September 16 2026](https://arxiv.org/html/2609.18630v1). Its authors explicitly restrict the main theorem to six rank-one families, omit reflected extended-real D_*H, and disclaim higher-rank ambient conclusions. This does not determine the full primary reflected-family definition.

**Indexed primary excerpt, NOT downloaded or inspected page image:** Zenkov–Medvedev (1999), printed p. 543, indexed by the search engine under [the MathNet full-text PDF URL](https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=2480&what=fullt). Direct web opening and command-line downloading timed out. The indexed page title is “О группах Длаба 543.” Therefore the following evidence should be checked against actual PDF pixels before a preprint relies on it.

The indexed passage places the reflected group inside the full group and states that the reflected group has continuum many bi-orders. The only preserved verbatim primary excerpt is in primary_left_germ_evidence.md.

The same indexed Proposition 2.3 gives the displayed group decomposition, here transcribed mathematically rather than copying its prose:

\[
D_{*H}\cong D_H\rtimes B,\qquad B\cong T_H
\]

for rank-one H, with a domination property in every group order. The proposition explicitly says its proof follows Proposition 2.2. Definition of T_H was not yet read from the primary definition page. It is expected to be the affine group from context, but **that expectation is not verified here**. Do not infer “eventually affine at minus infinity” as a primary-source quotation from p.543 alone.

## Consequence and open definition gap

The reflected D_*H is genuinely orderable according to Proposition 2.3. It cannot be replaced by the unrestricted group of every finite-point locally-right-affine homeomorphism having support bounded above if that broader group contains a nontrivial element conjugate to its inverse. The restriction comes from its containing master group bar(D)_H, whose endpoint definition remains to be obtained exactly.

An eventual affine germ at minus infinity would provide the correct structural restriction, but the passage from the primary bar(D)_H definition to that property remains an explicit citation gap. A proposed theorem for the larger class A_R of maps locally affine on finite right neighborhoods and affine on an initial ray would be mathematically meaningful independently of this citation gap. Identifying all classical Dlab families with subgroups of A_R requires the missing source verification.

No claim that reflected D_*H lacks a bi-order is justified. Nor is a restriction of the Kourovka target class to the six groups in Medvedev (2001) justified merely by that paper's scope.

## Reproducible search trail for indexed p.543

On 2026-10-17 the web search queries below all returned the MathNet primary PDF as a result containing p.543 and Proposition 2.3:

- `"О группах Длаба" "289–298" doi` (bibliographic route)
- `"О группах Длаба" "§ 2"` (returned p.543)
- `"О группах Длаба" "Группа" "ограниченным"`
- `"Длаба" "T_H" "2.2"`
- `"Длаба" "полупрямым" "T" "-1"`

The URL and page number are stable. Search snippets sometimes expose a complete page-sized excerpt, but this is search-index evidence, not a successful full-document retrieval. Bibliographic metadata is independently confirmed at the [Springer journal page](https://link.springer.com/article/10.1007/BF02671746): Algebra and Logic 38 (1999), 289–298; DOI 10.1007/BF02671746; Russian original 531–548.

## Broader priority refresh, September 16–October 17 2026

The current [arXiv abstract record](https://arxiv.org/abs/2609.18630) lists only v1 (September 16), and no higher-rank extension appeared in its displayed version history at the time of audit.

The following independent search families were run on the audit date:

- `"Dlab" "automorphism" "higher rank"`
- `"Dlab groups" "higher-rank"`
- `"Dlab groups" "arbitrary" "automorphism"`
- `"Dlab group" after:2026-09-15 before:2026-10-18`
- `"Dlab" "automorphism" site:arxiv.org/abs/`
- `"Dlab" "embedding" site:arxiv.org/abs/`
- `"Kourovka" "21.149"` excluding stale aggregator domains
- `"Dlab groups" homomorphism`
- `"Dlab groups" conjugate embedding`
- `"Dlab" "normalizer" "automorphism"`
- `"Dlab" "diagonal" group`
- `"Dlab" "embedding" "rigidity"`
- `"locally right" "automorphism" group conjugation`

Only the September Gong–Yang–Zeng preprint, the original-formulation Aristotle/van Doorn–Judin–Monticone–Morrison work, Dlab's original article, and older order classifications were materially relevant. No independently indexed higher-rank extension, two-endpoint obstruction, or all-ambient solution was found. This is a negative search finding, **not an exhaustive priority certificate**: indexing lag and inaccessible databases remain possible.

[Bludov–Glass–Kopytov–Medvedev (2009), arXiv:0906.2621](https://arxiv.org/html/0906.2621), problem 3.23, asks for the automorphism groups of interval and real-line Dlab groups. Its comments refer to Kopytov–Medvedev books for definitions; they do not supply an answer to the ambient-embedding question. This is a related older formulation requiring bibliographic acknowledgment if a broad automorphism theorem is proposed.

## Candidate-mechanism originality gate

The one-endpoint descending support obstruction is already prior art in the September preprint. A two-endpoint modification alone is not automatically a new solution: its added mathematical content must be precisely the treatment of previously omitted embeddings or ambient orders. The all-slope embedding theorem, if established, would need comparison with general topological action/reconstruction rigidity results, including results stated under piecewise-linear rather than Dlab terminology. No equivalence/immediate implication was found in the searches above, but that broader comparison remains required before first-discovery language.


## 2026-10-17T20:30:06.031317+00:00 — Scope reconciliation

The root and fresh independent scope reviewer reproduced the complete relevant primary p. 542 paragraph using the exact batch in primary_left_germ_evidence.md. It factors EVERY full real Dlab element into an affine map and an element fixing an initial ray. Along with p. 538 and the reflected-subgroup inclusion on p. 543, this closes the standard-real-family left-germ scope gate. The lack of downloadable PDF pixels remains an access limitation, not an unresolved mathematical ambiguity. Older pending-scope statements above are historical. Final assembled-package adversarial reviews and publication checks are still required.
