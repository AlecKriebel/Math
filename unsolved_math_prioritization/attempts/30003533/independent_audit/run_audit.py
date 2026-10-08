#!/usr/bin/env python3
"""Replay the independent audit against the frozen, unchanged author packet."""
import sys
sys.dont_write_bytecode=True
import difflib,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PACKET=ROOT.parent/'public'
MODES=[[],['-O'],['-OO']]
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')

def need(ok,label):
    if not ok:raise RuntimeError(label)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(p):return {x.name:{'sha256':sha(x),'mode':x.stat().st_mode & 0o777,'bytes':x.stat().st_size} for x in p.iterdir()}
def mutable_copy(source,target):
    shutil.copytree(source,target);target.chmod(0o755)
    for f in target.iterdir():f.chmod(0o644)

def run(script,mode,args=()):
    return subprocess.run([sys.executable,'-B']+mode+[str(script)]+list(args),cwd='/tmp',env=ENV,text=True,capture_output=True)

def replace_once(text,old,new):
    need(text.count(old)==1,'correction preimage is not unique')
    return text.replace(old,new)

def corrections(p):
    f=p/'PROOFS.md';s=f.read_text()
    s=replace_once(s,'Thus a coercive weighted form transfers only if this sufficient condition c>δ||A|| is verified.','This criterion guarantees transfer when c>δ||A|| is verified; it is sufficient, not necessary.')
    f.write_text(s)
    f=p/'verify.py';s=f.read_text()
    s=replace_once(s,"need([a.get('turn') for a in attempts]==[1,2,3,4,5],'ledger order')","need(all(type(a) is dict and type(a.get('turn')) is int for a in attempts),'ledger turn type')\n    need([a.get('turn') for a in attempts]==[1,2,3,4,5],'ledger order')")
    f.write_text(s)
    f=p/'selftest.py';s=f.read_text()
    s=replace_once(s,'def mutate(p,case):','def mutable_copy(source,target):\n    shutil.copytree(source,target)\n    target.chmod(0o755)\n    for f in target.iterdir(): f.chmod(0o644)\n\ndef mutate(p,case):')
    s=replace_once(s,"    name='CLAIMS.json';d=json.loads((p/name).read_text())","    if case=='ledger_bool_turn':\n        name='LEDGER.json';d=json.loads((p/name).read_text())\n        d['attempts'][0]['turn']=True\n        (p/name).write_text(json.dumps(d,indent=2)+'\\n');rebind(p,name);return\n    name='CLAIMS.json';d=json.loads((p/name).read_text())")
    s=replace_once(s,"'duplicate_key','nonfinite','truncated_json']","'duplicate_key','nonfinite','truncated_json','ledger_bool_turn']")
    s=replace_once(s,'p=temp/case;shutil.copytree(ROOT,p);mutate(p,case)','p=temp/case;mutable_copy(ROOT,p);mutate(p,case)')
    f.write_text(s)
    f=p/'VALIDATION.md';s=f.read_text()
    s=replace_once(s,'boolean/integer type confusion, an unknown claim','boolean/integer type confusion in claims and attempt ordinals, an unknown claim')
    s=replace_once(s,'The self-test creates and removes only disposable temporary directories.','The self-test creates and removes only disposable temporary directories. Mutation copies are made writable after copying, so replay also works when the source packet itself is read-only; the original packet is never made writable.')
    s=replace_once(s,'twelve mutation cases, each rejected in all three modes (36 rejections)','thirteen mutation cases, each rejected in all three modes (39 rejections)')
    f.write_text(s)
    m=json.loads((p/'MANIFEST.json').read_text())
    for name in m['files']:
        b=(p/name).read_bytes();m['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (p/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')

