#!/usr/bin/env python3
"""Verify the explicit curated public map against an EXTERNAL digest before imports.

Authenticate THIS bootstrap file from an independent receipt before execution.
A self-published checksum cannot establish trust in its own checker. The map
excludes itself and private tmp/ scratch; neither exclusion conveys authenticity.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

PUBLIC = {'AUDIT.md', 'RESULT.json', 'INITIAL_RECONSTRUCTION.md', 'RESEARCH_LOG.md',
          'AUTHENTICATION_START.json', 'AUTHENTICATION_END.json', 'PINNED_SNAPSHOT.json',
          'STATIC_REVIEW.json', 'REPLAY_RESULTS.json', 'PACKET_GUARD.py', 'GUARDED_RUN.py',
          'INDEPENDENT_CONTROLS.py', 'RELEASE_GATE.py', 'REPRODUCE.py', 'VERIFY.py'}
HERE = Path(__file__).absolute().parent


def need(condition, message):
    if not condition: raise RuntimeError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'nonregular public member: '+path.name)
    descriptor = os.open(path, os.O_RDONLY | getattr(os,'O_NOFOLLOW',0) | getattr(os,'O_NONBLOCK',0))
    try:
        need(stat.S_ISREG(os.fstat(descriptor).st_mode), 'nonregular opened member')
        with os.fdopen(descriptor,'rb',closefd=False) as stream: raw=stream.read(5_000_001)
        need(len(raw)<=5_000_000,'oversized public member')
        return raw
    finally: os.close(descriptor)


def strict_json(raw):
    def pairs(items):
        obj={}
        for key,value in items:
            need(key not in obj,'duplicate JSON key'); obj[key]=value
        return obj
    def bad(value): raise RuntimeError('nonfinite JSON constant')
    value=json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
    def finite(item):
        if type(item) is float: need(math.isfinite(item),'nonfinite JSON number')
        elif type(item) is dict:
            for v in item.values(): finite(v)
        elif type(item) is list:
            for v in item: finite(v)
    finite(value)
    return value


def verify(external):
    need(type(external) is str and re.fullmatch(r'[0-9a-f]{64}',external) is not None,'external public-map SHA256 required')
    for parent in reversed([HERE,*HERE.parents]):
        need(stat.S_ISDIR(parent.lstat().st_mode),'symlink or non-directory ancestor')
    need(stat.S_ISREG(Path(__file__).lstat().st_mode),'bootstrap symlink forbidden')
    raw=regular(HERE/'MANIFEST.json')
    need(sha(raw)==external,'external public-map anchor differs')
    manifest=strict_json(raw)
    need(type(manifest) is dict and set(manifest)=={'schema','files','self_excluded','private_paths_excluded'},'public-map schema')
    need(manifest['schema']=='pr932-reproducibility-audit-public-map-v1' and manifest['self_excluded']=='MANIFEST.json' and
         manifest['private_paths_excluded']==['tmp/'],'public-map scope')
    need(type(manifest['files']) is dict and manifest['files'].keys()==PUBLIC,'explicit public allowlist differs')
    names={entry.name for entry in HERE.iterdir()}
    need(names in (PUBLIC|{'MANIFEST.json'},PUBLIC|{'MANIFEST.json','tmp'}),'unexpected uncurated root entry')
    if 'tmp' in names: need(stat.S_ISDIR((HERE/'tmp').lstat().st_mode),'private scratch must be a real directory')
    for name,record in manifest['files'].items():
        need(type(record) is dict and set(record)=={'bytes','sha256'},'public record schema')
        need(type(record['bytes']) is int and record['bytes']>=0 and type(record['sha256']) is str and
             re.fullmatch(r'[0-9a-f]{64}',record['sha256']) is not None,'public record types')
        data=regular(HERE/name)
        need(len(data)==record['bytes'] and sha(data)==record['sha256'],'public bytes differ: '+name)
    return len(PUBLIC)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--run',action='store_true')
    p.add_argument('--packet')
    p.add_argument('--python',default=sys.executable)
    p.add_argument('--repository')
    args=p.parse_args()
    try:
        count=verify(args.expected_manifest)
        if args.run:
            need(args.packet is not None,'--packet required with --run')
            scratch=HERE/'tmp'; scratch.mkdir(exist_ok=True)
            output=scratch/'verified_reproduction.json'
            command=[args.python,'-I','-B',str(HERE/'REPRODUCE.py'),'--packet',args.packet,'--python',args.python,
                     '--scratch',str(scratch),'--output',str(output)]
            if args.repository: command+=['--repository',args.repository]
            env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
            env['PYTHONDONTWRITEBYTECODE']='1'
            cp=subprocess.run(command,cwd=scratch,env=env,timeout=600)
            need(cp.returncode==0,'meaningful reproduction pipeline failed')
            value=strict_json(regular(output))
            need(value['integrity_and_independent_controls_passed'] is True,'independent reproduction did not pass')
            need(value['status'] in ('PASS','EXACT_LEGACY_RECEIPT_MISMATCH'),'unexpected reproduction disposition')
            verify(args.expected_manifest)
        print(json.dumps({'public_map':'PASS','curated_public_files':count,'meaningful_pipeline_run':args.run,
                          'mathematical_acceptance':False,'private_tmp_authenticated':False},sort_keys=True))
    except (RuntimeError,OSError,ValueError,subprocess.SubprocessError) as error:
        print('PUBLIC_MAP_REJECT: '+str(error),file=sys.stderr); return 1
    return 0


if __name__=='__main__': raise SystemExit(main())
