"""Publish explicit owned PR370 mathematical and reproducibility checkpoint."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr370_30004811';paths=set()
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0,'shared main has an active merge; leave it untouched'
assert not subprocess.check_output(['git','diff','--name-only','--diff-filter=U'],cwd=R).strip(),'shared main has unmerged paths; leave them untouched'
def sha(b):return hashlib.sha256(b).hexdigest()
def add(f):
    f=f.resolve();assert f.is_relative_to(P) and f.is_file() and not f.is_symlink()
    assert not {'private','tmp','raw_sources','__pycache__'}.intersection(f.parts) and f.suffix not in ('.pdf','.png','.html')
    assert f.suffix!='.txt' or f in {A/'accepted_pr_body.txt',A/'merge_body.txt'}
    paths.add(f.relative_to(R).as_posix())
for family in ['asymptotic_normalization_review','priority_hypotheses_review','clean_final_adversary']:
    D=A/family;m=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
    for e in m['files']:
        p=PurePosixPath(e['path']);assert len(p.parts)==1 and '..' not in p.parts and e['path'] not in seen and e['path']!='PUBLIC_MANIFEST.json';seen.add(e['path'])
        b=(D/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(D/e['path'])
    add(D/'PUBLIC_MANIFEST.json')
original=json.loads((A/'root_original_reproduction_receipt.json').read_bytes());controls=json.loads((A/'root_family_control_reproduction.json').read_bytes())
assert original['status']=='PASS' and len(original['checks'])==135 and all(r['passed'] for r in original['checks']) and original['binding_count']==29
assert controls['status']=='PASS' and controls['new_controls_total']==48 and sum(f['bound_files'] for f in controls['families'])==51
for receipt,directory in [(original,'root_original_streams'),(controls,'root_family_control_streams')]:
    for row in receipt['replays']:
        label=row.get('label',row.get('family'));assert row['exit']==0 and row['stderr_bytes']==0
        for stream in ['stdout','stderr']:
            f=A/directory/(label+'.'+stream);b=f.read_bytes();assert len(b)==row[stream+'_bytes'] and sha(b)==row[stream+'_sha256'];add(f)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
c={'pr':370,'problem_id':30004811,'original_head':'567c2e493854b32d0cd325ad96e4c5b69c9c1e1b','accepted_status':'already_solved','author_turns':'1/5','workflow_completion_percent':80,'credited_original_class_resolution_percent':100,'novel_original_problem_resolution_claimed':False,'all18_original_target_artifacts_unchanged':True,'root_frozen_checks':135,'nested_manifest_bindings':29,'seven_historical_primary_pdf_identities_reproduced':True,'three_independent_source_first_math_reviews_pass_scoped':True,'root_earlier_brief_sibling_exposure_disclosed':True,'root_full_independence_from_sibling_findings_claimed':False,'exact_global_mass_verified':False,'historical_novelty_verified':False,'exact_live_root_and_whole_gates_pending':True,'actual_merge_pending':True,'body_sha256':sha((A/'accepted_pr_body.txt').read_bytes()),'no_paper_zenodo_doi_tracker_release':True}
(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_bytes());next(x for x in inv['items'] if x['number']==370).update(audit_workflow_percent=80,audit_completion_percent=80,audit_disposition='SCOPED_CREDITED_RESOLUTION_AND_COUNTEREXAMPLE_PASS_EXACT_LIVE_PENDING',credited_original_class_resolution_percent=100,novel_original_problem_resolution_claimed=False)
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=f'\n{now}: PR370 source/proof/code/history checkpoint80%; scoped already_solved1/5. Root135 frozen checks,19 actual remote/Git files,18 unchanged target artifacts,29 nested bindings,7 exact historical PDF identities,10 author-checkpoint files. Author5529 and prior3128 complete outputs reproduce across source-present/absent contracts; three independent sealed families51 bound files and48 new controls pass. Physical equality credited100%; new physical theorem0%, exact global negative-example mass/novelty unverified. Root brief sibling exposure disclosed. Fresh live gates/current-main queue repair/actual merge pending. Program18/349=5.1576%; no paper/DOI.\n'
for f in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with f.open('a') as h:h.write(entry)
for n in ['root_reproduce_frozen_packet.py','root_original_reproduction_receipt.json','root_reproduce_family_controls.py','root_family_control_reproduction.json','DECISION.md','merge_body.txt','ROOT_CHECKPOINT_FAILURES.md','acceptance_criteria.json','RESEARCH_LOG.md']:add(A/n)
add(A/'accepted_pr_body.txt')
for n in ['root_refresh_queue.py','root_integrate_reviewed_pr.py','inventory.json','RESEARCH_LOG.md',Path(__file__).name]:add(P/n)
allow=P/'checkpoint_370_math_public_allowlist.json';paths.add(allow.relative_to(R).as_posix());allow.write_text(json.dumps({'utc':now,'explicit_owned_paths':sorted(paths),'excluded':'All unlisted paths, raw primary sources, private copies/API streams and foreign index entries'},indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def foreign_index():
    out={}
    for row in git('ls-files','--stage','-z').split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1)
            if path.decode() not in paths:out.setdefault(path,[]).append(meta)
    return out
assert git('branch','--show-current').strip()==b'main';foreign=foreign_index();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish scoped adversarial audit of PR370 capacity-volume mass','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_370_math_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_370_math_'+label+'.stderr')).write_bytes(r.stderr);assert r.returncode==0,(label,r.stderr)
    assert foreign_index()==foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_PR370_MATH80','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True},indent=2))
