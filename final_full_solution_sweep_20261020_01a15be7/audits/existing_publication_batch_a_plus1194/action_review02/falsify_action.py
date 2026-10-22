"""Fresh whole-action adversary with no network or subprocess access.

Provider modules are replaced before either reviewed source is imported/executed.
The exact runner and helper execute with fixture-only paths. All controls are
reviewer-authored; no previous review's executable code is loaded or run.
"""
from pathlib import Path
import builtins
import concurrent.futures
import contextlib
import copy
import datetime
import hashlib
import io
import json
import os
import stat
import sys
import types
import urllib.parse

HERE = Path(__file__).resolve().parent
SOURCE = (HERE/'inputs/runner.py').read_bytes()
HELPER = (HERE/'inputs/helper.py').read_bytes()
PLAN_BYTES = (HERE/'inputs/plan.json').read_bytes()
PLAN = json.loads(PLAN_BYTES)
LEDGER = json.loads((HERE/'private_observations/ledger183.json').read_bytes())
BEFORE_ROWS = LEDGER['valueRanges'][0]['valueRange']['values']
PRS = json.loads((HERE/'private_observations/pr_bodies.json').read_bytes())
BOOK = PLAN['spreadsheet_id']
GID = PLAN['sheet_gid']
ITEMS = PLAN['items']
ROWS = [x['row'] for x in ITEMS]
MODE = 'double_optimized' if sys.flags.optimize == 2 else ('optimized' if sys.flags.optimize else 'normal')
REAL_THREADS = '--threads' in sys.argv
if REAL_THREADS:
    MODE += '_threads'


