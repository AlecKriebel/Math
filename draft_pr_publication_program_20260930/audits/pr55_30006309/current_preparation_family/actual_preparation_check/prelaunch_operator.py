"""Capture actual preparer command with literal argv, PID, UTC, source and complete streams."""
import datetime,hashlib,json,pathlib,subprocess,sys,os
F=pathlib.Path(__file__).absolute().parent
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert len(sys.argv)>=3
name=sys.argv[1];child=(F/sys.argv[2]).absolute()
assert name in ['actual_current_author_replay','actual_preparation_check']
assert child in [F/'science/verify_product_vectors.py',F/'verify_current.py']
dest=F/name;dest.mkdir(exist_ok=False)
operator=pathlib.Path(__file__).read_bytes();(dest/'prelaunch_operator.py').write_bytes(operator)
sources=[child]
if name=='actual_current_author_replay':sources.append(F/'science/CANDIDATE.md')
pins=[]
for i,p in enumerate(sources):
    b=p.read_bytes();saved='prelaunch_child.py' if i==0 else 'prelaunch_candidate.md'
    (dest/saved).write_bytes(b)
    pins.append({'path':str(p),'prelaunch_copy':saved,'bytes':len(b),'sha256':sha(b),'mode_at_launch':format(p.stat().st_mode&0o7777,'04o')})
argv=['/usr/bin/python3','-B',str(child)]
cap={'schema':'pr55-current-actual-preparer-command-capture/v1','argv':argv,'cwd':str(R),'started_utc':now(),'operator_pid':os.getpid(),'operator_sha256':sha(operator),'sources':pins,'actual_execution':True,'source_only':True,'root_execution':False,'candidate_context_bound_by_operator_not_read_by_checker':name=='actual_current_author_replay'}
proc=subprocess.Popen(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
cap['pid']=proc.pid
out,err=proc.communicate();cap.update({'finished_utc':now(),'exit_code':proc.returncode,'completed':True,'operator_unchanged':sha(pathlib.Path(__file__).read_bytes())==sha(operator)})
for k,b in [('stdout',out),('stderr',err)]:
    filename=k+'.bin';(dest/filename).write_bytes(b);cap[k]={'path':filename,'bytes':len(b),'sha256':sha(b)}
cap['sources_unchanged']=all(sha(pathlib.Path(x['path']).read_bytes())==x['sha256'] for x in pins)
(dest/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps({'name':name,'pid':proc.pid,'exit_code':proc.returncode,'started_utc':cap['started_utc'],'finished_utc':cap['finished_utc'],'stdout_bytes':len(out),'stderr_bytes':len(err),'source_only':True}))
sys.exit(proc.returncode)
