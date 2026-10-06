#!/usr/bin/env python3
"""GET-only citation-follow-up bodies; source bodies remain ignored and private."""
import concurrent.futures, datetime, hashlib, json, os, pathlib, subprocess, urllib.request
D=pathlib.Path(__file__).resolve().parent
P=D/'private_sources'; P.mkdir(exist_ok=True)
def ck(b,m):
    if not b: raise ValueError(m)
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(path):
    body=path.read_bytes()
    return {'relative_path':str(path.relative_to(D)), 'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
J={'schema':'pr117-original-question-citation-followups/v1','pid':os.getpid(),'started_utc':stamp(),'events':[],'new_proof_turns':0,'external_GET_only':True}
def emit(): (D/'FOLLOWUP_ACQUISITION_PROCESS_JOURNAL.json').write_text(json.dumps(J,indent=2,sort_keys=True)+'\n')
targets=[
 ('takagi_papers.html','https://www.ms.u-tokyo.ac.jp/~stakagi/paper.html','html'),
 ('openalex_citations.json','https://api.openalex.org/works?filter=cites:W2159499259&per-page=100','json'),
 ('blanco_encinas_1405.3942v5.pdf','https://arxiv.org/pdf/1405.3942v5','pdf'),
 ('badilla_leon_2305.00571v3.pdf','https://arxiv.org/pdf/2305.00571v3','pdf'),
 ('badilla_leon_published2025.pdf','https://link.springer.com/content/pdf/10.1007/s00009-025-02860-z.pdf','pdf'),
 ('laclair_published2025.pdf','https://link.springer.com/content/pdf/10.1007/s10801-025-01439-x.pdf','pdf'),
 ('hernandez_1112.2423v1.pdf','https://arxiv.org/pdf/1112.2423v1','pdf'),
 ('hernandez_1112.2427.pdf','https://arxiv.org/pdf/1112.2427','pdf'),
 ('teitler_1006.1915.pdf','https://arxiv.org/pdf/1006.1915','pdf'),
 ('thompson_1406.1788.pdf','https://arxiv.org/pdf/1406.1788','pdf'),
 ('takagi_adjoint2013.pdf','https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf','pdf'),
 ('schwede_tucker_1104.2000.pdf','https://arxiv.org/pdf/1104.2000','pdf'),
 ('generic_links_1908.03892.pdf','https://arxiv.org/pdf/1908.03892','pdf'),
 ('linkage_2406.05323.pdf','https://arxiv.org/pdf/2406.05323','pdf'),
 ('plus_pure_2501.07528.pdf','https://arxiv.org/pdf/2501.07528','pdf'),
 ('hibi_1201.5691.pdf','https://arxiv.org/pdf/1201.5691','pdf'),
 ('smith_basics_1309.4814.pdf','https://arxiv.org/pdf/1309.4814','pdf'),
 ('f_purity_1112.2424.pdf','https://arxiv.org/pdf/1112.2424','pdf'),
 ('arxiv_1405.3942.html','https://arxiv.org/abs/1405.3942','html'),
 ('arxiv_2305.00571.html','https://arxiv.org/abs/2305.00571','html'),
]
def get(target):
    name,url,kind=target
    ev={'utc':stamp(),'action':'public_GET','url':url,'destination':'private_sources/'+name,'kind':kind}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent priority audit)'})
        with urllib.request.urlopen(req,timeout=40) as res:
            body=res.read(12_000_001); ev.update({'http_status':res.status,'final_url':res.url})
        ck(len(body)<=12_000_000,'Body exceeds bounded retrieval cap')
        if kind=='pdf': ck(body.startswith(b'%PDF'),'Response is not actual PDF')
        if kind=='json': json.loads(body)
        dest=P/name
        if dest.exists(): ck(dest.read_bytes()==body,'Existing immutable source differs')
        else: dest.write_bytes(body)
        ev.update(pin(dest)); ev['status']='retrieved_and_pinned'
        if kind=='pdf':
            out=dest.with_suffix('.txt')
            r=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(dest),str(out)],capture_output=True,timeout=40,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'})
            ck(r.returncode==0 and len(r.stderr)==0,'PDF extraction failed')
            ev['text_extraction']={'returncode':r.returncode,'stderr_bytes':len(r.stderr),**pin(out)}
    except Exception as e: ev.update({'status':'unavailable','error_type':type(e).__name__,'error':str(e)})
    ev['finished_utc']=stamp()
    return ev
emit()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for ev in pool.map(get,targets): J['events'].append(ev); emit()
J['finished_utc']=stamp(); J['status']='complete_with_explicit_access_limits'; emit()
print(json.dumps({'pid':os.getpid(),'retrieved':sum(e['status']=='retrieved_and_pinned' for e in J['events']),'unavailable':[{'url':e['url'],'error':e.get('error')} for e in J['events'] if e['status']=='unavailable'],'status':J['status']},sort_keys=True))
