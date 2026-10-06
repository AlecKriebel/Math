"""ROOT authentication of the additive custody erratum; no mutation replay."""
from pathlib import Path
import datetime, gzip, hashlib, json, os
A=Path(__file__).resolve().parent; P=A.parent.parent; R=P.parent
W=A/'checkpoint041_count_erratum_09'; checked=[]
def ck(x,m):
    if not x: raise RuntimeError(m)
    checked.append(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=p.stat().st_mode&0o777)
def auth(z,mode=True):
    p=Path(z['path']); b=p.read_bytes()
    ck(len(b)==z['bytes'] and sha(b)==z['sha256'],'complete body:'+str(p))
    if mode: ck((p.stat().st_mode&0o777)==z['mode'],'mode:'+str(p))
    return b
terminal=(W/'TERMINAL_CLOSURE.json').read_bytes()
ck(sha(terminal)=='b34aadfc9754c3ce93b59a040b27d73322cb4c292025d52312593699efa646e6','pinned terminal closure')
t=json.loads(terminal); seen=set()
for z in t['all_files_except_this_terminal_record']:
    p=Path(z['path']); rel=str(p.relative_to(W))
    ck(rel not in seen and not p.is_symlink(),'unique owned terminal path:'+rel); seen.add(rel); auth(z)
files={str(p.relative_to(W)) for p in W.rglob('*') if p.is_file()}
ck(files==seen|{'TERMINAL_CLOSURE.json'} and len(files)==36,'exact36 closed file domain')
ck(sum(p.stat().st_size for p in W.rglob('*') if p.is_file())==142871,'closed complete byte total')
ck(all((p.stat().st_mode&0o777)==0o444 for p in W.rglob('*') if p.is_file()),'closed files444')
ck(all((p.stat().st_mode&0o777)==0o555 for p in [W,*[q for q in W.rglob('*') if q.is_dir()]]),'closed directories555')
results=json.loads((W/'RESULTS.json').read_bytes()); verdict=json.loads((W/'VERDICT.json').read_bytes())
ck(verdict['status']=='PASS_ADDITIVE_PR301_HELD_COUNT_AND_PROVENANCE_ERRATUM' and not verdict['unresolved_issues'] and not verdict['execution_authority_granted'],'narrow nonauthorizing verdict')
for z in results['full_read_pins']: auth(z)
for z in results['ROOT_predicate_source_pins']:
    s=auth(z['source']).decode()
    ck(".endswith('/SHARED_GIT_WINDOW_STATUS.json')" not in s,'no broad suffix exclusion in actual ROOT predicates')
    for line in z['literal_control_predicate_lines']: ck(s.splitlines()[line['line']-1]==line['text'],'exact literal ROOT exclusion line')
rows=json.loads(auth(results['baseline']))['files']; paths={z['path'] for z in rows}
ck(len(rows)==len(paths)==41253 and sum(z['bytes'] for z in rows)==1273600002,'ROOT independently parsed full baseline domain')
S=P/'SHARED_GIT_WINDOW_STATUS.json'; ck(str(S) not in paths,'live control absent from baseline')
owned=set(json.loads((A/'checkpoint_041_preparation/CONTENT_PLAN.json').read_bytes())['allowed_paths'])
ck(len(owned)==97 and not any(str(Path(z['path']).relative_to(R)) in owned for z in rows),'checkpoint97 has zero held overlap')
fixtures=[z for z in rows if z['path'].endswith('/SHARED_GIT_WINDOW_STATUS.json')]
ck(fixtures==results['exact19_suffix_fixture_entries'] and len(fixtures)==19 and sum(z['bytes'] for z in fixtures)==10288,'exact19 historical fixtures independently reproduced')
ck(len(rows)-len(fixtures)==41234 and sum(z['bytes'] for z in rows)-10288==1273589714,'actual06 subset arithmetic')
actual=json.loads(auth(results['actual041_ROOT_acceptance']))
ck(actual['known_nonowned_held_count']==41253 and actual['all_known_nonowned_held_complete_bodies_modes_preserved'] and len(actual['all_actual_native_captures_authenticated'])==844,'accepted actual041 complete held coverage')
native=[]
for C in sorted((W/'captures').iterdir()):
    req=json.loads((C/'request.json').read_bytes()); start=json.loads((C/'started.json').read_bytes()); e=json.loads((C/'execution.json').read_bytes())
    ck(all(e[k]==v for k,v in req.items()),'request preserved in actual envelope:'+C.name)
    ck(e['actual_PID']==start['actual_PID'] and e['full_stream_capture_complete'] and e['parent_reaped'] and not e['capture_exception'],'whole actual native envelope:'+C.name)
    ck(e['start_UTC']<=e['end_UTC'],'actual time ordering:'+C.name)
    streams={}
    for n in ('stdout','stderr'):
        z=e[n]; b=gzip.decompress(auth(z['archive'],mode=False)); streams[n]=b
        ck(len(b)==z['logical_bytes'] and sha(b)==z['logical_sha256'],'complete native stream:'+C.name+':'+n)
    for z in e['prelaunch_sources']:
        b=gzip.decompress(auth(z['archive'],mode=False)); live=auth(z['input'],mode=False)
        ck(b==live,'complete actual prelaunch source:'+C.name)
    expected=1 if C.name=='count-provenance' else 0
    ck(e['exit_code']==expected,'original failed attempt preserved:'+C.name)
    if expected: ck(b'Traceback' in streams['stderr'] and not streams['stdout'],'legacy schema failure explicitly preserved')
    else: ck(not streams['stderr'],'actual successful empty stderr:'+C.name)
    if C.name=='count-provenance-v02':
        out=json.loads(streams['stdout'])
        ck(all(out[k]==results[k] for k in out),'whole v02 result stdout bound to saved results')
        ck(out['actual_erratum_driver_PID']==e['actual_PID']==91296 and out['explicit_predicates']==60,'actual successful narrow provenance checks')
    native.append(dict(name=C.name,PID=e['actual_PID'],exit_code=e['exit_code'],execution=pin(C/'execution.json')))
out=dict(status='ROOT_ACCEPTS_ADDITIVE_PR301_CUSTODY_COUNT_ERRATUM09',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_ROOT_PID=os.getpid(),terminal=pin(W/'TERMINAL_CLOSURE.json'),erratum=pin(W/'ERRATUM.md'),verdict=pin(W/'VERDICT.json'),checks=checked,native_captures=native,baseline_files=41253,baseline_bytes=1273600002,reviewer06_files=41234,reviewer06_bytes=1273589714,reviewer06_omitted_mock_fixture_count=19,reviewer08_and_actual_ROOT_full_files=41253,full_held_bodies_not_reread=True,old_closed_errors_preserved=True,actual_Git_service_writes_not_repeated=True,scientific_and_priority_acceptance_unchanged=True,publication_authority=False,estimate_percent=100)
path=A/'ROOT_COUNT_ERRATUM09_ACCEPTANCE.json'
with path.open('x') as f: json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
path.chmod(0o444)
print(json.dumps(dict(status=out['status'],ROOT_PID=os.getpid(),checks=len(checked),acceptance=pin(path))))
