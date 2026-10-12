"""Publish exact owned PR369 acceptance and PR368 frozen audit; preserve foreign index."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr369_2302055';B=P/'audits/pr368_30004320';paths=set()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def add(f):
 assert f.is_file() and not f.is_symlink();f=f.resolve();assert f.is_relative_to(P)
 assert not any(x in ['tmp','private','raw_sources','private_sources','__pycache__','freeze_routing_failure'] or x.startswith('private_') for x in f.parts)
 assert f.suffix not in ['.pdf','.png','.html','.jpg','.jpeg']
 assert f.suffix!='.txt' or f.name in ['accepted_pr_body.txt','merge_body.txt']
 paths.add(f.relative_to(R).as_posix())
def mf(D,count):
 obj=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
 for e in obj['files']:
  p=PurePosixPath(e['path']);assert not p.is_absolute() and '..' not in p.parts and str(p)==e['path'] and e['path'] not in seen and e['path']!='PUBLIC_MANIFEST.json';seen.add(e['path']);b=(D/p).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(D/p)
 assert len(seen)==count;add(D/'PUBLIC_MANIFEST.json')
def snapshot(D,name,folder,count):
 m=json.loads((D/name).read_bytes());assert len(m['files'])==count
 for e in m['files']:
  f=D/folder/e['path'];b=f.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(f)
 add(D/name)
assert git('branch','--show-current').strip()==b'main';assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U').strip()
merge=json.loads((A/'ACTUAL_MERGE_VERIFICATION.json').read_bytes());assert merge['actual_merge']=='feec7623f289284c33d685f101342fc74502c819' and merge['all_expected_paths_exact']==50 and merge['all_target_file_hashes_exact']==49 and merge['status']=='unsolved'
compare=json.loads((A/'root_final_live_comparison.json').read_bytes());assert compare['status']=='PASS_ENTIRE_FINAL_LIVE_RECEIPTS' and compare['complete_equal_checks']==929 and compare['root_separate_checks']==1715 and compare['stream_pairs_count']==154
mf(A/'clean_final_adversary/final_live',18);mf(A/'clean_final_adversary/final_live/runs/root_20261003_exact_live_01',4)
snapshot(A,'repaired_snapshot_manifest.json','repaired_snapshot',50)
old=A/'queue_refresh_history/b6de823369765d321a1781032f7e08a557b21fea';snapshot(old,'repaired_snapshot_manifest.json','repaired_snapshot',50)
for name in ['queue_repair_receipt.json','root_exact_live_receipt.json']:add(old/name)
for name in ['root_exact_live_gate.py','root_exact_live_receipt.json','root_compare_final_live.py','root_final_live_comparison.json','ROOT_LIVE_FAILURES.json','queue_repair_receipt.json','ACTUAL_MERGE_VERIFICATION.json','ACCEPTANCE_DECISION.md','virtual_integration_receipt.json','DECISION.md','README.md','RESEARCH_LOG.md','acceptance_criteria.json']:add(A/name)
snapshot(B,'snapshot_manifest.json','snapshot',54)
for family,count in [('descent_cohomology_review',35),('residue_valuation_review',37),('clean_final_adversary',47)]:mf(B/family,count)
a=json.loads((B/'root_original_reproduction_receipt.json').read_bytes());c=json.loads((B/'root_family_control_reproduction.json').read_bytes());assert a['status']==c['status']=='PASS' and a['check_count']==501 and c['check_count']==3310 and all(e['pass'] for e in a['checks']+c['checks'])
assert a['nested_binding_instances']==130 and a['author_assertions']==128694 and a['historical_review_assertions']==8664 and c['new_controls_total']==13339 and c['negative_controls_replayed']==14
for seal in ['ROOT_SOURCE_FIRST_SEAL.json','ROOT_MATHEMATICAL_SEAL.json']:
 e=json.loads((B/seal).read_bytes());b=(B/e['file']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
for e in a['replays']:
 for stream in ['stdout','stderr']:
  f=B/'root_original_streams'/(e['label']+'.'+stream);b=f.read_bytes();assert len(b)==e[stream+'_bytes'] and sha(b)==e[stream+'_sha256'];add(f)
for e in c['families']:
 for stream in ['stdout','stderr']:
  f=B/'root_family_control_streams'/(e['family']+'.'+stream);b=f.read_bytes();assert (len(b)==e['control_stdout_bytes'] and sha(b)==e['control_stdout_sha256']) if stream=='stdout' else b==b'';add(f)
 for stream in ['stdout','stderr']:add(B/'root_family_control_streams'/(e['family']+'_manifest.'+stream))
for name in ['drift.stdout','drift.stderr','drift_failed_01.stdout','drift_failed_01.stderr']:add(B/'root_family_control_streams'/name)
for name in ['.gitignore','remote_original.json','README.md','RESEARCH_LOG.md','ROOT_SOURCE_FIRST_BASELINE.md','ROOT_SOURCE_FIRST_SEAL.json','ROOT_MATHEMATICAL_RECONSTRUCTION.md','ROOT_MATHEMATICAL_SEAL.json','root_fetch_primary.py','root_primary_fetch_receipt.json','root_fetch_supplemental.py','root_supplemental_fetch_receipt.json','root_reproduce_frozen_packet.py','root_original_reproduction_receipt.json','root_reproduce_family_controls.py','root_family_control_reproduction.json','ROOT_CONTROL_REPLAY_FAILURES.json','DECISION.md','accepted_pr_body.txt','merge_body.txt','acceptance_criteria.json']:add(B/name)
for name in ['inventory.json','RESEARCH_LOG.md',Path(__file__).name,'root_integrate_reviewed_pr.py']:add(P/name)
allow=P/'checkpoint_369_acceptance_368_math_public_allowlist.json';paths.add(allow.relative_to(R).as_posix());allow.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicit_owned_paths':sorted(paths),'excluded':'All unlisted paths, raw primary copies/private streams/runtimes and every foreign index entry'},indent=2)+'\n')
def foreign_index():
 out={}
 for row in git('ls-files','--stage','-z').split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1)
   if path.decode() not in paths:out.setdefault(path,[]).append(meta)
 return out
foreign=foreign_index();parent=git('rev-parse','HEAD').decode().strip();assert parent=='feec7623f289284c33d685f101342fc74502c819'
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish PR369 verified partial acceptance and PR368 adversarial mathematical audit','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0,'foreign merge became active'
 r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_369_acceptance_368_math_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_369_acceptance_368_math_'+label+'.stderr')).write_bytes(r.stderr);assert not r.returncode,(label,r.stderr);assert foreign_index()==foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_369_ACCEPTANCE_368_MATH80','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True},indent=2))
