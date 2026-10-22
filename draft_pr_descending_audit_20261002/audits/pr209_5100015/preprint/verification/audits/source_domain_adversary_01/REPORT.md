# PR209 independent source/domain adversary

Audit target: original claimed-solved PR209, head `fd09a95b479f376234835a4494693bb1316c85ec`, problem5100015 / AMR-050-0015, invariant k303,b. This is a source and mathematical-scope audit, not a whole-preprint or completed historical-priority review. All work is confined to this directory; no target files, Git state, provider state, publication or queue state were modified. No outside individual was contacted. No inherited reviewer conclusions were read.

## Verdict and exact claim

**Source/domain match passes. The written proof has no located mathematical gap for the source's nondegenerate confocal-ellipse-pair domain.** This conclusion is based on an independent source freeze, complete passage check of the submitted PROOF.md, primary-input checks, and new finite controls. Historical novelty and a broader hyperbolic-caustic theorem are not certified.

Fix a noncircular ellipse E, a>b>0, center O, and a strict interior nondegenerate confocal ellipse C. For an ordered N-periodic billiard traversal, form R_i as the intersection of the tangents to E at P_i,P_(i+1). Form Q_i as the perpendicular foot of O on the actual side line R_(i-1)R_i. For N odd or N=2 mod4, the claim is constancy of

`(1/2 sum det(R_i,R_(i+1))) (1/2 sum det(Q_i,Q_(i+1)))`.

Thus the claim concerns the outer tangent-intersection polygon and its center pedal on side lines, in induced traversal order. It concerns neither a caustic-contact polygon nor the original-chord pedal. It imposes no centroid statement and does not divide by a polygon area.

`SOURCE_CLAIM_FREEZE.md` was authored and hashed before opening the inherited proof/reviews. Its JSON receipt records the independent order and completion estimate. The submitted proof agrees with this reconstruction, including both allowed parity classes.

## Primary source evidence and domain boundaries

The v11 and published PDFs were read from the parent's supplied read-only source location, without copying PDFs. SHA256 hashes were checked independently:

| Source | SHA256 | Relevant passages checked |
|---|---|---|
| Reznik-Garcia-Koiller v11 | c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da | introduction/Figure1 p1; section2 pp2-3; sections3.1,3.3,3.4 and Table4 pp4-6; experimental method p13 |
| Published Fifty New Invariants | c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42 | introduction/Figure1 pp341-342; section2 p343; sections3.1,3.3,3.4 and Table4 pp344-346; method pp351-352 |
| Stachel, On the motion of billiards in ellipses | 9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8 | scope p1604; canonical derivation pp1612-1613; complete Theorem4.3/(4.9) p1614; neighboring turning-number/Poncelet-grid discussion |

Table4 was visually inspected in both editions; the published section2 signed-area definition and Stachel theorem were also visually checked. Reading-page renderings stay under `private_reading/`, excluded from the public manifest. The public audit contains original analysis, not third-party full text.

Both source editions explicitly describe the billiard in this paper as a pair of confocal ellipses. Their preliminary a>b>0 assumption excludes the circle. Their real positive caustic semiaxes and the experimental construction of a confocal ellipse agree with that scope. Consequently the author's restriction `0<lambda<b^2` is source-faithful. In particular, a hyperbolic caustic in an elliptic table is possible in the broader theory but is outside this source's stated ellipse-pair domain, including for N=2 mod4. The worklist's generic phrase 'confocal caustic' should be read with this primary definition; a claim advertised independently for arbitrary confocal conics would need a separate proof.

Both editions define all polygon areas as signed ordered shoelace sums. Table4 specifies the pedal with respect to the outer polygon's sides. The table row k303,b is a product for N not0mod4 and M=O. k303,a (arbitrary M but only2mod4) and k304 (a ratio for0mod4) are distinct rows.

No explicit primitive, convex, winding1, or coprime restriction appears in the relevant primary statement. The examples and numerical initializer are convex; they do not invalidate the stronger star coverage in the candidate. Stachel's theorem explicitly accommodates turning number tau with gcd(N,tau)=1. The author's full signed-order proof covers stars, and its separate repetition reduction covers nonprimitive listed periods.

A chord with consecutive antipodal endpoints passes through O and cannot be tangent to a nondegenerate inner ellipse. Since tangents to E at distinct points are parallel exactly for antipodal points, every required R_i is finite. Consecutive endpoints are distinct in a nondegenerate billiard; three distinct points of E cannot be collinear, so the outer sides used here do not collapse. The real foot denominator is at least b^2>0. N=1,2 have no nondegenerate elliptic-caustic family of this sort. Circle, caustic point/segment, grazing limit, and projection clamped to finite segments are separate boundary questions, not missing in-domain cases.

