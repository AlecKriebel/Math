# Turn 4: exact two-vertex interface and failed naive contraction

Status: an exact finite state formulation for a two-vertex separator; this does not prove the needed compatible state always exists. Original unresolved.

## 1. Separator conventions

Let V=V_1∪V_2 and V_1∩V_2={u,v}, u≠v, with no arc between the two exclusive sides. Partition the graph's colored arcs as E_1⊔E_2 with every arc of E_i having endpoints in V_i. An arc with endpoints {u,v} must be assigned to one side, never copied. Isolated boundary vertices remain part of each side's vertex set. Parallel arcs remain distinct colored elements.

If T is a spanning out-arborescence, its restriction F_i=T∩E_i is an undirected forest with indegree at most one. Every component of F_i contains u or v: an interior component meeting neither could have no edge to the other side and hence disconnect T. Thus c_i, its number of components, is1 or2. Counting arcs gives

n-1=(|V_1|-c_1)+(|V_2|-c_2), while n=|V_1|+|V_2|-2,

so c_1+c_2=3. Exactly one side is connected and the other has two boundary-rooted components in the undirected sense. The directed roots of these components need not both be boundary vertices if the global root lies in that side.

## 2. Exact gluing lemma

Conversely, suppose F_i is a spanning undirected forest on V_i, every component meets {u,v}, and all its indegrees are at most one. Their arc sets and colors are disjoint. Then F_1∪F_2 is an out-arborescence precisely when

c_1+c_2=3, and deg^-_{F_1}(w)+deg^-_{F_2}(w)≤1 for w=u,v.

For sufficiency, assume c_1=1,c_2=2. The connected first forest joins u to v; the second has separate components containing u and v. Their union is connected, and the arc count is n-1, so its underlying multigraph is a tree. All interior indegrees are already bounded by1 and the two displayed inequalities handle the shared vertices. The indegree sum n-1 then forces exactly one zero indegree; in a tree this is the unique root and all arcs point away from it. Necessity follows from Section1 and the global indegree bounds. Two parallel or oppositely oriented arcs on the same undirected edge count as a multigraph cycle of length2 and cannot occur in an underlying forest.

For q=n-1 colors, define a side state to be (J,c,ε_u,ε_v), where J is the exact color set of such an F_i and ε_w its indegree at w. The original rainbow problem on this separated graph is equivalent to finding two realizable states with complementary color sets, component counts summing to3, and boundary indegree sums at most1. This is an exact, finite interface; it is not an existence theorem for complementary states.

## 3. A concrete failure of single-arborescence restrictions

On the theta graph with boundary0,1 and internal vertices2,3,4, take four color classes:

A_0={(2,0),(2,1),(0,3),(1,4)},
A_1={(3,0),(3,1),(1,2),(0,4)},
A_2={(4,0),(4,1),(0,2),(1,3)},
A_3={(0,2),(2,1),(0,3),(1,4)}.

Each is a spanning out-arborescence, and the underlying union is K_{2,3}. Use V_1={0,1,2}, V_2={0,1,3,4}. A_0[V_1] is the fork2→0,2→1; it has no directed path from0 to1 or from1 to0. Its other restriction has two components0→3 and1→4. For A_1, the first restriction is disconnected while the second is connected. Thus neither applying the original conjecture independently to the two restricted color families nor replacing each side by a single directed boundary arc preserves the input hypothesis and root information.

The state lemma retains the missing information. The checker verifies this valid original instance has a rainbow tree, so this is an obstruction to those contraction rules, not a counterexample to the conjecture.

## 4. Where the route stops

Enumerating side states may require exponentially many color subsets. More importantly, the fact that each whole input color is a spanning arborescence gives one pair of complementary *monochromatic* side structures, but does not by itself produce the required colorful compatible states. Claiming this compatibility would transfer the original difficulty to an unsupported assertion. The root-count pigeonhole proof for an articulation does not supply it.

For reproducibility, `verify_turn4.py` compares the interface criterion with a direct rainbow-tree search, including instances outside the original promise so both positive and negative outcomes are tested. Such finite checks establish neither theta-graph existence in all sizes nor a general two-sum closure theorem.
