from capture_command import HERE,run
import json,sys
cap,out,err=run("preparation_check",["/usr/bin/python3","-B",str(HERE/"verify_preparation.py")],sources=[HERE/"verify_preparation.py",HERE/"packet_common.py"])
print(json.dumps({"child_pid":cap["child_pid"],"exit_code":cap["exit_code"],"stdout_bytes":len(out),"stderr_bytes":len(err)}));sys.exit(cap["exit_code"])
