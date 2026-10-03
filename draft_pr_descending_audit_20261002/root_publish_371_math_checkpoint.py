"""Publish an explicit owned PR371 source/proof/reproduction checkpoint on main."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr371_30006025';paths=set();verified=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def add(f):
    f=f.resolve();assert f.is_relative_to(P) and f.is_file() and not f.is_symlink()
    assert not {'tmp','private','raw_sources','private_sources','private_replays','__pycache__'}.intersection(f.parts)
    assert f.suffix not in ('.pdf','.png','.jpg','.html')
    paths.add(f.relative_to(R).as_posix())
for family in ['combinatorial_metric_review','hyperbolic_arithmetic_review','surface_surgery_review','clean_final_adversary']:
    root=A/family;manifest=root/'PUBLIC_MANIFEST.json';m=json.loads(manifest.read_bytes());seen=set()
    for row in m['files']:
        rel=PurePosixPath(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
        assert rel.as_posix()==row['path'] and row['path'] not in seen and row['path']!='PUBLIC_MANIFEST.json';seen.add(row['path'])
        f=root/row['path'];raw=f.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
        if 'git_blob_sha1' in row:assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob_sha1']
        add(f)
    add(manifest);verified.append({'family':family,'manifest_sha256':sha(manifest.read_bytes()),'bound_files':len(seen),'all_literal_bindings_verified':True})
base=json.loads((A/'root_source_first_seal.json').read_bytes());math=json.loads((A/'root_mathematical_reconstruction_seal.json').read_bytes())
assert sha((A/'ROOT_SOURCE_FIRST_BASELINE.md').read_bytes())==base['sha256']
assert sha((A/'ROOT_MATHEMATICAL_RECONSTRUCTION.md').read_bytes())==math['math_sha256'] and base['utc']<math['utc']
original=json.loads((A/'root_original_reproduction_receipt.json').read_bytes())
assert all(r['pass'] for r in original['checks']) and len(original['checks'])==255 and original['binding_instance_count']==113
for row in original['replays']:
    assert row['exit_code']==0 and row['stderr_bytes']==0
    for stream in ['stdout','stderr']:
        f=A/'root_original_streams'/(row['label']+'.'+stream);raw=f.read_bytes()
        assert len(raw)==row[stream+'_bytes'] and sha(raw)==row[stream+'_sha256'];add(f)
controls=json.loads((A/'root_family_control_reproduction.json').read_bytes());assert controls['status']=='PASS' and len(controls['replays'])==4
for row in controls['replays']:
    assert row['exit']==0 and row['stderr_bytes']==0 and row['all_mathematical_and_scope_fields_equal']
    for stream in ['stdout','stderr']:
        f=A/'root_family_control_streams'/(row['family']+'.'+stream);raw=f.read_bytes()
        assert len(raw)==row[stream+'_bytes'] and sha(raw)==row[stream+'_sha256'];add(f)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(A/'root_completed_family_manifest_verification.json').write_text(json.dumps({'utc':now,'status':'PASS','families':verified,'root_seals_verified':True,'root_frozen_checks':255,'new_control_assertions':controls['new_control_assertions'],'historical_all27_source_bytes_recertified':False},indent=2)+'\n')
criteria={'pr':371,'problem_id':30006025,'original_head':'51fddd150e8da33f4cf17b1a642a0ffd3466bf5d','workflow_completion_percent':80,'general_discovery_completion_percent':0,'accepted_status':'unsolved','author_turns':'5/5','all_46_original_target_files_preserved':True,'all_original_math_outputs_and_public_manifests_reproduced':True,'historical_all27_private_source_assets_recertified':False,'four_independent_source_first_math_reviews_pass_scoped':True,'root_source_first_math_reconstruction_pass_scoped':True,'exact_live_root_and_whole_gates_pending':True,'actual_merge_pending':True,'body_sha256':sha((A/'accepted_pr_body.txt').read_bytes()),'no_paper_zenodo_doi_tracker_release':True}
(A/'acceptance_criteria.json').write_text(json.dumps(criteria,indent=2)+'\n')
inventory=json.loads((P/'inventory.json').read_bytes());item=next(x for x in inventory['items'] if x['number']==371)
item.update(audit_workflow_percent=80,audit_completion_percent=80,audit_disposition='SCOPED_MATH_AND_REPRODUCTION_PASS_EXACT_LIVE_PENDING',general_discovery_completion_percent=0,source_first_seal='root_source_first_seal.json')
old=next(x for x in inventory['items'] if x['number']==372);old.update(audit_completion_percent=100,audit_disposition='ACCEPTED_ACTUAL_MERGE_AND_POSTMERGE_VERIFIED')
(P/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
entry=f'\n{now}: PR371 source/proof/code/history checkpoint80%; root255 frozen checks,113 manifest instances, all46 mathematical artifacts intact. Author15618 and prior24692 outputs reproduce fully; four independent source-first families plus new977848 finite controls pass. Strongest intrinsic perimeter/sparse-repair scope valid; original Question4 resolution0%,unsolved5/5. Root9/10 primary PDF identities,10/27 historical bindings; whole11/27 including its matching raster. No all27 or global novelty certification. Exact-live gates/merge pending. Program17/349=4.8711%.\n'
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with f.open('a') as h:h.write(entry)
for name in ['ROOT_SOURCE_FIRST_BASELINE.md','ROOT_MATHEMATICAL_RECONSTRUCTION.md','root_source_first_seal.json','root_mathematical_reconstruction_seal.json','root_reproduce_frozen_packet.py','root_original_reproduction_receipt.json','root_reproduce_family_controls.py','root_family_control_reproduction.json','root_recheck_source_provenance.py','root_source_provenance_recheck.json','root_completed_family_manifest_verification.json','DECISION.md','accepted_pr_body.txt','merge_body.txt','acceptance_criteria.json','RESEARCH_LOG.md']:
    add(A/name)
for name in ['inventory.json','RESEARCH_LOG.md',Path(__file__).name]:add(P/name)
allow=P/'checkpoint_371_math_public_allowlist.json';paths.add(allow.relative_to(R).as_posix())
allow.write_text(json.dumps({'utc':now,'checkpoint':'PR371 source/proof/reproduction80%, exact-live pending','explicit_owned_paths':sorted(paths),'exclusions':'Every unlisted path, raw source asset, private Git/API/execution copy and foreign index entry','completed_prs':17,'total_initial_drafts':349,'original_problem_resolution_percent':0},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def indexmap():
    out={}
    for row in git('ls-files','--stage','-z').split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);out.setdefault(path,[]).append(meta)
    return {k:v for k,v in out.items() if k.decode() not in paths}
assert git('branch','--show-current').strip()==b'main';foreign=indexmap();parent=git('rev-parse','HEAD').decode().strip()
for tag,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish source-first adversarial audit of PR371 geometric partials','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_371_math_'+tag+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_371_math_'+tag+'.stderr')).write_bytes(r.stderr);assert r.returncode==0,(tag,r.stderr)
    assert indexmap()==foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_SCOPED_PR371_AUDIT80','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_unchanged':True},indent=2))
