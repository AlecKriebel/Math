"""Fresh primary-source and immutable checkpoint receipt capture; GET requests only."""
from capture import *
import urllib.request
URLS={
 'owr1141':'https://ems.press/content/serial-article-files/51353',
 'owr1142':'https://ems.press/content/serial-article-files/46403',
 'petiard2019':'https://libra.unine.ch/bitstreams/cb35ac23-61a8-402a-9fdb-a1eb4d47c041/download',
 'owr1143':'https://ems.press/content/serial-article-files/46308',
 'owr1144':'https://ems.press/content/serial-article-files/46383',
 'owr1145':'https://ems.press/content/serial-article-files/46540',
 'hlost':'https://arxiv.org/pdf/1505.06445v3',
 'owr1146':'https://ems.press/content/serial-article-files/46494',
 'mos':'https://ems.press/content/serial-article-files/26354',
 'owr1147landing':'https://doi.org/10.4171/owr/2013/18',
 'owr1148':'https://ems.press/content/serial-article-files/46507',
 'bdim':'https://arxiv.org/pdf/1807.03992v1',
 'owr1149':'https://ems.press/content/serial-article-files/46530',
 'owr1150':'https://ems.press/content/serial-article-files/46609',
}
def source(item):
    name,url=item
    try:
        with urllib.request.urlopen(url,timeout=80) as r:
            data=r.read(); final=r.url; status=r.status
        ext='.pdf' if data.startswith(b'%PDF') else '.html'
        rec=save(PRIVATE/'sources'/(name+ext),data)
        rec.update(name=name,url=url,final_url=final,status=status,captured=now())
    except Exception as e: rec={'name':name,'url':url,'error':str(e),'captured':now()}
    return rec
def receipt(path):
    obj=json.loads(api(f'contents/{path}?ref={CHECKPOINT}'))
    data=base64.b64decode(obj['content'])
    assert hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==obj['sha']
    rec=save(PRIVATE/'checkpoint'/path,data)
    rec.update(remote_path=path,git_blob_sha=obj['sha'],checkpoint=CHECKPOINT)
    return rec
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        results=list(pool.map(source,URLS.items()))
    save(PRIVATE/'primary_source_receipts.json',json.dumps(results,indent=2).encode())
    root=HERE.parents[1]
    paths=[str(f.relative_to(root.parent)) for n in range(1141,1151) for f in root.glob(f'PR{n}_*.json')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(receipt,paths))
    save(PRIVATE/'checkpoint_receipts.json',json.dumps(results,indent=2).encode())
    print(json.dumps({'sources':len(URLS),'checkpoint_receipts':len(results)}))
