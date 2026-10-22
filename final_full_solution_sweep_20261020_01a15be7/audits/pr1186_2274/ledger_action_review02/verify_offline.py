"""Independent whole-runner stubs: no provider call and review-owned files only."""
from pathlib import Path
import contextlib
import copy
import hashlib
import io
import json
import os
import stat
import subprocess
import types
import urllib.parse

HERE = Path(__file__).resolve().parent
EFFORT = HERE.parents[2]
SOURCE = (HERE / 'inputs/reconcile_existing_row.py').read_bytes()
PROPOSAL = (HERE / 'inputs/PR1186_EXISTING_PUBLICATION_LEDGER_PROPOSAL.json').read_bytes()
PROOF = (HERE / 'inputs/ROOT_EXISTING_PUBLICATION_VERIFICATION.json').read_bytes()
OLD = json.loads((EFFORT / 'PR1186_DISPOSITION.json').read_bytes())
RECORD = json.loads((EFFORT / 'private/pr1186_existing_publication/record.json').read_bytes())
BOOK = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
HEADER = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']


def need(value, message):
    if not value:
        raise RuntimeError(message)


class Response:
    status = 200
    def __init__(self, data=b''):
        self.data = data
    def read(self):
        return self.data
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return None


class World:
    def __init__(self, name, kind, seed=None):
        self.name = name
        self.kind = kind
        self.root = HERE / 'private_controls' / name
        self.root.mkdir(parents=True, exist_ok=False)
        self.proposal = self.root / 'PR1186_EXISTING_PUBLICATION_LEDGER_PROPOSAL.json'
        self.proposal.write_bytes(PROPOSAL)
        proof = self.root / 'audits/pr1186_2274/ROOT_EXISTING_PUBLICATION_VERIFICATION.json'
        proof.parent.mkdir(parents=True)
        proof.write_bytes(PROOF)
        self.proof = proof
        (self.root / 'PR1186_DISPOSITION.json').write_text(json.dumps(OLD))
        self.case = self.root / 'private/pr1186_existing_publication/ledger_action_01'
        self.case.parent.mkdir(parents=True)
        self.rows = [HEADER, ['unrelated prior theorem', '', '10.1234/example', 'preserve']]
        if seed is not None:
            self.rows.append(seed)
        self.before = copy.deepcopy(self.rows)
        self.reads = 0
        self.writes = 0
        self.remote_reads = []
        self.fsyncs = []
        self.commands = []
        self.module = {'__name__': 'isolated_review', '__file__': str(HERE/'inputs/reconcile_existing_row.py')}
        exec(compile(SOURCE, str(HERE/'inputs/reconcile_existing_row.py'), 'exec'), self.module)
        self.module.update(ROOT=self.root, PROPOSAL=self.proposal, CASE=self.case)
        self.module['subprocess'] = types.SimpleNamespace(run=self.run, check_output=self.check_output)
        self.module['urllib'] = types.SimpleNamespace(parse=urllib.parse, request=types.SimpleNamespace(urlopen=self.urlopen))
        self.module['os'] = types.SimpleNamespace(O_RDONLY=os.O_RDONLY, open=os.open, close=os.close, fsync=self.fsync)

    def fsync(self, fd):
        directory = stat.S_ISDIR(os.fstat(fd).st_mode)
        self.fsyncs.append('directory' if directory else 'file')
        if self.kind == 'directory_sync_failure' and directory:
            raise OSError(28, 'review simulated no space')
        if self.kind == 'intent_sync_failure' and not directory and self.fsyncs.count('file') == 3:
            raise OSError(28, 'review simulated intent flush failure')
        if self.kind in {'late_proposal_drift','late_proof_drift'} and not directory and self.fsyncs.count('file') == 1:
            path = self.proposal if self.kind == 'late_proposal_drift' else self.proof
            path.write_bytes(path.read_bytes()+b' ')
        os.fsync(fd)

    def urlopen(self, url, timeout):
        self.remote_reads.append(url)
        if url == 'https://zenodo.org/api/records/18154085':
            record = copy.deepcopy(RECORD)
            if self.kind == 'unpublished':
                record['submitted'] = False
            if self.kind == 'payload_drift':
                record['files'][0]['checksum'] = 'md5:00000000000000000000000000000000'
            return Response(json.dumps(record).encode())
        if url == 'https://doi.org/10.5281/zenodo.18154085':
            result = Response()
            if self.kind == 'doi_error':
                result.status = 404
            return result
        raise RuntimeError('OFFLINE GUARD unknown network request: '+url)

    def check_output(self, command):
        need(command == ['gh', 'api', 'repos/AlecKriebel/Math/pulls/1186'], 'Unexpected external command')
        live = {'head': {'sha': OLD['inventory_head_sha']}, 'body': 'stub-body'}
        # Bind exactly to a stub body in this world's copied disposition.
        old = copy.deepcopy(OLD)
        old['inventory_body_sha256'] = hashlib.sha256(b'stub-body').hexdigest()
        (self.root/'PR1186_DISPOSITION.json').write_text(json.dumps(old))
        if self.kind == 'pr_head_drift':
            live['head']['sha'] = '0'*40
        if self.kind == 'pr_body_drift':
            live['body'] += ' changed'
        return json.dumps(live).encode()

    def run(self, command, capture_output):
        need(capture_output is True, 'capture_output lost')
        prefix = ['gws', 'sheets', 'spreadsheets']
        need(command[:3] == prefix, 'OFFLINE GUARD command escaped GWS stub')
        index = command.index('--params')
        parts = command[3:index]
        params = json.loads(command[index+1])
        need(params['spreadsheetId'] == BOOK, 'Wrong request book')
        body = json.loads(command[command.index('--json')+1]) if '--json' in command else None
        self.commands.append({'parts': parts, 'params': params, 'body': body})
        result = self.call(parts, body)
        if isinstance(result, subprocess.CompletedProcess):
            return result
        return subprocess.CompletedProcess(command, 0, json.dumps(result).encode(), b'')

    def call(self, parts, body):
        if parts == ['get']:
            sheet = {'sheetId': GID, 'title': 'Math Puzzles', 'sheetType': 'GRID',
                     'gridProperties': {'columnCount': 43, 'rowCount': 1178}}
            if self.kind == 'wrong_gid':
                sheet['sheetId'] += 1
            if self.kind == 'wrong_title':
                sheet['title'] = 'Other'
            if self.kind == 'wrong_width':
                sheet['gridProperties']['columnCount'] = 4
            book = 'wrong' if self.kind == 'wrong_book' else BOOK
            return {'spreadsheetId': book, 'sheets': [{'properties': sheet}]}
        if parts == ['values', 'batchGetByDataFilter']:
            need(body['dataFilters'] == [{'gridRange': {'sheetId': GID}}], 'Not exact full numeric gid read')
            need(body['majorDimension'] == 'ROWS', 'Wrong major dimension')
            self.reads += 1
            rows = copy.deepcopy(self.rows)
            if self.kind == 'formula_disagreement' and body['valueRenderOption'] == 'FORMULA':
                rows[1][0] = '=1+2'
            if self.kind == 'third_read_drift' and self.reads == 3:
                rows.append(['concurrent change'])
            if self.kind in {'proposal_drift', 'proof_drift'} and self.reads == 3:
                path = self.proposal if self.kind == 'proposal_drift' else self.proof
                path.write_bytes(path.read_bytes()+b' ')
            filter_ = {'gridRange': {'sheetId': GID}}
            if self.kind == 'response_filter_wrong_gid':
                filter_['gridRange']['sheetId'] += 1
            extent = "'Math Puzzles'!A1:AQ1178"
            if self.kind == 'short_read_extent':
                extent = "'Math Puzzles'!A1:D1178"
            if self.kind == 'earlier_row_drift' and self.writes:
                rows[1][0] = 'changed earlier row'
            if self.kind == 'postwrite_duplicate' and self.writes:
                rows.append(['https://www.erdosproblems.com/711'])
            if self.kind == 'postwrite_row_drift' and self.writes:
                rows[-1][-1] += 'changed'
            return {'spreadsheetId': BOOK, 'valueRanges': [{'dataFilters': [filter_],
                    'valueRange': {'range': extent, 'majorDimension': 'ROWS', 'values': rows}}]}
        if parts == ['batchUpdate']:
            self.writes += 1
            need(self.writes == 1, 'More than one append')
            need((self.case/'INTENT.json').is_file(), 'Intent not present before mutation')
            intent = json.loads((self.case/'INTENT.json').read_text())
            need(intent['proposal_sha256'] == hashlib.sha256(PROPOSAL).hexdigest(), 'Intent provenance drift')
            need(intent['request'] == body, 'Intent/request drift')
            need((self.case/'before_formula.json').is_file() and (self.case/'before_unformatted.json').is_file(), 'Before snapshots absent')
            need(self.fsyncs.count('directory') >= 4, 'Containing directories not flushed before append')
            requests = body['requests']
            need(len(requests) == 1 and set(requests[0]) == {'appendCells'}, 'Not a single appendCells')
            request = requests[0]['appendCells']
            need(request['sheetId'] == GID and request['fields'] == 'userEnteredValue', 'Wrong append scope')
            need(len(request['rows']) == 1 and len(request['rows'][0]['values']) == 4, 'Not four cells')
            cells = request['rows'][0]['values']
            need(all(set(c) == {'userEnteredValue'} and set(c['userEnteredValue']) == {'stringValue'} for c in cells), 'Nonliteral cell')
            row = [c['userEnteredValue']['stringValue'] for c in cells]
            need(row == json.loads(PROPOSAL)['row'] and row[1] == '', 'Row differs from reviewed proposal')
            if self.kind == 'unrelated_concurrent_append':
                self.rows.append(['unrelated concurrent append'])
            if self.kind != 'unknown_before_apply':
                self.rows.append(row)
            if self.kind in {'unknown_after_apply', 'unknown_before_apply'}:
                return subprocess.CompletedProcess([], 1, b'', b'synthetic ambiguous transport failure')
            if self.kind == 'unexpected_reply':
                return {'spreadsheetId': BOOK, 'replies': [{'unexpected': True}]}
            return {'spreadsheetId': BOOK, 'replies': [{}]}
        raise RuntimeError('OFFLINE GUARD unsupported command: '+repr(parts))

    def execute(self):
        output = io.StringIO()
        error = None
        try:
            with contextlib.redirect_stdout(output):
                self.module['main']()
        except Exception as exc:
            error = {'type': type(exc).__name__, 'message': str(exc)}
        receipt = self.root/'PR1186_EXISTING_PUBLICATION_LEDGER_RECONCILIATION.json'
        return {'name': self.name, 'kind': self.kind, 'writes': self.writes,
                'reads': self.reads, 'error': error, 'success_receipt': receipt.exists(),
                'receipt': json.loads(receipt.read_text()) if receipt.exists() else None,
                'case_guard_exists': self.case.exists(),
                'intent_exists': (self.case/'INTENT.json').exists(),
                'file_fsync_calls': self.fsyncs.count('file'),
                'directory_fsync_calls': self.fsyncs.count('directory'),
                'prior_rows_preserved_in_stub': self.rows[:len(self.before)] == self.before,
                'output_sha256': hashlib.sha256(output.getvalue().encode()).hexdigest()}


