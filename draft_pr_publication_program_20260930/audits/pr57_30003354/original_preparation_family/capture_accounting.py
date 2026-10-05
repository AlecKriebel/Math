from capture_command import HERE,run
import json,sys
cap,out,err=run('source_accounting',['/usr/bin/python3','-B',str(HERE/'select_source_accounting.py')],sources=[HERE/'select_source_accounting.py',HERE/'original/source_record.json'])
print(json.dumps(cap,indent=2,sort_keys=True));sys.exit(cap['exit_code'])
