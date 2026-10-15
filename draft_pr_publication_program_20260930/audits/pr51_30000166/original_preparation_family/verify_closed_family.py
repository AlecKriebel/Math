"""Separate SOURCE-only readback, for ROOT after actual closer child exit. No writes."""
import argparse
import hashlib
import json
from pathlib import Path
import stat

F=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--expected-index-sha256',required=True)
    p.add_argument('--expected-ready-sha256',required=True)
    p.add_argument('--expected-manifest-sha256')
    a=p.parse_args()
    assert F.name=='original_preparation_family' and F.parent.name=='pr51_30000166'
    m=F/'SELF_MANIFEST.json';mp=sha(m)
    if a.expected_manifest_sha256:assert mp==a.expected_manifest_sha256
    assert sha(F/'FIXED_PAYLOAD_INDEX.json')==a.expected_index_sha256
    assert sha(F/'READY.md')==a.expected_ready_sha256
    index=json.loads((F/'FIXED_PAYLOAD_INDEX.json').read_text())
    value=json.loads(m.read_text())
    assert index['schema']=='pr51-original-preparation-fixed-payload-index/v1'
    assert index['future_authority'] is False
    assert value['schema']=='pr51-original-preparation-self-only-manifest/v1'
    assert value['family_path']==str(F)==index['family_path']
    assert value['index_sha256']==a.expected_index_sha256 and value['ready_sha256']==a.expected_ready_sha256
    assert value['status']=='CLOSED_PREPARATION_SOURCE_ONLY'
    assert value['publication_approved'] is False and value['production_execution_approved'] is False
    assert value['independent_math_acceptance_supplied'] is False
    files=[];dirs=['.']
    for f in sorted(F.rglob('*')):
        s=f.lstat();r=f.relative_to(F).as_posix()
        assert not stat.S_ISLNK(s.st_mode),r
        if stat.S_ISDIR(s.st_mode):dirs.append(r)
        else:
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o444,r
            files.append(r)
    names=[q['path'] for q in value['files']]
    assert names==sorted(set(names)) and len(names)==value['files_count']
    assert files==sorted(names+['SELF_MANIFEST.json'])
    assert sorted(dirs)==value['directories']==index['directories']
    expected=[q['path'] for q in index['files']]
    assert expected==sorted(set(expected)) and len(expected)==index['files_count']
    assert names==sorted(expected+['FIXED_PAYLOAD_INDEX.json','READY.md'])
    bound={q['path']:q for q in index['files']}
    for q in value['files']:
        r=q['path']
        assert Path(r).as_posix()==r and not Path(r).is_absolute() and '..' not in Path(r).parts
        f=F/q['path'];assert q['mode']=='0444'
        assert f.stat().st_size==q['bytes'] and sha(f)==q['sha256']
        if q['path'] in bound:
            e=bound[q['path']];assert q['bytes']==e['bytes'] and q['sha256']==e['sha256']
    print(json.dumps({'status':'PASS_SOURCE_ONLY_CLOSED_READBACK',
                      'manifest_sha256':mp,'files_count':len(names),
                      'directories_count':len(dirs),'publication_approved':False,
                      'independent_math_acceptance_supplied':False}))


if __name__=='__main__':main()
