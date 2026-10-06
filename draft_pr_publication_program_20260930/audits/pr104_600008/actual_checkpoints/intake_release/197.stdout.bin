"""Retrieve publicly accessible primary sources; retain actual HTTP and extraction evidence."""
from pathlib import Path
import urllib.request,json,hashlib,datetime,subprocess,os
A=Path(__file__).resolve().parent
D=A/'primary_sources_20261006';D.mkdir(exist_ok=False)
source=json.loads((A/'original_source_authentication_20261006/original_attempt/source_manifest.json').read_text())
records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump():
    (D/'RETRIEVAL_MANIFEST.json').write_text(json.dumps({'UTC':now(),'operator_PID':os.getpid(),'records':records,'third_party_fulltexts_private':True},indent=2,sort_keys=True)+'\n')
for item in source['sources']:
    record={'file':item['file'],'requested_url':item['url'],'UTC_start':now(),'original_expected_sha256':item['sha256']}
    records.append(record)
    try:
        request=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0 mathematical research source verification'})
        with urllib.request.urlopen(request,timeout=45) as response:
            data=response.read(10*1024*1024+1)
            record.update({'HTTP_status':response.status,'final_url':response.url,'response_headers':dict(response.headers)})
        if len(data)>10*1024*1024 or not data.startswith(b'%PDF-'):raise RuntimeError('not a bounded PDF response')
        record.update({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'matches_submitted_pin':hashlib.sha256(data).hexdigest()==item['sha256']})
        path=D/item['file'];path.write_bytes(data)
        argv=['/opt/homebrew/bin/pdftotext','-layout',str(path),str(path.with_suffix('.txt'))]
        start=now();process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=process.communicate()
        path.with_suffix('.extraction.stdout.bin').write_bytes(out);path.with_suffix('.extraction.stderr.bin').write_bytes(err)
        record['extraction']={'argv':argv,'PID':process.pid,'UTC_start':start,'UTC_end':now(),'exit_code':process.returncode,
          'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()}
        if process.returncode:raise RuntimeError('PDF extraction failed')
        record['text_sha256']=hashlib.sha256(path.with_suffix('.txt').read_bytes()).hexdigest()
    except Exception as exc:
        record['error']=str(exc)
    record['UTC_end']=now();dump()
print(json.dumps({'directory':str(D),'records':records}))
if any('error' in r for r in records):raise SystemExit(1)
