# PR203 independent exact algebra / physical audit

No scoped mathematical counterexample or proof gap was found. The independently reconstructed exact result is the complete displayed N=4 family for every finite real M. The all-N conclusion additionally relies on the audited original analytic proof and credited published inputs. Finite numerical checks do not establish that conclusion. Original checker optimization and historical runtime provenance need qualification.

## Independence and scope

The plan was frozen at actual UTC 2026-10-16T07:32Z before original proof/code or favorable reports. Completed independent derivation/computations were frozen with hashes in tool output at 2026-10-16T07:39:31.576216Z before original proof/code access. Errno28 delayed the filesystem receipt; INDEPENDENT_FREEZE.json records both times. No sibling checkpoint or other PR was read.

Scope: a>b>0, fixed proper nested confocal elliptical caustic, primitive LEAST period N divisible by 4, signed original-trajectory and side-LINE pedal areas, all fixed finite real M, coprime stars, reversal and zero/negative pedal areas. No converse, hyperbolic extension, or padding-based extension is assumed. Primary Table3(arXivv11 p.6/journal p.346) literally says N=0mod4/allM, without literally printing least period.

## Exact independent reconstruction

INDEPENDENT_DERIVATION.md and physical_audit.py prove the displayed family
P=(ax,by), Q=(-a³y/D,b³x/D), -P,-Q,
D²=b⁴x²+a⁴y², x²+y²=1, D>0,
has caustic lambda=a²b²/(a²+b²) and product

    A B_M = 8 a⁴ b⁴/(a²+b²)².

Exact polynomial reductions verify boundary, both tangent side types, squared reflection and the strict positive sign margin D²-(a²-b²)²x²y²=(b²x²+a²y²)². Thus the squared tangential-velocity identity is unsquared reflection. The map sends Q to -P; det(P,Q)>0 gives nondegeneracy and least period 4. Strict nesting puts tangent contacts strictly inside chords. Direct arbitrary-M projection/shoelace algebra cancels M for any parallelogram. Reversal reverses both areas. Seven symbolic checks occur in each final run.

A real coefficient mutation8->9 is rejected by the exact product identity under ordinary Python and -O; mutation stdout and mutation_results.json retain both nonzero exits. Fresh code uses explicit exceptions throughout, so enforcement survives optimization.

## Independent physical diagnostics

The generator uses no Jacobi functions. It scales to the caustic unit circle, constructs a tangent contact, maps back, and takes the second outer-ellipse intersection. Bisection selects lambda by accumulated winding. It separately checks closure, winding, numerical least-period separation, both conics, strict interior contact, tangency, reflection and direct perpendicular projection onto complete original side lines.

Final ordinary and -O runs each pass 107,962 explicit checks, including 468 phase-product comparisons (many remaining checks are per-vertex/projection checks). They cover 39 caustics: a/b=1.0001,2,10 with b=1; N=4,8,12,16,20 and every coprime0<w<N/2; four phases0,.173,.731,1.417; M at origin, focus, generic(a/3,-.7), and large(100a,-53). Reversal and triple traversal are checked. At200  digits/600 bisections, maximum scaled phase-product error is2.81e-159, closure6.78e-159, reflection4.50e-159. These are noninterval diagnostics. The first85digit/215bisection run stopped at elongatedN16,w7 with reflection residual1.11e-48 versus1e-48 tolerance; higher precision resolves the conditioning issue. Both failure stdout logs remain.

Supplementary signed_edge_checks.py passes2000 explicit checks per mode: fixed zero/negative pedal M across four phases, all six quadratic-in-M coefficients across phase, and product scaling by9 for triple traversal. At a=2,b=1, N8,w3 has zero M approximately(1.55973422080334,.779867110401671); twice that M yields AB approximately-9.61342353840712. N12,w5 has zero M approximately(1.54924766004668,.774623830023341); twice that M yields AB approximately-9.56045349013426. Residuals are below 1.08e-176; these are numerical roots, not exact certificates.

Excluded padding tests exhibit variation: primitiveN3 repeated tolength12, N6 repeated tolength12, N5 repeated tolength20, at a=2,b=1,M=(.2,.3). RepeatedN6 has sampled AB range[78.2441700960,79.9489001308]. This substantiates preserving least period, without proving a parity converse.

## Full original proof / dependency audit

After freezing independent evidence, the complete original PROOF.md, verify.py and independent_checks.py were read. No flaw was found in the following chain:

