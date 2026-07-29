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
