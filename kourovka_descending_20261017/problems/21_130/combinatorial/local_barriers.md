# Additive barriers to local merging and insertion

Target remains unresolved. These are proved negative checks on candidate proof mechanisms, not counterexamples to the target.

## Two-successor switches cannot preserve the color set

Let `pi` be a permutation of a set A such that the colors `a+pi(a)` are distinct. Exchange the successors of distinct vertices a,b. The replacement colors are

`u=a+pi(b), v=b+pi(a)`.

Neither u nor v equals either removed color `s=a+pi(a), t=b+pi(b)`: each proposed equality cancels either a vertex or a successor and contradicts injectivity. Thus the new color pair is disjoint from {s,t}. Consequently this switch cannot be rainbow if every available edge color already belongs to the old color set. In particular, if A=G and G is a finite odd-order abelian group, every rainbow permutation uses all |G| group elements as colors, so **every two-successor switch destroys rainbowness**. A proof that merges arbitrary rainbow cycle covers with this operation is therefore false even for the full-group case.

## Single-vertex insertion can fail everywhere

Suppose A=G\{x} and a rainbow cycle on A exists. The colors form a subset S of G of size |G|-1. Since the sum of all group elements is zero in an odd-order abelian group,

`sum(S) = 2 sum(A) = -2x`.

If c is the omitted color, then `sum(S)=-c`, so c=2x. Inserting x in an edge ab removes a+b and adds a+x,b+x. Each new color is different from the removed color, because x is distinct from a,b. Both new colors would therefore have to be omitted colors of S, yet only one color is omitted (and neither new color equals 2x). Hence **no insertion into any edge works**. This holds for every rainbow cycle on G\{x}, whenever such a cycle exists.

## Identity trades need increasing support when the smallest prime grows

Let G be finite abelian, with smallest prime divisor p of |G|. Let B={b_1,...,b_k} be a subset. Suppose a permutation pi of B has pairwise distinct sums and exactly preserves the doubled identity color set:

`{b+pi(b): b in B} = {2b: b in B}`.

If pi is not the identity, then `p <= 2^(k-1)`. In particular, no uniformly bounded support operation can move away from the identity while retaining its color set for all odd-order groups.

Proof. Choose the unique permutation sigma of the indices with

`b_i + b_pi(i) = 2 b_sigma(i)`.

Create a directed multigraph on the k indices with arcs from sigma(i) to i and to pi(i). Every vertex has indegree two and outdegree two, allowing loops. A finite balanced directed graph is a disjoint union of its strongly connected components with no arcs between them: after condensing the graph, a source component has no entering arcs and therefore cannot have any leaving arcs; remove it and iterate. Therefore the indices partition into strongly connected blocks on which both pi and sigma restrict.

If all blocks are singletons, pi is the identity. Choose a non-singleton block C of size m. The equations say that the group-valued function b on C is harmonic for its outdegree-two Laplacian L. The directed matrix-tree theorem says any principal cofactor is the positive integer tau counting oriented spanning trees directed toward the removed root. Since each nonroot vertex chooses at most one of two outgoing arcs, `1 <= tau <= 2^(m-1)`.

Subtract the value at the root from every coordinate. The reduced system is `L_root b'=0`. Multiplying by the integer adjugate gives `tau b'=0` coordinatewise. If no prime divisor of |G| divided tau, multiplication by tau would be injective on G, so every b' would be zero, contradicting distinctness in the block. Some prime divisor q of |G| therefore divides tau. Hence `p <= q <= tau <= 2^(m-1) <= 2^(k-1)`.

Only the standard directed matrix-tree identity is used; the adjugate argument applies to arbitrary finite abelian G, not merely vector spaces over a prime field. The distinctness of b_i is essential. This barrier does not exclude switches that change the used color set or whose support grows with the group.
