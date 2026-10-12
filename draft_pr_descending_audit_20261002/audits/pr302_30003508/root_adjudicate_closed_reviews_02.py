"""ROOT literal custody and mathematical adjudication; no external actions."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, sys
A=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'Literal file required '+str(p))
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def match(row,mode=False):
    p=Path(row['path']);actual=pin(p)
    require(all(actual[k]==row[k] for k in ('bytes','sha256')),'Whole body differs '+str(p))
    if mode:require(actual['mode']==row['mode'],'Mode differs '+str(p))
    return p
def stream(row):
    p=match(row['stored']);b=gzip.decompress(p.read_bytes())
    require(len(b)==row['logical_bytes'] and sha(b)==row['logical_sha256'],'Full logical stream differs')
    return b
def time(s):
    d=datetime.fromisoformat(s);require(d.tzinfo is not None,'Timezone absent');return d
def executable(row):
    p=Path(row.get('resolved_path',str(Path(row['path']).resolve())))
    require(p==Path(row['path']).resolve(),'Executable resolution differs')
    actual=pin(p);require(all(actual[k]==row[k] for k in ('bytes','sha256','mode')),'Executable body differs')
def closure(v,msha,ssha,expected):
    m=v/'OUTPUT_MANIFEST.json';s=v/'CLOSURE_SEAL.json'
    require(pin(m)['sha256']==msha and pin(s)['sha256']==ssha,'External closure anchors differ')
    doc=load(m);rows=doc.get('files',doc.get('payload_files'))
    require(len(rows)+2==expected,'Expected closed size differs')
    paths={str(match(r,True)) for r in rows}|{str(m),str(s)}
    members=[v]+list(v.rglob('*'));files=[];dirs=[]
    for p in members:
        require(not p.is_symlink(),'Closure symlink')
        if p.is_file():require(stat.S_IMODE(p.stat().st_mode)==0o444,'Closure file mutable');files.append(p)
        elif p.is_dir():require(stat.S_IMODE(p.stat().st_mode)==0o555,'Closure dir mutable');dirs.append(p)
        else:raise RuntimeError('Nonregular closure')
    require({str(p) for p in files}==paths,'Literal closure inventory differs')
    require(sum(p.stat().st_blocks*512 for p in members)<20_000_000,'Closure capacity differs')
    match(load(s)['manifest'],True)
    return dict(namespace=str(v),files=[pin(p) for p in sorted(files)],directories=len(dirs),manifest=pin(m),seal=pin(s))
def native(p,outer_schema):
    x=load(p);q=load(p.parent/'request.json');start=load(p.parent/'started.json')
    require(all(x[k]==w for k,w in q.items()),'Actual request/result differs')
    if outer_schema=='science':
        pid=x['actual_child_PID'];t0=x['requested_UTC'];t1=x['started_UTC'];t2=x['completed_UTC']
        require(start['actual_child_PID']==pid and start['argv']==x['argv'] and start['cwd']==x['cwd'],'Actual start identity differs')
        executable(x['interpreter']);copies=x['sources_before']
        pairs=[(r['original'],r['stored']) for r in copies]
    else:
        pid=x['actual_PID'];t0=x['requested_UTC'];t1=x['start_UTC'];t2=x['end_UTC']
        require(start['actual_PID']==pid and start['start_UTC']==t1 and not x['timed_out'],'Actual operator start/timeout differs')
        executable(x['resolved_interpreter']);pairs=[(r['input'],r['stored_full_source']) for r in x['prelaunch_full_sources']]
    require(type(pid)==int and pid>0 and type(x['actual_launcher_PID'])==int and x['actual_launcher_PID']>0,'Actual PID missing')
    require(time(t0)<=time(t1)<=time(t2),'Actual UTC order differs')
    sources=[]
    for original,stored in pairs:
        b=gzip.decompress(match(stored).read_bytes());require(len(b)==original['bytes'] and sha(b)==original['sha256'],'Actual prelaunch full source differs')
        require(match(original).read_bytes()==b,'Current source differs from archived body')
        sources.append(dict(historical_input=original,current_input=pin(original['path']),full_archive=pin(stored['path'])))
    out=stream(x['stdout']);err=stream(x['stderr'])
    return dict(receipt=pin(p),actual_PID=pid,actual_launcher_PID=x['actual_launcher_PID'],argv=x['argv'],cwd=x['cwd'],UTC_interval=[t0,t1,t2],exit_code=x['exit_code'],sources=sources,stdout_bytes=len(out),stderr_bytes=len(err))
def main():
    require(not sys.flags.optimize,'Optimization forbidden')
    v=A/'preprint_adversary_02';o=A/'publication_operations_adversary_01';f=A/'preprint_package_v02'
    science=closure(v,'7396e13a35f6f9e2bab4d02906aed29f8aa8dcb9080717a16136b073eb75e8bf','3d37aad65b6363c3392e87fd531779f1ea42f1b58b65df6fede3b687938ac95a',492)
    operations=closure(o,'3ed73ed712c260eb51fdf6f1ade9e92a2bb845deba74256b37ea24bb006fc739','750eb9d926a1b0e3e4176be188edef7fb4759a65e2e114ac96a810caa82e7327',32)
    cm=f/'SECOND_CANDIDATE_MANIFEST.json';require(pin(cm)['sha256']=='b38a09c6768e11c2954892cdaa345a485557082c464d950f573a945f48b5ec71','Candidate differs')
    for r in load(cm)['files']:match(r,True)
    index=load(v/'SOURCE_ARCHIVE_INDEX.json');require(len(index['complete_body_copies'])==301,'Source archive count differs')
    for r in index['complete_body_copies']:
        b=gzip.decompress(match(r['complete_copy']).read_bytes())
        require(b==match(r['original']).read_bytes() and len(b)==r['logical_bytes'] and sha(b)==r['logical_sha256'],'Full source archive differs')
    for r in index['unredistributed_external_binary_anchors']:executable(r['input'])
    runs=[native(p,'science') for p in sorted((v/'process_evidence').glob('*/execution.json'))]
    require(len(runs)==5 and [r['actual_PID'] for r in runs]==[67816,45361,55642,56459,45536],'Actual scientific-parent inventory differs')
    require(sum(r['exit_code']!=0 for r in runs)==1 and next(r for r in runs if r['actual_PID']==55642)['exit_code']==1,'Genuine failed checker is lost')
    replay=load(v/'fresh_replay/REPLAY_RECEIPT.json');children=[]
    for e in replay['native_executions']:
        x=e['native_execution'];p=Path(e['scientific_output']['path']).parent/'execution.json'
        require(load(p)==x and x['actual_launcher_PID']==45361 and x['exit_code']==0,'Actual finite child binding differs')
        request=load(p.parent/'request.json');require(all(x[k]==w for k,w in request.items()),'Actual child prelaunch differs')
        require(time(x['started_UTC'])<=time(x['completed_UTC']),'Child time order differs')
        executable(x['runtime']['executable']);require(x['runtime']['optimization']==0 and x['runtime']['sympy']=='1.14.0','Actual child runtime differs')
        require(match(x['source']).read_bytes()==match(x['original_source']).read_bytes(),'Actual executed child differs from ZIP')
        match(x['runner_source']);out=stream(x['stdout']);require(not stream(x['stderr']),'Successful child stderr')
        match(e['scientific_output']);children.append(dict(receipt=pin(p),actual_PID=x['actual_child_PID'],stdout_bytes=len(out),exit_code=0))
    require(len(children)==8 and [c['actual_PID'] for c in children]==[45375,45394,45397,45406,45407,45414,45524,45535],'Actual child inventory differs')
    cross=load(v/'EVIDENCE_CROSSCHECK.json');require(len(cross['full_byte_checked_pins'])==293,'Crosscheck inventory differs')
    for r in cross['full_byte_checked_pins']:match(r)
    verdict=load(v/'VERDICT.json');require(verdict['mandatory_unresolved_issues']==[] and verdict['new_nonmandatory_suggestions']==[] and verdict['publication_clearance'] is False,'Science review scope differs')
    reconciliation=load(v/'DERIVATION_EDITORIAL_RECONCILIATION.json');require(match(reconciliation['literal_preserved_original']).read_bytes()!=match(reconciliation['current_derivation']).read_bytes(),'Editorial epochs collapsed')
    cases=native(o/'actual_isolated_cases_01/execution.json','operations');require(cases['actual_PID']==63096 and cases['exit_code']==0,'Actual isolated review runner differs')
    ov=load(o/'VERDICT.json');require([r['id'] for r in ov['mandatory_issues']]==['G1','G2'] and ov['publication_clearance'] is False,'Required operational repairs differ')
    oa=load(o/'AUTHENTICATION.json')
    for r in oa['original_inputs']:
        require(gzip.decompress(match(r['archive']).read_bytes())==match(r['input'],True).read_bytes(),'Original operational version differs before repair')
    result=dict(UTC=datetime.now(timezone.utc).isoformat(),actual_ROOT_recorder_PID=os.getpid(),argv=sys.argv,cwd=str(Path.cwd()),source=pin(__file__),resolved_interpreter=pin(Path(sys.executable).resolve()),status='PASS_SECOND_WHOLE_PACKAGE_REVIEW_AND_ACCEPT_REQUIRED_OPERATIONS_REPAIRS',ROOT_accepts_mathematics=True,ROOT_accepts_scoped_priority=True,whole_package_reviews_complete=2,unresolved_scientific_issues=[],required_operations_issues=['G1','G2'],publication_clearance=False,merge_authority=False,candidate_manifest=pin(cm),second_review=science,operations_first_review=operations,complete_source_archives=301,actual_science_parents=runs,actual_finite_children=children,actual_operations_case_runner=cases,full_crosschecked_pins=293,manual_scope='ROOT fully read report, reading ledger, verdict, independent proof and editorial reconciliation; ROOT already independently reconstructed proofs and visually read all eight PDF pages. Closure full bodies/sources/streams separately authenticated. Semantic primary reading is bounded as documented.',qualification='Recorder/tool observations and exact retained bytes; no independent OS/clock attestation. Historical launch modes differ from final444 closure and are preserved, not rewritten.',estimates_percent=dict(mathematics=100,bounded_priority=100,preprint_science=100,publication_workflow=65))
    with (A/'ROOT_SECOND_PREPRINT_REVIEW_ADJUDICATION.json').open('x') as h:json.dump(result,h,indent=2);h.write('\n')
    print(json.dumps({k:result[k] for k in ('status','actual_ROOT_recorder_PID','complete_source_archives','full_crosschecked_pins','required_operations_issues','publication_clearance')}))
if __name__=='__main__':main()
