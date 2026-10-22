from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess
OUT=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616/reviews/exact_priority_falsifier_01')
url='https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:
    data=r.read(); headers=dict(r.headers); final=r.url; status=r.status
assert len(data)==598093 and hashlib.sha256(data).hexdigest()=='eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7'
p=OUT/'private/primary_current.pdf'; p.write_bytes(data)
receipt={'request_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'final_url':final,'status':status,'headers':headers,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(OUT/'FETCH_PRIMARY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
subprocess.run(['pdftotext','-f','60','-l','60','-layout',str(p),str(OUT/'private/primary_p60.txt')],check=True)
subprocess.run(['pdftoppm','-f','60','-l','60','-scale-to','2000','-png','-singlefile',str(p),str(OUT/'private/primary_p60')],check=True)
subprocess.run(['pdfinfo',str(p)],stdout=(OUT/'private/pdfinfo.txt').open('w'),check=True)
print(json.dumps(receipt,indent=2));print((OUT/'private/primary_p60.txt').read_text());print((OUT/'private/pdfinfo.txt').read_text())
