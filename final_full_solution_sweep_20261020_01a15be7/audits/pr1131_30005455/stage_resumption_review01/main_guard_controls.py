"""Actual wrapper CLI pre-bootstrap refusals; all effects blocked beforehand."""
from pathlib import Path
import hashlib, json, sys, socket, http.client, subprocess, urllib.request, os

ROOT=Path(__file__).resolve().parent
MODE='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
OUT=ROOT/'private'/('main_guards_'+MODE);OUT.mkdir(exist_ok=False)
source=(ROOT/'private/resume_known_unattempted_stage.py').read_bytes()
WS='cc3b78b9728f4dbc9b5f3a899e7d5029c872387ab5af989ecddd1feb04d5bf6a'
if hashlib.sha256(source).hexdigest()!=WS:raise RuntimeError('source')
path=OUT/'wrapper.py';path.write_bytes(source)
attempts=[]
def blocked(*a,**k):attempts.append('forbidden outside interface');raise RuntimeError('blocked')
socket.socket=blocked;socket.create_connection=blocked;socket.getaddrinfo=blocked
http.client.HTTPConnection=blocked;http.client.HTTPSConnection=blocked
urllib.request.urlopen=blocked;urllib.request.OpenerDirector.open=blocked
subprocess.run=blocked;subprocess.Popen=blocked;os.system=blocked;os.popen=blocked
ns={'__file__':str(path),'__name__':'actual_wrapper_prebootstrap_guards'}
exec(compile(source,str(path),'exec'),ns)
ops=OUT/'ops';ops.mkdir();(ops/'bootstrap.py').write_text('raise RuntimeError("unreviewed bootstrap must never execute")\n')
ns['OPS']=ops
results=[]
for case,flags,expected in [
    ('no_execute_flag',['--source-sha256',WS],'execution flag'),
    ('wrong_wrapper_hash',['--execute','--source-sha256','0'*64],'wrapper mismatch'),
    ('wrong_bootstrap_hash',['--execute','--source-sha256',WS],'bootstrap changed')]:
    sys.argv=[str(path),*flags,'--adoption-sha256','0'*64]
    try:ns['main']()
    except RuntimeError as e:
        if expected not in str(e):raise
        results.append({'case':case,'rejected':True,'message':str(e)})
    else:raise RuntimeError('CLI guard accepted '+case)
if attempts:raise RuntimeError('outside interface attempted')
(ROOT/('MAIN_GUARD_RESULTS_'+MODE+'.json')).write_text(json.dumps({'mode':MODE,'actual_wrapper_sha256':WS,'cases':results,'real_escape_attempts':attempts,'service_mutations':0},indent=2)+'\n')
print(json.dumps({'mode':MODE,'component_CLI_refusals':len(results),'service_mutations':0}))
