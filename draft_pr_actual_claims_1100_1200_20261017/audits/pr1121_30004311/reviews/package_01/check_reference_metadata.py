from pathlib import Path
import concurrent.futures,datetime,hashlib,json,re,urllib.request
A=Path(__file__).resolve().parent
ids=['1511.08477','1705.08493','2001.08905','2401.12904','2608.01884','2609.20401','2609.24640']
dois=['10.1016/j.jpaa.2017.07.017','10.4171/OWR/2019/51','10.1016/j.jalgebra.2016.01.038','10.1142/S0219199718500426','10.4171/rmi/1168','10.1016/j.jpaa.2020.106476','10.1016/j.jpaa.2025.108025','10.1016/j.jalgebra.2020.04.004','10.1016/j.jalgebra.2022.03.008']
def arxiv(ident):
 url='https://arxiv.org/abs/'+ident
 out={'arxiv_id':ident,'url':url}
 try:
  with urllib.request.urlopen(url,timeout=30) as r:raw=r.read();out['status']=r.status
  (A/'sources/private'/('abs-'+ident+'.html')).write_bytes(raw)
  text=raw.decode();out['bytes']=len(raw);out['sha256']=hashlib.sha256(raw).hexdigest()
  out['version_markers']=sorted(set(re.findall(r'\[v(\d+)\]',text)))
  out['title']=re.search(r'<meta name="citation_title" content="(.*?)"',text).group(1)
  out['citation_date']=re.search(r'<meta name="citation_date" content="(.*?)"',text).group(1)
  out['history_dates']=re.findall(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} [A-Z][a-z]{2} \d{4} \d\d:\d\d:\d\d UTC',text)
 except Exception as e:out['error']=str(e)
 return out
def crossref(doi):
 out={'doi':doi,'url':'https://doi.org/'+doi}
 try:
  with urllib.request.urlopen('https://api.crossref.org/works/'+doi,timeout=30) as r:m=json.load(r)['message'];out['status']=r.status
  out.update(title=m.get('title'),author=[{'given':x.get('given'),'family':x.get('family')} for x in m.get('author',[])],volume=m.get('volume'),issue=m.get('issue'),page=m.get('page'),article_number=m.get('article-number'),published=m.get('published'),container_title=m.get('container-title'))
 except Exception as e:out['error']=str(e)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 versions=list(pool.map(arxiv,ids));references=list(pool.map(crossref,dois))
(A/'REFERENCE_METADATA_CHECK.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_arxiv_records':versions,'doi_metadata':references},indent=2)+'\n')
print(json.dumps({'current_arxiv_records':versions,'doi_metadata':references},indent=2))
