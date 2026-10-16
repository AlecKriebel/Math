"""RAM replay transport; code executes only in disposable shadow namespace.
Only the intended checker JSON write is captured in RAM. Source bytes and
stdout/traceback, commands, optimization and package versions are recorded.
"""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,os,json,sys,hashlib
D=Path(__file__).resolve().parent;O=D.parent/'original_submitted_head'
R=D.parent.parent.parent/'audits/pr200_5100007/math_algebra_family_01/runtime_packages'
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
CHILD=r'''
from pathlib import Path
import sys,io,json,hashlib,contextlib,traceback,dis,types
from datetime import datetime,timezone
code=sys.stdin.read();synthetic=Path(sys.argv[1]);expected=sys.argv[2];captures={}
def capture_write(self,data,*a,**kw):
 if self.parent==synthetic.parent and self.name==expected:
  captures[self.name]=json.loads(data);return len(data)
 raise RuntimeError('Unexpected write destination: '+str(self))
Path.write_text=capture_write
buf=io.StringIO();err=io.StringIO();status=0;started=datetime.now(timezone.utc).isoformat()
compiled=compile(code,str(synthetic),'exec')
def assertion_sites(c):
 return sum((i.opname=='LOAD_ASSERTION_ERROR' or (i.opname=='LOAD_COMMON_CONSTANT' and i.argrepr=='AssertionError')) for i in dis.get_instructions(c))+sum(assertion_sites(x) for x in c.co_consts if isinstance(x,types.CodeType))
with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(err):
 try:exec(compiled,{'__file__':str(synthetic),'__name__':'__main__'})
 except BaseException:
  status=1;traceback.print_exc()
import sympy,mpmath
print(json.dumps({'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),'returncode':status,'optimized':sys.flags.optimize,'python':sys.version,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'assertion_opcode_sites':assertion_sites(compiled),'intended_json_captured':captures,'stdout':buf.getvalue(),'stderr':err.getvalue(),'capture_method':'exec unchanged/explicitly mutated source bytes in disposable shadow namespace; intercept only intended result JSON writer to RAM'}))
'''
who=sys.argv[1];source=O/('verify.py' if who=='author' else 'independent_review/independent_checks.py');raw=source.read_text();rows=[]
shadow=D/'disposable_shadow/author_ordinary_unaltered'
for optimized in [False,True]:
 for mutated in [False,True]:
  code=raw
  if mutated:
   old,new=('am==a0+dot(M,M)*coeff','am==a0+dot(M,M)*(coeff+1)') if who=='author' else ('aa==bb==F(165888,625)','aa==bb==F(165889,625)')
   if code.count(old)!=1:raise RuntimeError('Bad mutation anchor')
   code=code.replace(old,new)
  intended='verification.json' if who=='author' else 'independent_receipt.json'
  synthetic=shadow/source.name
  env=os.environ.copy();env['PYTHONPATH']=str(R);env['PYTHONDONTWRITEBYTECODE']='1'
  argv=[PY,'-B']+(['-O'] if optimized else [])+['-c',CHILD,str(synthetic),intended]
  run=subprocess.run(argv,input=code,text=True,capture_output=True,cwd=shadow,env=env)
  if run.returncode:raise RuntimeError('Replay child transport failed: '+run.stderr)
  record=json.loads(run.stdout);record.update({'who':who,'source_original_sha256':hashlib.sha256(raw.encode()).hexdigest(),'mutated_actual_identity':mutated,'command':[PY,'-B']+(['-O'] if optimized else [])+['-c','<RAM transport in ram_replay.py>',str(synthetic),intended],'child_transport_exit':run.returncode})
  rows.append(record)
  label=f'{who}_{"optimized" if optimized else "ordinary"}_{"false_identity" if mutated else "unaltered"}'
  print(json.dumps({'label':label,'checker_exit':record['returncode'],'assertion_opcode_sites':record['assertion_opcode_sites'],'payload':record['intended_json_captured']}),flush=True)
  try:(D/f'ram_{who}_replay.json').write_text(json.dumps(rows,indent=2)+'\n')
  except OSError as e:print('DISK_RECEIPT_FAILURE '+str(e),flush=True)
print('COMPLETE '+who,flush=True)
