from capture_command import HERE,run
import json,sys
cap,out,err=run('source_accounting_corrected',['/usr/bin/python3','-B',str(HERE/'select_source_accounting_v2.py')],sources=[HERE/'select_source_accounting_v2.py',HERE/'original/source_record.json'])
print(json.dumps(cap,indent=2,sort_keys=True));sys.exit(cap['exit_code'])
