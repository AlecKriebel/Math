# PR204 independent physical reproduction and original-checker enforcement audit

Verdict: **finite physical reproduction and exact low-period controls pass; both original verifiers fail closed only when assertions are enabled. Their optimized executions accept actual false mathematical identities.** This audit does not certify the universal analytic proof or novelty. Original custody remains exactly20 files,59343 bytes, matching the supplied original SHA256 manifest.

## Independence, scope and provenance

The falsification plan was frozen in FROZEN_PLAN.md before author scripts, the favorable review, Root's proposed mechanism or any prior203 target proof. I independently read RGK arXiv2004.12497v11 pp1-6 and final journal DOI10.1007/s40598-021-00174-y printedpp341-346; the final Table3 was also visually inspected. They specify two confocal ellipses, a>b>0, signed shoelace areas Eq1, original trajectory-side pedals Sec3.3, and k203,b: A*A_m, M=O, N not2mod4. The table does not literally state least period. The exact repeated-list counterexample below makes that clarification necessary. The historical question mark and imported OPEN-TRIAGE are not present-day openness or novelty certificates.

No author modules, Jacobi formulas or prior target proof were used to construct the fresh physical or exact controls. Original scripts were read after plan freeze solely for their separate enforcement audit. Reused infrastructure is the preexisting readonly SymPy1.14.0/mpmath1.3.0 runtime identified in receipts; no packages were downloaded, installed or copied. All runtime-dependent Python subprocesses set PYTHONDONTWRITEBYTECODE=1. Original unchanged scripts and the historical PROOF.md were copied only into disposable layouts; no original outputs were overwritten. The proof file was copied for the author's unchanged hash calculation, not analytically cleared by this audit. No repository/index/ref/branch/native/PR/UI/tracker/publication or external-person communication occurred.

## Direct physical evidence

physical_shooting.py uses a Euclidean construction. Map the inner ellipse with axes sqrt(a²-lambda),sqrt(b²-lambda) to a circle, construct its tangent from a boundary point, map the contact back, and use that inward chord direction. Each subsequent bounce solves the second outer quadratic intersection and reflects velocity in the outer normal. A bisection in lambda solves the accumulated physical angle advance 2*pi*m over N bounces. No elliptic-function parametrization is used.

The final ordinary and optimized executions have identical stdout. At85 digits,63 primitive winding/shape cases produced378 orbits: five forward phases0,pi/2,.17pi,.41pi,.73pi plus reversal at.17pi. Aspect ratios are1.01,2,8. Tested periods are3,4,5,7,8,9,12,16, and excluded controls6,10; every coprime winding0<m<N/2 for these periods was included. There are54 target-parity cases and9 excluded cases. Every bounce has positive chord length, outer-ellipse membership, caustic discriminant zero to tolerance, unit reflected speed, equal/opposite normal components, equal tangent components, and a perpendicular origin foot. Every orbit has numerical position/velocity closure and no earlier numerical return. The minimum-return test is a finite numerical least-period diagnostic, not an interval proof.

Largest target product relative phase spread is1.28268628462e-58; largest scaled position closure residual7.12385249512e-58; largest normalized caustic tangency residual8.36211776817e-69. Reversal negates each signed area while retaining their product. These are noninterval diagnostics. Tested forward products are positive; neither zero products nor arbitrary negative product regimes were independently exhausted. Complex analytic chart/pole completeness belongs to the separate proof audit.

Moving the foot base to(a/7,b/9) breaks odd-period products (for example aspect2,N3 relative spread.0822349). Clipping the perpendicular to each finite segment breaks targetN4 (aspect2 relative spread.0277752, whereas its complete-line product varies below7.44e-76). Feet can lie far outside their finite segments; maximum observed projection-parameter excursion is28.2156581057. An unsigned-product extension is not refuted here: tested forward areas are positive and reversal changes both signs.

## Exact controls and exact scope counterexample

exact_low_period.py passes209 explicit-exception checks, identically in ordinary and optimized execution. For each of six polygons it verifies exact outer membership, vanishing common-caustic tangent discriminants, reflected incoming direction parallel to outgoing direction, **positive** dot product of those directions, perpendicular origin feet, proper0<lambda<b², signed positive areas, and distinct vertices establishing least physical period. It uses exact radical algebra, not numerical acceptance of a residual.

For axes(a,b)=(2,1), the primitive4 caustic is lambda4=4/5. The axis diamond has(A,B)=(4,32/25); the other axis-symmetric rectangle has(A,B)=(16/5,8/5). Both give product128/25. More generally the same construction has lambda=a²b²/(a²+b²), rectangle coordinates(+-a²/sqrt(a²+b²),+-b²/sqrt(a²+b²)), and product8a^4b^4/(a²+b²)²; the executable exact comparison is specialized to2,1.

