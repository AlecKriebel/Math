#!/usr/bin/env python3
"""Fail-closed inventory, public metadata, and independent-check replay."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

FILES={'README.md','second_review.md','check_algebra.py','algebra_results.json',
       'source_verification.json','corpus_verification.json','prior_replay_results.json',
       'verify_review.py','test_review.py','test_results.json','manifest.json',
       'verifier_path_hardening.patch','path_hardening_results.json'}


def need(ok,message):
    if not ok: raise ValueError(message)


def unique_pairs(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'Duplicate JSON key: '+key)
        out[key]=value
    return out


def read_json(path):
    return json.loads(path.read_text(),object_pairs_hook=unique_pairs)


def inventory(root):
    entries=list(root.iterdir())
    need({p.name for p in entries}==FILES,'Exact file inventory mismatch')
    for path in entries:
        need(stat.S_ISREG(path.lstat().st_mode),'Nonregular entry: '+path.name)
    manifest=read_json(root/'manifest.json')
    need(set(manifest)=={'schema','files'} and type(manifest['schema']) is int
         and manifest['schema']==1,'Manifest schema mismatch')
    need(set(manifest['files'])==FILES-{'manifest.json'},'Manifest file set mismatch')
    for name,entry in manifest['files'].items():
        need(set(entry)=={'bytes','sha256'} and type(entry['bytes']) is int
             and entry['bytes']>=0 and isinstance(entry['sha256'],str),
             'Manifest record schema mismatch')
        data=(root/name).read_bytes()
        need(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],
             'Manifest content mismatch: '+name)


def execute(root,optimized):
    p=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+
                     [str(root/'check_algebra.py')],cwd=root.parent,
                     env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),
                     capture_output=True,text=True,timeout=30)
    need(p.returncode==0,'Algebra replay failed: '+p.stderr)
    return json.loads(p.stdout,object_pairs_hook=unique_pairs)


def main():
    need(len(sys.argv)==1,'No arguments accepted')
    # Do not resolve __file__: a substituted verifier symlink must be rejected.
    root=Path(__file__).absolute().parent
    inventory(root)
    normal=execute(root,False); optimized=execute(root,True)
    need(normal==optimized==read_json(root/'algebra_results.json'),'Algebra saved-output mismatch')
    need(normal['status']=='PASS','Algebra status failure')
    metadata=read_json(root/'source_verification.json')
    need(metadata['source_display_matches_author_certificate'] is True
         and metadata['verified_relation_count']==6,'Source verification metadata mismatch')
    need([(s['bytes'],s['sha256']) for s in metadata['sources']]==[
        (620349,'c860a92325ab314dc5a784cfac5ad7812a7715735247465b7bf4c27d9bd4cd60'),
        (791166,'85fa0387680ea3724c41ba02203b91dc7bbc72a84da250ff0947301e96514e6d')],
        'Source metadata pins mismatch')
    prior=read_json(root/'prior_replay_results.json')
    need(prior['author']['sha256']=='018f641c1425c6cb28e09b5cf8cc17a0848f928bdd3f37ea57e64c7a70f6d0a9'
         and prior['audit']['sha256']=='075159f6da95ded37cbeb3aab31aa8cd26a441b3e2e1f53e18fcd1a41f0d8ae6',
         'Immutable archive pins mismatch')
    corpus=read_json(root/'corpus_verification.json')
    need(corpus['full_review_pair']['bytes']==5124
         and corpus['full_review_pair']['sha256']=='cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f'
         and corpus['full_review_pair']['matches_catalog'] is True,'Review-pair metadata mismatch')
    print(json.dumps({'status':'PASS','exact_regular_file_count':len(FILES),
          'normal_and_optimized_agree':True,'source_relation_count':6,
          'gf4_degree_cases':sum(len(x['degrees']) for x in normal['gf4_checks']),
          'prior_archive_records':'Verified hashes and recorded replay metadata; archives not bundled',
          'proof_status':'Unrefereed; complete algebraic counterexample to both literal assertions'},
          sort_keys=True,indent=2))


if __name__=='__main__':
    try: main()
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr)
        sys.exit(1)
