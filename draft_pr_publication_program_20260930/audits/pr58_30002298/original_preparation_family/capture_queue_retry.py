from capture_command import HERE,run
import json,sys
cap,out,err=run("queue_authentication_retry",["/usr/bin/python3","-B",str(HERE/"authenticate_queue_retry.py")],sources=[HERE/"authenticate_queue_retry.py"])
print(json.dumps({"child_pid":cap["child_pid"],"exit_code":cap["exit_code"],"stdout_bytes":len(out),"stderr_bytes":len(err)}));sys.exit(cap["exit_code"])
