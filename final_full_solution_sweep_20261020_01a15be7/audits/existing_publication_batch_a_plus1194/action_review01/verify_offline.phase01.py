"""Independent whole-action tests. All provider calls stubbed and files isolated."""
from pathlib import Path
import argparse
import copy
import contextlib
import hashlib
import io
import json
import os
import stat
import subprocess
import threading
import urllib.request

HERE = Path(__file__).resolve().parent
SOURCE = (HERE/'inputs/append_reviewed_rows.py').read_bytes()
HELPER = (HERE/'inputs/numeric_helper.py').read_bytes()
PLAN_BYTES = (HERE/'inputs/EXISTING_PUBLICATION_BATCH_A_PLUS1194_PROPOSAL.json').read_bytes()
PLAN = json.loads(PLAN_BYTES)
MOCK_PRS = json.loads((HERE/'inputs/MOCK_LIVE_PRS.json').read_text())
BOOK = PLAN['spreadsheet_id']
GID = PLAN['sheet_gid']
ORIGINAL_RUN = subprocess.run
ORIGINAL_CHECK_OUTPUT = subprocess.check_output
ORIGINAL_URLOPEN = urllib.request.urlopen
ORIGINAL_FSYNC = os.fsync


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


class Response:
    def __init__(self, data=b'', status=200, url='https://publisher.example/exact-article'):
        self.data, self.status, self.url = data, status, url
    def read(self):
        return self.data
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return None


def registry_message(item):
    x = item['registry_projection']
    result = {'DOI': x['doi'], 'title': x['title'], 'author': x['authors'],
              'type': x['type'], 'publisher': x['publisher'],
              'container-title': x['container_title'],
              'issued': {'date-parts': x['issued']}}
    for key, field in [('volume','volume'),('issue','issue'),('page','page'),('article-number','article_number')]:
        if x[field] is not None:
            result[key] = x[field]
    if x['published_online'] is not None:
        result['published-online'] = {'date-parts': x['published_online']}
    return result


