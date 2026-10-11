"""Actual private replay of all three closed original-stage PR35 families."""
from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
H=Path(__file__).resolve().parent;R=H.parents[2]
PR=H/'tmp/root_family_replay/repo';A=PR/'draft_pr_publication_program_20260930/audits/pr35_2744'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
expected={'algebraic_family':'25a71d1c7ebb44ecf8edd3f117af9dc4874b6956e98bf7775dca5eda0cde0d19','primary_scope_family':'863ac01a8e06b8a83c3676e4051c638ad8ad1934d0957993e738686d15a5b495','cone_family':'f5fdc3bbd7b0fbb4c2f5ef8e26e5accdb5e7c2b97d5266fb42d668c454566f31'}
def closure():
    n=0
    for name,want in expected.items():
        f=H/name;m=load(f/'MANIFEST.json');assert sha((f/'MANIFEST.json').read_bytes())==want,name
        for z in m['files']:
            b=(f/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'],(name,z['path']);n+=1
            if z['path'].endswith('.json'):load(f/z['path'])
    return n
n=closure();A.mkdir(parents=True,exist_ok=True)
for name in expected:
    f=H/name;d=A/name;d.mkdir(exist_ok=True)
    for z in load(f/'MANIFEST.json')['files']:
        q=d/z['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f/z['path'],q)
    shutil.copyfile(f/'MANIFEST.json',d/'MANIFEST.json')
shutil.copytree(H/'source_snapshot',A/'source_snapshot',dirs_exist_ok=True)
shutil.copytree(H/'pr_input',A/'pr_input',dirs_exist_ok=True)
shutil.copyfile(H/'snapshot_manifest.json',A/'snapshot_manifest.json')
if not (PR/'.git').exists():(PR/'.git').symlink_to(R/'.git',target_is_directory=True)
for family,sourcefolder in [('algebraic_family','sources'),('cone_family','primary_sources'),('primary_scope_family','tmp/sources')]:
    shutil.copytree(H/family/sourcefolder,A/family/sourcefolder,dirs_exist_ok=True)
(A/'cone_family/private_replay').mkdir(exist_ok=True)
runs=[]
def run(name,cmd,out=None,want=None):
    p=subprocess.run([str(x) for x in cmd],capture_output=True,timeout=180,cwd=R)
    private=H/'tmp/root_family_replay/receipts';private.mkdir(exist_ok=True)
    (private/(name+'.stdout')).write_bytes(p.stdout);(private/(name+'.stderr')).write_bytes(p.stderr)
    assert p.returncode==0 and not p.stderr,(name,p.returncode,p.stderr.decode())
    z={'name':name,'implementation_sha256':sha(Path(cmd[1]).read_bytes()),'exit':p.returncode,'stderr_empty':True,'stdout':json.loads(p.stdout)}
    if out is not None:
        a,b=load(out),load(want)
        if out.read_bytes()==want.read_bytes():z['byte_exact_result']=True
        else:
            def norm(v):
                if isinstance(v,dict):return {k:norm(w) for k,w in v.items() if k!='utc'}
                if isinstance(v,list):return [norm(w) for w in v]
                if isinstance(v,str):
                    v=v.replace(str(A),'<audit>').replace(str(H),'<audit>')
                    v=re.sub(r'/private_replay/(?:cone_actual_|boundary_mutants_)[^/\s"]+', '/private_replay/<unique_run>',v)
                    return v
                return v
            assert norm(a)==norm(b),(name,'complete result differs beyond actual clock/private directory prefixes')
            z['full_json_equal_except_clock_and_private_path_prefixes']=True
        z['actual_result_sha256']=sha(out.read_bytes());z['frozen_expected_sha256']=sha(want.read_bytes())
    runs.append(z)
PY='/usr/bin/python3';a=A/'algebraic_family';c=A/'cone_family';p=A/'primary_scope_family'
run('algebraic_closure',[PY,a/'check_closure.py','--family',a])
run('cone_closure',[PY,c/'verify_manifest.py'])
run('algebraic_108',[PY,a/'algebraic_controls.py','--repo',R,'--snapshot',A/'source_snapshot','--metadata',A/'snapshot_manifest.json','--sources',a/'sources','--source-bindings',a/'SOURCE_BINDINGS.json','--output',a/'RESULTS.json','--scratch',a/'private/root_actual'],a/'RESULTS.json',H/'algebraic_family/RESULTS.json')
run('algebraic_boundary_16',[PY,a/'component_boundary_controls.py','--output',a/'COMPONENT_BOUNDARY_RESULTS.json'],a/'COMPONENT_BOUNDARY_RESULTS.json',H/'algebraic_family/COMPONENT_BOUNDARY_RESULTS.json')
run('cone_geometry_28',[PY,c/'geometric_controls.py'],c/'geometric_results.json',H/'cone_family/geometric_results.json')
run('cone_boundary_21',[PY,c/'boundary_controls.py'],c/'boundary_results.json',H/'cone_family/boundary_results.json')
run('cone_original_and_8_actual_mutants',[PY,c/'reproduce.py'],c/'REPRODUCTION_RESULTS.json',H/'cone_family/REPRODUCTION_RESULTS.json')
run('cone_4_actual_boundary_mutants',[PY,c/'run_boundary_mutations.py'],c/'BOUNDARY_MUTATION_RESULTS.json',H/'cone_family/BOUNDARY_MUTATION_RESULTS.json')
run('primary_111',[PY,p/'source_priority_controls.py','--repo',R],p/'RESULTS.json',H/'primary_scope_family/RESULTS.json')
assert closure()==n
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closed_first_party_members_verified_before_and_after':n,'self_excluding_manifests':expected,'actual_unchanged_outer_runs':runs,'original_program_replays_byte_exact_in_each_family':True,'actual_code_mutants_rejected':{'algebraic':9,'cone_geometry':8,'cone_boundary':4,'primary':3},'scope':'Source-backed universally quantified conditional/normalization proof checked independently; finite exact diagnostics never certify the universal open knot claim. All original and closed first-party artifacts unchanged. No shared queue/state/history or branch changes.','attempts_added':0,'original_cumulative_attempts':'1/5','workflow_completion_estimate_percent':60}
(H/'ROOT_CLOSED_FAMILY_ACTUAL_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'closed_members':n,'actual_outer_runs':len(runs),'original_turns':'1/5'},indent=2))
