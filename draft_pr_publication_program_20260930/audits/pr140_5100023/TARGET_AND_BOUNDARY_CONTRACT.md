# PR140 mathematical audit contract

Treat all claims below as hypotheses. Original submitted head: 9e908ae58b5ceee6a0825bbebd8acf565db55340. Literal status claimed_solved, effort 2/5. This is an audit, not an assumption of mathematical or priority clearance.

The original target is k405 from Reznik–Garcia–Koiller, arXiv:2004.12497v11, Section 3.5 / Table 5: for even N, the vertex centroid of the unprimed antipedal polygon with respect to O or either focus is invariant along a fixed-caustic elliptic billiard Poncelet family. Verify the original source's exact setting and period convention independently; the candidate's scope must not silently replace the original problem.

Candidate setting: a > b > 0, c² = a² − b², ellipse x²/a² + y²/b² = 1; nested confocal elliptical caustic with 0 < λ < b². A polygon has even least period N and distinct successive vertices; simple and star polygons allowed. Q(M,i) is the intersection of lines through consecutive orbit vertices A,B perpendicular to A−M,B−M, respectively. C(M) = (1/N)Σ Q(M,i).

Candidate claimed formula, with L the family perimeter:

K = a²b² − λc²,
H = (a²/c²)[1 − bL/(2a√λN)],
C(O) = (0,0),
C(fσ) = (σc[−1 + KH/(a²(b²−λ))], 0), fσ = (σc,0).

Potential boundaries: central symmetry for primitive even star orbits; arbitrary orientation and winding; unwrapped angle choices; stationarity versus constrained caustic deformation; antipodal/chord degeneracy; antipedal lines versus pedal feet; λ→0 and λ→b²; a→b circle limit; focus/origin denominators; repeated odd orbits labelled with an even count; whether the source includes hyperbolic caustics. Degenerate limits may require honest exclusions rather than a false extension.

Keep initial independent families separate. Before reading author PROOF.md or verification code, freeze a short independent mechanism/obstruction note from this contract and primary source. Then audit the original proof and run original verifiers from separate scratch directories. Do not read original independent_review material, prior_imported_report, or the other family's files until a first verdict is frozen. Preserve all 17 captured original bytes. Write only inside your assigned audit subfolder; no shared native records, original files, Git refs/index, PR comments, merge/close, paper, DOI or tracker action.

Record actual UTC, checkable derivations/counterexamples, real reproduction counts and resource limits. Distinguish mathematical theorem validity, coverage of the original target, and novelty. Current program audit completion: 23/99 = 23.23%; this case intake is 5%; no PR140 mathematical clearance yet.
