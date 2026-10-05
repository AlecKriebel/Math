#!/usr/bin/env python3
"""Relocation and tamper tests in disposable copies; never edit audit inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

if sys.flags.optimize:raise SystemExit('Optimized Python is not supported.')

AUTHOR_ANCHOR='3f9f39f70e90cb78b8e36d86a80a88dc7bc8100fd29bda09cf25158d615955c8'

def tests(root,anchor,proof):
    outcomes={}
    with tempfile.TemporaryDirectory(prefix='hairs_5300062_audit_') as td:
        base=Path(td)
        def case(name,mutation=None,flags=(),expected=1):
            folder=base/name;shutil.copytree(root,folder)
            if mutation:mutation(folder)
            p=subprocess.run([sys.executable,*flags,'-B',str(folder/'verify.py'),'--expected-manifest',anchor],capture_output=True,timeout=120)
            if (p.returncode==0)!=(expected==0):raise RuntimeError('Unexpected result in '+name+': '+p.stderr.decode()+p.stdout.decode())
            outcomes[name]='PASS_ACCEPTED' if expected==0 else 'PASS_REJECTED'
        case('relocated_replay',expected=0)
        case('changed_analysis',lambda p:(p/proof).write_text((p/proof).read_text()+'\nModified.\n'))
        case('missing_result',lambda p:(p/'RESULTS.json').unlink())
        case('extra_file',lambda p:(p/'extra.txt').write_text('extra'))
        case('extra_empty_directory',lambda p:(p/'empty').mkdir())
        case('symlink',lambda p:(p/'link').symlink_to(p/proof))
        def coherent(p):
            (p/proof).write_text((p/proof).read_text()+'\nModified.\n')
            m=json.loads((p/'MANIFEST.json').read_text())
            for row in m['files']:
                b=(p/row['path']).read_bytes();row['bytes']=len(b);row['sha256']=hashlib.sha256(b).hexdigest()
            (p/'MANIFEST.json').write_text(json.dumps(m))
        case('coherent_rewrite_external_anchor',coherent)
        case('optimized_O',flags=('-O',))
        case('optimized_OO',flags=('-OO',))
    return outcomes

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--author',required=True,type=Path);p.add_argument('--audit',required=True,type=Path);a=p.parse_args()
    audit_anchor=hashlib.sha256((a.audit/'MANIFEST.json').read_bytes()).hexdigest()
    result={'problem_id':5300062,'result':'PASS_RELOCATION_AND_TAMPER_CONTROLS','author':tests(a.author,AUTHOR_ANCHOR,'REPORT.md'),'audit':tests(a.audit,audit_anchor,'AUDIT.md'),'original_inputs_modified':False,'limits':'These tests assume a trusted verifier and an independently retained manifest anchor. They do not prove mathematical claims.'}
    print(json.dumps(result,indent=2,sort_keys=True))
