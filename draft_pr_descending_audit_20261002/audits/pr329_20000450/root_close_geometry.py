"""Root closure of a stable independent namespace using actual replay records."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, stat
A=Path(__file__).resolve().parent;N=A/'geometry'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(A)), 'bytes':len(b),'sha256':sha(b),'mode':oct(stat.S_IMODE(p.stat().st_mode))}
def science(b):
    lines=[]
    for line in b.decode('utf-8').splitlines():
        if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+\+00:00',line):continue
        line=re.sub(r' native_utc \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+\+00:00$','',line)
        lines.append(line)
    return ('\n'.join(lines)+'\n').encode()
assert not (A/'ROOT_GEOMETRY_CLOSURE.json').exists()
entries=[];directories=[]
for p in sorted(N.rglob('*')):
    if any(x in {'.runtime','__pycache__'} for x in p.relative_to(N).parts):continue
    assert not p.is_symlink(),str(p)
    if p.is_file():entries.append(pin(p))
    elif p.is_dir():directories.append({'path':str(p.relative_to(A)),'mode':oct(stat.S_IMODE(p.stat().st_mode))})
replays=[]
for program,name in [('validate_candidate_geometry','geometry_external001'),('independent_source_geometry','geometry_source_external001'),('independent_quotient_geometry','geometry_quotient_external001')]:
    D=A/'root_runs_private'/name;j=json.loads((D/'execution.json').read_bytes())
    assert j['exit_code']==0 and (D/'stderr.bin').read_bytes()==b''
    for k in ['stdout','stderr']:
        b=(D/(k+'.bin')).read_bytes();assert len(b)==j[k+'_bytes'] and sha(b)==j[k+'_sha256']
    assert j['programs']==[dict(path=str(N/(program+'.py')),bytes=(N/(program+'.py')).stat().st_size,sha256=sha((N/(program+'.py')).read_bytes()))]
    own=json.loads((N/(program+'.run.json')).read_bytes());assert own['exit_code']==0
    assert (N/(program+'.stderr.txt')).read_bytes()==b''
    assert science((D/'stdout.bin').read_bytes())==science((N/(program+'.stdout.txt')).read_bytes())
    replays.append({'program':pin(N/(program+'.py')),'actual_execution':j,'execution_receipt':pin(D/'execution.json'),
        'mathematical_stdout_equal_after_only_native_UTC_metadata_removal':True,
        'mathematical_stdout_sha256':sha(science((D/'stdout.bin').read_bytes()))})
manifest={'utc':utc(),'namespace':'geometry','files':entries,'directories':directories,
    'excluded': ['geometry/.runtime/**','geometry/**/__pycache__/**'],
    'whole_completed_namespace_pinned':True,'historical_failed_and_terminated_attempts_retained':True}
M=A/'ROOT_GEOMETRY_NAMESPACE_MANIFEST.json';M.write_text(json.dumps(manifest,indent=2)+'\n')
j={'utc':utc(),'status':'PASS_ROOT_EXTERNALLY_CLOSED_GEOMETRY_FAMILY_ONLY',
    'namespace_manifest':pin(M),'root_reading_scope':[
        'Full operative primary source page including all four remarks; text and pixels',
        'Full source-only baseline, pre-candidate derivation, first candidate assessment and final report',
        'Full current three programs, original successful full stdout/stderr and native run metadata',
        'Full externally replayed current programs stdout/stderr and actual execution records',
        'Full computation-attempt explanation and final family summary; abandoned historical programs are retained and hashed, not used as proof'],
    'native_external_replays':replays,'geometry_family_percent':100,
    'strongest_verified_result':'Source-matched characteristic-zero normalized pentagonal pencil, exact elliptic parameter range, irreducibility/genus, both birational compositions and origin, infinity subgroup and actual Tate quadratic twist.',
    'exact_remaining_geometry_gap':'None identified within the specified normalized claim.',
    'not_closed_by_this_gate':['Full division polynomial and completeness','Full-level modular cover, specialized field equality and Galois module','Priority','Preprint reviews','Merge and publication'],
    'entire_candidate_accepted':False,'publication_ready':False,'original_author_turn_count':'1/5'}
(A/'ROOT_GEOMETRY_CLOSURE.json').write_text(json.dumps(j,indent=2)+'\n')
for e in entries:
    assert pin(A/e['path'])==e
print(json.dumps({'utc':j['utc'],'status':j['status'],'files':len(entries),'external_replays':len(replays),'geometry_percent':100,'entire_candidate_accepted':False},indent=2))
