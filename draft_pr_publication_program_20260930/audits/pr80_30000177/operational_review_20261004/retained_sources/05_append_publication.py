#!/usr/bin/env python3
"""Prepare or append one verified publication to the exact Math Puzzles tab.

Defaults to a local append dry run after authenticated reads. Only --execute can
dispatch one append. Root must serialize use; the Sheets API has no atomic
read/duplicate-check/append transaction or append idempotency key.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit
import uuid

SPREADSHEET_ID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
SHEET_ID = 1254632077
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']


class TrackerError(Exception):
    """A controlled failure; an attempted append must be reconciled before retry."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sync_directory(path: Path) -> None:
    directory = os.open(path, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def durable_mkdir(path: Path) -> None:
    """Sync each newly created directory's entry before retaining receipts."""
    if path.exists():
        if not path.is_dir():
            raise TrackerError('Receipt destination is not a directory')
        return
    durable_mkdir(path.parent)
    try:
        path.mkdir()
    except FileExistsError:
        if not path.is_dir():
            raise TrackerError('Receipt destination is not a directory')
    sync_directory(path.parent)
    sync_directory(path)


def save(path: Path, value) -> None:
    """Exclusive, durable evidence; never overwrite a prior receipt."""
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(path.parent)


def normalize_problem(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TrackerError('Original Problem must be a nonempty string')
    value = value.strip()
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
            raise TrackerError('Original Problem URL must use HTTP(S) without credentials')
        host = parsed.hostname.casefold()
        if host in ('unsolvedmath.com', 'www.unsolvedmath.com'):
            try:
                port = parsed.port
            except ValueError as exc:
                raise TrackerError('Invalid UnsolvedMath URL port') from exc
            if port not in (None, 80, 443):
                raise TrackerError('Unsupported UnsolvedMath URL port')
            match = re.fullmatch(r'/problems/([0-9]+|[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+)/?', unquote(parsed.path))
            if not match:
                raise TrackerError('UnsolvedMath URL must identify one /problems/<ID>')
            return 'unsolvedmath:' + match.group(1).upper()
        # Generic URLs preserve path case, query, and fragment identity because
        # client-side routes can identify distinct problems in a fragment.
        try:
            port = parsed.port
        except ValueError as exc:
            raise TrackerError('Invalid Original Problem URL port') from exc
        netloc = host + ((':' + str(port)) if port and not (
            parsed.scheme.lower() == 'https' and port == 443 or parsed.scheme.lower() == 'http' and port == 80
        ) else '')
        return 'url:' + urlunsplit((parsed.scheme.lower(), netloc, parsed.path or '/', parsed.query, parsed.fragment))
    if re.fullmatch(r'[0-9]+|(?:OWR|AMR)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+', value, re.IGNORECASE):
        return 'unsolvedmath:' + value.upper()
    return 'label:' + ' '.join(value.casefold().split())


def normalize_doi(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TrackerError('DOI must be a nonempty string')
    value = value.strip()
    if value.lower().startswith('doi:'):
        value = value[4:].strip()
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        if (parsed.scheme.lower() not in ('http', 'https') or (parsed.hostname or '').casefold() not in
                ('doi.org', 'www.doi.org', 'dx.doi.org') or parsed.username or parsed.password):
            raise TrackerError('DOI URL must use a recognized DOI resolver without credentials')
        try:
            port = parsed.port
        except ValueError as exc:
            raise TrackerError('Invalid DOI URL port') from exc
        if port not in (None, 80, 443):
            raise TrackerError('Unsupported DOI URL port')
        value = unquote(parsed.path.lstrip('/'))
    if not re.fullmatch(r'10\.[0-9]{4,9}/[^\s?#]+', value):
        raise TrackerError('DOI must be a complete bare DOI, doi:<DOI>, or DOI resolver URL')
    return value.casefold()


def quoted_tab(title: str) -> str:
    return "'" + title.replace("'", "''") + "'"


def a1_range(target_range: str, title: str) -> tuple[int, int]:
    """Decode quoted/unquoted canonical A1 titles and require exact A:D columns."""
    if not isinstance(target_range, str):
        raise TrackerError('Tracker range must be a string')
    match = re.fullmatch(r"(?:'((?:[^']|'')*)'|([^'!]+))!A([1-9][0-9]*):D([1-9][0-9]*)", target_range)
    if not match:
        raise TrackerError('Tracker range does not identify exact A:D columns')
    actual_title = match.group(1).replace("''", "'") if match.group(1) is not None else match.group(2)
    row, end_row = int(match.group(3)), int(match.group(4))
    if actual_title != title or end_row < row:
        raise TrackerError('Tracker range does not identify the exact target tab')
    return row, end_row


def range_row(target_range: str, title: str) -> int:
    """Require one body row while accepting canonical quoted/unquoted titles."""
    row, end_row = a1_range(target_range, title)
    if row != end_row or row < 2:
        raise TrackerError('Tracker range is not one body row in the exact target A:D range')
    return row


def padded_row(row) -> list[str]:
    if not isinstance(row, list) or len(row) > 4 or any(not isinstance(cell, str) for cell in row):
        raise TrackerError('Expected at most four string values in A:D')
    return row + [''] * (4 - len(row))


def run_gws(gws: str, parts: list[str], params: dict, attempt: Path, name: str,
            body: dict | None = None, dry_run: bool = False) -> dict:
    argv = [gws, 'sheets', *parts, '--params', json.dumps(params)]
    if body is not None:
        argv += ['--json', json.dumps(body)]
    if dry_run:
        argv += ['--dry-run']
    save(attempt / (name + '-command.json'), {'argv': argv, 'started_utc': utc_now()})
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired as exc:
        def partial(value):
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value
        save(attempt / (name + '-failure.json'), {
            'timeout': True, 'message': 'GWS operation exceeded 60 seconds',
            'stdout': partial(exc.stdout), 'stderr': partial(exc.stderr),
        })
        raise TrackerError(f'{name} timed out; no retry was attempted') from exc
    # Capture outputs before parsing, including errors and malformed responses.
    save(attempt / (name + '-raw.json'), {
        'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
    })
    if result.returncode:
        raise TrackerError(f'{name} failed with status {result.returncode}; see saved output; no retry was attempted')
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise TrackerError(f'{name} returned invalid JSON; see saved output; no retry was attempted') from exc
    if not isinstance(value, dict):
        raise TrackerError(f'{name} returned a non-object JSON response')
    save(attempt / (name + '.json'), value)
    return value


def resolve_tab(gws: str, attempt: Path) -> str:
    metadata = run_gws(gws, ['spreadsheets', 'get'], {
        'spreadsheetId': SPREADSHEET_ID,
        'fields': 'spreadsheetId,sheets(properties(sheetId,title))',
    }, attempt, 'metadata')
    if metadata.get('spreadsheetId') != SPREADSHEET_ID:
        raise TrackerError('Metadata returned a different spreadsheet')
    sheets = metadata.get('sheets')
    if not isinstance(sheets, list) or any(not isinstance(sheet, dict) or not isinstance(sheet.get('properties'), dict) for sheet in sheets):
        raise TrackerError('Malformed spreadsheet sheet properties')
    matches = [sheet['properties'] for sheet in sheets
               if type(sheet['properties'].get('sheetId')) is int and sheet['properties']['sheetId'] == SHEET_ID]
    if len(matches) != 1 or not isinstance(matches[0].get('title'), str) or not matches[0]['title']:
        raise TrackerError('Could not resolve the exact target sheetId uniquely')
    return matches[0]['title']


def read_table(gws: str, attempt: Path, title: str, name: str) -> list[list[str]]:
    params = {'spreadsheetId': SPREADSHEET_ID, 'range': quoted_tab(title) + '!A:D',
              'majorDimension': 'ROWS', 'valueRenderOption': 'UNFORMATTED_VALUE'}
    values = run_gws(gws, ['spreadsheets', 'values', 'get'], params, attempt, name)
    if values.get('majorDimension') != 'ROWS' or not isinstance(values.get('values'), list):
        raise TrackerError('Malformed tracker table values/majorDimension')
    if a1_range(values.get('range'), title)[0] != 1:
        raise TrackerError('Tracker table read does not start at A1 in the exact target tab')
    rows = [padded_row(row) for row in values['values']]
    if not rows or rows[0] != HEADERS:
        raise TrackerError('The target A:D headers do not exactly match the publication tracker')
    formula_params = {**params, 'valueRenderOption': 'FORMULA'}
    formulas = run_gws(gws, ['spreadsheets', 'values', 'get'], formula_params, attempt, name + '-formulas')
    if formulas.get('majorDimension') != 'ROWS' or not isinstance(formulas.get('values'), list):
        raise TrackerError('Malformed tracker formula values/majorDimension')
    if a1_range(formulas.get('range'), title) != a1_range(values.get('range'), title):
        raise TrackerError('Tracker value/formula reads identify different ranges')
    formula_rows = [padded_row(row) for row in formulas['values']]
    if not formula_rows or formula_rows[0] != HEADERS:
        raise TrackerError('Formula-backed or inconsistent tracker headers')
    if len(formula_rows) != len(rows):
        raise TrackerError('Tracker changed during the value/formula reads; reconcile before retry')
    for index, (row, formula_row) in enumerate(zip(rows, formula_rows), 1):
        for col in (0, 2):
            if formula_row[col].startswith('=') or formula_row[col] != row[col]:
                raise TrackerError(f'Formula-backed or changing tracker key at row {index}')
    return rows


def duplicate_row(rows: list[list[str]], problem_keys: set[str], doi_key: str) -> tuple[int, list[str]] | None:
    matches = []
    for number, row in enumerate(rows[1:], 2):
        try:
            existing_problem = normalize_problem(row[0]) if row[0] else None
        except (TrackerError, ValueError) as exc:
            raise TrackerError(f'Malformed nonempty problem key at tracker row {number}; reconcile it before append') from exc
        try:
            existing_doi = normalize_doi(row[2]) if row[2] else None
        except (TrackerError, ValueError) as exc:
            raise TrackerError(f'Malformed nonempty DOI key at tracker row {number}; reconcile it before append') from exc
        if existing_problem in problem_keys or existing_doi == doi_key:
            if existing_problem not in problem_keys or existing_doi != doi_key:
                raise TrackerError(f'Problem/DOI conflict at tracker row {number}; reconcile existing record')
            matches.append((number, row))
    if len(matches) > 1:
        raise TrackerError('Multiple tracker rows already contain this problem/DOI pair; reconcile duplicates')
    return matches[0] if matches else None


def readback(gws: str, attempt: Path, target_range: str, title: str, expected: list[str]) -> dict:
    value = run_gws(gws, ['spreadsheets', 'values', 'get'], {
        'spreadsheetId': SPREADSHEET_ID, 'range': target_range,
        'majorDimension': 'ROWS', 'valueRenderOption': 'UNFORMATTED_VALUE',
    }, attempt, 'readback')
    if value.get('majorDimension') != 'ROWS' or range_row(value.get('range'), title) != range_row(target_range, title):
        raise TrackerError('Independent tracker readback returned a different range or dimension')
    rows = value.get('values', [])
    if not isinstance(rows, list) or len(rows) != 1 or padded_row(rows[0]) != expected:
        raise TrackerError('Independent tracker readback does not exactly match the expected four cells')
    return value


def verify_existing(gws: str, attempt: Path, title: str, match: tuple[int, list[str]],
                    requested: list[str]) -> dict:
    number, actual = match
    target_range = quoted_tab(title) + f'!A{number}:D{number}'
    readback(gws, attempt, target_range, title, actual)
    result = {'state': 'verified_existing', 'append_performed': False, 'range': target_range,
              'actual_row': actual, 'requested_row_matches': actual == requested,
              'verified_utc': utc_now(), 'receipt_dir': str(attempt)}
    save(attempt / 'result.json', result)
    return result


def prior_append_attempts(receipts: Path, attempt: Path, problem_keys: set[str], doi_key: str) -> list[str]:
    found = []
    for path in receipts.glob('tracker-attempt-*/append-attempted.json'):
        if path.parent == attempt:
            continue
        try:
            marker = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            raise TrackerError('Unreadable prior append marker; reconcile receipts before execution') from exc
        if not isinstance(marker, dict):
            raise TrackerError('Malformed prior append marker; reconcile receipts before execution')
        previous_keys = marker.get('problem_keys', [marker.get('problem_key')])
        if not isinstance(previous_keys, list) or any(not isinstance(key, str) for key in previous_keys):
            raise TrackerError('Malformed prior problem-key marker; reconcile receipts before execution')
        if problem_keys.intersection(previous_keys) or marker.get('doi_key') == doi_key:
            found.append(str(path))
    return found


def operate(args, attempt: Path) -> dict:
    problem_key = normalize_problem(args.problem_url)
    problem_keys = {problem_key, *(normalize_problem(alias) for alias in args.problem_alias)}
    doi_key = normalize_doi(args.doi)
    notes_path = args.notes_file.resolve()
    notes_bytes = notes_path.read_bytes()
    notes = notes_bytes.decode('utf-8').rstrip('\r\n')
    if not notes.strip():
        raise TrackerError('Notes file is empty')
    if any('\x00' in cell for cell in (args.problem_url, args.doi, notes)):
        raise TrackerError('NUL characters are not accepted in publication cells')
    requested = [args.problem_url.strip(), '', 'https://doi.org/' + quote(doi_key, safe='/'), notes]
    gws = shutil.which('gws')
    if not gws:
        raise TrackerError('gws is absent from PATH')
    title = resolve_tab(gws, attempt)
    params = {'spreadsheetId': SPREADSHEET_ID, 'range': quoted_tab(title) + '!A:D',
              'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
              'includeValuesInResponse': True, 'responseValueRenderOption': 'UNFORMATTED_VALUE'}
    body = {'majorDimension': 'ROWS', 'values': [requested]}
    save(attempt / 'request.json', {
        'sheetId': SHEET_ID, 'resolved_title': title, 'params': params, 'body': body,
        'problem_key': problem_key, 'problem_keys': sorted(problem_keys), 'doi_key': doi_key,
        'supplied_problem_aliases': args.problem_alias,
        'notes_source': str(notes_path), 'notes_file_sha256': hashlib.sha256(notes_bytes).hexdigest(),
        'execute_requested': args.execute,
    })
    rows = read_table(gws, attempt, title, 'table-before')
    match = duplicate_row(rows, problem_keys, doi_key)
    if match:
        return verify_existing(gws, attempt, title, match, requested)
    run_gws(gws, ['spreadsheets', 'values', 'append'], params, attempt, 'dry-run', body, dry_run=True)
    if not args.execute:
        result = {'state': 'dry_run_ready', 'append_performed': False,
                  'receipt_dir': str(attempt), 'resolved_title': title,
                  'problem_key': problem_key, 'problem_keys': sorted(problem_keys), 'doi_key': doi_key}
        save(attempt / 'result.json', result)
        return result
    # Re-read after the local dry run, immediately before the one mutation.
    rows = read_table(gws, attempt, title, 'table-preexecute')
    match = duplicate_row(rows, problem_keys, doi_key)
    if match:
        return verify_existing(gws, attempt, title, match, requested)
    previous = prior_append_attempts(args.receipt_dir.resolve(), attempt, problem_keys, doi_key)
    if previous:
        save(attempt / 'prior-append-markers.json', previous)
        raise TrackerError('A prior append was attempted for either key but no matching row is visible; reconcile before another append')
    save(attempt / 'append-attempted.json', {
        'attempted_utc': utc_now(), 'problem_key': problem_key, 'problem_keys': sorted(problem_keys), 'doi_key': doi_key,
        'spreadsheetId': SPREADSHEET_ID, 'sheetId': SHEET_ID, 'range': params['range'],
    })
    response = run_gws(gws, ['spreadsheets', 'values', 'append'], params, attempt, 'response', body)
    updates = response.get('updates', {})
    if not isinstance(updates, dict):
        raise TrackerError('Append response updates must be an object')
    if (response.get('spreadsheetId') != SPREADSHEET_ID or updates.get('spreadsheetId') != SPREADSHEET_ID
            or any(type(updates.get(key)) is not int or updates[key] != number
                   for key, number in [('updatedRows', 1), ('updatedColumns', 4), ('updatedCells', 4)])):
        raise TrackerError('Append response does not confirm exactly four cells in one row of the expected spreadsheet')
    target_range = updates.get('updatedRange', '')
    target_row = range_row(target_range, title)
    updated_data = updates.get('updatedData')
    if not isinstance(updated_data, dict) or not isinstance(updated_data.get('values'), list):
        raise TrackerError('Append response updatedData/values must be an object containing rows')
    if updated_data.get('majorDimension') != 'ROWS' or range_row(updated_data.get('range'), title) != target_row:
        raise TrackerError('Append response echo has a different range or dimension')
    echoed = updated_data['values']
    if len(echoed) != 1 or padded_row(echoed[0]) != requested:
        raise TrackerError('Append response values do not exactly match the requested row')
    readback(gws, attempt, target_range, title, requested)
    result = {'state': 'appended_verified', 'append_performed': True, 'range': target_range,
              'verified_utc': utc_now(), 'receipt_dir': str(attempt)}
    save(attempt / 'result.json', result)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--problem-url', required=True, help='Original problem URL or explicit printed label')
    parser.add_argument('--problem-alias', action='append', default=[], help='Repeat for independently verified alternate problem URLs/IDs; no automatic alias inference')
    parser.add_argument('--doi', required=True, help='Published DOI: bare DOI, doi:<DOI>, or DOI resolver URL')
    parser.add_argument('--notes-file', type=Path, required=True, help='UTF-8 Notes text; terminal newlines are removed')
    parser.add_argument('--receipt-dir', type=Path, required=True, help='Candidate receipt folder; a unique tracker attempt subfolder is created')
    parser.add_argument('--execute', action='store_true', help='Perform exactly one append after publication/review; otherwise dry-run only')
    args = parser.parse_args(argv)
    args.receipt_dir = args.receipt_dir.resolve()
    durable_mkdir(args.receipt_dir)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = args.receipt_dir / f'tracker-attempt-{stamp}-{uuid.uuid4().hex[:8]}'
    durable_mkdir(attempt)
    try:
        result = operate(args, attempt)
    except (TrackerError, OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        result = {'state': 'failed', 'error': str(exc), 'receipt_dir': str(attempt),
                  'append_attempted': (attempt / 'append-attempted.json').exists(),
                  'recovery': 'Inspect saved receipts and live tracker before retry; no automatic append retry was made.'}
        save(attempt / 'failure.json', result)
        print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
