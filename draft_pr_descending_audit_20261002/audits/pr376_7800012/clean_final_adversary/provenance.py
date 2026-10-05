"""Read-only Git/object/source/manifests audit; no Git writes or external mutations."""
import pathlib,json,hashlib,subprocess,datetime
ROOT=pathlib.Path(__file__).parent;REPO=pathlib.Path('/Users/alec/Documents/Math');SNAP=ROOT.parent/'snapshot'
HEAD='9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1';BASE='efd29c05204703acca9a0860812f54b94fae54b1';WIP='d48fdb986d86b639219c0e50d426971fa1d8b8a6'
T='unsolved_math_prioritization/attempts/7800012';P=SNAP/T
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
manifest=json.loads((ROOT.parent/'snapshot_manifest.json').read_text());bindings=[]
changed=git('diff','--name-only',BASE,HEAD).decode().splitlines()
assert sorted(changed)==sorted(v['path'] for v in manifest['files'])
for e in manifest['files']:
 b=(SNAP/e['path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();actual=git('rev-parse',HEAD+':'+e['path']).decode().strip()
 assert len(b)==e['bytes'] and sha(b)==e['sha256'] and blob==actual==e['git_blob_sha']
 assert git('cat-file','blob',actual)==b
 bindings.append(dict(path=e['path'],bytes=len(b),sha256=sha(b),git_blob_sha=blob,status='PASS'))
assert len(bindings)==51 and sum(b['path'].startswith(T+'/') for b in bindings)==50
nested=[]
for f in sorted(P.rglob('*MANIFEST.json')):
 j=json.loads(f.read_text());items=[]
 for e in j.get('files',[]):
  b=(f.parent/e['path']).read_bytes();assert sha(b)==e['sha256'] and len(b)==e['bytes']
  items.append(e['path'])
 nested.append(dict(path=str(f.relative_to(P)),sha256=sha(f.read_bytes()),entries=len(items),status='PASS'))
pub=json.loads((P/'PUBLICATION_MANIFEST.json').read_text());review=json.loads((P/'final_review/REVIEW_MANIFEST.json').read_text());frozen=json.loads((P/'FINAL_FROZEN_MANIFEST.json').read_text())
assert pub['author_manifest_sha256']==sha((P/'FINAL_FROZEN_MANIFEST.json').read_bytes())==review['author_manifest_sha256']
assert pub['review_manifest_sha256']==sha((P/'final_review/REVIEW_MANIFEST.json').read_bytes())
assert review['author_wip']==WIP
author=[e['path'] for e in frozen['files']]+['FINAL_FROZEN_MANIFEST.json']
for path in author:assert git('show',WIP+':'+T+'/'+path)==(P/path).read_bytes()
chain=['371e6cbea692ad8f75278ac6009955ce44a52639','023516f441e4b396f095565c9bf00ae6c1ec1093','58f5e25631be7af0c2e258d13959e667a6ac598c','21a88a3c2735b12c2da367752e4d65eaa1b19628',WIP]
hist=[]
for turn,commit in enumerate(chain,1):
 ledger=(P/f'TURN_{turn}_LEDGER.jsonl').read_text().splitlines();previous=(P/f'TURN_{turn-1}_LEDGER.jsonl').read_text().splitlines() if turn>1 else []
 assert len(ledger)==turn+1 and ledger[:len(previous)]==previous
 events=[json.loads(x) for x in ledger];state=json.loads((P/f'TURN_{turn}_STATE.json').read_text())
 assert events[-1]==state and state['turns_used']==turn and state['event']=='proof_attempt_turn'
 assert state['status']==('exhausted' if turn==5 else 'in_progress')
 mf=json.loads((P/f'TURN_{turn}_MANIFEST.json').read_text())
 for e in mf['files']:assert git('show',commit+':'+T+'/'+e['path'])==(P/e['path']).read_bytes()
 assert git('show',commit+':'+T+f'/TURN_{turn}_MANIFEST.json')==(P/f'TURN_{turn}_MANIFEST.json').read_bytes()
 hist.append(dict(turn=turn,commit=commit,ledger_events=len(events),state_time=state['at'],status=state['status'],files=len(mf['files']),note=state['note'],binding='PASS'))
assert subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',BASE,HEAD]).returncode==0
assert subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',WIP,HEAD]).returncode==0
parents=git('show','-s','--format=%P',HEAD).decode().strip().split();assert parents==[BASE,WIP]
source_bindings=[]
for e in json.loads((P/'SOURCE_MANIFEST.json').read_text())['primary_sources']:
 b=(ROOT/'tmp/private_sources/source_names'/e['file']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 source_bindings.append(dict(file=e['file'],url=e['url'],bytes=len(b),sha256=sha(b),status='PASS_FRESH_DOWNLOAD'))
# Verify complete queue table equivalence except this target's two intended cells.
queue='unsolved_math_prioritization/QUEUE.md';before=git('show',BASE+':'+queue).decode().splitlines();after=(SNAP/queue).read_text().splitlines();assert len(before)==len(after)
diff=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b];assert len(diff)==1
row=diff[0];a=before[row].split('|');b=after[row].split('|');assert len(a)==len(b)
cells=[i for i,(aa,bb) in enumerate(zip(a,b)) if aa!=bb];assert cells==[8,9]
assert a[8:10]==[' queued ',' 0/5 '] and b[8:10]==[' unsolved ',' 5/5 ']
out=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_ORIGINAL_HEAD_BINDINGS_QUEUE_PENDING_REPAIRED_HEAD',head=HEAD,base=BASE,wip=WIP,parents=parents,all51_git_bindings=bindings,target50=True,nested_manifests=nested,frozen_author_files=len(author),frozen_author_wip_bytes_unchanged=True,history=hist,sources=source_bindings,original_queue=dict(changed_lines=1,changed_cells=cells,row_1based=row+1,all_other_rows_preserved=True),prior_gate_limit='Historical416/411 inventory assertions preserved but not independently recertified as present-day exhaustive novelty evidence.')
(ROOT/'PROVENANCE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status=out['status'],git_bindings=len(bindings),target_files=50,nested_manifest_entries=sum(e['entries'] for e in nested),frozen_author_files=len(author),fresh_sources=len(source_bindings),turn_history_bindings=5,original_queue_two_cells_only=True),indent=2))