- Radial projection identity: linear M terms cancel by opposite-line pairing, quadratic tangent terms telescope with coefficient |M|²/8. Half-determinant factors agree.
- Stachel published Thm4.3/(4.9), p.1614, supplies canonical k=sqrt(alpha²-beta²)/alpha, v=2Ktau/N, a=alpha dn(v)/cn(v), b=beta/cn(v). These imply the same confocal lambda and cover coprime stars. Contact half-shift agrees with tangency.
- Universal signed-area coefficient AB sn(v)cn(v)/dn(v) follows from addition formulas and is positive on0<v<K. Contact area does not vanish for the allowed real stars.
- Projection normal norm dn²/beta², removable sn/cn/dn poles, order-two dn-zero poles, evenness about K+iK', and the quarter-period signs are consistent with bilinear meromorphic continuation.
- Singular-vertex grouping reduces the cyclic area to simple poles even at simultaneous antipodal singularities. Adjacent singularities are excluded; incident-edge groups are disjoint. Reduced real periods and imaginary anti-periodicity are correct. The comparator has nonzero residue because every real translate occurs twice with the same sign. Two-pole cancellation, compactness and anti-periodicity yield proportionality, including zero coefficient. ForN=4n, K is a cyclic translate. No circularity was found.
- Chavez-Caliz Thm3/6 supplies the even-period area product for concentric ellipses in complex-projective general position. The submitted x²=a²alpha²/c², y²=-b²beta²/c² and determinant lambda c²/(a²b²alpha²beta²)>0 prove four finite transverse intersections. Contact/outer polarity has determinant alpha²beta²/(a²b²), with correct normalization and no infinite real outer vertex.

All four local primary-PDF hashes match source_manifest.json. DLMF shifts/poles and addition formulas were checked directly at https://dlmf.nist.gov/22.4 and https://dlmf.nist.gov/22.8. Those sources support the proof's stated constants/signs. No favorable historical verdict or shared-author sibling was used as proof support.

## Original receipts and enforcement

All 11 author manifest file hashes and all 5 reviewer manifest file hashes match, including proof/code and reviewer binding to author manifest. Original tree retains verification.json, author_replay.json and independent_receipt.json, but no raw stdout/stderr. Historical JSON lacks exact command, Python/package versions, timing and optimization state.

Both original scripts have two static assert sites, one exact helper and one numerical helper. Under -O all assertions disappear while counters continue incrementing. Advertised 21,419 exact / 2,691 numerical author counts are therefore compatible with ZERO enforced assertions. Reviewer has the same defect. The fresh exception-based code retains enforcement.

The first disposable shadow replay ended exit120 with empty runner stdout during APFS exhaustion; only the initial shadow code/proof were created. This is an infrastructure failure and establishes no mathematical failure or successful replay. RAM-captured replays of unchanged code bytes completed successfully; only the intended result-JSON writer was intercepted. Synthetic __file__ names and the working directory stay inside the own-folder disposable shadow. Archived originals are never modified.

## Limits

No mathematical rejection is justified by this audit. The independent exact theorem reconstructed here isN=4; finite physical checks corroborate selected higher periods. All-N acceptance relies on the full audited analytic proof and credited area-product theorem. This is not a novelty certification, interval proof or certification of arbitrary historical runtime execution. Preserve signed areas, side lines, fixed finite real M, proper elliptical caustics, least period and shared-author attribution in any promotion.

## Completed replay findings

REPLAY_SUMMARY.json and ram_author_replay.json / ram_reviewer_replay.json retain actual ordinary and -O commands, UTC times, Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0, executed-source hashes, stdout/stderr and captured JSON. The unchanged ordinary author and reviewer stdout are byte-identical to their archived JSON receipts, including all group counts and maximum errors. Ordinary author enforces 21,419 exact plus 2,691 numerical assertions (24,110 total); reviewer enforces 19,039 plus 1,539 (20,578 total). Each compiled ordinary checker has two assertion sites. Under -O both have zero sites/enforced assertions while advertising all the same counts.

An actual author expected coefficient was changed from coeff to coeff+1; the reviewer exact four-period product was changed from 165888/625 to false 165889/625. Both ordinary runs reject their false mathematical identities. Both optimized runs incorrectly return PASS with unchanged advertised counts. This independently demonstrates the checker-enforcement defect; it does not refute the written theorem. Fresh independently authored code rejects coefficient 8->9 in both modes.

The initial assertion-opcode metadata counter recognized only the pre-3.14 LOAD_ASSERTION_ERROR name and incorrectly reported zero even for ordinary Python. It was corrected without rerunning successful mathematical checks to recognize Python 3.14 LOAD_COMMON_CONSTANT AssertionError. Receipts retain the initial value, correction explanation, statically verified corrected values and execution-time transport hash. ram_replay_execution_transport.py preserves byte-identical execution-time capture code; ram_replay.py has the corrected counter.

Audit completion estimate: 100% of the assigned exact-algebra/physical/provenance audit. Strongest independently constructed exact theorem remains the displayed arbitrary-M N=4 family; no general-period theorem is inferred from numerics.
