from pathlib import Path
import datetime,hashlib,json,os,signal,subprocess,time,stat
A=Path(__file__).resolve().parent;K=A/"publication_package_v2";D=A/"preprint_export_v4_20261008"
def pin(p):
 b=p.read_bytes();return {"bytes":len(b),"mode":stat.S_IMODE(p.stat().st_mode),"sha256":hashlib.sha256(b).hexdigest()}
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def dump(p,j):
 with p.open("x") as f:json.dump(j,f,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
D.mkdir();(D/"raw").mkdir();source=pin(K/"k107_counterexample.tex");processes=[]
def run(role,argv):
 j={"UTC_start":now(),"argv":argv,"role":role};dump(D/"raw"/(role+"_START.json"),j)
 p=subprocess.Popen(argv,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 failure=None
 try:o,e=p.communicate(timeout=45)
 except BaseException as exc:
  failure=type(exc).__name__;os.killpg(p.pid,signal.SIGKILL);o,e=p.communicate(timeout=5)
 try:os.killpg(p.pid,0);empty=False
 except ProcessLookupError:empty=True
 if not empty:raise RuntimeError("owned subprocess group still present")
 for n,b in (("stdout",o),("stderr",e)):
  f=D/"raw"/(role+"_"+n+".bin");f.write_bytes(b);j[n]=pin(f)
 j.update(PID=p.pid,UTC_end=now(),exit_code=p.returncode,reaped=p.returncode is not None,group_absent=empty,failure=failure)
 dump(D/"raw"/(role+"_EXECUTION.json"),j);processes.append(j)
 if failure or p.returncode:raise RuntimeError("export subprocess failed "+role)
 return o
run("compile",["/opt/homebrew/Cellar/tectonic/0.16.9/bin/tectonic","--only-cached","--untrusted","--keep-logs","--outdir",str(K),str(K/"k107_counterexample.tex")])
info=run("pdfinfo",["/opt/homebrew/bin/pdfinfo",str(K/"k107_counterexample.pdf")]).decode()
run("extract",["/opt/homebrew/bin/pdftotext","-layout",str(K/"k107_counterexample.pdf"),str(D/"EXTRACTED.txt")])
run("render",["/opt/homebrew/bin/pdftoppm","-r","110","-png",str(K/"k107_counterexample.pdf"),str(D/"page")])
if pin(K/"k107_counterexample.tex")!=source:raise RuntimeError("source changed during export")
log=K/"k107_counterexample.log";log.rename(D/"EXPORTED_COMPILE_LOG.txt")
dump(D/"RECEIPT.json",{"status":"PASS_ACTUAL_CACHED_EXPORT_AND_ALL_PAGE_RENDER","UTC":now(),"actual_ROOT_PID":os.getpid(),"source":source,"PDF":pin(K/"k107_counterexample.pdf"),"info":info,"processes":processes,"page_images":[{"path":p.name,**pin(p)} for p in sorted(D.glob("page-*.png"))],"source_unchanged":True,"visual_QA_pending":True})
print(json.dumps({"status":"EXPORTED_ALL_PAGES","PDF":pin(K/"k107_counterexample.pdf"),"pages":len(list(D.glob("page-*.png"))),"receipt":str(D/"RECEIPT.json")}))

