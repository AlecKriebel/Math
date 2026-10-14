"""Record one confirmed preprint through Google Workspace CLI, without blind retries."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess

SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB = 'Math Puzzles'
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']


def call(method, params, body=None):
    command = ['gws', 'sheets', 'spreadsheets', 'values', method,
               '--params', json.dumps(params)]
    if body is not None:
        command += ['--json', json.dumps(body)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audit', type=Path)
    parser.add_argument('problem')
    parser.add_argument('pr', type=int)
    parser.add_argument('doi')
    args = parser.parse_args()
    audit = args.audit.resolve()
    publication = json.loads((audit / 'publication/PUBLISH_RECEIPT.json').read_text())
    if (publication.get('state') != 'published' or publication.get('doi') != args.doi
            or not args.doi.startswith('10.5281/zenodo.')):
        raise ValueError('DOI does not match the confirmed publication receipt')
    metadata = json.loads((audit / 'preprint/zenodo-metadata.json').read_text())['metadata']
    title = metadata['title']
    doi_url = 'https://doi.org/' + args.doi
    pr_url = f'https://github.com/AlecKriebel/Math/pull/{args.pr}'
    scope_path = audit / 'TRACKER_SCOPE.json'
    scope = 'Full claimed solution independently internally audited.'
    if scope_path.is_file():
        scope = json.loads(scope_path.read_text())['summary']
        if not isinstance(scope, str) or not scope.strip():
            raise ValueError('Tracker scope must be a nonempty authored statement')
    notes = (f"{title}; Alec Kriebel; version {metadata['version']}; "
             f"preprint date {metadata['publication_date']}; problem {args.problem}; "
             f"{pr_url}. {scope} "
             "Extensive AI use; unrefereed, no external human peer review or formal "
             "proof verification. Bounded priority audit found no earlier full "
             "resolution; first historical priority is not certified. "
             "Deposit includes PDF and source/verification archive.")
    values = [f'https://www.unsolvedmath.com/problems/{args.problem}', '', doi_url, notes]
    params = {'spreadsheetId': SHEET, 'range': f"'{TAB}'!A:D",
              'valueRenderOption': 'UNFORMATTED_VALUE'}
    existing = call('get', params).get('values', [])
    if not existing or existing[0] != HEADERS:
        raise ValueError('Tracker headers changed')
    same_doi = [(i + 1, row) for i, row in enumerate(existing)
                if any(args.doi in str(cell) for cell in row)]
    if same_doi:
        if len(same_doi) != 1 or (same_doi[0][1] + [''] * 4)[:4] != values:
            raise ValueError('Existing DOI entry is ambiguous or differs')
        row = same_doi[0][0]
        response = {'already_recorded': True,
                    'updates': {'updatedRange': f"'{TAB}'!A{row}:D{row}"}}
    else:
        if any(any(str(cell).rstrip('/').endswith('/' + args.problem) or
                       title in str(cell) or pr_url in str(cell) for cell in row)
               for row in existing[1:]):
            raise ValueError('Problem already has a different tracker entry; reconcile it')
        write_params = {'spreadsheetId': SHEET, 'range': f"'{TAB}'!A:D",
                        'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                        'includeValuesInResponse': True}
        # One write only. An ambiguous failure must be reconciled by reading the sheet.
        response = call('append', write_params, {'majorDimension': 'ROWS', 'values': [values]})
    (audit / 'publication/SHEET_APPEND_RECEIPT.json').write_text(
        json.dumps(response, indent=2) + '\n')
    actual_range = response['updates']['updatedRange']
    readback = call('get', {'spreadsheetId': SHEET, 'range': actual_range,
                            'valueRenderOption': 'UNFORMATTED_VALUE'})
    if readback.get('values') != [values]:
        raise ValueError('Tracker readback differs from the intended four cells')
    receipt = {'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'spreadsheetId': SHEET, 'tab_gid': 1254632077,
               'updated_range': actual_range, 'doi': args.doi,
               'intended_values': values, 'readback': readback, 'result': 'PASS'}
    (audit / 'publication/SHEET_VERIFICATION.json').write_text(
        json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'result': 'PASS', 'doi': args.doi, 'updated_range': actual_range}))


if __name__ == '__main__':
    main()
