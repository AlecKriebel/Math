# Fresh independent whole-package adversarial review 01

Completed 2026-10-13 UTC. Candidate: PR #1025, catalogue 30001102 / OWR-2489-008; submitted head `7769e6872c3d2f4267706dc2400be3519186cf3d`. Reviewed ZIP SHA-256 `f1bc76ccd687029f4b9f111ad561cf0f38be945c13c191cbcf0df31b2d65649b`. This is a new AI adversarial review, not human peer review. All prior acceptance and PASS records were hypotheses. No candidate file, other effort, shared Git index, remote service or publication gate was modified.

## Verdict and required repairs

**Mathematics, stated rational scope, archive provenance and portable diagnostics pass this review. Two P3 repairs are required before immutable promotion. No P0, P1 or P2 issue was found.** The ascending publication gate remains #1024; this audit is preparatory.

1. **P3 — Correct the GLS source label.** In `publication/research_note.tex`, line 211, `Theorem~10.2.7` mislabels a named algorithmic problem. Independently retrieved GLS1988 printed p.310 / PDF p.322 labels (10.2.7) “Submodular Function Minimization” and then explains three algorithms; it does not label that item a theorem. Replace the locator with `\S10.2, problem~10.3.8 and its reduction`, or with `problem~10.2.7 and its ensuing algorithms, problem~10.3.8 and its reduction`. The rational oracle-bit guarantee itself is supported. Recompile the note, reinspect affected pages, rebuild package inventory and ZIP after the edit.
2. **P3 — Define B for the explicitly allowed empty edge set.** In the uniform encoding paragraph, `B=max(1,max_e ceil|b_e|)` leaves the inner maximum over an empty set unspecified. Define `B=max({1} union {ceil|b_e|: e in E})`, or explicitly take `B=1` when `E` is empty. The stated theorem includes empty graphs and later uses B in the compact core. The mathematics passes with the intended convention B=1; this is a boundary notation repair. Regenerate the same paper/package artifacts after the edit.

These findings concern the original pinned bytes. A repaired package requires a new hash and an independent repair recheck. No optional stylistic repair or unreported low-severity issue is being withheld.

## Exact claim tested

The system has a specified finite bipartition U,V, explicitly encoded graph, arbitrary rational demands, free signs, and any selected integer coordinates. Objective and query coordinates are rational in the total binary model. Dimension, integrality dimension, numerical magnitudes and denominators all vary. The exact claim is polynomial optimization with attained rational minimizers or an integral improving direction, and polynomial strong separation/exact membership in the **actual** mixed convex hull, including its boundary.

Success requires (a) no assumed mixed attainment; (b) no numerical-denominator enumeration; (c) a nonempty, explicitly accessible ring domain; (d) exact rational oracle outputs with a known uniform bit bound; (e) actual-hull closedness rather than silently replacing the hull by its closure; and (f) the exact unbounded strong-optimization interface of GLS. The result does not establish Conjecture 2, general added side constraints, arbitrary unencoded real queries, a compact formulation, a strongly polynomial total algorithm, or an executable polynomial LP/SFM/GLS solver.

## Independent mathematical derivations

### Sign change, feasibility and unboundedness

Let J be diagonal with +1 on U and -1 on V. Since J and its inverse have integer entries, y=Jx preserves each selected integrality constraint, while every cover row becomes y_u-y_v>=b_uv. Taking all original x_i equal to an integer M>=max(0,max_e ceil b_e) supplies a feasible point with polynomial encoding. For the empty edge set take M=0.

The relaxation is feasible. If a=Jc is unbounded below, rational LP on the recession inequalities plus a^Tr<=-1 returns a polynomial-bit rational ray. The LCM of its coordinate denominators has bit length at most their sum. Multiplying by that LCM gives an integral ray with negative slope and polynomial encoding. Starting from the integral feasible point, all nonnegative integer steps remain mixed feasible. The converse follows from T subset P. Thus relaxation and mixed boundedness agree, including isolated vertices and component translation lineality. No unanchored vertex is needed.

### All signed threshold layers, not merely coordinates

For d, split positive entries and negative magnitudes into distinct increasing levels. A positive layer is the indicator of d_i>=t; a negative layer is minus the indicator of d_i<=-t. Both are nondecreasing functions of d_i. Therefore each layer difference r_i-r_j has the same sign as d_i-d_j or vanishes. Summing reconstructs d without cancellation on any coordinate or any pair difference. In particular, 0<=lambda(r_i-r_j)<=d_i-d_j when the latter is nonnegative, with inequalities reversed for negative differences. The total number of levels is at most the number of nonzero coordinates, hence at most n.

