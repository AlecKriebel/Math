"""Targeted exact-source M01/M02 controls; local children and in-memory providers only."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,hashlib,json,io,types,subprocess,http.client,traceback,zipfile,shutil,copy
HERE=Path(__file__).resolve().parent;PUB=HERE.parent;CASE=PUB.parent
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
REAL_RUN=subprocess.run
spec=importlib.util.spec_from_file_location('historical_fixture_code',PUB/'binding_repair_01/probes_01.py')
H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
H.SOURCE={n:(PUB/n).read_bytes() for n in H.NAMES};H.RUNS=HERE/'fixtures';H.SNAP=HERE/'source_snapshot'
RESULTS=[]
def utc():return datetime.now(timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,base):return dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
def reject(fn):
    try:fn()
    except Exception as e:return dict(type=type(e).__name__,error=str(e))
    raise AssertionError('Negative control accepted')
def compact(label):
    folder=H.RUNS/label
    if not folder.exists():return
    files={p.relative_to(folder).as_posix():p for p in folder.rglob('*') if p.is_file()}
    zpath=HERE/('FIXTURE_'+label+'.zip')
    with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,p in sorted(files.items()):z.write(p,name)
    with zipfile.ZipFile(zpath) as z:
        assert set(z.namelist())==set(files) and len(z.namelist())==len(files) and z.testzip() is None
        rows=[]
        for name,p in sorted(files.items()):
            assert z.read(name)==p.read_bytes();rows.append(dict(path=name,bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
    dump(HERE/('FIXTURE_'+label+'_MANIFEST.json'),dict(utc=utc(),archive=pin(zpath,HERE),exact_members=True,CRC=True,every_body=True,files=rows))
    shutil.rmtree(folder)
def test(label,fn):
    start=utc()
    try:r=dict(label=label,start_utc=start,completed_utc=utc(),PASS=True,result=fn())
    except Exception as e:r=dict(label=label,start_utc=start,completed_utc=utc(),PASS=False,error=repr(e),traceback=traceback.format_exc())
    r['completed_utc']=utc();RESULTS.append(r);dump(HERE/'RESULTS.json',RESULTS);print(json.dumps(r),flush=True)
    compact(label)

def fixture(label):
    f=H.Fixture(label);f.grid=1114;f.values_override=None
    f.sheet=[f.rb.HEADER.copy()]+[['foreign '+str(i),'','','unrelated'] for i in range(2,119)]
    old=f.run
    def run(cmd,**kw):
        assert kw.get('text') is False,'Exact readers must capture binary'
        if cmd[0].endswith('/gws'):
            params=json.loads(cmd[cmd.index('--params')+1]);f.calls.append(dict(gws_args=cmd,params=params))
            if cmd[1:4]==['sheets','spreadsheets','get']:
                v=dict(spreadsheetId=f.rb.SHEET,sheets=[dict(properties=dict(sheetId=f.rb.SHEET_ID,title='Math Puzzles',gridProperties=dict(rowCount=f.grid,columnCount=43)))])
            elif cmd[4]=='append':
                f.appends+=1;row=json.loads(cmd[cmd.index('--json')+1])['values'][0];f.sheet.append(row);f.grid+=1
                target="'Math Puzzles'!A"+str(len(f.sheet))+':D'+str(len(f.sheet))
                v=dict(spreadsheetId=f.rb.SHEET,updates=dict(updatedRows=1,updatedCells=4,updatedRange=target,updatedData=dict(range=target,majorDimension='ROWS',values=[row])))
                if getattr(f,'lose_append',False):raise subprocess.TimeoutExpired('LOCAL_STUB_APPEND',1,output=b'partial\x00\xff',stderr=b'err\xff')
            else:
                target=params['range']
                if target==f.rb.FULL_RANGE:
                    value_range="'Math Puzzles'!A1:D"+str(f.grid);values=copy.deepcopy(f.sheet)
                else:
                    number=f.rb.tracker_row_number(target);value_range=target;values=copy.deepcopy(f.sheet[number-1:number])
                v=dict(range=value_range,majorDimension='ROWS',values=values)
                if f.values_override:v=f.values_override(target,v)
            return subprocess.CompletedProcess(cmd,0,json.dumps(v).encode(),b'')
        result=old(cmd,**kw)
        if isinstance(result.stdout,str):result.stdout=result.stdout.encode()
        if isinstance(result.stderr,str):result.stderr=result.stderr.encode()
        return result
    f.run=run
    def opened(url,**kw):
        name=url.split('/files/')[1].split('?')[0];mapping=next(m for m in f.maps if m['name']==name)
        return io.BytesIO((f.r/mapping['path']).read_bytes())
    f.urlopen=opened
    return f

def canonical():
    f=fixture('canonical');z=f.publish();t=f.append()
    assert len(f.sheet)==119 and f.grid==1115 and t['updated_range']=="'Math Puzzles'!A119:D119"
    f.rb.tracker(f.r,f.pub,f.ctx,z)
    f.module('verify_published_readonly.py').verify_publication_live(f.r,f.pub,f.ctx)
    f.module('append_verified_tracker.py').verify_tracker_live(f.r,f.pub,f.ctx,z)
    f.trace()
    return dict(initial_values=118,initial_grid=1114,final_grid=1115,target=t['updated_range'],stage=f.stages,publish=f.publishes,append=f.appends)

def range_matrix():
    f=fixture('range_matrix');props=dict(spreadsheetId=f.rb.SHEET,sheets=[dict(properties=dict(sheetId=f.rb.SHEET_ID,title='Math Puzzles',gridProperties=dict(rowCount=1114,columnCount=43)))])
    good=dict(range="'Math Puzzles'!A1:D1114",majorDimension='ROWS',values=f.sheet)
    def record(v,target=f.rb.FULL_RANGE):return dict(request=dict(spreadsheetId=f.rb.SHEET,range=target),response=v)
    assert len(f.rb.tracker_readback(record(good),f.rb.FULL_RANGE,props))==118
    out={}
    for label,changes in [('missing_range',dict(range=None)),('wrong_tab',dict(range="'Wrong tab'!A1:D1114")),
        ('wrong_columns',dict(range="'Math Puzzles'!B1:E1114")),('truncated',dict(range="'Math Puzzles'!A1:D1113")),
        ('wrong_start',dict(range="'Math Puzzles'!A2:D1114")),('missing_dimension',dict(majorDimension=None)),
        ('columns_dimension',dict(majorDimension='COLUMNS')),('literal_full',dict(range=f.rb.FULL_RANGE))]:
        response=dict(good,**changes);dump(f.base/(label+'.json'),record(response))
        out[label]=reject(lambda:f.rb.tracker_readback(record(response),f.rb.FULL_RANGE,props))
    target="'Math Puzzles'!A119:D119";wrong=dict(range="'Math Puzzles'!A120:D120",majorDimension='ROWS',values=[['x']])
    out['wrong_target_row']=reject(lambda:f.rb.tracker_readback(record(wrong,target),target,props))
    p=copy.deepcopy(props);p['sheets'][0]['properties']['gridProperties'].pop('rowCount')
    out['missing_grid']=reject(lambda:f.rb.tracker_readback(record(good),f.rb.FULL_RANGE,p))
    dump(f.base/'RANGE_MATRIX.json',out);return out

def live_and_retained():
    f=fixture('live_and_retained');z=f.publish();t=f.append();original=(f.pub/'TRACKER_VERIFIED_APPEND.json').read_bytes();out={}
    for key in ['before_scan','target_readback','after_scan']:
        path=f.c/t['evidence'][key]['path'];raw=path.read_bytes();v=json.loads(raw);v['response']['majorDimension']='COLUMNS';dump(path,v)
        changed=copy.deepcopy(t);changed['evidence'][key]=pin(path,f.c)
        if key=='before_scan' and changed['append_count']==0:changed['evidence']['reconciliation_before']=changed['evidence'][key]
        dump(f.pub/'TRACKER_VERIFIED_APPEND.json',changed);dump(f.base/('BAD_'+key+'.json'),v)
        out[key]=reject(lambda:f.rb.tracker(f.r,f.pub,f.ctx,z));path.write_bytes(raw);(f.pub/'TRACKER_VERIFIED_APPEND.json').write_bytes(original)
    f.values_override=lambda target,v:dict(v,range="'Wrong tab'!Z999:AC999",majorDimension='COLUMNS')
    out['live']=reject(lambda:f.module('append_verified_tracker.py').verify_tracker_live(f.r,f.pub,f.ctx,z))
    assert (f.pub/'TRACKER_VERIFIED_APPEND.json').read_bytes()==original and f.appends==1
    f.trace();return out

def failed_after_write():
    f=fixture('failed_after_write');f.publish()
    f.values_override=lambda target,v:dict(v,range="'Math Puzzles'!A1:D1114") if target==f.rb.FULL_RANGE and f.grid==1115 else v
    failure=reject(f.append);assert f.appends==1 and not (f.pub/'TRACKER_VERIFIED_APPEND.json').exists()
    f.values_override=None;t=f.append();assert f.appends==1 and t['append_count']==0
    f.trace();return dict(failure=failure,append_calls=1,recovery_append_count=0)

CHILD_OUT=b'prefix\x00\xffsuffix';CHILD_ERR=b'error\x00\xffstream'
def real_children():
    f=fixture('real_children');out={}
    for timeout in [False,True]:
        for kind in ['tracker','inspect','publish']:
            folder=f.base/(kind+('_timeout' if timeout else '_decode'));folder.mkdir()
            script="import os,time;os.write(1,"+repr(CHILD_OUT)+");os.write(2,"+repr(CHILD_ERR)+")"+(";time.sleep(2)" if timeout else "")
            def child(cmd,**kw):
                assert kw.get('text') is False
                kw['timeout']=0.2 if timeout else 5
                return REAL_RUN([PY,'-B','-c',script],**kw)
            if kind=='tracker':
                a=f.module('append_verified_tracker.py');a.subprocess=types.SimpleNamespace(run=child)
                error=reject(lambda:a.reader(folder)('local-child',['UNUSED']))
                stdout=folder/'local-child-stdout.json';stderr=folder/'local-child-stderr.txt'
            elif kind=='inspect':
                v=f.module('verify_published_readonly.py');v.subprocess=types.SimpleNamespace(run=child)
                error=reject(lambda:v.inspect_existing(f.r,f.ctx,12345,folder))
                stdout=folder/'inspect-stdout.json';stderr=folder/'inspect-stderr.txt'
            else:
                p=f.module('publish_preprint.py');p.subprocess=types.SimpleNamespace(run=child)
                error=reject(lambda:p.publish_once(f.r,f.pub,f.base))
                run=sorted((f.pub/'private_transport/zenodo_stage').iterdir())[-1]
                stdout=run/'PR-head-preflight-stdout.json';stderr=run/'PR-head-preflight-stderr.txt'
            assert stdout.read_bytes()==CHILD_OUT and stderr.read_bytes()==CHILD_ERR
            out[kind+('_timeout' if timeout else '_decode')]=dict(error=error,stdout=CHILD_OUT.hex(),stderr=CHILD_ERR.hex())
    assert not (f.pub/'STAGE_ATTEMPT.json').exists();dump(f.base/'CHILD_RESULTS.json',out);return out

def interrupted_http():
    f=fixture('interrupted_http');v=f.module('verify_published_readonly.py');out={}
    for label,chunks,partial in [('first',[],b'partial-first\x00\xff'),('after_chunks',[b'earlier\x00\xff',b'second'],b'last\x00\xff')]:
        folder=f.base/label;folder.mkdir();remaining=list(chunks);expected=b''.join(chunks)+partial
        class Response:
            def __enter__(self):return self
            def __exit__(self,*a):return None
            def read(self,n):
                if remaining:return remaining.pop(0)
                raise http.client.IncompleteRead(partial,100)
        f.urlopen=lambda *a,**k:Response()
        error=reject(lambda:v.public_bytes(f.r,f.ctx,f.v(),folder))
        payload=folder/'k303b-outer-center-pedal-areas.pdf'
        assert payload.read_bytes()==expected
        failure=json.loads((folder/'k303b-outer-center-pedal-areas.pdf-READ_FAILURE.json').read_text())
        assert failure['exception_partial_bytes']==len(partial) and failure['retained_bytes']==len(expected)
        out[label]=dict(error=error,retained_bytes=len(expected),sha256=sha(expected))
    dump(f.base/'HTTP_RESULTS.json',out);return out

def http_pending_recovery():
    f=fixture('http_pending_recovery');normal=f.urlopen
    class Bad:
        def __enter__(self):return self
        def __exit__(self,*a):return None
        def read(self,n):raise http.client.IncompleteRead(b'available\x00\xff',99)
    f.urlopen=lambda *a,**k:Bad();failure=reject(f.publish)
    assert f.stages==f.publishes==1 and not (f.pub/'ZENODO_VERIFIED_PUBLICATION.json').exists()
    blocked=reject(f.publish);assert f.stages==f.publishes==1
    f.urlopen=normal;z=f.module('verify_published_readonly.py').verify_existing(f.r,f.pub,f.ctx)
    assert z['submitted'] and f.stages==f.publishes==1
    f.trace();return dict(failure=failure,blocked_retry=blocked,stages=1,publishes=1,read_only_recovery=True)

def preflight_identity():
    f=fixture('preflight_identity')
    f.values_override=lambda target,v:dict(v,majorDimension='COLUMNS')
    error=reject(f.publish);assert f.stages==f.publishes==0
    f.trace();return dict(error=error,stage_calls=0,publish_calls=0)

if __name__=='__main__':
    H.SNAP.mkdir()
    for n,raw in H.SOURCE.items():(H.SNAP/n).write_bytes(raw)
    dump(HERE/'EXACT_SOURCE_INPUTS.json',dict(utc=utc(),case_completion_percent=65,files=[pin(H.SNAP/n,HERE) for n in H.NAMES]))
    for label,fn in [('canonical',canonical),('range_matrix',range_matrix),('live_and_retained',live_and_retained),
        ('failed_after_write',failed_after_write),('real_children',real_children),('interrupted_http',interrupted_http),
        ('http_pending_recovery',http_pending_recovery),('preflight_identity',preflight_identity)]:
        test(label,fn)
    dump(HERE/'SUMMARY.json',dict(utc=utc(),groups=len(RESULTS),all_pass=all(x['PASS'] for x in RESULTS),case_completion_percent=65,no_release_authority=True))
    raise SystemExit(0 if all(x['PASS'] for x in RESULTS) else 1)
