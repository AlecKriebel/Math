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

## Representation-only parity mechanisms

Central ranks, Markov weights, Bratteli multiplicities, one-sided tower
embeddings, determinants, the complex quaternion algebra, and naive
Frobenius--Schur/Brauer arguments all permit \(d=2s\) with odd \(s\).
Consequently none can prove \(4\mid d\) without an additional theorem using
the simultaneous tensor placements \(P\otimes I\) and \(I\otimes P\).
See `notes/track_coherence_parity.md`.
