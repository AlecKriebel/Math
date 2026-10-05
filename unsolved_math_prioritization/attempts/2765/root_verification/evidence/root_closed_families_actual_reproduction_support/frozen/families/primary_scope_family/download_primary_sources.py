from pathlib import Path
import subprocess,hashlib,json,datetime
out=Path(__file__).resolve().parent
dest=out/'ignoredtmp/primary_sources'
urls={'leininger_v1.pdf':'https://arxiv.org/pdf/math/0302280v1','jyothis_v3.pdf':'https://arxiv.org/pdf/2309.14532v3','burger_published2021.pdf':'https://people.math.ethz.ch/~burger/pub/2021_Currents_systoles.pdf','trin_published2024.pdf':'https://aif.centre-mersenne.org/item/10.5802/aif.3625.pdf','trin_v2.pdf':'https://arxiv.org/pdf/2208.10763v2','K3_berkeley.pdf':'https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf'}
ledger=[]
for name,url in urls.items():
 c=subprocess.run(['curl','-L','--fail','--max-time','60','-A','Mozilla/5.0','-D',str(dest/(name+'.headers')),'-o',str(dest/name),url],capture_output=True,text=True)
 (dest/(name+'.curl.stdout')).write_text(c.stdout);(dest/(name+'.curl.stderr')).write_text(c.stderr)
 item={'requested_url':url,'file':'ignoredtmp/primary_sources/'+name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'curl_exit':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
 if c.returncode==0:
  b=(dest/name).read_bytes();item.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  r=subprocess.run(['pdftotext','-layout',str(dest/name),str(dest/(name+'.txt'))],capture_output=True,text=True);item.update(pdftotext_exit=r.returncode,stderr_pdftotext=r.stderr)
 ledger.append(item)
 (out/'operative_sources_download_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps(ledger,indent=2))
