"""Read-only bounded static validation. Prints JSON; no fetch, render or writes."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,io,json,re,stat,zipfile,zlib
from pypdf import PdfReader
E=Path(__file__).resolve().parent;B=E.parents[1];P=B.parents[1];S=B/'sources';checks=[]
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(n,c,d=None):checks.append({'check':n,'passed':bool(c),'detail':d})
def unchanged(rows,base=None):
    failed=[]
    for r in rows:
        p=Path(r['path']);p=p if p.is_absolute() else base/p
        if not p.is_file() or p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:failed.append(str(p))
    return failed
pub,pro=load(B/'publication.json'),load(B/'promotion.json');sb=pub['source_binding']
ready,meta,raw,trans,inv=[load(S/n) for n in ['SOURCE_READY.json','normalized-metadata.json','record.raw.json','api-receipts.json','archive-members.json']]
rootpath=P/'verification/root-clearance-23217863-20261025.json';root=load(rootpath)
baseline=load(E/'ORIGINAL_BINDINGS_BEFORE.json')
check('all273_bounded_baseline_files_unchanged',baseline['file_count']==len(baseline['files'])==273 and not unchanged(baseline['files']))
check('root_authority_exact',sha(rootpath)=='b8f379a432a6866d611b929b8c91a410312a36943b99051574edc135598b280a'==pro['root_clearance_sha256']==pub['review_metadata']['root_clearance_sha256'] and pro['root_clearance_record']==root)
check('qualified_root_status_not_collapsed',pro['status']==pub['review_metadata']['root_scientific_status']==root['status']=='PASS_AT_DECLARED_EXTERNAL_THEOREM_LEVEL')
check('source_READY_whole_native_object',ready==sb['source_receipt_original']==pro['source_receipt_original'] and sha(S/'SOURCE_READY.json')==sb['source_receipt_sha256']==pro['source_receipt_sha256'])
check('metadata_and_raw_whole_objects',sb['metadata_original']==meta and sb['raw_record_original']==raw and sha(S/'normalized-metadata.json')==sb['metadata_sha256'])
check('whole_ordered_assets_and_API_objects',ready['all_assets']==meta['all_assets']==sb['all_assets']==pro['all_assets'] and raw['files']==sb['published_file_objects']==pro['published_file_objects']==[r['original_api_file_object'] for r in ready['all_assets']])
check('actual_PDF_then_ZIP_order',[r['key'] for r in raw['files']]==['paper.pdf','source-and-verification.zip']==sb['actual_asset_order'])
check('genuine_five_entry_native_transport',trans==sb['transport_receipt_original']==pro['transport_receipt_original'] and len(trans)==sb['transport_receipt_entry_count']==5 and all(set(r)=={'requested_url','started_utc','completed_utc','status','final_url','headers','path','bytes','sha256'} and r['status']==200 and isinstance(r['headers'],dict) for r in trans))
check('transport_bodies_hash_match',not unchanged(trans))
check('version_absence_preserved','version' not in raw['metadata'] and ready['version'] is None and ready['version_field_present'] is False and meta['version_value'] is None and meta['version_field_present'] is False and pub['version'] is None and pub['version_field_present'] is False and pro['version'] is None and sb['zenodo_version'] is None and sb['manuscript_version'] is None)
check('no_invented_source_aliases',not any((S/n).exists() for n in ['receipt.json','record.json','SOURCE_MANIFEST.json','SOURCE_SEAL.json']))
ready_m=load(S/'SOURCE_READY_MANIFEST.json');ready_s=load(S/'SOURCE_READY_SEAL.json');final_m=load(S/'SOURCE_FINAL_MANIFEST.json');final_s=load(S/'SOURCE_FINAL_SEAL.json')
ready_rows=[dict(v,path=k) for k,v in ready_m['files'].items()] if isinstance(ready_m['files'],dict) else ready_m['files']
final_rows=[dict(v,path=k) for k,v in final_m['files'].items()]
check('native_ready50_and_final52_binding_shapes',len(ready_rows)==50 and len(final_rows)==52 and isinstance(final_m['files'],dict) and not unchanged(ready_rows,S) and not unchanged(final_rows,S))
check('actual_SOURCE_FINAL_nested_seal',final_s==sb['source_final_seal_original']==pro['source_final_seal_original'] and final_m==sb['source_final_manifest_original']==pro['source_final_manifest_original'] and final_s['manifest']=={'path':'SOURCE_FINAL_MANIFEST.json','bytes':(S/'SOURCE_FINAL_MANIFEST.json').stat().st_size,'sha256':sha(S/'SOURCE_FINAL_MANIFEST.json')} and ready_s['manifest_sha256']==sha(S/'SOURCE_READY_MANIFEST.json'))
check('all54_complete_source_files',len([p for p in S.rglob('*') if p.is_file()])==54)
check('complete_native_archive_inventory',inv==sb['recursive_archive_inventory_original']==pro['recursive_archive_inventory_original'] and inv['regular_member_occurrences']==41 and inv['container_count']==1 and inv['nested_archive_count']==0)
member_results=[];embedded=[]
with zipfile.ZipFile(S/'source-and-verification.zip') as z:
    infos=[i for i in z.infolist() if not i.is_dir()]
    expected={r['member']:r for r in inv['members']};seen=set()
    for i in infos:
        path=PurePosixPath(i.filename);safe=not path.is_absolute() and '..' not in path.parts and '\\' not in i.filename and i.filename not in seen and not stat.S_ISLNK(i.external_attr>>16)
        seen.add(i.filename);blob=z.read(i);r=expected[i.filename];p=S/'published-source'/i.filename
        good=safe and len(blob)==i.file_size==r['bytes'] and zlib.crc32(blob)&0xffffffff==i.CRC and f'{i.CRC:08x}'==r['CRC32'] and hashlib.sha256(blob).hexdigest()==r['sha256']==sha(p)
        member_results.append(good)
        if blob.startswith(b'%PDF-'):embedded.append({'member':i.filename,'sha256':hashlib.sha256(blob).hexdigest(),'pages':len(PdfReader(io.BytesIO(blob)).pages)})
check('all41_ZIP_members_CRC_hash_existing_bytes',len(member_results)==len(expected)==41 and all(member_results),{'expanded_bytes':sum(r['bytes'] for r in inv['members'])})
check('one_distinct28page_upstream_support_PDF',len(embedded)==1 and embedded[0]['pages']==28 and embedded[0]['sha256']=='56ec913df9fbe4a2daf371eec1cb06ddc5b544cf9defc838aab540f33171f753'!=sb['pdf_sha256'])
check('whole_original7page_target_reader',len(PdfReader(S/'paper.pdf').pages)==pub['pdf_pages']==7 and sha(S/'paper.pdf')==sb['pdf_sha256']==pro['pdf_sha256']=='64ef84935aa6b3d327e30d26719927ce603aa75116a6aefa70589342bafe1c0b')
check('complete_original_support_hash',sha(S/'source-and-verification.zip')==sb['supplement_sha256']==pro['supplement_sha256']=='c237465073726cf0da83abfa3e0251f15a30541dac693f35885694df632c7bb0')
for a in ready['all_assets']:
    p=Path(a['path']);check('asset_'+a['original_api_file_object']['key'],p.stat().st_size==a['bytes']==a['original_api_file_object']['size'] and sha(p)==a['sha256'] and hashlib.md5(p.read_bytes()).hexdigest()==a['md5']==a['original_api_file_object']['checksum'].removeprefix('md5:'))
cp=load(E/'ORIGINAL_OBJECT_COPIES.json');check('all17_exact_custody_copies',len(cp['copies'])==cp['count']==17 and all(Path(r['source']['path']).read_bytes()==Path(r['copy']['path']).read_bytes() for r in cp['copies']))
for family,entry in root['reviews'].items():
    v=load(P/entry['verdict']);rv=pro['reviews'][family]
    check('literal_'+family+'_verdict_and_root_authority',rv['verdict']==v==entry['whole_original_custom_verdict'] and rv['root_authority_entry']==entry and rv['report_sha256']==sha(P/entry['report']) and rv['verdict_sha256']==sha(P/entry['verdict']))
tex=(S/'published-source/manuscript/main.tex').read_text();at=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
normalized=' '.join(at.replace('Banach--Mazur','Banach–Mazur').replace('$*$','*').replace('~',' ').split())
prose,sections=load(E/'public-prose.json'),load(E/'public-sections.json');public=(E/'PUBLIC_COPY.md').read_text()
check('full_original_abstract_exact_typographic_conversion',(E/'ORIGINAL_ABSTRACT.tex').read_text()==at==sb['abstract_tex'] and pub['abstract']==prose['abstract']==normalized and sections['abstract']==[normalized] and normalized in public and pub['abstract_is_original'] is True)
check('all_public_paragraphs_and_background_retained',all(pub[k]==prose[k]==sections[k] and all(x in public for x in pub[k]) for k in ['plain_language','result','why_it_works','limitations']) and pub['background']==sections['background']==prose['background'] and all(r['title'] in public and r['note'] in public and r['url'] in public for r in pub['background']))
check('precise_quantifiers_and_prior_credit','For every complex von Neumann algebra M, there exists ε_M>0 such that, for every complex von Neumann algebra N' in public and 'd_BM(M_*,N_*)<1+ε_M' in public and 'Roydor had already announced the unrestricted conditional formulation' in public and 'essential input is OpenAI' in public)
check('prepared_BibTeX_exact_no_invented_version',pub['prepared_bibtex']==(E/'CITATION.bib').read_text() and not re.search(r'^\s*version\s*=',pub['prepared_bibtex'],re.M) and '10.5281/zenodo.23217863' in pub['prepared_bibtex'] and sha(E/'CITATION.bib')==sb['prepared_bibtex_sha256'])
check('declared_date_and_author_metadata',pub['publication_date']==ready['publication_date']==raw['metadata']['publication_date']=='2026-10-07' and pub['author']=='Alec Kriebel' and pub['orcid'].endswith('0009-0001-9320-500X'))
check('SEO_description_and_title',50<=len(pub['description'])<=170 and pub['title']==raw['metadata']['title'] and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',pub['slug']))
check('separate_CC_BY_and_Apache_notices','CC BY 4.0' in pub['license'] and 'Apache License 2.0' in pub['license_note'] and 'OpenAI' in pub['license_note'] and 'MIT' not in pub['license_note'] and 'Apache License' in (S/'published-source/sources/upstream/LICENSE').read_text())
check('concise_disclosure_and_passive_actual_contributions',pub['ai_disclosure']==prose['ai_disclosure'] and len(pub['ai_disclosure'].split())<70 and 'not human peer review' in pub['ai_disclosure'] and 'substantive research contributions' in pub['collaboration'] and 'mutual agreement' in pub['collaboration'])
gates=['rendered','deployed','rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received']
check('all_later_gates_false',all(pub['review_metadata'][k] is False and pro[k] is False for k in gates))
check('canonical_AA_followup_all_null',all(pub[k] is None and pro[k] is None for k in ['canonical_url','AA','follow_up']) and pub['review_metadata']['native_sheet_aa_url'] is None and pro['native_sheet_aa_url'] is None)
check('publication_config_hash_link',pro['publication_sha256']==sha(B/'publication.json'))
requirements=load(E/'METADATA_READER_SUPPORT_REQUIREMENTS.json')
check('complete_reader_support_citation_future_contract',requirements['future_article_files']==['index.html','paper.pdf','source-and-verification.zip','citation.bib'] and requirements['full_local_iframe_and_open_and_explicit_download_required'] is True and requirements['complete_local_ZIP_link_required'] is True and requirements['target_reader_pages']==7 and requirements['original_Zenodo_reader_url']==raw['files'][0]['links']['self'] and requirements['original_Zenodo_support_url']==raw['files'][1]['links']['self'])
check('no_rendered_page_or_new_source_alias',(E/'index.html').exists() is False and (S/'receipt.json').exists() is False)
result={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Read-only private static validation; no rendering/HTTP/browser/native/publication evidence.','passed':sum(r['passed'] for r in checks),'total':len(checks),'all_passed':all(r['passed'] for r in checks),'checks':checks}
print(json.dumps(result,indent=2,ensure_ascii=False))
raise SystemExit(0 if result['all_passed'] else 1)
