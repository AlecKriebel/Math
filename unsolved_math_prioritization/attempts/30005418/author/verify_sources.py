#!/usr/bin/env python3
"""Optional rehash of separately provided inputs; emits metadata, never source text."""
import hashlib,json,pathlib,sys
if not __debug__:raise SystemExit('Do not disable assertions.')
def metadata(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    if len(sys.argv)!=5:raise SystemExit('Usage: verify_sources.py PROBLEMS REPORTS CATALOG PDF_DIRECTORY')
    pth,rth,cth,pdfdir=map(pathlib.Path,sys.argv[1:]);expected=json.loads(pathlib.Path(__file__).with_name('SOURCES.json').read_text());loaded=[];corpus={}
    for name,path in zip(('problems.json','research_results.json','catalog.json'),(pth,rth,cth)):
        b=path.read_bytes();corpus[name]=metadata(b);assert corpus[name]==expected['dataset']['files'][name];loaded.append(json.loads(b))
    P,R,C=loaded;selected=[p for p in P if p['id']==30005418];assert len(selected)==1;p=selected[0]
    assert p['problem_number']=='OWR-12697689-014';assert p['problem_number'] not in R
    assert sum(q['problem_number']==p['problem_number'] for q in P)==1
    c=next(c for c in C if c['id']=='30005418');assert c['rank']==797
    sh=hashlib.sha256(p['statement'].encode()).hexdigest();rh=hashlib.sha256(json.dumps([p,{}],sort_keys=True).encode()).hexdigest()
    assert sh==c['statement_hash']==expected['dataset']['statement_hash'];assert rh==c['review_hash']==expected['dataset']['review_hash']
    b=cth.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==expected['dataset']['catalog_git_blob']
    pdfs=[]
    for s in expected['sources']:
        b=(pdfdir/s['filename']).read_bytes();assert b.startswith(b'%PDF-');m=metadata(b);assert m==s['pdf'];pdfs.append({'title':s['title'],'url':s['url'],**m,'match':True})
    print(json.dumps({'status':'PASS','id':30005418,'corpora':corpus,'statement_hash':sh,'review_hash':rh,'catalog_git_blob':blob,'pdfs':pdfs,'scope':'Byte/identity replay only; no new source-text inspection.'},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
