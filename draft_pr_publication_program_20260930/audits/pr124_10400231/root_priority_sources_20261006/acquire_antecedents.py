from pathlib import Path
import datetime,hashlib,json,os,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'private_sources';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save():
    (A/'ACTUAL_ANTECEDENT_ACCESS.json').write_text(json.dumps({'UTC':now(),'actual_operator_PID':os.getpid(),'events':events},indent=2,sort_keys=True)+'\n')
for name,url in [
 ('nicolaescu_book','https://www3.nd.edu/~lnicolae/Torsion.pdf'),
 ('turaev_book_full_access_attempt','https://link.springer.com/content/pdf/10.1007/978-3-0348-7999-6.pdf'),
 ('turaev_book_chapter_II_access_attempt','https://link.springer.com/content/pdf/10.1007/978-3-0348-7999-6_2.pdf'),
 ('turaev_book_chapter_III_access_attempt','https://link.springer.com/content/pdf/10.1007/978-3-0348-7999-6_3.pdf')]:
    e={'name':name,'URL':url,'requested_UTC':now()}
    try:
        with urllib.request.urlopen(url,timeout=25) as r:
            body=r.read();e.update({'HTTP_status':r.status,'final_URL':r.geturl(),'content_type':r.headers.get('Content-Type'),'bytes':len(body),'sha256':sha(body),'UTC':now()})
        is_pdf=body.startswith(b'%PDF');e['valid_PDF']=is_pdf
        (D/(name+('.pdf' if is_pdf else '.html'))).write_bytes(body)
        if is_pdf:
            args=['/opt/homebrew/bin/pdftotext','-layout',str(D/(name+'.pdf')),str(D/(name+'.txt'))]
            child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
            e.update({'extractor_PID':child.pid,'extractor_exit_code':child.returncode,'stderr_sha256':sha(err)})
            if child.returncode==0:
                t=(D/(name+'.txt')).read_bytes();e.update({'text_bytes':len(t),'text_sha256':sha(t)})
    except Exception as error:
        e.update({'valid_PDF':False,'error':str(error),'UTC':now()})
    events.append(e);save()
print(json.dumps({'operator_PID':os.getpid(),'UTC':now(),'PDFs':sum(e.get('valid_PDF',False) for e in events),'failed_PDF_requests':sum(not e.get('valid_PDF',False) for e in events)}))
