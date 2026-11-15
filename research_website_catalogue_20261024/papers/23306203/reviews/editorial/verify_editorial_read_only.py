#!/usr/bin/env python3
"""Pure custody/text/metadata closure only. No writes, project/science imports,
network, subprocess, renderer, scientific proof execution or fault campaign.
"""
from pathlib import Path
import hashlib
import html
import json
import re
E=Path(__file__).resolve().parent;P=E.parents[3];S=P/'papers/23306203/sources'
checks=0;typed=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def obj(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def names(p):return sorted(str(x.relative_to(p)) for x in p.rglob('*') if x.is_file())
def bound(p,r):need(pin(p)=={'bytes':r['bytes'],'SHA256':r['SHA256']},'whole bytes '+str(p))
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def whole(a,b,label):
 global typed
 need(same(a,b),'whole typed/key/list/null '+label);typed+=1
m=obj(E/'PROTECTED_INPUTS.json');rows={r['path']:r for r in m['files']};need(len(rows)==len(m['files'])==276,'complete distinct originals')
for ns in m['whole_original_namespaces']:
 d=Path(ns['path']);need(names(d)==ns['files'],'strict original file namespace');need(sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_dir())==ns['directories'],'strict original directories')
for r in m['files']:
 p=Path(r['path']);q=E/r['copy'];bound(p,r);bound(q,r);need(p.read_bytes()==q.read_bytes(),'whole original raw copy')
 if p.suffix=='.json' or '.response.body' in p.name:
  try:a=json.loads(p.read_bytes());b=json.loads(q.read_bytes())
  except (UnicodeDecodeError,json.JSONDecodeError):continue
  whole(a,b,'raw JSON '+str(p))
