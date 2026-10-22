"""One existing-publication row; native numeric-sheet append, never upload."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import unicodedata
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = ROOT / 'PR1186_EXISTING_PUBLICATION_LEDGER_PROPOSAL.json'
CASE = ROOT / 'private/pr1186_existing_publication/ledger_action_01'
BOOK = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
TITLE = 'Math Puzzles'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def durable(path, value):
    data = (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode()
    with path.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    sync_directory(path.parent)


def sync_directory(path):
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def cli(parts, params, body=None):
    command = ['gws', 'sheets', 'spreadsheets', *parts,
               '--params', json.dumps(params)]
    if body is not None:
        command += ['--json', json.dumps(body, ensure_ascii=False)]
    result = subprocess.run(command, capture_output=True)
    if result.returncode and CASE.exists():
        durable(CASE / 'CLI_FAILURE.json', {'parts': parts, 'returncode': result.returncode,
            'stdout': result.stdout.decode(errors='replace'),
            'stderr': result.stderr.decode(errors='replace')})
    require(result.returncode == 0, 'CLI failed; inspect private capture, do not retry append')
    return json.loads(result.stdout)


def metadata():
    value = cli(['get'], {'spreadsheetId': BOOK, 'fields': 'spreadsheetId,sheets(properties)'})
    require(value.get('spreadsheetId') == BOOK, 'Workbook mismatch')
    found = [x['properties'] for x in value['sheets'] if x['properties']['sheetId'] == GID]
    require(len(found) == 1, 'Numeric sheet not unique')
    sheet = found[0]
    require(sheet['title'] == TITLE and sheet['sheetType'] == 'GRID', 'Sheet identity mismatch')
    require(sheet['gridProperties']['columnCount'] == 43, 'Column extent changed')
    return sheet


def read(mode, sheet):
    value = cli(['values', 'batchGetByDataFilter'], {'spreadsheetId': BOOK}, {
        'dataFilters': [{'gridRange': {'sheetId': GID}}],
        'majorDimension': 'ROWS', 'valueRenderOption': mode})
    require(value.get('spreadsheetId') == BOOK, 'Read workbook mismatch')
    matches = value.get('valueRanges', [])
    require(len(matches) == 1, 'Read match not unique')
    match = matches[0]
    require(match.get('dataFilters') == [{'gridRange': {'sheetId': GID}}], 'Read filter mismatch')
    result = match['valueRange']
    expected = "'Math Puzzles'!A1:AQ"+str(sheet['gridProperties']['rowCount'])
    require(result.get('range') == expected and result.get('majorDimension') == 'ROWS', 'Read extent mismatch')
    rows = result.get('values', [])
    require(rows and rows[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'], 'Header mismatch')
    require(all(isinstance(row, list) and len(row) <= 43 for row in rows), 'Invalid rows')
    return value, rows


def identity_hits(rows):
    hits = []
    for index, row in enumerate(rows[1:], 2):
        text = urllib.parse.unquote(unicodedata.normalize('NFKC', ' '.join(map(str, row)))).casefold()
        text = ''.join(c for c in text if unicodedata.category(c) != 'Cf')
        if ('18154085' in text or '18154084' in text or 'van doorn' in text
                or 'distinct multiples' in text
                or re.search(r'(?<!\d)2274(?!\d)|ep\s*[-#]?\s*711(?!\d)', text)
                or re.search(r'erd[oőö]s\s+(?:problem\s*)?[-#]?\s*711(?!\d)', text)
                or re.search(r'erdosproblems\.com/(?:problems?/)?711(?:\D|$)', text)
                or re.search(r'github\.com/aleckriebel/math/pull/1186(?:\D|$)', text)):
            hits.append(index)
    return hits


def main():
    proposal_bytes = PROPOSAL.read_bytes()
    proposal_digest = hashlib.sha256(proposal_bytes).hexdigest()
    proposal = json.loads(proposal_bytes)
    require(proposal['spreadsheet_id'] == BOOK and proposal['sheet_gid'] == GID
            and proposal['sheet_title'] == TITLE, 'Proposal target mismatch')
    row = proposal['row']
    require(len(row) == 4 and all(type(x) is str for x in row) and row[1] == '', 'Four strings required')
    require(row[2] == 'https://doi.org/10.5281/zenodo.18154085', 'DOI mismatch')
    proof_path = ROOT / proposal['publication_verification']
    proof_bytes = proof_path.read_bytes()
    require(hashlib.sha256(proof_bytes).hexdigest() == proposal['publication_verification_sha256'], 'Verification drift')
    proof = json.loads(proof_bytes)
    record = json.loads(urllib.request.urlopen('https://zenodo.org/api/records/18154085', timeout=45).read())
    require(record.get('state') == 'done' and record.get('submitted') is True, 'Not published')
    require(record['doi'] == proof['doi'] and record['metadata']['title'] == proof['title']
            and record['metadata']['creators'] == proof['creators'], 'Publication metadata drift')
    require(len(record['files']) == 1 and record['files'][0]['key'] == proof['files'][0]['name']
            and record['files'][0]['size'] == proof['files'][0]['bytes']
            and record['files'][0]['checksum'] == proof['files'][0]['checksum'], 'Publication payload inventory drift')
    with urllib.request.urlopen('https://doi.org/'+proof['doi'], timeout=45) as response:
        require(response.status == 200, 'DOI does not resolve')
    live = json.loads(subprocess.check_output(['gh', 'api', 'repos/AlecKriebel/Math/pulls/1186']))
    old = json.loads((ROOT / 'PR1186_DISPOSITION.json').read_bytes())
    require(live['head']['sha'] == old['inventory_head_sha'], 'PR head changed')
    require(hashlib.sha256((live['body'] or '').encode()).hexdigest() == old['inventory_body_sha256'], 'PR body changed')
    sheet = metadata()
    first, before = read('UNFORMATTED_VALUE', sheet)
    formula, formula_rows = read('FORMULA', sheet)
    require(before == formula_rows, 'Formula/value ambiguity or concurrent edit')
    require(metadata() == sheet, 'Sheet metadata changed')
    final_before, before_again = read('UNFORMATTED_VALUE', sheet)
    require(before_again == before, 'Ledger changed during preflight')
    require(not identity_hits(before), 'Existing result lead requires reconciliation; no append')
    require(PROPOSAL.read_bytes() == proposal_bytes, 'Proposal changed during preflight')
    require(proof_path.read_bytes() == proof_bytes, 'Publication verification changed during preflight')
    CASE.mkdir(exist_ok=False)
    sync_directory(CASE.parent)
    durable(CASE / 'before_unformatted.json', first)
    durable(CASE / 'before_formula.json', formula)
    request = {'requests': [{'appendCells': {'sheetId': GID,
        'rows': [{'values': [{'userEnteredValue': {'stringValue': x}} for x in row]}],
        'fields': 'userEnteredValue'}}]}
    intent = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'new_publication': False,
              'proposal_sha256': proposal_digest,
              'previous_rows': len(before), 'request': request,
              'unknown_outcome_rule': 'Never repeat append; inspect current ledger first.'}
    durable(CASE / 'INTENT.json', intent)
    require(PROPOSAL.read_bytes() == proposal_bytes, 'Proposal changed before append')
    require(proof_path.read_bytes() == proof_bytes, 'Publication verification changed before append')
    # Exactly one write call. The private case directory prevents blind reruns.
    answer = cli(['batchUpdate'], {'spreadsheetId': BOOK}, request)
    durable(CASE / 'WRITE_RESPONSE.json', answer)
    require(answer.get('spreadsheetId') == BOOK and answer.get('replies') == [{}], 'Unexpected append response')
    after_sheet = metadata()
    after_value, after = read('UNFORMATTED_VALUE', after_sheet)
    durable(CASE / 'AFTER.json', after_value)
    require(after[:len(before)] == before, 'Earlier rows changed; inspect without rollback')
    exact = [index for index, value in enumerate(after, 1) if value == row]
    require(len(exact) == 1 and exact[0] > len(before), 'Exact appended row not unique')
    require(identity_hits(after) == exact, 'Result/DOI duplicate or drift after append')
    receipt = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'status': 'verified',
        'pr': 1186, 'doi': proof['doi'], 'row': exact[0], 'new_publication': False,
        'spreadsheet_mutation': True, 'new_row': True, 'previous_rows_preserved': len(before),
        'after_rows': len(after), 'numeric_sheet_id': GID, 'exact_four_cells_read_back': True,
        'proposal': PROPOSAL.name, 'request_method': 'native appendCells, four string values',
        'private_action_capture': str(CASE.relative_to(ROOT))}
    durable(ROOT / 'PR1186_EXISTING_PUBLICATION_LEDGER_RECONCILIATION.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
