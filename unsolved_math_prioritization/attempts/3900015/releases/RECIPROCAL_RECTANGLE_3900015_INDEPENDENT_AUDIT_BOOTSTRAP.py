#!/usr/bin/env python3
"""Independent trust-root bootstrap for the exact accepted audit archive."""
import hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
ARCHIVE_NAME='RECIPROCAL_RECTANGLE_3900015_INDEPENDENT_AUDIT_SAFE.zip'
ARCHIVE_BYTES=40619
ARCHIVE_SHA256='9ee19f929512178ad3da1a565a164570a94b014e73e80ffb877184c0fac1212b'
MANIFEST_NAME='RECIPROCAL_RECTANGLE_3900015_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'
MANIFEST_SHA256='299ab86e0bbcf4774615895f6a60d43f5e5f1ba6216341117eb3501927ebe97a'

def require(ok,message):
    if not ok:raise ValueError(message)

def digest(b):return hashlib.sha256(b).hexdigest()

def run():
    directory=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
    b=(directory/ARCHIVE_NAME).read_bytes()
    require(len(b)==ARCHIVE_BYTES and digest(b)==ARCHIVE_SHA256,'audit archive trust-root mismatch')
    b=(directory/MANIFEST_NAME).read_bytes()
    require(digest(b)==MANIFEST_SHA256,'external manifest trust-root mismatch')
    manifest=json.loads(b)
    require(manifest['archive']['sha256']==ARCHIVE_SHA256,'external archive identity mismatch')
    with tempfile.TemporaryDirectory(prefix='verified-reciprocal-audit-') as temporary:
        root=Path(temporary)
        with zipfile.ZipFile(directory/ARCHIVE_NAME) as z:
            entries=z.infolist()
            require(len(entries)==len(manifest['files']) and {x.filename for x in entries}==set(manifest['files']),'ZIP inventory mismatch')
            for member in entries:
                name=member.filename
                require(name==Path(name).name and not member.is_dir(),'unsafe ZIP member')
                require((member.external_attr>>16)&0o170000 != 0o120000,'ZIP symlink rejected')
                b=z.read(member);meta=manifest['files'][name]
                require(len(b)==meta['bytes'] and digest(b)==meta['sha256'],'ZIP member mismatch: '+name)
                (root/name).write_bytes(b)
        for optimized in [False,True]:
            command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/'verify_audit.py')]
            result=subprocess.run(command,cwd=temporary,capture_output=True,text=True,timeout=90)
            require(result.returncode==0,'audit replay failed: '+result.stderr)
            payload=json.loads(result.stdout)
            require(payload.get('verified') is True and payload.get('full_problem_resolved') is False,'invalid audit output')
        print(json.dumps({'bootstrap_verified':True,'audit_archive_sha256':ARCHIVE_SHA256,'normal_and_optimized_replay':True,'full_problem_resolved':False},sort_keys=True))

if __name__=='__main__':
    try:run()
    except Exception as exc:
        print('BOOTSTRAP FAILED: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
