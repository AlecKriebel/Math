# Failed and limited approaches

Record negative results here only with a precise statement of the searched
class.  A failed search is never evidence of global nonexistence unless an
exact completeness theorem and replayable certificate accompany it.

## Historical limitation

The numerical search that found the published \(d=4\) five-term Pauli support
was not preserved seed-by-seed.  It is not reproducible and will not be used
as evidence.  The final formula and its exact proof are reproducible.

## Cyclic Gaussian functional ansatz at \(d=6\)

Every trace-zero Hermitian involution \(H=f(U)\) in the cyclic algebra of
the standard order-six Gaussian Weyl generator was exhaustively checked.
There are exactly 20 spectral sign assignments.  None satisfies the cubic
relation; every failure has an exact nonzero twisted-group-algebra
coefficient.

This rules out only the one-generator functional ansatz \(H=f(U)\), not
general Weyl, group-algebra, or \(d=6\) solutions.  See
`notes/root_gaussian_functional_no_go.md`.

## Broad structured construction ansätze

Exact calculations also exclude the following precisely defined families:

- scalar-natural gluing across a local direct sum;
- a controlled odd-dimensional middle factor in the heterogeneous
  spectator construction;
- all 256 graph-phase/product-flip qutrit extensions of the published
  two-reflection mechanism, at every mixing angle;
- diagonal \(SU(2)\)-equivariant rank-six heterogeneous projections;
- the two central rank-six \(S_4\)-equivariant projections;
- factorwise Pauli or quaternionic substitutions on a qutrit;
- all ice-rule/unordered-pair block operators;
- all monomial unitary Hecke operators.

The noncentral \(S_4\)-equivariant branch was searched only numerically and
is not exactly excluded.  Full definitions, proofs, certificates, and
remaining scope are in `notes/track_additive_constructions.md`.

## Numerical dimension-six searches

Calibrated full-Grassmann, symmetry-reduced, and heterogeneous
\(12\times12\) searches found no \(d=6\) candidate.  Repeated
\(\sqrt{12}\) minima in the heterogeneous search were identified as an
involutive braid stratum whose exceptional linear term remains nonzero;
they are not near-solutions or lower bounds.

These searches are candidate generators and falsifiers only.  They neither
exhaust the continuous search spaces nor give evidence of global
nonexistence.  See `notes/track_d6_falsifier.md`.

## Rank-one Bloch-controlled face models

For
\[
V=\mathbb C^2\otimes\mathbb C^3,\qquad
H=\sum_{j=1}^{6}
\bigl((n_j\cdot\sigma)\otimes I_3\bigr)
\otimes|\psi_j\rangle\langle\psi_j|,
\]
the full continuous ansatz is excluded exactly, for every orthonormal
control basis and every six-tuple of unit Bloch vectors. This supersedes a
partially completed numerical search in the same ansatz.

The proof does not apply to higher-rank controls, reflections acting
nontrivially on the qutrit factor, general operator-valued face blocks, or
arbitrary \(36\times36\) solutions. See
`notes/face_rank_one_control_no_go_d6.md`.

## All directly controlled and diagonal-regular branches

The broader invariant theorem in `notes/controlled_leg_divisibility.md`
shows that a rank-\(r\) projection in either one-leg commutant forces
\(8\mid rd^2\). Thus a hypothetical \(d\equiv2\pmod4\) solution cannot
have an odd-rank leg-commutant projection. In particular, every solution
controlled in a local orthonormal basis, every leg-commutant MASA, and the
full diagonal-regular group-relative ansatz are excluded exactly.

This does not rule out scalar one-leg commutants or finite-dimensional
commutant representations whose minimal projection ranks are all even.
The theorem therefore narrows the unresolved branch to genuinely
noncontrolled solutions; it is not the desired global divisibility theorem.
See `notes/controlled_leg_divisibility.md` and
`notes/group_relative_ansatz_exact.md`.

## Cyclic three-color low-Schmidt models

The complete mixed Fourier three-color family and its pure-product boundary
are excluded by exact contraction and Fourier arguments. This family is
broader than the original fixed-angle numerical slice and contains the
two-color \(d=4\) circle as a calibration.

