# Independent analytic review of the published grandparent-graph comparison

Completed review checkpoint: 2026-10-24T22:53:09.208515+00:00. Estimated completion of this analytic review: 100%. Final disposition: **PASS for the analytic proof; the full theorem also requires the separately assigned certificate audit.**

Source reviewed: `../../sources/published-release/main.tex`, SHA-256 `2a6c8c01664db0a3b8ff10f50c9e1f82c96e5170430804a5c3316f158ae1a3d6`. Supporting source: the corrected 27 January 2009 author version of BLPS, https://rdlyons.pages.iu.edu/pdf/usf.pdf, specifically finite electrical principles/Theorem 4.1 and the opening of Section 5. No prior inventory assessments or prior mathematical reviews were consulted before this verdict. The deposited verifier, reduction script and current certificate were not read or run in this branch. A new independent word-tree construction and rational elimination calculation is supplied here.

## Exact claim and review scope

Let the 3-regular tree have a fixed end and parent map `p`. Let G join a vertex to its parent and grandparent. The central analytic assertion is

\[
\mathbb E\deg_{\mathrm{FUSF}(G)}(o)=(24-\sqrt2)/7=3.226540919660986\ldots.
\]

For H = G², the analytic transfer assertion is conditional on the finite certificate: if the forty listed flows have exactly the specified divergences and total squared integer numerator N = 3208526010913748780, then

\[
\mathbb E\deg_{\mathrm{FUSF}(H)}(o)\le N/10^{18}=3.20852601091374878.
\]

Both statements use unit conductances, simple squaring, free finite boundaries, and the complete root neighborhood. No unimodularity, mass transport, forest connectivity theorem, flow optimality, or simultaneous joint realization of forty flows is needed. The normalization b_F = Edegree/2 − 1 is an explicit convention here, not an identification with an unspecified nonunimodular L² invariant.

This review reconstructs both infinite limits and all structural/network steps. It validates the finite graph counts independently. It does not claim to have checked the 797240 certificate entries, settled historical priority, or supplied formal or human peer review.

## 1. Graph structure and full automorphism group

Every vertex has one parent and two children, plus one grandparent and four grandchildren. These sets are disjoint, giving 3 tree edges and 5 grandparent edges, hence degree 8. The graph contains the original tree, so it is connected; it is infinite, locally finite and simple.

An end-preserving automorphism of the regular tree can send any prescribed vertex to any other: map their parent rays in order and match the attached rooted binary trees. This proves vertex transitivity. The same construction sends an edge `{x,p^k(x)}` to `{y,p^k(y)}` for k = 1 or 2, so each of the two unordered edge classes is transitive. End-preserving automorphisms also preserve graph distance and therefore act transitively on H.

The claimed triangle counts are exact. The common neighbors of x and p(x) are p²(x) and the two children of x. The only common neighbor of x and p²(x) is p(x). Thus tree edges are recoverable from the graph by their triangle count. Among the three recovered tree neighbors of x, the parent is adjacent in G to both children, whereas the children are not adjacent to one another. The unique degree-two vertex of this K_{1,2} is p(x). Consequently the full automorphism group of G equals the end stabilizer of the original tree.

A direct Haar-measure argument verifies nonunimodularity without requiring it as a black-box assertion. Write Γ for this full group, a = p(x), K = Γ_x ∩ Γ_a. Since Γ_x fixes a, K = Γ_x. Since Γ_a can exchange its two child subtrees, `[Γ_a:K]=2`. Compact open stabilizers thus satisfy m(Γ_a)=2m(Γ_x) for left Haar measure m. Transitivity makes the stabilizers conjugate. In a unimodular group conjugation preserves Haar measure, a contradiction. This establishes nonunimodularity of the full group, not just of one subgroup.

## 2. Finite electrical facts and the correct infinite quantity

In a finite unit-conductance network, Thomson's energy is the sum of squared flows once per unordered edge. Adding edges or vertices cannot increase the minimum energy: extend any old flow by zero. Kirchhoff's marginal identity gives P(e in UST) = R(e⁻,e⁺) because the conductance of e is one. BLPS Theorem 4.1 and Section 5 support precisely these imports and the free weak limit; those references do not impose unimodularity.

