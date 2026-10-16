from pathlib import Path
import subprocess,sys,json,os
R=Path(__file__).resolve().parent
rows=[]
for name in ["REPRODUCE.py","DEEP_CONTROLS.py","STREAM_CONTROLS.py"]:
 label=name.removesuffix(".py")
 with (R/("ROOT_"+label+".stdout")).open("xb") as out,(R/("ROOT_"+label+".stderr")).open("xb") as err:
  p=subprocess.run([sys.executable,"-B",str(R/name)],cwd=R,stdout=out,stderr=err)
 print("ACTUAL_"+label+"_EXIT",p.returncode,flush=True)
 rows.append({"program":name,"actual_child_exit":p.returncode})
 with (R/"ROOT_PROGRAM_EXITS.json").open("w") as f:json.dump(rows,f,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
 if p.returncode:raise SystemExit(p.returncode)
