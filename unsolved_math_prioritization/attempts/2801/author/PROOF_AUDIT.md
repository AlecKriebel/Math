# Attributed proof audit for KP-3.3

## Scope and attribution

This is an audit of **Huabin Ge, arXiv:2609.27635v1, Theorem 1.1**, not an
independent discovery. The source is the 23 September 2026 preprint:
<https://arxiv.org/html/2609.27635v1>. Sections 2–4 contain the complete chain
needed for the catalogued geometric ideal triangulation question. The arXiv
HTML lists **CC BY 4.0**; this note adapts and explains that proof, with additional
audit details and independently written exact controls. Credit for the
construction and theorem belongs to Ge. The original PDF is not republished.

**Self-review conclusion:** the proof chain below is valid assuming the
classical Epstein–Penner decomposition in the stated standard form. No gap was
found in the new compatibility argument or its application. Fresh independent
complete review and administrative acceptance are pending. Neither journal
acceptance nor a formal proof-assistant verification is claimed.

## 1. Classical input and the actual affine polyhedra

Let M be a complete noncompact finite-volume hyperbolic 3-manifold, with no
orientability assumption. Write M = H³/Γ, where Γ is a torsion-free discrete
group of isometries; in Lorentz coordinates it lies in O⁺(3,1), and need not
preserve orientation.

The classical Epstein–Penner construction, after a choice of cusp decoration,
uses a Γ-invariant discrete set of future lightlike vectors in R^(3,1). The
relevant finite faces of its convex hull are bounded three-dimensional convex
polytopes lying in supporting affine hyperplanes A. Their radial projections
form a locally finite Γ-equivariant ideal polyhedral decomposition of H³ with
finitely many quotient cells. Each A has an equation λ(x)=1 with λ positive
on its vertices. Ge gives the stronger usual spacelike-hyperplane description.
This classical existence theorem is the external input, not a theorem proved
by our finite tests.

Choose one lifted polytope for each quotient cell. A neighboring lift across a
face F is carried to its chosen representative by some γ in Γ. The induced
face map is the restriction of the **linear Lorentz transformation γ** to F.
Thus this is an affine map between faces of the lifted Euclidean polytopes.
It is important not to replace this by the false assertion that all isometries
are affine in the Klein ball; their actions there are generally projective.

The vertices really are extreme vertices, and their affine span has dimension
three. A nonidentity γ cannot stabilize a lifted polytope or a face: it would
permute its finite vertex set and fix their future-timelike barycenter, yielding
a fixed point of H³, contrary to torsion freeness and discreteness. Hence facet
occurrences are genuinely paired; two distinct facets of the same chosen
polytope may be paired, but a geometric lifted facet does not have a nontrivial
stabilizer. This avoids any ambiguous fixed-face interpretation of an abstract
face-pairing system.

## 2. Regular subdivisions and their boundary restrictions

For a bounded convex 3-polytope P with vertex set V and a real height function
h on V, consider the lower faces of the convex hull of (v,h(v)). Projecting
them gives a regular subdivision Reg(P,h). A cell is the convex hull of those
vertices where an affine function r satisfies r(v)=h(v), subject to
r(w)≤h(w) for every vertex w. Adding an affine function to h leaves the
subdivision unchanged.

For a facet F of P,

    Reg(P,h) restricted to F = Reg(F,h restricted to V(F)).

Here is the supporting-function check behind Ge's Lemma 2.1. Restricting a
support r to F gives a lower cell of the face. Conversely, extend a supporting
affine function of F to an affine r₀ on P. Choose an affine q zero on F and
strictly positive at all vertices of P outside F. For sufficiently large K,
r₀−Kq is strictly below all outside lifted vertices, with the original contact
set on F. Thus every face-lower-cell occurs in the restriction. All required
maxima are over finite vertex sets.

