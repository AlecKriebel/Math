#!/usr/bin/env python3
"""Recheck endpoint dependency proof objects, retaining explicit trust boundaries.
Requires a previously successful full project runner receipt with matching source
snapshot. This does not authenticate cached Mathlib definitions against sources.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, sys
HERE=Path(__file__).resolve().parent
CHECKER=HERE/'verifier_probes/ReplayClosure.lean'
EXPECTED_COMMIT='6caaee842e9495688c1567e78c0e68dbb96942aa'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text())
def write(path,obj): path.write_text(json.dumps(obj,indent=2)+'\n')
def snapshot(root):
    files=[root/n for n in ['Bell.lean','lakefile.toml','lake-manifest.json','lean-toolchain','environment/pins.json','reports/declarations.json','reports/source_completion/source_inventory.json']]
    for directory in ['Bell','validation','scripts']:
        files.extend(p for p in (root/directory).rglob('*') if p.is_file() and p.suffix in {'.lean','.py','.sh'} and '__pycache__' not in p.parts)
    return {p.relative_to(root).as_posix():sha(p) for p in sorted(set(files))}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=HERE.parent/'bell_lean')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--lake',default='lake')
    ap.add_argument('--timeout',type=int,default=1800)
    a=ap.parse_args();root=a.root.resolve();out=(a.output or HERE/'replay_runs'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')).resolve();out.mkdir(parents=True,exist_ok=False)
    report={'status':'running','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(root),'commands':[],
      'trust_boundary':'Pinned Lean compiler/kernel/runtime and canonical Init are trusted. Imported safe proof bodies in the endpoint closure are replayed into an empty kernel environment. This is not another kernel implementation, a Mathlib source rebuild, or proof of source-to-cache correspondence for Mathlib definitions.'}
    env=dict(os.environ);env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
    def command(args,label,marker=None):
        log=out/(label+'.log')
        with log.open('w') as f:
            result=subprocess.run(args,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=a.timeout)
        text=log.read_text();report['commands'].append({'argv':args,'exit_code':result.returncode,'log':log.name,'sha256':sha(log)});write(out/'receipt.json',report)
        if result.returncode or re.search(r'\bPANIC\b|\berror:|uncaught exception|deep recursion',text):raise RuntimeError(f'{label} failed; inspect {log}')
        if marker and marker not in text:raise RuntimeError(f'{label}: success marker absent')
        return text
    try:
        before=snapshot(root);report['source_snapshot']=before
        pointer=read(root/'reports/latest_run.json');baseline=read(root/pointer['directory']/'kernel_report.json')
        if baseline.get('status')!='passed' or baseline.get('last_stage')!='complete' or baseline.get('run_id')!=pointer['run_id'] or baseline.get('source_snapshot')!=before:raise RuntimeError('Current source does not match a successful full-run receipt')
        report['source_build_run_id']=pointer['run_id'];checker_before={str(p.relative_to(HERE)):sha(p) for p in [CHECKER,Path(__file__).resolve()]};report['checker_snapshot']=checker_before
        version=command([a.lake,'env','lean','--version'],'compiler_version');commit=command([a.lake,'env','lean','--githash'],'compiler_commit')
        if not re.search(r'\bversion 4\.19\.0(?=[,\s)]|$)',version) or commit.strip()!=EXPECTED_COMMIT:raise RuntimeError('Wrong compiler identity')
        prefix=[a.lake,'env','lean','-s','262144','--run',str(CHECKER)]
        command(prefix+['controls'],'controls','PASS positive, malformed-proof, retyped-axiom, and changed-core controls')
        command(prefix+['inventory',str(out/'inventory_before.json')],'inventory','PASS dependency inventory only;')
        inventory=read(out/'inventory_before.json');artifacts={str((root/Path(m['olean'])).resolve()):sha(root/Path(m['olean'])) for m in inventory['modules']};write(out/'compiled_input_hashes.json',artifacts)
        text=command(prefix+['main',str(out/'inventory_replayed.json')],'main','PASS main-endpoint empty-environment replay;')
        after_inventory=read(out/'inventory_replayed.json')
        if inventory!=after_inventory:raise RuntimeError('Dependency inventory changed between preparation and replay')
        if any(sha(Path(p))!=h for p,h in artifacts.items()):raise RuntimeError('Compiled proof inputs changed during replay')
        if before!=snapshot(root) or checker_before!={str(p.relative_to(HERE)):sha(p) for p in [CHECKER,Path(__file__).resolve()]}:raise RuntimeError('Source/checker changed during replay')
        report.update(status='passed',closure_constants=len(inventory['constants']),compiled_modules=len(artifacts),all_compiled_input_hashes_unchanged=True,all_source_and_checker_hashes_unchanged=True)
    except BaseException as ex:
        report['status']='failed';report['error']=str(ex);raise
    finally:
        report['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write(out/'receipt.json',report)
    print(json.dumps({k:report[k] for k in ['status','source_build_run_id','closure_constants','compiled_modules']},indent=2))
if __name__=='__main__':main()
