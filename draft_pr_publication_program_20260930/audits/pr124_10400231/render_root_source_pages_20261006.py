from pathlib import Path
import subprocess,json,hashlib,datetime,os
A=Path(__file__).resolve().parent
S=A/'root_primary_sources_20261006';D=S/'private_sources';events=[]
def sha(b):return hashlib.sha256(b).hexdigest()
for name,pages in [('ohtsuki_collection',[170]),('alcaraz_v1',[11,12,13]),('massuyeau_preprint',[12,13])]:
 full=(D/(name+'.txt')).read_text().split('\f')
 for page in pages:
  path=D/(name+'_page_'+str(page)+'.txt');path.write_text(full[page-1])
  args=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','135','-png',str(D/(name+'.pdf')),str(D/(name+'_page_'+str(page)))]
  child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
  if child.returncode!=0:raise RuntimeError(err.decode())
  image=D/(name+'_page_'+str(page)+'.png')
  events.append({'source':name,'PDF_page_one_based':page,'render_PID':child.pid,'exit_code':child.returncode,'argv':args,'text_sha256':sha(path.read_bytes()),'image_sha256':sha(image.read_bytes()),'image_bytes':image.stat().st_size})
receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'rendered_pages':events,'rendering_is_not_reading':True}
(S/'ROOT_PAGE_RENDER_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'rendered':len(events),'PID':os.getpid(),'UTC':receipt['UTC']}))

