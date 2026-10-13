# Fresh whole mathematical adversarial review: PR261 / 5100021

Completed 2026-10-12 10:15 UTC. Review completion estimate: 100%.

**Decision: PASS for the theorem explicitly stated in PROOF.md, with SOURCE QUALIFICATION REQUIRED before calling it an unqualified solution of the imported wording.** No mathematical gap or counterexample was found for a noncircular ellipse, strict nested nondegenerate confocal elliptical caustic, least primitive N divisible by four, both original foci, original chord-line pedal feet, original vertex antipedal line intersections, and cyclic signed areas. The proof covers primitive stars, N=4 simultaneous singular coincidences, all real phases, negative antipedal area, and identically zero products. Novelty and priority were not assessed.

Submitted PROOF.md reviewed SHA256:

    f7aada9e28e92c6fab920f1330366acd6eaba8006b4cd0ce52e2dbd58e7ef5b9

## Independent attack and strongest verified result

The independent plan was recorded before proof/verdict exposure. Complete PROOF.md, target/source files, and the primary source definitions/tables were read; submitted checkers were read but not executed. I then built separate exact direct-geometry, triangular polynomial-remainder, local-series, and complex stress artifacts. The full analytic reconstruction was frozen at 10:11 UTC before reading the current elliptic, geometry, and reproduction/source review reports.

The sealed derivation establishes:

- Every admitted confocal ellipse pair is represented by the stated Jacobi coordinates; strict nesting determines a unique v in (0,K). The real parameter covers every starting point, and least period implies gcd(N,τ)=1 with 0<τ<N/2. Arbitrary primitive winding is retained.
- The rational antipedal formula satisfies both actual original-vertex line equations. Its normal determinant is strictly positive on the entire real family. The focal pedal formula is the direct Euclidean projection onto the original chord line, and all real vertices are finite.
- The complete antipedal pole support comes from the two simple roots of L=1-k²s²sn²(x), with all common Jacobi poles and the apparent focal factor removable. On the reduced torus only two imaginary pole classes remain. Every area summand has order at most two.
- Evenness plus imaginary antiperiodicity makes the antipedal Laurent germ odd at each allowed pole and eliminates its double term. This argument includes all cyclic edges when N=4 makes every antipedal vertex singular simultaneously; it does not presume separated singular pairs.
- The pedal's sole inverse-image pole is a double vertex pole with even germ and leading vector (2/k)(1,i). Its two regular incident neighbors occur as an odd difference, reducing the area pole to order at most one. No adjacent singular vertex or omitted closing edge occurs, including N=4.
- The dn trace has exactly two simple poles with noncanceling residues -2i and +2i. Matching known trace residues gives both area representations without dividing by either area or a possibly vanishing coefficient.
- Primitive parity makes the two traces differ by h/2. Evenness and antiperiodicity locate exactly the complementary simple zeros, so the trace product is holomorphic on the compact torus and constant. Positivity of real dn makes that trace product positive.
- The pedal signed area is strictly positive for positive ordering, including stars. The antipedal trace coefficient can vanish; no step divides by it. Reversal and scaling behave as claimed.

The strongest verified conclusion is therefore the **full all-parameter, all-period theorem in the proof's explicitly stated primitive domain**, not merely low-period or numerical evidence. The exact remaining mathematical gap in that domain is **none found**.

## Exact source-scope finding

The two primary Table 5 editions agree on original focal product k403,b and N congruent to zero modulo four. Signed areas and self-intersecting antipedals are explicit. Neither table, imported statement, nor a whole-text qualifier search literally supplies “least period.” Context supports an intended unrepeated winding-one family: N is said to determine a distinct caustic, and the numerical method starts N vertices evenly around the ellipse. The primitive convention is a defensible interpretation, but must be presented as such.

The submitted TARGET.json `source_correction` says both source tables and pinned record agree on **least** period. That is an overstatement of literal source evidence. The source gate and “complete source-matched” framing should distinguish the proved primitive formulation from a closure-only reading.

An independent exact certificate uses outer axes a=3,b=1 and caustic parameter λ=9/16. Two distinct phases of the same primitive six-bounce family have products -9261/64 and -10125/64. Listing each orbit twice produces twelve-step closed sequences with products -9261/16 and -10125/16, whose difference is **54**. The certificate verifies outer incidence, common-caustic tangency, actual specular reflection, distinct primitive six vertices, finite focus-normal determinants, direct original projections/intersections, both foci, and doubling of both signed areas under repetition.

