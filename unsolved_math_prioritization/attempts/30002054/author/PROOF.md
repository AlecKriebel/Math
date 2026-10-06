# Exact puncture normalization and the remaining additivity gap

## 1. Object, category, and status

Put n=d-1 ≥ 3. A triangulation here is a finite abstract simplicial complex:
a face is a set of vertices, and two faces cannot be distinct with the same
vertex set. Work with compact connected triangulable topological manifolds.
Punctures are standard locally flat open n-balls with pairwise disjoint closures.
The same arguments hold in the PL category with PL triangulations, standard
PL balls, and PL gluings, if every minimum is taken in that category consistently.

For a triangulation Delta of a manifold with nonempty boundary, write v=f0,
e=f1, and i for the number of interior vertices, and define

    gamma(Delta) = e - n v + binom(n+1,2) - i.
    Gamma(M) = min gamma(Delta).

This is the h2-minus-interior-vertices invariant in the question, not minimum
vertices, minimum facets, Matveev complexity, or a minimum over face-pairing
pseudotriangulations. For a closed triangulation K put

    g2(K) = f1(K) - (n+1)f0(K) + binom(n+2,2),
    G(N) = min g2(K), |K| homeomorphic to N.

We use the standard manifold lower bound g2(K) ≥ 0. More precisely, Novik–Swartz
[S5, Theorem 5.2] proves g2(K) ≥ binom(n+2,2) beta1(K;k) for connected,
k-orientable homology n-manifolds without boundary, n ≥ 3. An infinite field of
characteristic two makes this applicable to every closed triangulated manifold
used here. This also ensures that G(N) is an attained integer minimum.

Source reconciliation is essential. Swartz's 2012 report [S1, pp. 1427–1429]
uses a simplicial-complex subscript in the minimum; its final question follows
a discussion of closed manifolds. Its displayed puncture B^d must be read with
the ambient dimension n=d-1. The 2011 report [S2, pp. 411–412] explicitly asks
the boundary-sum question and records the +4 puncture normalization in dimension
three. Lutz–Sulanke–Swartz [S3, Conjecture 11] states the closed three-dimensional
conjecture. The literal boundary/interior-sum extension is therefore not an
adequate interpretation of the intended open problem.

## 2. Separate caps: an exact identity

Suppose Delta triangulates N_b, obtained from a closed connected n-manifold N
by removing b ≥ 1 standard balls. Its boundary has b components, each an
(n-1)-sphere. Attach a cone on each component, using b distinct new vertices.
The resulting complex K is simplicial and triangulates N: each cone is a
topological n-ball, and the boundary collars give a manifold after gluing.
In the PL version the same statement holds for PL sphere boundaries.

There are v-i boundary vertices in total. The caps introduce b vertices and
exactly v-i edges, since each old boundary vertex is joined only to the new apex
of its own boundary component. Hence

    f0(K) = v+b,          f1(K) = e+v-i,
    g2(K) = gamma(Delta) - (n+1)(b-1).                 (1)

In particular

    Gamma(N_b) ≥ G(N) + (n+1)(b-1).                   (2)

This argument caps components with distinct apices. Identifying the apices
would generally produce a singular vertex and would not justify this application
of a closed-manifold lower bound.

## 3. A single puncture without increasing g2

Take a closed triangulation K attaining G(N). Stellar subdivision of a top
n-simplex adds one vertex and n+1 edges, and removes no edges because n ≥ 3.
It therefore leaves g2 unchanged.

If desired to avoid any local-flatness issue for a non-PL triangulation,
perform n+1 such subdivisions inside a chosen facet. After the j-th
subdivision, retain a new facet omitting one of the original vertices not yet
omitted. After n+1 steps, the retained facet has only newly introduced vertices.
In the standard affine realization of the original simplex, all of those
vertices, and hence the whole retained closed simplex, lie in its interior.
Its boundary is therefore a locally flat standard sphere in an ordinary
Euclidean chart in N.

