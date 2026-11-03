# Residual audit: divisorial gonality and uniform subdivisions

2026-10-21. Problem 3000040, ordered row 1871. **PARTIAL / OPEN RESIDUAL.** No solution to any of the three residual questions is claimed. This is an authored mathematical attempt, not a republication of source material. No queue changes or publication were performed.

## Scope and evidence

Write a(m)=dgon(σ_m(G)), and d=dgon(Γ(G)), with every original edge replaced by m segments. The primary source is van Dobben de Bruyn, Smit and van der Wegen, *Discrete and metric divisorial gonality can be different*, JCTA 189 (2022), 105619, https://doi.org/10.1016/j.jcta.2022.105619, public PDF https://pure.mpg.de/rest/items/item_3377439/component/file_3377440/content. The local source gate and its source hashes were inspected. The source's Theorem 1.3, Lemma 4.5, Corollary 4.6, Theorem 4.8, Lemma 5.2, Proposition 5.3 and §6 are used below. The source is a dependency, not independently re-proved here.

Targeted web searches on 2026-10-21 for odd subdivisions, sharp ratio constants, σ3, and later work citing the paper yielded the original paper, the first author's thesis, and unrelated work, but no verified later solution. This limited search does not certify current openness. The surviving source targets are the sharp universal ratio, an odd-segment drop, and a graph with a(2)=a(1) but a(m)<a(1) for m>2. Stable harmonic-morphism gonality and arbitrary unequal subdivisions are not substituted for these quantities.

## Approach 1: sharpen endpoint rounding by vertex occupancy

Let D be an effective rank-one metric divisor of degree d, and suppose s of its chips, counted with multiplicity, lie on original vertices. Replacing each interior chip by one chip at each endpoint gives a graph divisor of degree 2d−s with positive rank. This is exactly the endpoint-domination argument of Proposition 5.3 with the actual occupancy retained: the endpoint pair on a unit edge is metrically equivalent to an effective divisor containing the original interior chip, and rank for vertex-supported divisors agrees in the discrete and unit-metric models. Add these dominations for all interior chips. Hence

    dgon(G) ≤ 2d−s.

Taking the maximum s over all effective degree-d positive-rank metric divisors gives a conditional route to a better universal constant. A universal s≥αd would imply c≤2−α. At present only s≥1 is guaranteed by rank one, reproducing the known bound 2d−1. In particular c≤6/5 would follow from s≥4d/5, but no such occupancy theorem is proved, and this condition is only sufficient, not necessary. Conversely any sequence with ratio tending to 2 must have d tending to infinity and maximum vertex occupancy divided by d tending to zero, by the displayed inequality. This is an elementary necessary condition, not a new extremal family.

**Outcome:** a precise missing lemma, no improved constant. Merely replacing one endpoint choice by another cannot remove the cost of interior chips without a new joint movement argument.

## Approach 2: test skewering as ratio amplification

Suppose blocks G_i have discrete gonalities a_i and metric gonalities b_i. Skewer them as in Lemma 5.2 using t≥Σa_i parallel connecting paths along a connected skeleton. Then the discrete gonality is Σa_i. For a common subdivision denominator attaining every block's metric minimum, Lemma 5.2 applies again and gives Σb_i. Every other uniform subdivision has block gonality at least b_i and at most a_i, so the same lemma and Theorem 1.3 show that the assembled metric gonality is exactly Σb_i. Connecting paths are permitted to have arbitrary subdivisions in that lemma; uniform further subdivision remains within its scope.

Consequently the assembled ratio is

    (Σa_i)/(Σb_i) = Σ [b_i/(Σb_j)] (a_i/b_i).

It cannot exceed the largest block ratio. In particular, repeating the known 6/5 tricycle blocks cannot improve 6/5, although it makes the additive gap unbounded. The common denominator exists by finite attainment and divisibility propagation of rank under regular subdivision.

**Outcome:** this natural amplification mechanism provably fails to improve the sharp-ratio lower bound. A better ratio needs a genuinely better block or a nonadditive coupling.

## Approach 3: exact odd-grid search in the smallest tricycle

The explicitly constructed multigraph has vertices 0,…,6, two parallel edges in each of (1,2),(3,4),(5,6), spokes (0,i) for i=1,…,6, and transitions (2,3),(4,5),(6,1). Uniform subdivision by m gives 7+15(m−1) vertices. By Lemma 4.5, every degree-five positive-rank class has a 0-reduced representative consisting of two chips at 0 and one chip on each closed transition path. Thus testing all (m+1)^3 such configurations is exhaustive for degree five; testing a superset of reduced configurations is harmless. Corollary 4.6 excludes smaller degree. The six transition vertices form a strong separator, giving a positive-rank degree-six divisor for every subdivision considered.