The proof does not cover arbitrary three-color block operators, higher
operator-Schmidt rank, or noncyclic couplings. See
`notes/track_color_low_schmidt_exact.md`.

## Direct use of the \(D^{(6)}\) connection

The Evans--Pugh cell system does yield an exact exceptional Hecke operator,
but on the 20-dimensional space of composable directed two-edge paths, not
on a 36-dimensional vertex tensor square. Zero extension to the full
100-dimensional edge tensor square is singular. Filling the forbidden
pairs by either Hecke eigenvalue gives a unitary Hecke operator but fails
the braid equation exactly.

Accordingly, the existing connection is not the sought ordinary \(d=6\)
witness under any of these direct identifications. A new vertex--face
intertwiner, finite-depth conversion, or all-strand equivalence remains
logically possible. See `notes/track_d6_ocneanu_cells.md`.

## Channel-only divisibility obstructions

Canonical channels supply strong universal constraints, including complete
positivity of both affine transforms and a prescribed traceless-Hermitian
Kraus geometry. Even after additionally imposing every commutation,
isospectrality, and joint-polynomial pattern observed in the exact \(d=4\)
families, an exact Weyl-diagonal \(d=6\) channel model exists.

Identity-pairing its Schmidt directions unexpectedly satisfies the cubic
relation exactly, but has eigenvalue multiplicities \(9\) and \(27\) and
is not an involution. Its affine involution is an ordinary braid involution
of trace \(18\), not an exceptional rank-half witness. Thus a valid
obstruction must use the simultaneous shared realization by a trace-zero
Hermitian involution, not channel spectra or affine positivity alone. See
`notes/track_channel_identities.md`.

## Representation-only parity mechanisms

Central ranks, Markov weights, Bratteli multiplicities, one-sided tower
embeddings, determinants, the complex quaternion algebra, and naive
Frobenius--Schur/Brauer arguments all permit \(d=2s\) with odd \(s\).
Consequently none can prove \(4\mid d\) without an additional theorem using
the simultaneous tensor placements \(P\otimes I\) and \(I\otimes P\).
See `notes/track_coherence_parity.md`.

## Full diagonal color symmetry and fixed Weyl pairings

The exact Weyl cubic point does not deform to an involution within any
pairing that preserves its two nine-dimensional color blocks. More broadly,
Schur--Weyl reduction excludes every diagonally \(U(m)\)-equivariant
exceptional solution on
\(\mathbb C^2\otimes\mathbb C^m\) when \(m\) is odd.

This closes the natural full-color mechanism in every unresolved
dimension, but it does not cover smaller finite symmetries, arbitrary
operator-Schmidt frames, or non-equivariant matrices. The general
\(O(19)\) deformation search remains numerical outside the exactly excluded
block-preserving subfamilies. See
`notes/track_weyl_h0_deformation.md`.

## Endpoint-commutant arithmetic and endomorphism ergodicity

Once odd-rank leg projections are excluded, all remaining represented
finite-dimensional \(C^*\)-algebra types pass the complete one-sided and
two-ended multiplicity arithmetic. At \(d=6\), the scalar algebra,
\(M_3\otimes I_2\), and all three even-atom direct-sum types survive every
such test.

The associated Yang--Baxter endomorphism is nonergodic for every exceptional
solution with \(d>2\), but nonergodicity need not produce an algebraic or
one-site fixed point. Therefore neither endpoint dimensions, Jones index,
nor the currently available fixed-point theorem closes the scalar/even-atom
branch. The missing datum is the relative position of the two endpoint
algebras on the middle tensor factor. See
`notes/leg_commutant_obstruction_audit.md`.

