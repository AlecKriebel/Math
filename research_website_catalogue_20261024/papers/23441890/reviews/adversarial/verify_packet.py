#!/usr/bin/env python3
"""Read-only owned-packet, input and all-native-payload integrity check."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile

HERE=Path(__file__).resolve().parent
SOURCES=HERE.parents[1]/'sources'


def ck(value,name):
    if not value:raise RuntimeError(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


mp=HERE/'ARTIFACT_MANIFEST.json'
manifest=json.loads(mp.read_text());expected={}
for e in manifest['files']:
    name=e['relative_path'];q=PurePosixPath(name)
    ck(not q.is_absolute() and '..' not in q.parts and name not in expected,
       'unsafe/duplicate packet path')
    expected[name]=e
actual=set()
for p in HERE.rglob('*'):
    ck(not p.is_symlink(),'packet symlink')
    if p.is_file():actual.add(p.relative_to(HERE).as_posix())
ck(actual==set(expected)|{'ARTIFACT_MANIFEST.json','FINAL_SEAL.json'},
   'unexpected/missing packet file')
for name,e in expected.items():
    p=HERE/name
    ck(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],
       'owned packet mismatch: '+name)
seal=json.loads((HERE/'FINAL_SEAL.json').read_text())
ck(sha(mp)==seal['artifact_manifest_sha256'],'artifact manifest seal mismatch')
for name,field in [('INITIAL_RECONSTRUCTION.md','initial_reconstruction_sha256'),
                   ('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),
                   ('DERIVATIONS.md','derivations_sha256'),
                   ('INPUT_MANIFEST.json','input_manifest_sha256')]:
    ck(sha(HERE/name)==seal[field],field+' mismatch')
inputs=json.loads((HERE/'INPUT_MANIFEST.json').read_text())
for e in inputs['files']:
    p=Path(e['path'])
    ck(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],
       'input mismatch: '+str(p))
count=0
with zipfile.ZipFile(SOURCES/'source-and-verification.zip') as z:
    for member in z.infolist():
        if not member.is_dir():
            count+=1
            ck((SOURCES/'published-source'/member.filename).read_bytes()==z.read(member),
               'native payload mismatch: '+member.filename)
ck(count==16,'native payload count mismatch')
ck((SOURCES/'paper.pdf').read_bytes()==(SOURCES/'published-source/kourovka-21-149/paper.pdf').read_bytes(),
   'embedded PDF differs')
print(json.dumps({'status':'PASS','owned_files_verified':len(expected),
                  'input_files_verified':len(inputs['files']),
                  'native_payloads_verified':count,
                  'artifact_manifest_sha256':sha(mp),
                  'final_seal_sha256':sha(HERE/'FINAL_SEAL.json'),
                  'scope':'Custody/integrity only. Infinite mathematics is in DERIVATIONS.md.'},
                 indent=2,sort_keys=True))
