# Scope and inference audit

This is an internal-to-the-packet mathematical scope check, not an independent referee report.

## Statement and assumptions

1. K3's actual 2026 author manuscript was inspected at printed/PDF page 164. The local problem statement agrees with both parts. The workshop-report URL in the inherited bibliography was not treated as the current book.
2. No nondegeneracy or genericity assumption was added to either universal question.
3. Inclusive spectral ellipticity was made explicit using the convention in K3's cited Abreu–Macarini paper. K3 itself gives no local definition. The strictly-nonreal alternative is distinguished by the round Hopf example.
4. Dynamical convexity belongs to the strictly convex subclass, not arbitrary standard-contact forms. Symmetry, Hessian pinching, and finite-orbit assumptions remain explicit extra hypotheses.
5. The highest-recency source, Shibata's September 2026 manuscript, is labeled a preprint. Its result is not mistaken for elliptic existence and is not used to prove our reductions.

## Proof checks

- In Sp(2,R), the characteristic polynomial gives exactly the claimed trace trichotomy. No higher-dimensional version is inferred.
- Hyperbolicity of every simple orbit implies nondegeneracy of every cover. Ellipticity of a cover implies ellipticity of the simple orbit.
- ECH generators are orbit sets, not individual orbits. The finite and filtered counts use multiplicity-one admissibility only for hyperbolic simple orbits.
- The Weyl-law count gives a lower bound on N(L). No equality, upper bound, or contradiction for infinite sets is claimed.
- All Lefschetz conclusions are conditional on a C1 closed-disk return map with no periodic boundary points. No unproved boundary extension from an arbitrary global section is used.
- Negative hyperbolic fixed points have index +1 for odd iterates and −1 for even iterates. The formal period-doubling pattern satisfies every Lefschetz identity but is not claimed realizable.
- The positive-Hamiltonian construction has exact endpoint diag(−2,−1/2). Its index statement uses the lifted angle along an eigenvector and the hyperbolic iteration formula. Smoothing preserves the endpoint type and index, not the exact matrix. No realization as a convex hypersurface's complete orbit spectrum is claimed.
- The Anosov criterion retains both uniform hyperbolicity of periodic-set closure and stable/unstable transversality. The formal family with periods j demonstrates why multiplier separation is not a uniform exponential rate.
- Bounded-period compactness uses C2 convergence of contact forms to obtain C1 convergence of Reeb fields. Positivity of the limiting period is justified; multiple covers in the limit cause no loss of inclusive ellipticity.
- The symmetry-distance formula concerns coefficient functions in a fixed contact trivialization and a fixed antipodal involution. It does not rule out all possible contactomorphic symmetry representations.

## Reproducibility

`verify_exact.py` was run normally and with Python optimization. Outputs agreed byte-for-byte. It checks the rational quarter-turn product, 64 powers and their fixed-point-index signs, the all-iterate formal model through n=512, ten dyadic recurrence instances, 511 index-gap inequalities, and five trace-type controls. The report's elementary proofs, not these finite tests, justify the infinite statements.

## Acceptance conclusion

Accept as a carefully scoped partial-results/failed-approach record, subject to independent mathematical review. Reject any label claiming a solution, a realized counterexample, or proven novelty. Both universal subquestions remain open in this work. Source acquisition, current-status checking, and this audit do not add mathematical approaches to the five recorded in the report.