Remove the interior of that retained facet, keeping every proper face.
The result Delta triangulates N_1. Its vertices and edges are unchanged; exactly
n+1 vertices lie on its boundary. Thus i=f0(K')-(n+1) and

    gamma(Delta)
      = f1(K') - (n+1)f0(K') + binom(n+1,2)+(n+1)
      = g2(K') = G(N).

Together with (2), this proves Gamma(N_1)=G(N), including the closed-manifold
normalization in the question. This construction avoids assuming that an
arbitrary vertex star of an arbitrary topological triangulation is a PL ball.

## 4. The cylinder and boundary gluing

Let C_n=S^(n-1)×[0,1]. Triangulate S^(n-1) as the boundary of an n-simplex,
whose n+1 vertices are totally ordered, and use the compatible staircase
triangulation of each prism over a boundary facet. More explicitly, if a
boundary facet has ordered vertices a0,...,a_(n-1), its n prism simplices are

    {(a0,0),...,(aj,0),(aj,1),...,(a_(n-1),1)}, 0 ≤ j < n.

The common order makes the constructions agree on shared prism faces. They
triangulate the product and use no interior vertices. Their edge set has two
horizontal copies of each edge, n+1 vertical edges, and one upward diagonal
for each ordered edge of the original boundary. Consequently

    f0 = 2(n+1),
    f1 = 3 binom(n+1,2)+(n+1),
    gamma = n+1.

Separate cone caps give S^n, so (2) and G(S^n)=0 show that this is minimal:

    Gamma(C_n)=n+1.                                  (3)

Here G(S^n)=0 follows from its simplex-boundary triangulation and g2≥0.

For two manifolds with nonempty boundary, take disjoint triangulations Delta1
and Delta2 and identify one boundary (n-1)-simplex from each. This is boundary
connected sum, denoted M1 natural M2. The gluing simplex has n vertices and
binom(n,2) edges. Each of its vertices stays on the boundary; the simplex has
no vertex in its relative interior. It follows that

    v = v1+v2-n,  e = e1+e2-binom(n,2),  i=i1+i2,
    gamma(Delta1 natural Delta2)=gamma(Delta1)+gamma(Delta2).   (4)

Thus Gamma is subadditive for boundary connected sum whenever the minima
exist. Applied to the explicit complexes above, adjoining C_n by a boundary
sum adds one puncture: C_n is an n-ball with an interior ball removed, and
boundary sum with the unpunctured ball does not change M. Repeated use of
(3)–(4) with a minimizing triangulation from Section 3 gives the reverse of (2).
Therefore, for all b ≥ 1,

    Gamma(N_b) = G(N)+(n+1)(b-1).                    (5)

In particular the sphere with b balls removed has Gamma=(n+1)(b-1).
The proof of (5) establishes existence of a minimum for these spaces without
needing a general boundary-manifold finiteness theorem.

## 5. What this disproves, and what it does not

For interior connected sum, remove one interior ball from each summand and glue
the two new sphere boundaries by the standard connected-sum identification.
The original boundary components remain. In particular

    B^n # B^n is homeomorphic to C_n,
    Gamma(B^n # B^n)=n+1 > 0=Gamma(B^n)+Gamma(B^n).    (6)

This is a rigorous counterexample to the all-boundary-manifolds/interior-sum
reading. By contrast B^n natural B^n is a ball. There is no contradiction to
boundary-sum or closed-sum additivity.

More generally, for closed N1,N2 and b1,b2 ≥ 1, capping the original boundary
components shows

    Gamma((N1)_(b1) # (N2)_(b2))
      = G(N1#N2)+(n+1)(b1+b2-1).                    (7)

Thus the defect for this interior sum is the closed G-additivity defect plus
n+1. Boundary sum instead has b1+b2-1 boundary components, and its Gamma
defect equals precisely the closed G-additivity defect. These statements use
consistent standard gluing choices; in the oriented category take the usual
orientation-reversing boundary identification.

For closed complexes the facet connected sum identifies n+1 vertices and
binom(n+1,2) edges and deletes the two facet interiors. Its g2 is exactly the
sum of the two g2 values. Minimizing proves the familiar upper bound

    G(N1#N2) ≤ G(N1)+G(N2).                          (8)

Equations (5)–(8) neither prove nor disprove the opposite inequality in (8).

## 6. The exact separator-capping defect

Let K be a closed simplicial n-manifold and let S be a locally flat simplicial
(n-1)-sphere separating it into subcomplexes A and B with A∩B=S. Suppose that
capping A and B gives the proposed connected-sum factors N1 and N2. Add
distinct cone vertices to S on the two sides, obtaining closed complexes K1,K2.
Writing s=f0(S), t=f1(S), direct inclusion–exclusion gives

    f0(K1)+f0(K2)=f0(K)+s+2,
    f1(K1)+f1(K2)=f1(K)+t+2s.

Therefore, with g2(S)=t-ns+binom(n+1,2),

    g2(K1)+g2(K2)
      = g2(K)+g2(S)+s-(n+1).                       (9)

For n=3, Euler's formula for the triangulated 2-sphere gives g2(S)=0, so the
loss is exactly s-4. For n≥4 the sphere lower bound gives g2(S)≥0. Since
s≥n+1, this route generally gives a positive loss. The simplex-boundary
separator has s=n+1 and g2(S)=0, hence loss zero.

In particular, if a g2-minimizing triangulation of N1#N2 contains a separating
missing facet realizing those factors, (9) and (8) prove additivity for that
pair. There is no proof here that such a minimizing triangulation must exist.
A topological prime decomposition alone supplies no missing facet in an
arbitrary minimizing triangulation. Subdivision to exhibit a separator also
does not, by itself, control the minimum or remove the loss in (9).

## 7. Scope of verification and conclusion

The accompanying checker constructs finite products, caps, punctured spheres,
boundary sums, and closed facet sums; it counts all faces directly and checks
the displayed identities, h-vector normalization, and selected mod-two homology
and link diagnostics. Those finite calculations check examples and algebra,
not the universal lower bound theorem or general manifold recognition.

Four substantive routes were pursued: the literal interior-sum test; exact
gluing/subadditivity; capping and puncture normalization; and separator extraction.
The first gives a scope correction, the next two give the formulas above, and
the last identifies the unrepaired reverse-inequality gap. The intended
closed/boundary additivity target remains unresolved by this work. The bounded
literature search did not locate a general resolution, which is not evidence
that no resolution exists. No novelty is claimed.

## References

- S1. Ed Swartz, *Face Enumeration on Manifolds*, in *Triangulations*,
  Oberwolfach Report 24/2012, pp. 1427–1429.
  https://ems.press/content/serial-article-files/46393
- S2. Ed Swartz, *f-vectors and three-manifold complexity*, in *Topological
  and Geometric Combinatorics*, Oberwolfach Report 08/2011, pp. 409–412.
  https://ems.press/content/serial-article-files/46323
- S3. Frank H. Lutz, Thom Sulanke, Ed Swartz, *f-Vectors of 3-Manifolds*,
  Electronic Journal of Combinatorics 16(2) (2009), R13, especially Lemma 9,
  Corollary 10, Conjecture 11.
  https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i2r13/pdf/
- S4. Isabella Novik, Ed Swartz, *g-vectors of manifolds with boundary*,
  Algebraic Combinatorics 3(4) (2020), 887–911, especially Section 7 and
  Proposition 7.8. https://doi.org/10.5802/alco.121
- S5. Isabella Novik, Ed Swartz, *Socles of Buchsbaum modules, complexes and
  posets*, Advances in Mathematics 222 (2009), 2059–2084, Theorem 5.2.
  Author manuscript: https://sites.math.washington.edu/~novik/publications/socle.pdf
