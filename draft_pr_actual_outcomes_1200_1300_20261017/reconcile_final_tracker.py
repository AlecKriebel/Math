#!/usr/bin/env python3
"""Read back all twelve completed own-shard tracker rows without mutation."""
from pathlib import Path
import datetime, hashlib, json, re, runpy

ROOT = Path(__file__).resolve().parent
ELIGIBLE = [1205, 1211, 1216, 1225, 1241, 1261, 1262, 1268, 1271, 1274, 1280, 1283]

def need(value, message):
    if not value:
        raise RuntimeError(message)

def main():
    state = json.loads((ROOT / 'PROGRAM_STATE.json').read_text())
    need(state['completed_prs'] == ELIGIBLE and state['current_pr'] is None,
         'All twelve admitted cases must complete first')
    records = state['publications']
    need([p['pr'] for p in records] == ELIGIBLE and len({p['doi'] for p in records}) == 12,
         'Exact twelve distinct publication identities required')
    out = ROOT / 'final_scope_refresh'
    need((out / 'FINAL_LIVE_METADATA.json').is_file(), 'Final metadata capture required first')
    need(not (out / 'FINAL_TRACKER_RECONCILIATION.json').exists(), 'Preserve prior readback')
    tracker = runpy.run_path(str(ROOT / 'audits/pr1283_30005434/publication/append_tracker.py'))
    properties = tracker['call'](['spreadsheets', 'get'],
                               {'spreadsheetId': tracker['SID'], 'fields': 'sheets.properties'})
    tabs = [s['properties'] for s in properties.get('sheets', [])
            if s.get('properties', {}).get('sheetId') == tracker['GID']]
    need(len(tabs) == 1 and tabs[0]['title'] == 'Math Puzzles', 'Designated sheet association differs')
    response = tracker['call'](['spreadsheets', 'values', 'get'],
                              {'spreadsheetId': tracker['SID'], 'range': "'Math Puzzles'!A:D",
                               'valueRenderOption': 'UNFORMATTED_VALUE'})
    rows = response.get('values', [])
    need(rows and rows[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'],
         'Tracker headers differ')
    checks = []
    for publication in records:
        folder = ROOT / 'audits' / ('pr' + str(publication['pr']) + '_' + str(publication['problem_id']))
        receipt_path = folder / 'publication/tracker/TRACKER_RECEIPT.json'
        receipt = json.loads(receipt_path.read_text())
        need(receipt['spreadsheetId'] == tracker['SID'] and receipt['gid'] == tracker['GID']
             and receipt['readback_verified'] is True, 'Wrong saved sheet identity')
        match = re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1", receipt['updatedRange'])
        need(match is not None and int(match.group(1)) >= 2, 'Invalid saved range')
        number = int(match.group(1))
        row = receipt['row']
        need(len(row) == 4 and row[1] == '' and row[2] == publication['doi_url']
             and publication['doi_url'] == 'https://doi.org/' + publication['doi'],
             'Saved complete row/DOI identity differs')
        need(number <= len(rows) and rows[number - 1] == row, 'Actual full row differs')
        pattern = re.compile(r'(?<![A-Za-z0-9])' + re.escape(publication['doi']) + r'(?![A-Za-z0-9])')
        matches = [i + 1 for i, cells in enumerate(rows)
                   if any(pattern.search(str(cell)) for cell in cells)]
        need(matches == [number], 'Missing or duplicate DOI row')
        need(publication['tracker_range'] == receipt['updatedRange'], 'Disposition range differs')
        checks.append({'pr': publication['pr'], 'doi': publication['doi'],
                       'range': receipt['updatedRange'], 'actual_full_four_cell_row_exact': True,
                       'matching_doi_rows': matches,
                       'saved_receipt_sha256': hashlib.sha256(receipt_path.read_bytes()).hexdigest()})
    report = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS', 'spreadsheetId': tracker['SID'], 'gid': tracker['GID'],
              'observed_sheet_properties': tabs[0], 'completed_publications': len(checks),
              'checks': checks,
              'scope': 'Fresh read-only full four-cell row and unique DOI-row checks for all twelve completed cases. Per-case alias checks and earlier public-artifact/metadata/immutable-merge verification remain separately recorded. No additional append or PR action.'}
    # Other projects' sheet rows are read-only comparison inputs, not our
    # publication material. Keep full responses in the ignored local folder.
    local = ROOT / '_local/final_tracker_readback'
    local.mkdir(parents=True, exist_ok=True)
    for name, value in [('FINAL_TRACKER_PROPERTIES.json', properties),
                        ('FINAL_TRACKER_VALUES.json', response)]:
        (local / name).write_text(json.dumps(value, indent=2) + '\n')
    (out / 'FINAL_TRACKER_RECONCILIATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'completed_publications': len(checks),
                      'gid': tracker['GID']}, indent=2))

if __name__ == '__main__':
    main()
