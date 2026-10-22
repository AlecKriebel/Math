"""Deliberate corruption controls; all mutations stay in disposable copies."""
import json,pathlib,shutil,subprocess,sys,tempfile

def require(ok,why):
    if not ok:raise RuntimeError(why)
def run(work,script,opt):
    return subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[script],cwd=work,capture_output=True,text=True,timeout=300)
def main():
    root=pathlib.Path(__file__).resolve().parent;checks=[]
    cases=['same_size_report','missing_file','extra_file','nested_manifest','manifest_hash','corrupt_saved_result','corrupt_hesse_input','corrupt_harmonic_input','independent_hesse_reference','independent_harmonic_reference']
    for opt in (False,True):
        baseline=run(root,'verify_manifest.py',opt)
        require(baseline.returncode==0,'Baseline manifest failed: '+baseline.stderr)
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='frame-corruption-') as tmp:
                work=pathlib.Path(tmp)/'package';shutil.copytree(root,work)
                target='verify_manifest.py';diagnostic=''
                if case=='same_size_report':
                    p=work/'RESULTS.md';b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:]);diagnostic='SHA-256 mismatch'
                elif case=='missing_file':
                    (work/'SOURCE_GATE.md').unlink();diagnostic='Inventory mismatch'
                elif case=='extra_file':
                    (work/'EXTRA.txt').write_text('extra');diagnostic='Inventory mismatch'
                elif case=='nested_manifest':
                    (work/'nested').mkdir();(work/'nested'/'MANIFEST.json').write_text('{}');diagnostic='Inventory mismatch'
                elif case=='manifest_hash':
                    p=work/'MANIFEST.json';obj=json.loads(p.read_text());obj['files'][0]['sha256']='0'*64;p.write_text(json.dumps(obj));diagnostic='SHA-256 mismatch'
                elif case=='corrupt_saved_result':
                    p=work/'exact_results.json';obj=json.loads(p.read_text());obj['total_nontrivial_partitions']=29;p.write_text(json.dumps(obj));target='run_checks.py';diagnostic='Complete saved output differs'
                elif case in ('corrupt_hesse_input','corrupt_harmonic_input'):
                    target='exact_check.py' if case=='corrupt_hesse_input' else 'harmonic_exact_check.py'
                    old='M.conjugate().T*M/2' if case=='corrupt_hesse_input' else 'D=[0,1,2,3,5,7,8,11]'
                    new='M.conjugate().T*M/3' if case=='corrupt_hesse_input' else 'D=[0,1,2,3,5,7,8,10]'
                    p=work/target;text=p.read_text();require(text.count(old)==1,'Mutation target changed');p.write_text(text.replace(old,new));diagnostic='Exact verification failed'
                else:
                    hesse=case=='independent_hesse_reference'
                    p=work/('exact_results.json' if hesse else 'harmonic_exact_results.json');obj=json.loads(p.read_text());key='proper_nonsingleton_tight_blocks_zero_based' if hesse else 'proper_tight_blocks_zero_based';obj[key]=obj[key][1:];p.write_text(json.dumps(obj))
                    target='independent_audit_check.py' if hesse else 'independent_harmonic_check.py';diagnostic='Independent exact audit failed' if hesse else 'Independent harmonic audit failed'
                done=run(work,target,opt)
                require(done.returncode!=0 and diagnostic in done.stderr,'Corruption not rejected: '+case+' '+done.stdout+done.stderr)
                checks.append({'mutation':case,'optimized':opt,'rejected':True,'diagnostic':diagnostic})
    print(json.dumps({'status':'PASS','controls':checks,'scope':'Selected accidental/input/reference corruption controls; not authentication or exhaustive fault coverage.'},indent=2))
if __name__=='__main__':main()
