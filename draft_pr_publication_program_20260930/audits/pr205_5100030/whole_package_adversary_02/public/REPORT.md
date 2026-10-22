# PR205: second fresh whole-package adversarial review

**Scientific/package disposition: CLEAN for the exact frozen packet below.** No substantive theorem, proof, attribution, current-code, PDF, or archive defect was found. No package repair is requested. This is one completed whole-package review event, subject to Root's acceptance. It does not authorize publication or certify novelty, literature absence, human peer review, or a formal proof.

There is a separately disclosed **audit-handling incident**: an initial read-only-intended Git status command apparently refreshed index metadata. The binary index was not hashed before that command. This report does not claim initial-to-final index-byte equality. The package authentication and mathematical conclusions are unaffected; Root owns disposition of the handling incident.

## Exact reviewed object and independence

The subject is PR205, problem 5100030 / AMR-050-0030 / k601, original submitted HEAD `e8d7e925d19698edcb75822e40ca5ac820eb4388`, and the complete `publication_package_v2` identified by:

| Object | Bytes | SHA-256 |
|---|---:|---|
| ROOT_WHOLE_PACKAGE_PACKET_02.json | 2448 | c7b2d4c2b8fe93ea62775859dc156e9332f194be9aa56a0f49eb28adbd987fc3 |
| publication_package_v2/PACKAGE_SEAL.json | 8512 | 232f7b02c00946b027a3141eb3d85062a77721d2f8a5ae0b2857b76b591642d3 |
| odd_period_focal_pedal.pdf | 77757 | 768f494b52e7b0354c11fa5384154ba0f59506200dd66e7573ccad8fd90dcc0a |
| odd_period_focal_pedal.tex | 14447 | 07e3d8f8549365b2005584c5fdadc37a55ff6b865c989ace2914c7b4d941ec9c |
| verification-package.zip | 101469 | 0eb74232d1be56c2e306adc5c55b4e614a23484a7ea1fba2398b035317ce911b |

The adversarial plan was frozen at **2026-10-16 17:04:32.946788 UTC**, before reading the theorem/proof or earlier favorable reports. Its 2821-byte SHA-256 is `7c4ad524474043de5fc8c579fa2460b6783152b0f5fc8693e5d18a500ce41df4`. The task brief supplied the target, scope questions, known historical guard risks, and primary-source locations; this was not a blind discovery exercise.

The independent mathematical assessment was separately frozen before reading the packaged favorable mathematical/priority reports. Its exact identity and timestamp are in `MATH_FREEZE.json`. The previous whole-package adversary's report and Root's acceptance of that review were never read. Later examination of the packaged reports was a consistency audit, after this review's mathematical assessment was fixed. One shorthand transcription in the reviewer's frozen note omitted the common determinant factor on both right-hand sides of a subtraction system; `MATH_FREEZE_ERRATUM.md` preserves the correction without modifying the frozen note. The packet has the correct equations throughout.

## Claim, original domain, and physical geometry

The exact claim is phase independence of the product of two sums of ordinary Euclidean distances from the common foci to the complete ORIGINAL chord lines, for a fixed proper nested confocal ellipse pair with odd physical least period. It includes every admitted coprime winding, stars, reversal, and repetitions with the square scaling factor. It is not an assertion about clipped segments, other derived polygons, hyperbolic or collapsed caustics, or every even primitive period.

