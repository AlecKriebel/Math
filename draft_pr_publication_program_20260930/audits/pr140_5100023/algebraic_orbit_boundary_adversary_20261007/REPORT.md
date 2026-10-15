# PR140 independent algebraic/orbit boundary review

Original immutable head: 9e908ae58b5ceee6a0825bbebd8acf565db55340. This family froze its own algebraic/projective line-intersection and physical billiard-shooting mechanism before reading the candidate proof or verifier. No original independent-review, imported report, or other family mathematics was semantically read.

**Mathematical verdict: PASS for the candidate's explicit nondegenerate, even-least-period theorem.** There is no remaining mathematical gap in its proof within that setting. This does not establish priority or an unqualified interpretation of every even traversal count in the source.

## Exact claim and source boundary

For a>b>0, 0<lambda<b² and a fixed-caustic Poncelet billiard family of even least period N, the unprimed origin/focal antipedal vertex centroids have the stated perimeter formula. Simple and primitive star polygons, either orientation, cyclic relabeling and repeated traversals of a primitive even polygon are covered. The formula excludes a=b; in a circle the separate centroid conclusion is zero.

I independently read the official arXiv:2004.12497v11 HTML (Introduction, Section2, Section3.5/Table5) and official published companion PDF text (printed341–343,347–349). I also visually read the pinned printed348/Table5 image. Both sources specify a confocal ellipse pair and k405 as the unprimed vertex centroid for even N and O/foci. Their stated setting supports excluding hyperbolic caustics. Table5 does **not** expressly define N as least period. The later published symmetry explanation on p349 is consistent with an intended primitive-period convention, but does not supply an explicit definition.

Consequently the candidate's sentence saying the source's N-periodic polygon “is understood” to have distinct vertices is an interpretation, not an independently established source quotation. A future write-up should identify the primitive/distinct-vertex convention as its own explicit theorem convention. The intended standard polygon reading is addressed; the broad repeated-list reading is false, as demonstrated exactly below. No claim of source authors' unstated intent is needed.

Sources: https://arxiv.org/html/2004.12497v11 ; https://arxiv.org/pdf/2004.12497v11 ; https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf (DOI10.1007/s40598-021-00174-y). The locally pinned companion is 1,836,579B/SHA256 c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42; Table5 image 294,429B/8cbf5b529b1e4548031522d27bf10f6283db4f2cc1e9afa6dc501d4615fc15cb. Neither body is copied into this review package. Web screenshot calls did not provide inspectable images; the visual claim above relies on the actual local image.

## Proof audit and independent mechanism

The two absolute line equations are (A−M)·Q=(A−M)·A and (B−M)·Q=(B−M)·B. They define antipedal intersections, rather than pedal feet. In chord coordinates C=cos(mu), S=sin(mu), U=cos(h), V=sin(h), the determinant is 2bV(aU−mC). Confocal support gives U²=1−lambda D², D²=C²/a²+S²/b². At m=±sqrt(a²−b²),
a²U²−m²C²=a²(b²−lambda)D²>0.
Thus aU>|mC| and every focus/origin line system is nonsingular. This argument supplies a sign as well as a nonzero squared denominator; no hidden square-root branch is admitted.

Independent sum/difference elimination produces
Qx=[C(a²+c²(U²−C²))−maU]/(aU−mC),
Qy=[aS(b²−c²(U²+C²))+2mc²CSU]/[b(aU−mC)].
These formulas, their line residuals, the opposite-chord pair, the determinant factor and squared chord length were verified as unspecialized polynomial identities using exact Groebner remainders. All seven cleared numerators reduce to zero under the stated circle, focus and tangency identities; analytic denominator signs justify clearing.

The candidate finite-action argument for central symmetry is valid. The oriented forward tangent map is an orientation-preserving homeomorphism; central inversion commutes with it. On the Poncelet family it has order equal to the primitive period. The generated finite commuting group admits the averaged positive nonatomic arc measure. Its cumulative coordinate conjugates all group elements to rotations. There is only one rotation of order two, so for even least period T^(N/2)=central inversion. This covers primitive even star rotation numerators as well; no simple-polygon assumption is used.

I then independently checked the candidate's use of stationarity. Incoming-minus-outgoing unit velocity is an ellipse normal by the reflection law; independent tangent displacements therefore have zero first variation of positive perimeter. Shifting all eccentric angles simultaneously is an allowed comparison variation on the outer ellipse even though it does not preserve the caustic. Differentiation must be done before reimposing tangency, as the proof does. This yields sum SC=0, including star polygons. The positive chord-length identity yields sum C²/N=H. Perimeter is constant along the smooth family by the same stationarity argument, without an unsupported imported invariant. Together with central symmetry and the independent focal pair identity these establish the formula.