If a primitive d-periodic traversal repeats r times, each ordered area multiplies by r. The product multiplies by r^2. When N=rd is not divisible by4, neither is d. This establishes the extension without a false assumption that every even listed traversal is centrally symmetric. In particular, a twice-traversed triangle has listed N=6 and is covered by repetition, not by a primitive-six symmetry argument.

## Complete submitted-proof passage coverage

Line references below use the frozen submitted PROOF.md; equation numbers are its labels. Every substantive proof passage was checked.

| Frozen lines | Check and result |
|---|---|
| 7-20, claim/conventions | Correct exact polygon, center, source parity, signed order, strict ellipse domain; primitive convention is later discharged by repetition. |
| 24-41, (2)-(4) | Stachel Theorem4.3 gives every confocal elliptic-caustic family a canonical parameter and shift2v. For a fixed nested pair cn(v)=beta/b determines v in(0,K), and confocality gives a=alpha dn(v)/cn(v). Primitive closure forces 2Nv=4tauK, gcd(tau,N)=1. This supplies both completeness and stars. Contact phase follows from the displayed caustic tangent equation by addition formulas. |
| 45-57, (5)-(7) | Direct addition of Jacobi sn/cn determinants gives the edge determinant, and the dn pair sum gives the trace area. Summing with the factor1/2 and cyclic reindexing yields exactly (7), with no convexity assumption. Real dn is positive, so no real denominator vanishes. |
| 59-67, (8) | Expanding det(P_(i+1)-P_i,P_(i+2)-P_(i+1)) yields 2area(P)-half the skip-two sum. (6) at2v gives (8); reindexing a sum is valid even when stepping by2 splits cycles. No illicit odd-N shortcut. |
| 71-80, (9)-(10) | Conic pole of the chord gives the actual endpoint-tangent intersection. Linear scaling has determinant ab/(alpha beta), yielding (10) from the shifted orbit area. The finite-vertex argument is sound. |
| 84-102, (11)-(13) | Orthogonal projection onto n.X=1 is n/(n.n). Elementary algebra gives (11). Quarter-period formulas imply dn(K-v)=b/a and (13). All denominators positive under the stated real parameters. |
| 104-118, (14)-(15) | Addition formulas for the sum at z±(K-v), followed by P(z-2K)=-P(z), give precisely the pointwise center foot. The matrix determinant b/(4a cn^2(K-v)) is correct. Its global minus sign preserves two-dimensional signed area. Multiplying this by (8) gives (15); no pedal substitution occurs. |
| 122-142, odd trace lemma | DLMF confirms dn periods2K,4iK', simple poles at iK'+2rK+2siK', imaginary antiperiod2iK', and evenness. At c=K+iK', evenness plus the shifts gives dn(c+t)=-dn(c-t). For odd q the real subgroup omits K; pairing h,-h makes U(c)=0 with no pole there. Any possible pole p of U satisfies U(p+K)=0 by subgroup/imaginary shifts, so every possible singularity of U(z)U(z+K) is removable. The two possible pole sets cannot create an uncanceled double pole. A holomorphic function on the compact period torus is constant. This proves the central invariant mechanism; it is not a restatement of the goal. |
| 146-171, (18)-(21) | Shifts 2iv modulo2K are a subgroup of order q=N/gcd(N,2), each with multiplicity r. Since gcd(tau,N)=1, this holds for every primitive star winding. q odd is exactly the claimed parity. Trace periodicity by2v aligns the two area phases, and the coefficient in (21) is the product of the independently checked coefficients. |
| 175-181, boundaries/credit | Star and repetition extensions valid. Circle comment is elementary and outside source requirements. Attribution and finite-control limits are appropriate. Claimed author chronology and full prior-search completeness were not independently authenticated in this scope. |

An adjacent printed formula in Stachel p1613 incorrectly assigns a sign change to dn under2K. The submitted proof explicitly uses DLMF's correct dn(z+2K)=dn(z), not that adjacent error. The actual Theorem4.3 parametrization used is unaffected.

