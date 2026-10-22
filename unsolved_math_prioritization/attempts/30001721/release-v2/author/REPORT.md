# Tree modules for roots of acyclic quivers: five-approach investigation

**Problem:** 30001721 / OWR-4800-012, queue rank 621.  
**Outcome:** `unsolved`. No proof or counterexample to the full target is claimed.  
**Date:** 2026-10-04.  
**Scope:** finite acyclic quivers, finite-dimensional representations over C, and nonzero positive roots. Parallel arrows are permitted. A tree means that the underlying undirected coefficient **multigraph** is a tree. Zero entries create no edges.

The target is existence of at least one indecomposable tree module in each root dimension, not a statement about every indecomposable in that dimension. The source also mentions a stronger multiplicity question for imaginary roots; that extra question is not silently included in this catalogue target. See SOURCES.md for provenance and checked literature.

## What this investigation establishes

1. A finite exact reformulation: every fixed dimension vector can be tested by enumerating 0–1 tree supports and testing their endomorphism algebras. The universal nonemptiness assertion remains unproved.
2. Elementary positive controls, including a real non-Schur root on the four-subspace quiver and an explicit tree module with endomorphism ring C[epsilon]/(epsilon^2).
3. Exact enumerations: 8 of 32 labelled tree supports for the 2-Kronecker dimension (2,2), 6 of 12 for D4 dimension (2;1,1,1), and 96 of 8,748 for affine D4 dimension (3;2,2,1,1) are indecomposable over C. These are labelled support counts, **not isomorphism-class counts**.
4. Concrete obstructions to replacing the problem by a Schur test, graph connectivity, thin universal-cover supports, or arbitrary degeneration to a fixed point.

These are controls and reductions, not a claim of novel resolution. In particular, all displayed positive examples lie in familiar small families.

## Approach 1: reflection descent and exceptional representations

**Mechanism attempted.** Reflect a root down to a simple root, construct a tree there, and transport the representation back.

An arbitrary simple reflection in the root lattice need not be a BGP reflection functor for the fixed orientation: BGP requires a sink or source. Its equivalences preserve the endomorphism algebra on their domains. Consequently, a chain of these equivalences starting at a simple representation cannot produce a non-Schur representation. This is a genuine restriction, not a computational inconvenience.

### An explicit real non-Schur control

Let Q have center 0 and arrows i -> 0 for i=1,2,3,4. Set

    d = (3; 2,2,1,1).

Use the following matrices, with center coordinates e1,e2,e3:

    A1 = [[1,0], [1,0], [0,1]],
    A2 = [[1,0], [0,0], [0,1]],
    A3 = [[0], [1], [1]],
    A4 = [[0], [1], [0]].

There are nine basis vertices and eight coefficient edges, and their graph is connected. Thus it is a tree. Explicitly its central backbone connects e1 to e2 through the first column of A1 and e2 to e3 through A3; all other vertices attach as leaves.

Every arrow map is injective. A center endomorphism F must preserve the four image subspaces. Preservation of the line Ce2 and the plane span(e1,e3) gives

    F(e2)=a e2, F(e1)=x e1+z e3, F(e3)=y e1+w e3.

Preservation of C(e2+e3) forces y=0 and w=a. Preservation of span(e1+e2,e3) forces x=a. Conversely each F=aI+zE31 preserves all four subspaces. The leaf endomorphisms are uniquely induced by F. Therefore

    End_Q(M) = C I + C N,  N^2=0, N != 0.

An idempotent aI+zN has a^2=a and (2a-1)z=0, hence it is 0 or I. A nontrivial direct-sum decomposition would supply another idempotent. M is indecomposable and non-Schur.

The root is real, not merely a vector with quadratic form one. In the root lattice, reflect leaves 1 and 2, then the center, then all four leaves. The successive vectors are

    (3;2,2,1,1) -> (3;1,2,1,1) -> (3;1,1,1,1)
    -> (1;1,1,1,1) -> (1;0,0,0,0).

Each step uses s_i(d)_i = sum_{j adjacent i} d_j - d_i and fixes other coordinates. The last vector is simple. At the center step the quiver obtained after the first two BGP leaf reflections has two incoming and two outgoing center arrows, so that lattice step is not an available BGP functor.

For completeness d is not a Schur root, rather than merely having one non-Schur representative. On a nonempty Zariski-open set all maps are injective, the two planes P1,P2 meet in a line L, the two one-dimensional images span a plane U, and L is not contained in U. Then V0=L direct-sum U, each P_i splits as L direct-sum (P_i intersect U), and both lines lie in U. Projection onto L preserves all four subspaces and induces a nontrivial idempotent. Thus End has dimension at least two on this open set. The endomorphism equations are linear with coefficients polynomial in the arrow matrices. If dimension one occurred anywhere, a corresponding nonzero minor would make dimension one hold on another nonempty open set, contradicting irreducibility of the full representation space. Hence End has dimension at least two everywhere.

