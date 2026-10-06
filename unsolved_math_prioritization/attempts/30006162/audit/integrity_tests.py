#!/usr/bin/env python3
"""Mutation and relocation controls on temporary copies only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(ok,message):
    if not ok:
        raise RuntimeError(message)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def run(verifier,root,pin,opt,cwd):
    command=[sys.executable,'-I','-B']+(['-O'] if opt else [])
    command += [str(verifier),'--root',str(root),'--manifest-sha256',pin]
    return subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=90)
def rebind(root,name):
    path=root/'MANIFEST.json'
    manifest=json.loads(path.read_bytes())
    data=(root/name).read_bytes()
    manifest['files'][name]={'bytes':len(data),'sha256':digest(data)}
    path.write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    return digest(path.read_bytes())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',required=True)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    original=Path(args.root).absolute()
    verifier=original/'verify_audit.py'
    labels=['report_tamper','checker_tamper','receipt_tamper','undeclared_file','missing_file',
        'empty_directory','cache_directory','loose_bytecode','payload_symlink','directory_symlink',
        'root_symlink','fifo','manifest_tamper','rehashed_payload_stale_pin',
        'rebound_checker_execution','rebound_expected_receipt','rebound_target_answer',
        'rebound_verifier_source']
    results=[]
    with tempfile.TemporaryDirectory(prefix='surface-audit-integrity-') as td:
        td=Path(td); elsewhere=td/'elsewhere';elsewhere.mkdir()
        for opt in (False,True):
            baseline=run(verifier,original,args.manifest_sha256,opt,elsewhere)
            require(baseline.returncode==0,'baseline failed: '+baseline.stderr)
            moved=td/('relocated_'+str(opt));shutil.copytree(original,moved)
            relocated=run(moved/'verify_audit.py',moved,args.manifest_sha256,opt,elsewhere)
            require(relocated.returncode==0 and relocated.stdout==baseline.stdout,'relocation failed')
            for index,label in enumerate(labels):
                root=td/('case_'+str(opt)+'_'+str(index));shutil.copytree(original,root)
                checkroot=root;pin=args.manifest_sha256
                if label in ['report_tamper','checker_tamper','receipt_tamper','rehashed_payload_stale_pin']:
                    name={'report_tamper':'REVIEW.md','checker_tamper':'independent_checks.py',
                          'receipt_tamper':'INDEPENDENT_RESULTS.json','rehashed_payload_stale_pin':'REVIEW.md'}[label]
                    with (root/name).open('a') as f:f.write('\nTampered.\n')
                    if label=='rehashed_payload_stale_pin':rebind(root,name)
                elif label=='undeclared_file':(root/'extra.json').write_text('{}')
                elif label=='missing_file':(root/'README.md').unlink()
                elif label=='empty_directory':(root/'empty').mkdir()
                elif label=='cache_directory':
                    (root/'__pycache__').mkdir();(root/'__pycache__'/'independent_checks.cpython-312.pyc').write_bytes(b'bad')
                elif label=='loose_bytecode':(root/'independent_checks.pyc').write_bytes(b'bad')
                elif label=='payload_symlink':
                    (root/'README.md').unlink();(root/'README.md').symlink_to(original/'README.md')
                elif label=='directory_symlink':(root/'linked').symlink_to(elsewhere,target_is_directory=True)
                elif label=='root_symlink':
                    checkroot=td/('root_link_'+str(opt));checkroot.symlink_to(root,target_is_directory=True)
                elif label=='fifo':os.mkfifo(root/'pipe.json')
                elif label=='manifest_tamper':
                    with (root/'MANIFEST.json').open('a') as f:f.write(' ')
                elif label=='rebound_checker_execution':
                    (root/'independent_checks.py').write_text("raise RuntimeError('INDEPENDENT_EXECUTION_SENTINEL')\n")
                    pin=rebind(root,'independent_checks.py')
                elif label=='rebound_expected_receipt':
                    obj=json.loads((root/'INDEPENDENT_RESULTS.json').read_bytes());obj['checks']+=1
                    (root/'INDEPENDENT_RESULTS.json').write_text(json.dumps(obj))
                    pin=rebind(root,'INDEPENDENT_RESULTS.json')
                elif label=='rebound_target_answer':
                    obj=json.loads((root/'SUMMARY.json').read_bytes());obj['target_answers']['sphere']='solved'
                    (root/'SUMMARY.json').write_text(json.dumps(obj))
                    pin=rebind(root,'SUMMARY.json')
                elif label=='rebound_verifier_source':
                    with (root/'verify_audit.py').open('a') as f:f.write('\n# changed verifier\n')
                    pin=rebind(root,'verify_audit.py')
                result=run(verifier,checkroot,pin,opt,elsewhere)
                require(result.returncode!=0,'accepted mutation: '+label)
                if label=='rebound_checker_execution':
                    require('INDEPENDENT_EXECUTION_SENTINEL' in result.stderr,'source sentinel not executed')
                results.append({'mutation':label,'optimized':opt,'rejected':True})
    print(json.dumps({'schema':1,'problem_id':30006162,'status':'PASS',
        'normal_and_optimized_baselines':True,'normal_and_optimized_relocation':True,
        'negative_controls':len(results),'cases':results,
        'scope':'Integrity and source-execution controls, not mathematical theorem verification.'},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,TypeError,KeyError,RuntimeError,subprocess.TimeoutExpired) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
