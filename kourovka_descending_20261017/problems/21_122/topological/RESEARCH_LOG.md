# Topological approach to Kourovka 21.122

## 2026-10-24T23:12:22Z — checkpoint 1

Discovery estimate: 2% toward a complete solution of the exact value-set dichotomy. No solution claimed.

Scope: a word map `w:G^d -> G` on an arbitrary profinite group; prove that its image is finite or has at least continuum cardinality. This concerns the value set, not finiteness of the closed verbal subgroup.

Mechanisms pursued independently: scattered compact image geometry, Cantor fusion, metrizable quotient reduction, finite inverse-system branching constraints. Read repository AGENTS.md; no outside communication or independent Git publication. Parent handles publication.

Primary sources checked: Shumyatsky, arXiv:2401.15707v2; Detomi–Klopsch–Shumyatsky, arXiv:1907.01344v2; de las Heras–Zozaya, arXiv:2502.07427v1. The first proves only `w(w(G))` finite under the small-image hypothesis. The perfect-fusion proposition only gives a local constant region, not a global finite image. No stronger conclusion imported.

Initial observation: any infinite value set can be preserved as infinite in a countably based quotient by selecting countably many distinct values and countably many separating open normal subgroups. A small-image counterexample would therefore have a countably infinite compact metrizable word image. This reduction must be written and independently checked; by itself it does not resolve the issue.

## 2026-10-24T23:17:00Z — checkpoint 2

Discovery estimate: 5% toward a complete solution. No full solution; estimate reflects clarified exact obstruction, not completion of the central argument.

Wrote the metrizable and inverse-limit reductions in `METRIZABLE_REDUCTION_AND_OBSTRUCTION.md`. Constructed an explicit continuous first-nonzero-coordinate map on an elementary abelian profinite group with countably infinite compact image; it meets conjugacy equivariance, all-integer power compatibility, dense local constancy, and finite conjugacy-orbit conditions but is not a word map. This blocks any route using only those topological properties. Its finite image inverse system has exactly one splitting fiber at each level and linearly increasing size. The exact checker passed levels 1–15.

Froze note, checker and certificate under `FROZEN_CHECKPOINT_01.json`; root assigned a fresh independent adversary. Subsequent mathematical developments belong in separate delta notes. Exact remaining gap: extract a fixed-word algebraic mechanism excluding thin splitting, or construct a genuine word-map instance.

## 2026-10-24T23:21:39Z — checkpoint 3

Discovery estimate: 5% toward the full problem, unchanged. No complete proof. Found and wrote an explicit class-two profinite group for odd p where the p-th-power image has continuum size but every abelian subgroup has at most p power values. This disproves an abelian-source extraction shortcut, including uniformly bounded finite-stage variants. Exact checker passed p=3, stages n=1–4. Construction and proof are in `DELTA_01_ABELIAN_EXTRACTION_OBSTRUCTION.md`; this is a mechanism obstruction, not a counterexample to 21.122.

Additional routes audited without importing unsupported claims: periodic profinite groups need not be assumed to have bounded exponent (that is a separate conjecture); arbitrary central-valued word maps need not be assumed polynomial of bounded degree; Haar atomicity alone does not force finite image. These routes remain blocked absent new word-specific evidence.

## 2026-10-24T23:23:51.144813+00:00 — terminal checkpoint 4

Discovery estimate: 5% toward the complete problem. No complete proof or counterexample. Froze delta 1 for independent review and wrote `TERMINAL_SYNTHESIS.md` with the exact theorem scope, verified reductions, failed mechanisms, primary-source boundaries, and remaining gap. The topological family is blocked at genuine fixed-word exclusion of countable thin branching; this is equivalent to the central unresolved claim after the reduction, so it is not being treated as a new proof mechanism.
