"""Small synthetic tests; never calls execute(), native.assess(), services or Git writes."""
import copy,importlib.util,json,os,pathlib,sys,time,unittest
import native_worker as w
import native_runner as r
import protocol as p
D=pathlib.Path(__file__).parent
ROOT=D/'fixtures'/('optimized' if sys.flags.optimize else 'normal')/('run_'+str(os.getpid()))
ROOT.mkdir(parents=True,exist_ok=False)
PY=os.path.realpath('/opt/homebrew/bin/python3')
POLICY={'deadline_seconds':2,'stdout_cap':256,'stderr_cap':256,'retain_bytes':128,'max_processes':12,
 'term_grace_seconds':1,'allocation_cap':160*1024*1024,'file_count_cap':512,'headroom_bytes':32*1024*1024,
 'commit_reserve_bytes':8*1024*1024,'runtime_reserve_bytes':8*1024*1024}
def rejected(fn,*args,**kwargs):
    try:fn(*args,**kwargs)
    except (ValueError,OSError,KeyError,TypeError):return
    raise AssertionError('Guard failed to reject '+fn.__name__)
def spec_for(path,invocation=None,chain=None):
    b=w.read_file(path,64*1024*1024)
    return {'invocation_path':str(invocation or path),'resolved_absolute_path':str(path),'symlink_chain':chain or [],**w.pin(b),'version':'synthetic-current-fixture'}
