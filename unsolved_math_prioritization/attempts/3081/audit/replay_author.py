#!/usr/bin/env python3
"""Fresh isolated relocation, semantic/integrity controls, and opt-in private replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent
A='EMPTY_MONOCHROMATIC_3081_AUTHOR_SAFE_FREEZE.zip'
M='EMPTY_MONOCHROMATIC_3081_AUTHOR_EXTERNAL_MANIFEST.json'
AP=(15603,'0edf7b3e9c4b7cfc72c0f194cc9a62da4ecf6d946b63e7d1b74e6c4afda41fd1')
MP=(1917,'5d974f4db3baa61297b08dfb753550956951b6c983b5cefe937ec6cc8efec885')

def need(ok,msg):
    if not ok:raise ValueError(msg)

def check_pin(path,pin):
    b=path.read_bytes();need((len(b),hashlib.sha256(b).hexdigest())==pin,'immutable external pin mismatch')

def reseal(root):
    p=root/'MANIFEST.json';m=json.loads(p.read_text())
    for r in m['files']:
        b=(root/r['name']).read_bytes();r['bytes']=len(b);r['sha256']=hashlib.sha256(b).hexdigest()
    p.write_text(json.dumps(m,indent=2)+'\n')

def mutate(root,mode,base):
    if mode=='changed_member':(root/'REPORT.md').write_text('changed\n');return
    if mode=='missing_member':(root/'REPORT.md').unlink();return
    if mode=='unexpected_member':(root/'EXTRA').write_text('extra\n');return
    if mode=='hidden_member':(root/'.hidden').write_text('extra\n');return
    if mode=='symlink_member':
        p=root/'REPORT.md';b=p.read_bytes();outside=base/'outside-report';outside.write_bytes(b);p.unlink();p.symlink_to(outside);return
    if mode=='duplicate_manifest':
        p=root/'MANIFEST.json';m=json.loads(p.read_text());m['files'].append(m['files'][0]);p.write_text(json.dumps(m));return
    p=root/'certificate.json';x=json.loads(p.read_text())
    if mode=='false_interior_resealed':x['monochromatic_triangles'][0]['inside']=[1]
    elif mode=='duplicate_geometry_resealed':x['points'][0]=x['points'][1]
    elif mode=='collinear_geometry_resealed':x['points'][0]=[2*x['points'][1][j]-x['points'][2][j] for j in range(2)]
    elif mode=='unbalanced_resealed':x['colors'][0]=1
    elif mode=='false_count_resealed':x['E0']=1
    elif mode=='wrong_scope_resealed':x['scope']='asymptotic counterexample'
    else:raise ValueError('unknown control')
    p.write_text(json.dumps(x,indent=2)+'\n');reseal(root)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus-dir',type=Path);parser.add_argument('--source-dir',type=Path)
    a=parser.parse_args();check_pin(ROOT/A,AP);check_pin(ROOT/M,MP)
    results=[]
    def run(label,optimized,root,base,args=(),wanted=True,script='checker.py'):
        cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/script)]+list(args)
        # -I intentionally ignores a hostile PYTHONPATH and user's local site setup.
        proc=subprocess.run(cmd,cwd=base,capture_output=True,text=True,env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'PYTHONPATH':str(base/'poison'),'HOME':str(base/'unrelated-home')},timeout=120)
        need((proc.returncode==0)==wanted,'unexpected result '+label+': '+proc.stderr)
        row={'case':label,'optimized':optimized,'isolated':True,'bytecode_disabled':True,'relocated':True,'returncode':proc.returncode,'expected_pass':wanted}
        if wanted:
            out=json.loads(proc.stdout);need(out['status']=='PASS','non-PASS output')
            if script=='checker.py':
                need(out['certificate']['E0']==0 and out['certificate']['E1']==8,'wrong positive geometry')
                need(len(out['family'])==15 and out['family'][-1]['blocked_fan_incidences']==31,'wrong family positive result')
                row.update(certificate=out['certificate'],corpora=out['corpora'],sources=out['sources'])
            else:
                need(len(out['cases'])==12,'author self-test coverage');row['self_test_cases']=out['cases']
        else:row['diagnostic']=proc.stderr.strip()
        results.append(row)
    with tempfile.TemporaryDirectory(prefix='independent-3081-relocated-') as td:
        base=Path(td);original=base/'trusted-original';original.mkdir()
        with zipfile.ZipFile(ROOT/A) as z:
            names=z.namelist();need(len(names)==len(set(names))==10,'archive membership')
            need(all('/' not in n and '\\' not in n and n not in ('.','..') for n in names),'unsafe archive names')
            z.extractall(original)
        corpus_args=[];source_args=[]
        if a.corpus_dir:
            private=base/'relocated-private-corpora';private.mkdir()
            for option,name in [('catalog','catalog.json'),('problems','problems.json'),('reports','research_results.json')]:
                shutil.copyfile(a.corpus_dir/name,private/name);corpus_args+=['--'+option,str(private/name)]
        if a.source_dir:
            src=base/'relocated-private-sources';src.mkdir()
            for row in json.loads((original/'SOURCE_VERIFICATION.json').read_text())['retrievals']:
                if row.get('status')==200:shutil.copyfile(a.source_dir/row['filename'],src/row['filename'])
            source_args=['--source-dir',str(src)]
        modes=['changed_member','missing_member','unexpected_member','hidden_member','symlink_member','duplicate_manifest','false_interior_resealed','duplicate_geometry_resealed','collinear_geometry_resealed','unbalanced_resealed','false_count_resealed','wrong_scope_resealed']
        for optimized in (False,True):
            run('fresh_relocated_positive',optimized,original,base)
            if corpus_args or source_args:run('fresh_relocated_complete_private_inputs',optimized,original,base,corpus_args+source_args)
            run('original_self_test',optimized,original,base,script='self_test.py')
            for mode in modes:
                target=base/(mode+str(optimized));shutil.copytree(original,target);mutate(target,mode,base)
                run(mode,optimized,target,base,wanted=False)
            run('incomplete_corpus_arguments',optimized,original,base,['--catalog',str(base/'absent')],wanted=False)
            if corpus_args:
                catalog=private/'catalog.json';good=catalog.read_bytes();catalog.write_bytes(good+b'\n')
                run('changed_complete_corpus',optimized,original,base,corpus_args,wanted=False);catalog.write_bytes(good)
            if source_args:
                source=src/'original_2008.pdf';good=source.read_bytes();source.write_bytes(good+b'\n')
                run('changed_source_bytes',optimized,original,base,source_args,wanted=False);source.write_bytes(good)
            # Tampered archive with re-sealed external metadata still must not pass immutable pinning.
            bad=base/('repacked'+str(optimized)+'.zip')
            with zipfile.ZipFile(bad,'w') as z:
                for p in sorted(original.iterdir()):z.writestr(p.name,p.read_bytes()+ (b'\n' if p.name=='REPORT.md' else b''))
            manifest=json.loads((ROOT/M).read_text());raw=bad.read_bytes();manifest['archive']['bytes']=len(raw);manifest['archive']['sha256']=hashlib.sha256(raw).hexdigest()
            badm=base/('repacked'+str(optimized)+'.json');badm.write_text(json.dumps(manifest))
            cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(ROOT/'independent_check.py'),'--archive',str(bad),'--external-manifest',str(badm),'--skip-family']
            proc=subprocess.run(cmd,cwd=base,capture_output=True,text=True,timeout=120)
            need(proc.returncode!=0 and 'external pin mismatch' in proc.stderr,'repacked original accepted')
            results.append({'case':'repacked_original_resealed_external','optimized':optimized,'isolated':True,'returncode':proc.returncode,'expected_pass':False,'diagnostic':proc.stderr.strip()})
    print(json.dumps({'status':'PASS','cases':results,'case_count':len(results),'private_corpora_relocated':bool(corpus_args),'private_sources_relocated':bool(source_args),'note':'Failures were checked by explicit exceptions and exit status, not removable assert statements.'},indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,TypeError,subprocess.TimeoutExpired) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
