"""Append PR211's verified published DOI once, never before final clearance."""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess

R = Path(__file__).resolve().parent.parent / 'preprint'
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
assert not clear['unresolved_optional_findings']
z = json.loads((PUB / 'ZENODO_VERIFIED_PUBLICATION.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified']
T.mkdir(parents=True, exist_ok=True)
doi = z['doi_url']
meta = call('01-properties', ['sheets', 'spreadsheets', 'get', '--params', json.dumps({'spreadsheetId': SHEET})])
tabs = [s['properties'] for s in meta['sheets'] if s['properties']['sheetId'] == 1254632077]
assert len(tabs) == 1 and tabs[0]['title'] == 'Math Puzzles'
row = ['https://arxiv.org/abs/2004.12497v11', '', doi,
       'An odd-period product for focal inversions of outer billiard polygons — Alec Kriebel, v1.0, 2026-10-15. '
       'AMR-050-0063 /5100063 /k904,a (v10 k808,a). Original-focus unit inversion of OUTER tangent vertices; '
       'signed straight-edge shoelace area product, strict nondegenerate confocal elliptical caustic, '
       'all odd least periods and coprime stars/N3, fixed repetition r^2. Explicit edge factorization, '
       'cyclic double-principal-part cancellation and classical complementary zero/pole argument. '
       'Stachel coordinates, AST complex billiard methods, KLS cyclic elliptic methods, Chavez-Caliz '
       'earlier complementary area-divisor work and related original-vertex products credited. '
       'No exact prior general proof verified in two independent bounded priority audits; historical '
       'novelty undetermined. Talented Mr Inversive Triangle journal-final subscription access limit, '
       'selected-passage and unresolved-source limits retained. No first-proof, absolute-priority, '
       'new-general-method or present-worldwide-open claim. Required fresh sequential whole-package '
       'adversarial reviews and global fixes completed. Portable ten-job replay and exact controls; '
       'uncertified numerics support rather than replace universal proof. Extensive AI use; unrefereed, '
       'no independent human peer review or proof-assistant formalization. '
       'PR:https://github.com/AlecKriebel/Math/pull/211']

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
