#!/usr/bin/python3
"""Read-only exact original-head and receipt audit; writes only own result."""
import datetime,hashlib,json,pathlib,stat,subprocess
own=pathlib.Path(__file__).resolve().parent
a=own.parent;repo=pathlib.Path('/Users/alec/Documents/Math')
head='036a5ed59bee5ed79f08349290481584610f1456'
base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
ops=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*args):
    argv=['git']+list(args);pre=utc()
    p=subprocess.Popen(argv,cwd=str(repo),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    ops.append({'argv':argv,'cwd':str(repo),'prelaunch_utc':pre,'completed_utc':utc(),'pid':p.pid,'returncode':p.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'full_both_streams_read':True})
    assert p.returncode==0,(argv,p.returncode)
    return out
def typed(x,y):
    if type(x) is not type(y):return False
    if isinstance(x,dict):return x.keys()==y.keys() and all(typed(x[k],y[k]) for k in x)
    if isinstance(x,list):return len(x)==len(y) and all(typed(u,v) for u,v in zip(x,y))
    return x==y
def pairs(ps):
    d={}
    for k,v in ps:
        assert k not in d,('duplicate key',k)
        d[k]=v
    return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs)
manifest=load(a/'snapshot_manifest.json')
assert manifest['schema']=='pr49-original-source-snapshot/v1'
assert manifest['head']==head and manifest['github_base']==base and manifest['merge_base']==base
rows=[]
for f in manifest['files']:
    p=a/'source_snapshot'/f['relative_path'];b=p.read_bytes()
    tree=git('ls-tree','-z',head,'--',f['path'])
    mode,kind,obj=tree.split(b'\t')[0].decode().split()
    original=git('cat-file','blob',obj)
    assert mode==f['git_mode']=='100644' and kind==f['git_kind']=='blob' and obj==f['git_object']
    assert b==original and len(b)==f['bytes'] and sha(b)==f['sha256']
    assert stat.S_IMODE(p.stat().st_mode)==f['snapshot_full_mode']==0o444
    rows.append({'relative_path':f['relative_path'],'bytes':len(b),'sha256':sha(b),'git_object':obj,'git_mode':mode,'snapshot_mode':'0444','exact_head_body_equal':True})
assert len(rows)==16
diff=git('diff','--no-ext-diff','--binary',base,head)
saved=(a/'original_diff.patch').read_bytes()
assert diff==saved and len(diff)==52829 and sha(diff)=='9aafdb42b2983020e919d6ff66b03720e1d858eebd98b4e46fa6b3909923fb50'
paths=git('diff','--name-status',base,head).decode().splitlines()
assert len(paths)==17
# Reconstruct all added scientific bodies from the complete diff, not hashes alone.
sections=diff.split(b'diff --git ')[1:];reconstructed=0
for sec in sections:
    line=sec.splitlines()[0].decode();path=line.split(' b/',1)[1]
    if not path.startswith('unsolved_math_prioritization/attempts/30000703/'):continue
    body=b''.join(v[1:] for v in sec.splitlines(keepends=True) if v.startswith(b'+') and not v.startswith(b'+++'))
    p=a/'source_snapshot'/path.split('/30000703/',1)[1]
    assert body==p.read_bytes(),path
    reconstructed+=1
assert reconstructed==16
queue=git('show',head+':unsolved_math_prioritization/QUEUE.md').decode()
queue_rows=[v for v in queue.splitlines() if '| 30000703 / OWR-1460-009 |' in v]
assert len(queue_rows)==1 and '| already_solved | 0/5 |' in queue_rows[0]
assert load(a/'source_snapshot'/'turns.json')=={'id':30000703,'count':0,'substantive_attempts':[],'reason':'Stopped at known-result source gate; the short point-to-arc application and examples verify the existing criterion rather than constitute a fresh proof-search route.'}
assert (a/'source_snapshot'/'prior_report.json').read_bytes()==b'null\n'
replay=[]
specs=[('author','author_replay/verify.py','verify.py','author_replay/verification.json','verification.json',69),('duplicate_author','duplicate_author_replay/submitted_verify.py','review/submitted_verify.py','duplicate_author_replay/verification.json','review/verification.json',69),('historical_independent','historical_independent_replay/independent_checks.py','review/independent_checks.py','historical_independent_replay/independent_results.json','review/independent_results.json',187)]
for name,copied,original,result,savedresult,count in specs:
    cp=own/copied;op=a/'source_snapshot'/original;rp=own/result;sp=a/'source_snapshot'/savedresult
    assert cp.read_bytes()==op.read_bytes()
    r=load(rp);savedr=load(sp)
    assert typed(r,savedr) and rp.read_bytes()==sp.read_bytes()
    assert type(r['passed']) is int and r['passed']==count and type(r['failed']) is int and r['failed']==0
    assert len(r['checks'])==count and all(type(k) is str and type(v) is str and v=='PASS' for k,v in r['checks'].items())
    replay.append({'name':name,'script_sha256':sha(cp.read_bytes()),'result_sha256':sha(rp.read_bytes()),'full_recursive_type_and_all_key_equality':True,'byte_identical':True,'passed':count,'failed':0})
assert (a/'source_snapshot'/'verify.py').read_bytes()==(a/'source_snapshot'/'review/submitted_verify.py').read_bytes()
result={'schema':'pr49-hyperbolic-family-provenance/v1','utc':utc(),'head':head,'base':base,'scientific_files':rows,'added_bodies_reconstructed':reconstructed,'whole_diff_bytes':len(diff),'whole_diff_sha256':sha(diff),'changed_paths':paths,'queue_proposed_status':'already_solved','queue_substantive_attempts':'0/5','queue_head_row':queue_rows[0],'literal_turns_count':0,'prior_report_literal':'null\n','helper_replays':replay,'duplicate_author_is_new_independent_evidence':False,'read_only_git_operations':ops,'new_substantive_attempts':0,'new_audit_attempts':0}
(own/'PROVENANCE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'scientific_files':len(rows),'added_bodies_reconstructed':reconstructed,'whole_diff_bytes':len(diff),'changed_paths':len(paths),'replays':[{'name':r['name'],'passed':r['passed'],'byte_identical':r['byte_identical']} for r in replay],'new_substantive_attempts':0}))