This also addresses geometric matching, rather than only matching lists of
diagonals. An affine face homeomorphism carries lower supporting inequalities
to lower supporting inequalities. If two face heights differ by an affine
function after this identification, their entire subdivisions agree.

## 3. The dimension count, including identifications

For each current 3-polytope P_i put

    H_i = R^(V_i) / Aff(P_i),       dim H_i = v_i−4.

Aff(P_i) denotes restrictions of ambient affine functions, a four-dimensional
space because the polytope is full-dimensional. For each paired n_α-gonal
facet define

    Q_α = R^(vertices of F_α) / Aff(F_α),       dim Q_α = n_α−3.

For the affine pairing φ_α:F_α⁻→F_α⁺ define the linear constraint

    B_α([h]) = [h⁻_α − h⁺_α composed with φ_α] in Q_α.

This is well-defined on the quotient: changing the height on either incident
polytope by an affine function changes its face restriction by an affine
function. The same argument applies if both paired facets belong to the same
polytope. A compatible family is exactly an element of ker B. Global cusp
vertices are **not** forced to have one common numerical height. Only equality
of the induced face subdivisions is needed, and the quotient conditions are a
sufficient linear way to obtain it.

Write v_i,e_i,f_i for local polytope counts and let F be the number of facet
pairs. Counting incidences before quotient identifications gives

    Σ f_i = 2F,           Σ e_i = Σ n_α.

The second identity holds because each polytope edge belongs to two facets;
pairing all facets divides the total facet-edge incidence count by two.
Euler's formula v_i−e_i+f_i=2 now gives

    dim(domain B)−dim(codomain B)
      = Σ(v_i−4) − Σ(n_α−3)
      = ½ Σ(f_i−4).

Consequently dim ker B is at least that number. Every bounded full-dimensional
convex 3-polytope has at least four facets, with equality exactly for a
tetrahedron. If any cell is not a tetrahedron, the lower bound is positive.
It is an integer: the sum of all f_i is even. No unproved independence of the
face equations is assumed; dependent equations only enlarge the kernel.

No additional linear conditions around edges are needed for this construction.
Every edge has only its two endpoints, so no subdivision of an existing edge
is introduced. Pairwise agreement of facet subdivisions descends through every
identification chain. The heights themselves are auxiliary and need not glue
to a scalar function on the quotient.

## 4. Nonzero heights give a strict admissible refinement

Select a nonzero compatible height class. At least one regular subdivision is
nontrivial. Indeed, if a polytope's subdivision consists only of itself, its
whole vertex set lies on a single lower affine support, so its height class is
zero. Every original extreme vertex appears in the regular subdivision: it
cannot be expressed as a convex combination of the other vertices, so it
cannot disappear under lower-hull projection. Thus triviality cannot hide
non-affine heights at discarded vertices.

Every maximal new cell is a full-dimensional bounded convex polytope whose
vertices are among the current vertices. The new cells form a face-to-face
subdivision. On paired outer facets the subdivisions agree by Section 2, and
the original map restricts to each new paired face. Each new internal facet
has two incident cells; regard them as disjoint copies and pair their facet
copies by the identity. Thus the result is another finite affine face-paired
system of the same type.

This is genuine refinement. It does not discard an earlier cut or globally
reselect a different decomposition of an original polytope. Reapplying the
dimension count to all current cells therefore preserves every already formed
interface as a union of new interfaces.

## 5. Finite termination without a genericity assertion

Let V_i denote an original polytope's finite vertex set throughout the process.
All later vertices remain in V_i. Every full-dimensional current cell contains
an affinely independent four-element subset of V_i. Two different current
cells cannot contain the same such subset: both would contain the tetrahedron
it spans, which has nonempty three-dimensional interior, contradicting the
disjointness of cell interiors.

Choosing one such subset for each cell therefore bounds the number of cells
inside the original polytope by

    b_i = #{four-element affinely independent subsets of V_i}.

