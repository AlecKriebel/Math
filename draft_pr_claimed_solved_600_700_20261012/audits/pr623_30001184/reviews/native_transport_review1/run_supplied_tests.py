"""Run supplied tests with all test writes redirected into this review."""
import importlib.util
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'native_transport_author'
sys.path.insert(0, str(AUTHOR))
spec = importlib.util.spec_from_file_location('supplied_native_tests', AUTHOR / 'test_native_transport.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.nt.HERE = HERE
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(module))
raise SystemExit(not result.wasSuccessful())
