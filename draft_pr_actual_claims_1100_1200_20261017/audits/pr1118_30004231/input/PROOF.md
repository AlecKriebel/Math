# Counterexamples for the printed totally mixed face poset questions

Problem 30004231 / OWR-17135-028. Complete negative resolution of both printed universal assertions, accepted by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md). No novelty claim is made.

This AI-assisted manuscript and audit are unrefereed. Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## Statement and conventions

The source is Sam Payne's problem in Joseph Doolittle's open-problem collection, Oberwolfach Report 39/2019, printed page 2464 (PDF page 70), DOI https://doi.org/10.4171/owr/2019/39, PDF https://ems.press/content/serial-article-files/46818. For two polytopes in R^n, retain exactly those faces F=F1+F2 for which both summand faces have positive dimension and dim(F)=dim(F1)+dim(F2). The two questions ask whether their inclusion poset is shellable and whether its realization has the rational homology of a wedge of (n-2)-spheres.

We use the order complex of this inclusion poset: its vertices are the qualifying faces and its simplices are nonempty strict chains. Its geometric realization is the standard realization of a finite poset. No artificial minimum or maximum is appended. The empty face never qualifies because its summands do not have positive dimension. A whole polytope is allowed as a face if it satisfies the displayed conditions; in every example below the whole sum fails the dimension equality. Thus including or excluding the improper whole face does not change any example.

A finite pure d-dimensional simplicial complex is shellable if its facets can be ordered so that each facet after the first meets the union of earlier facets in a pure (d-1)-dimensional subcomplex. For d=1 the intersection must contain at least one vertex. Hence a shellable pure graph is connected. Standard nonpure shellability imposes the same condition here because all facets have dimension one. We do not call a discrete set of several vertices nonshellable: such a zero-dimensional complex is shellable.

The counterexample to both assertions uses two full-dimensional lattice polytopes in R^5. It is therefore independent of lower-dimensional embeddings, empty realizations, negative-dimensional spheres, and the zero-sphere convention. The source does not require general position. Our two five-dimensional summands have a common segment factor and are deliberately not in relative general position. This result makes no assertion about a modified problem imposing a genericity condition.

## Main theorem

Let D=conv(0,e1,e2,e3,e4) be the standard four-simplex in R^4 and I=[0,1]. Set

P1 = D x I,     P2 = (-D) x I   in R^5.

Let T be the poset of totally mixed faces in the source's additive-dimension sense. Then its order complex is a disjoint union of two connected pure graphs. Each graph has 50 vertices and 60 edges. In particular,

H_0(|T|;Q) = Q^2,     H_1(|T|;Q) = Q^22,     H_k(|T|;Q)=0 for k>=2.

Thus T is not shellable, and |T| does not have the rational homology of a wedge of (5-2)-spheres. The latter obstruction already follows from reduced H_0(|T|;Q)=Q. A wedge of any number of positive-dimensional spheres, including the zero-fold wedge consisting of a point, is connected.

## 1 Faces of a simplex difference

We prove the necessary face classification for every m>=1. Let v0=0 and vi=ei in R^m for 1<=i<=m, and D_m=conv(v0,...,vm). Put E={0,...,m}. For disjoint nonempty subsets A,B of E define

F(A,B) = conv{vi : i in A} + conv{-vj : j in B}.

These are exactly the nonempty proper faces of D_m-D_m. Indeed, for a nonzero linear functional u let a_i=u(vi), let A be the indices of its maximum value and B those of its minimum. Since the v_i affinely span R^m, the a_i are not all equal. Hence A and B are nonempty and disjoint. The face exposed by u on the difference is exactly F(A,B), because maximizing u(x-y) requires maximizing u(x) and minimizing u(y) separately.

Conversely, for any such A,B assign values b_i=1 on A, -1 on B and 0 on the remaining indices. The linear functional with u(e_i)=b_i-b_0 realizes precisely these maximum and minimum sets. Thus every listed pair occurs. This also explains why inequalities between middle values give no additional face types.

The dimensions of the summand faces are |A|-1 and |B|-1. Their direction spaces have zero intersection. To see this, any vector in their intersection can be expressed both as sum_{i in A} alpha_i v_i and as sum_{j in B} beta_j v_j with sum alpha_i=sum beta_j=0. Subtracting gives an affine dependence among the affinely independent v_i. Disjointness of A and B forces every coefficient to vanish. Consequently

