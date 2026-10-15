"""PR52 private source preparation command capture; no merge/publication authority."""
import argparse,datetime,hashlib,json,os,subprocess,sys,traceback
from pathlib import Path
F=Path(__file__).resolve().parent
R=Path('/Users/alec/Documents/Math')
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(p.stat().st_mode&0o7777,'04o')}
def main():
 p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--cwd',default=str(R));p.add_argument('--source',action='append',default=[]);p.add_argument('argv',nargs=argparse.REMAINDER);a=p.parse_args()
 assert a.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in a.name)
 argv=a.argv[1:] if a.argv[:1]==['--'] else a.argv;assert argv and all(type(x) is str for x in argv)
 d=F/'captures'/a.name;d.mkdir(parents=True,exist_ok=False)
 op=Path(__file__).read_bytes();(d/'OPERATOR_PRELAUNCH.py').write_bytes(op)
 sources=[]
 for i,x in enumerate(a.source):
  q=Path(x).resolve(strict=True);b=q.read_bytes();s=d/('SOURCE_PRELAUNCH_%02d'%i+q.suffix);s.write_bytes(b);sources.append({'original':ident(q),'saved':ident(s)})
 rec={'schema':'pr52-private-explicit-command/v1','argv':argv,'cwd':str(Path(a.cwd).resolve(strict=True)),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator':ident(d/'OPERATOR_PRELAUNCH.py'),'sources':sources,'actual_execution':False,'pid':None,'exit_code':None,'completed':False,'preparation_only':True}
 (d/'PRELAUNCH.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
 out=err=b''
 try:
  child=subprocess.Popen(argv,cwd=rec['cwd'],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rec.update(actual_execution=True,pid=child.pid);out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode)
 except BaseException:rec['launch_error']=traceback.format_exc();err=rec['launch_error'].encode()
 for n,b in [('STDOUT.bin',out),('STDERR.bin',err)]:(d/n).write_bytes(b);rec[n]=ident(d/n)
 rec['operator_unchanged']=Path(__file__).read_bytes()==op;rec['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();rec['status']='PASS' if rec['completed'] and rec['exit_code']==0 and rec['operator_unchanged'] else 'FAIL'
 (d/'COMPLETE.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');print(json.dumps({'capture':str(d),'pid':rec['pid'],'exit_code':rec['exit_code'],'status':rec['status'],'stdout_bytes':len(out),'stderr_bytes':len(err)},sort_keys=True));return 0 if rec['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
