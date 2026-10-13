"""Reopen all actual public bytes and native captures before the tracker write.

This supplements the reviewed publisher without changing its five sources.
Only a fresh real publication can produce this ROOT acceptance receipt.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
import sys, json, hashlib, stat
if sys.flags.optimize:
    raise RuntimeError('Optimized evidence checks are forbidden.')
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D/'publication_preparation'))
import submission_gate as g
from public_identity import identity, resolution_binding

def stamp(value):
    answer = datetime.fromisoformat(value.replace('Z', '+00:00'))
    assert answer.utcoffset() == timedelta(0)
    return answer

def whole(path):
    path = Path(path)
    assert path.resolve() == path and not path.is_symlink()
    assert stat.S_ISREG(path.lstat().st_mode)
    return path.read_bytes()

def inspect_native(directory, label, native, argv, outer):
    actual = json.loads(whole(directory/(label+'.execution.json')))
    assert actual == native
    assert actual['argv'] == argv and actual['cwd'] == str(D)
    assert actual['orchestrator_sha256'] == g.pin(D/'publication_preparation/public_identity.py')['sha256']
    assert actual['exit_code'] == 0 and actual['timed_out'] is False
    assert actual['automatic_retry'] is False
    assert actual['default_configuration_disabled'] is True and actual['origin_credentials_absent'] is True
    start, end = stamp(actual['started_utc']), stamp(actual['finished_utc'])
    assert stamp(outer['started_utc']) <= start <= end <= stamp(outer['ended_utc'])
    raw = {}
    for key in ['stdout', 'stderr']:
        raw[key] = whole(directory/(label+'.'+key))
        assert len(raw[key]) == actual[key+'_bytes']
        assert g.sha(raw[key]) == actual[key+'_sha256']
    assert not raw['stderr']
    return raw['stdout']

def verify(outer_label, public_label):
    assert Path(outer_label).name == outer_label and Path(public_label).name == public_label
    assert outer_label.startswith('root_pr305_public_record_actual') and public_label.startswith('public_readback_')
    lock = g.acquire()
    lease = g.window()
    outer_directory = D/'root_runs_private'/outer_label
    outer = json.loads(whole(outer_directory/'execution.json'))
    operator = D/'publication_preparation/verify_public_record.py'
    assert outer['argv'] == ['/opt/homebrew/bin/python3', '-E', '-B', str(operator), public_label]
    assert outer['cwd'] == str(D) and outer['exit_code'] == 0 and outer['stderr_bytes'] == 0
    assert outer['driver_sha256'] == g.sha(whole(D/'root_run.py'))
    assert outer['programs'] == [dict(path=str(operator), bytes=operator.stat().st_size, sha256=g.sha(whole(operator)))]
    for key in ['stdout', 'stderr']:
        raw = whole(outer_directory/(key+'.bin'))
        assert len(raw) == outer[key+'_bytes'] and g.sha(raw) == outer[key+'_sha256']
    now = datetime.now(timezone.utc)
    assert stamp(outer['started_utc']) <= stamp(outer['ended_utc']) <= now
    assert now - stamp(outer['ended_utc']) <= timedelta(seconds=120), 'Run a new read-only public verifier if actual readback has become stale.'
    published = json.loads(whole(g.OUT/'inspect_published_receipt.json'))
    assert published['state'] == 'published' and published['environment'] == 'production'
    rid = identity(published)
    resolution_binding(published['doi_resolution'], rid)
    local = json.loads(whole(g.O/'zenodo-deposit.json'))
    aggregate_path = g.OUT/'PUBLIC_RECORD_VERIFICATION.json'
    aggregate = json.loads(whole(aggregate_path))
    assert aggregate['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
    assert aggregate['record_id'] == rid and aggregate['doi'] == published['doi']
    assert aggregate['metadata_semantics_changed'] is False and aggregate['exact_record_identity_bound'] is True
    assert aggregate['no_mutation_or_person_contact'] is True
    assert aggregate['only_public_schema_mapping'] == ['license.id', 'resource_type.type', 'resource_type.subtype']
    directory = g.OUT/'private_public_downloads'/public_label
    assert aggregate['private_capture_directory'] == str(directory) and directory.resolve() == directory
    api = 'https://zenodo.org/api/records/'+str(rid)
    assert aggregate['public_api'] == api
    base = ['/usr/bin/curl','-q','--fail','--silent','--show-error','--location','--proto','=https','--proto-redir','=https','--no-netrc','--header','Authorization:','--header','Cookie:','--max-time','55','--user-agent','Math-Zenodo-Deposit-Tool/1.0']
    body = inspect_native(directory, 'record', aggregate['public_record_native'], base+[api], outer)
    record = json.loads(body)
    assert record['id'] == rid and record['doi'] == published['doi'] and record['metadata']['doi'] == published['doi']
    checked = []
    for key, expected in local['metadata'].items():
        metadata = record['metadata']
        actual = metadata['license']['id'] if key == 'license' else metadata['resource_type']['type'] if key == 'upload_type' else metadata['resource_type']['subtype'] if key == 'publication_type' else metadata[key]
        assert actual == expected, ('Metadata mismatch', key)
        checked.append(key)
    assert len(checked) == 11 and aggregate['all_reviewed_metadata_keys_compared'] == checked
    doi_url = 'https://doi.org/'+published['doi']
    resolution = aggregate['doi_resolution']
    resolution_binding(resolution, rid)
    assert resolution['controlled_unauthenticated_fresh_request'] is True
    raw = inspect_native(directory, 'exact_doi_resolution', resolution['native'], base+['--head','--output','/dev/null','--write-out','%{json}',doi_url], outer)
    resolved = json.loads(raw)
    assert resolved['http_code'] == resolution['http_status'] == 200
    assert resolved['url_effective'] == resolution['resolved_url']
    known = {e['name']: e for e in published['files']}
    accepted = {e['name']: e for e in aggregate['all_file_bytes']}
    remote = {e['key']: e for e in record['files']}
    assert len(published['files']) == len(aggregate['all_file_bytes']) == len(record['files']) == 2
    assert set(known) == set(accepted) == set(remote) == {'focal-pedal-ratios-note.pdf','focal-pedal-ratios-verification.zip'}
    labels = ['record', 'exact_doi_resolution']
    for name, file in remote.items():
        assert Path(name).name == name
        url = 'https://zenodo.org/api/records/'+str(rid)+'/files/'+name+'/content'
        assert file['links']['self'] == url
        label = 'file_'+name; labels.append(label)
        raw = inspect_native(directory, label, accepted[name]['native'], base+[url], outer)
        expected = whole(g.O/name)
        digest, md5 = g.sha(expected), hashlib.md5(expected).hexdigest()
        assert raw == expected and file['size'] == len(expected) and file['checksum'] == 'md5:'+md5
        assert known[name]['sha256'] == accepted[name]['sha256'] == digest
        assert known[name]['size'] == accepted[name]['bytes'] == len(expected) and accepted[name]['md5'] == md5
        assert accepted[name]['entire_public_download_equals_reviewed_local_file'] is True
    assert {p.name for p in directory.iterdir()} == {label+suffix for label in labels for suffix in ['.stdout','.stderr','.execution.json']}
    assert stamp(outer['started_utc']) <= stamp(aggregate['utc']) <= stamp(outer['ended_utc'])
    assert json.loads(whole(outer_directory/'stdout.bin')) == {k:v for k,v in aggregate.items() if k != 'all_file_bytes'}
    pins = {str(p):g.pin(p) for p in [aggregate_path,g.OUT/'inspect_published_receipt.json',outer_directory/'execution.json',outer_directory/'stdout.bin',outer_directory/'stderr.bin', *sorted(directory.iterdir())]}
    # This is the last actual read-only guard before a separate tracker action.
    g.current_clearance(); g.operational_clearance(); assert g.window() == lease
    assert datetime.now(timezone.utc)-stamp(outer['ended_utc']) <= timedelta(seconds=120)
    for path, expected in pins.items(): assert g.pin(path) == expected
    receipt = dict(status='PASS_PR305_ACTUAL_FULL_PUBLIC_EVIDENCE_AUTHENTICATED_BEFORE_TRACKER',utc=g.utc(),pr=305,record_id=rid,doi=published['doi'],record_url=published['record_url'],all_metadata_keys=checked,all_whole_files_and_MD5_and_SHA256_verified=True,all_actual_full_HTTP_streams_and_argv_and_cwd_and_programs_reopened=True,evidence_pins=pins,outer_native_capture=outer,lease_token=lease['token'],no_external_mutation=True,no_individual_contact=True)
    target = D/'ROOT_ACTUAL_PUBLIC_EVIDENCE_READBACK.json'
    assert not target.exists(), 'Preserve any earlier acceptance and reconcile before replacing it.'
    with target.open('x') as f: f.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__ == '__main__':
    assert len(sys.argv) == 3
    verify(sys.argv[1],sys.argv[2])
