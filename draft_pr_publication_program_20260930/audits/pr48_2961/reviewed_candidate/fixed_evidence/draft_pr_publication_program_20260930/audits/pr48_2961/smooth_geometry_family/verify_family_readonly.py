import pathlib, json, hashlib, stat, datetime, os
assert __debug__
ROOT=pathlib.Path(__file__).resolve().parent
def verify():
 mf=ROOT/'MANIFEST.json';assert not mf.is_symlink() and stat.S_IMODE(mf.stat().st_mode)==0o444
 m=json.loads(mf.read_bytes());assert m['self_excluded'] is True and m['root']==str(ROOT)
 expected={row['path']:row for row in m['files']};assert len(expected)==m['files_count']
 actual=set();dirs={'.':stat.S_IMODE(ROOT.lstat().st_mode)}
 for p in sorted(ROOT.rglob('*')):
  s=p.lstat();assert not p.is_symlink()
  if stat.S_ISDIR(s.st_mode):dirs[str(p.relative_to(ROOT))]=stat.S_IMODE(s.st_mode);continue
  assert stat.S_ISREG(s.st_mode)
  rel=str(p.relative_to(ROOT));actual.add(rel)
  if rel=='MANIFEST.json':continue
  row=expected[rel];b=p.read_bytes()
  assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
  assert stat.S_IMODE(s.st_mode)==row['full_mode']==0o444
 assert actual==set(expected)|{'MANIFEST.json'}
 wanted={row['path']:row['full_mode'] for row in m['owned_directories']}
 assert dirs==wanted and len(wanted)==m['owned_directories_count']
 assert not any(p.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.webp'} for p in ROOT.rglob('*') if p.is_file())
 assert not (ROOT/'tmp').exists() and not any(p.name=='__pycache__' for p in ROOT.rglob('*'))
 v=json.loads((ROOT/'VERDICT.json').read_bytes())
 assert v['open_problem_outcome']=='unsolved' and v['mathematical_partial']=='PASS'
 assert v['new_substantive_turns']==v['audit_turn_charge']==0
 return {'schema':'pr48-smooth-geometry-family-read-only-verifier/v1','status':'PASS','actual_pid':os.getpid(),'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':hashlib.sha256(mf.read_bytes()).hexdigest(),'payload_files':len(expected),'files_including_manifest':len(actual),'owned_directories':len(dirs),'all_files_full0444':True,'exact_owned_topology':True,'foreign_transients_present':False,'new_substantive_turns':0,'audit_turn_charge':0,'promotion_claim':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
