#!/usr/bin/env python3
"""Reject false mathematical claims and mutated packets in Python, -O and -OO."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(condition,message):
    if not condition:
        raise ValueError(message)


def run(script,mode,*args):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable,*mode,str(script),*map(str,args)],
                          capture_output=True,text=True,env=env)


def replace_claim(c,key,value,nested=False):
    target=c['mathematical_checks'] if nested else c
    target[key]=value


def rehash(root,name):
    p=root/'MANIFEST.json'
    m=json.loads(p.read_text())
    data=(root/name).read_bytes()
    matches=[x for x in m['files'] if x['name']==name]
    require(len(matches)==1,'rehash target missing')
    matches[0]['bytes']=len(data)
    matches[0]['sha256']=hashlib.sha256(data).hexdigest()
    p.write_text(json.dumps(m,indent=2)+'\n')


def main():
    root=Path(__file__).parent
    base=json.loads((root/'CLAIMS.json').read_text())
    mathematical=[
        ('zero_escape_tail','escape_tail_limit',0,True),
        ('wrong_hat_sign','hat_sign',1,True),
        ('wrong_spectral_sign','spectral_sign',1,True),
        ('coordinate_has_derivation','coordinate_derivation_dimensions',[1,0,0,0,0],True),
        ('spin_rigid','spin_derivation_dimensions',[0,0,0,0],True),
        ('permute_unequal_charges','tensor_automorphism_order',6,True),
        ('claim_full_proof','full_conjecture_proved',True,False),
        ('claim_v5_verified','han_v5_verified_as_resolution',True,False),
        ('mislabel_affine_weight_one','affine_escape_has_weight_one_zero',True,False),
        ('claim_already_solved','status','already_solved',False),
    ]
    integrity=['change_report','remove_report','add_unlisted','symlink_report',
               'rehashed_false_claim','rehashed_bad_ledger','rehashed_source_redistribution']
    details=[]
    with tempfile.TemporaryDirectory(prefix='voa-negative-') as td:
        temp=Path(td)
        for mode in [[],['-O'],['-OO']]:
            mode_name='normal' if not mode else mode[0]
            result=run(root/'verify_packet.py',mode)
            require(result.returncode==0,'positive baseline failed in '+mode_name+': '+result.stderr)
            details.append({'mode':mode_name,'kind':'positive_baseline','accepted':True})
            for name,key,value,nested in mathematical:
                c=copy.deepcopy(base)
                replace_claim(c,key,value,nested)
                p=temp/'false_claim.json'
                p.write_text(json.dumps(c))
                result=run(root/'verify_math.py',mode,'--claims',p)
                require(result.returncode!=0,'FALSE mathematical claim accepted: '+mode_name+' '+name)
                require('ValueError' in result.stderr,'unexpected negative-control failure: '+name)
                details.append({'mode':mode_name,'kind':'mathematical','fixture':name,'rejected':True})
            for name in integrity:
                target=temp/('packet_'+mode_name.replace('-','')+'_'+name)
                shutil.copytree(root,target)
                # Only disposable mutation fixtures become writable.
                target.chmod(0o700)
                for fixture_file in target.iterdir():
                    fixture_file.chmod(0o600)
                if name=='change_report':
                    with (target/'REPORT.md').open('a') as f:f.write('\nMUTATION\n')
                elif name=='remove_report':
                    (target/'REPORT.md').unlink()
                elif name=='add_unlisted':
                    (target/'unlisted.txt').write_text('extra')
                elif name=='symlink_report':
                    (target/'REPORT.md').unlink()
                    (target/'REPORT.md').symlink_to(root/'REPORT.md')
                elif name=='rehashed_false_claim':
                    c=copy.deepcopy(base);c['full_conjecture_proved']=True
                    (target/'CLAIMS.json').write_text(json.dumps(c));rehash(target,'CLAIMS.json')
                elif name=='rehashed_bad_ledger':
                    p=target/'LEDGER.json';d=json.loads(p.read_text());d['author_approaches_completed']=4
                    p.write_text(json.dumps(d));rehash(target,'LEDGER.json')
                elif name=='rehashed_source_redistribution':
                    p=target/'SOURCES.json';d=json.loads(p.read_text());d['pdf_sources'][0]['redistributed']=True
                    p.write_text(json.dumps(d));rehash(target,'SOURCES.json')
                else:
                    raise ValueError('unknown fixture '+name)
                result=run(target/'verify_packet.py',mode)
                require(result.returncode!=0,'MUTATED packet accepted: '+mode_name+' '+name)
                require('ValueError' in result.stderr,'unexpected integrity-control failure: '+name)
                details.append({'mode':mode_name,'kind':'integrity','fixture':name,'rejected':True})
    require(len(details)==54,'negative-control count mismatch')
    print(json.dumps({'ok':True,'positive_baselines':3,'mathematical_rejections':30,
                      'integrity_rejections':21,'modes':['normal','-O','-OO'],'details':details},indent=2))


if __name__=='__main__':
    main()
