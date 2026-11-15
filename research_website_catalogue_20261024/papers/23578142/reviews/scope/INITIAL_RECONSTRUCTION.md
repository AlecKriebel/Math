# Row126 paper-first independent source/scope reconstruction

This document is written after personal reading of all7 actual published PDF pages, all391 controlling TeX lines, and all7 freshly rendered individual PDF pages. No foreign scientific primary, native scientific programme/results, archived/current inventory opinion or sibling/root mathematical findings has been read. Only the target paper itself and identity/opaque custody metadata were available. Claims below are hypotheses assessed by reconstruction, not presumed true because deposited. Root gate is CLOSED; mathematical findings stay local until explicitly opened.

## Literal target and success criteria

The paper is A singleton-supported cycle correction to Byrnes's differential-poset bound, Alec Kriebel, printed Version1.0.0,22October2026,unrefereed. Native API version1.0.0,declared22October2026,created22October at21:01:06.850027Z,updated21:01:07.620984Z. Source API license CC BY4.0; prose itself says CC BY4.0 and companion code MIT. The mathematical domain is an infinite ordinary unweighted r-differential poset with finite ranks, unique minimum, N-grading, r a positive integer, and DU−UD=rI over Q/equivalent exact integer incidence counts. A weak identity only modulo a prime, a weighted graph or a locally-valid middle-layer fragment is outside that domain.

For n≥2 let Z=P_(n−2), X=P_(n−1), B_j the full incidence graph between ranks j−1,j, and b_j=β(B_j). Define S={z∈Z: some a∈X has pred(a)={z}}. A singleton successor is an upper element with exactly that predecessor, not an element z with only one successor. H_S has vertices S⊔X, retaining every X isolate, and all z-to-X incidences for z∈S. Define q_n=β(H_S)=Σ_(z∈S)(u(z)−1)−|X|+c(H_S).

The main full claim is 0≤q_n≤b_(n−1) and b_n≥q_n; consequently p_n≤U_n−q_n, U_n=1+rΣ_(k=0)^(n−2)p_k+(r−1)p_(n−1). Equivalently p_n≤r p_(n−1)+p_(n−2)+b_(n−1)−q_n. The preceding two ranks determine q_n without constructing rank n. Positive/attained q_n examples at r=3,n=3 and r=1,n=7 show coefficient1 sharp. Further full claims: all z supported implies local recurrence; at least two singleton successors for every z and n≥3 gives equality iff rank n is reflection-extension up to relabeling; every rank-one z has at least two singleton successors and hence p3≤r p2+r with reflection-only equality. All universal claims must follow without finite enumeration or chosen-witness restrictions. The reported finite enumeration/5764 witness selections are separate reproducibility statements, not assumptions of proof.

No claim of general local recurrence, improved global Fibonacci envelope, combinatorial strict growth, new reflection/Young families or unrestricted historical firstness is made. These exclusions are substantive scope, not missing proofs of asserted conclusions.

## Family1 — descent, connectivity and exact slack

If two same-rank elements share ≥2 upper covers, equal common-cover counts supply ≥2 lower covers. The lower pair again shares the original pair above. Repeating decreases rank until it requires two rank-zero elements, contradicting uniqueness. This proves both common-cover counts≤1, using exact integer equality, not linear algebra modulo a field.

B1 is the star with r leaves. For connected B_j, any two rank-j vertices can be joined by a path alternating through common lower covers; replace each projected step by the unique common upper cover guaranteed by the axiom. All rank-j vertices are then connected in B_(j+1). Every rank-(j+1) vertex has a predecessor because P is graded with unique minimum. Hence B_(j+1) is connected. The one-vertex projection case is harmless.

Sum u(x)=d(x)+r on rank j−1: e_j=e_(j−1)+r p_(j−1), e0=0, so e_j=rΣ_(k<j)p_k. Then b_j=e_j−p_(j−1)−p_j+1. Rearranging gives p_n=U_n−b_n and b_n−b_(n−1)=r p_(n−1)+p_(n−2)−p_n. Thus Byrnes's inequality follows from b_n≥0 but local recurrence needs monotonicity, a different claim. Check all signs and indices independently; b0 is unnecessary.

## Family2 — witness trees and simultaneous replacement

For each z∈S choose a singleton a_z. For each y∈N_z=succ(z) other than a_z, pair(a_z,y) has predecessor z and a unique common upper t. Any other lower cover w of such t shares an upper with a_z; a_z's sole predecessor forces w∈N_z. Distinct nonsingleton t covering a_z have no shared terminal other than a_z, since another common terminal would make a pair with two common uppers. Every other y appears once. Thus the union of these complete stars is a connected acyclic tree T_z with terminal set exactly N_z. When |N_z|=1 it is the terminal alone.

