#!/usr/bin/env python3
"""Closed public namespace verifier; no writes, network, subprocesses or Git mutation."""
import argparse, gzip, hashlib, json, pathlib

parser=argparse.ArgumentParser()
parser.add_argument('--require-private',action='store_true')
args=parser.parse_args()
public=pathlib.Path(__file__).resolve().parent
own=public.parent;A=own.parent;private=own/'private'
def h(data):return hashlib.sha256(data).hexdigest()
def read_json(p):return json.loads(p.read_text())
mf=read_json(public/'PUBLIC_MANIFEST.json')
listed={entry['path'] for entry in mf['files']}
assert len(listed)==len(mf['files'])
actual={str(p.relative_to(public)) for p in public.rglob('*') if p.is_file()}
assert actual==listed|{'PUBLIC_MANIFEST.json'}
assert not any(p.is_symlink() for p in public.rglob('*'))
for entry in mf['files']:
    p=public/entry['path'];assert p.parent==public
    data=p.read_bytes();assert len(data)==entry['bytes'] and h(data)==entry['sha256']
for document,receipt in [('independent_graph_analysis.md','independent_source_seal.json'),('candidate_analytic_assessment.md','candidate_analytic_seal.json')]:
    seal=read_json(public/receipt);data=(public/document).read_bytes()
    assert seal['sha256']==h(data) and seal['bytes']==len(data)
evidence=read_json(public/'FROZEN_EVIDENCE.json')
assert evidence['actual_paths']==42 and evidence['target_files']==41
assert evidence['nested_entries']==135 and evidence['historical_author_nested_entries']==88
assert len(evidence['scope'])==42
snapshot=A/'snapshot';snapshot_status='NOT_CHECKED_SNAPSHOT_ABSENT'
if snapshot.is_dir():
    snapshots={str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
    assert snapshots=={entry['path'] for entry in evidence['scope']}
    for entry in evidence['scope']:
        data=(snapshot/entry['path']).read_bytes()
        assert len(data)==entry['bytes'] and h(data)==entry['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['head_blob']
        assert entry['head_mode']=='100644'
    snapshot_status='ALL42_FROZEN_BYTES_MATCH'
controls=read_json(public/'GRAPH_CONTROLS.json')
assert controls['status']=='PASS' and controls['exact_assertions']==122568
assert controls['minimum_integer_gap']=='1/108'
commands=read_json(public/'COMMAND_RECEIPTS.json')
sources=read_json(public/'SOURCE_RECEIPTS.json')
private_checks=[]
for entry in sources['private_artifact_hashes']:
    p=private/'sources'/entry['file'];available=p.is_file()
    if available:
        data=p.read_bytes();assert len(data)==entry['bytes'] and h(data)==entry['sha256']
    private_checks.append({'kind':'source_artifact','name':entry['file'],'available':available})
for kind,entries,location in [('outer',commands['outer'],private),('git',commands['git'],private/'frozen_evidence_capture')]:
    for entry in entries:
        if kind=='outer':
            folder=location/entry['capture_relative'];outpath=folder/'stdout.bin';errpath=folder/'stderr.bin'
        else:
            outpath=location/(entry['private_capture_stem']+'_stdout.bin.gz');errpath=location/(entry['private_capture_stem']+'_stderr.bin.gz')
        available=outpath.is_file() and errpath.is_file()
        if available:
            out=gzip.decompress(outpath.read_bytes()) if kind=='git' else outpath.read_bytes()
            err=gzip.decompress(errpath.read_bytes()) if kind=='git' else errpath.read_bytes()
            assert len(out)==entry['stdout_bytes'] and len(err)==entry['stderr_bytes']
            assert h(out)==entry['stdout_sha256'] and h(err)==entry['stderr_sha256']
            assert h(b'STDOUT\0'+out+b'STDERR\0'+err)==entry['logical_stream_sha256']
        private_checks.append({'kind':kind,'name':entry.get('name',entry.get('private_capture_stem')),'available':available})
private_complete=all(entry['available'] for entry in private_checks)
if args.require_private:assert private_complete
print(json.dumps({'status':'PASS_CLOSED_PUBLIC_NAMESPACE','public_files':len(actual),'manifest_entries':len(listed),'snapshot_status':snapshot_status,'collective_private_captures':'ALL_LISTED_HASHES_MATCH' if private_complete else 'INCOMPLETE_OR_ABSENT_NOT_FRESHLY_VERIFIED','private_components':len(private_checks),'missing_private_components':[entry for entry in private_checks if not entry['available']],'scope':'Integrity of this exact public namespace and available recorded evidence. No new Git/source fetch/replay, proof by count, true invariant-minimum evaluation or priority certificate is claimed.'},indent=2,sort_keys=True))
