"""Root literal independent-family manifests/seals and full new-control outputs."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, shutil, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
scratch=A/'tmp/root_new_family_controls';scratch.mkdir(parents=True,exist_ok=True);streams=A/'root_family_control_streams';streams.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
replays=[];families=[]
configs=[('asymptotic_normalization_review','independent_controls.py',23,'INDEPENDENT_CONTROLS.json'),('priority_hypotheses_review','distinct_controls.py',15,'DISTINCT_CONTROLS_RECEIPT.json'),('clean_final_adversary','independent_controls.py',10,None)]
for family,program,count,record in configs:
    D=A/family;m=load(D/'PUBLIC_MANIFEST.json');seen=set()
    for e in m['files']:
        p=PurePosixPath(e['path']);assert len(p.parts)==1 and not p.is_absolute() and '..' not in p.parts and e['path']!='PUBLIC_MANIFEST.json' and e['path'] not in seen;seen.add(e['path'])
        f=D/e['path'];raw=f.read_bytes();assert not f.is_symlink() and len(raw)==e['bytes'] and sha(raw)==e['sha256']
    actual={p.name for p in D.iterdir() if p.is_file()};assert actual==seen|{'PUBLIC_MANIFEST.json'}
    if family=='asymptotic_normalization_review':
        seals=[load(D/n) for n in ['SOURCE_FIRST_BASELINE_SEAL.json','INDEPENDENT_VERDICT_SEAL.json']]
        for s in seals:assert sha((D/s['artifact']).read_bytes())==s['sha256']
        assert seals[0]['sealed_utc']<seals[1]['sealed_utc']
    elif family=='priority_hypotheses_review':
        seals=[load(D/n) for n in ['SOURCE_BASELINE_SEAL.json','MATH_VERDICT_SEAL.json']]
        for s in seals:assert sha((D/s['file']).read_bytes())==s['sha256']
        assert seals[0]['sealed_utc']<seals[1]['sealed_utc']
    else:
        seals=[load(D/n) for n in ['SOURCE_FIRST_SEAL.json','MATHEMATICAL_SEAL.json','FINAL_SEAL.json']]
        for s in seals:
            for name,h in s['files'].items():assert sha((D/name).read_bytes())==h
        assert [s['sealed_utc'] for s in seals]==sorted(s['sealed_utc'] for s in seals)
        candidate=load(D/'JSON_AUDIT.json')['complete_candidate_json'];target=A/'snapshot/problems/30004811_capacity_volume_mass'
        assert candidate=={p.relative_to(target).as_posix():load(p) for p in target.rglob('*.json')}
        provenance=load(D/'PROVENANCE.json');assert provenance['git_parents']==['efd29c05204703acca9a0860812f54b94fae54b1','1901d52ea8b47b4dd3c843cb2e02be2c520da7cb']
        assert len(provenance['git_snapshot_byte_checks'])==19 and all(x['equal'] for x in provenance['git_snapshot_byte_checks'])
        assert load(D/'REPRODUCTION.json')['all_expected_outcomes']
    f=scratch/(family+'.py');shutil.copyfile(D/program,f);p=subprocess.run([str(PY),str(f)],cwd=scratch,capture_output=True)
    (streams/(family+'.stdout')).write_bytes(p.stdout);(streams/(family+'.stderr')).write_bytes(p.stderr);assert p.returncode==0 and not p.stderr
    result=json.loads(p.stdout)
    expected=load(D/record) if record else load(D/'REPRODUCTION.json')['runs']['independent_controls']['parsed_stdout']
    assert result==expected
    actual_count=result.get('exact_assertions',result.get('assertions',result.get('exact_identities')));assert actual_count==count
    replays.append({'family':family,'program':program,'program_sha256':sha((D/program).read_bytes()),'exit':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr),'new_exact_controls':count,'complete_json_equal':True,'complete_output':result})
    families.append({'family':family,'public_manifest_sha256':sha((D/'PUBLIC_MANIFEST.json').read_bytes()),'bound_files':len(seen),'literal_scope_and_all_bindings_verified':True,'all_independence_seals_verified':True})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','families':families,'replays':replays,'new_controls_total':sum(r['new_exact_controls'] for r in replays),'finite_controls_replace_universal_proofs':False,'root_prior_brief_sibling_exposure_disclosed':True,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_family_control_reproduction.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','bound_family_files':sum(r['bound_files'] for r in families),'family_manifests':len(families),'new_controls':out['new_controls_total']},indent=2))
