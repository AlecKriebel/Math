# Credited reconstruction of the compression-body answer

## 1. Exact scope and conventions

The target asks for the compression-body replacement in the double-coset
description of a Heegaard splitting of a compact orientable 3-manifold with
boundary, an explanation using the handle decomposition, and the knot-exterior
specialization. These conventions come from Birman's preceding discussion
on pp. 142 and 145–146 [B]. Her default splitting genus is at least two.
We also explain the low-genus and spherical-boundary bookkeeping below.

Fix the two compression bodies, their positive-boundary identifications with
a closed oriented surface S, the assignment of the negative boundary to the
two sides, and any boundary markings being retained. Equivalence means an
orientation-preserving homeomorphism of the glued manifolds carrying each
specified side onto the corresponding side. It does not mean an isotopy
relative to an already fixed ambient manifold. It does not forget the splitting.
The choice to allow exchanging the two sides is an additional quotient.

For an oriented compression body C with positive boundary S, write

    E(C) = image(Mod⁺(C; ∂₊C) → Mod⁺(S)).

Here the notation means homeomorphisms preserving the distinguished positive
boundary, with no pointwise condition on the other boundary unless specified.
It is the full image, not an injectivity assertion for a restriction map.
For a handlebody H this is the usual handlebody subgroup. For a product
C = S×I it is all of Mod⁺(S).

Oertel's Definition 1.3 [O] is precisely this extendible subgroup, denoted
Hₓ(W), together with its boundary-relative version H_d(W).

## 2. Handle data give a concrete subgroup

First use the conventional compression bodies with nonspherical negative
boundary: attach 2-handles along a finite disjoint curve system X on S×{1}
and cap the resulting sphere boundary components with 3-balls. The untouched
S×{0} is the positive boundary. Empty X is allowed. Let

    N_X = normal closure in π₁(S) of the attaching curves in X.

Basepoint paths and orientations of these curves do not affect this normal
subgroup. Van Kampen gives

    ker(π₁(S) → π₁(C)) = N_X.

Indeed a 2-handle kills the normal class of its attaching circle, whereas a
3-handle does not change π₁. Thus a concrete answer in terms of handle data is

    E(C) = { f ∈ Mod⁺(S) : f₍*₎(N_X) = N_X }.                 (1)

The outer automorphism f₍*₎ is enough: inner automorphisms preserve every
normal subgroup, so the condition is well-defined without choosing a
basepoint-preserving representative.

Proof of (1). An extension over C necessarily preserves the kernel of the
inclusion, by naturality. Conversely, apply Biringer–Johnson–Minsky,
Lemma 4.2 [J], to two copies of C, with positive-boundary markings id and f.
Their marking kernels are N_X and f₍*₎⁻¹(N_X). Under the condition in (1)
these are equal, so that lemma supplies a homeomorphism extending f. Since
f preserves the orientation of the positive boundary, the extension preserves
the orientation of the connected 3-manifold. This proves the reverse inclusion.
This is an immediate use of the published marked-compression-body lemma, not
a new extension theorem.

The condition concerns the entire normal subgroup, rather than preserving
the finite set X. Requiring f(X)=X would incorrectly freeze one handle
decomposition. Bonahon's Proposition B.1 [F] says that minimal complete
disk systems are related by slides and isotopies. Different systems describing
the same marked C have the same N_X and therefore give the same group (1).
One may instead use preservation of the full set of disk-bounding curves:
these normally generate N_X, so setwise preservation implies (1), while an
extension preserves that full set. This observation does not assert that a
one-way inclusion of disk sets is enough.

For the dual 1-handle description, let F=∂₋C have k≥1 components of genera
h₁,...,h_k. If n 1-handles are attached to F×{1} and the result is connected,
the positive genus is

    g = Σ hᵢ + n − k + 1.                                   (2)

To see this directly, F×I has Euler characteristic Σ(2−2hᵢ), and each
1-handle subtracts one. Since the boundary has Euler characteristic twice
that of the orientable 3-manifold, adding χ(F) and 2−2g gives (2).
Connecting k components requires at least k−1 handles. The empty-negative-
boundary case is separately a handlebody, constructed from one 0-handle
and g 1-handles. Neither the number n alone nor the genera alone replace
the marked attaching data N_X on S.

## 3. The double coset, including its orientation convention

Let C₁ and C₂ be fixed oriented models with identified positive boundaries S.
A gluing map α:∂₊C₁→∂₊C₂ reverses orientation. The convention-free answer is
the orbit set

    E(C₂) \ Isom⁻(∂₊C₁,∂₊C₂) / E(C₁),                     (3)

where Isom⁻ denotes isotopy classes of orientation-reversing homeomorphisms.
Left and right multiplication are by the boundary maps of extendible
homeomorphisms. Equivalently, fix one orientation-reversing identification
j:∂₊C₁→∂₊C₂ and write α=jφ, φ∈Mod⁺(S). Then (3) becomes

    (j⁻¹E(C₂)j) \ Mod⁺(S) / E(C₁).                         (4)

Proof. Suppose a side-preserving equivalence has restrictions b₁:C₁→C₁
and b₂:C₂→C₂. Their boundary maps satisfy

    α₂ b₁ = b₂ α₁,

so α₂=b₂α₁b₁⁻¹, exactly the orbit relation (3). In the j coordinates this
is φ₂=(j⁻¹b₂j)φ₁b₁⁻¹, giving (4). Conversely, choose extensions realizing
such boundary classes. Representatives can be adjusted in boundary collars
so the equality holds pointwise; then the two extensions glue to the
required homeomorphism. A boundary isotopy extends over its collar, which
justifies using isotopy classes. Both directions are therefore proved.

