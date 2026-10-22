#!/usr/bin/env python3
"""Pinned, non-root, relocated archive replay and independently selected controls.
Outputs no machine-local paths. Fixed-files/trusted-Python threat model only.
"""
import argparse, hashlib, json, os, pathlib, shutil, stat, subprocess, sys, tarfile, tempfile

def need(value, message):
    if not value: raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,value):p.write_text(json.dumps(value))
def unlock(root):
    for d,dirs,files in os.walk(root):
        pathlib.Path(d).chmod(0o755)
        for name in files:
            p=pathlib.Path(d)/name
            if not p.is_symlink() and p.is_file():p.chmod(0o644)
def snapshot(root):
    return {str(p.relative_to(root)):{'sha256':sha(p),'mode':stat.S_IMODE(p.stat().st_mode)} for p in sorted(root.rglob('*')) if p.is_file()}
def checked_run(cmd,cwd,env=None):return subprocess.run(cmd,capture_output=True,text=True,cwd=cwd,env=env,timeout=90)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True)
    for name in ['archive-sha256','manifest-sha256','bootstrap-sha256','verifier-sha256']:ap.add_argument('--'+name,required=True)
    ap.add_argument('--ledger-hardened',action='store_true');args=ap.parse_args()
    need(os.getuid()!=0 and os.geteuid()!=0,'real and effective UID must both be nonzero')
    need(sys.flags.isolated==1,'isolated audit process required')
    archive=pathlib.Path(args.archive).resolve();need(sha(archive)==args.archive_sha256,'archive external pin')
    work=pathlib.Path(tempfile.mkdtemp(prefix='quadrisecant-independent-'));frozen=work/'relocated';frozen.mkdir()
    receipt={'schema':'wild-quadrisecants-independent-replay-v1','uid':os.getuid(),'euid':os.geteuid(),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'manifest_sha256':args.manifest_sha256,'bootstrap_sha256':args.bootstrap_sha256,'verifier_sha256':args.verifier_sha256,'members':[],'modes':[],'read_only_denials':[],'controls':[],'ledger_regression':[],'formal_certification':False}
    try:
        with tarfile.open(archive,'r:gz') as tar:
            ms=tar.getmembers();need(len(ms)==len({m.name for m in ms}),'duplicate archive members')
            allowed={'packet','freeze','audit_tools','evidence'}
            packet={'LEDGER.json','README.md','REPORT.md','SOURCES.json','STATUS.json','proof_checks.py','verify.py'}
            names={m.name for m in ms}
            mandatory={'packet','freeze','audit_tools'}|{'packet/'+n for n in packet}|{'freeze/'+n for n in ['BOOTSTRAP_PINS.json','FREEZE_MANIFEST.json','bootstrap.py']}|{'audit_tools/replay_tests.py'}
            need(mandatory<=names<=mandatory|{'evidence','evidence/ACCEPTANCE.json','evidence/ACCEPTANCE.md'},'archive inventory allowlist')
            for m in ms:
                p=pathlib.PurePosixPath(m.name)
                need(not p.is_absolute() and '..' not in p.parts and (m.isfile() or m.isdir()),'unsafe archive member')
                dest=frozen/m.name
                if m.isdir():dest.mkdir(parents=True,exist_ok=True)
                else:
                    need(m.size<=2_000_000,'archive member size')
                    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tar.extractfile(m).read());dest.chmod(0o444)
                receipt['members'].append({'name':m.name,'bytes':m.size,'kind':'file' if m.isfile() else 'directory'})
        for p in sorted(frozen.rglob('*'),reverse=True):
            if p.is_dir():p.chmod(0o555)
        frozen.chmod(0o555)
        pins={'freeze/bootstrap.py':args.bootstrap_sha256,'freeze/FREEZE_MANIFEST.json':args.manifest_sha256,'packet/verify.py':args.verifier_sha256}
        for name,pin in pins.items():need(sha(frozen/name)==pin,'extracted external pin')
        before=snapshot(frozen);bootstrap=frozen/'freeze/bootstrap.py';verifier=frozen/'packet/verify.py';packet=frozen/'packet'
        for flags in [[],['-O'],['-OO']]:
            p=checked_run([sys.executable,'-I','-B',*flags,str(bootstrap),str(packet)],work)
            need(p.returncode==0,'clean frozen replay failed');result=json.loads(p.stdout)
            need(result['uid']==os.geteuid() and result['optimize']==len(flags[0])-1 if flags else result['uid']==os.geteuid() and result['optimize']==0,'execution identity/mode')
            receipt['modes'].append(result)
        for name in ['packet/REPORT.md','packet/forbidden-create','freeze/FREEZE_MANIFEST.json','freeze/forbidden-create','forbidden-create']:
            try:fd=os.open(frozen/name,os.O_WRONLY|os.O_CREAT,0o600)
            except PermissionError:receipt['read_only_denials'].append(name)
            else:os.close(fd);raise RuntimeError('read-only denial failed')
        p=checked_run([sys.executable,'-I','-B',str(frozen/'audit_tools/replay_tests.py')],work)
        need(p.returncode==0,'distributed author harness replay failed');r=json.loads(p.stdout)
        need(r['hostile_case_count']==31 and r['hostile_run_count']==93 and r['frozen_files_unchanged'],'distributed count mismatch')
        receipt['distributed_harness']={k:r[k] for k in ['hostile_case_count','hostile_run_count','frozen_files_unchanged','uid']}
        def case(name,mutate,direct=False,accept=False,no_isolation=False,rootlink=False):
            for level,flags in enumerate([[],['-O'],['-OO']]):
                d=work/('case-'+str(len(receipt['controls'])+len(receipt['ledger_regression'])))
                d.mkdir();shutil.copytree(frozen/'packet',d/'packet');shutil.copytree(frozen/'freeze',d/'freeze');unlock(d)
                mutate(d);target=d/'packet'
                if rootlink:(d/'rootlink').symlink_to(target,target_is_directory=True);target=d/'rootlink'
                if direct:cmd=[sys.executable,'-I','-B',*flags,str(verifier),'--packet',str(target),'--manifest',str(d/'freeze/FREEZE_MANIFEST.json'),'--manifest-sha256',sha(d/'freeze/FREEZE_MANIFEST.json')]
                else:cmd=[sys.executable,*([] if no_isolation else ['-I']),'-B',*flags,str(d/'freeze/bootstrap.py'),str(target)]
                p=checked_run(cmd,d,dict(os.environ,PYTHONPATH=str(d)))
                need((p.returncode==0)==accept,'unexpected control outcome: '+name)
                need(not(d/'executed-marker').exists(),'injected code executed: '+name)
                entry={'case':name,'optimize':level,'accepted':p.returncode==0,'returncode':p.returncode,'direct_repin':direct}
                (receipt['ledger_regression'] if name.startswith('ledger regression') else receipt['controls']).append(entry)
                unlock(d);shutil.rmtree(d)
        def change_manifest(d,fn):
            p=d/'freeze/FREEZE_MANIFEST.json';v=json.loads(p.read_text());fn(v);dump(p,v)
        def repin(d,name):
            p=d/'packet'/name;change_manifest(d,lambda v:v['files'].__setitem__(name,{'bytes':p.stat().st_size,'sha256':sha(p)}))
        def change_doc(d,name,fn):
            p=d/'packet'/name;v=json.loads(p.read_text());fn(v);dump(p,v);repin(d,name)
        def raw_doc(d,name,raw):p=d/'packet'/name;p.write_text(raw);repin(d,name)
        def replacement(d,name,kind):
            p=d/'packet'/name;p.unlink()
            if kind=='symlink':p.symlink_to(packet/name)
            elif kind=='directory':p.mkdir()
            elif kind=='fifo':os.mkfifo(p)
        case('tampered report',lambda d:(d/'packet/REPORT.md').write_text('changed'))
        case('tampered finite checker',lambda d:(d/'packet/proof_checks.py').write_text('raise RuntimeError'))
        case('substituted verifier',lambda d:(d/'packet/verify.py').write_text('from pathlib import Path;Path("executed-marker").touch()'))
        case('repinned report bootstrap rejection',lambda d:(raw_doc(d,'REPORT.md','changed')))
        case('missing file',lambda d:(d/'packet/STATUS.json').unlink())
        case('extra file',lambda d:(d/'packet/EXTRA').write_text('x'))
        case('extra directory',lambda d:(d/'packet/EXTRA').mkdir())
        for kind in ['symlink','directory','fifo']:case('nonregular report '+kind,lambda d,k=kind:replacement(d,'REPORT.md',k))
        case('symlink packet root',lambda d:None,rootlink=True)
        case('non-isolated bootstrap',lambda d:None,no_isolation=True)
        for name,raw in [('broken JSON','{'),('array','[]'),('duplicate key','{"schema":0,"schema":1}'),('NaN','{"schema":NaN}'),('infinity','{"schema":Infinity}')]:
            case('manifest '+name,lambda d,s=raw:(d/'freeze/FREEZE_MANIFEST.json').write_text(s),direct=True)
        for name,val in [('boolean',True),('float',1.0),('negative',-1),('oversize',2_000_001),('string','3')]:
            case('byte count '+name,lambda d,v=val:change_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',v)),direct=True)
        for name,val in [('short','a'),('uppercase','A'*64),('integer',5)]:
            case('digest '+name,lambda d,v=val:change_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('sha256',v)),direct=True)
        for path in ['../escape','/synthetic-absolute-control']:
            case('forbidden manifest path '+('relative' if path[0]=='.' else 'absolute'),lambda d,k=path:change_manifest(d,lambda x:x['files'].__setitem__(k,{'bytes':0,'sha256':'0'*64})),direct=True)
        case('manifest extra field',lambda d:change_manifest(d,lambda x:x.__setitem__('extra',0)),direct=True)
        case('file record extra field',lambda d:change_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('extra',0)),direct=True)
        for key,value in [('problem_id',True),('turns',True),('turns',5.0),('main_problem_resolved',True),('formal_certification',True),('novelty_claim',True),('status','solved')]:
            case('status '+key+' '+type(value).__name__,lambda d,k=key,v=value:change_doc(d,'STATUS.json',lambda x:x.__setitem__(k,v)),direct=True)
        case('status duplicate JSON key',lambda d:raw_doc(d,'STATUS.json','{"problem_id":11300004,"problem_id":11300004}'),direct=True)
        case('status malformed shape',lambda d:raw_doc(d,'STATUS.json','[]'),direct=True)
        case('ledger wrong length',lambda d:change_doc(d,'LEDGER.json',lambda x:x['approaches'].pop()),direct=True)
        case('ledger wrong turn order',lambda d:change_doc(d,'LEDGER.json',lambda x:x['approaches'].reverse()),direct=True)
        case('source redistribution true',lambda d:change_doc(d,'SOURCES.json',lambda x:x.__setitem__('source_documents_included',True)),direct=True)
        case('source duplicate JSON key',lambda d:raw_doc(d,'SOURCES.json','{"source_documents_included":false,"source_documents_included":false}'),direct=True)
        case('isolated external module shadow ignored',lambda d:(d/'json.py').write_text('from pathlib import Path;Path("executed-marker").touch();raise RuntimeError'),accept=True)
        for key,value in [('turn',True),('turn',1.0),('turns_used',True),('turn_budget',False)]:
            def mutation(d,k=key,v=value):
                def update(x):
                    if k=='turn':x['approaches'][0][k]=v
                    else:x[k]=v
                change_doc(d,'LEDGER.json',update)
            case('ledger regression '+key+' '+type(value).__name__,mutation,direct=True,accept=not args.ledger_hardened)
        need(before==snapshot(frozen),'frozen archive extraction mutated')
        receipt.update(frozen_files_unchanged=True,independent_case_count=len(receipt['controls'])//3,independent_run_count=len(receipt['controls']),ledger_regression_case_count=len(receipt['ledger_regression'])//3,ledger_hardened=args.ledger_hardened)
        print(json.dumps(receipt,indent=2,sort_keys=True))
    finally:unlock(work);shutil.rmtree(work)
if __name__=='__main__':main()
