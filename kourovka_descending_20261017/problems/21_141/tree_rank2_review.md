# Adversarial review: rank-two path obstruction

Checkpoint: **2026-10-17 21:16:51 UTC**. Review scope: the proposed path-of-groups construction and its precise consequences only; no other approach family was consulted. Completion estimate: **100% for validating the finite-family obstruction stated below**. This is not a completion estimate for Kourovka 21.141, which remains unanswered by this construction. No external communication or Git operation was performed by this reviewer.

## Verdict and exact claim

The proposed construction is correct for every prime `p` and every integer `n >= 1`. It gives a proper reduced finite tree of pro-p groups with `n` edges, all vertex and edge groups isomorphic to `Z_p^2`, and fundamental pro-p group of minimal generator number exactly two. Consequently **there is no finite universal bound for the number of edges in arbitrary proper reduced decompositions depending only on `d(P)` and the maximum of `d(E)` over edge groups**, or even depending on `d(P)` and the fixed edge isomorphism type `H = Z_p^2`.

There is one important hidden hypothesis to watch: the original standard tree action is not faithful. Its kernel is exactly the central subgroup `C = <x^(p^n), y^(p^n)> ~= Z_p^2`. A modification described below repairs faithfulness while retaining fixed edge type and fixed generator number three. Neither family proves inaccessibility of one fixed group, establishes a failure of coherence, or answers 21.141.

The conventions used here agree with Castellano–Zalesskii, *A pro-p version of Sela's accessibility and Poincare duality pro-p groups*, §2.11, Definitions 2.12 and 2.17: properness means vertex embeddings into the fundamental group, and reducedness excludes a surjective boundary map at a nonloop edge. Their §2.2 also imposes a faithful-action convention; that extra condition must be distinguished from properness and reducedness. [Primary source](https://ems.press/content/serial-article-files/48579?nt=1).

## Construction with all maps explicit

Let the underlying finite graph be the path `v_0 -- ... -- v_n`. Put

```
A_i = <a_i,b_i | [a_i,b_i]=1>_pro-p ~= Z_p^2,
E_i = <c_i,d_i | [c_i,d_i]=1>_pro-p ~= Z_p^2,  0 <= i < n.
```

The boundary maps for edge `E_i` are

```
                to A_i             to A_(i+1)
c_i             a_i^p              a_(i+1)
d_i             b_i                b_(i+1)^p.
```

They are continuous injective homomorphisms. Relative to the displayed bases their matrices are `diag(p,1)` and `diag(1,p)`, respectively. Each image has index exactly `p`. In particular neither boundary map is surjective, including the two end edges and the case `n=1`; the graph is reduced under the stated definition.

Because the underlying graph is a tree, its fundamental pro-p group has presentation

```
P_n = <a_i,b_i (0<=i<=n) |
       [a_i,b_i]=1 (0<=i<=n),
       a_i^p=a_(i+1), b_i=b_(i+1)^p (0<=i<n)>_pro-p.
```

All normal closures and generation in this note are topological. The commutativity relations make the maps from a whole `Z_p^2` edge well-defined; matching its two generators matches every edge element by continuity.

## Properness: no circular use of injectivity

Define continuous maps from the vertex groups to the additive group `Z_p^2` by

```
a_i |-> (p^i,0),           b_i |-> (0,p^(n-i)).
```

Both boundary images of `c_i` map to `(p^(i+1),0)`, and both boundary images of `d_i` map to `(0,p^(n-i))`. Thus the universal property supplies a homomorphism

```
phi : P_n -> Z_p^2.
```

Its restriction along the canonical vertex map `A_i -> P_n` is the injective `Z_p`-linear map `diag(p^i,p^(n-i))`. If a vertex element dies in `P_n`, it therefore dies under this injective composite, so it was already trivial. Compactness and the Hausdorff property turn these continuous injections into topological embeddings. This proves properness directly; it does not assume normal forms or injectivity of the pro-p amalgams in advance. Edge embeddings then follow by composition.

The map `phi` is onto, since `phi(a_0)=(1,0)` and `phi(b_n)=(0,1)`.

## Presentation and minimal generator number

Set `x=a_0` and `y=b_n`. The edge relations yield exactly

```
a_i = x^(p^i),             b_i = y^(p^(n-i)).
```

Eliminating the other generators therefore gives

```
P_n = <x,y | [x^(p^i), y^(p^(n-i))]=1,  0<=i<=n>_pro-p.
```

