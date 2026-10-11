from capture_command import HERE,run
import json,sys
cap,out,err=run('helper_orchestration',['/usr/bin/python3','-B',str(HERE/'reproduce_helpers.py')],sources=[HERE/'reproduce_helpers.py'])
print(json.dumps(cap,indent=2,sort_keys=True));sys.exit(cap['exit_code'])
