"""Reconcile only the delayed GitHub readback after the one successful push."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,gzip,stat,subprocess,sys
D=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');A=D.parent;P=A.parent.parent
sys.path.insert(0,str(D/'publication_preparation'));import submission_gate as g
HEAD='cc083024dbd00de06ad444cd4070f51f60d209eb';BASE='3311d193e8c124bb97884fbe41710a957d3122c8';MERGED='b3eaf7561c83b37881eec11f5972396dbad9575d';PREFIX='problems/5100034_focal_pedal_equality';QUEUE='unsolved_math_prioritization/QUEUE.md'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
operator=D/'native_integration_preparation/integrate_pr305.py';assert g.pin(operator)==dict(bytes=18292,sha256='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897',mode='0644')
attempt=D/'native_integration_actual';outerp=D/'root_runs_private/root_pr305_native_integration_actual001/execution.json';outer=load(outerp)
assert outer['exit_code']==1 and outer['stdout_bytes']==0
for k in ['stdout','stderr']:
 b=(outerp.parent/(k+'.bin')).read_bytes();assert len(b)==outer[k+'_bytes'] and sha(b)==outer[k+'_sha256']
assert b'GitHub exact merge readback missing' in (outerp.parent/'stderr.bin').read_bytes()
assert outer['programs'][0]['sha256']==g.pin(operator)['sha256'] and outer['cwd']==str(D)
native=[];streams={};indices=[];flags=[];dirtyreads=[];diffreads=[]
files=sorted(attempt.glob('*_execution.json'),key=lambda p:int(p.name.split('_')[0]));assert len(files)==377
for f in files:
 n=f.name.split('_')[0];j=load(f);request=load(attempt/(n+'_request.json'));started=load(attempt/(n+'_started.json'))
 assert all(j[k]==v for k,v in request.items()) and all(j[k]==v for k,v in started.items())
 assert j['operator']==g.pin(operator) and j['cwd']==str(R) and 0<j['actual_PID']<100000000 and j['cooperative_process_group']==j['actual_PID']
 assert j['full_stream_capture_complete'] and j['parent_reaped'] and datetime.fromisoformat(j['end_UTC'])>=datetime.fromisoformat(j['start_UTC'])
 assert j['exit_code']==0 or j['exit_code']==1 and j['argv']==['/usr/bin/git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD]
 data={}
 for k in ['stdout','stderr']:
  e=j[k];stored=Path(e['path']).read_bytes();raw=gzip.decompress(stored)
  assert len(stored)==e['stored_bytes'] and sha(stored)==e['stored_sha256'] and len(raw)==e['logical_bytes'] and sha(raw)==e['logical_sha256'];data[k]=raw
 a=j['argv']
 if a==['/usr/bin/git','--no-optional-locks','ls-files','--stage','-z']:indices.append(data['stdout'])
 if a==['/usr/bin/git','--no-optional-locks','ls-files','-v','-z']:flags.append(data['stdout'])
 if a==['/usr/bin/git','--no-optional-locks','diff','--name-only','-z','HEAD']:dirtyreads.append(data['stdout'])
 if a[:6]==['/usr/bin/git','--no-optional-locks','diff','--binary','HEAD','--']:diffreads.append(data['stdout'])
 native.append(dict(path=str(f),pin=g.pin(f),actual_PID=j['actual_PID'],exit_code=j['exit_code'],argv=a));streams[n]=(j,data)
assert len({x['actual_PID'] for x in native})==377 and [int(f.name.split('_')[0]) for f in files]==list(range(1,378))
pushes=[(j,data) for j,data in streams.values() if j['argv'][:3]==['/usr/bin/git','--no-optional-locks','push']];assert len(pushes)==1
push,_=pushes[0];assert push['actual_PID']==62553 and push['exit_code']==0 and push['argv']==['/usr/bin/git','--no-optional-locks','push','--force-with-lease=refs/heads/main:'+BASE,'https://github.com/AlecKriebel/Math.git',MERGED+':refs/heads/main']
last,data=streams['377'];oldpr=json.loads(data['stdout']);assert last['argv']==['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/305'] and not oldpr['merged'] and oldpr['head']['sha']==HEAD
statusp=P/'SHARED_GIT_WINDOW_STATUS.json';status=g.pin(statusp);assert status['sha256']=='d3eb30fa9a2052426cc3ca266320f76b683a055b974d41c8f3ef1eb577ca0afe'
readback=D/'actual_merge_reconciliation_readonly_01';assert not readback.exists();readback.mkdir();ops=[]
def run(argv):
 start=datetime.now(timezone.utc).isoformat();p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=p.communicate(timeout=30);n=str(len(ops)+1)
 for k,b in [('stdout',out),('stderr',err)]:
  q=readback/(n+'_'+k+'.gz');q.write_bytes(gzip.compress(b,6,mtime=0));assert gzip.decompress(q.read_bytes())==b
 j=dict(argv=argv,cwd=str(R),actual_PID=p.pid,start_UTC=start,end_UTC=datetime.now(timezone.utc).isoformat(),exit_code=p.returncode,stdout_bytes=len(out),stdout_sha256=sha(out),stderr_bytes=len(err),stderr_sha256=sha(err),readonly=True)
 (readback/(n+'_execution.json')).write_text(json.dumps(j,indent=2)+'\n');ops.append(j);assert p.returncode==0 and not err,argv;return out
git=lambda *args:run(['/usr/bin/git','--no-optional-locks',*args]);names=lambda b:{x.decode() for x in b.split(b'\0') if x}
assert git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==MERGED
fetch,push_endpoint=g.safe_endpoints();assert fetch==push_endpoint=='https://github.com/AlecKriebel/Math.git'
assert git('ls-remote',fetch,'refs/heads/main').split()[0].decode()==MERGED
assert git('show','-s','--format=%P',MERGED).decode().split()==[BASE,HEAD];git('merge-base','--is-ancestor',BASE,MERGED)
fresh=json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/305']))
assert fresh['merged'] and fresh['merged_at'] and fresh['state']=='closed' and fresh['head']['sha']==HEAD and fresh['merge_commit_sha']==MERGED
assert fresh['body']==(attempt/'PR_BODY.md').read_text()
manifest=load(A/'snapshot_manifest.json');assert manifest['head']==HEAD and manifest['original_submitted_status']=='claimed_solved' and manifest['original_author_turn_count']=='1/5'
owned={e['path'] for e in manifest['files']}|{PREFIX+'/CURRENT_ACCEPTANCE.md'}|{PREFIX+'/publication/'+n for n in ['focal-pedal-ratios-note.pdf','focal-pedal-ratios-verification.zip','zenodo-deposit.json']}
assert len(owned)==34 and names(git('diff','--name-only','-z',BASE,MERGED))==owned
body=(attempt/'PR_BODY.md').read_text();expected={e['path']:(A/'snapshot'/e['path']).read_bytes() for e in manifest['files'] if e['path']!=QUEUE}
expected[PREFIX+'/CURRENT_ACCEPTANCE.md']=body.split('\nThe exact original PRhead ')[0].replace('(https://github.com/AlecKriebel/Math/blob/main/'+PREFIX+'/publication/','(publication/').encode()
for n in ['focal-pedal-ratios-note.pdf','focal-pedal-ratios-verification.zip','zenodo-deposit.json']:expected[PREFIX+'/publication/'+n]=(g.O/n).read_bytes()
qbefore=git('show',BASE+':'+QUEUE);qafter=git('show',MERGED+':'+QUEUE)
row=lambda b:next(x for x in b.splitlines(keepends=True) if b'| 5100034 /' in x)
qb=row(qbefore);qa=row(qafter);assert qafter.replace(qa,b'',1)==qbefore.replace(qb,b'',1)
assert [i for i,(x,y) in enumerate(zip(qb.split(b'|'),qa.split(b'|'))) if x!=y]==[8,9,11,12]
assert qa.split(b'|')[8].strip()==b'claimed_solved' and qa.split(b'|')[9].strip()==b'1/5' and qa.split(b'|')[12].strip()==b'https://doi.org/10.5281/zenodo.23149775'
expected[QUEUE]=qafter
for rel,b in expected.items():
 assert git('show',MERGED+':'+rel)==b and (R/rel).read_bytes()==b and stat.S_IMODE((R/rel).stat().st_mode)==0o644,rel
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert git('ls-tree',MERGED,'--',rel).decode().split()[:3]==['100644','blob',blob]
exclude=lambda b:b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in owned)
assert exclude(git('ls-files','--stage','-z'))==exclude(indices[0]) and exclude(git('ls-files','-v','-z'))==exclude(flags[0])
dirty=names(git('diff','--name-only','-z','HEAD'));assert dirty==names(dirtyreads[0])
assert git('diff','--binary','HEAD','--',*sorted(dirty))==diffreads[0]
held=load(D/'peer_pr80_final_completion_window/KNOWN_HELD_INVENTORY.json')
for e in held['files']:
 if e['path']==str(statusp.relative_to(R)):continue
 p=R/e['path'];now=g.pin(p);assert now['bytes']==e['bytes'] and now['sha256']==e['sha256'] and int(now['mode'],8)==e['mode']
assert g.pin(statusp)==status and not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists()
g.current_clearance();g.operational_clearance();pub=load(g.OUT/'inspect_published_receipt.json');tracker=load(g.OUT/'TRACKER_COMPLETE.json')
assert load(D/'ROOT_ACTUAL_PUBLICATION_TRACKER_FINAL_CUSTODY.json')['DOI']==pub['doi']==tracker['doi']=='10.5281/zenodo.23149775'
assert git('rev-parse','HEAD').decode().strip()==MERGED and git('ls-remote',fetch,'refs/heads/main').split()[0].decode()==MERGED
receipt=dict(UTC=datetime.now(timezone.utc).isoformat(),status='PASS_PR305_EXACT_ORIGINAL_HEAD_MERGED_PUBLISHED_TRACKER_VERIFIED',PR=305,original_head=HEAD,actual_merge=MERGED,parents=[BASE,HEAD],merged_at=fresh['merged_at'],owned_paths=sorted(owned),original29_bodies_modes_blobs_preserved=True,original_author_history='1/5',queue_only_cells=[8,9,11,12],foreign_queue_bytes_preserved=True,whole_foreign_logical_index_flags_dirty_bodies_modes_preserved=True,main_branch_retained=True,index_empty=True,DOI=pub['doi'],record_url=pub['record_url'],tracker_range=tracker['updatedRange'],mathematics_percent=100,bounded_priority_percent=100,PR_workflow_percent=100,no_external_human_review=True,extensive_AI_use=True,historical_firstness_certified=False,global_descending_inventory_checkpoint_pending=True,root_actual_capture_directory=str(attempt),reconciliation=dict(original_outer_exit_code=1,original_outer_capture=g.pin(outerp),sole_successful_push_PID=62553,sole_commit_PID=62318,fresh_GitHub_exact_merge_confirmed=True,no_merge_commit_stage_push_or_PR_mutation_repeated=True,original377_full_actual_captures_authenticated=native,fresh_readonly_operations=ops,source=g.pin(Path(__file__).resolve())))
out=D/'ROOT_PR305_ACTUAL_MERGE_VERIFICATION.json';assert not out.exists();out.write_text(json.dumps(receipt,indent=2)+'\n')
(D/'ROOT_PR305_POST_MERGE_CUSTODY.json').write_text(json.dumps(dict(UTC=receipt['UTC'],status='PASS_ROOT_PR305_ACTUAL_MERGE_FULL_NATIVE_CUSTODY',actual_merge=MERGED,original_actual_native_captures=377,fresh_readonly_operations=len(ops),exact_owned_paths=34,other_known_held_bodies_modes_verified=19145,foreign_state_preserved=True,publication_tracker_immutable=True,actual_merge_receipt=g.pin(out),original_failed_outer_preserved=True,no_mutation_repeated=True),indent=2)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+receipt['UTC']+' — One actual original-head PR305 merge and push succeeded (commit62318/push62553). Initial outerexit1 truthfully preserves immediateGitHubOPENlag; fresh read-only reconciliation confirms exactmergedb3eaf,2parents/34paths/29historicbody-mode-blobs/author1/5/fourQUEUEcells/publicfiles. Full377 actual nativecaptures+freshreadbacks/19145held/wholeforeignindexflagsdiff verified, no mutation repeated. DOI23149775 and trackerA24D24 unchanged. Math100%,boundedpriority100%,PRworkflow100%; global completion checkpoint pending.\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='reconciliation'},indent=2))
