# Independent source and Turn 1-2 LP/incidence audit of PR383

**PASS within the assigned scopes. No mandatory source or Turn 1-2 mathematical repair found. The original target remains unsolved, 5/5 author turns. No merge-readiness, novelty-paper, release or DOI recommendation.**

Reviewed frozen head `967e8e489aa4599f712d5ddcde62e591827f7e38`. All 49 files, comprising 48 target files and the queue file, were independently matched to frozen Git objects, recorded byte lengths and SHA-256 values. No Git/index, queue, PR or external service mutation was performed. All new files are confined to this reviewer folder. The earlier PR385 and PR384 dispositions must be completed before advancing the descending audit; this family review does not dispose them.

## Independence and chronology

Primary-source reconstruction was recorded at 2026-10-03T02:23:07Z before candidate proof or historical review reading. The exact OWR contribution and published EJC article were independently downloaded. Candidate Turn 1-2 proofs and all five author checkers plus packet/publication verifiers were then read. New controls used no candidate imports. Historical `review/REVIEW.md` and `review/independent_check.py` were first opened only after the independent controls had finished, at 02:30:16Z. No historical reviewer code was executed. No root verdict or other family conclusion was used to derive this verdict.

## Source contract

The independent reconstruction in `SOURCE_RECONSTRUCTION.md` agrees with candidate `SOURCE_SCOPE.md`: real x,y in (0,1]; finite nonempty parts; only A-to-B and B-to-C lower degree conditions; distinct reached A vertices; and a universal guarantee, equivalently the infimum of the maximum reach over all admissible graphs. The original two-edge-path formulation may be normalized to stable parts with only A-B and B-C edges, as in the published paper. Removing extra edges preserves the degree assumptions and cannot create additional paths.

The original is Seymour's “Concatenating bipartite graphs,” joint with Chudnovsky, Scott and Spirkl, OWR 1/2019 printed pp.46-47, physical PDF pages 42-43. Both complete printed pages were visually checked. Official EMS metadata confirms report volume 16 (2019), DOI 10.4171/OWR/2019/1, and publication February 27, 2020. The published joint paper adds Hompe: EJC 29(2) (2022), P2.47, DOI 10.37236/8451, published June 3, 2022.

The exact target retains

    every integer k>=1: x+ky>1 and kx+y>=1 => phi(x,y)>=1/k.

The first inequality is strict; the second is weak. The diagonal x>1/3 question follows at k=2. Published 4.2 proves this for the four-condition biconstrained psi; published Conjecture 5.1 asks it for phi. They are distinct. The source's finite LP/weighted machinery (2.1-2.3), elementary k=1 case (5.2), partial one-third bound (5.3), and parameter-dependent half bound (6.6) are properly credited. The latter's diagonal threshold approximately 0.352202 does not reach every x>1/3. Published pages 19, 21 and 33 were visually checked to confirm the exact inequality symbols and attribution.

The separate Hompe arXiv1908.07453 v3 explicitly records withdrawal by incorporation into arXiv1902.10878. The joint preprint v3 dated December 7, 2020 and the published 2022 article are distinct source versions; the withdrawn separate paper is not an active later resolution. The current check is bounded: primary metadata, arXiv records, primary author lists and title/conjecture searches. No exhaustive open-status or historical novelty certification is inferred. The neighboring psi-symmetry PR364 remains background; its separate proof was not re-audited by this family.

## Turn 1: finite LP and complete-uniform templates

At lines 5-27, aggregating identical A neighborhoods loses no information about degrees or distinct reach. The finite matrix has one column per beta-heavy set S and one row per C vertex, with payoff 1[S intersects T_c]. Its primal minimizes the maximum row payoff over an A probability distribution; its dual maximizes the minimum column payoff over a C probability distribution. Nonnegative row multipliers sum to one. This is standard finite LP duality, and the displayed primal and dual correctly place the maximum outside the A average. The dual distribution q is a certificate; gamma enforces B-to-C admissibility and does not average the maximum. Rational probability data have finite clone realizations. There is no optimization or minimax exchange over all templates.

At lines 31-41, if an A vertex chooses at least ceil(x binomial(n,r)) middle r-sets, its union has size at least h because a j-element set contains only binomial(j,r) such sets. Double counting the A-C reach pairs yields maximum reach at least h/n. All h-subsets as A, adjacent to their contained r-subsets, attain this value in an ordinary finite graph. This works for every real x in the domain and includes r=n, h=n and x=1. No irrational limiting argument is needed.

At lines 45-67, the all-k family obstruction is valid. When k=1 and h<n, x+y<=1. For k>=2 and r>=2, each factor (h-i)/(n-i)<=h/n; hence x<1/k^2 and y<1/k, giving kx+y<2/k<=1 even at k=2. When r=1, integer kh<n gives n>=kh+1, while h+k<=kh+1, so x+ky<=1. These arguments retain the distinct strict and weak source boundaries. They exclude every first part over the fixed template, not merely the attaining construction. They do not identify this fixed-template optimum with unrestricted phi.

At lines 71-86, the 396-vertex ordinary graph has parts 55,330,11, degrees 126>=120 and 4, and reach 45/55=9/11. For every pair c,d, the A vertex [11] minus {c,d} reaches neither; the avoiding middle mass is 126/330=21/55>4/11. Thus the proposed two-C-vertex cover mechanism fails at a strict diagonal point. It supplies no counterexample to half reach. Repeated C selections cannot fix the cover.

## Turn 2: weighted rank-two incidence

