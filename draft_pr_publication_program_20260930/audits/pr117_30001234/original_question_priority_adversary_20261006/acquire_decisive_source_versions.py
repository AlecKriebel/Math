#!/usr/bin/env python3
import concurrent.futures, datetime, hashlib, json, os, pathlib, subprocess, urllib.request
D=pathlib.Path(__file__).resolve().parent
P=D/'private_sources'; R=D/'private_renders'; P.mkdir(exist_ok=True); R.mkdir(exist_ok=True)
def ck(b,m):
    if not b: raise ValueError(m)
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(path):
    body=path.read_bytes(); return {'relative_path':str(path.relative_to(D)),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
J={'schema':'pr117-exact-prior-counterexample-source-verification/v1','pid':os.getpid(),'started_utc':stamp(),'events':[],'new_proof_turns':0,'external_GET_only':True}
def emit(): (D/'DECISIVE_SOURCE_PROCESS_JOURNAL.json').write_text(json.dumps(J,indent=2,sort_keys=True)+'\n')
targets=[
 ('takagi_1105.0072v1.pdf','https://arxiv.org/pdf/1105.0072v1','pdf'),
 ('takagi_1105.0072v5.pdf','https://arxiv.org/pdf/1105.0072v5','pdf'),
 ('arxiv_1105.0072.html','https://arxiv.org/abs/1105.0072','html'),
 ('msp_takagi_p06.xhtml','https://msp.org/ant/2013/7-4/p06.xhtml','html'),
]
def get(target):
    name,url,kind=target; ev={'utc':stamp(),'action':'public_GET','url':url,'kind':kind}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent priority audit)'})
        with urllib.request.urlopen(req,timeout=40) as response:
            body=response.read(12_000_001); ev.update({'http_status':response.status,'final_url':response.url})
        ck(len(body)<=12_000_000,'bounded body limit')
        if kind=='pdf': ck(body.startswith(b'%PDF'),'Response not PDF')
        dest=P/name
        if dest.exists(): ck(dest.read_bytes()==body,'Existing immutable source differs')
        else: dest.write_bytes(body)
        ev.update(pin(dest)); ev['status']='retrieved_and_pinned'
        if kind=='pdf':
            out=dest.with_suffix('.txt'); argv=['/opt/homebrew/bin/pdftotext','-layout',str(dest),str(out)]
            res=subprocess.run(argv,capture_output=True,timeout=40,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
            ck(res.returncode==0 and len(res.stderr)==0,'PDF extraction failed')
            ev['private_text_extraction']={'returncode':res.returncode,'stderr_bytes':len(res.stderr),**pin(out)}
    except Exception as e: ev.update({'status':'unavailable','error_type':type(e).__name__,'error':str(e)})
    ev['finished_utc']=stamp(); return ev
emit()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for ev in pool.map(get,targets): J['events'].append(ev); emit()
pages=[('takagi_adjoint2013.pdf',[22,24,25])]
for name,nums in pages:
    for num in nums:
        prefix=R/(pathlib.Path(name).stem+'_physical_p'+str(num))
        argv=['/opt/homebrew/bin/pdftoppm','-f',str(num),'-l',str(num),'-singlefile','-r','180','-png',str(P/name),str(prefix)]
        ev={'utc':stamp(),'action':'render_actual_source_page','argv':argv,'physical_page_1_based':num,'source_pin':pin(P/name)}
        J['events'].append(ev); emit()
        res=subprocess.run(argv,capture_output=True,timeout=40,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
        ck(res.returncode==0 and len(res.stderr)==0,'Actual source render failed')
        ev.update({'returncode':res.returncode,'stderr_bytes':len(res.stderr),'status':'actual_source_rendered',**pin(prefix.with_suffix('.png'))}); emit()
J['finished_utc']=stamp(); J['status']='complete_with_explicit_access_limits'; emit()
print(json.dumps({'pid':os.getpid(),'status':J['status'],'events':len(J['events']),'unavailable':[e['url'] for e in J['events'] if e['status']=='unavailable']},sort_keys=True))
