"""Replay every saved result completely, in isolated disposable directories."""
import ast, hashlib, json, pathlib, shutil, subprocess, sys, tempfile
PAIRS = [('exact_check.py','exact_results.json'),('harmonic_exact_check.py','harmonic_exact_results.json'),('independent_audit_check.py','independent_audit_results.json'),('independent_harmonic_check.py','independent_harmonic_results.json')]
def require(ok, why):
    if not ok: raise RuntimeError(why)
def main():
    root=pathlib.Path(__file__).resolve().parent
    for p in root.glob('*.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'Assertion-dependent guard: '+p.name)
    checks=[]
    for optimized in (False,True):
        with tempfile.TemporaryDirectory(prefix='frame-replay-') as tmp:
            work=pathlib.Path(tmp)
            for script,result in PAIRS:
                shutil.copyfile(root/script,work/script)
            for script,result in PAIRS:
                done=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[script],cwd=work,capture_output=True,text=True,timeout=240)
                require(done.returncode==0 and not done.stderr,'Checker failed: '+script+' '+done.stderr)
                saved=(root/result).read_bytes(); actual=(work/result).read_bytes()
                require(actual==saved,'Complete saved output differs: '+result)
                require(json.loads(done.stdout)==json.loads(saved),'Stdout differs: '+result)
                checks.append({'script':script,'optimized':optimized,'saved_output_byte_match':True,'stdout_json_match':True,'output_sha256':hashlib.sha256(actual).hexdigest()})
            require({p.name for p in work.iterdir()}=={n for pair in PAIRS for n in pair},'Unexpected replay files')
    print(json.dumps({'status':'PASS','overall_problem_status':'UNSOLVED','avenues_completed':5,'checks':checks,'assertion_nodes':0},indent=2))
if __name__=='__main__':main()
