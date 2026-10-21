"""SOURCE ONLY. ROOT may run after preparer exit; closes only this fixed private family."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import stat

F=Path(__file__).resolve().parent
INDEX='FIXED_PAYLOAD_INDEX.json'
READY='READY.md'
MANIFEST='SELF_MANIFEST.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def inventory():
    files=[];dirs=['.']
    for p in sorted(F.rglob('*')):
        s=p.lstat();r=p.relative_to(F).as_posix()
        assert not stat.S_ISLNK(s.st_mode),r
        if stat.S_ISDIR(s.st_mode):dirs.append(r)
        else:
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1,r
            files.append(r)
    return files,sorted(dirs)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--expected-index-sha256',required=True)
    p.add_argument('--expected-ready-sha256',required=True)
    p.add_argument('--after-preparer-exit',action='store_true',required=True)
    a=p.parse_args()
    assert F.name=='original_preparation_family' and F.parent.name=='pr51_30000166'
    assert a.after_preparer_exit and not (F/MANIFEST).exists()
    assert sha(F/INDEX)==a.expected_index_sha256 and sha(F/READY)==a.expected_ready_sha256
    index=json.loads((F/INDEX).read_text())
    assert index['schema']=='pr51-original-preparation-fixed-payload-index/v1'
    assert index['family_path']==str(F) and index['future_authority'] is False
    expected=index['files'];names=[q['path'] for q in expected]
    assert names==sorted(set(names)) and len(names)==index['files_count']
    files,dirs=inventory()
    assert files==sorted(names+[INDEX,READY]) and dirs==index['directories']
    rows=[]
    for q in expected:
        r=q['path'];f=F/r
        assert Path(r).as_posix()==r and not Path(r).is_absolute() and '..' not in Path(r).parts
        assert f.stat().st_size==q['bytes'] and sha(f)==q['sha256'],r
    for r in files:
        f=F/r;s=f.lstat()
        assert stat.S_IMODE(s.st_mode)==0o444,r
        rows.append({'path':r,'bytes':s.st_size,'sha256':sha(f),'mode':'0444'})
    value={'schema':'pr51-original-preparation-self-only-manifest/v1',
           'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'family_path':str(F),'status':'CLOSED_PREPARATION_SOURCE_ONLY',
           'original_head':'8006dd5f134ad0a2fa930e7278d3cb17945f4201',
           'index_sha256':a.expected_index_sha256,'ready_sha256':a.expected_ready_sha256,
           'files_count':len(rows),'files':rows,'directories':dirs,
           'manifest_excludes_only_itself':MANIFEST,
           'publication_approved':False,'production_execution_approved':False,
           'independent_math_acceptance_supplied':False}
    m=F/MANIFEST
    with m.open('x') as t:t.write(json.dumps(value,indent=2)+'\n')
    m.chmod(0o444)
    print(json.dumps({'manifest':str(m),'manifest_sha256':sha(m),
                      'files_count':len(rows),'directories_count':len(dirs),
                      'status':'CLOSED_PREPARATION_SOURCE_ONLY'}))


if __name__=='__main__':main()
