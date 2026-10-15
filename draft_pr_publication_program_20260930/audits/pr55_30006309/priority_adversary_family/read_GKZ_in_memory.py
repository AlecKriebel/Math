"""Fresh primary book retrieval in memory; no PDF or book-body file is retained."""
from pathlib import Path
from io import BytesIO
import datetime,hashlib,json,os,sys,urllib.request
from pypdf import PdfReader
F=Path(__file__).resolve().parent
u='https://webhomes.maths.ed.ac.uk/~v1ranick/papers/gelkapzel.pdf'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with urllib.request.urlopen(u,timeout=45) as r:
 b=r.read();headers=dict(r.headers);final=r.url
reader=PdfReader(BytesIO(b));selections=[]
for i,p in enumerate(reader.pages):
 s=p.extract_text() or ''
 if i>300 and ('massive' in s.lower() or ('Theorem 3.4' in s and 'Newton' in s)):
  selections.append({'pdf_page_index':i,'characters':len(s),'text_sha256':hashlib.sha256(s.encode()).hexdigest()})
  if 'Theorem 3.2' in s or 'Theorem 3.4' in s or 'Theorem 3.3' in s:
   print('SELECTED BOOK PAGE INDEX',i);print(s)
result={'schema':'pr55-priority-fresh-book-memory-retrieval/v1','url':u,'final_url':final,'actual_child_pid':os.getpid(),'argv':sys.argv,'started_utc':start,'body_and_selected_pages_read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf_bytes':len(b),'pdf_sha256':hashlib.sha256(b).hexdigest(),'pdf_pages':len(reader.pages),'selected_page_text_hashes':selections,'headers_selected':{k:v for k,v in headers.items() if k.lower() in ['content-type','content-length','last-modified','etag']},'pdf_or_whole_book_retained':False,'selected_book_text_persisted':False,'root_authority':False,'retrieval_scope':'Fresh content retrieved in memory; selected theorem text emitted for personal reading. This metadata is not a whole-process stream capture or ROOT certificate.'}
(F/'GKZ_FRESH_RETRIEVAL_METADATA.json').write_text(json.dumps(result,indent=2)+'\n')
print('RETRIEVAL_METADATA',json.dumps(result))