class World:
    def __init__(self, namespace, name, kind, seed=None):
        self.name, self.kind = name, kind
        self.root = HERE/'private_controls'/namespace/name
        self.root.mkdir(parents=True, exist_ok=False)
        self.plan = self.root/'EXISTING_PUBLICATION_BATCH_A_PLUS1194_PROPOSAL.json'
        self.plan.write_bytes(PLAN_BYTES)
        self.helper = self.root/'audits/pr1186_2274/reconcile_existing_row.py'
        self.helper.parent.mkdir(parents=True)
        self.helper.write_bytes(HELPER)
        self.evidence = []
        for name_ in PLAN['input_pins']:
            dst = self.root/name_
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes((HERE/'inputs/evidence'/name_).read_bytes())
            self.evidence.append(dst)
        self.case = self.root/'private/existing_publication_batch_a_plus1194_action01'
        self.case.parent.mkdir(parents=True)
        self.receipt = self.root/'EXISTING_PUBLICATION_BATCH_A_PLUS1194_RECONCILIATION.json'
        if kind == 'existing_case':
            self.case.mkdir()
        if kind == 'initial_plan_drift':
            self.plan.write_bytes(PLAN_BYTES+b' ')
        if kind == 'initial_helper_drift':
            self.helper.write_bytes(HELPER+b' ')
        if kind == 'initial_evidence_drift':
            self.evidence[0].write_bytes(self.evidence[0].read_bytes()+b' ')
        self.rows = [PLAN['schema'], ['unrelated prior result','','10.1234/example','preserve all cells']]
        if seed is not None:
            self.rows.append(seed)
        self.before = copy.deepcopy(self.rows)
        self.writes = 0
        self.reads = 0
        self.registry_calls = []
        self.doi_calls = []
        self.pr_calls = []
        self.fsyncs = []
        self.lock = threading.Lock()
        self.module = {'__name__':'isolated_adversarial_review',
                       '__file__':str(self.root/'audits/existing_publication_batch_a_plus1194/append_reviewed_rows.py')}
        exec(compile(SOURCE, str(HERE/'inputs/append_reviewed_rows.py'), 'exec'), self.module)

    def mutate(self, prefix):
        if self.kind == prefix+'plan_drift':
            self.plan.write_bytes(self.plan.read_bytes()+b' ')
        if self.kind == prefix+'helper_drift':
            self.helper.write_bytes(self.helper.read_bytes()+b' ')
        if self.kind == prefix+'evidence_drift':
            self.evidence[0].write_bytes(self.evidence[0].read_bytes()+b' ')

    def fsync(self, descriptor):
        is_directory = stat.S_ISDIR(os.fstat(descriptor).st_mode)
        self.fsyncs.append('directory' if is_directory else 'file')
        if self.kind == 'directory_sync_failure' and is_directory:
            raise OSError(28, 'synthetic directory sync failure')
        if not is_directory and self.fsyncs.count('file') == 1:
            self.mutate('late_')
        if self.kind == 'intent_sync_failure' and not is_directory and self.fsyncs.count('file') == 4:
            raise OSError(28, 'synthetic intent sync failure')
        ORIGINAL_FSYNC(descriptor)

    def urlopen(self, url, timeout):
        with self.lock:
            if url.startswith('https://api.crossref.org/works/'):
                item = next((x for x in PLAN['items'] if x['registry_url'] == url), None)
                need(item is not None, 'OFFLINE unknown registry URL')
                self.registry_calls.append(item['pr'])
                message = registry_message(item)
                if self.kind == 'registry_title_drift' and item['pr'] == 1068:
                    message['title'] = ['other article']
                if self.kind == 'registry_author_drift' and item['pr'] == 1068:
                    message['author'] = [{'family':'Other'}]
                if self.kind == 'registry_date_drift' and item['pr'] == 1142:
                    message['issued'] = {'date-parts':[[2025]]}
                if self.kind == 'registry_doi_drift' and item['pr'] == 1152:
                    message['DOI'] = '10.1234/other'
                if self.kind == 'registry_type_drift' and item['pr'] == 1142:
                    message['type'] = 'journal-article'
                status = 503 if self.kind == 'registry_unavailable' and item['pr'] == 1194 else 200
                return Response(json.dumps({'status':'ok','message':message}).encode(),status)
            if url.startswith('https://doi.org/'):
                item = next((x for x in PLAN['items'] if 'https://doi.org/'+x['doi'] == url),None)
                need(item is not None, 'OFFLINE unknown DOI URL')
                self.doi_calls.append(item['pr'])
                status = 404 if self.kind == 'doi_failure' and item['pr'] == 1145 else 200
                return Response(status=status)
        raise RuntimeError('OFFLINE unknown network request')

    def check_output(self, command):
        with self.lock:
            prefix = ['gh','api','repos/AlecKriebel/Math/pulls/']
            need(len(command)==3 and command[:2] == prefix[:2] and command[2].startswith(prefix[2]), 'OFFLINE unknown command')
            pr = int(command[2].removeprefix(prefix[2]))
            need(str(pr) in MOCK_PRS, 'OFFLINE unknown PR')
            self.pr_calls.append(pr)
            result = copy.deepcopy(MOCK_PRS[str(pr)])
            if self.kind == 'pr_head_drift' and pr == 1021:
                result['head']['sha'] = '0'*40
            if self.kind == 'pr_body_drift' and pr == 1065:
                result['body'] += 'changed'
            return json.dumps(result).encode()

    def run(self, command, capture_output):
        need(capture_output is True, 'CLI capture lost')
        need(command[:3] == ['gws','sheets','spreadsheets'], 'OFFLINE unknown subprocess')
        index = command.index('--params')
        parts = command[3:index]
        params = json.loads(command[index+1])
        body = json.loads(command[command.index('--json')+1]) if '--json' in command else None
        need(params['spreadsheetId'] == BOOK, 'Wrong request workbook')
        result = self.call(parts, body)
        if isinstance(result, subprocess.CompletedProcess):
            return result
        return subprocess.CompletedProcess(command,0,json.dumps(result).encode(),b'')

    def call(self, parts, body):
        if parts == ['get']:
            sheet = {'sheetId':GID,'title':'Math Puzzles','sheetType':'GRID',
                     'gridProperties':{'rowCount':1178,'columnCount':43}}
            if self.kind == 'wrong_gid':
                sheet['sheetId'] += 1
            if self.kind == 'wrong_title':
                sheet['title'] = 'Other'
            if self.kind == 'wrong_width':
                sheet['gridProperties']['columnCount'] = 4
            return {'spreadsheetId':'wrong' if self.kind == 'wrong_book' else BOOK,
                    'sheets':[{'properties':sheet}]}
        if parts == ['values','batchGetByDataFilter']:
            need(body['dataFilters'] == [{'gridRange':{'sheetId':GID}}] and body['majorDimension'] == 'ROWS', 'Not complete numeric-gid read')
            self.reads += 1
            rows = copy.deepcopy(self.rows)
            if self.kind == 'formula_disagreement' and body['valueRenderOption'] == 'FORMULA':
                rows[1][0] = '=2+3'
            if self.reads == 3:
                self.mutate('prewrite_')
                if self.kind == 'third_read_drift':
                    rows.append(['concurrent preflight change'])
            if self.writes:
                if self.kind == 'earlier_row_drift':
                    rows[1][0] = 'earlier row changed'
                if self.kind == 'postwrite_row_drift':
                    rows[-1][-1] += 'changed'
                if self.kind == 'postwrite_duplicate':
                    rows.append([PLAN['items'][0]['doi']])
                if self.kind == 'postwrite_row_missing':
                    rows.pop()
            filter_ = {'gridRange':{'sheetId':GID}}
            if self.kind == 'response_wrong_gid':
                filter_['gridRange']['sheetId'] += 1
            return {'spreadsheetId':BOOK,'valueRanges':[{'dataFilters':[filter_],
                     'valueRange':{'range':"'Math Puzzles'!A1:"+('D' if self.kind=='truncated_extent' else 'AQ')+'1178',
                                   'majorDimension':'ROWS','values':rows}}]}
        if parts == ['batchUpdate']:
            self.writes += 1
            need(self.writes == 1, 'More than one append')
            for p in ['BEFORE_UNFORMATTED.json','BEFORE_FORMULA.json','PUBLICATION_PREFLIGHT.json','INTENT.json']:
                need((self.case/p).is_file(), 'Required prewrite capture missing')
            intent = json.loads((self.case/'INTENT.json').read_text())
            need(intent['request'] == body and intent['plan_sha256'] == hashlib.sha256(PLAN_BYTES).hexdigest()
                 and intent['helper_sha256'] == hashlib.sha256(HELPER).hexdigest(), 'Intent input binding mismatch')
            need(self.fsyncs.count('directory') >= 5, 'Prewrite directory flushes missing')
            need(sorted(self.registry_calls) == sorted(x['pr'] for x in PLAN['items']) and
                 sorted(self.doi_calls) == sorted(self.registry_calls) and sorted(self.pr_calls) == sorted(self.registry_calls),
                 'Not all8 publication preflights complete')
            need(len(body['requests']) == 1 and set(body['requests'][0]) == {'appendCells'}, 'Not one native append')
            request = body['requests'][0]['appendCells']
            need(request['sheetId'] == GID and request['fields'] == 'userEnteredValue' and len(request['rows']) == 8, 'Wrong8row write scope')
            rows = []
            for item,row in zip(PLAN['items'], request['rows']):
                cells = row['values']
                need(len(cells)==4 and all(set(c)=={'userEnteredValue'} and set(c['userEnteredValue'])=={'stringValue'} for c in cells), 'Nonliteral native cell')
                values = [c['userEnteredValue']['stringValue'] for c in cells]
                need(values == item['row'] and values[1] == '', 'Row not the reviewed four cells')
                rows.append(values)
            if self.kind == 'unrelated_concurrent_append':
                self.rows.append(['unrelated concurrent result'])
            if self.kind == 'noncontiguous_apply':
                for row in rows:
                    self.rows.extend([row,['unrelated intervening row']])
            elif self.kind != 'unknown_before_apply':
                self.rows.extend(rows)
            if self.kind in {'unknown_before_apply','unknown_after_apply'}:
                return subprocess.CompletedProcess([],1,b'',b'synthetic ambiguous write response')
            if self.kind == 'unexpected_reply':
                return {'spreadsheetId':BOOK,'replies':[{'unexpected':True}]}
            return {'spreadsheetId':BOOK,'replies':[{}]}
        raise RuntimeError('OFFLINE unknown GWS method')

    def execute(self):
        error = None
        captured = io.StringIO()
        subprocess.run, subprocess.check_output = self.run, self.check_output
        urllib.request.urlopen, os.fsync = self.urlopen, self.fsync
        try:
            with contextlib.redirect_stdout(captured):
                self.module['main']()
        except Exception as exc:
            error = {'type':type(exc).__name__,'message':str(exc)}
        finally:
            subprocess.run, subprocess.check_output = ORIGINAL_RUN, ORIGINAL_CHECK_OUTPUT
            urllib.request.urlopen, os.fsync = ORIGINAL_URLOPEN, ORIGINAL_FSYNC
        return {'name':self.name,'kind':self.kind,'writes':self.writes,'reads':self.reads,
                'error':error,'success_receipt':self.receipt.is_file(),
                'receipt':json.loads(self.receipt.read_text()) if self.receipt.is_file() else None,
                'case_exists':self.case.exists(),'intent_exists':(self.case/'INTENT.json').is_file(),
                'registry_preflights':sorted(self.registry_calls),'doi_preflights':sorted(self.doi_calls),
                'pr_preflights':sorted(self.pr_calls),'file_fsyncs':self.fsyncs.count('file'),
                'directory_fsyncs':self.fsyncs.count('directory'),
                'prior_rows_preserved':self.rows[:len(self.before)] == self.before,
                'stdout_sha256':hashlib.sha256(captured.getvalue().encode()).hexdigest()}


