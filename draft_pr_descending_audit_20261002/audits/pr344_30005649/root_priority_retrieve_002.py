#!/usr/bin/env python3
"""One-shot independent primary-source retrieval for the priority audit."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent
OUT=A/'root_priority_private/primary_retrieval002'
ENV={'PATH':'/opt/homebrew/bin:/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':p.stat().st_mode&0o7777}
if OUT.exists():raise RuntimeError('One-shot capture exists')
OUT.mkdir(parents=True)
program=pin(Path(__file__))
def run(label,argv,inputs):
 before={str(p):pin(p) for p in inputs}
 pre={'utc':now(),'argv':argv,'cwd':str(A),'environment_exact':ENV,'program':program,'inputs_before':before}
 (OUT/(label+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
 child=subprocess.run(argv,cwd=A,env=ENV,capture_output=True)
 (OUT/(label+'.stdout')).write_bytes(child.stdout)
 (OUT/(label+'.stderr')).write_bytes(child.stderr)
 after={str(p):pin(p) for p in inputs}
 receipt=dict(pre,completed_utc=now(),exit_status=child.returncode,stdout=pin(OUT/(label+'.stdout')),stderr=pin(OUT/(label+'.stderr')),inputs_after=after,input_stability=before==after)
 (OUT/(label+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 if child.returncode or before!=after:raise RuntimeError(label+' actual native failure')
 return child.stdout
run('curl_version',['/usr/bin/curl','--version'],[Path('/usr/bin/curl'),Path(__file__)])
sources=[('pries_ulmer_correction_2024','https://nyjm.albany.edu/j/2024/30-45v.pdf'),('pries_ulmer_jacobian_2022','https://par.nsf.gov/servlets/purl/10380173')]
results=[]
for label,url in sources:
 pdf=OUT/(label+'.pdf');headers=OUT/(label+'.headers')
 argv=['/usr/bin/curl','--fail','--location','--silent','--show-error','--max-time','45','--dump-header',str(headers),'--output',str(pdf),url]
 run(label+'_download',argv,[Path('/usr/bin/curl'),Path(__file__)])
 assert pdf.read_bytes().startswith(b'%PDF-')
 output=run(label+'_extract',['/opt/homebrew/bin/pdftotext','-layout',str(pdf),'-'],[pdf,Path('/opt/homebrew/bin/pdftotext').resolve(),Path(__file__)])
 text=OUT/(label+'.txt');text.write_bytes(output)
 results.append({'label':label,'url':url,'pdf':pin(pdf),'response_headers':pin(headers),'whole_native_layout_text':pin(text),'download_receipt':pin(OUT/(label+'_download.json')),'extraction_receipt':pin(OUT/(label+'_extract.json'))})
assert pin(Path(__file__))==program
record={'utc':now(),'status':'TWO_PRIMARY_PRIORITY_SOURCES_ACTUALLY_RETRIEVED_AND_EXTRACTED','sources':results,'all_native_exits_zero':True,'source_read_scope':'Retrieval does not certify reading; operative page and full-text reading scopes will be recorded separately.','interpreter':sys.executable,'version':sys.version,'program':program}
(OUT/'RETRIEVAL_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
