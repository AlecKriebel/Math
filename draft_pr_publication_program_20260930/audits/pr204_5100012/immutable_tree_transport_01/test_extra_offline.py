"""Additional offline atomicity, cross-instance locking and fail-closed controls."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import copy,datetime,gzip,hashlib,json,os,sys,tempfile
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
import tree_transport as t
from test_offline import D,TREES,FakeAPI,rejects
def main():
    controls=[];sha=next(iter(TREES));j=TREES[sha]
    with tempfile.TemporaryDirectory(prefix='private_crossinstance_',dir=D) as d:
        api=FakeAPI()
        with t.TreeCache(api,Path(d)) as one,t.TreeCache(api,Path(d)) as two:
            with ThreadPoolExecutor(max_workers=8) as pool:result=list(pool.map(lambda i:[one,two][i%2]('git/trees/'+sha),range(16)))
            t.require(len(api.calls)==1 and all(x==j for x in result),'Cross-instance per-SHA locking');controls.append('two cache instances/16 concurrent requests use one original call')
    with tempfile.TemporaryDirectory(prefix='private_exclusive_',dir=D) as d:
        root=Path(d);raw=t.validate_tree(sha,j);payload=t.canonical({'requested_sha':sha,'api_json_sha256':hashlib.sha256(raw).hexdigest(),'api_json':j});other=gzip.compress(payload,mtime=123)
        calls=[]
        def race(endpoint,method='GET',body=None):
            calls.append(endpoint);f=root/(sha+'.json.gz')
            with f.open('xb') as out:out.write(other)
            f.chmod(0o600);return copy.deepcopy(j)
        with t.TreeCache(race,root) as cache:
            controls.append(rejects(lambda:cache('git/trees/'+sha),'exclusive publish refuses raced existing final object'))
            t.require((root/(sha+'.json.gz')).read_bytes()==other and len(calls)==1,'Existing object overwritten/retried')
            t.require(cache('git/trees/'+sha)==j and len(calls)==1,'Valid raced object not preserved')
    with tempfile.TemporaryDirectory(prefix='private_badfresh_',dir=D) as d:
        calls=[]
        def wrong(endpoint,method='GET',body=None):calls.append(endpoint);x=copy.deepcopy(j);x['truncated']=True;return x
        with t.TreeCache(wrong,Path(d)) as cache:
            controls.append(rejects(lambda:cache('git/trees/'+sha),'fresh invalid response not cached/retried'));t.require(len(calls)==1 and not list(Path(d).glob('*.json.gz')),'Bad fresh response cached')
    with tempfile.TemporaryDirectory(prefix='private_budget_',dir=D) as d:
        saved=t.MAX_FILES;t.MAX_FILES=0;api=FakeAPI()
        try:
            with t.TreeCache(api,Path(d)) as cache:
                controls.append(rejects(lambda:cache('git/trees/'+sha),'private cache file-count budget fails closed'));t.require(len(api.calls)==1 and not list(Path(d).glob('*.json.gz')),'Budget response retried/stored')
        finally:t.MAX_FILES=saved
    with tempfile.TemporaryDirectory(prefix='private_symlinktarget_',dir=D) as d:
        link=D/'private_root_symlink_test';os.symlink(d,link)
        try:controls.append(rejects(lambda:t.TreeCache(FakeAPI(),link),'symlink private cache root rejected'))
        finally:link.unlink()
    with tempfile.TemporaryDirectory(prefix='private_postfailure_',dir=D) as d:
        calls=[]
        def fails(*args):calls.append(args);raise RuntimeError('Offline POST failure')
        with t.TreeCache(fails,Path(d)) as cache:
            controls.append(rejects(lambda:cache('git/commits','POST',{'tree':sha}),'mutating transport failure forwarded once without retry'));t.require(len(calls)==1 and not list(Path(d).glob('*.json.gz')),'Mutation cached/retried')
    controls.append(rejects(lambda:t.parse_json(b'{"x":1,"x":2}'),'duplicate cached JSON keys rejected'))
    controls.append(rejects(lambda:t.parse_json(b'{"x":NaN}'),'nonfinite cached JSON rejected'))
    with tempfile.TemporaryDirectory(prefix='private_closed_',dir=D) as d:
        api=FakeAPI();cache=t.TreeCache(api,Path(d));cache.close();controls.append(rejects(lambda:cache('git/trees/'+sha),'closed cache rejects before any filesystem/API action'));t.require(not api.calls and not list(Path(d).iterdir()),'Closed cache performed work')
    result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Additional offline synthetic controls only','controls_passed':controls,'no_remote_calls':True,'no_live_installation_or_helper_phase':True,'all_temporary_owned_private_cache_fixtures_removed':True,'production_cache_created':False,'research_case_percent_actual_baseline':60,'publication_or_mathematical_clearance':False}
    f=D/'OFFLINE_EXTRA_RESULTS_03.json'
    with f.open('xb') as out:out.write((json.dumps(result,indent=2)+'\n').encode())
    f.chmod(0o444);print(json.dumps({'extra_controls_passed':len(controls),'no_remote_calls':True,'production_cache_created':False}))
if __name__=='__main__':main()
