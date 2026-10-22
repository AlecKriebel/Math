from pathlib import Path
import subprocess, json, hashlib, datetime, os, sys
A=Path(__file__).resolve().parents[2]
R=Path(__file__).resolve().parent
P=A/'NEWpreprint_v1_0'
S=R/'scratch'
S.mkdir(exist_ok=True)
PYTHONS={'py311':'/opt/homebrew/opt/python@3.11/bin/python3.11','py314':'/opt/homebrew/bin/python3'}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(name,data): (R/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def run(label,argv,cwd=P,expected=0):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True)
    out=R/(label+'.stdout');err=R/(label+'.stderr')
    out.write_bytes(proc.stdout);err.write_bytes(proc.stderr)
    item={'label':label,'utc':start,'argv':[str(x) for x in argv],'cwd':str(cwd),'exit':proc.returncode,'expected':expected,'stdout':out.name,'stdout_bytes':len(proc.stdout),'stdout_sha256':sha(out),'stderr':err.name,'stderr_bytes':len(proc.stderr),'stderr_sha256':sha(err)}
    with (R/'COMMANDS.jsonl').open('a') as f:f.write(json.dumps(item)+'\n')
    if proc.returncode!=expected:raise RuntimeError(item)
    return proc
if __name__=='__main__':
    for key,py in PYTHONS.items():
        run(key+'-version',[py,'-c','import sys,json;print(json.dumps({"version":sys.version,"float":list(sys.float_info)}))'])
        for name,flag in [('normal',[]),('optimized',['-O'])]:
            prefix=key+'-'+name
            run(prefix+'-verify',[py,*flag,P/'scripts/verify_package.py'])
            run(prefix+'-strict',[py,*flag,P/'scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/'PR1071_preprint_v1_0_support.zip'])
            run(prefix+'-check',[py,*flag,P/'scripts/check.py','--out',S/(prefix+'-check')])
            run(prefix+'-archive',[py,*flag,P/'scripts/build_archive.py','--out',S/(prefix+'.zip')])
            run(prefix+'-pdf',[py,*flag,P/'scripts/build_pdf.py','--out',S/(prefix+'-pdf')])
            if sha(S/(prefix+'.zip'))!=sha(P/'PR1071_preprint_v1_0_support.zip'):raise RuntimeError('archive mismatch '+prefix)
            if sha(S/(prefix+'-pdf')/'paper.pdf')!=sha(P/'paper.pdf'):raise RuntimeError('PDF mismatch '+prefix)
    run('render-paper',['/opt/homebrew/bin/pdftoppm','-r','95','-png',P/'paper.pdf',R/'page'])
    put('PUBLIC_REPLAY.json',{'status':'PASS','runtimes':PYTHONS,'unmodified_wrappers':True,'four_archive_bytes_exact':True,'four_PDF_bytes_exact':True})
