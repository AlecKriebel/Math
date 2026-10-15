"""Frozen author suites; private scratch only and no real network."""
from pathlib import Path
from datetime import datetime,timezone
import sys,types,unittest,hashlib,json
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
AUDIT=HERE.parent.parent
AUTHOR=AUDIT/'reviews/native_transport_author'
SNAP=HERE/'tmp/inputs'/AUTHOR.relative_to(ROOT)
TESTDIR=HERE/'tmp/supplied'
TESTDIR.mkdir(parents=True,exist_ok=True);(TESTDIR/'tmp').mkdir(exist_ok=True)
binding=json.loads((HERE/'INPUT_BINDING.json').read_bytes())['inputs']
def source(name):
    data=(SNAP/name).read_bytes(); expected=binding[str((AUTHOR/name).relative_to(ROOT))]
    if len(data)!=expected['size'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:raise RuntimeError('Snapshot drift '+name)
    return data
for name in ('native_transport.py','run_native_transport.py','native_shape.json'):(TESTDIR/name).write_bytes(source(name))
def module(name):
    m=types.ModuleType(name);m.__file__=str(TESTDIR/(name+'.py'));sys.modules[name]=m
    exec(compile(source(name+'.py'),m.__file__,'exec',dont_inherit=True),m.__dict__)
    return m
nt=module('native_transport')
bootstrap=module('run_native_transport')
original=module('test_native_transport')
repairs=module('test_repairs')
annotations=module('test_file_annotations_wire')
if __name__=='__main__':
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in (original,repairs,annotations))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'checked_utc':datetime.now(timezone.utc).isoformat(),'optimization':sys.flags.optimize,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'network_calls':0}
    (HERE/('SUPPLIED_OPTIMIZED.json' if sys.flags.optimize else 'SUPPLIED_NORMAL.json')).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
