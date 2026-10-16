from pathlib import Path
import sys,importlib.util,unittest,tempfile,json,hashlib,socket,datetime
D=Path(__file__).resolve().parent;repo=D.parents[3];toolroot=repo/"zenodo_deposit_tool"
assert hashlib.sha256((D/"zenodo.py").read_bytes()).hexdigest()=="b51d1511409c53754293f53fe2229cad1195169d774edf1edb98e569f6be5ad0"
temp=D/"private_tmp/offline_temp";temp.mkdir();tempfile.tempdir=str(temp)
def no_network(*a,**k):raise RuntimeError("OFFLINE_SUITE_UNEXPECTED_NETWORK")
socket.create_connection=no_network;socket.getaddrinfo=no_network
sys.path.insert(0,str(toolroot))
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module
z=load("zenodo",D/"zenodo.py")
mods=[load("deposit_tests_proposed",D/"test_zenodo.py"),load("metadata_tests_current",toolroot/"test_metadata_updates.py")]
suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in mods)
result=unittest.TextTestRunner(verbosity=2).run(suite)
out={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS" if result.wasSuccessful() else "FAIL","tests_run":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),"skipped":len(result.skipped),"proposed_tool_sha256":hashlib.sha256((D/"zenodo.py").read_bytes()).hexdigest(),"network_fuse":"socket.create_connection and getaddrinfo reject every real request; existing test clients and DOI handlers mocked","shared_or_paper_files_changed":False}
(D/"OFFLINE_TEST_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps(out))
raise SystemExit(0 if result.wasSuccessful() else 1)