def check(ok, message):
    if not ok:
        raise RuntimeError('HARNESS: '+message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def response(value, status=200, url='https://fixture.invalid/'):
    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return json.dumps(value).encode()
    result = Response()
    result.status = status
    result.url = url
    return result


def registry_message(item):
    p = item['registry_projection']
    return {'DOI': p['doi'], 'title': p['title'], 'author': p['authors'],
        'type': p['type'], 'publisher': p['publisher'], 'container-title': p['container_title'],
        'volume': p['volume'], 'issue': p['issue'], 'page': p['page'],
        'article-number': p['article_number'], 'issued': {'date-parts': p['issued']},
        'published-online': {'date-parts': p['published_online']}}


class SerialExecutor:
    """Deterministic delivery of the production pool's same map contract."""
    def __init__(self, max_workers):
        check(max_workers == 4, 'Unexpected pool extent')
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def map(self, fn, items):
        return map(fn, items)


class Fixture:
    def __init__(self, number, spec):
        self.spec = spec
        self.root = HERE/'private_controls'/MODE/(str(number).zfill(3)+'_'+spec['name'])
        self.root.mkdir(parents=True, exist_ok=False)
        self.plan_path = self.root/'EXISTING_PUBLICATION_BATCH_A_PLUS1194_PROPOSAL.json'
        self.plan_path.write_bytes(PLAN_BYTES)
        self.helper_path = self.root/'audits/pr1186_2274/reconcile_existing_row.py'
        self.helper_path.parent.mkdir(parents=True)
        self.helper_path.write_bytes(HELPER)
        self.case = self.root/'private/existing_publication_batch_a_plus1194_action01'
        self.case.parent.mkdir(parents=True)
        self.receipt = self.root/'EXISTING_PUBLICATION_BATCH_A_PLUS1194_RECONCILIATION.json'
        for rel in PLAN['input_pins']:
            dest = self.root/rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((HERE/'inputs/evidence'/rel).read_bytes())
        self.rows = copy.deepcopy(BEFORE_ROWS)
        self.read_calls = 0
        self.metadata_calls = 0
        self.write_calls = 0
        self.external_calls = 0
        self.provider_calls = []
        self.command_calls = []
        self.events = []
        self.fd_paths = {}
        self.injected_late = False
        self.intent_verified_before_write = False
        self.namespace_sync_before_write = False
        self.live_rows = []
        if 'seed' in spec:
            row = ['Fixture identity lead', '', '', '']
            column = spec.get('column', 3)
            row.extend(['']*max(0, column+1-len(row)))
            row[column] = spec['seed']
            self.rows.append(row)
        self.old_rows = copy.deepcopy(self.rows)
        if spec.get('fault') == 'case_already_exists':
            self.case.mkdir()
        if spec.get('fault') in ['initial_plan', 'initial_helper', 'initial_evidence']:
            self.mutate(spec['fault'][8:])
        if spec.get('fault') == 'symlink_evidence':
            target = self.root/spec['input']
            other = target.with_name(target.name+'.real')
            target.rename(other)
            target.symlink_to(other)
        self.override_plan_sha = None
        if spec.get('fault', '').startswith('structure_'):
            p = copy.deepcopy(PLAN)
            fault = spec['fault']
            if fault == 'structure_original_alias':
                item = p['items'][spec['item']]
                item['aliases'].remove(spec['identity'])
            elif fault == 'structure_original_list':
                p['items'][0]['original_problem_ids'] = []
            elif fault == 'structure_order':
                p['items'].reverse()
            elif fault == 'structure_duplicate_doi':
                p['items'][1]['doi'] = p['items'][0]['doi']
            elif fault == 'structure_nonblank_b':
                p['items'][0]['row'][1] = 'An unreviewed chat address'
            elif fault == 'structure_literal_type':
                p['items'][0]['row'][0] = 30000977
            elif fault == 'structure_missing_pr_alias':
                p['items'][0]['aliases'].remove('https://github.com/AlecKriebel/Math/pull/1021')
            elif fault == 'structure_wrong_target':
                p['sheet_gid'] = 0
            else:
                raise RuntimeError('Unknown structural control')
            data = json.dumps(p).encode()
            self.plan_path.write_bytes(data)
            self.override_plan_sha = sha(data)

    def mutate(self, which):
        target = self.plan_path if which == 'plan' else (self.helper_path if which == 'helper' else self.root/self.spec['input'])
        target.write_bytes(target.read_bytes()+b'\n')
        self.events.append('injected_'+which)

    def os_open(self, path, flags, *args, **kwargs):
        path = Path(path)
        check(path.is_relative_to(self.root), 'Directory access escaped fixture')
        fd = os.open(path, flags, *args, **kwargs)
        self.fd_paths[fd] = path
        return fd

    def os_close(self, fd):
        self.fd_paths.pop(fd, None)
        return os.close(fd)

    def fsync(self, fd):
        isdir = stat.S_ISDIR(os.fstat(fd).st_mode)
        where = self.fd_paths.get(fd)
        self.events.append('dirsync:'+str(where.relative_to(self.root)) if isdir else 'filesync')
        fault = self.spec.get('fault')
        if fault == 'directory_sync_failure' and isdir:
            raise OSError('Injected fixture-only directory sync failure')
        os.fsync(fd)
        if isdir and where == self.case and (self.case/'INTENT.json').exists() and not self.injected_late:
            self.injected_late = True
            if fault in ['late_plan', 'late_helper', 'late_evidence']:
                self.mutate(fault[5:])

    def urlopen(self, url, timeout):
        self.external_calls += 1
        self.provider_calls.append(url)
        check(timeout == 45, 'Wrong provider timeout')
        item = next((x for x in ITEMS if url in [x['registry_url'], 'https://doi.org/'+x['doi']]), None)
        check(item is not None, 'Unexpected URL (including any unrequested upload/Zenodo call): '+url)
        targeted = item['pr'] == self.spec.get('pr')
        fault = self.spec.get('fault') if targeted else None
        if url == item['registry_url']:
            m = copy.deepcopy(registry_message(item))
            if fault == 'registry_projection':
                key = self.spec['field']
                if key in ['title', 'author', 'container-title']:
                    m[key] = ['Injected wrong value'] if key != 'author' else [{'given': 'Wrong', 'family': 'Author'}]
                elif key in ['issued', 'published-online']:
                    m[key] = {'date-parts': [[1900]]}
                else:
                    m[key] = 'Injected wrong value'
            if self.spec.get('fault') == 'neutral_registry_extra':
                m['indexed'] = {'date-time': '2099-01-01'}
                m['author'].append({})
            status = 503 if fault == 'registry_http' else 200
            state = 'error' if fault == 'registry_status' else 'ok'
            return response({'status': state, 'message': m}, status, url)
        return response({}, 503 if fault == 'doi_http' else 200, 'https://publisher.invalid/'+str(item['pr']))

    def check_output(self, command):
        self.external_calls += 1
        self.command_calls.append(command)
        check(command[:3] == ['gh', 'api', 'repos/AlecKriebel/Math/pulls/'+command[2].rsplit('/',1)[-1]] and len(command)==3,
              'Unexpected subprocess API')
        prnum = int(command[2].rsplit('/', 1)[-1])
        check(prnum in {x['pr'] for x in ITEMS}, 'Unexpected PR')
        cached = PRS[str(prnum)]
        live = {'head': {'sha': cached['headRefOid']}, 'body': cached['body'],
                'state': cached['state'].lower(), 'merged': cached['mergedAt'] is not None}
        if prnum == self.spec.get('pr'):
            if self.spec.get('fault') == 'pr_head':
                live['head']['sha'] = '0'*40
            if self.spec.get('fault') == 'pr_body':
                live['body'] = (live['body'] or '')+'\nChanged'
        return json.dumps(live).encode()

    def run(self, command, capture_output):
        self.external_calls += 1
        self.command_calls.append(command)
        check(capture_output is True and command[:3] == ['gws','sheets','spreadsheets'], 'Unexpected executable')
        pi = command.index('--params')
        parts = command[3:pi]
        params = json.loads(command[pi+1])
        check(params['spreadsheetId'] == BOOK, 'Wrong request workbook')
        body = json.loads(command[command.index('--json')+1]) if '--json' in command else None
        fault = self.spec.get('fault')
        if parts == ['get']:
            self.metadata_calls += 1
            sheet = {'sheetId':GID,'title':'Math Puzzles','sheetType':'GRID',
                     'gridProperties':{'columnCount':43,'rowCount':1178}}
            if fault == 'wrong_gid':sheet['sheetId'] = 0
            if fault == 'wrong_title':sheet['title'] = 'Papers'
            if fault == 'wrong_sheet_type':sheet['sheetType'] = 'OBJECT'
            if fault == 'wrong_columns':sheet['gridProperties']['columnCount'] = 42
            if fault == 'metadata_drift' and self.metadata_calls == 2:sheet['gridProperties']['rowCount'] = 1179
            answer = {'spreadsheetId': 'wrong-book' if fault == 'wrong_book' else BOOK,
                      'sheets':[{'properties':sheet}]}
            if fault == 'duplicate_gid':answer['sheets'].append({'properties':copy.deepcopy(sheet)})
        elif parts == ['values','batchGetByDataFilter']:
            self.read_calls += 1
            check(body['dataFilters'] == [{'gridRange':{'sheetId':GID}}] and body['majorDimension']=='ROWS', 'Wrong full numeric filter')
            check(body['valueRenderOption'] in ['FORMULA','UNFORMATTED_VALUE'], 'Wrong read mode')
            rows = copy.deepcopy(self.rows)
            if fault == 'wrong_header':rows[0][0] = 'Changed header'
            if fault == 'too_many_columns':rows[1].extend(['']*(44-len(rows[1])))
            if fault == 'formula_drift' and self.read_calls == 2:rows[1][0] = '=1'
            if fault == 'final_preflight_drift' and self.read_calls == 3:rows.append(['New concurrent row'])
            filt = [{'gridRange':{'sheetId':0}}] if fault == 'wrong_read_filter' else body['dataFilters']
            extent = "'Math Puzzles'!A1:AQ1178"
            if fault == 'truncated_read':extent = "'Math Puzzles'!A1:D1178"
            dimension = 'COLUMNS' if fault == 'wrong_read_dimension' else 'ROWS'
            answer = {'spreadsheetId':BOOK,'valueRanges':[{'dataFilters':filt,
                'valueRange':{'range':extent,'majorDimension':dimension,'values':rows}}]}
        elif parts == ['batchUpdate']:
            self.write_calls += 1
            check(self.write_calls == 1, 'More than one native write')
            expected = {'requests':[{'appendCells':{'sheetId':GID,
                'rows':[{'values':[{'userEnteredValue':{'stringValue':cell}} for cell in row]} for row in ROWS],
                'fields':'userEnteredValue'}}]}
            check(body == expected, 'Mutation is not exact single eight-row/four-literal-string append')
            required = ['BEFORE_UNFORMATTED.json','BEFORE_FORMULA.json','PUBLICATION_PREFLIGHT.json','INTENT.json']
            check(all((self.case/x).is_file() for x in required), 'Missing pre-write capture')
            intent = json.loads((self.case/'INTENT.json').read_bytes())
            self.intent_verified_before_write = (intent['request']==body and intent['plan_sha256']==sha(PLAN_BYTES)
                and intent['helper_sha256']==sha(HELPER) and intent['previous_rows']==len(self.old_rows))
            check(self.intent_verified_before_write, 'Intent not bound to exact inputs/request')
            self.namespace_sync_before_write = ('dirsync:private' in self.events and
                self.events.count('dirsync:private/existing_publication_batch_a_plus1194_action01') >= 4)
            check(self.namespace_sync_before_write, 'Expected case-parent and snapshot/intent directory fsyncs missing')
            self.events.append('native_write')
            if fault == 'write_exception':raise TimeoutError('Synthetic ambiguous fixture transport')
            if fault != 'unknown_before_apply':
                if fault == 'concurrent_append_before':self.rows.append(['Concurrent unrelated result'])
                added = copy.deepcopy(ROWS)
                if fault == 'post_missing':added.pop()
                if fault == 'post_changed':added[0][3] += ' [changed]'
                if fault == 'post_reverse':added.reverse()
                if fault == 'post_interleaved':added.insert(3,['Unrelated row interleaved after service write'])
                self.rows.extend(added)
                if fault == 'post_exact_duplicate':self.rows.append(copy.deepcopy(ROWS[0]))
                if fault == 'post_alias_duplicate':self.rows.append(['Duplicate evidence', '', '', ITEMS[0]['doi']])
                if fault == 'post_prior_change':self.rows[1][3] += ' [concurrent edit]'
                if fault == 'concurrent_append_after':self.rows.append(['Concurrent unrelated result'])
            if fault in ['unknown_before_apply','unknown_after_apply']:
                return types.SimpleNamespace(returncode=1, stdout=b'', stderr=b'Synthetic ambiguous CLI failure')
            if fault == 'write_bad_json':
                return types.SimpleNamespace(returncode=0,stdout=b'not JSON',stderr=b'')
            answer = {'spreadsheetId':BOOK,'replies':[{}]}
            if fault == 'write_bad_book':answer['spreadsheetId'] = 'wrong-book'
            if fault == 'write_bad_replies':answer['replies'] = []
        else:
            raise RuntimeError('Unexpected GWS operation: '+str(parts))
        return types.SimpleNamespace(returncode=0,stdout=json.dumps(answer).encode(),stderr=b'')

    def execute(self):
        fake_urllib = types.SimpleNamespace(parse=urllib.parse, request=types.SimpleNamespace(urlopen=self.urlopen))
        fake_subprocess = types.SimpleNamespace(run=self.run, check_output=self.check_output)
        fake_os = types.SimpleNamespace(open=self.os_open,close=self.os_close,fsync=self.fsync,O_RDONLY=os.O_RDONLY)
        executor = concurrent.futures.ThreadPoolExecutor if REAL_THREADS else SerialExecutor
        fake_concurrent = types.SimpleNamespace(futures=types.SimpleNamespace(ThreadPoolExecutor=executor))
        actual_import = builtins.__import__
        def import_safe(name, globals=None, locals=None, fromlist=(), level=0):
            if name == 'subprocess':return fake_subprocess
            if name == 'os':return fake_os
            if name in ['urllib.parse','urllib.request']:return fake_urllib
            if name == 'concurrent.futures':return fake_concurrent
            return actual_import(name,globals,locals,fromlist,level)
        safe_builtins = dict(vars(builtins))
        safe_builtins['__import__'] = import_safe
        def exec_safe(code, globals, locals=None):
            globals['__builtins__'] = safe_builtins
            return builtins.exec(code,globals,globals if locals is None else locals)
        safe_builtins['exec'] = exec_safe
        ns = {'__name__':'_reviewed_action_inert_import','__file__':str(self.root/'audits/existing_publication_batch_a_plus1194/append_reviewed_rows.py'),
              '__builtins__':safe_builtins}
        builtins.exec(compile(SOURCE,'exact_reviewed_runner','exec'),ns)
        check(ns['ROOT']==self.root, 'Wrong fixture root')
        if self.override_plan_sha is not None:ns['PLAN_SHA'] = self.override_plan_sha
        output = io.StringIO()
        error = None
        with contextlib.redirect_stdout(output):
            try:ns['main']()
            except Exception as exc:error = type(exc).__name__+': '+str(exc)
        return error


def specs():
    out = [{'name':'baseline','expect':'success'},
           {'name':'neutral_registry_extra','fault':'neutral_registry_extra','expect':'success'},
           {'name':'concurrent_append_before','fault':'concurrent_append_before','expect':'success'},
           {'name':'concurrent_append_after','fault':'concurrent_append_after','expect':'success'}]
    # Deliberately choose every available alias, preserving all43-column coverage.
    for i,item in enumerate(ITEMS):
        for j,alias in enumerate(item['aliases']):
            out.append({'name':'duplicate_'+str(item['pr'])+'_'+str(j),'seed':alias,
                        'column':42 if j%2 else 3,'expect':'block'})
        for j,identity in enumerate(item['original_problem_ids']):
            out.append({'name':'original_encoded_'+str(item['pr'])+'_'+str(j),
                'seed':urllib.parse.quote(urllib.parse.quote(identity,safe=''),safe='').replace('-', '%252D'),
                'column':42,'expect':'block'})
            out.append({'name':'required_original_'+str(item['pr'])+'_'+str(j),
                'fault':'structure_original_alias','item':i,'identity':identity,'expect':'block'})
        author = item['registry_projection']['authors'][0]
        name = ' '.join(author.get(k,'') for k in ['given','family','name']).strip()
        out.append({'name':'alternate_doi_named_'+str(item['pr']),
                    'seed':'https://doi.org/10.9999/an.alternate '+name,'column':42,'expect':'block'})
        for fault in ['registry_http','registry_status','doi_http','pr_head','pr_body']:
            out.append({'name':fault+'_'+str(item['pr']),'fault':fault,'pr':item['pr'],'expect':'block'})
    # All fields in the exact bibliographic projection have independent faults.
    for field in ['DOI','title','author','type','publisher','container-title','volume','issue','page','article-number','issued','published-online']:
        out.append({'name':'registry_'+field.replace('-','_'),'fault':'registry_projection','field':field,'pr':1021,'expect':'block'})
    for fault in ['wrong_gid','wrong_book','wrong_title','wrong_sheet_type','wrong_columns','duplicate_gid',
                  'metadata_drift','wrong_header','too_many_columns','formula_drift','final_preflight_drift',
                  'wrong_read_filter','truncated_read','wrong_read_dimension','case_already_exists',
                  'initial_plan','initial_helper','late_plan','late_helper','directory_sync_failure',
                  'structure_original_list','structure_order','structure_duplicate_doi','structure_nonblank_b',
                  'structure_literal_type','structure_missing_pr_alias','structure_wrong_target']:
        out.append({'name':fault,'fault':fault,'expect':'block'})
    for index,rel in enumerate(PLAN['input_pins']):
        for phase in ['initial_evidence','late_evidence','symlink_evidence']:
            out.append({'name':phase+'_'+str(index),'fault':phase,'input':rel,'expect':'block'})
    for fault in ['unknown_before_apply','unknown_after_apply','write_exception','write_bad_json','write_bad_book',
                  'write_bad_replies','post_missing','post_changed','post_reverse','post_interleaved',
                  'post_exact_duplicate','post_alias_duplicate','post_prior_change']:
        out.append({'name':fault,'fault':fault,'expect':'post_block'})
    if REAL_THREADS:
        selected = {'baseline','neutral_registry_extra','registry_title','pr_head_1194',
                    'pr_body_1021','unknown_after_apply','post_alias_duplicate'}
        return [x for x in out if x['name'] in selected]
    return out


def main():
    result_rows = []
    for n,spec in enumerate(specs(),1):
        f = Fixture(n,spec)
        error = f.execute()
        receipt = json.loads(f.receipt.read_bytes()) if f.receipt.exists() else None
        result = {'name':spec['name'],'expect':spec['expect'],'writes':f.write_calls,
                  'error':error,'success_receipt':receipt is not None,'read_calls':f.read_calls,
                  'metadata_calls':f.metadata_calls,'stubbed_calls':f.external_calls,
                  'real_provider_calls':0,'real_subprocesses':0,
                  'structural_control_overrides_fixture_plan_pin':f.override_plan_sha is not None}
        if spec['expect']=='success':
            check(error is None and f.write_calls==1 and receipt is not None,'Positive control failed: '+str(result))
            check(receipt['new_publications']==0 and receipt['new_rows']==8 and len(receipt['items'])==8,'Wrong successful accounting')
            check(f.intent_verified_before_write and f.namespace_sync_before_write,'Missing positive intent/sync evidence')
            check(f.rows[:len(f.old_rows)]==f.old_rows,'Successful prefix not preserved')
            numbers = [x['row'] for x in receipt['items']]
            check(numbers == list(range(numbers[0],numbers[0]+8)),'Successful batch not contiguous')
            result['exact_four_literal_cells_each'] = True
            result['blank_b_each'] = True
            result['intent_precedes_write'] = True
            result['directory_sync_precedes_write'] = True
            result['row_numbers'] = numbers
        elif spec['expect']=='block':
            check(error is not None and f.write_calls==0 and receipt is None,'Pre-write fault escaped: '+str(result))
        else:
            check(error is not None and f.write_calls==1 and receipt is None,'Post-write fault escaped: '+str(result))
            check((f.case/'INTENT.json').exists(),'Lost unknown-outcome intent')
        # Every case that created the guard is independently tried a second time.
        if f.case.exists():
            old_calls,old_writes = f.external_calls,f.write_calls
            retry_error = f.execute()
            check(retry_error and f.external_calls==old_calls and f.write_calls==old_writes,
                  'Rerun contacted services or repeated mutation: '+spec['name'])
            result['guarded_rerun_zero_calls'] = True
        if f.write_calls:
            (f.root/'events.json').write_text(json.dumps(f.events,indent=2)+'\n')
        result_rows.append(result)
    output = {'mode':MODE,'scenarios':len(result_rows),'all_expectations_passed':True,
        'real_provider_calls':0,'real_subprocesses':0,'rows':result_rows,
        'simulation_order':('actual standard-library four-worker ThreadPoolExecutor; services still fully stubbed' if REAL_THREADS else
            'deterministic serial executor preserves same production map order; does not model thread scheduling'),
        'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (HERE/('RESULTS_'+MODE+'.json')).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='rows'},indent=2))


if __name__=='__main__':main()
