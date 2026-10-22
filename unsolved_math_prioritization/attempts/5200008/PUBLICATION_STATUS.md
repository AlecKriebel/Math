# Publication status and moving-domain clarification

2026-10-03 UTC. Problem 5200008 / AMR-051-0008 remains **unsolved, five attempts**.

The nine frozen author files in `public/` and seven independent review files in `audit/` are preserved unchanged. Statements that review was pending in the frozen author files describe their earlier freeze. The completed [independent audit](audit/AUDIT_REPORT.md) passes the conditional reduction and restricted partial results with no blocking findings. Its 1,682 independently implemented exact controls pass, and the author's 1,682 controls replay byte for byte. These are AI-assisted mathematical reviews and finite exact checks, not a formal proof-assistant certificate or human peer review.

The full reflection-only density problem with arbitrary nonsymmetric small deformations and unbounded word lengths is still open in this attempt. No construction of the base inverse and no obstruction covering that full class has been established. The abstract matrix model has no claimed optical realization. No novelty or priority is asserted.

## Clarification of the moving-domain extension

The audit recommends making the cutoff in Proposition 4, Step 4 explicit for an isotopy F_t from an initial domain V to moving domains V_t. Work in the open spacetime domain D={(y,t):y in V_t}, relative to M times [0,1]. For a compact K contained in V, its trace L={(F_t(x),t):x in K,0<=t<=1} is compact and lies inside D.

Choose a smooth spacetime cutoff chi compactly supported in D and equal to one on a neighborhood of L. Multiply the time-dependent Hamiltonian on D by chi and extend it by zero outside D. This is smooth; its support projects into one compact subset of M. The resulting Hamiltonian flow agrees with F_t on K by uniqueness of solutions. A spatial cutoff whose support lies inside every moving V_t is not needed. For the main self-map assertion, where all V_t equal the phase cylinder, the spatial cutoff in the original argument is already sufficient.

This supplies the audit's optional clarification without changing the frozen proof, its scope, or the unresolved status.
