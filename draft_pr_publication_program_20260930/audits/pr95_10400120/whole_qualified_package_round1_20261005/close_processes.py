from pathlib import Path
import json,os,datetime,subprocess
A=Path(__file__).resolve().parent;rows=[];pids=set()
for root in [A/'processes',A/'fresh_reproduction']:
 for f in root.rglob('process.json'):
  d=json.loads(f.read_text());pid=d.get('child_pid',d.get('pid'));pids.add(pid)
  if d.get('exit_code') is None:raise RuntimeError('unfinished receipt '+str(f))
for pid in sorted(pids):
 p=subprocess.run(['ps','-p',str(pid),'-o','pid=,command='],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 rows.append({'pid':pid,'ps_exit':p.returncode,'live_process':p.stdout.decode().strip()})
 if p.stdout.strip():raise RuntimeError('controlled PID remains live/reused: '+str(pid))
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_probe_pid':os.getpid(),'prior_unique_controlled_children':len(pids),'all_prior_processes_terminated':True,'rows':rows,'closure_probe':'The probe process itself subsequently receives its own captured exit0 receipt.'}
(A/'PROCESS_CLOSURE.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['prior_unique_controlled_children','all_prior_processes_terminated']}))
