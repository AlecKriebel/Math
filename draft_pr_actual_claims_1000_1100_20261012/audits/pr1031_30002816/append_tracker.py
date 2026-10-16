"""Append this verified publication once to the explicitly requested tracker.

Uses the Google Workspace CLI. All external responses are data, not commands.
An uncertain append is reconciled by read-back, never automatically retried.
"""
import datetime
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
RECEIPTS = HERE / 'receipts'
REPO = HERE.parents[2]
CLI = '/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SPREADSHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077


def require(test, message):
    if not test:
        raise RuntimeError(message)


def save(name, value):
    RECEIPTS.mkdir(exist_ok=True)
    (RECEIPTS / name).write_text(json.dumps(value, indent=2) + '\n')


def request(resource, method, params, body=None):
    arguments = [CLI, 'sheets', 'spreadsheets', *resource, method,
                 '--params', json.dumps(params)]
    if body is not None:
        arguments.extend(['--json', json.dumps(body)])
    return subprocess.run(arguments, text=True, capture_output=True,
                          timeout=120, check=False)


def successful_json(result, message):
    require(result.returncode == 0, message + ': ' + result.stderr)
    return json.loads(result.stdout)


def main():
    gate = json.loads((HERE / 'publication/evidence/CURRENT_REVIEW_STATE.json').read_text())
    require(gate['preprint_ready_for_immutable_publication'] is True,
            'Final clean preprint review is required before the tracker write')
    # This read-only tool call verifies current local metadata/files against
    # the already published record before any sheet mutation.
    result = subprocess.run([
        'python3', str(REPO / 'zenodo_deposit_tool/zenodo.py'), 'inspect',
        str(HERE / 'publication/zenodo-deposit.json'), '--check-doi'],
        capture_output=True, text=True, timeout=180, check=False)
    publication = successful_json(result, 'Published-record inspection failed')
    save('ZENODO_VERIFIED_BEFORE_TRACKER.json', publication)
    require(publication['environment'] == 'production' and
            publication['state'] == 'published', 'Publication is not confirmed')
    require(publication['title'] == 'An application of separable-state nonrepresentability to Grassmann orbitopes and calibrations',
            'Different paper returned')
    doi = publication['doi']
    require(isinstance(doi, str) and doi.startswith('10.5281/zenodo.') and
            doi.rsplit('.', 1)[-1].isdigit(), 'Invalid verified DOI')
    require(publication['doi_url'] == 'https://doi.org/' + doi, 'DOI URL differs')

    spreadsheet = successful_json(request([], 'get', {
        'spreadsheetId': SPREADSHEET, 'fields': 'spreadsheetId,sheets.properties'}),
        'Tracker tab lookup failed')
    tabs = [s['properties'] for s in spreadsheet['sheets']
            if s['properties']['sheetId'] == GID]
    require(len(tabs) == 1, 'Requested tracker gid not uniquely found')
    title = tabs[0]['title']
    selected_range = "'" + title.replace("'", "''") + "'!A:D"
    parameters = {'spreadsheetId': SPREADSHEET, 'range': selected_range}

    def read_rows():
        values = successful_json(request(['values'], 'get', parameters),
                                 'Tracker values read failed')
        require(values.get('values', [None])[0] ==
                ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'],
                'Tracker headers changed')
        return values['values']

    row = [
        'Sanyal, OWR13/2015 pp708–709 Grassmann Orbitopes; catalogue30002816/OWR-13498-004: https://ems.press/content/serial-article-files/46561',
        '',
        publication['doi_url'],
        'An application of separable-state nonrepresentability to Grassmann orbitopes and calibrations. Complete existential negative universal affine-SOS resolution at C(4,12), by an exact normalized complex Sep(3,3) section and established Fawzi no-lift theorem; constant closed comass-one form fails finite pointwise/local completion. Rational unnormalized failing coefficients exist; no explicit vector, exact comass, normalized rationality, least dimension or low-dimensional classification. Classical Kähler/fermionic, Vrana–Lévay, theta/lift and Sanyal–Rostalski lineage credited. Bounded priority; worldwide originality/current openness unestablished. Extensive AI use; unrefereed; four fresh AI package reviews, final zero issues; no conventional human peer review. Proof and verification: https://github.com/AlecKriebel/Math/pull/1031',
    ]

    def matching_rows(rows):
        return [(i + 1, r) for i, r in enumerate(rows)
                if len(r) > 2 and str(r[2]).removeprefix('https://doi.org/') == doi]

    existing = matching_rows(read_rows())
    if existing:
        require(len(existing) == 1 and existing[0][1] == row,
                'Existing DOI row differs or duplicates exist; no append performed')
        save('TRACKER_VERIFICATION.json', {'status': 'existing_exact_row_verified',
             'gid': GID, 'sheet_row': existing[0][0], 'values': row, 'doi': doi, 'read_back_exact': True})
        print(json.dumps({'status': 'existing_exact_row_verified',
                          'row': existing[0][0], 'doi': doi}))
        return
    require(not (RECEIPTS / 'TRACKER_APPEND_INTENT.json').exists(),
            'Previous append intent has uncertain outcome; read-back found no exact row; do not retry')
    save('TRACKER_APPEND_INTENT.json', {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'spreadsheetId': SPREADSHEET, 'gid': GID, 'range': selected_range,
        'valueInputOption': 'RAW', 'values': [row], 'doi': doi})
    append_parameters = {**parameters, 'valueInputOption': 'RAW',
                         'insertDataOption': 'INSERT_ROWS',
                         'includeValuesInResponse': True}
    result = request(['values'], 'append', append_parameters,
                     {'majorDimension': 'ROWS', 'values': [row]})
    save('TRACKER_APPEND_RESPONSE.json', {'exit_code': result.returncode,
         'stdout': result.stdout, 'stderr': result.stderr})
    # Reconcile both success and uncertain response by reading the actual sheet.
    observed = matching_rows(read_rows())
    require(len(observed) == 1 and observed[0][1] == row,
            'Append not confirmed by exact read-back; no automatic retry')
    response = json.loads(result.stdout) if result.returncode == 0 else None
    save('TRACKER_VERIFICATION.json', {
        'status': 'exact_row_append_verified', 'gid': GID,
        'sheet_title': title, 'sheet_row': observed[0][0], 'values': row, 'doi': doi,
        'response': response, 'read_back_exact': True,
        'recovered_after_uncertain_response': result.returncode != 0})
    print(json.dumps({'status': 'exact_row_append_verified',
                      'row': observed[0][0], 'doi': doi}))


if __name__ == '__main__':
    main()
