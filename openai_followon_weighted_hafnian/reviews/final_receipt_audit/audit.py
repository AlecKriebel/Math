#!/usr/bin/env python3
"""Bounded read-only receipt audit; output only in this review directory."""
import hashlib
import json
import subprocess
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/alec/Documents/Math/openai_followon_weighted_hafnian')
OUT = ROOT / 'reviews/final_receipt_audit'
OUT.mkdir(parents=True, exist_ok=True)
UTC = datetime.now(timezone.utc).isoformat()
RECORD = 23205294
DOI = '10.5281/zenodo.23205294'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
ROW = "'Math Puzzles'!A53:D53"
failures = []

def read(rel):
    return json.loads((ROOT / rel).read_text())

def h(data):
    return hashlib.sha256(data).hexdigest()

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def check(label, condition):
    if not condition:
        failures.append(label)
    return bool(condition)

def public_get(url, limit):
    req = urllib.request.Request(url, headers={'User-Agent': 'Independent-Receipt-Audit/1.0'})
    with urllib.request.urlopen(req, timeout=25) as response:
        data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError('Bounded response limit exceeded')
        return data, {'url': url, 'http_status': response.status, 'resolved_url': response.url,
                      'bytes': len(data), 'sha256': h(data)}

identity = read('publication/CANDIDATE_IDENTITY.json')
seal = read('reviews/package_review_05/V5_CUSTODY_SEAL.json')
delivery = read('reviews/package_review_05/DELIVERY_RECEIPT.json')
approval = read('receipts/ROOT_RELEASE_APPROVAL_V5.json')
prepublish = read('receipts/PREPUBLISH_VERIFICATION_V5.json')
manifest = read('zenodo-deposit.json')
current = {}
for rel, expected in seal['files'].items():
    data = (ROOT / rel).read_bytes()
    current[rel] = {'sha256': h(data), 'bytes': len(data),
                    'matches_seal': h(data) == expected['sha256'] and len(data) == expected['bytes']}
    check('Current sealed file differs: ' + rel, current[rel]['matches_seal'])
check('Custody seal hash differs from reviewer delivery',
      h((ROOT / 'reviews/package_review_05/V5_CUSTODY_SEAL.json').read_bytes()) == delivery['v5_custody_seal_sha256'])
report_path = Path(delivery['final_report']['path'])
check('Complete-review report hash mismatch', h(report_path.read_bytes()) == delivery['final_report']['sha256'])
check('Root approval reviewer report mismatch', approval['review_report_sha256'] == delivery['final_report']['sha256'])
check('Root approval custody mismatch', approval['review_custody_seal_sha256'] == delivery['v5_custody_seal_sha256'])
check('Root approval reviewed-file set mismatch', approval['exact_reviewed_files'] == seal['files'])
check('Candidate identity and custody differ', all(identity['files'][p]['sha256'] == seal['files'][p]['sha256'] and
      identity['files'][p]['bytes'] == seal['files'][p]['bytes'] for p in identity['files']))
authored = {}
for rel, expected in identity['authored_payload'].items():
    local_rel = 'manuscript/main.tex' if rel == 'main.tex' else 'manuscript/main.pdf' if rel == 'paper.pdf' else rel
    local = ROOT / local_rel
    actual = h(local.read_bytes())
    authored[rel] = {'sha256': actual, 'matches_identity': actual == expected}
    check('Authored payload differs: ' + rel, actual == expected)
with zipfile.ZipFile(ROOT / 'publication/zenodo-upload-kit/source-and-verification.zip') as archive:
    check('ZIP CRC mismatch', archive.testzip() is None)
    check('ZIP member set mismatch', set(archive.namelist()) == set(seal['zip_members']))
    check('ZIP contains duplicate names', len(archive.namelist()) == len(set(archive.namelist())))
    archive_members = {}
    for rel in archive.namelist():
        data = archive.read(rel)
        exp = seal['zip_members'][rel]
        archive_members[rel] = {'sha256': h(data), 'bytes': len(data)}
        check('ZIP sealed member differs: ' + rel, h(data) == exp['sha256'] and len(data) == exp['bytes'])
        if rel in identity['authored_payload']:
            check('ZIP member differs from current authored payload: ' + rel, h(data) == authored[rel]['sha256'])

receipt_names = ['zenodo_check_v5', 'zenodo_stage_v5', 'zenodo_inspect_draft_v5',
                 'zenodo_publish_v5', 'zenodo_inspect_published_v5']
sequence = []
expected_files = [{'name': Path(f['path']).name, 'size': current[f['path']]['bytes'],
                   'sha256': current[f['path']]['sha256']} for f in manifest['files']]
