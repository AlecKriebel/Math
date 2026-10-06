from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;D=A/'private_sources';events=[]
def sha(b):return hashlib.sha256(b).hexdigest()
for name,pages in [('nicolaescu_book',[80,81,140,141]),('truman2006',[14,20,21])]:
    full=(D/(name+'.txt')).read_text().split('\f')
    for page in pages:
        stem=D/(name+'_page_'+str(page));stem.with_suffix('.txt').write_text(full[page-1])
        argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','125','-png',str(D/(name+'.pdf')),str(stem)]
        child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
        event={'source':name,'PDF_page_one_based':page,'render_PID':child.pid,'exit_code':child.returncode,'argv':argv,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stderr_sha256':sha(err)}
        if child.returncode==0:event.update({'image_bytes':stem.with_suffix('.png').stat().st_size,'image_sha256':sha(stem.with_suffix('.png').read_bytes()),'text_sha256':sha(stem.with_suffix('.txt').read_bytes())})
        events.append(event)
        if child.returncode:raise RuntimeError(err.decode())
(A/'ACTUAL_EXTRA_PAGE_RENDER.json').write_text(json.dumps({'operator_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':events,'rendering_is_not_reading':True},indent=2,sort_keys=True)+'\n')
print(json.dumps({'operator_PID':os.getpid(),'rendered_pages':len(events)}))