For any mixed feasible z and d=z-y*, y*+lambda r lies rowwise between y* and z. Relaxation optimality implies a^Tr>=0. If lambda>=1, z-r also lies between those endpoints rowwise; it preserves integer coordinates and cannot increase objective. Each nonzero layer coordinate has |d_i|>=lambda>=1, so its absolute distance decreases by exactly one. This proves a strict l1 decrease, including layers with negative entries and equality lambda=1.

### Attainment is not circular; proximity is existential

For any z0, the mixed objective sublevel through z0 is closed and nonempty. Its intersection with the closed l1 ball centered at y* through z0 is compact and nonempty. A distance minimizer of this intersection is also a distance minimizer of the full sublevel: any point outside the ball is farther than z0. A removable layer contradicts that minimality. Every layer weight is therefore below one; at most n layers imply strict sup-distance below n.

This construction works separately for **every** starting sublevel, producing a no-more-expensive representative in one common compact box. Minimizing objective over the closed mixed subset of that box attains a value no larger than any point in T, hence a global minimum. Repeating the distance argument on the optimal sublevel yields at least one nearby optimum. Nothing here claims that every optimum is nearby; unrestricted translation produces arbitrarily distant optima in many cases.

### Exact projection and completion

A fixed integer assignment p must satisfy p_u-p_v>=ceil b_uv only when both endpoints are integer. Conversely undo J on the fixed coordinates and make every unfixed original coordinate a sufficiently large common integer. Each edge with one fixed endpoint can be met by enlarging that number, each edge with two unfixed endpoints is met simultaneously, and the two-fixed edges were already checked. This gives an explicit completion; there are no hidden directed-path constraints in this bipartite orientation. Rounding a demand with a continuous endpoint would incorrectly strengthen the domain.

The intervals ceil(y*_i-n) through floor(y*_i+n) have width at most 2n and at most 2n+1 labels. Proximity supplies a nonempty assignment domain. Every slice is feasible, bounded below by global boundedness, and has an attained exact LP optimum.

### Partial-value submodularity and uniform bit bound

The minimum and maximum of two feasible difference-label vectors are feasible because y_u>=y_v+b and z_u>=z_v+b imply the corresponding min/min and max/max inequalities. The same holds in the bounded integer projection. Min and max of optimal completions give feasible completions of meet and join; the linear objective is modular on these two vectors. This proves the asserted submodular inequality in the transformed coordinates. It fails for original cover variables, as (1,0) and (0,1) show for demand 1.

In a slice component without a fixed coordinate, both translation signs remain feasible recession directions, so boundedness forces the objective sum on that component to zero. Anchoring one coordinate there at zero preserves optimal value. This removes all lineality and makes the slice pointed. If a tight-edge component of an optimal vertex contained no anchor, translating just that component by a sufficiently small amount in both directions would preserve all tight rows and all positive-slack rows, contradicting extremality. A spanning forest rooted at fixed/zero anchors therefore writes every vertex coordinate as an anchor plus at most n-1 signed demands.

The anchors have magnitude at most H*, so coordinate magnitude is at most H*+nB; denominators divide demand LCM k. Multiplying by objectives whose denominators divide q gives value denominators dividing kq and magnitude at most n A0(H*+nB). A value numerator is bounded by that magnitude times kq. The logs of k and q are bounded by summed input denominator lengths; y* has a standard rational-LP polynomial encoding. Hence a known uniform rational value-bit bound, not merely a number of oracle calls, is available.

### Domain access and exact rational SFM

The threshold ground set includes only l_i<t<=h_i. Prefix implications make every chosen set a prefix in each coordinate. For each integer edge, the base condition p_u>=l_v+ceil b_uv handles the lowest value of p_v; implication from every higher v-threshold handles its entire remaining range. A target below the u range is automatic, an in-range target is an implication, and a target above the range forbids its source. An impossible base makes the family empty. These rules are equivalent to the displayed integer domain, including negative and extremely large labels.

Reachability from all forced nodes is the smallest family member, unless it reaches a forbidden node. Adding a queried node before reachability gives its smallest containing member or a nonexistence certificate. This is exactly the additional domain access needed by Schrijver §6. Removing fixed/intersection nodes, excluding nodes with no containing member and identifying equivalence classes gives a poset-ideal domain. Alternatively its intersection, union and implication relation give the GLS lattice encoding. All graph operations are polynomial in the O(n|I|) threshold nodes; the labels themselves have polynomial bit lengths.

I checked the actual rational-output convention and known beta in GLS §10.2, the three algorithms following problem (10.2.7), and §10.3's explicit lattice encoding and reduction for (10.3.8). Schrijver §6 supplies the minimum/containing-minimum reduction as well. The needed conclusion is exact rational oracle-polynomial minimization. Scaling all values by the common denominator kq is also a direct way to see that the integer/rational interface does not introduce exponentially long arithmetic. A minimizer of the localized partial-value function and its exact LP completion are globally optimal by proximity. No production SFM or ellipsoid implementation is needed for the theorem-as-algorithm-existence claim.

