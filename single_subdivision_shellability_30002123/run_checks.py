"""Full normal and optimized replays in disposable copies; no changes to frozen files."""
import ast,hashlib,json,pathlib,shutil,subprocess,sys,tempfile

def require(ok,why):
    if not ok:raise RuntimeError(why)
def main():
    root=pathlib.Path(__file__).resolve().parent
    for p in root.glob('*.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'Assertion-dependent guard: '+p.name)
    checks=[]
    pairs=[('verify.py',['computation_results.json','two_4simplices_certificate.json']),('sweep_test.py',['failed_convex_sweep.json']),('research_controls.py',['research_control_results.json']),('independent_check.py',['INDEPENDENT_RESULTS.json'])]
    inputs=['two_4simplices_certificate.json','failed_convex_sweep.json','realization.json','negative_controls.json']
    for opt in (False,True):
        with tempfile.TemporaryDirectory(prefix='shellability-replay-') as tmp:
            work=pathlib.Path(tmp)
            for name in inputs+[x[0] for x in pairs]:shutil.copyfile(root/name,work/name)
            for script,outputs in pairs:
                done=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[script],cwd=work,capture_output=True,text=True,timeout=300)
                require(done.returncode==0 and not done.stderr,'Checker failed: '+script+' '+done.stderr)
                hashes={}
                for name in outputs:
                    actual=(work/name).read_bytes();saved=(root/name).read_bytes()
                    require(actual==saved,'Complete saved output differs: '+name)
                    hashes[name]=hashlib.sha256(actual).hexdigest()
                checks.append({'script':script,'optimized':opt,'complete_output_byte_matches':hashes})
    print(json.dumps({'status':'PASS','problem_status':'UNSOLVED','avenues':5,'assertion_nodes':0,'checks':checks},indent=2))
if __name__=='__main__':main()
