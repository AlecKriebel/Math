"""Read and retain only the relevant primary-source pages, plus whole-download hashes."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,urllib.request
F=Path(__file__).resolve().parent;D=F/'primary_selected';D.mkdir(exist_ok=False);T=F/'tmp/pdfs';T.mkdir(parents=True,exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':format(p.stat().st_mode&0o7777,'04o')}
pins=json.loads((F/'original/source_provenance.json').read_bytes())['sources'];ledger=[];commands=[]
for name,start,end,visual in [('owr2007',20,23,22),('acta-open-problems2007',15,15,15)]:
 original=next(x for x in pins if x['file']==name+'.pdf');url=original['url'];started=datetime.datetime.now(datetime.timezone.utc).isoformat();request=urllib.request.Request(url,headers={'User-Agent':'Math-source-audit/1.0'})
 with urllib.request.urlopen(request,timeout=45) as response:body=response.read();final_url=response.geturl();content_type=response.headers.get('Content-Type')
 assert body.startswith(b'%PDF') and len(body)==original['bytes'] and sha(body)==original['sha256']
 p=T/(name+'.pdf');p.write_bytes(body);ledger.append({'url':url,'resolved_url':final_url,'content_type':content_type,'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(body),'sha256':sha(body),'matches_original_source_provenance':True,'whole_pdf_persisted':False,'selected_printed_pages':'24-27' if name=='owr2007' else '317','selected_pdf_one_based_pages':list(range(start,end+1)),'rendered_pdf_one_based_page':visual})
 for kind,argv in [('extract',[shutil.which('pdftotext'),'-f',str(start),'-l',str(end),'-layout',str(p),'-']),('render',[shutil.which('pdftoppm'),'-f',str(visual),'-l',str(visual),'-r','110','-singlefile','-png',str(p),str(D/(name+'-decisive-page'))])]:
  assert argv[0];ts=datetime.datetime.now(datetime.timezone.utc).isoformat();child=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate();op=D/(name+'-'+kind+'.stdout.bin');ep=D/(name+'-'+kind+'.stderr.bin');op.write_bytes(out);ep.write_bytes(err);commands.append({'argv':argv,'cwd':os.getcwd(),'pid':child.pid,'actual_execution':True,'completed':True,'exit_code':child.returncode,'started_utc':ts,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':ident(op),'stderr':ident(ep)});assert child.returncode==0
 p.unlink()
(F/'PRIMARY_DOWNLOAD_LEDGER.json').write_text(json.dumps({'schema':'pr52-primary-selected-pages/v1','date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'downloads':ledger,'selected_page_commands':commands,'all_downloads_unchanged_historical_source_versions':True,'journal_full_text_retrieved':False,'institutional_web_metadata_checked_separately':True,'no_outreach':True},indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','primary_downloads':len(ledger),'historical_sha256_matches':True,'whole_pdfs_retained':False,'selected_text_outputs':2,'selected_page_renders':2},sort_keys=True))
