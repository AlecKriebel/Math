from pathlib import Path
import datetime,hashlib,json,os,subprocess,urllib.request
P=Path(__file__).resolve().parent;D=P/'private_primary_sources_20261006';events=[]
items=[
 ('mocanu_reade1975.pdf','https://www.ams.org/journals/proc/1975-051-02/S0002-9939-1975-0374404-5/S0002-9939-1975-0374404-5.pdf'),
 ('miller_mocanu_reade1973.pdf','https://www.ams.org/journals/proc/1973-037-02/S0002-9939-1973-0313490-3/S0002-9939-1973-0313490-3.pdf'),
 ('arif_ayaz_aouf2013.pdf','https://downloads.hindawi.com/journals/tswj/2013/280191.pdf')]
for name,url in items:
 e={'requested_url':url,'file':name,'actual_operator_PID':os.getpid(),'UTC_started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=20) as response:b=response.read();final=response.geturl();status=response.status
  e.update({'status':status,'final_url':final,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'PDF_header':b.startswith(b'%PDF')})
  if not b.startswith(b'%PDF'):raise RuntimeError('not PDF')
  (D/name).write_bytes(b)
  cmd=['/opt/homebrew/bin/pdftotext','-layout',str(D/name),str((D/name).with_suffix('.txt'))]
  proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate()
  e.update({'actual_extraction_PID':proc.pid,'extraction_exit_code':proc.returncode,'extraction_stderr_sha256':hashlib.sha256(err).hexdigest()})
 except Exception as exc:e['failure']=str(exc)
 e['UTC_finished']=datetime.datetime.now(datetime.timezone.utc).isoformat();events.append(e)
 v={'schema':'pr134-parent-priority-primary-fetch/v1','actual_operator_PID':os.getpid(),'events':events,'private_source_bytes_ignored':True}
 (P/'PARENT_PRIORITY_PRIMARY_FETCH_20261006.json').write_text(json.dumps(v,indent=2)+'\n')
 print(json.dumps(e),flush=True)

