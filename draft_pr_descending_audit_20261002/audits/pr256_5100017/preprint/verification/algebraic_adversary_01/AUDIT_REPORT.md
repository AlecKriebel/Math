# Algebraic adversary audit: PASS

Final status: **PASS for the submitted domain-qualified theorem** on every primitive even least period N≥4, real orbit phase, and confocal nondegenerate elliptic caustic in a>b>0, 0<λ<b². The centroid formula holds for every fixed real M where its signed-area quotient exists. No algebraic, sign, scaling, antipodal-symmetry, circularity, or domain error was found.

The strongest verified result is the all-period signed-area and signed-first-moment identity, not merely agreement of finite examples. The independent derivation is in `INDEPENDENT_DERIVATION.md`; exact and numerical reproducible checks are in `independent_verifier.py`, `EXACT_CHECKPOINT.json`, and `INDEPENDENT_EVIDENCE.json`. Initial falsifiers were preserved before reading the submitted proof or any prior review in `INITIAL_MECHANISM.md`. No submitted prior review or conclusions were consulted.

## Verified mathematical claims

| Claim | Independent verification | Status |
|---|---|---|
| T^(N/2)=R, exact least-period requirement | Finite commuting group is cyclic via its faithful circular-order action; unique involution | PASS |
| Positive successive normal-angle sine and S(0)>0, including stars | Origin lies strictly inside elliptic caustic; Gauss map preserves half-turn order | PASS |
| Adjacent-normal bilinear identity (5) | Chord support equation plus independent Cartesian coefficient reduction | PASS |
| F>0, F²−e²d²>0 | Both factors F±ed strictly positive in the entire open domain | PASS |
| Doubled-normal relation (7) | Exact support-square Laurent identity | PASS |
| Cyclic moment lemma (8) | Two edge telescopes, valid even at antipodal/coincident doubled normals | PASS |
| S(0)=D S_Z/2 and S_Z≠0 for d≠0 | Exact support/angle edge coboundary and S(0)>0 | PASS |
| Antipodal area and complete cubic moment (11)–(12) | Formal conjugation; extraction of all monomials; two exact coefficient coboundaries | PASS |
| Explicit centroid (2) | Raw moment divided by 6S, with signed translation identity and exact d elimination | PASS |
| N=4 and d=0 | Unrestricted-M raw rectangle shoelace; converse from antipodal S_Z=0 | PASS |
| Natural zero-area circle and its phase independence | Area factorization with strictly positive S(0),F | PASS |
| Simple even winding-one all-M statement | Convex twice-traversed doubled-normal polygon, plus N=4 converse | PASS |
| Noncircular exact 8/3 control | Exact ellipse/tangency/reflection checks, eight distinct vertices, signed winding certificate | PASS |
| Exact exceptional radius squared 123539/20736 | Exact constants and raw symbolic-M Cartesian projections | PASS |
| Orientation reversal, units, scaling, and d→0 limit | Algebraic sign/unit audit plus numeric reversal/scaling checks | PASS |

## Checkable evidence

The main verifier passed 68 exact assertions. Its raw exact star projections were computed with unrestricted symbolic M=(x,y), so this is a complete polynomial control for that orbit, not a few sampled centroid values:

    S(M) = −sqrt(30)(20736x²+20736y²−123539)/134784,
    T_x = −sqrt(30)x(41472x²+41472y²−272935)/109512,
    T_y = −sqrt(30)y(52992x²+52992y²−347633)/97344.

These agree exactly with (1) and 6S times (2). At M=(13sqrt(731)/144,0), S=0 and T_x≠0. The source centroid quotient therefore is genuinely undefined at this point. An extra exact ray-crossing certificate verifies winding three independently of floating angle accumulation.

The numeric generator is an independent mechanism: it constructs each tangent contact on the inner ellipse, intersects that line a second time with the outer ellipse, and tunes λ by period/winding bisection. It does not use the submitted verifier's Jacobi generator. All parameter tuning and orbit generation used 90 decimal digits. Independent Cartesian projection arithmetic then checked 141 families across all even N=4,…,30 and their coprime windings 1≤k<N/2, at aspect ratios 1.01, 1.7, 4.3; 564 real phases; and 2520 fixed-M cases, including 264 points on the exact-form zero locus. Ten families were near the degenerate boundary, with minimum b²−λ approximately 2.81×10^−24, while remaining strictly inside the audited domain.

Maximum normalized residuals: raw signed area 2.49×10^−15, raw moment 7.87×10^−14, reflection 6.68×10^−15, scaling 6.71×10^−12, and exact floating order-reversal cancellation. The numeric checks corroborate the written proof; they do not establish the all-period result by themselves.

## Four-period converse and candidate paragraph check

The text directly proves d=0⇒N=4, then says the N=4 case was already treated in its simple-family argument. For completeness, one can add the converse: if N=4 and d≠0, antipodality makes S_Z=0, contradicting S(0)=D S_Z/2>0. This is an immediate consequence of already proved identities. It does not require a theorem change or new hypothesis and is not a reason to fail the mathematical proof.

I directly read the complete `candidate_repair_01/PROOF.md` and verified that its only change from the submitted proof is the new N=4⇒d=0 paragraph. That paragraph gives an even shorter correct argument: n_2=−n_0 and h_2=h_0 negate both right-hand terms in (5) for the second edge while leaving its left-hand side equal to the first. Adding gives 2d h_0h_1=0, and positive supports give d=0. An independent Cartesian symbolic check found the summed right-hand side exactly zero. The paragraph is **PASS**, invokes no unproved later identity, and fully resolves the exposition observation. Hashes and the exact added text are preserved in `CANDIDATE_REPAIR_CHECK.json`.

## Preserved diagnostic failures and repair

The original double-precision generator exited normally with code 1 on its assertion threshold, first at aspect ratio 1.7, N=20, winding 9, phase 0, normalized raw-moment residual 1.7316632969461483e−7. A selective high-precision repair left a second double-generated family outside its cutoff and exited code 1 at ratio 4.3, N=28, winding 11, phase 0.317, residual 5.311199719618375e−8. The final all-family 90-digit generator passed. These were instabilities in an independent diagnostic generator and were not accepted as counterexamples to the theorem.

The first complete script snapshots were not retained before editing. A preserved minimal reproducer reconstructed from the original functions reproduces both originally observed residuals exactly and records the normal return. Recomputing only those two families with 90-digit generation reduces their worst raw-moment residuals to 1.1025968495928332e−14 and 3.52163460817876e−14, respectively. See `double_precision_failure_reproducer.py`, `DOUBLE_PRECISION_FAILURE_REPRODUCTION.json`, its raw standard output, and `DOUBLE_PRECISION_FAILURE_HISTORY.md`. No additional broad numeric run was performed after the completed controls.

## Boundaries and remaining gap

No proof gap remains within the assigned scope. The precise boundary is the submitted signed-area qualification: arbitrary star families with d<0 have a circle on which the centroid is undefined. An unqualified all-M conclusion including those stars would fail; the submitted theorem explicitly records and excludes that quotient's undefined locus. Hyperbolic/degenerate caustics, the circle, odd least-period padded traversals, and publication/priority claims were not promoted by this audit.

Assigned audit completion: **100%**. All authored work stays in this folder; submitted sources remain unchanged. No external communications or Git/index/ref/branch/native-provider writes were performed.
