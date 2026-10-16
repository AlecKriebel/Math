# Independent adversarial review: proximity, optimization, and bit complexity

**Verdict: PASS for the complete rational binary-input linear-optimization theorem, conditional only on the identified established rational LP and finite submodular-minimization algorithms. No mathematical blocker or required repair found in this family.** The membership/separation hull argument and novelty judgment are separate work. This report does not infer either of them from finite tests or from the original report's informal optimization/membership equivalence.

PR #1025, problem 30001102 / OWR-2489-008. Reviewed pinned head `7769e6872c3d2f4267706dc2400be3519186cf3d`; candidate proof SHA-256 `c90d5a287718b26026cbee07f77d8710807a2c7a85f2057a1b7d00f5bb72ce32`. Read the candidate first and then independently retrieved the original question directly. Source-interface notes and PR metadata were read as claims to verify, not findings adopted. The metadata itself includes historical acceptance wording; this was not used as mathematical evidence. Did not read the separate historical `INDEPENDENT_AUDIT.md`, acceptance files, or another current review. `INPUT_PINS.json` records the authored inputs read.

## Exact target and scope

The directly inspected [Oberwolfach original](https://ems.press/content/serial-article-files/46195), printed pages 2904–2905, uses a bipartite graph, rational edge demands, selected integral coordinates, and unrestricted real variables subject to covering inequalities. Problem 1 concerns the hull's membership complexity and the text connects this to linear optimization. Conjecture 2 is a different subtree-hull assertion. The present optimization theorem addresses the explicitly encoded rational objective/input model; it makes no oracle-computation assertion for arbitrary unencoded real numbers.

I independently checked variable signs and source wording in rendered source pages. The diagonal sign change sends the original inequalities to `y_u-y_v >= b_uv` and preserves precisely the selected integer coordinates. It also sends a rational original objective to the corresponding rational signed objective. No nonnegativity restriction is introduced.

## Recession and feasibility

For any demands the original model has an integral feasible point: choose every coordinate equal to an integer `M >= max(0, max_e ceil(b_e))`. Then each left side is `2M >= b_e`. This also handles negative demands. With no edges choose `M=0`.

If the continuous difference-system LP is unbounded, solve the rational system

`r_u-r_v >= 0`, `a^T r <= -1`.

Its feasibility follows from ordinary rational-polyhedron recession theory. A polynomial-bit rational feasible solution is available by rational LP. Multiply by the least common multiple of its coordinate denominators, which has polynomial binary length, to get an integral improving direction. Beginning at the integral feasible point, every nonnegative integer step stays mixed feasible. Therefore the mixed and continuous boundedness decisions coincide. The reverse implication follows by set inclusion.

No vertex of the unanchored relaxation is needed: its component translation lineality usually rules vertices out. Rational LP still returns a polynomial-bit exact minimizer when the objective is finite. For isolated vertices any nonzero objective coefficient causes unboundedness; a zero coefficient creates harmless lineality.

## Signed layers and noncircular attainment

Here is the logical content of the proximity mechanism, derived independently.

For `d=z-y*`, decompose its positive coordinates by nested positive thresholds and its negative coordinates by nested negative thresholds. There are at most `n` distinct layers `(lambda,r)`, with `lambda>0` and `r` uniformly `0/1` or `0/-1`. For every pair of coordinates, all nonzero layer differences have the same sign as `d_i-d_j`. Thus each layer's coordinate and each row difference is bounded in magnitude by the corresponding displacement. This includes pairs of opposite signs, pairs of negative values, ties, and zero coordinates.

Consequently `y*+lambda r` is feasible: on each inequality row its value lies between the values at `y*` and `z`. Continuous optimality gives `a^T r >= 0`. If `lambda>=1`, the same row argument proves `z-r` feasible. It preserves integral coordinates, does not increase cost, and decreases the `l1` distance strictly. This is a feasible finite move, not an unsupported claim that `r` is always a global recession direction.

To obtain attainment, fix an arbitrary mixed feasible `z0` and restrict the closed objective sublevel set `a^T z <= a^T z0` to the closed `l1` ball of radius `||z0-y*||1`. The intersection is nonempty and compact. Its distance minimizer has no layer with coefficient at least one, since removal would stay in the same sublevel set and decrease distance. Hence its sup-norm distance is less than `n`. Every mixed point therefore has a no-more-expensive representative in the same compact box about `y*`. Minimizing on the closed mixed subset of that box attains the global mixed minimum.

This uses both mixed feasibility and finite continuous optimum; neither is a conclusion assumed inside its proof. The candidate's ancillary general difference-system lemma explicitly includes these hypotheses. Without mixed feasibility, opposing inequalities can force a half-integer difference between two integral coordinates; that example is outside the original bipartite covering model.

## Integer projection and partial LP values

The interval width for integer coordinate `i` is at most `2n`, because its endpoints are `ceil(y*_i-n)` and `floor(y*_i+n)`. Their magnitudes and denominators do not increase the number of labels. A nearby global optimum exists; it is not necessary that every optimum lie there.

Necessity of the integer–integer edge constraints `p_u-p_v >= ceil(b_uv)` is immediate. Their sufficiency is special to this target: convert fixed signed values to original fixed coordinates and choose all remaining original coordinates sufficiently large. Constraints with a continuous endpoint are then satisfied simultaneously. A computable integral choice is at least zero, every relevant demand, and every demand minus its incident fixed original value. Its bit length is polynomial. This projection would not be valid for a general arbitrarily oriented difference system with additional bounds.

Every resulting partial LP slice is nonempty. Its objective is bounded below by the continuous optimum, so it is finite and attained despite possible zero-cost recession or lineality. Exact rational LP supplies both its rational value and a polynomial-bit completion. The coordinatewise minimum/maximum closure belongs to signed difference variables; it is false in the original covering variables. The meet/join completions are feasible, and the objective is modular, which proves the claimed submodular inequality without exchanging an unattained infimum with a minimum.

## Domain interface and arithmetic

I checked the threshold domain's base condition, prefix implications, forced/forbidden thresholds, and out-of-range targets. The base condition is necessary when `p_v=l_v` and no source threshold is present. Integer–integer rounding is upward; constraints involving continuous variables are not rounded. Prefixes decode a unique assignment. The domain is nonempty by proximity, and implication closure gives the smallest feasible member and smallest feasible member containing each possible ground element. The number of ground elements is at most `2n|I|`; arithmetic on labels does not enumerate a large denominator or a numerically large interval.

The directly inspected [Schrijver manuscript](https://homepages.cwi.nl/~lex/files/minsubm6.pdf), Section 6, needs exactly these minimum-member data, including nonexistence for elements absent from all family members. It explicitly handles a union/intersection closed family rather than treating an unknown finite-valued domain as free information. Its reduction removes fixed and impossible elements and identifies equal minimum-containing sets; reachability supplies the candidate's corresponding data. This source is an imported minimization algorithm, not implemented by the finite scripts.

For an explicit uniform bit bound, the following additional derivation is useful. Let

`B=max(1,max_e ceil(|b_e|))`, `A=max(1,max_i ceil(|a_i|))`,

`H*=ceil(max_i |y*_i|)+n`, `k=lcm(denominators of b)`,

`q=lcm(denominators of a)`, `Q=kq`, `M=nA(H*+nB)`.

Each chosen integer assignment has magnitude at most `H*`. In each component having no fixed integer coordinate, anchor one coordinate to zero. The objective annihilates that component's translation direction, so this preserves the optimum. Components with fixed coordinates already have translation removed. The remaining slice is pointed. An optimal vertex exists and its tight-edge components each connect to a fixed or zero anchor. Along a tight spanning forest every coordinate is a sum of at most `n-1` signed demands plus its anchor. Therefore it has magnitude at most `H*+nB` and denominator dividing `k`.

It follows that every exact oracle value has denominator dividing `Q` and absolute value at most `M`. All of `log k`, `log q`, `log M`, and the encoding of `H*` are polynomial in the total input size and the polynomial-bit relaxation output. This bound holds uniformly over the whole finite domain, rather than only the assignments queried in a diagnostic run.

A count of arithmetic operations alone would not suffice to prove bit complexity. The candidate invokes an established strongly polynomial minimization algorithm, which includes controlled encodings in the standard rational model. There is also a direct checked route using an already cited source: [GLS 1988](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf), Section 10.2 and problem 10.3.8, provides oracle-polynomial rational minimization with a known output-length bound. The preceding `Q,M` supply that bound. Its rational LP theorem 6.4.12 supplies the slice solver. Thus the polynomial-bit optimization conclusion does not depend on inferring bit control from operation count alone. See the inspected page/version pins in `SOURCE_INSPECTION_MANIFEST.json`.

These established dependencies do not transfer the problem to an equally unsupported conjecture. None requires a fixed number of integer coordinates, small numerical denominators, an enumerated domain, or a compact extended formulation. No strongly polynomial complexity is asserted for the complete LP-based procedure.

## Finite attacks and their limits

The newly authored `independent_exact_check.py` imports no candidate module, performs no network operation or file write, and uses explicit exception guards. Its normal, `-O`, and `-OO` runs produce identical complete output. Per run it checks:

- 7,380 vectors, 21,600 signed layers, 84,368 coordinate checks and 331,696 difference checks;
- 45 models, including empty/disconnected graphs, isolated vertices, small arbitrary integer-coordinate selections, and large binary numerators/denominators;
- 2,095 exact tiny slice LPs and 199,661 submodular pairs;
- 2,474 actual removable-layer checks, 1,497 finite nearest-sublevel representatives, 4,624 coordinate denominator checks and 2,994 uniform value checks;
- 21 empty/isolated/zero-dimensional boundary checks, four large-number checks, and four explicit rejection examples for unsupported substitutions.

The checker deliberately enumerates tiny LP vertices and integer assignments. Its running time is not offered as evidence for the universal complexity bound. Its finite nearest-completion test does not replace the compactness proof. The 180-bit demand-numerator and 127-bit denominator cases test arithmetic and fixed label counts, not all large inputs.

Five deliberate source faults are tested in all three modes: omitting negative layers, using strict thresholds, reversing the LP sign, removing a layer smaller than one, and reversing submodularity. All fail for a specific mathematical guard. `SOURCE_MUTATIONS_TRIAL.json` preserves initial reviewer mispredictions of the earliest guard for two faults; six targeted reruns check the corrected exact expectations. No repetitions are counted as new mathematical coverage.

I inspected the candidate's original diagnostic checker but did not import or run it. Historical replay environments, old permission controls, and acceptance seals were not recreated or used as mathematical evidence.

## Repairs, publication wording, and residual scope

No required mathematical repair in this review family. Two useful wording improvements for a new paper are (1) state that **at least one** optimum lies in the proximity box and (2) make controlled bit arithmetic explicit, for example by the uniform `Q,M` argument and direct GLS lattice-family dependency above. They strengthen presentation of valid claims, rather than supply a missing central lemma.

The strongest result independently verified here is: for every explicit finite bipartite free-sign covering system with arbitrary rational binary demands and arbitrary selected integer coordinates, exact rational linear optimization either returns an attained optimum or detects mixed unboundedness with a polynomial-bit integral improving direction, in polynomial total binary-input time using established exact LP and finite submodular-minimization algorithms.

This is a mathematical audit, not a novelty certificate, formal proof-assistant certificate, implementation of the optimizer, or peer review by a human. The separately submitted hull/facet/separation argument must receive its own review before promoting the full membership claim. No source or service was modified and no individual was contacted.
