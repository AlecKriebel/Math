#!/usr/bin/env python3
"""Replay the closed authored packet, with optional external source-byte checks."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys

def require(test,message):
    if not test: raise RuntimeError(message)

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path);ap.add_argument('--corpus-dir',type=Path);args=ap.parse_args()
    require(not sys.flags.optimize,'optimized Python is not accepted')
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
    expected={row['path'] for row in manifest['files']}|{'AUTHOR_MANIFEST.json','SHA256SUMS'}
    actual=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink present')
        if p.is_file():actual.add(p.relative_to(root).as_posix())
    require(actual==expected,'packet inventory differs')
    for row in manifest['files']:
        path=Path(row['path']);require(not path.is_absolute() and '..' not in path.parts,'unsafe inventory path')
        b=(root/path).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'],'hash or byte count mismatch: '+str(path))
    sums=[]
    for p in sorted(root.iterdir()):
        if p.is_file() and p.name!='SHA256SUMS':sums.append(sha(p.read_bytes())+'  '+p.name)
    require((root/'SHA256SUMS').read_text()=='\n'.join(sums)+'\n','SHA256SUMS differs')
    run=subprocess.run([sys.executable,str(root/'verify.py')],capture_output=True)
    require(run.returncode==0,'exact verifier failed')
    require(run.stdout==(root/'verification_results.json').read_bytes(),'exact verifier output differs')
    negatives=[]
    for flag in ('jacobian','all_retro'):
        r=subprocess.run([sys.executable,str(root/'verify.py'),'--mutant',flag],capture_output=True,text=True)
        require(r.returncode!=0,'faulty mathematical variant accepted')
        negatives.append({'mutation':flag,'exit_code':r.returncode,'rejected':True,'error_tail':r.stderr.splitlines()[-1]})
    r=subprocess.run([sys.executable,'-O',str(root/'verify.py')],capture_output=True,text=True)
    require(r.returncode!=0,'optimized verifier accepted')
    negatives.append({'mutation':'optimized_python','exit_code':r.returncode,'rejected':True,'error_tail':r.stderr.strip()})
    require(negatives==json.loads((root/'negative_control_results.json').read_text()),'negative-control results differ')
    metadata=json.loads((root/'SOURCE_METADATA.json').read_text())
    external={'source_pdfs':'NOT_RUN','corpora':'NOT_RUN'}
    for key,directory,rows in [('source_pdfs',args.source_dir,metadata['pdfs']),('corpora',args.corpus_dir,metadata['corpora'])]:
        if directory is None:continue
        for row in rows:
            b=(directory/row['filename']).read_bytes()
            require(len(b)==row['bytes'] and sha(b)==row['sha256'],'external input mismatch: '+row['filename'])
        external[key]='PASS_COMPLETE_BYTES'
    result=json.loads(run.stdout)
    print(json.dumps({'status':'PASS_AUTHOR_PACKET_REPLAY','inventory_files':len(actual),'author_assertions':result['assertions'],'negative_controls_rejected':len(negatives),'external_inputs':external,'independent_review':'NOT_PERFORMED_BY_THIS_AUTHOR','full_problem_solved':False},indent=2,sort_keys=True))

if __name__=='__main__':main()
