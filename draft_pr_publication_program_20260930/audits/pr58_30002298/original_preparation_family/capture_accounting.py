from capture_command import HERE,run
import json,sys
cap,out,err=run("source_accounting",["/usr/bin/python3","-B",str(HERE/"select_source_accounting.py")],sources=[HERE/"select_source_accounting.py",HERE/"original/source_record.json",HERE/"original/readiness.json",HERE/"original/turns.jsonl"])
print(json.dumps({"child_pid":cap["child_pid"],"exit_code":cap["exit_code"],"stdout_bytes":len(out),"stderr_bytes":len(err)}));sys.exit(cap["exit_code"])
