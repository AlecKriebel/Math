"""Run frozen-equivalent read-only source, with private scratch and receipts."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'preprint/support'
TMP=ROOT/'tmp'
TMP.mkdir(exist_ok=True)

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def ident(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    env=os.environ.copy(); env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'; env['TMPDIR']=str(TMP)
    bundled='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
    results=[]
    before={p.relative_to(SOURCE).as_posix():ident(p) for p in SOURCE.rglob('*') if p.is_file()}
    for label,exe,flags,opt in [('system_normal',sys.executable,['-B'],None),('system_outer_O',sys.executable,['-O','-B'],None),('system_env_2',sys.executable,['-B'],'2'),('bundled_normal',bundled,['-B'],None)]:
        saved=ROOT/('REPLAY_'+label+'.json')
        if saved.is_file():
            old=json.loads(saved.read_text())
            if old['returncode']==0 and json.loads(old.get('stdout','{}')).get('result')=='PASS':
                old['observed_result']=json.loads(old.pop('stdout'));results.append(old);print(label,'previous PASS receipt retained',flush=True);continue
        e=env.copy()
        if opt is not None:e['PYTHONOPTIMIZE']=opt
        cmd=[exe,*flags,str(SOURCE/'verify_bundle.py')]
        started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        r=subprocess.run(cmd,cwd=TMP,env=e,text=True,capture_output=True,timeout=600)
        receipt={'mode':label,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'PYTHONOPTIMIZE':opt,'returncode':r.returncode,'stderr':r.stderr,'stdout':r.stdout}
        print(label,'finished returncode',r.returncode,'stdout sha256',hashlib.sha256(r.stdout.encode()).hexdigest(),flush=True)
        (ROOT/('REPLAY_'+label+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        need(r.returncode==0,label+' failed: '+r.stderr)
        parsed=json.loads(r.stdout); need(parsed['result']=='PASS','Wrapper result')
        receipt['observed_result']=parsed;receipt.pop('stdout')
        results.append(receipt)
        print(label,'PASS',flush=True)
    out=TMP/'rebuild'
    r=subprocess.run([sys.executable,'-B',str(SOURCE/'build_package.py'),'--output-dir',str(out),'--pdf',str(ROOT/'frozen/output/pdf/paper.pdf')],cwd=TMP,env=env,text=True,capture_output=True,timeout=120)
    need(r.returncode==0,'Builder failed: '+r.stderr)
    binding=json.loads((ROOT/'INPUT_BINDING.json').read_text())
    rebuilt=[]
    for e in binding['frozen_publication_files']:
        found=ident(out/e['path']);need(found=={k:e[k] for k in ('bytes','sha256')},'Rebuild differs: '+e['path'])
        rebuilt.append({'path':e['path'],**found})
    inv=json.loads((out/'PACKAGE_INVENTORY.json').read_text())
    need(inv['files']==rebuilt and inv['support_files']==155,'Rebuild inventory')
    shutil.rmtree(out)
    after={p.relative_to(SOURCE).as_posix():ident(p) for p in SOURCE.rglob('*') if p.is_file()}
    need(before==after,'Read-only equivalent source changed')
    receipt={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','source':str(SOURCE),'source_equivalent_to_frozen_zip':'PACKAGE_RECEIPT.json','replay_modes':results,'portable_builder':{'returncode':r.returncode,'outputs':rebuilt,'inventory_timestamp':inv['built_at'],'support_files':155,'output_outside_closed_source':True,'temporary_rebuild_removed':True},'all_closed_source_bytes_unchanged':True}
    (ROOT/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('portable_builder PASS',flush=True)

if __name__=='__main__':main()
