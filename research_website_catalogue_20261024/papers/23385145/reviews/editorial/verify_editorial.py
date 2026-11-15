#!/usr/bin/env python3
"""Pure offline editorial/custody closure. Reads files only; no network, subprocess,
source programs, renderer, scientific campaign, or file writes. --unsealed permits
the first owned-manifest construction; default requires the final seal."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from html.parser import HTMLParser
from copy import deepcopy
import json, re, sys, zipfile
E=Path(__file__).resolve().parent; Q=E.parent.parent; P=Q.parent.parent
checks=0
def require(ok, label):
 global checks
 if not ok: raise RuntimeError(label)
 checks+=1
def load(p): return json.loads(Path(p).read_text())
def digest(p): return sha256(Path(p).read_bytes()).hexdigest()
def typed(v):
 if isinstance(v,dict): return ('dict',tuple((k,typed(x)) for k,x in v.items()))
 if isinstance(v,list): return ('list',tuple(typed(x) for x in v))
 return (type(v).__name__,v)
def object_binding(x,pathkey='path',objkey='whole_literal_original_object',hashkey='sha256'):
 p=Path(x[pathkey]); require(digest(p)==x[hashkey],'native byte identity '+str(p));require(typed(load(p))==typed(x[objkey]),'whole typed/order object '+str(p))
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.data=[];self.script=False
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)));self.script=(t=='script') or self.script
 def handle_endtag(self,t):
  if t=='script':self.script=False
 def handle_data(self,d):
  if not self.script:self.data.append(d)

def norm_abstract(s):
 s=s.replace("Berg\\'e",'Bergé').replace('$O(n\\log^5(2n))$','O(n log⁵(2n))').replace('~',' ').replace("Ducoffe's",'Ducoffe’s')
 return ' '.join(s.split())
def public_checks(p,s):
 require(p['abstract']==norm_abstract((E/'abstract-source.tex').read_text()),'complete original abstract')
 require(p['abstract_is_original'] is True,'original abstract label')
 text=' '.join(p['result'])
 for term in ['finite, nonempty, connected, simple','unit edge lengths','finite nonnegative real','adjacency lists','promise that G is median','entire set C_w','O(n log⁵(2n)) exact operations','0≤k≤n−1','Zero-weight vertices','n=1 or all weights are zero','O(B+log n)','input reading','O(n log²(2n))']:
  require(term in text,'full theorem/model phrase '+term)
 alltext=' '.join(x for k in ['why_it_works','limitations','background'] for x in p[k])
 for term in ['Bergé','Ducoffe','Habib','Chalopin','stronger O(n log²n)','arXiv:2410.10235v1','no assertion that the inaccessible final SODA','Recognition','arbitrary edge lengths','continuous facilities','unimodality','not a fast general implementation']:
  require(term in alltext,'credit/boundary phrase '+term)
 require(p['result']==s['sections']['result']+s['sections']['comparison_model'],'common result key preserves separately headed bit model')
 for k in ['plain_language','why_it_works','limitations','background','collaboration']:
  require(p[k]==s['sections'][k],'full unique paragraph fidelity '+k)
 require(p['publication_date']=='2026-10-14' and p['version']=='1.0' and p['printed_version'] is None,'date/API-version/no-printed-version')
 require(p['license']=='CC BY 4.0' and p['code_license'] is None,'actual rights/no invented separate code license')
 require(p['follow_up'] is None and p['canonical_url'] is None and p['AA'] is None and p['native_sheet_aa_url'] is None,'null gates')
 require('extensively' in p['ai_disclosure'] and 'not human peer review' in p['ai_disclosure'] and 'not received human peer review or proof-assistant certification' in p['ai_disclosure'],'AI/nonhuman/nonformal status')
 require(p['proposed_canonical_url']=='https://aleckriebel.com/research/multiplicatively-weighted-centers-median-graphs/','separate proposed URL')

pub=load(Q/'publication.json'); prom=load(Q/'promotion.json'); s=load(E/'public-sections.json'); bind=load(E/'metadata-support/SOURCE_PROTOCOL_BINDINGS.json'); auth=load(P/'verification/root-clearance-23385145-20261115.json'); ready=load(Q/'sources/SOURCE_READY.json')
require(digest(P/'verification/root-clearance-23385145-20261115.json')=='7103359ae07eb8c6e6560c7c8626cd991cc0c69f222134e10bea642b50350331','root authority exact SHA-256')
for f in load(E/'PROTECTED_INPUTS.json')['files']:
 p=Path(f['absolute_path']);require(p.stat().st_size==f['bytes'] and digest(p)==f['sha256'],'preexisting immutable '+str(p))
for key in ['root_authority','source_ready','source_manifest','source_seal','actual_transport_aggregate','whole_archive_custody','native_schema_types','printed_identity']:object_binding(bind[key])
for x in bind['all_seven_actual_transport_objects_in_original_collection_order']:object_binding(x,'actual_transport_file')
require(len(bind['all_seven_actual_transport_objects_in_original_collection_order'])==7,'all seven transport shapes/order')
for x in bind['all_four_native_API_objects_in_source_ready_order']:object_binding(x,'actual_path')
require(len(bind['all_four_native_API_objects_in_source_ready_order'])==4,'all four native API objects')
for x in bind['all_three_whole_literal_scientific_verdicts']:
 object_binding(x,'actual_verdict_path');require(digest(x['actual_seal_path'])==x['seal_sha256'],'literal science seal');require(typed(load(x['actual_seal_path']))==typed(x['whole_literal_original_seal']),'whole scientific seal object')
for x in bind['byte_identical_raw_copies']:
 require(Path(x['original_path']).read_bytes()==(E/'metadata-support'/x['owned_copy_relative_path']).read_bytes(),'raw byte copy identity')
for owner in [pub['source_binding'],prom]:
 require(typed(owner['whole_original_source_ready'])==typed(ready),'whole SOURCE_READY and historical flags')
 api=owner.get('whole_original_native_api_objects',owner.get('whole_original_native_api_objects'))
 require(typed(api)==typed(bind['all_four_native_API_objects_in_source_ready_order']),'complete native API objects/types/order')
 tr=owner.get('whole_original_seven_native_transport_objects',owner.get('whole_original_native_transport_receipts'))
 require(typed(tr)==typed(bind['all_seven_actual_transport_objects_in_original_collection_order']),'complete opaque transport objects/types/order')
 require(typed(owner['whole_original_native_transport_aggregate'])==typed(bind['actual_transport_aggregate']),'whole native aggregate')
require(typed(pub['review_metadata']['whole_root_scientific_clearance_record'])==typed(auth),'publication complete root authority')
require(typed(prom['whole_root_scientific_clearance_record'])==typed(auth),'promotion complete root authority')
for vv in [pub['review_metadata']['whole_original_custom_family_verdicts'],prom['whole_original_custom_family_verdicts']]:require(typed(vv)==typed(bind['all_three_whole_literal_scientific_verdicts']),'whole three literal custom verdicts')
require(prom['publication_sha256']==digest(Q/'publication.json'),'publication-config binding')
for k in ['rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified','current_five_stage_member','human_peer_review','formal_certification','source_repair','narrowed_replacement']:require(prom[k] is False,'false production/review/scope gate '+k)
for k in ['canonical_url','AA','native_sheet_aa_url','follow_up']:require(prom[k] is None,'null promotion gate '+k)
public_checks(pub,s)
copy=(E/'PUBLIC_COPY.md').read_text(); page=Page();page.feed((E/'candidate/index.html').read_text());visible=' '.join(page.data)
for key,paras in s['sections'].items():
 for para in paras:require(para in copy and para in visible,'whole visible public paragraph '+key)
for text in [pub['abstract'],pub['edition_note'],pub['reader_intro'],pub['rights_notice']]:require(text in copy and text in visible,'whole visible identity/abstract/rights')
require(any(t=='iframe' and a.get('src')=='assets/weighted_centers.pdf' and 'five-page' in a.get('title','') for t,a in page.tags),'original PDF iframe')
require(any(t=='meta' and a.get('name')=='robots' and a.get('content')=='noindex, nofollow' for t,a in page.tags),'private noindex')
require(not any(t=='link' and a.get('rel')=='canonical' for t,a in page.tags),'no assigned canonical in private candidate')
require(any(t=='meta' and a.get('name')=='citation_publication_date' and a.get('content')=='2026/10/14' for t,a in page.tags),'correct citation date')
for asset in ready['all_assets_in_original_order']:
 name=asset['original_api_file_object']['key'];require((E/'candidate/assets'/name).read_bytes()==Path(asset['path']).read_bytes(),'complete unchanged native asset '+name)
require((E/'candidate/assets/citation.bib').read_bytes()==(E/'citation.bib').read_bytes(),'citation download')
with zipfile.ZipFile(E/'candidate/assets/verification_package.zip') as z:
 require(len(z.infolist())==93 and len([x for x in z.infolist() if not x.is_dir()])==93,'entire 93-member original ZIP')
 require(z.testzip() is None,'original ZIP full CRC check')
require('Page' not in pub['publication_date_label'],'no audit date used as publication date')
for term in ['2026-11-15','2026-11-14','474 checks','431 preexisting','SEAL.json','SOURCE_READY','root-clearance','custody closure','SHA256','sha256','HTTP_status']:
 require(term not in copy and term not in visible,'no private audit-log leak '+term)
# Small boundary examples exercise exactly the preserved feasible set and zero-candidate issue.
d=[[abs(i-j) for j in range(3)] for i in range(3)]; boundary_cases=0
for w,R in [([Fraction(0)]*3,Fraction(0)),([Fraction(1),Fraction(0),Fraction(1)],Fraction(1)),([Fraction(1,2),Fraction(0),Fraction(3,2)],Fraction(3,4))]:
 D=2;b=[max(k for k in range(3) if k*a<=R) for a in w];a=[D-k for k in b]
 direct={x for x in range(3) if max(w[u]*d[x][u] for u in range(3))<=R}; transformed={x for x in range(3) if max(d[x][u]+a[u] for u in range(3))<=D}
 require(direct==transformed,'small exact all-feasible-set editorial boundary');boundary_cases+=1
 require(all(b[u]==D for u in range(3) if w[u]==0),'zero budgets retained')
require({x for x in range(3) if max(Fraction(w)*d[x][u] for u,w in enumerate([1,0,1]))<=1}=={1},'zero-weight vertex may be unique center')
# These mutations are memory-only; no supplied code, numerical campaign or disk edits.
mutations=[lambda x:x.update(abstract=x['abstract'][:-20]),lambda x:x['result'].__setitem__(0,x['result'][0].replace('unit edge lengths','arbitrary edge lengths')),lambda x:x['result'].__setitem__(1,x['result'][1].replace('promise that G is median','arbitrary input graph')),lambda x:x['result'].__setitem__(1,x['result'][1].replace('entire set C_w','one center only')),lambda x:x['result'].pop(),lambda x:x['background'].__setitem__(2,x['background'][2].replace('stronger O(n log²n)','earlier bound')),lambda x:x['why_it_works'].__setitem__(4,x['why_it_works'][4].replace('no assertion that the inaccessible final SODA','assertion that the final SODA')),lambda x:x.update(printed_version='1.0'),lambda x:x.update(publication_date='2026-10-15'),lambda x:x.update(code_license='MIT'),lambda x:x.update(follow_up='new conjecture'),lambda x:x.update(canonical_url=x['proposed_canonical_url'])]
rejected=0
for mutate in mutations:
 bad=deepcopy(pub);mutate(bad)
 try:public_checks(bad,s)
 except RuntimeError:rejected+=1
require(rejected==len(mutations),'all memory-only editorial-loss mutations rejected')
sealed=(E/'SEAL.json').exists()
if sealed:
 seal=load(E/'SEAL.json');require(digest(E/'OWNED_MANIFEST.json')==seal['owned_manifest_sha256'],'owned manifest seal')
 manifest=load(E/'OWNED_MANIFEST.json')
 for x in manifest['files']:
  p=Path(x['absolute_path']);require(p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],'owned file manifest '+str(p))
 expected={str(E/'OWNED_MANIFEST.json'),str(E/'SEAL.json')}|{x['absolute_path'] for x in manifest['files']}
 require({str(x) for x in E.rglob('*') if x.is_file()}|{str(Q/'publication.json'),str(Q/'promotion.json')}==expected,'exact owned namespace, no extras')
else:require('--unsealed' in sys.argv,'final seal required')
print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL_FIDELITY_AND_CUSTODY','checks':checks,'preexisting_files_unchanged':len(load(E/'PROTECTED_INPUTS.json')['files']),'whole_literal_scientific_verdicts':3,'whole_actual_transports':7,'full_ZIP_regular_payloads':93,'small_exact_editorial_boundary_cases':boundary_cases,'memory_only_editorial_mutations_rejected':rejected,'owned_manifest_seal_checked':sealed,'network_or_subprocess_or_file_writes':False,'source_or_legacy_programs_or_science_campaigns_run':False,'publication_or_AA_authority':False},indent=2))
