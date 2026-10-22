import concurrent.futures,datetime,difflib,hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parent;S=R/'private_suites';rows=[];adapt=[]
PIN='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8'
tasks=[]
for name,label,arg in [('test_operations_installed.py','operations','--core-sha256'),('test_source_gate_installed.py','source_gate','--core-sha256'),('test_native_recovery.py','native_recovery','--proposal-sha256')]:
 p=S/name;b=p.read_text();new=b.replace('optimize=0','optimize=sys.flags.optimize');q=S/('optimized_'+name);q.write_text(new)
 adapt.append({'source':name,'copy':q.name,'diff':''.join(difflib.unified_diff(b.splitlines(True),new.splitlines(True),fromfile=name,tofile=q.name))})
 for mode,flag,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2)]:tasks.append((label,mode,opt,[sys.executable,'-I','-S','-B',*flag,str(q),arg,PIN,*(['--installed'] if label=='native_recovery' else [])]))
def launch(task):
 label,mode,opt,args=task;start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,cwd=S,capture_output=True);stem=f'OPTCORE_{label}_{mode}';(R/(stem+'.stdout.raw')).write_bytes(p.stdout);(R/(stem+'.stderr.raw')).write_bytes(p.stderr)
 row={'label':label,'mode':mode,'core_compile_optimize':opt,'args':args,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode}
 if p.returncode==0:row['events']=json.loads(p.stdout)['event_count']
 (R/(stem+'.launch.json')).write_text(json.dumps(row,indent=2)+'\n');return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(launch,tasks))
(R/'OPTIMIZED_CORE_REPLAY.json').write_text(json.dumps({'rows':rows,'adaptations':adapt,'scope':'Only compile optimization adaptation in separate own copies; original prior suites retained; actual authenticated core source unchanged.'},indent=2)+'\n');print('EXPLICIT_CORE_OPTIMIZATION_REPLAY',[(r['label'],r['mode'],r['returncode'],r.get('events')) for r in rows])
