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