A top t cannot belong to both T_z,T_w with z≠w because it would cover a_z and a_w with disjoint predecessor sets. Every source/target internal vertex is therefore assigned to one replacement only; shared X terminals are allowed. Replace each source star with its T_z and retain all X vertices. For k internal vertices the tree has |N_z|+k−1 edges; replacing the source star changes E and V both by k−1. Connections among terminals and hence whole component count are preserved. β(K)=β(H_S), K⊂B_n, so b_n≥q_n. The separate inequality q_n≤b_(n−1) is just subgraph cycle-space inclusion and does not assert arbitrary β monotonicity over different rank graphs.

## Family3 — independent graph-minor formulation

There is an alternative concrete minor argument, useful to expose hidden gluing assumptions. In H_S contract each edge(z,a_z). In K contract each edge(t,a_z) for internal t∈T_z. Each internal t belongs to exactly one z and each a_z is distinct, so these contractions never identify distinct X terminals. Both contractions yield the same graph M on X: for every z∈S, put an edge a_z−y for each y∈N_z\{a_z}. No edge from two z can coincide, as two distinct predecessor neighborhoods intersect in at most one terminal. Thus M is simple, though allowing parallel-edge bookkeeping would not alter the argument. Every contracted edge is a nonloop tree edge and preserves β; deleting unused B_n vertices/edges cannot increase β. Therefore β(H_S)=β(M)=β(K)≤β(B_n). This avoids relying solely on the printed E−V count and shows a genuine cycle-space injection. Proposed check: construct M independently from the preceding incidence only, compare with both quotient graphs and exact binary cycle-space bases. Do not replace the bipartite graph by an unqualified clique projection: clique triangles can create spurious cycles.

## Family4 — equality and the second singleton's exact role

When S=Z, H_S=B_(n−1), and K is connected containing every X vertex. Any unused top t adds its full star with one new vertex and d(t) edges, all terminals already in the component; its β increment is exactly d(t)−1. Equality b_n=b_(n−1) forces all unused upper vertices to be singletons, not just an aggregate cancellation.

If a_z and b are distinct singleton successors of z, every nonsingleton top over b must lie in K and specifically T_z: its coexistence with a_w would force b's predecessor z=w. It also covers a_z. For each y∈N_z\{b}, the unique top covering b,y must then cover a_z,b, so it is the same unique h. Thus h covers all N_z. Another nonsingleton in T_z would share a pair with h, impossible. There is one h_z per z, distinct across z. For n≥3, z has a lower cover and |N_z|=u(z)≥r+1≥2, so h_z is indeed nonsingleton. Every x lies in d(x) such neighborhoods; u(x)=d(x)+r leaves r singleton tops. This is exactly reflection. Conversely reflection has p_(n−2)+r p_(n−1) tops. The statement does not promise equality classification with only one singleton, nor at n=2. Proposed falsifier: use a valid prefix with one singleton in later ranks, compare arbitrary star partitions; do not infer the second singleton automatically outside rank one.

## Family5 — rank-one lemma and infinite examples

For rank one, there are r vertices and each has r+1 uppers. Nonsingleton uppers of z use disjoint nonempty subsets of the other r−1 vertices (otherwise some pair has two uppers), hence number≤r−1, leaving≥2 singleton uppers. This is a self-contained count; source attribution to Gaetz–Venkataramana Proposition3.4 must be verified later, not treated as novelty.

A reflection step over any valid finite prefix adds one upper over N_z for each preceding z plus r singleton uppers for each current x. It preserves exact common-cover and degree identities at the current rank; older ranks stay unchanged. All new tops have lower covers, ranks stay finite, and iteration gives an infinite ordinary poset, so finite examples really enter the quantified domain.

For r=3, root→3 singletons, then rank2 has the3 pair blocks and2 singleton copies at each rank1 vertex: sizes1,3,9; e2=12,β2=12−3−9+1=1. Reflect gives p3=3+3·9=30,e3=39,β3=39−9−30+1=1. All rank1 z have singleton successors, q3=β2=1. U3=1+3(1+3)+2·9=31. Hence attained improved30.

