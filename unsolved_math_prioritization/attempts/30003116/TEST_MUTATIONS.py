#!/usr/bin/env python3
"""Actual malformed-copy tests through an independently pinned wrapper bootstrap."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BOOTSTRAP = r'''import hashlib,os,runpy,stat,sys
p=sys.argv[1]; pin=sys.argv[2]
if not stat.S_ISREG(os.lstat(p).st_mode):
 print('BOOTSTRAP_REJECT: nonregular wrapper',file=sys.stderr);sys.exit(9)
if hashlib.sha256(open(p,'rb').read()).hexdigest()!=pin:
 print('BOOTSTRAP_REJECT: wrapper anchor mismatch',file=sys.stderr);sys.exit(9)
sys.argv=[p]+sys.argv[3:]
runpy.run_path(p,run_name='__main__')
'''


def need(x,message):
    if not x: raise RuntimeError(message)


def sha(b): return hashlib.sha256(b).hexdigest()


def write_json(path,value): path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')


def writable_copy(source,dest):
    shutil.copytree(source,dest); dest.chmod(0o755)
    for p in dest.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)


def rebind(root,name):
    path=root/'PUBLICATION_MANIFEST.json'; m=json.loads(path.read_text())
    for item in m['files']:
        if item['path']==name:
            b=(root/name).read_bytes();item.update(bytes=len(b),sha256=sha(b))
    write_json(path,m);return sha(path.read_bytes())


def run(source,manifest_pin,wrapper_pin):
    need(sha((source/'PUBLICATION_MANIFEST.json').read_bytes())==manifest_pin,'Manifest preflight mismatch')
    need(sha((source/'VERIFY_PUBLICATION.py').read_bytes())==wrapper_pin,'Wrapper preflight mismatch')
    cases=['clean','invalid_pin','stale_pin_rebinding','proof_drift','missing_file','extra_file','extra_directory','nested_extra_directory',
           'file_symlink','directory_symlink','manifest_symlink','wrapper_symlink','special_fifo','file_mode_drift','directory_mode_drift',
           'manifest_list','manifest_null','manifest_bad_json','manifest_duplicate_key','manifest_nonfinite','wrong_problem','boolean_problem',
           'boolean_rank','wrong_status','wrong_turns','wrong_anchor','source_flag_integer','outer_extra_field','inventory_null',
           'inventory_duplicate','boolean_bytes','negative_bytes','invalid_digest','wrong_mode','unsafe_path','member_extra_field',
           'frozen_manifest_drift','rebound_false_result','rebound_false_proof','rebound_bad_syntax','rebound_assert','corrected_patch_drift',
           'bootstrap_changed_wrapper','bootstrap_wrapper_and_manifest_rebinding']
    rows=[]
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')};env['PYTHONDONTWRITEBYTECODE']='1'
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='rational-orbit-mutation-') as temporary:
                temp=Path(temporary);root=temp/'packet';writable_copy(source,root);pin=manifest_pin
                mp=root/'PUBLICATION_MANIFEST.json';m=json.loads(mp.read_text())
                if case=='invalid_pin':pin='invalid'
                elif case=='stale_pin_rebinding':
                    p=root/'README.md';p.write_bytes(p.read_bytes()+b'\nDrift.\n');rebind(root,'README.md')
                elif case=='proof_drift':
                    p=root/'original/03_difference_amplification.md';p.write_bytes(p.read_bytes()+b'\nDrift.\n')
                elif case=='missing_file':(root/'original/README.md').unlink()
                elif case=='extra_file':(root/'extra.md').write_text('extra')
                elif case=='extra_directory':(root/'extra').mkdir()
                elif case=='nested_extra_directory':(root/'original/extra').mkdir()
                elif case in ('file_symlink','wrapper_symlink'):
                    p=root/('README.md' if case=='file_symlink' else 'VERIFY_PUBLICATION.py');b=p.read_bytes();p.unlink();q=temp/'target';q.write_bytes(b);p.symlink_to(q)
                elif case=='directory_symlink':
                    p=root/'original';q=temp/'original';p.rename(q);p.symlink_to(q,target_is_directory=True)
                elif case=='manifest_symlink':b=mp.read_bytes();mp.unlink();q=temp/'manifest';q.write_bytes(b);mp.symlink_to(q)
                elif case=='special_fifo':os.mkfifo(root/'extra.md')
                elif case=='file_mode_drift':(root/'README.md').chmod(0o600)
                elif case=='directory_mode_drift':(root/'original').chmod(0o700)
                elif case in ('manifest_list','manifest_null'):
                    write_json(mp,[] if case=='manifest_list' else None);pin=sha(mp.read_bytes())
                elif case=='manifest_bad_json':mp.write_text('{bad');pin=sha(mp.read_bytes())
                elif case=='manifest_duplicate_key':mp.write_bytes(mp.read_bytes().replace(b'{',b'{"problem_id":0,',1));pin=sha(mp.read_bytes())
                elif case=='manifest_nonfinite':mp.write_bytes(mp.read_bytes().replace(b'30003116',b'NaN',1));pin=sha(mp.read_bytes())
                elif case in ('wrong_problem','boolean_problem','boolean_rank','wrong_status','wrong_turns','wrong_anchor','source_flag_integer','outer_extra_field','inventory_null','inventory_duplicate','boolean_bytes','negative_bytes','invalid_digest','wrong_mode','unsafe_path','member_extra_field'):
                    if case=='wrong_problem':m['problem_id']=0
                    elif case=='boolean_problem':m['problem_id']=True
                    elif case=='boolean_rank':m['rank']=True
                    elif case=='wrong_status':m['status']='claimed_solved'
                    elif case=='wrong_turns':m['turns']='0/5'
                    elif case=='wrong_anchor':m['frozen_manifest_anchors']['original']='0'*64
                    elif case=='source_flag_integer':m['source_files_redistributed']=0
                    elif case=='outer_extra_field':m['extra']=0
                    elif case=='inventory_null':m['files']=None
                    elif case=='inventory_duplicate':m['files'].append(m['files'][0])
                    elif case=='boolean_bytes':m['files'][0]['bytes']=True
                    elif case=='negative_bytes':m['files'][0]['bytes']=-1
                    elif case=='invalid_digest':m['files'][0]['sha256']='bad'
                    elif case=='wrong_mode':m['files'][0]['mode']='0444'
                    elif case=='unsafe_path':m['files'][0]['path']='../outside.md'
                    elif case=='member_extra_field':m['files'][0]['extra']=0
                    write_json(mp,m);pin=sha(mp.read_bytes())
                elif case=='frozen_manifest_drift':
                    p=root/'original/MANIFEST.json';p.write_bytes(p.read_bytes()+b' ');pin=rebind(root,'original/MANIFEST.json')
                elif case in ('rebound_false_result','rebound_false_proof','rebound_bad_syntax','rebound_assert','corrected_patch_drift'):
                    name={'rebound_false_result':'original/checks.json','rebound_false_proof':'original/03_difference_amplification.md','rebound_bad_syntax':'original/check_math.py','rebound_assert':'original/check_math.py','corrected_patch_drift':'corrected/04_average_collision.md'}[case]
                    p=root/name
                    if case=='rebound_false_result':o=json.loads(p.read_text());o['checks']+=1;write_json(p,o)
                    elif case=='rebound_bad_syntax':p.write_text('def !\n')
                    elif case=='rebound_assert':p.write_bytes(p.read_bytes()+b'\nassert False\n')
                    else:p.write_bytes(p.read_bytes()+b'\nFalse altered theorem.\n')
                    pin=rebind(root,name)
                elif case in ('bootstrap_changed_wrapper','bootstrap_wrapper_and_manifest_rebinding'):
                    p=root/'VERIFY_PUBLICATION.py';p.write_text('raise SystemExit(0)\n')
                    if case.endswith('rebinding'):pin=rebind(root,p.name)
                wrapper=root/'VERIFY_PUBLICATION.py'
                cp=subprocess.run([sys.executable,'-I','-B',*flags,'-c',BOOTSTRAP,str(wrapper),wrapper_pin,'--packet',str(root),'--expected-manifest',pin,'--check-only'],env=env,cwd=temp,capture_output=True,timeout=30)
                expected=0 if case=='clean' else 9 if case in ('wrapper_symlink','bootstrap_changed_wrapper','bootstrap_wrapper_and_manifest_rebinding') else 1
                need(cp.returncode==expected,label+'/'+case+': '+cp.stdout.decode(errors='replace')+cp.stderr.decode(errors='replace'))
                if expected:need(cp.stderr.startswith(b'BOOTSTRAP_REJECT:' if expected==9 else b'REJECT:'),'Uncontrolled rejection')
                rows.append({'mode':label,'case':case,'returncode':cp.returncode})
    return {'status':'PASS','cases':len(rows),'clean_acceptances':3,'rejections':len(rows)-3,'bootstrap_cases':9,'results':rows,'scope':'Actual disposable-copy mutations; wrapper bytes authenticated outside the payload before executing them. Independently replacing both trust anchors remains outside the threat model.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,required=True);p.add_argument('--expected-manifest',required=True);p.add_argument('--expected-wrapper',required=True);a=p.parse_args()
    try:print(json.dumps(run(a.packet.absolute(),a.expected_manifest,a.expected_wrapper),indent=2,sort_keys=True))
    except (RuntimeError,OSError,ValueError,subprocess.SubprocessError) as error:print('FAILED: '+str(error),file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
