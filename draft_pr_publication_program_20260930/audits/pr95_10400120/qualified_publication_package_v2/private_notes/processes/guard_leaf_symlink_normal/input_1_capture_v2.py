from pathlib import Path
import datetime,hashlib,json,os,platform,shutil,subprocess,sys,time
N=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def capture(label,argv,cwd,inputs,expected=0):
    root=N/"processes"/label;root.mkdir(parents=True)
    snapshots=[]
    for p in inputs:
        p=Path(p);target=root/("input_"+str(len(snapshots))+"_"+p.name)
        shutil.copyfile(p,target);snapshots.append({"origin":str(p),"snapshot":target.name,"sha256":sha(target),"bytes":target.stat().st_size})
    record={"schema":"pr95-v2-repair-process/v1","label":label,"argv":argv,"cwd":str(cwd),"recorder_pid":os.getpid(),"started_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"inputs":snapshots,
            "environment":{"python":platform.python_version(),"implementation":platform.python_implementation(),"PYTHON_variables_removed":sorted(k for k in os.environ if k.startswith("PYTHON")),"LC_ALL":"C"}}
    env={k:v for k,v in os.environ.items() if not k.startswith("PYTHON")};env["LC_ALL"]="C"
    start=time.monotonic()
    with (root/"stdout.bin").open("wb") as o,(root/"stderr.bin").open("wb") as e:
        child=subprocess.Popen(argv,cwd=cwd,env=env,stdout=o,stderr=e);record["pid"]=child.pid;dump(root/"process.json",record);code=child.wait()
    record.update(exit_code=code,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start)
    for name in ("stdout.bin","stderr.bin"):
        p=root/name;record[name]={"sha256":sha(p),"bytes":p.stat().st_size}
    dump(root/"process.json",record)
    if code!=expected:raise RuntimeError(label+" unexpected exit "+str(code))
    return record
if __name__=="__main__":
    P=N.parent;F=P/"publicfiles"
    r=capture("assembly",[sys.executable,"-E","-B",str(F/"verification/run_all.py"),"--output-dir",str(N/"assembled_run")],F,[F/"verification/run_all.py",F/"PAYLOAD_MANIFEST.json",F/"pr95_note.tex"])
    print(json.dumps({"assembly_exit":r["exit_code"]}))