This can also be checked without a Tietze-transformation convention: in the two-generator presented group the displayed powers give compatible homomorphisms from all `A_i`, and the universal-property maps in both directions fix the displayed generators. They are inverse continuous homomorphisms.

Hence `d(P_n)<=2`. The surjection `phi` onto `Z_p^2` gives `d(P_n)>=2`, so `d(P_n)=2`. Equivalently, all defining relators are commutators, so the abelianization is exactly `Z_p^2`. No assertion that `P_n` itself is abelian is being made. For example, mapping `x,y` to the two factors of `C_p coproduct C_p` gives a nonabelian quotient for every `n>=1`.

## Exact action kernel and the finite quotient variant

Inside every vertex group the elements

```
x^(p^n) = a_i^(p^(n-i)),   y^(p^n) = b_i^(p^i)
```

are present. Each commutes with every vertex group, and vertex groups generate `P_n`. Thus

```
C = <x^(p^n),y^(p^n)>
```

is central and isomorphic to `Z_p^2` by properness. It is also contained in every edge group, because `i+1<=n` and `n-i<=n`.

The intersection of the finitely many chosen vertex groups is exactly `C`. Indeed,

```
intersection_i phi(A_i)
  = intersection_i (p^i Z_p x p^(n-i) Z_p)
  = p^n Z_p x p^n Z_p
  = phi(C).
```

If an element belongs to every `A_i`, choose the element of `C` with its `phi`-image. Both are in `A_0`, where `phi` is injective; they are equal. This argument does not require an intersection or fixed-set theorem for arbitrary pro-p subtrees.

Let `K` be the kernel of the standard tree action. It lies in every chosen vertex stabilizer, hence `K<=C`. Conversely, a central subgroup contained in every vertex and edge stabilizer fixes every vertex and edge coset; therefore `C<=K`. Thus **`K=C` exactly**.

Quotienting by `C` gives a faithful proper reduced graph of finite p-groups of the same length. More explicitly,

```
A_i/C ~= C_(p^(n-i)) x C_(p^i),
E_i/C ~= C_(p^(n-i-1)) x C_(p^i),
```

where a cyclic factor of order `p^0` is trivial. The quotient boundary indices remain `p`. Properness can again be seen from the map to `(Z/p^n)^2`, which is injective on every displayed quotient vertex. The quotient group is two-generated and maps onto `(Z/p^n)^2`, so its minimal generator number is two. Its edge groups have generator number at most two but do not have a fixed isomorphism type as `n` varies. At `n=1` the single edge group becomes trivial; the two vertex groups are `C_p`.

## Faithful modification retaining fixed edge type

Replace only `A_0` by

```
A'_0 = A_0 coproduct <z> ~= Z_p^2 coproduct Z_p,
```

and use the original map `E_0 -> A_0 -> A'_0`; keep the rest of the path unchanged. Denote the fundamental group by `Q_n`. The universal property gives

```
Q_n ~= P_n coproduct Z_p.
```

In particular `Q_n` has presentation obtained from the preceding presentation of `P_n` by adjoining `z` without any additional relators. Thus `d(Q_n)=3`: its displayed generators give the upper bound and its abelianization `Z_p^3` gives the lower bound.

