# Source and prior-attempt gate

Checked 2026-10-03 UTC. Rank 456, ID 20001546, AIM-GEOMETRIC_GROUP_THEORY-0055.

## Exact target

Does the affine Artin group

    A = <a,b,c | aba=bab, bcb=cbc, cac=aca>

act properly and cocompactly on some Helly graph?

This is AIM *Geometry and topology of Artin groups*, Section 4, Problem 4.2.
The catalogue title, “A character-twist obstruction on the extended Deligne Helly
graph”, describes the previous machine-generated partial result, not the question.
The intended target is the existence of ANY geometric Helly action.

## Source identity

- Exact catalogue URL https://www.unsolvedmath.com/problems/20001546 was requested:
  web extraction failed and an ordinary public HTTP request returned 403. No live
  page content is claimed.
- Current AIM URL http://aimpl.org/geomartingp/4/ was unavailable to web extraction.
- The original AIM archive was retrieved successfully as HTML through ordinary
  public HTTP: https://web.archive.org/web/20240828224700/http://aimpl.org/geomartingp/4/.
  Its Problem 4.2 exactly agrees with the displayed target. Its status is empty.
  The “Known for RAAGs...” remark belongs to the separate Problem 4.25 on systolicity.
- The primary workshop summary, https://aimath.org/pastworkshops/geomartingprep.pdf,
  printed page 2, explicitly names Thomas Haettel's question whether this Artin
  group is Helly, distinguishes A from A x Z, and reports discussion of a possible
  negative strategy, without supplying a proof.
- The pinned catalogue source at revision
  37e53eabe540fb458758e198be61634bd02ee008 was checked locally. Full-file SHA256:
  problems.json: 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf;
  research_results.json: 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b.
  Its original_statement agrees with the archive. Its prior report explicitly
  disclaims solving the original question.

## Current literature gate

No full resolution was located in the primary sources and targeted searches
checked on 2026-10-03. This is a bounded search result, not a proof of worldwide
openness or of novelty.

- Thomas Haettel, *Group actions on injective spaces and Helly graphs*, current
  author-hosted lecture notes, https://imag.umontpellier.fr/~haettel/Lecture_Notes_Helly.pdf,
  Section 13, Question 3 (printed page 55), explicitly asks this exact question and
  distinguishes the Helly property of the product with Z.
- Haettel–Huang, *New Garside structures and applications to Artin groups*, Duke
  Mathematical Journal 174 (2025), 1665–1722; arXiv:2305.11622v2,
  https://arxiv.org/html/2305.11622v2. Theorem D and Corollary G give A x Z Helly
  and A a geometric weakly modular/CUB model, not a Helly model. Section 5.2 and
  Corollary 4.5 identify the finite generating set tested below.
- Hoda, *Crystallographic Helly Groups*, arXiv:2010.07407v2,
  https://arxiv.org/html/2010.07407v2, proves the affine Coxeter group is not Helly.
  This is a different group: the pure-Artin kernel is infinite.
- Haettel, *Lattices, injective metrics and the K(pi,1) conjecture*, AGT 24 (2024),
  4007–4060, https://doi.org/10.2140/agt.2024.24.4007: the extended Deligne
  thickening is Helly, but its natural action has infinite parabolic stabilizers.
- Huang–Osajda, *Helly meets Garside and Artin*, Invent. Math. 225 (2021),
  395–426, https://doi.org/10.1007/s00222-021-01030-8: finite-type weak Garside
  and FC Artin groups are Helly. The full affine triangle is not FC.

## True prior-attempt gate

The live AlecKriebel/Math queue, blob c87c275c638939b8008fd58db80657491d14971e,
records rank 456 as queued, 0/5. GitHub searches for PRs containing 20001546,
Helly, or Deligne returned no matches. Branch searches for 20001546 and helly
returned no matches; the paginated search for 456 was exhausted and found only
unrelated dot/math-30004563. A default-branch code search for 20001546 returned
no indexed result (the directly fetched queue is the authoritative positive hit).
These are bounded negative repository checks; they do not establish that no
private or unindexed work exists.

The historical catalogue report is an explicitly scoped partial obstruction and
is not counted as a new proof attempt. This pass has a fresh budget of five
substantive written mathematical attempts. Retrieval, auditing, and packaging
are not proof attempts. No full-resolution certificate is appropriate at the gate.

Only authored text, small reproducible scripts, and their results are candidates
for publication. Source PDFs/HTML, raw corpus records, and private history stay
out of the public package. Publication and final queue updates remain gated.
