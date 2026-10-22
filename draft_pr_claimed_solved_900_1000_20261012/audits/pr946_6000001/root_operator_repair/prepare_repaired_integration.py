"""Adapt the independently replayed old integration to the repaired subject.

The controlled fixture retains six actual previous rounds plus synthetic07.
A fresh whole review must separately test all seven actual rounds plus08.
"""
import hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent;A=O.parent
source=(O/'baseline_operator_integration.py').read_text()
operator=(A/'publication_operator.py').read_bytes()
pin={'bytes':len(operator),'sha256':hashlib.sha256(operator).hexdigest()}
changes=[]
def replace(old,new):
    global source
    if source.count(old)!=1:raise RuntimeError('Expected one exact adaptation: '+old[:120])
    source=source.replace(old,new);changes.append({'before':old,'after':new})
replace("{'bytes':9163,'sha256':'4d219a1543a1c01ef3653ef48ade657db4dabc4c0fafe8cd245c0d13af86524e'}",repr(pin))
replace("'DEFECT_final_GET_'+kind+'_before_POST'","'REPAIRED_final_GET_'+kind+'_before_POST'")
replace("need(rec['POST_count']==1,'final GET defect did not reproduce')","need(rec['POST_count']==0,'repaired final GET allowed POST')")
replace("rec['required_finding']='FP07-OPS-001';rec['approval_or_source_invalid_before_POST']=True;rec['later_closing_guard_detected_only_after_POST']=True",
        "rec['resolved_finding']='FP07-OPS-001';rec['approval_or_source_invalid_before_POST']=True;rec['publication_blocked_before_POST']=True")
replace("rec=action('DEFECT_operator_drift_during_first_GET_survives_all_later_guards','publish',API(mutate=drift));need(rec['POST_count']==1,'operator drift defect');rec['required_finding']='FP07-OPS-002';rec['canonical_operator_drifted']=True",
        "rec=action('REPAIRED_operator_drift_during_first_GET_is_blocked','publish',API(mutate=drift),True);need(rec['POST_count']==0,'operator drift allowed POST');rec['resolved_finding']='FP07-OPS-002';rec['canonical_operator_drifted']=True")
replace("exec(compile(p.read_bytes(),str(p),\"exec\",optimize=0),n); print(sys.flags.no_site)",
        "print(sys.flags.no_site,flush=True); exec(compile(p.read_bytes(),str(p),\"exec\",optimize=0),n)")
replace("need(proc.returncode==0 and proc.stdout.strip()=='0','no-site absence was rejected')",
        "need(proc.returncode!=0 and proc.stdout.strip()=='0' and 'Use Python -I -S -B' in proc.stderr,'missing-S entry was not rejected')")
replace("'DEFECT_actual_operator_import_accepts_no_site_zero','required_finding':'FP07-OPS-003'",
        "'REPAIRED_actual_operator_import_rejects_no_site_zero','resolved_finding':'FP07-OPS-003'")
replace("out={'status':'NONCLEAN'","out={'status':'PASS'")
replace("(W/'OPERATOR_INTEGRATION.json').write_bytes(enc(out))","(W/'REPAIRED_OPERATOR_INTEGRATION.json').write_bytes(enc(out))")
replace("'required_findings':['FP07-OPS-001','FP07-OPS-002','FP07-OPS-003']",
        "'resolved_findings':['FP07-OPS-001','FP07-OPS-002','FP07-OPS-003']")
extra=r'''
# Additional actual final-GET boundaries, including same-size executable drift.
fixture_manifest=w/'MANIFEST.json';fixture_result=w/'RESULT.json'
saved={q:q.read_bytes() for q in [a/'ACCEPTANCE.json',d/'FREEZE.json',d/'research_note.tex',
    w/'FULL_AUDIT.md',fixture_manifest,p/'accept_pr946.py',a/'OPERATIONS_INVENTORY.json',
    root/next(iter(json.loads((d/'FREEZE.json').read_bytes())['evidence_files']))]}
extra_review=a/'reviews/full_package_08'
def restore_extra():
    global hold
    import shutil
    if extra_review.exists():shutil.rmtree(extra_review)
    for q,b in saved.items():q.write_bytes(b)
    clean()
for kind in ['pending','adverse','theorem','tex','freeze','payload','seal','core','inventory','evidence','operator_same_size']:
    restore_extra();(d/'ZENODO_STAGE.json').write_bytes(stage_raw)
    def invalidate(n):
        if n!=2:return
        if kind in ['pending','adverse']:
            extra_review.mkdir()
            if kind=='adverse':(extra_review/'RESULT.json').write_bytes(enc({'required_issues':[{'id':'SYNTHETIC'}]}))
        elif kind=='theorem':
            x=json.loads(accepted_raw);x['exact_claim']='SYNTHETIC revoked theorem';(a/'ACCEPTANCE.json').write_bytes(enc(x))
        elif kind=='operator_same_size':operator_path.write_bytes(source.replace(b'Resume only',b'resume only',1))
        else:
            q={'tex':d/'research_note.tex','freeze':d/'FREEZE.json','payload':w/'FULL_AUDIT.md',
               'seal':fixture_manifest,'core':p/'accept_pr946.py','inventory':a/'OPERATIONS_INVENTORY.json',
               'evidence':root/next(iter(json.loads(saved[d/'FREEZE.json'])['evidence_files']))}[kind]
            q.write_bytes(saved[q]+b'\n')
    rec=action('final_GET_blocks_'+kind,'publish',API(mutate=invalidate),True)
    need(rec['POST_count']==0,'Final GET invalidation allowed POST: '+kind)
    need(not(d/'ZENODO_PUBLISH.json').exists(),'Invalid publication receipt written')
restore_extra()
for mode in ['inspect-stage','inspect']:
    clean()
    def operator_changed(n):
        if n==1:operator_path.write_bytes(source+b'\n# SYNTHETIC changed canonical operator\n')
    rec=action('receipt_closure_blocks_operator_drift_'+mode,mode,API(mutate=operator_changed,published=mode=='inspect'),True)
    need(rec['POST_count']==0,'Read-only path published')
    need(not(d/('ZENODO_STAGE.json' if mode=='inspect-stage' else 'ZENODO_INSPECT.json')).exists(),'Invalid read-only receipt written')
clean()
'''
replace("out={'status':'PASS'",extra+"\nout={'status':'PASS'")
target=O/'repaired_operator_integration.py';target.write_text(source)
(O/'REPAIRED_INTEGRATION_ADAPTATION.json').write_text(json.dumps({
    'baseline_sha256':hashlib.sha256((O/'baseline_operator_integration.py').read_bytes()).hexdigest(),
    'adapted_sha256':hashlib.sha256(source.encode()).hexdigest(),'operator':pin,
    'controlled_replacements':changes,'new_actual_core_final_GET_and_receipt_cases':13,
    'actual_external_mutations':0,'fixture_history':'Six real prior rounds plus explicitly synthetic07; not production approval or the future whole08.'},indent=2)+'\n')
print(json.dumps({'prepared':str(target),'operator':pin,'additional_cases':13}))
