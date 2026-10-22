# Second fresh whole-package adversarial reconstruction

2026-10-22 UTC. This derivation was recorded after reading the entire proposed manuscript and writing/running the new dyadic-coordinate/determinant checker, and before opening the first review's derivation or mathematical checking program. Earlier PASS and root adoption are disclosed context, never proof premises. Estimated review completion at this checkpoint: 55%; remaining tasks include primary-source scope, physical release reconstruction, PDF inspection, and closure.

## Exact claim and scope

The claim is an explicit counterexample to Abért's 2010 Question 24 for infinite connected locally finite vertex-transitive graphs with arbitrary full automorphism group. It compares expected **free** uniform-spanning-forest degree on a graph and its simple square. The original question abbreviates its quantity as an L²-Betti number, without specifying its normalization. The paper makes its own convention explicit: b_F(X)=Edeg_FUSF(X)/2−1. It neither identifies this with every definition of a nonunimodular Betti number nor answers a restriction to unimodular graphs.

## Graph, full group, and counting

Orient the 3-regular tree toward an end, and write p for the unique parent. Add each grandparent edge {v,p²v} to its tree edges. End-preserving tree automorphisms act transitively. Degree is 3+5=8, all added edges are distinct and the original tree ensures connectivity. The full group requires justification: a tree edge belongs to three triangles, whereas a grandparent edge belongs to just one. Thus all graph automorphisms recover the tree-edge subgraph intrinsically. Among the three tree neighbors of v, their induced grandparent edges form K_{1,2}, whose center is p(v). Hence every graph automorphism preserves p and the chosen end; the full group is exactly the end stabilizer. Stabilizer suborbit sizes for (v,p(v)) and its reverse are 1 and 2, proving full-group nonunimodularity. A nonunimodular subgroup alone would not suffice.

For an independent representation, vertices are (h,r), with integer h and a dyadic rational 0≤r<2^(−h). Parent is (h+1,r modulo 2^(−h−1)); the two children are (h−1,r) and (h−1,r+2^(−h)). Every upward ray eventually has r=0, and the resulting degree-three connected acyclic graph is a tree with a distinguished end. This does not import the preparation's indexed or binary-word constructor or the prior review's free-product constructor.

The square's root neighbors comprise four ancestors, thirty descendants at levels 1 through 4, one sibling, one uncle, two children of the sibling, and two children of the uncle: forty distinct vertices. Every length≤2 path in G has tree length≤4, so the tree ball of radius ten contains every possible such root path and captures all forty square-root edges in J=(G[ball_T(o,10)])². The order of square and restriction matters; J need not equal H[ball]. The weaker inclusion J⊂H suffices.

## Actual finite free networks, first exhaustion

Let B_m be the descendant branch of u of depth m with terminals a=p(u), b=p²(u), omit the terminal edge ab, and retain all branch grandparent edges. For m=0 it is u joined by unit conductance to a,b, giving κ_0=1/2. The two depth-m child interiors attach only to u,a; reducing them gives two parallel contributions κ_m. The remaining two-edge series path has conductance κ_(m+1)=(1+2κ_m)/(2+2κ_m). This increasing bounded sequence converges to 1/√2; the fixed point with nonnegative conductance is unique.

Build L_(m,n) from the spine x_i=p^i(o), 0≤i≤n, its tree and skip-one edges, two descendant branches at x_0, and one off-spine branch at x_i for 1≤i<n. Its edges are actual unshorted edges of G. The diagonal L_(n,n) is nested and exhausts every edge, because each finite vertex's upward ray eventually coalesces with the root ray. The omitted branch at the current top is present in a later network. For fixed terminals, sandwiching by induced balls shows this exhaustion gives the same free limiting resistance; no wire-to-infinity boundary was introduced.

After branch elimination, the root adjacent conductance is A_m=1+2κ_m and every higher adjacent conductance is C_m=1+κ_m; all skip conductances are one. Eliminate the upper spine from its actual finite terminal backward: its effective suffix conductance is B_(m,n)=T_(C_m)^(n−2)(C_m), T_C(t)=C+t/(1+t). On the relevant nonnegative compact interval t≥1, |T'_C(t)|≤1/4. Therefore B_(n,n) converges to the positive fixed point of T_(1+1/√2), namely A=1+√2. This is a uniform diagonal bound, not an unjustified exchange of two limits.

