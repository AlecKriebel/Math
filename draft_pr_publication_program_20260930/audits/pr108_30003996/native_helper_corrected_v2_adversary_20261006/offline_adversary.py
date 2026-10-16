#!/usr/bin/env python3
"""Independent pure/offline V2 challenges. Never calls prepare or worker execute."""
import copy, datetime, hashlib, io, json, os, sys, unittest
from pathlib import Path
sys.dont_write_bytecode = True
O = Path(__file__).resolve().parent
F = O / 'copied_helper'
sys.path.insert(0, str(F))
import v2_guards as g
import prepare_review_bundle as helper
from bounded_process import BoundedRunner
import test_v2_guards as original_tests

MODE = 'optimized' if not __debug__ else 'normal'
RESULTS = []
POLICY = {'max_process_count': 8, 'retain_bytes_per_stream': 64, 'max_stdout_bytes': 1024,
          'max_stderr_bytes': 1024, 'deadline_seconds': 3, 'terminate_grace_seconds': 1}

def note(name, kind, **fields):
    RESULTS.append({'name': name, 'kind': kind, 'fixture_only': True, **fields})

def sheet_fixture(blank_chat=False):
    # All PID/actual flags below are synthetic shapes, never actual service evidence.
    values = ['https://doi.org/10.4171/OWR/2016/33', '' if blank_chat else 'https://example.invalid/existing-chat',
              'https://doi.org/10.5281/zenodo.123', g.K+' / '+g.CODE+' bounded fixture resolution']
    selected = "'Math Puzzles'!A42:D42"; store = {}; records = {}
    def pin(data):
        path = 'synthetic/'+str(len(store))+'.json'; store[path] = data
        return {'path':path, 'bytes':len(data), 'sha256':g.sha(data)}
    def operation(role, verb, params, response, second, body=None):
        params_text = json.dumps(params, separators=(',',':'))
        outpin = pin(g.canonical(response)); errpin = pin(b'')
        argv = ['/synthetic/gws', *verb, '--params', params_text]
        record = {'actual_process_record':True, 'fixture':False, 'PID':100+len(records), 'exit_code':0,
                  'argv':argv, 'params_bytes':len(params_text.encode()), 'params_sha256':g.sha(params_text.encode()),
                  'stdout_pin':outpin, 'response_body_pin':outpin, 'stderr_pin':errpin,
                  'UTC_start':f'2026-10-06T00:00:{second:02}Z', 'UTC_end':f'2026-10-06T00:00:{second+1:02}Z'}
        if body is not None:
            text = json.dumps(body, separators=(',',':')); argv.extend(['--json',text]); record['request_body_pin']=pin(text.encode())
        records[role] = record
    operation('metadata',['sheets','spreadsheets','get'], {'spreadsheetId':g.SHEET},
              {'spreadsheetId':g.SHEET,'sheets':[{'properties':{'sheetId':g.GID,'title':g.TITLE}}]},2)
    operation('headers',['sheets','spreadsheets','values','get'], {'spreadsheetId':g.SHEET,'range':"'Math Puzzles'!A1:D1"}, {'values':[g.COLUMNS]},4)
    operation('write',['sheets','spreadsheets','values','append'],
              {'spreadsheetId':g.SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},
              {'spreadsheetId':g.SHEET,'updates':{'updatedRange':selected,'updatedRows':1,'updatedColumns':4,'updatedCells':4}},6,
              {'majorDimension':'ROWS','values':[values]})
    for role,second in [('readback',8),('independent_readback',10)]:
        operation(role,['sheets','spreadsheets','values','get'], {'spreadsheetId':g.SHEET,'range':selected}, {'range':selected,'values':[values]},second)
    receipt = {'schema':'pr108-actual-gws-sheet-service-receipt/v2','actual_receipt':True,'fixture':False,
               'spreadsheet_id':g.SHEET,'sheet_id':g.GID,'sheet_title':g.TITLE,'columns':g.COLUMNS,
               'problem_id':30003996,'problem_code':g.CODE,'DOI':'10.5281/zenodo.123','row_index':42,
               'range':selected,'processes':records,'independent_service_authentication_required':True}
    def read(spec):
        data=store[spec['path']]
        if len(data)!=spec['bytes'] or g.sha(data)!=spec['sha256']: raise ValueError('Fixture pin changed')
        return Path(spec['path']),data
    return receipt, {'DOI':receipt['DOI'],'row_index':42,'values':values},read

