"""Authenticate the fresh v02 audit, independently replay it, and adjudicate math only."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');A=Path(__file__).resolve().parent;V=A/'corrected_math_adversary_02';D=A/'root_corrected_math_replay'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p):
    p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def bodymatch(p,row):
    got=pin(p);need(got['bytes']==row['bytes'] and got['sha256']==row['sha256'],'complete file equality');return got
def main():
    need(not sys.flags.optimize,'unoptimized adjudication')
    manifest=V/'ARTIFACT_MANIFEST.json';need(pin(manifest)['sha256']=='e19c5a188770d1a73c5ee0c03b03efa8832da287ce3dd42940f6741a89e7175b','announced full audit manifest')
    packet=json.loads(manifest.read_bytes());rows=packet['files'];need(len(rows)==228 and len({r['path'] for r in rows})==228,'nonvacuous full packet')
    verified=[bodymatch(V/x['path'],x) for x in rows]
    actual={str(p.relative_to(V)) for p in V.rglob('*') if p.is_file()}
    allowed_extras={'ARTIFACT_MANIFEST.json'}|{x for x in actual if x.startswith('captures/finalize_packet/')}
    need(actual=={r['path'] for r in rows}|allowed_extras,'whole packet physical domain')
    inputrows=json.loads((V/'INPUT_PINS.json').read_bytes());need(len(inputrows)==8,'eight exact original/current/source inputs')
    for row in inputrows:bodymatch(R/row['path'],row)
    proof=A/'CURRENT_CORRECTED_PROOF_v02.md';need(pin(proof)['sha256']=='d92a870709f5ce62440fa8a83313dd13790773f247e01cfb63c43c5ae8ea272a','exact repaired target')
    captures=[]
    for q in sorted((V/'captures').iterdir()):
        e=json.loads((q/'execution.json').read_bytes());s=json.loads((q/'started.json').read_bytes());req=json.loads((q/'request.json').read_bytes())
        need(e['actual_pid']==s['actual_pid'] and e['actual_pid']>0 and e['start_utc']==s['start_utc'],'actual captured PID/start')
        for label in ['stdout','stderr']:
            b=gzip.decompress((q/(label+'.gz')).read_bytes());need(len(b)==e[label+'_bytes'] and sha(b)==e[label+'_sha256'],'full logical native stream')
        need(gzip.decompress((q/'recorder_source.py.gz').read_bytes())==(V/'record_run.py').read_bytes(),'exact recorder source')
        for row in req.get('source_files',[]):
            matches=[p for p in q.glob('argv_source_*.gz') if sha(gzip.decompress(p.read_bytes()))==row['sha256']]
            need(bool(matches),'full archived requested source body')
        captures.append(dict(name=q.name,PID=e['actual_pid'],exit_code=e['exit_code'],execution=pin(q/'execution.json')))
    final=V/'captures/final_control_coverage';fe=json.loads((final/'execution.json').read_bytes());fq=json.loads((final/'request.json').read_bytes())
    need(fe['exit_code']==0 and fe['stderr_bytes']==0 and fq['argv']==['python3',str((V/'independent_exact_controls.py').relative_to(R))],'actual authoritative reviewer control run')
    # Reviewer interpreter flags/version were not pinned. Explicit check/raise
    # predicates do not rely on optimization-sensitive Python assert statements.
    import ast
    control_tree=ast.parse((V/'independent_exact_controls.py').read_bytes())
    need(not any(isinstance(x,ast.Assert) for x in ast.walk(control_tree)),'reviewer checks are not optimization-sensitive asserts')
    checkfn=next(x for x in control_tree.body if isinstance(x,ast.FunctionDef) and x.name=='check')
    need(any(isinstance(x,ast.Raise) and isinstance(x.exc,ast.Call) and isinstance(x.exc.func,ast.Name) and x.exc.func.id=='AssertionError' for x in ast.walk(checkfn)),'explicit failed-check exception')
    original=V/'independent_exact_controls.py';need(any(x['sha256']==pin(original)['sha256'] for x in fq['source_files']),'actual final source equality')
    expected=json.loads((V/'RESULTS.json').read_bytes());need(expected['assertions']==46068 and expected['orbit_edge_evaluations']==0,'correct final assertion coverage')
    need(json.loads(gzip.decompress((final/'stdout.gz').read_bytes()))==expected,'complete final expected native output')
    D.mkdir(exist_ok=False);source=D/'independent_exact_controls.py';source.write_bytes(original.read_bytes());source.chmod(0o444)
    (D/'source.gz').write_bytes(gzip.compress(source.read_bytes(),mtime=0));(D/'recorder.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0))
    req=dict(argv=['/opt/homebrew/bin/python3','-E','-B',str(source)],cwd=str(D),UTC=utc(),source=pin(source),recorder=pin(__file__),expected=pin(V/'RESULTS.json'),automatic_retry=False)
    (D/'request.json').write_text(json.dumps(req,indent=2)+'\n')
    child=subprocess.Popen(req['argv'],cwd=D,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    started=dict(actual_PID=child.pid,start_UTC=utc());(D/'started.json').write_text(json.dumps(started,indent=2)+'\n');out,err=child.communicate(timeout=55)
    streams={}
    for label,b in [('stdout',out),('stderr',err)]:
        p=D/(label+'.gz');p.write_bytes(gzip.compress(b,mtime=0));streams[label]=dict(stored=pin(p),logical_bytes=len(b),logical_sha256=sha(b))
    e=dict(**started,end_UTC=utc(),exit_code=child.returncode,parent_reaped=True,streams=streams);(D/'execution.json').write_text(json.dumps(e,indent=2)+'\n')
    need(child.returncode==0 and not err and json.loads(out)==expected==json.loads((D/'RESULTS.json').read_bytes()),'independent ROOT replay full expected output')
    for row in rows:bodymatch(V/row['path'],row)
    result=dict(status='ROOT_ACCEPTS_PR301_CORRECTED_V02_MATHEMATICS_ONLY',UTC=utc(),actual_ROOT_PID=os.getpid(),source=pin(__file__),
       original_head='125d90fa3f5a4f90b813fec7a7c0f1918914d885',original_status='claimed_solved',original_author_budget='1/5',
       reviewer_runtime_qualification='Final reviewer argv is python3 without interpreter-version or optimization-flag pins; explicit check/raise controls contain no assert statements. ROOT separately reproduces the exact source under native /opt/homebrew/bin/python3 -E -B.',
       current_proof=pin(proof),fresh_report=pin(V/'REPORT.md'),fresh_derivations=pin(V/'DERIVATIONS.md'),fresh_manifest=pin(manifest),
       complete_packet_files_verified=verified,complete_native_review_captures=captures,ROOT_replay=pin(D/'execution.json'),actual_ROOT_control_PID=child.pid,
       ROOT_manual_adjudication='Full current proof and independent derivations read. Finite construction, exact predicates, generic joint rational witness, maximal portions, collar winding, all-end LP-to-APS classification, genus branches and connected-factor proof checked; two required logical/domain repairs are explicit in v02. No unresolved mathematical gap under credited established theorems.',
       repaired_original_printed_APS_sufficiency_reference=True,repaired_original_boundary_compact_core_domain=True,
       all_original_snapshots_and_historical_failed_attempts_preserved=True,mathematical_acceptance=True,mathematical_discovery_percent=100,
       priority_acceptance=False,priority_percent=0,workflow_percent=20,preprint_or_full_software_or_human_peer_review_certification=False,
       original_v01_not_final_accepted_proof=True,checkpoint039_is_separate_historical_partial_snapshot=True,
       strongest_result='Terminating theoretical complete-invariant algorithm including zero/disconnected/isolated cases, under the cited PPP/APS/LP theorems; finite control experiments only supplement the proof.',
       exact_remaining_gap='Deep priority audit, then preprint and two sequential new package adversaries with repairs, Zenodo, single tracker row, original-head integration and final acceptance.',
       no_git_shared_control_or_service_mutation=True,overall_descending_goal_complete=False)
    p=A/'ROOT_CORRECTED_MATHEMATICAL_ACCEPTANCE.json';p.write_text(json.dumps(result,indent=2)+'\n');p.chmod(0o444)
    print(json.dumps(dict(status=result['status'],fresh_review_captures=len(captures),packet_files=len(verified),actual_ROOT_control_PID=child.pid,result=pin(p)),indent=2))
if __name__=='__main__':main()
