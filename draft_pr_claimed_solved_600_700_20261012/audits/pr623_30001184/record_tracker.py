#!/usr/bin/env python3
"""Prepare or append the confirmed PR623 DOI with duplicate/read-back guards.

No write occurs without --apply. An uncertain append is marked before dispatch
and is never blindly retried; a later read can confirm the exact existing row.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from prepare_integration import (A, TITLE, json_bytes, parse_json, publication_inputs,
                                 regular_bytes, require, utc, valid_doi, write_json)

ID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
TAB = 'Math Puzzles'
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
PENDING = A / 'TRACKER_UNCONFIRMED.json'


def call(resource, method, params, body=None):
    cmd = ['gws', 'sheets', *resource.split('.'), method, '--params', json.dumps(params)]
    if body is not None:
        cmd += ['--json', json.dumps(body, ensure_ascii=False)]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return parse_json(proc.stdout)


def wanted_row(doi):
    valid_doi(doi)
    return ['https://doi.org/10.4171/OWR/2009/09', '', 'https://doi.org/' + doi,
            TITLE + '. Skeide\'s first module-approach problem, OWR 2009 pp. 542–543; catalogue ID 30001184 / OWR-3392-012. '
            'Accepted negative counterexample to generation-only universal GNS descent for general unital C*-E0 dilations. '
            'Explicit corollary of Burgarth-Facchi-Hillier\'s established clock/evaluation/translated-unitary mechanism; conditional extension after kernel invariance, '
            'stronger minimality and normal W*-promotion remain unresolved here. Extensively AI-assisted; unrefereed, no independent human peer review '
            'or exhaustive first-priority claim. PR #623: https://github.com/AlecKriebel/Math/pull/623']


def doi_matches(values, doi):
    exact = {doi, 'https://doi.org/' + doi}
    return [i + 1 for i, row in enumerate(values)
            if type(row) is list and len(row) > 2 and type(row[2]) is str
            and row[2].strip().rstrip('/') in exact]


def inspect():
    info = call('spreadsheets', 'get', {'spreadsheetId': ID, 'fields': 'sheets(properties(sheetId,title))'})
    matches = [s['properties'] for s in info.get('sheets', []) if s.get('properties', {}).get('sheetId') == GID]
    require(matches == [{'sheetId': GID, 'title': TAB}], 'tracker gid/title does not identify the intended sheet')
    headers = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': "'" + TAB + "'!A1:D1"}).get('values', [])
    require(headers == [HEADERS], 'tracker A:D headers differ')
    values = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': "'" + TAB + "'!A:D"}).get('values', [])
    require(type(values) is list, 'tracker values are not a row list')
    return values


def exact_existing(values, row, doi):
    matches = doi_matches(values, doi)
    require(len(matches) <= 1, 'duplicate exact DOI already present; reconcile without another append')
    if matches:
        actual = (values[matches[0] - 1] + [''] * 4)[:4]
        require(actual == row, 'existing exact DOI row differs; no duplicate append or silent overwrite')
    return matches


def append_once(doi, row, ready):
    # Refresh the exact DOI/header guard immediately before any possible POST.
    values = inspect()
    matches = exact_existing(values, row, doi)
    if matches:
        return ready | {'applied': True, 'already_present': True,
                        'updated_range': f"'{TAB}'!A{matches[0]}:D{matches[0]}"}
    if PENDING.exists():
        old = parse_json(regular_bytes(PENDING))
        require(old.get('action_outcome') == 'confirmed',
                'earlier append outcome is unconfirmed and exact DOI is absent; inspect/reconcile before retry')
    # Record before dispatch, including process termination and malformed reply.
    pending = ready | {'action_outcome': 'unconfirmed; read sheet before any retry', 'dispatch_utc': utc()}
    write_json(PENDING, pending)
    response = call('spreadsheets.values', 'append', {
        'spreadsheetId': ID, 'range': "'" + TAB + "'!A:D", 'valueInputOption': 'RAW',
        'insertDataOption': 'INSERT_ROWS', 'includeValuesInResponse': True},
        {'majorDimension': 'ROWS', 'values': [row]})
    updates = response.get('updates', {})
    target = updates.get('updatedRange', '')
    match = re.fullmatch(r"(?:'Math Puzzles'|Math Puzzles)!A([1-9][0-9]*):D\1", target)
    require(match is not None and int(match.group(1)) > 1, 'append returned an unexpected target range')
    require(updates.get('updatedRows') == 1 and updates.get('updatedColumns') == 4
            and updates.get('updatedCells') == 4, 'append response is not exactly one A:D row')
    actual = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': target}).get('values', [])
    require(actual == [row], 'post-write exact target row read-back mismatch')
    all_values = call('spreadsheets.values', 'get', {'spreadsheetId': ID, 'range': "'" + TAB + "'!A:D"}).get('values', [])
    matches = exact_existing(all_values, row, doi)
    require(matches == [int(match.group(1))], 'post-write global DOI uniqueness/range check failed')
    receipt = ready | {'applied': True, 'already_present': False, 'updated_range': target,
                       'append_response': response, 'read_back': actual,
                       'global_exact_doi_rows': matches}
    # Any exception above leaves the durable unconfirmed marker in place.
    write_json(PENDING, pending | {'action_outcome': 'confirmed', 'confirmed_utc': utc(),
                                 'updated_range': target})
    return receipt


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--doi', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    valid_doi(args.doi)
    _, _, validation = publication_inputs(A / 'publication', args.doi,
        A / 'ZENODO_PUBLICATION_RECEIPT.json', A / 'ZENODO_POST_PUBLICATION_INSPECTION.json')
    row = wanted_row(args.doi)
    values = inspect()
    matches = exact_existing(values, row, args.doi)
    ready = {'schema': 'pr623-tracker-row-receipt-v1', 'prepared_utc': utc(),
             'spreadsheet_id': ID, 'sheet_id': GID, 'sheet_title': TAB, 'doi': args.doi,
             'row': row, 'existing_rows': matches, 'publication_validation': validation, 'applied': False}
    write_json(A / 'TRACKER_ROW_READY.json', ready)
    if matches:
        receipt = ready | {'applied': True, 'already_present': True,
                           'updated_range': f"'{TAB}'!A{matches[0]}:D{matches[0]}"}
    elif args.apply:
        receipt = append_once(args.doi, row, ready)
    else:
        print(json.dumps(ready, indent=2, ensure_ascii=False))
        return
    receipt['confirmed_utc'] = utc()
    write_json(A / 'TRACKER_RECEIPT.json', receipt)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
