from pathlib import Path
import urllib.request,subprocess,concurrent.futures,json,hashlib,datetime
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary';P=E/'private/pr0344_0396_review/primary_sources';P.mkdir(exist_ok=True)
S={344:('https://ems.press/content/serial-article-files/47479?nt=1',[99,100,101,102]),356:('https://ems.press/content/serial-article-files/46296',[25]),359:('https://ems.press/content/serial-article-files/46250',[15,16]),364:('https://ems.press/content/serial-article-files/46780',[41,42]),367:('https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf',[132,137,138])}
def run(it):
 n,(url,pages)=it
 req=urllib.request.Request(url,headers={'User-Agent':'Independent-research-readonly-audit/1.0'})
 with urllib.request.urlopen(req,timeout=90) as r:data=r.read();status=r.status;final=r.url
 f=P/f'pr{n:04d}_primary.pdf';f.write_bytes(data);assert data.startswith(b'%PDF')
 subprocess.run(['pdftotext','-layout',str(f),str(f.with_suffix('.txt'))],check=True)
 text=f.with_suffix('.txt').read_text();pgs=text.split('\f')
 chosen={str(i):pgs[i] for i in pages};(P/f'pr{n:04d}_statement_pages.txt').write_text('\n'.join('PAGE '+str(int(i)+1)+'\n'+t for i,t in chosen.items()))
 return {'pr':n,'url':url,'final_url':final,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'read_pdf_page_numbers_one_based':[i+1 for i in pages]}
rs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for it in pool.map(run,S.items()):rs.append(it);print('primary',it['pr'],it['sha256'],flush=True)
(O/'primary_source_evidence.json').write_text(json.dumps({'downloaded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rs},indent=2)+'\n')