For completeness, the exhaustion-independence step can be made entirely explicit. Let \(\mathcal F_{x,y}\) be all finite connected subgraphs containing terminals x,y. For any increasing edge exhaustion X_n,

\[
\lim_n R_{X_n}(x,y)=\inf_{F\in\mathcal F_{x,y}}R_F(x,y).
\]

The left side exists by monotonicity. Every fixed F is eventually contained in X_n, giving one inequality; every X_n is itself such an F, giving the other. Thus connected edge exhaustions and induced free exhaustions yield the same resistance. The edge event is a cylinder event, so the finite Kirchhoff identity passes to the free weak limit. This justifies the displayed marginal identity in the manuscript.

Equivalently, the relevant energy infimum is over **finitely supported** unit flows. The manuscript never replaces this by an unrestricted square-summable infinite flow. Such a replacement would be a different variational problem and would destroy the needed free-boundary inference.

## 3. First exhaustion: exact geometry and diagonal limit

For the branch B_m, every edge from its strict descendant region to the outside reaches a or b. The direct terminal edge ab is omitted, so child branches have disjoint edge interiors and contribute in parallel without double counting. At m = 0 the terminal path has two unit resistors, giving κ_0 = 1/2. Replacing the two child branches of u by κ_m leaves conductance 1+2κ_m from u to a, in series with the unit edge from u to b. Hence

\[
\kappa_{m+1}=\frac{1+2\kappa_m}{2+2\kappa_m}.
\]

The map is increasing and maps [1/2,1/√2] into itself. Its positive fixed point is κ = 1/√2. A useful explicit convergence estimate, stronger than required, follows from its derivative:

\[
F'(t)=\frac1{2(1+t)^2}\le\frac29\quad(t\ge1/2),\qquad
0\le\kappa-\kappa_m\le(\kappa-1/2)(2/9)^m.
\]

For L_{m,n}, each off-spine subtree attaches precisely to its two consecutive spine vertices. The two branches at x_0 give A_m=1+2κ_m; one branch above each higher nonterminal spine vertex gives C_m=1+κ_m. Skip-one edges retain unit conductance. No edge is identified with another boundary edge.

These graphs are nested in both m and n. For an arbitrary vertex z, its parent ray meets the chosen spine at a finite x_j. The finite path from z to x_j belongs either to a branch below x_0 or to the off-spine branch attached at x_j. For sufficiently large diagonal n, both j<n and the required branch depth are accommodated. Every edge is ancestor/descendant of tree distance one or two, and its endpoints plus required spine terminals occur at a finite later stage. Thus the diagonal is an edge exhaustion. Omitted top branches reappear when the top is extended.

Eliminate x_n, then x_{n-1}, and continue through x_3. At each step a direct C_m is parallel to a unit edge in series with the remaining conductance, so

\[
B_{m,n}=T_{C_m}^{n-2}(C_m),\qquad T_C(t)=C+\frac{t}{1+t}.
\]

The positive fixed point is \(B_*(C)=(C+\sqrt{C^2+4C})/2\). For C≥1 and t≥C the derivative in t is at most 1/4. Since C_m∈[3/2,1+1/√2], both starting values and fixed points are uniformly bounded. Hence, for an absolute finite M,

\[
|B_{m,n}-B_*(C_m)|\le M4^{-(n-2)}.
\]

On the actual diagonal C_n→C=1+κ. Since A=1+2κ satisfies A=C+A/(1+A), continuity of B_* yields B_{n,n}→A. This is a valid single diagonal limit; no exchange of unrelated limits is needed.

The final triangle has conductances (A_m,B_{m,n},1). Parallel/series reduction gives exactly the two displayed resistance formulas. Therefore

\[
R^F_G(o,p(o))=(A+A/(1+A))^{-1}=(1+3\kappa)^{-1}
=\frac{3\sqrt2-2}{7},
\]
\[
R^F_G(o,p^2(o))=(1+A/2)^{-1}=\frac2{3+2\kappa}
=\frac{6-2\sqrt2}{7}.
\]

## 4. Second exhaustion: induced finite sets and indices

S_n comprises all descendants of v_n through depth 2n. A point in S_n gains one unit of depth relative to v_{n+1}, while the depth cutoff gains two, proving nesting. For arbitrary z with parent-ray merging point v_j and branch depth d, its depth below v_n is n−j+d once n≥j. This is ≤2n for sufficiently large n. Thus S_n exhausts the tree and G[S_n] is an induced free exhaustion.