When C₁=H is a handlebody and C₂=C is the boundary-bearing compression
body, replace just the left factor by j⁻¹E(C)j. Reversing the direction of
the chosen gluing convention puts the replacement on the other side.
If both pieces bear portions of ∂M, replace both factors. This also covers
disconnected nonspherical negative boundary and permutations of equal-genus
components, unless labels have been imposed. It is important not to omit
the j conjugation without compatible model identifications.

The quotient classifies fixed-genus splittings, not all homeomorphic
3-manifolds uniquely at that genus. Different splittings of one manifold
may occupy different double cosets. Stabilization and boundary partition
must be treated separately; see Scharlemann [S], §§2.2, 3.1, and 7. The
description here supplies no algorithm for minimal genus or stabilization
number. None is requested by this particular problem. Allowing a swap
of isomorphic sides adds the corresponding involution on (3).

## 4. Boundary markings and the knot space

For ordinary compression bodies, Oertel [O], Theorems 1.4(b) and 1.5,
provides the well-defined boundary-restriction map

    ρ:E(C) → Mod⁺(F),       1 → E(C rel F) → E(C) → Mod⁺(F) → 1,

where F=∂₋C; disconnected components may be permuted. His hypotheses hold
for the nonspherical F used here. The relative group is the image of maps
that restrict to the identity on F, not the mapping class group of an
arbitrarily punctured positive boundary. If the extension induces an
isotopically trivial map on F, collar isotopy makes its restriction exactly
the identity without changing its positive-boundary class.

Thus use E(C rel F) when the negative boundary is fixed pointwise. More
generally use ρ⁻¹(B) when the permissible negative-boundary mapping classes
form B≤Mod⁺(F). For labels, markings, or slopes, B is their stabilizer.
Apply the same restriction to either side of (3) as needed.

Now let K⊂S³ be a tame knot and E_K the compact exterior of an open tubular
neighborhood. A p-tunnel description in Birman's pp. 145–146 [B] gives

    E_K = C_p ∪_α H_{p+1},       C_p=(T²×I) ∪ p 1-handles,
    ∂₋C_p=T²,                    ∂₊C_p=S_{p+1}.

Consequently its side-preserving fixed-splitting double coset is (3) with
these two models. Equation (1) uses the p meridians dual to the p tunnel
1-handles as the attaching system; compressing along them restores T².
The other factor is the ordinary genus-(p+1) handlebody group. This is the
requested knot-space specialization, and (2) gives its genus p+1.

If the peripheral torus is parametrized and fixed, use kerρ. If an
unoriented meridian slope μ is retained to specify the filling back into
S³, use ρ⁻¹(Stab(μ)) instead. An exterior equivalence preserving μ extends
over the attached solid torus, because a torus homeomorphism extends over
a solid torus precisely when it preserves its meridian slope. This gives
an equivalence of the resulting knot pairs. Conversely a knot-pair
equivalence preserves that slope. Any extra orientation or longitude
marking must likewise be encoded in B. We do not identify arbitrary
unmarked torus-boundary manifolds with knots in S³: the meridional filling
must actually be S³. No appeal to a knot-complement uniqueness theorem
is needed for this marked statement.

For p=0, C₀=T²×I and its full extendible group is SL(2,Z), whereas its
relative group has trivial image on the other torus. Thus the bare and
boundary-parametrized versions differ even in this elementary case.

## 5. Spherical boundary and low genus

The source's conventional 2/3-handle definition caps spherical negative
boundary. If a general compact M has actual sphere boundary components,
one must retain that information rather than lose it in N_X. Use a
punctured compression-body model: take an ordinary C and remove a specified
finite collection of disjoint interior balls. The number, side assignment,
and any labels of the resulting boundary spheres are extra model data.

For the unrestricted or component-labelled boundary equivalence considered
here, the positive-boundary extendible subgroup is still E(C). In one
direction an automorphism of the punctured model extends over the missing
balls. In the other, an automorphism of C sends the prescribed balls to a
collection of the same size. An isotopy supported in the interior moves
this labelled collection back to the prescribed balls: shrink inside
coordinate neighborhoods, move the centers one at a time along paths
avoiding the other finitely many balls, then enlarge. Isotopy extension
turns those moves into an ambient isotopy, fixing the existing boundary.
Restrict the adjusted homeomorphism to the punctured C. If an identity
restriction on each spherical boundary is wanted, its orientation-preserving
sphere map is isotopic to the identity and can be corrected in the collar.
Thus (3) remains exact with these fixed puncture data. This elementary
ball/collar bookkeeping is not a claim that N_X detects sphere counts.

If S=S² the orientation-preserving surface mapping class group is trivial,
and the relevant ball or punctured-ball versions have the unique gluing
class for fixed models. For a torus, product and solid-torus cases have,
respectively, the full SL(2,Z) and the meridian-slope stabilizer; the latter
is also immediate from the explicit disk extension. These cases do not
rely on a genus-at-least-two theorem. Disconnected M is treated component
by component, with an additional permutation quotient only when its
components are unlabelled. Noncompact or nonorientable manifolds are not
the chapter's target and are not claimed here.

## 6. Attribution and conclusion

The handle-kernel criterion is a direct corollary of [J], the changes of
disk system are [F], and the full/relative extension groups are [O].
The gluing-orbit argument is the usual argument already used in [B] for
handlebodies. Barbar [A], equation (3.37), explicitly uses the relative
compression-body/handlebody double-coset space, citing [O]. His formal
infinite TQFT sums and weights are not mathematical dependencies here.
All three requested components are covered as a credited reconstruction.

References and exact checked locations are in `SOURCE_GATE.md`.
