#!/usr/bin/env python3
"""Isolated subprocess CLI tests with an explicitly synthetic API boundary."""
import argparse,base64,contextlib,copy,datetime,hashlib,importlib.util,io,json
from pathlib import Path
import subprocess,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def child(a):
    t=load(HERE/'continuation_controls.py','fixture_types');m=t.load(HERE/'pr411_admin.py')
    spec=json.loads((a.case/'private_sources/merge_preparation_v5/ACTUAL_PREINTENT_DESCRIPTOR.json').read_bytes())
    originals={ref['path']:m.read_local(a.case,ref['path'],ref['sha256']) for ref in spec.values() if isinstance(ref,dict)}
    w=t.World(m,a.private_dir,spec,originals)
    if a.control=='stale':w.plan['native_evidence']['sheet_freshness_deadline_utc']='2000-01-01T00:00:00Z'
    planpath=w.case/'approved_plan.json';planpath.write_bytes(t.pretty(w.plan))
    approval=w.approval() if a.control!='badapproval' else {}
    apppath=w.case/'approval.json';apppath.write_bytes(t.pretty(approval))
    api=t.FakeAPI(a.control=='unknown');m.API=lambda:api
    clean=a.control!='dirty'
    m.fresh_gate=lambda *args,**kw:({'skip':False},{'mergeable':clean,'mergeable_state':'clean' if clean else 'unknown'},b'')
    m.prepare=lambda *args,**kw:(copy.deepcopy(w.plan),{})
    m.descendant_main_guard=lambda *args,**kw:{'synthetic':True}
    m.verify_integrated=lambda *args,**kw:{'synthetic':True}
    m.verify_merge=lambda *args,**kw:{'synthetic':True,'native_success_certified':False}
    operation='plan' if a.control=='plan' else 'apply'
    base=[str(HERE/'pr411_admin.py'),operation,'--phase','merge','--case',str(w.case),'--head',w.plan['expected_head'],
          '--main',w.plan['main_head'],'--map','unused_map.json:'+w.plan['approved_map_sha256'],
          '--evidence','unused_evidence.json:'+w.plan['evidence_bindings_sha256'],
          '--continuation',w.ref['path']+':'+w.ref['sha256'],'--journal-root',str(w.root)]
    if operation=='apply':base+=['--plan','approved_plan.json:'+t.sha(planpath.read_bytes()),'--approval','approval.json:'+t.sha(apppath.read_bytes()),'--run-id','cli_successor']
    calls=[]
    def invoke(argv):
        sys.argv=argv;out,err=io.StringIO(),io.StringIO();code=0
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
            try:m.main()
            except (m.Stop,OSError,KeyError,TypeError,ValueError) as e:print('STOP: '+str(e),file=sys.stderr);code=2
        calls.append({'argv':argv,'returncode':code,'stdout_base64':base64.b64encode(out.getvalue().encode()).decode(),
                      'stderr_base64':base64.b64encode(err.getvalue().encode()).decode()})
    invoke(base)
    if a.control in ('double','unknown'):
        second=base[:];second[second.index('--run-id')+1]='cli_second';invoke(second)
    expected={'plan':[0],'apply':[0],'badapproval':[2],'dirty':[2],'double':[0,2],'unknown':[2,2],'stale':[2]}[a.control]
    t.require([x['returncode'] for x in calls]==expected,'actual isolated CLI status mismatch')
    expectedwrites=1 if a.control in ('apply','double','unknown') else 0
    t.require(len(api.writes)==expectedwrites,'actual isolated CLI fake-write count mismatch')
    w.unchanged()
    if a.control in ('plan','badapproval','stale'):t.require(not (w.root/'continuations').exists(),'pre-journal failed CLI allocated guard')
    print(json.dumps({'result':'PASS_ISOLATED_SYNTHETIC_CLI','control':a.control,'calls':calls,'fake_API_writes':len(api.writes),
        'native_requests':0,'native_mutations':0,'native_success_certified':False,'original_copied_custody_unchanged':True,
        'boundary':'Actual subprocess main()/argparse/approval/Journal/execute behavior with fake prepare/current API/readbacks. Original operator root never written; no science/assets/native requests.'},sort_keys=True))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',type=Path,required=True);p.add_argument('--private-dir',type=Path,required=True)
    p.add_argument('--child',action='store_true');p.add_argument('--control',choices=['plan','apply','badapproval','dirty','double','unknown','stale']);a=p.parse_args()
    if a.child:child(a);return
    a.private_dir.mkdir(parents=True,exist_ok=False);results=[]
    for opt in [False,True]:
        for control in ['plan','apply','badapproval','dirty','double','unknown','stale']:
            tag=('optimized_' if opt else 'normal_')+control
            command=[sys.executable,'-B']+(['-O'] if opt else [])+[str(Path(__file__).resolve()),'--child','--case',str(a.case),'--private-dir',str(a.private_dir/tag),'--control',control]
            native=subprocess.run(command,capture_output=True)
            (a.private_dir/(tag+'.stdout')).write_bytes(native.stdout);(a.private_dir/(tag+'.stderr')).write_bytes(native.stderr)
            if native.returncode!=0:raise RuntimeError(tag+' isolated CLI failed: '+native.stderr.decode())
            result=json.loads(native.stdout);result['optimized']=opt
            result['actual_child_stdout_sha256']=hashlib.sha256(native.stdout).hexdigest();result['actual_child_stderr_sha256']=hashlib.sha256(native.stderr).hexdigest()
            results.append(result)
    output={'format':'pr411-v5-actual-isolated-offline-CLI-controls-v1','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','subprocess_controls':len(results),'results':results,'native_requests':0,'native_mutations':0,'boundary':'Isolated Python subprocesses with explicitly fake API/prepare/native readbacks only. Not production or fresh native validation.'}
    (a.private_dir/'RESULT.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))

if __name__=='__main__':main()
