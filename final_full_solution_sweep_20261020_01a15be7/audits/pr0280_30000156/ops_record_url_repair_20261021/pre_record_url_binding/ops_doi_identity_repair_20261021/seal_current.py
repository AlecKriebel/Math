#!/usr/bin/env python3
"""Current DOI/directory repair seal; prior manifests are immutable historical inputs."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=HERE/'pre_review03_binding'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py',
         'publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']
OLD_SHA='96702c6f1b8981817fa4b8ae2b6201fab36f4518418274f7b584de924918c8de'
ROOT_SHA='4db5e01602ed978612c58aaa1736cd894a8b4123f7de7c6d51e14a344546febb'


def sha(data):return hashlib.sha256(data).hexdigest()


def check_inputs():
    entries=json.loads((HERE/'INPUT_PRESERVATION.json').read_text())['files']
    if len(entries)!=53:raise RuntimeError('Preserved input inventory differs')
    for e in entries:
        body=(FROZEN/e['path']).read_bytes()
        if len(body)!=e['bytes'] or sha(body)!=e['sha256']:raise RuntimeError('Preserved input differs: '+e['path'])
    old=AUDIT/'ops_repair_20261021/MANIFEST.json'
    if sha(old.read_bytes())!=OLD_SHA:raise RuntimeError('Historical44 manifest changed')
    for e in json.loads(old.read_text())['files']:
        body=(FROZEN/e['path']).read_bytes()
        if len(body)!=e['bytes'] or sha(body)!=e['sha256']:raise RuntimeError('Old44 cannot be reconstructed')
    root=AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json'
    if sha(root.read_bytes())!=ROOT_SHA:raise RuntimeError('Root reconciliation changed')
    release=AUDIT/'preprint/publication/RELEASE_FILES.json'
    for name in ['RELEASE_FILES.json']+[e['path'] for e in json.loads(release.read_text())['files']]:
        if (release.parent/name).read_bytes()!=(FROZEN/'preprint/publication'/name).read_bytes():raise RuntimeError('Scientific file changed')
    snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())
    for e in snapshot['files']:
        body=(AUDIT/e['snapshot']).read_bytes()
        if len(body)!=e['bytes'] or sha(body)!=e['sha256']:raise RuntimeError('Original17 changed')
    for e in json.loads((HERE/'CURRENT_HELPER_BINDING.json').read_text())['files']:
        body=(AUDIT/e['path']).read_bytes()
        if len(body)!=e['bytes'] or sha(body)!=e['sha256']:raise RuntimeError('Current helper binding changed')


def selection():
    check_inputs()
    excluded={HERE/'MANIFEST.json',HERE/'MANIFEST.sha256'}
    paths=[p for p in HERE.rglob('*') if p.is_file() and p not in excluded and '__pycache__' not in p.parts]
    paths += [AUDIT/n for n in HELPERS]+[AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',AUDIT/'SOURCE_SNAPSHOT.json']
    release=AUDIT/'preprint/publication/RELEASE_FILES.json'
    paths += [release]+[release.parent/e['path'] for e in json.loads(release.read_text())['files']]
    paths += [AUDIT/e['snapshot'] for e in json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())['files']]
    paths += [AUDIT/'reviews/package_adversary_03/AUTHORED_FILE_MANIFEST.json']
    if len(paths)!=len(set(paths)) or any(p.is_symlink() for p in paths):raise RuntimeError('Unsafe or duplicate seal path')
    return sorted(paths)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    path=HERE/'MANIFEST.json';checksum=HERE/'MANIFEST.sha256';paths=selection()
    if args.verify:
        value=json.loads(path.read_text())
        if checksum.read_text().split()[0]!=sha(path.read_bytes()):raise RuntimeError('Current repair seal differs')
        if {p.relative_to(AUDIT).as_posix() for p in paths}!={e['path'] for e in value['files']}:raise RuntimeError('Repair inventory differs')
        for e in value['files']:
            body=(AUDIT/e['path']).read_bytes()
            if len(body)!=e['bytes'] or sha(body)!=e['sha256']:raise RuntimeError('Sealed file changed: '+e['path'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':sha(path.read_bytes()),'old44_reconstructed':True}))
        return
    value={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':280,'completion_estimate_percent':100,
           'publication_ready':False,'scope':'Local DOI/directory operations repair only; NEW whole-package reviewer04 required. No scientific promotion or lifecycle/provider outcomes asserted.',
           'previous44_manifest_sha256':OLD_SHA,'root_reconciliation_sha256':ROOT_SHA,
           'files':[{'path':p.relative_to(AUDIT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths]}
    path.write_text(json.dumps(value,indent=2)+'\n');checksum.write_text(sha(path.read_bytes())+'  MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':sha(path.read_bytes())}))


if __name__=='__main__':main()
