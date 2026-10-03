import sys,pathlib,subprocess,datetime,hashlib,json,os

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
root=pathlib.Path(__file__).resolve().parent
label=sys.argv[1];source=pathlib.Path(sys.argv[2]).resolve();argv=[sys.executable,str(source),*sys.argv[3:]]
target=root/'actual_runs'/label
target.mkdir(parents=True,exist_ok=False)
operator=pathlib.Path(__file__).read_bytes();body=source.read_bytes()
(target/'prelaunch_operator.py').write_bytes(operator)
(target/'prelaunch_source.py').write_bytes(body)
pre={'schema':'pr45-own-actual-capture/v1','prepared_utc':utc(),'operator_pid':os.getpid(),'cwd':str(root),'argv':argv,'source_path':str(source),'source_sha256':sha(body),'operator_path':str(pathlib.Path(__file__).resolve()),'operator_sha256':sha(operator)}
(target/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
start=utc();p=subprocess.Popen(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(target/'LAUNCHED.json').write_text(json.dumps({'start_utc':start,'operator_pid':os.getpid(),'child_pid':p.pid,'argv':argv},indent=2)+'\n')
out,err=p.communicate();end=utc()
(target/'stdout.bin').write_bytes(out);(target/'stderr.bin').write_bytes(err)
cap={**pre,'start_utc':start,'end_utc':end,'child_pid':p.pid,'exit_code':p.returncode,'stdout':{'path':str(target/'stdout.bin'),'bytes':len(out),'sha256':sha(out)},'stderr':{'path':str(target/'stderr.bin'),'bytes':len(err),'sha256':sha(err)},'source_unchanged':source.read_bytes()==body,'operator_unchanged':pathlib.Path(__file__).read_bytes()==operator}
(target/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps(cap,indent=2))
sys.exit(p.returncode)