The restriction is at most two **positive-weight A types** per middle vertex, with separate positive probability weights on A,B,C. It is not a bound on the total A weight of a middle neighborhood. It is also not a reduction theorem for arbitrary incidence. Zero-weight types may be deleted; duplicate middle types and empty A neighborhoods cause no omission.

Under below-half reach, every occurring middle type has A weight below half, since it has a positive-weight C neighbor. Each A type has weight below half, and n>=3. Counting using beta without alpha gives nx<=2; it does not assume equal A weights. The independence inequality and the incompatible-union certificate ty<=1 use exactly the two forward degree conditions.

For n=3, only singleton/empty types are possible, so x<=1/3. For n=4, two disjoint occurring edges would have total A weight one while each weighs below half. The star-or-triangle classification is complete. A star has an independent set of three. A triangle's fourth vertex must occur as a singleton; the three edges plus that singleton are pairwise incompatible. The charges 1/2,1/2,1/2,1 have total 5/2 and load at most one on every possible occurring type, proving x<=2/5 and y<=1/4 in the non-star case.

The five-vertex lemma at lines 59-69 is checkable. Its dual extreme points are half integral because each fractional tight component either has a two-sided bipartite perturbation or an odd cycle forcing one-half coordinates. A feasible one-half vector and primal cost strictly below three force optimal cost 5/2. Equality of total incident mass forces a fractional perfect matching with no singleton mass. An extreme matching has independent support incidence columns; a leaf component is one unit edge, while every remaining component has minimum degree two and at most as many edges as vertices, so it is an odd cycle. On five vertices the possibilities are exactly C5 or triangle plus disjoint edge. Introducing all singleton columns in that minimization is legitimate: the supplied occurring-type cover remains feasible in the larger covering LP, and the resulting fractional matching uses edges of the original graph.

At lines 73-79, dividing beta by x supplies the needed cost <3 when x>1/3. Complementary occurring edges or singletons show the required unions exceed half. The triangle-plus-edge certificate gives 4y<=1; C5 gives 5y<=1. The proof establishes exactly below-half => x<=2/5, and, if x>1/3, y<=1/4. No reverse degrees have entered. The endpoint graphs meet those weak upper barriers and fail a required source inequality, as stated. The |A|<=6 ordinary corollary correctly uses integer reach to force each middle neighborhood to have cardinality at most two. Later stronger size claims belong to the other review family.

## New controls and replays

`new_controls.py` uses standard-library exact Fraction arithmetic and Gaussian elimination to enumerate finite LP vertices; it imports no candidate module. `NEW_CONTROLS.json` preserves every primal, dual and example rather than just a PASS count.

- 219 unequal-weight finite-template instances: all 49 two-middle, three-last nonempty-row templates at three rational x values, plus 24 seeded three-middle templates with beta=(1,2,4)/7 at three x values. Primal/dual equality, feasibility and complementary slackness are exact. Every optimal rational A distribution was expanded into an actual ordinary finite incidence graph and every distinct reach was counted.
- 330 complete-uniform cases through n=9 use below/at/above binomial jumps, actual attaining graphs, x=1, r=1 and k=1. For n<=5 all admissible A neighborhood families are explicitly checked against h. Integer-k implications use both the maximum y and half that y, keeping strict/weak boundaries separate. These are finite controls, not the universal proof.
- Seven exact five-vertex covering primal/dual certificates include empty, single-edge, star, C5, triangle-plus-edge, P5 and complete supports. P5 has cost exactly three and neither required witness, showing why weakening the lemma's strict <3 assumption is invalid.
- Three nonuniform weighted rank-two models were expanded to ordinary graphs with parts (20,5,4), (15,5,4), (15,5,5). Their maximum reaches are 9/20, 7/15 and 7/15. The first two have x=2/5,y=1/4; the cycle has x=2/5,y=1/5. Every incompatible union and every finite degree/reach was checked. The clone graphs need not have ordinary cardinality rank two: the theorem's rank refers to positive-weight types before cloning.

`private_replay.py` copied all 49 files into this output-local private B directory, checked both independently downloaded PDFs against `SOURCE_MANIFEST.json`, and ran the inspected author packet verifier and all five inspected author checkers. Each checker's complete stdout is byte-identical to its frozen CHECKS JSON. The packet reports 27 historical bindings, 67 total bindings, two source PDFs and 12,967,236 author assertions. Full 49-file byte identity was rechecked after replay, including the queue and all historical review files. No reviewer code was executed, and replay validity does not substitute for proof review of Turns 3-5.

## Disposition and exact gap

Strongest independently verified assigned results are the complete-uniform fixed-template optimum and full integer-k implication within that entire family; the precise obstruction to the two-vertex cover shortcut; and the arbitrary-positive-weight rank-two half-reach theorem. No mandatory repairs arose in source attribution, hypotheses, duality, blowup, attainment, parameter bounds or endpoint handling.

The exact unresolved gap remains arbitrary overlapping higher-rank middle neighborhoods, especially without a bound on the number of A types. No support reduction or general template reduction is proved. A universal source conclusion, original counterexample, exhaustive novelty claim, sixth substantive author turn, novelty paper or immutable DOI snapshot is not supported by this audit.

`OUTPUT_MANIFEST.json` binds all reviewer artifacts except itself and its verification receipt; `OUTPUT_MANIFEST_VERIFY.json` records a byte/hash verification and binds the manifest by SHA-256. Raw sources, render intermediates and private B are audit-local evidence and are not proposed public paper assets.
