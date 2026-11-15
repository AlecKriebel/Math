"""Run only two inspected native functions from an immutable isolated copy."""
from pathlib import Path
from hashlib import sha256
import importlib.util
import json

native=Path(__file__).with_name('native-oracle-controls.py')
spec=importlib.util.spec_from_file_location('native_oracle_subset',native)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
branch=module.source_branch_controls()
counter=module.log_base_counterexample()
print(json.dumps({'verdict':'PASS','native_copy_SHA256':sha256(native.read_bytes()).hexdigest(),
 'functions_called':['source_branch_controls','log_base_counterexample'],
 'source_branch_controls':branch,'exact_counts':dict(module.STATS),
 'literal_v1_volume_counterexample':counter,
 'not_called':['all_small','main','run_all.py'],
 'limitations':'Bounded brute structural reference; no fast implementation or asymptotic certification.',
 'writes':[]},indent=2))