Finite braid image does not close this gap. Rowell does prove that every
fixed-strand \((3,6)\) image is finite, but the growing sequence of finite
groups supplies no global finite-group average. More sharply,
\[
S_m=(q-1)(I_m\boxplus I_m),\qquad d=2m\ge4,
\]
has finite braid images, finite-order generators, the exact exceptional
scalar normalized partial trace, scalar one-leg commutants, no algebraic
fixed points, and a nontrivial von Neumann fixed algebra. This exact family
has an opposite eigenvalue pair, so it closes only the finite-image shortcut:
an exceptional-specific bridge using no-opposite-spectrum and horizontal
braid-subfactor irreducibility remains open. See
`notes/finite_braid_image_fixed_point_audit.md`.

## Crossed-factor versus equal-color face models

The crossed-factor \(3\times2\) and \(2\times3\) face ansätze are now
excluded exactly: one leg always has a rank-three control projection, so the
controlled-leg divisibility theorem applies. This supersedes their negative
numerical runs.

The equal-size three-color model instead has rank-two atoms on both legs.
Only its cyclic low-Schmidt subfamily is excluded exactly. The general
relative-position and arbitrary-block problem remains open.

## Four-site intersection parity

The canonical common-one projection on three sites obeys a new shifted
Temperley--Lieb-like relation with squared angle \(1/4\). Its exact
four-site block count is \(d^4/8\), which is integral for every even \(d\).
The induced partial isometry acts between two different subspaces and has
no basis-independent determinant; the canonical full-space direct rotation
has determinant one on each individual block.

An exact \(d=6\) GHZ-times-spectator countermodel satisfies all marginals,
same-sign \(1/4\)-angle relations, and opposite-sign orthogonality derived
in this route while failing the original cubic because the chosen
projection is not the full common intersection. Thus these consequences
cannot be detached from the full-intersection/generic-\(1/3\)-sector data
and used as a parity theorem. See
`notes/intersection_projection_structure.md`.

## Nontrivial tensor-product extensions

Lechner's tensor product has product dimension and product spectrum. The
multiplicative stabilizer of the exceptional spectrum
\(\{-1,e^{i\pi/3}\}\) is only \(\{1\}\). Therefore an exceptional tensor
product can use only an identity spectator factor. This recovers the known
\(4m\) construction but cannot generate \(d=6\).

The argument does not cover non-product colored gluing or off-diagonal
couplings. See `notes/tensor_product_extension_no_go.md`.

## Uniform rank-two cells and the odd factor branch

The endpoint arithmetic initially made \(M_3\otimes I_2\) look viable at
\(d=6\). It is now excluded by a genuinely spatial argument: factor
commutation reduces one local leg to a scalar-free qubit Pauli expansion,
and involutivity forces rank-one control on the opposite leg. This
contradicts the controlled-leg divisibility theorem.

That proof does **not** apply after weakening the factor to three central
rank-two atoms. In the weakened branch, standardness permits 217 labelled
two-site cell-rank tables, and the endpoint equations permit 1540 labelled
common-rank tables. In particular, assuming nine rank-two cells or uniform
endpoint multiplicity \(3\) is unjustified. The full-\(U(6)\) numerical
search covers only the uniform-cell subansatz and is negative evidence,
not a classification. See `notes/rank_two_leg_commutant_branches.md`.

More is excluded exactly: the two three-atom decompositions cannot share
even one rank-two atom. A shared cell becomes scalar by the base-\(2\)
classification and determinant gap, and scalar propagation contradicts
the partial trace. This still leaves genuinely transverse relative
\(U(6)\) positions.

The same proof now rules out *any* nontrivial intersection of the two
leg commutants at \(d=6\), because every nontrivial common projection has
rank two or has a rank-two complement.  This kills aligned and
flip-symmetric versions of the two-block algebras as well.  It does not
kill arbitrary relative position: explicit permutation conjugates of all
remaining two-block algebra pairs have scalar intersection, and abstract
three-strand cubic models realize their complete endpoint counts.

The expanded numerical falsifier sampled all nine discrete cell-rank
orbits in the three-color branch with an arbitrary relative \(U(6)\).
Its best residual was \(6\), but one seed per orbit is not exhaustive and
cannot be promoted to a no-go theorem.

## Scalar permutation, reshuffling, and cup-cap contractions

