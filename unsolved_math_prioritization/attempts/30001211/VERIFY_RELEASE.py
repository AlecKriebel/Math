#!/usr/bin/env python3
"""Strict, portable release check. Finite replays do not prove asymptotic claims."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
AUTHOR='96e071e004aef40ae132a5ec27c8c8aaacf55b5fd52202ef1da25999771db544'
AUDIT='aa7c9ada9fd76d97c7b68275b54c3fb3bc795367fd77ccbe8d5db22a986e53cf'

def digest(data): return hashlib.sha256(data).hexdigest()
def verify_entries(root,manifest,strict=False):
    entries=manifest['files']; paths=[]
    for row in entries:
        p=row['path']; parts=PurePosixPath(p)
        assert isinstance(p,str) and not parts.is_absolute() and '..' not in parts.parts
        assert p==parts.as_posix() and p and '\\' not in p
        f=root/p
        assert f.is_file() and not f.is_symlink(),p
        raw=f.read_bytes()
        assert len(raw)==row['bytes'],p
        assert digest(raw)==row['sha256'],p
        paths.append(p)
    assert len(paths)==len(set(paths)),'duplicate paths'
    if strict:
        actual={str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}
        assert actual==set(paths)|{'RELEASE_MANIFEST.json'},'unexpected or missing file'
    return len(paths)

def verify(root):
    raw=(root/'public/MANIFEST.json').read_bytes()
    assert digest(raw)==AUTHOR,'original author manifest changed'
    verify_entries(root/'public',json.loads(raw))
    raw=(root/'audit/AUDIT_MANIFEST.json').read_bytes()
    assert digest(raw)==AUDIT,'original audit manifest changed'
    verify_entries(root/'audit',json.loads(raw))
    return verify_entries(root,json.loads((root/'RELEASE_MANIFEST.json').read_bytes()),True)

def main():
    checked=verify(ROOT)
    outputs=[]
    for script,expected,count in [('public/verification/check.py','public/verification/result.json',105120),
                                   ('audit/discriminating_checks.py','audit/discriminating_results.json',175860)]:
        result=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,check=True,timeout=180)
        assert not result.stderr,script
        assert result.stdout==(ROOT/expected).read_bytes(),script+' output differs'
        report=json.loads(result.stdout)
        assert report['status']=='PASS' and report['total_assertions']==count
        outputs.append({'script':script,'assertions':count,'output_sha256':digest(result.stdout)})
    failures=[]
    for mutation in ['change_author_bytes','extra_file','remove_audit_file','wrong_byte_count','unsafe_path']:
        with tempfile.TemporaryDirectory(prefix='iet-release-check-') as temp:
            copy=Path(temp)/'packet';shutil.copytree(ROOT,copy)
            if mutation=='change_author_bytes':
                f=copy/'public/RESULT.md';f.write_bytes(f.read_bytes()+b'\nMUTATION\n')
            elif mutation=='extra_file':(copy/'unexpected.txt').write_text('MUTATION')
            elif mutation=='remove_audit_file':(copy/'audit/discriminating_results.json').unlink()
            else:
                f=copy/'RELEASE_MANIFEST.json';m=json.loads(f.read_bytes())
                if mutation=='wrong_byte_count':m['files'][0]['bytes']+=1
                else:m['files'][0]['path']='../outside.txt'
                f.write_text(json.dumps(m))
            try: verify(copy)
            except (AssertionError,FileNotFoundError):failures.append(mutation)
            else: raise AssertionError('undetected mutation: '+mutation)
    assert len(failures)==5
    print(json.dumps({'status':'PASS','manifest_files':checked,'author_manifest_sha256':AUTHOR,'audit_manifest_sha256':AUDIT,'replays':outputs,'integrity_negative_controls':failures,'limits':'Finite replay and integrity checks; not a full IET resolution, novelty certification, or literature completeness claim.'},indent=2))

if __name__=='__main__':main()
