from capture_command import HERE,run
import json,sys
cap,out,err=run("helper_orchestration",["/usr/bin/python3","-B",str(HERE/"reproduce_helpers.py")],sources=[HERE/"reproduce_helpers.py"])
print(json.dumps({"child_pid":cap["child_pid"],"exit_code":cap["exit_code"],"stdout_bytes":len(out),"stderr_bytes":len(err)}));sys.exit(cap["exit_code"])
