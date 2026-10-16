"""Publish completed partial audits and a clearly pending preprint checkpoint.

Only exact owned paths are selected; every foreign staged entry is preserved.
The new second reviewer remains outside this checkpoint until its seal exists.
"""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;paths=set()
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def add(p):
    assert p.is_file() and not p.is_symlink()
    p=p.resolve();assert p.is_relative_to(P)
    parts=p.relative_to(P).parts
    assert not any(x in {'tmp','raw_sources','private','private_runs','__pycache__','freeze_routing_failure'} or 'private' in x for x in parts)
    assert p.suffix not in {'.png','.jpg','.jpeg','.html','.ps'}
    assert p.suffix!='.pdf' or parts[-2:] == ('preprint','fixed_generator_classification.pdf')
    paths.add(p.relative_to(R).as_posix())
def manifest(d,name,count):
    m=json.loads((d/name).read_bytes());seen=set()
    for row in m['files']:
        q=PurePosixPath(row['path']);assert not q.is_absolute() and '..' not in q.parts and q.as_posix()==row['path'] and row['path'] not in seen
        seen.add(row['path']);p=d/q;b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];add(p)
    assert len(seen)==count;add(d/name)
def immediate(d):
    for p in d.iterdir():
        if p.is_file():add(p)
def directory(d):
    for p in d.rglob('*'):
        if p.is_file():add(p)
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U').strip()
for pr,count,streams in [('pr369_2302055',19,174),('pr368_30004320',60,1484)]:
    a=P/'audits'/pr;j=json.loads((a/'root_postmerge_receipt.json').read_bytes())
    assert j['workflow_completion_percent']==100 and j['accepted_status']=='unsolved' and j['original_problem_resolution_percent']==0 and j['paper_zenodo_doi_tracker_release'] is False
    assert j.get('complete_unique_stream_pairs_verified',j.get('all1484_full_stream_pairs_verified')) == (streams if streams==174 else True)
    immediate(a);manifest(a/'clean_final_adversary/post_merge','PUBLIC_MANIFEST.json',count)
    if pr.startswith('pr368'):
        manifest(a/'clean_final_adversary/final_live','PUBLIC_MANIFEST.json',1635)
        directory(a/'repaired_snapshot')
    else:manifest(a/'clean_final_adversary/final_live/runs/root_post_merge_20261003_01','PUBLIC_MANIFEST.json',4) if (a/'clean_final_adversary/final_live/runs/root_post_merge_20261003_01/PUBLIC_MANIFEST.json').exists() else None
a=P/'audits/pr367_11000151';immediate(a);directory(a/'snapshot')
for family,count in [('group_presentations_review',40),('mapping_class_geometry_review',52),('clean_final_adversary',127)]:
    manifest(a/family,'PUBLIC_MANIFEST.json',count)
    if (a/family/'FINAL_SEAL.json').exists():add(a/family/'FINAL_SEAL.json')
manifest(a/'priority_audit','IMMUTABLE_MANIFEST.json',8)
manifest(a/'preprint_review_01','IMMUTABLE_MANIFEST.json',14)
for d in a.glob('root_*streams*'):
    if d.is_dir():directory(d)
d=a/'preprint';manifest(d/'verification','MANIFEST.json',58)
for name in ['fixed_generator_classification.tex','fixed_generator_classification.pdf','wajnryb-artin-a5-verification.zip','zenodo-deposit.json','INITIAL_REVIEW_PACKAGE.json','REPAIRED_REVIEW_PACKAGE_02.json','REPAIR_LOG.md','PREPARATION_FAILURES.json','.gitignore']:add(d/name)
j=json.loads((d/'REPAIRED_REVIEW_PACKAGE_02.json').read_bytes());assert j['workflow_completion_percent']==75 and j['zip_members']==60 and j['package_verification_exit_code']==0
for row in j['sealed_files']:
    b=(d/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
for name in ['root_original_reproduction_receipt.json','root_family_reproduction_receipt.json']:
    j=json.loads((a/name).read_bytes());assert j['status']=='PASS' and j['check_count']==(857 if name.startswith('root_original') else 652)
for name in ['inventory.json','RESEARCH_LOG.md','ROOT_PRIVATE_STORAGE_GZIP_20261003_1353.json','ROOT_PRIVATE_DEDUP_20261003_1435.json','ROOT_PRIVATE_DEDUP_20261003_1455.json',Path(__file__).name]:add(P/name)
allow=P/'checkpoint_369_368_final_367_preprint_public_allowlist.json';paths.add(allow.relative_to(R).as_posix())
allow.write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'scope':'PR369/368 completed unsolved partial audits; PR367 repaired preprint75%, second fresh reviewer pending. No deposit or solved merge.','explicit_owned_paths':sorted(paths),'excluded':'Every unlisted path, private runs/raw primary copies, incomplete second reviewer and foreign index entries'},indent=2)+'\n')
def foreign_index():
    result={}
    for row in git('ls-files','--stage','-z').split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1)
            if path.decode() not in paths:result.setdefault(path,[]).append(meta)
    return result
foreign=foreign_index();parent=git('rev-parse','HEAD').decode().strip();assert parent=='2da0adc1c56dbb15e53be162489eb001cfa83e03'
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish final PR369/368 partial audits and repaired PR367 preprint checkpoint','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
    r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_369_368_final_367_preprint_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_369_368_final_367_preprint_'+label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0,(label,r.stderr);assert foreign_index()==foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_FINAL_PARTIAL_AUDITS_AND_PREPRINT75','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True},indent=2))
