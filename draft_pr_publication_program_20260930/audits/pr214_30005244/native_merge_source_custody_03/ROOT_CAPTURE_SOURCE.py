from pathlib import Path
import types,hashlib,json,os,datetime,difflib
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244");D=A/'native_merge_source_custody_03';D.mkdir(exist_ok=False)
s=(A/'native_source_custody_01/capture_native_custody.py').read_bytes()
assert len(s)==11941 and hashlib.sha256(s).hexdigest()=='a7732c6bef25ca818a03494ba213ce457138213fb25ee863a221f07a43239d6e'
p=D/'PINNED_CAPTURE_CONTEXT.py'
with p.open('xb') as f:f.write(s);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
m=types.ModuleType('Root214_merge_Main_extension');m.__file__=str(p);exec(compile(s,str(p),'exec'),m.__dict__)
def exact_commit(j):
 v=j.get('verification',{});payload=v.get('payload');sig=v.get('signature')
 if type(payload) is str and type(sig) is str:
  hd,body=payload.encode().split(b'\n\n',1)
  out=hd+b'\ngpgsig '+b'\n '.join(sig.encode().split(b'\n'))+b'\n\n'+body
  assert m.native('commit',out)==j['sha']
  assert hd.split(b'\n')[0]==('tree '+j['tree']['sha']).encode()
  assert [x.decode().split(' ',1)[1] for x in hd.split(b'\n') if x.startswith(b'parent ')]==[x['sha'] for x in j['parents']]
  return out
 return m.raw_commit(j)
