"""Parent's read-only whole closed-review and new-control reproduction."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess

A=Path(__file__).resolve().parent;V=A/'preprint_review_01'
D=A/'root_replay_private/preprint_review01_closed_001'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
def inventory():
    result={}
    for p in sorted(V.rglob('*')):
        assert not p.is_symlink() and (p.is_file() or p.is_dir())
        row={'type':'file' if p.is_file() else 'directory','mode':stat.S_IMODE(p.stat().st_mode)}
        if p.is_file():
            b=p.read_bytes();row.update(bytes=len(b),sha256=sha(b))
        result[str(p.relative_to(V))]=row
    return result
assert not D.exists();D.mkdir(parents=True)
closed=load(V/'CLOSURE.json')
assert closed['status']=='CLOSED' and closed['closed'] is True
assert (V/'ROOT_APPROVAL.json').read_bytes()==(A/'ROOT_PREPRINT_REVIEW01_APPROVAL.json').read_bytes()
before=inventory()
(D/'whole_inventory_before.json').write_text(json.dumps(before,indent=2)+'\n')
captures=[]
def run(label,args):
    started=utc();r=subprocess.run(args,cwd=D,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (D/(label+'.'+name)).write_bytes(b)
    rec={'argv':args,'cwd':str(D),'started_utc':started,'finished_utc':utc(),'exit_code':r.returncode,
         'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),
         'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)}
    (D/(label+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    captures.append(rec);assert r.returncode==0 and not r.stderr,rec
    return r
public=load(V/'PUBLIC_MANIFEST.json')['files'];private=load(V/'PRIVATE_MANIFEST.json')['files']
assert len(public)==17
def expected(full):
    obj={'status':'PASS','closed_review':True,'public_payloads_checked':len(public),
         'private_payloads_checked':len(private) if full else 0,'private_payloads_declared':len(private),
         'private_scope':'full local custody checked' if full else 'not checked',
         'scope':'Byte/mode/inventory and native-stream custody; no proof evaluation, program execution, source download or publication action.'}
    return (json.dumps(obj,indent=2)+'\n').encode()
f=run('full',['python3','-B',str(V/'verify_review.py')]);assert f.stdout==expected(True)
p=run('public',['python3','-B',str(V/'verify_review.py'),'--public-only']);assert p.stdout==expected(False)
external=A/'root_replay_private/preprint_review01_external_closure_001'
assert f.stdout==(external/'verify_full/stdout.bin').read_bytes()
assert p.stdout==(external/'verify_public/stdout.bin').read_bytes()
assert (external/'verify_full/stderr.bin').read_bytes()==(external/'verify_public/stderr.bin').read_bytes()==b''
c=run('controls',['/opt/homebrew/bin/python3.11','-B',str(V/'fresh_controls.py')])
assert c.stdout==(V/'CONTROL_CHECKS.json').read_bytes()==(V/'native_runs/fresh_controls/stdout.bin').read_bytes()
assert c.stdout==(A/'root_replay_private/preprint_review01_preseal_controls_001/control.stdout').read_bytes()
assert before==inventory(),'Closed review namespace changed during root reproduction.'
files=[]
for name,pin in closed['current_submission_pins'].items():
    b=(A/'preprint'/name).read_bytes();assert {'bytes':len(b),'sha256':sha(b)}==pin
    files.append({'path':name,**pin})
approval=load(A/'ROOT_PREPRINT_REVIEW01_APPROVAL.json')
for name,pin in approval['approved_artifact_bindings'].items():
    assert {'bytes':len((V/name).read_bytes()),'sha256':sha((V/name).read_bytes())}==pin
seal_sha=sha((V/'CLOSURE.json').read_bytes())
result={'utc':utc(),'status':'PASS_ROOT_CLOSED_PREPRINT_REVIEW01','review_number':1,
        'mandatory_findings':0,'closed_namespace_unchanged':True,'whole_verifier_output_compared':True,
        'review_seal_path':'CLOSURE.json','review_seal_sha256':seal_sha,'sealed_utc':closed['utc'],
        'baseline_seal':load(V/'source_baseline/BASELINE_SEAL.json'),
        'whole_payload_files':sum(r['type']=='file' for r in before.values()),
        'whole_directories':sum(r['type']=='directory' for r in before.values()),
        'public_payload_count':len(public),'private_payload_count':len(private),
        'sealed_submission_files':files,'captures':captures,
        'fully_read_report_sha256':sha((V/'REPORT.md').read_bytes()),
        'all_mandatory_submission_findings_resolved':True,
        'scope':'Root fully read the analytical report/baseline/control/custody code; reproduced complete new controls and verified full/public closed inventory without writes. Second NEW review, native acceptance and publication remain pending.'}
(A/'ROOT_PREPRINT_REVIEW01_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
control={'utc':utc(),'entire_stdout_identical':True,'closed_review_namespace_unchanged':True,
         'control_source_sha256':sha((V/'fresh_controls.py').read_bytes()),'execution':captures[-1],
         'complete_stdout':json.loads(c.stdout),'review_seal_sha256':seal_sha}
(A/'ROOT_PREPRINT_REVIEW01_CONTROL_REPRODUCTION.json').write_text(json.dumps(control,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'captures','baseline_seal'}},indent=2))
