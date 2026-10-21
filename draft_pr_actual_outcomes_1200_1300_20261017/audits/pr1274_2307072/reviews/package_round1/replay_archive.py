from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, stat, subprocess, sys, zipfile
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/"publication";L=R/"own_local";target=L/"archive"
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
build=json.loads((P/"BUILD_RECEIPT.json").read_text());archive=P/build["verification_zip"]["path"]
entries=[]
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    if len(names)!=194 or len(set(names))!=len(names):raise RuntimeError("ZIP duplicate/member count")
    for info in z.infolist():
        raw=info.filename;rel=PurePosixPath(raw)
        if rel.is_absolute() or ".." in rel.parts or "\\" in raw or str(rel)!=raw or stat.S_ISLNK(info.external_attr>>16):raise RuntimeError("Unsafe ZIP entry")
        data=z.read(raw);local=P/"verification"/raw
        if data!=local.read_bytes():raise RuntimeError("ZIP/local bytes differ "+raw)
        dest=target/raw;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        entries.append({"path":raw,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
results=[]
for flags in [[],["-O"],["-OO"]]:
    args=[arg for key,value in build["verification_anchors"].items() for arg in ["--expected-"+key+"-sha256",value]]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(L));env.pop("PYTHONOPTIMIZE",None)
    run=subprocess.run([sys.executable,"-B",*flags,str(target/"verify.py"),*args],cwd=L,env=env,capture_output=True,text=True,timeout=180)
    (L/("archive_verify"+str(len(flags))+('OO' if flags==['-OO'] else '')+".stdout")).write_text(run.stdout)
    if run.returncode:raise RuntimeError(run.stderr)
    results.append({"flags":flags,"returncode":run.returncode,"result":json.loads(run.stdout)})
result={"schema":"math-pr1274-review-archive-replay-v1","started_at_utc":start,"completed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"zip_sha256":digest(archive),"member_count":len(entries),"all_current_zip_members_match":True,"outside_anchors":build["verification_anchors"],"all_modes_identical":all(e["result"]==results[0]["result"] for e in results),"runs":results,"limits":"Authenticity to supplied outside anchors and finite diagnostics only; separate written mathematical and source review required."}
(R/"ARCHIVE_REPLAY.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps({k:v for k,v in result.items() if k!="runs"}))