def getref(label):
 rr=m.h.bounded_get([m.h.GH,'api','--hostname','github.com','repos/AlecKriebel/Math/git/ref/heads/main']);assert rr.returncode==0
 m.write(D/'_private'/(label+'.RAW_STDOUT.json'),rr.stdout);m.write(D/'_private'/(label+'.RAW_STDERR.txt'),rr.stderr)
 j=m.h.decode(rr.stdout);assert j['ref']=='refs/heads/main' and j['object']['type']=='commit' and m.h.hexid(j['object']['sha'])
 return j['object']['sha'],{'method':'GET','hostname':'github.com','route':'git/ref/heads/main','stdout':m.pin(rr.stdout),'stderr':m.pin(rr.stderr),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
merge=m.fetch('git/commits/'+m.MERGE);raw=exact_commit(merge);m.write(D/'_private/native_commits'/(m.MERGE+'.commit'),raw)
parents=[r['sha'] for r in merge['parents']];assert parents==['5fde5b9aa46bb620d7a0d3b036ceb914076c6303',m.CURRENT]
root=merge['tree']['sha'];assert root==m.CURRENT_ROOT
attempt=m.lookup(root,m.ATTEMPT);assert attempt=={'mode':'040000','type':'tree','sha':'f457caef697fbb8e82f79588a4f2fb3c0860546d'}
prior='draft_pr_descending_audit_20261002/audits/pr214_30005244'
merge_old=m.lookup(root,prior);prepared_old=m.lookup(m.CURRENT_ROOT,prior);assert merge_old==prepared_old
R,before=getref('MAIN_BEFORE');cm=m.fetch('git/commits/'+R);cr=exact_commit(cm);m.write(D/'_private/native_commits'/(R+'.commit'),cr);rt=cm['tree']['sha']
ra=m.lookup(rt,m.ATTEMPT);ro=m.lookup(rt,prior);assert ra['mode']=='040000' and ra['type']=='tree'
prepared_leaves=m.descendants(attempt['sha'],m.ATTEMPT);main_leaves=m.descendants(ra['sha'],m.ATTEMPT)
assert len(prepared_leaves)==41 and len(main_leaves)<=60
history=m.ATTEMPT+'/history'
assert m.lookup(root,history)==m.lookup(rt,history)
records=[];changed=[];diffs=[]
for path,row in sorted(main_leaves.items()):
 assert row['type']=='blob' and row['mode']=='100644'
 bb=m.body(row['sha']);m.write(D/'_private/reading/Main'/path,bb)
 records.append({'path':path,**row,**m.pin(bb),'actual_native_body_GET_or_same_capture_OID_cache':True})
 old=prepared_leaves.get(path)
 if old!=row:
  assert '/history/' not in path
  oldraw=m.body(old['sha']) if old else b''
  if old:m.write(D/'_private/reading/prepared'/path,oldraw)
  changed.append({'path':path,'prepared':old,'observed_Main':row,'prepared_body':m.pin(oldraw) if old else None,'Main_body':m.pin(bb)})
  diffs.append(''.join(difflib.unified_diff(oldraw.decode().splitlines(True),bb.decode().splitlines(True),fromfile='prepared/'+path,tofile='Main/'+path)))
removed=sorted(set(prepared_leaves)-set(main_leaves));assert not removed
candidate=m.ATTEMPT+'/CANDIDATE.md'
oldcandidate=m.body(prepared_leaves[candidate]['sha']);newcandidate=m.body(main_leaves[candidate]['sha'])
marker=b'# Spectral correctness of cubic DDA away from the static lattice interval'
assert oldcandidate.count(marker)==1 and newcandidate.count(marker)==1
assert oldcandidate.split(marker,1)[1]==newcandidate.split(marker,1)[1]
qe=m.lookup(rt,'unsolved_math_prioritization/QUEUE.md');qb=m.body(qe['sha']);assert qe['mode']=='100644' and qe['type']=='blob'
own=[]
for line in qb.splitlines(keepends=True):
 cells=line.decode().split('|')
 if len(cells)==14 and cells[2].strip().split(' / ')[0]=='30005244':own.append((line,cells))
assert len(own)==1 and own[0][1][8].strip()=='claimed_solved' and own[0][1][9].strip()=='2/5'
m.write(D/'_private/reading/Main/unsolved_math_prioritization/QUEUE.md',qb)
critical=[]
for suffix,expected_bytes,expected_sha in [
 ('dipole_spectrum.tex',34975,'5d1145a052135d34997614be42142f9b63ef76730ca9992e045d52548747dd7e'),
 ('metadata.json',2895,'1b31ef284ddb6cc918513e9d9a05c0ec3249cdd0c884b7ad0daa78547d0c3b2d'),
 ('deposit.json',3109,'afeda4d189d627ac27c8525a06789b0c065366ad307e82eb476b8b679a30f761')]:
 path=prior+'/preprint/'+suffix;tuples=[m.lookup(x,path) for x in [m.CURRENT_ROOT,root,rt]]
 assert all(t==tuples[0] and t['type']=='blob' and t['mode']=='100644' for t in tuples)
 bb=m.body(tuples[0]['sha']);assert len(bb)==expected_bytes and hashlib.sha256(bb).hexdigest()==expected_sha
 critical.append({'path':path,'tuple_at_prepared_merge_Main':tuples[0],**m.pin(bb)})
instructions={}
for prefix in ('','unsolved_math_prioritization','unsolved_math_prioritization/attempts',m.ATTEMPT):
 for filename in ('AGENTS.md','CLAUDE.md'):
  path=(prefix+'/' if prefix else '')+filename;row=m.lookup(rt,path)
  if row:
   assert row['type']=='blob' and row['mode'] in ('100644','100755')
   bb=m.body(row['sha']);m.write(D/'_private/reading/Main'/path,bb);instructions[path]={**row,**m.pin(bb),'tuple_same_as_prepared':row==m.lookup(root,path)}
R2,after=getref('MAIN_AFTER')
m.write(D/'AUTHENTICATED_TREES.json',m.encode(m.TREES))
m.write(D/'MAIN_OWN_BODY_RECORDS.json',m.encode(records))
m.write(D/'PREPARED_TO_MAIN_OWN_DELTA.json',m.encode({'changed':changed,'removed':removed,'history_subtree_unchanged':True,'analytical_candidate_after_exact_title_unchanged':True}))
m.write(D/'PREPARED_TO_MAIN_OWN_DIFF.txt','\n'.join(diffs).encode())
result={'schema':'pr214-root-dated-merge-and-Main-source-extension-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':214,'actual_merge_commit':m.MERGE,'merge_root':root,'merge_ordered_parents':parents,'raw_merge_commit_pin':m.pin(raw),'prepared_head':m.CURRENT,'prepared_root':m.CURRENT_ROOT,'actual_MAIN_observed':R,'actual_MAIN_tree':rt,'raw_Main_commit_pin':m.pin(cr),'Main_ref_after':R2,'coherent_before_after_Main_ref':R2==R,'Main_ref_observations':[before,after],'own_attempt_path':m.ATTEMPT,'own_attempt_tuple_prepared_and_merge':attempt,'own_attempt_tuple_observed_Main':ra,'prepared_own_file_count':len(prepared_leaves),'Main_own_file_count':len(main_leaves),'changed_own_file_count':len(changed),'removed_own_file_count':0,'history_subtree_unchanged':True,'analytical_candidate_after_exact_title_unchanged':True,'old_owned_audit_path':prior,'old_owned_audit_tuple_prepared_and_merge':merge_old,'old_owned_audit_tuple_observed_Main':ro,'whole_old_audit_unchanged_since_merge':ro==merge_old,'critical_published_sources_same_at_prepared_merge_Main':critical,'whole_Main_QUEUE':{**qe,**m.pin(qb)},'own_Main_QUEUE_row_pin':m.pin(own[0][0]),'own_Main_QUEUE_row':own[0][0].decode(),'own_Main_status':'claimed_solved','own_Main_effort':'2/5','applicable_Main_instructions':instructions,'scope':'Actual native immutable merge and dated Main bodies/tree associations. Distinct prepared/merge/Main attempt identities retained; post-merge changes require Root reading/acceptance, not inferred from ancestry. No Main parent admission, candidate, math/priority/adoption/CAS/completion authority. Later admission must preserve actual fresh-parent own and old-audit opaque tuples.','Root_no_Git_commands':True,'no_mutations_or_original_lock_actions':True,'subtask_percent':95}
m.write(D/'ROOT_MERGE_MAIN_ASSOCIATION_01.json',m.encode(result))
print(json.dumps({'result':str(D/'ROOT_MERGE_MAIN_ASSOCIATION_01.json'),**m.pin(m.encode(result)),'merge_root':root,'merge_parents':parents,'R':R,'Rroot':rt,'Rafter':R2,'coherent':R2==R,'Main_files':len(main_leaves),'changed':len(changed),'native_GETs':len(m.ledger())+2}))
