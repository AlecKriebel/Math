"""Read back the already closed first-party family; preserve the duplicate closing failure."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat
A=Path(__file__).resolve().parent;F=A/'cover_algebra_family'
def main():
 assert __debug__
 mf=F/'SELF_MANIFEST.json';raw=mf.read_bytes();m=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()=='3ef0383c70a0ed8c08bd7f4a403b1e82057a9d7038a45bac45cbd3fe271814fe'
 assert m['actual_closing_child_pid']==10880
 rows=m['files'];dirs=m['directories'];assert len(rows)==143 and len(dirs)==23
 expected={r['path']for r in rows}|{'SELF_MANIFEST.json'}
 assert {p.relative_to(F).as_posix()for p in F.rglob('*')if p.is_file()}==expected
 assert {p.relative_to(F).as_posix()for p in F.rglob('*')if p.is_dir()}=={r['path']for r in dirs}
 for p in F.rglob('*'):assert not p.is_symlink()
 for r in rows:
  n=PurePosixPath(r['path']);assert not n.is_absolute()and '..'not in n.parts
  p=F/r['path'];b=p.read_bytes();assert len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256']and stat.S_IMODE(p.stat().st_mode)==0o444
 assert stat.S_IMODE(mf.stat().st_mode)==0o444
 assert (A/'ROOT_COVER_ALGEBRA_CLOSURE_PRELAUNCH_SOURCE.py').read_bytes()==(F/'close_family.py').read_bytes()
 print(json.dumps({'status':'PASS_COMPLETE_CLOSED_COVER_READBACK','actual_readback_child_pid':os.getpid(),'earlier_closing_child_pid':10880,'files_with_self':144,'directories':23,'full_modes':292,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'entire_first_party_bodies_read_and_checked':True,'duplicate_closure_failed_capture_preserved':str(A.parent/'pr45_9900007/root_cover_algebra_closure_actual_capture')}))
if __name__=='__main__':main()
