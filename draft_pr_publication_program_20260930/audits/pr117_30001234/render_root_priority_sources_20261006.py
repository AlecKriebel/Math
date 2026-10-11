from pathlib import Path
import subprocess,hashlib,json,os,datetime
A=Path(__file__).resolve().parent
D=A/"root_priority_audit_20261006"; S=D/"private_sources"; R=D/"private_renders";R.mkdir(exist_ok=True)
events=[]
for name,page in [("yuen_math_0608632v1",8),("yuen_math_0608632v1",10),("teitler_software_2015_publisher",7),("miller_singh_varbaro_2014_author",2)]:
 prefix=R/(name+"_physical_p"+str(page))
 argv=["/opt/homebrew/bin/pdftoppm","-f",str(page),"-l",str(page),"-r","240","-singlefile","-png",str(S/(name+".pdf")),str(prefix)]
 p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(timeout=60)
 if p.returncode:raise ValueError("Rendering failed")
 path=prefix.with_suffix(".png");b=path.read_bytes()
 events.append({"argv":argv,"actual_child_PID":p.pid,"exit_code":p.returncode,"stderr_bytes":len(err),"render_path":str(path.relative_to(D)),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"root_visual_inspection_pending_at_render":True,"private_excluded":True})
record={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"actual_operator_PID":os.getpid(),"events":events}
(D/"ROOT_PRIVATE_RENDER_RECEIPT.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
print(json.dumps(record,indent=2))

