# Independent adversarial checkpoint: FUSF graph-square degree

Timestamp: 2026-10-24T10:38:34-07:00. Completion estimate for this scoped verification task: **100%**. Record: **23575190**, “Free spanning-forest degree can decrease under squaring.”

**Verdict: no substantive mathematical gap found in the stated expected-root-degree comparison.** The complete finite-current certificate freshly passes both the deposited verifier and a newly written independent word-tree verifier. Two exact finite reduction checks were also independently reconstructed. The infinite free-boundary passage is mathematically justified by finite support and exhaustion, not by a wired-resistance calculation. This is a focused internal AI-assisted mathematical check, not full human peer review or historical firstness certification.

## Claim independently reconstructed

Let T be the3-regular tree with a chosen end and p its endward parent. G joins v to p(v) and p²(v), all edges simple and of unit conductance. H=G² adds every simple edge at graph distance at most2. Then

- G is infinite, connected, locally finite, simple and vertex-transitive of degree8, with nonunimodular full automorphism group.
- H is vertex-transitive of degree40.
- Edeg_FUSF(G)(o)=(24−sqrt(2))/7=3.226540919660986… .
- Edeg_FUSF(H)(o)≤3208526010913748780/10¹⁸=3.20852601091374878.

Thus squaring lowers the expected root degree by more than0.0180149, using the exact original value and the certified upper bound. The paper states the simpler rational separation Edeg(G)>3.22 and Edeg(H)<3.21. With its adopted b_F=Edeg/2−1, the displayed manuscript gap>1/200 follows. The fresh rational-only check actually yields b_F(G)−b_F(H)>573699454312561/10¹⁷=0.00573699454312561 from the coarser original lower bound3.22. The stronger decimal estimate is explanatory; all decisive inequalities are exact.

## Fresh evidence

The supplied ZIP was read and safely extracted only beneath `reviews/fusf_check/release`. Its certificate is SHA256 `6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f`.

1. `release/verify_currents.py` freshly exited0 with PASS. It checked797,240 actual integer current entries,122,800 vertex-divergence equations, all40 individual energies and their exact total. Its four deliberate corruptions were rejected. Actual execution output is preserved in `run_0.json`.
2. `release/check_reductions.py` freshly exited0 with PASS, recovering branch depths0–3 and induced-exhaustion circuits n=2,3. Actual output is `run_1.json`.
3. **New independent reconstruction:** `independent_currents.py` uses tuple words, with a three-way first branch and binary later branches, rather than importing or calling any deposited verifier function. It independently built the3070-vertex radius10 tree ball, oriented parent relation, induced grandparent graph, its finite simple square, all19,931 sorted edges and all40 infinite-square root neighbors. It checked every current, divergence and energy against these freshly generated objects and reproduced the exact total. It exited0 with PASS_INDEPENDENT_WORD_TREE_CERTIFICATE; output is `run_2.json`.
4. **New independent circuit check:** `independent_reductions.py` separately constructs endward descendant cones by tuple words and performs global exact rational star-mesh/Schur elimination. Branch conductances at depths0–4 are1/2,2/3,7/10,12/17,41/58. The n=2 induced circuit has31vertices and terminal triangle(7/3,17/10,1), giving parent resistance27/80 and grandparent resistance121/240. The n=3 circuit has127vertices and triangle(12/5,6236/2669,1), giving8905/27608 and7901/17255. These match the manuscript. It exited0 with PASS_INDEPENDENT_EXACT_REDUCTIONS; output is `run_3.json`.

No floating-point solver, source claimant search program, third-party package or network was needed for any fresh computation. The finite checks are not asserted to prove an infinite theorem by sampling.

## Free versus wired boundary audit

For finite unit-conductance graphs, Kirchhoff gives the edge marginal equal to effective resistance; Thomson gives resistance at most the energy of any feasible unit flow. The manuscript defines free resistance as the decreasing limit over connected finite induced free subgraphs. Therefore the finite marginal identity passes to FUSF one edge at a time.

Each of the40 certified flows lives on J=(G[W])², a finite subgraph of H. Its divergence is exactly+1 at its named root neighbor and−1 at o. Any sufficiently large induced free H-exhaustion contains J. Extending the flow by zero does not create divergence at outside vertices and does not change energy. Hence R_(H_n)(o,v)≤E(theta_v) for every large n; taking the free limit preserves that upper bound. All40 root neighbors are present, so summing the40 edge marginals bounds the entire expected root degree.

This uses neither a boundary identification nor an arbitrary square-summable infinite flow. Minimizing over the latter would generally concern wired resistance; that tempting shortcut is explicitly avoided. Currents for different targets need not form one simultaneous multicommodity flow because expectation is the sum of individual edge marginals. Failure of simultaneous compatibility is therefore not a gap.

