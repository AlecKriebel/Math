from pathlib import Path
import urllib.request,urllib.error,hashlib,json,datetime,subprocess,base64
OUT=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616/reviews/exact_priority_falsifier_01')
url='https://web.archive.org/web/20261002014549id_/https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf'
rec={'url':url,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 try:r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)
 except urllib.error.HTTPError as e:r=e
 data=r.read();rec.update({'status':r.code,'final_url':r.url,'headers':dict(r.headers),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'sha1_base32':base64.b32encode(hashlib.sha1(data).digest()).decode().strip('=')})
 p=OUT/'private/archive_20261002.body';p.write_bytes(data)
 if data.startswith(b'%PDF'):
  subprocess.run(['pdftotext','-f','60','-l','60','-layout',str(p),str(OUT/'private/archive_p60.txt')],check=True)
  subprocess.run(['pdftoppm','-f','60','-l','60','-scale-to','2000','-png','-singlefile',str(p),str(OUT/'private/archive_p60')],check=True)
  subprocess.run(['pdfinfo',str(p)],stdout=(OUT/'private/archive_pdfinfo.txt').open('w'),check=True)
except Exception as e:rec['exception']=str(e)
rec['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(OUT/'ARCHIVE_FETCH_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
current=(OUT/'private/primary_current.pdf').read_bytes()
print('current sha1 base32',base64.b32encode(hashlib.sha1(current).digest()).decode().strip('='))
