import os,json
from pathlib import Path
p=Path(__file__).parent
found=[]
for r in sorted((p/'runs').glob('*/receipt.json')):
 m=json.loads(r.read_text());pid=m['actual_child_PID']
 try:os.kill(pid,0);state='PID_exists'
 except ProcessLookupError:state='gone'
 except PermissionError:state='PID_exists_without_permission'
 found.append({'label':m['label'],'actual_child_PID':pid,'state':state})
if any(r['state']!='gone' for r in found):raise RuntimeError('Some previously controlled child PIDs still exist; inspect rather than assume completion.')
print(json.dumps({'status':'CLOSED','observed_completed_runs':len(found),'children':found},indent=2))
