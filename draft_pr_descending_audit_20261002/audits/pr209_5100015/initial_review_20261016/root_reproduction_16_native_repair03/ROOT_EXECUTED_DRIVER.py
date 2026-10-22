from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
for label,program in [("receipt124","receipt_controls.py"),("r03","R03_regression.py")]:
 with (R/("ROOT_"+label+".stdout")).open("xb") as out,(R/("ROOT_"+label+".stderr")).open("xb") as err:
  p=subprocess.run([sys.executable,"-B",str(R/program)],cwd=R,stdout=out,stderr=err)
 print("ACTUAL_"+label+"_EXIT",p.returncode,flush=True)
 (R/("ROOT_"+label+"_EXIT.json")).write_text(json.dumps({"actual_child_exit":p.returncode})+"\n")
 if p.returncode:raise SystemExit(p.returncode)
