"""Reproduce all exact PR147 diagnostic families in fresh owned directories.

POSIX, Python3.11+, and SymPy1.14.0 for the library families. Nothing is
installed. A pre-existing output directory is never overwritten.
"""
from pathlib import Path
import argparse, ast, datetime, hashlib, json, os, shutil, signal, stat, subprocess, sys
HERE=Path(__file__).resolve().parent
FAMILIES=[
 ("author_exact","stdlib","author/verify.py",None),
 ("inherited_independent","library","inherited/independent_checks.py","independent_results.json"),
 ("fresh_rational","stdlib","fresh/independent_rational_certificate.py","RATIONAL_CERTIFICATE.json"),
 ("polynomial","library","fresh/independent_polynomial_identities.py","POLYNOMIAL_IDENTITIES.json"),
 ("nonsymmetric","library","fresh/independent_nonsymmetric_certificate.py","NONSYMMETRIC_CERTIFICATE.json")]
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def safe_regular(path):
 s=path.lstat()
 need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,"regular single-link file required: "+str(path))
 return path.read_bytes()
def run(argv,cwd,raw,receipt,expected=0):
 entry={"argv":argv,"UTC_start":utc()};receipt["children"].append(entry)
 child=None;out=b"";err=b""
 try:
  child=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,start_new_session=True)
  entry["PID"]=child.pid
  out,err=child.communicate(timeout=120)
 except BaseException as exc:
  entry["exception"]=type(exc).__name__
  if child is None:
   entry.update(child_reaped=False,process_group_empty=False,constructor_outcome_unknown=True)
  else:
   try:os.killpg(child.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   out,err=child.communicate(timeout=5)
  raise
 finally:
  if child is not None:
   try:os.killpg(child.pid,0);empty=False
   except ProcessLookupError:empty=True
   if not empty:
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    child.wait(timeout=5)
    try:os.killpg(child.pid,0);empty=False
    except ProcessLookupError:empty=True
   entry.update(exit_code=child.returncode,child_reaped=child.returncode is not None,
                process_group_empty=empty,UTC_end=utc())
   raw.mkdir(exist_ok=False)
   for label,body in [("stdout",out),("stderr",err)]:
    p=raw/(label+".bin");p.write_bytes(body)
    entry[label]={"path":str(p),"bytes":len(body),"sha256":sha(body)}
  (Path(receipt["output_directory"])/"REPRODUCTION_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
 need(entry.get("child_reaped") and entry.get("process_group_empty"),"child custody not closed")
 need(child.returncode==expected,"unexpected child result; see full raw output")
 return out
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--stdlib-python",required=True)
 parser.add_argument("--library-python",required=True)
 parser.add_argument("--output-directory",required=True)
 args=parser.parse_args()
 need(os.name=="posix","runner requires POSIX process groups")
 output=Path(args.output_directory).absolute()
 for p in [output,*output.parents]:need(not p.is_symlink(),"output symlink")
 package=HERE.parent
 need(output!=package and package not in output.parents,"output must be outside publication package")
 need(not output.exists(),"output directory already exists; use a fresh path")
 for p in [HERE,*HERE.parents]:need(not p.is_symlink(),"source path symlink")
 manifest=json.loads(safe_regular(HERE/"SOURCE_MANIFEST.json"))
 for m in manifest["members"]:
  rel=Path(m["path"])
  need(not rel.is_absolute() and ".." not in rel.parts,"noncanonical source member")
  p=HERE/rel
  for q in [p,*p.parents]:need(not q.is_symlink(),"source member symlink")
  b=safe_regular(p)
  need(len(b)==m["bytes"] and sha(b)==m["sha256"],"source pin mismatch: "+str(rel))
 python={"stdlib":args.stdlib_python,"library":args.library_python}
 for p in python.values():need(Path(p).is_absolute() and Path(p).is_file(),"absolute existing interpreter path required")
 output.mkdir(parents=True,exist_ok=False)
 receipt={"status":"RUNNING","actual_supervisor_PID":os.getpid(),"UTC_start":utc(),
          "source_manifest_sha256":sha((HERE/"SOURCE_MANIFEST.json").read_bytes()),
          "output_directory":str(output),"families":[],"guards":[],"children":[],
          "limitations":["Diagnostics do not replace the manuscript's analytic proof.",
                         "No historical priority or formal proof-assistant certificate."]}
 try:
  for kind in ["stdlib","library"]:
   code="import sys,json;"+("import sympy;" if kind=="library" else "")+"print(json.dumps({'python':sys.version,"+("'sympy':sympy.__version__" if kind=="library" else "'stdlib_only':True")+"}))"
   flags=["-E","-B","-P"]+(["-S"] if kind=="stdlib" else [])
   out=run([python[kind],*flags,"-c",code],output,output/("runtime_"+kind),receipt)
   runtime=json.loads(out);need(tuple(map(int,runtime["python"].split()[0].split(".")[:2]))>=(3,11),"Python3.11+ required")
   if kind=="library":need(runtime["sympy"]=="1.14.0","recorded baselines require SymPy1.14.0")
   receipt[kind+"_runtime"]=runtime
  for name,kind,rel,result_name in FAMILIES:
   observed=[]
   for optimized in [False,True]:
    label=name+("_optimized" if optimized else "_normal")
    stage=output/label;stage.mkdir()
    # Copy the declared immutable source history to fresh writable run files.
    shutil.copytree(HERE/"source",stage/"source")
    script=stage/"source"/rel
    flags=["-E","-B","-P"]+(["-S"] if kind=="stdlib" else [])+(["-O"] if optimized else [])
    stdout=run([python[kind],*flags,str(script)],stage,output/("raw_"+label),receipt)
    body=stdout if result_name is None else safe_regular(script.parent/result_name)
    expected=safe_regular(HERE/"baseline"/(name+".json"))
    need(body==expected,"complete baseline mismatch: "+label)
    observed.append(body)
    receipt["families"].append({"name":name,"optimized":optimized,"baseline_sha256":sha(body),"PASS":True})
   need(observed[0]==observed[1],"normal/optimized results differ: "+name)
  # These true/false calls exercise the actual submitted/repaired guard
  # definitions. In particular -O must not delete false-value rejection.
  for rel,function in [("author/verify.py","ck"),("inherited/independent_checks.py","ck"),("fresh/independent_rational_certificate.py","require")]:
   source=HERE/"source"/rel
   for optimized in [False,True]:
    for truth in [True,False]:
     code=("import ast,sys;from collections import Counter;"
       "t=ast.parse(open(sys.argv[1],encoding='utf-8').read());"
       "f=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==sys.argv[2]];"
       "ns={'C':Counter(),'checks':0};"
       "exec(compile(ast.Module(body=f,type_ignores=[]),'<actual guard>','exec'),ns);"
       "ns[sys.argv[2]]('control',sys.argv[3]=='True') if sys.argv[2]=='ck' and 'g' in f[0].args.args[0].arg else ns[sys.argv[2]](sys.argv[3]=='True','control') if sys.argv[2]=='require' else ns[sys.argv[2]](sys.argv[3]=='True')")
     label="guard_"+str(len(receipt["guards"]))
     flags=["-E","-S","-B","-P"]+(["-O"] if optimized else [])
     run([python["stdlib"],*flags,"-c",code,str(source),function,str(truth)],output,output/label,receipt,0 if truth else 1)
     receipt["guards"].append({"source":rel,"optimized":optimized,"truth":truth,"expected_exit":0 if truth else 1,"PASS":True})
  receipt.update(status="PASS_ALL_EXACT_FAMILIES_NORMAL_AND_OPTIMIZED",UTC_end=utc())
 except BaseException as exc:
  receipt.update(status="FAILED_PRESERVED",error_type=type(exc).__name__,error=str(exc),UTC_end=utc())
  raise
 finally:
  (output/"REPRODUCTION_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(json.dumps({"status":receipt["status"],"family_runs":len(receipt["families"]),"guard_controls":len(receipt["guards"]),"closed_children":len(receipt["children"])}))
if __name__=="__main__":main()

