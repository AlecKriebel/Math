"""Offline synthetic guard fixtures. Never prepare/native-assess/export/service calls."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import copy,csv,hashlib,io,json,os,tempfile,unittest,zipfile
import v3_guards as g
import prepare_review_bundle as helper
from bounded_process import BoundedRunner,validate_policy as process_policy
from native_assess_worker import validate_policy as worker_policy
D=Path(__file__).resolve().parent
FIXTURE_ONLY=True
POLICY={'max_process_count':8,'retain_bytes_per_stream':64,'max_stdout_bytes':4096,
        'max_stderr_bytes':1024,'deadline_seconds':2,'terminate_grace_seconds':1}
CAPACITY={'headroom_bytes':32*1024*1024,'max_artifact_count':512,'max_materialized_bytes':160*1024*1024,
    'wrapper_bytes_cap':65536,'receipt_json_bytes_cap':128*1024,'per_native_growth_bytes':512*1024,'max_package_files':64,
    'future_commit_overhead_bytes':8*1024*1024,'runtime_overhead_bytes':8*1024*1024}
def fixture_environment_policy():
    # Metadata-shaped placeholders are never used for actual Git/GH commands.
    return {'schema':'pr108-reviewed-process-environment/v3','ambient_inheritance':False,
        'python':{'argv_prefix':g.PYTHON_PREFIX,'environment':dict(g.COMMON_ENV)},
        'initial_launcher':{'program':'launch_review_bundle.sh','shell':'/bin/sh','environment':dict(g.COMMON_ENV)},
        'git':{'environment':dict(g.GIT_ENV),'repository_directory':str(D/'unused_git_repo'),'repository_location_pins':[],'repository_config_pins':[{'path':str(D/'unused_git_config/config'),'bytes':0,'sha256':'0'*64}]},
        'gh':{'environment':{**g.GH_ENV_FIXED,'GH_CONFIG_DIR':str(D/'unused_gh_config')},
            'config_pins':[{'path':str(D/'unused_gh_config/hosts.yml'),'bytes':0,'sha256':'0'*64}],'expected_login':'synthetic-fixture'},
        'credentials_in_environment_or_receipts':False}
ENV_POLICY=fixture_environment_policy()

def fixture_row(identity,eligible=True,status='queued',holds=None,turns=0,present=True):
    return {'id':identity,'rank':1,'holds':holds or [],'reasons':[],'local_status':status,'turns_used':turns,
            'eligible':eligible,'review_hash':'a'*64,'present':present,'impact':4.0}

class CSVFixtures(unittest.TestCase):
    def csv_bytes(self,sep,newline='\n',last_newline=True,target_multiline=False):
        stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator=newline)
        w.writerow(['id','title','holds','reasons']);w.writerow(['other-1','left'+sep+'tail','',''])
        w.writerow([g.K,'old'+('\r\nmultiline' if target_multiline else ''),'',''])
        w.writerow(['other-2','right','',''])
        data=stream.getvalue().encode()
        return data if last_newline else data[:-len(newline)]
    def assert_spans(self,data):
        _,old=g.csv_records(data);target={'id':g.K,'title':'new','holds':[],'reasons':[]}
        newdata=g.csv_overlay(data,target);_,new=g.csv_records(newdata)
        self.assertEqual(len(old),len(new));self.assertEqual([x['fields'][0] for x in old],[x['fields'][0] for x in new])
        self.assertEqual([x['bytes'] for i,x in enumerate(old) if i!=2],[x['bytes'] for i,x in enumerate(new) if i!=2])
        self.assertEqual(new[2]['fields'][1],'new')
    def test_all_eight_nonphysical_separators(self):
        for sep in ['\v','\f','\x1c','\x1d','\x1e','\x85','\u2028','\u2029']:
            with self.subTest(separator=repr(sep)):self.assert_spans(self.csv_bytes(sep))
    def test_cr_lf_crlf_and_quoted_multiline(self):
        for ending in ['\r','\n','\r\n']:
            for eof in [True,False]:
                with self.subTest(ending=repr(ending),eof=eof):self.assert_spans(self.csv_bytes('\u2028',ending,eof,True))
    def test_target_at_eof_without_newline(self):
        data=b'id,title,holds,reasons\r\nother,untouched,,\r\n30003996,old,,'
        out=g.csv_overlay(data,{'id':g.K,'title':'new','holds':[],'reasons':[]})
        self.assertTrue(out.endswith(b'30003996,new,,'));self.assertFalse(out.endswith(b'\n'))
        self.assertEqual(out.split(b'30003996')[0],data.split(b'30003996')[0])
    def test_duplicate_and_bad_quote_rejected(self):
        with self.assertRaises(ValueError):g.csv_overlay(b'id,title,holds,reasons\n30003996,x,,\n30003996,y,,\n',{})
        with self.assertRaises(csv.Error):g.csv_records(b'id,title\n"unclosed,x\n')
    def test_new_target_quoted_multiline_at_eof(self):
        data=b'id,title,holds,reasons\rother,untouched,,\r30003996,old,,'
        title='new\rquoted\nmultiple\r\nlines'
        out=g.csv_overlay(data,{'id':g.K,'title':title,'holds':[],'reasons':[]})
        _,records=g.csv_records(out);self.assertEqual(records[-1]['fields'][1],title)
        self.assertEqual(records[1]['bytes'],b'other,untouched,,\r');self.assertFalse(out.endswith(b'\n'))

class BindingFixtures(unittest.TestCase):
    def test_templates_and_missing_roles_reject(self):
        cfg={'schema':'pr108-native-publication-integration-config/v3','template_only':True,
            'commissioned_after_independent_review':False,'execution_inputs':None,'gates':{}}
        with self.assertRaises(ValueError):g.validate_thin_config(cfg)
        cfg['template_only']=False;cfg['commissioned_after_independent_review']=True
        with self.assertRaises(ValueError):g.validate_thin_config(cfg)
    def test_all_effective_fields_and_canonical_bytes_required(self):
        doc={'schema':'pr108-immutable-execution-inputs/v3','template_only':False,
            'effective':{x:None for x in g.CHOICES},'program_files':[{'path':x} for x in g.PROGRAMS],'input_files':[]}
        doc['effective'].update(execution_mode='review_bundle_only',scoped_rank_interpretation='preserve_baseline_labels_and_positions_not_global_rerank')
        g.validate_execution_manifest(doc,g.canonical(doc))
        for mutation in ['extra_choice','campaign_note']:
            wrong=copy.deepcopy(doc)
            if mutation=='campaign_note':del wrong['effective'][mutation]
            else:wrong['effective'][mutation]='changed'
            with self.assertRaises(ValueError):g.validate_execution_manifest(wrong,g.canonical(wrong))
        with self.assertRaises(ValueError):g.validate_execution_manifest(doc,json.dumps(doc).encode())
    def test_duplicate_json_keys_reject(self):
        with self.assertRaises(ValueError):g.loads('{"x":1,"x":2}')
    def test_pinned_capture_once_and_no_unused_inputs(self):
        with tempfile.TemporaryDirectory(dir=D) as folder:
            root=Path(folder);path=root/'prior.json';data=b'{}\n';path.write_bytes(data)
            pin={'path':'prior.json','bytes':len(data),'sha256':g.sha(data)}
            obj=g.ReviewedInputs({'input_files':[pin]},root,root)
            self.assertEqual(obj.read(pin)[1],data);path.write_bytes(b'{"late":true}')
            self.assertEqual(obj.read(pin)[1],data);obj.finish()
            altered={**pin,'sha256':'0'*64}
            with self.assertRaises(ValueError):obj.read(altered)
            unused=g.ReviewedInputs({'input_files':[pin]},root,root)
            with self.assertRaises(ValueError):unused.finish()
    def test_nested_anchors(self):
        self.assertEqual(helper.D,D);self.assertEqual(helper.A,D.parent.parent)
        self.assertEqual(helper.C,helper.A.parents[2]);self.assertEqual(helper.V1,D.parent)
    def test_gate_exact_input_and_entire_program_binding(self):
        # Synthetic dictionaries exercise correspondence; they authenticate no review.
        programs={x:'b'*64 for x in g.PROGRAMS};base='a'*40
        gate={'schema':'pr108-publication-root-gate/v3','role':'pre_execution_adversary','PR':108,'problem_id':30003996,
            'main_parent':base,'original_head':helper.HEAD,'review_hash':helper.REVIEW,'statement_hash':helper.STATEMENT,
            'effective_proof_sha256':helper.PROOF,'package_manifest_sha256':'c'*64,'execution_inputs_sha256':'d'*64,
            'actual_root_review':True,'clearance':True,'new_central_proof_search_turns':0,'original_budget':'2/5',
            'exact_claim':'Synthetic binding fixture only','checked_artifacts':[{'path':'synthetic'}],
            'UTC':'2026-10-06T00:00:00Z','native_scope_and_invariants_checked':True,'reviewed_program_sha256':programs,
            'scoped_rank_interpretation':'preserve_baseline_labels_and_positions_not_global_rerank'}
        helper.validate_gate(gate,'pre_execution_adversary','c'*64,'d'*64,programs,base)
        for field in ['main_parent','execution_inputs_sha256','reviewed_program_sha256','scoped_rank_interpretation']:
            wrong=copy.deepcopy(gate);wrong[field]='changed'
            with self.assertRaises(ValueError):helper.validate_gate(wrong,'pre_execution_adversary','c'*64,'d'*64,programs,base)

class OriginalFixtures(unittest.TestCase):
    def data(self):
        files=[{'relative_path':name,'path':g.N+name,'Git_mode':'100644','git_blob_SHA1':hashlib.sha1(name.encode()).hexdigest()} for name in sorted(g.ORIGINAL_NAMES)]
        auth={'source_head':g.HEAD,'incoming_body_count':15,'original_author_effort':'2/5','literal_status':'claimed_solved','files':files}
        tree={x['path']:{'mode':'100644','blob':x['git_blob_SHA1']} for x in files};return auth,tree
    def test_exact_names_maps_and_modes(self):
        auth,tree=self.data();self.assertEqual(set(g.validate_original_map(auth,tree)),g.ORIGINAL_NAMES)
        for kind in ['swap','mode','head','missing']:
            bad=copy.deepcopy(auth)
            if kind=='swap':
                a=next(x for x in bad['files'] if x['relative_path']=='README.md');b=next(x for x in bad['files'] if x['relative_path']=='RESEARCH_LOG.md')
                a['relative_path'],b['relative_path']=b['relative_path'],a['relative_path']
            elif kind=='mode':bad['files'][0]['Git_mode']='100755'
            elif kind=='head':bad['source_head']='0'*40
            else:bad['files'].pop()
            with self.assertRaises(ValueError):g.validate_original_map(bad,tree)
    def test_queue_sha_parse_status_and_count(self):
        cells=['','124',g.K+' / '+g.CODE,'title','0.2','3','2018','unused','claimed_solved','2/5','','note','','']
        row='|'.join(cells);queue=(row+'\n').encode()
        auth={'head':g.HEAD,'PR':108,'literal_status':'claimed_solved','original_budget':'2/5','whole_QUEUE_bytes':len(queue),
            'whole_QUEUE_sha256':g.sha(queue),'selected_row':row,'selected_row_sha256':g.sha(row.encode()),
            'QUEUE_git_blob_SHA1':hashlib.sha1(b'blob '+str(len(queue)).encode()+b'\0'+queue).hexdigest()}
        self.assertEqual(g.validate_original_queue(auth,queue),g.sha(row.encode()))
        wrong={**auth,'selected_row_sha256':'0'*64}
        with self.assertRaises(ValueError):g.validate_original_queue(wrong,queue)
        for status,effort in [('queued','2/5'),('claimed_solved','0/5')]:
            badcells=list(cells);badcells[8]=status;badcells[9]=effort;badrow='|'.join(badcells);badqueue=(badrow+'\n').encode()
            bad={**auth,'whole_QUEUE_bytes':len(badqueue),'whole_QUEUE_sha256':g.sha(badqueue),'selected_row':badrow,
                'selected_row_sha256':g.sha(badrow.encode()),'QUEUE_git_blob_SHA1':hashlib.sha1(b'blob '+str(len(badqueue)).encode()+b'\0'+badqueue).hexdigest()}
            with self.assertRaises(ValueError):g.validate_original_queue(bad,badqueue)

class EligibilityFixtures(unittest.TestCase):
    def test_eligibility_only_false_drift_rejects(self):
        old=[fixture_row('other'),fixture_row(g.K)];new=copy.deepcopy(old);new[0]['eligible']=False
        ass={'other':{'review_hash':'a'*64,'decision':'candidate'}}
        with self.assertRaises(ValueError):g.scoped_catalog(old,new,{}, {'turn_limit':5},ass)
    def test_exact_held_and_budget_projection_preserved(self):
        old=[fixture_row('other'),fixture_row(g.K)];new=copy.deepcopy(old)
        new[0].update(local_status='claimed_solved',turns_used=2,eligible=False,rank=None)
        out,drift=g.scoped_catalog(old,new,{'other':{'status':'claimed_solved','turns_used':2}},{'turn_limit':5},{})
        self.assertEqual(out[0],old[0]);self.assertEqual(len(drift),1);self.assertFalse(drift[0]['expected_eligible'])
        self.assertFalse(g.expected_eligible(fixture_row('h',holds=['hold']),{}, {'turn_limit':5},{'decision':'candidate'}))
        self.assertFalse(g.expected_eligible(fixture_row('t'),{'status':'queued','turns_used':5},{'turn_limit':5},{}))
    def test_score_or_hold_drift_rejects(self):
        old=[fixture_row('other'),fixture_row(g.K)];new=copy.deepcopy(old);new[0]['impact']=7
        with self.assertRaises(ValueError):g.scoped_catalog(old,new,{}, {'turn_limit':5},{})

class SheetFixtures(unittest.TestCase):
    def data(self,chat='https://example.invalid/existing-authorized-chat'):
        values=['https://example.invalid/original',chat,'https://doi.org/10.5281/zenodo.123',g.K+' / '+g.CODE+' synthetic fixture only']
        row=42;selected="'Math Puzzles'!A42:D42";store={};counter=0
        def pin(data):
            nonlocal counter
            counter+=1;name='synthetic-'+str(counter)+'.json';store[name]=data
            return {'path':name,'bytes':len(data),'sha256':g.sha(data)}
        records={}
        def proc(role,verb,params,response,t,body=None):
            raw=g.canonical(response);stdout=pin(raw);stderr=pin(b'');pt=json.dumps(params,separators=(',',':'));argv=['/synthetic/gws',*verb,'--params',pt]
            obj={'actual_process_record':True,'fixture':False,'PID':100+len(records),'exit_code':0,'argv':argv,
                'params_bytes':len(pt.encode()),'params_sha256':g.sha(pt.encode()),'stdout_pin':stdout,'response_body_pin':stdout,'stderr_pin':stderr,
                'UTC_start':'2026-10-06T00:00:'+str(t).zfill(2)+'Z','UTC_end':'2026-10-06T00:00:'+str(t+1).zfill(2)+'Z'}
            if body is not None:
                bt=json.dumps(body,separators=(',',':'));argv+=['--json',bt];obj['request_body_pin']=pin(bt.encode())
            records[role]=obj
        proc('metadata',['sheets','spreadsheets','get'],{'spreadsheetId':g.SHEET},{'spreadsheetId':g.SHEET,'sheets':[{'properties':{'sheetId':g.GID,'title':g.TITLE}}]},2)
        proc('headers',['sheets','spreadsheets','values','get'],{'spreadsheetId':g.SHEET,'range':"'Math Puzzles'!A1:D1"},{'values':[g.COLUMNS]},4)
        proc('write',['sheets','spreadsheets','values','append'],{'spreadsheetId':g.SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},
             {'spreadsheetId':g.SHEET,'updates':{'updatedRange':selected,'updatedRows':1,'updatedColumns':4,'updatedCells':4}},6,{'majorDimension':'ROWS','values':[values]})
        for role,t in [('readback',8),('independent_readback',10)]:
            proc(role,['sheets','spreadsheets','values','get'],{'spreadsheetId':g.SHEET,'range':selected},{'range':selected,'values':[values]},t)
        receipt={'schema':'pr108-actual-gws-sheet-service-receipt/v3','actual_receipt':True,'fixture':False,
            'spreadsheet_id':g.SHEET,'sheet_id':g.GID,'sheet_title':g.TITLE,'columns':g.COLUMNS,'problem_id':30003996,
            'problem_code':g.CODE,'DOI':'10.5281/zenodo.123','row_index':row,'range':selected,'processes':records,
            'independent_service_authentication_required':True}
        def read(p):
            data=store[p['path']];self.assertEqual(p['bytes'],len(data));self.assertEqual(p['sha256'],g.sha(data));return Path(p['path']),data
        return receipt,{'DOI':receipt['DOI'],'row_index':row,'values':values,'existing_chat_authorized':chat!=''},read
    def test_blank_chat_accepts_without_share_and_bad_existing_links_reject(self):
        receipt,expected,read=self.data('');self.assertEqual(g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)['row_index'],42)
        self.assertFalse(expected['existing_chat_authorized'])
        receipt['schema']='pr108-actual-gws-sheet-service-receipt/v2'
        self.assertEqual(g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)['row_index'],42)
        for link in ['http://example.invalid','https://','https:///missing-host','https://example.invalid bad','javascript:alert(1)','https://[broken','https://user:password@example.invalid']:
            with self.subTest(link=link):
                receipt,expected,read=self.data(link)
                with self.assertRaises(ValueError):g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)
        receipt,expected,read=self.data();expected['existing_chat_authorized']=False
        with self.assertRaises(ValueError):g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)
    def test_synthetic_shape_and_wrong_row_doi_time_or_fixture(self):
        receipt,expected,read=self.data();result=g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)
        self.assertEqual(result['row_index'],42)
        for kind in ['row','doi','time','fixture','service']:
            bad=copy.deepcopy(receipt)
            if kind=='row':bad['row_index']=43
            elif kind=='doi':bad['DOI']='10.5281/zenodo.999'
            elif kind=='time':bad['processes']['write']['UTC_start']='2026-10-05T00:00:00Z'
            elif kind=='fixture':bad['processes']['readback']['fixture']=True
            else:bad['sheet_id']=1
            with self.assertRaises(ValueError):g.validate_sheet(bad,expected,'2026-10-06T00:00:01Z',read)
    def test_local_tracker_or_missing_service_readback_rejects(self):
        receipt,expected,read=self.data();del receipt['processes']['independent_readback']
        with self.assertRaises(ValueError):g.validate_sheet(receipt,expected,'2026-10-06T00:00:01Z',read)
        with self.assertRaises(ValueError):g.validate_sheet({'schema':'pr108-local-tracker/v1'},expected,'2026-10-06T00:00:01Z',read)

class ResourceFixtures(unittest.TestCase):
    def test_published_archive_requires_exact_manifest_and_inventory(self):
        payload={'proof.md':b'fixture only'};manifest=b'fixture manifest only'
        def archive(extra=None,manifest_body=manifest):
            stream=io.BytesIO()
            with zipfile.ZipFile(stream,'w') as z:
                for name,data in {**payload,'PACKAGE_MANIFEST.json':manifest_body,**(extra or {})}.items():z.writestr(name,data)
            return stream.getvalue()
        helper.validate_published_archive(archive(),payload,manifest)
        with self.assertRaises(ValueError):helper.validate_published_archive(archive({'extra.txt':b'not reviewed'}),payload,manifest)
        with self.assertRaises(ValueError):helper.validate_published_archive(archive(manifest_body=b'changed'),payload,manifest)
    def test_capacity_full_entries_counts_and_reserve(self):
        pins=[{'path':'unsolved_math_prioritization/'+name,'bytes':100,'sha256':'0'*64} for name in helper.BASE_NAMES]
        gates={role:{'bytes':128} for role in g.GATE_ROLES};p=g.capacity_inventory(pins,[('bundle/'+g.N+'prior.json',3)],gates,{'proof.pdf':b'x'*40},CAPACITY,POLICY)
        self.assertGreater(p['required_free_bytes'],sum(x['max_bytes'] for x in p['entries']))
        self.assertIn('WORKER_RESULT.json',[x['path'] for x in p['entries']]);self.assertEqual(p['exclusive_atomic_write_slot_max_bytes'],100+512*1024)
        for kind in ['count','headroom','bytes','duplicate']:
            policy=dict(CAPACITY);copies=[('bundle/'+g.N+'prior.json',3)]
            if kind=='count':policy['max_artifact_count']=1
            elif kind=='headroom':policy['headroom_bytes']=1
            elif kind=='bytes':policy['max_materialized_bytes']=1
            else:copies*=2
            with self.assertRaises(ValueError):g.capacity_inventory(pins,copies,gates,{},policy,POLICY)
    def test_worker_policy_only_no_native_invocation(self):
        worker_policy({'deadline_seconds':90,'cpu_seconds':60,'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'open_files':32,'memory_limit_mode':'advisory_no_hard_memory_claim'})
        with self.assertRaises(ValueError):worker_policy({'deadline_seconds':10000})
    def test_bounded_tiny_subprocess_actual_custody_fixture(self):
        mode='optimized' if not __debug__ else 'normal';output=D/'fixture_custody'/mode;output.mkdir(parents=True,exist_ok=True)
        runner=BoundedRunner(output,D,POLICY,ENV_POLICY)
        out,_,record=runner.run([sys.executable,*g.PYTHON_PREFIX,'-c','print("fixture only")'],fixture=True)
        self.assertEqual(out,b'fixture only\n');self.assertTrue(record['fixture']);self.assertEqual(record['exit_code'],0)
        _,_,record=runner.run([sys.executable,*g.PYTHON_PREFIX,'-c','print("x"*10000)'],stdout_cap=100,fixture=True,allow_failure=True)
        self.assertEqual(record['termination_reason'],'stdout_read_cap_exceeded');self.assertLessEqual(record['stdout']['retained_bytes'],64)
        _,_,record=runner.run([sys.executable,*g.PYTHON_PREFIX,'-c','import time; time.sleep(10)'],deadline=1,fixture=True,allow_failure=True)
        self.assertEqual(record['termination_reason'],'deadline_exceeded');self.assertNotEqual(record['exit_code'],0)
        self.assertTrue(all(r['fixture'] for r in runner.records))
    def test_actual_harmless_worker_resource_setup_and_file_cap(self):
        mode='optimized' if not __debug__ else 'normal';output=D/'fixture_resource_setup'/mode;output.mkdir(parents=True,exist_ok=True)
        policy={'deadline_seconds':5,'cpu_seconds':2,'address_space_bytes':512*1024*1024,'file_size_bytes':4096,'open_files':32,
                'memory_limit_mode':'advisory_no_hard_memory_claim'}
        code='from native_assess_worker import apply_resource_policy; from pathlib import Path; import json,sys; setup=apply_resource_policy(json.loads(sys.argv[1])); probe=Path(sys.argv[2]); failed=False\ntry: probe.write_bytes(b"x"*8192)\nexcept OSError: failed=True\nprint(json.dumps({"fixture_only":True,"setup":setup,"file_cap_blocked_oversize_write":failed,"probe_bytes":probe.stat().st_size,"native_assess_executed":False}))'
        runner=BoundedRunner(output,D,POLICY,ENV_POLICY);out,_,record=runner.run([sys.executable,*g.PYTHON_PREFIX,'-c',code,json.dumps(policy),str(output/'probe.bin')],fixture=True)
        result=json.loads(out);self.assertTrue(result['file_cap_blocked_oversize_write']);self.assertLessEqual(result['probe_bytes'],4096)
        self.assertFalse(result['setup']['memory_policy']['hard_memory_limit_claimed']);self.assertEqual(result['setup']['enforced_limit_readbacks']['RLIMIT_FSIZE'],[4096,4096])
        if sys.platform=='darwin':self.assertFalse(result['setup']['memory_policy']['RLIMIT_AS_requested'])
        (output/'RESOURCE_FIXTURE_RESULT.json').write_bytes(g.canonical({**result,'actual_fixture_PID':record['PID'],'UTC_start':record['UTC_start'],'UTC_end':record['UTC_end']}))


class StartupFixtures(unittest.TestCase):
    def folder(self):
        mode='optimized' if not __debug__ else 'normal'
        root=D/'fixture_startup'/mode;root.mkdir(parents=True,exist_ok=True);return root
    def test_clean_python_and_initial_launcher_ignore_injected_startup(self):
        root=self.folder();injected=root/'injected';injected.mkdir(exist_ok=True)
        sentinel=root/'STARTUP_INJECTION_SENTINEL_MUST_BE_ABSENT'
        (injected/'sitecustomize.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("untrusted startup executed")\n')
        old=dict(os.environ)
        try:
            os.environ.update(PYTHONPATH=str(injected),PYTHONHOME=str(injected/'invalid-home'),
                PYTHONSTARTUP=str(injected/'sitecustomize.py'),GH_TOKEN='synthetic-unused-secret-must-not-be-retained',
                GIT_CONFIG_GLOBAL=str(injected/'unreviewed-config'),ENV=str(injected/'unreviewed-shell-startup'))
            python_root=root/'python';python_root.mkdir(exist_ok=True)
            runner=BoundedRunner(python_root,D,POLICY,ENV_POLICY)
            code='import os,json,sys; import v3_guards,prepare_review_bundle,native_assess_worker; v3_guards.validate_python_startup(os.environ); print(json.dumps({"family_imports":True,"flags":[sys.flags.ignore_environment,sys.flags.no_site,sys.flags.dont_write_bytecode],"environment":dict(os.environ),"native_calls":0}))'
            out,_,record=runner.run([sys.executable,*g.PYTHON_PREFIX,'-c',code],fixture=True)
            result=json.loads(out);self.assertEqual(result['environment'],g.COMMON_ENV);self.assertEqual(result['flags'],[1,1,1]);self.assertTrue(result['family_imports'])
            self.assertFalse(sentinel.exists());self.assertFalse(record['ambient_environment_inherited'])
            _,_,worker_record=runner.run([sys.executable,*g.PYTHON_PREFIX,str(D/'native_assess_worker.py'),'--help'],fixture=True)
            self.assertEqual(worker_record['exit_code'],0);self.assertFalse(sentinel.exists())
            launcher_root=root/'launcher';launcher_root.mkdir(exist_ok=True)
            runner=BoundedRunner(launcher_root,D,{**POLICY,'retain_bytes_per_stream':4096},ENV_POLICY)
            out,_,record=runner.run(['/bin/sh',str(D/'launch_review_bundle.sh'),sys.executable,'--verify-startup-only'],fixture=True,role='initial_launcher')
            result=json.loads(out);self.assertTrue(result['startup_probe_only']);self.assertFalse(result['native_prepare_called']);self.assertFalse(result['native_assess_called'])
            self.assertEqual(set(result['program_sha256']),set(g.PROGRAMS));self.assertEqual(result['effective_nonsecret_environment'],g.COMMON_ENV)
            self.assertFalse(sentinel.exists())
            clean_launcher_record=record
            dirty_root=root/'dirty_initial_launcher';dirty_root.mkdir(exist_ok=True)
            runner=BoundedRunner(dirty_root,D,{**POLICY,'retain_bytes_per_stream':4096},ENV_POLICY)
            # Fixture exec trampoline keeps the actual PID but supplies deliberately dirty shell startup inputs.
            code='import os,sys; env=dict(os.environ); env.update(PYTHONPATH=sys.argv[3],PYTHONHOME=sys.argv[3]+"/invalid-home",PYTHONSTARTUP=sys.argv[3]+"/sitecustomize.py",GH_TOKEN="synthetic-unused",GIT_CONFIG_GLOBAL="synthetic-unused",ENV="synthetic-unused"); os.execve("/bin/sh",["/bin/sh",sys.argv[1],sys.argv[2],"--verify-startup-only"],env)'
            out,_,record=runner.run([sys.executable,*g.PYTHON_PREFIX,'-c',code,str(D/'launch_review_bundle.sh'),sys.executable,str(injected)],fixture=True)
            result=json.loads(out);self.assertTrue(result['startup_probe_only']);self.assertEqual(result['effective_nonsecret_environment'],g.COMMON_ENV)
            self.assertFalse(sentinel.exists());self.assertFalse(result['native_prepare_called'])
            (root/'ABSENT_SENTINEL_RESULT.json').write_bytes(g.canonical({'fixture_only':True,'sentinel_path':str(sentinel),
                'sentinel_present':sentinel.exists(),'clean_initial_launcher_actual_PID':clean_launcher_record['PID'],'dirty_initial_launcher_trampoline_actual_PID':record['PID'],'worker_help_actual_PID':worker_record['PID'],'UTC_start':record['UTC_start'],'UTC_end':record['UTC_end'],
                'injected_ambient_variables_removed':['PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','GH_TOKEN','GIT_CONFIG_GLOBAL','ENV'],
                'initial_helper_and_worker_family_imports_available':True,'native_prepare_assess_export_calls':0}))
        finally:os.environ.clear();os.environ.update(old)
    def test_missing_startup_flags_and_ambient_policy_reject_before_spawn(self):
        root=self.folder()/'rejections';root.mkdir(exist_ok=True)
        runner=BoundedRunner(root,D,POLICY,ENV_POLICY)
        with self.assertRaises(ValueError):runner.run([sys.executable,'-B','-c','print("should not execute")'],fixture=True)
        self.assertEqual(runner.records,[])
        for role in ['python','git','gh','initial_launcher']:
            bad=copy.deepcopy(ENV_POLICY);bad[role]['environment']['PYTHONPATH']='unreviewed'
            with self.assertRaises(ValueError):g.validate_environment_policy(bad)
    def test_private_config_pins_exact_locations_and_no_credential_copy(self):
        root=self.folder()/'private_config';root.mkdir(exist_ok=True)
        repo=root/'repository';configdir=repo/'.git';configdir.mkdir(parents=True,exist_ok=True)
        auth=root/'auth';auth.mkdir(exist_ok=True)
        config=configdir/'config';config.write_text('[core]\nrepositoryformatversion = 0\nfsmonitor = false\n')
        hosts=auth/'hosts.yml';secret=b'github.com:\n    oauth_token: synthetic-fixture-secret-no-actual-credential\n';hosts.write_bytes(secret)
        def pin(path):return {'path':str(path),'bytes':path.stat().st_size,'sha256':g.sha(path.read_bytes())}
        policy=copy.deepcopy(ENV_POLICY);policy['git'].update(repository_directory=str(repo),repository_location_pins=[],repository_config_pins=[pin(config)])
        policy['gh']['environment']['GH_CONFIG_DIR']=str(auth);policy['gh']['config_pins']=[pin(hosts)]
        metadata=g.verify_private_runtime_configuration(policy)
        self.assertTrue(all(x['body_retained_or_disclosed'] is False for x in metadata));self.assertNotIn('synthetic-fixture-secret',json.dumps(metadata))
        hosts.write_bytes(secret+b'# changed\n')
        with self.assertRaises(ValueError):g.verify_private_runtime_configuration(policy)
        hosts.write_bytes(secret)
        config.write_text('[include]\npath = unreviewed\n');policy['git']['repository_config_pins']=[pin(config)]
        with self.assertRaises(ValueError):g.verify_private_runtime_configuration(policy)
        config.write_text('[core]\nthis malformed line includes synthetic-fixture-secret\n');policy['git']['repository_config_pins']=[pin(config)]
        try:g.verify_private_runtime_configuration(policy)
        except ValueError as error:self.assertNotIn('synthetic-fixture-secret',str(error))
        else:self.fail('Malformed private config accepted')
        config.write_text('[core]\nfsmonitor = false\n');policy['git']['repository_config_pins']=[pin(config)]
        fake=root/'elsewhere';fake.mkdir(exist_ok=True);other=fake/'config';other.write_bytes(config.read_bytes());policy['git']['repository_config_pins']=[pin(other)]
        with self.assertRaises(ValueError):g.verify_private_runtime_configuration(policy)


class WorkerCorrespondenceFixtures(unittest.TestCase):
    """Pure dictionaries only. Never create actual control/config or execute native worker."""
    def data(self):
        native_manifest=g.canonical({'revision':g.WORKER_DATASET_REVISION,'records':123})
        pins=[{'path':'unsolved_math_prioritization/'+name,'bytes':100,'sha256':'a'*64} for name in g.WORKER_NATIVE_NAMES]
        next(x for x in pins if x['path'].endswith('/manifest.json')).update(bytes=len(native_manifest),sha256=g.sha(native_manifest))
        effective={x:None for x in g.CHOICES};effective.update(execution_mode='review_bundle_only',
            scoped_rank_interpretation='preserve_baseline_labels_and_positions_not_global_rerank',native_baseline_pins=pins,
            queue_py_sha256='a'*64,capacity_policy=copy.deepcopy(CAPACITY),worker_policy={'deadline_seconds':120,'cpu_seconds':2,
            'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'open_files':32,'memory_limit_mode':'advisory_no_hard_memory_claim'})
        execution={'schema':'pr108-immutable-execution-inputs/v3','template_only':False,'effective':effective,
            'program_files':[{'path':x} for x in g.PROGRAMS],'input_files':[]}
        data=g.canonical(execution);output=D/('candidate_'+g.sha(data)[:16])
        control=g.derive_worker_control(execution,data,output,native_manifest)
        return execution,data,output,native_manifest,control
    def result(self,control):
        policy=control['worker_policy'];pid=12345
        return ({'schema':'pr108-native-assess-worker-receipt/v3','fixture':False,'outcome':'success',
            'native_assess_returned_without_exception':True,'actual_operator_PID':pid,'execution_inputs_sha256':control['execution_inputs_sha256'],
            'validated_worker_control':copy.deepcopy(control),'worker_control_binding_sha256':g.sha(g.canonical(control)),
            'requested_resource_policy':copy.deepcopy(policy),'ROOT':control['ROOT'],'queue_py_sha256':control['queue_py_sha256'],
            'native_function':'queue.py:assess','SQL_connection':'mode=ro&immutable=1','native_status_command_called':False,
            'applied_limits':{name:[policy[key],policy[key]] for name,key in [('RLIMIT_CPU','cpu_seconds'),('RLIMIT_FSIZE','file_size_bytes'),('RLIMIT_NOFILE','open_files')]},
            'hard_memory_limit_claimed':False,'memory_policy':{'hard_memory_limit_claimed':False,'platform':sys.platform,
                'requested_advisory_bytes':policy['address_space_bytes'],'RLIMIT_RSS_used':False,'RLIMIT_AS_enforcement_certified':False,'RLIMIT_AS_requested':False}},
            {'PID':pid,'exit_code':0,'termination_reason':None,'child_reaped':True,'deadline_seconds':policy['deadline_seconds']})
    def test_valid_derivation_and_capacity_formula_match(self):
        execution,data,output,manifest,control=self.data()
        self.assertEqual(g.validate_worker_control(control,execution,data,output,manifest),control)
        inventory=g.capacity_inventory(execution['effective']['native_baseline_pins'],[],{role:{'bytes':1} for role in g.GATE_ROLES},{},CAPACITY,POLICY)
        self.assertEqual(control['backend_file_caps'],{Path(x['path']).name:x['max_bytes'] for x in inventory['entries'] if x['path'].startswith('private_native_backend/')})
        result,process=self.result(control);g.validate_worker_result(result,control,process)
    def test_altered_valid_policy_rejected_before_resources_or_module(self):
        execution,data,output,manifest,control=self.data();changed=copy.deepcopy(control);changed['worker_policy']['cpu_seconds']=90
        worker_policy(changed['worker_policy']) # Valid numeric bounds reproduce the adversary trigger.
        with self.assertRaises(ValueError):g.validate_worker_control(changed,execution,data,output,manifest)
        result,process=self.result(changed)
        with self.assertRaises(ValueError):g.validate_worker_result(result,control,process)
    def test_all_other_derived_control_fields_reject(self):
        execution,data,output,manifest,control=self.data()
        for field in ['schema','fixture','ROOT','SQL_cache','dataset_revision','record_count','queue_py_sha256','execution_inputs_sha256','backend_file_caps','extra']:
            with self.subTest(field=field):
                bad=copy.deepcopy(control)
                if field=='fixture':bad[field]=True
                elif field=='record_count':bad[field]=124
                elif field=='backend_file_caps':bad[field]['catalog.json']+=1
                else:bad[field]='changed'
                with self.assertRaises(ValueError):g.validate_worker_control(bad,execution,data,output,manifest)
        bad=copy.deepcopy(control);bad['record_count']=123.0
        with self.assertRaises(ValueError):g.validate_worker_control(bad,execution,data,output,manifest)
    def test_authenticated_manifest_and_reviewed_baseline_binding(self):
        execution,data,output,manifest,control=self.data()
        with self.assertRaises(ValueError):g.validate_worker_control(control,execution,data,output,manifest+b' ')
        wrong=copy.deepcopy(execution);wrong['effective']['queue_py_sha256']='b'*64;wrongdata=g.canonical(wrong)
        with self.assertRaises(ValueError):g.derive_worker_control(wrong,wrongdata,D/('candidate_'+g.sha(wrongdata)[:16]),manifest)
    def test_parent_rejects_requested_applied_control_and_deadline_drift(self):
        *_,control=self.data()
        for field in ['requested','applied_cpu','applied_file','applied_open','control','control_sha','queue','memory','deadline']:
            with self.subTest(field=field):
                result,process=self.result(control)
                if field=='requested':result['requested_resource_policy']['cpu_seconds']=90
                elif field=='applied_cpu':result['applied_limits']['RLIMIT_CPU']=[90,90]
                elif field=='applied_file':result['applied_limits']['RLIMIT_FSIZE']=[1,1]
                elif field=='applied_open':result['applied_limits']['RLIMIT_NOFILE']=[64,64]
                elif field=='control':result['validated_worker_control']['record_count']=124
                elif field=='control_sha':result['worker_control_binding_sha256']='b'*64
                elif field=='queue':result['queue_py_sha256']='b'*64
                elif field=='memory':result['memory_policy']['requested_advisory_bytes']+=1
                else:process['deadline_seconds']=119
                with self.assertRaises(ValueError):g.validate_worker_result(result,control,process)

if __name__=='__main__':unittest.main(verbosity=2)
