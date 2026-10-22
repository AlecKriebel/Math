#!/usr/bin/env python3
"""Fetch primary bytes into memory only; pin access, versions and extraction.

No PDF, full extracted text, HTML, or provider response is saved by this script.
Optional --show-relevant prints selected primary extracts for human reading.
"""
from pathlib import Path
import datetime, hashlib, json, subprocess, urllib.request, sys

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/'submitted/unsolved_math_prioritization/attempts/9700040/source_manifest.json'
URLS=[
 ('question','https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html',None),
 ('patience1993','https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf',(36,39)),
 ('ad1999','https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf',(5,7)),
 ('or2003v3','https://arxiv.org/pdf/math/0107056v3',(8,9)),
 ('psasp_published2018','https://www.math.umb.edu/~vuletic/Site/Research_files/PSASP.pdf',(35,36)),
 ('ad1995_context','https://www.stat.berkeley.edu/~aldous/Papers/me71.pdf',(1,1)),
 ('psasp_arxiv_v3_fallback','https://arxiv.org/pdf/1407.3764v3',(23,25))]

def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    pins={s['url']:s for s in json.loads(ORIGINAL.read_text())['sources']}
    rows=[]
    for key,url,pages in URLS:
        r={'key':key,'requested_url':url,'started_utc':stamp(),'storage':'memory only; full bytes/text excluded'}
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'IndependentSourceAudit/1.0'})
            with urllib.request.urlopen(req,timeout=35) as response:
                b=response.read()
                r.update({'status':response.status,'final_url':response.geturl(),'headers':{
                    k:response.headers.get(k) for k in ('Content-Type','Content-Length','Last-Modified','ETag')},
                    'bytes':len(b),'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()})
            if url in pins:
                p=pins[url];r['matches_original_size_sha256']=len(b)==p['bytes'] and r['sha256']==p['sha256']
            if pages:
                info=subprocess.run(['pdfinfo','-'],input=b,capture_output=True,check=True).stdout.decode(errors='replace')
                r['pdfinfo_selected']=[line for line in info.splitlines() if line.startswith(('Title:','Author:','Creator:','Producer:','CreationDate:','ModDate:','Pages:','PDF version:'))]
                t=subprocess.run(['pdftotext','-f',str(pages[0]),'-l',str(pages[1]),'-layout','-','-'],input=b,capture_output=True,check=True).stdout
                r['inspected_pdf_pages_1based']=list(pages)
                r['extracted_selection_bytes']=len(t);r['extracted_selection_sha256']=hashlib.sha256(t).hexdigest()
                if '--show-relevant' in sys.argv and key=='psasp_arxiv_v3_fallback':print(t.decode(errors='replace'))
            r['completed_utc']=stamp()
        except Exception as e:
            r.update({'error_type':type(e).__name__,'error':str(e),'completed_utc':stamp()})
        rows.append(r)
    out={'utc':stamp(),'sources':rows,'primary_publication_web_tool_access':{
        'url':URLS[4][1],'observed_pdf_pages':38,'inspected_printed_pages':[415,416],
        'observed_equation':'(6.6)','content':'exponential specialization equals skew standard-tableau count times t^degree/degree factorial; Poissonized RSK discussion',
        'limitation':'web provider itself did not expose raw PDF bytes; independent urllib raw fetch results are recorded separately above'},
        'policy':'Third-party full PDFs/text/HTML/provider responses excluded from public artifacts; only metadata, hashes, locators and authored descriptions retained.'}
    (HERE/'SOURCE_ACCESS_RECEIPTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'COMPLETE' if all('sha256' in r for r in rows) else 'COMPLETE_WITH_ACCESS_LIMITS','source_count':len(rows),
                      'raw_successes':sum('sha256' in r for r in rows),
                      'pinned_original_matches':sum(r.get('matches_original_size_sha256',False) for r in rows),
                      'errors':[{'key':r['key'],'error':r['error']} for r in rows if 'error' in r]},indent=2))

if __name__=='__main__':main()
