"""Actual prepare/build main replay on a copy; no Git operation allowed."""
from pathlib import Path
import contextlib,datetime,hashlib,importlib.util,io,json,shutil,subprocess,types
HERE=Path(__file__).resolve().parent;A=HERE.parents[1];W=HERE/'scratch_local/build_copy'
if W.exists():shutil.rmtree(W)
for e in json.loads((HERE/'INPUT_FREEZE.json').read_text())['files']:
    dst=W/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/e['path'],dst)
P=W/'publication';events=[]
def load(n):
    spec=importlib.util.spec_from_file_location('r2_rebuild_'+n,P/(n+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
prep=load('prepare_package');build=load('build_package');original_run=subprocess.run
def intercepted(args,**kwargs):
    if args[0]=='git':
        if args!=['git','check-ignore','--no-index','-z','--stdin']:raise RuntimeError('Forbidden Git operation')
        events.append('mocked_ignore_classification_all_scratch_candidates_ignored')
        return types.SimpleNamespace(returncode=0,stdout=kwargs['input'],stderr=b'')
    if len(args)>2 and str(args[-1])==str(P/'prepare_package.py'):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):prep.main()
        events.append('actual_prepare_main_on_copy');return types.SimpleNamespace(returncode=0,stdout=output.getvalue(),stderr='')
    if args[0]=='pdfinfo' or len(args)>2 and str(args[-1])==str(P/'verification/verify.py'):
        events.append('actual_pdfinfo' if args[0]=='pdfinfo' else 'actual_portable_verify_main_on_copy')
        return original_run(args,**kwargs)
    raise RuntimeError('Unexpected process in copied build '+repr(args))
proxy=types.SimpleNamespace(run=intercepted);prep.subprocess=proxy;build.subprocess=proxy
output=io.StringIO()
with contextlib.redirect_stdout(output):build.main()
(HERE/'BUILD_REPRODUCTION_STDOUT.txt').write_text(output.getvalue())
checks=[]
for n in ['Johnson_Filtration_Multiplicity_Note_v1.0.pdf','Johnson_Filtration_Multiplicity_Verification_v1.0.zip']:
    data=(P/n).read_bytes();same=data==(A/'publication'/n).read_bytes()
    if not same:raise RuntimeError('Copied rebuilt artifact differs '+n)
    checks.append({'name':n,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'exact_original_bytes':True})
(HERE/'BUILD_REPRODUCTION_RESULTS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifact_checks':checks,'events':events,'scope':'Unmodified actual prepare_package.main and build_package.main on frozen-input copies. Only git check-ignore is replaced by an in-memory classifier returning all scratch candidates ignored; explicit frozen members are nevertheless restored by actual preparation. No real Git command/object/ref/index operation. Actual pdfinfo and portable verifier run on the copy. Exact same cached-compiler PDF reproduction is recorded separately.'},indent=2)+'\n')
print('Actual copied prepare/build reproduced exact PDF and ZIP')
