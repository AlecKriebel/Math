import urllib.request,pathlib,json,hashlib,datetime,concurrent.futures
h=pathlib.Path(__file__).resolve().parent;s=h/'tmp/primary';s.mkdir(exist_ok=True)
urls={
 'OWR.pdf':'https://ems.press/content/serial-article-files/46818',
 'FW-v4.pdf':'https://arxiv.org/pdf/math/0510470v4',
 'ST.html':'https://arxiv.org/html/0704.3471',
 'A-2020.pdf':'https://webusers.imj-prg.fr/~karim.adiprasito/cint.pdf',
 'HSWW-v2.pdf':'https://arxiv.org/pdf/2606.10817v2',
 'HSWW-v2.html':'https://arxiv.org/html/2606.10817v2',
 'AB-published.html':'https://oup.silverchair-cdn.com/article-minimal/4085561',
 'BW.pdf':'https://www.math.miami.edu/~wachs/papers/nonpure1.pdf',
 'A-publisher.html':'https://link.intlpress.com/JDetail/1806163228180819970',
 'A-institution.html':'https://cris.huji.ac.il/en/publications/a-note-on-the-topology-of-minkowski-sums-and-complete-intersectio/',
 'FrickSanyal-v2.pdf':'https://arxiv.org/pdf/1607.07814v2',
}
def get(item):
 name,url=item;rec={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'}),timeout=40) as r:
   b=r.read();rec.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  (s/name).write_bytes(b)
 except Exception as e:rec['error']=str(e)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:r=list(ex.map(get,urls.items()))
(h/'evidence/PRIMARY_RETRIEVAL.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
