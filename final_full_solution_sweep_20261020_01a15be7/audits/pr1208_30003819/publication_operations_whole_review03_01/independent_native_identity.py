"""Independent data-validation controls on exact PR1208 source; inert services only."""
from pathlib import Path
import base64,copy,datetime as dt,gzip,hashlib,http.client,json,os,shutil,socket,stat,subprocess,sys,urllib.request,zipfile
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/"publication_operations_whole_review03_01_actor"
OUT=ROOT/"private/physical"
SOURCE_SHA="4403a056d8cbd39ab06cf225cd0d294daaaa81a8e4318b970c77367826f6bd02"
BOOT_SHA="f1c9823ce373884b8f630e1ce405de3761eacb65f2ee480a710aeb0fe26bb2b0"
attempts=[]
def need(ok,message):
    if not ok:raise RuntimeError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def blobpin(b):return {"bytes":len(b),"sha256":digest(b)}
def blocked(*a,**kw):attempts.append("external interface");raise RuntimeError("No external interfaces allowed in review")
socket.socket=blocked;socket.create_connection=blocked;socket.getaddrinfo=blocked
http.client.HTTPConnection=blocked;http.client.HTTPSConnection=blocked;urllib.request.urlopen=blocked;urllib.request.OpenerDirector.open=blocked
subprocess.run=blocked;subprocess.Popen=blocked;os.system=blocked;os.popen=blocked
raw=(SOURCE/"bootstrap.py").read_bytes();need(digest(raw)==BOOT_SHA,"Bootstrap prehash")
ns={"__file__":str(SOURCE/"bootstrap.py"),"__name__":"independent_prehashed_bootstrap"}
exec(compile(raw,str(SOURCE/"bootstrap.py"),"exec",dont_inherit=True,optimize=0),ns)
load,_=ns["load_verified"](SOURCE,SOURCE_SHA,BOOT_SHA)
c=load("common");c.zenodo.token_for=blocked
models=load("models");runner=load("runner");fixture=models.inputs()
OUT.mkdir(parents=True,exist_ok=False)
def call(w,action):
    return runner.main([action,"--expected-pr-head",w.git.head],provider=w,test_adoption=w.adoption,test_journal=w.j)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def durable(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("xb")as f:f.write(canonical(v)+b"\n");f.flush();os.fsync(f.fileno())
    fd=os.open(p.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
seed=models.World(fixture)
for action in ["integrate","describe","ready","merge"]:call(seed,action)
class PhysicalJournal(c.Journal):
    def __init__(self,*a,**kw):self.after=None;super().__init__(*a,**kw)
    def write(self,key,value):
        super().write(key,value)
        if self.after is not None:self.after(self,key)
def transport_identity(legacy,native,files):
    """Correct inherited unused historical record links in BOTH controls."""
    record=str(native["id"]);parent=str(native["parent"]["id"])
    def replace(value):
        if type(value)is str:
            for old in ["23224103","21753316"]:value=value.replace(old,record)
            for old in ["23224102","21753315"]:value=value.replace(old,parent)
            return value
        if type(value)is dict:return {k:replace(v)for k,v in value.items()}
        if type(value)is list:return [replace(v)for v in value]
        return value
    native["links"]=replace(native["links"])
    native["links"]["self"]="https://zenodo.org/api/records/"+record+(""if native["is_published"]else"/draft")
records=[];custody=[]
def pack(case):
    entries=[];directories=[]
    for p in [case]+sorted(case.rglob("*")):
        s=p.lstat();rel="."if p==case else str(p.relative_to(case))
        need(not p.is_symlink(),"Unexpected symlink")
        m={"path":rel,"mode":stat.S_IMODE(s.st_mode),"mtime_ns":s.st_mtime_ns}
        if p.is_dir():directories.append(m)
        else:b=p.read_bytes();entries.append({**m,**blobpin(b)})
    archive=OUT/(case.name+".zip")
    with zipfile.ZipFile(archive,"x",compression=zipfile.ZIP_DEFLATED)as z:
        for x in entries:z.writestr(x["path"],(case/x["path"]).read_bytes())
    with archive.open("rb")as f:os.fsync(f.fileno())
    with zipfile.ZipFile(archive)as z:
        need(z.testzip()is None and set(z.namelist())=={x["path"]for x in entries},"Archive closure/CRC")
        for x in entries:need(blobpin(z.read(x["path"]))=={"bytes":x["bytes"],"sha256":x["sha256"]},"Archive member")
    manifest={"case":case.name,"archive":archive.name,"archive_pin":blobpin(archive.read_bytes()),"entries":entries,"directories":directories,"all_bytes_read_before_retirement":True,"forensic_archive_not_operational_CASE":True,"original_inodes_not_restored":True}
    mp=OUT/(case.name+".manifest.json");durable(mp,manifest);custody.append({"manifest":str(mp.relative_to(ROOT)),"pin":blobpin(mp.read_bytes()),"files":len(entries),"directories":len(directories)})
    shutil.rmtree(case)
for name in ["positive_current_target_links","late_native_self_identity_contradiction"]:
    need(shutil.disk_usage(ROOT).free>=64*1024*1024,"Review reserve")
    case=OUT/name;case.mkdir()
    w=seed.clone();events=list(w.j.events.items());w.physical_state_path=case/"SIMULATED_CANONICAL_STATE.json"
    def relocate(value):
        if type(value)is str:return str(w.physical_state_path)if value=="/SIMULATED_STATE_ONLY"else value
        if type(value)is dict:return {k:relocate(v)for k,v in value.items()}
        if type(value)is list:return [relocate(v)for v in value]
        return value
    w.j=PhysicalJournal(case/"SIMULATED_ONLY_JOURNAL",{"simulation_only":True,"production_CASE":False,"pr":1208,"source_sha256":SOURCE_SHA,"case":name})
    for key,value in events:w.j.write(key,relocate(value))
    fired=[];observed=[]
    def native_fault(l,n,f):
        transport_identity(l,n,f)
        if fired:
            expected=n["links"]["self"];n["links"]["self"]="https://zenodo.org/api/records/999"+(""if n["is_published"]else"/draft")
            observed.append({"published":n["is_published"],"record":n["id"],"concept":n["parent"]["id"],"correct_self":expected,"observed_self":n["links"]["self"]})
    w.native.fault=native_fault
    call(w,"stage")
    if name.startswith("late"):
        def after(j,key):
            if key=="ZENODO_PUBLISH_INTENT"and not fired:
                raw=(j.path/(key+".json")).read_bytes();fired.append({"after_real_file_and_directory_fsync_and_seal":True,"intent_pin":blobpin(raw)})
        w.j.after=after
    before=len(w.native.calls)
    try:
        answer=call(w,"publish")
        if name.startswith("positive"):
            row=call(w,"ledger");need(row["verified"]is True and w.row_writes==1,"Full positive row")
        error=None
    except Exception as e:answer=None;error=type(e).__name__+": "+str(e)
    certified=(w.j.path/"PUBLISH_VERIFIED.json").exists()
    result={"case":name,"answer":answer,"error":error,"post_intent_hook":fired,"native_observations":observed,"fake_native_calls":w.native.calls,"publish_delta":len(w.native.calls)-before,"fake_rows":w.row_writes,"PUBLISH_VERIFIED":certified,"shared_installs":w.state_saves,"private_publication_receipts":w.state_receipts,"real_external_attempts":list(attempts),"actual_fsynced_Journal":True,"source_guards_unchanged":True,"expected":"success"if name.startswith("positive")else"reject-before-publish-for-self-identity-contradiction"}
    if name.startswith("positive"):
        need(error is None and certified and w.native.calls.count("publish")==1,"Positive control")
        reopened=c.Journal(w.j.path,c.strict_json(w.j.header_raw));reopened.verify();result["physical_restart_integrity_passed"]=True
    else:
        need(bool(fired),"Late condition did not run")
        result["verdict"]="COUNTEREXAMPLE"if answer is not None and certified and w.native.calls.count("publish")==1 else"REJECTED"
    durable(case/"RESULT.json",result);records.append(result);pack(case)
need(not attempts,"Real interface attempted")
report={"at":dt.datetime.now(dt.timezone.utc).isoformat(),"source_manifest_sha256":SOURCE_SHA,"bootstrap_sha256":BOOT_SHA,"actual_parser_cases":len(records),"results":records,"custody":custody,"real_external_attempts":attempts,"real_service_mutations":0,"root_action_authority":False,"original_source_unchanged":True}
durable(ROOT/"PHYSICAL_RESULTS.json",report)
print(json.dumps({"cases":[{"case":x["case"],"error":x["error"],"PUBLISH_VERIFIED":x["PUBLISH_VERIFIED"],"native_calls":x["fake_native_calls"],"verdict":x.get("verdict","POSITIVE_PASS")}for x in records],"real_external_attempts":attempts,"custody_files":sum(x["files"]for x in custody)},indent=2))
