from pathlib import Path
import datetime, hashlib, html.parser, json, os, subprocess, urllib.error, urllib.request

D=Path(__file__).resolve().parent
P=D/'private'
class Extract(html.parser.HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.hidden=0
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.hidden+=1
        elif t in ('p','div','section','h1','h2','h3','li','br','tr'):self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('script','style'):self.hidden=max(0,self.hidden-1)
    def handle_data(self,t):
        if not self.hidden:self.parts.append(t)

sources=[
 ('regnier_2022.pdf','https://sites.santafe.edu/~redner/pubs/pdf/PhysRevE.105.064104.pdf'),
 ('collaboration_2023.html','https://arxiv.org/html/2302.14241v1'),
]
rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name,url in sources:
    row={'name':name,'URL':url,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:
            body=r.read(3_000_001);row.update(HTTP=r.status,final_URL=r.url,content_type=r.headers.get('Content-Type'))
        if len(body)>3_000_000:raise RuntimeError('bounded retrieval size exceeded')
        if name.endswith('.pdf') and not body.startswith(b'%PDF'):raise RuntimeError('not a PDF')
        dest=P/name
        if dest.exists():raise RuntimeError('refusing overwrite')
        dest.write_bytes(body)
        row.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),private_path=str(dest))
        if name.endswith('.html'):
            parser=Extract();parser.feed(body.decode('utf-8','replace'));(P/(name+'.txt')).write_text(''.join(parser.parts))
        else:
            proc=subprocess.Popen(['/opt/homebrew/bin/pdftotext','-layout',str(dest),str(P/(name+'.txt'))],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            try:out,err=proc.communicate(timeout=25)
            except subprocess.TimeoutExpired:proc.kill();out,err=proc.communicate();raise RuntimeError('extraction timeout; killed/reaped')
            row['extract_child']={'pid':proc.pid,'exit_code':proc.returncode,'reaped':proc.poll() is not None,'stderr':err.decode('utf-8','replace')}
            if proc.returncode:raise RuntimeError('extraction failed')
        textpath=P/(name+'.txt');txt=textpath.read_bytes()
        row.update(text_bytes=len(txt),text_sha256=hashlib.sha256(txt).hexdigest())
        print(name,'OK',len(body),flush=True)
    except Exception as e:
        row.update(error_type=type(e).__name__,error=str(e))
        if isinstance(e,urllib.error.HTTPError):row['HTTP']=e.code
        print(name,'FAIL',type(e).__name__,str(e),flush=True)
    rows.append(row)
receipt={'schema':'pr141-priority-followup-primary-retrieval/v1','actual_agent_PID':os.getpid(),'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows,'full_third_party_bodies_private_and_ignored':True}
(D/'FOLLOWUP_RETRIEVAL.json').write_text(json.dumps(receipt,indent=2)+'\n')
