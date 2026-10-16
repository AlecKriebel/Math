from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,os,sys,shutil
ROOT=Path(__file__).resolve().parent

def run(name, argv, url=None, artifacts=()):
    started=datetime.now(timezone.utc).isoformat()
    result=subprocess.run(argv,cwd=ROOT,capture_output=True)
    finished=datetime.now(timezone.utc).isoformat()
    prefix=ROOT/'receipts'/name
    prefix.with_suffix('.stdout').write_bytes(result.stdout)
    prefix.with_suffix('.stderr').write_bytes(result.stderr)
    receipt={'name':name,'UTC_start':started,'UTC_finish':finished,'native_argv':argv,'cwd':str(ROOT),'exit_code':result.returncode,'url':url,'stdout_file':str(prefix.with_suffix('.stdout')),'stderr_file':str(prefix.with_suffix('.stderr')),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(result.stderr).hexdigest(),'artifacts':[]}
    for item in artifacts:
        p=ROOT/item
        if p.exists(): receipt['artifacts'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode&0o777)})
    prefix.with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
    return result

def fetch(name,url):
    out='sources_private/'+name+'.pdf'
    return run(name+'_retrieve',[shutil.which('curl'),'-L','--fail','--max-time','120','--retry','2','--silent','--show-error','-o',out,url],url,[out])

def extract(name):
    return run(name+'_extract',[shutil.which('pdftotext'),'-layout','sources_private/'+name+'.pdf','sources_private/'+name+'.txt'],artifacts=['sources_private/'+name+'.pdf','sources_private/'+name+'.txt'])

if __name__=='__main__':
    if sys.argv[1]=='fetch': fetch(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='extract': extract(sys.argv[2])
