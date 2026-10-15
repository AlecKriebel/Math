"""Run one guarded step of the repository kit; never replay an uncertain publication."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys
PRE=Path(__file__).resolve().parent
PUB=PRE.parent/'publication'
KIT=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
step=sys.argv[1]
assert step in {'stage','inspect-draft','publish','inspect-published'}
clear=json.loads((PRE/'FINAL_CLEARANCE.json').read_text())
assert clear['mathematical_verdict']=='PASS' and clear['fresh_clean_reviews']>=3
for name,p in clear['candidate_files'].items():
    data=(PRE/name).read_bytes();assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256']
assert clear['publication_cleared'] is True
args=[sys.executable,str(KIT)]
if step=='stage':args+=['stage',str(PRE/'deposit.json')]
elif step=='inspect-draft':args+=['inspect',str(PRE/'deposit.json')]
elif step=='publish':
    stage=json.loads((PUB/'zenodo-stage.stdout.json').read_text())
    inspect=json.loads((PUB/'zenodo-inspect-draft.stdout.json').read_text())
    assert stage['id']==inspect['id'] and inspect['state']=='ready_to_publish'
    assert not (PUB/'ZENODO_PUBLISH_ATTEMPT.json').exists(), 'Prior publication outcome needs read-only inspect'
    (PUB/'ZENODO_PUBLISH_ATTEMPT.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'id':stage['id'],'status':'publication about to be attempted; outcome not known'},indent=2)+'\n')
    args+=['publish',str(PRE/'deposit.json'),'--confirm-id',str(stage['id'])]
else:args+=['inspect',str(PRE/'deposit.json'),'--check-doi']
run=subprocess.run(args,capture_output=True,text=True)
(PUB/('zenodo-'+step+'.stdout.json')).write_text(run.stdout)
(PUB/('zenodo-'+step+'.stderr.txt')).write_text(run.stderr)
assert run.returncode==0, 'Kit failed; reconcile saved output before any uncertain action'
result=json.loads(run.stdout)
if step=='inspect-published':
    published=json.loads((PUB/'zenodo-publish.stdout.json').read_text())
    assert result['state']=='published' and result['id']==published['id'] and result['doi']==published['doi']
    expected=[]
    for f in json.loads((PRE/'deposit.json').read_text())['files']:
        p=PRE/f['path'];data=p.read_bytes();expected.append({'name':p.name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    assert result['files']==expected and published['files']==expected
    result.update(submitted=True,metadata_and_files_verified=True,
                  verification_method='Repository kit successful publication readback and separate inspect against exact frozen metadata and file checksums')
    (PUB/'ZENODO_VERIFIED_PUBLICATION.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,indent=2,ensure_ascii=False))
