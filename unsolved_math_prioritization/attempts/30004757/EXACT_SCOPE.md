# Exact source target: 30004757

## Source and scope gate

The primary source is Connor Mooney's contribution, “Singular structures in exterior solutions to the Monge–Ampère equation,” OWR 35/2021, printed pp. 1884–1886. Problem 4 is on p. 1886. Its setting is **real**, not complex, Monge–Ampère geometry. The entire finite convex potential is defined on R^n and satisfies

    M_u = Lebesgue measure + sum_i a_i delta_{p_i},   a_i > 0,

in the Alexandrov sense. M_u(E) = |∂u(E)|. The examples in the original cited paper have n = 3 or 4. Their singular graph can be the one-skeleton of a compact convex polytope, including a degenerate segment, or a finite star such as a Y. The solutions are smooth away from that graph, and affine along its edges. In the polytope normalization, u is zero on the one-skeleton. Positive atomic weights are outputs of the construction, not independently prescribed inputs of that existence theorem.

Mooney's Remark 1.6 gives the normalization at infinity:

    u(x) = c + |x|^2/2 + O(|x|^(2-n)).

Affine transformations alter this normalization and cannot be used to claim nonuniqueness for a fixed normalized global problem.

The question asks for a precise description of the graph tangent cones at the atomic vertices, with the preceding paragraph emphasizing the resulting asymptotics of D²u. The later Mooney–Rakshit Section 5(2) makes the intended regularity issue explicit. Ordinary convex blow-up existence and the support-function formula are therefore preliminaries, not full resolution. The source suggests the axisymmetric two-mass problem as a starting case. Neither source supplies a single universal cone shape to disprove.

## Dataset discrepancies and related records

The pinned record's `original_statement` bundles nonpolyhedral obstacles into this item. The primary PDF places those in a separate Problem 5, already represented by ID 30004758. The clean statement of 30004757 matches Problem 4 only. We preserve that distinction rather than treating Problem 5 as silently solved or silently included.

ID 30004756 collects the preceding higher-dimensional, stability, and moduli questions. Mooney–Rakshit establishes the higher-dimensional construction and stability results, but its Section 5 still asks the tangent-cone regularity question. These theorems are credited, not counted as this campaign's discoveries.

## Primary-source hypothesis checks

- Mooney, J. Geom. Anal. 31 (2021), 9509–9526; arXiv:2004.06696. Theorem 1.1, Proposition 3.6, Lemma 4.2, Remark 4.6, and Theorem 5.1 supply the original examples and dual contact geometry.
- Mooney–Rakshit, Math. Eng. 5 (2023), article 083; arXiv:2204.11365. Theorems 1.1–1.3 extend constructions and prove stability. Section 5(2) still asks whether the axisymmetric two-mass cone is smooth away from its inward ray.
- Huang–Tang–Wang, Duke Math. J. 173 (2024), 2259–2313; arXiv:2111.10575. Theorems 1.1–1.2 require positive boundary data for a single-plane obstacle, equivalently strict convexity of the dual potential. A mass incident to an affine singular edge does not satisfy that strict-convexity hypothesis. Restricting to a small neighborhood does not remove the edge.
- Jin–Tu–Xiong, arXiv:2504.21253 (2025). Its global classification is for one-plane obstacles, not a polyhedral obstacle. Local regularity applies to exposed points in the interior of the PDE domain. A contact point on a crease is on the boundary of a single affine chamber; the theorem cannot simply be applied across that crease.
- A 2026 Jin–Tu–Xiong paper on sharp global Alexandrov estimates gives sufficient strict-convexity conditions. It does not classify the tangent cones in the singular graph regime. This limited search is not a certification of the global literature or novelty.

URLs and retrieved PDF checksums are in `source_manifest.json`. The source pages 1885–1886 were checked visually. No source executable was downloaded or run.
