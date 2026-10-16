#!/usr/bin/env python3
"""Check frozen authored bytes and scope; print JSON, never write files."""
import ast
import hashlib
import json
from pathlib import Path
import os
import sys


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())
    require(manifest['schema']==1,'Unsupported manifest schema')
    wanted=set(manifest['files'])|{'MANIFEST.json'}
    actual={p.name for p in root.iterdir()}
    require(actual==wanted,'Unexpected or missing frozen-packet member')
    for name,expected in manifest['files'].items():
        require(Path(name).name==name,'Nonflat manifest path')
        data=(root/name).read_bytes()
        require({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}==expected,
                'Frozen byte mismatch: '+name)
        if name.endswith('.py'):
            tree=ast.parse(data)
            require(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)),
                    'Optimization-sensitive assertion found')
    budget=json.loads((root/'BUDGET.json').read_text())
    require(budget['outcome']=='UNSOLVED' and budget['full_candidate'] is False,'Full target overclaim')
    require(budget['substantive_families']==5,'Wrong shared target budget')
    require([f['number'] for f in budget['families']]==[1,2,3,4,5],'Family ledger mismatch')
    require(budget['same_target_component_id']==30006622,'Duplicate target binding lost')
    forbidden={'.pdf','.png','.jsonl','.sqlite','.db','.csv','.zip'}
    require(not any(Path(name).suffix in forbidden for name in wanted),'Non-authored/source payload present')
    print(json.dumps({'status':'PASS','uid':os.geteuid(),'optimization':sys.flags.optimize,
                      'members':len(wanted),'source_free_extension_check':True,
                      'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
