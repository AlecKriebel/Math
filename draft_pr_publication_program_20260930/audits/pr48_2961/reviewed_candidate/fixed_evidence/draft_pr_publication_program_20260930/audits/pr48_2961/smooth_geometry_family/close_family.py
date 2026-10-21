import pathlib, json, hashlib, stat, datetime, os, sys
assert __debug__
r=pathlib.Path(__file__).resolve().parent
assert str(r)=='/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr48_2961/smooth_geometry_family'
assert len(sys.argv)==2 and len(sys.argv[1])==64
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((r/'REPORT.md').read_bytes())==sys.argv[1]
assert not (r/'MANIFEST.json').exists()
assert not (r/'tmp').exists()
v=json.loads((r/'VERDICT.json').read_bytes())
assert v['open_problem_outcome']=='unsolved' and v['mathematical_partial']=='PASS'
assert v['new_substantive_turns']==v['audit_turn_charge']==0
assert json.loads((r/'FINAL_READBACK_AND_TRANSIENT_REMOVAL.json').read_bytes())['foreign_bodies_remaining'] is False
files=[];directories=[{'path':'.','full_mode':stat.S_IMODE(r.lstat().st_mode)}]
for p in sorted(r.rglob('*')):
 s=p.lstat();assert not p.is_symlink()
 if stat.S_ISDIR(s.st_mode):
  assert p.name not in {'tmp','__pycache__'}
  directories.append({'path':str(p.relative_to(r)),'full_mode':stat.S_IMODE(s.st_mode)});continue
 assert stat.S_ISREG(s.st_mode)
 assert p.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.webp'}
 b=p.read_bytes();assert not b.startswith(b'%PDF')
 files.append({'path':str(p.relative_to(r)),'bytes':len(b),'sha256':sha(b),'full_mode':0o444})
assert files and len({x['path'] for x in files})==len(files)
m={'schema':'pr48-smooth-geometry-family-closure-manifest/v1','root':str(r),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'self_excluded':True,'files_count':len(files),'files':files,'owned_directories_count':len(directories),'owned_directories':directories,'original_manifest_sha256':'278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4','original_head':'e2e5c8c3e5ad218f867fa753c465bb96b3687bda','report_sha256':sys.argv[1],'foreign_transients_present':False,'open_problem_outcome':'unsolved','new_substantive_turns':0,'audit_turn_charge':0,'root_actual_capture_external':True,'promotion_or_merge_claim':False}
for row in files:
 p=r/row['path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];p.chmod(0o444)
mf=r/'MANIFEST.json'
with mf.open('xb') as f:f.write((json.dumps(m,indent=2)+'\n').encode())
mf.chmod(0o444)
import verify_family_readonly
print(json.dumps(verify_family_readonly.verify(),indent=2))
