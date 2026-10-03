"""Read exact Git originals and reproduce unchanged helpers in private copies."""
from pathlib import Path
import hashlib,json,os,stat,subprocess,sys,datetime
F=Path(__file__).resolve().parent
A=F.parent
S=A/'source_snapshot'
R=Path('/Users/alec/Documents/Math')
def sha(b):return hashlib.sha256(b).hexdigest()
def typed_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b
actual=[]
def run(name,argv,target=None):
    cmd=[sys.executable,'-B',str(F/'capture_actual_command.py')]
    if target is not None:cmd+=['--target-source',str(target)]
    name = 'v2_'+name
    cmd += [name,'--']+argv
    p=subprocess.run(cmd,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    assert p.returncode==0,(name,p.stderr.decode())
    d=F/name
    c=json.loads((d/'CAPTURE.json').read_bytes())
    assert c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0
    assert c['operator_unchanged'] is True and (target is None or c['target_unchanged'] is True)
    assert c['argv']==argv
    for n in ['stdout','stderr']:
        b=(d/(n+'.bin')).read_bytes();assert len(b)==c[n]['bytes'] and sha(b)==c[n]['sha256']
    actual.append({'name':name,'capture_sha256':sha((d/'CAPTURE.json').read_bytes()),'record':c})
    return (d/'stdout.bin').read_bytes()
snapshot=json.loads((A/'snapshot_manifest.json').read_bytes())
assert snapshot['head']=='036a5ed59bee5ed79f08349290481584610f1456'
assert snapshot['original_files']==16 and len(snapshot['files'])==16
read=[]
for i,row in enumerate(snapshot['files']):
    f=S/row['relative_path'];b=f.read_bytes()
    assert not f.is_symlink() and stat.S_IMODE(f.stat().st_mode)==row['snapshot_full_mode']==0o444
    assert len(b)==row['bytes'] and sha(b)==row['sha256']
    gb=run('replay_git_body_%02d'%i,['git','show',snapshot['head']+':'+row['path']])
    assert gb==b
    tb=run('replay_git_tree_%02d'%i,['git','ls-tree',snapshot['head'],'--',row['path']])
    assert tb.decode().strip()==row['git_mode']+' '+row['git_kind']+' '+row['git_object']+'\t'+row['path']
    assert row['git_mode']=='100644' and row['git_kind']=='blob'
    read.append(dict(row))
mb=run('replay_git_merge_base',['git','merge-base',snapshot['head'],snapshot['github_base']]).decode().strip()
assert mb==snapshot['merge_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
diff=run('replay_git_full_diff',['git','diff','--no-ext-diff','--no-textconv','--binary',mb,snapshot['head'],'--'])
assert diff==(A/'original_diff.patch').read_bytes()
assert len(diff)==52829 and sha(diff)=='9aafdb42b2983020e919d6ff66b03720e1d858eebd98b4e46fa6b3909923fb50'
assert (S/'verify.py').read_bytes()==(S/'review/submitted_verify.py').read_bytes()
assert (S/'verification.json').read_bytes()==(S/'review/verification.json').read_bytes()
helpers=[]
for name,source,old_result,count in [
    ('submitted_author','verify.py','verification.json',69),
    ('identical_historical_submitted','review/submitted_verify.py','review/verification.json',69),
    ('historical_independent','review/independent_checks.py','review/independent_results.json',187)]:
    d=F/'private_replays_v2'/name;d.mkdir(parents=True,exist_ok=False)
    target=d/Path(source).name
    sb=(S/source).read_bytes();target.write_bytes(sb)
    old=(S/old_result).read_bytes()
    out=run('replay_'+name,[sys.executable,'-B',str(target)],target)
    result=d/Path(old_result).name
    new=result.read_bytes()
    before=json.loads(old);after=json.loads(new)
    assert new==old and typed_equal(before,after)
    assert type(after['passed']) is int and after['passed']==count and after['failed']==0
    assert len(after['checks'])==count and all(v=='PASS' for v in after['checks'].values())
    short={k:v for k,v in after.items() if k!='checks'}
    assert typed_equal(json.loads(out),short)
    assert target.read_bytes()==sb
    helpers.append({'name':name,'source':source,'source_sha256':sha(sb),'result_sha256':sha(new),'result_bytes':len(new),'passed':count,'full_result_byte_exact':True,'all_scalar_types_exact':True,'duplicate_run_is_new_independence':False if name=='identical_historical_submitted' else None})
turns=json.loads((S/'turns.json').read_bytes())
assert type(turns['count']) is int and turns['count']==0 and turns['substantive_attempts']==[]
res={'schema':'pr49-boundary-unchanged-original-reproduction/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'original_head':snapshot['head'],'complete_16_git_body_mode_checks':read,'full_17_path_diff_bytes':len(diff),'full_diff_sha256':sha(diff),'merge_base':mb,'helpers':helpers,'complete_actual_captures':actual,'original_substantive_attempts':0,'own_added_substantive_attempts':0,'source_verification_response':1,'full_original_preparation_closure_checked':False,'ROOT_acceptance_authority':False,'paper_DOI_or_tracker_created':False}
(F/'UNCHANGED_REPRODUCTION_V2.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'passed_helpers':len(helpers),'counts':[v['passed'] for v in helpers],'actual_children':len(actual),'original_files':len(read),'full_diff_sha256':sha(diff),'acceptance_authority':False},indent=2))
