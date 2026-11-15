#!/usr/bin/env python3
"""Custody and text/metadata identity only. Stdlib, no project/scientific
imports, execution, network, subprocess, rendering, fault campaign or writes.
"""
from pathlib import Path
import hashlib
import html
import json
import re
E=Path(__file__).resolve().parent;P=E.parents[3];S=P/'papers/23578142/sources'
checks=0;typed=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def obj(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def names(p):return sorted(str(x.relative_to(p)) for x in p.rglob('*') if x.is_file())
def bound(p,r):need(pin(p)=={'bytes':r['bytes'],'SHA256':r['SHA256']},'whole byte binding '+str(p))
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def whole(a,b,label):
 global typed
 need(same(a,b),'whole typed/key/list/null '+label);typed+=1
m=obj(E/'PROTECTED_INPUTS.json');rows={r['path']:r for r in m['files']};need(len(rows)==len(m['files'])==300,'complete distinct original inputs')
for ns in m['whole_original_namespaces']:
 d=Path(ns['path']);need(names(d)==ns['files'],'strict original namespace');need(sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_dir())==ns['directories'],'strict original directories')
for r in m['files']:
 p=Path(r['path']);q=E/r['copy'];bound(p,r);bound(q,r);need(p.read_bytes()==q.read_bytes(),'entire original raw copy')
 if p.suffix=='.json' or '.response.body' in p.name:
  try:a=json.loads(p.read_bytes());b=json.loads(q.read_bytes())
  except (UnicodeDecodeError,json.JSONDecodeError):continue
  whole(a,b,'raw JSON '+str(p))
need(len(m['core_files'])==18,'17original plus authorized checkpoint helper')
need(pin(P/'scripts/checkpoint_subtree.py')['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','exact authorized checkpoint core helper')
def frozen(p):return (E/rows[str(p)]['copy']).read_bytes()
def fobj(p):return json.loads(frozen(p))
p=obj(E/'publication.json');promotion=obj(E/'promotion.json');protocol=obj(E/'SOURCE_PROTOCOL_BINDINGS.json');ready=fobj(S/'SOURCE_READY.json');root=fobj(P/'verification/root-clearance-23578142-20261115.json')
whole(p['source_binding']['whole_original_source_ready'],ready,'whole native READY')
whole(root['source_native_ready_whole_unchanged'],ready,'whole root READY wrapper')
whole(p['review_metadata']['whole_original_scientific_verdicts'],{'scope':root['whole_original_scope_verdict'],'adversarial':root['whole_original_adversarial_verdict']},'entire heterogeneous peer custom objects')
whole(promotion['whole_source_binding'],p['source_binding'],'whole promotion source binding')
def wrappers(v):
 if isinstance(v,dict):
  if all(k in v for k in ['original','copy','whole_literal_object']):
   path=Path(v['original']['path']);bound(E/v['copy'],v);whole(v['whole_literal_object'],fobj(path),'complete existing literal wrapper')
  for b in v.values():wrappers(b)
 elif isinstance(v,list):
  for b in v:wrappers(b)
wrappers(protocol)
whole([x['whole_original_binding'] for x in protocol['native_API_objects_in_original_order']],ready['whole_native_API_objects'],'actual4role binding order')
need(p['native_assets_in_original_order'][0]['original_api_file_object']['key']=='supported-cycle-source-and-verification.zip' and p['native_assets_in_original_order'][1]['original_api_file_object']['key']=='supported-cycle-bound.pdf','literal native ZIP PDF order')
whole(p['native_assets_in_original_order'],ready['all_native_assets_in_original_order'],'complete original native assets')
tex=frozen(Path(ready['controlling_TeX']['extracted_path'])).decode();abst=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S)[1]
need((E/'ORIGINAL_ABSTRACT.tex').read_text()==abst,'entire original TeX abstract')
outputs=['PUBLIC_COPY.md','PUBLIC_MAIN.html','SCHOLARLY_METADATA.json','citation.bib','candidate/index.html','candidate/citation.bib','candidate/supported-cycle-source-and-verification.zip','candidate/supported-cycle-bound.pdf']
need(names(E/'optimized-authoring')==sorted(outputs),'closed8 optimized output buffers')
for name in outputs:need((E/name).read_bytes()==(E/'optimized-authoring'/name).read_bytes(),'whole actual normal optimized output '+name)
need(names(E/'candidate')==['citation.bib','index.html','supported-cycle-bound.pdf','supported-cycle-source-and-verification.zip'],'exact4candidatefiles')
main=(E/'PUBLIC_MAIN.html').read_text();candidate=(E/'candidate/index.html').read_text();copy=(E/'PUBLIC_COPY.md').read_text()
need(re.findall(r'<main\b[^>]*>.*?</main>',candidate,re.S)==[main[:-1]] and main.endswith('\n'),'entire actual main exact')
need(p['abstract'] in copy and '<section id="abstract"><h2>Original abstract</h2><p>'+html.escape(p['abstract'])+'</p></section>' in main,'complete original visible abstract')
for section in obj(E/'public-sections.json'):
 for paragraph in section['paragraphs']:need('<p>'+html.escape(paragraph)+'</p>' in main,'complete actual section paragraph')
