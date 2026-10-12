#!/usr/bin/env python3
"""Register PR464 through the native Google Workspace CLI, at most once.

Without --apply, only preflight reads and local receipts occur. Uncertain
appends are reconciled by readback; this runner never automatically retries.
"""
import argparse
import json
import re
import subprocess
from common import (AUDIT, SHEET, TAB, TAB_ID, check_sheet, doi_matches, dump,
                    confirm_live_publication, gws, live_eligibility, now, read_json, require, sheet_get,
                    tracker_values, validate_gate, validate_publication, validate_tracker)


def exact_registration(doi, expected):
    rows = sheet_get("'Math Puzzles'!A:D").get('values', [])
    matching = doi_matches(doi, rows)
    require(len(matching) == 1 and rows[matching[0] - 1] == expected[0],
            'Tracker DOI registration is not unique and exact; reconcile read-only')
    target = f"'Math Puzzles'!A{matching[0]}:D{matching[0]}"
    require(sheet_get(target).get('values', []) == expected,
            'Exact tracker range changed; reconcile without another append')
    return target


def prior_registration(context, pub, values, matching):
    """A surviving write record prohibits another append even after row loss."""
    prior_path = AUDIT / 'TRACKER_APPEND_OPERATION.json'
    receipt_path = AUDIT / 'TRACKER_APPEND_RECEIPT.json'
    prior = read_json(AUDIT, prior_path.name) if prior_path.exists() else None
    receipt = read_json(AUDIT, receipt_path.name) if receipt_path.exists() else None
    if prior:
        require(prior.get('doi') == pub['doi_url'] and prior.get('values') == values,
                'Prior registration operation belongs to different intended bytes')
        require(prior.get('state') in {'read_only_preflight', 'append_attempted_once',
                                      'outcome_unconfirmed', 'verified_registration'},
                'Unknown prior registration state; read-only reconciliation required')
    if receipt:
        require(receipt.get('verified') is True and receipt.get('doi') == pub['doi_url']
                and receipt.get('values') == values, 'Prior tracker receipt belongs to different or invalid intended bytes')
        validate_tracker(context, pub)
    attempted = prior is not None and prior['state'] != 'read_only_preflight'
    require(not ((attempted or receipt is not None) and not matching),
            'Prior append or verified registration is unconfirmed or its row was removed; read-only reconciliation required')
    return prior, receipt


def run(apply=False):
    context = validate_gate()
    pub = confirm_live_publication(context)
    live_eligibility()
    check_sheet()
    doi = pub['doi_url']
    values = tracker_values(context['metadata'], doi)
    existing = sheet_get("'Math Puzzles'!A:D").get('values', [])
    matching = doi_matches(doi, existing)
    require(len(matching) <= 1, 'Duplicate DOI rows already exist; do not append')
    prior, prior_receipt = prior_registration(context, pub, values, matching)
    if matching:
        exact_registration(doi, values)
    operation = {'prepared_at_utc': now(), 'spreadsheet_id': SHEET, 'sheet_id': TAB_ID,
                 'tab': TAB, 'doi': doi, 'values': values, 'matching_existing_rows': matching,
                 'state': 'read_only_preflight'}
    # Preserve an earlier uncertain write receipt until it is positively
    # reconciled; a new read-only run must not erase the no-retry guard.
    if prior_receipt is None and (not prior or prior.get('state') == 'read_only_preflight'):
        dump('TRACKER_APPEND_OPERATION.json', operation)
    if not apply:
        return {'state': 'read_only_preflight', 'matching_existing_rows': matching}
    response = None
    if matching:
        state = 'existing_identical_registration'
    else:
        # Recheck immediately before the write. This is a snapshot, not an
        # atomic multi-runner claim. A final full read detects later duplicates.
        live_eligibility()
        check_sheet()
        require(not doi_matches(doi, sheet_get("'Math Puzzles'!A:D").get('values', [])),
                'DOI appeared during preflight; restart with read-only reconciliation')
        validate_gate()
        confirm_live_publication(context)
        # Re-read durable guards immediately before writing; the earlier
        # preflight may have overlapped another runner's registration.
        prior_registration(context, pub, values, [])
        operation['state'] = 'append_attempted_once'
        dump('TRACKER_APPEND_OPERATION.json', operation)
        try:
            response = gws('append', {'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:D",
                                     'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                                     'includeValuesInResponse': True},
                           {'majorDimension': 'ROWS', 'values': values})
        except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError):
            operation['state'] = 'outcome_unconfirmed'
            dump('TRACKER_APPEND_OPERATION.json', operation)
            exact_registration(doi, values)
            state = 'recovered_append_readback'
        else:
            updates = response.get('updates', {})
            require(type(updates.get('updatedRows')) is int and updates['updatedRows'] == 1
                    and type(updates.get('updatedColumns')) is int and updates['updatedColumns'] == 4
                    and type(updates.get('updatedCells')) is int and updates['updatedCells'] == 4,
                    'Unexpected append size; inspect without repeating')
            target = updates.get('updatedRange')
            require(type(target) is str and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1", target),
                    'Unexpected append range; inspect without repeating')
            require(sheet_get(target).get('values', []) == values, 'Returned appended range differs from intended row')
            state = 'appended_once'
    target = exact_registration(doi, values)
    receipt = {'verified_at_utc': now(), 'verified': True, 'state': state, 'spreadsheet_id': SHEET,
               'sheet_id': TAB_ID, 'tab': TAB, 'updated_range': target, 'values': values,
               'append_response': response, 'doi': doi, 'unique_doi_row_at_final_snapshot': True,
               'unrelated_rows_saved': False,
               'concurrency_scope': 'One append by this runner and exact final unique snapshot; no atomic multi-runner guarantee.'}
    dump('TRACKER_APPEND_RECEIPT.json', receipt)
    operation.update(state='verified_registration', updated_range=target, verified_at_utc=now())
    dump('TRACKER_APPEND_OPERATION.json', operation)
    return {'state': state, 'verified': True, 'updated_range': target, 'doi': doi}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    print(json.dumps(run(parser.parse_args().apply), indent=2))


if __name__ == '__main__':
    main()
