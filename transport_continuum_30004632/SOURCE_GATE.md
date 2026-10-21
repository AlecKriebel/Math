# Source gate: row 1850 / 30004632 / OWR-4990379-002

Checked 2026-10-21. Exact source recovered; research target remains open in the inspected primary literature. No queue or GitHub writes performed. This is an authored scope audit, not a solution.

## Identity and precise target

The corpus ID and source key identify the same unique record, titled Global Optimality of Domain-Decomposition Transport Algorithms. Its source is DOI 10.4171/OWR/2021/10, Schmitzer's contribution “Domain decomposition for entropic optimal transport” (joint with Mauro Bonafini and Ismael Medina), printed pp.515–517 of Applications of Optimal Transportation in the Natural Sciences. Workshop dates: 21–27 February 2021. The corpus's bibliographic year 2022 should not be silently substituted for the workshop/report year 2021.

The source's actual open question concerns the long-time behavior of a trajectory obtained after the partition scale tends to zero. It is NOT the already-established convergence of alternating local minimization with a fixed positive entropy parameter and a fixed finite partition. The OWR contribution's final paragraph, p.517, says that the limiting trajectory need not become globally optimal and requests sufficient conditions preventing this failure. It also distinguishes concentration on a map's graph from optimality of that map.

Recovered research question: for the continuum trajectory selected by the increasingly fine domain-decomposition algorithms, identify nontrivial hypotheses on the cost, marginals, initialization, discretization, and entropy scaling that imply existence of a long-time limit and its global optimality for the transport problem. A certificate imposed directly on an already optimal limiting plan, or a proof solely at fixed scale, does not by itself answer this question.

Primary source: https://ems.press/doi/pdf/10.4171/OWR/2021/10

## Objective, algorithm, and distinctions

The OWR setup has compact convex X,Y in R^d, continuous nonnegative c, and probability marginals μ,ν. Minimize Eε(π)=∫c dπ+ε KL(π|μ⊗ν) over Π(μ,ν), with ε≥0. For ε=0 interpret this as the unregularized cost without imposing finite entropy.

In the illustrative three-cell partition X1,X2,X3, the active domains are X12=X1∪X2 and X23=X2∪X3. Start from a feasible π. Optimize its restriction to X12×Y while fixing the complement, then do the same on X23×Y, and alternate. For a general active cell J, both μ restricted to XJ and the current subplan's Y-marginal νJ are preserved. The reference in the entropy is μJ⊗ν, not a changing global marginal. Disjoint cells in a given partition can be updated in parallel; the two staggered partitions alternate. This is not an arbitrary sequence of coordinate updates or a global transport solve.

At fixed ε>0, Bonafini–Schmitzer prove global convergence for bounded costs and positive-mass basic cells with connected partition graph: join two basic cells if a composite cell in either partition contains both. Shared basic cells may be merged to obtain the graph convention in their Definition 7. The result applies to continuous and discrete measures; no Lebesgue density is required for this fixed-scale entropic result. Their Theorem 2 establishes linear suboptimality/KL convergence over a fixed number of iterations, with constants depending on cell masses, graph geometry and ε. Those constants deteriorate as ε decreases and partition resolution grows. This is background, not a later solution of the target.

For ε=0, squared Euclidean cost and absolutely continuous μ, Benamou's fixed-partition theorem uses geometric convex overlap, not merely graph connectivity. Discrete unregularized analogues can be fixed at locally optimal but globally suboptimal plans. The 2021 asymptotic arXiv v1 Appendix A gives a more general finite-cover cyclic theorem: X a compact convex polytope, bounded Y, μ with positive Lebesgue density a.e.; closed convex-polytope basic tiling; convex-polytope composite covering; each touching pair of composite cells with no interior overlap is bridged at every point of contact by a third cell with interior overlap with both. Cyclically optimize each cell. Theorem A.2 gives convergence to the unique global minimizer. This appendix is a v1 reference and must not be cited as an appendix of the shortened published 2023 paper.

Fixed-partition source: https://doi.org/10.1007/s00211-021-01245-0 ; preprint https://arxiv.org/abs/2001.10986

## Published 2023 continuum theorem: exact usable assumptions

Bonafini–Medina–Schmitzer, Asymptotic analysis of domain decomposition for optimal transport, Numerische Mathematik 153, 451–492 (2023), DOI 10.1007/s00211-023-01347-x. Published online 28 February 2023. The published PDF was downloaded and inspected separately from the older arXiv v1.

