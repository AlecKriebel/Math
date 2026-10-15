# Exact trajectory-edge criterion and a coordinate-rich connectivity theorem

These are independently authored supplementary results. They make no novelty claim. These results do not resolve the general Bixby–Flint–Miklós conjecture. The hypotheses below are essential to the proofs given; no arbitrary coordinate-set lifting is asserted.

Use the notation and proved trajectory-fiber description from STRUCTURAL_LEMMAS.md: A is symmetric over F_2, of rank r, has a successful word, and its radical quotient V has the induced nondegenerate bilinear form B. Each exact pressing trajectory F has a partition (L_1(F),...,L_r(F)) of the nonzero original vertices, and its successful words are exactly the Cartesian product of these layers.

## 1. Exact edge criterion between trajectory fibers

For two trajectories F,G, put a marked cell at (i,j) when

L_i(F) intersect L_j(G) is nonempty.

Let h(F,G) be the greatest number of marked cells with strictly increasing first coordinates and strictly increasing second coordinates.

**Proposition.** The maximum LCS(S,T) over all successful words S in the fiber of F and T in the fiber of G equals h(F,G). Consequently, for distinct trajectories F and G, their fibers have a four-deletion/four-insertion edge between them if and only if h(F,G)≥r−4. The max-LCS identity also holds when F=G; an edge of the simple quotient graph refers to distinct trajectories.

**Proof.** Every common subsequence specifies its positions i_1<...<i_k in S and j_1<...<j_k in T. Its common letters witness the marked cells (i_a,j_a), giving the upper bound. Conversely, choose a vertex v_a in each marked intersection along an increasing chain. These vertices are distinct because their first-layer indices are distinct. Specify the corresponding entries in S and T to be these vertices. Fill every other position arbitrarily from its nonempty layer. The Cartesian-fiber theorem guarantees that both complete words are successful; the chosen vertices form a common subsequence. QED.

This is a genuine exact lifting statement: the independent choices inside a fiber were proved by equality of full pressing states. It does not use an exchange axiom for unordered feasible sets.

## 2. An elementary generation lemma for orthonormal bases

In a standard orthonormal basis e_1,...,e_r, there are two allowed transformations:

- Swap two basis positions.
- Choose four distinct positions I, and replace each vector b_i for i in I by the sum of the other three vectors in that four-tuple; leave all other basis vectors unchanged.

The four-position transformation preserves orthonormality. Each new vector has norm 3=1 in F_2, and two distinct new vectors have inner product 2=0. It is an involution; its matrix on the four positions is I_4+J_4.

**Lemma.** Every two ordered orthonormal bases of a nondegenerate standard dot-product space over F_2 are connected by a finite sequence of these transformations.

**Proof.** It suffices to show that permutation matrices and four-position matrices generate all matrices Q satisfying Q^TQ=I. We reduce an arbitrary Q to I by left multiplication with these generators.

In a residual dimension m>1, the first column v has odd weight. It cannot be the all-ones vector w: for every other column u, orthogonality would give B(u,w)=0, whereas B(u,w)=B(u,u)=1. (If m is even, w already has norm zero, also excluding it.) Thus, when v has weight at least three, choose three coordinates where v has entry 1 and one coordinate where it has entry 0. Let z be the indicator vector of those four coordinates. Left multiplication by I+zz^T is precisely the four-position transformation and sends

v to v+B(v,z)z=v+z.

It removes three ones and adds one one, reducing the weight by two. Repeat until v has weight one, and use a coordinate transposition to make v=e_1. Orthogonality then forces every other column to have first coordinate zero, so Q has block form diag(1,Q') with Q' orthogonal. Induct on the remaining dimension, using generators supported entirely in that block. Dimension one is immediate; in dimensions two and three the odd-weight/non-all-ones argument already forces the first column to have weight one. This constructs a finite generator expression for Q. Since all generators are involutions, the same generating set acts transitively by right multiplication on ordered orthonormal bases, with each right multiplication changing just the indicated basis positions. QED.

The proof deliberately distinguishes left multiplication in matrix reduction from right multiplication on an ordered basis. The latter is what bounds the number of changed word positions.

## 3. Connectivity when every norm-one quotient vector is a vertex

**Theorem.** Suppose that A has a successful word and that for every y in V with B(y,y)=1, some original coordinate vertex v satisfies x_v=y, where x_v is the image of its coordinate vector in V. Then the successful-word graph with adjacency LCS≥r−4 is connected, for every rank r and ambient vertex count n.

**Proof.** For each norm-one vector y, fix a representing vertex rho(y). Different vectors necessarily have different representatives.

Take a successful word S with induced ordered orthonormal basis f_1,...,f_r. The representative rho(f_j) lies in layer L_j of S's trajectory: its coordinates in that orthonormal basis have a unique 1, in position j. The Cartesian-fiber theorem therefore connects S to the successful word

(rho(f_1),...,rho(f_r))

by single-position replacements, each changing at most one letter. Do the same for any target successful word T, obtaining representatives of its ordered orthonormal basis g_1,...,g_r.

Apply the preceding generation lemma to connect the two ordered orthonormal bases. At every stage all basis vectors have norm one, so all their fixed representatives are actual original vertices. An ordered orthonormal list of these representatives is a successful word: the vectors are independent, have Gram matrix I, and span all of V, so its legal presses exhaust the rank and leave the full original matrix zero. A swap changes at most two word positions, and a four-position move changes at most four. Keeping all unaffected positions gives a common subsequence of length at least r−4. Every intermediate word therefore belongs to the original successful-word graph, and every step is an allowed edge. Concatenating the initial fiber path, the basis path, and the reversed final fiber path connects S to T. QED.

For r=0 there is only the empty word and the conclusion is immediate. The representation hypothesis is independent of the number or types of any additional coordinate vertices: they may be zero, repeated, or of norm zero, and are handled by the same full-state argument.

## 4. Scope of the missing step

The representation hypothesis in Section 3 is much stronger than successful pressability and is not assumed in the original conjecture. Without it, a generated intermediate norm-one vector need not be an original vertex. Furthermore, a change of orthonormal basis can destroy the property that its prefix flag has coordinate representatives. One cannot project the saturated-basis path back to the original coordinate set by an unproved matroid or congruence argument.

Even when two proposed trajectories are both realized, their actual coordinate-word bridge must meet the marked-cell criterion in Section 1. This describes exactly the further condition required, rather than presuming it.

## Source dependence

The proofs above use only the elementary full-state/fiber lemmas established in the companion note. No external group-generation theorem is invoked. All vectors and transformations are over F_2.