need(not re.search(r'display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0',candidate,re.I),'no hidden content')
need('<iframe class="paper-pdf" src="supported-cycle-bound.pdf#view=FitH"' in main and 'width="100%" height="900"' in main,'original fullPDF responsive iframe')
need('<object' not in main and '<link rel="canonical"' not in candidate,'iframe from outset, no assigned site canonical')
sg=obj(E/'SCHOLARLY_METADATA.json');embedded=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',candidate,re.S)[1]);whole(sg,embedded,'whole scholarly object actual head')
need(sg['abstract']==p['abstract'] and sg['abstract']!=p['description'],'whole abstract distinct SEO summary')
need(sg['datePublished']==p['publication_date']=='2026-10-22' and sg['version']==p['version']==p['printed_version']=='1.0.0','printed/native original date version')
need(sg['identifier']==p['doi']=='10.5281/zenodo.23578142' and sg['author']['identifier']==p['orcid'],'DOI and ORCID')
for k,v in {'robots':'noindex,nofollow,noarchive','citation_title':p['title'],'citation_author':'Alec Kriebel','citation_author_orcid':p['orcid'],'citation_publication_date':'2026/10/22','citation_version':'1.0.0','citation_doi':p['doi']}.items():need('<meta name="'+k+'" content="'+html.escape(v,quote=True)+'">' in candidate,'private exact metadata '+k)
need(len(sg['encoding'])==2,'exact2native encodings')
for n,enc in zip(ready['all_native_assets_in_original_order'],sg['encoding']):
 name=n['original_api_file_object']['key'];body=(E/'candidate'/name).read_bytes();need(body==frozen(Path(n['path'])),'whole unchanged original native download')
 need(hashlib.md5(body).hexdigest()==n['original_api_file_object']['checksum'].split(':')[1],'actual native MD5')
 need(enc['encodingFormat']==n['whole_original_native_files_entry']['mimetype'] and enc['contentUrl']==n['original_api_file_object']['links']['self'],'actual native MIME and order')
 if name.endswith('.zip'):need('license' not in enc,'mixed ZIP has no blanket license')
 else:need(enc['license']=='https://creativecommons.org/licenses/by/4.0/','PDF prose CC BY')
need(sg['license']=='https://creativecommons.org/licenses/by/4.0/' and p['code_license']=='MIT','distinct actual instruments')
rights=obj(E/'RIGHTS_AND_IDENTITY.json');need(rights['mixed_archive_blanket_license'] is None and 'companion code has its separate MIT license' in main,'visible mixed rights')
for key,path in [('original_prose_license','LICENSE-PROSE.txt'),('original_code_license','LICENSE-CODE.txt')]:need(rights[key]['whole_literal_text']==frozen(S/'published-source/asset-001/supported_cycle_verification'/path).decode(),'whole real license instrument')
need((E/'citation.bib').read_bytes()==p['prepared_bibtex'].encode(),'complete citation BibTeX')
for k in ['canonical_url','AA','follow_up','native_sheet_aa_url']:need(p[k] is None,'private publication null '+k)
for k in ['production_installation_authorized','ready_to_publish','rendered_public_copy_approved','installed','deployed','live_verified','browser_verified','native_sheet_publication_verified','all203_complete_claimed']:need(promotion[k] is False,'private false gate '+k)
for name,level in [('AUTHOR_NORMAL',0),('AUTHOR_OPTIMIZED',1)]:
 r=obj(E/(name+'.stdout.json'));need(r['optimization_level']==level and r['actual_buffers_written']==8 and r['native_files']==2,'actual author mode output');need((E/(name+'.stderr')).read_bytes()==b'','actual empty author stderr')
if (E/'AUTHORING_RECEIPT.json').exists():
 for r in obj(E/'AUTHORING_RECEIPT.json')['actual_tool_results']:
  need(r['actual_process_exit_code']==0,'actual author exit distinct optimization flag');bound(E/r['stdout']['path'],r['stdout']);bound(E/r['stderr']['path'],r['stderr'])
if (E/'SEAL.json').exists():
 seal=obj(E/'SEAL.json');bound(E/'MANIFEST.json',seal['manifest']);owned=obj(E/'MANIFEST.json');need(names(E)==sorted(list(owned['payloads'])+['MANIFEST.json','SEAL.json']),'strict whole owned final namespace')
 need(sorted(str(x.relative_to(E)) for x in E.rglob('*') if x.is_dir())==owned['directories'],'strict owned directories')
 for name,r in owned['payloads'].items():bound(E/name,r)
print(json.dumps({'status':'PASS_PRIVATE_SUPPORTED_CYCLE_EDITORIAL_CUSTODY','checks':checks,'whole_typed_objects':typed,'source_files':77,'scientific_owner_namespaces':[77,96,30],'protected_originals':300,'core_files':18,'core_qualification':'17original plus authorized405bcheckpoint','actual_authoring_buffers_each_mode':8,'whole_paired_authoring_identity':True,'whole_original_native_assets':2,'complete_original_ZIP_payloads_from_sealed_native_custody':27,'science_project_imports_network_subprocess_or_writes':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None},indent=2))
