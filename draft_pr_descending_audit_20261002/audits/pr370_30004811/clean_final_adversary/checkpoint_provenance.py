"""Read-only audit of immutable author bytes, snapshot blobs, and current refs."""
from pathlib import Path
import json, hashlib, subprocess, datetime, sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
SNAP=HERE.parent/'snapshot'
P=SNAP/'problems/30004811_capacity_volume_mass'
def sha(b): return hashlib.sha256(b).hexdigest()
checks=[]
for e in json.loads((HERE.parent/'snapshot_manifest.json').read_text())['files']:
    b=(SNAP/e['path']).read_bytes()
    checks.append({'path':e['path'],'bytes_match':len(b)==e['bytes'],
                   'sha256_match':sha(b)==e['sha256'],
                   'git_blob_match':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']})
assert all(all(v for k,v in e.items() if k!='path') for e in checks)
author=json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_text())
review=json.loads((P/'review/REVIEW_MANIFEST.json').read_text())
paths=[e['path'] for e in author['files']]+['FINAL_AUTHOR_MANIFEST.json']
paths+=['review/'+e['path'] for e in review['files']]+['review/REVIEW_MANIFEST.json']
parent_checks=[]
for i,rel in enumerate(paths):
    p=subprocess.run(['git','show','1901d52ea8b47b4dd3c843cb2e02be2c520da7cb:problems/30004811_capacity_volume_mass/'+rel],cwd=REPO,capture_output=True)
    (HERE/'private'/f'author_parent_{i}.stdout').write_bytes(p.stdout)
    (HERE/'private'/f'author_parent_{i}.stderr').write_bytes(p.stderr)
    parent_checks.append({'path':rel,'returncode':p.returncode,'unchanged_in_author_parent':p.returncode==0 and p.stdout==(P/rel).read_bytes(),
                          'expected_absent_in_author_parent':rel.startswith('review/') and p.returncode==128})
assert all(e['unchanged_in_author_parent'] for e in parent_checks[:10])
assert all(e['expected_absent_in_author_parent'] for e in parent_checks[10:])
commands=[('main_local',['git','rev-parse','HEAD']),
          ('remote_refs',['git','ls-remote','origin','refs/heads/main','refs/heads/math/30004811-capacity-volume-wip']),
          ('current_main_queue',['git','show','HEAD:unsolved_math_prioritization/QUEUE.md'])]
receipts=[]
for name,argv in commands:
    p=subprocess.run(argv,cwd=REPO,capture_output=True)
    (HERE/'private'/f'{name}.stdout').write_bytes(p.stdout)
    (HERE/'private'/f'{name}.stderr').write_bytes(p.stderr)
    receipts.append({'name':name,'argv':argv,'returncode':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),
                     'small_output':p.stdout.decode() if name!='current_main_queue' else [line for line in p.stdout.decode().splitlines() if '30004811' in line]})
result={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'snapshot_manifest_checks':checks,'author_parent_checks':parent_checks,'read_only_receipts':receipts,
        'own_checkpoint_commit':'PENDING_ROOT_CHECKPOINT',
        'review_historical_git_anchor':'Four review files are not in the author parent; they are bound in the frozen head and review/publication manifests. No earlier Git anchor is claimed.',
        'exact_live_approval':'PENDING_ROOT_REFRESH_AND_ADDITIVE_FINAL_LIVE'}
(HERE/'CHECKPOINT_PROVENANCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'snapshot_manifest_entries':len(checks),'immutable_author_files':10,'review_files_bound_at_frozen_head':4,'receipts':receipts},indent=2))