class Programs(unittest.TestCase):
    def area(self):
        path=ROOT/self._testMethodName;path.mkdir(mode=0o700);return path
    def test_json_and_pin_guards(self):
        rejected(r.loads,b'{"x":1,"x":2}');rejected(w.loads,b'{"x":NaN}')
        rejected(r.audit_path,{'path':'../escape','bytes':1,'sha256':'0'*64})
        rejected(r.audit_path,{'path':'x','bytes':True,'sha256':'0'*64})
        rejected(r.audit_path,{'path':'x','bytes':1,'sha256':'g'*64})
    def test_atomic_and_collision(self):
        a=self.area();w.atomic_write(a,'good',b'old',32)
        rejected(w.atomic_write,a,'good',b'other',32)
        rejected(w.atomic_write,a,'good',b'new',32,replace=True)
        rejected(w.atomic_write,a,'good',b'new',32,replace=True,expected=w.pin(b'stale'))
        w.atomic_write(a,'good',b'new',32,replace=True,expected=w.pin(b'old'));self.assertEqual((a/'good').read_bytes(),b'new')
        (a/'blocked.tmp').write_bytes(b'collision');rejected(w.atomic_write,a,'blocked',b'new',32)
        self.assertEqual((a/'blocked.tmp').read_bytes(),b'collision');self.assertFalse((a/'blocked').exists())
        rejected(w.atomic_write,a,'../escape',b'x',32);rejected(w.atomic_write,a,'oversized',b'x'*33,32)
    def test_read_symlink_hardlink_and_mkdir(self):
        a=self.area();(a/'real').write_bytes(b'data');(a/'link').symlink_to('real')
        rejected(w.read_file,a/'link',32);rejected(r.bootstrap_read,a/'link',32)
        os.link(a/'real',a/'hard');rejected(w.read_file,a/'real',32);(a/'hard').unlink()
        (a/'dir').mkdir();(a/'ancestor').symlink_to('dir');(a/'dir/f').write_bytes(b'x')
        rejected(w.read_file,a/'ancestor/f',32);rejected(w.safe_mkdir,a,'dir')
        w.safe_mkdir(a,'unique');self.assertEqual((a/'unique').stat().st_mode&0o777,0o700)
    def test_native_path_adapter(self):
        a=self.area();caps={'ledger':256,'csv':256,'json':256}
        for name in caps:w.atomic_write(a,name,b'old\n',256)
        Safe=w.guarded_native_paths(a,caps)
        with (Safe(a)/'ledger').open('a') as f:f.write('new\n')
        self.assertEqual((a/'ledger').read_bytes(),b'old\nnew\n')
        with (Safe(a)/'csv').open('w',newline='') as f:f.write('a,b\r\n"multi\nline",x\r\n')
        self.assertEqual((a/'csv').read_bytes(),b'a,b\r\n"multi\nline",x\r\n')
        (Safe(a)/'json').write_text('λ');self.assertEqual((a/'json').read_bytes(),'λ'.encode())
        rejected((Safe(a)/'unlisted').write_text,'x');rejected((Safe(a.parent)/'json').read_text)
        rejected((Safe(a)/'json').open,'rb')
    def test_runtime_chain_preserves_invocation(self):
        a=self.area();(a/'actual').mkdir();f=a/'actual/tool';f.write_bytes(b'current bytes')
        (a/'ancestor').symlink_to('actual');inv=a/'ancestor/tool'
        chain=[{'path':str(a/'ancestor'),'target':'actual','target_utf8_sha256':w.sha(b'actual')}]
        spec=spec_for(f,inv,chain);self.assertEqual(r.resolve_invocation(spec,w),str(f));self.assertEqual(spec['invocation_path'],str(inv))
        bad=copy.deepcopy(spec);bad['symlink_chain']=[];rejected(r.resolve_invocation,bad,w)
        bad=copy.deepcopy(spec);bad['sha256']='0'*64;rejected(r.resolve_invocation,bad,w)
        (a/'ancestor').unlink();(a/'ancestor').symlink_to('other');(a/'other').mkdir();(a/'other/tool').write_bytes(b'current bytes')
        rejected(r.resolve_invocation,spec,w)
        (a/'cycle').symlink_to('cycle');bad=spec_for(f,a/'cycle',[]);rejected(r.resolve_invocation,bad,w)
    def test_gh_actual_compatible_and_dangerous(self):
        good='git_protocol: https\neditor:\nprompt: enabled\npager:\naliases:\n    co: pr checkout\nhttp_unix_socket:\nbrowser:\nversion: "1"\n'
        r.validate_gh_configuration_lines(good)
        for bad in [good.replace('pager:','pager: evil'),good.replace('pr checkout','!curl evil'),good+'git_protocol: https\n',
                    good+'unknown: x\n',good.replace('    co:','\tco:'),good.replace('http_unix_socket:','http_unix_socket: /tmp/evil')]:
            rejected(r.validate_gh_configuration_lines,bad)
    def test_resources_and_cache_path(self):
        limits={'cpu_seconds':2,'file_size_bytes':4096,'open_files':32,'memory_advisory_bytes':128*1024*1024,'hard_memory_claimed':False}
        w.limits_policy(limits)
        for key,value in [('cpu_seconds',True),('file_size_bytes',33*1024*1024),('open_files',100),('hard_memory_claimed',True)]:
            bad={**limits,key:value};rejected(w.limits_policy,bad)
        rejected(w.check_cache,ROOT/'fake.sqlite',{'bytes':0,'sha256':'0'*64},p.REV,15458,b'{}',b'{}')
    def test_actual_small_process_receipts(self):
        a=self.area();runner=r.Processes(a,POLICY,w);env=w.clean_environment()
        out,rec=runner.run([PY,'-E','-S','-B','-c','print("harmless synthetic stdout")'],a,env,fixture=True)
        self.assertEqual(out,b'harmless synthetic stdout\n');self.assertTrue(rec['reaped']);self.assertTrue(rec['streams_fully_drained'])
        self.assertEqual(rec['streams']['stdout']['observed_sha256'],w.sha(out));self.assertTrue(rec['environment_captured_before_spawn'])
        out,rec=runner.run([PY,'-E','-S','-B','-c','import os;os.write(1,b"x"*1024)'],a,env,fixture=True,allow_failure=True)
        self.assertEqual(rec['termination_reason'],'stdout_cap');self.assertTrue(rec['reaped']);self.assertLessEqual(len(out),256)
        out,rec=runner.run([PY,'-E','-S','-B','-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(20)'],a,env,deadline=1,fixture=True,allow_failure=True)
        self.assertEqual(rec['termination_reason'],'deadline');self.assertTrue(rec['SIGKILL_attempted']);self.assertTrue(rec['reaped'])
        out,rec=runner.run([PY,'-E','-S','-B','-c','import time;time.sleep(20)'],a,env,watch=lambda:(_ for _ in ()).throw(ValueError('synthetic watchdog')),fixture=True,allow_failure=True)
        self.assertTrue(rec['termination_reason'].startswith('watchdog:'));self.assertTrue(rec['reaped'])
    def test_actual_limit_readbacks(self):
        a=self.area();runner=r.Processes(a,{**POLICY,'stdout_cap':4096,'stderr_cap':4096,'retain_bytes':4096},w)
        code='import importlib.util,json,os; s=importlib.util.spec_from_file_location("w",'+repr(str(D/'native_worker.py'))+'); w=importlib.util.module_from_spec(s); s.loader.exec_module(w); lim={"cpu_seconds":2,"file_size_bytes":4096,"open_files":32,"memory_advisory_bytes":134217728,"hard_memory_claimed":False}; x=w.apply_limits(lim); f=os.open("bounded",os.O_WRONLY|os.O_CREAT,0o600);\ntry:\n os.write(f,b"x"*8192)\nexcept OSError:\n pass\nos.close(f); print(json.dumps({"synthetic_fixture_only":True,"limits":x,"file_bytes":os.stat("bounded").st_size}))'
        out,rec=runner.run([PY,'-E','-S','-B','-c',code],a,w.clean_environment(),fixture=True,allow_failure=True)
        self.assertEqual(rec['exit_code'],0);result=json.loads(out);self.assertTrue(result['synthetic_fixture_only'])
        self.assertEqual(result['limits']['enforced'],{'RLIMIT_CPU':[2,2],'RLIMIT_FSIZE':[4096,4096],'RLIMIT_NOFILE':[32,32]})
        self.assertLessEqual(result['file_bytes'],4096);self.assertFalse(result['limits']['memory']['hard_memory_limit_claimed'])
    def test_template_and_unclean_startup_rejected_before_execution(self):
        a=self.area();cfg=a/'template.json';cfg.write_bytes(r.canonical({'schema':'pr110-concrete-native-config/v1','template_only':True,'packet':None,'adversary':None,'commission':None}))
        runner=r.Processes(a,{**POLICY,'stdout_cap':4096,'stderr_cap':4096,'retain_bytes':4096},w)
        out,rec=runner.run([PY,'-E','-S','-B','-P',str(D/'native_runner.py'),'--config',str(cfg)],a,w.clean_environment(),fixture=True,allow_failure=True)
        self.assertNotEqual(rec['exit_code'],0);self.assertFalse((D/'workspaces').exists())
        out,rec=runner.run([PY,'-E','-B',str(D/'native_runner.py'),'--config',str(cfg)],a,w.clean_environment(),fixture=True,allow_failure=True)
        self.assertNotEqual(rec['exit_code'],0);self.assertEqual(rec['termination_reason'],None)
    def test_prior_and_unrelated_scope_guards(self):
        old=D.parent/'native_integration_preparation_20261006/test_protocol.py'
        spec=importlib.util.spec_from_file_location('previous_fixture_support',old);support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)
        before,after,overlay,event=support.native_fixture();scoped,drift=p.scoped_outputs(before,after,overlay,event,support.NOTE,support.DOI)
        formatted=r.format_scoped_json(before,scoped,p);self.assertEqual(p.loads(formatted['catalog.json'])[0],p.loads(before['catalog.json'])[0])
        bad=copy.deepcopy(after);rows=p.loads(bad['catalog.json']);rows[0]['impact']+=0.25;bad['catalog.json']=p.canonical(rows)
        rejected(p.scoped_outputs,before,bad,overlay,event,support.NOTE,support.DOI)
        source=(D.parent/'original_head_authentication_20261006/original_attempt/source_record.json').read_bytes()
        prior=(D.parent/'original_head_authentication_20261006/original_attempt/prior_imported_report.json').read_bytes()
        p.sourcepair(source,prior);rejected(p.sourcepair,source,b'{}');rejected(p.sourcepair,source+b' ',prior)
        changed={**event,'turns_used':True};rejected(p.scoped_outputs,before,after,overlay,changed,support.NOTE,support.DOI)
    def test_full_diff_text_binary_and_cap(self):
        offers={r.N+'state.json':b'{"a":2}\n',r.N+'attempts/'+p.K+'/binary':b'\xff\0'}
        diff=r.full_diff({'state.json':b'{"a":1}\n'},offers,'unused');self.assertIn(b'-{"a":1}',diff);self.assertIn(b'+{"a":2}',diff)
        self.assertIn(b'Complete new binary addition',diff);rejected(r.full_diff,{'state.json':b'{"a":1}\n'},offers,'unused',10)
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Programs);result=unittest.TextTestRunner(verbosity=2).run(suite)
    body=w.canonical({'schema':'pr110-offline-program-fixtures/v1','UTC':w.now(),'actual_test_operator_PID':os.getpid(),
      'Python':sys.version,'optimization':sys.flags.optimize,'synthetic_fixture_only':True,'actual_service_calls':0,'actual_native_assess_calls':0,
      'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful(),
      'program_pins':{name:w.read_file(D/name,128*1024,retain=False) for name in r.PROGRAMS}})
    w.atomic_write(ROOT,'RESULT.json',body,65536);print(str(ROOT));sys.exit(0 if result.wasSuccessful() else 1)
