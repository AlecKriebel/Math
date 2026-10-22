"""Fail-closed inventory, full replay and real mathematical corruption controls."""
import ast, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXPECTED={'README.md','RESEARCH.md','FIVE_APPROACHES.md','SOURCE_GATE.md','SOURCE_METADATA.json','INDEPENDENT_FLUX_AUDIT.md','POSITIVE_ETA_AUDIT.md','ZERO_ENTROPY_AUDIT.md','VERIFICATION_METADATA.json','check_exact.py','check_zero_entropy.py','check_positive_eta.py','EXACT_CHECKS.json','ZERO_CHECKS.txt','POSITIVE_CHECKS.txt','verify.py','MANIFEST.json'}
def require(ok,message):
    if not ok: raise RuntimeError(message)
def inventory(root):
    entries=list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries),'Symlink in package')
    require(not any(not p.is_file() for p in entries),'Unexpected directory or special entry')
    names={p.relative_to(root).as_posix() for p in entries}
    require(names==EXPECTED,'Strict inventory mismatch')
    m=json.loads((root/'MANIFEST.json').read_text())
    require(set(m['files'])==EXPECTED-{'MANIFEST.json'},'Manifest key mismatch')
    for name,spec in m['files'].items():
        data=(root/name).read_bytes()
        require(spec=={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()},'Hash/size mismatch: '+name)
def run(path,opt):
    return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(path)],capture_output=True,text=True,timeout=180,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
def main():
    inventory(ROOT)
    if '--inventory-only' in sys.argv:
        print('inventory PASS');return
    for script in ('verify.py','check_exact.py','check_zero_entropy.py','check_positive_eta.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((ROOT/script).read_text()))),'Inactive optimized-mode assertion')
    replay=[]
    for script,result in [('check_exact.py','EXACT_CHECKS.json'),('check_zero_entropy.py','ZERO_CHECKS.txt'),('check_positive_eta.py','POSITIVE_CHECKS.txt')]:
        for opt in (False,True):
            proc=run(ROOT/script,opt)
            require(proc.returncode==0,proc.stderr)
            require(proc.stdout==(ROOT/result).read_text(),'Complete output mismatch: '+script)
            replay.append({'script':script,'optimized':opt,'full_output_match':True})
    mutations=[('flux_sign','check_exact.py','f=(r-s.sqrt(r*r-4*p*(1-p)))/2','f=(r+s.sqrt(r*r-4*p*(1-p)))/2'),('cost_factor','check_exact.py','cost_derivative=h*(D.subs(x,x+h)-D)','cost_derivative=2*h*(D.subs(x,x+h)-D)'),('barrier_speed','check_exact.py','tau=-theta2*kk/2','tau=-theta2*kk'),('sorting_direction','check_zero_entropy.py','max(0,z-d),min(d,z)','min(d,z),max(0,z-d)'),('positive_direction','check_positive_eta.py','a[:]=p-f;b[:]=p+f','a[:]=p+f;b[:]=p-f')]
    controls=[];tamper=[]
    with tempfile.TemporaryDirectory() as temp:
        base=Path(temp)
        for name,script,before,after in mutations:
            source=(ROOT/script).read_text();require(source.count(before)==1,'Nonunique mutation target')
            path=base/(name+'.py');path.write_text(source.replace(before,after))
            for opt in (False,True):
                proc=run(path,opt)
                require(proc.returncode!=0 and 'RuntimeError: MATHEMATICAL CHECK:' in proc.stderr,'Mathematical mutant survived: '+name)
                controls.append({'mutation':name,'optimized':opt,'rejected':True,'failure':proc.stderr.strip().splitlines()[-1]})
        for case in ('missing','altered','extra','nested_manifest','symlink'):
            copy=base/case;shutil.copytree(ROOT,copy)
            if case=='missing':(copy/'README.md').unlink()
            if case=='altered':(copy/'README.md').write_text('altered')
            if case=='extra':(copy/'extra.txt').write_text('extra')
            if case=='nested_manifest':
                (copy/'nested').mkdir();(copy/'nested'/'MANIFEST.json').write_text('{}')
            if case=='symlink':(copy/'extra').symlink_to('README.md')
            for opt in (False,True):
                proc=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(copy/'verify.py'),'--inventory-only'],capture_output=True,text=True)
                require(proc.returncode!=0 and 'RuntimeError:' in proc.stderr,'Inventory mutant survived: '+case)
                tamper.append({'case':case,'optimized':opt,'rejected':True})
    print(json.dumps({'inventory':'PASS','explicit_guards':'PASS','replay':replay,'mathematical_controls':controls,'inventory_controls':tamper},indent=2))
if __name__=='__main__':main()