### Objective-independent compact core and actual closed hull

For **every** bounded real objective, lineality annihilation permits anchoring one vertex of each relaxation graph component at zero. The pointed anchored LP has an optimal vertex. The same tight-tree argument bounds its coordinates by (n-1)B. Applying the proximity argument yields a mixed optimum in [-H,H]^n for H=nB+n. The bound does not depend on the objective; the mathematical argument also applies to real separating objectives, even though the computational oracle receives rationals.

There are finitely many integer-coordinate choices in that box. The corresponding bounded rational slice polytopes give a finite rational polytope K after taking convex hull. R=rec(P) has an integral finite signed-threshold generating family: each layer of r in R also lies in R, by conformity with every nonnegative row difference.

For integral d in R and z in T, z+md is in T for all nonnegative integers m. Writing t=m+theta with 0<=theta<1 gives z+td=(1-theta)(z+md)+theta(z+(m+1)d) in conv(T). The same interpolation extends to every finite convex combination of z, and then to finite sums of threshold layers. Thus K+R lies in the **finite** convex hull; it is not merely a limit argument.

If a mixed point z lay outside the closed rational polyhedron K+R, strict separation gives a finite lower supporting value. The separating objective is nonnegative on R, hence bounded below on P. Its mixed optimum lies in K, contradicting strict separation of z. Therefore T is contained in K+R, and convexity gives conv(T)=K+R. This independently establishes closedness of the actual hull. The proof does not assume the hull closed in order to prove it.

### TU grid, facets, lineality and exact separation

Incidence difference rows, unit fixings and integer box rows are TU. Scaling bounded slice coordinates by k makes all right sides integral, so every slice vertex is in (1/k)Z^n. Homogenized point generators multiplied by k and integral rays have integer coordinates bounded by k(H+1). The hull is full-dimensional: the original cover set contains all sufficiently large integer vectors, whose convex hull contains a translated positive orthant.

A facet of the full-dimensional homogenized cone has n independent generators spanning its supporting hyperplane. Point and ray generators suffice; lineality may contribute both signs and does not invalidate the rank argument. Their n-by-n minors yield a nonzero integral normal, including the constant coordinate, bounded by n![k(H+1)]^n. The displayed generous phi bounds total coefficient encodings and is polynomial; it also handles the no-facet whole-space case. No generator enumeration is required by the algorithm.

An exact mixed minimizer is a feasible optimal point of the hull, whether or not it is a vertex. The integral improving ray lies in R=rec(conv(T)); negating the minimizing objective and scaling the ray meets GLS Definition (6.2.1)'s >=1 maximizing normalization. Together with the explicit phi, this is the unbounded well-described-polyhedron strong-optimization interface. GLS Theorem (6.4.9) then supplies exact strong separation at rational queries, from which exact membership follows, including boundary queries. An approximate-membership statement would be insufficient; the cited theorem is the exact one.

## Source scope and contribution audit

Fresh independent retrievals and body locations are in `SOURCE_RETRIEVAL.json` and `SOURCE_INSPECTIONS.json`. All third-party PDFs, extracted text and images stay inside this review's `sources/raw/`; they must not be redistributed as authored package files.

- OWR51/2008 printed pp.2904–2905 was read in text and full rendered images. Problem 1 has precisely rational demands, arbitrary selected integer coordinates, no nonnegativity constraint, and a real query with implicit encoding. The candidate's rational-query qualification is explicit and appropriate. Conjecture 2 is a separate claim.
- Cook–Gerards–Schrijver–Tardos1986 printed p.258 was visually and textually inspected. It already gives all-coordinate mixed proximity <=n Delta for integral combined matrices, assuming a mixed optimum exists. It also cautions that proximity alone does not give general mixed-hull facet bounds. The candidate grants this prior credit and supplies its own attainment and grid/hull argument.
- The full three-page THM2004 author translation was read, including Proposition 2 and the conclusion. Hybrid partial minimization is prior; the paper leaves algorithm development as future work. Murota2002 §4.1 explicitly records an earlier <=n² ground-set ring minimization lineage. The candidate accurately presents these as inherited mechanisms.
- The network2008 and covers2009 author manuscripts were read at their exact-model, size, formulation and complexity discussions. The latter explicitly uses numerical k and leaves general optimization complexity unknown at that time. The network construction depends on lists of fractionalities and gives exponential-size examples. Neither inspected body supplies the present bit guarantee. Their historical gap is a historical statement, not proof of current worldwide openness.
- The half2007 primary body has half-integral demands and nonnegative variables. Papaefthymiou1990 printed pp.53–54 and §5.4 were read from a text-bearing scan, with full pp.53–54 images inspected. Its solved objective is supported on integer vertices, while general MI-Dual-Flow hardness is a conjecture. Leiserson–Saxe1985 printed p.1 was visually inspected and asks mixed difference **feasibility**, not arbitrary-objective minimization. The supplement's distinctions hold.
- I also inspected a fresh current arXiv copy of `Convexification of classes of mixed-integer sets with L^natural-convexity` at §4, §5.1–5.4, Assumption 1 and Proposition 5.17. Its structured max/hyperrectangle/nonnegative-continuous model has additional assumptions and is not an inspected full arbitrary-bipartite solution. This supports only a bounded comparison.
- Eight fresh focused searches found no matching full prior solution. A September2026 EulerSolve primary page/PDF for OWR-2489-009 claims separate subtree counterexamples and expressly leaves membership open. I did not referee those counterexamples; local download was blocked (403), although the primary body was accessible through the browser tool. Candidate wording “unresolved here”/“unaddressed” is work-specific and remains accurate. It should not be turned into worldwide Conjecture 2 openness wording.

