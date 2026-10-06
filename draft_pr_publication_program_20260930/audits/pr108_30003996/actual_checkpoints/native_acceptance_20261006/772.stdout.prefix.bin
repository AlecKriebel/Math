from pathlib import Path
import datetime,hashlib,json,os,subprocess
O=Path(__file__).absolute().parent;A=O.parent;D=A/'native_publication_integration_plan_20261006/corrected_v5';F=D/'EXECUTION_INPUTS_FROZEN_20261006.json';J=A/'native_actual_input_preparation_v2_20261006/draft_dfe3e71993e3bd99/READ_ONLY_GIT_PROCESS_JOURNAL.json'
env={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
records=[]
for mode in ['normal','optimized']:
 argv=['/opt/homebrew/bin/python3','-E','-S','-B']+(['-O'] if mode=='optimized' else [])+[str(O/'independent_pure_challenges.py'),str(D),str(F),str(J)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(argv,cwd=O,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(timeout=30)
 for name,b in [('stdout',out),('stderr',err)]: (O/(mode.upper()+'_'+name.upper()+'.bin')).write_bytes(b)
 records.append({'actual_process_record':True,'PID':p.pid,'argv':argv,'cwd':str(O),'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'ambient_inherited':False,'effective_environment':env,'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest(),'path':mode.upper()+'_STDOUT.bin'},'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest(),'path':mode.upper()+'_STDERR.bin'}})
 (O/'INDEPENDENT_PROCESS_CUSTODY.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},sort_keys=True,indent=2)+'\n')
 print(mode,p.pid,p.returncode,out.decode(),err.decode())
 if p.returncode:raise SystemExit(p.returncode)
