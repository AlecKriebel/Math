from pathlib import Path
import subprocess,os,signal,time,hashlib,json,shutil,datetime
b=Path(__file__).resolve().parent
src=b.parents[1]/'sources/support'
kit=b/'runs/kit_copy'
shutil.copytree(src,kit)
checks=[('supplied_kit',['/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python','-I','-B',str(kit/'scripts/verify_kit.py'),'--archive',str(src.parent/'pr1032_supportkit_v1.1.zip')],150),('independent_reconstruction',['/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python','-I','-B',str(b/'independent_reconstruction.py')],150)]
receipts=[]
for name,cmd,timeout in checks:
 start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.Popen(cmd,cwd=b/'runs',stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 timedout=False
 try:out,err=p.communicate(timeout=timeout)
 except subprocess.TimeoutExpired:
  timedout=True;os.killpg(p.pid,signal.SIGTERM)
  try:out,err=p.communicate(timeout=3)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate()
 # Descendants cannot outlive successful parent check under these read programs;
 # defensive process-group kill if any remain after parent completion.
 try:os.killpg(p.pid,signal.SIGTERM);cleanup='remaining_group_TERMed'
 except ProcessLookupError:cleanup='process_group_absent'
 (b/'runs'/f'{name}.stdout.json').write_bytes(out)
 (b/'runs'/f'{name}.stderr.txt').write_bytes(err)
 receipts.append({'name':name,'command':cmd,'started_utc':utc,'elapsed_seconds':time.monotonic()-start,'returncode':p.returncode,'timed_out':timedout,'timeout_seconds':timeout,'descendant_cleanup':cleanup,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()})
(b/'runs/RUN_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps(receipts,indent=2))
