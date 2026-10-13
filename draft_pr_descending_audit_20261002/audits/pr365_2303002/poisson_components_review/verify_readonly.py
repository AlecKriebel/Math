"""Validate a sealed review without writes, network, or candidate execution."""
from pathlib import Path
import gzip, hashlib, json, sys

ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
SNAPSHOT=AUDIT/'snapshot'
TARGET=SNAPSHOT/'unsolved_math_prioritization/attempts/2303002'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def identity(p,expected):
    b=p.read_bytes()
    assert len(b)==expected['bytes'] and sha(b)==expected['sha256'],str(p)
    return b

seal=load('FINAL_SEAL.json')
assert sha((ROOT/'PUBLIC_MANIFEST.json').read_bytes())==seal['public_manifest_sha256']
manifest=load('PUBLIC_MANIFEST.json')
assert manifest['excluded_closure_files']==['PUBLIC_MANIFEST.json','FINAL_SEAL.json']
public={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
        and 'private' not in p.relative_to(ROOT).parts
        and '__pycache__' not in p.relative_to(ROOT).parts
        and p.name not in ('PUBLIC_MANIFEST.json','FINAL_SEAL.json')}
assert public==set(manifest['files']),('public inventory mismatch',public^set(manifest['files']))
for path,f in manifest['files'].items():identity(ROOT/path,f)
private=load('receipts/private_inventory.json')
actual_private={str(p.relative_to(ROOT)) for p in (ROOT/'private').rglob('*') if p.is_file()}
assert actual_private==set(private['files'])
for path,f in private['files'].items():
    b=identity(ROOT/path,f)
    if path.endswith('.gz'):
        logical=gzip.decompress(b)
        assert len(logical)==f['logical_bytes'] and sha(logical)==f['logical_sha256']
for early in ['BASELINE_SEAL.json','ANALYTICAL_SEAL.json']:
    for path,f in load(early)['files'].items():identity(ROOT/path,f)
baseline=load('BASELINE_SEAL.json');analytical=load('ANALYTICAL_SEAL.json')
assert baseline['candidate_proof_or_code_or_history_read'] is False
assert analytical['candidate_programs_executed'] is False
assert baseline['sibling_or_root_analysis_read'] is False
assert analytical['sibling_or_root_analysis_read'] is False
assert baseline['sealed_utc']<analytical['sealed_utc']<seal['sealed_utc']
assert baseline['sealed_utc']<load('receipts/target_read.json')['completed_utc']<analytical['sealed_utc']
for r in load('receipts/primary_fetch.json'):
    assert r['completed_utc']<baseline['sealed_utc']
    for suffix,keys in [('.pdf.gz',('bytes','sha256','stored_pdf_gzip_bytes','stored_pdf_gzip_sha256')),
                        ('.txt.gz',('text_bytes','text_sha256','text_gzip_bytes','text_gzip_sha256'))]:
        b=(ROOT/'private'/(r['name']+suffix)).read_bytes();logical=gzip.decompress(b)
        assert len(b)==r[keys[2]] and sha(b)==r[keys[3]]
        assert len(logical)==r[keys[0]] and sha(logical)==r[keys[1]]
snapshot=json.loads((AUDIT/'snapshot_manifest.json').read_text())
assert snapshot['head']==seal['head'] and snapshot['base']==seal['base']
assert len(snapshot['files'])==19
for f in snapshot['files']:
    b=identity(SNAPSHOT/f['path'],f);assert blob(b)==f['git_blob_sha']
for name in ['FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json']:
    for f in json.loads((TARGET/name).read_text())['files']:identity(TARGET/f['path'],f)
for path,h in json.loads((TARGET/'final_review/REVIEW_MANIFEST.json').read_text()).items():
    assert sha((TARGET/'final_review'/path).read_bytes())==h
pub=json.loads((TARGET/'PUBLICATION_MANIFEST.json').read_text())
assert pub['author_manifest_sha256']==sha((TARGET/'FINAL_FROZEN_MANIFEST.json').read_bytes())
assert pub['review_manifest_sha256']==sha((TARGET/'final_review/REVIEW_MANIFEST.json').read_bytes())
commands=load('receipts/commands.json')
assert len(commands)==45
for r in commands+[load('receipts/driver.json')]:
    assert r['exit']==0 and r['started_utc']>analytical['sealed_utc']
    for name,s in r['streams'].items():
        b=(ROOT/s['path']).read_bytes();logical=gzip.decompress(b)
        assert len(b)==s['stored_bytes'] and sha(b)==s['stored_sha256']
        assert len(logical)==s['logical_bytes'] and sha(logical)==s['logical_sha256']
        if name=='stderr':assert logical==b''
by_name={r['name']:r for r in commands}
expected=(TARGET/'final_review/INDEPENDENT_CHECKS.json').read_bytes()
for name,b in [('author_controls',(TARGET/'SOURCE_CHECKS.json').read_bytes()),
               ('review_math_only',expected.replace(b'1667',b'1665')),
               ('review_sources',expected)]:
    r=by_name[name]
    assert r['whole_stdout_equals_expected'] is True
    assert gzip.decompress((ROOT/r['streams']['stdout']['path']).read_bytes())==b
scope=load('receipts/execution_scope.json')
assert scope['scope_files']==19 and scope['target_files']==18 and scope['branch']=='main'
assert scope['whole_receipt_matches']==3 and scope['candidate_snapshot_unchanged_after'] is True
assert scope['api_files_exact'] is True and scope['api_draft'] is True
assert len(scope['author_files_unchanged'])==10
assert scope['new_controls']['exact_assertions']==735
assert len(scope['new_controls']['rejected_false_claims'])==37
assert len(scope['queue_only_change'])==1 and scope['queue_only_change'][0]['line']==405
assert load('receipts/driver.json')['driver_sha256']==sha((ROOT/'replay_and_scope.py').read_bytes())
print(json.dumps({'status':'PASS','public_files':len(public),'private_files':len(actual_private),
                  'frozen_scope_files':19,'captured_commands':45,'whole_receipt_matches':3,
                  'new_exact_controls':735,'false_claims_rejected':37,
                  'new_theorems':0,'writes':0},indent=2,sort_keys=True))
