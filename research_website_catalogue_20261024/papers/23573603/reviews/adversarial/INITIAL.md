# Source-only adversarial INITIAL — supercritical nonuniqueness

The complete actual five-page manuscript and all323 TeX lines were personally read, followed by five individually viewed fresh own PDF rasters. The co-deposited PDF is byte-identical to the standalone reader; this covers one mathematical five-page body, without claiming separate pixels for the duplicate occurrence. No supplied/native code, results, archived audit, README opinion, current peer/root finding or foreign primary body has been opened. All controls below are independently authored source-only work.

## Exact target and failure hypotheses

The source claims one deterministic countable connected simple graph of maximum degree4, roughly isometric to Z^2 with the stated multiplicative-plus-additive convention and C=100, satisfying pc<=9/10 and P_19/20(N_infinity>=2)>2200741829/6461571200>1/3. Every actual vertex survives with positive probability at9/10. The original source question is expressly treated under a declared all-supercritical almost-sure-uniqueness interpretation; the manuscript says the original omits a p-quantifier. This audit preserves that scope instead of attributing unique author intent, asserting failure arbitrarily near1, exact cluster count, almost-sure multiplicity, critical nonuniqueness, or a simultaneous-in-p law.

Attacks targeted: bounded subdivision concealing nonuniform distortion; omitted chain midpoints; coarse independence lost at shared endpoints; infinite actual components containing only finitely many originals; dual-cut holes/diagonal contacts/degree4; probability assigned to nonexistent quadrant edges; all-distance A-B connections missed by a finite window; strong excursions invalidating all-weak extraction; hidden uniqueness monotonicity/transitivity; and arithmetic or infinite-event independence errors. No lattice threshold formula is used.

## Full-domain metric and series reduction

Include original Z^2 in G. Its lattice edges expand to lengths in[1,100], so d_Z<=d_G<=100d_Z on originals. Every actual vertex is at distance<=50 from its chosen nearest original endpoint. The projection f sends adjacent vertices to equal or neighboring originals, including the tie transition at positions50/51 of a weak chain. For arbitrary actual x,y, triangle expansion through anchors gives d_G(x,y)<=100d_Z(fx,fy)+100. Original surjectivity gives net distance0<100. The source lower bound with C=100 follows from the stronger d_Z<=d_G. The own10201 midpoint-pair checks corroborate the uniform argument; a midpoint mapped to its original endpoint has positive actual distance and zero projected distance, explicitly rejecting an additive-free upper-bound mutation for this f. Unbounded subdivision lengths would destroy the fixed uniform argument; they are not used.

At actual bond parameter p, the indicator that a weak chain is traversable is the product of100 independent bond indicators, so its probability is p^100. Distinct chains have disjoint edge sets, even when endpoints coincide; all coarse states are independent. This is a bond argument, not a site argument. The own64-state two-chain control checks complete original-vertex connectivity and exact product independence, with a shared-site countercontrol that is genuinely dependent.

An actual path between originals can be loop-erased and must traverse every private degree2 chain completely. Conversely any coarse open path expands. If an actual component contains k finite originals, it lies in those vertices and at most4k incident finite chains, hence is finite. A component without an original lies in one chain. Thus infinite actual/coarse components correspond, including partial dangling chain fragments.

## Independent mod2 cutset and sharper first-step counting

For any finite D subset Q=N_0^2 containing(0,0), its edge coboundary intersects the bottom primal ray an odd number of times: membership starts1 and eventually becomes0. The crossing dual graph has even interior degrees and bottom/left boundary stubs of degree1. By componentwise degree parity, some component with an odd number of bottom stubs has an odd number of left stubs. A finite simple path joins opposite stub types. This proof uses mod2 intersections, not an asserted simple outer tour. Its path starts at(i+1/2,-1/2), ends(-1/2,j+1/2), and has length m>=i+j+2.

The independently implemented exact control enumerates ALL32768 subsets of a4x4 certificate box containing the corner, but includes every outgoing Q-edge beyond that box in its coboundary. It checks parity, boundary degrees and an explicit simple bottom-left path. It includes disconnected sets, holes and20839 degree4 cases. The two-point set{(0,0),(1,1)} already forces a degree4 dual vertex, rejecting a false degree2-only boundary premise. A full finite box has an empty cut if one wrongly deletes outgoing edges; that negative control demonstrates why the infinite-quadrant definition matters. The enumeration is falsification evidence, not the proof for arbitrary D.

