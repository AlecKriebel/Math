"""Append PR209's verified published DOI once, never before final clearance."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release helpers refuse optimized Python before any action')
from release_binding import context,binding,unchanged,publication,tracker,acquire,exclusive_json,pr_identity,require,digest,durable_mkdir
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
_RELEASE_LOCK=acquire(PUB)
CTX=context(R)
clear=CTX['clear']
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
assert not clear['unresolved_optional_findings']
z=publication(R,PUB,CTX)
assert z['submitted'] and z['metadata_and_files_verified']
durable_mkdir(T)
doi = z['doi_url']
meta = call('01-properties', ['sheets', 'spreadsheets', 'get', '--params', json.dumps({'spreadsheetId': SHEET})])
tabs = [s['properties'] for s in meta['sheets'] if s['properties']['sheetId'] == 1254632077]
assert len(tabs) == 1 and tabs[0]['title'] == 'Math Puzzles'
row = ['https://arxiv.org/abs/2004.12497v11', '', doi, 'The outer center-pedal area product in elliptic billiards — Alec Kriebel, v1.0,2026-10-16. AMR-050-0015 /5100015 /k303,b. Signed product of outer tangent-polygon area and actual perpendicular-center-foot area on its boundary tangent side LINES; strict nondegenerate confocal elliptical caustic, periods not divisible by four, admitted coprime stars, reversal and fixed repeats(d²); circle separate. Explicit fixed-linear edge-vector map and classical odd cyclic Jacobi identity give a full all-phase proof and constant. KLS2002, KS2003/2004, AST/BT2020, Stachel/Jacobi/conic and established pole methods credited. A.Ferudun2026v1.1 Theorem2/Section6 DOI10.5281/zenodo.23088516 is the exact full contemporary theorem; v1.0 centered primitive even subset distinguished. Historical ordering, independent non-derivation and novelty undetermined; no first-proof/exclusive/new-identity/current-worldwide-open claim. Required fresh sequential whole-package reviews/global fixes completed before deposit; portable eight-suite exact/uncertified numerical controls, originals and correction evidence retained. Extensive AI use; unrefereed, no independent human peer review/formal proof verification. PR:https://github.com/AlecKriebel/Math/pull/209']


values = call('02-before', ['sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({
    'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:D"})]).get('values', [])
assert values and values[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
import re
problem=re.compile(r'(?<![0-9])5100015(?![0-9])|AMR-050-0015',re.I)
problem_rows=[(i,r) for i,r in enumerate(values,1) if any(problem.search(str(c)) for c in r)]
existing = [(i, r) for i, r in enumerate(values, 1) if any(z['doi'] in str(c) for c in r)]
require(not problem_rows or (len(problem_rows)==1 and problem_rows==existing and problem_rows[0][1]==row),'Conflicting problem row already exists; reconcile read-only')
attempt = T / 'APPEND_ATTEMPT.json'
if existing:
    assert len(existing) == 1 and existing[0][1] == row and attempt.exists(), 'Existing DOI requires reconciliation'
    old_attempt=json.loads(attempt.read_text())
    require(old_attempt.get('release_binding')==binding(CTX) and old_attempt.get('payload',{}).get('values')==[row],'Prior attempt belongs to different release/payload')
    target = "'Math Puzzles'!A" + str(existing[0][0]) + ':D' + str(existing[0][0])
    append_count = 0
else:
    assert not attempt.exists(), 'Previous append outcome unresolved; no second write permitted'
    payload = {'majorDimension': 'ROWS', 'values': [row]}
    unchanged(R,CTX);publication(R,PUB,CTX)
    exclusive_json(attempt,{'utc':datetime.now(timezone.utc).isoformat(),'spreadsheet_id':SHEET,'sheet_id':1254632077,'doi_url':doi,'payload':payload,'release_binding':binding(CTX),'status':'single append about to be attempted'})
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
           'reconciled_existing_attempt': append_count == 0, 'exact_all_four_cells_readback': True,'release_binding':binding(CTX),'publication_receipt_sha256':digest(PUB/'ZENODO_VERIFIED_PUBLICATION.json')}
(PUB / 'TRACKER_VERIFIED_APPEND.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(receipt, indent=2, ensure_ascii=False))
