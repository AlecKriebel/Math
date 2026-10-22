"""Verify exact public/review artifact inventory, source pins, and finite controls."""
from hashlib import sha256,sha1
from pathlib import Path
from subprocess import run
import json
import sys

ROOT=Path(__file__).resolve().parent
EXCLUDED={'private','__pycache__'}
SEAL_FILES={'MANIFEST.json','MANIFEST.json.sha256'}


def artifacts():
    return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                  if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(ROOT).parts)
                  and p.relative_to(ROOT).as_posix() not in SEAL_FILES)


def checks():
    source=ROOT/'private'
    findings=[]
    private_inventory=ROOT/'PRIVATE_SOURCE_MANIFEST.json'
    if source.exists() and private_inventory.exists():
        items=json.loads(private_inventory.read_text())['files']
        actual=sorted(p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file())
        if actual!=sorted(x['path'] for x in items):
            raise ValueError('private source exact inventory mismatch')
        for item in items:
            data=(source/item['path']).read_bytes()
            if len(data)!=item['bytes'] or sha256(data).hexdigest()!=item['sha256']:
                raise ValueError('private source hash mismatch: '+item['path'])
    pins=json.loads((ROOT/'public/SOURCE_PINS.json').read_text())
    for row in pins['sources']:
        filename=row['local_private_name']; path=source/filename
        if path.exists():
            data=path.read_bytes()
            if len(data)!=row['bytes'] or sha256(data).hexdigest()!=row['sha256']:
                raise ValueError('source pin mismatch: '+filename)
            findings.append(filename)
    if (source/'winter_pinned.pdf').exists():
        data=(source/'winter_pinned.pdf').read_bytes()
        if data!=(source/'winter_current.pdf').read_bytes():
            raise ValueError('live versus pinned note mismatch')
        blob=sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!='592725cde9a0783de0f4a6216f241ab07db2518b':
            raise ValueError('Git blob identity mismatch')
        commit=json.loads((source/'winter_commit.json').read_text())
        file=next(x for x in commit['files'] if x['filename']=='pdf/publications/Stokers_conjecture.pdf')
        if file['sha']!=blob or file['status']!='added':
            raise ValueError('Git commit file evidence mismatch')
    if (source/'winter_pages_run.json').exists():
        r=json.loads((source/'winter_pages_run.json').read_text())
        if not (r['id']==33918657115 and r['head_sha']=='766c313bc2187a5eafd5757dca43ffefc6a9ced6'
                and r['created_at']=='2026-09-04T20:55:50Z' and r['conclusion']=='success'):
            raise ValueError('Actions run provenance mismatch')
        ds=json.loads((source/'winter_deployment_statuses.json').read_text())
        success=next(s for s in ds if s['id']==17842306951)
        if not (success['state']=='success' and success['created_at']=='2026-09-04T20:56:33Z'
                and success['environment_url']=='https://martinwintermath.github.io/'):
            raise ValueError('deployment success provenance mismatch')
    candidate=json.loads((ROOT/'ORIGINAL_PIN_CHECK.json').read_text())
    if not candidate['original_proof_pin_pass']:
        raise ValueError('candidate input pin failed')
    bridge=run([sys.executable,'-B',str(ROOT/'public/check_bridge.py')],capture_output=True,text=True,check=True)
    finite=json.loads(bridge.stdout)
    return {'status':'PASS','checked_stored_private_sources':findings,
            'candidate_input_pin':'PASS','exact_diagnostics':finite,
            'scope':'Artifact, provenance, and finite diagnostics. Does not formally verify the mathematical proof or establish exhaustive worldwide priority.'}


if __name__=='__main__':
    result=checks()
    if '--checks-only' not in sys.argv:
        mbytes=(ROOT/'MANIFEST.json').read_bytes()
        expected=(ROOT/'MANIFEST.json.sha256').read_text().split()[0]
        if sha256(mbytes).hexdigest()!=expected:
            raise ValueError('detached manifest hash mismatch')
        manifest=json.loads(mbytes)
        expected_files=sorted(x['path'] for x in manifest['files'])
        if artifacts()!=expected_files:
            raise ValueError('exact inventory mismatch')
        for x in manifest['files']:
            data=(ROOT/x['path']).read_bytes()
            if len(data)!=x['bytes'] or sha256(data).hexdigest()!=x['sha256']:
                raise ValueError('artifact hash mismatch: '+x['path'])
        result['manifest_exact_inventory']='PASS'
        result['manifest_files']=len(expected_files)
        result['detached_manifest_seal']='PASS'
    print(json.dumps(result,indent=2))
