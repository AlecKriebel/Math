"""Eight existing Crossref publications; one native append, never an upload."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import html
import json
import re
import subprocess
import unicodedata
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / 'EXISTING_PUBLICATION_BATCH_A_PLUS1194_PROPOSAL.json'
PLAN_SHA = '6aa80b6d6db0197d953d4b237c2477ec1421a79409321323aec94b749fe2ca8c'
HELPER = ROOT / 'audits/pr1186_2274/reconcile_existing_row.py'
HELPER_SHA = '0360bb97064000502aa04a38c7f8816229b298fcdcb2295f16acc7f2e53af1a5'
CASE = ROOT / 'private/existing_publication_batch_a_plus1194_action01'
BOOK = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
PRS = [1021, 1065, 1068, 1142, 1145, 1146, 1152, 1194]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def folded(value):
    text = str(value)
    for unused in range(8):
        decoded = html.unescape(urllib.parse.unquote(text))
        if decoded == text:
            break
        text = decoded
    text = unicodedata.normalize('NFKD', text).casefold()
    return ''.join(c for c in text if c.isalnum())


def hits(rows, item):
    aliases = [folded(x) for x in item['aliases']]
    return [n for n, row in enumerate(rows[1:], 2)
            if any(alias in folded(' '.join(map(str, row))) for alias in aliases)]


def registry_projection(message):
    return {
        'doi': message['DOI'].casefold(), 'title': message['title'],
        'authors': [{k: x[k] for k in ['given', 'family', 'name'] if k in x}
                    for x in message.get('author', [])
                    if any(x.get(k) for k in ['given', 'family', 'name'])],
        'type': message['type'], 'publisher': message.get('publisher'),
        'container_title': message.get('container-title', []),
        'volume': message.get('volume'), 'issue': message.get('issue'),
        'page': message.get('page'), 'article_number': message.get('article-number'),
        'issued': message.get('issued', {}).get('date-parts'),
        'published_online': message.get('published-online', {}).get('date-parts')}


def verify_publication(item):
    expected_url = 'https://api.crossref.org/works/' + item['doi']
    require(item['registry_url'] == expected_url, 'Unexpected registry URL')
    with urllib.request.urlopen(expected_url, timeout=45) as response:
        require(response.status == 200, 'Registry unavailable')
        raw = response.read()
    registry = json.loads(raw)
    require(registry.get('status') == 'ok' and
            registry_projection(registry['message']) == item['registry_projection'],
            'Bibliographic identity changed')
    with urllib.request.urlopen('https://doi.org/' + item['doi'], timeout=45) as response:
        require(response.status == 200, 'DOI does not resolve')
        final_url = response.url
    live = json.loads(subprocess.check_output(
        ['gh', 'api', 'repos/AlecKriebel/Math/pulls/' + str(item['pr'])]))
    require(live['head']['sha'] == item['head'] and
            digest((live.get('body') or '').encode()) == item['body_sha256'],
            'Reviewed PR identity changed')
    return {'pr': item['pr'], 'doi': item['doi'], 'doi_status': 200,
            'doi_final_url': final_url, 'registry_sha256': digest(raw),
            'bibliographic_projection_matches': True, 'live_head': live['head']['sha'],
            'live_state': live['state'], 'live_merged': live['merged']}


def verify_inputs(plan_bytes, plan):
    require(PLAN.read_bytes() == plan_bytes, 'Plan changed')
    require(digest(HELPER.read_bytes()) == HELPER_SHA, 'Numeric helper changed')
    for name, expected in plan['input_pins'].items():
        relative = Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts,
                'Unsafe input path')
        path = ROOT / relative
        require(not any(ROOT.joinpath(*relative.parts[:i]).is_symlink()
                        for i in range(1, len(relative.parts) + 1)), 'Symlink input')
        require(digest(path.read_bytes()) == expected, 'Review input changed: ' + name)


def main():
    require(not CASE.exists(), 'Action already has a case; reconcile, never retry')
    plan_bytes = PLAN.read_bytes()
    require(digest(plan_bytes) == PLAN_SHA, 'Plan not the reviewed exact bytes')
    plan = json.loads(plan_bytes)
    require(plan['spreadsheet_id'] == BOOK and plan['sheet_gid'] == GID and
            plan['sheet_title'] == 'Math Puzzles' and plan['new_publications'] == 0,
            'Wrong action target')
    items = plan['items']
    require([x['pr'] for x in items] == PRS, 'Wrong eight publications')
    require(len({x['doi'].casefold() for x in items}) == 8, 'Duplicate DOI in batch')
    for item in items:
        row = item['row']
        require(len(row) == 4 and all(type(x) is str for x in row) and row[1] == ''
                and row[2] == 'https://doi.org/' + item['doi'], 'Invalid four cells')
        require(item['aliases'] and all(type(x) is str and folded(x) for x in item['aliases']),
                'Empty identity alias')
        original_ids = list(dict.fromkeys(re.findall(r'\b(?:OWR|AMR)-\d+-\d+\b', row[0])))
        require(item['original_problem_ids'] == original_ids and
                all(x in item['aliases'] for x in original_ids),
                'Known original problem identity missing')
        require(item['doi'] in item['aliases'] and
                all(x in item['aliases'] for x in item['problem_ids']) and
                'https://github.com/AlecKriebel/Math/pull/' + str(item['pr']) in item['aliases'],
                'Required identity alias missing')
    verify_inputs(plan_bytes, plan)
    source = HELPER.read_bytes()
    require(digest(source) == HELPER_SHA, 'Numeric helper source drift')
    functions = {'__file__': str(HELPER), '__name__': '_verified_numeric_dependency'}
    exec(compile(source, str(HELPER), 'exec'), functions)
    functions['CASE'] = CASE
    metadata, read = functions['metadata'], functions['read']
    durable, cli = functions['durable'], functions['cli']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        publications = list(pool.map(verify_publication, items))
    sheet = metadata()
    before_raw, before = read('UNFORMATTED_VALUE', sheet)
    formula_raw, formulas = read('FORMULA', sheet)
    require(before == formulas and metadata() == sheet, 'Ledger view/metadata drift')
    unused, final_before = read('UNFORMATTED_VALUE', sheet)
    require(final_before == before, 'Ledger changed before append')
    for item in items:
        require(not hits(before, item), 'Existing identity lead for PR' + str(item['pr']))
    require(before[0] == plan['schema'], 'Plan header mismatch')
    verify_inputs(plan_bytes, plan)
    CASE.mkdir(exist_ok=False)
    functions['sync_directory'](CASE.parent)
    durable(CASE / 'BEFORE_UNFORMATTED.json', before_raw)
    durable(CASE / 'BEFORE_FORMULA.json', formula_raw)
    durable(CASE / 'PUBLICATION_PREFLIGHT.json', publications)
    rows = [item['row'] for item in items]
    request = {'requests': [{'appendCells': {'sheetId': GID,
        'rows': [{'values': [{'userEnteredValue': {'stringValue': cell}}
                             for cell in row]} for row in rows],
        'fields': 'userEnteredValue'}}]}
    durable(CASE / 'INTENT.json', {'at': dt.datetime.now(dt.timezone.utc).isoformat(),
        'plan_sha256': digest(plan_bytes), 'helper_sha256': HELPER_SHA,
        'previous_rows': len(before), 'request': request,
        'unknown_outcome_rule': 'Never repeat append; inspect exact live rows and case.'})
    verify_inputs(plan_bytes, plan)
    # Exactly one write attempt; an existing case always blocks another invocation.
    answer = cli(['batchUpdate'], {'spreadsheetId': BOOK}, request)
    durable(CASE / 'WRITE_RESPONSE.json', answer)
    require(answer.get('spreadsheetId') == BOOK and answer.get('replies') == [{}],
            'Unexpected native append reply')
    after_raw, after = read('UNFORMATTED_VALUE', metadata())
    durable(CASE / 'AFTER.json', after_raw)
    require(after[:len(before)] == before, 'Earlier rows changed; inspect, no rollback')
    found = []
    for item in items:
        exact = [n for n, row in enumerate(after, 1) if row == item['row']]
        require(len(exact) == 1 and exact[0] > len(before) and hits(after, item) == exact,
                'Missing, duplicated or changed result row for PR' + str(item['pr']))
        found.append({'pr': item['pr'], 'doi': item['doi'], 'row': exact[0],
                      'problem_ids': item['problem_ids']})
    require([x['row'] for x in found] == list(range(found[0]['row'], found[0]['row'] + 8)),
            'Batch order/contiguity mismatch')
    receipt = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'status': 'verified',
        'new_publications': 0, 'spreadsheet_mutation': True, 'native_write_calls': 1,
        'new_rows': 8, 'previous_rows_preserved': len(before), 'after_rows': len(after),
        'numeric_sheet_id': GID, 'exact_four_cells_read_back_each': True,
        'plan_sha256': digest(plan_bytes), 'items': found,
        'private_case': str(CASE.relative_to(ROOT))}
    durable(ROOT / 'EXISTING_PUBLICATION_BATCH_A_PLUS1194_RECONCILIATION.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
