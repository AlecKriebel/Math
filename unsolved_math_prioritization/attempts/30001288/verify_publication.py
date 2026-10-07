#!/usr/bin/env python3
"""Externally anchored closed inventory and finite-controls replay, not a proof checker."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ANCHORS = {
    'original': ('AUTHOR_MANIFEST.json', 'e3849b16c9617fdbb72cd81ce14dd282ed2fbd1b64d01664e4c14411ac2cb892'),
    'audit': ('AUDIT_MANIFEST.json', 'c355015e39cd2417d9ad97f3b650372e7a49e6f0c40b21702b00036d0e76906f'),
    'corrected': ('AUTHOR_MANIFEST.json', '8dcbfa59690c015db89b9d0ef5e5c35258fbc3bbda70618799446dd147b4e518'),
}
TOP_LEVEL = {'README.md', 'RESEARCH_LOG.md', 'PUBLICATION_STATUS.json', 'requirements.txt',
             'verify_publication.py', 'mutation_tests.py', 'PUBLIC_MANIFEST.json'}

def need(value, message):
    if not value: raise RuntimeError(message)

def sha(data): return hashlib.sha256(data).hexdigest()

def file_bytes(path):
    need(not path.is_symlink() and path.is_file(), 'Nonregular or symlinked file: '+str(path))
    return path.read_bytes()

def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        need(key not in obj, 'Duplicate JSON key')
        obj[key] = value
    return obj

def parse(data): return json.loads(data, object_pairs_hook=unique_object)

def safe_name(name):
    need(isinstance(name, str) and name and not name.startswith('/') and '\\' not in name
         and all(x not in ('', '.', '..') for x in name.split('/')), 'Unsafe path')
    return PurePosixPath(name)

def match(data, record):
    return record == {'bytes':len(data), 'sha256':sha(data)} and type(record['bytes']) is int

def apply_patch(original, patch):
    """Strict multi-file unified diff application without executing an external program."""
    lines=patch.decode('utf-8').splitlines(keepends=True); index=0; result={}
    while index<len(lines):
        need(lines[index].startswith('--- a/'), 'Invalid patch file header')
        name=lines[index][6:].rstrip('\n');index+=1
        need(name in {'checks.py','AUTHOR_MANIFEST.json'} and name not in result, 'Unexpected patch target')
        need(index<len(lines) and lines[index]=='+++ b/'+name+'\n', 'Patch target mismatch');index+=1
        source=original[name].decode('utf-8').splitlines(keepends=True);output=[];cursor=0;hunks=0
        while index<len(lines) and not lines[index].startswith('--- a/'):
            m=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[index]);need(m is not None,'Invalid hunk')
            old_start,old_count,new_start,new_count=map(int,m.groups());start=old_start-1
            need(cursor<=start<=len(source),'Hunk range');output.extend(source[cursor:start]);cursor=start
            need(len(output)==new_start-1,'Hunk output position');index+=1;consumed=produced=0
            while index<len(lines) and not lines[index].startswith(('@@ ','--- a/')):
                line=lines[index];index+=1;need(line[0] in ' +-','Invalid hunk line')
                if line[0] in ' -':
                    need(cursor<len(source) and source[cursor]==line[1:],'Patch context mismatch');cursor+=1;consumed+=1
                if line[0] in ' +':output.append(line[1:]);produced+=1
            need((consumed,produced)==(old_count,new_count),'Hunk line count');hunks+=1
        need(hunks==2,'Unexpected patch hunk count');output.extend(source[cursor:]);result[name]=''.join(output).encode()
    need(set(result)=={'checks.py','AUTHOR_MANIFEST.json'},'Incomplete patch')
    return result

def verify(root, expected, integrity_only=False):
    need(re.fullmatch('[0-9a-f]{64}',expected) is not None,'Invalid external pin')
    need(root.is_dir() and not root.is_symlink(),'Invalid package root')
    manifest_bytes=file_bytes(root/'PUBLIC_MANIFEST.json');need(sha(manifest_bytes)==expected,'External manifest pin mismatch')
    manifest=parse(manifest_bytes)
    need(manifest['schema']=='motivic-albanese-source-free-publication-v1','Manifest schema')
    entries=manifest['files'];need(isinstance(entries,dict),'Manifest file map')
    expected_files=set(entries)|{'PUBLIC_MANIFEST.json'};expected_dirs=set()
    for name in expected_files:
        p=safe_name(name);expected_dirs.update(str(x) for x in p.parents if str(x)!='.')
    actual_files=set();actual_dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'Symlink rejected');name=p.relative_to(root).as_posix()
        if p.is_dir():actual_dirs.add(name)
        else:need(p.is_file(),'Special file rejected');actual_files.add(name)
    need((actual_files,actual_dirs)==(expected_files,expected_dirs),'Closed inventory mismatch')
    for name,record in entries.items():need(match(file_bytes(root/name),record),'Payload mismatch: '+name)
    closed=set(TOP_LEVEL)
    for role,(filename,pin) in ANCHORS.items():
        mb=file_bytes(root/role/filename);need(sha(mb)==pin,'Frozen manifest pin: '+role);m=parse(mb)
        need(m['manifest_excludes']==[filename] and m['problem_id']==30001288,'Frozen schema')
        names=set()
        for entry in m['files']:
            need(set(entry)=={'file','bytes','sha256'},'Frozen record shape');name=entry['file']
            need(safe_name(name).name==name and name not in names,'Frozen duplicate or unsafe name');names.add(name)
            need(match(file_bytes(root/role/name),{'bytes':entry['bytes'],'sha256':entry['sha256']}),'Frozen payload mismatch')
        need({x.name for x in (root/role).iterdir()}==names|{filename},'Frozen inventory mismatch')
        closed.update(role+'/'+name for name in names|{filename})
    need(closed==expected_files,'Top-level allowlist mismatch')
    original=root/'original';corrected=root/'corrected';audit=root/'audit'
    changes=sorted(x.name for x in original.iterdir() if file_bytes(x)!=file_bytes(corrected/x.name))
    need(changes==['AUTHOR_MANIFEST.json','checks.py'],'Corrected scope mismatch')
    patched=apply_patch({name:file_bytes(original/name) for name in changes},file_bytes(audit/'CORRECTION.patch'))
    need(all(data==file_bytes(corrected/name) for name,data in patched.items()),'Exact patch replay mismatch')
    need(file_bytes(corrected/'checks.py')==file_bytes(audit/'corrected_checks.py'),'Corrected verifier duplicate mismatch')
    need(file_bytes(corrected/'AUTHOR_MANIFEST.json')==file_bytes(audit/'CORRECTED_AUTHOR_MANIFEST.json'),'Corrected manifest duplicate mismatch')
    status=parse(file_bytes(root/'PUBLICATION_STATUS.json'))
    need(status['problem_id']==30001288 and status['status']=='unsolved' and status['turns']=='5/5','Status mismatch')
    need(status['full_connected_comparison_proved'] is False and status['novelty_claimed'] is False,'Claim boundary')
    replays=[]
    if not integrity_only:
        env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
        with tempfile.TemporaryDirectory(prefix='albanese-replay-') as cwd:
            for mode in (0,1):
                cmd=[sys.executable,'-I','-S','-B']+(['-O'] if mode else [])+[str(audit/'audit_checks.py'),'--packet',str(original),'--corrected-packet',str(corrected)]
                p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=300)
                need(p.returncode==0 and not p.stderr,'Audit replay failed: '+p.stderr.decode(errors='replace')[-500:])
                got=parse(p.stdout);frozen=parse(file_bytes(audit/('AUDIT_CHECK_RESULTS_OPTIMIZED.json' if mode else 'AUDIT_CHECK_RESULTS_NORMAL.json')))
                need(got==frozen,'Audit output differs from frozen receipt')
                need(got['wrapper_optimization_level']==mode and got['child_optimization_levels_explicitly_exercised']==[0,1],'Audit child modes')
                need(got['total_checks']==57135 and len(got['verifier_regressions'])==56,'Audit counts')
                replays.append({'audit_wrapper_optimization_level':mode,'explicit_child_modes':[0,1],'checks':57135,'regression_cases':56,'frozen_result_equal':True})
    return {'status':'PASS','problem_id':30001288,'files':len(expected_files),'external_manifest_sha256':expected,
            'publication_wrapper_optimization_level':sys.flags.optimize,'integrity_only':integrity_only,'audit_replays':replays,
            'original_optimized_integrity_is_defective':True,'scope':'Package integrity and finite controls; general comparison remains unresolved.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--integrity-only',action='store_true');p.add_argument('--root',type=Path);a=p.parse_args()
    root=a.root if a.root is not None else Path(__file__).absolute().parent
    print(json.dumps(verify(root.absolute(),a.expected_manifest_sha256,a.integrity_only),indent=2,sort_keys=True))
if __name__=='__main__':main()
