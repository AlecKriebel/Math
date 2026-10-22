"""Bounded unauthenticated primary-source GETs; retain receipt only, no duplicate bodies."""
import concurrent.futures,datetime,hashlib,json,pathlib,urllib.request
O=pathlib.Path(__file__).resolve().parent;B=O.parents[1]
def one(v):
 p=v['prior_source'];url=p['url'];at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-source-audit/1.0'}),timeout=45)as r:
   h=hashlib.sha256();n=0
   while True:
    z=r.read(65536)
    if not z:break
    n+=len(z)
    if n>6*1024*1024:raise ValueError('bounded cap exceeded')
    h.update(z)
   return {'pr':v['pr'],'at':at,'url':url,'final_url':r.url,'status':r.status,'bytes':n,'sha256':h.hexdigest(),'expected':p.get('sha256'),'hash_matches':h.hexdigest()==p.get('sha256'),'body_saved':False}
 except Exception as e:return {'pr':v['pr'],'at':at,'url':url,'error':type(e).__name__+': '+str(e),'body_saved':False}
v=json.loads((B/'audits/prior_source_accounting_tail_review01/NINE_CASE_EVIDENCE_MATRIX.json').read_text())['cases']
v += [{'pr':1189,'prior_source':{'url':'https://webhomes.maths.ed.ac.uk/cook/iss_no60.PDF','sha256':hashlib.sha256((B/'audits/pr1189_finite_ceiling_prior_review/private_sources/freud1993.pdf').read_bytes()).hexdigest()}},{'pr':1224,'prior_source':{'url':'https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos783-3.pdf','sha256':hashlib.sha256(__import__('gzip').decompress((B/'audits/pr1224_2302/existing_source_row_whole_review01/private/tao3.pdf.gz').read_bytes())).hexdigest()}}]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:r=list(ex.map(one,v))
(O/'FRESH_SOURCE_GETS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
