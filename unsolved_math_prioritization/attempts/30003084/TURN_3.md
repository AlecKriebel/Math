# Author turn3: ordinary complex conics for at most ten points

**Partial theorem, awaiting final independent review with the full attempt.** Every set of at most ten distinct complex projective points not on a conic has an ordinary conic in the exact source sense. This extends TURN_2, but is not a general-cardinality result or a novelty claim. The rank4 lemma below is proved in full, with finite algebra/graph controls supplied separately.

Let V be the rank6 quadratic evaluation matrix of ten distinct points not on a conic, and G a rank4 Gale matrix. Assume no ordinary conic, so G has no5-element circuit by the rank formula in TURN_2. The original evaluation matroid has no circuit of size<=3. We prove a contradiction.

## Rank4 configuration lemma, including multiplicities and zeros

Over C, a spanning rank4 vector configuration with no5-element circuit is either a direct sum of at least2 nonzero spanning components, or all its nonzero projective directions lie on3 concurrent lines whose private directions are independent modulo their common point. Zero columns can be retained separately throughout.

Choose4 basis columns e1,e2,e3,e4 and use their projective representatives as coordinates. Invertible row operations and nonzero rescaling of column representatives preserve circuit supports and all the geometric containment statements used below. Every other column has support size<=3; a full4-support column together with the basis would be a5-circuit.

First suppose a3-support column exists. Rescale basis coordinates and its representative to take a=e1+e2+e3. A column q outside this coordinate3-space has nonzero fourth coordinate. Relative to each alternative basis {a,e_j,e_k,e4} (omit e_i), absence of a5-circuit says that whenever q_i!=0, at least one of the other two q_j equals q_i. Together with absence of4-support this forces q either to be parallel to e4 or to have the form e_i+e_j+t e4, with distinct i,j in{1,2,3} and t!=0, up to scalar.

If every outside column is parallel to e4, the configuration splits as the3-space and that line. Otherwise rename indices to take q=e1+e2+t e4. No outside column q'=e1+e3+u e4 is possible (nor the analogous other pair). If u!=t, the columns {q,q',e1,e2,e3} have rank4 and the unique relation

u q - t q' + (t-u)e1 - u e2 + t e3=0

has all coefficients nonzero, giving a5-circuit. If u=t, the columns {a,q,q',e1,e4} have rank4 and relation

a-q-q'+e1+2t e4=0,

again a5-circuit in characteristic0. Thus every outside direction lies in span(e1+e2,e4).

Apply the same3-support argument using q and the coordinate3-space span(e1,e2,e4) to a column p in the original plane with p3!=0. It gives p parallel to e3 or p1=p2. Hence every column lies in one of

span(e1,e2), span(e1+e2,e3), span(e1+e2,e4).

These are the required3 concurrent projective lines, with common direction e1+e2 and3 independent private directions.

Second, suppose every nonbasis column has support<=2. Form the graph on4 basis indices whose edges are the2-support columns. A disconnected graph gives a direct-sum decomposition of the vector configuration. A simple3-edge path on4 vertices would, together with the2 endpoint basis vectors, give a5-circuit: the3 edge vectors and endpoint basis vectors have a unique relation with all coefficients nonzero, obtained successively along the path. A connected graph on4 vertices with no such path is a star. Its columns therefore lie in3 lines through the central basis direction, again with independent private directions. This proves the lemma.

## Why neither case can occur for ten quadratic evaluations

In the concurrent-line case, let A_i consist of indices on the i-th line away from the common direction. Columns at the common direction and zero columns are not in these sets. The other2 geometric lines span a3-dimensional vector hyperplane. Choose a nonzero linear functional vanishing on this hyperplane. Its values on the columns of G give a relation among the original V columns, supported exactly on A_i: on the i-th line the functional vanishes only at the common direction. Each A_i is nonempty, since otherwise the full Gale configuration would have rank at most3. Thus each support carries a nonzero original dependency and has size at least4, because any3 distinct quadratic evaluations are independent. The3 sets are disjoint, giving at least12 original points, impossible for n=10. No unnecessary assumption that the other two sets of actual columns span the entire geometric hyperplane is needed.

In the decomposable case, split all nonzero Gale columns into indecomposable direct-sum components of ranks r_j>0 and sizes n_j. Zero Gale columns give c free original columns. The original relation space is the row space of G. In row coordinates adapted to its direct-sum components, that relation space is itself the direct sum of r_j-dimensional spaces supported on the respective index blocks. A relation among columns from different blocks therefore splits into relations internal to each block; their column spans form a direct sum. Thus the original columns split into pieces of dimensions m_j=n_j-r_j, together with c free columns. Each component has an original dependency because r_j>0; if m_j<=2, it has a circuit of size<=m_j+1<=3, impossible. Thus every m_j>=3. Since the total original rank is6, there can only be2 nonzero Gale components, each m_j=3, and c=0. Each has at least4 original points, all collinear by TURN_2's quadratic-rank3 criterion. Their union lies on2 lines, a conic, contradiction.

It follows that every ten-point set satisfying the source hypotheses has an ordinary conic. Together with TURN_2, this extends the affirmative partial theorem to all |P|<=10. It does not classify rank5 Gale configurations for eleven points or prove the general theorem.

## Exact checks, scope and continuation

`verify_gale_controls.py` checks the two explicit five-circuit relations and all their four-column determinants, the endpoint circuit for weighted graph paths, the elementary graph classification, the three-branch annihilator supports, and the Gale rank identity on small exact rational evaluation matrices. It also checks the quadratic interpolation facts in finite models. These controls corroborate the algebra and conventions; the universal rank4 proof is the argument above.

The proof requires characteristic different from2 in the displayed five-circuit obstruction; the actual target is C. It handles zero and proportional Gale columns explicitly. The ordinary conic it produces may be reducible, and its five-point evaluation rank is exactly5. No open-set or generic-position assumption on P is used.

Three substantive author turns complete. Original arbitrary-cardinality target remains unresolved. Completion estimate35%. The next route should exploit the general connection between reducible ordinary conics and pairs of3-point lines, together with the larger Gale-rank obstruction, rather than assume the rank4 classification continues unchanged. Two substantive turns remain unless a full result appears earlier.