dim F(A,B) = |A|+|B|-2.

In particular all proper faces of this simplex difference satisfy dimension additivity, and F(A,B) is totally mixed exactly when |A|>=2 and |B|>=2. The whole difference has dimension m, whereas its canonical summand faces both have dimension m, so it is not totally mixed when m>=1.

The indexing and order are unambiguous:

F(A,B) subseteq F(C,D)  if and only if  A subseteq C and B subseteq D.

The forward implication can be checked by a functional w exposing F(C,D). For every i in A and j in B, the point vi-vj belongs to F(A,B). If it lies in F(C,D), then w(vi)-w(vj)=max_k w(vk)-min_k w(vk). Equality forces i in C and j in D. Because A and B are nonempty, this proves both inclusions. The reverse implication is immediate from the convex-hull formula. In particular equal faces have equal index pairs.

For completeness, the summand faces associated with any exposed Minkowski-sum face are the canonical faces exposed by the same functional. They are not independent arbitrary choices. If a decomposition by smaller faces of the summands produced the same sum, these smaller faces would be contained in the canonical faces. Equality of the sums forces equality of their support functions in every direction; the nonnegative deficits of the two support functions must both be zero. Thus each smaller face is actually the corresponding canonical face. No alternate decomposition rescues a face that fails our dimension test.

## 2 The mixed face graph in dimension four

Apply the classification with m=4 and |E|=5. The possible ordered cardinality pairs of mixed faces are (2,2), (2,3), and (3,2). Faces of type (2,2) have dimension two and are minimal; faces of the other two types have dimension three and are maximal.

There are binom(5,2) binom(3,2)=30 minimal elements. There are 2 binom(5,2)=20 maximal elements, since a maximal pair partitions E into sets of sizes two and three. Each maximal element contains exactly three minimal elements. Each minimal pair (A,B) leaves one unused index c and lies below exactly two maximal elements, namely (A,B union {c}) and (A union {c},B). There are no other comparisons and no chains of length three. The order complex K is therefore a pure graph with 50 vertices and 60 edges.

Here is a self-contained connectivity proof. Index a maximal element of type (2,3) by A^+, and an element of type (3,2) by B^-, where A and B are two-element subsets of E. The minimal element (A,B) lies between these two maximal elements precisely when A and B are disjoint. Suppressing all degree-two minimal vertices identifies K with a subdivision of the graph H having vertices A^+,A^- and edges A^+--B^- whenever A and B are disjoint.

Let G have just the two-element subsets of E as vertices, with adjacency meaning disjointness. G is connected: disjoint distinct sets are adjacent, and distinct intersecting sets have a two-element complement of their union which is adjacent to both. G has the odd cycle

01, 23, 04, 12, 34, 01,

where ij denotes {i,j}. The graph H is its bipartite double cover, so it is connected as well. Explicitly, a walk in G lifts uniquely after choosing its initial sign and flips sign at each step. Between any two underlying vertices there is a walk. If that walk has the wrong parity for the required final sign, first travel from its initial vertex to the displayed odd cycle, traverse that cycle, and return along the same path. This detour has odd length and changes the parity. Thus any two signed vertices are connected in H and hence in K.

A connected graph with 50 vertices and 60 edges has a spanning tree with 49 edges. Contracting that tree gives a wedge of 60-49=11 circles. This is also an elementary proof that its rational Betti numbers are (1,11), independently of the exact computational checks.

## 3 The shared segment factor produces two separated copies

The Minkowski sum in the theorem is

P1+P2 = (D-D) x [0,2].

Consider a supporting functional (u,t) on R^4 x R. Write A=D^u and B=(-D)^u for the canonical base faces. If t>0, the summand faces are A x {1} and B x {1}, and their sum is (A+B) x {2}. If t<0, the corresponding faces are A x {0}, B x {0}, and their sum is (A+B) x {0}. In both cases positivity and dimension additivity are exactly the base conditions.

If t=0, the summand faces are A x I and B x I. Set a=dim A and b=dim B, and c=dim(A+B). Then the sum face has dimension c+1, while the sum of summand dimensions is a+b+2. Since c<=a+b, the required equality is impossible. This excludes every face spanning the common interval direction, including cases in which one base face is a vertex. It also excludes the whole polytope.

For u=0 and t nonzero, the base faces are both full-dimensional and have dimensions four and four, but their sum has dimension four. Those two end faces also fail the dimension equality. All other qualifying faces are therefore precisely