for name in receipt_names:
    value = read('receipts/' + name + '.json')
    check('Receipt environment differs: ' + name, value['environment'] == 'production')
    check('Receipt file set differs: ' + name, value['files'] == expected_files)
    check('Receipt title differs: ' + name, value['title'] == manifest['metadata']['title'])
    if 'id' in value:
        check('Receipt ID differs: ' + name, value['id'] == RECORD)
    if 'doi' in value:
        check('Receipt DOI differs: ' + name, value['doi'] == DOI)
    sequence.append({'receipt': name, 'id': value.get('id'), 'state': value.get('state'),
                     'verified_utc': value.get('verified_utc')})
for name in ['zenodo_publish_v5', 'zenodo_inspect_published_v5']:
    value = read('receipts/' + name + '.json')
    check('Published receipt not published: ' + name, value['state'] == 'published')
    check('Saved DOI resolution not 200: ' + name, value['doi_resolution']['http_status'] == 200 and
          value['doi_resolution']['resolved_url'] == f'https://zenodo.org/records/{RECORD}')
check('Prepublication confirmation ID differs', prepublish['actual_verified_draft_id'] == RECORD)
check('Prepublication gates do not pass', all(prepublish[x] for x in ['all_reviewed_bytes_unchanged',
      'remote_metadata_verified_by_repository_tool', 'remote_file_set_size_md5_match_reviewed_files']) and
      prepublish['submitted_before_publish'] is False)
check('Approval did not precede prepublish', approval['approved_utc'] < prepublish['verified_utc'])
check('Prepublish did not precede publication', prepublish['verified_utc'] < read('receipts/zenodo_publish_v5.json')['verified_utc'])
metadata_checks = {}
for name in ['zenodo_remote_draft_metadata_v5', 'zenodo_remote_published_metadata_v5']:
    receipt = read('receipts/' + name + '.json')
    comparisons = {}
    for key, expected in manifest['metadata'].items():
        actual = receipt['metadata'][key]
        if key == 'creators':
            actual = [{k: v for k, v in creator.items() if not (k == 'affiliation' and v is None)} for creator in actual]
        comparisons[key] = actual == expected
        check('Saved metadata differs: ' + name + '/' + key, comparisons[key])
    check('Saved metadata record differs: ' + name, receipt['id'] == RECORD and receipt['environment'] == 'production')
    metadata_checks[name] = comparisons

raw, record_get = public_get(f'https://zenodo.org/api/records/{RECORD}', 2_000_000)
(OUT / 'public_record.json').write_bytes(raw)
record = json.loads(raw)
check('Fresh public record ID differs', record['id'] == RECORD)
check('Fresh public record DOI differs', record['doi'] == DOI)
check('Fresh public file set differs', {f['key'] for f in record['files']} == {f['name'] for f in expected_files})
public_files = []
saved_downloads = {f['name']: f for f in read('receipts/zenodo_public_downloads_v5.json')['files']}
for f in record['files']:
    name = f['key']
    data, receipt = public_get(f['links']['self'], 1_000_000)
    (OUT / name).write_bytes(data)
    local = (ROOT / 'publication/zenodo-upload-kit' / name).read_bytes()
    receipt.update({'name': name, 'md5': hashlib.md5(data).hexdigest(), 'matches_current_bytes': data == local,
                    'public_api_size': f['size'], 'public_api_checksum': f['checksum'],
                    'matches_saved_download_receipt': h(data) == saved_downloads[name]['sha256'] and
                    len(data) == saved_downloads[name]['bytes']})
    check('Fresh public download differs from current: ' + name, data == local)
    check('Fresh public download differs from saved receipt: ' + name, receipt['matches_saved_download_receipt'])
    check('Fresh public checksum differs: ' + name, f['checksum'] == 'md5:' + receipt['md5'] and len(data) == f['size'])
    public_files.append(receipt)
public_metadata = record['metadata']
public_metadata_checks = {}
for key, expected in manifest['metadata'].items():
    if key in ('upload_type', 'publication_type'):
        actual = public_metadata['resource_type']['type' if key == 'upload_type' else 'subtype']
    elif key == 'license':
        actual = public_metadata['license']['id']
    else:
        actual = public_metadata[key]
        if key == 'creators':
            actual = [{k: v for k, v in creator.items() if not (k == 'affiliation' and v is None)} for creator in actual]
    public_metadata_checks[key] = actual == expected
    check('Fresh public metadata differs: ' + key, actual == expected)
_, doi_get = public_get('https://doi.org/' + DOI, 2_000_000)
check('Fresh DOI does not resolve correctly', doi_get['http_status'] == 200 and
      doi_get['resolved_url'].rstrip('/') == f'https://zenodo.org/records/{RECORD}')