For r=1, Young prefix sizes1,1,2,3,5,7 through5; reflect gives12 then19. e6=19 and β6=19−7−12+1=1. Rank6 has a singleton over every rank5 element; q7=1, β7=1, U7=20. Either example forbids any universal coefficient c>1 since p=U−q with q=1. Sharp coefficient does not establish the best arbitrary function of preceding incidence data.

## Family6 — exact failure outside the claimed category

The displayed relaxed sizes1,3,3,7 can be reconstructed independently without native code. Root covers three rank1 vertices; rank2 consists of the3 pair blocks of that triple; rank3 has one block containing all3 rank2 vertices plus2 singleton copies at each. At rank1, upper Gram has diagonal2 and off-diagonal1, lower Gram is all-ones, difference I. At rank2, upper Gram diagonal3/off1 minus lower Gram diagonal2/off1 gives I. But the root has3 uppers, so rank-zero commutator is3I, not I. These middle layers have β2=1,β3=0; this is not a counterexample in the target class. In characteristic2 the root discrepancy disappears, so the weakened mod2 r=1 category even has p2=3>U2=2. This explicitly tests the exact-integer restriction and the need for a full valid prefix. It is not a repaired/narrowed replacement theorem.

## Family7 — boundaries, witnesses and residual gap

At n=2, Z is just the root; every rank1 vertex is a singleton successor, but H_S is a star and q2=0, b1=0. Thus p2≤r²+1. For r=1 the sole-terminal replacement has no internal top; E,V both decrease by1 and β stays0. Empty S gives X isolates, c=|X| and q=0; dropping isolates carelessly can corrupt component bookkeeping. Retaining/removing a lone isolate changes V and c together and β should not change; a check must not conflate this with forcing connectivity.

Witness choice must be arbitrary. Different witnesses can yield different K subgraphs but the contraction argument gives the same β=q, not necessarily identical labeled edge sets. The finite paper statement samples first/last above thresholds and cannot establish all choices; the proof does. Proposed independent bounded check can exhaust every witness in small custom examples, using quotient graphs rather than the native exact_checks implementation.

The exact residual is b_(n−1)−q≥0. For ordinary Young n6, p6=11, U6=13, local bound12, b5=1 and q6=0 according to the target; this needs an independent partition/incidence reconstruction. If confirmed it falsifies any assertion that the refined RHS always equals the local RHS. It does not falsify the actual partial improvement claim. General b_n≥b_(n−1) remains unproved here. r=n=1 gives p0=p1=1, so an unqualified strict-growth claim would be false; the note explicitly avoids it.

## Family8 — source/prior-work interfaces and falsifiability table

The actual printed improvement request and exact formula on OWR1452 must be read; the terminal '=1' axiom claim must be compared with Stanley's ordinary definition and examples, not silently normalized. Byrnes Chapter5 must be read for cumulative upper bound versus separate local conjecture/global envelope. Stanley Proposition6.1 and following paragraph must cover reflection/extension of arbitrary prefixes. Stanley–Zanello Remark8 should delimit existing incidence/dimension sums. GV Proposition3.4 must match the credited lemma. Lewis/Miller–Reiner singleton/crown antecedents, Qing Chapters2–3 and Wright2019 slides/abstract need actual bodies/explicit access limits before broad priority comparisons. Miller strict growth preprint must not be mistaken for a combinatorial proof or a new consequence here. No primary body is claimed read at this checkpoint; all locators came only from the target bibliography.

| Mechanism | Current independent status | Exact pending test/gap |
|---|---|---|
| Degree/cycle identities | Algebraically reconstructed | Independent finite matrices and connected components |
| Universal transfer | Reconstructed by replacement and independent contractions | Attack shared internal vertices and arbitrary witnesses; no reliance on native output |
| Equality characterization | Reconstructed using d(t)−1 and two singleton witnesses | Exact complete-star condition and n≥3 boundary controls |
| Strict/attained correction | Hand computations agree | Construct full finite incidences and indefinite-extension proof |
| Weak middle-layer false positive | Explicit outside-category construction derived | Verify all three integer Gram differences and mod2 warning |
| General local recurrence | Not claimed or proved | Residual b_(n−1)−q can remain positive |
| Literature contribution | Bounded candidate interpretation only | Actual primary bodies needed; novelty/open status not certified |
| Native reproducibility claims | Unread and unexecuted | Coordinate one lane owner, then meaningful scoped inspection without duplicate campaign |

Initial provisional assessment: no substantive defect found in the universal argument as reconstructed, but source-interface and meaningful independent finite controls remain required. This is not a final verdict or publication authority. No source repair, stronger new theorem, firstness assertion or follow-up is proposed.