The final triangle has conductances A on two sides and one on the skip side. Thus R_F(o,p(o))=[A+A/(1+A)]^(−1)=(3√2−2)/7, and R_F(o,p²(o))=[1+A²/(2A)]^(−1)=(6−2√2)/7. Full-group symmetry gives three edges of the first type and five of the second. Finite Kirchhoff followed by the free exhaustion yields Edeg_FUSF(G)=3R_tree+5R_grandparent=(24−√2)/7.

## Second induced free exhaustion, independent boundary check

Let S_n be all descendants of v_n=p^n(o) down to depth 2n, with every induced G edge retained. S_n⊂S_(n+1), since old depth increases by one while allowed depth increases by two. The sets exhaust G by end-ray coalescence. Top branches with just one attachment affect neither of the terminal resistances; this is finite electrical elimination, not deletion of an infinite boundary condition.

Put c_0=1 and c_m=1+2c_(m−1)/(1+c_(m−1)); off-spine elimination gives a_m=1+c_(m−1)/(1+c_(m−1)). Along the retained upper spine the first adjacent conductance is c_n, higher ones are a_(n+j), and skips are one. The real finite top is u_(n−1,n)=a_(2n−1), and u_(j,n)=a_(n+j)+u_(j+1,n)/(1+u_(j+1,n)). Derivative bounds 1/2 for the c recursion and 1/4 for the suffix recursion give c_m→1+√2 and a_m→1+1/√2. Uniform coefficient errors for indices≥n+1 and a geometric series bound show |u_(1,n)−(1+√2)|≤(4/3)ε_n+C·4^(−n+2), with ε_n→0. The retained terminal's effect vanishes. This reproduces the same two free resistances through another actual nested finite network, excluding an accidental wired fixed point.

The independently authored integer Bareiss determinant checker verifies actual two-terminal branch conductances at depths 0–4. On the full induced S_2 and S_3 graphs (31 and 127 vertices), matrix-tree/separating-forest determinant ratios compute all three terminal-pair resistances; inversion reconstructs their triangle conductances. These are checks of finite identities, not substitutes for the universal exhaustion proof.

## Finite-supported currents bound the FREE forest on H

Each of the forty stored rows assigns an integer current to each of 19931 unoriented edges of J. The sole allowed orientation is its ordered endpoint pair. Dividing by D=10^9 gives divergence +1 at its indicated neighbor, −1 at root, and zero at all other 3068 vertices. Its energy is exactly Σ_e I_e²/D², with every unoriented edge counted once. The new dyadic checker reads every one of 797240 strict integer values, recomputes all 122800 divergence coordinates, forty exact energies, edge order, and target set.

For every sufficiently large induced finite free exhaustion H_n of H containing J, zero-extension of each stored current is a unit flow in H_n. Finite Thomson gives R_(H_n)(o,x)≤E(I_x). Kirchhoff identifies this with its finite UST edge marginal, and the free limit preserves the inequality. Summing over all forty actual root neighbors gives Edeg_FUSF(H)≤3208526010913748780/10^18. The forty separate flow trials need not coexist as disjoint commodities. Optimizing over arbitrary infinite ℓ² unit flows would instead compute the wired quantity; that invalid replacement is never needed here.

## Strict conclusion and adversarial controls

Exact rational/radical arithmetic gives (24−√2)/7>161/50 and 3208526010913748780/10^18<321/100. Hence the expected-degree decrease exceeds 1/100 and the explicitly normalized b_F decrease exceeds 1/200. Only the G degree is claimed exact; H has a certified upper bound, not a numerically asserted exact value.

The new checker uses matrix-tree determinants, finite Möbius matrix powers, Q(√2) exact arithmetic, and the dyadic model. Its eleven negative mechanisms catch a bad divergence, Boolean current, floating current, missing current, wrong terminal, reversed orientation, Boolean denominator, divergence-preserving circulation with false energy, doubled unoriented energy, omitted target, and wrong branch boundary. Normal, −O and −OO executions are three runtime modes of this one independent checking route, not three independent mathematical reviews. All modes have byte-identical outputs, and their exact source and output identities appear in INDEPENDENT_REPLAY.json.

No substantive mathematical objection was found in this reconstruction. This checkpoint is not the final package disposition; primary priority scope and artifact verification remain required.