I counted the preserved priority ledger independently: 72 listed queries and 19 verified fetched PDFs. Those counts are accurate provenance, not proof of absence of prior work. The contribution description as an explicit assembled rational application is appropriately modest. Unindexed, unpublished, differently named and uninspected work remain possible; exhaustive priority and current openness are not certified.

## Portable kit, provenance and extra attacks

`PACKAGE_INTEGRITY.json` verifies all 155 inventoried payload files, the manifest/ZIP byte agreement, all five actual mutation hashes, equal metadata/deposit metadata, and working relative README/evidence-index links. The ZIP has 156 files including the self-excluded manifest. Local build log/render images and the separate deposit plan are intentionally outside the ZIP. No third-party source body is included in the ZIP.

`ORIGINAL_GIT_PROVENANCE.json` independently reads every blob of the locally available pinned commit. Exactly 35 files occur under the submitted attempt; all 35 match their declared hashes and the retained historical copies, and the pinned list is complete. All three portable arithmetic sources also match their preserved source copies. Historical acceptance counts, missing historical external seals and the UID1000 environment are explicitly stage evidence; the current kit does not falsely replay that harness.

The proposed runner passed the 24 cases both directly and from a clean ZIP extraction: 9 baselines and 15 actual defective-source cases across normal/-O/-OO. Whole stdout, stderr and exit codes match. The fault replacements occur once each, their computed hashes match, and the five faults yield the intended first mathematical failure. Reversing a checker inequality is a diagnostic source fault with an explicit strict witness; it is not presented as mutation of a production polynomial solver.

`guard_checks.py` gives 29 fresh positive/negative controls. It tests three execution modes, output suffixes, unexpected stderr, wrong exits, floats replacing optimization-mode integers, incorrect modes, unrelated crashes, and recursive boolean/integer/float/container/key/value confusion. Every intended negative was rejected. Full-byte comparison independently prevents ignored extra JSON fields or duplicate-output tricks. The runner is an integrity/diagnostic harness, not a security sandbox or resistance to intentionally malicious source spoofing; the documentation already says so.

`independent_fm_checks.py` is freshly written without importing proposed mathematics. It works in **original cover coordinates**, using exact Fourier–Motzkin elimination and back-substitution rather than the package's anchored vertex enumeration. Each of normal/-O/-OO checked the same 28 models, 1740 exact slice LPs, 11637 submodular pairs, 374 layer removals, 2800 signed vectors, 28 bounded-core comparisons, 155 recession interpolations, 35 hull/unbounded boundary controls, 5 explicit invalid-substitution witnesses and 38 generous facet-bound arithmetic checks. Cases include empty graphs, empty integer sets, isolated nodes, zero costs, negative demands, mixed/integer demands, disconnected models and >100-bit data. No counterexample was found. Modes repeat cases, not independent instance counts.

These finite attacks corroborate mechanisms and do not prove asymptotics or implement polynomial SFM/GLS. The universal result is supported by the written deductions and the correctly scoped classical algorithm interfaces, subject to the two minor repairs above.

## PDF and final limitations

All six PDF pages were independently rendered at 120 dpi and individually viewed. Title/author/ORCID, all formulas, section transitions, proof ending, references, page numbers and margins are readable. No clipping, overlap, missing glyph, hidden warning text, broken citation placeholder or actionable visual defect was found. Page 6 contains the remaining bibliography and ordinary white space; that is not a defect.

The mathematical claim survived this adversarial review, but this is neither a proof-assistant certificate nor human peer review. I verified the portable kit on macOS/Python3.14.6; other operating systems remain untested. The theoretical polynomial solver itself is not implemented in the package. Novelty remains a bounded-search inference. No outside individual was contacted and no outreach was prepared. Candidate bytes remain unmodified by this reviewer, and no publication or remote action was performed.
