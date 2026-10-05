#!/usr/bin/env python3
"""Keep native final full streams and metadata writable through preopened FDs."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(p.stat().st_mode&0o777)}
dest=R/'process_evidence/final_close';dest.mkdir(exist_ok=False)
for source,name in [(pathlib.Path(__file__),'executed_driver.py'),(R/'close_family.py','executed_child.py')]:
 (dest/name).write_bytes(source.read_bytes())
argv=[sys.executable,'-E','-B',str(R/'close_family.py')]
record={'label':'final_close','driver_actual_pid':os.getpid(),'driver_argv':sys.argv,'argv':argv,'cwd':str(R),'started_utc':now(),'driver_source_at_launch':pin(pathlib.Path(__file__)),'executed_driver':pin(dest/'executed_driver.py'),'child_source_at_launch':pin(R/'close_family.py'),'executed_child':pin(dest/'executed_child.py'),'actual_executable_at_launch':pin(pathlib.Path(sys.executable).resolve()),'python':sys.version,'mode_semantics':'Sources start0644, criteria already0444. Child seals all files0444 and dirs0555. Full child streams and metadata are completed through preopened file descriptors after that mode transition; no frozen modes are reopened or weakened.'}
(dest/'request.json').write_text(json.dumps(record,indent=2)+'\n')
with (dest/'stdout.bin').open('wb') as out,(dest/'stderr.bin').open('wb') as err,(dest/'execution.json').open('w') as meta:
 child=subprocess.Popen(argv,cwd=R,stdout=out,stderr=err);record['actual_pid']=child.pid;record['exit_code']=child.wait();record['ended_utc']=now();out.flush();err.flush();os.fsync(out.fileno());os.fsync(err.fileno())
 record['stdout']=pin(dest/'stdout.bin');record['stderr']=pin(dest/'stderr.bin')
 if (R/'OUTPUT_INVENTORY.json').is_file():record['output_inventory']=pin(R/'OUTPUT_INVENTORY.json')
 record['all_current_files0444_dirs0555']=all(p.stat().st_mode&0o777==0o444 for p in R.rglob('*') if p.is_file()) and all(p.stat().st_mode&0o777==0o555 for p in R.rglob('*') if p.is_dir()) and R.stat().st_mode&0o777==0o555
 meta.write(json.dumps(record,indent=2)+'\n');meta.flush();os.fsync(meta.fileno())
print(json.dumps({'actual_pid':child.pid,'exit_code':record['exit_code'],'metadata':str(dest/'execution.json'),'stdout_bytes':record['stdout']['bytes'],'stderr_bytes':record['stderr']['bytes'],'all_current_files0444_dirs0555':record['all_current_files0444_dirs0555']}))
sys.exit(record['exit_code'])
