"""Publish explicit owned acceptance/review files while preserving foreign index entries."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, subprocess
P=Path(__file__).resolve().parent; R=P.parent
A=P/'audits/pr370_30004811'; B=P/'audits/pr369_2302055'; paths=set()
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U').strip()
def add(f):
    assert f.is_file() and not f.is_symlink(); f=f.resolve()
    assert f.is_relative_to(P)
    assert not any(k in {'tmp','private','raw_sources','private_sources','__pycache__'} or k.startswith('private_') for k in f.parts)
    assert f.suffix not in ('.pdf','.png','.html','.jpg')
    assert f.suffix!='.txt' or f.name in {'accepted_pr_body.txt','merge_body.txt'}
    paths.add(f.relative_to(R).as_posix())
def manifest(D):
    m=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes()); seen=set()
    for row in m['files']:
        p=PurePosixPath(row['path']); assert not p.is_absolute() and '..' not in p.parts and row['path'] not in seen
        assert row['path']!='PUBLIC_MANIFEST.json'; seen.add(row['path'])
        b=(D/p).read_bytes(); assert len(b)==row['bytes'] and sha(b)==row['sha256']
        if 'git_blob_sha1' in row: assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
        add(D/p)
    add(D/'PUBLIC_MANIFEST.json'); return len(seen)
def snapshot(D,name,folder,count):
    m=json.loads((D/name).read_bytes()); assert len(m['files'])==count
    for row in m['files']:
        f=D/folder/row['path']; b=f.read_bytes(); assert len(b)==row['bytes'] and sha(b)==row['sha256']; add(f)
    add(D/name)
assert manifest(A/'clean_final_adversary/final_live')==9
post_count=manifest(A/'clean_final_adversary/post_merge')
assert post_count>=5
actual=json.loads((A/'ACTUAL_MERGE_VERIFICATION.json').read_bytes())
assert actual['actual_merge']=='a765b9d3d9c5adbf8d123055b64fccb7887fe948' and actual['workflow_percent']==100
post=json.loads((A/'root_postmerge_comparison.json').read_bytes()); assert post['status']=='PASS'
snapshot(A,'repaired_snapshot_manifest.json','repaired_snapshot',19)
snapshot(B,'snapshot_manifest.json','snapshot',50)
assert sum(manifest(B/f) for f in ['function_theory_review','geometric_hypotheses_review','clean_final_adversary'])==53
assert manifest(B/'function_theory_review/provenance_appendix')==5
clar=json.loads((B/'ROOT_PROVENANCE_CLARIFICATION_RECEIPT.json').read_bytes())
assert clar['status']=='PASS_ADDITIVE_PROVENANCE_CLARIFICATION' and not clar['supplemental_full_source_read_before_math_seal']
for f in ['ROOT_SOURCE_FIRST_SEAL.json','ROOT_MATHEMATICAL_SEAL.json']:
    s=json.loads((B/f).read_bytes()); raw=(B/s['file']).read_bytes()
    assert len(raw)==s['bytes'] and sha(raw)==s['sha256']
    assert not s['substantive_sibling_conclusions_read_before_seal']
original=json.loads((B/'root_original_reproduction_receipt.json').read_bytes())
controls=json.loads((B/'root_family_control_reproduction.json').read_bytes())
assert original['status']=='PASS' and len(original['checks'])==672 and all(r['pass'] for r in original['checks'])
assert original['nested_binding_instances']==211 and original['author_assertions']==38066 and original['historical_review_assertions']==1420
assert controls['status']=='PASS' and len(controls['checks'])==206 and all(r['pass'] for r in controls['checks']) and controls['new_controls_total']==1262
for receipt,directory in [(original,'root_original_streams'),(controls,'root_family_control_streams')]:
    for row in receipt['replays']:
        label=row.get('label',row.get('family')); assert row['exit']==0 and row['stderr_bytes']==0
        for stream in ['stdout','stderr']:
            f=B/directory/(label+'.'+stream); b=f.read_bytes()
            assert len(b)==row[stream+'_bytes'] and sha(b)==row[stream+'_sha256']; add(f)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
c=json.loads((A/'acceptance_criteria.json').read_bytes())
c.update(workflow_completion_percent=100,postmerge_review_pending=False,postmerge_independent_checks=post['checks'],postmerge_root_replay_checks=post['checks'],postmerge_complete_receipts_verified=True)
(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_bytes())
next(x for x in inv['items'] if x['number']==370).update(audit_completion_percent=100,audit_workflow_percent=100,audit_disposition='ACCEPTED_ACTUAL_MERGE_AND_POSTMERGE_VERIFIED',credited_original_class_resolution_percent=100,novel_original_solution_claimed=False)
next(x for x in inv['items'] if x['number']==369).update(audit_completion_percent=80,audit_workflow_percent=80,audit_disposition='SCOPED_PARTIAL_MATH_AND_REPRODUCTION_PASS_EXACT_LIVE_PENDING',general_discovery_completion_percent=0)
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=f'\n{now}: PR370 final acceptance100% at actual a765b9d3; separate root615 and whole134/root134 exact-live checks, complete receipts with individually validated runtime leaves and repository metadata; independent/root postmerge {post["checks"]} checks. All18 mathematical targets and29 bindings preserved; full queue only owncells8/9, already_solved1/5, credited original resolution100%, no novel solution claim. PR369 math/reproduction80%, original resolution0%: source-first root seals and three independently sealed families53 files, root672 frozen checks/211bindings/five author checkpoints/38066 author+1420 historical controls, root206 family binding checks+1262 new controls, five fresh primary identities. Supplemental Picard full-source-after-seal chronology clarified additively and verified. Source/novelty and general-resolution gaps explicit. Program19/349=5.4441%; no paper/Zenodo/DOI/tracker/release for either partial.\n'
for f in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'README.md']:
    with f.open('a') as h:h.write(entry)
with (A/'DECISION.md').open('a') as h:h.write('\n## Actual acceptance and publication\n'+entry)
for n in ['root_exact_live_gate.py','root_exact_live_receipt.json','root_compare_final_live.py','root_final_live_comparison.json','root_final_live_replay.stdout','root_final_live_replay.stderr','root_final_live_replay_02.stdout','root_final_live_replay_02.stderr','root_compare_postmerge.py','root_postmerge_receipt.json','root_postmerge_comparison.json','queue_repair_receipt.json','ACTUAL_MERGE_VERIFICATION.json','ACCEPTANCE_DECISION.md','virtual_integration_receipt.json','DECISION.md','README.md','RESEARCH_LOG.md','ROOT_CHECKPOINT_FAILURES.md','acceptance_criteria.json']:add(A/n)
for n in ['RECEIPT_root_replay_01.json','RECEIPT_root_replay_02.json']:add(A/'clean_final_adversary/final_live'/n)
for n in ['.gitignore','remote_original.json','README.md','RESEARCH_LOG.md','ROOT_SOURCE_FIRST_BASELINE.md','ROOT_SOURCE_FIRST_SEAL.json','ROOT_MATHEMATICAL_RECONSTRUCTION.md','ROOT_MATHEMATICAL_SEAL.json','root_fetch_primary.py','root_primary_fetch_receipt.json','root_reproduce_frozen_packet.py','root_original_reproduction_receipt.json','root_reproduce_family_controls.py','root_family_control_reproduction.json','ROOT_PROVENANCE_CLARIFICATION_RECEIPT.json','ROOT_PREVIEW_CLEANUP_RECEIPT.json','DECISION.md','accepted_pr_body.txt','merge_body.txt','acceptance_criteria.json']:add(B/n)
for n in ['inventory.json','RESEARCH_LOG.md','ROOT_PRIVATE_STORAGE_CLEANUP_20261003_1240.json',Path(__file__).name]:add(P/n)
allow=P/'checkpoint_370_final_369_math_public_allowlist.json'; paths.add(allow.relative_to(R).as_posix())
allow.write_text(json.dumps({'utc':now,'explicit_owned_paths':sorted(paths),'excluded':'Every unlisted path, primary source copy/private stream/runtime and all foreign index entries'},indent=2)+'\n')
def foreign_index():
    out={}
    for row in git('ls-files','--stage','-z').split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1)
            if path.decode() not in paths:out.setdefault(path,[]).append(meta)
    return out
assert git('branch','--show-current').strip()==b'main'; foreign=foreign_index(); parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish PR370 actual acceptance and PR369 rigorous partial-result audit','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_370_final_369_math_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_370_final_369_math_'+label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0,(label,r.stderr);assert foreign_index()==foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_370_FINAL_369_MATH80','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True},indent=2))
