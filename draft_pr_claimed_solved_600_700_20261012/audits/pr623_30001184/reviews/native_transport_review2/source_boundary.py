"""Independent original import-failure reproducer and root trust-chain controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,tempfile,types,unittest
from unittest.mock import patch
import run_supplied as capture
HERE=Path(__file__).resolve().parent
ROOT=capture.ROOT
nt=capture.nt
kit_source=(HERE/'tmp/inputs/zenodo_deposit_tool/zenodo.py').read_bytes()
adapter_source=(capture.SNAP/'native_transport.py').read_bytes()
bootstrap_source=(capture.SNAP/'run_native_transport.py').read_bytes()
BOOT_SHA='81b41e0dda32122b3c3f3d744829fab365381714107ec63703c337a856cdf72e'
def checked_exec(path,sha,name='__main__'):
    source=path.read_bytes()
    if hashlib.sha256(source).hexdigest()!=sha:raise RuntimeError('source rejected before execution')
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(source,str(path),'exec',dont_inherit=True),m.__dict__)
    return m
class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE/'tmp');self.folder=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_original_stale_import_exploit_cannot_bind_loaded_code(self):
        stale=types.ModuleType('zenodo');stale.__file__=str(nt.KIT_PATH)
        exec(compile(kit_source+b'\ndef run(args, client=None):\n return {"unreviewed":True}\n',str(nt.KIT_PATH),'exec'),stale.__dict__)
        stale.digest=lambda *a:nt.KIT_SHA
        stale_adapter=types.ModuleType('native_transport');stale_adapter.main=lambda:'unreviewed'
        with patch.dict(sys.modules,{'zenodo':stale,'native_transport':stale_adapter}):
            fresh=capture.bootstrap.load_reviewed_adapter()
            data=fresh.capture_inputs()
            result=fresh.run_captured_kit(types.SimpleNamespace(command='check',sandbox=False),data)
            self.assertNotIn('unreviewed',result)
            self.assertIs(sys.modules['zenodo'],stale);self.assertIs(sys.modules['native_transport'],stale_adapter)
            self.assertIsNot(fresh.zenodo,stale)
            self.assertEqual(fresh.zenodo.__verified_source_sha256__,nt.KIT_SHA)
            self.assertEqual(fresh.zenodo.ROOT,ROOT)
    def test_outer_bootstrap_wrong_sha_before_top_level_side_effect(self):
        path=self.folder/'bad-bootstrap.py';marker=self.folder/'ran'
        path.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
        with self.assertRaises(RuntimeError):checked_exec(path,BOOT_SHA)
        self.assertFalse(marker.exists())
    def test_bad_adapter_and_kit_wrong_sha_before_top_level_side_effect(self):
        for kind,load in [('adapter',capture.bootstrap.load_reviewed_adapter),('kit',nt.load_checked_kit)]:
            path=self.folder/(kind+'.py');marker=self.folder/(kind+'-ran')
            path.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
            with self.subTest(kind=kind),self.assertRaises(RuntimeError):load(path)
            self.assertFalse(marker.exists())
    def test_all_three_source_reopen_races_execute_only_captured_bytes(self):
        for kind,source,sha,loader in [('bootstrap',bootstrap_source,BOOT_SHA,lambda p:checked_exec(p,BOOT_SHA,'isolated_bootstrap')),
                                      ('adapter',adapter_source,capture.bootstrap.ADAPTER_SHA256,capture.bootstrap.load_reviewed_adapter),
                                      ('kit',kit_source,nt.KIT_SHA,nt.load_checked_kit)]:
            path=self.folder/(kind+'.py');path.write_bytes(source);marker=self.folder/(kind+'-ran')
            calls=[];read=Path.read_bytes
            def raced(p):
                data=read(p)
                if p==path:
                    calls.append(p)
                    p.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
                return data
            with self.subTest(kind=kind),patch.object(Path,'read_bytes',new=raced):fresh=loader(path)
            self.assertEqual(len(calls),1);self.assertFalse(marker.exists())
            self.assertNotEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha)
            if kind=='kit':self.assertEqual(fresh.__verified_source_sha256__,sha)
            if kind=='adapter':self.assertEqual(fresh.zenodo.__verified_source_sha256__,nt.KIT_SHA)
    def test_single_manifest_capture_rejects_wrong_bytes_before_payload_read(self):
        manifest=self.folder/'zenodo-deposit.json';manifest.write_bytes(b'{"files":[]}')
        calls=[];read=Path.read_bytes
        def track(p):calls.append(p);return read(p)
        with patch.object(Path,'read_bytes',new=track),self.assertRaises(nt.zenodo.DepositError):nt.capture_inputs(manifest)
        self.assertEqual(calls,[manifest])
    def test_root_inline_launcher_full_check_without_token_or_network(self):
        launch=capture.AUTHOR/'run_native_transport.py'
        read=Path.read_bytes
        captured=[]
        def record(p):
            data=read(p)
            if p==launch:captured.append(hashlib.sha256(data).hexdigest())
            return data
        with patch.object(Path,'read_bytes',new=record),patch.object(sys,'argv',['-','check']),patch.object(nt.http.client,'HTTPSConnection',side_effect=AssertionError('network prohibited')):
            with self.assertRaises(SystemExit) as e:checked_exec(launch,BOOT_SHA)
        self.assertEqual(e.exception.code,0);self.assertEqual(captured,[BOOT_SHA])
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceTests))
    record={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'real_network_calls':0}
    (HERE/('SOURCE_OPTIMIZED.json' if sys.flags.optimize else 'SOURCE_NORMAL.json')).write_text(json.dumps(record,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
