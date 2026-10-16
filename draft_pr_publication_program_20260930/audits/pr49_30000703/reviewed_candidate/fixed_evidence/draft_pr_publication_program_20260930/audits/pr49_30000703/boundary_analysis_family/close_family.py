"""ROOT-only self-manifest closer; never supplies future acceptance authority."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,stat
F=Path(__file__).resolve().parent
MANIFEST='MANIFEST.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def scan():
 rows=[];dirs=[]
 for directory,names,files in os.walk(F,followlinks=False):
  d=Path(directory);assert not d.is_symlink() and stat.S_ISDIR(d.lstat().st_mode)
  dirs.append({'path':'.' if d==F else d.relative_to(F).as_posix(),'full_mode':stat.S_IMODE(d.lstat().st_mode)})
  for name in names:
   p=d/name;assert not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode)
  for name in files:
   p=d/name;relative=p.relative_to(F).as_posix()
   if relative==MANIFEST:continue
   st=p.lstat();assert stat.S_ISREG(st.st_mode) and not p.is_symlink() and st.st_nlink==1
   assert p.suffix.lower() not in ['.pdf','.png','.jpg','.jpeg','.sqlite','.db']
   b=p.read_bytes();rows.append({'path':relative,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(st.st_mode)})
 return sorted(rows,key=lambda v:v['path']),sorted(dirs,key=lambda v:v['path'])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-report-sha256',required=True);args=ap.parse_args()
 assert __debug__ and not (F/MANIFEST).exists()
 assert sha((F/'REPORT.md').read_bytes())==args.expected_report_sha256
 v=json.loads((F/'VERDICT.json').read_bytes())
 assert v['verdict']=='PASS_CREDITED_KNOWN_UNRESTRICTED_REFLECTION_CRITERION'
 assert v['mandatory_corrections']==[] and v['recommended_status']=='already_solved'
 assert v['report_sha256']==args.expected_report_sha256 and v['proof_sha256']==sha((F/'BOUNDARY_PROOF.md').read_bytes())
 assert v['original_substantive_turns']==0 and v['new_substantive_turns']==0
 assert v['original_closed_family_validation_complete'] is True
 assert v['future_acceptance_authority'] is False and v['project_solved'] is False and v['new_result'] is False
 assert json.loads((F/'TRANSIENT_PRIMARY_REMOVAL.json').read_bytes())['all_foreign_bodies_removed'] is True
 val=json.loads((F/'ORIGINAL_CLOSED_VALIDATION.json').read_bytes())
 assert val['all_original_manifest_members_read_in_full'] is True and val['complete_actual_original_capture_validation'] is True
 assert val['original_manifest']['sha256']==v['original_manifest_sha256']
 assert val['closure_chronology_verified'] is True and val['future_acceptance_authority'] is False
 before,dirs=scan()
 for row in before:os.chmod(F/row['path'],0o444)
 rows,dirs=scan();assert rows and all(row['full_mode']==0o444 for row in rows)
 record={'schema':'pr49-boundary-independent-self-only-closure/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'family':str(F),'self_excluded':[MANIFEST],'members':rows,'member_count':len(rows),'directories':dirs,'directory_count':len(dirs),'all_payload_full_modes':0o444,'foreign_bodies_copied':False,'future_acceptance_authority':False,'external_post_exit_readback_required':True,'report_sha256':args.expected_report_sha256}
 body=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
 with (F/MANIFEST).open('xb') as stream:stream.write(body);stream.flush();os.fsync(stream.fileno())
 os.chmod(F/MANIFEST,0o444)
 actual,actual_dirs=scan();assert actual==rows and actual_dirs==dirs and (F/MANIFEST).read_bytes()==body
 print(json.dumps({'manifest_sha256':sha(body),'payload_members':len(rows),'total_files':len(rows)+1,'directories':len(dirs),'future_acceptance_authority':False,'actual_closing_pid':os.getpid()},sort_keys=True))
if __name__=='__main__':main()