All six closures of the three-site cubic against the permutation algebra
\(\mathbb C[S_3]\) have now been reduced exactly. Four are tautologies,
and the other two are scalar shadows of the known outer operator-valued
channel identities. The middle ordinary partial contraction yields a
positive operator with fixed trace, bounds, and scalar marginals, but
those data have an exact scalar \(d=6\) model.

The negative audit is stronger: the standard rank-half involution
\[
H=(Z\otimes I_3)\otimes(X\otimes I_3)
\]
annihilates all 48 scalar pairings obtained from the six permutations by
arbitrary sitewise partial transposes, yet its cubic residual has squared
norm \(192\). Thus Brauer-style scalar closures, reshufflings, and
cup-cap contractions cannot replace the operator-valued overlap
identities in a parity proof. See
`notes/permutation_contraction_audit.md`.

## Full retained Weyl coefficient interpolation

The Weyl-channel near-miss was broadened from a fixed Schmidt orbit to all
\(361\) real coefficients in the retained traceless-Hermitian
qubit--qutrit Weyl frame. Forty predeclared random, direct, continuation,
and mixed-strata searches found no simultaneous involution/cubic point.

The endpoints consistently returned to two algebraic strata. One is the
known exact cubic with the wrong quadratic. The other consists of scaled
adjacent-anticommuting involutions; exactly, such an involution obeys the
cubic with coefficient \(1\), rather than the required \(1/3\). This is a
useful structural explanation of the numerical basins, but the search is
neither exhaustive within its \(361\)-dimensional linear subspace nor a
test of all traceless Hermitian \(36\times36\) matrices. See
`notes/d6_weyl_full_coefficient_search.md`.

## Direct fusion-grading, Frobenius--Schur, and projective-\(A_4\) parity

The neutral fusion component does expose a genuine parity-bearing algebra:
the nontrivial twisted \(A_4\) algebra is
\(M_2(\mathbb C)^{\oplus3}\). If it acted on an invariant
\(s=d/2\)-dimensional multiplicity space, then \(s\) would be even.

The direct argument stops at exactly that descent. The natural projective
action is on the categorical two-dimensional factor of
\(\mathbb C^2\otimes\mathbb C^s\) and exists for odd \(s\). The generator
is non-self-dual, the determinant-channel braid action is scalar, and
spatial reversal sends \(P\) to \(FPF\) rather than preserving a general
solution. The published \(d=4\) witness has a nonzero exact reversal
defect, so reflection cannot be silently used as an internal
Frobenius--Schur operator. See
`notes/fusion_anomaly_parity_audit.md`.

## Closing determinant channels with boundary Hecke words

The rank-\(s^3\) common-one and common-zero three-site blocks initially
look like natural places to seek a parity-forcing complex or quaternionic
structure. This route is now closed for every number of added boundary
sites. The exact corner identity
\[
(a\otimes I)\mathcal A_{m+3}(a\otimes I)=a\otimes\mathcal A_m
\]
shows that the determinant multiplicity is always a spectator. Even the
first \(M_2\) Clifford block at six sites acts on the newly added path
factor, where its module multiplicity \(3s^6\) may be odd. Tensor reversal
does not evade the theorem because it maps \(P\) to \(FPF\), not generally
back to \(P\). See
`notes/determinant_boundary_corner_factorization.md`.

## Cutting unresolved dimensions out of identity amplifications

The direct construction
\[
H^{(4)}\boxtimes I_m
\quad\leadsto\quad
\text{a square-invariant local }(4m-2)\text{-plane}
\]
is impossible for every \(m\ge2\).  A rank-\((4m-2)\) commuting local
projection has two-dimensional complement.  Leakage through that complement
forces a two-dimensional kernel in a three-operator Schmidt pencil, but the
exact Bell-basis rank cone is only a union of six lines.  The remaining
coefficients then force the full active \(M_4\), making the projection rank
divisible by four.

This is an exact no-go for a natural construction mechanism, not an
unrestricted nonexistence theorem in dimension \(4m-2\).  See
`notes/no_rank_six_subspace_of_d8_amplification.md`.

## Inferring complementary invariance from two-site data

