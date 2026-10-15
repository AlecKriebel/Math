# A one-vector augmentation with unbounded recovery distance

## Scope

The following elementary family strengthens the finite projection obstruction. It rules out any rank-independent bound on the number of Bixby–Flint–Miklós edges needed to move an arbitrary augmented trajectory back to one realized on the old coordinates. The lower bound holds in both the successful-word graph and its exact-trajectory quotient, with the distinction proved explicitly.

This is not a counterexample to the original pressing-connectivity conjecture. The original graph has exactly one successful word, and the augmented successful-word graph is connected even at the stronger LCS≥r−1 threshold. A genuinely nonlocal component-preservation or path-rerouting theorem is not ruled out.

Throughout let r≥2. An edge means LCS≥r−4 unless a different threshold is explicitly stated.

## 1. A thin original coordinate configuration

Let V=F₂^r with its standard dot product and ordered orthonormal basis e_0,…,e_{r−1}. Take the original coordinate vectors

x_0=e_0,
x_i=e_{i−1}+e_i  for 1≤i≤r−1.

Their coefficient matrix is unit lower triangular, so they form a basis. Their Gram matrix A is the path on vertices 0,1,…,r−1 with exactly the endpoint 0 black: A_00=1; A_ii=0 for i>0; A_i,i+1=A_i+1,i=1; all other entries are zero. In particular rank(A)=r.

At any stage of pressing this path, its unpressed suffix remains a path with just its left endpoint black. Pressing that endpoint clears its row and column and toggles the next endpoint to black. It is the only legal move. Thus A has exactly one successful word,

S=(0,1,…,r−1).

Its Gram–Schmidt basis is (e_0,e_1,…,e_{r−1}).

## 2. Adjoin one norm-one vector

Adjoin the single new coordinate

y=e_{r−1}=x_0+x_1+⋯+x_{r−1},

and label it r. It has norm one, and its only nonzero inner product with an old coordinate is B(y,x_{r−1})=1. Consequently the augmented Gram matrix is the path on 0,1,…,r with both endpoints 0 and r black and all internal vertices white. Its rank remains r because its coordinate span remains V.

For a remaining interval containing at least three vertices, exactly the two endpoints are black. Pressing either endpoint clears it and leaves a shorter interval with its two endpoints black. When two adjacent vertices remain, their matrix is [[1,1],[1,1]], and pressing either clears both simultaneously.

Every augmented successful word therefore has r−1 endpoint removals followed by one final press at either of the remaining two vertices. Conversely, every such choice sequence is successful. There are exactly 2^r successful words and 2^{r−1} exact trajectories. Each trajectory fiber has two words, differing only in the final letter. Before that last step the two possible endpoint columns are distinct whenever the remaining interval has at least three vertices, so no additional words have the same full matrix trajectory.

## 3. Unbounded overlap deficit from one artificial trajectory

Always choose the right endpoint until the final two-vertex interval {0,1}. The resulting exact trajectory has fiber

F_rev = {
(r,r−1,…,2,1),
(r,r−1,…,2,0)
}.

Both words are strictly decreasing, whereas S is strictly increasing. Each has at least one old label because r≥2. Thus

max_{w∈F_rev} LCS(w,S)=1.

Equivalently, the best deletion/insertion deficit from the whole fiber to the old-word set is r−1. In particular, for r≥6 this augmented trajectory has no BFM edge to any trajectory realized by the original coordinate set. More generally, no fixed deficit bound can support nearest-original projection for all ranks, even when only one norm-one vector was adjoined.

The orthonormal basis of this trajectory is (e_{r−1},e_{r−2},…,e_0), and its coordinate layers are

({r},{r−1},…,{2},{0,1}).

This also checks the complete fiber directly using the highest-support characterization.

## 4. Exact successful-word recovery distance

For length-r words define d(U,W)=r−LCS(U,W). This is half their insertion/deletion distance and hence satisfies the triangle inequality. Every BFM edge has d≤4. Since every w in F_rev has d(w,S)=r−1, every successful-word path from this fiber to S has at least

ceil((r−1)/4)

edges.

This bound is attained. For 0≤k≤r−1 define

W_k=(0,1,…,k−1, r,r−1,…,k+1).

The ascending portion is empty when k=0. This word first presses k left endpoints, then presses right endpoints, and is successful; it omits the old label k. For k<l, W_k and W_l share the subsequence

