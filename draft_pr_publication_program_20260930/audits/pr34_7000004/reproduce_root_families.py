"""Actual unchanged family replays in private trees; no shared artifact writes."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text())
families=['differential_family','differential_family/qualification_readiness_hash','linking_family','primary_scope_family']
bindings=[]
for name in families:
    f=HERE/name;m=load(f/'MANIFEST.json')
    for z in m.get('members',m.get('files')):
        b=(f/z['path']).read_bytes();assert len(b)==z.get('bytes',z.get('size')) and sha(b)==z['sha256'],z['path']
        bindings.append({'path':str((f/z['path']).relative_to(HERE)),'sha256':sha(b)})
    bindings.append({'path':name+'/MANIFEST.json','sha256':sha((f/'MANIFEST.json').read_bytes())})
assert len(bindings)==90,len(bindings)
private=HERE/'tmp/root_remaining_replays';private.mkdir(parents=True,exist_ok=True)
def copy_members(source,dest):
    dest.mkdir(parents=True,exist_ok=True)
    m=load(source/'MANIFEST.json')
    for z in m.get('members',m.get('files')):
        p=dest/z['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/z['path'],p)
    shutil.copyfile(source/'MANIFEST.json',dest/'MANIFEST.json')
def run(name,code,args,expected=None):
    r=subprocess.run(['/usr/bin/python3',str(code)]+[str(x) for x in args],capture_output=True)
    (private/(name+'.stdout')).write_bytes(r.stdout);(private/(name+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and not r.stderr,(name,r.returncode,r.stderr.decode())
    return {'name':name,'actual_code_sha256':sha(code.read_bytes()),'exit_code':r.returncode,'stderr_empty':True,'stdout_sha256':sha(r.stdout),'output':json.loads(r.stdout)}
link=private/'linking_family';copy_members(HERE/'linking_family',link)
shutil.copytree(HERE/'source_snapshot',private/'source_snapshot',dirs_exist_ok=True)
runs=[run('linking_full',link/'reproduce.py',['--output',private/'linking_outputs'])]
actual=runs[0]['output'];old=load(HERE/'linking_family/REPRODUCTION_RESULTS.json')
assert actual==old,'Full linking reproduction JSON differs'
runs[0]['full_saved_reproduction_json_equal']=True
replica=private/'scope_replica'; target=replica/'draft_pr_publication_program_20260930/audits/pr34_7000004'
copy_members(HERE/'primary_scope_family',target/'primary_scope_family')
shutil.copytree(HERE/'source_snapshot',target/'source_snapshot',dirs_exist_ok=True)
shutil.copyfile(HERE/'snapshot_manifest.json',target/'snapshot_manifest.json')
u=replica/'unsolved_math_prioritization';u.mkdir(parents=True,exist_ok=True)
for name in ['manifest.json','policy.json','QUEUE.md']:
    shutil.copyfile(ROOT/'unsolved_math_prioritization'/name,u/name)
(u/'review_v2').mkdir(exist_ok=True)
shutil.copyfile(ROOT/'unsolved_math_prioritization/review_v2/related_target_groups.json',u/'review_v2/related_target_groups.json')
for name,src in [('.git',ROOT/'.git'),('unsolved_math_prioritization/cache',ROOT/'unsolved_math_prioritization/cache')]:
    p=replica/name
    if not p.exists():p.symlink_to(src,target_is_directory=True)
code=target/'primary_scope_family/source_priority_controls.py'
runs.append(run('primary_scope_actual',code,[]))
result=code.with_name('source_priority_controls_results.json')
assert result.read_bytes()==(HERE/'primary_scope_family/source_priority_controls_results.json').read_bytes()
runs[-1]['saved_result_byte_exact']=True;runs[-1]['saved_result_sha256']=sha(result.read_bytes())
qual=private/'qualification_readiness_hash';copy_members(HERE/'differential_family/qualification_readiness_hash',qual)
cache=ROOT/'unsolved_math_prioritization/cache'
runs.append(run('hash_roles_actual',qual/'verify_hash_roles.py',['--repo',ROOT,'--problems',cache/'problems.json','--reports',cache/'research_results.json']))
result=qual/'RESULTS.json';assert result.read_bytes()==(HERE/'differential_family/qualification_readiness_hash/RESULTS.json').read_bytes()
runs[-1]['saved_result_byte_exact']=True;runs[-1]['saved_result_sha256']=sha(result.read_bytes())
for z in bindings:assert sha((HERE/z['path']).read_bytes())==z['sha256'],z['path']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closed_members_and_manifests_verified':90,'all_closed_bytes_unchanged':True,'actual_unchanged_runs':runs,'hash_role_input_scope':'Complete pinned cached source corpus; earlier fresh retrieval independently bound by family receipts; pure actual queue.score only, no generator.','new_substantive_attempts_for_reproduction':0,'scope':'Root actual program replays supplement universal proofs; diagnostic counts do not prove global claims.'}
(HERE/'ROOT_REMAINING_FAMILY_REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':True,'closed_bindings':90,'runs':len(runs),'new_original_attempts':0}))