I directly inspected the original [arXiv v11](https://arxiv.org/abs/2004.12497v11) scope and Table 7, PDF page 9, and the [published article](https://doi.org/10.1007/s40598-021-00174-y), printed page 349. Both k601 rows have the same product of sums and odd parity. The introduction specifies a confocal ellipse pair. The pedal-foot definitions, rather than a newly substituted quantity, identify the observable. The manuscript candidly says that the source row does not literally print either a primitive-period qualifier or a complete-line qualifier. Standard perpendicular pedal projection uses a supporting line, including its extensions; this convention is also explicitly defined in the related primary bicentric paper. An arbitrary odd indexed closed trajectory has an odd primitive divisor, so the repetition rule restores the original indexed scope. The historical question mark supplies no present-day openness evidence.

The completeness check does not merely assume that a few canonical samples are billiards. For any fixed proper pair, there is a unique h in (0,K) with cn(h)=beta/b. Confocality gives a=alpha dn(h)/cn(h). The canonical boundary parametrization covers the outer ellipse once over 4K; the two tangents through each vertex connect its parameters u and u±2h. These facts match [Stachel's published Theorem 4.3 and equation (4.9)](https://doi.org/10.1007/s40879-021-00524-2). His symbol m is a modulus, whereas the current paper's m is its square. The conversion is correct.

I independently checked the subtraction system. With C=cn(x)cn(y), D=dn(x)dn(y), S=sn(x)sn(y), and Delta=1-mS², its equations are C+SD=cn(y-x)Delta and D+mSC=dn(y-x)Delta. Since Delta>=1-m>0 on the real family, inversion gives the displayed endpoint/contact identity with no omitted exceptional phase.

A separate reflection check uses a point p on the outer ellipse and a unit chord direction v. The caustic support condition is equivalent to

    lambda = a² v_y²+b² v_x²-(p_x v_y-p_y v_x)²
           = a²b²(p_x v_x/a²+p_y v_y/b²)².

Reflection about the outer gradient normal preserves this value by reversing the normal scalar product. It exchanges the two caustic tangents through p, selecting the outgoing inward branch. Thus the construction supplies the whole physical family. Closure requires 2Nh in 4K Z; least period requires gcd(tau,N)=1 in h=2tau K/N. The proper branch gives 0<tau<N/2. There is no prime-period assumption. Reversal permutes lines; r repetitions multiply each sum by r.

The unnormalized tangent normal has norm dn(v)/beta. At the foci its evaluations have the strictly positive magnitudes 1±k sn(v), bounded below by 1-k. Also dn(v)>=k'>0. This verifies ordinary distances and the signs before any complex argument. The pointwise product beta² agrees with [Bialy--Tabachnikov, Lemma 4.2](https://par.nsf.gov/servlets/purl/10408490). Their support-function proof is a line-distance formula despite its informal use of “segments.” That local product does not by itself prove the product of sums.

## Universal analytic step and exact boundary

For each fixed 0<m<1, the [classical cn/dn Fourier coefficients](https://dlmf.nist.gov/22.11) are absolutely summable, uniformly in real phase, by geometric-series bounds. The grid sum and series interchange is therefore legitimate. The dn filter selects N|2n, equivalent to N|n for every odd N. The cn filter selects 2n+1=N(2s+1). These arithmetic statements remain true for composite odd periods and do not require coprimality of a Fourier index with N.

Consequently the nome becomes Q=q^N. [Theta inversion](https://dlmf.nist.gov/22.2) determines one transformed parameter M and one argument scale gamma=K/(N K_M). Coefficient comparison gives D=dn(t/gamma|M)/gamma and H=sqrt(M/m)cn(t/gamma|M)/gamma. The unequal amplitudes are necessary and correctly printed. Hence D²-mH²=(1-M)/gamma². The filtered cn trace at zero is positive, making the eta normalization legitimate; the alternative relation M=m gamma²/eta² has the correct direction and powers.

The quarter-period shift gives A=D(v+K)/k' and B=-H(v+K)/k'. Its minus sign is correct, and beta²/k'²=alpha² supplies the required length scale. Pairing the odd function sn/dn at phase zero then gives the reciprocal-dn value in Theorem 1. Every real denominator is controlled: alpha, beta, cn(h), dn(v), k', and Delta are strictly positive. No division by a cyclic sn shift is needed by this manuscript's Fourier proof. The historical telescoping proof separately controls those shifts using oddness.

The entire trace step is directly prior mathematics, rather than just inspired by prior work. I read [Khare--Sukhatme's exact 0312074v1](https://arxiv.org/abs/math-ph/0312074v1), equations 14, 18, 32, 53, and 68--70 and the common-parameter discussion. Its dn grid and the current 4K grid agree by an odd-period permutation; its alpha is gamma and its alpha_1 is eta. I also inspected [0201004v2 Table 1, equation 29](https://arxiv.org/abs/math-ph/0201004v2), and the general finite-Fourier/principal-part framework and pair correlations in [0207019v2](https://arxiv.org/abs/math-ph/0207019v2). The manuscript correctly distinguishes the older catalog's stated all-odd identities from the supplied general proof framework. The documented source typos do not enter the current proof. In particular Stachel's printed alternating dn half-period sign is actually present and correctly corrected by the manuscript.

The N=4 pair was checked exactly, not inferred from a nonclosing point list. The outer axes squared are 3/2 and 3/4; lambda=1/2 gives alpha=1, beta=1/2. The diamond's side normals have norm sqrt2, and their caustic support equation is satisfied. Opposite line distances sum to 2/sqrt2, giving I=8. The rectangle's boundary equation is 2/3+1/3=1; its four lines are tangent to the same caustic, and its gradient normals have components (±2/3,±2/3), which verify reflection. Its focal sum is 3, giving I=9. All four vertices in each list are distinct. This is a same-family, primitive physical counterexample to an unrestricted even-period extension. The separate archived 64/5 versus 20 counterexample uses a different pair and is consistent with this one.

At the circle boundary, every side is tangent to a concentric circle at distance beta from the coincident foci, so I=N²beta² directly. The proof does not apply a singular normalization at m=0 or m=1. Its units are length squared, and similarity/repetition scaling agree with that dimension.

## Actual executions and falsification

The fresh archive was safely extracted into the private audit directory. The exact current source SHA is `7fbee76b89716091b84e2ec4f99f252d7cd1b0a47f517e4f605c806f762398bd`. Executions used Python **3.14.6**, flags `-E -S -B -P`, mpmath **1.3.0** from a preexisting read-only external runtime, and additionally `-O` for optimized subprocesses. No dependency was installed or copied. Public code accepts an explicit external runtime path when needed.

| Actual execution | Exit | Evidence |
|---|---:|---|
| Current verifier, ordinary | 0 | 8 proper configurations, 70 traversals, 25 required rejection controls; stdout byte-identical to sealed results_normal.json |
| Current verifier, optimized | 0 | Same counts and values; stdout byte-identical to sealed results_optimized.json |
| Additional current fault probes, ordinary | 0 | 52 required explicit rejections |
| Additional current fault probes, optimized | 0 | Same 52 required explicit rejections |
| Fresh tangent-intersection diagnostic | 0 | 12 configurations, 72 traversals, 4238 checks, plus direct N4 checks |
| Archived candidate, ordinary only | 0 | Exact archived 903-byte result reproduced byte-for-byte |
| Archived independent checker, ordinary only | 0 | Exact archived 1093-byte result reproduced byte-for-byte |

The current physical code first chooses a tangent by elementary affine circle tangency, propagates the forward outer-ellipse intersection, reflects about the gradient normal, and shoots closure by accumulated ordinary ellipse angle. Its measured focal distances come from the actual propagated chords, not the analytic predicted invariant. Closure, winding, boundary, caustic tangency, reflection, primitive return, and local focal product are checked before comparison. Actual repeated traversals and both orientations are exercised. The stored maximum scaled comparison residual `1.61539717061843029100893e-84` reproduces exactly. Python 3.10 syntax was parsed successfully; actual execution on Python 3.10 is not claimed.

The new independent diagnostic never imports verify.py. It intersects consecutive caustic tangent lines, reconstructs endpoints, measures physical distances, and checks reflection/boundary/tangency independently of the analytic value. It covers composite N=9,15,21,25, low and high coprime windings, m from 1e-12 to .999999, three phases, both directions, and a nonunit caustic scale. It checks the transformed nome and separate cn/dn traces. Its worst reflection residual is about 2.54e-96; the tolerance is 1e-75 at 100 working digits. These remain noninterval observations.

The extra fault harness places NaN, positive/negative infinity, complex values, and booleans in each position of reductions and comparisons; it challenges empty reductions, invalid primitive composite periods, tolerances, parameter/modulus confusion, a wrong finite identity, a dependency returning NaN, and a whole current main execution with its analytic normalization corrupted by 1%. All required failures occur through explicit VerificationError under ordinary and optimized Python. Inspection confirms finite validation occurs before the dangerous reductions and JSON forbids nonfinite output.

The exact archived near-function AST rejects false/NaN inputs ordinarily and accepts them when compiled with optimization. The candidate's exact running-max AST masks an injected NaN as zero even ordinarily. These reproduce the described vulnerabilities; they do not endorse those programs as current verification. Both the root README and archive notice explicitly direct readers to verification/verify.py. The notice's path is correct from the package root. Favorable archived reports and historic PASS files are clearly marked as historic evidence.

## Entire-package consistency, custody, and source limits

All **46 sealed payload files** match their sizes and hashes, and the package has no unexpected or missing file. All **44 ZIP members** match the corresponding sealed files byte-for-byte. The 43-entry public payload manifest plus its own member gives the complete ZIP inventory. There are no duplicate names, absolute paths, parent traversals, symlinks, corrupt members, third-party full texts/pages, dependency copies, credentials, or runtime caches in the archive. The PDF is intentionally uploaded separately and excluded from the ZIP; the TeX is present both separately and inside it.

The 17 archived originals total **41845 bytes**. Their SHA-256 and native Git blob SHA-1 identities match custody and the canonical original files. I independently rebuilt all **10 nonrecursive native tree identities**, resolved all 17 original leaves through the authenticated submitted tree, and checked that the exact tree delta consists of those files and the queue path. This authenticates the declared original file scope; it does not independently recreate a historical discovery clock or every remote authorization event.

I read all packaged mathematical reports, priority/source ledgers, original proof/review/code/receipts, current documentation, license, manifests, metadata, and actual results. The partial physical-family report labels its unproved global identity as a gap. The complex proof and adversary correctly control the full divisor, simple pole cancellation, odd grid separation, and real distance positivity; their stronger even-period diagnostic is consistent. Historical local-environment paths are identified as such and are not prerequisites of the portable current verifier. No unsupported inference from local q+q-=beta² to the product of sums survives in the package.

The main bibliography's eight entries were checked against direct primary texts and official version records. Relevant complete primary pages and all five manuscript pages were inspected visually. The 5-page PDF has readable equations, footnote, links and references, complete pagination, and no clipping or overlapping content. Extracted text and visible source agree. PDF metadata reports no encryption, forms, or JavaScript; its producer/date are consistent with the supplied artifact. PDF regeneration in a different TeX installation is not claimed to be byte reproducible.

For the supplementary geometric map, 11 of 13 fresh reading-copy downloads match their registry hashes exactly. The IMPA book URL returned HTTP400; the published CZ repository returned HTTP403. The matching current CZ primary preprint was available and directly verifies the elliptic trace/residue mechanism and the later n-1-term Property discrepancy. I do not certify the inaccessible book's entire selected contents or fresh published-CZ equation numbering from that failed access. Selected statements from AST, BT, Stachel, the self-intersected/bicentric/harmonic/spatial papers, and the integrability background were checked in their primary copies. Two additional Crossref metadata requests returned429; primary PDF covers and arXiv version/DOI links supply the relevant core source checks. No access control was bypassed.

These limits do not affect the universal proof or the positive classical prior implication. The package does not depend on proving absence of an earlier full k601 application. Its bounded nonlocation, record-clock and discovery-timing qualifications are explicit. The current paper, README and metadata consistently disclaim theorem/formula/method novelty, firstness, current openness, independent discovery and simultaneity. AI involvement, unrefereed status, finite noninterval diagnostics, and the absence of formal certification are disclosed.

## Preservation and remaining authority

Packet, seal, all 46 payload bytes, and the exact package inventory match their initial audit bindings at the final check. The separately observed Git state is a qualification: the first status command did not disable optional locks, and index mtime coincides with that command. The precommand binary index identity was not recorded. Before Root prohibited further Git commands, the initial and later logical porcelain outputs matched exactly, and the checkout remained main at `b6c79c95f7a7b793054249f81406bff37a496930`. A file-only mid-to-final snapshot confirms exact bytes/modes/mtimes of 16 recorded index/HEAD/ref/config/log objects. This supports no stronger initial binary-index claim. No index restoration was attempted; Root was promptly notified.

All deliberate writes stayed inside this new audit directory. No branch, commit, checkout, ref, PR, queue, tracker, release, DOI, publication service, next intake, GUI/editor, or unrelated document action was performed. No human was contacted. Private primary texts/images, runtime wrappers, full local command records and operational snapshots are excluded from the public-safe allowlist.

The relevant research goal for this assignment is complete: an independent adversarial assessment of this exact complete packet. **Best-guess completion: 100% of this review.** Root must decide acceptance of this event and handle any later live publication/custody workflow. The result is a scoped clean assessment with the stated evidence and limits, not a blanket endorsement.