If \(W\otimes W\) is invariant and balanced, invariance of
\(W^\perp\otimes W^\perp\) is exactly the zero-variance condition
\[
\delta=\frac{u^2}{2}-\operatorname{Tr}(K^2)=0.
\]
An exact \(d=6\), \(4+2\) projection has all required two-site ranks,
scalar partial traces, unitarity, Hecke polynomial, and the exact published
\(d=4\) restriction, but \(\delta=1/2\).  It fails the ambient cubic.
Therefore positivity, marginal, and multiplicative-domain arguments at two
sites cannot prove complementary invariance.  The unresolved implication
must use mixed-sector compressions of the full three-site cubic.  See
`notes/one_sided_square_invariance_audit.md`.

## Recovering Rowell's quaternion frame from the braid image

At one bond, the two-eigenvalue braid generator determines only
\[
K_i=u_i+v_i+u_iv_i=-2qR_i-1
\]
inside the two-dimensional algebra
\(\mathbb C[R_i]=\operatorname{span}\{1,K_i\}\).  The individual
anticommuting generators \(u_i,v_i\) belong to the larger ambient
quaternionic algebra and are not braid words on that bond.  Hence their
quaternionic parity cannot be assigned to a one-site or
\(s=d/2\)-dimensional factor without a new compatible frame-selection or
splitting theorem.  Fixed-level complex quaternion modules already exist
for odd \(s\), so the ambient frame by itself supplies no divisibility.

## Using the standard balanced \(GL(s|s)\) Manin Hecke symmetry

After multiplication by \(t=e^{i\pi/6}\), the standard super-Hecke
symmetry has exactly the exceptional roots \(\{q,-1\}\), satisfies the
ordinary braid equation, and for superdimension \((s|s)\) has equal
eigenspace dimensions \(2s^2=d^2/2\).  Thus it is a genuine algebraic
all-even-dimension near miss, including a \(36\times36\) matrix at \(d=6\).

It cannot be made unitary by any local change of basis.  If \(G>0\) were
a local metric, the even diagonal \(q\)-eigenvectors and odd diagonal
\((-1)\)-eigenvectors would force \(G_{ia}=0\) across the parity split.
For a mixed even--odd pair, the two eigenvectors then have inner product
\[
(\bar t-t)G_{ii}G_{aa}\ne0,
\]
contradicting orthogonality for a unitary operator.  See
`notes/manin_super_hecke_unitarity_no_go.md`.

This rules out the standard one-parameter family and its local conjugates
only.  Multiparameter super-Hecke symmetries and nonlocal twists have not
been classified by this argument.

Orthogonalizing the standard \(GL(3|3)\) \((-1)\)-eigenspace does produce
a legitimate rank-eighteen projection, but not a Yang--Baxter solution.
Its exact cubic squared residual is \(140/3\), and each marginal has
squared scalar deviation \(6\). Sixteen predeclared unrestricted
Grassmann runs, with and without a marginal penalty, returned to this same
exact near miss. This identifies a numerical basin but proves neither
local minimality nor nonexistence.

## Diagonal \(S_4\) symmetry on the heterogeneous \((2,3,2)\) block

The full \(S_4\)-equivariant active space
\(V_2\otimes V_3\otimes V_2\) has commutant
\(M_2(\mathbb C)\oplus M_2(\mathbb C)\). The two central balanced
involutions were already excluded. The remaining branch is exactly
\(S^2\times S^2\), not a smaller numerical ansatz. An exact rational
Pauli parametrization, twenty sparse cubic coordinates, seven derived
branch relations, and three final coordinates exclude every real branch;
the selected-coordinate ideal is also the unit ideal over \(\mathbb Q\).
Thus diagonal \(S_4\) symmetry supplies no \(d=6\) witness. This does not
exclude other finite symmetries or an asymmetric solution. See
`notes/s4_equivariant_exact_no_go.md`.

## Diagonal binary-tetrahedral symmetry on the heterogeneous \((2,3,2)\) block

