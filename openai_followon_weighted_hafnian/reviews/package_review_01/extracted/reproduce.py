"""Verify authored payload integrity and reproduce all finite checks in a clean copy."""
import argparse, hashlib, json, platform, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args()
    manifest=json.loads((ROOT/'PAYLOAD_SHA256.json').read_text())
    for name,digest in manifest.items():
        if sha(ROOT/name)!=digest: raise RuntimeError('Payload mismatch: '+name)
    runs=[]
    with tempfile.TemporaryDirectory(prefix='hafnian-clean-',dir=Path(args.output).resolve().parent) as td:
        copy=Path(td)/'package'; shutil.copytree(ROOT,copy)
        for name in ('test_gadget.py','test_sampling.py','upstream_cell_checks.py'):
            run=subprocess.run([sys.executable,'-I','-B',str(copy/'code'/name)],cwd=copy,capture_output=True,text=True)
            # Isolated mode deliberately suppresses ambient modules; local sibling
            # imports need an explicit bounded launcher for these owned scripts.
            if run.returncode and 'ModuleNotFoundError' in run.stderr:
                launcher="import runpy,sys; sys.path.insert(0,sys.argv[1]); runpy.run_path(sys.argv[2],run_name='__main__')"
                run=subprocess.run([sys.executable,'-I','-B','-c',launcher,str(copy/'code'),str(copy/'code'/name)],cwd=copy,capture_output=True,text=True)
            if run.returncode: raise RuntimeError(name+' failed: '+run.stderr)
            runs.append({'check':name,'returncode':run.returncode,'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest(),'stdout':run.stdout})
        reports={name:json.loads((copy/'data'/name).read_text()) for name in ('gadget_verification.json','sampling_verification.json')}
    receipt={'status':'passed','python_version':platform.python_version(),'payload_hashes_verified':len(manifest),'runs':runs,'reports':reports,'scope':'finite construction and sampling-wrapper checks, not upstream FPRAS certification'}
    Path(args.output).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'passed','payload_hashes_verified':len(manifest),'checks':[r['check'] for r in runs]}))
if __name__=='__main__': main()
