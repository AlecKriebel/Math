#!/usr/bin/env python3
"""Read-only closure/PR/ledger checks. Never executes proposal or publisher code."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
BOOK = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077


def require(value, message):
    if not value:
        raise RuntimeError(message)


def main():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_bytes())
    pins = []
    for entry in manifest['files']:
        path = Path(entry['file'])
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe manifest path')
        content = (ROOT / path).read_bytes()
        require(len(content) == entry['bytes'] and hashlib.sha256(content).hexdigest() == entry['sha256'], 'Artifact drift: ' + str(path))
        pins.append(str(path))
    require(len(pins) == len(set(pins)), 'Duplicate manifest path')
    proposal = json.loads((ROOT / 'PROPOSED_ROWS.json').read_bytes())
    items = proposal['items']
    require([x['pr'] for x in items] == [1021,1065,1068,1142,1145,1146,1152], 'Wrong exact batch')
    require(len({x['doi'].casefold() for x in items}) == 7, 'Duplicate DOI')
    for item in items:
        require(len(item['row']) == 4 and all(type(x) is str for x in item['row']) and item['row'][1] == '', 'Row schema')
        require(item['row'][2] == 'https://doi.org/' + item['doi'], 'DOI cell mismatch')
    bindings = json.loads((ROOT / 'PR_SOURCE_BINDINGS.json').read_bytes())
    def pr_check(binding):
        response = json.loads(subprocess.check_output(['gh','api','repos/AlecKriebel/Math/pulls/' + str(binding['pr'])]))
        require(response['head']['sha'] == binding['head'], 'PR head drift')
        body = (response.get('body') or '').encode()
        require(hashlib.sha256(body).hexdigest() == binding['body_sha256'], 'PR body drift')
        return {'pr': binding['pr'], 'head': binding['head'], 'body_unchanged': True, 'live_state': response['state'], 'live_merged': response['merged']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        prs = list(pool.map(pr_check, bindings))
    response = subprocess.run(['gws','sheets','spreadsheets','values','batchGetByDataFilter', '--params',json.dumps({'spreadsheetId': BOOK}), '--json',json.dumps({'dataFilters':[{'gridRange':{'sheetId':GID}}], 'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'})], capture_output=True,check=True)
    value = json.loads(response.stdout)
    require(value.get('spreadsheetId') == BOOK and len(value.get('valueRanges', [])) == 1, 'Workbook match')
    match = value['valueRanges'][0]
    require(match.get('dataFilters') == [{'gridRange':{'sheetId':GID}}], 'Numeric sheet filter mismatch')
    result = match['valueRange']
    require(result.get('majorDimension') == 'ROWS' and result.get('range','').startswith("'Math Puzzles'!A1:AQ"), 'Read extent mismatch')
    rows = result['values']
    require(rows[0] == proposal['schema'] and max(map(len,rows)) <= 43, 'Header/schema mismatch')
    leads = {}
    for item in items:
        terms = [item['doi'], *item['problem_ids'], '/pull/' + str(item['pr'])]
        leads[str(item['pr'])] = {term: [index for index,row in enumerate(rows,1) if term.casefold() in ' '.join(map(str,row)).casefold()] for term in terms}
    print(json.dumps({'at':dt.datetime.now(dt.timezone.utc).isoformat(),'read_only':True,'manifest_members_rehashed':len(pins),'live_prs':prs,'ledger_rows':len(rows),'ledger_raw_sha256':hashlib.sha256(response.stdout).hexdigest(),'ledger_target_leads':leads,'limits':'Leads are not semantic identity decisions; any fresh hit requires parent adjudication. No write or target-proof recomputation.'},indent=2))


if __name__ == '__main__':
    main()
