#!/usr/bin/env python3
"""Copy-only confirmation supersedes the initial source-entrypoint diagnostic."""
from pathlib import Path
import hashlib,json,os,shutil,socket,subprocess,sys,time
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
WORK=HERE/'replay'
SOURCE=WORK/'relocated assembly with spaces/publication_20261014/verification_package'
PIN='19d20ccc3b5533a45d262f7c784e052555b3bf8cc47d9a2b76bc17ab5eda9360'
def need(c,m):
    if not c:raise RuntimeError(m)
def main():
    records=[]
    for generation in ['r1','r2']:
        original=AUDIT.parents[1]/('work/pr826_revision_'+generation)/'publication_20261014/preprint/build_verification.py'
        program=WORK/(generation+' disposable-builder.py');shutil.copyfile(original,program)
        need(program.read_bytes()==original.read_bytes(),'builder copy changed bytes')
        for kind in (['fifo'] if generation=='r1' else ['fifo','socket','directory','symlink']):
            for opt in [False,True]:
                root=WORK/('copy-only '+generation+' '+kind+' '+str(opt));shutil.copytree(SOURCE,root)
                p=root/'package_index.json';p.unlink()
                if kind=='fifo':os.mkfifo(p)
                elif kind=='socket':
                    previous=Path.cwd();s=socket.socket(socket.AF_UNIX)
                    try:os.chdir(root);s.bind('package_index.json')
                    finally:os.chdir(previous);s.close()
                elif kind=='directory':p.mkdir()
                else:p.symlink_to(SOURCE/'package_index.json')
                output=WORK/('copy-only-output '+generation+' '+kind+' '+str(opt));t=time.monotonic()
                try:
                    r=subprocess.run([sys.executable,'-I','-S','-B',*(['-O'] if opt else []),str(program),'--from-package',str(root),'--trusted-index-sha256',PIN,'--output-root',str(output)],cwd='/',capture_output=True,text=True,timeout=1)
                    rc,err,timed=r.returncode,r.stderr,False
                except subprocess.TimeoutExpired:rc,err,timed=None,'',True
                need(timed if generation=='r1' else (not timed and rc!=0 and 'regular file' in err),'nonregular behavior')
                need(not output.exists(),'rejected builder wrote output')
                records.append(dict(generation=generation,kind=kind,optimized=opt,mutation_applied=True,executed_disposable_program=str(program.relative_to(HERE)),program_sha256=hashlib.sha256(program.read_bytes()).hexdigest(),timed_out=timed,returncode=rc,stderr=err,seconds=time.monotonic()-t));shutil.rmtree(root)
    (HERE/'COPY_ONLY_NONREGULAR_REPLAY.json').write_text(json.dumps(dict(status='PASS',test_count=len(records),results=records,diagnostic='Supersedes initial ten nonregular-index diagnostics, which used original unchanged builder script entrypoints with only scratch input/output. No reviewed file changed. All accepted confirmation runs execute byte-identical disposable program copies; public harness corrected accordingly.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',test_count=len(records))))
if __name__=='__main__':main()
