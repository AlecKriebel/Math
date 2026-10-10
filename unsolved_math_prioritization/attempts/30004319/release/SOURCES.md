# Source verification and current-literature scope

Checked 4 October 2026. Links below identify the sources; copyrighted full texts
are not included in this packet.

## Exact statement

- [Catalogue, problem 30004319](https://www.unsolvedmath.com/problems/30004319).
  Attempted first; web retrieval was unavailable and the direct request returned
  HTTP 403. No claim is made to have read the live page.
- [OWR 52/2019 report PDF](https://ems.press/content/serial-article-files/46832),
  [DOI](https://doi.org/10.4171/OWR/2019/52). The contribution “Root Graded Groups
  and the Blueprint Technique”, pp. 3260–3262, supplies the exact question on
  p. 3261. The adjacent C3 statement is a different target. The same page reports
  conditional results of Faulkner and of Mühlherr–Weiss for 5-plump Tits polygons;
  these extra hypotheses are not inserted here.

## Primary structure reference

- Torben Wiedemann, [*Root Graded Groups*, arXiv:2404.02042v1](https://arxiv.org/abs/2404.02042v1),
  2 April 2024. Full text inspected. §5.3.3, p.119, explicitly retains the open
  A2 problem. Definitions 2.5.2, 5.1.1, 5.1.12 and 5.6.2 fix the grading, ring,
  inverse, and coordinate conventions. Remark 5.6.11, p.129, is the source for
  the strong-unit Moufang input. Proposition 5.6.10 requires rank at least three.
  Proposition 5.6.6 and Remark 5.6.7 support the Weyl-word calculation.
  Proposition 8.2.6 gives the standard alternative/Moufang equivalence.
  The page containing 5.6.11 was also visually inspected to check parentheses.
- Egor Voronetsky, [*Root graded groups revisited*, arXiv:2406.03558v1](https://arxiv.org/abs/2406.03558v1),
  subsequently *European Journal of Mathematics* 10:50 (2024),
  [DOI](https://doi.org/10.1007/s40879-024-00760-2). Full text inspected.
  Its rank ≥3 restriction excludes the target; an existence theorem in that
  range does not yield a rank-two answer.

## Later primary-source checks

- Egor Voronetsky, [*Weyl elements in isotropic reductive groups*, arXiv:2601.14419v2](https://arxiv.org/abs/2601.14419v2),
  revised 6 May 2026. Full text inspected. Its announced open-problem resolution
  concerns squares of Weyl elements in isotropic reductive groups, not
  alternativity for every abstract A2-graded group.
- Tom De Medts and Torben Wiedemann,
  [*From cubic norm pairs to G2- and F4-graded groups and Lie algebras*, arXiv:2602.06147v1](https://arxiv.org/abs/2602.06147v1),
  5 February 2026. Full text inspected. The constructions concern cubic norm
  pairs and G2/F4 structures, not an unrestricted converse for A2.
- Pavel Gvozdevsky,
  [*Abstract isomorphisms of isotropic root graded groups over rings*, arXiv:2505.04749](https://arxiv.org/abs/2505.04749).
  Abstract-level scope check only: an isomorphism theorem for group-scheme
  point groups under conditions. It is not cited as a classification of all
  abstract A2-graded groups.
- Bernhard Mühlherr and Richard M. Weiss,
  [*Root graded groups of rank 2*, J. Comb. Algebra 3 (2019), 189–214](https://ems.press/journals/jca/articles/16120),
  [DOI](https://doi.org/10.4171/JCA/30). Publisher abstract checked. Its
  root-graded-group/Tits-polygon equivalence should not be mistaken for the
  unconditional alternativity theorem. The subscription text was not claimed
  as directly read.

The Faulkner and Tits-triangle results mentioned above were checked through
Wiedemann's explicit statements and references; their original full proofs
were not independently reread. In particular the unit-Moufang input is clearly
attributed, rather than presented as proved from scratch in this packet.

Targeted searches included combinations of “A2-graded”, “A_2-graded”,
“root graded groups”, “alternativity”, “Torben Wiedemann”, and 2025/2026.
These checks found no full resolution applicable to the exact target.
That negative search outcome is bounded evidence, not a proof that no such
publication exists. The strongest explicit open-status statement inspected is
the 2024 monograph.

## Repository/source-record provenance

The live queue read on 2026-10-04 lists rank 602 as queued 0/5. The default
branch head observed during the check was
`03c3cc4ee2502f6937185fb55d17e1143fe5b6ea`.
The target attempt directory returned 404. PR searches for 30004319 and
“alternativity” returned no matches. A broader A2 search returned unrelated
Helly-graph and analytic-function records; none duplicates this target.
The live `related_target_groups.json` has no 30004319 entry.

The prior individual desk review in `review_v2/reviews_3.json` suggested a
Hall–Witt route and identified the lack of independent root directions as its
obstacle. This checkpoint tested both aspects directly. The pinned imported
problem record matches the original statement; the separately pinned legacy
research-results corpus has no corresponding OWR record. Hashes of the source
record, corpora and locally inspected primary PDFs are recorded in
`SOURCE_PROVENANCE.json`, without redistributing their contents.
