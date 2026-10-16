"""Independent trusted-entry checks; private copies, no network/credentials."""
from pathlib import Path
from datetime import datetime,timezone
import contextlib,hashlib,io,json,sys,tempfile,types,unittest
from unittest.mock import patch
import run_supplied as loaded
HERE=Path(__file__).resolve().parent
SHA='16ac53b7127971de17c0948783fbc23ccc6854c7720e7e63cbd585305df7bf3b'
def launch_from_capture(path):
    source=path.read_bytes()
    if hashlib.sha256(source).hexdigest()!=SHA:raise RuntimeError('Review3 outer bootstrap hash differs before execution')
    module=types.ModuleType('__main__');module.__file__=str(path)
    exec(compile(source,str(path),'exec',dont_inherit=True),module.__dict__)
class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE/'tmp');self.folder=Path(self.temp.name)
        for name in('run_native_transport.py','native_transport.py'):(self.folder/name).write_bytes((loaded.SNAP/name).read_bytes())
    def tearDown(self):self.temp.cleanup()
    def test_actual_outer_capture_launcher_dispatches_only_checked_check(self):
        stream=io.StringIO()
        stale=types.ModuleType('zenodo');stale.run=lambda *_:raise_unreviewed()
        with patch.dict(sys.modules,{'zenodo':stale}),patch.object(sys,'argv',['-', 'check']),contextlib.redirect_stdout(stream):
            with self.assertRaises(SystemExit)as exited:launch_from_capture(self.folder/'run_native_transport.py')
        self.assertEqual(exited.exception.code,0);self.assertIs(sys.modules.get('zenodo'),None)
        result=json.loads(stream.getvalue());self.assertEqual(result['environment'],'production');self.assertEqual(len(result['files']),2)
    def test_outer_rejects_modified_bootstrap_before_marker(self):
        marker=self.folder/'ran-unreviewed';source=self.folder/'run_native_transport.py'
        source.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
        with self.assertRaises(RuntimeError):launch_from_capture(source)
        self.assertFalse(marker.exists())
    def test_outer_uses_captured_bootstrap_after_path_changes(self):
        path=self.folder/'run_native_transport.py';read=Path.read_bytes;hits=[]
        def race(p):
            data=read(p)
            if p==path:hits.append(p);p.write_bytes(b'raise RuntimeError("changed path executed")\n')
            return data
        stream=io.StringIO()
        with patch.object(Path,'read_bytes',new=race),patch.object(sys,'argv',['-', 'check']),contextlib.redirect_stdout(stream):
            with self.assertRaises(SystemExit)as exited:launch_from_capture(path)
        self.assertEqual(exited.exception.code,0);self.assertEqual(len(hits),1);self.assertEqual(len(json.loads(stream.getvalue())['files']),2)
    def test_bad_adapter_marker_rejected_after_valid_bootstrap_capture(self):
        marker=self.folder/'ran-bad-adapter'
        (self.folder/'native_transport.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
        with patch.object(sys,'argv',['-', 'check']),contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit)as exited:launch_from_capture(self.folder/'run_native_transport.py')
        self.assertEqual(exited.exception.code,1);self.assertFalse(marker.exists())
def raise_unreviewed():raise RuntimeError('Unreviewed cached kit')
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceTests))
    report={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'network_calls':0,'credential_loads':0}
    (HERE/('SOURCE_OPTIMIZED.json'if sys.flags.optimize else'SOURCE_NORMAL.json')).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
