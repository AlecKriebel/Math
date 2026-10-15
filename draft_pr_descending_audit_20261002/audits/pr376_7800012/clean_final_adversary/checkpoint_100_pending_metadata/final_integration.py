"""Read-only exact repaired-head/queue/API/remote certification after PR377."""
import pathlib,json,hashlib,subprocess,datetime
R=pathlib.Path(__file__).parent;A=R.parent;REPO=pathlib.Path('/Users/alec/Documents/Math')
H='b19a834793c4b1acef3c6a48fa66299170df8560';B='28519ba7648c003d4e1212dd315005c93a21a9d6';O='9a92b6a0bd7cff3a8c11bf66ff9338264ab012d1';TREE='7de779381f5fced59e64a0f2ffc6c03c1a447830';WIP='d48fdb986d86b639219c0e50d426971fa1d8b8a6';MERGED='b3b1a74df434768ee221b17eea3be22b97b4ad3c'
T='unsolved_math_prioritization/attempts/7800012';Q='unsolved_math_prioritization/QUEUE.md'
def git(*v):return subprocess.check_output(['git','-C',str(REPO),*v])
def sha(b):return hashlib.sha256(b).hexdigest()
def anc(x,y):return subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',x,y],capture_output=True).returncode==0
mfpath=A/'repaired_snapshot_manifest.json';mf=json.loads(mfpath.read_text());original=json.loads((A/'snapshot_manifest.json').read_text());old={e['path']:e for e in original['files']}
assert mf['head']==H and mf['base']==B and mf['original_frozen_head']==O
assert git('rev-parse',H+'^{tree}').decode().strip()==TREE
parents=git('show','-s','--format=%P',H).decode().strip().split();assert parents==[O,B]
assert anc(O,H) and anc(B,H) and anc(WIP,H) and anc(MERGED,B)
assert git('rev-parse','refs/heads/main').decode().strip()==B
paths=git('diff','--name-only',B,H).decode().splitlines();assert len(paths)==51 and sorted(paths)==sorted(e['path'] for e in mf['files'])
assert sorted(paths)==sorted(old)
entries=[]
for e in mf['files']:
 p=e['path'];b=(A/'repaired_snapshot'/p).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 actual=git('show',H+':'+p);assert actual==b
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert git('rev-parse',H+':'+p).decode().strip()==blob
 same=(b==git('show',O+':'+p))
 if p!=Q:
  assert p.startswith(T+'/') and same and sha(b)==old[p]['sha256'] and len(b)==old[p]['bytes']
  assert b==(A/'snapshot'/p).read_bytes()
 entries.append(dict(path=p,bytes=len(b),sha256=sha(b),git_blob_sha=blob,original_target_byte_identical=same if p!=Q else None,status='PASS'))
assert sum(e['path'].startswith(T+'/') for e in entries)==50
# Literal byte reconstruction: exactly two cells on one physical line.
base=git('show',B+':'+Q);head=git('show',H+':'+Q);rows=base.splitlines(keepends=True);newrows=head.splitlines(keepends=True)
assert len(rows)==len(newrows)
changed=[i for i,(x,y) in enumerate(zip(rows,newrows)) if x!=y];assert changed==[414]
i=changed[0];cells=rows[i].split(b'|');newcells=newrows[i].split(b'|');assert len(cells)==len(newcells)
different=[j for j,(x,y) in enumerate(zip(cells,newcells)) if x!=y];assert different==[8,9]
assert cells[1].strip()==b'404' and b'7800012 / AMR-077-0012'==cells[2].strip()
assert cells[8:10]==[b' queued ',b' 0/5 '] and newcells[8:10]==[b' unsolved ',b' 5/5 ']
cells[8]=b' unsolved ';cells[9]=b' 5/5 ';expected=rows[:];expected[i]=b'|'.join(cells);assert b''.join(expected)==head
queue=dict(physical_line=415,rank=404,cells=[8,9],from_values=['queued','0/5'],to_values=['unsolved','5/5'],base_sha256=sha(base),head_sha256=sha(head),all_other_queue_bytes_identical=True)
# Nested manifests and frozen wrappers are historical target bytes, kept intact.
P=A/'repaired_snapshot'/T;nested=[]
for path in sorted(P.rglob('*MANIFEST.json')):
 obj=json.loads(path.read_text());n=0
 for e in obj.get('files',[]):
  b=(path.parent/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];n+=1
 nested.append(dict(path=str(path.relative_to(P)),entries=n,sha256=sha(path.read_bytes()),status='PASS'))