**Outcome and exact gap.** Root-system descent and the exceptional-module theorem do not settle arbitrary real non-Schur roots. A new indecomposability-preserving tree construction, beyond the allowed BGP chain, is required. This particular small example is solved by the explicit matrices above; it is a control, not a counterexample to the target. Generalized universal-extension functors have broader domains than BGP; their scope must be checked separately, and the source literature itself records limitations (S3, Example 4.1).

## Approach 2: universal covers and thin supports

**Mechanism attempted.** Lift to the universal covering quiver and use a finite thin subtree whose pushdown has the required dimension.

Here is the elementary positive case. If a dimension vector is 0 or 1 at every vertex and its support is connected, choose a spanning tree of the support multigraph, assign 1 to those arrows and 0 to all other arrows. Any endomorphism is a scalar at each supported vertex; the chosen nonzero edges force all scalars to agree. Thus End=C and this is an indecomposable tree module.

The proposed extension to all roots fails already as a method on D4. Take three leaves into a center, dimension (2;1,1,1), and image columns e1,e2,e1+e2. The coefficient graph has five vertices and four edges and is connected. Preserving the three image lines forces a center endomorphism to be scalar. Thus this is an indecomposable tree module. But the underlying quiver is itself a tree, so every connected component of its universal cover is isomorphic to that same quiver. A thin representation in one component cannot have center dimension two. Since an indecomposable lift cannot occupy disjoint components, no cover-thin construction can realize this dimension.

**Outcome and exact gap.** The universal-cover reduction is useful, but tree-shaped base quivers can have non-thin roots. Tree-shaped Q and a tree coefficient quiver are different assertions. A covering reduction leaves the need to build suitable non-thin indecomposables; it does not make them automatically thin or exceptional. The reduction checked in S4 is independently supported by the Kac-polynomial covering formula in S5. No stronger claim about arbitrary lifts is assumed here.

## Approach 3: gluing extensions along one coefficient edge

**Mechanism attempted.** Glue smaller tree modules with one nonzero cross coefficient, obtaining a larger coefficient tree.

A precise sufficient statement is available. Suppose X,Y are Schur tree modules with Hom(X,Y)=Hom(Y,X)=0. For a nonsplit extension

    0 -> X -> E -> Y -> 0,

any endomorphism of E preserves X because Hom(X,Y)=0. It induces scalar a on X and scalar b on Y. Compatibility with the nonzero extension class e gives ae=be, hence a=b. Subtracting that scalar endomorphism leaves a map factoring through Y -> X, which is zero. Thus End(E)=C. If the extension is represented, relative to the chosen tree bases, by a single matrix-unit cross entry, its coefficient graph joins two trees with one edge and is itself a tree. This proves the proposed induction step under explicit hypotheses.

The hypotheses cannot be replaced by connectivity. On the 2-Kronecker quiver 0 => 1, dimension (2,2), take

    A = [[1,1],[1,0]],   B=0.

Its coefficient graph is connected with four vertices and three edges. However A is invertible, so this representation is isomorphic to (I2,0), which is the direct sum of two copies of the (1,1) representation (1,0). This is a decomposable tree module at a genuine root dimension.

Also, an induction that always stays Schur misses needed modules. For the same quiver,

    A=I_n, B=J_n(0)

has 2n vertices and 2n-1 edges forming a path. Its endomorphism algebra is the centralizer of a single nilpotent Jordan block, namely C[J_n] ≅ C[t]/(t^n), so it is indecomposable for every n and is non-Schur when n>1. The centralizer description follows by determining a commuting map from its value on a cyclic vector. The only idempotents of C[t]/(t^n) are 0 and 1, for instance because an idempotent or its complement lies in the nilpotent ideal (t).

**Outcome and exact gap.** One needs a decomposition for every outstanding root satisfying actual Hom/Ext and independence conditions, allowing local non-scalar endomorphism rings. Simply summing roots, selecting arbitrary nonzero extensions, or counting coefficient edges does not provide this. S4, Question 4.1, makes the recursive decomposition problem explicit.

## Approach 4: geometric degeneration, stability, and Kac counts

**Mechanism attempted.** Start from an indecomposable, specialize along a torus orbit to a sparse fixed point, and infer a tree representative; alternatively infer existence from a positive counting polynomial.

Indecomposability need not survive specialization. The family

    M_t=(I2,t J2(0))

consists of indecomposables for t!=0: its endomorphism ring is the dual-number algebra above. At t=0 it becomes (I2,0), a direct sum. This is specifically an arrow-scaling torus orbit and its limit. Sparse limits alone therefore do not prove the target.

A theta-stable representation over C is Schur. To see this, take a nonscalar endomorphism and subtract an eigenvalue so it becomes nonzero and noninvertible. Its image and kernel are both nonzero proper subrepresentations. Under the convention theta(M)=0 and theta(W)<0 for every nonzero proper subrepresentation W, additivity in the exact sequence kernel -> M -> image contradicts stability. Consequently, stable-moduli arguments alone cannot produce a representation of the non-Schur dimension from Approach 1.

The covering formula for Kac polynomials is a statement about counts of all absolutely indecomposables over finite fields. It is not an unconditional identification of those counts with tree modules. S5 states an additional exceptional-root hypothesis for an equality and separately asks a stronger tree-count lower-bound question. Invoking that missing lower bound would transfer, rather than solve, the current difficulty.

