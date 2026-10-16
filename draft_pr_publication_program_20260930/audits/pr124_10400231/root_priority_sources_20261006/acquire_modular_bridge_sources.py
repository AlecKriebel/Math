from pathlib import Path
import datetime,hashlib,json,os,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'private_sources';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save():
    (A/'ACTUAL_MODULAR_BRIDGE_SOURCE_ACQUISITION.json').write_text(json.dumps({'operator_PID':os.getpid(),'UTC':now(),'events':events,'rendering_is_not_reading':True},indent=2,sort_keys=True)+'\n')
for name,url,expected,pages in [
 ('truman_thesis2006','https://drum.lib.umd.edu/bitstreams/bdff5925-5370-4b7a-914c-34b29a1f6b91/download','3c77621dd7b99bae783e81bcc2202c2bb544ddb8579dc816e1bce679226465f3',[1,44,54]),
 ('ye2023','https://msp.org/agt/2023/23-3/agt-v23-n3-p03-p.pdf','a0826ffde2756ece13fe0e111505892b0f40c57d9926147542fe614db654672c',[1,36,37])]:
    e={'name':name,'URL':url,'requested_UTC':now(),'expected_SHA256':expected}
    try:
        with urllib.request.urlopen(url,timeout=35) as r:
            b=r.read();e.update({'HTTP_status':r.status,'final_URL':r.geturl(),'content_type':r.headers.get('Content-Type'),'bytes':len(b),'sha256':sha(b),'downloaded_UTC':now()})
        if not b.startswith(b'%PDF') or sha(b)!=expected:raise ValueError('PDF magic/hash mismatch')
        (D/(name+'.pdf')).write_bytes(b)
        argv=['/opt/homebrew/bin/pdftotext','-layout',str(D/(name+'.pdf')),str(D/(name+'.txt'))]
        child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
        e.update({'extractor_PID':child.pid,'extractor_exit_code':child.returncode,'stderr_sha256':sha(err)})
        if child.returncode:raise RuntimeError(err.decode())
        txt=(D/(name+'.txt')).read_bytes();e.update({'text_bytes':len(txt),'text_sha256':sha(txt),'success':True})
        full=txt.decode().split('\f')
        e['renders']=[]
        for page in pages:
            stem=D/(name+'_page_'+str(page));stem.with_suffix('.txt').write_text(full[page-1])
            argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','125','-png',str(D/(name+'.pdf')),str(stem)]
            child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
            entry={'PDF_page_one_based':page,'render_PID':child.pid,'exit_code':child.returncode,'argv':argv,'UTC':now(),'stderr_sha256':sha(err)}
            if child.returncode:raise RuntimeError(err.decode())
            entry.update({'image_bytes':stem.with_suffix('.png').stat().st_size,'image_sha256':sha(stem.with_suffix('.png').read_bytes()),'text_sha256':sha(stem.with_suffix('.txt').read_bytes())});e['renders'].append(entry)
    except Exception as error:
        e.update({'success':False,'error':str(error),'UTC':now()})
    events.append(e);save()
print(json.dumps({'operator_PID':os.getpid(),'UTC':now(),'successful_full_source_downloads':sum(e.get('success',False) for e in events)}))