## Computations and falsification

independent_checks.py imports no author code. It uses a physical specular-reflection recurrence and second ellipse intersection, shoots lambda by unfolded eccentric-angle winding, directly solves every antipedal line pair, and checks closure, distinctness, winding, confocal tangency, unit velocities and centroids. It passed 39,761 explicit guarded checks in normal PID91947 and optimized PID91948, at 2026-10-07T15:35:37 UTC: 594 rational chords; 13 periodic families and65 physical orbits over five phases each. Periods4,6,8,10,14,30 include primitive star p/N=3/8,3/10,5/14, near-circle, circle, scaling, reverse traversal, cyclic shift, and even-orbit repetition. Tested lambda/b² ranged0.0176108178–0.9957057728. Maximum relative closure4.65e−13; half-pairing5.03e−13; maximum focal-formula error8.74e−9 and focal-y error2.31e−9, with the largest amplification near the small denominator. These finite tests do not prove all periods.

symbolic_elimination.py passed seven unspecialized certificates normal PID93495 and optimized PID93494 at15:37:51–52 UTC. Its wrong x-sign, omitted y-term and altered line constant are rejected by the same polynomial reduction mechanism. This is checkable exact algebra supporting the analytic proof, distinct from finite numerical evidence.

The original verify.py uses assert in ck. The actual isolated production ck(False) rejects normally and silently accepts with -O; optimized reported check counts would be vacuous. This is a supporting-verifier robustness defect, not a failure of the mathematical proof. Preserve captured original bytes; harden any prospective published verifier using explicit exceptions, or explicitly prohibit optimized execution. ROOT separately replayed the complete author verifier; I did not duplicate those long loops. My own complete test guards survive both modes.

## Exact repeated-odd boundary witness

Let x=(9−sqrt(481))/16, y=sqrt(1−x²)>0, lambda=25(1−x²). On X²/25+Y²/9=1, take
(5,0),(5x,3y),(5x,−3y).
Since −1<x<−4/5, 0<lambda<9. Exact polynomial certificates verify all three ellipse equations, unit velocities, six reflection components, three confocal tangencies, six origin-antipedal line equations and both centroid components. The selected signs justify the positive edge lengths and all cleared denominators. There are23 exact certificates, actual normal/optimized v2 PIDs98794/98793 at15:44:44–45 UTC. The v2 controls genuinely alter the caustic, a reflection component and the asserted zero centroid; all are rejected. The earlier v1 witness and receipts are preserved; its two unit controls are weaker, and v2 is the final falsification control set.

The origin antipedal centroid is ((34/15)(2+1/x),0)≈(1.728858093915508,0), rigorously nonzero because 3/4<2+1/x<1. Central inversion gives another orbit on the same caustic with the negative centroid. Repeating each triangle twice creates a six-entry list and leaves each centroid unchanged. Thus an even traversal-count interpretation permitting odd primitive orbits is false. It is not a counterexample to the candidate's stated even-least-period theorem.

NUMERICAL_ODD_FULL_READBACK.json additionally retains actual physical points, velocities, tangency and closed-reflection residuals, all six antipedal vertices and direct centroids for phases0,pi,0.731 using the same ellipse/caustic. This actual binary64 reproduction PID99427 at15:45:31 UTC has maximum direct reflection residual4.58e−15. It is labeled numerical evidence; the exact certificate proves the0/pi pair independently.

## Limits, remaining disposition and custody

At lambda=0 chords coalesce; at lambda=b² the nested caustic degenerates and focal determinants may vanish. The theorem makes no endpoint assertion. Near these limits conditioning is nonuniform. a=b is handled as a separate circle conclusion, avoiding evaluation of H's singular a²/c² expression. Hyperbolic caustics and even-labeled repetitions of odd primitive orbits are outside the proved theorem. No extension was inferred.

All17 captured originals remain byte/mode exact; binary custody hashes of unread review material do not imply a semantic read. No shared native records, Git ref/index/worktree, PR, publication, DOI, tracker or external-contact action was taken. One ENOSPC event prevented a tiny here-document and two successor invocations from starting source evaluation; subsequent bounded writes succeeded. No child remains active. No large fixtures or source downloads were created.

Required before an unqualified public-resolution claim: qualify the source period interpretation honestly, and repair/enforce the verifier execution mode in supporting material. There are no mandatory mathematical repairs to the explicit theorem. Priority and novelty remain NOT ASSESSED. Family audit100%; PR140 overall estimate60% pending independent-family convergence and priority; original effort2/5 retained, zero new central proof-search turns.