There is a useful independent sharper count: the first step from a bottom stub is forced, subsequent nonbacktracking choices are at most3, and at most m-1 bottom starts can occur. Therefore finite corner-cluster probability is at most

    sum_{m>=2}(m-1)3^(m-1)(1-t)^m = z^2/[3(1-z)^2], z=3(1-t)<1.

At t=9/10 this equals3/49, giving corner survival>=46/49. This collateral strengthening is not needed to repair or replace the printed143/245 bound. The printed looser path count independently evaluates to102/245 failure and143/245 survival. It only overcounts eligible paths; each eligible path crosses distinct existing Q-bonds and has exact closed probability(1-t)^m. No nonexistent boundary bond receives a probability.

The positive corner-survival probability gives pc<=9/10. For any actual vertex, condition a fixed finite path to that corner open. Coupling the untouched bonds identically makes the corner-survival event increasing under this conditioning; multiplication by p^length gives positive survival. This justifies basepoint independence without transitivity or a lattice pc formula.

## Every weak bridge, not a local barrier

Given any finite A-B coarse connection, keep the part between its last A-visit before its first B-visit, then loop-erase. All internal vertices are outside A union B, so every retained edge is weak. This handles arbitrarily distant crossings and strong-edge excursions. A start lies on one of the boundary rays(1,n),(n,1), with n>=1, and distance to B is n+3. There are at most4*3^(m-1) self-avoiding length-m paths from a start. Summing the distance-weighted walk bound over every start gives

    (8/3) sum_{n>=1} sum_{m>=n+3} r^m
    = (8/3) sum_{m>=4}(m-3)r^m
    = (8/3) r^4/(1-r)^2, r=3p^100.

The own explicit paths(1,n),(0,n),(-1,n),...,(-1,-1), n=1,...,64, are simple all-weak paths of EXACT length n+3. The same construction for arbitrary n proves that no finite-window barrier argument could replace this all-distance sum. The source does not make that mistake.

Bernoulli's inequality gives(20/19)^20>=39/19>2, so at p=19/20, q=p^100<1/32 and r<3/32. The positive generating function is increasing, giving P(W)<27/107648. Exact rational controls verify the full printed product2200741829/6461571200 and its excess140654287/19384713600 over1/3. The mutation with unit subdivision has3p>=1 and cannot use this convergent-series estimate; no claim that100 is a minimal valid length is made.

S_A,S_B and W depend on disjoint infinite bond families. Finite-cylinder independence extends to their sigma-fields by a monotone-class argument. Survival is a countable intersection of finite-distance events, and W a countable union of finite-path events, so all events are measurable. On S_A intersect S_B intersect W-complement, the two infinite strong clusters cannot share an actual component: any such component connection would be a finite path and hence force W. The printed positive probability bound follows without uniqueness monotonicity or a0-1-infinity theorem for N_infinity.

## Separate tail-event strengthening as an independence check

A different infinite-event route gives a collateral check. Let E_A mean that SOME infinite strong cluster exists in A. Changing finitely many bonds cannot remove every infinite component: deleting k edges splits an infinite connected component into at most k+1 pieces, at least one infinite. Adding finitely many bonds cannot create infinity from finitely many finite components joined at their finitely many endpoints. Hence E_A is tail-measurable. Independence from every finite cylinder and a monotone-class argument imply E_A is independent of itself, so its probability is0 or1. Positive corner survival makes it1. The same holds for B. Therefore P(N_infinity>=2)>=P(W-complement)>107621/107648.

This stronger local validation is not the claimed0-1-infinity classification of cluster counts and does not assert almost-sure multiplicity. The printed weaker theorem is already supported independently. No new publication/priority claim or follow-up programme is inferred from this elementary collateral corollary.

## Remaining primary interfaces

No internal counterexample or substantive combinatorial/probabilistic gap was found in the full explicit graph theorem. The literal 2013 definition/question/context, and the exact assumptions/model/version of the comparative literature, remain uninspected until per-paper PrimaryGO. The declared interpretation must be matched honestly to its ambiguous source rather than silently upgraded. Historical earlier-publication/current-openness/exclusive-priority statements are not certified by these mathematics. Follow-up null. Current scientific-review completion estimate65%, pending these actual primary interfaces and any selected meaningful native-route inspection.
