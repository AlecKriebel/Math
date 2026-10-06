#!/usr/bin/env python3
"""Independent normal/optimized relocation and adversarial inventory campaign."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile


def require(value, message):
    if not value:
        raise RuntimeError(message)


def hashed(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def run():
    source=Path(__file__).resolve().parent
    pins=json.loads((source/'CODE_PINS.json').read_text())['files']
    for name in ('independent_checks.py','verify_audit.py','test_audit_package.py'):
        require(hashed((source/name).read_bytes())==pins[name], 'initial executable pin: '+name)
    def execute(root,opt):
        return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(root/'verify_audit.py')],
            cwd='/tmp',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=90,check=False)
    def update_manifest(root,name):
        p=root/'MANIFEST.json'; manifest=json.loads(p.read_text())
        manifest['files'][name]=hashed((root/name).read_bytes())
        p.write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix='exchangeable-independent-audit-') as temp:
        temp=Path(temp)
        pristine=temp/'relocated package with spaces'; shutil.copytree(source,pristine)
        for opt in (False,True):
            result=execute(pristine,opt)
            require(result.returncode==0,'relocation: '+result.stderr.decode())
            outcomes.append({'test':'relocation','optimized':opt,'status':'PASS'})
        cases=('extra_file','missing_proof','modified_proof','empty_directory','cache_directory','cache_regular_file',
               'extra_symlink','replaced_file_symlink','fifo','socket','changed_code_updated_manifest',
               'changed_result_updated_manifest','missing_manifest','duplicate_manifest_key')
        for case in cases:
            root=temp/case; shutil.copytree(source,root); sock=None
            if case=='extra_file': (root/'EXTRA').write_text('extra')
            elif case=='missing_proof': (root/'INDEPENDENT_LEMMAS.md').unlink()
            elif case=='modified_proof':
                p=root/'INDEPENDENT_LEMMAS.md'; p.write_bytes(p.read_bytes()+b'\nmutation\n')
            elif case=='empty_directory': (root/'empty').mkdir()
            elif case=='cache_directory': (root/'__pycache__').mkdir()
            elif case=='cache_regular_file': (root/'__pycache__').write_text('cache')
            elif case=='extra_symlink': (root/'LINK').symlink_to('AUDIT.md')
            elif case=='replaced_file_symlink':
                p=root/'INDEPENDENT_LEMMAS.md'; p.unlink(); p.symlink_to(source/'INDEPENDENT_LEMMAS.md')
            elif case=='fifo': os.mkfifo(root/'FIFO')
            elif case=='socket':
                try:
                    sock=socket.socket(socket.AF_UNIX); sock.bind(str(root/'SOCKET'))
                except PermissionError:
                    if sock: sock.close()
                    for opt in (False,True):
                        outcomes.append({'test':case,'optimized':opt,'status':'NOT_RUN_ENVIRONMENT_PERMISSION_RESTRICTION'})
                    continue
            elif case=='changed_code_updated_manifest':
                p=root/'independent_checks.py'; p.write_bytes(p.read_bytes()+b'\n# modified\n'); update_manifest(root,p.name)
            elif case=='changed_result_updated_manifest':
                p=root/'INDEPENDENT_RESULTS.json'; d=json.loads(p.read_text()); d['total_checks']+=1
                p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n'); update_manifest(root,p.name)
            elif case=='missing_manifest': (root/'MANIFEST.json').unlink()
            elif case=='duplicate_manifest_key':
                p=root/'MANIFEST.json'; s=p.read_text(); p.write_text(s.replace('{','{"schema":1,',1))
            try:
                for opt in (False,True):
                    result=execute(root,opt)
                    require(result.returncode!=0 and b'FAIL:' in result.stderr, 'mutation not rejected: '+case)
                    outcomes.append({'test':case,'optimized':opt,'status':'REJECTED'})
            finally:
                if sock: sock.close()
    return {'schema':1,'status':'PASS','positive_relocation_runs':2,'mutation_types':len(cases),
            'mutation_runs':sum(o['status']=='REJECTED' for o in outcomes),
            'mutation_types_tested':len({o['test'] for o in outcomes if o['status']=='REJECTED'}),
            'not_run':sum(o['status'].startswith('NOT_RUN') for o in outcomes),'outcomes':outcomes,
            'scope':'Fail-closed package integrity; not an infinite mathematical proof.'}


if __name__=='__main__':
    try:
        print(json.dumps(run(),sort_keys=True,indent=2))
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