For primitive3, put D=sqrt13, c=(1-D)/3, d=(D-4)/3. The two exact phases have vertices

- (2,0),(2c,sqrt(1-c²)),(2c,-sqrt(1-c²));
- (0,1),(-2sqrt(1-d²),d),(2sqrt(1-d²),d).

Both have lambda3=(-20+8sqrt13)/9 and product(52832-14480sqrt13)/729. These are two checkable phases, not a proof of every phase.

The excluded primitive6 control uses the proper caustic lambda6=4/9 and the following two positively oriented physical polygons:

- H=((2,0),(4/3,sqrt5/3),(-4/3,sqrt5/3),(-2,0),(-4/3,-sqrt5/3),(4/3,-sqrt5/3));
- J=((0,1),(-4sqrt2/3,1/3),(-4sqrt2/3,-1/3),(0,-1),(4sqrt2/3,-1/3),(4sqrt2/3,1/3)).

Their exact products are14000/729 and14336/729, difference-112/243. Repeating each vertex and foot list twice multiplies each signed area by2 and its product by4. Thus formal12-vertex repeated lists differ by-448/243. This exactly disproves a version based only on displayed list lengthN not2mod4. The primitive least-period interpretation avoids that counterexample.

Both fresh implementations intentionally compare a genuine equal product with the other equal product **plus1** under --false-identity. Each rejects with exit1 in ordinary and optimized execution. Valid runs exit0. stdout/stderr hashes, code hashes, environment and execution times are in authored_execution_receipts.json.

## Actual original assertion enforcement and metadata

All eight required executions ran in disposable layouts. The original archive before and after matches custody byte-for-byte, including all three original hash manifests. Exact stdout and writable verification files are retained where produced. Both unchanged original programs reproduce the archived JSON byte-for-byte in ordinary **and** optimized execution.

| Original program | Reported controls | Actually enforced ordinary assertion statements | Enforced under -O |
|---|---:|---:|---:|
| author verify.py |37393 exact +4092 numerical|41485|0|
| reviewer independent_check.py |13712 exact +348 diagnostics|14061|0|

The reviewer's additional one is the final existential excluded-parity nonconstancy assertion. Its12 residue_nonzero fields are computed metadata, not enforced assertions. The author's6231 primitive lattice rotations throughN202 and reviewer's3428 throughN150 were independently enumerated. Author exact counts are7 symbolic/formal controls plus6 per rotation. They are finite controls, not37393 separate universal theorem proofs. Under -O counters still increase and residuals may still be computed even though correctness enforcement is removed.

Actual mathematical mutations, with exact before/after text and derivative hashes recorded in original_execution_receipts.json:

- Author: replace the first universal chord-contact identity ==0 by ==1. Ordinary execution rejects immediately. Optimized execution exits0 with PASS and exactly the same37393/4092 counts and byte-identical original JSON.
- Reviewer: replace each target product comparison against reference by comparison against reference+1. Ordinary execution rejects the first3-orbit comparison, error.132359743979568... . Optimized execution exits0 with PASS, unchanged13712/348 counters and maximum scaled diagnostic error.4312484217 (archived3.6894188e-34). Its numerical fields therefore change, while its status remains PASS.

This establishes actual defects in these PR204 originals rather than extrapolating from another program. It does not establish that historical authors ran -O; their historical flags are unknown. Archived model/effort verification fields are null. The requested model and substantive_author_turns=1 are author metadata; this audit does not verify those historical claims. The original scripts' default ordinary executions do enforce and pass their advertised checks, so those normal-run counts must not be erased or described as universally unenforced.

## Limits, failures and remaining gap

This assigned audit is complete. The strongest fresh evidence is exact physical low-period geometry, an exact repeated-list scope counterexample, broad independent real physical reproduction, and demonstrated original-verifier optimization defects. A universal complex analytic proof and a current literature/priority determination remain outside this family's clearance.

Two bookkeeping incidents are preserved in RESEARCH_LOG.md: the first long audit process ended before its final receipt, so only the unrecorded last optimized reviewer run was resumed; and an exact-only harness rerun overwrote earlier physical receipt entries, so receipt preservation was repaired and the physical quartet rerun to restore direct bindings. No mathematical failures were suppressed. All real false controls failed as intended. SAFE_AUTHORED_ALLOWLIST.json is the exact proposed evidence allowlist; disposable author code/proof copies, primary PDFs, dependencies and temporary source render are excluded. A later explicit-exception repair, if prepared, belongs in a separate report and manifest and must not alter this sealed original-behavior audit.