For the two-terminal descendant network rooted at x with parent y, the retained xy edge supplies conductance 1. Each child network supplies its c_{m−1} in series with a unit grandparent edge to y. This yields

\[
c_0=1,\qquad c_m=1+\frac{2c_{m-1}}{1+c_{m-1}},\qquad
a_m=1+\frac{c_{m-1}}{1+c_{m-1}}.
\]

At v_0 there are n descendant generations and both children contribute, giving c_n. At v_j with 1≤j<n, its depth below v_n is n−j, so the total available depth beneath it is n+j. The off-spine child has depth n+j−1 remaining below itself. Its series contribution uses c_{n+j−1}, hence coefficient a_{n+j}, exactly as stated. At the top v_n, the off-spine subtree has only the one attachment v_n. It carries no current in a terminal problem elsewhere and contributes no effective edge.

Successive upper elimination therefore gives

\[
u_{n-1,n}=a_{2n-1},\qquad
u_{j,n}=a_{n+j}+\frac{u_{j+1,n}}{1+u_{j+1,n}}.
\]

There is no off-by-one error in either the bottom or top index. The n=2 case, where the recursion has no internal iteration, is well defined.

The c-map has derivative 2/(1+t)^2≤1/2 on [1,∞), with fixed point c=1+√2. In particular

\[
|c_m-c|\le\sqrt2\,2^{-m},\qquad
|a_m-a|\le\sqrt2\,2^{-(m+1)},\quad a=1+\frac c{1+c}.
\]

Every u is at least 1, so its update has derivative at most 1/4 in the suffix argument. All coefficient indices are at least n+1. Taking ε_n = sup_{m≥n+1}|a_m−a| gives ε_n≤√2·2^{−(n+2)}. Also c=a+c/(1+c). Iterating the error inequality yields

\[
|u_{1,n}-c|\le \frac43\epsilon_n+2\,4^{-(n-2)}\to0.
\]

The explicit choice C_0=2 is sufficient because the starting coefficient lies in [1,2] and c∈(2,3), with actual difference less than 2. Thus the manuscript's unnamed uniform constant is legitimate. The final triangle tends to (c,c,1), recovering the two resistances above.

The two calculations use different free exhaustions but share the same local branch mechanism. Indeed κ_m=c_m/(1+c_m) and 1+2κ_m=c_{m+1}. Their agreement is valuable indexing and boundary corroboration; it should not be described as two unrelated mathematical mechanisms. The manuscript's wording that the second calculation independently recovers the value is reasonable.

## 5. Expected degree and exact inequalities

Automorphism invariance of the free forest and the two edge orbits give

\[
3R_{\rm tree}+5R_{\rm gp}
=\frac{9\sqrt2-6+30-10\sqrt2}{7}
=\frac{24-\sqrt2}{7}.
\]

The factors 3 and 5 count all incidences at the root exactly once. No factor of two, orientation convention or mass-transport assumption is missing. Since (73/50)²=5329/2500>2,

\[
(24-\sqrt2)/7>(24-73/50)/7=161/50.
\]

The claimed square upper bound is strictly below 321/100 because

\[
321\cdot10^{18}-100N=147398908625122000>0.
\]

The final normalized inequality follows from strict G lower bound and strict H upper bound:

\[
b_F(G)-b_F(H)>\tfrac12(3.22-3.21)=1/200.
\]

If the exact certificate bound is used directly, the difference is at least approximately 0.0090074543736; the weaker advertised strict bound 0.005 is conservative.

## 6. Square geometry, certificate interpretation, and free transfer

Every G step is an ancestor or descendant move of tree length one or two. Two moves in the same direction give strict ancestors or descendants at depths one through four. If the directions differ, either the moves cancel along their shared segment, giving a comparable vertex already counted, or they diverge at a common ancestor. The noncomparable possibilities are the sibling, the uncle, the sibling's two children, and the uncle's two children. These are disjoint. The degree is therefore 4+(2+4+8+16)+1+1+2+2=40.

Any two-step G witness from the root uses a tree walk of at most four edges, including the intermediate vertex. It therefore lies inside the radius-four tree ball, a subset of W. Hence J=(G[W])² contains the entire H-neighborhood of the root. Globally J need only be a subgraph of H; the proof does not mistake J for H[W].

