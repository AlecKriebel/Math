#!/usr/bin/env python3
"""Additional independent hostile tests of the pinned author packet.
All mutations are confined to disposable copies. A new caller-chosen manifest
is used only to exercise parser validation, never as authenticity evidence.
"""
import argparse, hashlib, json, os
from pathlib import Path
import shutil, subprocess, sys, tempfile

MANIFEST='4a68c2510b717b1e6e4afcf267fdc0b40bf97a8156eab1c4c44c51f65e7410da'
BOOTSTRAP='b79a21252ad5d12e5cf44bed4543578d15226f15ed12c2d2594fa79697e9a950'
VERIFIER='7fb843326a441b6898836dc50b59fea41a6c9bf071352ad3470008a76f84e469'
def need(value, message):
    if not value:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(base):
    return {str(p.relative_to(base)):[sha(p),p.stat().st_mode & 0o777] for folder in ['packet','freeze'] for p in sorted((base/folder).iterdir())}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('author');args=ap.parse_args();base=Path(args.author).resolve()
    need(sys.flags.isolated==1 and os.geteuid()!=0,'isolated nonroot process required')
    need(sha(base/'freeze/FREEZE_MANIFEST.json')==MANIFEST and sha(base/'freeze/bootstrap.py')==BOOTSTRAP and sha(base/'packet/verify.py')==VERIFIER,'external author pins')
    before=snapshot(base);results=[]
    mutations=[
      ('duplicate status key','STATUS.json',lambda raw:raw[:-2]+b', "status":"unsolved"}\n'),
      ('duplicate ledger key','LEDGER.json',lambda raw:raw[:-2]+b', "schema":"erdos-cycle-sets-ledger-v1"}\n'),
      ('nonfinite source metadata','SOURCES.json',lambda raw:raw.replace(b'"checked_utc": "2026-10-08"',b'"checked_utc": Infinity')),
      ('invalid UTF8 status','STATUS.json',lambda raw:b'\xff'),
      ('UTF8 BOM ledger','LEDGER.json',lambda raw:b'\xef\xbb\xbf'+raw),
      ('trailing source text','SOURCES.json',lambda raw:raw+b' false'),
      ('float problem id','STATUS.json',lambda raw:raw.replace(b'"problem_id": 1919',b'"problem_id": 1919.0')),
      ('zero numeric formal status','STATUS.json',lambda raw:raw.replace(b'"formal_certification": false',b'"formal_certification": 0')),
      ('missing required source flag','SOURCES.json',lambda raw:raw.replace(b'"source_documents_included": false,',b'')),
    ]
    # json.loads(bytes) intentionally accepts a BOM, whereas the packet parser
    # receives bytes too. Record this benign format behavior separately.
    strict_cases=[x for x in mutations if x[0]!='UTF8 BOM ledger']
    for mode in [[],['-O'],['-OO']]:
      for name,filename,mutate in strict_cases:
        with tempfile.TemporaryDirectory(prefix='cycle-audit-') as rawdir:
          d=Path(rawdir)
          for folder in ['packet','freeze']:
            shutil.copytree(base/folder,d/folder);(d/folder).chmod(0o755)
            for p in (d/folder).iterdir():p.chmod(0o644)
          p=d/'packet'/filename;p.write_bytes(mutate(p.read_bytes()))
          mf=d/'freeze/FREEZE_MANIFEST.json';m=json.loads(mf.read_bytes());m['files'][filename]={'bytes':p.stat().st_size,'sha256':sha(p)};mf.write_text(json.dumps(m))
          cmd=[sys.executable,'-I','-B',*mode,str(base/'packet/verify.py'),'--packet',str(d/'packet'),'--manifest',str(mf),'--manifest-sha256',sha(mf)]
          result=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
          need(result.returncode!=0,'parser accepted '+name)
          boot=subprocess.run([sys.executable,'-I','-B',*mode,str(d/'freeze/bootstrap.py'),str(d/'packet')],capture_output=True,text=True,timeout=30)
          need(boot.returncode!=0,'bootstrap accepted repinned '+name)
          results.append({'case':name,'optimize':len(mode) and (2 if mode==['-OO'] else 1) or 0,'parser_rejected':True,'fixed_bootstrap_rejected':True})
      # Probe the exact semantic scope, rather than calling the parser complete.
      with tempfile.TemporaryDirectory(prefix='cycle-audit-semantic-') as rawdir:
        d=Path(rawdir)
        for folder in ['packet','freeze']:
          shutil.copytree(base/folder,d/folder);(d/folder).chmod(0o755)
          for p in (d/folder).iterdir():p.chmod(0o644)
        p=d/'packet/LEDGER.json';ledger=json.loads(p.read_bytes());ledger['approaches'][0]['turn']=True;p.write_text(json.dumps(ledger))
        mf=d/'freeze/FREEZE_MANIFEST.json';m=json.loads(mf.read_bytes());m['files']['LEDGER.json']={'bytes':p.stat().st_size,'sha256':sha(p)};mf.write_text(json.dumps(m))
        direct=subprocess.run([sys.executable,'-I','-B',*mode,str(base/'packet/verify.py'),'--packet',str(d/'packet'),'--manifest',str(mf),'--manifest-sha256',sha(mf)],capture_output=True,text=True,timeout=30)
        boot=subprocess.run([sys.executable,'-I','-B',*mode,str(d/'freeze/bootstrap.py'),str(d/'packet')],capture_output=True,text=True,timeout=30)
        need(direct.returncode==0 and boot.returncode!=0,'semantic boundary probe changed')
        results.append({'case':'boolean ledger turn under caller-repinned manifest','optimize':len(mode) and (2 if mode==['-OO'] else 1) or 0,'direct_verifier_accepts':True,'fixed_bootstrap_rejected':True,'interpretation':'Nonblocking semantic-validation limitation outside externally pinned authenticity contract.'})
    need(snapshot(base)==before,'author frozen files changed')
    print(json.dumps({'schema':'erdos-cycle-sets-extra-integrity-v1','uid':os.geteuid(),'results':results,'strict_parser_cases':len(strict_cases),'strict_parser_runs':len(strict_cases)*3,'all_fixed_bootstrap_mutations_rejected':True,'semantic_limitations':1,'author_frozen_bytes_and_modes_unchanged':True,'manifest_sha256':MANIFEST},indent=2))
if __name__=='__main__':main()
