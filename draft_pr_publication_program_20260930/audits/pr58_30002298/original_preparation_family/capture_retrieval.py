from capture_command import HERE,run
import json,sys
cap,out,err=run("retrieval_operator",["/usr/bin/python3","-B",str(HERE/"retrieve_original.py")],sources=[HERE/"retrieve_original.py"])
print(json.dumps({"child_pid":cap["child_pid"],"exit_code":cap["exit_code"],"stdout_bytes":len(out),"stderr_bytes":len(err)}))
sys.exit(cap["exit_code"])
