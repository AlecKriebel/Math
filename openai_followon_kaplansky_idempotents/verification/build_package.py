#!/usr/bin/env python3
"""Build a deterministic source/audit archive and freeze its review manifest.

No network, publication or shared-index operation is performed.
Complete-package review verdicts live outside the immutable archive.
"""
from pathlib import Path
import datetime
import hashlib
import json
import sys
import zipfile

project = Path(__file__).resolve().parents[1]
version = sys.argv[1]
names = [
    'main.tex', 'README.md', 'CURRENT_THEOREM.md', 'DEPENDENCY_LEDGER.md',
    'APPROACH_TABLE.md', 'LICENSES.md', 'LICENSE_CODE.txt',
    'sources/SOURCE_MANIFEST.json', 'sources/PRIORITY_SOURCE_MANIFEST.json',
    'sources/UPSTREAM_LICENSE.txt',
    'notes/ALGEBRA_PROOF.md', 'notes/PRIORITY_AUDIT.md',
    'notes/CLASSICAL_PROVENANCE_AUDIT.md',
    'notes/EXTENSION_PARAMETER_AUDIT.md',
    'notes/EXTENSION_PARAMETER_FALSIFICATION.md',
    'notes/EXTENSION_PRIORITY_ATTACK.md', 'notes/EXTENSION_EMBEDDING_AUDIT.md',
    'reviews/source_combinatorics.md', 'reviews/source_topology.md',
    'data/plane32_incidence.json',
    'verification/verify.py', 'verification/verify_parameter.py',
    'verification/verify_plane32.py', 'verification/verify_embedding.py',
    'verification/reproduce.py', 'verification/build_package.py',
]
names.extend(str(x.relative_to(project)) for x in
             sorted((project/'notes/priority_evidence').glob('*')) if x.is_file())

def entry(name):
    data = (project/name).read_bytes()
    return {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

payload = [entry(name) for name in names]
archive_manifest = json.dumps({'version': version, 'files': payload,
    'scope': 'Authored source, finite certificates, proof audits and source identities; no third-party manuscripts or successful matching certificate.'},
    indent=2).encode()+b'\n'
archive = project/'source-and-audit.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name in names+['SOURCE_ARCHIVE_MANIFEST.json']:
        info = zipfile.ZipInfo(name, date_time=(2026,10,6,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, archive_manifest if name=='SOURCE_ARCHIVE_MANIFEST.json'
                   else (project/name).read_bytes())
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:
        raise RuntimeError('Archive CRC failed')
    for item in payload:
        data = z.read(item['path'])
        if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise RuntimeError('Archive member mismatch: '+item['path'])
record = {'version': version, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'files': payload+[entry('paper.pdf'),entry('source-and-audit.zip'),entry('zenodo-deposit.json')],
          'archive_members': names+['SOURCE_ARCHIVE_MANIFEST.json'],
          'no_review_verdict_in_immutable_archive': True}
target = project/'reviews'/(version+'_manifest.json')
if target.exists():
    raise RuntimeError('Refusing to overwrite an existing review version manifest')
target.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'manifest':str(target.relative_to(project)), 'scientific_files':len(record['files']),
                  'archive_members':len(record['archive_members']), 'archive':entry('source-and-audit.zip')},indent=2))
