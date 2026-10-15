#!/usr/bin/env python3
"""Externally pinned original PR909 bytes, closed inventory, optional replay.

Trust this verifier's reviewed bytes, OS, Python, dependencies and SHA-256.
Not a sandbox, signature, proof assistant or defense against concurrent attackers.
Never reads FIFOs/sockets. Rejects symlinks and explicit . or .. root components;
accepts trailing slashes and repeated separators after pathlib normalization.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

SOURCE_HEAD = 'd186dea31791cd3e8acf6829e0b65d01849623b8'
SOURCE_PREFIX = 'unsolved_math_prioritization/attempts/30001345/'
EXPECTED_DIRS = {'audit_a', 'audit_b', 'frozen_v2'}
PINS = {'ACCEPTANCE.md': {'bytes': 2609, 'sha256': '11e398e5e1e8db4695e4a0715b88221cda6f1fed85e8c866866910039ff7448a'}, 'APPROACH_LEDGER.md': {'bytes': 547, 'sha256': '090ac9ceffa0db796a03bc160da02d6e04c986b2a596db0c6449e36460eb3cfd'}, 'PACKAGE_MANIFEST.json': {'bytes': 4329, 'sha256': 'a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02'}, 'PACKAGE_MANIFEST.sha256': {'bytes': 88, 'sha256': '09898bb3083a618afa85cf098eddc7d00abf1520dae2c48cf46c9691a85c5b6c'}, 'README.md': {'bytes': 3038, 'sha256': '6a4afaef39b71b90febcfaa2e21558ea1f378ef35356634a45a0b064bd77c284'}, 'RESEARCH_LOG.md': {'bytes': 1093, 'sha256': '504fbb4ddf1554555564b2eeabd8eca4786616432fee156905ac0111be49031b'}, 'audit_a/AUDIT.md': {'bytes': 15535, 'sha256': '94a418eb803099290e5832683210bccbfc348462dc4bb7e4303c924b6d8b4156'}, 'audit_a/AUDIT_MANIFEST.json': {'bytes': 1330, 'sha256': '218b4dd72de1aa92ed88be04c5010b4eccea7331985dcd853a5c2465e032bf9e'}, 'audit_a/AUTHOR_CHECK_RESULTS.json': {'bytes': 578, 'sha256': '59eb46695f4df37b3d9b7643346af9aa0191fc2ef730c630e8346c09a3d81aa5'}, 'audit_a/AUTHOR_CHECK_RESULTS_OPTIMIZED.json': {'bytes': 578, 'sha256': '59eb46695f4df37b3d9b7643346af9aa0191fc2ef730c630e8346c09a3d81aa5'}, 'audit_a/INDEPENDENT_CHECK_RESULTS.json': {'bytes': 589, 'sha256': '4289a41de2b9b5749e44e358a20b486b12d39e53a9f5f018e43720859e303f4d'}, 'audit_a/INDEPENDENT_SOURCE_RETRIEVAL.json': {'bytes': 908, 'sha256': 'e864395f9586fd523781d28892fe93abacd84ce535196c9cd4a6901c2d6c3616'}, 'audit_a/independent_checks.py': {'bytes': 5896, 'sha256': '8392948fcff58982851c707e369bb600611375940b461c73553bcfa5cd7006a1'}, 'audit_b/AUDIT_MANIFEST.json': {'bytes': 1508, 'sha256': 'ca49b07b2dfc4c83f9d7c6f03b7185e56a662ee820eba58a5c63f905973f94c5'}, 'audit_b/AUDIT_REPORT.md': {'bytes': 16063, 'sha256': 'a2d183a87e08e5efe5a795d19aa0711d59bc5fb4b3f931695fe45cca845c7b76'}, 'audit_b/INDEPENDENT_RESULTS.json': {'bytes': 1441, 'sha256': '0c7dfa297c570dcbc501187399a5d62190f99d3a7582837026965dba2f43ed43'}, 'audit_b/SOURCE_METADATA.json': {'bytes': 4708, 'sha256': '55c30626278c0abbd5e46b5c9e515c64b1586609d7a934682ae80754a98a8cf5'}, 'audit_b/independent_checks.py': {'bytes': 6912, 'sha256': 'eb7d58f31569bc210121bf43c939f181cf52d8db0627cef2546b7199918cf28c'}, 'frozen_v2/CHECK_RESULTS.json': {'bytes': 578, 'sha256': '59eb46695f4df37b3d9b7643346af9aa0191fc2ef730c630e8346c09a3d81aa5'}, 'frozen_v2/FROZEN_MANIFEST.json': {'bytes': 1606, 'sha256': '199dc44fdb8de8f37024d170e6246281e1a7b6b5b7e1cdd94a21f4a1b195e478'}, 'frozen_v2/PROOF.md': {'bytes': 16696, 'sha256': '561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b'}, 'frozen_v2/README.md': {'bytes': 1534, 'sha256': 'a7825973f8edff090827fdf7a47eef372f585ccef6a375bba93f1e35e9776767'}, 'frozen_v2/SOURCE_MANIFEST.json': {'bytes': 3681, 'sha256': '473f60889553c413491453007a8a4983a8c72ad88d7d17d253e15a52064d1dd1'}, 'frozen_v2/checks.py': {'bytes': 6922, 'sha256': '1aae2c393ee6fbf063183a2633643d5cf66e3704e31400881cc713b04b7a832c'}, 'mutation_tests.py': {'bytes': 4447, 'sha256': '2dd11fcbb9c1d73b4a7b70f2cb99c0d02fff7e9773b451cc4f29cf5c29738858'}, 'requirements.txt': {'bytes': 28, 'sha256': '47fd19021144e071cc43b6e265aafada0056abe89724ad95bd6e3a8e37995b94'}, 'run_audit_a.py': {'bytes': 394, 'sha256': 'b42307645aaf457fb1f1deaec03c3a5c23528b34be1ccbf77ec931343604edce'}, 'verify_publication.py': {'bytes': 5798, 'sha256': 'a0b4213b21f0c9e910d5bfd1cacef0950a380fa7cc66e6e336b91504859fbab3'}}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def safe_bytes(path):
    fd=os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    try:
        require(stat.S_ISREG(os.fstat(fd).st_mode), 'Not a regular file: '+str(path))
        chunks=[]
        while True:
            b=os.read(fd,1024*1024)
            if not b:
                return b''.join(chunks)
            chunks.append(b)
    finally:
        os.close(fd)

def strict_json(data):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result, 'Duplicate JSON key: '+key)
            result[key]=value
        return result
    def constant(value):
        raise ValueError('Nonstandard JSON constant: '+value)
    return json.loads(data,object_pairs_hook=pairs,parse_constant=constant)

def integrity(root_text):
    require(os.path.isabs(root_text),'Absolute root required')
    require(not any(part in {'.','..'} for part in root_text.split('/')),'Root aliases prohibited')
    root=Path(root_text)
    require(root==root.resolve(strict=True),'Symlink root/ancestor prohibited')
    require(stat.S_ISDIR(root.lstat().st_mode),'Root must be a directory')
    files=set(); dirs=set()
    def walk(folder):
        for entry in os.scandir(folder):
            path=Path(entry.path); rel=path.relative_to(root).as_posix()
            mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(rel in EXPECTED_DIRS,'Unexpected directory: '+rel)
                dirs.add(rel); walk(path)
            elif stat.S_ISREG(mode):
                require(rel in PINS,'Unexpected file: '+rel)
                files.add(rel)
            else:
                raise ValueError('Symlink or special entry prohibited: '+rel)
    walk(root)
    require(files==set(PINS) and dirs==EXPECTED_DIRS,'Closed inventory mismatch')
    for rel,pin in PINS.items():
        b=safe_bytes(root/rel)
        require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'Pinned bytes mismatch: '+rel)
        if rel.endswith('.json'):
            strict_json(b)
    manifest=strict_json(safe_bytes(root/'PACKAGE_MANIFEST.json'))
    require(type(manifest['schema']) is int and manifest['schema']==1,'Strict schema version required')
    require(type(manifest['problem_id']) is int and manifest['problem_id']==30001345,'Strict problem ID required')
    for item in manifest['files']:
        require(type(item['bytes']) is int and type(item['file']) is str and type(item['sha256']) is str,'Strict manifest field types required')
    return root

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root')
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    root=integrity(args.root)
    result={'status':'VERIFIED_ORIGINAL_BYTES','source_head':SOURCE_HEAD,'files':len(PINS),'directories':len(EXPECTED_DIRS),'proof_certified':False}
    if args.replay:
        env=os.environ.copy()
        for name in ('PYTHONOPTIMIZE','PYTHONPATH'):
            env.pop(name,None)
        env['PYTHONDONTWRITEBYTECODE']='1'
        process=subprocess.run([sys.executable,'-I','-B',str(root/'verify_publication.py')],cwd=root.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
        require(process.returncode==0,'Historical replay failed: '+process.stderr.decode(errors='replace'))
        replay=strict_json(process.stdout)
        require(replay.get('status')=='PASS','Replay did not report PASS')
        integrity(args.root)
        result['historical_replay']='PASS'
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
