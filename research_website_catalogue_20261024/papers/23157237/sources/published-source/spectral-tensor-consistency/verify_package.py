"""Portable finite-control replay. A passing result is not a theorem certificate."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,gzip,hashlib,json,math,os,stat,subprocess,sys
HERE=Path(__file__).resolve().parent
now=lambda:datetime.now(timezone.utc).isoformat()
def require(value,message):
 if not value:raise RuntimeError(message)
def pin(path):
 p=Path(path);b=p.read_bytes()
 return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def compare(actual,expected,path='result'):
 if type(expected) is float:
  require(type(actual) in (float,int) and math.isfinite(actual) and math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-14),path+' floating diagnostic differs')
 elif type(expected) is dict:
  require(type(actual) is dict and actual.keys()==expected.keys(),path+' keys/type differ')
  for k in expected:compare(actual[k],expected[k],path+'.'+k)
 elif type(expected) is list:
  require(type(actual) is list and len(actual)==len(expected),path+' list type/length differs')
  for i,(a,b) in enumerate(zip(actual,expected)):compare(a,b,path+'['+str(i)+']')
 else:require(type(actual) is type(expected) and actual==expected,path+' exact value/type differs')
def main():
 require(sys.flags.optimize==0,'Run with optimization disabled; use python3 -E -B')
 import sympy
 require(sympy.__version__=='1.14.0','This recorded control version requires SymPy1.14.0')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True)
 args=ap.parse_args();out=Path(args.output).resolve()
 require(not out.exists(),'Output directory already exists; choose a new directory')
 require(out!=HERE and HERE not in out.parents,'Replay output must be outside the package directory')
 manifest=json.loads((HERE/'MANIFEST.json').read_text())
 require(manifest['schema']=='spectral-tensor-supplement/v1','Unexpected manifest schema')
 for row in manifest['payload']:
  rel=Path(row['path']);require(not rel.is_absolute() and '..' not in rel.parts,'Unsafe member path')
  p=HERE/rel;require(p.is_file() and not p.is_symlink(),'Missing/nonregular package member '+str(rel))
  got=pin(p);require(all(got[k]==row[k] for k in ('bytes','sha256')),'Package member differs '+str(rel))
 cases=json.loads((HERE/'CONTROL_CASES.json').read_text())
 expected=json.loads((HERE/'EXPECTED_SCIENTIFIC_OUTPUTS.json').read_text())
 require(len(cases)==8 and len({c['label'] for c in cases})==8,'Expected eight distinct control cases')
 out.mkdir(parents=True);(out/'executed_runner.py').write_bytes(Path(__file__).read_bytes());receipts=[]
 runtime=dict(python=sys.version,executable=pin(sys.executable),sympy=sympy.__version__,optimization=sys.flags.optimize)
 for case in cases:
  label=case['label'];work=out/label;work.mkdir()
  original=HERE/case['source'];got=pin(original)
  require(got['sha256']==case['source_sha256'] and got['bytes']==case['source_bytes'],'Control source differs '+label)
  source=work/original.name;source.write_bytes(original.read_bytes())
  argv=[sys.executable,'-E','-B',str(source)]
  req=dict(label=label,actual_launcher_PID=os.getpid(),started_UTC=now(),argv=argv,cwd=str(work),source=pin(source),original_source=got,runner_source=pin(__file__),runtime=runtime)
  (work/'request.json').write_text(json.dumps(req,indent=2)+'\n')
  process=subprocess.Popen(argv,cwd=work,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdout,stderr=process.communicate()
  req.update(actual_child_PID=process.pid,completed_UTC=now(),exit_code=process.returncode)
  for name,body in [('stdout',stdout),('stderr',stderr)]:
   p=work/(name+'.bin.gz');p.write_bytes(gzip.compress(body,mtime=0));require(gzip.decompress(p.read_bytes())==body,'Stream round-trip failed')
   req[name]=dict(codec='gzip',logical_bytes=len(body),logical_sha256=hashlib.sha256(body).hexdigest(),stored=pin(p))
  (work/'execution.json').write_text(json.dumps(req,indent=2)+'\n')
  require(process.returncode==0,'Control failed; inspect retained streams: '+label)
  require(not stderr,'Control wrote stderr; inspect retained streams: '+label)
  require(pin(source)==req['source'],'Executed control source changed '+label)
  data=json.loads(stdout if case['output']=='stdout' else (work/case['output']).read_bytes())
  selected={k:data[k] for k in case['scientific_fields']}
  compare(selected,expected[label],label)
  (work/'scientific_output.json').write_text(json.dumps(selected,indent=2,ensure_ascii=False)+'\n')
  receipts.append(dict(label=label,native_execution=req,scientific_output=pin(work/'scientific_output.json'),comparison='PASS; exact nonfloating fields; rel1e-12/abs1e-14 floating diagnostics'))
  print(label+': PASS',flush=True)
 receipt=dict(status='PASS_ALL_EIGHT_FINITE_CONTROL_SUITES',UTC=now(),actual_launcher_PID=os.getpid(),launcher_argv=sys.argv,cwd=os.getcwd(),runtime=runtime,manifest=pin(HERE/'MANIFEST.json'),native_executions=receipts,float_comparison={'relative_tolerance':1e-12,'absolute_tolerance':1e-14},limits='Finite algebra and stress controls only; not an infinite PDE/statistical proof, general-domain estimator implementation, priority guarantee, human peer review or proof-assistant certificate. Parent invocation provenance is actual self-report; no upstream launcher certificate.')
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(receipt['status'],flush=True)
if __name__=='__main__':main()
