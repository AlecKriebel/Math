# Frozen independent claim map — physical Cartesian geometry family

Frozen UTC: 2026-10-15T11:56:58Z. Source head: `2180d64b648b81ac660a792f7823d0b715f9cf12` (PR 210 / 5100033).

Independence boundary: this map was written after reading INTAKE.json and the immutable original PROOF.md and SOURCES.md only. No inherited independent_review document, numerical report, verify.py, other current review, or root notes has been read. The supplied parent task is the audit scope, not mathematical evidence. No novelty claim is assessed.

## Exact falsifiable target

For every strictly nested confocal elliptic caustic with a primitive odd-period billiard family, including primitive stars, take the outer polygon formed by intersections of consecutive tangents to the original boundary ellipse. Project the original ellipse's two foci onto that outer polygon's ordered side lines. The product of the two signed shoelace areas must be independent of orbit phase. Reflection/closure/caustic tangency and true outer side lines must hold before a numerical case can count as a theorem test. Hyperbolic, collapsed, repeated shorter, and exactly circular cases are controls or limits, not counterexamples to the stated domain.

## Independent mechanism to develop

1. Represent a boundary vertex by Cartesian coordinates. Its tangent line is `(x/a^2,y/b^2) dot X = 1`. Construct actual outer vertices by solving adjacent tangent intersections, recover their side lines, and project foci using the Euclidean point-to-line formula. Derive the focal-pedal map and auxiliary-circle identity independently from that geometry.
2. Trace real billiards by reflecting a chord direction in the ellipse normal and solving for the next boundary hit. Determine a periodic confocal caustic independently by a real geometric closure solve or exact rational/algebraic constructions; do not merely replay an author's Jacobi-foot evaluator.
3. Check caustic tangency and reflection for every resulting orbit, signed area order and winding for stars, focus pairing, orientation reversal, cyclic shifts, rigid motions, scaling, near-circular/eccentric/near-boundary regimes, and even-period non-invariance controls.
4. Seek exact algebraic triangle/pentagon examples if feasible. Numerical results alone are evidence, not a universal proof or interval certificate.

## Claims requiring proof audit

* Canonical coverage: the cited Stachel theorem must actually cover all strictly nested elliptic caustics and primitive star turns with the displayed modulus and semiaxis relations. Check modulus-vs-parameter conventions and existence/range of the canonical step.
* Geometry-to-function bridge: outer side lines are precisely the original tangents in the correct cyclic order, and consecutive intersections are finite for allowed shifts. A non-antipodal canonical phase shift must imply non-antipodal geometric vertices, even for stars.
* Rational foot map: the cancellation has the correct sign/focus and no lost real denominator or complex pole. The second focus must be a half-real-period shift, with determinant signs accounted for.
* Pole claim: Jacobi common poles removable; all denominator zeros simple and exhausted; two displayed poles have collinear opposite residues. Imaginary translation changes the relevant vectors as stated.
* Collision claim: simultaneous singular adjacent endpoints really occur and may cancel only the double coefficient. Explicitly inspect N=3, whose cyclic neighbor structure can identify the two other incident edges; do not assume generic N>=5 indexing. Check no extra pole coincidences occur modulo the full lattice or reduced lattice.
* Analytic symmetries: reduced real period from gcd, imaginary anti-period, reflection-even character, and chosen center must all be literal identities of the meromorphic continuation.
* Divisor inference: every alleged zero must be regular; no hidden multiplicity, coincidence, or unjustified nonzero assumption may enter. The pole-free case must be handled separately. Check the half-real-period shift exchanges poles and zeros on the correct doubled imaginary torus.
* Odd parity: verify the congruence and focus pairing; even periods should yield equal individual areas and generally varying product, so a test setup that also makes even products constant is suspicious.

## Initial adversarial status and success criteria

The theorem is a hypothesis. The submitted proof has a plausible two-pole character argument, but no step is accepted solely because it is written. No defect is established at freeze. Strongest verified result so far: the target and supplied proof dependencies have been identified. Completion estimate: 10% toward an independently checkable adjudication, not toward proving the conjecture true.

Deliverables: a standalone deterministic physical-geometry program, exact algebra where achievable, saved results, standalone REPORT.md with every proof gap and strongest verified claim, UTC research log with completion estimates, and an authored-file hash manifest excluding itself and private inputs. No Git/provider/SQLite mutations, outreach, or other-shard communication.
