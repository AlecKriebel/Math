from pathlib import Path
import datetime, hashlib, json, os, subprocess, urllib.request

A = Path(__file__).resolve().parent
D = A / 'private_sources'
D.mkdir(exist_ok=True)
OLD = A.parent / 'root_primary_sources_20261006' / 'private_sources'
events = []
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):
    return hashlib.sha256(b).hexdigest()
def save():
    (A/'ACTUAL_ACQUISITION_AND_RENDER.json').write_text(json.dumps({'operator_PID':os.getpid(),'UTC':now(),'events':events,'rendering_is_not_reading':True}, indent=2,sort_keys=True)+'\n')
sources = [
    ('turaev1986','https://webhomes.maths.ed.ac.uk/~v1ranick/papers/turaev1.pdf',[8,9,13,14,15,23]),
    ('turaev2002_survey','https://www.maths.tcd.ie/EMIS/journals/UW/gt/ftp/main/m4/m4l19.pdf',[1,2,3,4,5,6,7,8]),
    ('truman2006','https://arxiv.org/pdf/math/0611210',[1]),
]
for name,url,pages in sources:
    event={'name':name,'requested_URL':url,'requested_UTC':now()}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source audit'})
        with urllib.request.urlopen(request,timeout=40) as response:
            body=response.read()
            event.update({'final_URL':response.geturl(),'HTTP_status':response.status,'content_type':response.headers.get('Content-Type')})
        if not body.startswith(b'%PDF'):
            raise ValueError('Response is not a PDF')
        pdf=D/(name+'.pdf');pdf.write_bytes(body)
        event.update({'downloaded_UTC':now(),'bytes':len(body),'sha256':digest(body)})
        args=['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(D/(name+'.txt'))]
        child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=child.communicate()
        event.update({'extractor_PID':child.pid,'extractor_exit_code':child.returncode,'extractor_stderr_sha256':digest(err)})
        if child.returncode:
            raise RuntimeError(err.decode())
        text=(D/(name+'.txt')).read_bytes()
        event.update({'text_bytes':len(text),'text_sha256':digest(text),'page_count_from_form_feeds':len(text.decode().split('\f'))-1,'success':True})
    except Exception as error:
        event.update({'success':False,'error':str(error),'failed_UTC':now()})
    events.append(event);save()

renders=[('massuyeau_preprint',OLD,[17,18,19,20]),('alcaraz_v1',OLD,[15,16,17])]
renders += [(name,D,pages) for name,url,pages in sources if any(e.get('name')==name and e.get('success') for e in events)]
for name,base,pages in renders:
    full=(base/(name+'.txt')).read_text().split('\f')
    for page in pages:
        stem=D/(name+'_page_'+str(page));path=stem.with_suffix('.txt')
        path.write_text(full[page-1])
        args=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','125','-png',str(base/(name+'.pdf')),str(stem)]
        child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
        image=stem.with_suffix('.png')
        event={'render_source':name,'PDF_page_one_based':page,'render_PID':child.pid,'exit_code':child.returncode,'argv':args,'UTC':now(),'text_sha256':digest(path.read_bytes()),'stderr_sha256':digest(err)}
        if child.returncode==0:
            event.update({'image_bytes':image.stat().st_size,'image_sha256':digest(image.read_bytes())})
        events.append(event);save()
        if child.returncode:
            raise RuntimeError(err.decode())
print(json.dumps({'operator_PID':os.getpid(),'UTC':now(),'downloads_successful':sum(e.get('success',False) for e in events),'render_count':sum('render_source' in e for e in events)}))
