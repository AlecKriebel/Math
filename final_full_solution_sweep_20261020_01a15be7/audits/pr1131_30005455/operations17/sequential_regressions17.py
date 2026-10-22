from pathlib import Path
import subprocess,sys,json,datetime,time,hashlib,os
P=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
need(not(P/'MANIFEST.json').exists(),'Closed packet')
# The focus process writes this receipt only after all its worlds have been
# archived/readback. No chunk writer overlaps another.
deadline=time.monotonic()+1800
while not(P/'private/final_phase17_normal/RESULT.json').exists():
 need(time.monotonic()<deadline,'Focus did not complete; no other cohort launched')
 time.sleep(1)
focus=json.loads((P/'private/final_phase17_normal/RESULT.json').read_bytes())
need(focus['case_count']==55 and all(r['status']=='PASS'for r in focus['results']),'Focus incomplete')
results=[]
for name in ['retention17.py','native_only17.py','retention_edges17.py','fact_edges17.py','fact_get_corrected17.py','baseline16_unicode17.py']:
 need(os.statvfs(P).f_bavail*os.statvfs(P).f_frsize>=150*1024*1024+1024*1024,'Actual free reserve before cohort')
 argv=[sys.executable,'-I','-S','-B',str(P/'run_case17.py'),name]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 child=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1800)
 log={'at':start,'argv':argv,'child_helper_sha256':sha((P/name).read_bytes()),'returncode':child.returncode,'stdout':child.stdout.decode('utf-8','backslashreplace'),'stderr':child.stderr.decode('utf-8','backslashreplace'),'actual_services':0}
 (P/'private'/('RUN_'+name+'.json')).write_text(json.dumps(log,indent=2)+'\n')
 results.append({k:v for k,v in log.items()if k not in {'stdout','stderr'}})
 print(name,child.returncode,flush=True)
 need(child.returncode==0,'Cohort failed; retained output, no further cohorts')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cohorts':results,'actual_effects':0,'publication_ready':False}
(P/'private/SEQUENTIAL_REGRESSION_DRIVER.json').write_text(json.dumps(out,indent=2)+'\n')
