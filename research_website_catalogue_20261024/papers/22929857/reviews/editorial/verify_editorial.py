"""Read-only static closure: literal objects, complete prose, assets and withheld gates.
No network, writes, source programs, scientific replays, shared adapters, rendering or app changes.
"""
from pathlib import Path
import json,hashlib,copy,argparse,zipfile,zlib,re
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');B=P/'papers/22929857';E=B/'reviews/editorial';S=B/'sources'
PIN='3f747e63612ccc879b10f6241865b804374c85951743ceb46046935d3da0dc79'
CLEAR=P/'verification/root-clearance-22929857-20261114.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,label):
 if not ok:raise ValueError(label)
def literal(a,b):return json.dumps(a,ensure_ascii=False,separators=(',',':'))==json.dumps(b,ensure_ascii=False,separators=(',',':'))
def load(p):return json.loads(p.read_text())
GATES=['rendered','deployed','rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified']
def validate(pub,prom,req):
 root=load(CLEAR);ready=load(S/'SOURCE_READY.json');acq=load(S/'acquisition.transport.json');rt=load(S/'record.transport.json');record=load(S/'record.raw.json');sb=pub['source_binding']
 need(sha(CLEAR)==PIN and root['status']=='PASS_WITH_EXPLICIT_METRIC_CLASSICAL_METHOD_AND_PRIORITY_LIMITS','exact qualified root authority')
 need(prom['status']=='PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED' and prom['scientific_status']==root['status'],'private versus scientific status')
 need(literal(prom['whole_root_scientific_clearance_record'],root),'whole root object and key orders')
 need(literal(sb['whole_original_source_ready'],ready) and literal(prom['whole_original_source_ready'],ready),'whole readiness history')
 for key,original in [('whole_native_acquisition_transport_receipt',acq),('whole_native_record_transport_receipt',rt)]:
  need(literal(sb[key],original) and literal(prom[key],original),'both literal native transports '+key)
 need(sb['transport_receipt_paths']==['sources/acquisition.transport.json','sources/record.transport.json'],'actual two receipt paths')
 need(literal(sb['whole_native_record'],record),'whole raw record')
 need(literal(sb['all_native_assets_in_original_order'],ready['all_native_assets_in_original_order']),'native asset order and schema')
 for family,entry in root['reviews'].items():
  need(literal(prom['reviews'][family]['root_authority_entry'],entry),'whole root family entry '+family)
  need(literal(prom['reviews'][family]['verdict'],load(Path(entry['verdict_path']))),'whole original custom verdict '+family)
 for obj in [pub,prom,pub['review_metadata'],req]:
  for name in ['canonical_url','AA','native_sheet_aa_url']:
   if name in obj:need(obj[name] is None,'withheld '+name)
 for obj in [prom,pub['review_metadata'],req]:
  for gate in GATES:need(obj.get(gate) is False,'withheld '+gate)
 need(pub['follow_up'] is None and prom['follow_up'] is None and req['follow_up'] is None,'null follow-up')
 need(pub['version']=='1.1' and pub['edition_label']=='Version 1.1' and pub['publication_date']=='2026-09-23','actual date/version')
 need(pub['doi']=='10.5281/zenodo.22929857' and pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','identity and citation')
 need(pub['title']==record['metadata']['title'],'actual title')
 tex=(S/'published-source/paper/main.tex').read_text();raw=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
 need(raw==(E/'ORIGINAL_ABSTRACT.tex').read_text()==sb['abstract_tex'],'complete exact TeX abstract')
 normalized=raw
 for old,new in sb['abstract_normalization']['exact_presentational_replacements'].items():normalized=normalized.replace(old,new)
 need(' '.join(normalized.split())==pub['abstract'],'full normalized original abstract')
 need(pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True,'abstract label')
 statement='\n'.join(pub['result'])
 for token in ['For every finite n ≥ 2 and N ≥ 1','unit-round','induced length metric','unnormalized Hilbert–Schmidt','operator norm','uniform topology','Fix p','L ≤ 1/2','For every t ∈ [0,1]','A(WΦ(x) + tI)(I + tWΦ(x))^(−1)','((1 − t²)/(1 + t²)) L','constant Φ(p)','t = 0','t = 1','strict L < 1/2','nonsmooth','copy of U(N)','angular distance π','For any topological parameter space Y','constant Q,R','Ht(QΦR) = QHt(Φ)R']:
  need(token in statement,'complete quantified result '+token)
 why=' '.join(pub['why_it_works']);need('intrinsic curve length' in why and 'actual image of a shortest sphere geodesic' in why and 'nonsmooth' in why,'intrinsic nonsmooth proof interface')
 limits=' '.join(pub['limitations']);need('fixed domain basepoint' in limits and 'one prescribed point' in limits and 'sphere-fibration' in limits and 'first-publication priority' in limits and 'continued worldwide openness' in limits,'explicit scope and priority limits')
 need('classical Cayley' in why and 'logarithm chart' in why and len(pub['background'])==2,'positive classical credit')
 ai=pub['ai_disclosure'];need(all(t in ai for t in ['extensively','unrefereed','not external human or journal peer review','no journal acceptance or formal proof-assistant certification','named author is responsible']),'complete AI and review disclosure')
 need(pub['license']=='CC BY 4.0' and pub['license_url']=='https://creativecommons.org/licenses/by/4.0/' and pub['code_license']=='MIT','actual separate rights')
 need(pub['prepared_bibtex']==(E/'CITATION.bib').read_text(),'exact BibTeX')
 need('version = {1.1}' in pub['prepared_bibtex'] and '10.5281/zenodo.22929857' in pub['prepared_bibtex'] and 'day = {23}' in pub['prepared_bibtex'],'actual citation fields')
 need(pub['pdf_pages']==4 and pub['pdf_filename']=='paper.pdf' and pub['supplement_filename']=='reproducibility.zip','complete reader and support')
 need(sb['pdf_sha256']==sha(S/'paper.pdf') and sb['supplement_sha256']==sha(S/'reproducibility.zip'),'exact asset hashes')
 need(req['reader']['iframe_count']==1 and req['reader']['complete_page_count']==4 and req['reader']['iframe_src']=='paper.pdf','single complete reader')
 need(req['reader']['local_PDF_download']['download_attribute']=='paper.pdf' and req['reader']['local_ZIP_download']['download_attribute']=='reproducibility.zip' and req['reader']['citation_download']['download_attribute']=='citation.bib','explicit downloads')
 need(len(req['article_assets'])==4 and req['third_party_primary_caches_public_assets'] is False,'whole article asset set')
 zipasset=next(z for z in req['article_assets'] if z['local_name']=='reproducibility.zip');need(zipasset['whole_native_archive'] is True and zipasset['bytes']==133556 and zipasset['sha256']==sha(S/'reproducibility.zip'),'whole unchanged ZIP requirement')
 need(prom['pdf_sha256']==sb['pdf_sha256'] and prom['supplement_sha256']==sb['supplement_sha256'],'promotion asset relations')
 return True

def controls(pub,prom,req):
 mutations=[]
 def add(name,func):mutations.append((name,func))
 add('abridged original abstract',lambda a,b,c:a.update(abstract=a['abstract'].split('.')[0]+'.'))
 add('normalized HS substitution',lambda a,b,c:a['result'].__setitem__(0,a['result'][0].replace('unnormalized','normalized')))
 add('finite dimension narrowing',lambda a,b,c:a['result'].__setitem__(0,a['result'][0].replace('For every finite n ≥ 2 and N ≥ 1','For n = 2 and N = 2')))
 add('wrong q coefficient',lambda a,b,c:a['result'].__setitem__(1,a['result'][1].replace('((1 − t²)/(1 + t²)) L','((1 − t)/(1 + t)) L')))
 add('missing nonsmooth qualification',lambda a,b,c:a['result'].__setitem__(2,a['result'][2].replace('nonsmooth','smooth')))
 add('S0 path-metric substitution',lambda a,b,c:a['result'].__setitem__(3,a['result'][3].replace('angular distance π','intrinsic path distance')))
 add('missing arbitrary parameter families',lambda a,b,c:a['result'].__setitem__(4,'One smooth family is allowed.'))
 add('chordal substitution',lambda a,b,c:a['why_it_works'].__setitem__(1,a['why_it_works'][1].replace('intrinsic curve length','chordal distance')))
 add('missing classical credit',lambda a,b,c:a['why_it_works'].__setitem__(2,'This is a first-ever mechanism.'))
 add('missing priority qualification',lambda a,b,c:a['limitations'].__setitem__(3,'This is the first solution.'))
 add('missing extensive AI disclosure',lambda a,b,c:a.update(ai_disclosure='Internally checked.'))
 add('wrong printed version',lambda a,b,c:a.update(version='1.0'))
 add('created-date replacing publication',lambda a,b,c:a.update(publication_date='2026-09-24'))
 add('wrong DOI',lambda a,b,c:a.update(doi='10.5281/zenodo.22929856'))
 add('wrong rights',lambda a,b,c:a.update(code_license='CC BY 4.0'))
 add('omitted ZIP',lambda a,b,c:a.update(supplement_filename=None))
 add('truncated reader',lambda a,b,c:a.update(pdf_pages=2))
 add('wrong asset hash',lambda a,b,c:a['source_binding'].update(pdf_sha256='0'*64))
 add('rewritten original source reading history',lambda a,b,c:a['source_binding']['whole_original_source_ready'].update(target_manuscript_scientifically_read=True))
 add('source asset reordering',lambda a,b,c:a['source_binding']['all_native_assets_in_original_order'].reverse())
 add('transport header reordering',lambda a,b,c:a['source_binding']['whole_native_acquisition_transport_receipt']['responses_in_requested_order'][0][1]['headers'].reverse())
 add('native hash key lowercased',lambda a,b,c:a['source_binding']['all_native_assets_in_original_order'][0].update(sha256=a['source_binding']['all_native_assets_in_original_order'][0].pop('SHA256')))
 add('record receipt invented MD5',lambda a,b,c:a['source_binding']['whole_native_record_transport_receipt'].update(MD5='0'*32))
 add('acquisition object coerced to list',lambda a,b,c:a['source_binding'].update(whole_native_acquisition_transport_receipt=a['source_binding']['whole_native_acquisition_transport_receipt']['responses_in_requested_order']))
 add('historical root adoption rewritten',lambda a,b,c:b['reviews']['analytic']['verdict'].update(root_adoption={'approved':True}))
 add('whole ZIP flag replaced by subset',lambda a,b,c:c['article_assets'][2].update(whole_native_archive=False))
 add('fabricated generic receipt path',lambda a,b,c:a['source_binding'].update(transport_receipt_paths=['sources/receipt.json']))
 add('custom verdict normalized to PASS',lambda a,b,c:b['reviews']['analytic']['verdict'].update(assessment='PASS'))
 add('root original publication authority rewritten',lambda a,b,c:b['whole_root_scientific_clearance_record'].update(public_promotion_authority=True))
 add('qualified scientific status normalized',lambda a,b,c:b.update(scientific_status='PASS'))
 add('premature canonical',lambda a,b,c:a.update(canonical_url=a['proposed_canonical_url']))
 add('premature native AA',lambda a,b,c:b.update(AA=a['proposed_canonical_url']))
 add('premature publication clearance',lambda a,b,c:b.update(publication_clearance=True))
 add('invented follow-up',lambda a,b,c:a.update(follow_up={'question':'Generic extension'}))
 add('missing iframe',lambda a,b,c:c['reader'].update(iframe_count=0))
 add('missing PDF download attribute',lambda a,b,c:c['reader']['local_PDF_download'].update(download_attribute=None))
 names=[]
 for name,func in mutations:
  a,b,c=copy.deepcopy(pub),copy.deepcopy(prom),copy.deepcopy(req);func(a,b,c)
  try:validate(a,b,c)
  except (ValueError,KeyError,TypeError):names.append(name)
  else:raise ValueError('control failed to reject '+name)
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preseal',action='store_true');args=ap.parse_args();pub=load(B/'publication.json');prom=load(B/'promotion.json');req=load(E/'PUBLICATION_REQUIREMENTS.json');validate(pub,prom,req)
 before=load(E/'ORIGINAL_INPUTS_BEFORE.json')
 for item in before['original_bindings']+before['protected_prior_immutable_bindings']:
  p=Path(item['path']);need(p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'protected original '+str(p))
 copies=load(E/'ORIGINAL_OBJECT_COPIES.json')
 for item in copies:need((E/item['copy_path']).read_bytes()==Path(item['original_path']).read_bytes(),'byte-identical object copy')
 for item in load(S/'SOURCE_READY_MANIFEST.json')['files']:
  p=S/item['path'];need(p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'native source binding')
 for item in load(E/'PREPARED_CONFIG_COPIES.json'):need(Path(item['current_path']).read_bytes()==Path(item['prepared_copy']).read_bytes(),'historical prepared-config copy')
 record=load(S/'record.raw.json')
 for item in record['files']:
  p=S/item['key'];need(p.stat().st_size==item['size'] and 'md5:'+hashlib.md5(p.read_bytes()).hexdigest()==item['checksum'],'native asset MD5 and size')
 with zipfile.ZipFile(S/'reproducibility.zip') as z:
  members=[x for x in z.infolist() if not x.is_dir()];need(len(members)==30,'complete ZIP payload count')
  for item in members:
   data=z.read(item);need(zlib.crc32(data)&0xffffffff==item.CRC and data==(S/'published-source'/item.filename).read_bytes(),'every CRC/extraction identity')
 need((S/'paper.pdf').read_bytes()==(S/'published-source/paper/main.pdf').read_bytes(),'unique original reader')
 public=(E/'PUBLIC_COPY.md').read_text();sections=load(E/'public-sections.json')
 need(public.count(pub['abstract'])==1 and sections['abstract']['text']==pub['abstract'],'original abstract in complete public copy')
 for field in ['plain_language','result','why_it_works','limitations']:
  for paragraph in pub[field]:need(paragraph in public,'every unique public paragraph '+field)
 for field in ['status','ai_disclosure','collaboration','edition_note'] :need(pub[field] in public,'complete public '+field)
 for forbidden in ['SOURCE_READY','SHA256','root-clearance','7679','33,057','INITIAL_SEAL','2026-11-15','PRIVATE_EDITORIAL'] :need(forbidden not in public,'no private audit narrative '+forbidden)
 need(prom['publication_sha256']==sha(B/'publication.json'),'config binding')
 schema=load(E/'SCHOLARLY_METADATA.json');need(schema['canonical_url'] is None and schema['citation_pdf_url'] is None and schema['jsonld']['url'] is None,'private scholarly template')
 names=controls(pub,prom,req)
 if not args.preseal:
  seal=load(E/'SEAL.json');need(sha(E/'MANIFEST.json')==seal['manifest_sha256'],'final envelope')
  for item in load(E/'MANIFEST.json')['owned_files']:
   p=Path(item['path']);need(p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'final owned artifact '+str(p))
 print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL_RELATIONS_CUSTODY_AND_WITHHELD_GATES','scope':'Static editorial relations and unchanged evidence; not mathematical replay, renderer, local/live/browser/native verification or publication authority.','original_bindings_verified':len(before['original_bindings']),'prior_immutable_bindings_verified':len(before['protected_prior_immutable_bindings']),'whole_object_copies_verified':len(copies),'native_payloads_CRC_and_identity':30,'literal_transport_receipts':2,'negative_controls_rejected':len(names),'negative_control_names':names,'all_original_native_schemas_and_historical_states_unchanged':True,'canonical_url':None,'AA':None,'follow_up':None,'publication_clearance':False,'final_envelope_verified':not args.preseal},indent=2))
if __name__=='__main__':main()
