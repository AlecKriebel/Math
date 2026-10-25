"""Record root's full-manuscript/final-report adoption with unchanged source custody."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile

P=Path(__file__).resolve().parents[1]
def sha(f):
    with Path(f).open('rb')as s:return hashlib.file_digest(s,'sha256').hexdigest()
def load(f):return json.loads(Path(f).read_text())
def save(f,d):Path(f).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat()
# These two reading-only third-party excerpts were accidentally tracked in the
# prior checkpoint. Preserve their exact bytes privately and remove tracked
# working copies on the next ordinary programme checkpoint; do not rewrite history.
for part in [1,2]:
    old=P/f'papers/23430326/reviews/root/primary-flo-reading-part{part}.txt'
    private=P/f'papers/23430326/sources/primary-cache/root-flo-reading-part{part}.txt'
    if old.exists():
        assert not private.exists()
        old.rename(private)

specs={
 '23390551':{
  'version':'1.0','date':'2026-10-15','receipt':'sources/acquisition_receipt.json','metadata':'sources/zenodo_record.json',
  'pdf':'sources/cache/dipole_spectrum.pdf','zip':'sources/cache/dipole_spectrum_verification.zip',
  'pdf_sha':'7fc583c50f2d75e08fc008d0b7891a81135fa8c2109af9f33472f2a492784d46','zip_sha':'5cbd35e7c4b30d3d7e90a953cffb689b03bc957e60c4aa6905b0a60e38c069d7',
  'seals':[('reviews/scope/SEALED_MANIFEST.json','.'),('reviews/analytic/artifact_seal.json','reviews/analytic'),('reviews/adversarial/HASH_SEAL.json','reviews/adversarial')],
  'reports':{'scope':'reviews/scope/REVIEW.md','analytic':'reviews/analytic/REVIEW.md','adversarial':'reviews/adversarial/REVIEW.md'},
  'scope':'Full published Theorems1and5: fixedcomplexfrequency, boundedmeasurableOmega with chosenrepresentative and center-selectedtranslatedcubicvoxels satisfying volume(G); actualzerodiagonalDDA offexactclosedstaticlatticeinterval,uniformcompactresolventstability,nooffintervalpollution,normconvergentembeddedRieszprojections,totalalgebraicmultiplicity,bothgeneralizedsubspacegaps,uniformmatrixnorms. Existentialfixedcompactpositive-volumeempty-interiorobstructionatfrequency1/10000withallrationalmeshes3x3zero.',
  'limits':['No inside-interval correctness, exact numerical endpoint extrema, rate, mesh-dependent frequency, individual Jordan sizes, necessary geometry classification or effective support index.', 'Unseen Rahola and announced2022/2023time-harmonic bodies remain priority/coverage limits; no unseen theorem is imported centrally.'],
  'proof':'''Root read the complete actual eleven-page selected PDF before any full family report, then all three COMPLETE final reports and original verdicts. Actual PDF pages2,6,9 were visually checked: closed numerical-range bar, conjugate spectral parameter and closed-ball bar are present. The paired TeX confirms these symbols. No source text was repaired.

The distributional shift is A_kappa-I/3. The static full-lattice bound is imported from actual CDN arXiv2302.13159v3: root read the exact homogeneous/cancellation hypotheses, Theorem1.6, matrix extension/Lemma2.7, full relevant3.5.1-2/Proposition3.15 statement and proof, and numerical qualification3.5.4. Root also read Costabel's entire original OWR contribution2580-2582. Deep Ewald/source theorems remain established dependencies, not newly reproved foundations.

Root reconstructed exact finite radial-shell cancellation, the O(delta) near estimate, translated smooth far quadrature and uniform r^-3 tails giving whole-space strong static consistency. Volume(G) gives strong mask convergence. The actual zero-diagonal dynamic kernel has near-diagonal L2 mass O(delta+h); uniform far continuity and mask-volume control give Hilbert-Schmidt convergence. This is the actual sampled matrix, not an integrated-cell substitute.

Factoring z-S through the selfadjoint static resolvent makes R_n C_n converge in norm. On isolating contours the analytic static term integrates to zero. The remaining compact factor on the left uses strong convergence of ADJOINT resolvents, supplied at conjugate z by selfadjointness. Thus Riesz projections converge in norm, finite ranks agree and both gaps and total algebraic clusters converge. Full static norm/resolvent convergence and individual Jordan preservation are neither needed nor claimed. Extra whole-space zero complements lie inside the excluded interval.

For Theorem5, root reconstructed the intrinsic ball decomposition and harmonic spectrum: three constant modes form the isolated shifted zero eigenspace, gap1/15. Taylor remainder/graph estimates give Im trace <= -2kappa^3/3+1446kappa^4, exactly -(7831/15000)kappa^3 at1/10000. This certifies some nonreal eigenvalue, not simplicity or a computed location. Rational holes in the CLOSED ball leave nested compact positive-volume empty-interior sets; a restored isolated null anchor is the sole rational-mesh center. Strong static mask and Hilbert-Schmidt dynamic convergence preserve a nonreal cluster on one sufficiently large FIXED support. Its index is existential and(G) fails there.

The complete current family reports provide independent exact controls and quarantined fresh replays; their numerical illustrations are not universal proofs. Root independently rehashed final seals and all323 recursively mapped archive occurrences. No substantive defect or central unresolved gap was found at the literal scope. Every original custom scope/verdict and receipt remains unchanged; this later root adoption is separate. Historical firstness and worldwide novelty/openness remain unverified. No follow-up met the high bar. Scientific review100%; overall203-paper programme remains ongoing.'''
 },
 '23430326':{
  'version':'1.1','date':'2026-10-16','receipt':'sources/receipt.json','metadata':'sources/record.json',
  'pdf':'sources/paper.pdf','zip':'sources/pr1032_supportkit_v1.1.zip',
  'pdf_sha':'1144eb3999212084bef013e7984bfc54bf43a9f931d959b63ba2743d814cf0a9','zip_sha':'1f1a66d7e67b1434e4c17af96c9461b1d2f6bd7f4197de4ef88f95aad8105dc1',
  'seals':[('reviews/scope/SEAL.json','.'),('reviews/analytic/FINAL_SEAL.json','reviews/analytic'),('reviews/adversarial/FINAL_ARTIFACT_HASHES.json','reviews/adversarial')],
  'reports':{'scope':'reviews/scope/REVIEW.md','analytic':'reviews/analytic/REPORT.md','adversarial':'reviews/adversarial/REPORT.md'},
  'scope':'Full published Theorem1: F=Q3,E/Funramifiedquadratic,smoothadmissiblecomplexGL15,LanglandsQUOTIENTm=[0,2]+[1,4]+[3,3]+[2,5]+[4,6] is tau-invariant,notanENTIREpropernormalizedparabolicinduction,andHom_U(V)(pi,C)=0forEVERYnonsingulardimension15HermitianV; historicalk1orbit-total0versus2,FLO6.12andunrestrictedlocalunitaryconverseconsequences.',
  'limits':['Exact field/category instance; no all-field, modular, global or unitarizable/generic/spherical claim. No kernel-generation equality or separate disproof.', 'Complete Luo-Zha substantive overlap, transformed parameters, mechanism and period consequences remain UNKNOWN. Example may overlap, be contained in or be superseded; no firstness/current-openness claim.','FLO N definition is the unnumbered display immediately before(1.10), whose Whittaker identity follows. Given p201 locator and actual normalization are unambiguous; optional bibliographic precision only, no mandatory mathematical repair.'],
  'proof':'''Root read the entire actual nine-page published PDF before any full final reviewer report. Root then read all three COMPLETE final reports and every original verdict. The independently recorded root initial proof checkpoint precedes those report readings. All sources remain unchanged.

Root directly read actual primary FLO printed201-202,217,224-225,242,283,289-294, quotient/preorder definitions, tau-Witt definitions214-215 and Conjecture6.12; LM actual segment/classification/additive constituent, Definition5.13, exact graph arrows/left shift, Proposition5.20 with relevant proof and same-parameter ring involutionA.5; actual JPSS scanned395-396/444-445; exact historical OWR Conjectures1/4 and imprimitive definition. These published deep theorems remain dependencies, not newly reproved. Two cached primary-reading excerpts were mistakenly tracked in a checkpoint; their exact bytes were moved to ignored local primary-cache and working tracked copies removed, without rewriting history. No public paper or source theorem was changed.

Centers5,7/2,3,5/2,1 and lengths3,4,1,4,3 give the proper standard module and unique tau-invariant quotient. Each of three admissible orders has the complete16-coordinate unnormalized period basis for EACH fixed Hermitian orbit. Common quadratic twist fixes a representative epsilon_T=0 without losing coordinates. Generic compatibility is used only for individual square-integrable inducing factors.

Root independently derived gamma(-u,i-dual*j)/gamma(u,i*j-dual) as L(1+u,ij-dual)L(u,ij-dual)/[L(-u,i-dualj)L(1-u,i-dualj)], giving the displayed Q(z^-1)/P(z) factor. Opposite-label linked coefficients have zeros2,2,1,2,1; equal-label coefficients are units. Nested DC/CB have unit F coefficients and E normalizers. Strict center difference1/2 plus chamber holomorphy and meromorphic inverse identities give ACTUAL specialized inverse operators. They transport segment-labelled supports by nonzero diagonal scalars.

Each linked reverse image, after exact nonzero-preserving induction, remains a proper submodule and lies in the unique maximal quotient kernel. A quotient period annihilates it at zero. Constant-coefficient extensions need not vanish off zero; restricting the functional equation to entire INDEPENDENT open-orbit functionals makes specialization legitimate. Thus equal labels are deleted coordinatewise. The transported necessary opposite constraints TD,DB,BA,AC,CT form a5cycle, impossible overF2. No equality generating the whole maximal kernel is assumed.

Any ENTIRE proper irreducible induction reduces to a two-factor irreducible product. The multiplicity-one additive Langlands constituent forces an actual multisegment partition, not just equal cuspidal support. All15 unordered partitions have a ladder side; the exact two directed LC obligations and same-parameter Z-to-L ring involution apply. Every published entire-Y/witness row gives an isolated X in one direction, so no partition survives. This proves entire noninduction and the fixed-orbit vanishing. The historical k1 sum over two forms is0 instead of2; tau-Witt index0 follows from the individually invariant unitary Steinberg Langlands inputs, not an unproved quotient-descent theorem.

Independent analytic and nilpotent-tensor falsification computations support all40 germs,30 directed graphs,15 exact current manuscript rows and the parity obstruction. Supplied code was inspected by root at its central scalar/graph/table/allowlist interfaces; independent safe replays in the complete reports are supplementary finite evidence, not Hom computations. Root rehashed every final family seal and all37 original archive members. Reviewers' initial timestamp transcription errors are explicitly corrected in their custody records; original early-sealed bytes remain intact. No substantive mathematical defect or central missing implication was found. Optional source-locator precision is nonblocking. Full Luo-Zha overlap/priority remains UNKNOWN exactly as the manuscript prominently discloses. No source repair or follow-up was authorized. Scientific review100%; overall203-paper programme ongoing.'''
 }
}
results=[]
for rid,s in specs.items():
    p=P/'papers'/rid;root=p/'reviews/root';root.mkdir(exist_ok=True)
    checked=[]
    for seal_file,relative_base in s['seals']:
        d=load(p/seal_file);entries=d.get('files',d.get('objects'))
        if isinstance(entries,dict):entries=[{'path':path,**v}for path,v in entries.items()]
        for e in entries:
            f=p/relative_base/e['path']
            assert f.stat().st_size==e['bytes']and sha(f)==e['sha256'],str(f)
            checked.append({'path':str(f.relative_to(P)),'bytes':e['bytes'],'sha256':e['sha256']})
    assert sha(p/s['pdf'])==s['pdf_sha']and sha(p/s['zip'])==s['zip_sha']
    if rid=='23390551':
        members=load(p/'sources/custody_before.json')['members']
        for e in members:
            f=p/'sources'/e['cache_relative_path']
            assert f.stat().st_size==e['bytes']and sha(f)==e['sha256'],str(f)
        count=len(members);assert count==323
    else:
        with zipfile.ZipFile(p/s['zip'])as z:
            members=[x for x in z.infolist()if not x.is_dir()];assert len(members)==37
            for e in members:assert z.read(e)==(p/'sources/support'/e.filename).read_bytes()
        count=len(members)
    custody=root/'custody-recheck-20261025.json'
    save(custody,{'utc':now,'status':'PASS','final_family_seal_bindings_rehashed':checked,'archive_members_byte_compared':count,'pdf_sha256':s['pdf_sha'],'supplement_sha256':s['zip_sha'],'source_receipt_sha256':sha(p/s['receipt']),'metadata_sha256':sha(p/s['metadata']),'source_repair':False})
    report=root/'ROOT_REVIEW.md';report.write_text('# Root scientific disposition: '+rid+'\n\n'+now+'\n\n'+s['proof']+'\n')
    reviews={}
    for role,path in s['reports'].items():
        verdict='reviews/'+role+'/verdict.json'
        reviews[role]={'report':str((p/path).relative_to(P)),'report_sha256':sha(p/path),'verdict':str((p/verdict).relative_to(P)),'verdict_sha256':sha(p/verdict),'root_disposition':'SCOPE_COMPLETE'if role=='scope'else'PASS'}
    c={'utc':now,'record_id':rid,'status':'PASS','disposition_by':'root','reviewed_zenodo_version':s['version'],'publication_date':s['date'],'actual_complete_published_manuscript_read':True,'all_complete_final_family_reports_and_verdicts_read':True,'approved_scope':s['scope'],'scope_gate_resolution':'Original scope-only pending/null/false fields remain unchanged. Later root actual-proof and primary-interface assessment together with complete independent analytic/adversarial reviews clears the full literal published scope.','root_review':str(report.relative_to(P)),'root_review_sha256':sha(report),'source_receipt_path':s['receipt'],'source_receipt_sha256':sha(p/s['receipt']),'metadata_path':s['metadata'],'metadata_sha256':sha(p/s['metadata']),'pdf_sha256':s['pdf_sha'],'supplement_sha256':s['zip_sha'],'reviews':reviews,'root_custody_receipt':str(custody.relative_to(P)),'root_custody_receipt_sha256':sha(custody),'seal_bindings_rehashed':len(checked),'original_archive_members_compared':count,'limits':s['limits'],'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,'follow_up':None,'rendered_live_browser_native_gates_passed':False,'completion_estimate_percent_this_scientific_review':100,'overall_goal_complete':False}
    save(P/('verification/root-clearance-'+rid+'-20261025.json'),c)
    (root/'RESEARCH_LOG.md').open('a').write(now+' — Root actual fullpaper/all3completefinalreports/primaryinterfaces adopted; science100%, source/archiveseals exact. No priority/human-review/formalization claim. Overall catalogue ongoing.\n')
    results.append({'record':rid,'family_bindings':len(checked),'archive_members':count,'root_clearance_sha256':sha(P/('verification/root-clearance-'+rid+'-20261025.json'))})
print(json.dumps(results))