Primary online inputs independently opened during this audit: [DLMF periods/poles/zeros and shifts](https://dlmf.nist.gov/22.4), [DLMF addition formulas](https://dlmf.nist.gov/22.8), and [Stachel published paper](https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf). These support the analytic inputs; no private communication or unread external theorem is a remaining mathematical dependency.

## New checkable controls

`independent_controls.py` imports no submitted code and does not execute the submitted verifier. Its exact fixtures were freshly derived rather than copied from the author's six-period controls.

1. For E:x^2/4+y^2=1, derive two genuine axis-symmetric triangle phases from reflection. The horizontal phase has nonaxis x-coordinate h=(2-2sqrt(13))/3; the vertical phase has nonaxis y-coordinate v=(sqrt(13)-4)/3. Both share lambda=(-20+8sqrt(13))/9 in(0,1). Exact boundary equations and every chord's confocal tangency are checked, including the unsquared horizontal reflection relation.
2. Compute outer vertices by solving pairs of outer tangent equations. Compute pedal feet from the actual lines through consecutive outer vertices, independently of the proof's pointwise map. Check actual side incidence and perpendicularity exactly, product equality between the two triangle phases, cyclic shifts, reversal of both signed areas, and repetition by factors2,3,6 (listed N=6,9,18).
3. The excluded4-period diamond and rectangle for a=4,b=3 share confocal lambda=144/25. Exact products1152 and1250 kill an extension that drops the parity restriction.
4. Off-center M=(1/3,1/5) on the odd triangle pair kills an extension that drops M=O. Wrong original-chord pedals are detected by wrong target values/construction. A subtlety recorded below is that their products are still constant on the exact triangle pair.
5. A separate physical billiard map constructs both tangent contact points on the actual inner ellipse, intersects the selected ray with E, and selects positive angular advance. It uses no Jacobi functions, trace formulas, or submitted geometry. Bisection determines lambda for10 prescribed period/winding/axis families. Four phases per family check closure, winding, confocal tangency, outer-side foot incidence, nonparallel tangent margins, and target-product constancy. Families include odd and2mod4, primitive stars, a near-circle table and an elongated table. These are high-precision corroborations, not interval-certified numerical proofs.
6. Wrong spatial sorting of star vertices and scrambling pedal order are controlled separately. Exact residue arithmetic checks effective subgroup order/multiplicity, oddness, and absence of the half-period K for every reduced admissible winding through N=99.

## Failures, exact gaps, and strongest verified result

The first independent harness incorrectly expected wrong original-chord pedal products to vary on the two exact triangle phases. That assertion failed: this mutant survives that constancy-only test. The harness was corrected to check the actual target product value and construction; no submitted mathematical formula was changed. Likewise, a feet-order reversal in a triangle reverses its signed area and can preserve constancy, so constancy alone is not a complete construction oracle. A second harness run also showed that spatial-sorting a primitive star can preserve constancy; that mutant is now tested for its wrong target value, with its measured phase range retained. These observations are recorded rather than concealed.

No in-domain mathematical counterexample or uncovered parity/winding case was found. The strongest verified result is the full claimed constancy on nondegenerate fixed-confocal-elliptic-caustic families for all N not0mod4, with signed traversal order and repeated orbits included. The universal conclusion rests on the checked analytic proof; the exact and numerical artifacts corroborate its construction and scope.

No unresolved mathematical/source gap was identified. Exact remaining work outside this audit: independent whole-package/preprint review, complete author-history/provenance audit if needed, and a fresh historical-priority investigation before a novelty claim. A generic hyperbolic-caustic extension has neither been claimed nor verified here.

## Reproduction and result receipt

Run the file with Python-B using the provided scientific environment:

`/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python -B independent_controls.py`

The program writes `control_results.json` beside itself. It uses only standard library, SymPy1.14 and mpmath1.3 already installed; no network, installs, caches, secrets, or provider writes. The run completed at 2026-10-16T04:42:33.045102+00:00 with PASS: 5209 assertions (3826 exact checks and 1383 high-precision diagnostic checks). All10 physical families and40 phase samples passed. Maximum scaled checked discrepancy was 2.0262590224e-70 at85 decimal digits. The freshly derived exact triangle product is `(57+15sqrt(13))/2` in both phases; the exact off-center products differ and the excluded N=4 products are1152 and1250. The source-freeze receipt remains unchanged. `AUTHORED_MANIFEST.json` lists every public payload with its byte count/hash and excludes itself and private reading material.

Final audit completion estimate:100% for the assigned mathematical/source-domain audit;0% certification of a completed historical-priority review. This percentage does not represent progress toward proving a generic hyperbolic extension.
