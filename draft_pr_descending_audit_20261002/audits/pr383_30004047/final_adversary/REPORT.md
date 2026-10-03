# Final adversarial whole-package audit of PR383

**Result: the written restricted theorems withstand this audit. Required mathematical or package repairs at the repaired head: `[]`. The original remains unsolved, five of five author turns.**

Exact reviewed head: `5f576c1b527f88730c7ee15fd204536069753f9a`. This report makes no merge or readiness disposition. It supplies an independent mathematical and integrity assessment to the root reviewer. No new paper, release, DOI, historical novelty conclusion, or sixth author search is produced.

## Independence and source access

The first substantive reads were primary sources, with candidate proof text and candidate executable code still unopened. `INDEPENDENCE.md` records four materially distinct falsification designs. Their code, full stdout and full rational certificates were sealed in `INDEPENDENT_SEAL.json` at **2026-10-03T03:20:56.379323+00:00**, before candidate proofs, root reconstruction, three family verdicts or the historical reviewer were read. The task message supplied the head, expected broad mechanisms and replay totals; those supplied facts were treated as assignments, not independently obtained evidence. All later comparisons and post-inspection controls are distinguished from that initial seal.

I obtained raw PDFs directly from both original publishers. [EMS46780](https://ems.press/content/serial-article-files/46780), printed46–47, supplies the question; [EMS metadata](https://ems.press/journals/owr/articles/16763) distinguishes the January2019 workshop from publication27February2020. The [published EJC article](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v29i2p47), 29(2), P2.47, was published3June2022. Its [published PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/) p21 states Conjecture5.1. I read relevant definitions and proofs in Sections2,4,5 and6.6, including the weighted/LP machinery, elementary case, small-cover argument and credited half-reach bound. The raw PDFs exactly match both SOURCE_MANIFEST entries by length and SHA256. This is fresh source access, not certification inferred from a source-free public replay.

The [joint preprint record](https://arxiv.org/abs/1902.10878) identifies v3 as7December2020. The [separate Hompe record](https://arxiv.org/abs/1908.07453) identifies the23June2022 withdrawal and incorporation into the joint paper. These metadata checks occurred after the initial seal; the published PDF controls theorem numbering. None of these checks certifies an exhaustive current literature search or originality. The candidate's broader historical prior-search narrative was read as historical context and was not independently re-certified here.

The exact target is: all finite nonempty tripartitions, all real x,y in(0,1], and all integer k>=1, with only A-to-B minimum degree x|B| and B-to-C minimum degree y|C|, satisfy the conclusion of at least |A|/k **distinct** A predecessors at some C vertex whenever

    x+ky>1,     kx+y>=1.

The first inequality is strict and the second weak. The diagonal x=y>1/(k+1) is a subregion. The biconstrained psi theorem adds two reverse degrees and cannot supply a mono-constrained phi proof. Retaining only the two relevant edge layers makes distinct two-step reach unambiguous.

## Turn1: optimization, blow-up and exact template values

The aggregation of identical A neighborhoods preserves each required degree and each C payoff. For fixed B weights and fixed C neighborhoods, F_x is finite and nonempty, since B itself is heavy. Its 0/1 payoff matrix has rows C and columns F_x. Minimizing z with each row payoff<=z over the A simplex yields the stated dual: a C probability distribution q maximizing the minimum column payoff. Nonnegative row multipliers must sum to one. Gamma determines whether the B-to-C template is admissible; it does not weight the maximum over C. Bounding z between0 and1 gives compact feasible polytopes, and finite LP duality is a legitimate standard input. No optimization over arbitrary templates is interchanged with this finite minimax.

Rational optimal distributions have ordinary finite clone realizations. With separate common denominators for the parts, complete edges between clones preserve normalized first degrees, second degrees and distinct reach. Rank measured in positive-weight types need not remain ordinary cardinality rank after cloning. The text correctly limits its fixed-template rational blow-up claim and uses a direct ordinary attainment construction for every real x in the complete-uniform family.

For B all r-subsets of[n] and C membership, an A neighborhood with union j has at most binomial(j,r) middle members. Thus the minimum possible union has the stated h, including exact binomial jumps, r=1, r=n, h=n and x=1. Averaging gives maximum reach>=h/n; A consisting of all h-subsets attains exactly h/n. This does not equate the fixed-template value with unrestricted phi.

If h/n<1/k, the entire-template exclusion is correct. For k=1, h<=n-1 gives x<=1-r/n and x+y<=1. For k>=2,r>=2, every binomial factor is at most h/n, so x<1/k² and y<=r/n<=h/n<1/k; hence kx+y<2/k<=1, contradicting the weak second hypothesis. For r=1, integer kh<n implies h+k<=kh+1<=n and x+ky<=1. All strictness is preserved.

The explicit55+330+11 graph has A degree126, B degree4 and every C reach45. At x=y=4/11 the source wedge is strictly satisfied, while every C pair misses the unique A nine-set omitting that pair. The heavy complement has weight126/330>4/11. This refutes the integral two-C-cover mechanism, not the source conclusion; the actual reach9/11 is above half.

## Turn2: arbitrary positive weights, rank at most two

Below-half reach and y>0 force every occurring middle A-neighborhood to have alpha mass<1/2. Every A type has positive first degree, so its singleton mass is also<1/2. Counting incidence using beta, independently of alpha, gives nx<=2. For an independent set I in the pair-support graph, each middle type meets I at most once, so |I|x<=1. Types whose union weighs>=1/2 have disjoint C neighborhoods, yielding ty<=1 for t pairwise incompatible representatives. Empty middle types and duplicate types cause no omission.

For n=3, an allowed pair would be the complement of a singleton of mass<1/2 and therefore weigh>1/2; only singleton/empty types remain. For n=4, two disjoint allowed pairs would have combined mass1 while each is strictly below half, an impossibility. The pair graph with no two disjoint edges is a star or triangle with an isolated fourth vertex. The star has an independent triple. In the triangle case the fourth vertex must occur as a singleton. The three edge types plus that singleton are pairwise incompatible, giving y<=1/4. Charges1/2 on the triangle and1 on the fourth have total5/2 and load<=1 on every occurring type, giving x<=2/5.

The five-vertex cover lemma is valid. The finite cover LP may allow all singleton columns: the actual occurring-type cover remains feasible, so this enlargement does not invalidate its cost<3 premise. Its dual has u_i in[0,1] and u_i+u_j<=1 for support edges. A fractional tight component that is bipartite admits a two-sided alternating perturbation; slack inequalities allow a sufficiently small perturbation. Tight edges to integral coordinates cannot meet a fractional coordinate. Every fractional extreme component therefore has an odd cycle and all its coordinates equal1/2. Compactness yields a maximizing half-integral extreme point. The feasible all-half vector and the strict primal cost<3 force optimum5/2.

At cover cost5/2, summing the five vertex constraints forces zero singleton weight and exactly unit incident edge weight at every vertex. At an extreme fractional perfect matching, a positive-support leaf forces its incident edge to be a unit isolated edge. Every other component has minimum degree2 and linearly independent incidence columns, hence edge count at most vertex count and therefore is a cycle. An even cycle admits an alternating perturbation, so these cycles are odd. On five vertices the only possibilities are C5 or triangle plus disjoint edge. This derives, rather than assumes, the structural witness.

Dividing beta by x gives cover cost<=1/x<3 when x>1/3. Complements of occurring edges or light singletons make the witness unions strictly heavier than half. Triangle-plus-edge supplies four incompatible types and C5 five. For n>=6, nx<=2 already gives x<=1/3. Together these cases establish exactly below-half =>x<=2/5 and, if x>1/3, y<=1/4. Both sufficient conditions and their stated endpoints follow. The fourteen-vertex endpoint example has x=2/5,y=1/4 but x+2y=9/10, so it is not a source counterexample.

The ordinary |A|<=6 corollary validly converts integer below-half reach into middle cardinality<=2. This argument is not available for arbitrary A weights; support cardinality and reached mass are different quantities.

## Turns3–4: charges, the bounded uniform-A theorem and the exceptional case

For n equal A weights, strict below-n/k reach permits exactly r=ceil(n/k)-1=floor((n-1)/k) vertices, including n divisible by k. Every middle neighborhood is contained in some reached set because y>0. An occurring r-type T forces all its C neighbors into the exact-reach class C_T, of gamma mass>=y. Different such classes are disjoint. Here t counts occurring types of cardinality r, not all inclusion-maximal types of smaller sizes.

If k distinct r-types existed, any middle type contained in none would have available C mass<=1-ky<y. Hence all middle types would lie in their containment union. Positive A degree would force n<=kr, contradicting kr<=n-1. This proves t<=k-1. The r=0 case contradicts nonempty first incidence and r=1 contradicts coverage by too few singleton types; no division by r-1 is used in those cases.

Charge1/r on U, the union of r-types, and1/(r-1) elsewhere gives every r-type load1 and every smaller type load<=1. Therefore

    x <= r(r-1)/(rn-|U|) <= (r-1)/(n-t) <= (r-1)/(n-k+1).

All denominators are positive and |U|<=rt gives the displayed inequality directions. Overlap strengthens the first bound. For n<=4k, r<=3; the r2 bound is <=1/(k+2), and the r3 bound <=1/(k+1), both incompatible with strict x>1/(k+1). For4k+2<=n<=5k, r=4 and the bound3/(n-k+1)<=1/(k+1) gives the same contradiction.

The only missing size is n=4k+1. A bound t<=k-2 would already contradict x>1/(k+1), so exactly k-1 four-types occur. Their disjoint C classes leave residual C mass<=1-(k-1)y<2y. Any two residual middle vertices, each with C degree>=y, must share a C neighbor; their A unions have cardinality<=4. No reverse degree is being inserted.

Residual triples therefore intersect pairwise in at least two points. Two distinct triples have a common pair; a third omitting that pair forces all triples into their four-point union. This covers empty and singleton families too. The no-triple and pair-star charges are feasible for contained types, all pairs and singletons, not just triples, and their totals are at least k+1.

In the four-set alternative without a common pair there are at least three triples. The base charge1/4 on U,1/3 on D minus U and1/2 elsewhere has total n/2-|U|/4-|D minus U|/6. The totals stated for |U|<=4k-5 or D meeting maximal-size U are correct. The only exception has |U|=4k-4, D disjoint from U and one remaining w. No contained type or residual triple contains w. An occurring pair{w,v} must have v in every triple, so v lies in their intersection I. If I is a singleton, the charges w:1,I:0,other D:1/2,U:1/4 cover every possible type and total k+3/2. If I is empty, w cannot occur in a pair; charges w:1,D:1/3,U:1/4 total k+4/3. Nonnegative zero charge is valid even though graph weights are positive. The exceptional case is complete.

This proves the written |A|<=5k theorem for equal A weights and strict x,y>1/(k+1), all k>=2, with arbitrary positive B,C weights. For an ordinary diagonal half-reach counterexample, at least eleven A vertices are necessary. Eleven is not an upper bound on possible counterexample size, nor a universal support bound or a weighted-mass result.

The separate nine-vertex first-incidence relaxation really attains its charge3/8. It cannot be completed at y>1/3: the exact T class has mass>=y, every outside C vertex can cover at most four of the ten D triples, and summing their requirements yields10y<=4(1-y), so y<=2/7. It is a sharp isolated relaxation, not a tripartite counterexample.

## Turn5: the full asymmetric structural class and local obstruction

Pairwise-disjoint maximal nonempty A-neighborhoods cover A and partition it into blocks M_i. Each nonempty middle type belongs to exactly one block; empty middle mass remains unassigned. Each block's assigned beta mass is at least x, yielding mx<=1. Below-1/k reach makes each occurring maximal block strictly lighter than1/k, so m>=k+1. Every A type has a middle neighbor with C mass>=y, and averaging distinct reach yields y<1/k. This averaging respects arbitrary positive alpha and gamma.

For m>=k+2,

    kx+y < k/m+1/k <= k/(k+2)+1/k <=1,

where the final endpoint is equality at k=2 but the preceding inequality remains strict. This contradicts the weak source condition. Thus m=k+1. Any two full blocks weigh>1/k because the other k-1 blocks each weigh<1/k. The C neighborhoods of maximal representatives are pairwise disjoint, giving(k+1)y<=1; combining with(k+1)x<=1 contradicts the strict source condition. C vertices may reach partial pieces of multiple blocks, so the proof does not assume whole-block reach. Laminar incidence has disjoint maximal blocks. The k1 case separately uses the standard averaging/intersection argument with x+y>1.

The deletion theorem is correctly conditional. Deleting actual exceptional beta mass epsilon<x leaves positive middle mass and first degree at least x'=(x-epsilon)/(1-epsilon). Remaining B-to-C degree y is unchanged. For k>=2 and y>0 both ky and k+y-1 are positive. Exact cross multiplication gives

    x'+ky>1  iff  epsilon<(x+ky-1)/(ky),
    kx'+y>=1 iff  epsilon<=(kx+y-1)/(k+y-1).

The weak boundary kx+y=1 permits only epsilon0. Reached vertices in the smaller graph are reached in the original. No existence or smallness theorem for the needed structural deletion is supplied, and no such theorem is inferred here.

In the396-vertex graph the crossing A-neighborhoods have sizes21,21, intersection3 and union39. Union/intersection replacement preserves first degrees because the altered middle weights are equal. It need not preserve degrees for unequal weights. Removing the two old C links leaves each C's original45 predecessors intact: each containing nine-set has56 relevant four-subsets and at least54 remain. Adding the union type raises reach to51 when c belongs to either four-label and55 otherwise. Consequently it cannot receive even one C edge while preserving the old maximum, whereas its required degree is four. Intersection edges cannot reduce this reach. All other328 middle vertices are fixed.

My separate complete enumeration of all108900 ordered minimal legal four-neighbor reassignments confirms minimum possible maximum51/55:23100 assignments give51 and85800 give55. More than four neighbors cannot lower reach. This strengthens the finite local control and agrees with the structural family computation. It still refutes only this specified local monotone operation; global rearrangements, reweighting and the original conjecture are unaffected.

## New controls and limitations

`independent_controls.py` uses no author or earlier reviewer import. It completed before candidate inspection, preserving full stdout and every rational certificate:

| Mechanism | Exact completed controls | Qualification |
|---|---:|---|
| Literal two-layer graphs |1,045,924 graphs;4,585,424 triggered graph/k instances|All nonempty row matrices for A<=4,B<=3,C<=3;k1–6; no universal extrapolation|
| Weighted primal/dual systems |70 systems,64 with rank2 and68 with overlapping incomparable allowed unions|Exact positive unequal A weights, all relevant support topologies in the stated finite boxes;63 strict-boundary equalities|
| Disjoint partition bounds |247 nonvacuous systems,90 endpoint equalities|Every set partition through six A vertices under the enumerated equal/unequal weights|
| Actual-graph conditioning |1,038,258 checks,173043 nonempty A/B cuts and56547 positive remaining-y checks|Independent cut identities with all denominators retained; includes C deletion, not a substitute for the candidate-specific B deletion audit|

`postinspection_controls.py`, explicitly outside the initial independence seal, adds three actual sharply unequal rank-two graphs, including weights at10^18 scale; eighty B-deletion boundary checks with eight zero-deletion weak boundaries; a real exceptional B deletion; and the108900 legal local reassignments. These distinguish nonvacuous examples from implication checks whose premise fails. A rational k1 equality graph already shows why replacing the strict source condition by equality fails.

No floating point is used. `comparison_audit.py` separately rechecks every one of my70 primal/dual certificates and every frozen source-family219 LP certificate,330 binomial endpoints and seven covering primal/dual certificates. Primal and dual feasibility plus equal objective values provide checkable finite optimality certificates; mere solver output is never treated as proof. The infinite theorem scopes come from the written analytic arguments above, not enumeration totals.

## Complete replay, frozen artifacts and repaired queue

All five proof texts, all five author checkers, both package wrappers and the historical independent checker were fully read before execution. All remaining target source/state/result/request/publication/log/receipt files and nested manifests were inspected. All executable family-review code was read for later comparison and its frozen hashes validated.

Private executions are captured by `replay_capture.py`. The five author outputs are byte-identical to their respective frozen TURN_CHECKS receipts:377063,20643,12105108,164794,299628 assertions, totaling **12,967,236**. The historical reviewer adds **30,053**, with complete stdout byte-identical to its frozen receipt. All nine captured executions exited0 with empty stderr, including source-bound packet/publication and source-free publication runs. The private source-bound packet stdout exactly equals the frozen `review/AUTHOR_REPLAY.json`; the complete source-bound publication stdout also exactly equals root's independently captured full stdout.

The aggregate historical `FINAL_REPLAY.json` contains29 bindings because it predates the final author manifest. The current source-bound packet has67:27 historical bindings,38 final-author-file bindings and two raw-source bindings. Its per-turn replays match the old aggregate exactly. I do **not** assert aggregate byte equality between29 and67. The source-free packet has65 bindings and zero source PDFs; its successful public replay does not certify raw-source access.

`binding_audit.py` checks the repaired49-path diff from actual current-main parent `86a2c300cfc07fb2fdb8ac3ab45544c5f3231828`:48 target artifacts plus QUEUE. Every file matches its repaired manifest and exact Git blob. All48 target artifact bytes also equal the original frozen head `967e8e489aa4599f712d5ddcde62e591827f7e38` and original snapshot. All five historical manifests, their predecessor hash chain, final author manifest, historical review manifest, publication manifest and freshly downloaded source hashes validate.

The actual repair parents are exactly the original frozen head followed by current main. Comparing their queue blobs against the repaired head finds only physical line420 changed; splitting that line finds only cells8 and9 changed to `unsolved` and `5/5`. Every other current-main queue byte is preserved. This independently verifies the repair rather than trusting its receipt. Prior PR384's actual merge `3f18fa7b30851b165b604645d05f332263e9a301` exists with two parents and is an ancestor of that current-main parent, verified read-only.

The three family output manifests validate with exact inventories:80 source/LP files,36 maximal-type files,27 laminar files. An additional external snapshot-manifest binding makes37 checks for the maximal family in my receipt; this does not conflict with root's36-file count. Their complete mathematical conclusions agree with my independently established scopes. Their original49 bindings are to the original head, so they remain mathematical comparisons; the repaired queue and parents were checked anew here. Historical references in those reports to pending predecessor dispositions were not substituted for the actual ancestry check.

I compared all four full root maximal-family stdout JSON records to the corresponding family artifacts, excluding only recorded elapsed-time metadata. Root's source/LP and laminar stdout summaries match the frozen full artifact counts; every referenced code hash, source/LP output verification receipt and root public replay stream hash validates. The detailed family artifacts remain manifest-bound. Root's claim of complete private family-output equality is root evidence, not a claim that I re-executed all family programs; I independently verified all exact LP certificate fields and the full direct-stream artifacts available for comparison.

## Strongest verified result and exact remaining gap

The strongest unbounded-size statement verified is the full asymmetric all-k implication for pairwise-disjoint maximal first neighborhoods, with arbitrary positive weights, together with conditional deletion stability. Other completed scopes are exact complete-uniform template optimization, arbitrary-positive-weight rank-two half reach, cardinality-sensitive maximal-type inequalities and the strict symmetric threshold through uniform |A|<=5k. The failed cover and local uncrossing operations are precisely scoped obstructions.

Arbitrarily large overlapping higher-rank first-incidence families remain unsupported. No general support reduction, laminarization, small structural deletion, universal proof or source counterexample is given. A route that merely assumes such a reduction transfers the central difficulty to an unsupported claim and remains blocked absent a materially new mechanism. The original package must retain **unsolved5/5**. Required repairs: **`[]`**.

All writes are confined to `final_adversary/`. Git/index/branch/queue/candidate/remote/service state was left unchanged. Raw sources and private execution copies are ignored. No individual was contacted and no outreach was prepared. `OUTPUT_MANIFEST.json` seals reproducible code, full outputs, this report and the timestamped research log; `OUTPUT_MANIFEST_VERIFY.json` reports its external SHA256 verification.
