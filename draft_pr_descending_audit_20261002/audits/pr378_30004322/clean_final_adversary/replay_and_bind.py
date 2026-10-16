from pathlib import Path
import hashlib,json,subprocess,sys,datetime

D=Path(__file__).resolve().parent
A=D/'private_replay/author'
S=D.parent/'snapshot'
streams=D/'streams'

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':[],'bindings':{}}

for i in range(1,6):
    p=subprocess.run([sys.executable,str(A/f'check_turn_{i}.py')],cwd=A,capture_output=True)
    (streams/f'author_turn_{i}.stdout.txt').write_bytes(p.stdout)
    (streams/f'author_turn_{i}.stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0 and not p.stderr
    assert p.stdout==(A/f'TURN_{i}_CHECKS.json').read_bytes()
    out['runs'].append({'name':f'author_turn_{i}','returncode':p.returncode,'stdout_sha256':sha(p.stdout),'assertions':json.loads(p.stdout)['assertions'],'receipt_byte_exact':True})
out['author_assertions']=sum(r['assertions'] for r in out['runs'])
assert out['author_assertions']==214070

for name,script,args,expected in [
    ('old_independent',A/'review/independent_checks.py',[],A/'review/INDEPENDENT_CHECKS.json'),
    ('author_wrapper',A/'REPLAY_ALL.py',[],None),
    ('review_wrapper',A/'review/verify_review.py',['--author-dir',str(A)],None),
    ('extension_fermat',D/'private_replay/extension/exact_fermat_check.py',[],D.parent/'cover_duality_review/exact_fermat_check.stdout.txt'),
    ('extension_subfamily',D/'private_replay/extension/exact_subfamily_check.py',[],D.parent/'cover_duality_review/exact_subfamily_check.stdout.txt')]:
    p=subprocess.run([sys.executable,str(script),*args],cwd=A,capture_output=True)
    (streams/f'{name}.stdout.txt').write_bytes(p.stdout)
    (streams/f'{name}.stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0 and not p.stderr,name
    if expected is not None:assert p.stdout==expected.read_bytes(),name
    summary={'name':name,'returncode':0,'stdout_sha256':sha(p.stdout),'receipt_byte_exact':expected is not None}
    if name=='old_independent':
        summary['assertions']=json.loads(p.stdout)['assertions'];assert summary['assertions']==93918
    if name.endswith('wrapper'):
        summary['result']=json.loads(p.stdout);assert summary['result']['source_files_checked']==0
    out['runs'].append(summary)

counts={}
for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json']:
    m=json.loads((A/name).read_text())
    for e in m['files']:
        b=(A/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
    counts[name]=len(m['files'])
    if 'previous_manifest_sha256' in m:
        prev=f'TURN_{int(name.split("_")[1])-1}_MANIFEST.json'
        assert sha((A/prev).read_bytes())==m['previous_manifest_sha256']
assert sum(counts.values())==62
out['bindings']['author_manifest_entries']=counts

hist=[]
for i in range(1,5):
    m=json.loads((A/f'TURN_{i}_REMOTE_RECEIPT.json').read_text())
    for e in m['files']:
        b=(A/e['path']).read_bytes();assert len(b)==e['size'] and blob(b)==e['sha']
    hist.append({'turn':i,'head':m['head'],'entries':len(m['files']),'all_blob_bindings_match_snapshot':True})
out['bindings']['historical_receipts']=hist

m=json.loads((A/'review/REMOTE_BINDING.json').read_text())
for e in m['files']:
    b=(A/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert blob(b)==e['expected_git_blob']==e['remote_git_blob']
out['bindings']['old_remote_blob_entries']=len(m['files'])
m=json.loads((A/'review/REVIEW_MANIFEST.json').read_text())
for e in m['files']:
    b=(A/'review'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
out['bindings']['old_review_entries']=len(m['files'])

m=json.loads((D.parent/'snapshot_manifest.json').read_text())
for e in m['files']:
    b=(S/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
out['bindings']['snapshot_entries']=len(m['files'])
out['bindings']['snapshot_math_entries']=sum(e['path'].startswith('problems/') for e in m['files'])
out['bindings']['original_head']=m['head']

m=json.loads((D.parent/'cover_duality_review/FINAL_AUDIT_MANIFEST.json').read_text())
for e in m['files']:
    b=(D.parent/'cover_duality_review'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
assert sha((D.parent/'snapshot_manifest.json').read_bytes())==m['snapshot_manifest_sha256']
assert sha((D.parent/'cover_duality_review/independence_seal.json').read_bytes())==m['independence_seal_sha256']
out['bindings']['extension_manifest_entries']=len(m['files'])
out['qualification']='Fresh wrapper replay explicitly omitted raw source bindings: sources directory absent, source_files_checked=0. Historical AUTHOR_REPLAY.json source_files_checked=6 is a different source-populated run. Mathematical/history bytes match, but remote claims are checked against frozen receipts here; final repaired tree and actual-main queue check remain separate.'
print(json.dumps(out,sort_keys=True,indent=2))
