"""Strict bundle inventory and diagnostic replay; no mathematical certification."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

EXPECTED_AUTHOR = {
    'proof': (16717, '74c727c159d7af1ec7be50c3766356f43a07171f3787a629627d2fce9bfe3a57'),
    'safe_archive': (19189, '1afc6d7c39a334dc3c271dfa2944426a92589236822d8a06fb97ca4c64e71d40'),
    'manifest': (1699, 'c9c1b418218bbb6f831908733d4b8a27d819cdd3abbb72a142d3f57aea3ab171'),
}


def must(value, message):
    if not value:
        raise RuntimeError(message)


def unique_object(pairs):
    answer={}
    for key,value in pairs:
        must(key not in answer, 'duplicate JSON key: '+key)
        answer[key]=value
    return answer


def decode(text):
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=lambda token: (_ for _ in ()).throw(RuntimeError('nonfinite JSON constant')))


def load(path):
    return decode(path.read_text(encoding='utf-8'))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def verify(root, external):
    manifest=load(root/'MANIFEST.json')
    must(set(manifest)=={'schema','files'} and type(manifest['schema']) is int and manifest['schema']==1, 'manifest schema')
    must(type(manifest['files']) is list, 'manifest files list')
    expected=set()
    for row in manifest['files']:
        must(type(row) is dict and set(row)=={'path','bytes','sha256'}, 'manifest entry schema')
        path=row['path']
        must(type(path) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',path) is not None and path!='MANIFEST.json', 'unsafe manifest path')
        must(path not in expected, 'duplicate manifest path')
        expected.add(path)
        must(type(row['bytes']) is int and row['bytes']>=0, 'invalid byte count')
        must(type(row['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}',row['sha256']) is not None, 'invalid digest')
        file=root/path
        must(not file.is_symlink() and file.is_file(), 'missing, symlink, or non-file member: '+path)
        content=file.read_bytes()
        must(len(content)==row['bytes'] and hashlib.sha256(content).hexdigest()==row['sha256'], 'member integrity failure: '+path)
    actual=set()
    for path in root.iterdir():
        must(not path.is_symlink() and path.is_file(), 'non-file or symlink in bundle')
        actual.add(path.name)
    must(actual==expected|{'MANIFEST.json'}, 'exact bundle inventory mismatch')
    binding=load(root/'AUTHOR_BINDING.json')
    for key,(size,digest) in EXPECTED_AUTHOR.items():
        must(type(binding[key]['bytes']) is int and binding[key]['bytes']==size and binding[key]['sha256']==digest, 'author binding mismatch')
        if external.get(key):
            contents=pathlib.Path(external[key]).read_bytes()
            must(len(contents)==size and hashlib.sha256(contents).hexdigest()==digest, 'external author mismatch: '+key)
    expected_result=load(root/'EXPECTED_RESULTS.json')
    run=subprocess.run([sys.executable,'-B','-O',str(root/'independent_diagnostics.py')],capture_output=True,text=True,check=True,timeout=60)
    result=decode(run.stdout)
    must(canonical(result)==canonical(expected_result), 'independent diagnostic exact replay mismatch')
    must(len(result['negative_controls'])==5 and all(value is True for value in result['negative_controls'].values()), 'negative control coverage')
    must(result['counts']['variable_stabilizer_models']==2 and result['counts']['complete_nonfree_slab_inventories']==10, 'required model coverage')
    must(all(type(value) is int and value>0 for value in result['counts'].values()), 'nonpositive or invalid test counter')
    return {'schema':1,'status':'passed','manifested_files':len(expected),'external_author_files_checked':sorted(external),'diagnostic_counts':result['counts'],'negative_controls_passed':len(result['negative_controls']),'certifies_infinite_theorem':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--author-proof')
    parser.add_argument('--author-zip')
    parser.add_argument('--author-manifest')
    args=parser.parse_args()
    external={key:value for key,value in {'proof':args.author_proof,'safe_archive':args.author_zip,'manifest':args.author_manifest}.items() if value}
    try:
        print(json.dumps(verify(args.root.resolve(),external),sort_keys=True,indent=2))
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc),file=sys.stderr)
        sys.exit(1)
