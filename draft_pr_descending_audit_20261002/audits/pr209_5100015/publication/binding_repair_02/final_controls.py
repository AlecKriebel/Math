"""Final targeted controls with the corrected NEW finite HTTP adapter."""
from pathlib import Path
import importlib.util,types,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base_targeted',HERE/'probes.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
P.HERE=HERE/'final_controls';P.H.RUNS=P.HERE/'fixtures';P.H.SNAP=P.HERE/'source_snapshot'
P.H.SOURCE={n:(HERE.parent/n).read_bytes() for n in P.H.NAMES}
original=P.fixture
def fixture(label):
    f=original(label);old=f.imp
    def imp(name,globals=None,locals=None,fromlist=(),level=0):
        if name=='urllib.request':return types.SimpleNamespace(request=types.SimpleNamespace(Request=lambda *a,**k:a[0],urlopen=lambda *a,**k:f.urlopen(*a,**k)))
        return old(name,globals,locals,fromlist,level)
    f.imp=imp;return f
def unknown_append():
    f=fixture('unknown_append');f.publish();f.lose_append=True;error=P.reject(f.append)
    f.lose_append=False;t=f.append();assert f.appends==1 and t['append_count']==0 and t['reconciled_existing_attempt']
    f.rb.tracker(f.r,f.pub,f.ctx);f.trace()
    return dict(error=error,actual_appends=1,recovery_append_count=0,grid=f.grid)
def retained_publication_preflight():
    f=fixture('retained_publication_preflight');f.publish()
    stage=f.pub/'STAGE_ATTEMPT.json';s=json.loads(stage.read_text());pre=f.c/s['preflight']['path'];p=json.loads(pre.read_text())
    scan=f.c/p['tracker_scan']['path'];v=json.loads(scan.read_text());v['response']['range']="'Math Puzzles'!A1:D1113"
    P.dump(scan,v);p['tracker_scan']=P.pin(scan,f.c);P.dump(pre,p);s['preflight']=P.pin(pre,f.c);P.dump(stage,s)
    error=P.reject(lambda:f.rb.publication(f.r,f.pub,f.ctx))
    assert 'complete authenticated' in error['error'];f.trace();return error
def generic_http_exception():
    f=fixture('generic_http_exception');v=f.module('verify_published_readonly.py');folder=f.base/'stream';folder.mkdir();chunks=[b'earlier\x00\xff']
    class Broken:
        def __enter__(self):return self
        def __exit__(self,*args):return None
        def read(self,n):
            if chunks:return chunks.pop(0)
            raise OSError('local controlled interrupted stream')
    f.urlopen=lambda *a,**k:Broken();error=P.reject(lambda:v.public_bytes(f.r,f.ctx,f.v(),folder))
    assert (folder/'k303b-outer-center-pedal-areas.pdf').read_bytes()==b'earlier\x00\xff'
    return dict(error=error,earlier_bytes_retained=True)
if __name__=='__main__':
    P.H.SNAP.mkdir(parents=True)
    for n,raw in P.H.SOURCE.items():(P.H.SNAP/n).write_bytes(raw)
    P.dump(P.HERE/'EXACT_SOURCE_INPUTS.json',dict(utc=P.utc(),case_completion_percent=65,files=[P.pin(P.H.SNAP/n,P.HERE) for n in P.H.NAMES]))
    for label,fn in [('unknown_append',unknown_append),('retained_publication_preflight',retained_publication_preflight),('generic_http_exception',generic_http_exception)]:
        P.test(label,fn)
    raise SystemExit(0 if all(x['PASS'] for x in P.RESULTS) else 1)
