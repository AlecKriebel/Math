#!/usr/bin/env python3
"""Remove only the verified superseded ZIP from the same unpublished draft.

The normal repository kit subsequently uploads the accepted replacement.
Default is a read-only preflight. No automatic repeat of a DELETE is allowed.
API contract: https://developers.zenodo.org/#delete-a-deposition-file
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

PROGRAM = Path(__file__).resolve().parent
REPOSITORY = PROGRAM.parent
AUDIT = PROGRAM / 'audits/pr468_30000689'
MANIFEST = AUDIT / 'package/deposit.json'
DRAFT_ID = 23310484
ZIP_NAME = 'missing_faces_verification_v1.zip'
PDF_NAME = 'missing_faces_and_sphere_skeleta.pdf'
ORIGINAL = '8527ccdba064bca52035fc6c8d96caa750ac9c00'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dump(name, value):
    (AUDIT / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    freeze = json.loads((AUDIT / 'PACKAGE_REVIEW_INPUT_4.json').read_text())
    for name, entry in freeze['files'].items():
        data = (AUDIT / 'package' / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == entry['sha256'] and len(data) == entry['bytes'],
                'Frozen round4 packet changed')
    if args.apply:
        gate = json.loads((AUDIT / 'FINAL_ACCEPTANCE_GATE.json').read_text())
        require(gate['verdict'] == 'ACCEPTED_FOR_PREPRINT_PUBLICATION'
                and gate['review_input_manifest'] == 'PACKAGE_REVIEW_INPUT_4.json',
                'Final round4 acceptance absent')
        require(len(gate['complete_package_reviews']) >= 2, 'Successive fresh reviews absent')
        for report in gate['complete_package_reviews']:
            require(report['verdict'] == 'PASS'
                    and type(report.get('blocking_issue_count')) is int
                    and report['blocking_issue_count'] == 0
                    and type(report.get('required_correction_count')) is int
                    and report['required_correction_count'] == 0,
                    'Accepted review has a remaining issue')
            path = (AUDIT / report['path']).resolve()
            require(path.is_relative_to(AUDIT)
                    and hashlib.sha256(path.read_bytes()).hexdigest() == report['sha256'],
                    'Accepted review changed')
        pr = json.loads(subprocess.check_output([
            'gh', 'pr', 'view', '468', '--repo', 'AlecKriebel/Math',
            '--json', 'state,isDraft,headRefOid']))
        require(pr == {'state': 'OPEN', 'isDraft': True, 'headRefOid': ORIGINAL},
                'Original eligible draft changed')
        queue = subprocess.check_output([
            'gh', 'api', 'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref=' + ORIGINAL,
            '-H', 'Accept: application/vnd.github.raw+json']).decode()
        header = next(line for line in queue.splitlines()
                      if line.startswith('|') and 'ID / code' in line and 'Status' in line)
        columns = [x.strip() for x in header.split('|')[1:-1]]
        rows = [line.split('|')[1:-1] for line in queue.splitlines()
                if line.startswith('|') and line.split('|')[2].strip().startswith('30000689 /')]
        require(len(rows) == 1 and rows[0][columns.index('Status')].strip() == 'claimed_solved',
                'Selected status is excluded')

    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('existing_zenodo_kit', REPOSITORY / 'zenodo_deposit_tool/zenodo.py')
    kit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kit)
    metadata, files = kit.load_manifest(MANIFEST.resolve())
    _, state = kit.local_state(MANIFEST.resolve(), 'production')
    require(state is not None and state['id'] == DRAFT_ID, 'Same saved production draft absent')
    client = kit.ZenodoClient('production', kit.token_for('production'))
    deposit = client.get(DRAFT_ID)
    kit.validate_record(deposit, DRAFT_ID)
    require(deposit['submitted'] is False, 'Published files must never be deleted')
    require(all(deposit['metadata'].get(k) == v for k, v in metadata.items()),
            'Draft metadata differs from exact canonical values')
    remote = kit.server_files(deposit)
    wanted = {item['name']: item for item in files}
    require(set(wanted) == {PDF_NAME, ZIP_NAME}, 'Unexpected accepted filenames')
    require(set(remote).issubset(set(wanted)) and PDF_NAME in remote,
            'Unexpected remote file set')
    require(kit.matching_file(remote[PDF_NAME], wanted[PDF_NAME]), 'Reviewed PDF differs remotely')
    entry = remote.get(ZIP_NAME)
    operation_path = AUDIT / 'ZENODO_ARCHIVE_REPLACE_OPERATION.json'
    prior = json.loads(operation_path.read_text()) if operation_path.exists() else None
    if entry and kit.matching_file(entry, wanted[ZIP_NAME]):
        kit.verify(deposit, metadata, files)
        summary = {'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'id': DRAFT_ID, 'state': 'accepted_archive_already_present', 'write_performed': False}
        dump('ZENODO_ARCHIVE_REPLACE_RECEIPT.json', summary)
        print(json.dumps(summary, indent=2))
        return
    old = json.loads((AUDIT / 'ZENODO_DRAFT_METADATA_RECONCILIATION.json').read_text())
    old_files = {item['name']: item for item in old['remote_files']}
    require(old['id'] == DRAFT_ID and old['submitted'] is False, 'Original draft receipt invalid')
    backup = AUDIT / 'references/private_sources/round3_accepted/missing_faces_verification_v1.zip'
    old_md5 = hashlib.md5(backup.read_bytes()).hexdigest()
    old_sha = hashlib.sha256(backup.read_bytes()).hexdigest()
    old_freeze = json.loads((AUDIT / 'PACKAGE_REVIEW_INPUT_3.json').read_text())
    require(old_sha == old_freeze['files'][ZIP_NAME]['sha256']
            and old_md5 == old_files[ZIP_NAME]['checksum'], 'Old ZIP backup differs from draft receipt')
    if entry:
        require(int(entry['filesize']) == backup.stat().st_size and entry['checksum'].removeprefix('md5:') == old_md5,
                'Remote ZIP is not the known superseded archive')
        file_id = entry['id']
        require(isinstance(file_id, str) and re.fullmatch(r'[A-Za-z0-9-]+', file_id), 'Unsafe remote file ID')
    else:
        require(prior is not None and prior['id'] == DRAFT_ID
                and prior['state'] == 'delete_attempted_once' and prior['old_archive_sha256'] == old_sha,
                'Archive missing without a recorded replacement operation')
        file_id = prior['file_id']
    summary = {'prepared_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'environment': 'production', 'id': DRAFT_ID, 'submitted': False,
               'filename': ZIP_NAME, 'file_id': file_id, 'old_archive_sha256': old_sha,
               'accepted_archive_sha256': wanted[ZIP_NAME]['sha256'],
               'pdf_preserved': True, 'metadata_exact': True,
               'contract': 'https://developers.zenodo.org/#delete-a-deposition-file',
               'state': 'read_only_preflight', 'write_performed': False}
    dump('ZENODO_ARCHIVE_REPLACE_PREFLIGHT.json', summary)
    if not args.apply:
        print(json.dumps(summary, indent=2))
        return
    if entry:
        require(prior is None, 'Prior DELETE exists; reconcile read-only rather than repeat it')
        summary.update(state='delete_attempted_once', write_performed=True)
        dump('ZENODO_ARCHIVE_REPLACE_OPERATION.json', summary)
        try:
            client.request('DELETE', client.base + f'/api/deposit/depositions/{DRAFT_ID}/files/{file_id}')
        except kit.DepositError as exc:
            # A successful DELETE has documented empty HTTP204 content, which
            # the unchanged kit's generic JSON reader rejects. Any lost/error
            # response is resolved by one GET, never another DELETE.
            summary['delete_response_note'] = str(exc)
    refreshed = client.get(DRAFT_ID)
    kit.validate_record(refreshed, DRAFT_ID)
    remaining = kit.server_files(refreshed)
    require(refreshed['submitted'] is False and set(remaining) == {PDF_NAME}
            and kit.matching_file(remaining[PDF_NAME], wanted[PDF_NAME])
            and all(refreshed['metadata'].get(k) == v for k, v in metadata.items()),
            'Replacement removal outcome unconfirmed; no automatic retry')
    summary.update(state='superseded_zip_absent_verified',
                   verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   next_action='Resume stage on same stable manifest with existing repository kit')
    dump('ZENODO_ARCHIVE_REPLACE_RECEIPT.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