(0,1,…,k−1, r,r−1,…,l+1),

of length r−(l−k). Thus increments l−k≤4 give BFM edges. Choose k=0,4,8,… while k<r−1, and finish with S when the remaining increase to r−1 is at most four. If the last preterminal index is k≤r−2, W_k and S share (0,1,…,k−1,k+1), of length k+1, giving deficit r−k−1≤4. For r≤5 the direct edge already suffices.

Therefore the minimum successful-word graph distance from F_rev to the old-word set {S} is exactly

ceil((r−1)/4).

The triangle-inequality argument above counts every edge, including any changes made inside a trajectory fiber. It does not silently treat fiber movement as free.

## 5. Exact trajectory-quotient recovery distance

Here a separate argument is needed because movement inside a fiber is free in the quotient.

For any augmented trajectory F, let p(F) be the number of left-endpoint removals among its first r−1 presses. This is well-defined because those first r−1 letters are fixed throughout its two-word fiber. If p(F)=a, the two vertices remaining just before the final press are {a,a+1}. Every word in F has:

- old labels 0,…,a−1 in increasing order;
- labels a+2,…,r in decreasing order;
- a final letter chosen from {a,a+1}.

The two lists in the first two bullets may be interleaved arbitrarily.

Let F and G have p(F)=a<b=p(G), and set δ=b−a. Consider only labels in the interval of integers I={a,a+1,…,b+1}. A word from F contains exactly δ+1 such labels: a+2,…,b+1, followed eventually by its final letter a or a+1. Their relative order is strictly decreasing. A word from G also contains exactly δ+1 such labels: a,…,b−1, followed eventually by its final letter b or b+1. Their relative order is strictly increasing.

Hence any common subsequence of any F-word and any G-word contains at most one label from I. Since an F-word has δ+1 letters from I, at least δ of its letters must be deleted. Therefore

max_{U∈F,W∈G} LCS(U,W) ≤ r−|p(F)−p(G)|.

In particular every quotient BFM edge changes p by at most four. The reverse trajectory has p=0. The unique trajectory realized by the old coordinate set, when extended to the full augmented matrix, has p=r−1; its augmented fiber consists of S and (0,1,…,r−2,r). Thus the quotient distance from F_rev to the old-realized-trajectory subgraph is at least ceil((r−1)/4).

For the trajectories C_k of the canonical words W_k from Section 4, p(C_k)=k. The displayed common subsequence has length r−|k−l|, so the preceding upper bound is attained:

max_{U∈C_k,W∈C_l} LCS(U,W)=r−|k−l|.

The canonical sweep path therefore attains the lower bound in the quotient as well. Its exact trajectory-quotient recovery distance is

ceil((r−1)/4).

Consequently free choices of the final representative do not erase the unbounded-distance obstruction.

## 6. The augmented graph remains connected

Every successful word has a fixed number p of left removals among the first r−1 steps. Two consecutive removals from opposite endpoints commute while preserving the exact state after both steps. At the first r−1 positions such a pair starts with an interval of at least four vertices, so both orders simply remove the two distinct endpoints and leave the same smaller interval. Swapping the two letters is an LCS≥r−1 move.

Using these swaps puts all p left removals before all right removals. Then a one-letter replacement in the final two-vertex fiber yields W_p. Consecutive canonical words W_p and W_{p+1} have LCS at least r−1, and W_{r−1} differs from S only in its final letter. Hence the whole augmented successful-word graph is connected using only moves with LCS≥r−1.

This is consistent with its unbounded distance to the single old word under the coarser four-deficit adjacency: connected graphs can have unbounded diameter as rank grows.

## 7. Consequence for the proof attempt

Neither nearest-neighbor projection nor a uniformly bounded number of intermediate augmented edges can recover arbitrary augmented words or trajectories on the original coordinates. The failure persists when the augmentation consists of a single norm-one vector, both configurations are paths, all fibers have only two words, and the original successful word is unique.

A nonlocal retraction, a component-preservation theorem for adjoining one vector, or an original-coordinate invariant could still prove the general conjecture. This note establishes none of those. The original connectivity question remains open in this work.

The argument is self-contained and does not rely on computations or outside source text. A separate finite verifier checks the formulas on small ranks; it is a cross-check, not a proof prerequisite. No novelty claim is made.
