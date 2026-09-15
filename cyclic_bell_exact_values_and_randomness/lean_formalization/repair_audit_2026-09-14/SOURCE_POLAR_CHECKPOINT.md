# Source/polar coverage checkpoint

2026-09-14 (local research session), best estimate 80% of the source appendix
formalization complete; this excludes independent global qa/qc closure work.

Normal Lake builds have now checked the repaired GeneralSourceFourier and new
GeneralCoveragePolarAlgebra, GeneralCoverageCovariance, SourcePolar,
SourceInterpolation, SourceWeyl, SourceLiteralInterpolation, SourceFactors,
SourceCanonical, SourceOrbit, and SpectralMeasurement modules.

Strongest checked result: the literal source cosecant coefficients define a
unitary matrix for every d≥2. Its transpose is the finite functional calculus
of the actual source W_y, with scalar function exactly conjugate((1+z)/|1+z|)
on every spectral point, multiplied by Z†. The source pencil L_y=Z+chi(y)X has
an explicit positive, invertible modulus, identified with CFC.sqrt(L_y† L_y).
The literal source Bob matrix is entrywise conjugate to its unitary polar
factor. All scalar signs, phase order, transposes, and d−1 wraparound were
proved, not numerical assumptions.

Generic finite-order unitaries now produce actual d-outcome Measurement
objects whose positivity, completeness, orthogonality, idempotence, and exact
encoding are all proved via spectral projectors. Source order is the next
bridge: SourceOrder is drafted and compiling using the parent's checked
ordered noncommutative twisted-product lemma and the checked scalar orbit
product. Actual source strategy/attainment endpoint follows it. Full simple
spectra are under independent investigation by the Fourier agent.

No axiom or sorry was added. Final clean rebuild and transitive axiom audit are
still required by the parent task, so this is an implementation checkpoint,
not a final certification claim.

## Verified follow-up checkpoint

2026-09-14, best estimate 95% of source appendix coverage complete; remaining
work is the independently assigned exact full simple-spectrum statement.

SourceOrder and SourceStrategy now both pass normal Lake builds.
`sourcePhysicalStrategy_attains` constructs the actual maximally entangled
state, source Z/X Alice PVMs, literal source-coefficient Bob PVMs, and extra
Z† PVM, and proves the physical firstValue equals 2/sin(pi/(2d))+1 for every
d≥2. This closes the previously missing source-validity and actual-attainment
chain. SourceCanonical also proves the exact inverse formula and actual
relative modulus. SourceEndpointAxioms.lean checked every central new endpoint;
all use only propext, Classical.choice, and Quot.sound. The output is retained
in source_endpoint_axioms.log. No hidden endpoint premise, sorry, new axiom,
or computational trust shortcut was introduced.

The top-level `GeneralCoverageSourceStrategy` import includes the whole source
implementation chain. Parent integration and final clean rebuild remain
separate release checks.

Final bounded-task checkpoint: 100% of the source appendix coverage is now
implemented and normally compiled, including the separately authored exact
full simple spectra. The latter received independent semantic review of all
clock, phase, and transpose conventions. Final global clean-build acceptance
remains parent-owned.
