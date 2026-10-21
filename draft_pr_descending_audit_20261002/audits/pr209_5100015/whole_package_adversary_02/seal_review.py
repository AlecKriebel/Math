"""Write the completed scoped review and self-excluded authored seal."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

O=Path(__file__).resolve().parent;B=O.parent/'preprint'
F=json.loads((O/'FROZEN_INPUTS.json').read_text())
V=json.loads((O/'FINAL_VALIDATION.json').read_text())
assert V['status']=='PASS'
for name,row in F['core'].items():
    raw=(B/name).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
for row in F['all_candidate_files']:
    raw=(B/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
completed=datetime.now(timezone.utc).isoformat()
table='\n'.join('| '+n+' | '+str(r['bytes'])+' | `'+r['sha256']+'` |' for n,r in F['core'].items())
report='''# Second new independent adversarial whole-package review — PR209 / 5100015 / k303,b

**Scientific verdict: PASS in the stated strict-confocal-ellipse domain. Dated publication/package snapshot: PASS, with no mandatory findings and no optional findings.** This is an automated scoped package review, not release authorization, human peer review, formal verification, an exhaustive worldwide priority certification, or certification of future publication operations.

Review completed at COMPLETED_UTC. Review assignment completion:100%. Best estimate of the overall research/publication case remains55%; later clearance and actual release actions belong to the coordinator's separate workflow.

## Exact frozen object and independence

Candidate root: `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint`.

Machine freeze time: FROZEN_UTC. FROZEN_INPUTS.json records actual hashes and sizes of all230 candidate files, every actual source ZIP member and the seven core objects below. None of the supplied labels was accepted without hashing actual bytes.

| Actual frozen object | Bytes | SHA-256 |
|---|---:|---|
CORE_TABLE

The assignment disclosed the previous M1 finding and the claimed repair. I treated those as hypotheses. INITIAL_MECHANISM.md fixed my own geometric/pole and Fourier falsification plan at the freeze. INDEPENDENT_RECONSTRUCTION.md and PRE_PRIOR_REVIEW_CHECKPOINT.json preserve the complete first-principles reconstruction and successful fresh executions before I opened the actual first whole-package ASSESSMENT/REPORT, its additive report correction, or ROOT_REVIEW01_RESOLUTION.json. The checkpoint is machine dated2026-10-16T06:04:40.533937+00:00. This is new independent checking under the same automated system, not a claim of human or historical discovery independence.

FINAL_VALIDATION.json confirms all230 candidate files and all211 extracted actual ZIP members remained byte-identical to the freeze after the review. No candidate file was edited.

## Full universal mathematical assessment

The exact target fixes a>b>0 and0<lambda<b², with alpha²=a²-lambda and beta²=b²-lambda. It uses signed cyclic determinant areas of the outer boundary-tangent intersection polygon and the orthogonal feet of O on those same tangent lines. This is the actual original ellipse-pair source domain. Hyperbolic, focal, zero-axis or collapsed caustics, arbitrary reference points, filled star lobes and spatially reordered vertices are not silently included.

The full derivation is retained in INDEPENDENT_RECONSTRUCTION.md. It reconstructs why Stachel's coordinates exhaust the asserted families: cn(v)=beta/b selects a unique v in(0,K), the displayed axes satisfy the common focal difference, P(z)=(-a sn z,b cn z) covers the boundary once in4K, and addition verifies both endpoints on the caustic tangent. The two real tangents to the strictly interior caustic exhaust chord choices. Closure and least period give v=2tauK/N with gcd(tau,N)=1; orientation can be chosen with0<tau<N/2. Thus this is not merely a proof for a sampled convenient subfamily.

Direct tangent-line equations give the actual outer vertex at chord midpoint z as (-a dn(v)sn(z)/cn(v),b cn(z)/cn(v)). This also follows from elementary polarity relative to the boundary ellipse. The half-step u+v and linear area factor are correct. Consecutive real endpoint tangents cannot be parallel: that would force antipodal endpoints, whose origin-crossing chord cannot touch the strict interior ellipse.

Jacobi addition gives the positive determinant identity with f(t)=sn(t)cn(t)/dn(t). Summing yields area(P)=ab f(v)T(u). Expanding determinants of consecutive edge vectors gives ab[2f(v)-f(2v)]T(u). This is an identity of complete ordered sums; skip-by-two need not be one connected cycle.

The actual foot is Q=n/(n·n), n=(-sn(z)/a,cn(z)/b). Setting w=K-v and directly adding P(z+w)+P(z-w) yields

    Q(z)=diag(b/a,1)[P(z+K-v)-P(z+K+v)]/(2cn(w)).

The determinant of this linear map is b/(4a cn²(w)). The common negative edge sign preserves planar signed area. The resulting two actual area traces are

    A'=(a²b²/(alpha beta)) f(v) T(u+v),
    A'_O=b²[2f(v)-f(2v)]T(u+K-v)/(4cn²(K-v)).

The period2v aligns the second phase with u+v+K. For r=gcd(N,2) and q=N/r, coprimality makes the shifts modulo2K exhaust the q-subgroup exactly r times. Hence T=rUq, and q odd is exactly4 not dividing N. This handles odd periods, twice-odd periods, composite orders and every admitted coprime star winding.

I independently verified both complete meromorphic mechanisms. For the native reflected-zero proof, evenness and half-period signs give dn(K+iK'+t)=-dn(K+iK'-t); the odd subgroup avoids K, so its complementary values are all finite and pair to zero. Every possible simple trace pole has a complementary K-shift zero, and the converse removes every shifted-factor pole. Repeated terms change residue coefficients, not pole orders. No pole-pole product is called removable.

For the printed classical coefficient, Res(dn at iK')=-i and dn(iK'+t)=-i cs(t). Pairing subgroup elements t and2K-t gives

    Res(product dn)/Res(Uq)=product_{j=1}^{(q-1)/2}cs²(2Kj/q)=Cq.

Subgroup periodicity and imaginary antiperiodicity transfer that coefficient to every pole. The entire elliptic difference product(dn)-Cq Uq is constant and antiperiodic, hence zero. Multiplication by the K-shift proves Uq(z)Uq(z+K)=(k')^q/Cq². This is old mathematics, correctly credited rather than described as a new identity or method.

The strongest verified result is the full theorem with the printed invariant value

    a² b⁴ f(v)[2f(v)-f(2v)] r²(k')^q
    ---------------------------------- .
      4 alpha beta cn²(K-v) Cq²

Every real denominator is controlled: alpha,beta,a,b>0; dn(t)>=k'>0; cn(v)>0; cn(K-v)>0; addition denominators>=1-k²>0; n·n>0; the Cq arguments lie strictly in(0,K), so sn and cn there are finite nonzero. No area is divided out. Units are length^4.

Reversal negates both areas; fixed d-fold repetition multiplies each by d and the product by d². If the listed length avoids4, its least divisor does too. Genuine one/two-bounce strict-ellipse-caustic cases do not exist. The q=1 trace identity is nevertheless valid. Circles have a separate rotation proof and the continuous formula N²R^4 sin²(pi tau/N), without using a collapsed elliptic torus. Beta=0/lambda=0 are excluded endpoints. The printed N4 examples genuinely have the same caustic lambda=4/5, forward reflection and segment tangency, with products32 and50. More generally the generic Cartesian products are8a²b² and2(a²+b²)², separated by2(a²-b²)². Thus the parity exclusion is substantive and does not arise from a hidden real singularity.

I also checked the supplemental direct area-divisor reconstruction and classical bridge. They distinguish a complete universal proof from a Cartesian reduction that still needs a trace identity. The old CC theorem concerns ORIGINAL/OUTER areas; its auxiliary primitive2q construction validly gives the odd trace constancy because K-K/q is a subgroup period. The strict confocal pair has four distinct transverse complex intersections, so the general-position hypothesis is not lost. Landen normalization retains the argument scale eta; odd and even reduced orders are distinguished correctly.

## New falsification and real offline reproduction

I read all eight actual scientific programs, run_checks.py, integrity.py and harness_failure_controls.py before executing scientific or harness code. Preparation/bundle code was inspected as data and was not run. Retrieval/inventory/release helpers were not executed. No installation, environment creation, network use by the scientific code, or downloaded third-party code execution was needed.

BYTE_AUDIT.json records1,586 independent byte/membership checks. The actual ZIP was safely extracted into this review's owned folder. I personally ran all eight unchanged scientific suites from that exact extraction, using the assigned existing scientific Python with -B. The aggregate at real_eight_suite_replay/REPRODUCTION.json is PASS;149 manifest inputs match before/after, every child returned0, every copied program matches its actual source, and every scientific output field matches the frozen expectation, ignoring only the declared timestamp fields. FINAL_VALIDATION.json independently recomputes those comparisons rather than trusting the aggregate flags. It also compares root's revised-ZIP eight-suite run and root's unchanged2,657-control replay of the first reviewer; those corroborate but do not replace my own execution.

My new independent_spectral_controls.py imports no candidate checker. It projects the standard dn Fourier expansion onto subgroup modes and independently tests the exact nome Laurent product through degree32:139 series terms and561 product coefficient positions, with all nonconstant coefficients zero. A wrong even-order shift is rejected. Fifteen new spectral families cover q=1,3,9,17,31 and k=0.003,0.77,0.9999999 across five real phases each; maximum scaled discrepancy is about7.80e-100 at100 digits. Explicit truncation tails are bounded, while floating rounding is not interval-certified. Six direct circle families, including N4 and high winding31/62 cases, and the generic symbolic N4 construction test the limits and excluded class. These are materially different from repeating the submitted trace checker. Exact finite series and floating diagnostics do not substitute for the universal proof.

My independent_harness_controls.py executes the exact unchanged harness orchestration through runpy with real operating-system child fixtures. Every successful child outcome in these controls is explicitly synthetic expected-result data, never scientific evidence. Real subprocess timeout with binary partial stdout/stderr, real missing-executable launch failure, nonzero exit23, malformed JSON, missing output file, and an after-input integrity fault in a separately labelled owned clone all produce the intended aggregate FAIL. All eight outcomes and the after-input check survive; the binary markers containing NUL and non-UTF8 bytes remain byte-exact. Safe output guards reject both the archive root and a native sibling path before creation; optimized harness/integrity runs are rejected. The original archive still verifies149 files afterward. Complete failure receipts, exception traces, fixture source and raw streams remain under own_real_failure_controls/. These controlled failures are not lost or promoted into scientific successes.

The previous M1 is independently resolved on the current bytes: timeout/launch exceptions are captured before stream writing and per-suite finalization, completed suite results remain, and after-input failure prevents PASS. The new README accurately qualifies preservation by writable storage. The provided synthetic fixture program is openly labelled as orchestration testing. No remaining mandatory or optional finding follows from the previously defective path.

## Source domain, attribution, chronology and versions

SOURCE_EVIDENCE.json pins32 primary/retained evidence files read in place, both actual Ferudun source archives and every member, nine raw chronology captures and seven original/additive audit seals. Relevant primary passages, rather than previous acceptance alone, were read. Third-party primary bodies are not duplicated in this review.

The original April2020 v1 Table3 and October2020 v11 Table4, and the 2021 published Table4p346/Section3.4 with signed area in Section2, specify this target and ellipse-pair domain. The current manuscript correctly distinguishes *Eighty New Invariants* (arXiv2020) from *Fifty New Invariants* (AMJ7(2021)341-355, DOI10.1007/s40598-021-00174-y). Their historical question marks are not evidence that the problem remains currently open.

KLS2002v1 AppendixA Eq86 and v2 Eq85 give exactly the odd product-to-sum coefficient used here, with arbitrary base point. Its journal reference JMP44(2003)1822-1841 and DOI10.1063/1.1560856 are correct. KS's2003 author version and2004 Pramana63:921-936 *Connecting Jacobi elliptic functions with different modulus parameters*, DOI10.1007/BF02704331, are distinguished correctly; the retained published Eq61 matches the old identity and the Landen formulas include their normalization. A fresh publisher PDF was not authenticated in the source audit and is not claimed here; the actual2002/2003 primary PDFs already supply the mathematical inputs. AST's Theorem4 proof and Lemma3.1/Remark3.2 give the velocity/foot and skew-hodograph mechanism, BT's Theorem4.1 proof the actual center-foot telescope, Stachel's published Theorem4.3/(4.9)p1614 the canonical coordinates, and CC's Theorem6 the different original/outer theorem. Bibliographic versions, DOIs and scopes agree with the retained primary material. The known nearby Stachel dn shift-sign typo is avoided; DLMF's correct dn(z+2K)=dn(z) is used.

Ferudun v1.1, DOI10.5281/zenodo.23088516, concept DOI23087220, contains the exact full theorem in Theorem2 and Section6: the same strict domain, true boundary-tangent feet, signed stars, both parity classes and repeated listed lengths. I read the exact theorem and complete centered proof, including the odd self-paired removable-zero case and repetition argument. The actual v1.1 PDF is100,311bytes with SHA2565ff816c279e39f478e96ae5454779cc3b5280bc9eed1084429578540b3d352b6. Its actual PDF and138,800-byte source ZIP match the retained provider's MD5 checksums, and the read main source matches the ZIP member. Version1.0, DOI23087221, has the narrower primitive even arbitrary-point theorem and hence only the primitive centered even subset. It is not confused with the full version or represented as an arXiv posting merely because its archive is named arxiv_source.zip.

Actual retained raw GitHub captures contain the same11,596-byte original proof body, SHA2564f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2, and authenticate check-suite receipt of its candidate commit/tree at05:35:19Z and PR209 creation05:48:56Z on1October2026. Actual Zenodo captures give version1.0 creation16:56:14.316216Z and version1.1 creation18:12:36.529602Z that day. All nine raw capture hashes verify, including lossless decompression where needed. These establish the bounded server chronology stated in the manuscript. They do not prove past repository visibility, exclude earlier website posting, establish historical firstness, or certify independent non-derivation. No new exhaustive worldwide search is claimed. The current manuscript, metadata, deposit and native documents explicitly leave historical ordering/novelty undetermined and make no first-proof, exclusive-resolution, new-identity or current-worldwide-open claim.

Extensive AI assistance, separately prompted automated adversaries, unrefereed status, no independent human peer review and no formal verification are explicit. The contemporary theorem is not hidden behind a vague citation.

## Package, presentation and honesty

All210 source-manifest files match their actual bytes. ZIP membership is exactly those210 entries plus SOURCE_MANIFEST.json:211 unique regular members, correct CRCs, safe relative paths, no traversal/symlink/encrypted/private-paper/cache/environment payload. Source, verification, current native top-level and complete current-packet manifests match actual bytes and membership. Deposit metadata equals metadata.json and identifies the two actual upload payloads bound by PACKAGE_MANIFEST.json. Those are byte bindings, not circular approval certificates.

The actual23 intake files match both verification/original_submission and the native dated history byte-for-byte and with identical membership. Both historical16-entry author seals and four-entry inherited-review seals still verify. Current verification.json labels the historical author's unchanged proof/result explicitly; it does not misbind the edited current proof to an old receipt. Dated old source, independent-review and pending-status records retain their historical scope. Current README/PROOF/SOURCES/STATUS/readiness/PUBLICATION_STATUS and metadata consistently present the complete credited theorem and later workflow as pending separately.

I rendered and personally visually inspected all five current PDF pages against the TeX and retained the text extraction and render hashes. No missing symbol, overlap, clipping, broken reference, source/PDF discrepancy or layout defect was found. Title, author, ORCID, date, equations, explicit invariant, version/DOI references, limitations and AI disclosure are consistent.

The72,751-byte failed physical output decompresses to its recorded precompaction hash b74725bfa1ff239c31f73443898644c6fcf29cc044de4f30edc32c2c75333dbb. Temporary compaction, exact recovery, the corrected triangle derivation, the N12 negative-threshold correction, nondiscriminating wrong-construction samples, earlier missing-B caveat and preparation ENOSPC correction are disclosed. Failed evidence is not called a passing theorem check. Additive timestamp and prior-report-reference corrections preserve their original seals and payloads. The first review's clerically damaged references are resolved by its explicit supplement, not silently rewritten or treated as a current package flaw.

This review had two read-only failed alias lookups, recorded with their exact error fragments and machine bookkeeping times in FAILED_LOOKUP_01/02.json. Subsequent file discovery located the correct chronology and source-receipt records. No scientific run failed unexpectedly; deliberate negative fixtures retain all failure data. Initial assertions and timestamps have not been rewritten.

## Findings and exact remaining scope

Mandatory findings: **none**. Optional actionable findings: **none**. No candidate correction is requested by this review.

This pass covers the exact frozen scientific/preprint/native/deposit snapshot and its portable verification package. It does not authorize release and does not certify FINAL_CLEARANCE, DOI issuance, publication, tracker writes, PR updates/merge or future helper behavior. Release-helper code outside this dated package was not inspected or certified in this review. Absent future release events are not snapshot defects. Historical firstness, public-visibility history, independent historical derivation, excluded conic/arbitrary-point extensions, human peer review and formal proof verification remain unassessed or explicitly unclaimed.

All authored writes are confined to this review folder. Every Python invocation used -B; no install, environment creation, intentional cache creation, Git/index/ref/queue/database/provider/tracker write, external contact or other-agent message occurred. The end check finds no owned cache payload. Primary text and private transport bodies remained read-only in their original locations. AUTHORED_MANIFEST.json seals authored code/results/freeze/report/assessment/log and labelled candidate fixtures; its own exclusion and the copied input-tree exclusions are explicit.
'''.replace('COMPLETED_UTC',completed).replace('FROZEN_UTC',F['frozen_utc']).replace('CORE_TABLE',table)
report=report.replace('high winding31/62 cases','period31/62 stars')
(O/'REPORT.md').write_text(report)
def pin(p):
    raw=p.read_bytes();return dict(path=p.relative_to(O).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
assessment=dict(schema='pr209-whole-package-assessment-v1',review_id='whole_package_adversary_02',candidate=str(B),review_completed=True,frozen_utc=F['frozen_utc'],completed_utc=completed,frozen_bindings=F['core'],verdict='PASS',scientific_verdict='PASS in stated strict-confocal-ellipse domain',publication_snapshot_verdict='PASS_NO_FINDINGS',mandatory_findings=[],optional_findings=[],previous_review_M1_resolution='Independently verified on current frozen bytes using real OS timeout/launch/nonzero failure branches and aggregate/after-input checks',all_frozen_core_and_source_entries_unchanged_at_completion=True,actual_archive_members=211,actual_source_manifest_entries=210,actual_verification_files=149,personally_executed_real_scientific_suites=8,evidence=dict(report=pin(O/'REPORT.md'),freeze=pin(O/'FROZEN_INPUTS.json'),independent_reconstruction=pin(O/'INDEPENDENT_RECONSTRUCTION.md'),pre_prior_checkpoint=pin(O/'PRE_PRIOR_REVIEW_CHECKPOINT.json'),actual_real_reproduction=pin(O/'real_eight_suite_replay/REPRODUCTION.json'),new_spectral_controls=pin(O/'INDEPENDENT_SPECTRAL_RESULTS.json'),real_failure_controls=pin(O/'INDEPENDENT_HARNESS_RESULTS.json'),source_evidence=pin(O/'SOURCE_EVIDENCE.json'),final_validation=pin(O/'FINAL_VALIDATION.json')),reviewed_whole_package_scope=['Full universal geometric and old trace proof, exact original source domain, actual tangent feet/outer area and canonical exhaustion/phase/polarity','All residue coefficients, real denominators, parity/gcd/stars/reversal/repetition, units/circle/N4 boundary','Exact contemporary Ferudunv1.1 Theorem2/Section6, earlier classical mechanisms, bibliography/versions/DOIs and bounded chronology','Current manuscript/five-page PDF, metadata/deposit and native presentation coherence, AI/unrefereed/no human peer review disclosure','All actual frozen manifests/source members and ZIP safety, original23 file archives and historical/additive seals','Personal genuine eight-suite offline replay, independent Fourier/nome and Cartesian controls, real OS failure-branch probes and failure honesty'],explicitly_unassessed=['Release authorization, final clearance or future DOI/publication/tracker/PR/merge outcomes','Release-helper code outside this dated scientific/preprint package','Absolute firstness, exhaustive worldwide priority, undocumented public visibility or independent historical non-derivation','Human peer review, formal proof verification, excluded conics/arbitrary-point/unsigned-area extensions'],case_completion_estimate_percent=55,review_completion_estimate_percent=100,no_candidate_or_external_state_mutation=True,release_authorization=False)
(O/'ASSESSMENT.json').write_text(json.dumps(assessment,indent=2)+'\n')
with (O/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n- {completed}: Second new whole-package review complete: scientific PASS and dated snapshot PASS, mandatory0/optional0. Verified all230 candidate files unchanged, every211 ZIP member,210 source files,149 verification files, actual23 archives, personal genuine8-suite replay, new spectral/Cartesian controls, real failure branches,32 primary/retained evidence pins,9 raw chronology captures and additive seals. Actual prior M1 independently resolved. No release authorization or outside helper certification. Review100%; case55%.\n')
excluded=['actual_zip_extraction/','own_real_failure_controls/faulted_owned_archive/']
rows=[]
for p in sorted(O.rglob('*')):
    if not p.is_file() or p==O/'AUTHORED_MANIFEST.json':continue
    rel=p.relative_to(O).as_posix()
    if any(rel.startswith(prefix) for prefix in excluded):continue
    r=pin(p)
    r['role']='candidate fixture or copied science execution evidence' if '/inputs/' in rel or (rel.startswith('real_eight_suite_replay/') and p.suffix=='.py') or (rel.startswith('own_real_failure_controls/') and p.suffix=='.py') else 'authored review evidence'
    rows.append(r)
manifest=dict(schema='pr209-authored-review-sha256-v1',sealed_utc=datetime.now(timezone.utc).isoformat(),review_id='whole_package_adversary_02',self_excluded=True,files=rows,excluded_copied_input_trees=[dict(prefix=excluded[0],reason='Actual candidate ZIP input copy; every member bound in FROZEN_INPUTS and final validation, not authored'),dict(prefix=excluded[1],reason='Disposable explicitly faulted synthetic input clone; excluded from scientific input integrity assertions')],scope='Seals authored code/results/freeze/report/assessment/log plus retained raw failure evidence and clearly labelled candidate fixtures. No third-party full papers/private transport bodies, environments or caches are copied.')
(O/'AUTHORED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert all((O/r['path']).stat().st_size==r['bytes'] and hashlib.sha256((O/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in rows)
print(json.dumps(dict(completed_utc=completed,verdict='PASS',mandatory_findings=0,optional_findings=0,report=pin(O/'REPORT.md'),assessment=pin(O/'ASSESSMENT.json'),manifest=pin(O/'AUTHORED_MANIFEST.json'),sealed_files=len(rows)),indent=2))
