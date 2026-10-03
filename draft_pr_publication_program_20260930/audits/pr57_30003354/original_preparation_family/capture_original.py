from capture_command import HERE,run
import json,sys
cap,out,err=run('retrieve_original',['/usr/bin/python3','-B',str(HERE/'retrieve_original.py')],sources=[HERE/'retrieve_original.py'])
print(json.dumps(cap,indent=2,sort_keys=True))
sys.exit(cap['exit_code'])
