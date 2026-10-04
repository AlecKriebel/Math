"""Root full-byte frozen artifact/history/source and complete-output reproduction."""
from pathlib import Path
import base64, concurrent.futures, datetime, hashlib, json, shutil, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];prefix='problems/30004811_capacity_volume_mass';Q='unsolved_math_prioritization/QUEUE.md'
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
S=A/'snapshot';D=S/prefix;private=A/'tmp/root_reproduction';private.mkdir(parents=True,exist_ok=True);streams=A/'root_original_streams';streams.mkdir(exist_ok=True)
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(c,name,**v):
    checks.append({'name':name,'passed':bool(c),**v});assert c,name
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def data(rev,path):return git('show',rev+':'+path)
frozen=json.loads((A/'snapshot_manifest.json').read_bytes());head=frozen['head'];base=frozen['base'];ck(len(frozen['files'])==19,'exact19_declared_paths')
paths={r['path'] for r in frozen['files']};ck(paths==set(git('diff','--name-only',base,head).decode().splitlines()),'actual_git_diff_exact19')
ck(paths-{Q}=={prefix+'/'+p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()},'complete18_target_snapshot_scope')
def remote(e):
    p=e['path'];r=subprocess.run(['gh','api','repos/AlecKriebel/Math/contents/'+p+'?ref='+head],capture_output=True);(private/(p.replace('/','__')+'.api')).write_bytes(r.stdout);ck(r.returncode==0,'remote_read_'+p)
    j=json.loads(r.stdout);b=(S/p).read_bytes();local=data(head,p)
    return {'path':p,'bytes':len(b),'sha256':sha(b),'git_blob':blob(b),'passed':base64.b64decode(j['content'])==b==local and len(b)==e['bytes']==j['size'] and sha(b)==e['sha256'] and blob(b)==e['git_blob_sha']==j['sha']}
remote_rows=list(concurrent.futures.ThreadPoolExecutor(8).map(remote,frozen['files']))
for row in remote_rows:ck(row['passed'],'literal_git_remote_snapshot_'+row['path'])
nested=[]
for manifest,root in [('FINAL_AUTHOR_MANIFEST.json',D),('PUBLICATION_MANIFEST.json',D),('REVIEW_MANIFEST.json',D/'review')]:
    m=json.loads((root/manifest).read_bytes());seen=set()
    for e in m['files']:
        p=e['path'];ck(p not in seen and not Path(p).is_absolute() and '..' not in Path(p).parts,'safe_manifest_'+manifest+'_'+p);seen.add(p)
        b=(root/p).read_bytes();row={'manifest':manifest,'path':(root/p).relative_to(D).as_posix(),'bytes':len(b),'sha256':sha(b),'passed':len(b)==e['bytes'] and sha(b)==e['sha256']};nested.append(row);ck(row['passed'],'nested_binding_'+manifest+'_'+p)
ck(len(nested)==29,'all29_manifest_instances')
author='1901d52ea8b47b4dd3c843cb2e02be2c520da7cb'
author_files={prefix+'/'+e['path'] for e in json.loads((D/'FINAL_AUTHOR_MANIFEST.json').read_bytes())['files']}|{prefix+'/FINAL_AUTHOR_MANIFEST.json'}
for p in sorted(author_files):ck(data(author,p)==data(head,p),'actual_author_checkpoint_byte_'+p)
ck(len(author_files)==10,'ten_author_files_anchored_to_actual_checkpoint')
ck(subprocess.run(['git','merge-base','--is-ancestor',author,head],cwd=R).returncode==0,'author_checkpoint_ancestor')
before=data(base,Q);lines=before.splitlines(keepends=True);target=[i for i,l in enumerate(lines) if b'30004811 / OWR-8415343-014' in l];ck(len(target)==1,'unique_original_queue_row');i=target[0];cells=lines[i].split(b'|');ck(cells[8:10]==[b' queued ',b' 0/5 '],'original_queue_before_cells');cells[8:10]=[b' already_solved ',b' 1/5 '];lines[i]=b'|'.join(cells);ck(b''.join(lines)==(S/Q).read_bytes(),'original_wholequeue_onlycells8_9')
sources=[];source_mf=json.loads((D/'SOURCE_MANIFEST.json').read_bytes());test=private/'candidate_with_sources';test.mkdir(exist_ok=True)
for p in paths-{Q}:
    f=test/Path(p).relative_to(prefix);f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/p,f)
(test/'sources').mkdir(exist_ok=True)
for e in source_mf['files']:
    p=A/'raw_sources'/e['name'];p=p if p.exists() else A/'raw_sources'/'OWR2021-40.pdf';b=p.read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'fresh_historical_primary_'+e['name']);sources.append({'name':e['name'],'bytes':len(b),'sha256':sha(b),'matches_historical':True});shutil.copyfile(p,test/'sources'/e['name'])
ck(len(sources)==7,'seven_source_identities_freshly_reproduced')
commands=[('author',[str(PY),str(D/'check_turn_1.py')]),('original_review',[str(PY),str(D/'review/check.py'),str(test)]),('portable_no_sources',[str(PY),str(D/'review/portable_check.py'),str(D)]),('portable_with_sources',[str(PY),str(D/'review/portable_check.py'),str(test)]),('publication_no_sources',[str(PY),str(D/'verify_publication.py')]),('publication_with_sources',[str(PY),str(test/'verify_publication.py')])]
replays=[];old_author=(D/'TURN_1_CHECKS.json').read_bytes();old_review=json.loads((D/'review/CHECKS.json').read_bytes())
for label,args in commands:
    r=subprocess.run(args,cwd=private,capture_output=True);(streams/(label+'.stdout')).write_bytes(r.stdout);(streams/(label+'.stderr')).write_bytes(r.stderr);ck(r.returncode==0 and not r.stderr,'replay_exit_'+label);out=json.loads(r.stdout)
    if label=='author':ck(r.stdout==old_author,'author_full_byte_exact')
    elif label in ['original_review','portable_with_sources']:ck(out==old_review,'complete_review_json_'+label)
    elif label=='portable_no_sources':expected=dict(old_review,source_pdfs=0);ck(out==expected,'portable_complete_json_only_source_count0')
    else:expected={'status':'PASS','all_public_hashes':True,'author_assertions':5529,'independent_assertions':3128,'raw_source_hashes_checked_this_run':7 if label.endswith('with_sources') else 0};ck(out==expected,'complete_publication_json_'+label)
    replays.append({'label':label,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'complete_output':out})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','frozen_head':head,'base':base,'checks':checks,'remote_files':remote_rows,'manifest_binding_instances':nested,'binding_count':29,'primary_sources':sources,'author_checkpoint':author,'author_checkpoint_files':10,'historical_review_first_parent_anchor_claimed':False,'queue_physical_line':i+1,'original_accepted_row':lines[i].decode(),'replays':replays,'math_seal_precedes_replay':json.loads((A/'root_mathematical_reconstruction_seal.json').read_bytes())['utc'],'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'remote_files':len(remote_rows),'nested_bindings':29,'replays':len(replays),'author_assertions':5529,'independent_assertions':3128,'primary_pdfs':7},indent=2))
