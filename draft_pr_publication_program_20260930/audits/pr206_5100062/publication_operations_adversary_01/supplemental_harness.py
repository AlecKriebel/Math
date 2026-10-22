"""SYNTHETIC_NON_RECEIPT. New independent edge/CLI probes after initial 81 cases."""
import pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent
raw=(ROOT/'independent_harness.py').read_text().split("case('actual_absent_authority'",1)[0]
raw=raw.replace("'independent_work_O'","'supplemental_work_O'")
exec(compile(raw,str(ROOT/'independent_harness.py'),'exec'),globals())
import contextlib,io

for target in ('STAGE_INFLIGHT.json','stage.json','kit_state'):
 def probe(target=target):
  f=Fixture();pub,k,h=f.publisher();pub.directory.mkdir(parents=True)
  q=pub.directory/target;write(q,{'SYNTHETIC_NON_RECEIPT':True})
  if target=='kit_state':pub.kit_state_path=lambda *_:q
  denied(lambda:pub.invoke('stage'),'existing '+target+' stops mutation');check(not k.calls,'zero mutation transports')
 case('preexisting_'+target,probe)

def symlink():
 f=Fixture();target=f.base/'private_target';target.mkdir();(f.base/'private_operations').symlink_to(target,target_is_directory=True);pub,k,h=f.publisher();denied(lambda:pub.invoke('stage'),'private ancestor symlink denied');check(not k.calls,'symlink denies before transport')
case('private_symlink',symlink)

def partial_marker():
 f=Fixture();pub,k,h=f.publisher();pub.directory.mkdir(parents=True);real=os.write
 def broken(fd,data):raise OSError('SYNTHETIC disk write failure')
 os.write=broken
 try:denied(lambda:pub.invoke('stage'),'marker write failure')
 finally:os.write=real
 check((pub.directory/'STAGE_INFLIGHT.json').exists() and not k.calls,'partial marker retained before zero transports');denied(lambda:pub.invoke('stage'),'partial marker cannot replay');check(not k.calls,'still zero transports')
case('partial_inflight_write',partial_marker)

def lost_publish():
 f=Fixture();pub,k,h=f.publisher();pub.invoke('stage');real=k.run
 def run(argv,env):
  answer=real(argv,env)
  if argv[6]=='publish':raise TimeoutError('SYNTHETIC publish response lost')
  return answer
 k.run=run;denied(lambda:pub.invoke('publish',k.id),'lost publish response');denied(lambda:pub.invoke('publish',k.id),'lost publish no duplicate');pub.invoke('inspect-doi',k.id);pub.finalize();check(k.mutations==['stage','publish'],'read-only inspect-doi recovers lost publish')
case('lost_publish_recovery',lost_publish)

for key in ('metadata','public_downloads','context','doi','files'):
 def probe(key=key):
  f=Fixture();f.published();q=f.base/'ROOT_PUBLICATION_RECEIPT.json';r=c.read(q)
  if key=='metadata':r[key]['creators'][0]['orcid']='corrupt'
  elif key=='public_downloads':r[key][0]['sha256']='0'*64
  elif key=='context':r[key]['checkpoint_commit']='e'*40
  elif key=='doi':r[key]='10.5281/zenodo.1'
  elif key=='files':r[key][0]['size']+=1
  write(q,r);s=Sheet(f);denied(lambda:t.Tracker(f.base,s).run(),'corrupt publication '+key);check(not s.calls,'publication corruption rejected before Sheet reads')
 case('publication_receipt_'+key,probe)

def shift_second():
 f=Fixture();f.published();s=Sheet(f);real=s.run
 def run(resources,params,body=None):
  if resources[-1]=='get' and params.get('range')==t.FULL_RANGE and s.full==3:s.data.insert(1,['SYNTHETIC concurrent row','','',''])
  return real(resources,params,body)
 s.run=run;tr=t.Tracker(f.base,s);denied(tr.run,'row shift before second full readback');denied(lambda:tr.run(True),'shifted row cannot recover with stale marker range');check(s.appends==1,'shift never duplicates append')
case('shift_second_full_readback',shift_second)

def drift_append():
 f=Fixture();f.published();s=Sheet(f);real=s.run
 def run(resources,params,body=None):
  answer=real(resources,params,body)
  if resources[-1]=='append':write(f.gp,f.gate|{'SYNTHETIC_after_append_drift':True})
  return answer
 s.run=run;denied(lambda:t.Tracker(f.base,s).run(),'context drift after successful append');check(s.appends==1 and not (f.base/'ROOT_TRACKER_RECEIPT.json').exists(),'uncertain drift preserves one append without acceptance')
case('tracker_context_drift',drift_append)

def main_binding():
 f=Fixture();k=Kit(f);h=Public(f);oldargv=sys.argv;oldkit=p.KitProcess;oldpublic=p.PublicHTTP;stream=io.StringIO();ap=f.base/'SYNTHETIC_OPS_ADOPTION.json';pin=c.pin(ap)
 p.KitProcess=lambda:k;p.PublicHTTP=lambda:h;sys.argv=['authenticated-publisher','stage','--base',str(f.base),'--kit',str(KIT),'--adoption',ap.name,'--adoption-bytes',str(pin['bytes']),'--adoption-sha256',pin['sha256']]
 try:
  with contextlib.redirect_stdout(stream):result=p.main()
 finally:sys.argv=oldargv;p.KitProcess=oldkit;p.PublicHTTP=oldpublic
 j=json.loads(stream.getvalue());check(result is None and j['id']==k.id and j['state']=='ready_to_publish' and k.mutations==['stage'],'publisher exact main prints actual fake result JSON')
 # Successful direct script compile must still refuse entry, with no additional calls.
 for name in ('publisher206','tracker206'):
  m=types.ModuleType('__main__');m.__file__=str(SOURCE/(name+'.py'));denied(lambda name=name,m=m:exec(compile((SOURCE/(name+'.py')).read_bytes(),m.__file__,'exec'),m.__dict__),'direct script refuses '+name)
 check(k.mutations==['stage'],'direct scripts launch no transport')
case('main_stdout_and_direct_entry_binding',main_binding)

result={'SYNTHETIC_NON_RECEIPT':True,'offline_only':True,'status':'PASS' if all(x['status']=='PASS' for x in RESULTS) else 'FAIL','optimization_flag':sys.flags.optimize,'case_count':len(RESULTS),'check_count':sum(len(x['checks']) for x in RESULTS),'cases':RESULTS,'blocked_events':offline_guard.BLOCKED_EVENTS}
out=ROOT/('SUPPLEMENTAL_RESULT_O'+str(sys.flags.optimize)+'.json');out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':result['status'],'case_count':result['case_count'],'check_count':result['check_count'],'optimization_flag':sys.flags.optimize,'failed_cases':[x['id'] for x in RESULTS if x['status']!='PASS']},sort_keys=True))
raise SystemExit(0 if result['status']=='PASS' else 1)