class IndependentChallenges(unittest.TestCase):
    def test_blank_chat_workflow_rejection(self):
        receipt,expected,read=sheet_fixture(True)
        with self.assertRaisesRegex(ValueError, 'Exact four target row values') as error:
            g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)
        note('blank_chat_column', 'required_defect_reproduced', actual_guard_error=str(error.exception),
             all_five_synthetic_process_bodies_match_blank_row=True, no_service_called=True)

    def test_existing_chat_and_bad_custody_controls(self):
        receipt,expected,read=sheet_fixture(False)
        self.assertEqual(g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)['row_index'],42)
        cases=[]
        for role in ['metadata','headers','write','readback','independent_readback']:
            bad=copy.deepcopy(receipt); bad['processes'][role]['fixture']=True
            with self.assertRaises(ValueError):g.validate_sheet(bad,expected,'2026-10-06T00:00:01Z',read)
            cases.append(role)
        note('synthetic_sheet_shape_and_failing_custody', 'guard_success', rejected_fixture_flags=cases)

    def test_unreviewed_pythonpath_startup_runs_before_child_body(self):
        root=O/'extended_fixture_processes'/MODE; root.mkdir(parents=True,exist_ok=True)
        startup=root/'unreviewed_startup'; startup.mkdir(exist_ok=True)
        (startup/'sitecustomize.py').write_text('print("INJECTED_UNREVIEWED_STARTUP")\n')
        old=os.environ.get('PYTHONPATH'); os.environ['PYTHONPATH']=str(startup)
        try:
            runner=BoundedRunner(root,F,POLICY)
            out,err,record=runner.run([sys.executable,'-B','-c','print("FIXTURE_CHILD_BODY")'],fixture=True)
        finally:
            if old is None:os.environ.pop('PYTHONPATH',None)
            else:os.environ['PYTHONPATH']=old
        self.assertEqual(out,b'INJECTED_UNREVIEWED_STARTUP\nFIXTURE_CHILD_BODY\n')
        self.assertEqual(record['exit_code'],0); self.assertIsNone(record['termination_reason'])
        note('pythonpath_sitecustomize', 'required_defect_reproduced', actual_child_PID=record['PID'],
             UTC_start=record['UTC_start'],UTC_end=record['UTC_end'],exit_code=record['exit_code'],
             stdout_bytes=len(out),stdout_sha256=g.sha(out),stderr_bytes=len(err),stderr_sha256=g.sha(err),
             recorded_controlled_environment=record['controlled_environment'], startup_file_sha256=g.sha((startup/'sitecustomize.py').read_bytes()),
             native_worker_or_assess_called=False)

    def test_policy_projection_cross_product(self):
        cases=0
        for decision in [None,'candidate','defer','exclude','repair']:
            for resolution in [None,'already_solved']:
                for stale in [False,True]:
                    for holds in [[],['fixture_hold']]:
                        for status in [None,'queued','claimed_solved','ready','exhausted']:
                            for turns in [0,2,5]:
                                row={'present':True,'local_status':'queued','turns_used':0,'holds':holds,'review_hash':'current'}
                                assessment={'decision':decision,'resolution':resolution,'review_hash':'stale' if stale else 'current'}
                                state={'turns_used':turns};
                                if status is not None:state['status']=status
                                default='queued' if decision=='candidate' else 'deferred' if decision in ['defer','exclude'] else 'unreviewed'
                                if default=='queued' and holds:default='unreviewed'
                                if resolution=='already_solved' and not stale:default='already_solved'
                                projected=state.get('status',default)
                                self.assertEqual(g.native_status_turns(row,state,{'turn_limit':5},assessment),(projected,turns))
                                self.assertEqual(g.expected_eligible(row,state,{'turn_limit':5},assessment),not holds and projected in ['queued','unreviewed','ready'] and turns<5)
                                cases+=1
        note('native_policy_projection_cross_product','guard_success',case_count=cases,oracle='Independently transcribed pinned native queue.py: default/local status and turns predicate; no native function invoked')

    def test_capacity_real_baseline_illustrative_plan_and_missing_reserve(self):
        pins=json.loads((O/'NATIVE_BASELINE_PINS.json').read_text())
        pins=[{k:v for k,v in pin.items() if k!='revision'} for pin in pins]
        p=dict(original_tests.CAPACITY); gates={role:{'bytes':65536} for role in g.GATE_ROLES}
        result=g.capacity_inventory(pins,[],gates,{},p,original_tests.POLICY)
        self.assertGreater(result['required_free_bytes'],sum(x['max_bytes'] for x in result['entries']))
        bad=dict(p);bad['future_commit_overhead_bytes']=1
        with self.assertRaises(ValueError):g.capacity_inventory(pins,[],gates,{},bad,original_tests.POLICY)
        note('real_native_capacity_illustrative_plan','guard_success', materialized_bytes=result['max_materialized_bytes'],
             required_free_bytes=result['required_free_bytes'],entry_count=len(result['entries']),
             qualification='Illustrative baseline-only conservative plan under standard fixture policies and maximally sized gates. Omits future non-gate inputs and final package. This is not a mathematical minimum over all allowed policies or real configuration/workload certification.')

if __name__=='__main__':
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(original_tests),unittest.defaultTestLoader.loadTestsFromTestCase(IndependentChallenges)])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    output={'schema':'pr108-corrected-v2-independent-offline-fixtures/v1','actual_fixture_operator_PID':os.getpid(),
            'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,
            'tests_run':result.testsRun,'failure_count':len(result.failures),'error_count':len(result.errors),
            'successful':result.wasSuccessful(),'challenges':RESULTS,'native_prepare_assess_export_execution_count':0,
            'actual_service_operation_count':0,'no_real_configuration_certified':True}
    (O/('RESULTS_'+MODE.upper()+'.json')).write_bytes(g.canonical(output))
    print(json.dumps({'mode':MODE,'tests':result.testsRun,'successful':result.wasSuccessful(),'fixture_operator_PID':os.getpid()}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