For \(A=\mathbb C^2\) the defining binary-tetrahedral representation and
\(B=\mathbb C^3\) its rotation representation, the complete active module
decomposes as
\[
A\otimes B\otimes A
\cong1\oplus1'\oplus1''\oplus3^{\oplus3}.
\]
Balanced equivariant involutions therefore form, up to complement, exactly
one \(\mathbb{CP}^2\), rather than merely a selected numerical family.
This whole branch is empty: two diagonal cubic coordinates force a
codimension-two real condition, under which a third coordinate has
\[
|F_{57,20}|^2=16/729.
\]
The 64-seed full-complex search is retained only as provenance; the route
is closed by the exact three-entry proof. This does not exclude other
finite symmetries or an asymmetric \(d=6\) solution. See
`notes/binary_tetrahedral_cp2_no_go.md`.

## Kramers degeneracy on the \(1/3\)-overlap space

The generic two-projection sector has the exact form
\[
M_2(\mathbb C)\otimes I_k,\qquad k=3(d/2)^3.
\]
Its canonical normalized commutator squares to \(-I\), but exchanges the
two \(k\)-dimensional halves. It therefore explains only the already
visible even dimension \(2k\). A commuting or projection-swapping
antiunitary of square \(-1\) exists precisely when \(k\) is even:
after standard conjugation it has the form
\((I_2\otimes u)C_0\), and its square is \(I_2\otimes u\bar u\).
The determinant condition for \(u\bar u=-I_k\) is exactly the parity one
wanted to prove.

The tensor-local cyclic compression does not close this gap. On the
published exact \(d=4\) witness, its left and right \(1/3\)-singular
projections are different and the compression is nonnormal:
\[
\operatorname{Tr}(K_LK_R)=18<24,\qquad
\|WW^*-W^*W\|_{\rm HS}^2=16/3.
\]
Reality supplies only conjugation of square \(+1\); adjoint closure, flip,
and outer reversal all fail exactly. Hence no parity follows from these
natural operations. A future proof would need an additional tensor-local
closure or alternating form not present in the audited data. See
`notes/overlap_kramers_parity_audit.md`.

## Forcing projective \(A_4\) descent from commuting-square data

For every exceptional localizer, the represented Hecke algebra
\(\mathcal A_n\) is already the full finite horizontal relative
commutant \(\mathcal L_{R,n}\). Normalized last-site trace gives
\[
E_n(\mathcal A_{n+1})=\mathcal A_n,
\]
so no extra finite horizontal algebra is available to act on the
\(s=d/2\) multiplicity.

Even the first nontrivial Markov commuting square exists exactly at
formal local dimension two. There are rank-four projections
\(p,q\in M_8\) satisfying the exceptional cubic, with
\[
\operatorname{alg}(p,q)\cong
\mathbb C\oplus M_2(\mathbb C)\oplus\mathbb C
\]
and the correct partial-trace expectation onto
\(\operatorname{alg}(p_0)\subset M_4\), but
\[
p=p_0\otimes I_2,\qquad
\|q-I_2\otimes p_0\|_{\rm HS}^2=4.
\]
Thus a commuting square and its first connection cell forget the
same-\(P\) tensor placement that fails in dimension two. Spectator
amplification passes the low-level inclusion arithmetic for every
integer \(s\).

This closes parity arguments based only on horizontal relative
commutants, inclusion matrices, indices, finite braid image, or a single
commuting-square cell. It does not close an all-level flat-connection
argument retaining the common two-site \(P\), nor a module-category
argument preceded by a proved extension from diagonal endomorphism
algebras to off-diagonal coherent morphisms. See
`notes/commuting_square_projective_descent_audit.md`.

## Cutting amplified noncanonical \(d=4\) representatives

The exact C40 theorem applies to the published \(d=4\) witness. Three
exact points of the separate C15 color/face circle were therefore
amplified to \(d=8\), and rank-six square-invariant subspaces were sought
without symmetry constraints. Twelve predeclared reduced runs all
settled at normalized squared commutator \(0.22729901088344\), and no
candidate appeared.

This is not an exact extension of C40. It leaves open other points of the
circle, other \(d=4\) solutions, and the possibility that the optimizer
missed a zero.
