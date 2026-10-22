# Checkable implication from the cited prior machinery

This is a source-check derivation, not a claim of a new theorem. The polar and
radial-scaling route is already given by Martin Winter in [the two-page author
note](https://martinwintermath.github.io/pdf/publications/Stokers_conjecture.pdf).
Its specialized rigidity input is Lemma 4.3 of [Winter's earlier
paper](https://arxiv.org/abs/2302.14194v2), associated with
[DOI 10.1093/imrn/rnad298](https://doi.org/10.1093/imrn/rnad298).
The details below make the potentially problematic non-realization and equality
steps explicit.

## Precise implication

Let P and Q be bounded full-dimensional convex polytopes in R^d, d >= 2,
with a fixed face-lattice isomorphism. Let n_i and m_i be corresponding outward
unit facet normals. Suppose the corresponding interior dihedral angles satisfy
theta_P(i,j) <= theta_Q(i,j) for every adjacent facet pair. Then one orthogonal
linear map carries every m_i to n_i; equivalently their entire labeled normal
Gram matrices agree. The candidate is the d=3 case.

## 1. Polarity and the inequality sign

Translate interior points to 0, and write the irredundant facet inequalities as

    n_i . x <= h_i,       m_i . y <= k_i,       h_i,k_i > 0.

The source polar A=P^o has vertices a_i=n_i/h_i. The target polar B=Q^o has
vertices b_i=m_i/k_i. Polarity turns the fixed facet correspondence into a
vertex correspondence between A and B, and adjacent facets into edges.

Set c_i=m_i/h_i. These c_i need not be vertices of a polytope combinatorially
equivalent to A. Nothing below assumes that they are.

For unit normals, the interior angle equals pi-arccos of their inner product;
this is increasing in that inner product. Thus the angle hypothesis gives

    n_i . n_j <= m_i . m_j.

For every edge ij of A,

    |a_i-a_j|^2 - |c_i-c_j|^2
      = 2 (m_i.m_j - n_i.n_j)/(h_i h_j) >= 0,

and |a_i|=|c_i|=1/h_i. These are precisely edge contraction and equal radii.
They are not equal support-number assumptions on P and Q.

## 2. The origin condition for a general graph embedding

Let alpha_i(x) be the Wachspress coordinates on A. The properties used are:
continuity on A, nonnegative coefficients with sum 1, linear precision
x=sum alpha_i(x) a_i, and support on the vertices of the minimal face containing
x. For interior x all coefficients are positive. These are the properties
recorded in Remark 3.7 and Section 4 of the earlier paper.

For t in [0,1] define

    s_i(t)=(1-t)/k_i+t/h_i > 0,
    c_i(t)=s_i(t)m_i,
    Phi_t(x)=sum_i alpha_i(x)c_i(t).

At t=0, the boundary map Phi_0 takes each proper face f of A into its
corresponding proper face f' of B. Choose a face-preserving PL homeomorphism
g:boundary A -> boundary B using barycentric subdivisions. For each x in f,
the segment between Phi_0(x) and g(x) lies in f', by convexity. It therefore
avoids 0. Radial normalization of this homotopy shows that
Phi_0/|Phi_0| on boundary A has degree +1 or -1. The sign is irrelevant.
This argument requires neither injectivity of the Wachspress map nor any
unproved injectivity conjecture about it.

Now fix any proper face f of A. The vertices b_i corresponding to a_i in f
belong to a proper face f' of B. Since 0 is interior to B, some linear
functional ell_f and number beta_f>0 satisfy

    ell_f(b_i)=beta_f  whenever a_i belongs to f.

For all such i and all t,

    ell_f(c_i(t))=s_i(t) k_i beta_f > 0.

By the face support property, ell_f(Phi_t(x))>0 for every x in f. Hence no
Phi_t(boundary A) meets 0. Compactness also gives a positive distance from 0
for the full boundary homotopy, although only avoidance is needed.

The normalized boundary degree stays +1 or -1 until t=1. If Phi_1 avoided 0
on all of A, its normalization would extend that map to the ball A and its
boundary degree would be zero. Contradiction. Therefore

    Phi_1(x_*)=0 for some x_* in interior A.

This verifies the nontrivial origin hypothesis in the published lemma's
graph-embedding formulation. In particular, replacing it with the weaker
condition 0 in interior(conv{c_i}) would not be a valid general proof.

## 3. Equality and orthogonality without an extra rigidity assumption

Applying Lemma 4.3 directly now gives a_i=T c_i for one orthogonal T. For an
explicit check of the equality mechanism, one can instead use Theorem 3.2 as
follows. Let alpha=alpha(x_*), and define

    E_alpha(z)=(1/2)sum_{i,j} alpha_i alpha_j |z_i-z_j|^2.

The theorem gives E_alpha(a)>=E_alpha(c), with equality only when c_i=L a_i+b
is affine on the entire skeleton and all edge lengths are unchanged. On the
other hand, equal radii and Phi_1(x_*)=0 give the exact variance identity

    |x_*|^2+E_alpha(a)
       =sum_i alpha_i|a_i|^2
       =sum_i alpha_i|c_i|^2
       =E_alpha(c).

Consequently x_*=0 and E_alpha(a)=E_alpha(c). The theorem's equality case
applies. Linear precision gives Phi_1(0)=b=0, so c_i=L a_i.

It remains to check that affine equivalence cannot conceal a nonorthogonal
flex preserving these data. Put S=L^T L-I. Equal radii give a_i^T S a_i=0 at
every vertex, and unchanged edge lengths give d^T S d=0 for each incident
edge direction d=a_j-a_i. Expanding the equality at a_j yields

    0=(a_i+d)^T S(a_i+d)-a_i^T S a_i=2 a_i^T S d.

The edge directions incident to any vertex of a full-dimensional convex
polytope span R^d: their cone is the full-dimensional tangent cone. Thus
S a_i=0 at every vertex. The vertices linearly span R^d, so S=0. Hence L is
orthogonal, and T=L^T has the required direction. This explicitly supplies
the equality-to-orthogonality step; it does not import support or edge-length
rigidity of the original polytopes.

## 4. Exact target and original question

Multiplying a_i=T c_i by h_i yields n_i=T m_i for every facet. Orthogonality
immediately implies n_i.n_j=m_i.m_j for every pair, including nonadjacent
facets. Conversely equal full Gram matrices of spanning vector families
define a well-defined orthogonal map by sum u_i m_i -> sum u_i n_i: the
squared norms of every linear combination agree, so relations and inner
products are preserved. Facet normals span because a common perpendicular
direction would make the original polytope unbounded.

The original OWR problem asks only for one corresponding edge with
theta_P<=theta_Q (or all corresponding angles equal). If no such edge
existed, theta_Q<theta_P at every edge. Applying this theorem with P,Q
reversed would force equality, a contradiction. The added all-equal
alternative is redundant for a weak inequality. OWR's question does not by
itself assert equality of all normal Gram entries.

## Boundary and limiting cases

- Nonsimple vertices: the face support property and the exposing functional
  work for faces with arbitrarily many vertices. No triangulation into a
  simplicial polar is assumed.
- Arbitrarily obtuse genuine dihedral angles: the inner product identity
  needs no acute-angle bound.
- Orientation-reversing correspondence: degree -1 is sufficient.
- Different supports: h_i and k_i may be different; all interpolation factors
  remain strictly positive.
- Reflection, rotation, translation, and homothetic rescaling: these are
  consistent with the conclusion about normals. The original polytopes need
  not be congruent; for example different rectangular boxes have identical
  labeled unit normals.
- Unbounded, lower-dimensional, redundant-facet, or flat-degenerate objects
  are outside the target. Positive supports and a full-dimensional polar
  are used essentially.

The imported nontrivial theorem remains Winter's Wachspress expansion
theorem, proved there using the Izmestiev matrix. This derivation checks its
application and equality step; it is not a new from-scratch verification of
all foundational convex-geometry and spectral results in that paper.
