#!/usr/bin/env python3
"""Reproduce mutation checks in temporary copies; optional pinned author archive."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile

CASES = ('same_size_text','missing_payload','extra_file','extra_directory',
         'symlink_payload','symlink_verifier','duplicate_manifest_key','boolean_byte_count',
         'malformed_hash','unsafe_manifest_path','wrong_manifest_schema',
         'rehashed_false_results','rehashed_wrong_target','rehashed_false_novelty')
AUTHOR_SHA = '2ed1cf89f1d8e3ea19184fa5bd14b840a2e12183b0ab4c1f0b690c9eea4f1e62'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def invoke(folder, optimized):
    cmd = [sys.executable, '-I'] + (['-O'] if optimized else []) + [str(folder/'verify.py')]
    return subprocess.run(cmd,capture_output=True,text=True,cwd='/')

def rewrite(folder, name, data):
    p=folder/name
    p.write_text(json.dumps(data,sort_keys=True)+'\n')
    mpath=folder/'MANIFEST.json'
    m=json.loads(mpath.read_text())
    raw=p.read_bytes()
    m['files'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    mpath.write_text(json.dumps(m,sort_keys=True)+'\n')

def test(folder, work, author=False):
    result={'positive':{},'negative':{},'positive_runs':4,'negative_runs':2*len(CASES)}
    moved=work/'path with spaces'/'relocated'
    shutil.copytree(folder,moved)
    for name,path in (('normal',folder),('relocated',moved)):
        for opt in (False,True):
            r=invoke(path,opt)
            need(r.returncode==0,'unexpected positive failure: '+r.stderr)
            result['positive'][name+('_optimized' if opt else '')]='pass'
    target='RESULT.md' if author else 'AUDIT.md'
    for case in CASES:
        trial=work/case
        shutil.copytree(folder,trial)
        mp=trial/'MANIFEST.json'
        m=json.loads(mp.read_text())
        if case=='same_size_text':
            p=trial/target;b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:])
        elif case=='missing_payload': (trial/target).unlink()
        elif case=='extra_file': (trial/'unexpected.txt').write_text('extra')
        elif case=='extra_directory': (trial/'unexpected').mkdir()
        elif case=='symlink_payload':
            (trial/target).unlink();(trial/target).symlink_to(folder/target)
        elif case=='symlink_verifier':
            (trial/'verify.py').unlink();(trial/'verify.py').symlink_to(folder/'verify.py')
        elif case=='duplicate_manifest_key': mp.write_text('{"schema":1,'+mp.read_text()[1:])
        elif case=='boolean_byte_count':
            m['files'][target]['bytes']=True;mp.write_text(json.dumps(m))
        elif case=='malformed_hash':
            m['files'][target]['sha256']='NOT-A-HASH';mp.write_text(json.dumps(m))
        elif case=='unsafe_manifest_path':
            m['files']['../'+target]=m['files'].pop(target);mp.write_text(json.dumps(m))
        elif case=='wrong_manifest_schema': m['schema']=2;mp.write_text(json.dumps(m))
        elif case=='rehashed_false_results':
            d=json.loads((trial/'CHECK_RESULTS.json').read_text());d['total_checks']+=1
            rewrite(trial,'CHECK_RESULTS.json',d)
        elif case=='rehashed_wrong_target':
            d=json.loads((trial/'PUBLIC_METADATA.json').read_text());d['identity' if author else 'target']['id']='6200021'
            rewrite(trial,'PUBLIC_METADATA.json',d)
        elif case=='rehashed_false_novelty':
            d=json.loads((trial/'PUBLIC_METADATA.json').read_text())
            if author: d['disposition']['novel_solution_claimed']=True
            else: d['verdict']['novelty_claimed']=True
            rewrite(trial,'PUBLIC_METADATA.json',d)
        result['negative'][case]={}
        for opt in (False,True):
            r=invoke(trial,opt)
            need(r.returncode!=0 and 'FAIL:' in r.stderr,'mutation not explicitly rejected: '+case)
            result['negative'][case]['optimized' if opt else 'normal']='rejected'
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-archive',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    result={'problem_id':'6200022','status':'pass','audit':None}
    with tempfile.TemporaryDirectory(prefix='diagonal-core-audit-') as temporary:
        tmp=Path(temporary)
        result['audit']=test(root,tmp/'audit')
        if args.author_archive:
            raw=args.author_archive.read_bytes()
            need(len(raw)==16021 and hashlib.sha256(raw).hexdigest()==AUTHOR_SHA,'author archive anchor')
            out=tmp/'extracted-author';out.mkdir()
            with zipfile.ZipFile(args.author_archive) as z:
                names=z.namelist()
                expected={'CHECK_RESULTS.json','MANIFEST.json','PUBLIC_METADATA.json','README.md',
                          'RESEARCH_LOG.md','RESULT.md','VERIFY_TESTS.json','check_math.py','verify.py'}
                need(len(names)==len(expected) and set(names)=={'6200022/'+n for n in expected},'author archive allowlist')
                need(z.testzip() is None,'author archive CRC')
                for name in names: (out/Path(name).name).write_bytes(z.read(name))
            result['author']=test(out,tmp/'author',author=True)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
