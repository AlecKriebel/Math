"""Verify authored payload integrity and reproduce all finite checks in a clean copy."""
import argparse, hashlib, json, os, platform, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args()
    manifest_path=ROOT/'PAYLOAD_SHA256.json'
    manifest_bytes=manifest_path.read_bytes()
    manifest=json.loads(manifest_bytes)
    if not isinstance(manifest,dict): raise RuntimeError('Invalid payload manifest')
    output=Path(args.output).resolve()
    sources={}
    for name in manifest:
        if not isinstance(name,str): raise RuntimeError('Invalid payload path')
        relative=PurePosixPath(name)
        if (not name or relative.is_absolute() or str(relative)!=name
                or '\\' in name or any(p in ('.','..') for p in relative.parts)):
            raise RuntimeError('Invalid payload path: '+name)
        source=(ROOT/name).resolve()
        if ROOT not in source.parents or not source.is_file():
            raise RuntimeError('Payload is not an internal regular file: '+name)
        sources[name]=source
    for protected in [manifest_path,*sources.values()]:
        if output==protected or (output.exists() and output.samefile(protected)):
            parser.error('Receipt output collides with a protected package file')
    if not output.parent.is_dir() or (output.exists() and not output.is_file()):
        parser.error('Receipt output must be a file in an existing directory')
    # Read/hash each payload once; execute precisely those verified bytes.
    payload={}
    for name,digest in manifest.items():
        contents=sources[name].read_bytes()
        if hashlib.sha256(contents).hexdigest()!=digest:
            raise RuntimeError('Payload mismatch: '+name)
        payload[name]=contents
    runs=[]
    with tempfile.TemporaryDirectory(prefix='hafnian-clean-',dir=output.parent) as td:
        copy=Path(td)/'package'; copy.mkdir()
        for name,contents in payload.items():
            destination=copy/name; destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_bytes(contents)
        (copy/'PAYLOAD_SHA256.json').write_bytes(manifest_bytes)
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
    # Atomic replacement also avoids modifying an existing file through an alias.
    with tempfile.NamedTemporaryFile(mode='w',dir=output.parent,
            prefix='.hafnian-receipt-',delete=False) as stream:
        temporary=Path(stream.name)
        json.dump(receipt,stream,indent=2); stream.write('\n')
    try: os.replace(temporary,output)
    finally: temporary.unlink(missing_ok=True)
    print(json.dumps({'status':'passed','payload_hashes_verified':len(manifest),'checks':[r['check'] for r in runs]}))
if __name__=='__main__': main()
