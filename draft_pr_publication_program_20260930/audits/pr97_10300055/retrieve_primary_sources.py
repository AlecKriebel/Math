from pathlib import Path
import datetime,hashlib,json,os,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'primary_source_cache_20261005';D.mkdir(exist_ok=False)
sources=[('calegari2002','https://arxiv.org/pdf/math/0209081v1'),('vogel2011','https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf'),('vogel2016','https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf'),('dathe_rukimbira2008','https://arxiv.org/pdf/0812.3389')]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
records=[]
for name,url in sources:
    start=now()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math-Independent-Source-Audit/1.0'}),timeout=45) as response:b=response.read();status=response.status;resolved=response.url
        if status!=200 or not b.startswith(b'%PDF-'):raise RuntimeError('unexpected HTTP/file type')
        pdf=D/(name+'.pdf');pdf.write_bytes(b)
        argv=['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(D/(name+'.txt'))];child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
        (D/(name+'.pdftotext.stdout.bin')).write_bytes(out);(D/(name+'.pdftotext.stderr.bin')).write_bytes(err)
        records.append({'name':name,'URL':url,'resolved_url':resolved,'HTTP_status':status,'UTC_start':start,'UTC_end':now(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'PDF_path':str(pdf),'pdftotext_argv':argv,'pdftotext_PID':child.pid,'pdftotext_exit_code':child.returncode,'pdftotext_stdout_sha256':hashlib.sha256(out).hexdigest(),'pdftotext_stderr_sha256':hashlib.sha256(err).hexdigest()})
        if child.returncode:raise RuntimeError('PDF extraction failed')
    except Exception as exc:
        records.append({'name':name,'URL':url,'UTC_start':start,'UTC_end':now(),'error':str(exc),'retrieval_succeeded':False})
    (D/'HTTP_AND_PROCESS_RECORDS.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records,'redistribution':'Research cache only; not a public artifact.'},indent=2)+'\n')
print(json.dumps({'sources':[{'name':r['name'],'bytes':r.get('bytes'),'sha256':r.get('sha256'),'error':r.get('error')} for r in records]}))
if len([r for r in records if r.get('HTTP_status')==200])!=4:raise SystemExit(1)