All modified vertex maps are embeddings. One way to verify the only additional point, the embedding of `A'_0`, is first to attach a separate `Z_p` vertex to `A_0` using a trivial edge. This enlarged graph is proper: the fundamental group is `P_n coproduct Z_p`, both free factors embed by the canonical retractions, and the old vertices embed through `P_n`. Its connected two-vertex subgraph has group `A_0 coproduct Z_p`, which embeds by the proper finite-subgraph lemma. Collapsing this connected subgraph gives the desired modified graph. The precise local references are Castellano–Zalesskii Lemma 2.15 and Remark 2.19; alternatively their Corollary 3.4 applied to the free product with trivial amalgam gives the same embedding. [Primary source](https://ems.press/content/serial-article-files/48579?nt=1).

Reducedness persists. The image of `E_0` is a proper subgroup already of `A_0`, and remains proper in `A'_0`; every other boundary image still has index `p`. Each edge group is still exactly `Z_p^2` in isomorphism type. Vertex generator numbers are uniformly at most three.

The modified action is faithful. If `N` is its action kernel, then `N` is normal in `Q_n` and `N<=E_0<=P_n`. Consequently

```
N <= P_n intersection z P_n z^(-1) = 1.
```

The last intersection needs only the elementary free-product case, not a general subgroup-decomposition theorem: in the standard tree for `P_n coproduct <z>`, the vertices `P_n` and `zP_n` are joined by the explicit two-edge path through `<z>`. The edge stabilizers are trivial. An element in the displayed intersection fixes the two endpoints, hence their unique finite path, and therefore a trivial-stabilizer edge. This proves the intersection is trivial. Uniqueness of a finite path follows from absence of finite circuits in a pro-p tree.

Therefore the faithful modification disproves a universal edge bound depending only on `d(Q_n)=3` and edge generator number two, **even when all edge groups have fixed isomorphism type `Z_p^2`**. It also disproves such a bound if a uniform bound of three on vertex generator numbers is added. This strengthened family is a nontrivial free pro-p product; it does not address a theorem that additionally restricts ambient groups to be freely indecomposable.

## Optional relation-rank check: the original groups really vary

Redundancy or repeated isomorphism types would not invalidate the edge-bound obstruction. Nevertheless, the continuous cohomological Mayer–Vietoris sequence proves

```
dim_Fp H^2(P_n,F_p) = n+1.
```

Here is the complete low-degree calculation. A vertex `H^1(A_i,F_p)` has coordinates `(alpha_i,beta_i)`. The difference of restrictions to edge `E_i` has coordinates

```
(-alpha_(i+1), beta_i),
```

up to an irrelevant overall sign convention. The map from the direct sum of vertex `H^1` to the direct sum of edge `H^1` is therefore surjective. Both boundary restrictions `H^2(A_i,F_p)->H^2(E_i,F_p)` vanish: `H^*(Z_p^2,F_p)` is exterior on the two degree-one generators, and either boundary matrix has determinant divisible by `p`. Exactness of

```
direct_sum_vertices H^1 -> direct_sum_edges H^1 -> H^2(P_n)
   -> direct_sum_vertices H^2 -> direct_sum_edges H^2
```

therefore identifies `H^2(P_n,F_p)` with the direct sum of the `n+1` one-dimensional vertex `H^2` spaces. The Mayer–Vietoris input for proper pro-p amalgams is given in Gareth Wilkes, *Relative cohomology theory for profinite groups*, §4.3, Theorem 4.6, with the empty relative families; iterating along this finite proper tree gives the displayed sequence. [Primary source](https://api.repository.cam.ac.uk/server/api/core/bitstreams/85a7dfb3-ae1a-4f65-b9cf-a088742b052d/content).

In particular the `P_n` are pairwise nonisomorphic. By the usual minimal pro-p presentation interpretation of `H^2`, the displayed `n+1` relators are a minimal relator set; this latter interpretation is not needed for any graph-size conclusion. The same `H^2` dimensions persist after freely adjoining `z`.

## Exact limits and remaining research gap

- The quantified counterexample concerns a family of varying ambient groups with reduced decompositions of unbounded size. It does not exhibit one fixed finitely generated group with unbounded reduced decomposition sizes, nor an infinite strictly refining sequence of splittings of one group.
- The central-kernel caveat affects the two-generator fixed-edge-type construction; the three-generator modification repairs that caveat, subject to the explicit extra free decomposition just recorded.
- None of these actions is shown to satisfy a uniform acylindricity condition. No contradiction with acylindrical accessibility is claimed.
- Every displayed `P_n` and `Q_n` is finitely presented. No finitely generated, infinitely related subgroup has been constructed, and no coherent factors of one fixed polycyclic amalgam with an incoherent result have been exhibited.
- No embedding of the entire family into one fixed amalgam, nor realization as all the induced decompositions of subgroups of that fixed amalgam, is proved. Additional structure from a fixed ambient amalgam might rule out this path pattern.
- The comparison with procyclic-edge results must be made against each theorem's actual hypotheses. The verified point here is that replacing “procyclic” by “two-generated abelian” in an otherwise unrestricted universal graph-size bound cannot work. No blanket theorem about every rank-one setting was assumed or independently certified in this review.

The strongest verified result of this review is the faithful three-generator, fixed-`Z_p^2`-edge-type obstruction. The remaining central gap for Kourovka 21.141 is to connect subgroup actions in one fixed amalgam to finite presentation, or produce a verified counterexample to coherence. This obstruction alone supplies neither mechanism.
