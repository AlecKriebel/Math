# Turn4: affirmative result for translated sums of coordinate simplices

AI-assisted mathematical proof candidate; independent review pending. Original unresolved4/5. This is the hypergraphic/coverage subclass of integral base polyhedra. Minkowski-sum and greedy facts are classical; no novelty certification is made.

## 1. Representation and statement

For a nonempty subset H of the coordinate ground set, let Delta_H=conv{e_i:i in H}. Suppose

B=sum_{H in a finite multiset} Delta_H - a

with a integral, all vertices of B in{−1,0,1}^n and0 in B. Then B has opposite vertices.

Such sums are base polyhedra of the submodular coverage function b(S)=sum_H 1_{H intersect S nonempty}-a(S). Repeated subsets are allowed. Singleton simplices are fixed translations and may be removed while adjusting a. We henceforth assume every H has size at least2. Coordinates in no remaining H are fixed and hence zero. This class includes graphical zonotopes but also non-zonotopal sums with larger simplices; it does not include all integral base polyhedra.

## 2. A dual incidence graph forced to be a pseudoforest

Let d_i be the number of remaining simplex summands containing coordinate i, counted with multiplicity. The coordinate interval of the sum is exactly[0,d_i]: each non-singleton simplex containing i permits both endpoint values0 and1, and independent Minkowski choices add. Thus the interval of B is[−a_i,d_i−a_i]. Containment in[-1,1] forces d_i<=2. Integrality and0 membership imply:
- d_i=2: a_i=1
- d_i=1: a_i is0 or1
- d_i=0: a_i=0

Construct a multigraph G whose nodes are simplex summands. Each coordinate occurring twice is an edge joining the two summands; each coordinate occurring once is a stub at its summand. Parallel edges are allowed, loops are not. Call a stub required if a_i=1 and optional if a_i=0.

For any connected component of G, its summands contribute exactly one unit each to the sum of its incident coordinate set. Since0 is in B, the same total equals the sum of the translation coordinates. If the component has h nodes,m edges and r required stubs, this gives

h=m+r.

Connectedness gives m>=h-1. Therefore either m=h-1,r=1 (a tree with one required stub) or m=h,r=0 (a unicyclic component with no required stub). This uses the actual0 membership, not an assumed integral allocation. An isolated node is the tree case with exactly one required stub.

## 3. Construct exposed opposite vertices

A weight vector with a unique largest coordinate in each simplex exposes a unique point of the Minkowski sum: select that coordinate in each summand and add. Subtracting a gives an exposed vertex of B. We construct two such weights componentwise.

**Tree component.** Root it at the node bearing its unique required stub. Give that stub weight0. Give each tree-edge coordinate weight minus its distance level from the root: the edge to a node at depth j has weight−j. Give every optional stub a still smaller weight, below all edge weights. At the root the required stub is the unique largest incident coordinate; at every other node the edge to its parent is uniquely largest. Thus every tree edge is selected exactly once, the required stub once, and all optional stubs zero times. These counts equal a, so this component's exposed vertex is0. Use the same weights for the second vertex.

**Unicyclic component.** Its unique cycle has length at least2, allowing a two-edge parallel cycle. Assign pairwise distinct positive weights to the cycle-edge coordinates. Give attached tree edges negative weights strictly decreasing with distance from the cycle; optional stubs receive weights below all these. Every off-cycle node uniquely selects its edge toward the cycle. Each cycle node uniquely selects the heavier of its two cycle edges, ignoring attached edges and stubs.

For the second weighting reverse the total order of cycle-edge weights while keeping them positive, and leave all other weights unchanged. At each cycle node the other cycle edge is now selected. Hence for each cycle-edge coordinate the two selection counts add to2, while each attached tree edge is selected once under both weights. Every optional stub is selected zero times under both. Since a_i=1 on all edge coordinates and0 on the stubs in this component, the two translated exposed vertices are negatives of one another.

Different components use disjoint coordinate sets, so these assignments combine into two global weight vectors. Each yields a unique exposed point of every simplex and therefore a vertex of B. Their translated coordinate vectors sum to zero, proving the theorem.

## 4. Scope and reproducibility

The proof does not require the whole hypergraphic polytope to be centrally symmetric. It identifies an exposed product face on which the tree factors contribute0 and cycle factors provide opposite choices. The stronger assumption of a positive coordinate-simplex decomposition is essential to the incidence graph. General submodular functions need not admit that decomposition; no reduction of the original problem to this class is asserted.

The checker builds tree and unicyclic incidence components with required/optional stubs, constructs both exposing weight vectors, verifies unique choices and the exact opposite counts, and checks coordinate widths and translations. Each simplex is kept non-singleton. Finite random fixtures test the implementation; the all-dimensional proof is the pseudoforest classification and explicit exposing weights, not the fixtures.