This is an exact counterexample to an unrestricted closure-only interpretation of N=12, **not** to the least-period theorem. Recommended scope wording is: “We prove the primitive least-period formulation of source row k403,b, under the conventional unrepeated interpretation of N-periodic. A closure-only interpretation is false.” If the repository intends the imported target to include padded sequences, that target requires correction rather than unqualified solved status.

## Independent computations and limits

- `independent_symbolic_audit.py`: PASS for both actual antipedal line incidences, focal normal determinant, both pedal projection coordinates, unit-circle identity, and the quarter-shift leading vector. All polynomial checks use exact triangular quadratic reductions.
- `independent_exact_geometry.py`: PASS for the exact six-orbit/repeated-twelve scope counterexample above. This is a proof certificate using exact radicals, not numerical phase samples.
- `independent_complex_stress.py`: PASS at 115 decimal digits for N=4,8,12,16,20,28,44, high primitive star windings, k=.001 and .9999, regular complex phases, both foci, symmetry, and points 10^-14 from the antipedal and pedal pole rows. Maximum scaled discrepancy: 2.245432537e-69. Local zB remains bounded and z²B tends to zero, including N=4. These are non-interval diagnostics and do not prove all N.

The theorem excludes circular, degenerate, hyperbolic, grazing, and infinite-semiaxis endpoints. No excluded limit was used to prove an admitted case. All claimed nonzero denominator-leading coefficients are nonzero for every admitted fixed parameter.

## Post-freeze contradiction audit

After freezing my derivation, I read `elliptic_divisor_adversary/REVIEW_REPORT.md`, `geometry_adversary/GEOMETRY_REVIEW.md`, and `reproduction_source_adversary/SOURCE_AUDIT.md`. Their mathematical and source conclusions agree with the frozen result. The elliptic report's contact-phase pole classes become exactly my original-phase classes after adding v; there is no phase-convention contradiction. Its explicit local residue checks supplement, rather than replace, the global odd-germ proof.

I independently rechecked the geometry report's exact N=8 zero-area witnesses using my own direct geometry routines, after learning the construction from that report. For its continuous r-family, both symbolic first-quadrant caustic tangency residuals are zero. At r=3 the antipedal area is 56sqrt(6)/81>0; at r=5 it is -10064sqrt(30)/625<0. Exact outer incidence, tangency, and specular reflection pass for both witnesses. Throughout the interval the geometry stays admissible and intersections finite, so continuity proves a genuine admitted zero signed antipedal area, and the independently verified trace lemma makes it identically zero in phase. This post-exposure verification is clearly separate from the independent freeze.

The proof's reference identity for the original area was also checked: the endpoint determinant is 2absc dn(x)/L, while the sum of endpoint dn values is 2d dn(x)/L; cyclic summation gives A=absc T/d. A direct exact replay of both supplied N4 examples verifies their common ellipse/caustic, reflections, stated areas, and common product 256/25.

The source report's independent repeated-six counterexample uses a different ellipse and agrees with mine about the essential qualifier. Its literature information was encountered during comparison but was not verified or used to make a priority verdict. A later external claimed proof does not strengthen or weaken the submitted theorem's mathematical verification by itself.

## Artifact and reproduction index

- `INDEPENDENT_PLAN.md`, `RESEARCH_LOG.md`, `INDEPENDENT_FREEZE.json`: exposure order, timestamps, completion estimates, and frozen decision.
- `INDEPENDENT_DERIVATION.md`: full independent analytic reconstruction, complete pole divisor, local cancellation, parameter coverage, and exact scope counterexample. Frozen SHA256: `07183ecf53f9f4ad094b5418601a92e04fb2d26c22334c5dc1770871f3c7051e`.
- `independent_symbolic_audit.py`, `SYMBOLIC_AUDIT_RECEIPT.json`: exact direct-line/projection and local-series audit.
- `independent_exact_geometry.py`, `EXACT_GEOMETRY_RECEIPT.json`: exact repeated-period counterexample.
- `independent_complex_stress.py`, `COMPLEX_STRESS_RECEIPT.json`: direct real/complex falsification diagnostics.
- `post_freeze_zero_witness.py`, `POST_FREEZE_ZERO_WITNESS.json`: explicit post-exposure cross-audit of real zero products.
- `post_freeze_reference_controls.py`, `POST_FREEZE_REFERENCE_CONTROLS.json`: exact original-area reference and both N4 examples.
- `requirements.txt`: SymPy 1.14.0 and mpmath 1.3.0. Install these into local `dependencies/`, then run the scripts from this directory or any working directory. The scripts locate their local dependencies automatically.

Primary PDFs were read from the existing local source folder and their hashes match the submitted manifest. Rendered source pages and installed dependencies are private/ignored local reading aids. No Git mutation, remote write, PR action, external communication, or change outside this assigned folder was performed.
