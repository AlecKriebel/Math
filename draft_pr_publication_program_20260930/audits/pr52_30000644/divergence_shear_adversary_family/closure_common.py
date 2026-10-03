"""Read-only full-body checks shared by unexecuted ROOT-only close/read SOURCE."""
from pathlib import Path
from datetime import datetime
import hashlib,json,stat

HERE=Path(__file__).resolve().parent
SELF='SELF_MANIFEST.json'
def bind(path,relative=False):
    body=path.read_bytes()
    return {'path':path.relative_to(HERE).as_posix() if relative else str(path),
            'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
            'mode':format(stat.S_IMODE(path.stat().st_mode),'04o')}
def require(value,message):
    if not value:
        raise AssertionError(message)
def load(name):return json.loads((HERE/name).read_bytes())
def actual_capture(directory,source,results):
    run=HERE/directory
    cap=json.loads((run/'CAPTURE.json').read_bytes())
    require(cap['exit_code']==0 and cap['source_unchanged_after'],'successful source-bound run')
    require(cap['child_pid']>0 and cap['operator_pid']>0,'real positive process ids')
    start=datetime.fromisoformat(cap['utc_start'])
    end=datetime.fromisoformat(cap['utc_end'])
    require(start<=end,'ordered actual UTC interval')
    require(cap['argv']==['/usr/bin/python3','-B',str(HERE/source)],'literal argv')
    require(cap['cwd']==str(HERE),'literal cwd')
    body=(HERE/source).read_bytes()
    require(cap['source']['bytes']==len(body) and cap['source']['sha256']==hashlib.sha256(body).hexdigest(),'complete checker source')
    prelaunch=run/('prelaunch_independent_checks.py' if directory=='private_capture' else 'prelaunch_edge_mutation_checks.py')
    require(prelaunch.read_bytes()==body,'full prelaunch checker source')
    for stream in ('stdout','stderr'):
        body_stream=(run/(stream+'.bin')).read_bytes()
        require(cap[stream]=={'bytes':len(body_stream),'sha256':hashlib.sha256(body_stream).hexdigest()},'full stream '+stream)
    require((run/'stderr.bin').read_bytes()==b'','empty complete stderr')
    require(json.loads((run/'stdout.bin').read_bytes())==load(results),'typed complete stdout/result equality')
    require(cap['production_executed'] is False and cap['ROOT_authority'] is False,'no production or ROOT run claims')
    if directory=='edge_capture':
        operator=(run/'prelaunch_operator.py').read_bytes()
        require(operator==(HERE/'capture_edges.py').read_bytes(),'complete edge operator')
        require(cap['prelaunch_operator']=={'bytes':len(operator),'sha256':hashlib.sha256(operator).hexdigest()},'edge operator binding')
        require(cap['operator_unchanged_after'] is True,'edge operator remained unchanged')
    return cap
def inspect(closed):
    index=load('INDEX.json')
    ready=load('READY.json')
    rows=index['files']
    require(len(rows)==len({r['path'] for r in rows}),'unique payload paths')
    require([r['path'] for r in rows]==sorted(r['path'] for r in rows),'canonical payload order')
    expected={r['path'] for r in rows}|{'INDEX.json','READY.json'}
    if closed:expected.add(SELF)
    actual=set()
    for p in HERE.rglob('*'):
        require(not p.is_symlink(),'no symlink inputs')
        if p.is_file():actual.add(p.relative_to(HERE).as_posix())
    require(actual==expected,'entire family exact file set')
    for row in rows:
        p=HERE/row['path']
        require(p.is_file() and bind(p,True)==row,'complete frozen payload '+row['path'])
        require(row['mode']=='0444','payload full mode 0444')
    for name in ('INDEX.json','READY.json'):
        require(stat.S_IMODE((HERE/name).stat().st_mode)==0o444,'full frozen index/ready modes')
    dirs=[HERE]+sorted(p for p in HERE.rglob('*') if p.is_dir())
    actual_dirs=[{'path':'.' if p==HERE else p.relative_to(HERE).as_posix(),
                  'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')} for p in dirs]
    require(actual_dirs==index['directories'],'whole directory set and full modes')
    require(all(r['mode']=='0555' for r in actual_dirs),'all family dirs frozen')
    require(ready['index']==bind(HERE/'INDEX.json',True),'full index binding')
    require(ready['self_manifest_absent_at_source_ready'] is True,'honest absent self at preparation')
    require(ready['ROOT_execution_performed'] is False,'preparer did not execute ROOT closure')
    references=load('REFERENCE_BINDINGS.json')
    for row in references['files']:
        require(bind(Path(row['path']))==row,'full external reference '+row['path'])
    require(references['original_head']=='d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a','original head pin')
    for row in references['original_git_blobs']:
        body=Path(row['path']).read_bytes()
        got=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        require(got==row['git_blob_sha1'],'complete original Git blob hash')
    verdict=load('VERDICT.json')
    require(verdict['mandatory_mathematical_corrections']==[],'no unresolved mandatory math correction')
    require(verdict['recommended_status']=='already_solved' and verdict['novelty'] is False,'known theorem disposition')
    require(verdict['report']==bind(HERE/'REPORT.md',True),'whole report binding')
    require(verdict['proof']==bind(HERE/'INDEPENDENT_PROOF.md',True),'whole universal proof binding')
    require(verdict['ROOT_approval'] is False and verdict['native_acceptance'] is False,'no borrowed operational approval')
    main=actual_capture('private_capture','independent_checks.py','RESULTS.json')
    edge=actual_capture('edge_capture','edge_mutation_checks.py','EDGE_RESULTS.json')
    require(load('RESULTS.json')['total_assertions']==6672,'main exact assertion count')
    require(load('EDGE_RESULTS.json')['total_assertions']==9,'edge exact assertion count')
    return {'schema':'pr52-divergence-shear-inspection-v1','status':'PASS',
            'payload_files_without_self':len(expected)-(1 if closed else 0),
            'external_full_body_references':len(references['files']),
            'original_git_blobs':len(references['original_git_blobs']),
            'actual_private_child_pids':[main['child_pid'],edge['child_pid']],
            'new_finite_assertions':6681,'closed':closed}
