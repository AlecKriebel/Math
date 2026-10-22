"""Reproduce this owned audit only; never execute submitted code."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,os,json,hashlib,platform
import sympy,mpmath
assert sympy.__version__=='1.14.0'
assert mpmath.__version__=='1.3.0'
root=Path(__file__).resolve().parent
runs=root/'run_logs'; runs.mkdir(exist_ok=True)
programs=['algebra_check.py','telescoping_certificate.py','euclidean_check.py','meromorphic_check.py','telescoping_numeric.py']
steps=[]
for name in programs:
    result=subprocess.run([sys.executable,str(root/name)],cwd=root,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
    (runs/(name+'.stdout.txt')).write_text(result.stdout)
    (runs/(name+'.stderr.txt')).write_text(result.stderr)
    steps.append({'program':name,'sha256':hashlib.sha256((root/name).read_bytes()).hexdigest(),'returncode':result.returncode})
    print(name,'PASS' if result.returncode==0 else 'FAIL',flush=True)
    assert result.returncode==0, result.stderr
record={'completed_utc':datetime.now(timezone.utc).isoformat(),'interpreter':sys.executable,'python':sys.version,'platform':platform.platform(),'sympy':sympy.__version__,'mpmath':mpmath.__version__,'steps':steps,'scope':'Only independent owned audit programs were executed.'}
(root/'reproduction_run.json').write_text(json.dumps(record,indent=2)+'\n')
