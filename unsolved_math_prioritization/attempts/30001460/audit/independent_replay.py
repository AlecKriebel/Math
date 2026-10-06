#!/usr/bin/env python3
"""Independent static-file replay of a separately supplied, byte-pinned author ZIP.
No source corpora or third-party documents are read. Python standard library only.
"""
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

ZIP_SHA = '41b212dc7842cdedf598efebf41976351489115363f30ab2cb599cfa93050e34'
ZIP_BYTES = 16235
VERIFIER_SHA = 'c79a9341e612a200111114922f22a8575326c1fa972089eb13fa47c71352b87d'
CERTIFICATE_SHA = 'd5bcdd749406083c2128441b09ce545886db4745325d73d0e98c048835fb2cf0'
MANIFEST_SHA = 'af504b427d73f7f5e1651ef42d8bfef8b8f7942ace53b6d2a379025cabe4188e'
NAMES = {'APPROACHES.md','EXPECTED.json','MANIFEST.json','README.md',
         'RESULT.md','SOURCES.json','certificate.py','verify.py'}

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(path, expected):
    require(stat.S_ISREG(path.lstat().st_mode), 'pin input is not regular')
    require(sha(path.read_bytes()) == expected, 'pin mismatch: ' + path.name)

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def refresh(root):
    manifest = json.loads((root/'MANIFEST.json').read_bytes())
    for name in manifest['files']:
        path = root/name
        if path.is_file():
            data = path.read_bytes()
            manifest['files'][name] = {'bytes':len(data),'sha256':sha(data)}
    write_json(root/'MANIFEST.json',manifest)

def execute(root, optimized):
    # Anchor executable code independently of the possibly refreshed manifest.
    if sha((root/'verify.py').read_bytes()) != VERIFIER_SHA:
        return {'returncode':97,'stderr':'independent bootstrap rejected verifier pin',
                'stdout':'','verifier_executed':False}
    command = [sys.executable] + (['-O'] if optimized else [])
    command += ['-B',str(root/'verify.py')]
    proc = subprocess.run(command,cwd=root.parent,capture_output=True,text=True,timeout=30)
    return {'returncode':proc.returncode,'stderr':proc.stderr.strip(),
            'stdout':proc.stdout.strip(),'verifier_executed':True}

def replay(archive):
    data=archive.read_bytes()
    require(len(data)==ZIP_BYTES and sha(data)==ZIP_SHA,'author archive pin mismatch')
    positives=[]; negatives=[]
    with tempfile.TemporaryDirectory(prefix='independent K sheet audit ') as raw:
        work=Path(raw)
        pristine=work/'pristine';pristine.mkdir()
        with zipfile.ZipFile(archive) as z:
            infos=z.infolist()
            require(len(infos)==len(NAMES) and {i.filename for i in infos}==NAMES,
                    'archive inventory mismatch')
            for info in infos:
                require(stat.S_ISREG(info.external_attr>>16),'nonregular archive member')
                require('/' not in info.filename and '\\' not in info.filename,
                        'archive path is not flat')
                (pristine/info.filename).write_bytes(z.read(info))
        for name,expected in [('verify.py',VERIFIER_SHA),('certificate.py',CERTIFICATE_SHA),
                              ('MANIFEST.json',MANIFEST_SHA)]:
            pin(pristine/name,expected)
        for label,optimized in [('normal',False),('optimized',True),
                                ('relocated path with spaces',False),
                                ('relocated optimized path with spaces',True)]:
            root=work/label;shutil.copytree(pristine,root)
            result=execute(root,optimized)
            require(result['returncode']==0 and not result['stderr'],'baseline rejected: '+label)
            payload=json.loads(result['stdout'])
            require(payload['verified'] is True and payload['identities_passed']==23,
                    'unexpected baseline payload')
            positives.append({'control':label,'optimized':optimized,'outcome':'passed',
                              'result':payload})
        cases=['extra_file','cache_directory','unexpected_directory','missing_file',
               'tampered_report','symlink_report','fifo_node','directory_in_place',
               'manifest_missing_entry','changed_expected_refreshed_manifest',
               'changed_certificate_refreshed_manifest','changed_verifier_refreshed_manifest']
        for case in cases:
            for optimized in (False,True):
                root=work/(case+('_optimized' if optimized else '_normal'))
                shutil.copytree(pristine,root)
                if case=='extra_file': (root/'EXTRA.txt').write_text('unexpected')
                elif case=='cache_directory': (root/'__pycache__').mkdir()
                elif case=='unexpected_directory': (root/'unlisted').mkdir()
                elif case=='missing_file': (root/'RESULT.md').unlink()
                elif case=='tampered_report':
                    with (root/'RESULT.md').open('ab') as stream: stream.write(b'\nchanged\n')
                elif case=='symlink_report':
                    (root/'RESULT.md').unlink();(root/'RESULT.md').symlink_to(pristine/'RESULT.md')
                elif case=='fifo_node': os.mkfifo(root/'pipe')
                elif case=='directory_in_place':
                    (root/'EXPECTED.json').unlink();(root/'EXPECTED.json').mkdir()
                elif case=='manifest_missing_entry':
                    value=json.loads((root/'MANIFEST.json').read_bytes())
                    del value['files']['RESULT.md'];write_json(root/'MANIFEST.json',value)
                elif case=='changed_expected_refreshed_manifest':
                    value=json.loads((root/'EXPECTED.json').read_bytes())
                    value['identities_passed']=24;write_json(root/'EXPECTED.json',value);refresh(root)
                elif case in ('changed_certificate_refreshed_manifest','changed_verifier_refreshed_manifest'):
                    target='certificate.py' if case.startswith('changed_certificate') else 'verify.py'
                    (root/target).write_text('from pathlib import Path\nPath(__file__).with_name("EXECUTED_SENTINEL").write_text("executed")\n')
                    refresh(root)
                result=execute(root,optimized)
                require(result['returncode']!=0,'tamper accepted: '+case)
                require(not (root/'EXECUTED_SENTINEL').exists(),'mutated executable ran')
                negatives.append({'control':case,'optimized':optimized,'outcome':'rejected',
                                  'returncode':result['returncode'],'reason':result['stderr'],
                                  'verifier_executed':result['verifier_executed'],
                                  'execution_sentinel_absent':True})
    require(archive.read_bytes()==data,'author archive changed during audit')
    return {'schema':1,'problem_id':30001460,'author_archive_sha256':ZIP_SHA,
            'author_archive_bytes':ZIP_BYTES,'author_archive_unchanged':True,
            'positive_controls':positives,'negative_controls':negatives,
            'positive_count':len(positives),'negative_count':len(negatives),
            'scope':'sealed static-file identity and author rank-one symbolic replay; not a descent proof or a hostile-concurrent-writer security test'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--author-archive',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=replay(args.author_archive.resolve())
    if args.output:write_json(args.output,result)
    else:print(json.dumps(result,indent=2,sort_keys=True))
