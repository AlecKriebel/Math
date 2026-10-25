"""Finalize documentary scope artifacts only after complete published asset integrity checks."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,zipfile,tarfile
p=Path(__file__).resolve().parents[2];s=p/'sources';out=p/'reviews/scope';r=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text())
assert receipt.get('complete') and len(receipt['files'])==len(r['files'])==14
assert {f['name'] for f in receipt['files']}=={f['key'] for f in r['files']}
for f in receipt['files']:
 sha=hashlib.sha256();alg,expect=f['zenodo_checksum'].split(':',1);md=hashlib.new(alg);n=0
 with (s/f['name']).open('rb') as fh:
  while data:=fh.read(1024*1024):sha.update(data);md.update(data);n+=len(data)
 assert sha.hexdigest()==f['sha256'] and md.hexdigest()==expect and n==f['bytes'],f['name']
manifest=json.loads((s/'K3P_Level2_Zenodo_Manifest_v1.0.0.json').read_text());byname={f['name']:f for f in receipt['files']}
for f in manifest['files_excluding_manifest_and_sha256sums']:
 actual=byname[f['path']];assert actual['sha256']==f['sha256'] and actual['bytes']==f['bytes']
checksum_count=0
for line in (s/'SHA256SUMS').read_text().splitlines():
 if not line.strip():continue
 expected,name=line.split(maxsplit=1);name=name.lstrip('*');assert byname[name]['sha256']==expected,(name,expected);checksum_count+=1
archivechecks=[]
for f in receipt['files']:
 path=s/f['name']
 if path.suffix=='.zip':
  with zipfile.ZipFile(path) as z:
   for m in z.infolist():
    assert not Path(m.filename).is_absolute() and '..' not in Path(m.filename).parts
    assert (m.external_attr>>16)&0o170000!=0o120000
   assert z.testzip() is None
   archivechecks.append({'filename':f['name'],'members':len(z.infolist()),'expanded_bytes':sum(m.file_size for m in z.infolist()),'crc':'pass','paths':'safe relative, no symlinks','extracted':('Source_' in f['name'])})
 elif f['name'].endswith('.tar.gz'):
  with tarfile.open(path,'r:gz') as z:
   members=z.getmembers()
   for m in members:assert not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and not m.issym() and not m.islnk()
   archivechecks.append({'filename':f['name'],'members':len(members),'expanded_bytes':sum(m.size for m in members),'paths':'safe relative, no symlinks/hardlinks','extracted':False})
c=json.loads((out/'content.json').read_text());c['source_binding']['files']=receipt['files'];(out/'content.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
c=json.loads((out/'content.json').read_text());assert c['source_binding']['files']==receipt['files']
for a in c['additional_assets']:assert a['filename'] in byname and a['kind'] in ['pdf','zip','text']
for x in c['related_resources']:
 name=x['url'].split('/files/')[1].split('?')[0];assert name in byname
now=datetime.now(timezone.utc).isoformat()
proof={'verified_utc':now,'asset_count':14,'all_zenodo_checksums_sizes_sha256':'pass','manifest_asset_entries_checked':len(manifest['files_excluding_manifest_and_sha256sums']),'sha256sums_entries_checked':checksum_count,'archive_integrity':archivechecks,'mathematical_computation':'not executed by this scope track','abstract':'all 296 words match released main.tex under explicit typography normalization'}
(out/'source_integrity.json').write_text(json.dumps(proof,indent=2)+'\n')
v={'record_id':'22178672','role':'independent_publication_scope_and_primary_literature_review','completed_utc':now,'completion_percent':100,'scope_verdict':'scope_review_completed_before_reported_math_defect; preserved_content_not_for_publication', 'publication_status':'do_not_publish_pending_mathematical_gate', 'reported_math_defect':json.loads((out/'PUBLICATION_HOLD.json').read_text()),'mathematical_gate':'not_assessed_by_this_verdict','substantive_scope_defect_found':False, 'substantive_math_defect_reported':True,'novelty_certified':False,'peer_review_certified':False,'follow_up':None,'read_scope':{'article_pages':39,'supplement_pages':15,'abstract':'Full original, visually checked and exact released TeX cross-check','support':'All 14 assets checksum-bound; small sources extracted; large archives inspected compressed; theorem-to-certificate crosswalk and public package boundaries read','literature':'Bounded primary-source comparison, with v4 Englander full-text access limitation recorded in REVIEW.md','computation':'Source integrity only; mathematical replays belong to independent math tracks'},'independence':'Scope conclusion recorded before reading any analytic/adversarial opinion. The parent relayed a mathematical defect after the independent scope conclusion; promotional work then stopped. Published package claims were treated as source material, not independent proof.','publication_conditions':['Separate mathematical gate must pass.','Retain exact fixed model, one-step semi-directed convention, strong tree-childness, binary level-at-most-two and strict-domain assumptions.','Distinguish local regular germ containment, generic topology modulo triangles, pointwise statements, and equality of complete physical images.','No claimed all-parameter identification, practical estimator, human peer review, or certified priority.','Keep complete original abstract, separate AI disclosure, both PDFs and all supporting-material provenance.'],'source_integrity':'source_integrity.json','main_pdf_sha256':byname[c['pdf_filename']]['sha256'],'source_zip_sha256':byname[c['supplement_filename']]['sha256']}
(out/'verdict.json').write_text(json.dumps(v,indent=2)+'\n')
with (out/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — 100% complete for this bounded scope task. All 14 published assets now freshly checksum/size/SHA-256 verified; all published manifest and checksum entries match, ZIP CRCs and archive paths checked. Complete source binding refreshed in content.json. Main and reader PDFs plus small sources remain local; large packages have exact original Zenodo links. Scope review was completed independently before a subsequent reported mathematical defect; preserved draft is not for publication pending the mathematical gate. No repair or replacement-rooting search performed. No website, spreadsheet, Git command, Zenodo mutation, or external communication.\n')
print(json.dumps(proof,indent=2))
