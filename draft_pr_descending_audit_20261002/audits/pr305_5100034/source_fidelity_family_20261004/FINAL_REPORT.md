# PR305 / 5100034 source-fidelity and hidden-formulation audit

Audit completed UTC: 2026-10-04T23:13:01.926731+00:00

## Verdict

**The candidate passes the source-fidelity gate for the openly corrected, displayed focal-pedal ratio equality. The primary source's broader phase-constancy implication is false.** The submitted theorem has no identified hidden restriction relative to the literal confocal-ellipse-pair geometric domain. Its proof restates and derives the local mechanisms it needs, rather than treating earlier review verdicts as premises.

The qualification is essential. An affirmative solution of the original uncorrected assertion that the ratio value is conserved would be false. The honest result consists of (i) a positive proof of the exact displayed equality and (ii) a negative exact resolution of the stronger phase-constancy reading. Both belong in any research disposition. This is a mathematical/source-fidelity gate; no historical-priority or independently new-method claim has been checked.

## Independence chronology and retained inputs

Acceptance criteria were frozen at 2026-10-04T22:59:47.832752Z before candidate or inherited evidence access (`INDEPENDENT_CRITERIA.md`, SHA-256 a59034ee34159739a8a32267b7f58f0ececc15dfac21fb8e01dde1f91ab01485). Complete arXiv-v11 and journal contents were read in their retained native PDF extractions. Table 7 in each edition was rendered and visually inspected. The source-only claim and control plan were frozen at 23:02:15.189587Z (SHA-256 8c57fdaa5ffae0b8653bbd091252b656183a3676da351447d47dce7ca5d693a1).

Before opening the candidate, this family independently derived and froze an exact counterexample at 23:05:30.687640Z (`INDEPENDENT_DERIVATION.md`, SHA-256 649c013485bf2f77d247688dbcf0b4123976df5f1cb9dda66c27225b5e41e46e). Only afterward were the submission, its code/results and its inherited review read. The old review uses the same natural axis-symmetric a=2,b=1 control; the earlier freezes establish that this family's construction was not obtained from that review.

All 29 submitted snapshot files were read and hashed. All 28 entries bound by `PUBLIC_MANIFEST.json` match their stored sizes and hashes. The two author-rerun scripts are byte-identical to the already-read original scripts. Newly captured primary target PDFs match the corresponding submitted `SOURCE_HASHES.json` references exactly. The candidate proof SHA-256 is 1abb4eaea5ef795f056ea89636defc99eb48f526cd20012b70d663cbeb2c4a34. `SNAPSHOT_READ_RECEIPT.json` retains every submitted file's mode, bytes and hash.

## Exact source target, editions and interpretation

