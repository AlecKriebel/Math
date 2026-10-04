from pathlib import Path
import subprocess,json,datetime,hashlib,sys,os
BASE=Path(__file__).resolve().parent
PRIVATE=Path('/Users/alec/.cache/codex-pr66-audit-20261004/prior_disposition_fresh_adversary')
PRIVATE.mkdir(parents=True,exist_ok=True)
def run(label,argv):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(BASE))
    stdout,stderr=child.communicate()
    p=subprocess.CompletedProcess(argv,child.returncode,stdout,stderr)
    end=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for kind,b in [('stdout',p.stdout),('stderr',p.stderr)]:
        (BASE/'receipts'/(label+'.'+kind+'.txt')).write_bytes(b)
    r={'label':label,'argv':argv,'actual_child_pid':child.pid,'actual_controller_pid':os.getpid(),'cwd':str(BASE),'utc_start':start,'utc_end':end,'exit_code':p.returncode,'streams':{k:{'path':'receipts/'+label+'.'+k+'.txt','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for k,b in [('stdout',p.stdout),('stderr',p.stderr)]}}
    (BASE/'receipts'/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2));print(p.stdout.decode('utf-8','replace'));print(p.stderr.decode('utf-8','replace'),file=sys.stderr)
    if p.returncode:raise RuntimeError('Command failed')
    return p
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='primary':
        run('002_tools',['sh','-c','command -v pdftotext; command -v pdftoppm; command -v pdfinfo'])
        run('003_download_target',['curl','-L','--fail','--silent','--show-error','https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf','-o',str(PRIVATE/'ohtsuki_primary.pdf')])
        run('004_prior_info',['pdfinfo','/Users/alec/.cache/codex-pr66-audit-20261004/ROOT_priority_sources/inv_author.pdf'])
        run('005_prior_text',['pdftotext','-layout','/Users/alec/.cache/codex-pr66-audit-20261004/ROOT_priority_sources/inv_author.pdf',str(PRIVATE/'inv_author.txt')])
        run('006_target_text',['pdftotext','-layout',str(PRIVATE/'ohtsuki_primary.pdf'),str(PRIVATE/'ohtsuki_primary.txt')])
        for file in ['ohtsuki_primary.pdf','inv_author.txt','ohtsuki_primary.txt']:
            b=(PRIVATE/file).read_bytes();print(json.dumps({'private_file':str(PRIVATE/file),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}))