**Outcome and exact gap.** A specialization argument must exhibit a limit that remains indecomposable and has exactly N-1 coefficient edges; neither assertion follows from a torus action. A counting argument must supply a proved bridge to tree supports. Neither bridge is established here.

## Approach 5: finite support search and exact algebra certificates

### Normalization and finite reformulation

Let a tree coefficient quiver have nonzero edge weights lambda_e. Choose one basis vertex as a root and scale its basis vector arbitrarily. Proceed along the unique undirected paths: on an arrow b -> c, choose the still-undetermined scale so that lambda_e times the source scale divided by the target scale equals 1. Reverse traversal uses the inverse equation. A tree has no cycles, so no consistency obstruction occurs. Every tree module is consequently isomorphic to a representation with only 0 and 1 entries.

For fixed Q and d, let N=sum_i d_i and E=sum_{a:u->v} d_u d_v. There are E possible coefficient positions. Enumerate the subsets of N-1 positions, retain those whose coefficient multigraph is connected and cycle-free, fill their entries with 1, and test indecomposability. This enumeration is complete for tree modules of that dimension. It is deliberately redundant under general changes of basis. The one-vertex, one-dimensional case uses the empty edge set and is included conceptually; zero dimension is excluded from the target.

The outstanding universal assertion is now exact: for every positive root d, at least one of these finitely many candidates has a local endomorphism algebra. No uniform nonemptiness proof follows from the finite procedure.

### Endomorphism test

The attached script solves, over Q, all equations F_v A_a = A_a F_u. A rational nullspace basis is also a C-basis after extension of scalars. It verifies multiplication closure and builds the left-regular matrices L_b of this algebra A=End(M). It computes the exact rank of

    T(b,c)=trace(L_b L_c).

In characteristic zero, this rank equals dim(A/rad A). Indeed, trace is additive on a composition series of the left regular module; each simple factor contributes a positive integer multiple of the usual nondegenerate matrix trace pairing of the corresponding matrix block of A/rad A. The radical acts trivially on these factors. Thus the radical is precisely the kernel of T. Over C the quotient is a product of matrix algebras. Rank one is equivalent to quotient C, or A being local. A finite-dimensional representation is indecomposable exactly when its endomorphism algebra is local (equivalently, has only trivial idempotents, using Fitting's lemma and idempotent lifting). This gives an exact C-test, not merely a finite-field sample.

### Exhaustive results

- 2-Kronecker, d=(2,2): 32 tree supports. The pairs (dim End, rank T) occur as (2,1):8, (2,2):16, (4,4):8. Exactly 8 are indecomposable, all non-Schur.
- D4 with three inward leaves, d=(2;1,1,1): 12 supports. The pairs are (1,1):6 and (2,2):6. Exactly 6 are indecomposable.
- A2, d=(2,1): one tree support, pair (3,2), decomposable. This non-root is a negative control.
- Affine D4 with four inward leaves, d=(3;2,2,1,1): 8,748 supports, checked through 485 basis-permutation orbits. Exactly 96 are indecomposable, each with pair (2,1). The script stores the full histogram and a witness. Permutations only change bases within each quiver vertex and do not permute arrows or quiver vertices; all 8,748 labelled supports still contribute to the counts.

A second algebra test independently checks all 32 Kronecker supports. For each pair (A,B), the script finds an invertible P=A+tB with t in {0,1,2}, which exists because the degree-at-most-two determinant polynomial is nonzero for these tree supports. The endomorphism algebra is the centralizer of C=P^{-1}B. For a nonscalar 2-by-2 C it is local exactly when trace(C)^2-4 det(C)=0; a scalar C has full matrix centralizer and is decomposable. This discriminant test agrees with the regular-trace computation in every case. Simple and doubled one-vertex representations additionally test empty-arrow equations.

The support totals also have independent combinatorial checks. The 2-Kronecker total is 4 spanning trees of K_{2,2}, each with 2^3 arrow-color choices. The affine D4 coefficient-position graph is K_{3,6}, with 3^5*6^2=8,748 spanning trees. For D4 choose which leaf meets both center basis vertices (3 choices) and the center endpoint of each remaining leaf (2^2 choices), giving 12.

**Outcome and exact gap.** The procedure and tested cases pass, but fixed small dimensions do not prove existence for unbounded dimensions and arbitrary acyclic quivers. No finite search result is promoted to an all-roots theorem.

## Final assessment

The full target remains `unsolved` after five materially distinct approaches. The missing ingredient is a uniformly valid construction or existence argument for all remaining non-Schur roots, with an actual local endomorphism-algebra certificate for at least one tree support. The residual must not be described as only imaginary non-Schur roots without an additional theorem covering arbitrary real non-Schur roots. The displayed examples refute shortcuts, not the original conjecture.

The literature check is bounded to the primary sources listed in SOURCES.md and targeted follow-up searches, not a certification that no resolution exists anywhere. There is no full candidate proof to promote, no counterexample to the conjecture, and no reason here to mark the target `already_solved`.
