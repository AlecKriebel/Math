"""Release only owned public PR364 source/proof/preprint preparation and PR365 receipt."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr364_30004048';B=P/'audits/pr365_2303002';paths=set();sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 rel=p.relative_to(P);assert not any(x=='private' or x.startswith('private_') or x in {'tmp','__pycache__','raw_sources','root_replay_private','root_primary_private'} for x in rel.parts[:-1]),rel
 assert p.suffix not in {'.png','.pdf','.zip'} or p.parent==A/'preprint' and p.name in {'biconstrained_asymmetry.pdf','biconstrained-asymmetry-verification.zip'}
 paths.add(str(p.relative_to(R)))
def directory(d):
 for p in d.rglob('*'):
  if p.is_file():add(p)
families=[]
for d,expected in [(A/'graph_boundary_review/public','f7f87c47b7604cfabc10110af936d29ccd41b6afe755bfd8a6502828d3889052'),(A/'polytope_duality_review','5c0032d82c71a8632668ad6ce56ce0414a2aa16f777421f038265e768a24c6e8'),(A/'priority_review','30d56fa9c4632d09e69d978ae61bbbf15cb27842e0319482379136ee3968fbbc')]:
 b=(d/'PUBLIC_MANIFEST.json').read_bytes();assert sha(b)==expected;m=json.loads(b);files=m.get('files',m.get('public_files'));files={e['path']:e for e in files} if isinstance(files,list) else files
 for n,e in files.items():
  q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts;v=(d/n).read_bytes();assert len(v)==e['bytes'] and sha(v)==e['sha256'];add(d/n)
 add(d/'PUBLIC_MANIFEST.json')
 if (d/'FINAL_SEAL.json').exists():add(d/'FINAL_SEAL.json')
 families.append({'namespace':str(d.relative_to(P)),'manifest_sha256':expected,'public_files':len(files)})
for p in A.iterdir():
 if p.is_file() and (p.suffix in {'.py','.md','.json'} or p.name=='.gitignore'):add(p)
directory(A/'snapshot');directory(A/'preprint/verification')
for n in ['biconstrained_asymmetry.tex','biconstrained_asymmetry.pdf','biconstrained-asymmetry-verification.zip','zenodo-deposit.json','INITIAL_REVIEW_PACKAGE.json','PREPARATION_QA.json','FINAL_PRE_REVIEW_QA.json','.gitignore']:add(A/'preprint'/n)
for n in ['GIT_PUBLICATION_RECEIPT.json','GIT_PUBLICATION_MISSING_DECLARED_ARTIFACTS.json','acceptance_criteria.json','CURRENT_ACCEPTANCE_STATUS.md','RESEARCH_LOG.md','root_record_publication.py']:add(B/n)
for n in ['inventory.json','RESEARCH_LOG.md',Path(__file__).name,'root_publish_365_final.py','checkpoint_365_final_publication_receipt.json','checkpoint_365_initial_incomplete_publication_receipt.json','checkpoint_365_corrective_stage.stdout','checkpoint_365_corrective_stage.stderr','checkpoint_365_corrective_commit.stdout','checkpoint_365_corrective_commit.stderr','checkpoint_365_corrective_push.stdout','checkpoint_365_corrective_push.stderr']:add(P/n)
assert git('branch','--show-current')==b'main\n';assert not git('diff','--name-only','--diff-filter=U');assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert subprocess.run(['git','merge-base','--is-ancestor','0bf23eb6754032c86352b6671fc61299b8a0250d','HEAD'],cwd=R).returncode==0
allow=P/'checkpoint_364_preprint_allowlist.json';paths.add(str(allow.relative_to(R)));allow.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicit_owned_paths':sorted(paths),'families':families,'stage':'Prepared preprint under first fresh review, no actual merge/Zenodo/tracker yet; PR365 final audit publication observed'},indent=2)+'\n')
def foreign():
 out={}
 for row in git('ls-files','--stage','-z').split(b'\0'):
  if row:
   meta,n=row.split(b'\t',1)
   if n.decode() not in paths:out.setdefault(n,[]).append(meta)
 return out
old=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,argv in [('stage',['git','add','-f','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish biconstrained boundary proof audits and preprint preparation','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 s=subprocess.run(argv,cwd=R,capture_output=True);(P/('checkpoint_364_preprint_'+label+'.stdout')).write_bytes(s.stdout);(P/('checkpoint_364_preprint_'+label+'.stderr')).write_bytes(s.stderr);assert s.returncode==0,(label,s.stderr);assert foreign()==old
C=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',C).decode().splitlines());assert changed<=paths
out={'status':'PUBLISHED_PR364_PREPRINT_PREPARATION_CHECKPOINT','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':C,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True,'families':families,'preprint_first_fresh_review_pending':True,'pr364_merge_zenodo_tracker_pending':True,'pr365_final_audit_observed':'0bf23eb6754032c86352b6671fc61299b8a0250d'}
(P/'checkpoint_364_preprint_publication_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
