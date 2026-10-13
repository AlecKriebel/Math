# Source, status, and prior-work audit

Checked: 2026-10-04 UTC. Numeric identity: **10400107**, code **AMR-103-0107**,
queue rank **605**. The truncated catalogue title is not the mathematical target.

## Exact source target

Tomotada Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*,
Geometry & Topology Monographs **4** (2002), 377–572. Problem 5.11,
C. Rourke and B. Sanderson, printed p.465, PDF page 93 (zero-based 92):

> Is there a natural quandle space whose cohomology groups are the quandle cohomology groups?

[Publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).
The complete problem and its adjacent remark were both extracted and visually
checked. The remark rules out naively treating the degenerate chains as the
cells of a rack-space subcomplex. Section 5.3, beginning on printed p.459,
specifies the ordinary quandle cochains with an abelian coefficient group A.
No finiteness or connectedness restriction is part of Problem 5.11.
The adjacent Conjecture 5.12 is a separate target and is not bundled here.

The requested catalogue page
[UnsolvedMath 10400107](https://www.unsolvedmath.com/problems/10400107)
was attempted first: the web tool could not open it, and direct retrieval
returned HTTP 403. The pinned imported statement matches the inspected primary
source. The catalogue's continued “Open” label is not a status certificate.

## Decisive published construction and correction

Katsumi Ishikawa and Kokoro Tanaka, *Quandle colorings vs. biquandle colorings*,
Topology and its Applications **345** (2024), article 108832,
[DOI 10.1016/j.topol.2024.108832](https://doi.org/10.1016/j.topol.2024.108832).
The publisher's introduction identifies §6.1 as the rigorous definition and
Remark 6.1 as the discussion of earlier faulty definitions.

The full primary text inspected is
[arXiv:1912.12917v2](https://arxiv.org/pdf/1912.12917v2), dated March 5, 2020,
posted March 26, 2020, 25 PDF pages. Section 6.1 on pp.17–18 specifies the
quotient and its CW structure, with nondegenerate tuples indexing cells.
Remark 2.1 on p.4 gives the quandle specialization. Remark 6.1 on p.18 explains
why the earlier disjoint-cube cone and another proposed quotient fail.
The all-degree cochain comparison in `PROOF.md` is derived from these explicit
cellular maps, rather than assumed from the word “quandle space.”

This establishes an existing affirmative answer. The 2024 publication date is
not being asserted as the earliest date of every part of the construction.
The inspected 2020 preprint is already sufficient prior work for the result.

## Historical false positive avoided

Takefumi Nosaka, *Quandle homotopy invariants of knotted surfaces*,
Mathematische Zeitschrift **274** (2013), 341–365,
[DOI 10.1007/s00209-012-1073-1](https://doi.org/10.1007/s00209-012-1073-1).
Definition 2.1 and §4.1 claim the desired realization, but the literal definition
uses a cone on a map from disjoint cubes. It is not the construction certified
here. The singleton cofiber calculation in `PROOF.md` rejects it.
Both the publisher's full HTML and
[arXiv:1011.6035v3](https://arxiv.org/pdf/1011.6035v3) were inspected.
The preceding 2011 Topology and its Applications paper defines only the relevant
3-skeleton, so it cannot alone certify an all-degree answer.

## Independent later primary corroboration

- Katsumi Ishikawa, *Extended quandle spaces and their applications*, OCAMI
  Reports **9** (2021), printed pp.69–72, §1 and Remark 1.1.
  [Institutional proceedings](https://ocu-omu.repo.nii.ac.jp/record/2020728/files/111F0000022-009.pdf).
  It uses the equal-sum quotient, credits Ishikawa–Tanaka, and states the quandle
  homology realization for arbitrary quandles.
- Katsumi Ishikawa, *Efficient knot invariants from quandles*, Osaka Journal of
  Mathematics **62** (2025), 467–476, printed p.470 and references [8]–[9].
  [Institutional version of record](https://ir.library.osaka-u.ac.jp/repo/ouka/all/102435/ojm62_03_467.pdf).
  It again uses the corrected quotient and cites the 2024 published construction.

The current literature check searched the exact original question, “quandle
space” with cohomology and homology, the Nosaka construction, its errors, and
Ishikawa–Tanaka's correction. It is a focused status check, not a claim of an
exhaustive bibliography. The affirmative conclusion rests on the actual
construction and chain comparison, not on absence of contradictory search hits.

## Repository and duplicate checks

Read-only inspection of AlecKriebel/Math pinned `main` at
`03c3cc4ee2502f6937185fb55d17e1143fe5b6ea` found:

- `unsolved_math_prioritization/QUEUE.md`, rank 605: `queued`, `0/5`.
- Selected catalog record: the same identity, statement and review hashes below.
- No entry for `10400107` in `state.json`.
- The path `unsolved_math_prioritization/attempts/10400107` did not exist, and
  the commit-history query for it returned an empty array.
- PR search for `10400107` returned no results. A wider “quandle” PR search found
  PR 87 on Ohtsuki Conjecture 5.3, a different question about Vassiliev invariants.
- `review_v2/related_target_groups.json` has no group containing this target.
- A scan of all pinned statements for quandle space/cohomology context found
  nearby problems 10400099, 10400100, 10400102, and 30004307; none duplicates
  the space-realization target. Virtual-knot records 10600006 and 10600046 are
  also distinct. No status change for those records is recommended.

The upstream report merely called the question open-triage and requested a
thorough literature search. The effective desk review already cautioned that
newer constructions needed checking. Neither contained a proof attempt or
competing resolution to preserve as a local candidate.

## Immutable provenance

Dataset: `ulamai/UnsolvedMath`, revision
`37e53eabe540fb458758e198be61634bd02ee008`.

- `problems.json`: 68,931,837 bytes; SHA-256
  `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- `research_results.json`: 80,334,822 bytes; SHA-256
  `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`
- Selected statement hash:
  `e9b81c2960e4a0d187aaebd700e22a2c56c7bb0463637a13461704d85acd7204`
- Selected review hash:
  `502b8c9cbe11de3f2111c08c258cb6a9efaeb341baf7db8df8efb81515520801`

Privately retained source-byte checksums, without redistributing those bytes:

- Ohtsuki publisher PDF, 4,731,008 bytes:
  `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd`
- Nosaka arXiv v3 PDF, 447,273 bytes:
  `ff9c123cb2d4df57d2ff34e7b6caed83edf9953d721cf53c53d87885137d7e61`
- Ishikawa–Tanaka arXiv v2 PDF, 2,541,803 bytes:
  `7a836f75420f0cb3a364ea9b1fbc1c9818a6dc25a78ff00ff6638f563654204a`
- OCAMI Reports 9 proceedings PDF, 5,770,570 bytes:
  `b0d2dbf339ba6b2db928736c17fbf61c3177a3d1b04041362061009b349e430e`
- Ishikawa 2025 institutional PDF, 930,100 bytes:
  `b4c0d9583d7b7d6e12a3447ed6e329e8ca747bb2f293f80f342727eb6907d475`

## Disposition

Recommended `already_solved`, `1/5`: one substantive complete verification of
the existing corrected construction. No novel contribution or priority claim.
No mathematical gap remains in the exact ordinary-cohomology target;
independent audit of this submitted verification remains required.