need(len(m['core_files'])==18,'17 original core plus sole authorized checkpoint helper')
need(pin(P/'scripts/checkpoint_subtree.py')['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','exact authorized checkpoint SHA')
def frozen(p):return (E/rows[str(p)]['copy']).read_bytes()
def fobj(p):return json.loads(frozen(p))
p=obj(E/'publication.json');promotion=obj(E/'promotion.json');protocol=obj(E/'SOURCE_PROTOCOL_BINDINGS.json');ready=fobj(S/'SOURCE_READY.json');root=fobj(P/'verification/root-clearance-23306203-20261115.json');record=fobj(S/'record.response.body')
whole(p['source_binding']['whole_original_source_ready'],ready,'whole native READY')
whole(root['whole_original_SOURCE_READY_unchanged'],ready,'whole root READY wrapper')
whole(p['source_binding']['whole_native_record'],record,'entire record')
whole(p['source_binding']['whole_original_support_metadata'],fobj(S/'published-source/asset-001/metadata.json'),'entire original support metadata')
whole(p['review_metadata']['whole_root_scientific_authority'],root,'whole root authority')
whole(p['review_metadata']['whole_original_scientific_verdicts'],{'scope':root['whole_scope_literal_verdict'],'adversarial':root['whole_adversarial_literal_verdict']},'complete heterogeneous peer verdicts')
whole(promotion['whole_root_scientific_authority'],root,'promotion whole root')
whole(promotion['whole_source_binding'],p['source_binding'],'promotion source whole')
whole(promotion['whole_original_scientific_verdicts'],p['review_metadata']['whole_original_scientific_verdicts'],'promotion peer whole')
def wrappers(v):
 if isinstance(v,dict):
  if all(k in v for k in ['original','copy','whole_literal_object']):
   bound(E/v['copy'],v);whole(v['whole_literal_object'],fobj(Path(v['original']['path'])),'entire existing literal wrapper')
  for b in v.values():wrappers(b)
 elif isinstance(v,list):
  for b in v:wrappers(b)
wrappers(protocol)
whole([x['whole_original_binding'] for x in protocol['native_API_objects_in_original_order']],ready['whole_native_API_objects'],'actual record/latest/versions/files role binding order')
whole(p['native_assets_in_original_order'],ready['all_native_assets_in_original_order'],'complete native assets original order')
need([x['original_api_file_object']['key'] for x in p['native_assets_in_original_order']]==['focal_product_support.zip','focal_product_period_criterion.pdf'],'native ZIP then PDF')
tex=frozen(Path(ready['controlling_TeX']['extracted_path'])).decode();fragment=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)[1]
need((E/'ORIGINAL_PRINTED_ABSTRACT.tex').read_text()==fragment,'entire original printed TeX abstract')
abstract=' '.join(fragment.split()).replace('\\(2\\)','2').replace('\\(4\\)','4').replace('\\(k_{114}\\)','k₁₁₄').replace('Reznik--Garcia--Koiller','Reznik–Garcia–Koiller')
need(p['abstract']==abstract,'whole printed abstract typography-only text')
need(p['native_deposit_description_html']==record['metadata']['description'] and (E/'NATIVE_DEPOSIT_DESCRIPTION.html').read_bytes()==record['metadata']['description'].encode(),'whole distinct original native deposit description')
outputs=['PUBLIC_COPY.md','PUBLIC_MAIN.html','SCHOLARLY_METADATA.json','citation.bib','candidate/index.html','candidate/citation.bib','candidate/focal_product_support.zip','candidate/focal_product_period_criterion.pdf']
need(names(E/'optimized-authoring')==sorted(outputs),'closed exact8 optimized buffers')
for n in outputs:need((E/n).read_bytes()==(E/'optimized-authoring'/n).read_bytes(),'whole actual normal optimized buffer '+n)
need(names(E/'candidate')==['citation.bib','focal_product_period_criterion.pdf','focal_product_support.zip','index.html'],'exact4candidate files')
main=(E/'PUBLIC_MAIN.html').read_text();candidate=(E/'candidate/index.html').read_text();copy=(E/'PUBLIC_COPY.md').read_text()
need(main.endswith('\n') and re.findall(r'<main\b[^>]*>.*?</main>',candidate,re.S)==[main[:-1]],'whole actual main equals candidate')
need('<section id="abstract"><h2>Original printed abstract</h2><p>'+html.escape(abstract)+'</p></section>' in main and abstract in copy,'complete visible printed abstract')
deposit='<details id="native-deposit-description"><summary>Original Zenodo deposit description</summary>'+record['metadata']['description']+'</details>'
need(deposit in main and deposit in copy,'entire separately labelled native description')
for section in obj(E/'public-sections.json'):
 for paragraph in section['paragraphs']:need('<p>'+html.escape(paragraph)+'</p>' in main and paragraph in copy,'complete actual paragraph')
need(not re.search(r'display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0',candidate,re.I),'no hidden content CSS')
need('<iframe class="paper-pdf" src="focal_product_period_criterion.pdf#view=FitH"' in main and 'width="100%" height="900"' in main,'actual original fullPDF iframe')
need('<object' not in main and '<link rel="canonical"' not in candidate,'iframe from outset and no site canonical assignment')
sg=obj(E/'SCHOLARLY_METADATA.json');embedded=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',candidate,re.S)[1]);whole(sg,embedded,'entire actual Scholarly head')
need(sg['abstract']==abstract and sg['abstract']!=p['description'] and sg['abstract']!=p['native_deposit_description_html'],'printed abstract distinct from SEO and deposit description')
need(p['printed_version_field_present'] is False and p['printed_version'] is None,'printed version ABSENT not API version')
need(sg['version']==p['version']==record['metadata']['version']=='1.0.0' and 'Native deposit version 1.0.0' in main and 'printed paper has no version line' in main,'actual native version labelled separately')
need(sg['datePublished']==p['publication_date']=='2026-10-11' and p['printed_date']=='11 October 2026','original declared and printed dates')
need(sg['identifier']==p['doi']=='10.5281/zenodo.23306203' and sg['author']['identifier']==p['orcid']=='https://orcid.org/0009-0001-9320-500X','DOI ORCID identity')
for k,v in {'robots':'noindex,nofollow,noarchive','citation_title':p['title'],'citation_author':'Alec Kriebel','citation_author_orcid':p['orcid'],'citation_publication_date':'2026/10/11','citation_version':'1.0.0','citation_doi':p['doi']}.items():need('<meta name="'+k+'" content="'+html.escape(v,quote=True)+'">' in candidate,'exact private metadata '+k)
need(len(sg['encoding'])==2,'exact2native encodings')
for n,enc in zip(ready['all_native_assets_in_original_order'],sg['encoding']):
 name=n['original_api_file_object']['key'];b=(E/'candidate'/name).read_bytes();need(b==frozen(Path(n['path'])),'entire unchanged native download')
 need(hashlib.md5(b).hexdigest()==n['original_api_file_object']['checksum'].split(':')[1],'native MD5')
 need(enc['encodingFormat']==n['whole_original_native_files_entry']['mimetype'] and enc['contentUrl']==n['original_api_file_object']['links']['self'],'native MIME/order/link')
 need(enc['license']=='https://creativecommons.org/licenses/by/4.0/','actual CC BY both encodings')
