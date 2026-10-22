#!/usr/bin/env python3
"""Authenticate supplied immutable PR1262 records; no writes except explicit output."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    snapshot_bytes = (root/'SUBMITTED_SNAPSHOT.json').read_bytes()
    snapshot = json.loads(snapshot_bytes)
    require(snapshot['head'] == 'fb7b750865f3e220590f128661c487c5984bae75', 'wrong reviewed head')
    require(snapshot['body_sha256'] == '3ab8f23a031f563bb7b5367792af9b723b1d637ada5cc78d44c717197be51d3c', 'wrong original body pin')
    require(snapshot['pr'] == 1262 and snapshot['problem_id'] == 30001248, 'wrong identity')
    require(len(snapshot['files']) == 8, 'not exactly eight supplied files')
    rows = []
    for item in snapshot['files']:
        data = (root/item['local']).read_bytes()
        require(len(data) == item['bytes'] and digest(data) == item['sha256'], 'submitted bytes changed: '+item['local'])
        blob = subprocess.check_output(['git', 'cat-file', 'blob', snapshot['head']+':'+item['path']], cwd=root)
        require(blob == data, 'head blob differs: '+item['path'])
        git_sha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(git_sha == item['blob'], 'git blob identity differs')
        rows.append({'path':item['local'], 'bytes':len(data), 'sha256':digest(data), 'git_blob':git_sha})
    manifest_data = (root/'submitted/MANIFEST.json').read_bytes()
    manifest = json.loads(manifest_data)
    require(set(manifest['members']) == {Path(i['local']).name for i in snapshot['files']}, 'manifest member mismatch')
    require(len(manifest['entries']) == 7 and manifest['self_hash_excluded'] == 'MANIFEST.json', 'manifest self convention')
    for entry in manifest['entries']:
        data = (root/'submitted'/entry['file']).read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'inner manifest mismatch')
    live = json.loads((root/'_local/live_pr.json').read_bytes())
    require(live['headRefOid'] == snapshot['head'] and live['headRefName'] == snapshot['branch'], 'captured original branch/head differs')
    body_hash = digest(live['body'].encode())
    require(body_hash == snapshot['body_sha256'], 'captured original body differs')
    branch = subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=root,text=True).strip()
    require(branch == 'main', 'checkout is not main')
    output = {'at_utc':datetime.now(timezone.utc).isoformat(), 'status':'PASS', 'pr':1262,
      'problem_id':30001248,'reviewed_head':snapshot['head'],'original_body_sha256':body_hash,
      'submitted_snapshot_sha256':digest(snapshot_bytes),'manifest_sha256':digest(manifest_data),
      'scope':'Eight submitted files, seven inner-manifest hashes, captured original head/branch/body and local Git head blobs; no fresh live remote API claim.',
      'checkout_branch':branch, 'files':rows}
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'PASS','output':str(args.output),'files':len(rows)}))

if __name__ == '__main__':
    main()
