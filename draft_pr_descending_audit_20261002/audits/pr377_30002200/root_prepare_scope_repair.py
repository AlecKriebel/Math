"""Prepare additive, globally bound Ext-direction correction; preserve frozen history."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent
old=A/'snapshot/unsolved_math_prioritization/attempts/30002200'
P=A/'tmp/scope_repaired_packet'
assert not P.exists()
shutil.copytree(old,P)
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
python='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
src=(P/'verify_source_cases.py').read_text()
wrong='# Corrected exceptional extension shifts, a=b=1, m=2.\nassert 10-9!=2 and 13-9!=2;checks+=1'
assert src.count(wrong)==1
right='''# Current correction: derive the FREE TARGET shifts from coker(iota)[rd].
# V_J has homological degree -3|J|; high V_J survive in the cokernel.
# FREE QUOTIENT shifts instead come from ker(iota)[rd-1] and W_J.
r=5;m=2;d=3;dbar=1
left_free_targets=sorted(r*d-j*d for j in range(m+2,r+1))
right_free_quotients=sorted(r*d-1-j*d-dbar for j in range(m))
right_koszul_shift=(m+2)*d-2*dbar-1
differences=[l-right_koszul_shift for l in left_free_targets]
assert (left_free_targets==[0,3] and right_free_quotients==[10,13]
        and right_koszul_shift==9 and differences==[-9,-6]
        and all(x!=2 for x in differences));checks+=1'''
(P/'verify_corrected_source_cases.py').write_text(src.replace(wrong,right))
src=(P/'review/independent_check.py').read_text()
wrong='ck([3*j-2-9 for j in [4,5]]==[1,4])'
assert src.count(wrong)==1
right='''# Independently generated left/right free summands at rank5.
# Coker high V subsets are TARGETS, ker low W subsets are QUOTIENTS.
rank=5;half=2;sphere_dim=3;fixed_dim=1
targets=sorted(rank*sphere_dim-size*sphere_dim for size in range(half+2,rank+1))
quotients=sorted(rank*sphere_dim-1-size*sphere_dim-fixed_dim for size in range(half))
quotient_koszul=(half+2)*sphere_dim-2*fixed_dim-1
ck(targets==[0,3] and quotients==[10,13] and quotient_koszul==9
   and [shift-quotient_koszul for shift in targets]==[-9,-6]
   and all(shift-quotient_koszul!=2 for shift in targets))'''
src=src.replace(wrong,right).replace('rank parities and corrected shifts.','rank parities and corrected free-target/quotient extension direction.')
(P/'review/independent_check_corrected.py').write_text(src)
streams=[]
for name,script,out in [('corrected_author','verify_corrected_source_cases.py','CORRECTED_SOURCE_CASE_CHECKS.json'),('corrected_review','review/independent_check_corrected.py','review/CORRECTED_INDEPENDENT_CHECKS.json')]:
 r=subprocess.run([python,'-B',str(P/script)],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (A/('root_prepared_'+name+'.stdout')).write_bytes(r.stdout);(A/('root_prepared_'+name+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(script,r.stderr.decode());(P/out).write_bytes(r.stdout)
 streams.append({'script':script,'receipt':out,'bytes':len(r.stdout),'sha256':sha(r.stdout),'output':json.loads(r.stdout)})
note='''# Current mathematical correction: extension direction

This note supersedes the exceptional-rank extension paragraph in the frozen CREDITED_PROOF_GUIDE.md and review/REVIEW.md, and the final extension assertion in each frozen checker. It does not alter the credited all-rank existence conclusion or assert a new solution.

At a=b=1, r=5, m=2, the actual primary sequence is

    0 -> C=(coker iota)[15] -> H_T*(X) -> Q=(ker iota)[14] -> 0,
    C=R[0] plus R[3]^5 plus K_2[6],
    Q=K_4[9] plus R[10]^5 plus R[13].

The free TARGET shifts in Ext1(Q,C) are0 and3. The shifts10 and13 belong to free QUOTIENT summands; these split automatically and cannot be used as Ext targets. Consequently the relevant target-minus-quotient differences are−9 and−6, not1 and4. AFP Lemma2.4, with polynomial generators of degree2, gives Ext1(K_4[9],R[l]) degree0 nonzero only if l−9=2. Neither actual target satisfies this condition. The K_4[9]-to-K_2[6] extension vanishes by parity. Thus the splitting conclusion is valid with the corrected justification.

For every odd rank2m+1, the free targets arise from high-cardinality V_J in the cokernel, of shifts3r−3|J| for |J|>m+1. The free quotient shifts arise from low-cardinality W_J in the kernel, of shifts3r−2−3|J| for |J|<m. These complement indices explain the final source's displayed direct-sum formula but cannot be interchanged inside its proof sequence. Corrected v4 nonfree shifts remain3m and3m+3. For m≥3 the relevant positive Ext into a free module occurs only in degree m−1>1. No rank is omitted.

The exact-order proof also requires no splitting. At the homogeneous maximal ideal C has depth m and Q has depth m+2, so the middle has depth exactly m by the depth lemma. Away from that ideal a variable is invertible and both localized Koszul terms are free. This proves the mth-syzygy inequalities at all primes and failure at m+1. For even rank the extra effective circle sphere has free cohomology Q[s] plus Q[s][3]. Polynomial extension preserves the lower bound and a witness prime excluding s retains depth m. Full enlarged maximal depth alone would give an incorrect inference.

The two original programs and their PASS outputs remain immutable historical arithmetic evidence. Their original final assertions checked the wrong shifts; replay success never established semantic correctness of those assertions. verify_corrected_source_cases.py and review/independent_check_corrected.py replace those assertions with shifts derived from the actual inclusion-map degrees. Their complete outputs are separately bound. Counts overlap the historical controls and are not additional distinct358064/983 discoveries. A new whole-package adversary must verify this repair before acceptance. All current publication wrappers bind this note and those corrected programs/receipts.

This is a rational b=1 construction. The source's blanket free-target splitting assertion for b>1 is not exported: Ext then contains R/(t_i^b), whose positive degrees can allow further classes. The separate Puppe splitting argument is not required by the nonsplit depth proof and is not newly certified here. The fixed-circle Euler t_j and the vanishing negative Morse-bundle Euler are different; the candidate's perfection uses reflection characters. The source's separate dimension bound requires effective action, and no minimal-dimension result is claimed.

Disposition remains credited already_solved,0/5. Extensive AI tools were used; this reconstruction is unrefereed and is not external human peer review. No paper, new DOI, Zenodo deposit, tracker row or release.
'''
(P/'CURRENT_SCOPE_CORRECTION.md').write_text(note)
files=['CURRENT_SCOPE_CORRECTION.md','verify_corrected_source_cases.py','CORRECTED_SOURCE_CASE_CHECKS.json','review/independent_check_corrected.py','review/CORRECTED_INDEPENDENT_CHECKS.json']
entries=lambda names:[{'path':n,'bytes':len((P/n).read_bytes()),'sha256':sha((P/n).read_bytes())} for n in names]
current={'utc':utc,'problem_id':30002200,'status':'already_solved','author_turns':0,'correction':'Free targets and free quotients in the rank-five Ext argument; historical author/review preserved','superseded_historical_claims':[{'path':n,'sha256':sha((P/n).read_bytes())} for n in ['CREDITED_PROOF_GUIDE.md','verify_source_cases.py','review/REVIEW.md','review/independent_check.py']],'files':entries(files)}
(P/'CURRENT_SCOPE_MANIFEST.json').write_text(json.dumps(current,indent=2)+'\n')
(P/'PUBLICATION.md').write_text('''# Credited prior resolution: already solved,0/5

Franz's published big polygon construction answers the original rational all-rank sharpness question. No new solution, minimal dimension, integral or positive-characteristic extension is claimed. Odd ranks use equilateral a=b=1; even ranks add the independently acting sphere factor.

Read CURRENT_SCOPE_CORRECTION.md as the authoritative current qualification. The original guide, both checkers and prior review reversed the rank-five free-target/free-quotient roles in one justification. Actual targets0,3 give differences−9,−6 against K4[9];10,13 are free quotients. The corrected justification and splitting-independent depth proof retain the exact syzygy order. CURRENT_SCOPE_MANIFEST.json binds the correction and two corrected programs/receipts; every current wrapper verifies it. The11 author and5 prior-review files retain frozen bytes as historical records; their old PASS receipts are arithmetic replay evidence, not semantic validation of the superseded assertion. Corrected counts overlap historical checks and are not new distinct control counts.

Run python verify_publication.py with SymPy1.14.0. It checks all current and historical hashes, reproduces both historical streams and both corrected streams, and explicitly does not fetch/reverify source PDFs. SOURCE_MANIFEST.json binds four primary URLs/hashes separately. Fresh source reading and a new whole-package adversary remain distinct from these executable checks. The corrected2023 author version is distinguished from the2015 IMRN publication; later published corroboration is Franz–Huang2020. Source cautions and original author/review history remain explicit.

AI tools were used extensively. This is unrefereed and is not external human peer review. Accept only as credited literature findings after final audit; no paper, Zenodo, DOI, tracker row or release.
''')
(P/'verify_publication.py').write_text('''from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
manifests=[(p/'PUBLICATION_MANIFEST.json',p),(p/'FINAL_SOURCE_MANIFEST.json',p),(p/'review/REVIEW_MANIFEST.json',p/'review'),(p/'CURRENT_SCOPE_MANIFEST.json',p)]
for manifest,root in manifests:
 for e in json.loads(manifest.read_text())['files']:
  b=(root/e['path']).read_bytes()
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(manifest.name,e['path'])
for script,receipt in [('verify_source_cases.py','SOURCE_CASE_CHECKS.json'),('review/independent_check.py','review/INDEPENDENT_CHECKS.json'),('verify_corrected_source_cases.py','CORRECTED_SOURCE_CASE_CHECKS.json'),('review/independent_check_corrected.py','review/CORRECTED_INDEPENDENT_CHECKS.json')]:
 out=subprocess.check_output([sys.executable,'-B',str(p/script)])
 assert out==(p/receipt).read_bytes(),script
print(json.dumps({'publication_bound_files':len(json.loads((p/'PUBLICATION_MANIFEST.json').read_text())['files'])+1,'frozen_author_files':11,'frozen_review_files':5,'historical_and_corrected_receipts_byte_exact':True,'source_pdfs_reverified':False,'current_ext_free_targets':[0,3],'current_ext_target_minus_quotient':[-9,-6],'old_assertions_historical_only':True,'scope_correction_globally_bound':True},sort_keys=True))
''')
pub=json.loads((P/'PUBLICATION_MANIFEST.json').read_text());pub['current_scope_manifest']='CURRENT_SCOPE_MANIFEST.json';names=[e['path'] for e in pub['files']]+files+['CURRENT_SCOPE_MANIFEST.json'];assert len(set(names))==len(names);pub['files']=entries(names);(P/'PUBLICATION_MANIFEST.json').write_text(json.dumps(pub,indent=2)+'\n')
for name in ['FINAL_SOURCE_MANIFEST.json','review/REVIEW_MANIFEST.json']:
 assert (P/name).read_bytes()==(old/name).read_bytes()
historical=[e['path'] for e in json.loads((old/'FINAL_SOURCE_MANIFEST.json').read_text())['files']]+['FINAL_SOURCE_MANIFEST.json']+['review/'+e['path'] for e in json.loads((old/'review/REVIEW_MANIFEST.json').read_text())['files']]+['review/REVIEW_MANIFEST.json']
assert len(historical)==16
for name in historical:assert (P/name).read_bytes()==(old/name).read_bytes()
r=subprocess.run([python,'-B',str(P/'verify_publication.py')],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(A/'root_prepared_publication.stdout').write_bytes(r.stdout);(A/'root_prepared_publication.stderr').write_bytes(r.stderr);assert r.returncode==0 and not r.stderr,r.stderr.decode()
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_frozen_head':'75bea4d3be9904e90c3843892671a440ba4d2c42','private_packet':str(P),'original_target_files':19,'current_target_files':25,'historical_target_files_unchanged':16,'only_changed_prior_paths':['PUBLICATION.md','PUBLICATION_MANIFEST.json','verify_publication.py'],'six_new_correction_files':files+['CURRENT_SCOPE_MANIFEST.json'],'all_current_bindings_and_four_fullstreams_verified':True,'publication_stdout_sha256':sha(r.stdout),'publication_full_stdout':json.loads(r.stdout),'corrected_streams':streams,'files':entries(sorted(str(x.relative_to(P)) for x in P.rglob('*') if x.is_file())),'workflow_percent':70,'branch_push_pending_prior378_actual_acceptance':True,'new_whole_package_review_pending':True,'paper':False,'doi':False}
(A/'scope_repair_preparation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='files'},indent=2))
