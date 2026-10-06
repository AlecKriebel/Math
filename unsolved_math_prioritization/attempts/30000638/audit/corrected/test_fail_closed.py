#!/usr/bin/env python3
"""Exercise both integrity failures and rehashed semantic corruptions."""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def must(ok,msg):
    if not ok:
        raise RuntimeError(msg)


def update_hash(root,name):
    p=root/name; b=p.read_bytes(); m=json.loads((root/'MANIFEST.json').read_text())
    m['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (root/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')


def main():
    must(len(sys.argv)==1,'no arguments accepted')
    source=Path(__file__).resolve().parent
    baseline=json.loads((source/'results.json').read_text())
    def changed(fn):
        d=copy.deepcopy(baseline); fn(d); return json.dumps(d,sort_keys=True)+'\n'
    semantic={
      'interior':changed(lambda d:d['cases']['cube_scale_2'].__setitem__('interior_count',25)),
      'volume':changed(lambda d:d['cases']['cross_stretch_2'].__setitem__('volume_normalized',17)),
      'removed_case':changed(lambda d:d['cases'].pop('stress_00')),
      'vertex_changed':changed(lambda d:d['cases']['stress_00']['vertices'][0].__setitem__(0,4)),
      'float_vertex':changed(lambda d:d['cases']['stress_00']['vertices'][0].__setitem__(0,0.5)),
      'bool_interior':changed(lambda d:d['cases']['cross_stretch_1'].__setitem__('interior_count',True)),
      'hstar':changed(lambda d:d['cases']['cross_stretch_2']['hstar'].__setitem__(1,99)),
      'unknown_claim':changed(lambda d:d.__setitem__('universal_conjecture_proved',True)),
      'overclaim':changed(lambda d:d.__setitem__('status','SOLVED')),
      'residue':changed(lambda d:d['arithmetic']['residue_cases'][0].__setitem__('determinant_absolute',2)),
      'laguerre':changed(lambda d:d['arithmetic']['laguerre_rows'][0].__setitem__('L_plus_at_2',[1,1])),
      'duplicate_json_key':'{"status":"PARTIAL_UNSOLVED","status":"SOLVED"}',
      'truncated_json':'{"status":',
    }
    passed=[]
    with tempfile.TemporaryDirectory(prefix='symmetric lattice audit ') as temp:
        base=Path(temp)
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal'
            for label in ['baseline']+list(semantic)+['unhashed_proof','missing_manifest_entry','extra_file','symlink']:
                root=base/(mode+' '+label)
                shutil.copytree(source,root,ignore=shutil.ignore_patterns('__pycache__'))
                if label in semantic:
                    (root/'results.json').write_text(semantic[label]); update_hash(root,'results.json')
                elif label=='unhashed_proof':
                    with (root/'PROOF.md').open('a') as f:f.write('\nCORRUPTION\n')
                elif label=='missing_manifest_entry':
                    m=json.loads((root/'MANIFEST.json').read_text());m['files'].pop('PROOF.md')
                    (root/'MANIFEST.json').write_text(json.dumps(m))
                elif label=='extra_file':
                    (root/'unexpected.txt').write_text('unexpected')
                elif label=='symlink':
                    (root/'unexpected-link').symlink_to(root/'PROOF.md')
                cmd=[sys.executable]+(['-O'] if optimized else [])+[str(root/'verify.py')]
                p=subprocess.run(cmd,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60)
                must((p.returncode==0)==(label=='baseline'),mode+' '+label+': '+p.stdout+p.stderr)
                passed.append(mode+':'+label)
    print(json.dumps({'status':'PASS_FAIL_CLOSED','checks':len(passed),'passed':passed},sort_keys=True))


if __name__=='__main__':
    main()