def rebind(p,name):
    m=json.loads((p/'MANIFEST.json').read_text());b=(p/name).read_bytes();m['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};(p/'MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')

def mutate(p,case):
    if case=='extra':(p/'EXTRA').write_text('x');return
    if case=='missing':(p/'RESULT.md').unlink();return
    if case=='symlink':(p/'RESULT.md').unlink();(p/'RESULT.md').symlink_to('PROOFS.md');return
    if case=='corrupt_proof':(p/'PROOFS.md').write_text('corrupt');return
    if case=='duplicate_manifest':(p/'MANIFEST.json').write_text('{"schema_version":1,"schema_version":1,"files":{}}');return
    if case=='manifest_bool_bytes':
        m=json.loads((p/'MANIFEST.json').read_text());m['files']['RESULT.md']['bytes']=True;(p/'MANIFEST.json').write_text(json.dumps(m));return
    name='CLAIMS.json';v=json.loads((p/name).read_text())
    if case=='duplicate':(p/name).write_text('{"status":"unsolved","status":"unsolved"}');rebind(p,name);return
    if case=='truncated':(p/name).write_text('{');rebind(p,name);return
    if case=='nonfinite':(p/name).write_text('{"x":NaN}');rebind(p,name);return
    if case=='infinity':(p/name).write_text('{"x":Infinity}');rebind(p,name);return
    if case=='claims_list':v=[]
    elif case=='false_solved':v['original_target_resolved']=True
    elif case=='false_smooth':v['smooth_counterexample_proved']=True
    elif case=='false_curvature':v['geometric_controls']['curvature_at_pi_over_3']='8/3'
    elif case=='unknown_claim':v['unknown']=False
    elif case=='bool_schema':v['schema_version']=True
    elif case=='float_dimension':v['deformation_dimension']=3.0
    elif case=='wrong_coupling':v['coupling']='eta may depend on k'
    elif case=='wrong_operator':v['operator']='0.5 I + D_k - i eta S_k'
    elif case.startswith('ledger_'):
        name='LEDGER.json';v=json.loads((p/name).read_text())
        if case=='ledger_bool_turn':v['attempts'][0]['turn']=True
        elif case=='ledger_missing_gap':del v['attempts'][0]['gap']
        elif case=='ledger_wrong_rank':v['rank']=999
        elif case=='ledger_false_solved':v['original_target_resolved']=True
        else:raise ValueError(case)
    else:raise ValueError(case)
    (p/name).write_text(json.dumps(v)+'\n');rebind(p,name)

def main():
    before=snapshot(PACKET)
    receipt={'problem_id':30003533,'original_manifest_sha256':sha(PACKET/'MANIFEST.json'),'original_unchanged':False,'pde_target_resolved':False}
    author=[];independent=[];failures=[]
    for mode in MODES:
        r=run(PACKET/'verify.py',mode);need(r.returncode==0,'original author verifier');author.append(json.loads(r.stdout))
        r=run(ROOT/'independent_controls.py',mode);need(r.returncode==0,r.stderr);independent.append(json.loads(r.stdout))
        r=run(PACKET/'selftest.py',mode)
        need(r.returncode!=0 and 'PermissionError' in r.stderr,'read-only harness defect not reproduced')
        failures.append({'mode':mode or ['normal'],'exception':'PermissionError','stage':'mutating a copied read-only proof'})
    receipt['original_author_controls']=author[0];receipt['independent_controls']=independent[0];receipt['original_readonly_selftest_failures']=failures
    receipt['original_normal_O_OO_author_and_independent_passes']=6
    cases=['extra','missing','symlink','corrupt_proof','duplicate_manifest','manifest_bool_bytes','duplicate','truncated','nonfinite','infinity','claims_list','false_solved','false_smooth','false_curvature','unknown_claim','bool_schema','float_dimension','wrong_coupling','wrong_operator','ledger_bool_turn','ledger_missing_gap','ledger_wrong_rank','ledger_false_solved']
    rejected=0
    with tempfile.TemporaryDirectory(prefix='independent_coercivity_audit_') as tmp:
        tmp=Path(tmp)
        for case in cases:
            p=tmp/case;mutable_copy(PACKET,p);mutate(p,case)
            for mode in MODES:
                r=run(ROOT/'independent_controls.py',mode,['--packet',str(p),'--manifest',sha(p/'MANIFEST.json')])
                need(r.returncode!=0,'independent mutation accepted: '+case);rejected+=1
            if case=='ledger_bool_turn':
                for mode in MODES:
                    r=run(p/'verify.py',mode);need(r.returncode==0,'original ledger bool defect not reproduced')
        p=tmp/'corrected';mutable_copy(PACKET,p);corrections(p)
        patch=''
        for name in sorted(before):
            a=(PACKET/name).read_text().splitlines(keepends=True);b=(p/name).read_text().splitlines(keepends=True)
            patch+=''.join(difflib.unified_diff(a,b,fromfile='a/'+name,tofile='b/'+name))
        (ROOT/'CORRECTIONS.patch').write_text(patch)
        (ROOT/'CORRECTED_MANIFEST.json').write_bytes((p/'MANIFEST.json').read_bytes())
        corrected_manifest=sha(p/'MANIFEST.json')
        for f in p.iterdir():f.chmod(0o444)
        p.chmod(0o555)
        corrected_before=snapshot(p);corrected_runs=[]
        for mode in MODES:
            r=run(p/'selftest.py',mode);need(r.returncode==0,r.stderr);corrected_runs.append(json.loads(r.stdout))
            r=run(ROOT/'independent_controls.py',mode,['--packet',str(p),'--manifest',corrected_manifest]);need(r.returncode==0,r.stderr)
        need(snapshot(p)==corrected_before,'corrected readonly copy changed')
        receipt['corrected_manifest_sha256']=corrected_manifest
        receipt['corrected_selftest_modes']=corrected_runs
        receipt['corrected_independent_modes_passed']=3
        receipt['corrected_readonly_bytes_and_modes_preserved']=True
        # Genuine relocation of the unmodified original; neither files nor parent writable.
        q=tmp/'original_relocated';shutil.copytree(PACKET,q);relocated_before=snapshot(q)
        for mode in MODES:
            r=run(ROOT/'independent_controls.py',mode,['--packet',str(q)]);need(r.returncode==0,r.stderr)
        need(snapshot(q)==relocated_before,'relocated original changed')
        receipt['original_readonly_relocation_modes_passed']=3
        # Verify the deliverable patch independently, rather than trusting correction generation.
        q2=tmp/'patch_applied';mutable_copy(PACKET,q2)
        r=subprocess.run(['patch','--batch','--forward','-p1','-i',str(ROOT/'CORRECTIONS.patch')],cwd=q2,text=True,capture_output=True)
        need(r.returncode==0,r.stderr)
        need(sha(q2/'MANIFEST.json')==corrected_manifest and {f.name:sha(f) for f in q2.iterdir()}=={f.name:sha(f) for f in p.iterdir()},'patch does not reproduce corrected bytes')
        receipt['patch_applies_and_reproduces_corrected_packet']=True
        for q in (p,q):
            q.chmod(0o755)
            for f in q.iterdir():f.chmod(0o644)
    receipt['independent_malformed_cases']=cases;receipt['independent_rejections']=rejected
    receipt['original_ledger_boolean_turn_accepted_in_three_modes']=True
    need(snapshot(PACKET)==before,'original packet modified')
    receipt['original_unchanged']=True;receipt['status']='PASS_WITH_DOCUMENTED_CORRECTIONS'
    (ROOT/'VALIDATION_RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
