#!/usr/bin/env python3
"""Adversarial package controls, including repinned mathematical mutations."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode=True
import verify

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(root,flag,pin):
    args=[sys.executable,'-B']+([flag] if flag else [])+[str(root/'verify.py'),'--manifest-sha',pin]
    return subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

def repin(root):
    m=json.loads((root/'MANIFEST.json').read_text())
    m['files']['certificate.json']={'sha256':sha(root/'certificate.json'),'bytes':(root/'certificate.json').stat().st_size}
    (root/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    return sha(root/'MANIFEST.json')

def mutate(c,name):
    if name=='good_count': c['curves']['713']['good_factors'][1]['count_p']+=1
    elif name=='node_sign': c['curves']['713']['bad_factors'][0]['epsilon']*=-1
    elif name=='theta_index': c['borcherds_inputs'][0]['index']+=1
    elif name=='residual_group': c['residual']['713']['group']='S6'
    elif name=='false_solution': c['status']='SOLVED'
    elif name=='boolean_for_integer': c['borcherds_inputs'][0]['m']=True
    elif name=='twist_conductor': c['finite_match_control']['new_conductor_multiplier']=1
    else: raise verify.VerificationError('unknown mutation')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--manifest-sha',required=True); a=p.parse_args()
    original=Path(__file__).resolve().parent
    verify.verify_inventory(original,a.manifest_sha)
    cert=json.loads((original/'certificate.json').read_text())
    report={'modes':[],'positive_relocated_runs':0,'rejected_mathematical_mutations':0,'rejected_integrity_mutations':0}
    for flag in ('','-O','-OO'):
        mode=flag or 'normal'; report['modes'].append(mode)
        with tempfile.TemporaryDirectory(prefix='borcherds-replay-') as td:
            base=Path(td)/'positive';shutil.copytree(original,base)
            r=run(base,flag,a.manifest_sha)
            verify.need(r.returncode==0 and 'PASS_BOUNDED_ARITHMETIC_ONLY' in r.stdout,'relocated positive replay failed: '+r.stderr)
            report['positive_relocated_runs']+=1
            for name in ('good_count','node_sign','theta_index','residual_group','false_solution','boolean_for_integer','twist_conductor'):
                root=Path(td)/name;shutil.copytree(original,root)
                c=copy.deepcopy(cert);mutate(c,name)
                (root/'certificate.json').write_text(json.dumps(c,indent=2,sort_keys=True)+'\n')
                # Rebind inventory deliberately: the arithmetic layer must catch this, not a stale hash.
                pin=repin(root);r=run(root,flag,pin)
                verify.need(r.returncode==2 and 'arithmetic certificate mismatch' in r.stderr,
                            'mathematical negative control not rejected: '+mode+'/'+name)
                report['rejected_mathematical_mutations']+=1
            for name in ('wrong_pin','missing_file','extra_file','changed_proof','symlink'):
                root=Path(td)/name;shutil.copytree(original,root)
                pin=a.manifest_sha
                if name=='wrong_pin': pin='0'*64; marker='manifest pin mismatch'
                elif name=='missing_file': (root/'RESULT.md').unlink();marker='packet inventory mismatch'
                elif name=='extra_file': (root/'unexpected.txt').write_text('unlisted');marker='packet inventory mismatch'
                elif name=='changed_proof':
                    with (root/'RESULT.md').open('a') as f:f.write('\ncorruption\n')
                    marker='file hash mismatch'
                else: (root/'unlisted_link').symlink_to('RESULT.md');marker='symlink forbidden'
                r=run(root,flag,pin)
                verify.need(r.returncode==2 and marker in r.stderr,'integrity negative control not rejected: '+mode+'/'+name)
                report['rejected_integrity_mutations']+=1
    report['status']='PASS_NEGATIVE_CONTROLS_ONLY'
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':
    try: main()
    except Exception as error:
        print('NEGATIVE_CONTROL_ERROR: '+str(error),file=sys.stderr)
        raise SystemExit(2)
