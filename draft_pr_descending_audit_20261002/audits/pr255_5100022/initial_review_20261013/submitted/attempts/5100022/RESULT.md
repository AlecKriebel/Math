# Result: full source-target candidate for k404

**Author turn 1/5; independent review pending. No novelty claim.**

For a strict noncircular confocal elliptic billiard with primitive period N=2 modulo 4, including primitive stars, the signed area of the original orbit's antipedal polygon about either original focus is a constant multiple of its original-side focal pedal area.

Every focal antipedal intersection is finite. The focal pedal area is strictly positive for the orientation 0<tau<N/2, so the source quotient is defined everywhere in the stipulated family. The constant may be zero; antipedal numerator zeros are allowed. Both foci give the same value.

## Mechanism

- Stachel's canonical coordinates and a direct line-intersection calculation produce an explicit meromorphic focal antipedal formula.
- The only possible area poles arise from adjacent original vertices and have order at most two.
- Even-period central symmetry, reversal with reflection, and the imaginary anti-period force odd Laurent expansions at those poles, eliminating every double-pole coefficient.
- The resulting area is a scalar multiple of the original-area cyclic dn trace.
- The credited focal pedal trace aligns with that same trace exactly for N=2 modulo 4.
- Positivity of every consecutive focal-pedal determinant follows because the focus lies inside the caustic and the contact normals turn by less than pi per step.

The complete proof, including both source editions, period arithmetic, pole completeness and denominator justification, is in PROOF.md. It reproduces the needed focal pedal argument rather than treating a related-target theorem as an automatic substitute.

## Evidence and limits

The checker passes 27,524 exact algebra/period controls and 27,320 separately labeled 90-digit diagnostics. It uses actual antipedal intersections and perpendicular feet, includes primitive stars, near-complex-pole tests and excluded-parity controls. Finite checks do not prove the all-period analytic theorem.

The strict source ensemble excludes circular and hyperbolic/degenerate caustics. Repetition cannot manufacture the primitive parity; repetitions of already-admissible primitive orbits preserve the ratio. Area is signed shoelace area. No statement about unsigned filled regions, arbitrary antipedal centers, or neighboring table invariants is included in the source-target conclusion.

Independent adversarial review is required before a result PR. Source PDFs, extracted full texts, table images, complete imported records and exploratory probes are excluded from the portable packet.
