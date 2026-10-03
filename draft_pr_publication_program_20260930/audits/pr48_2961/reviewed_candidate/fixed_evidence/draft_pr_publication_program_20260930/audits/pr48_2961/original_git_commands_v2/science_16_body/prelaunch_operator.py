"""Literal PR48 original export; no old helper execution or native writes."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat, subprocess
A=Path(__file__).resolve().parent
R=A.parents[2]
ID='2961'
HEAD='e2e5c8c3e5ad218f867fa753c465bb96b3687bda'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX='unsolved_math_prioritization/attempts/'+ID+'/'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        assert p.is_file() and not p.is_symlink() and p.read_bytes()==b,('existing unequal',str(p));return
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def js(p,x):write(p,(json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
def cmd(label,argv):
    d=A/'original_git_commands_v2'/label;d.mkdir(parents=True)
    src=Path(__file__).read_bytes();write(d/'prelaunch_operator.py',src)
    rec=dict(schema='pr48-original-git-command/v1',argv=argv,cwd=str(R),operator_sha256=sha(src),started_utc=now(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    js(d/'PRELAUNCH.json',rec)
    p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();rec.update(actual_execution=True,completed=True,pid=p.pid,exit_code=p.returncode,finished_utc=now())
    for key,b in [('stdout',out),('stderr',err)]:write(d/(key+'.bin'),b);rec[key]=dict(path=key+'.bin',bytes=len(b),sha256=sha(b))
    rec['operator_unchanged']=Path(__file__).read_bytes()==src;js(d/'CAPTURE.json',rec);assert p.returncode==0,(label,p.returncode)
    return out
def blob(path,i):
    t=cmd('science_%02d_tree'%i,['git','ls-tree','-z',HEAD,'--',path]);assert t.count(b'\0')==1 and t.endswith(b'\0')
    meta,literal=t[:-1].split(b'\t');mode,kind,oid=meta.decode().split(' ');assert kind=='blob' and literal.decode()==path
    b=cmd('science_%02d_body'%i,['git','cat-file','blob',oid]);return b,dict(path=path,git_mode=mode,git_object=oid,bytes=len(b),sha256=sha(b))
def memory_native(ref,path):
    t0=now();p=subprocess.Popen(['git','ls-tree','-z',ref,'--',path],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);t,e=p.communicate();t1=now();assert p.returncode==0 and not e and t.count(b'\0')==1
    meta,literal=t[:-1].split(b'\t');mode,kind,oid=meta.decode().split(' ');assert kind=='blob' and literal.decode()==path
    b0=now();q=subprocess.Popen(['git','cat-file','blob',oid],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,er=q.communicate();b1=now();assert q.returncode==0 and not er
    return b,dict(path=path,git_ref=ref,git_mode=mode,git_object=oid,bytes=len(b),sha256=sha(b),body_read_in_full=True,tree_query_pid=p.pid,tree_query_started_utc=t0,tree_query_finished_utc=t1,body_read_pid=q.pid,body_read_started_utc=b0,body_read_finished_utc=b1,native_raw_body_retained=False)
def read_native(path):
    p=R/path;before=p.stat();b=p.read_bytes();after=p.stat();assert (before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_size,after.st_mtime_ns,after.st_mode)
    return b,dict(path=path,bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(before.st_mode),mtime_ns=before.st_mtime_ns,body_read_in_full=True,raw_body_retained=False,captured_utc=now())
def exact_selected(obj):
    if isinstance(obj,list):return [x for x in obj if isinstance(x,dict) and type(x.get('id')) is int and x['id']==2961]
    if isinstance(obj,dict):return dict(key=ID,key_present=ID in obj,value=obj.get(ID))
    raise AssertionError(type(obj))
def treeparse(b):
    out=[]
    for v in b.split(b'\0'):
        if not v:continue
        meta,path=v.split(b'\t');mode,kind,oid=meta.decode().split(' ');out.append(dict(path=path.decode(),git_mode=mode,git_kind=kind,git_object=oid))
    return out
def main():
    src=Path(__file__).read_bytes();write(A/'EXPORT_V2_PRELAUNCH_SOURCE.py',src)
    m=json.loads((A/'github_metadata_actual_capture/stdout.bin').read_bytes());api=sum(json.loads((A/'github_changed_files_actual_capture/stdout.bin').read_bytes()),[])
    assert m['number']==48 and m['state']=='open' and m['draft'] is True and m['head']['sha']==HEAD and m['base']['sha']==BASE
    assert cmd('current_branch',['git','branch','--show-current'])==b'main\n'
    mainhead=cmd('current_head',['git','rev-parse','HEAD']).decode().strip();mb=cmd('merge_base',['git','merge-base',BASE,HEAD]).decode().strip()
    for label,ref in [('head_commit',HEAD),('base_commit',BASE),('actual_merge_base_commit',mb)]:cmd(label,['git','cat-file','commit',ref])
    names=cmd('changed_paths',['git','diff','--name-status','-z',mb,HEAD]).split(b'\0');assert names.pop()==b'' and len(names)%2==0
    changes=[dict(status=names[i].decode(),path=names[i+1].decode()) for i in range(0,len(names),2)]
    assert len(changes)==m['changed_files']==len(api)==18 and {x['path'] for x in changes}=={x['filename'] for x in api}
    diff=cmd('whole_diff',['git','diff','--no-ext-diff','--no-textconv','--binary',mb,HEAD,'--']);write(A/'original_diff.patch',diff)
    whole=cmd('whole_repository_head_tree',['git','ls-tree','-r','-t','-z',HEAD]);wholeentries=treeparse(whole)
    science=cmd('scientific_full_tree',['git','ls-tree','-r','-t','-z',HEAD,'--',PREFIX]);tree=treeparse(science)
    js(A/'original_full_tree.json',dict(head=HEAD,whole_repository_entries=wholeentries,scientific_entries=tree,whole_repository_tree_bytes=len(whole),whole_repository_tree_sha256=sha(whole),scientific_tree_bytes=len(science),scientific_tree_sha256=sha(science)))
    files=[]
    for i,r in enumerate(changes):
        path=r['path'];assert r['status'] in ('A','M') and (path.startswith(PREFIX) or path=='unsolved_math_prioritization/QUEUE.md')
        b,row=blob(path,i)
        if path.startswith(PREFIX):
            rel=path[len(PREFIX):];pp=PurePosixPath(rel);assert not pp.is_absolute() and '..' not in pp.parts
            p=A/'source_snapshot'/rel;write(p,b);os.chmod(p,0o444);row.update(relative_path=rel,snapshot_full_mode=stat.S_IMODE(p.stat().st_mode));files.append(row)
        else:write(A/'original_queue_in_head.md',b);queue=b;queuebinding=row
    assert len(files)==17 and {x['path'] for x in tree if x['git_kind']=='blob'}=={x['path'] for x in files}
    qrows=[x for x in queue.decode().splitlines() if x.startswith('|') and any(c.strip()==ID or c.strip().startswith(ID+' / ') for c in x.split('|')[1:-1])];assert len(qrows)==1
    natives=['catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','manifest.json','review_v2/related_target_groups.json']
    hn=[]
    for name in natives:
        b,row=memory_native(HEAD,'unsolved_math_prioritization/'+name)
        obj=[json.loads(x) for x in b.splitlines() if x.strip()] if name.endswith('.jsonl') else json.loads(b)
        out='original_native_selected/'+name.replace('/','__');selected=exact_selected(obj) if name not in ('manifest.json','review_v2/related_target_groups.json') else obj
        js(A/out,dict(original_path=row['path'],original_git_binding=row,selected_problem_id=ID,complete_selected_objects=selected,selection_method='exact integer id in list or exact string dictionary key; full policy/group object where applicable',selection_only=True,priority_or_claim_verification=False));row['selected_objects_path']=out;hn.append(row)
    currentpaths=['draft_pr_publication_program_20260930/inventory.json']+['unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]
    current=[]
    for path in currentpaths:
        b,row=read_native(path);row.update(observed_main_head=mainhead,authority_for_future_main=False);current.append(row)
    assert len(current)==13
    wb=[read_native('unsolved_math_prioritization/'+n)[1] for n in natives+['QUEUE.md','README.md','AGENTS.md']]
    foreign=[read_native(p.relative_to(R).as_posix())[1] for p in sorted((R/'unsolved_math_prioritization/cache').glob('*')) if p.is_file()]
    js(A/'original_native_input_bindings.json',dict(schema='pr48-original-native-individual-bindings/v1',captured_utc=now(),actual_pid=os.getpid(),observed_main_head=mainhead,current_canonical_native_inputs=current,current_canonical_native_inputs_count=13,current_native_future_authority=False,head_native_individual_inputs=hn,working_native_individual_inputs=wb,foreign_cached_inputs_individually_bound=foreign,foreign_cached_bytes_never_copied=True,native_input_writes=False))
    js(A/'original_pr_metadata.json',dict(schema='pr48-original-github-and-git-metadata/v1',number=48,problem_id=ID,url=m['html_url'],title=m['title'],body=m['body'],head=HEAD,github_base=BASE,merge_base=mb,observed_main_head=mainhead,github_state=m['state'],github_draft=m['draft'],all_changed_paths=changes,changed_files=len(changes),original_queue_row=qrows[0],original_queue_git_binding=queuebinding,full_diff=dict(path='original_diff.patch',bytes=len(diff),sha256=sha(diff)),captured_utc=now(),actual_pid=os.getpid(),acceptance_verdict=None,mathematical_reproduction_performed=False))
    js(A/'snapshot_manifest.json',dict(schema='pr48-original-source-snapshot/v1',head=HEAD,github_base=BASE,merge_base=mb,files=files,original_files=len(files),scientific_tree_entries=tree,whole_repository_diff_files=len(changes),created_utc=now(),actual_pid=os.getpid(),helper_execution_performed=False,acceptance_verdict=None))
    assert Path(__file__).read_bytes()==src
    print(json.dumps(dict(status='ORIGINAL_EXPORT_COMPLETED_ONLY',head=HEAD,github_base=BASE,merge_base=mb,observed_main_head=mainhead,original_files=len(files),scientific_tree_entries=len(tree),whole_repository_tree_entries=len(wholeentries),diff_files=len(changes),diff_bytes=len(diff),diff_sha256=sha(diff),original_queue_row=qrows[0],canonical_current_native_inputs=len(current)),sort_keys=True))
if __name__=='__main__':main()