Each strict refinement increases the total cell count by at least one. It is
bounded by the finite sum Σb_i, so refinement terminates. At termination no
non-tetrahedral cell can remain, because Section 3 would supply another strict
refinement. Hence all cells are tetrahedra, and all face triangulations match.

This avoids two unjustified stronger claims: that a single generic height in
the initial compatibility space necessarily triangulates every polytope, or
that all successive refinements must be represented by one global regular
height function. Neither is used or needed.

## 6. Nondegenerate ideal geometry and descent

Take a resulting tetrahedron with affinely independent vertices v₁,…,v₄ in an
original supporting hyperplane λ(x)=1. If Σc_k v_k=0, applying λ gives Σc_k=0;
affine independence then forces all c_k=0. Thus these four Lorentz-space
vectors are linearly independent.

Their time coordinates t_k are positive. Dividing each vector by t_k gives
(1,p_k), where p_k is an ideal point of the Klein ball. Column-wise nonzero
scaling preserves linear independence; therefore p₁,…,p₄ are affinely
independent in the three-dimensional Klein chart. They are not coplanar, so
the projected ideal tetrahedron is nonflat and has strictly positive volume.

For nonnegative coefficients a_k, the radial projection identity is

    π(Σ a_k v_k) = Σ [a_k t_k / Σ a_j t_j] π(v_k).

Consequently projection takes each affine tetrahedron to the convex hull of
its ideal vertices. It carries the geometric subdivision of the lifted
polytope to a geometric subdivision of the original ideal cell, preserving
face intersections and disjoint interiors. There are no newly introduced
finite or ideal vertices.

Extend the subdivision of representative cells by Γ. Trivial cell stabilizers
make this extension well-defined; compatibility handles shared faces. The
original decomposition is locally finite and each cell has finitely many
tetrahedra, so the result is a locally finite equivariant triangulation of H³.
There are finitely many tetrahedron orbits. Its quotient gives the required
finite face-pairing ideal triangulation of M.

The complete metric is unchanged because this is a geometric subdivision of
the existing metric, not a solution of approximate gluing equations. In the
orientable case, order each tetrahedron compatibly with the orientation to
obtain positive imaginary parts of shape parameters. In the nonorientable
case, no global positive orientation is demanded; the same nondegenerate
geometric gluing realizes the given nonorientable manifold. No double-cover
descent assumption or orientation-preserving group restriction was inserted.

## 7. Exact finite controls and their limitations

`verify_affine_controls.py` independently enumerates lower supporting affine
functions over rational vertex data and verifies Ge's Example 3.5:

- The first cube height function yields exactly the claimed two triangular
  prisms.
- The second-stage prism height functions yield the claimed six tetrahedra.
- Each tetrahedron has Euclidean volume 1/6, and the volumes sum to 1.
- All three opposite-square translation pairs have identical induced
  triangulations.
- The internal rectangle uses the same diagonal on both sides.

Eight additional square-pairing parity cases verify that the compatibility
equations kill all ambient affine heights, retain a nonzero quotient class,
meet Ge's lower dimension bound, and produce a strict regular refinement.
The quotient dimensions are 1,1,1,2,1,2,2,3. These algebraic cases need not be
hyperbolic-manifold quotients. The original cube has 58 independent vertex
four-sets, furnishing a finite control of the termination capacity.

All **64 assertions passed** using exact SymPy rational arithmetic. The script
does not claim an exhaustive census, a universal computational certificate,
or an independent proof of Epstein–Penner. It tests sensitive finite steps;
the universal argument is the mathematics in Sections 1–6.

## 8. Result boundary

The audit reaches exactly the complete finite-volume cusped target, with usual
face-pairing ideal triangulations. It does not certify arbitrary incomplete
metrics, infinite-volume manifolds, geodesic-boundary extensions, an embedded
triangulation of a compactification, all consequences in Ge Sections 5–6,
or historical first priority. The entire pertinent new proof is credited to
Ge's recent unrefereed preprint. The independent complete gate remains pending.
