#!/usr/bin/env python3
"""Local audit bindings only. No remote, Git, service, or candidate mutation."""
from pathlib import Path
import hashlib,json

p=Path(__file__).resolve().parent
audit=p.parent
packet=audit/'snapshot/problems/30004322_arrangement_seshadri'
H=lambda b:hashlib.sha256(b).hexdigest()
snap=json.loads((audit/'snapshot_manifest.json').read_text())
assert snap['head']=='5da73632ab7a621de7b62edb5f70dfb8017e4a50'
for e in snap['files']:
    b=(audit/'snapshot'/e['path']).read_bytes()
    assert len(b)==e['bytes'] and H(b)==e['sha256']
seal=json.loads((p/'independence_seal.json').read_text())
for path,h in seal['files'].items():
    assert H((p/path).read_bytes())==h,path
remote=json.loads((packet/'review/REMOTE_BINDING.json').read_text())
for e in remote['files']:
    b=(packet/e['path']).read_bytes()
    assert len(b)==e['bytes'] and H(b)==e['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['expected_git_blob']==e['remote_git_blob']
review=json.loads((packet/'review/REVIEW_MANIFEST.json').read_text())
for e in review['files']:
    b=(packet/'review'/e['path']).read_bytes()
    assert len(b)==e['bytes'] and H(b)==e['sha256']
assert (p/'old_independent.full.stdout.txt').read_bytes()==(packet/'review/INDEPENDENT_CHECKS.json').read_bytes()
author=json.loads((p/'author_replay.full.stdout.txt').read_text())
assert author=={'all_receipts_byte_exact':True,'assertions':214070,'manifest_entries':62,'source_files_checked':0}
assert (p/'author_replay.full.stderr.txt').read_bytes()==b''
assert (p/'old_independent.full.stderr.txt').read_bytes()==b''
sources=json.loads((packet/'SOURCE_MANIFEST.json').read_text())['files']
pdf_map={'sources/owr2019-53.pdf':'source/owr201953.pdf','sources/pokora2017.pdf':'source/pokora_1711_09364v3.pdf'}
for e in sources:
    if e['path'] in pdf_map:
        b=(p/pdf_map[e['path']]).read_bytes()
        assert H(b)==e['sha256'] and len(b)==e['bytes']
result={
    'frozen_head':snap['head'],'snapshot_manifest_sha256':H((audit/'snapshot_manifest.json').read_bytes()),
    'snapshot_files_verified':len(snap['files']),'pre_exposure_seal_files_verified':len(seal['files']),
    'historical_remote_capture_local_blob_bindings_verified':len(remote['files']),
    'historical_review_manifest_entries_verified':len(review['files']),
    'fresh_remote_verification':False,
    'author_assertions_replayed':author['assertions'],'author_manifest_entries_replayed':author['manifest_entries'],
    'prior_independent_assertions_replayed':93918,'prior_independent_stdout_byte_exact':True,
    'portable_replay_source_files_checked':0,
    'separately_downloaded_primary_pdf_source_hashes_verified':len(pdf_map),
    'not_checked_historical_source_artifacts':['sources/curve-config.pdf','sources/printed3297.png','sources/hanumanthu-harbourne2021.pdf','sources/janasz-pokora2020.pdf'],
    'all_local_bindings':'PASS'
}
print(json.dumps(result,indent=2,sort_keys=True))