def main():
    scenarios = [('success', 'success', None), ('concurrent_unrelated', 'unrelated_concurrent_append', None)]
    aliases = {
        'canonical_problem_url': 'https://www.erdosproblems.com/711',
        'canonical_pr_url': 'https://github.com/AlecKriebel/Math/pull/1186',
        'version_doi': '10.5281/zenodo.18154085',
        'concept_doi': 'https://doi.org/10.5281/zenodo.18154084',
        'named_erdos': 'Erdős Problem #711',
        'named_erdos_decomposed': 'Erdo\u030bs 711',
        'ep': 'EP-711',
        'problem_id': '2274',
        'author': 'Wouter van Doorn',
        'title': 'distinct multiples',
        'percent_encoded_concept': '10.5281%2Fzenodo.18154084',
        'zero_width_concept': '10.5281/zenodo.1815\u200b4084',
    }
    for name, value in aliases.items():
        scenarios.append(('duplicate_'+name, 'duplicate', [value]))
    scenarios.append(('duplicate_in_AQ', 'duplicate', ['']*42+['2274']))
    for kind in ['wrong_book','wrong_gid','wrong_title','wrong_width','response_filter_wrong_gid',
                 'short_read_extent','formula_disagreement','third_read_drift','proposal_drift',
                 'proof_drift','late_proposal_drift','late_proof_drift','pr_head_drift','pr_body_drift','unpublished','payload_drift',
                 'doi_error','directory_sync_failure','intent_sync_failure','earlier_row_drift','postwrite_duplicate',
                 'postwrite_row_drift','unexpected_reply','unknown_after_apply','unknown_before_apply']:
        scenarios.append((kind, kind, None))
    results = []
    for name, kind, seed in scenarios:
        world = World(name, kind, seed)
        result = world.execute()
        success = kind in {'success','unrelated_concurrent_append'}
        after_write_failure = kind in {'earlier_row_drift','postwrite_duplicate','postwrite_row_drift',
                                      'unexpected_reply','unknown_after_apply','unknown_before_apply'}
        need(result['success_receipt'] == success, name+': unexpected success receipt')
        need(result['writes'] == (1 if success or after_write_failure else 0), name+': unexpected write count')
        need((result['error'] is None) == success, name+': unexpected exception result')
        if kind in {'unknown_after_apply','unknown_before_apply','directory_sync_failure','intent_sync_failure'}:
            previous_writes = world.writes
            rerun = world.execute()
            need(world.writes == previous_writes and not rerun['success_receipt'], name+': rerun caused mutation')
            result['rerun_error'] = rerun['error']
            result['rerun_no_extra_write'] = True
        results.append(result)
    output = {'source_sha256':hashlib.sha256(SOURCE).hexdigest(), 'proposal_sha256':hashlib.sha256(PROPOSAL).hexdigest(),
              'offline_only':True, 'scenario_count':len(results), 'all_expected_outcomes':True, 'results':results}
    (HERE/'OFFLINE_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'scenario_count':len(results),'all_expected_outcomes':True,
                      'source_sha256':output['source_sha256']},sort_keys=True))


if __name__ == '__main__':
    main()
