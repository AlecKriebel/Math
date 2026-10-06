"""Independent bounded offline adversary. Never prepare/native assess/service calls."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,copy,csv,datetime,hashlib,io,itertools,json,os,subprocess,unittest
import v3_guards as g
import prepare_review_bundle as h
import test_v3_guards as sealed
from bounded_process import BoundedRunner
O=Path(__file__).resolve().parent.parent
A=O.parent
C=A.parents[2]
D=A/'native_publication_integration_plan_20261006/corrected_v3'
READS={}
def read_pin(pin):
    p=C/g.relative(pin['path']);b=p.read_bytes()
    if len(b)!=pin['bytes'] or g.sha(b)!=pin['sha256']:raise ValueError('Actual evidence pin mismatch')
    READS[str(p)]={'bytes':len(b),'sha256':g.sha(b),'role':'offline_actual_evidence_read'}
    return p,b
def read_path(p):
    b=p.read_bytes();READS[str(p)]={'bytes':len(b),'sha256':g.sha(b),'role':'offline_actual_input_read'};return b

def native_blob(name):
    args=['/usr/bin/git','show','04a66906a97293b9c89495fda7bec0727e62f51b:unsolved_math_prioritization/'+name]
    env={**g.GIT_ENV};t=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(args,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=p.communicate(timeout=20)
    if p.returncode:raise ValueError('Read-only source blob failed')
    records=RESULT.setdefault('read_only_git_processes',[]);records.append({'argv':args,'PID':p.pid,'UTC_start':t,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(b),'stdout_sha256':g.sha(b),'stderr_bytes':len(e),'stderr_sha256':g.sha(e),'read_only':True})
    return b
RESULT={'fixture_only':True,'native_prepare_assess_export_calls':0,'service_calls':0,'central_proof_turns':0}
class IndependentFixtures(unittest.TestCase):
    def test_actual_immutable_v2_sheet_receipt(self):
        sb=read_path(A/'ROOT_ACTUAL_GOOGLE_SHEET_SERVICE_RECEIPT_20261006.json');s=g.loads(sb)
        pub=g.loads(read_path(A/'ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json'))
        self.assertEqual(s['schema'],'pr108-actual-gws-sheet-service-receipt/v2');self.assertEqual(s['values'][1],'')
        expected={'DOI':s['DOI'],'row_index':s['row_index'],'values':s['values'],'existing_chat_authorized':False}
        result=g.validate_sheet(s,expected,pub['UTC_end'],read_pin)
        self.assertEqual(result['range'],"'Math Puzzles'!A31:D31")
        self.assertEqual(read_path(A/'ROOT_ACTUAL_GOOGLE_SHEET_SERVICE_RECEIPT_20261006.json'),sb)
        RESULT['actual_immutable_sheet_compatibility']={'unchanged_receipt_sha256':g.sha(sb),'schema':s['schema'],'range':result['range'],'blank_B':True,'pure_guard_pass':True,'fresh_service_authentication_performed':False}
    def test_actual_publication_receipt_and_exact_packet(self):
        root=A/'publication_ready_package_v2';mb=read_path(root/'PACKAGE_MANIFEST.json');m=g.loads(mb);files={}
        for e in m['files']:
            b=read_path(root/e['relative_path']);self.assertEqual(len(b),e['bytes']);self.assertEqual(g.sha(b),e['sha256']);files[e['relative_path']]=b
        p=A/'ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json';pb=read_path(p)
        cfg={'publication':{'receipt':{'path':str(p.relative_to(C)),'bytes':len(pb),'sha256':g.sha(pb)}}}
        receipt,doi=h.publication_check(cfg,files,mb,read_pin)
        self.assertEqual(doi,'10.5281/zenodo.23181280');self.assertEqual(read_path(p),pb)
        RESULT['actual_immutable_publication_compatibility']={'DOI':doi,'receipt_sha256':g.sha(pb),'package_manifest_sha256':g.sha(mb),'logical_files':len(files),'pure_guard_pass':True,'fresh_service_authentication_performed':False}
    def test_independent_csv_matrix(self):
        # Separate writer/reader oracle; all unrelated serialized records stay exact.
        controls=['\v','\f','\x1c','\x1d','\x1e','\x85','\u2028','\u2029','é','数学']
        cases=0
        for ending,control,target_pos,eof in itertools.product(['\r','\n','\r\n'],controls,[0,1,2],[False,True]):
            strings=[('other1','left'+control+'\r\nquoted'),('other2','right,comma"quote'),(g.K,'old'+control)]
            strings.insert(target_pos,strings.pop())
            stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\r\n');w.writerow(['id','title','holds','reasons'])
            # Deliberate CRLF serialization quotes both CR/LF, then replace terminators outside fields.
            records=[]
            for ident,title in strings:
                out=io.StringIO(newline='');csv.writer(out,lineterminator='\r\n').writerow([ident,title,'','']);records.append(out.getvalue()[:-2]+ending)
            data=('id,title,holds,reasons'+ending+''.join(records)).encode()
            if eof:data=data[:-len(ending.encode())]
            old=g.csv_records(data)[1];title='new'+control+'\n\r\n"tail';out=g.csv_overlay(data,{'id':g.K,'title':title,'holds':[],'reasons':[]});new=g.csv_records(out)[1]
            self.assertEqual([r['fields'][0] for r in old],[r['fields'][0] for r in new]);self.assertEqual(len(old),len(new))
            for x,y in zip(old,new):
                if x['fields'][0]!=g.K:self.assertEqual(x['bytes'],y['bytes'])
                else:self.assertEqual(y['fields'][1],title)
            self.assertEqual(out.endswith(ending.encode()),not eof);cases+=1
        RESULT['independent_csv_cases']=cases
    def test_campaign_preserves_cells_and_unicode_lines(self):
        before=b'# Queue\r\n'+('unrelated unicode\u2028control\x85line\r\n').encode()+b'| 7 | 30003996 / OWR-16633-013 | title | ev | diff | year | age | queued | 0/5 | links | old note |  |\r\n'+b'tail without newline'
        out=h.campaign_overlay(before,'Authenticated complete result published with exact source and author provenance','10.5281/zenodo.23181280')
        old=g.physical_lines(before.decode());new=g.physical_lines(out.decode());self.assertEqual(len(old),len(new))
        for i in [0,1,3]:self.assertEqual(old[i],new[i])
        oc=old[2].rstrip('\r\n').split('|');nc=new[2].rstrip('\r\n').split('|')
        for i in range(14):
            if i not in [8,9,11,12]:self.assertEqual(oc[i],nc[i])
        self.assertEqual(nc[8].strip(),'claimed_solved');self.assertEqual(nc[9].strip(),'2/5')
        with self.assertRaises(ValueError):h.campaign_overlay(before,'Unsupported | note injection must fail guard','10.5281/zenodo.23181280')
    def test_literal_native_predicate_cross_product(self):
        code=native_blob('queue.py').decode();tree=ast.parse(code);rank=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='rank')
        loop=next(n for n in rank.body if isinstance(n,ast.For));assignments=[n for n in loop.body if 158<=n.lineno<=163]
        fn=compile(ast.fix_missing_locations(ast.Module(body=assignments,type_ignores=[])),'exact-native-predicate','exec')
        count=0
        for limit,decision,resolution,stale,holds,status,turns in itertools.product([5,7],['candidate','defer','exclude','repair',None],[None,'already_solved'],[False,True],[[],['hold']],[None,'queued','ready','claimed_solved','exhausted'],[0,2,5,7]):
            policy={'turn_limit':limit};review={'decision':decision,'resolution':resolution};local={'turns_used':turns}
            if status is not None:local['status']=status
            scope={'cfg':policy,'review':review,'local':local,'a':{'holds':holds},'stale':stale};exec(fn,scope)
            row=sealed.fixture_row('unrelated',holds=holds,present=True);review['review_hash']='b'*64 if stale else row['review_hash']
            self.assertEqual(g.native_status_turns(row,local,policy,review),(scope['local_status'],scope['turns']))
            self.assertIs(g.expected_eligible(row,local,policy,review),scope['eligible']);count+=1
        RESULT['independent_exact_native_predicate_cases']=count
    def test_actual_baseline_scoped_projection_model(self):
        rows=g.loads(native_blob('catalog.json'));states=g.loads(native_blob('state.json'));ass=g.loads(native_blob('assessments.json'));policy=g.loads(native_blob('policy.json'))
        modeled=copy.deepcopy(rows)
        for row in modeled:
            status,turns=g.native_status_turns(row,states.get(row['id'],{}),policy,ass.get(row['id'],{}));row.update(local_status=status,turns_used=turns,eligible=g.expected_eligible(row,states.get(row['id'],{}),policy,ass.get(row['id'],{})))
        scoped,drift=g.scoped_catalog(rows,modeled,states,policy,ass)
        for old,new in zip(rows,scoped):
            if old['id']!=g.K:self.assertEqual(old,new)
        RESULT['actual_baseline_model']={'records':len(rows),'explained_projection_drift_count':len(drift),'all_unrelated_rows_ranks_positions_preserved':True,'native_regeneration_executed':False,'model_only':True}
        bad=copy.deepcopy(modeled);other=next(r for r in bad if r['id']!=g.K);other['source_url']='https://example.invalid/unauthenticated'
        with self.assertRaises(ValueError):g.scoped_catalog(rows,bad,states,policy,ass)
    def test_capacity_with_actual_sizes_and_64MiB_commit_reserve(self):
        pins=g.loads(read_path(O/'NATIVE_BASELINE_PINS.json'))['pins'];policy={**sealed.CAPACITY,'future_commit_overhead_bytes':64*1024*1024};process={**sealed.POLICY,'max_process_count':64,'retain_bytes_per_stream':4096}
        gates={role:{'bytes':65536} for role in g.GATE_ROLES};plan=g.capacity_inventory(pins,[],gates,{},policy,process)
        self.assertEqual(plan['required_free_bytes'],sum(e['max_bytes'] for e in plan['entries'])+plan['exclusive_atomic_write_slot_max_bytes']+plan['headroom_bytes']+plan['future_commit_overhead_bytes']+plan['runtime_overhead_bytes'])
        self.assertEqual(len(plan['entries'])+1,plan['file_count_cap']);self.assertEqual(plan['future_commit_overhead_bytes'],64*1024*1024)
        RESULT['illustrative_capacity_without_package_or_inputs']={k:v for k,v in plan.items() if k!='entries'}
        RESULT['illustrative_capacity_without_package_or_inputs']['final_exact_configuration_clearance']=False
        for change in [{'runtime_overhead_bytes':1},{'future_commit_overhead_bytes':1},{'headroom_bytes':1}]:
            with self.assertRaises(ValueError):g.capacity_inventory(pins,[],gates,{},dict(policy,**change),process)
    def test_worker_control_values_are_valid_but_not_manifest_recompared(self):
        # A static observation only; no execute/control/config/gate/native fixture created.
        import native_assess_worker as worker
        reviewed={'deadline_seconds':120,'cpu_seconds':90,'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'open_files':32,'memory_limit_mode':'advisory_no_hard_memory_claim'}
        changed={**reviewed,'cpu_seconds':1};worker.validate_policy(reviewed);worker.validate_policy(changed)
        tree=ast.parse(read_path(D/'native_assess_worker.py'));execute=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
        comparisons=[ast.unparse(n) for n in ast.walk(execute) if isinstance(n,ast.Compare)]
        compared=any('worker_policy' in c and 'execution' in c for c in comparisons)
        self.assertFalse(compared)
        RESULT['worker_control_static_question']={'control_policy_can_differ_while_both_valid':True,'manifest_policy_correspondence_comparison_present':compared,'actual_control_or_worker_execution':False,'requires_threat_scope_assessment':True}

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(sealed)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(IndependentFixtures))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    mode='optimized' if not __debug__ else 'normal';RESULT.update(actual_fixture_operator_PID=os.getpid(),UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),mode=mode,test_count=result.testsRun,successful=result.wasSuccessful(),failures=len(result.failures),errors=len(result.errors),reads=READS)
    (O/('INDEPENDENT_RESULTS_'+mode.upper()+'.json')).write_bytes(g.canonical(RESULT))
    raise SystemExit(0 if result.wasSuccessful() else 1)
