#!/usr/bin/env python3
"""Pure offline editorial/custody check; no network/subprocess/source code or
file writes. Optional --semantic-controls checks tiny transcription boundaries,
not a scientific campaign. Default never reruns those controls or native code."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
from copy import deepcopy
import json,re,sys,zipfile,ast
E=Path(__file__).resolve().parent;Q=E.parent.parent;P=Q.parent.parent
checks=0
def need(v,s):
 global checks
 if not v:raise RuntimeError(s)
 checks+=1
def load(p):return json.loads(Path(p).read_text())
def h(p):return sha256(Path(p).read_bytes()).hexdigest()
def typed(v):
 if isinstance(v,dict):return ('dict',tuple((k,typed(x))for k,x in v.items()))
 if isinstance(v,list):return ('list',tuple(typed(x)for x in v))
 return(type(v).__name__,v)
class Page(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.tags=[];self.data=[];self.skip=0;self.feed(s)
 def handle_starttag(self,t,a):
  self.tags.append((t,dict(a)))
  if t in ['head','script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['head','script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.data.append(d)
def original_abstract():
 s=(E/'abstract-source.tex').read_text();s=re.sub(r'\\\((.*?)\\\)',lambda m:m[1].replace('\\Delta','Δ'),s,flags=re.S);return ' '.join(s.replace('~',' ').split())
def content(c):
 need(c['abstract']==original_abstract()and c['abstract_is_original']is True,'entire original abstract')
 r=' '.join(c['result']);w=' '.join(c['why_it_works']);b=' '.join(c['background']);l=' '.join(c['limitations'])
 for phrase in ['positive integers','every assignment of k-element','not restricted to intervals','prescribed common bounded palette','eleven vertices, ten edges','A={1,2,3,4,5}','B={1,3,4,5,6}','parameter of T is 5','λ(T)=4','parameter is 6','For every nonempty finite tree','(Δ(S)+3)-element','every six-element list assignment','every independently chosen six-tuple','nonnegative finite integers','Zero lengths are allowed','unbounded diameter']:
  need(phrase in r or phrase in r.replace('For every','for every'),'full original model/theorem phrase '+phrase)
 for phrase in ['breadth-first order','at most three integers','at most Δ−1','At most Δ+2','(1,5,3,1,5,3,4,2,4,2,3)','parent forbids at most three','grandparent at most one','new vertices on different','written proofs carry']:
  need(phrase.lower()in w.lower(),'proof/witness/family phrase '+phrase)
 for phrase in ['Kohl','Conjecture 4','Conjecture 4.4','Voigt','Fiala','2001','cyclic graph','complete 2005 journal mathematical body was not obtained']:
  need(phrase in b,'actual prior-credit/access phrase '+phrase)
 for phrase in ['No minimum vertex order','historical firstness','present worldwide open status','independent discovery','repository deposit-date metadata was not independently authenticated']:
  need(phrase in l,'scope/priority limit '+phrase)
 need(c['version']==c['printed_version']=='1.0'and c['publication_date']=='2026-10-17','actual printed/API edition and declared date')
 need(c['license']=='CC BY 4.0'and c['authored_package_license']=='CC BY 4.0'and c['code_license']is None,'actual broad authored grant/no distinct code instrument')
 need(c['follow_up']is c['canonical_url']is c['AA']is c['native_sheet_aa_url']is None,'all null native/public/followup gates')
 need('extensively'in c['ai_disclosure']and 'not human peer review'in c['ai_disclosure']and 'no formal proof-assistant certification'in c['ai_disclosure'],'AI/unrefereed/nonhuman/nonformal disclosure')

def semantic_controls(c):
 # Finite original-data transcription only; no exhaustive labeling search.
 vs=['a','b','c','d','e','a1','a2','b1','d1','e1','e2'];edges=[('a','b'),('b','c'),('c','d'),('d','e'),('a','a1'),('a','a2'),('b','b1'),('d','d1'),('e','e1'),('e','e2')];adj={v:set()for v in vs}
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 dist={}
 for s in vs:
  ds={s:0};queue=[s]
  for u in queue:
   for v in adj[u]:
    if v not in ds:ds[v]=ds[u]+1;queue.append(v)
  dist[s]=ds
 need(len(vs)==11 and len(edges)==10 and max(map(len,adj.values()))==3 and all(len(ds)==11 for ds in dist.values()),'exact finite tree transcription')
 need(max(max(ds.values())for ds in dist.values())==6 and min(max(ds.values())for ds in dist.values())==3,'exact radius/diameter transcription')
 witness=dict(zip(vs,[1,5,3,1,5,3,4,2,4,2,3]));need(all(abs(witness[u]-witness[v])>=2 for u,v in edges),'displayed ordinary witness edges');need(all(witness[u]!=witness[v]for u in vs for v in vs if dist[u][v]==2),'displayed ordinary witness distance-two pairs')
 need(all(sum(abs(x-y)>=2 for y in range(1,5))<=2 for x in range(1,5)),'ordinary [4] degree-three bound')
 B={1,3,4,5,6};remaining={a:{x for x in B if abs(x-a)>=2 and x!=1}for a in [4,5]};need(remaining=={4:{6},5:{3}}and dist['a1']['a2']==2,'two forced-leaf choices from original lists')
 mutations=[lambda x:x.update(abstract=x['abstract'][:-30]),lambda x:x['result'].__setitem__(0,x['result'][0].replace('not restricted to intervals','restricted to intervals')),lambda x:x['result'].__setitem__(3,x['result'][3].replace('λ(T)=4','λ(T)=5')),lambda x:x['result'].__setitem__(3,x['result'][3].replace('parameter is 6','parameter is 5')),lambda x:x['result'].__setitem__(5,x['result'][5].replace('nonnegative finite integers','positive finite integers')),lambda x:x['result'].__setitem__(5,x['result'][5].replace('independently chosen six-tuple','equal-length extension')),lambda x:x['background'].__setitem__(1,x['background'][1].replace('Voigt','a new bound')),lambda x:x.update(code_license='MIT'),lambda x:x.update(canonical_url=x['proposed_canonical_url']),lambda x:x.update(follow_up='new generic problem')]
 rejected=0
 for f in mutations:
  bad=deepcopy(c);f(bad)
  try:content(bad)
  except RuntimeError:rejected+=1
 need(rejected==len(mutations),'all ten memory-only editorial semantic losses rejected')
 return {'fixed_eleven_vertex_witness_and_forcing_checked':True,'exhaustive_search_or_native_programs_run':False,'memory_only_editorial_fault_shapes_rejected':rejected}

pub=load(Q/'publication.json');prom=load(Q/'promotion.json');ready=load(Q/'sources/SOURCE_READY.json');bind=load(E/'metadata-support/SOURCE_PROTOCOL_BINDINGS.json');auth=load(P/'verification/root-clearance-23440389-20261115.json')
need(h(P/'verification/root-clearance-23440389-20261115.json')=='7f8b7b17b240e6c2ac4c1366072da760c17bc4a32331dc0fd7256335cd6d713e','root authority SHA256');need(h(Q/'sources/SOURCE_READY.json')=='8316224d19c14731bfe4a66946ea1fbe612965bcef284479ebfd9163846147a8','complete SOURCE_READY SHA256')
for row in load(E/'PROTECTED_INPUTS.json')['files']:
 p=Path(row['absolute_path']);need(p.stat().st_size==row['bytes']and h(p)==row['sha256'],'228 preexisting protected bytes '+str(p))
def bound(x):
 p=Path(x['path']);need(p.stat().st_size==x['bytes']and h(p)==x['SHA256'],'actual whole-object bytes '+str(p));need(typed(load(p))==typed(x['whole_literal_object']),'whole typed/order object '+str(p))
for key in ['source_ready','root_authority','transport_aggregate','archive_custody','native_schema_types','printed_identity']:bound(bind[key])
for key in ['source_terminal_objects','native_API_objects','transport_objects','scientific_custom_verdicts','scientific_review_seals']:
 for x in bind[key]:bound(x)
need(len(bind['native_API_objects'])==4 and len(bind['transport_objects'])==7 and len(bind['scientific_custom_verdicts'])==2,'actual4 API/7 transport/2 science interfaces')
for x in bind['raw_byte_copies']:need(Path(x['original_path']).read_bytes()==(E/'metadata-support'/x['copy_path']).read_bytes(),'whole raw byte copy')
for owner in [pub['source_binding'],prom]:
 need(typed(owner['whole_original_source_ready'])==typed(ready),'complete original source schema/old flags')
 for ownkey,key in [('whole_original_native_API_objects','native_API_objects'),('whole_original_seven_transport_objects','transport_objects'),('whole_original_transport_aggregate','transport_aggregate')]:need(typed(owner[ownkey])==typed(bind[key]),'whole heterogeneous object preservation '+key)
need(typed(pub['review_metadata']['whole_root_scientific_clearance_record'])==typed(auth)and typed(prom['whole_root_scientific_clearance_record'])==typed(auth),'whole exact root record')
for owner in [pub['review_metadata'],prom]:need(typed(owner['whole_original_custom_scientific_verdicts'])==typed(bind['scientific_custom_verdicts']),'whole literal two custom scientific verdicts')
need(pub['source_binding']['source_protocol_binding_sha256']==h(E/'metadata-support/SOURCE_PROTOCOL_BINDINGS.json'),'final source binding pin');need(prom['publication_sha256']==h(Q/'publication.json'),'publication config pin')
for k in ['source_repair','narrowed_replacement','human_peer_review','formal_certification','rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified','force_into_118_119_batch','all203_complete_claimed']:need(prom[k]is False,'false review/public/batch gate '+k)
for k in ['follow_up','canonical_url','AA','native_sheet_aa_url','private_batch_assignment']:need(prom[k]is None,'null native/followup/batch gate '+k)
content(pub);sections=load(E/'public-sections.json');copy=(E/'PUBLIC_COPY.md').read_text();page=Page((E/'candidate/index.html').read_text());visible=''.join(page.data)
for k,paras in sections['sections'].items():
 for p in paras:need(p in copy and p in visible,'full exact visible public paragraph '+k)
for p in [pub['abstract'],pub['edition_note'],pub['reader_intro'],pub['rights_notice']]:need(p in copy and p in visible,'full visible abstract/reader/identity/rights')
need(any(t=='meta'and a.get('name')=='robots'and a.get('content')=='noindex,nofollow'for t,a in page.tags),'private noindex/nofollow');need(not any(t=='link'and a.get('rel')=='canonical'for t,a in page.tags),'no assigned candidate canonical')
frames=[a for t,a in page.tags if t=='iframe'];need(len(frames)==1 and frames[0]['src'].split('#')[0]=='assets/'+pub['pdf_filename']and 'three-page'in frames[0]['title'],'full titled original PDF iframe')
links=[a for t,a in page.tags if t=='a'];need(any(a.get('href')=='assets/'+pub['pdf_filename']and 'download'in a for a in links),'explicit complete PDF download');need(any(a.get('href')=='assets/'+pub['supplement_filename']and 'download'in a for a in links),'explicit complete ZIP download')
for asset in ready['all_native_assets_in_original_order']:
 p=E/'candidate/assets'/asset['original_api_file_object']['key'];need(p.read_bytes()==Path(asset['path']).read_bytes(),'whole unchanged native asset')
need((E/'candidate/assets/citation.bib').read_bytes()==(E/'citation.bib').read_bytes()and(E/'citation.bib').read_text()==pub['prepared_bibtex'],'exact accurate citation copies');need('day = {17}'in pub['prepared_bibtex']and 'version = {1.0}'in pub['prepared_bibtex']and pub['doi']in pub['prepared_bibtex'],'original citation date/version/DOI')
with zipfile.ZipFile(E/'candidate/assets'/pub['supplement_filename'])as z:need(len(z.infolist())==61 and z.testzip()is None,'complete61-payload original ZIP CRC')
for term in ['2026-11-15','2026-11-14','SOURCE_READY','SEAL.json','root-clearance','641 checks','228 preexisting','SHA256','sha256']:need(term not in copy and term not in visible,'no public internal-audit leak '+term)
ast.parse((E/'PREPARE_EDITORIAL.py').read_text());need(True,'one-shot drafting source syntax')
semantic=semantic_controls(pub)if'--semantic-controls'in sys.argv else None
sealed=(E/'SEAL.json').exists()
if sealed:
 seal=load(E/'SEAL.json');need(h(E/'MANIFEST.json')==seal['manifest_sha256'],'owned manifest seal');m=load(E/'MANIFEST.json')
 for row in m['files']:
  p=Path(row['absolute_path']);need(p.stat().st_size==row['bytes']and h(p)==row['sha256'],'owned private editorial bytes '+str(p))
 need({str(p)for p in E.rglob('*')if p.is_file()}|{str(Q/'publication.json'),str(Q/'promotion.json')}=={x['absolute_path']for x in m['files']}|{str(E/'MANIFEST.json'),str(E/'SEAL.json')},'complete own editorial/config namespace')
else:need('--unsealed'in sys.argv,'final seal required')
print(json.dumps({'literal_status':'PASS_COMPLETE_PRIVATE_122_EDITORIAL_FIDELITY_AND_NATIVE_CUSTODY','checks':checks,'preexisting_inputs_unchanged':228,'whole_scientific_custom_verdicts':2,'whole_native_API_objects':4,'whole_actual_transports':7,'complete_original_ZIP_payloads':61,'optional_small_semantic_controls':semantic,'own_final_seal_checked':sealed,'network_subprocess_source_or_legacy_or_scientific_programs_or_file_writes':False,'publication_or_AA_authority':False},indent=2))
