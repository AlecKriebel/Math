"""Read-only verification of the entire ROOT-closed boundary family."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,stat
F=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest-sha256',required=True);args=ap.parse_args()
 p=F/'MANIFEST.json';body=p.read_bytes()
 assert __debug__ and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o444 and sha(body)==args.expected_manifest_sha256
 m=json.loads(body);assert m['schema']=='pr49-boundary-independent-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json']
 assert m['future_acceptance_authority'] is False
 rows=[];dirs=[]
 for directory,names,files in os.walk(F,followlinks=False):
  d=Path(directory);assert not d.is_symlink() and stat.S_ISDIR(d.lstat().st_mode)
  dirs.append({'path':'.' if d==F else d.relative_to(F).as_posix(),'full_mode':stat.S_IMODE(d.lstat().st_mode)})
  for name in names:assert not (d/name).is_symlink() and stat.S_ISDIR((d/name).lstat().st_mode)
  for name in files:
   f=d/name;relative=f.relative_to(F).as_posix()
   if relative=='MANIFEST.json':continue
   st=f.lstat();assert stat.S_ISREG(st.st_mode) and not f.is_symlink() and st.st_nlink==1 and stat.S_IMODE(st.st_mode)==0o444
   b=f.read_bytes();rows.append({'path':relative,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(st.st_mode)})
 assert sorted(rows,key=lambda v:v['path'])==m['members'] and len(rows)==m['member_count']
 assert sorted(dirs,key=lambda v:v['path'])==m['directories'] and len(dirs)==m['directory_count']
 assert sha((F/'REPORT.md').read_bytes())==m['report_sha256']
 print(json.dumps({'status':'PASS_COMPLETE_CLOSED_BOUNDARY_FAMILY_READ_ONLY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_readback_pid':os.getpid(),'manifest_sha256':sha(body),'payload_members':len(rows),'total_files':len(rows)+1,'directories':len(dirs),'future_acceptance_authority':False},sort_keys=True))
if __name__=='__main__':main()
