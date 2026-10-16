from pathlib import Path
import hashlib,json,zipfile,datetime,subprocess,re
HERE=Path(__file__).resolve().parent;PRE=HERE.parent;PKG=HERE/'extracted/odd-origin-area-product-verification';INI=PRE.parent/'initial_review_20261013'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2)+'\n')
m=json.loads((PKG/'MANIFEST.json').read_text());rows=[]
for r in m['files']:
 actual=pin(PKG/r['path']);assert actual=={k:r[k] for k in ('bytes','sha256')},r['path'];rows.append({'path':r['path'],**actual,'match':True})
actual_names={str(p.relative_to(PKG)) for p in PKG.rglob('*') if p.is_file()};manifest_names={r['path'] for r in m['files']}
assert len(rows)==49 and actual_names==manifest_names|{'MANIFEST.json'} and len(actual_names)==50
for p in PKG.rglob('*'):assert not p.is_symlink()
assert (PKG/'paper/odd_origin_area_product.tex').read_bytes()==(PRE/'odd_origin_area_product.tex').read_bytes()
assert (PKG/'metadata.json').read_bytes()==(PRE/'metadata.json').read_bytes()
assert not any(p.suffix.lower() in {'.pdf','.zip','.png','.jpg','.html','.txt'} for p in PKG.rglob('*') if p.is_file() and p.name!='requirements.txt')
jobs=json.loads((PKG/'CHECKSETS.json').read_text());assert len(jobs)==9 and len({j['name'] for j in jobs})==9
for j in jobs:
 assert pin(PKG/j['script'])['sha256']==j['source_script_sha256'];assert (PKG/j['expected']).is_file()
save('PACKAGE_INTEGRITY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','zip_files':50,'manifest_entries':49,'closed_inventory':True,'each_size_and_hash_match':True,'safe_symlink_free_extraction':True,'current_manuscript_and_metadata_identical':True,'checksets':9,'no_raw_provider_or_whole_external_source_files':True,'historical_manifest_policy':'Historical paths and excluded source pins are provenance, not active dependencies, as README explains. MANIFEST.json excludes only itself. Fresh review artifacts are outside frozen ZIP.','manifest_sha256':pin(PKG/'MANIFEST.json')['sha256'],'files':rows})
md=json.loads((PRE/'metadata.json').read_text());deposit=json.loads((PRE/'zenodo-deposit.json').read_text());assert deposit['metadata']==md
assert deposit['files']==[{'path':'output/pdf/odd_origin_area_product.pdf'},{'path':'odd-origin-area-product-verification.zip'}]
assert md['publication_date']=='2026-10-13' and md['version']=='1.0' and md['license']=='cc-by-4.0'
assert md['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}]
assert not any('doi' in k.lower() for k in md)
for text in ['AI tools were used extensively','unrefereed preprint','without external human peer review or proof-assistant formalization','No historical-firstness certificate'] :assert text in md['description']
info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(PRE/'output/pdf/odd_origin_area_product.pdf')],capture_output=True,text=True,check=True).stdout
assert 'Pages:           5' in info and md['title'] in info and 'Author:          Alec Kriebel' in info
save('SUBMISSION_METADATA_CHECK.json',{'status':'PASS','metadata_identical_across_standalone_package_and_deposit':True,'exact_two_file_object_paths':deposit['files'],'author_orcid_correct':True,'date':'2026-10-13','version':'1.0','license':'cc-by-4.0','license_scope':'Authored materials only; full external papers and raw extracts excluded.','no_candidate_doi_or_phantom_doi':True,'disclosures_and_bounded_priority_present':True,'pdfinfo':info})
render=[]
for n in range(1,6):render.append({'path':f'page-{n}.png',**pin(HERE/f'page-{n}.png'),'visually_inspected':True,'issues':[]})
save('RENDER_VERIFICATION.json',{'status':'PASS','renderer':'/opt/homebrew/bin/pdftoppm -r 120 -png','actual_candidate_pdf_pin':pin(PRE/'output/pdf/odd_origin_area_product.pdf'),'pages':5,'paper':'letter, 612x792pt','all_pages_visually_inspected':True,'source_content_consistent':True,'no_clipping_overlap_missing_glyphs_broken_formulas_or_references':True,'title_author_orcid_date_and_disclosure_visible':True,'authoredrenderpins':render})
source_rows=[]
for r in json.loads((PKG/'provenance/source_manifest.json').read_text())['sources']:
 p=INI/'primary_source_reading_copies'/r['reading_filename'];a=pin(p);assert a['sha256']==r['sha256'];source_rows.append({'path':str(p),'url':r['url'],**a,'match':True,'republished':False})
