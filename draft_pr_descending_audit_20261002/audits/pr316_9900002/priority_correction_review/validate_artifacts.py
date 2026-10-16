from pathlib import Path
from hashlib import sha256, sha1
from fractions import Fraction as F
import json, subprocess
root=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr316_9900002')
owned=root/'priority_correction_review'
packet=root/'priority_correction_packet'
author=root/'snapshot/unsolved_math_prioritization/attempts/9900002'
checks=[]
def ck(cond,label):
    if not cond: raise AssertionError(label)
    checks.append(label)
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha256(b).hexdigest(),'git_blob_sha1':sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
prep=json.loads((root/'PRIORITY_CORRECTION_PREPARATION.json').read_text())
snap=json.loads((root/'snapshot_manifest.json').read_text())
pub=json.loads((packet/'PUBLICATION_MANIFEST.json').read_text())
oldpub=json.loads((author/'PUBLICATION_MANIFEST.json').read_text())
pins={}
for name,expected in prep['prepared_files'].items():
    actual=pin(packet/name);pins[name]=actual
    ck(actual==expected,'prepared '+name)
ck(set(pins)=={p.name for p in packet.iterdir() if p.is_file()},'exactly six prepared files')
orig_entries={e['path'].split('attempts/9900002/',1)[1]:e for e in snap['files'] if 'attempts/9900002/' in e['path']}
ck(len(orig_entries)==18,'snapshot has original eighteen files')
ck(set(orig_entries)=={str(p.relative_to(author)) for p in author.rglob('*') if p.is_file()},'original scope exact')
for name,e in orig_entries.items():
    a=pin(author/name)
    ck(a['bytes']==e['bytes'] and a['sha256']==e['sha256'] and a['git_blob_sha1']==e['git_blob_sha'],'snapshot '+name)
for name,e in oldpub['files'].items(): ck(pin(author/name)==e,'original publication pin '+name)
wrappers=set(pub['current_wrappers'])
preserved=set(orig_entries)-wrappers
ck(wrappers=={'README.md','CURRENT_STATUS.json','PUBLICATION_MANIFEST.json'},'only three old wrappers replaced')
ck(len(preserved)==15,'fifteen historical files')
for name in preserved: ck(pub['files'][name]==pin(author/name),'preserved '+name)
for name in wrappers: ck(pub['original_current_wrapper_pins'][name]==pin(author/name),'old wrapper pin '+name)
expected=set(orig_entries)-{'PUBLICATION_MANIFEST.json'}|{'CURRENT_PRIORITY_NOTE.md'}
ck(set(pub['files'])==expected,'publication exact combined nineteen-file target scope minus self')
for name in ['CURRENT_STATUS.json','README.md','CURRENT_PRIORITY_NOTE.md']: ck(pub['files'][name]==pin(packet/name),'new wrapper/addition '+name)
ck(pub['historical_author_review_files_preserved']==15,'preserved count metadata')
ck(pub['substantive_author_turns']==1,'publication turn count')
for name in ['CURRENT_STATUS.json','TURN_STATE.json','TURN_1_MANIFEST.json']:
    data=json.loads((author/name).read_text());ck(data['substantive_author_turns']==1,'original turn count '+name)
status=json.loads((packet/'CURRENT_STATUS.json').read_text())
ck(status['substantive_author_turns']==1 and status['turn_limit']==5,'current author one of five')
ck(status['author_manifest_sha256']==pin(author/'TURN_1_MANIFEST.json')['sha256'],'author manifest reference')
# Hash the old inherited review manifest, without opening its contents/conclusions.
ck(status['review_manifest_sha256']==pin(author/'review/REVIEW_MANIFEST.json')['sha256'],'inherited manifest reference')
ck(status['status']=='already_solved' and status['mathematical_acceptance'] and not status['new_resolution_claim'],'current outcome scope')
ck(status['paper']==False and status['zenodo_upload']==False and status['doi'] is None and status['tracker_row']==False,'publication exclusions')
# Replay only the permitted author checker. No inherited review code is read/run.
r=subprocess.run(['/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',str(author/'verify_turn1.py')],cwd=owned,capture_output=True)
(owned/'executions/author_checker.stdout').write_bytes(r.stdout)
(owned/'executions/author_checker.stderr').write_bytes(r.stderr)
ck(r.returncode==0,'author checker actual exit zero')
ck(r.stdout==(author/'TURN_1_CHECKS.json').read_bytes(),'author checker output byte-identical')
result={'status':'PASS','artifact_assertions':len(checks),'prepared_pins':pins,'original_scope':18,'preserved_historical_scope':15,'author_replay_exit_code':r.returncode,'author_output':json.loads(r.stdout),'inherited_review_scope':'six files authenticated by hashes only; no content/conclusions read or code executed','criteria_sha256':pin(owned/'INDEPENDENT_SOURCE_CRITERIA.md')['sha256']}
(owned/'executions/artifact_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
# Independent exact finite endpoint controls, distinct from the author checker.
assertions=0;cases=0
laws=[{1:F(1,3),2:F(2,3)},{1:F(1,5),3:F(2,5),7:F(2,5)},{2:F(1,4),4:F(1,4),9:F(1,2)}]
for law in laws:
    for ti in range(0,25):
        t=F(ti,2);u=[F(0)]*(int(t)+1);u[0]=F(1)
        for s in range(1,int(t)+1):u[s]=sum((p*u[s-x] for x,p in law.items() if x<=s),F(0))
        U=sum(u)
        total=sum((u[s]*p for s in range(len(u)) for x,p in law.items() if s+x>t),F(0))
        assert total==1;assertions+=1
        for xi in range(ti,ti+25):
            x=F(xi,2)
            direct=sum((u[s]*p for s in range(len(u)) for length,p in law.items() if s+length>t and length>x),F(0))
            survival=sum((p for length,p in law.items() if length>x),F(0))
            assert direct==U*survival;assertions+=1;cases+=1
for n in range(1,10):
    p=F(1,2**(2**n))
    partial=sum((p**(2**j) for j in range(5)),F(0))
    qnext=sum((p**(2**j) for j in range(1,5)),F(0))
    assert qnext/partial<=p/(1-p);assertions+=1
output={'status':'PASS','exact_assertions':assertions,'straddling_identity_cases':cases,'inspection_times':'integer and half-integer, including zero','boundary':'x=t included; atomic laws; strict-after convention','scope':'finite controls only; analytic proof separately checked'}
(owned/'executions/independent_endpoint_controls.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
