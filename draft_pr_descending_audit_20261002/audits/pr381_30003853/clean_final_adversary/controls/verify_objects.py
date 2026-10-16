from pathlib import Path
import hashlib,json,subprocess,difflib,datetime
D=Path(__file__).resolve().parents[1]; A=D.parent
M=json.loads((A/'scope_repaired_snapshot_manifest.json').read_text());S=A/'scope_repaired_snapshot';repo=Path('/Users/alec/Documents/Math')
head=M['head'];base=M['base'];old=M['original_frozen_head'];previous=M['previous_review_head']
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
def blob(rev,path):return git('show',f'{rev}:{path}')
assert head=='83862044e1bb334d582b2082bf8b63c6b0eee4c5'
parents=git('show','-s','--format=%P',head).decode().strip().split();assert parents==[previous,base]
entries=[]
for e in M['files']:
 b=(S/e['path']).read_bytes();g=blob(head,e['path'])
 assert b==g
 assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
 actual=git('rev-parse',f"{head}:{e['path']}").decode().strip();assert actual==e['git_blob_sha']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==actual
 entries.append({'path':e['path'],'bytes':len(b),'sha256':e['sha256'],'git_blob_sha':actual,'exact_blob_match':True})
paths={e['path'] for e in M['files']}
diffs=set(git('diff','--name-only',base,head).decode().splitlines());assert diffs==paths,(diffs-paths,paths-diffs)
q='unsolved_math_prioritization/QUEUE.md';before=blob(base,q);after=blob(head,q)
a=before.decode().splitlines(keepends=True);b=after.decode().splitlines(keepends=True)
change=[(i,x,y) for i,(x,y) in enumerate(zip(a,b),1) if x!=y];assert len(a)==len(b) and len(change)==1
line,x,y=change[0];assert '30003853' in x and '30003853' in y
xc=x.split('|');yc=y.split('|');cells=[i for i,(a,b) in enumerate(zip(xc,yc)) if a!=b];assert cells==[8,9],cells
assert xc[8].strip()=='queued' and xc[9].strip()=='0/5';assert yc[8].strip()=='unsolved' and yc[9].strip()=='5/5'
assert before.replace(x.encode(),y.encode(),1)==after
prefix='problems/30003853_thompson_subgroup_abelianization/'
author_changes=set(git('diff','--name-only',old,head,'--',prefix).decode().splitlines())
expected_current={prefix+p for p in ['CURRENT_SCOPE_CORRECTION.md','CURRENT_SCOPE_MANIFEST.json','REVIEWED_STATUS.md','PUBLICATION_MANIFEST.json','verify_publication.py']}
assert author_changes==expected_current
historical=paths-{q}-expected_current
assert len(historical)==41
for p in historical:assert blob(old,p)==blob(head,p)
queue_only=set(git('diff','--name-only',old,previous,'--',prefix,q).decode().splitlines());assert queue_only=={q}
# Parse and bind all historical nested manifest entries without assigning hashes to unreproduced source images/text.
P=S/prefix;bindings=[];source=[];states=[]
for p in sorted(P.rglob('*.json')):
 doc=json.loads(p.read_text())
 if p.name.endswith('STATE.json') or p.name=='TURN_STATE.json':states.append({'path':str(p.relative_to(P)),'data':doc})
 if p.name in ['SOURCE_MANIFEST.json','TURN_3_SOURCES.json','TURN_5_SOURCES.json']:source+=doc['files'];continue
 for e in doc.get('files',[]):
  f=p.parent/e['path']
  if not f.is_file():raise AssertionError(f)
  z=f.read_bytes();assert len(z)==e['bytes'] and hashlib.sha256(z).hexdigest()==e['sha256']
  if 'git_blob_sha' in e:assert hashlib.sha1(b'blob '+str(len(z)).encode()+b'\0'+z).hexdigest()==e['git_blob_sha']
  bindings.append({'manifest':str(p.relative_to(P)),'path':e['path'],'bytes':len(z),'sha256':e['sha256']})
# Independently fetched complete PDFs match their credited historical source bytes. Processed author text/PNGs remain unreproduced.
mapnames={'owr2018-26.pdf':'owr26_2018_46748.pdf','bieri-geoghegan-kochloukova2010.pdf':'bgk0807.5138v1.pdf','bleak2006-algebraic.pdf':'bleak_math0602038v2.pdf','kassabov-matucci.pdf':'kassabov_matucci_math0607167v3.pdf','guba-sapir2003.pdf':'guba_sapir_math0301225v2.pdf','golan2026.pdf':'golan2609.14702v1.pdf','farley2026.pdf':'farley2606.27753v2.pdf'}
source_receipts=[]
for e in source:
 n=Path(e['path']).name
 if n in mapnames:
  z=(D/'sources'/mapnames[n]).read_bytes();assert len(z)==e['bytes'] and hashlib.sha256(z).hexdigest()==e['sha256'];status='complete independently fetched primary PDF bytes match'
 else:status='author processed text/image binding not reproduced; no current hash-match claim'
 source_receipts.append({'historical_path':e['path'],'historical_sha256':e['sha256'],'status':status})
assert len(source_receipts)==20 and sum('PDF bytes match' in x['status'] for x in source_receipts)==7
assert not any(p.is_symlink() for p in S.rglob('*'))
assert not any(p.name=='.git' for p in S.rglob('*'))
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':head,'parents':parents,'actual_workspace_head':git('rev-parse','HEAD').decode().strip(),'workspace_branch':git('branch','--show-current').decode().strip(),'exact_git_objects':entries,'diff_from_actual_base_paths':sorted(diffs),'historical_unchanged_paths':sorted(historical),'current_correction_paths':sorted(author_changes),'original_to_prior_target_and_queue_scope_only_paths':sorted(queue_only),'queue':{'line':line,'changed_cells':cells,'before':x,'after':y,'all_other_bytes_preserved':True},'nested_manifest_bindings':bindings,'source_receipts':source_receipts,'states':states,'snapshot_no_symlinks_or_nested_git':True}
(D/'OBJECT_SOURCE_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['utc','head','parents','actual_workspace_head','workspace_branch','queue','snapshot_no_symlinks_or_nested_git']},indent=2))
print('exact Git object matches',len(entries),'historical unchanged',len(historical),'nested binding occurrences',len(bindings),'complete fresh PDFs matched',7,'processed source bindings not reproduced',13)
