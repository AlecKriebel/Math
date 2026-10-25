from pathlib import Path
import hashlib,json,datetime
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=P/'verification/browser-display-five-20261025'
SITE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
def load(p):return json.loads(p.read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def info(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
expected=load(O/'expected-links.json');live_path=P/'verification/live-22089373-23444839-23592692-23441906-23431313.json';live=load(live_path)
bindings=[]
def bind(p,expected_hash,kind):
 x=info(p);x.update(expected_sha256=expected_hash,kind=kind,passed=x['sha256']==expected_hash);bindings.append(x);assert x['passed'],str(p);return x
papers=[]
for p in expected['papers']:
 i=p['record_id'];q=P/'papers'/i;e=load(O/i/'evidence.json');assert e['status']=='PASS' and all(e['checks'].values())
 bind(Path(p['local_html']),p['html_sha256'],'approved article HTML')
 bind(q/'publication.json',p['publication_sha256'],'approved publication data')
 bind(q/'promotion.json',p['promotion_sha256'],'scientific promotion record')
 prom=load(q/'promotion.json')
 bind(P/prom['root_clearance_file'],prom['root_clearance_sha256'],'root scientific clearance')
 receipts=prom.get('related_source_receipts') or {'sources/receipt.json':{'sha256':prom['source_receipt_sha256']}}
 for rp,rd in receipts.items():
  rr=q/rp;bind(rr,rd['sha256'],'source receipt');r=load(rr)
  if r.get('record_sha256'):bind(rr.parent/'record.json',r['record_sha256'],'published record metadata')
  for f in r['files']:
   fpath=rr.parent/(f.get('name') or f['filename']);bind(fpath,f['sha256'],'published original asset')
 for family,r in prom['reviews'].items():
  bind(q/r['report'],r['sha256'],family+' report')
  bind(q/r['verdict_file'],r['verdict_sha256'],family+' verdict')
  assert load(q/r['verdict_file'])==r['verdict']
 for d in p['local_downloads']:
  observed=next(a for a in e['downloads'] if a['label']==d['label']);assert observed['sha256']==d['sha256'] and observed['bytes']==d['bytes']
  bind(Path(observed['path']),d['sha256'],'browser-click downloaded archive')
 assert e['desktop']['canonical']==p['canonical'];assert e['mobile']['width']==e['mobile']['scrollWidth']==390
 assert e['desktop']['width']==e['desktop']['scrollWidth']
 assert e['full_pdf_url']==p['pdfs'][0]['url'] and e['full_pdf_observed_pages']==p['pdfs'][0]['pages']
 assert all(a['href']==b['href'] and a['text']==b['text'] and a['download']==b['download'] for a,b in zip(e['desktop']['links'],p['expected_links']))
 assert len(e['desktop']['links'])==len(p['expected_links'])
 for iframe,ex in zip(e['desktop']['iframes'],p['expected_iframe']):assert iframe['src']==p['url']+ex['src'] and iframe['title']==ex['title']
 natural=None
 if i in ('23441906','23431313'):
  natural=load(O/i/'natural-flow.json');assert natural['status']=='PASS' and natural['no_reload'] and natural['first_embed_capture_rendered']
 if i=='22089373':assert e['reader_observed_pages']==7 and e['reader_url']==p['pdfs'][1]['url']
 papers.append({'record_id':i,'url':p['url'],'status':'PASS','display_evidence':info(O/i/'evidence.json'),'natural_flow':info(O/i/'natural-flow.json') if natural else None,'main_pdf_pages_observed':e['full_pdf_observed_pages'],'reader_pdf_pages_observed':e.get('reader_observed_pages'),'desktop_size':[e['desktop']['width'],e['desktop']['height']],'mobile_size':[e['mobile']['width'],e['mobile']['height']],'mobile_overflow':False,'all_dom_links_match':True,'download_hashes':[{'label':d['label'],'bytes':d['bytes'],'sha256':d['sha256']} for d in e['downloads']]})
for c in live['checks']:bind(SITE/c['path'],c['actual_sha256'],'live HTTP verified website file')
assert live['passed'] and len(live['checks'])==25
root_content=P/'verification/root-five-content-clearance-20261025.json'
cleanup=load(O/'browser-cleanup.json');assert not cleanup['remaining_agent_tabs'] and cleanup['viewport_restored']=={'width':2056,'height':1146}
receipt={'schema_version':1,'completed_utc':now,'completion_percent':100,'status':'PASS','reviewer':'batch3_scope','method':'Actual Chrome extension CUA screenshots and browser link interactions; read-only DOM geometry and link checks; local byte hashing of clicked downloads and immutable approved files. No external browser-control libraries.','site_commit':'f918c7f3b09850726466df349df46e673d5b0e95','hosting_version':'057d4fa1e519b021','root_content_clearance':info(root_content),'live_http_receipt':info(live_path),'expected_links':info(O/'expected-links.json'),'papers':papers,'bound_file_checks':bindings,'all_bound_file_checks_passed':all(x['passed'] for x in bindings),'browser_cleanup':info(O/'browser-cleanup.json'),'issues_and_limits':['All five article full-page desktop and 390px images were visually inspected. Six PDF files rendered actual first pages; visible PDF toolbar page counts were 33+7,5,7,5,5. This is a display test, not a new line-by-line mathematical review of all PDF pages.','Initial lazy embedded viewers on brace and Nijenhuis stayed blank through two captures. Their original states are preserved. Fresh ephemeral-tab normal top-to-Read-on-this-page tests displayed actual PDFs on the first post-click capture without reload. The original cause is not established. These tests used the existing browser profile/cache, not a controlled cold-cache profile.','A few Chrome navigation commands detached after completing navigation; tab inventory and fresh state recovered the same temporary tab. No native-app control was used.','The six local ZIP archive download links were actually clicked and downloaded bytes hashed. The remote 94MB JC companion archive was not redundantly downloaded through the browser; its exact visible URL and previously acquired original/receipt were rehashed and bound.','Prior-work links and contact links were inspected as DOM targets; no outreach, form submission or blanket external-link test was performed.','The user Sheet was never claimed or changed. No site/source/CSS/Git/deployment/redirect mutation was made during display review.']}
(O/'evidence.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
(O/'REPORT.md').write_text('All five pages pass the bounded browser display review.\n\n'+ '\n'.join('- '+p['record_id']+': '+p['url']+' — desktop and 390px readable; no horizontal overflow; actual PDF and archive-download checks passed.' for p in papers)+'\n\nThe JC 33-page main paper and 7-page reader both opened and rendered. The other main PDFs showed 5, 7, 5 and 5 pages. All six clicked archive downloads match the approved source SHA-256 and size. Canonical, iframe and research-index targets match the approved manifest.\n\nBrace and Nijenhuis had initial blank lazy embeds; the screenshots remain untouched. Separate fresh-tab normal navigation rendered both without a reload on the first post-click capture. No persistent failure was reproduced; the original cause remains unestablished, and these were not cold-cache tests.\n\n'+str(len(bindings))+' immutable source, publication, review, clearance, live-file and downloaded-file hash checks passed. This display review does not expand the scientific claims or certify all external background links.\n\nAll three ephemeral tabs were closed. The viewport was restored to 2056×1146; the user Sheet was untouched. Browser ownership released.\n\nCompleted '+now+'; 100%. Full provenance and bounds: evidence.json.\n')
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — 100%: Final hash-bound global receipt sealed; '+str(len(bindings))+' file bindings PASS. All5 pages and6PDF files visually rendered;6archive downloads hash matched. All3temporarytabs closed, viewport restored, browser ownership released. Prior screenshots and receipts unchanged.\n')
artifacts=[info(f) for f in sorted(O.rglob('*')) if f.is_file() and f.name not in ['artifact-manifest.json']]
(O/'artifact-manifest.json').write_text(json.dumps({'utc':now,'status':'PASS','files':artifacts,'file_count':len(artifacts),'screenshots':sum(f['path'].endswith('.jpg') for f in artifacts)},indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'file_bindings':len(bindings),'artifact_files':len(artifacts),'screenshots':sum(f['path'].endswith('.jpg') for f in artifacts),'evidence_sha256':sha(O/'evidence.json'),'artifact_manifest_sha256':sha(O/'artifact-manifest.json'),'report_sha256':sha(O/'REPORT.md')},indent=2))
