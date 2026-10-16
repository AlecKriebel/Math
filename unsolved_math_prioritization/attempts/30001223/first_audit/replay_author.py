#!/usr/bin/env python3
"""Externally pinned author archive replay and adversarial mutation controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PIN='e82e3a8349c00e74199090c3463918f5a83b915d85003438fa030adabf797978'
SIZE=12753
NAMES={'README.md','audit.py','case.json','expected_results.json','manifest.json','proof.md','sources.json','verify.py'}

def need(ok,msg):
    if not ok:
        raise ValueError(msg)

def check_tree(root):
    need(stat.S_ISDIR(root.lstat().st_mode),'not a regular root directory')
    entries={p.name:p for p in root.iterdir()}
    need(set(entries)==NAMES,'inventory mismatch')
    need(all(stat.S_ISREG(p.lstat().st_mode) for p in entries.values()),'nonregular member')
    m=json.loads(entries['manifest.json'].read_text())
    need(set(m)=={'schema','files'} and m['schema']=='young-tops-safe-v1','manifest schema')
    need(set(m['files'])==NAMES-{'manifest.json'},'manifest inventory')
    for n,d in m['files'].items():
        b=entries[n].read_bytes()
        need(set(d)=={'bytes','sha256'},'metadata keys')
        need(type(d['bytes']) is int and d['bytes']==len(b),'size')
        need(d['sha256']==hashlib.sha256(b).hexdigest(),'hash')

def repin(root,name):
    p=root/name; m=json.loads((root/'manifest.json').read_text());b=p.read_bytes()
    m['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (root/'manifest.json').write_text(json.dumps(m,sort_keys=True))

def mutate(root,kind):
    if kind in ('source','proof','case','expected'):
        name={'source':'verify.py','proof':'proof.md','case':'case.json','expected':'expected_results.json'}[kind]
        p=root/name;p.write_bytes(p.read_bytes()+b' ')
    elif kind=='cache':
        (root/'__pycache__').mkdir();(root/'__pycache__'/'verify.pyc').write_bytes(b'bad cache')
    elif kind=='unexpected_file':(root/'other.txt').write_text('extra')
    elif kind=='missing':(root/'case.json').unlink()
    elif kind in ('directory','symlink','fifo'):
        p=root/'case.json';p.unlink()
        if kind=='directory':p.mkdir()
        elif kind=='symlink':p.symlink_to('proof.md')
        else:os.mkfifo(p)
    elif kind in ('schema','manifest_extra','manifest_entry'):
        p=root/'manifest.json';m=json.loads(p.read_text())
        if kind=='schema':m['schema']='bad'
        elif kind=='manifest_extra':m['unexpected']=True
        else:m['files']['other.txt']={'bytes':0,'sha256':'0'*64}
        p.write_text(json.dumps(m))
    elif kind=='repinned_false_result':
        p=root/'expected_results.json';m=json.loads(p.read_text());m['sym5_coefficient_span_rank']=35
        p.write_text(json.dumps(m));repin(root,p.name)
    elif kind=='repinned_wrong_case':
        p=root/'case.json';m=json.loads(p.read_text());m['characteristic']=2
        p.write_text(json.dumps(m));repin(root,p.name)
    else:raise ValueError('unknown mutation')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('author_zip',type=Path);a=ap.parse_args()
    need(stat.S_ISREG(a.author_zip.lstat().st_mode),'archive must be regular')
    b=a.author_zip.read_bytes();need(len(b)==SIZE and hashlib.sha256(b).hexdigest()==PIN,'external archive pin mismatch')
    results=[]
    with tempfile.TemporaryDirectory(prefix='young-tops-replay-') as td:
        base=Path(td);frozen=base/'frozen';frozen.mkdir()
        with zipfile.ZipFile(a.author_zip) as z:
            infos=z.infolist();need(len(infos)==len(NAMES) and {i.filename for i in infos}==NAMES,'archive inventory')
            for i in infos:
                mode=i.external_attr>>16
                need(not i.is_dir() and (stat.S_IFMT(mode) in (0,stat.S_IFREG)),'nonregular archive member')
                (frozen/i.filename).write_bytes(z.read(i))
        check_tree(frozen)
        source=(frozen/'verify.py').read_bytes()
        for optimize in (False,True):
            flags=['-B']+(['-O'] if optimize else [])
            for case in ['baseline','relocation','source','proof','case','expected','cache','unexpected_file','missing','directory','symlink','fifo','schema','manifest_extra','manifest_entry','repinned_false_result','repinned_wrong_case']:
                dest=base/('optimized' if optimize else 'normal')/case/'path with spaces'/'root'
                shutil.copytree(frozen,dest)
                if case not in ('baseline','relocation'):mutate(dest,case)
                run=subprocess.run([sys.executable,*flags,str(dest/'audit.py')],cwd=base,capture_output=True,text=True,timeout=30)
                positive=case in ('baseline','relocation')
                passed=(run.returncode==0) if positive else (run.returncode!=0 and 'REJECT:' in run.stderr)
                need(passed,'unexpected outcome: '+case+' '+run.stderr)
                row={'case':case,'optimized':optimize,'passed':passed,'returncode':run.returncode}
                if positive:
                    report=json.loads(run.stdout);need(report['status']=='PASS','bad positive result');row['source_sha256']=report['verified_source_sha256']
                else:row['rejection']=run.stderr.strip().splitlines()[-1]
                results.append(row)
        print(json.dumps({'status':'PASS','author_archive':{'sha256':PIN,'bytes':SIZE},'source':{'sha256':hashlib.sha256(source).hexdigest(),'bytes':len(source)},'checks':results,'scope':'Externally pinned immutable archive plus normal, optimized, relocation and mutation checks. Manifest hashes alone are not an authenticity guarantee.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