The authored integer-only Dhar implementation tests reachability of every vertex. With a chipless target q, burn q and successively any vertex with more burned incident edges than chips. If all burn, the divisor is q-reduced and cannot reach q. Otherwise fire the unburned set, an effective legal move, and repeat. Stop positively once q has a chip. The iteration cap raises an exception rather than silently treating a timeout as failure. Parallel edges are explicitly counted. No floating-point or optimization tolerance enters.

Results for m=1,…,9: gonality is 6 at odd m and 5 at even m. At even m the sole successful candidate in the enumerated class is the midpoint triple (m/2,m/2,m/2). There are 3,024 enumerated configurations in total. This is a finite computation, not a theorem for all odd m or all tricycles. Outputs and reproduction code are included locally.

**Outcome:** no odd drop, and no first drop beyond two, in this finite test. A proof that the midpoint triple is forced for every m would explain this obstruction but is not supplied.

## Approach 4: asymmetric metric lengths and first-drop search

To escape the uniform midpoint obstruction, fix each of the six outer-cycle edge lengths to one, make all six spokes length s∈{1,2}, and independently choose the three transition lengths in {1,2,3}. These give 54 labelled base graphs, with lengths realized as integral edge subdivisions, not as a change in the definition of σ_m. For each base graph evaluate its uniform m=1,2,3 subdivisions by the same exhaustive degree-five test and the same 5≤gonality≤6 certificate. There are 162 graph tests; some graphs are isomorphic, and no isomorphism reduction or claim of all small graphs is made.

The triples (a(1),a(2),a(3)) occur with counts: (5,5,5) for 42 graphs, (6,5,6) for 9 graphs, and (6,6,6) for 3 graphs. No graph had a(3)<a(1), and therefore none had a(2)=a(1)>a(3). This search is exhaustive only within the stated parameter box. It does not test m>3 for those asymmetric graphs and says nothing about other topology or larger lengths. LENGTH_CHECKS.json records every length vector and either a degree-five witness or the negative exhaustive result.

**Outcome:** the small asymmetric tricycle box also does not produce a residual counterexample. Increasing transition lengths alone is not evidence of creating a new odd-denominator rank-one class.

## Approach 5: denominator arithmetic and prime-step reduction

The basic monotonicity available is divisibility monotonicity: a(mn)≤a(m), obtained by lifting a rank-one divisor through another regular subdivision. It does not imply a(m+1)≤a(m). If the metric minimum is attained at N, then a(kN)=d for every k≥1. No odd denominator follows when N is even.

More precisely, an odd subdivision drop exists for some graph if and only if an odd-prime subdivision drop exists for some graph (not necessarily the same one). Factor an odd m giving a(m)<a(1) into odd primes. Along the chain of intermediate subdivisions at least one step strictly lowers gonality. Its starting graph H therefore satisfies dgon(σ_p(H))<dgon(H) for an odd prime p. The converse is immediate. This reduces possible witnesses to prime steps but does not bound p or preserve any desired simplicity/minimality conditions beyond regular subdivision.

The first-drop-beyond-two question remains separate: a(4)<a(2)=a(1) would answer it even if all odd subdivisions preserved gonality. The prime-step argument then yields only a double-subdivision drop of σ_2(G), which is already compatible with known behavior and does not solve the residual.

A tempting rational-density argument fails. Finite attainment gives a rational point in a rank-feasibility locus, not an odd-denominator point. Even an elementary rational polytope can impose 2x=1, excluding every odd grid. Odd-denominator rationals are dense in ambient space but not necessarily in a rational affine subspace with this congruence obstruction. This example diagnoses a proof gap, not a claim that a specific gonality locus has that equation. A valid approach needs actual control of the lattice of feasible divisors or of the affine equations defining relevant cells.

**Outcome:** a prime-step reduction and a precise obstruction to inferring odd attainment from rational attainment. No parity theorem or odd-grid counterexample is established.

## Acceptance boundary

The report does not settle the sharp constant, produce an odd drop, prove odd invariance, or produce/prohibit a first drop beyond two. Conditional inequalities and the skewering/prime-step observations are elementary consequences of the cited framework, without a novelty claim. Finite numerical exclusions must not be promoted to general statements. No independent full audit of the source's tricycle lemma is claimed. All source PDFs/text remain outside the authored deliverable directory.
