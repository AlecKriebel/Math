#!/usr/bin/env python3
"""Prepare or append PR662's verified DOI; only --apply can send a write.

An append intent is durably recorded before dispatch. Ambiguous responses or
readback failures leave a sticky marker, so absence of the DOI never silently
authorizes a retry. A matching existing row can be reconciled by read-only checks.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import types

sys.dont_write_bytecode = True
# Capture the one local dependency as source, never through a bytecode cache.
# -B suppresses new pyc writes but would not prevent reading a stale existing pyc.
_dependency_path = Path(__file__).absolute().with_name('prepare_integration.py')
if any(parent.is_symlink() for parent in _dependency_path.parents):
    raise ValueError('linked integration-helper parent')
_dependency_fd = os.open(_dependency_path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
with os.fdopen(_dependency_fd, 'rb') as _dependency_stream:
    if not stat.S_ISREG(os.fstat(_dependency_stream.fileno()).st_mode):
        raise ValueError('integration helper must be a regular source file')
    _dependency_source = _dependency_stream.read()
INTEGRATION_HELPER_SHA256 = hashlib.sha256(_dependency_source).hexdigest()
_dependency = types.ModuleType('_pr662_tracker_captured_integration')
_dependency.__file__ = str(_dependency_path)
exec(compile(_dependency_source, str(_dependency_path), 'exec'), _dependency.__dict__)
for _name in ('A', 'TITLE', 'action_lock', 'parse_json', 'publication_inputs',
              'regular_bytes', 'require', 'sha', 'utc', 'valid_doi', 'write_json'):
    globals()[_name] = getattr(_dependency, _name)

ID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
TAB = 'Math Puzzles'
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
PENDING = A / 'TRACKER_UNCONFIRMED.json'


def call(resource, method, params, body=None):
    command = ['gws', 'sheets', *resource.split('.'), method, '--params', json.dumps(params)]
    if body is not None:
        command += ['--json', json.dumps(body, ensure_ascii=False)]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return parse_json(result.stdout)


def wanted_row(doi):
    valid_doi(doi)
    return ['https://arxiv.org/abs/1809.07200v2', '', 'https://doi.org/' + doi,
        TITLE + '. Hayman-Lingham Problem 6.86, printed p. 147; catalogue 2306086 / AMR-022-6086. '
        'Accepted qualitative fixed-nonreal-point improvement uniform over the normalized real-coefficient schlicht class; '
        'uniform gap on compact nonreal sets, sharp classical real-diameter radius, zero source expression at zero. '
        'Classical coefficient equality, slit rigidity and compactness. Explicit upper gap, sharp quantitative radius '
        'and general extremizers undetermined. Bounded priority audit retains Jenkins (1960) and Aleksandrov-Popova (1973) '
        'original-source limits; no historical firstness, exhaustive novelty clearance or current-openness guarantee. '
        'Extensively AI-assisted; unrefereed, without independent human peer review. '
        'PR #662: https://github.com/AlecKriebel/Math/pull/662']


def doi_matches(values, doi):
    valid_doi(doi)
    pattern = re.compile(r'(?:(?:https?://(?:dx\.)?doi\.org/)|doi:\s*)?' + re.escape(doi) + r'/?', re.I)
    return [i + 1 for i, row in enumerate(values) if type(row) is list and len(row) > 2
            and type(row[2]) is str and pattern.fullmatch(row[2].strip())]


def inspect():
    info = call('spreadsheets', 'get', {'spreadsheetId': ID, 'fields': 'sheets(properties(sheetId,title))'})
    require(type(info) is dict and type(info.get('sheets')) is list, 'tracker metadata malformed')
    matches = [sheet.get('properties') for sheet in info['sheets']
               if type(sheet) is dict and type(sheet.get('properties')) is dict and sheet['properties'].get('sheetId') == GID]
    require(matches == [{'sheetId': GID, 'title': TAB}], 'tracker gid/title does not identify intended tab')
    headers = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': "'" + TAB + "'!A1:D1"}).get('values', [])
    require(headers == [HEADERS], 'tracker A:D headers differ')
    values = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': "'" + TAB + "'!A:D"}).get('values', [])
    require(type(values) is list and all(type(row) is list and len(row) <= 4 for row in values), 'tracker rows malformed')
    require(values and values[0] == HEADERS, 'global tracker scan header differs')
    return values


def exact_existing(values, row, doi):
    matches = doi_matches(values, doi)
    require(len(matches) <= 1, 'duplicate DOI already present; reconcile without another append')
    if matches:
        require((values[matches[0] - 1] + [''] * 4)[:4] == row,
                'existing DOI row differs; no duplicate append or silent overwrite')
    return matches


def pending_record(ready):
    if not PENDING.exists() and not PENDING.is_symlink():
        return None
    old = parse_json(regular_bytes(PENDING))
    require(old.get('schema') == 'pr662-tracker-intent-v1' and old.get('spreadsheet_id') == ID
            and old.get('sheet_id') == GID and old.get('doi') == ready['doi'] and old.get('row') == ready['row']
            and old.get('publication_validation') == ready['publication_validation'],
            'prior tracker intent does not bind the exact current accepted publication; reconcile manually')
    return old


def readback_existing(ready, matches):
    require(len(matches) == 1, 'one exact existing row is required')
    target = f"'{TAB}'!A{matches[0]}:D{matches[0]}"
    actual = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': target}).get('values', [])
    require(actual == [ready['row']], 'existing target row readback mismatch')
    current = exact_existing(inspect(), ready['row'], ready['doi'])
    require(current == matches, 'existing row/global DOI uniqueness changed')
    old = pending_record(ready)
    if old is not None:
        write_json(PENDING, old | {'action_outcome': 'confirmed', 'confirmed_utc': utc(), 'updated_range': target})
    return ready | {'applied': True, 'already_present': True, 'updated_range': target,
                    'read_back': actual, 'global_exact_doi_rows': current}


def append_once(ready):
    """Caller holds the local operation lock; remote uniqueness is also read back."""
    row, doi = ready['row'], ready['doi']
    matches = exact_existing(inspect(), row, doi)
    if matches:
        return readback_existing(ready, matches)
    old = pending_record(ready)
    require(old is None, 'a prior append was dispatched and DOI is absent; reconcile, never blindly retry')
    pending = {'schema': 'pr662-tracker-intent-v1', 'spreadsheet_id': ID, 'sheet_id': GID,
        'doi': doi, 'row': row, 'publication_validation': ready['publication_validation'],
        'dispatch_utc': utc(), 'action_outcome': 'unconfirmed; read sheet before any retry'}
    write_json(PENDING, pending)
    response = call('spreadsheets.values', 'append', {
        'spreadsheetId': ID, 'range': "'" + TAB + "'!A:D", 'valueInputOption': 'RAW',
        'insertDataOption': 'INSERT_ROWS', 'includeValuesInResponse': True},
        {'majorDimension': 'ROWS', 'values': [row]})
    require(response.get('spreadsheetId') == ID, 'append response identifies a different spreadsheet')
    updates = response.get('updates', {})
    target = updates.get('updatedRange', '')
    matched = re.fullmatch(r"(?:'Math Puzzles'|Math Puzzles)!A([1-9][0-9]*):D\1", target)
    require(matched is not None and int(matched.group(1)) > 1, 'append returned unexpected target range')
    require(all(type(updates.get(key)) is int and updates[key] == value for key, value in
                (('updatedRows', 1), ('updatedColumns', 4), ('updatedCells', 4))), 'append is not exactly one A:D row')
    require(updates.get('updatedData', {}).get('values') == [row], 'append response values differ from RAW row')
    actual = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': target}).get('values', [])
    require(actual == [row], 'post-write exact target row readback mismatch')
    matches = exact_existing(inspect(), row, doi)
    require(matches == [int(matched.group(1))], 'post-write global DOI uniqueness/range failed')
    receipt = ready | {'applied': True, 'already_present': False, 'updated_range': target,
                       'append_response': response, 'read_back': actual, 'global_exact_doi_rows': matches}
    write_json(PENDING, pending | {'action_outcome': 'confirmed', 'confirmed_utc': utc(), 'updated_range': target})
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--doi', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args(); valid_doi(args.doi)
    with action_lock('TRACKER_OPERATION.lock'):
        inputs = publication_inputs(A / 'publication', args.doi, A / 'ZENODO_PUBLICATION_RECEIPT.json',
                                    A / 'ZENODO_POST_PUBLICATION_INSPECTION.json')
        row = wanted_row(args.doi)
        matches = exact_existing(inspect(), row, args.doi)
        ready = {'schema': 'pr662-tracker-row-receipt-v1', 'prepared_utc': utc(),
            'spreadsheet_id': ID, 'sheet_id': GID, 'sheet_title': TAB, 'doi': args.doi,
            'row': row, 'existing_rows': matches, 'publication_validation': inputs['validation'],
            'helper_sha256': sha(regular_bytes(Path(__file__).absolute())),
            'integration_helper_sha256': INTEGRATION_HELPER_SHA256, 'applied': False}
        write_json(A / 'TRACKER_ROW_READY.json', ready)
        if matches:
            receipt = readback_existing(ready, matches)
        elif args.apply:
            receipt = append_once(ready)
        else:
            print(json.dumps(ready, indent=2, ensure_ascii=False)); return
        receipt['confirmed_utc'] = utc()
        write_json(A / 'TRACKER_RECEIPT.json', receipt)
        print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
