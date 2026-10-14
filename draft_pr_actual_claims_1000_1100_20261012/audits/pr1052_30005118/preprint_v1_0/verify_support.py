#!/usr/bin/env python3
"""Verify current payload, archive, sidecar, and optional external upload wrapper."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
TITLE = 'Cyclic self-sumset recognition: a credited corollary of the integer hardness theorem'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def safe(name):
    require(isinstance(name, str) and name and '\\' not in name and ':' not in name and '\x00' not in name, 'invalid member path')
    p = PurePosixPath(name)
    require(not p.is_absolute() and all(x not in ('', '.', '..') for x in name.split('/')), 'unsafe member path')
    return name

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify_metadata():
    z = json.loads((ROOT/'.zenodo.json').read_text())
    w = json.loads((ROOT/'metadata.json').read_text())
    require(z == w['metadata'], 'metadata copies disagree')
    require(z['title'] == TITLE and z['upload_type'] == 'publication' and z['publication_type'] == 'preprint', 'invalid publication identity')
    require(z['version'] == '1.0' and z['publication_date'] == '2026-10-14' and z['language'] == 'eng', 'invalid version/date/language')
    require(z['license'] == 'cc-by-4.0' and z['access_right'] == 'open', 'invalid license/access')
    require(z['creators'] == [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher', 'orcid': '0009-0001-9320-500X'}], 'invalid creator')
    require(w['publication_ready'] is False and w['all_issues_resolved'] is False, 'preparation hold changed')
    require(w['preparation_snapshot_date'] == '2026-10-14' and w['stage'] == 'PENDING_NEW_WHOLE_02', 'current preparation stage/date changed')
    require(z['notes'] == 'Alec Kriebel is the sole named author. OpenAI Codex AI systems were used extensively. Exact historical priority of the cyclic formulation is unknown. Prepared locally on 2026-10-14 before deposit or publication.', 'dated preparation notes changed')
    require(w['pr'] == 1052 and w['problem_id'] == 30005118 and not w['novelty_established'] and not w['human_peer_review'] and not w['formal_certification'], 'scope/status changed')
    require('iff P=NP' in z['description'] and 'Extensive AI assistance' in z['description'] and 'Unrefereed' in z['description'], 'missing conditional/disclosure')
    return z

def verify_payload():
    allow = json.loads((ROOT/'SUPPORT_ALLOWLIST.json').read_text())['members']
    require(len(allow) == len(set(allow)), 'duplicate allowlist entry')
    for name in allow:
        safe(name)
        p = ROOT/name
        require(p.is_file() and not p.is_symlink(), 'missing or nonregular payload')
        p.resolve().relative_to(ROOT)
    manifest = json.loads((ROOT/'SUPPORT_MANIFEST.json').read_text())
    require(manifest['members'] == sorted(allow), 'manifest allowlist mismatch')
    expected = set(allow)-{'SUPPORT_MANIFEST.json'}
    entries = manifest['entries']
    require({e['path'] for e in entries} == expected and len(entries) == len(expected), 'manifest missing/duplicate entries')
    for e in entries:
        data = (ROOT/safe(e['path'])).read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'payload hash mismatch: '+e['path'])
    require('zenodo-deposit.json' not in allow and not any('raw/' in x or 'private_raw/' in x for x in allow), 'excluded source/deposit entered archive')
    verify_metadata()
    mapping = json.loads((ROOT/'support/COPY_MAP.json').read_text())['copies']
    require(len(mapping) == len({x['package_path'] for x in mapping}), 'duplicate copy map')
    for e in mapping:
        data = (ROOT/safe(e['package_path'])).read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'frozen copy mismatch')
    return allow

def verify_archive(path, members):
    require(path.is_file() and not path.is_symlink(), 'archive missing/nonregular')
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        require([i.filename for i in infos] == sorted(members), 'archive member set/order changed')
        for i in infos:
            safe(i.filename)
            require(not i.is_dir() and stat.S_ISREG(i.external_attr >> 16) and (i.external_attr >> 16) & 0o777 == 0o644, 'archive mode changed')
            require(i.date_time == (2026, 10, 14, 0, 0, 0) and i.compress_type == zipfile.ZIP_STORED, 'archive determinism fields changed')
            require(z.read(i) == (ROOT/i.filename).read_bytes(), 'archive payload differs')
        require(z.testzip() is None, 'archive CRC failure')
    sidecar = Path(str(path)+'.sha256')
    require(sidecar.read_text() == sha(path.read_bytes())+'  '+path.name+'\n', 'archive sidecar mismatch')

def verify_upload_if_present():
    p = ROOT/'zenodo-deposit.json'
    if not p.exists():
        return 'intentionally absent from extracted support archive'
    d = json.loads(p.read_text())
    require(set(d) == {'metadata', 'files'}, 'unexpected external wrapper fields')
    require(d['metadata'] == verify_metadata(), 'external metadata mismatch')
    required = ['paper.pdf', 'pr1052_support_v1_0.zip']
    require(len(d['files']) == 2 and [x['filename'] for x in d['files']] == required, 'external upload file set changed')
    for e in d['files']:
        require(set(e) == {'filename', 'bytes', 'sha256'}, 'unexpected upload binding fields')
        data = (ROOT/safe(e['filename'])).read_bytes()
        require(type(e['bytes']) is int and e['bytes'] == len(data) and e['sha256'] == sha(data), 'upload file binding mismatch')
    return 'present, metadata and both upload files verified'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--archive')
    args = ap.parse_args()
    members = verify_payload()
    if args.archive:
        path = ROOT/args.archive
        path.resolve().relative_to(ROOT)
        verify_archive(path, members)
    print(json.dumps({'payload_members': len(members), 'all_checks_passed': True, 'upload_wrapper': verify_upload_if_present()}))

if __name__ == '__main__':
    main()
