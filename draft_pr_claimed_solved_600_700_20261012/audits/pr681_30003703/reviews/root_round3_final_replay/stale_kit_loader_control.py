#!/usr/bin/env python3
"""Read-only diagnostic exact-source/pyc separation probe in a toy root only."""
import contextlib,hashlib,importlib._bootstrap_external,importlib.util,io,json,shutil,sys,types
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent
T=R/'tmp'/('stale-kit-optimized'if sys.flags.optimize else'stale-kit-normal');T.mkdir(parents=True,exist_ok=True)
F=T/'toyrepo/program/audits/pr681_30003703';F.mkdir(parents=True,exist_ok=True)
K=T/'toyrepo/zenodo_deposit_tool/zenodo.py';K.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(A.parents[2]/'zenodo_deposit_tool/zenodo.py',K)
shutil.copy2(A/'root_zenodo_readback.py.before_source_capture_repair',F/'root_zenodo_readback.py')
K.parent.joinpath('__pycache__').mkdir(exist_ok=True)
st=K.stat();source="raise RuntimeError('STALE_KIT_PYC_WAS_EXECUTED_IN_TOY_ROOT')"
cache=Path(importlib.util.cache_from_source(str(K)))
cache.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(compile(source,str(K),'exec'),int(st.st_mtime),st.st_size))
m=types.ModuleType('exact_root_readback_probe');m.__file__=str(F/'root_zenodo_readback.py')
exec(compile((F/'root_zenodo_readback.py').read_bytes(),m.__file__,'exec'),m.__dict__)
argv=sys.argv;sys.argv=['root_zenodo_readback.py','--phase','staged','--receipt','FAKE.json']
try:
 try:
  with contextlib.redirect_stdout(io.StringIO()):m.main()
 except RuntimeError as e:
  if str(e)!='STALE_KIT_PYC_WAS_EXECUTED_IN_TOY_ROOT':raise
  result={'status':'REPRODUCED_EXECUTED_BYTECODE_DESPITE_PINNED_SOURCE','message':str(e),'kit_source_sha256':hashlib.sha256(K.read_bytes()).hexdigest(),'root_readback_sha256':hashlib.sha256((F/'root_zenodo_readback.py').read_bytes()).hexdigest(),'network_or_credentials_accessed':False,'toy_fixture_only':True}
 else:raise ValueError('unexpected success')
finally:sys.argv=argv
print(json.dumps(result,indent=2))
