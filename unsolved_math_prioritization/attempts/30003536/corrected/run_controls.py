#!/usr/bin/env python3
"""Reproduce optimizer, wrong-claim, malformed-input, integrity and relocation controls."""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class ControlError(Exception):
    pass

def need(condition,message):
    if not condition:
        raise ControlError(message)

def invoke(script,mode,args=(),cwd=None):
    flags=['-I','-B']+([mode] if mode else [])
    result=subprocess.run([sys.executable,*flags,str(script),*map(str,args)],cwd=cwd,capture_output=True,check=False)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-manifest-sha256',required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    pin=args.expected_manifest_sha256
    summary={'positive_replays':0,'wrong_claim_rejections':0,'malformed_claim_rejections':0,
             'integrity_rejections':0,'read_only_relocations':0,'no_assert_scripts':0}
    expected=(root/'CHECKS.expected.json').read_bytes()
    claims=json.loads((root/'CLAIMS.json').read_text())
    for path in root.glob('*.py'):
        tree=ast.parse(path.read_text())
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)), 'assert statement in '+path.name)
        summary['no_assert_scripts']+=1
    wrong=[]
    changes=[('status','claimed_solved'),('original_inequality_proved',True),
             ('original_inequality_disproved',True),('author_turns',4),
             ('mass_lower_coefficient','1'),('independent_audit_performed',True)]
    for k,v in changes:
        obj=copy.deepcopy(claims);obj[k]=v;wrong.append(obj)
    for path,value in [(('latitude','hessian_transverse'),'4/147'),
                       (('latitude','global_counterexample'),True),
                       (('target','density'),'signed C_c^infinity'),
                       (('target','support'),'points where f is nonzero'),
                       (('flat_model','admissible_target_density'),True)]:
        obj=copy.deepcopy(claims);obj[path[0]][path[1]]=value;wrong.append(obj)
    obj=copy.deepcopy(claims);obj['original_inequality_proved']=0;wrong.append(obj)
    malformed=['{','[]','{"problem_id":30003536,"problem_id":30003536}','{"x":NaN}']
    with tempfile.TemporaryDirectory(prefix='riesz-controls-') as td:
        tmp=Path(td)
        outside=tmp/'outside.txt';outside.write_text('control fixture\n')
        for mode in ('','-O','-OO'):
            good=invoke(root/'check_math.py',mode,cwd=tmp)
            need(good.returncode==0 and good.stdout==expected and not good.stderr,'normal algebra replay failed')
            summary['positive_replays']+=1
            good=invoke(root/'verify_packet.py',mode,['--expected-manifest-sha256',pin],tmp)
            need(good.returncode==0 and not good.stderr,'normal integrity replay failed')
            summary['positive_replays']+=1
            for number,obj in enumerate(wrong):
                path=tmp/'wrong.json';path.write_text(json.dumps(obj))
                bad=invoke(root/'check_math.py',mode,['--claims',path],tmp)
                need(bad.returncode==2 and json.loads(bad.stdout)['result']=='FAIL', 'wrong claim accepted '+str(number))
                summary['wrong_claim_rejections']+=1
            for data in malformed:
                path=tmp/'malformed.json';path.write_text(data)
                bad=invoke(root/'check_math.py',mode,['--claims',path],tmp)
                need(bad.returncode==2 and json.loads(bad.stdout)['result']=='FAIL','malformed claims accepted')
                summary['malformed_claim_rejections']+=1
            for kind in ('changed','missing','unexpected','symlink','manifest_bad_json','manifest_list','manifest_traversal','manifest_duplicate'):
                clone=tmp/'mutant';shutil.copytree(root,clone)
                clone.chmod(0o755)
                for item in clone.iterdir():item.chmod(0o644)
                use_pin=pin
                if kind=='changed':
                    with (clone/'REPORT.md').open('ab') as f:f.write(b'\nchanged\n')
                elif kind=='missing': (clone/'REPORT.md').unlink()
                elif kind=='unexpected': (clone/'unexpected.pdf').write_bytes(b'negative control, not source material')
                elif kind=='symlink':
                    (clone/'REPORT.md').unlink();(clone/'REPORT.md').symlink_to(outside)
                else:
                    if kind=='manifest_bad_json': raw=b'{'
                    elif kind=='manifest_list': raw=b'[]'
                    else:
                        doc=json.loads((clone/'MANIFEST.json').read_text())
                        if kind=='manifest_traversal': doc['files'][0]['path']='../outside.txt'
                        else:doc['files'].append(copy.deepcopy(doc['files'][0]))
                        raw=json.dumps(doc).encode()
                    (clone/'MANIFEST.json').write_bytes(raw)
                    # Supply the changed pin intentionally to reach parser and
                    # path validation rather than only the digest mismatch.
                    use_pin=hashlib.sha256(raw).hexdigest()
                bad=invoke(clone/'verify_packet.py',mode,['--expected-manifest-sha256',use_pin],tmp)
                need(bad.returncode==2 and json.loads(bad.stdout)['result']=='FAIL','integrity mutation accepted: '+kind)
                summary['integrity_rejections']+=1
                shutil.rmtree(clone)
            clone=tmp/'readonly';shutil.copytree(root,clone)
            before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in clone.iterdir()}
            for p in clone.iterdir():p.chmod(0o444)
            clone.chmod(0o555)
            try:
                need(all((p.stat().st_mode & 0o222)==0 for p in clone.iterdir()),'readonly file modes')
                need((clone.stat().st_mode & 0o222)==0,'readonly directory mode')
                good=invoke(clone/'verify_packet.py',mode,['--expected-manifest-sha256',pin],tmp)
                need(good.returncode==0 and not good.stderr,'readonly relocated replay failed')
                after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in clone.iterdir()}
                need(before==after,'readonly inventory changed')
                summary['read_only_relocations']+=1
            finally:
                clone.chmod(0o755)
                for p in clone.iterdir():p.chmod(0o644)
                shutil.rmtree(clone)
    print(json.dumps({'result':'PASS','controls':summary,'manifest_sha256':pin,
                      'modes':['normal','-O','-OO'],'analytic_proof_certified':False},sort_keys=True,indent=2))
    return 0

if __name__=='__main__':
    try:
        sys.exit(main())
    except (ControlError,ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'result':'FAIL','error':str(exc)},sort_keys=True))
        sys.exit(2)
