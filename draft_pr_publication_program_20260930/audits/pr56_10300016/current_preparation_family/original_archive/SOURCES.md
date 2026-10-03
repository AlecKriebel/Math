# Sources and status audit

Checked 30 September 2026. Full PDFs of the four references below were
retrieved; the cited sections and their surrounding hypotheses were read.
This is a focused primary-literature audit, not a claim to have checked every
proof in the 133-page Landry–Tsang paper.

1. Danny Calegari, *Problems in foliations and laminations of 3-manifolds*,
   arXiv:math/0209081v1 (2002).
   [Record](https://arxiv.org/abs/math/0209081),
   [PDF](https://arxiv.org/pdf/math/0209081).
   Exact target: Question 7.1 (Agol), printed p.13, also visually inspected.
   Definitions 1.9–1.10 and both following remarks were checked. The
   triangulation in the remark is auxiliary, not a hypothesis of Question 7.1.
2. Ian Agol, *Ideal Triangulations of Pseudo-Anosov Mapping Tori*,
   arXiv:1008.1606v2 (21 August 2010), later in Contemporary Mathematics 560
   (2011), 1–17.
   [Record](https://arxiv.org/abs/1008.1606),
   [PDF](https://arxiv.org/pdf/1008.1606).
   Theorem 3.5, pp.6–7, and the layered construction in Section 4 were checked.
   The periodicity is modulo the supplied pseudo-Anosov map and measure
   rescaling; it is not a theorem about every embedded branched surface.
3. Michael P. Landry and Chi Cheuk Tsang, *Endperiodic maps, splitting sequences,
   and branched surfaces*, Geometry & Topology 29 (2025), 4531–4663.
   [DOI](https://doi.org/10.2140/gt.2025.29.4531),
   [published PDF](https://msp.org/gt/2025/29-9/gt-v29-n9-p02-p.pdf),
   [preprint](https://arxiv.org/abs/2304.14481).
   Checked the introduction; Theorems 4.10, 7.10, 9.22; Definition 8.3;
   Lemma 9.21; and the discussion of full-support measures in Example 10.6.
   The full-support measure caveat is consistent with the distinction in
   Approach 1, but no new geometric example is inferred from it here.
4. Ian Agol and Tao Li, *An algorithm to detect laminar 3-manifolds*, Geometry
   & Topology 7 (2003), 287–309.
   [DOI](https://doi.org/10.2140/gt.2003.7.287),
   [full journal PDF](https://www.maths.tcd.ie/EMIS/journals/UW/gt/ftp/main/2003/2003-8.pdf),
   [preprint](https://arxiv.org/abs/math/0201310).
   Definitions 3.1, 3.3; Theorems 3.2, 3.5; and Lemma 3.4, pp.293–295.
   The bounded-cell enumeration in Lemma 3.4 retains sheet order and pairing
   restrictions. It is not, by itself, a finite bound on self-return witnesses.

## Imported record and prior-attempt gate

The pinned UnsolvedMath record and report were read at dataset revision
`37e53eabe540fb458758e198be61634bd02ee008`. The numeric ID and problem code match
uniquely. The imported report is third-party source triage and does not establish
a previous attempt by this repository's author. Its attribution to
“Landes–Taylor” was not used; the relevant primary work located here is by
Landry–Tsang.

Before this attempt, the live queue row was queued, 0/5. Exact-ID and title PR
searches, branch/path history, local attempt directories, and related-target
metadata revealed no prior attempt at this target. Other Question 7.x records
are different questions. No previous result was reset or overwritten.

## Search limitation

Current searches included the exact question, self-splitting/self-similarity
terminology, Agol's periodic splitting results, the Landry–Tsang program, and
splitting-complex radius criteria. No verified general characterization was
located. This negative search finding is weaker than proving that the problem
remains open in all literature. The mathematical stopping point is instead the
explicit missing converse and completeness estimate in `OBSTRUCTION.md`.
