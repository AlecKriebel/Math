import gzip,hashlib,json,os,pathlib,datetime
W=pathlib.Path(__file__).resolve().parent
records=[]
for name in ('snapshot_auth','original_controls','independent_GF2','primary_fetch'):
    C=W/'native'/name; r=json.loads((C/'request.json').read_bytes()); s=json.loads((C/'started.json').read_bytes()); e=json.loads((C/'execution.json').read_bytes())
    if e['exit_code']!=0 or e['error'] is not None or not e['parent_reaped'] or e['actual_child_PID']!=s['actual_child_PID'] or e['actual_recorder_PID']!=s['actual_recorder_PID'] or e['actual_recorder_PID']!=r['actual_recorder_PID']: raise RuntimeError('bad native completion')
    for key,pin in r['sources'].items():
        p=pathlib.Path(pin['path']); b=p.read_bytes()
        if len(b)!=pin['bytes'] or hashlib.sha256(b).hexdigest()!=pin['sha256'] or b!=gzip.decompress((C/(key+'_PRELAUNCH.gz')).read_bytes()): raise RuntimeError('prelaunch source changed')
    for stream in ('stdout','stderr'):
        b=gzip.decompress((C/(stream+'.gz')).read_bytes())
        if len(b)!=e[stream]['bytes'] or hashlib.sha256(b).hexdigest()!=e[stream]['sha256']: raise RuntimeError('bad full stream')
    stdout=json.loads(gzip.decompress((C/'stdout.gz').read_bytes()))
    records.append({'name':name,'request':r,'execution':e,'stdout':stdout})
expected=json.loads((W.parent/'snapshot/unsolved_math_prioritization/attempts/30002792/final_review/SMALL_CHARACTERISTIC_CHECKS.json').read_bytes())
if records[1]['stdout']!=expected: raise RuntimeError('original controls differ')
independent=records[2]['stdout']
if independent['union_count']!=7175 or independent['plane_multiset_count']!=15488 or independent['explicit_checks']!=60182: raise RuntimeError('independent controls changed')
for f in records[3]['stdout']['records']:
    b=pathlib.Path(f['path']).read_bytes()
    if len(b)!=f['bytes'] or hashlib.sha256(b).hexdigest()!=f['sha256']: raise RuntimeError('primary capture changed')
print(json.dumps({'status':'PASS_COMPLETE_NATIVE_REPRODUCTION_AND_SOURCE_CUSTODY','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'original_JSON_exact_match':True,'records':records},indent=2,sort_keys=True))