rights=obj(E/'RIGHTS_AND_IDENTITY.json');need(rights['whole_original_license_text']==frozen(S/'published-source/asset-001/LICENSE.md').decode(),'whole deposited license')
need(sg['license']=='https://creativecommons.org/licenses/by/4.0/' and p['code_license']=='CC BY 4.0' and rights['MIT_license_inferred'] is False,'actual all authored code CC BY no invented MIT')
need(ready['whole_regular_payload_occurrences']==13 and ready['embedded_PDFs']==[],'whole literal native archive13 noembeddedPDF')
need((E/'citation.bib').read_bytes()==p['prepared_bibtex'].encode(),'complete BibTeX')
for k in ['canonical_url','AA','follow_up','native_sheet_aa_url']:need(p[k] is None,'private null gate '+k)
for k in ['production_installation_authorized','ready_to_publish','rendered_public_copy_approved','installed','deployed','live_verified','browser_verified','native_sheet_publication_verified','all203_complete_claimed']:need(promotion[k] is False,'private false gate '+k)
for stem,flag in [('AUTHOR_NORMAL',0),('AUTHOR_OPTIMIZED',1)]:
 r=obj(E/(stem+'.stdout.json'));need(r['optimization_level']==flag and r['actual_buffers_written']==8 and r['native_files']==2,'actual author mode');need((E/(stem+'.stderr')).read_bytes()==b'','actual empty stderr')
initial=obj(E/'INITIAL_EXPECTATIONS_SEAL.json')
for n,r in initial['payloads'].items():bound(E/n,r)
if (E/'AUTHORING_RECEIPT.json').exists():
 for r in obj(E/'AUTHORING_RECEIPT.json')['actual_tool_results']:
  need(r['actual_process_exit_code']==0,'process exit separate from optimization flag');bound(E/r['stdout']['path'],r['stdout']);bound(E/r['stderr']['path'],r['stderr'])
if (E/'SEAL.json').exists():
 seal=obj(E/'SEAL.json');bound(E/'MANIFEST.json',seal['manifest']);owned=obj(E/'MANIFEST.json');need(names(E)==sorted(list(owned['payloads'])+['MANIFEST.json','SEAL.json']),'strict whole owner namespace no nested terminal exclusion')
 need(not any(x.is_symlink() for x in E.rglob('*')),'no owned symlinks');need(sorted(str(x.relative_to(E)) for x in E.rglob('*') if x.is_dir())==owned['directories'],'strict owned directories')
 for n,r in owned['payloads'].items():bound(E/n,r)
print(json.dumps({'status':'PASS_PRIVATE_FOCAL_PERIOD_EDITORIAL_CUSTODY','checks':checks,'whole_typed_objects':typed,'protected_originals':276,'source_files':66,'scientific_owner_namespaces':[65,96,29],'qualified_core_inputs':18,'core_qualification':'17 original plus separately authorized405b checkpoint helper','actual_buffers_each_author_mode':8,'whole_actual_normal_optimized_buffer_identity':True,'whole_original_native_files':2,'whole_original_ZIP_payloads_from_sealed_native_custody':13,'science_project_imports_network_subprocess_or_writes':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None},indent=2))
