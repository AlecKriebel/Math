import os,sys,pathlib,subprocess,hashlib,json,datetime
D=pathlib.Path(__file__).parent
url,name=sys.argv[1:3]
receipt={'operator_pid':os.getpid(),'operator_argv':sys.argv,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':[]}
target=D/'private'/name
argv=['curl','--location','--fail','--silent','--show-error','--max-time','40','--max-filesize','5000000','--output',str(target),url]
p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
for label,b in [('stdout',out),('stderr',err)]: (D/'private'/(name+'.curl.'+label+'.bin')).write_bytes(b)
e={'pid':p.pid,'argv':argv,'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()}
if target.exists():
 b=target.read_bytes();e.update({'retrieved_bytes':len(b),'retrieved_sha256':hashlib.sha256(b).hexdigest()})
receipt['events'].append(e)
if p.returncode==0 and name.endswith('.pdf'):
 argv=['pdftotext','-layout',str(target),'-'];p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
 (D/'private'/(name+'.txt')).write_bytes(out);(D/'private'/(name+'.pdftotext.stderr.bin')).write_bytes(err)
 receipt['events'].append({'pid':p.pid,'argv':argv,'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()})
receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(D/'private'/(name+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