Published §2–§3 setup:
- X=[0,1]^d, Y compact in R^d; μ,ν probability measures; μ absolutely continuous with density strictly positive a.e.
- Even n; basic grid cubes have side 1/n. Composite A-cells group 2^d adjacent basic cells. B-cells use the same grouping shifted by one basic cell along every axis, with smaller boundary cells.
- μ^n preserves μ's mass on each basic cell and places no mass on cell boundaries. ν^n converges weak* to ν. Feasible initial π_init^n converges weak* to π_init.
- c∈C^1(X×Y). ε^n≥0 and η=lim nε^n∈[0,∞] exists. Unlike arXiv v1, the published setup does not introduce an approximating c^n.
- Time per iteration is 1/n; the trajectory is defined using composite-cell-normalized Y-marginal disintegrations, rather than assuming that arbitrary raw pointwise plans have already converged.
- Assumption 1: along a subsequence, these disintegrations converge in Wasserstein distance on Y for Lebesgue-a.e. time and μ-a.e. x to those of a trajectory π_t∈Π(μ,ν). This is a real extra assumption, not an automatic consequence of weak compactness.
- Assumption 2 / Definition 4: normalized, rescaled X-cell marginals on Z=[−1,1]^d converge weak* a.e. in (t,x) to a single σ∈P(Z), with σ({z:z_l=0})=0 for every l. This regular-discretization condition covers the canonical continuous and grid discretizations discussed in Lemma 1.

Published Theorem 3 (§4.5) then gives subsequential weak* convergence on compact time intervals of trajectory and horizontal momentum, with distributional equation ∂tπ_t+div_X ω_t=0 and π_0=π_init. For finite η, the limiting cell problem is

min over λ∈Π(σ,π_{t,x}) of ∫[∇_X c(x,y)·z] dλ(z,y)+η KL(λ|σ⊗π_{t,x}).

The l-th component of the momentum disintegration is the difference between Y-projections of λ restricted to z_l>0 and z_l<0. For η=∞, λ=σ⊗π_{t,x}, ω=0, and π_t=π_init. Thus fixed ε>0 actually lies in the frozen n→∞ scaling, despite fixed-n global convergence.

The published theorem is Theorem 3, NOT Theorem 5.22. The latter numbering belongs to arXiv:2106.08084v1 (June 2021). Likewise the published assumptions are 1–2, not v1's 5.1 and 5.8. The published paper explicitly leaves long-time convergence, optimality, and quantitative speed open in §1.2 and §6.

Published source: https://link.springer.com/content/pdf/10.1007/s00211-023-01347-x.pdf

## Known obstructions and later work

The 2023 paper §5.1 constructs locally optimal discrete restrictions from an indefinite quadratic potential whose negative directions are invisible within each small composite grid cell. The full map is not globally optimal. §5.2 illustrates semi-discrete freezing when almost all cells see only one target and the error is concentrated along an interface. The latter mechanism is not cured merely by imposing a smooth quadratic cost, continuous μ, or connectivity. Remark 8 also observes nonuniqueness of the limiting PDE: a nonoptimal deterministic coupling can give a stationary PDE solution. Therefore arbitrary PDE solutions cannot automatically be identified with algorithm-selected trajectories.

Medina–Schmitzer, Flow updates for domain decomposition of entropic optimal transport (arXiv:2405.09400v3, revised 27 March 2025; journal ESAIM M2AN 59 (2025), 1239–1270), changes the algorithm by inserting nonlocal flow moves. Proposition 3.14 proves weak* convergence of this hybrid to the unique fixed-ε minimizer for continuous c, ε>0, positive basic cell masses, connected partition graph, and gluing edge candidates. The continuum discussion is formal, and Remark 3.15 says the proof uses only nonincrease of the objective by the added flow step. It is not a proof of global optimality for the original continuum limit. Its experiments and the author's publication list confirm freezing remains the motivation.

https://arxiv.org/abs/2405.09400 ; https://arxiv.org/pdf/2405.09400v3 ; https://ot.cs.uni-goettingen.de/publications.html

Bounded search checked the published 2023 text, 2025 hybrid text, and current author publication listing (including 2026 unbalanced work). No primary resolution of the original question was located. This is a dated search result, not a claim of exhaustive nonexistence. Stop classification: source gate passed; original continuum-optimality question remains a valid research target, with substantial pre-existing obstructions and major finite-scale/limit-order traps.

## Public provenance and handling

Only public PDF hashes and byte counts are retained in SOURCE_METADATA.json; source PDFs, extracted text, dataset contents, and private coordination material are not part of this package. The initial download attempt lacked the optional requests module; urllib succeeded. The ESAIM endpoint returned HTTP 403; the public arXiv v3 version was inspected instead. This is a dated bounded source review, not an exhaustive literature or novelty claim.