Primary sources: [Reznik–Garcia–Koiller, arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), 29 October 2020; [journal edition](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Arnold Mathematical Journal 7 (2021), 341–355, DOI 10.1007/s40598-021-00174-y. See full context in §§1–3, Table 7, experimental §4, and the symbol appendices. The exact equality is arXiv Table 7 **k606**, printed p.9, and journal Table 7 **k607**, printed p.349. Journal k606 is an outer focal-pedal area product; arXiv k607 is an antipedal ratio. The candidate's formula-based edition mapping is correct.

The outer ellipse has a>b>0. The caustic is the inner confocal ellipse. For a closed periodic trajectory P, its outer polygon P' has side lines tangent to the outer ellipse at P's vertices. A_j is the signed cyclic shoelace area of perpendicular feet from focus f_j onto P's side lines; A'_j uses P' side lines. These are Euclidean projections onto complete supporting lines. The primary definitions fix signed areas, and the candidate faithfully keeps them.

The literal row asks

    E: A1/A2 = A1'/A2' for every allowed N and orbit phase where the ratios exist.

The article-wide meaning of an invariant strongly additionally implies

    C: for a fixed ellipse/caustic periodic family, that common ratio value is phase-independent.

E is explicitly displayed. C is not separately displayed in that row but follows naturally from arXiv p.2's family-constancy selection criterion, both editions' definition of the table invariant column, and both experimental methods. A Boolean equality can hold throughout a family even while its two sides vary. The candidate's distinction is mathematically necessary. Its repeated term “imported extra assertion” should not be used to imply that C arose only in the imported dataset: the primary articles' broader wording also encourages C. The correction remains openly documented, rather than silent.

There is no late concluding conjecture that replaces E. The journal §3.7 anticipates analogous antipedal invariants, explicitly without having checked them; those are a different construction and do not alter the focal-pedal target.

## Independent exact falsification of C

On x²/4+y²=1, foci (±sqrt3,0), put d=sqrt13,

    A=2(d−1)/3, B=(4−d)/3,
    Y²=1−A²/4, X²=4(1−B²).

The triangles ((2,0),(−A,Y),(−A,−Y)) and ((0,1),(−X,−B),(X,−B)) have the same strictly nested positive-axis confocal caustic x²/A²+y²/B²=1. The retained independent derivation verifies exact ellipse incidence, tangency and the normal-bisector reflection law. The exact control checks the sign branch after squaring; it does not mistake squared reflection for the reflection law.

At the first phase direct signed-foot area calculation gives

    R_x=(2−sqrt3)/(2+sqrt3) · (sqrt13+2sqrt3)/(sqrt13−2sqrt3)
       =3.5884019759959343412457523971432027957001….

At the second phase focus-swapping reflection gives R_y=1. The first denominator is positive: (sqrt13/2)²−(sqrt3)²=1/4, and subtracting the cross-multiplied numerator products gives 2sqrt3(2−sqrt13/2)>0. Every area used is nonzero. These are genuine N=3 members of the same Poncelet family, so C is false inside the original domain without appeal to any excluded limit.

The pre-candidate native Decimal85 control checked reflection, common-caustic tangency, ellipse incidence and equality E at both phases, with all geometry residuals below 5e−84. Its exact content and full streams are retained. The later independently written SymPy1.14.0 checker verified 14 exact identities/sign controls, including the frozen witness and all four candidate triangle area formulas. Neither author nor old-review checker was imported or executed by this family. The candidate's other triangle also correctly disproves C, with its shared ratios R and 1/R and multiplier125/24.

## Quantifiers and boundary adversary

| Case | Source status | Candidate treatment | Finding |
|---|---|---|---|
| Nondegenerate nested confocal elliptical caustic, primitive N≥3 | Central defined domain | Positive proportionality at each focus, all primitive turning numbers | Correct source coverage |
| Primitive stars | No convex-only restriction in row | Signed areas and step0<delta<2K | Positivity argument remains valid |
| Repeated traversal | Not explicitly forbidden | Areas multiplied by repetition count | Correct extension |
| Reversal and cyclic relabeling | Same geometric object/conventions | All area signs reverse; cyclic sums unchanged | Equality unchanged |
| Focus exchange | Both source foci | Phase shift2K | Correct and explains odd-period ratio variation |
| Hyperbolic caustic | Outside the source's defined ellipse-pair model | Excluded | No original-source omission defect |
| Collapsed caustic/focal separatrix/two-period diameter | Not a nondegenerate ellipse pair; ratios/outer intersections can fail | Excluded | Explicitly scoped, no silent universal denominator claim |
| Circular billiard a=b | Explicit a>b hypothesis excludes it | Separate trivial observation | Harmless extension, not a needed original case |
| Unsigned lobe areas or segment-clamped projections | Different from source conventions | Excluded | Correct |

The source's row does not itself specify N≥3 or prove ratio denominators nonzero. A nondegenerate positive-inner-ellipse periodic billiard cannot have a diameter two-cycle tangent to that caustic; excluding the degenerate N=2 case makes the implicit geometry explicit. It does not remove a genuine family in the stated source domain.

## Candidate deduction versus inherited verdicts

The canonical representation is independently supported by the retained published [Stachel paper](https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf), Theorem4.3 and eq.(4.9), pp.1614–1615. Its elliptic-caustic modulus and primitive turning-number hypotheses match the candidate. The [NIST DLMF periods/quarter shifts](https://dlmf.nist.gov/22.4) and [addition formulas](https://dlmf.nist.gov/22.8) independently support the classical identities. Native DLMF retrieval returned403, while the web reader exposed the needed formulas; this does not affect the retained target PDFs. Stachel has a printed real-period sign error for dn just before his theorem; the candidate's argument uses the correct DLMF identities and does not import that error.

After scaling the caustic major axis to1, every strictly nested confocal ellipse pair gives k∈(0,1), k'>0 and a unique v∈(0,K) through cn(v)=k'/b. The identity dn²(v)=k'²+k²cn²(v) gives a=dn(v)/cn(v). Closure gives delta=2v=4K tau/N and primitive coprimality; reversal selects0<tau<N/2. Thus the canonical restrictions are domain consequences rather than an unexplained loss of families.

I independently checked the candidate's local-to-global chain: actual side-line feet, original contact phase shift, focus exchange, original even double-pole germ times an odd regular neighbor difference, outer adjacent opposite/collinear residues, primitive incidence, common lattice4K/N, imaginary anti-periodicity and residue subtraction on a compact torus. The common Jacobi poles are removable in the projection maps. The original root occurs once per primitive phase; the outer roots occur at two adjacent indices. These facts are restated locally in the candidate; earlier PASS verdicts are not needed as logical assumptions.

The denominator argument is independently checkable. For the normal n(u)=(−sn(u)/R,cn(u)/S),

    det(n,n')=dn(u)/(RS)>0 on the real line,
    n(u+2K)=−n(u).

The normal angle advances strictly between0 andpi over any step0<delta<2K. Each focus lies strictly inside each ellipse, so a foot vector relative to its focus is a positive multiple of n. Every consecutive determinant is positive, including the closing lifted edge. The signed area is therefore positive for stars as well. This excludes identically-zero traces and real denominator zeros before residue matching or forming the requested ratios. The central step is a complete local derivation, not a transfer to an unsupported earlier parity conclusion.

No mathematical counterexample to E or missing assumption inside this source scope was found. The accepted strongest analytic claim is a positive phase-independent multiplier C0 with A'_j=C0 A_j at both foci; E follows. C0 is an outer/original multiplier, not the varying ratio between the two foci.

## Exact remaining gaps and disposition guidance

1. **No unresolved source-domain/equality proof gap was identified by this family.** Other independent proof families remain responsible for their final universal mathematical verdicts.
2. **Affirmative phase constancy is false**, rather than merely unproved. Any summary or status must retain the corrected E / falsified C split. Use “corrected displayed ratio equality proved; phase-constancy reading disproved.” Calling the entire uncorrected invariant sentence positively solved is unsupported.
3. The submitted snapshot omits its native raw imported `source_record.json` and `upstream_research.json`. Their hashes are present, but this family cannot independently confirm that dataset's exact wording or ID metadata from hashes alone. The primary formula/edition mapping is fully confirmed.
4. Historical priority, prior full equivalent theorems, provenance searches and publication decisions were intentionally outside this gate. Credited mechanisms do not establish either novelty or prior full resolution.

Progress:100% of this assigned source-fidelity audit. This is not a percentage toward historical novelty or a claim that every project gate is complete.

## Execution and closure

Native control receipts retain exact argv, cwd, start/end UTC, environment delta, exit status and complete stdout/stderr in `independent_triangle_control.execution.json` and `independent_symbolic_control.execution.json`; full streams are separate `.stdout.txt`/`.stderr.txt` files. PDF extraction/render receipts and input retrieval metadata are retained. `ENVIRONMENT.json` identifies native Python, symbolic runtime and Poppler. `ARTIFACT_SEAL.json` binds every artifact's exact bytes, SHA-256 and final read-only mode; its own SHA-256 is transmitted separately to ROOT.

All writes were confined to this newly created family directory. No Git command, tracked-source edit, index/ref change, install, external individual communication, other-chat message, publication or PR action was performed. Only collaboration messages were sent to ROOT. **No more writes will be made by this family after its final seal and closure.**
