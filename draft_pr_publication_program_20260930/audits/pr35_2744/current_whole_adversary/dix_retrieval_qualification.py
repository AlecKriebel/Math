from pathlib import Path
import urllib.request,json,datetime,hashlib
h=Path(__file__).resolve().parent;url='https://escholarship.org/content/qt27j2v475/qt27j2v475_noSplash_7f3e70d717e17eaf9515cffc4ef313be.pdf'
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'scope':'Separate retry receipt. The initial assertion failure is preserved unchanged in SOURCE_RETRIEVAL. Fresh official web operative proof was genuinely read; no local historical PDF hash certified.'}
try:
 with urllib.request.urlopen(url,timeout=45) as x:b=x.read();r.update(http_status=x.status,final_url=x.url,headers=dict(x.headers),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),is_pdf=b.startswith(b'%PDF'))
 (h/'tmp/dix_retry_response.bin').write_bytes(b)
except Exception as e:r.update(error=repr(e))
(h/'DIX_RETRIEVAL_QUALIFICATION.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