frozen=json.loads((P/'FINAL_FROZEN_MANIFEST.json').read_text());author=[e['path'] for e in frozen['files']]+['FINAL_FROZEN_MANIFEST.json']
assert len(author)==41
for p in author:assert (P/p).read_bytes()==git('show',WIP+':'+T+'/'+p)
assert sum(x['entries'] for x in nested)==210
# Live API and remote observations captured independently in complete streams.
pr=json.loads((R/'streams/final_live_pr376.stdout').read_text());prev=json.loads((R/'streams/final_live_pr377.stdout').read_text());commit=json.loads((R/'streams/final_live_commit.stdout').read_text())
assert pr['number']==376 and pr['headRefOid']==H and pr['baseRefOid']==B and pr['headRefName']=='dot/math-7800012' and pr['baseRefName']=='main'
assert pr['state']=='OPEN' and pr['isDraft'] is True and pr['mergeable']=='MERGEABLE' and pr['mergeStateStatus']=='CLEAN'
assert commit['sha']==H and commit['tree']['sha']==TREE and [p['sha'] for p in commit['parents']]==[O,B]
assert prev['number']==377 and prev['state']=='MERGED' and prev['mergeCommit']['oid']==MERGED and prev['mergedAt']=='2026-10-03T06:55:15Z'
remote=dict(line.split()[::-1] for line in (R/'streams/final_remote_refs.stdout').read_text().splitlines());assert remote=={'refs/heads/main':B,'refs/heads/dot/math-7800012':H}
body=pr['body']
for text in [H,O,B,'ordered parents:','41 frozen author-file bytes','not the refreshed head\'s second parent','physical line415/rank404','51 changed paths','50 unchanged target files','Source-free public replay reports0','separate source-bound replay verifies3','unrefereed','external human peer review','remains unresolved','None establishes unrestricted quarter-flux optimality or a bulk counterexample']:
 assert text in body,text
assert '**unsolved, 5/5**' in body
historical=['RESULT.md','READINESS.json','PRIOR_GATE.json','FINAL_REVIEW_REQUEST.md','FINAL_FROZEN_MANIFEST.json','PR_BODY.md']
assert all((P/f).read_bytes()==git('show',O+':'+T+'/'+f) for f in historical)
metadata=dict(live_pr_body_sha256=sha(body.encode()),parent_claim_corrected=True,frozen_in_repo_PR_BODY_remains_historical=True,live_body_observed_updated_at=pr['updatedAt'],live_body_pending_integration_statement='fresh reviewer is completing the exact refreshed-head integration gate' in body,status_update_after_this_gate='Replace pending integration phrase by completed gate before promotion; parent/base/path claims already verified.')
out=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_EXACT_REPAIRED_HEAD_QUEUE_ALL51',audit_completion_percent=100,head=H,base=B,tree=TREE,ordered_parents=parents,repaired_snapshot_manifest_sha256=sha(mfpath.read_bytes()),git_bindings=entries,target50_original_byte_identical=True,author_wip41_original_byte_identical=True,nested_manifest_entries=210,nested_manifests=nested,queue=queue,pr376_api=dict(url=pr['url'],state=pr['state'],draft=pr['isDraft'],mergeable=pr['mergeable'],merge_state=pr['mergeStateStatus']),pr377_predecessor=dict(merge=MERGED,merged_at=prev['mergedAt'],ancestor_of_base=True),remote_refs=remote,metadata=metadata,mathematical_verdict='PASS_SCOPED_ORIGINAL_UNSOLVED_5_OF_5',historical_scope='Earlier pending/readiness inventories are frozen historical statements, with bounded eligibility and no worldwide novelty/open-status certification.',no_candidate_git_index_or_service_writes=True)
(R/'FINAL_INTEGRATION_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status=out['status'],percent=100,head=H,base=B,tree=TREE,git51=True,target50_unchanged=True,nested210=True,queue_only_two_cells=True,api_remote_agree=True,predecessor_merged=True,live_parent_claim_corrected=True,pending_metadata_phrase=metadata['live_body_pending_integration_statement']),indent=2))
