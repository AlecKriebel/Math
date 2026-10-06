"""Reproduce frozen finite controls in separate writable copies, never originals."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,stat,subprocess,sys
if sys.flags.optimize:raise RuntimeError('Unoptimized reproduction required.')
A=Path(__file__).resolve().parent;R=A.parent.parent.parent
T=A/'snapshot/unsolved_math_prioritization/attempts/30003508';W=A/'root_reproduction'
assert not W.exists();W.mkdir();P=R/'.venv/bin/python'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
    p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
copies=[]
for rel in ['verify_turn1.py','verify_turn2.py','review/independent_controls.py']:
    src=T/rel;dst=W/src.name;dst.write_bytes(src.read_bytes());dst.chmod(0o644)
    copies.append(dict(original=pin(src),copy=pin(dst),whole_body_equal=src.read_bytes()==dst.read_bytes()))
for stem in ['verify_turn1.py','verify_turn2.py']:
    assert (T/stem).read_bytes()==(T/'review/author_replay'/stem).read_bytes()
ops=[]
def run(label,argv):
    n=W/label;n.mkdir();start=utc()
    proc=subprocess.Popen(argv,cwd=W,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    j=dict(argv=argv,cwd=str(W),actual_PID=proc.pid,start_UTC=start,
        root_driver=pin(Path(__file__).resolve()),interpreter=pin(P.resolve()),
        program_sources=[pin(Path(x)) for x in argv if x.endswith('.py') and Path(x).is_file()])
    (n/'started.json').write_text(json.dumps(j,indent=2)+'\n')
    out,err=proc.communicate(timeout=55)
    for k,b in [('stdout',out),('stderr',err)]:
        (n/(k+'.bin')).write_bytes(b);j[k+'_bytes']=len(b);j[k+'_sha256']=sha(b)
    j.update(end_UTC=utc(),exit_code=proc.returncode)
    (n/'execution.json').write_text(json.dumps(j,indent=2)+'\n');ops.append(j)
    assert proc.returncode==0 and not err,(label,proc.returncode)
    return json.loads(out)
runtime=run('runtime',[str(P),'-E','-B','-c',"import json,sys,sympy; print(json.dumps(dict(version=sys.version,optimized=sys.flags.optimize,sympy_version=sympy.__version__,sympy_file=sympy.__file__)))"])
assert runtime['sympy_version']=='1.14.0' and runtime['optimized']==0
counts=[]
for label,name,saved,key in [('author1','verify_turn1.py','TURN_1_CHECKS.json','exact_checks'),
    ('author2','verify_turn2.py','TURN_2_CHECKS.json','exact_checks'),
    ('old_independent','independent_controls.py','review/independent_output.json','independent_exact_assertions')]:
    actual=run(label,[str(P),'-E','-B',str(W/name)])
    assert actual==json.loads((T/saved).read_bytes()),'Original finite-control receipt differs.'
    if label in ['author1','author2']:
        assert (W/saved).read_bytes()==(T/saved).read_bytes()
    counts.append(dict(label=label,count=actual[key],saved_output=pin(T/saved)))
assert counts[0]['count']+counts[1]['count']==53 and counts[2]['count']==1905
for e in copies:
    assert pin(e['original']['path'])==e['original'] and pin(e['copy']['path'])==e['copy']
receipt=dict(status='PASS_ROOT_PR302_ORIGINAL53_AND1905_FINITE_CONTROLS_REPRODUCED',UTC=utc(),
    copies=copies,runtime=runtime,native_captures=ops,counts=counts,
    exact_JSON_and_author_saved_output_bytes_reproduced=True,
    no_original_snapshot_or_Git_or_index_or_service_write=True,
    finite_controls_do_not_prove_elliptic_or_statistical_theorems=True,
    independent_new_mathematical_review_still_required=True,
    math_review_percent=50,priority_percent=0,workflow_percent=20)
(A/'ROOT_ORIGINAL_CONTROL_REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write(utc()+' — ROOT reproduced unchanged author53 controls and historical independent1905 controls in exact writable copies under unoptimized Python/SymPy1.14.0. Full actual PID/argv/cwd/UTC/streams/source/interpreter custody retained; originals unchanged. Finite algebra is supplementary only; three NEW independent analytical families completing. Mathreview50%,priority0%,workflow20%.\n')
print(json.dumps(dict(status=receipt['status'],counts=counts,native_runs=len(ops),runtime=runtime),indent=2))
