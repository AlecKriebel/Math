from pathlib import Path
import subprocess,json,hashlib,datetime
D=Path(__file__).resolve().parent
A=D.parent/'snapshot/problems/30004322_arrangement_seshadri'
repo=Path('/Users/alec/Documents/Math')
prefix='problems/30004322_arrangement_seshadri/'
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
heads=[]
for i in range(1,5):
    m=json.loads((A/f'TURN_{i}_REMOTE_RECEIPT.json').read_text())
    for e in m['files']:
        b=git('show',m['head']+':'+prefix+e['path'])
        assert b==(A/e['path']).read_bytes()
        assert blob(b)==e['sha'] and len(b)==e['size']
    heads.append({'head':m['head'],'files':len(m['files']),'local_git_bytes_match_frozen_receipts':True})
m=json.loads((A/'review/REMOTE_BINDING.json').read_text())
for e in m['files']:
    b=git('show',m['commit']+':'+prefix+e['path'])
    assert b==(A/e['path']).read_bytes() and blob(b)==e['expected_git_blob']==e['remote_git_blob']
heads.append({'head':m['commit'],'files':len(m['files']),'local_git_bytes_match_frozen_receipts':True})
m=json.loads((D.parent/'snapshot_manifest.json').read_text())
for e in m['files']:
    b=git('show',m['head']+':'+e['path'])
    assert b==(D.parent/'snapshot'/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
heads.append({'head':m['head'],'files':len(m['files']),'local_git_bytes_match_snapshot':True})
allheads=[e['head'] for e in heads]
for before,after in zip(allheads,allheads[1:]):
    assert subprocess.run(['git','merge-base','--is-ancestor',before,after],cwd=repo).returncode==0
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_existing_git_objects':heads,'ordered_ancestry':allheads,'all_ancestry_checks_pass':True,'mutation':'none; only show and merge-base --is-ancestor','qualification':'These are independent reads of existing local Git objects, not fresh network raw-blob fetches. Frozen receipts include historical remote claims; final repaired head/queue comparison remains pending.'}
print(json.dumps(result,sort_keys=True,indent=2))