F(A,B) x {0} and F(A,B) x {2},

where A,B are disjoint subsets of E, both of size at least two. No nonempty face at height zero is contained in a face at height two, or conversely. The mixed face poset is the disjoint union of two copies of the base mixed face poset. Its order complex is consequently K disjoint union K.

## 4 The two conclusions fail separately

Every vertex of K belongs to an edge, so K disjoint union K is pure of dimension one. Suppose it had a shelling. Consider the first edge in that ordering lying in the component that does not contain the initial edge. Its intersection with all preceding edges is empty, contrary to the required zero-dimensional shelling intersection. This argument also rules out standard nonpure shellability, which has the same nonempty-intersection requirement for a new one-dimensional facet in a pure graph.

The homology calculation follows from the two disjoint copies and Section 2: reduced beta_0=1 and beta_1=22. In particular this is not the homology of any wedge of three-spheres. Even replacing the printed sphere dimension by n-3 would not repair this example: a wedge of two-spheres is connected and has no first homology.

## 5 A smaller control for the homology assertion

For n=3 take P1=D_3 and P2=-D_3. These are full-dimensional tetrahedra. In Section 1 the index set has four elements, so mixed pairs must have cardinalities (2,2) and partition that set. There are binom(4,2)=6 such ordered pairs. All are two-dimensional parallelogram facets and none is comparable with another. The order complex is six isolated vertices, with reduced H_0=Q^5. It cannot have the rational homology of a wedge of circles, which is the printed n-2 target.

This six-point complex is shellable under the standard zero-dimensional convention. Thus the dimension-three example refutes only the homology assertion. The dimension-five example independently refutes shellability as well.

## 6 Boundaries and what is not claimed

The empty face is excluded by the positive-dimension conditions, rather than by an arbitrary decision. For n<=1 no qualifying face can have dimension at least two. In dimension two, full-dimensional summands cannot have a qualifying proper face, and their full sum also fails additivity. We do not use those empty cases or any convention for their homology as counterexamples. Lower-dimensional summands may have a qualifying full sum; that possibility is preserved by the definition and does not occur here.

The order complex is different from taking a union of original Euclidean faces or using a fan, an avoiding complex, or a Cayley complex. The proof answers the printed poset-realization question under its standard meaning. Appending an artificial maximum as a vertex of the realization would cone off every finite poset and change the question. Reversing the order does not change the chains and hence does not change the result. Restricting to facets would likewise change the question; in the five-dimensional example the totally mixed faces have dimensions two and three, not four.

The cited paper by Adiprasito, Brinkmann, Padrol, Patak, Patakova, and Sanyal, *Colorful simplicial depth, Minkowski sums, and generalized Gale transforms*, arXiv:1607.00347v1, uses a different definition requiring summand facets for its totally mixed facets. Its Theorem 1.4 and Gale dictionary are not invoked here. The published version is IMRN 2019(6), 1894-1919, DOI https://doi.org/10.1093/imrn/rnx184 (published online 19 August 2017). The arXiv version's Lemma 3.7 becomes Lemma 3.8 in the published version. The unrelated positive results in that paper retain their original scope.

Payne's earlier conference abstract, *Totally mixed faces of Minkowski sums*, https://sci-tech.ksc.kwansei.ac.jp/~hohsugi/CREST/abstract%28ver0%29.pdf, discusses positive-dimensional summand faces without stating this additive-dimension restriction in the abstract. It does not establish an alternative definition for the 2019 printed problem. We make no inference about unprinted intended hypotheses and no claim to settle generic or modified variants.

The bounded literature searches found no exact prior resolution. That is not a novelty guarantee. The proof above is elementary and self-contained; its correctness does not depend on absence of prior work.

## Exact checks

During the original proof review, exact checks enumerated normal-face types, computed dimensions over the rationals from coordinates, independently reconstructed the predicted index-pair posets, checked all inclusion relations, computed rational boundary ranks, and verified positive and negative controls. The checker used explicit exceptions rather than removable assertions and was run in normal and optimized Python modes. These historical finite checks are supplementary; the complete arguments above prove the counterexamples without any program, generated certificate, raw output or dataset. This proof-only edition distributes none of those computational artifacts. Public source identities and inspection history are recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json) and [SOURCE_REVIEW.md](SOURCE_REVIEW.md). Copied scholarly sources and their text or images are excluded.
