from pathlib import Path
import urllib.request, hashlib, datetime, json
root=Path(__file__).resolve().parent
sources=[
('stubborn_v1_pdf','https://arxiv.org/pdf/2602.01191v1','stubborn_v1.pdf'),
('stubborn_current_record','https://arxiv.org/abs/2602.01191','stubborn_current_record.html'),
('stubborn_v1_record','https://arxiv.org/abs/2602.01191v1','stubborn_v1_record.html'),
('owr_2023_14','https://ems.press/content/serial-article-files/47007','owr.pdf'),
('bkr_pdf','https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C4BAF1C7EBA17DE741C36DB40691412/S2050509426102217a.pdf/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares.pdf','bkr.pdf'),
('stubborn_author_current_status','https://sites.google.com/site/grrigg/','blekherman_current.html'),
('bkr_publisher','https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares/7C4BAF1C7EBA17DE741C36DB40691412','bkr.html')]
receipts=[]
if (root/'sources'/'FETCH_RECEIPTS.json').exists():
  receipts=json.loads((root/'sources'/'FETCH_RECEIPTS.json').read_text())
for name,url,filename in sources:
  previous=next((r for r in reversed(receipts) if r['id']==name and 'error' not in r),None)
  if previous and (root/previous['private_path']).exists() and hashlib.sha256((root/previous['private_path']).read_bytes()).hexdigest()==previous['sha256']: continue
  stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
  item={'id':name,'requested_url':url,'retrieved_utc':stamp,'private_path':'sources/private/'+filename}
  try:
    request=urllib.request.Request(url,headers={'User-Agent':'Independent mathematics source audit/1.0'})
    with urllib.request.urlopen(request,timeout=55) as response:
      body=response.read(); item.update(final_url=response.url,status=response.status,content_type=response.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
    (root/item['private_path']).write_bytes(body)
  except Exception as exc: item.update(error=str(exc))
  receipts.append(item)
(root/'sources'/'FETCH_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
for x in receipts: print(x['id'],x.get('bytes'),x.get('sha256'),x.get('error'))