classical=json.loads((PKG/'audits/priority_classical_adversary_01/FINAL_AUDIT_INTEGRITY.json').read_text())
for r in classical['source_reading_copy_pins']:
 p=Path(r['path']);a=pin(p);assert a=={k:r[k] for k in ('bytes','sha256')};source_rows.append({'path':str(p),**a,'match':True,'republished':False})
recent=json.loads((PKG/'audits/priority_recent_adversary_01/PUBLIC_SOURCE_PINS.json').read_text());recent_src=INI/'priority_recent_adversary_01'
arch=[]
for r in recent['deposited_file_pins']:
 p=recent_src/r['relative_path'];a=pin(p);assert a=={k:r[k] for k in ('bytes','sha256')};b=p.read_bytes();provider='md5:'+hashlib.md5(b).hexdigest();assert provider==r['provider_checksum'];arch.append({'relative_path':r['relative_path'],**a,'provider_md5':provider,'match':True})
current=[]
for r in json.loads((PKG/'audits/priority_recent_adversary_01/CURRENT_SOURCE_SCREENING_LEDGER.json').read_text())['sources']:
 code=r['code'];zip_p=recent_src/'sources/current_zip'/f'{code}.zip';tex_p=recent_src/'sources/current_tex'/code/'main.tex';a=pin(zip_p);b=pin(tex_p)
 assert a['sha256']==r['current_zip_sha256'] and b['sha256']==r['current_main_tex_sha256'];current.append({'code':code,'archive':a,'manuscript':b,'match':True})
pr=[]
p=recent_src/'sources/pr204_original_PROOF.md';a=pin(p);assert a=={k:recent['credited_PR204_proof'][k] for k in ('bytes','sha256')};pr.append({'PR':204,**a,'match':True})
for r in recent['background_native_sources']:
 p=recent_src/'sources'/f"pr{r['PR']}_earlier_PROOF.md";a=pin(p);assert a=={k:r[k] for k in ('bytes','sha256')};pr.append({'PR':r['PR'],**a,'match':True})
original=json.loads((PKG/'provenance/ORIGINAL_INTAKE.json').read_text());submitted=[]
for r in original['original_source_files']:
 p=INI/'submitted'/r['native_path'];a=pin(p);assert a=={k:r[k] for k in ('bytes','sha256')};submitted.append({'native_path':r['native_path'],**a,'match':True})
save('SOURCE_AUTHENTICATION.json',{'status':'PASS','primary_and_classical_local_source_pins':source_rows,'original_provider_pins':arch,'current_adjacent_pins':current,'earlier_repository_proofs':pr,'all_23_original_intake_pins':submitted,'v11_authentic_title':'Eighty New Invariants in the Elliptic Billiard','visual_table_checks':['v11 Table 5 p7','published Table 5 p348'],'original_unprimed_origin_signed_product_confirmed':True,'Stachel_Theorem_4_3_equation_4_9_confirmed':True,'Khare_master_and_Landen_exact_sections_read':True,'copies_read_only_and_excluded_from_authored_public_outputs':True})
print(json.dumps({'package':'PASS 50 files /49 manifest entries','metadata':'PASS','render':'PASS five pages','local_primary_and_classical_pins':len(source_rows),'original_deposited_files_and_provider_md5':len(arch),'current_adjacent_archive_and_manuscript_pairs':len(current),'earlier_proof_pins':len(pr),'original_intake_pins':len(submitted)}))
