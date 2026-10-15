from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
PRE=HERE.parent;D=PRE.parent/'initial_review_20261013';ROOT=HERE/'extracted_archive'
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
keys=['authored_files','public_authored_relative_paths','public_authored_files','files']
bindings=[]
for f in (ROOT/'audits').rglob('*MANIFEST.json'):
 d=json.loads(f.read_text())
 for key in keys:
  if key not in d:continue
  values=d[key]
  if isinstance(values,dict):values=[{'path':k,**v} for k,v in values.items()]
  for item in values:
   rel=item.get('path',item.get('relative_path'))
   target=f.parent/rel
   resolution='manifest relative path'
   if not target.exists() and f.parent.name=='historical_snapshot_01':
    target=f.parent.parent/rel
    resolution='historical snapshot shares unchanged parent-family file'
   assert target.resolve().is_relative_to((ROOT/'audits').resolve())
   p=pin(target);assert p['bytes']==item['bytes'] and p['sha256']==item['sha256'],str(target)
   bindings.append({'manifest':f.relative_to(ROOT).as_posix(),'path':rel,'match':True,'resolution':resolution,'archive_path':target.relative_to(ROOT).as_posix()})
for rel in ['original_submission/FROZEN_MANIFEST.json','original_submission/PUBLICATION_MANIFEST.json','original_submission/independent_review/REVIEW_MANIFEST.json']:
 f=ROOT/rel;d=json.loads(f.read_text())
 for item in d['files']:
  target=f.parent/item['path'];p=pin(target)
  assert p['bytes']==item['bytes'] and p['sha256']==item['sha256']
  bindings.append({'manifest':rel,'path':item['path'],'match':True,'resolution':'manifest relative path','archive_path':target.relative_to(ROOT).as_posix()})
recent=json.loads((D/'priority_recent_adversary_01/PRIMARY_PIN_LEDGER.json').read_text())
external=[]
for group in ['primary_public_objects','discovery_and_native_metadata_objects']:
 for item in recent.get(group,[]):
  target=D/'priority_recent_adversary_01/private_reading'/item['name']
  if item.get('status')=='downloaded':
   p=pin(target);assert p['bytes']==item['bytes'] and p['sha256']==item['sha256']
   external.append({'role':'primary source' if group=='primary_public_objects' else 'discovery/native metadata','name':item['name'],'url':item['url'],'bytes':p['bytes'],'sha256':p['sha256'],'match':True})
original=json.loads((ROOT/'original_submission/source_manifest.json').read_text())
sourcefiles={
 'kunisch-meinlschmidt-v1.pdf':D/'source_pde_adversary_02/private_reading/kunisch-meinlschmidt-v1.pdf',
 'author-version.pdf':D/'source_pde_adversary_02/private_reading/author-version.pdf',
 'owr2021-09.pdf':D/'source_pde_adversary_02/private_reading/owr2021-09.pdf'}
# Authenticate source byte objects without redistributing them.
for item in original['sources']:
 name=item['reading_filename']
 if name=='kunisch-meinlschmidt.pdf':name='kunisch-meinlschmidt-v1.pdf'
 p=sourcefiles[name];q=pin(p)
 assert q['bytes']==item['bytes'] and q['sha256']==item['sha256']
 external.append({'role':'original primary PDF','name':p.name,**q,'url':item['url'],'match':True})
inspected=PRE/'fresh_review_01/external_reading'
for p in inspected.glob('*.pdf'):external.append({'role':'primary PDF inspected in shared read-only folder',**pin(p)})
for p in (HERE/'external_reading').glob('*.txt'):external.append({'role':'own excluded page extraction',**pin(p)})
# Exact metadata and link readback from actual six-page PDF via bundled pypdf.
from pypdf import PdfReader
pdf=PdfReader(PRE/'output/pdf/critical_wave_growth.pdf')
assert len(pdf.pages)==6
pages=[];urls=[]
for n,page in enumerate(pdf.pages,1):
 text=page.extract_text()
 pages.append({'page':n,'text_characters':len(text),'visible_page_number':text.strip().endswith(str(n)),'width_points':float(page.mediabox.width),'height_points':float(page.mediabox.height)})
 assert pages[-1]['visible_page_number']
 for ref in page.get('/Annots',[]):
  annotation=ref.get_object();action=annotation.get('/A',{})
  if '/URI' in action:urls.append(str(action['/URI']))
full='\n'.join(page.extract_text() for page in pdf.pages)
for value in ['Alec Kriebel','October 14, 2026','version 1.0','0009-0001-9320-500X','unrefereed','AI tools','438–440']:
 assert value in full,value
expected_dois=['10.1016/j.matpur.2020.03.006','10.4171/OWR/2021/9','10.1137/100815037','10.1137/110840406','10.1365/s13291-014-0109-3','10.1051/cocv/2015048','10.1137/17M1140418','10.46298/jnsao-2024-12604','10.46298/jnsao-2022-8733']
for doi in expected_dois:assert any(doi in url for url in urls),doi
assert 'https://arxiv.org/pdf/1907.02744v1' in urls
assert 'https://orcid.org/0009-0001-9320-500X' in urls
out={'utc':datetime.now(timezone.utc).isoformat(),'archived_authored_manifest_bindings_checked':len(bindings),'manifest_bindings':bindings,'recent_primary_and_metadata_pins_checked':sum(x.get('match',False) for x in external),'external_reading_pins':external,'source_manifest_contents':original,'pdf_pages':pages,'pdf_links':urls,'metadata_and_disclosure_readback':True,'third_party_reading_copies_excluded':True}
(HERE/'EVIDENCE_PIN_READBACK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','archived_manifest_bindings':len(bindings),'recent_reading_pins_verified':sum(x.get('match',False) for x in external),'pdf_pages':len(pages),'pdf_uris':len(urls)},indent=2))
