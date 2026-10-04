# Validation and limits

## Checked analytically in the candidate

- The torus skew shift is well-defined and preserves area.
- Fourier coefficient orbits prove ergodicity; a separate orthogonal Fourier orbit disproves almost periodicity.
- The suspension quotient is a smooth compact mapping torus, with globally descending closed forms.
- Adding a circle produces a closed nondegenerate symplectic form with total volume one.
- A real-valued smooth cutoff Hamiltonian has unit suspension speed on a band of volume 1/4.
- A globally descending frame gives the exact derivative shear and two-sided polynomial norm bounds in all four directions.
- Fubini, rational-time invariance, strong continuity, and suspension ergodicity classify invariant measurable subsets of the band modulo null sets.
- The orthogonal orbit persists on every such positive-volume subset, excluding all almost-periodic regions.

## Exact reproducible controls

`verify.py` runs 3,248 exact checks with Python rational/integer arithmetic. It checks return-map formulas including negative iterates, composition, area and four-dimensional symplectic matrices, Fourier index transport, finite segments of distinct coefficient chains, orthogonality indices, frame gluing, derivative/inverse formulas, Hamiltonian contraction, cutoff plateau endpoints, and the band volume.

Six controls explicitly expose common invalid substitutions: the wrong frame sign, removing the shear, rationalizing the rotation, treating a circle coordinate as a global real function, neglecting the cutoff, and using only the clock eigenfunction as a noncompactness witness.

These are supplemental finite algebra checks. The proof's irrationality, infinite Fourier argument, smooth-quotient construction, smooth cutoff, measurable disintegration, and asymptotic Lyapunov conclusion require the written analytic arguments. No finite numerical simulation is used to infer those conclusions. Passing the script is not formal verification or expert review.

## Scope and outstanding validation

The compact smooth symplectic category is explicit. No result is claimed for an extra prescribed ambient manifold, a standard cotangent form, analytic Hamiltonians, natural kinetic-plus-potential models, contact-type energies, or robust/generic examples. The flow is not weakly mixing; the problem's stated existential question does not require that.

An independent mathematical and source-scope audit is required before remote publication. The bounded source search has not established first priority. The standard ingredients and this construction should not be advertised as novel without a substantially deeper historical check. Any 'claimed_solved' designation remains a provisional manuscript status, not certification.