def scenarios():
    result = [('success','success',None),('unrelated_concurrent_append','unrelated_concurrent_append',None)]
    for item in PLAN['items']:
        result.append(('doi_'+str(item['pr']),'duplicate',[item['doi']]))
    for label, value in [
        ('canonical_pr',PLAN['items'][1]['aliases'][2]),
        ('problem_id',PLAN['items'][6]['problem_ids'][1]),
        ('arxiv_alias','https://doi.org/10.48550/arXiv.2306.16954'),
        ('encoded_journal','10.4171%252FJEMS%252F712'),
        ('zero_width_doi','10.4171/JE\u200bMS/712'),
        ('owr_original_id','OWR-1971-010'),
        ('amr_original_id','AMR-030-0034')]:
        result.append(('alias_'+label,'duplicate',[value]))
    result.append(('alias_AQ','duplicate',['']*42+[PLAN['items'][0]['doi']]))
    for kind in ['existing_case','initial_plan_drift','initial_helper_drift','initial_evidence_drift',
                 'registry_title_drift','registry_author_drift','registry_date_drift','registry_doi_drift','registry_type_drift',
                 'registry_unavailable','doi_failure','pr_head_drift','pr_body_drift','wrong_book','wrong_gid','wrong_title','wrong_width',
                 'response_wrong_gid','truncated_extent','formula_disagreement','third_read_drift',
                 'prewrite_plan_drift','prewrite_helper_drift','prewrite_evidence_drift',
                 'late_plan_drift','late_helper_drift','late_evidence_drift','directory_sync_failure','intent_sync_failure',
                 'earlier_row_drift','postwrite_row_drift','postwrite_duplicate','postwrite_row_missing',
                 'noncontiguous_apply','unexpected_reply','unknown_before_apply','unknown_after_apply']:
        result.append((kind,kind,None))
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--namespace',required=True)
    args=parser.parse_args()
    all_results=[]; unexpected=[]
    postwrite={'earlier_row_drift','postwrite_row_drift','postwrite_duplicate','postwrite_row_missing',
               'noncontiguous_apply','unexpected_reply','unknown_before_apply','unknown_after_apply'}
    for name,kind,seed in scenarios():
        world=World(args.namespace,name,kind,seed)
        value=world.execute()
        success=kind in {'success','unrelated_concurrent_append'}
        expected_writes=1 if success or kind in postwrite else 0
        expected=(value['success_receipt']==success and value['writes']==expected_writes
                  and (value['error'] is None)==success)
        value['expected_outcome']=expected
        if not expected:
            unexpected.append(name)
        if kind in {'unknown_before_apply','unknown_after_apply','directory_sync_failure','intent_sync_failure'}:
            before_writes=world.writes
            rerun=world.execute()
            value['rerun_error']=rerun['error']
            value['rerun_no_extra_write']=world.writes==before_writes
            need(value['rerun_no_extra_write'] and not rerun['success_receipt'],'Unsafe automatic retry')
        all_results.append(value)
    result={'source_sha256':hashlib.sha256(SOURCE).hexdigest(),'helper_sha256':hashlib.sha256(HELPER).hexdigest(),
            'plan_sha256':hashlib.sha256(PLAN_BYTES).hexdigest(),'offline_only':True,
            'scenario_count':len(all_results),'unexpected_scenarios':unexpected,'results':all_results}
    (HERE/('OFFLINE_RESULTS_'+args.namespace+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'scenario_count':len(all_results),'unexpected_scenarios':unexpected},sort_keys=True))


if __name__=='__main__':
    main()