The indexed tree rule and parent direction are internally consistent, including at the special ray and the outer boundary. A separate implementation using finite tree words, with parent `append zero` along the distinguished all-zero ray and `delete last letter` elsewhere, reconstructs the radius-ten ball without using the deposited indexing formula. It obtains 3070 vertices, 6137 edges in K, 19931 edges in J, and root indices exactly 1,…,22; 24,25; 30,…,45. Therefore the displayed graph size and root list are correct. Also 40·19931=797240 and 40·3070=122800.

For each target v, the stated divergence equation means a flow of one unit from v to o after division by D. The orientation is consistent; reversing all signs would leave energy unchanged in any event. Thomson gives R_J(o,v)≤E(θ_v). For any finite induced free exhaustion H_n, sufficiently large H_n contains the whole finite J, so extension by zero is a legal unit flow of the same energy. Thus

\[
R_{H_n}(o,v)\le R_J(o,v)\le\mathcal E(\theta_v).
\]

Passing to the free limit, applying the marginal identity and summing over all forty edges gives the claimed expected-degree bound. This is a complete analytic bridge from finitely many exact identities to the infinite free forest. It requires neither existence nor optimality of a limiting current, and the forty flows need not be mutually compatible.

## 7. Independent checks and falsification attempts

`independent_finite_checks.py` is a fresh standard-library-only program. It constructs the oriented tree with words and computes a global exact rational Schur complement in a shuffled vertex-elimination order. It does not call or import deposited scripts. Results are in `independent_finite_checks.json`.

- The induced n=2 graph has 31 vertices and 58 edges, and reduces to (7/3,17/10,1); its two resistances are 27/80 and 121/240.
- The induced n=3 graph has 127 vertices and 250 edges, and reduces to (12/5,6236/2669,1), exactly the published triangle.
- First-exhaustion cases (m,n)=(0,2),(1,3),(2,4) match the formula for (A_m,B_{m,n},1).
- A fresh radius-ten construction confirms the square graph and terminal counts and list.
- Interior tree and grandparent edges have the stated triangle counts.

The meaningful potential failure modes tested were: double-counted branch edges; hidden wired boundary identifications; top components with more than one attachment; incorrect descendant-depth indices; diagonal limits lacking a uniform estimate; omission of root square neighbors; confusing finite-square with induced-square edges; an invalid subgraph-to-free-resistance inequality; replacing full-group nonunimodularity by subgroup nonunimodularity; and oriented-edge energy factor errors. None survives inspection. The exact finite checks corroborate the graph realization, while the written arguments above, not those checks, establish the infinite limits.

## Disposition and exact remaining uncertainty

**Analytic PASS.** No erroneous displayed equation, substantive auxiliary claim, or missing analytic hypothesis was found. No change to the published mathematical proof is required by this review.

For the complete theorem, the exact integer divergence/energy claims remain a separately assigned computational gate. This branch deliberately did not duplicate that entrywise audit. The scope of Abért's question, literature priority, identity of public release files, and website wording are also outside this analytic gate. Numerical experiments alone, AI agreement alone, or the existence of a DOI would not close those distinct checks.

Public-safe explanation: “The paper gives an explicit vertex-transitive graph whose free spanning forest has expected root degree about 3.22654, while its graph square has expected root degree at most 3.208527. Two finite free-exhaustion calculations establish the original value. A finite exact-current certificate, together with a separate free-boundary argument, establishes the square upper bound. The example is nonunimodular; it does not contradict the Cayley or unimodular cases. This is an unrefereed result with substantial AI involvement, not formal proof-assistant or independent human certification.”


## Final adversarial reconciliation

2026-10-24T22:53:09.208515+00:00 — The isolated adversarial reviewer returned an independent PASS after 35 fresh exact rational checks, including induced graphs through n=5 (2047 vertices). Its written argument separately confirms both exhaustion constructions and all coefficient indices. It gives the stronger allowable constants M=1 in the first uniform bound and C_0=1 in the second; these agree with, and strengthen, the conservative bounds above. Its report is `adversarial/verdict.txt`, with its independent code and complete rational output in the same folder. No discrepancy or new correction arose. Analytic review is complete.