## Original-graph exhaustion and algebra audit

I checked both written free-exhaustion constructions in the complete seven-page manuscript.

For a depth-m child branch with two attachment terminals and no terminal edge, elimination gives kappa_0=1/2 and kappa_(m+1)=(1+2kappa_m)/(2+2kappa_m). The increasing bounded sequence has positive fixed point1/sqrt(2). When branches are grafted to the endward spine, the bottom conductance is A_m=1+2kappa_m, upper adjacent conductance C_m=1+kappa_m, and every skip-one edge retains conductance1. The suffix map is T_C(t)=C+t/(1+t), with derivative≤1/4 on the relevant t≥1 range. Its limiting fixed point is A=1+sqrt(2), since C=1+1/sqrt(2) and A=C+A/(1+A). Uniform contraction justifies the actual diagonal free edge-exhaustion, rather than an unproved interchange of limits.

The second construction uses nested *induced* finite descendant cones rooted at p^n(o), depth2n. End-ray coalescence puts every fixed vertex and edge in all sufficiently large cones. The local recurrence c_m=1+2c_(m−1)/(1+c_(m−1)), c_0=1, contracts on[1,infinity) by≤1/2 and converges to1+sqrt(2). The suffix maps again contract by≤1/4; their coefficient tails converge uniformly, giving the same terminal triangle limit. No point outside the finite induced graph is inserted or wired to another point.

The limiting terminal conductances are(A,A,1), so

R_tree=1/(A+A/(1+A))=(3sqrt(2)−2)/7,
R_gp=1/(1+A/2)=(6−2sqrt(2))/7.

The end stabilizer is transitive on each unoriented edge type. FUSF is automorphism invariant by exhaustion independence. There are three tree edges and five grandparent edges at o, hence3R_tree+5R_gp=(24−sqrt(2))/7. This counting requires no mass-transport principle and is legitimate on a nonunimodular transitive graph.

## Nonunimodularity and quantifier audit

A tree edge belongs to three triangles and a grandparent edge to one, so every automorphism of G intrinsically preserves the underlying tree edges. The induced G-graph on the three recovered tree neighbors is K_(1,2), whose center identifies the unique parent. Thus the full automorphism group, not merely one chosen subgroup, preserves the end. Parent and child paired suborbit sizes are1 and2; this is the nonunimodular situation used by the example. No tracial or unimodular invariance theorem is silently extended.

I also read the complete locally retained seven-page primary source, Abért’s *Some questions* dated2November2010. Section4 is headed “Vertex transitive graphs.” Question24 explicitly says “arbitrary vertex transitive graph” and its adjacent comment affirms the Cayley case. Question23 separately singles out the known unimodular case; Question22 explicitly mentions unimodularity. There is no global stated restriction to unimodular graphs that would exclude this construction. The source does not print a formula for its Betti-number normalization, so the paper is appropriately explicit about adopting b_F=Edeg_FUSF/2−1 and directly proving unequal expected degrees. It does **not** prove noninvariance of every alternative nonunimodular L² invariant or refute the known Cayley statement.

The original problem list warns that questions may since have been solved. I did not treat that old question as current-openness or priority evidence, and no fresh firstness claim is justified by this check.

## Plain-English interpretation

**Fair:** “Adding all distance-two edges can lower the expected number of edges touching a vertex in the free random spanning forest of an infinite transitive graph.” The numerical contrast is striking: available neighbors increase from8 to40 while expected retained forest degree drops from3.22654… to at most3.208526… .

“Adding edges lowers mean random spanning-forest degree” is acceptable as a short headline only with **can**, the **infinite** setting and the **free** forest made clear nearby. It must not suggest universal monotonic decrease, a finite uniform spanning tree counterexample, or uniform sampling of a vertex from an infinite set. “Expected root degree” is the precise statistic: average over the forest randomness at any fixed vertex, the same at every vertex by transitivity. No uniform random vertex of the whole infinite graph is required.

## Remaining limits

No concrete counterexample to the central stated claim, circularity, wired/free substitution, missing root-neighbor term, normalization mismatch or unsupported exchange of limits was found. The exact expected degree of H is not computed; a certified strict upper bound suffices. Historical firstness, all uninspected literature, final inaccessible journal editions, and a full foundational reproof of Kirchhoff/Thomson/free-exhaustion theory remain outside this checkpoint. This positive result supports using the paper as a most-surprising-result candidate and a strong specialist submission candidate, not as a declaration of peer-reviewed acceptance.
