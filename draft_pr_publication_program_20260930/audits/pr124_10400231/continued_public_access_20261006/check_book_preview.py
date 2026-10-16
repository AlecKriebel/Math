"""Bounded read-only public Google Books metadata probe; never treats snippets as fulltext."""
from pathlib import Path
import datetime,hashlib,json,os,urllib.request,urllib.parse
D=Path(__file__).resolve().parent;S=D/'private_sources';S.mkdir(exist_ok=True)
out=D/'ACTUAL_BOOK_PREVIEW_PROBE.json'
if out.exists():raise RuntimeError('Completed preview probe exists; inspect before rerun')
events=[]
for name,query in [('hardcover','isbn:9783764369118'),('ebook','isbn:9783034879996'),('exact_title','intitle:Torsions of 3-dimensional Manifolds inauthor:Turaev')]:
 url='https://www.googleapis.com/books/v1/volumes?'+urllib.parse.urlencode({'q':query,'maxResults':10})
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();body=b'';status=None;error=None;final=url
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Math-priority-source-audit/1.0'}),timeout=20) as r:body=r.read();status=r.status;final=r.url
 except urllib.error.HTTPError as e:body=e.read();status=e.code;error=str(e)
 except Exception as e:error=str(e)
 path=S/(name+'.json');path.write_bytes(body)
 record={'name':name,'query':query,'requested_URL':url,'final_URL':final,'requested_UTC':start,'completed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HTTP_status':status,'error':error,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'private_response_file':str(path)}
 if status==200:
  parsed=json.loads(body);record['totalItems']=parsed.get('totalItems');record['volumes']=[{'id':x.get('id'),'volumeInfo':{k:x.get('volumeInfo',{}).get(k) for k in ['title','authors','publishedDate','industryIdentifiers','previewLink','infoLink','canonicalVolumeLink']},'accessInfo':{k:x.get('accessInfo',{}).get(k) for k in ['viewability','embeddable','publicDomain','textToSpeechPermission','epub','pdf','webReaderLink','accessViewStatus']}} for x in parsed.get('items',[])]
 events.append(record)
 if status==429:break
receipt={'schema':'pr124-lawful-public-book-preview-probe/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'events':events,'provider_mutation':False,'source_chapter_fulltext_read':False,'snippet_not_theorem_evidence':True,'source_gap_resolved':False,'publication_clearance':False,'root_shared_writer_released':True,'shared_tracked_index_changes':False}
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt))