params = {'spreadsheetId': SHEET, 'range': ROW, 'majorDimension': 'ROWS', 'valueRenderOption': 'UNFORMATTED_VALUE'}
cmd = ['gws', 'sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps(params)]
run = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=25)
fresh_row = json.loads(run.stdout)
save('tracker_exact_row_live.json', fresh_row)
request = read('receipts/tracker_append_request.json')
response = read('receipts/tracker_append_response.json')
readback = read('receipts/tracker_readback.json')
verification = read('receipts/tracker_verification.json')
execution = read('receipts/tracker_append_execution.json')
preappend = read('receipts/tracker_preappend_scan.json')
resolution = read('receipts/tracker_metadata_resolution.json')
tracker_checks = {
    'exact_live_readback': fresh_row == readback,
    'exact_requested_values': fresh_row['values'] == request['body']['values'] == response['updates']['updatedData']['values'] == verification['values'],
    'exact_range': fresh_row['range'] == ROW == response['updates']['updatedRange'] == verification['updated_range'],
    'sheet_id_title_resolved': resolution['target_sheet']['sheetId'] == 1254632077 and resolution['target_sheet']['title'] == 'Math Puzzles',
    'schema_consistent': request['schema'] == verification['headers'] == preappend['headers'] == ['Original Problem','Solution Chat URL','DOI','Notes'],
    'raw_insert_rows': request['params']['valueInputOption'] == execution['valueInputOption'] == verification['valueInputOption'] == 'RAW' and request['params']['insertDataOption'] == execution['insertDataOption'] == verification['insertDataOption'] == 'INSERT_ROWS',
    'one_row_four_cells_response': response['updates']['updatedRows'] == 1 and response['updates']['updatedCells'] == 4 and response['updates']['updatedColumns'] == 4,
    'one_append_recorded': execution['append_attempts_by_this_project'] == verification['append_attempts'] == 1,
    'no_prior_duplicate_recorded': all(not rows for rows in preappend['exact_duplicate_rows'].values()),
    'only_row_53_duplicate_scan_recorded': verification['duplicate_doi_rows_after_append'] == [53],
    'publication_preceded_tracker': read('receipts/zenodo_inspect_published_v5.json')['verified_utc'] < resolution['utc'] < execution['completed_utc'],
    'doi_in_schema_column_C': fresh_row['values'][0][2] == 'https://doi.org/' + DOI,
}
for label, condition in tracker_checks.items():
    check('Tracker check failed: ' + label, condition)

summary = {'started_utc': UTC, 'completed_utc': datetime.now(timezone.utc).isoformat(),
           'verdict': 'PASS' if not failures else 'DISCREPANCY', 'failures': failures,
           'current_sealed_files': current, 'current_authored_payload': authored,
           'zip_member_count': len(archive_members), 'zip_member_hashes': archive_members,
           'saved_tool_sequence': sequence, 'saved_metadata_checks': metadata_checks,
           'fresh_public_record_get': record_get, 'fresh_public_metadata_checks': public_metadata_checks,
           'fresh_public_downloads': public_files, 'fresh_doi_get': doi_get,
           'tracker_checks': tracker_checks, 'tracker_live_read_params': params,
           'input_hashes': {rel: h((ROOT / rel).read_bytes()) for rel in [
               'research/USER_REQUEST.txt','publication/CANDIDATE_IDENTITY.json',
               'reviews/package_review_05/V5_CUSTODY_SEAL.json','reviews/package_review_05/DELIVERY_RECEIPT.json',
               'reviews/PACKAGE_REVIEW_05.md','receipts/ROOT_RELEASE_APPROVAL_V5.json',
               'receipts/PREPUBLISH_VERIFICATION_V5.json','receipts/tracker_preappend_scan.json',
               'receipts/tracker_verification.json','receipts/tracker_append_execution.json']},
           'limitations': [
               'Bounded publication/receipt audit only; no fresh mathematical or literature audit.',
               'Tool sequence and single-append history are checked against saved nonsecret receipts and the repository tool guards, not an independent immutable process transcript.',
               'No-duplicate conclusion relies on saved pre/post scans; this auditor reads only A53:D53 live and never reads other tracker rows.',
               'Web preview could not open the exact Zenodo or DOI endpoints; fresh urllib GETs independently succeeded without credentials.',
               'Missing gws-shared skill was not generated, as the original user request forbids skill generation in the research checkout; installed read skill and current schema were read.',
               'No secrets, frozen publication files, sheet mutations, Git changes, upstream mutations, or contacts to individuals were performed.']}
save('AUDIT_RESULT.json', summary)
print(json.dumps({'verdict': summary['verdict'], 'failures': failures, 'public_record': record_get,
                  'public_downloads': public_files, 'doi': doi_get, 'tracker_checks': tracker_checks}, indent=2))
