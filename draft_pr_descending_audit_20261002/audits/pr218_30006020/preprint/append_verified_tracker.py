"""Append PR218's verified published DOI once, never before final clearance."""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess

R = Path(__file__).resolve().parent
PUB = R.parent / 'publication'
T = PUB / 'private_transport/tracker'
GWS = '/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'


def call(label, args):
    p = subprocess.run([GWS, *args], capture_output=True, text=True, timeout=60)
    (T / (label + '-stdout.json')).write_text(p.stdout)
    (T / (label + '-stderr.txt')).write_text(p.stderr)
    if p.returncode:
        raise RuntimeError(label + ' failed; reconcile saved outcome before any retry')
    return json.loads(p.stdout)


assert not (PUB / 'TRACKER_VERIFIED_APPEND.json').exists(), 'Already verified; use read-only reconciliation'
clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified']
T.mkdir(parents=True, exist_ok=True)
doi = z['doi_url']
meta = call('01-properties', ['sheets', 'spreadsheets', 'get', '--params', json.dumps({'spreadsheetId': SHEET})])
tabs = [s['properties'] for s in meta['sheets'] if s['properties']['sheetId'] == 1254632077]
assert len(tabs) == 1 and tabs[0]['title'] == 'Math Puzzles'
row = ['https://doi.org/10.4171/owr/2024/41', '', doi,
       'Intermediate-area cylinders in the principal quadratic stratum — Alec Kriebel, v1.0, 2026-10-15. '
       'OWR-14298589-005 /30006020, Problem2,p2387: iterated square-count cutoff then genus, principal holomorphic quadratic stratum, '
       'unbounded heights, normalized maximal horizontal cylinder areas. Every intermediate scale gives '
       'PPP(dx/(2x)) with all fixed joint compact-window count moments; the original [1/sqrt(g),2/sqrt(g)] '
       'count tends to Poisson(log(2)/2), with the same limiting mean and variance. '
       'Credited consequence of DL/DGZZ geometry and classical ABT/AT assembly theory. '
       'Announced Delecroix–Liu microscopic work credited; unavailable manuscript contents remain a priority '
       'uncertainty, no universal first-priority claim. The separate 4g−4/6g−6 microscopic reservation is retained. '
       'Mathematical/source reproduction, extensive bounded priority audit and fresh sequential manuscript '
       'reviews passed after global fixes. Seven-page note and portable verification:7100 exact assertions, '
       '46233 labelled permutations,123 DVV cases. AI tools used extensively; unrefereed, no external human '
       'peer review. PR:https://github.com/AlecKriebel/Math/pull/218']
values = call('02-before', ['sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({
    'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:D"})]).get('values', [])
assert values and values[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
existing = [(i, r) for i, r in enumerate(values, 1) if any(z['doi'] in str(c) for c in r)]
attempt = T / 'APPEND_ATTEMPT.json'
if existing:
    assert len(existing) == 1 and existing[0][1] == row and attempt.exists(), 'Existing DOI requires reconciliation'
    target = "'Math Puzzles'!A" + str(existing[0][0]) + ':D' + str(existing[0][0])
    append_count = 0
else:
    assert not attempt.exists(), 'Previous append outcome unresolved; no second write permitted'
    payload = {'majorDimension': 'ROWS', 'values': [row]}
    attempt.write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(), 'spreadsheet_id': SHEET,
                                  'sheet_id': 1254632077, 'doi_url': doi, 'payload': payload,
                                  'status': 'write about to be attempted; outcome not yet known'}, indent=2) + '\n')
    result = call('03-append', ['sheets', 'spreadsheets', 'values', 'append', '--params', json.dumps({
        'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:D", 'valueInputOption': 'RAW',
        'insertDataOption': 'INSERT_ROWS', 'includeValuesInResponse': True}), '--json', json.dumps(payload)])
    update = result['updates']
    assert update['updatedRows'] == 1 and update['updatedCells'] == 4
    assert update['updatedData']['values'] == [row]
    target = update['updatedRange']
    append_count = 1
readback = call('04-readback', ['sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({
    'spreadsheetId': SHEET, 'range': target})])
assert readback['values'] == [row]
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'verified': True, 'spreadsheet_id': SHEET,
           'sheet_id': 1254632077, 'updated_range': target, 'doi_url': doi, 'values': row,
           'cli': 'Google Workspace CLI', 'append_count': append_count,
           'reconciled_existing_attempt': append_count == 0, 'exact_all_four_cells_readback': True}
(PUB / 'TRACKER_VERIFIED_APPEND.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(receipt, indent=2, ensure_ascii=False))
