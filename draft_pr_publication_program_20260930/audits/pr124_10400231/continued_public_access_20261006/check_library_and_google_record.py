"""Check public catalogue and preview endpoints; no borrowing/login/download bypass."""
from pathlib import Path
import datetime,hashlib,json,os,re,urllib.request,urllib.error
D=Path(__file__).resolve().parent;S=D/'private_sources';S.mkdir(exist_ok=True)
dest=D/'ACTUAL_LIBRARY_AND_GOOGLE_PROBE.json'
if dest.exists():raise RuntimeError('Actual probe already exists; inspect before repeating')
events=[]
for name,url in [
 ('archive_metadata','https://archive.org/metadata/torsionsdimensio00tura'),
 ('openlibrary_edition','https://openlibrary.org/books/OL3565865M.json'),
 ('google_isbn_preview','https://books.google.com/books?vid=ISBN9783764369118')]:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();body=b'';status=None;final=url;error=None;ctype=None
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; mathematical-source-audit)'}),timeout=20) as r:body=r.read();status=r.status;final=r.url;ctype=r.headers.get('Content-Type')
 except urllib.error.HTTPError as e:body=e.read();status=e.code;error=str(e);ctype=e.headers.get('Content-Type')
 except Exception as e:error=str(e)
 p=S/(name+('.json' if name!='google_isbn_preview' else '.html'));p.write_bytes(body)
 event={'name':name,'requested_URL':url,'final_URL':final,'requested_UTC':start,'completed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HTTP_status':status,'content_type':ctype,'error':error,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'private_response_path':str(p)}
 if status==200 and name=='archive_metadata':
  x=json.loads(body);event['top_level_keys']=sorted(x);event['is_dark']=x.get('is_dark');event['metadata']={k:x.get('metadata',{}).get(k) for k in ['identifier','title','creator','date','access-restricted-item','collection','isbn']};event['file_count']=len(x.get('files',[]));event['file_metadata']=[{k:f.get(k) for k in ['name','format','private']} for f in x.get('files',[]) if f.get('name','').endswith(('.pdf','_djvu.txt'))]
 elif status==200 and name=='openlibrary_edition':
  x=json.loads(body);event['edition_metadata']={k:x.get(k) for k in ['key','title','isbn_10','isbn_13','publish_date','ocaid','identifiers','works']}
 elif status==200:
  s=body.decode('utf8','replace');event['page_titles']=re.findall(r'<title>(.*?)</title>',s,re.S);event['preview_link_candidates']=sorted(set(re.findall(r'https?://(?:books\.google\.com|play\.google\.com)[^\s"<>]+',s)))[:15];event['access_labels']=[label for label in ['No preview available','Preview this book','Sign in','Book not found','Try these suggestions'] if label.lower() in s.lower()]
 events.append(event)
receipt={'schema':'pr124-public-library-and-Google-book-catalogue-probe/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'events':events,'no_login_borrow_or_purchase':True,'no_full_book_chapter_read':True,'catalogue_not_theorem_evidence':True,'priority_clearance':False,'shared_index_tracked_or_service_mutations':False,'root_writer_released':True}
dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps(receipt))
