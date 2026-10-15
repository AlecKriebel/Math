"""Execute captured author tests with all mutable state confined to this review."""
from pathlib import Path
import sys, types, unittest, hashlib, json
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/alec/Documents/Math')
AUDIT = ROOT/'draft_pr_claimed_solved_600_700_20261012/audits/pr623_30001184'
AUTHOR = AUDIT/'reviews/native_transport_author'
SNAP = HERE/'tmp/inputs'/AUTHOR.relative_to(ROOT)
TESTDIR = HERE/'tmp/supplied'
TESTDIR.mkdir(parents=True,exist_ok=True)
(TESTDIR/'tmp').mkdir(exist_ok=True)
for name in ['native_transport.py','run_native_transport.py','native_shape.json']:
    (TESTDIR/name).write_bytes((SNAP/name).read_bytes())
def module(name, file, source):
    m = types.ModuleType(name)
    m.__file__ = str(file)
    sys.modules[name] = m
    exec(compile(source, str(file),'exec',dont_inherit=True),m.__dict__)
    return m
nt_source = (SNAP/'native_transport.py').read_bytes()
if hashlib.sha256(nt_source).hexdigest() != '10525be2c736213116173c2bcc75b32e32c0e6addd5a2c123f23efa812f01af8':
    raise RuntimeError('adapter snapshot differs')
nt = module('native_transport', TESTDIR/'native_transport.py',nt_source)
bootstrap = module('run_native_transport',TESTDIR/'run_native_transport.py',(SNAP/'run_native_transport.py').read_bytes())
original = module('test_native_transport',TESTDIR/'test_native_transport.py',(SNAP/'test_native_transport.py').read_bytes())
repairs = module('test_repairs',TESTDIR/'test_repairs.py',(SNAP/'test_repairs.py').read_bytes())
if __name__ == '__main__':
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(original),unittest.defaultTestLoader.loadTestsFromModule(repairs)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
