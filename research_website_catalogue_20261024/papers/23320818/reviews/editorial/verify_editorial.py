"""Read-only static editorial relations/custody; no science, source helpers, network or rendering."""
from pathlib import Path
import json,hashlib,copy,zipfile,zlib,argparse
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');B=P/'papers/23320818';E=B/'reviews/editorial';S=B/'sources';C=P/'verification/root-clearance-23320818-20261114.json';PIN='a915c2103724bb58e2fba7ab964d61e4c129c89ad232e486f5374fe65745d084'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def literal(a,b):return json.dumps(a,ensure_ascii=False,separators=(',',':'))==json.dumps(b,ensure_ascii=False,separators=(',',':'))
def need(ok,n):
 if not ok:raise ValueError(n)
GATES=['rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_sheet_publication_verified','native_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified','public_promotion_authority']
def validate(pub,prom,req):
 root=load(C);ready=load(S/'SOURCE_READY.json');record=load(S/'record.raw.json');sb=pub['source_binding']
 need(sha(C)==PIN and root['status']=='PASS_WITH_EXPLICIT_STATIC_FOLIATION_BOUNDARY_VECTOR_AND_PRIORITY_LIMITS','exact qualified root authority')
 need(prom['status']=='PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED' and prom['scientific_status']==root['status'],'private and scientific states')
 need(literal(prom['whole_root_scientific_clearance_record'],root),'whole original root authority')
 need(literal(sb['whole_original_source_ready'],ready) and literal(prom['whole_original_source_ready'],ready),'literal native readiness/history')
 need(literal(sb['whole_native_record'],record) and literal(sb['all_assets_in_original_order'],ready['all_assets_in_original_order']),'native record and asset order/schema')
 need(literal(sb['whole_native_latest_record'],load(S/'latest.raw.json')) and literal(sb['whole_native_versions'],load(S/'versions.raw.json')),'whole native latest and versions bodies')
 need(literal(sb['whole_native_transport_objects'],root['transport_receipts_original']) and literal(prom['whole_native_transport_objects'],root['transport_receipts_original']),'all actual six whole transport objects/orders')
 need(len(sb['whole_native_transport_objects'])==6,'five individual receipts plus aggregate')
 for item in sb['whole_native_transport_objects']:need(sha(Path(item['path']))==item['sha256'] and literal(load(Path(item['path'])),item['original']),'actual native transport body')
 for fam,entry in root['reviews'].items():
  need(literal(prom['reviews'][fam]['root_authority_entry'],entry),'whole root family entry')
  need(literal(prom['reviews'][fam]['verdict'],load(Path(entry['verdict_path']))),'whole custom verdict')
 for obj in [pub,prom,pub['review_metadata'],req]:
  for k in ['canonical_url','AA','native_sheet_aa_url']:
   if k in obj:need(obj[k] is None,'null '+k)
 for obj in [prom,pub['review_metadata'],req]:
  for k in GATES:need(obj.get(k) is False,'withheld '+k)
 need(pub['follow_up'] is None and prom['follow_up'] is None and req['follow_up'] is None,'null follow-up')
 need(pub['title']==record['metadata']['title'] and pub['version']=='1.0' and pub['publication_date']=='2026-10-12','title/version/date')
 need(pub['doi']=='10.5281/zenodo.23320818' and pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','author/DOI/ORCID')
 raw=(S/'published-source/manuscript.tex').read_text().split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0];need(raw==(E/'ORIGINAL_ABSTRACT.tex').read_text()==sb['abstract_tex'],'full TeX abstract')
 normalized=raw
 for a,b in sb['abstract_normalization']['exact_presentational_replacements'].items():normalized=normalized.replace(a,b)
 need(' '.join(normalized.split())==pub['abstract'] and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True,'whole original abstract')
 clauses={0:['Fix any a > 0','ρ = |x| ≥ a','entire boundary sphere','every ψ','contravariant vector fields','arbitrary time and angular dependence','normal boundary trace may be nonzero'],1:['signature (−+++)','complete scalar contraction'],2:['g = −φ^(−2)dt² + φ⁴','natural static foliation','K = 0','harmonically regular','mass −2a','C¹ approaching-surface'],3:['For every test','∫_M |G^μ_ν ∇_μψ^ν| dV_g is finite','−(2/a²)','dt dA_δ','∫η dt = 1','equal to 1 near a','−8π'],4:['Ric_μν Ric^μν = 6a²/(ρ⁶φ¹⁰)','finite affine length','limiting radial conformal sense','no nondegenerate smooth extension','violates the null energy condition'],5:['every a > 0, A,B ≥ 0','A + B > 0','N = A + B(ρ + a)/(ρ − a)','For every allowed ψ','absolutely integrable','−(4A/a²)','exactly when A = 0','−16πA','A = B = 1/2','vacuum endpoint A = 0, B > 0','nonvacuum endpoint B = 0, A > 0','A = B = 0 is excluded']}
 for i,tokens in clauses.items():
  for token in tokens:need(token in pub['result'][i],'complete theorem/proposition '+token)
 why=' '.join(pub['why_it_works']);limits=' '.join(pub['limitations'])
 need('D^i_j = Nφ⁶G^i_j = (Aa/ρ³)(6n_i n_j − 2δ_ij)' in why,'exact full-family density coefficient')
 for token in ['entire singular connection contraction pointwise','complete scalar density','before integration','inner outward normal −n','Dadhich, Kar, Mukherjee and Visser','Bray and Jauregui','Burtscher, Kiessling and Tahvildar-Zadeh']:need(token in why,'full-scalar proof and credit '+token)
 for token in ['natural static foliation','not a regularity assertion on every arbitrary tilted','independently smooth covectors','collapsing S_a to a point','Lowering a vector','nearly-null','limiting radial conformal','ordinary classical identity','homogeneous zero functional','inhomogeneous boundary-flux','violates NEC','No specified electromagnetic','every stronger possible formalization','O((ρ − a)^(−5+κ))','2a³','historical firstness','continued worldwide openness']:need(token in limits,'explicit original scope '+token)
 need(len(pub['background'])==4,'all primary credit interfaces')
 ai=pub['ai_disclosure'];need(all(t in ai for t in ['extensively','unrefereed','not external human or journal peer review','no journal acceptance or formal proof-assistant certification','named author is responsible']),'complete AI/unrefereed/nonhuman/nonformal status')
 need(pub['license']=='CC BY 4.0' and pub['license_url']=='https://creativecommons.org/licenses/by/4.0/' and 'code_license' not in pub,'native authored license without invented MIT')
 need('License: CC BY 4.0.' in (S/'published-source/README.md').read_text(),'actual license source')
 hist=sb['historical_manifest_provenance'];need(literal(hist,prom['historical_manifest_provenance']) and hist['status']=='UNATTESTED' and hist['standalone_author_manifest_digest_attested'] is False and hist['supplied_path_or_bytes_available'] is False and hist['historical_bytes_reconstructed'] is False,'unattested remains unattested')
 need(root['unattested_historical_manifest_digest_remains_unattested'] is True and literal(hist['current_analytic_verdict_original_computation'],load(Path(root['reviews']['analytic']['verdict_path']))['computation']),'literal historical qualification')
 need(pub['prepared_bibtex']==(E/'CITATION.bib').read_text() and 'version = {1.0}' in pub['prepared_bibtex'] and 'day = {12}' in pub['prepared_bibtex'] and '10.5281/zenodo.23320818' in pub['prepared_bibtex'],'exact citation')
 need(pub['pdf_pages']==6 and pub['pdf_filename']=='regular_zas_bianchi_defect.pdf' and pub['supplement_filename']=='regular_zas_bianchi_verification_v1.zip','whole reader/support')
 need(sb['pdf_sha256']==prom['pdf_sha256']==sha(S/pub['pdf_filename']) and sb['supplement_sha256']==prom['supplement_sha256']==sha(S/pub['supplement_filename']),'complete native asset hashes')
 need(sb['embedded_PDF_payloads']==0 and sb['public_page_reader_pdf_count']==1,'standalone reader not invented ZIP reader')
 need(req['reader']['iframe_count']==1 and req['reader']['complete_page_count']==6 and req['reader']['iframe_src']==pub['pdf_filename'],'one complete accessible reader')
 for key,name in [('local_PDF_download',pub['pdf_filename']),('local_ZIP_download',pub['supplement_filename']),('citation_download','citation.bib')]:need(req['reader'][key]['download_attribute']==name,'download attribute '+key)
 need(len(req['article_assets'])==4 and req['third_party_primary_caches_public_assets'] is False,'complete article assets')
 z=next(x for x in req['article_assets'] if x['local_name']==pub['supplement_filename']);need(z['whole_native_archive'] is True and z['bytes']==258059 and z['sha256']==sb['supplement_sha256'],'no archive subset')
 return True

def controls(p,q,r):
 cases=[]
 def add(n,f):cases.append((n,f))
 add('abstract abridged',lambda a,b,c:a.update(abstract=a['abstract'].split('.')[0]+'.'))
 add('radial-only tests substituted',lambda a,b,c:a['result'].__setitem__(0,a['result'][0].replace('arbitrary time and angular dependence','radial tests only')))
 add('smooth covectors substituted',lambda a,b,c:a['result'].__setitem__(0,a['result'][0].replace('contravariant vector fields','covector fields')))
 add('boundary collapsed to point',lambda a,b,c:a['result'].__setitem__(0,a['result'][0].replace('entire boundary sphere','collapsed boundary point')))
 add('boundary normal prohibited',lambda a,b,c:a['result'].__setitem__(0,a['result'][0].replace('normal boundary trace may be nonzero','normal boundary trace must vanish')))
 add('conditional scalar convergence substituted',lambda a,b,c:a['result'].__setitem__(3,a['result'][3].replace('∫_M |G^μ_ν ∇_μψ^ν| dV_g is finite','a principal value exists')))
 add('wrong main boundary sign',lambda a,b,c:a['result'].__setitem__(3,a['result'][3].replace('−(2/a²)','+(2/a²)')))
 add('wrong radial value',lambda a,b,c:a['result'].__setitem__(3,a['result'][3].replace('−8π','+8π')))
 add('affine family narrowed to main member',lambda a,b,c:a['result'].__setitem__(5,a['result'][5].replace('every a > 0, A,B ≥ 0','a = 1, A = B = 1/2')))
 add('vacuum iff endpoint omitted',lambda a,b,c:a['result'].__setitem__(5,a['result'][5].replace('exactly when A = 0','for some parameters')))
 add('zero lapse endpoint admitted',lambda a,b,c:a['result'].__setitem__(5,a['result'][5].replace('A = B = 0 is excluded','A = B = 0 is included')))
 add('all arbitrary tilts claimed',lambda a,b,c:a['limitations'].__setitem__(0,a['limitations'][0].replace('not a regularity assertion on every arbitrary tilted','a regularity assertion on every arbitrary tilted')))
 add('NEC qualification removed',lambda a,b,c:a['result'].__setitem__(4,a['result'][4].replace('violates the null energy condition','satisfies the null energy condition')))
 add('physical extension invented',lambda a,b,c:a['result'].__setitem__(4,a['result'][4].replace('no nondegenerate smooth extension','a nondegenerate smooth extension')))
 add('principal-value proof substituted',lambda a,b,c:a['why_it_works'].__setitem__(2,'A principal value proves the theorem.'))
 add('classical method credit removed',lambda a,b,c:a['why_it_works'].__setitem__(3,'This is a new metric, tensor and flux method.'))
 add('density coefficient corrupted',lambda a,b,c:a['why_it_works'].__setitem__(1,a['why_it_works'][1].replace('(Aa/ρ³)','(2Aa/ρ³)')))
 add('priority qualification removed',lambda a,b,c:a['limitations'].__setitem__(5,'This was the first-ever solution.'))
 add('matter limitation removed',lambda a,b,c:a['limitations'].__setitem__(3,'Every electromagnetic model is resolved.'))
 add('missing AI disclosure',lambda a,b,c:a.update(ai_disclosure='Verified by reviewers.'))
 add('wrong date',lambda a,b,c:a.update(publication_date='2026-10-03'))
 add('wrong version',lambda a,b,c:a.update(version='1.0.0'))
 add('wrong DOI',lambda a,b,c:a.update(doi='10.5281/zenodo.23320817'))
 add('invented MIT code license',lambda a,b,c:a.update(code_license='MIT'))
 add('unavailable digest attested',lambda a,b,c:a['source_binding']['historical_manifest_provenance'].update(status='VERIFIED',standalone_author_manifest_digest_attested=True))
 add('historical bytes invented',lambda a,b,c:a['source_binding']['historical_manifest_provenance'].update(historical_bytes_reconstructed=True))
 add('readiness reading history rewritten',lambda a,b,c:a['source_binding']['whole_original_source_ready'].update(target_manuscript_scientifically_read=True))
 add('native asset order reversed',lambda a,b,c:a['source_binding']['all_assets_in_original_order'].reverse())
 add('whole latest body fabricated',lambda a,b,c:a['source_binding']['whole_native_latest_record'].update(unpublished_alias='substitute'))
 add('whole versions body fabricated',lambda a,b,c:a['source_binding']['whole_native_versions'].update(unpublished_alias='substitute'))
 add('native source hash key case changed',lambda a,b,c:a['source_binding']['all_assets_in_original_order'][0].update(SHA256=a['source_binding']['all_assets_in_original_order'][0].pop('sha256')))
 add('aggregate receipt flattened',lambda a,b,c:a['source_binding']['whole_native_transport_objects'][-1].update(original=a['source_binding']['whole_native_transport_objects'][-1]['original']['ordinary_HTTPS_requests_in_native_object_and_file_order']))
 add('individual receipt body fabricated',lambda a,b,c:a['source_binding']['whole_native_transport_objects'][0]['original'].update(body={}))
 add('receipt headers reordered',lambda a,b,c:a['source_binding']['whole_native_transport_objects'][0]['original']['response_headers_in_received_order'].reverse())
 add('individual receipt omitted',lambda a,b,c:a['source_binding']['whole_native_transport_objects'].pop(0))
 add('custom verdict normalized',lambda a,b,c:b['reviews']['analytic']['verdict'].update(assessment='PASS'))
 add('qualified authority normalized',lambda a,b,c:b.update(scientific_status='PASS'))
 add('whole root authority rewritten',lambda a,b,c:b['whole_root_scientific_clearance_record'].update(public_promotion_authority=True))
 add('public canonical prematurely set',lambda a,b,c:a.update(canonical_url=a['proposed_canonical_url']))
 add('native AA prematurely set',lambda a,b,c:b.update(AA=a['proposed_canonical_url']))
 add('publication clearance prematurely set',lambda a,b,c:b.update(publication_clearance=True))
 add('follow-up invented',lambda a,b,c:a.update(follow_up={'question':'Generic variation'}))
 add('reader truncated',lambda a,b,c:a.update(pdf_pages=2))
 add('ZIP subset substituted',lambda a,b,c:c['article_assets'][2].update(whole_native_archive=False))
 add('ZIP reader invented',lambda a,b,c:a['source_binding'].update(embedded_PDF_payloads=1))
 add('iframe omitted',lambda a,b,c:c['reader'].update(iframe_count=0))
 add('download attribute omitted',lambda a,b,c:c['reader']['local_PDF_download'].update(download_attribute=None))
 names=[]
 for n,f in cases:
  a,b,c=copy.deepcopy(p),copy.deepcopy(q),copy.deepcopy(r);f(a,b,c)
  try:validate(a,b,c)
  except (ValueError,KeyError,TypeError):names.append(n)
  else:raise ValueError('Control failed to reject: '+n)
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preseal',action='store_true');args=ap.parse_args();pub=load(B/'publication.json');prom=load(B/'promotion.json');req=load(E/'PUBLICATION_REQUIREMENTS.json');validate(pub,prom,req)
 old=load(E/'ORIGINAL_INPUTS_BEFORE.json')
 for x in old['original_bindings']+old['protected_prior_immutable_bindings']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'protected original '+str(p))
 copies=load(E/'ORIGINAL_OBJECT_COPIES.json')
 for x in copies:need((E/x['copy_path']).read_bytes()==Path(x['original_path']).read_bytes(),'byte-identical raw copy')
 for x in load(E/'PREPARED_CONFIG_COPIES.json'):need(Path(x['current_path']).read_bytes()==Path(x['prepared_copy']).read_bytes(),'historical prepared config')
 manifest=load(S/'SOURCE_READY_MANIFEST.json')
 for x in manifest['files']:
  p=S/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'native source manifest')
 for x in load(S/'record.raw.json')['files']:
  p=S/x['key'];need(p.stat().st_size==x['size'] and 'md5:'+hashlib.md5(p.read_bytes()).hexdigest()==x['checksum'],'native size/MD5')
 with zipfile.ZipFile(S/pub['supplement_filename']) as z:
  members=[x for x in z.infolist() if not x.is_dir()];need(len(members)==181,'all ZIP payloads');pdfs=0
  for x in members:
   d=z.read(x);need(zlib.crc32(d)&0xffffffff==x.CRC and d==(S/'published-source'/x.filename).read_bytes(),'ZIP CRC/extraction identity');pdfs+=d.startswith(b'%PDF')
  need(pdfs==0,'no embedded PDF')
 text=(E/'PUBLIC_COPY.md').read_text();sections=load(E/'public-sections.json');need(text.count(pub['abstract'])==1 and sections['abstract']['text']==pub['abstract'],'complete public abstract')
 for field in ['plain_language','result','why_it_works','limitations']:
  for paragraph in pub[field]:need(paragraph in text,'every public paragraph '+field)
 for field in ['status','edition_note','ai_disclosure','collaboration']:need(pub[field] in text,'public '+field)
 need(prom['publication_sha256']==sha(B/'publication.json'),'publication/config binding')
 for token in ['SOURCE_READY','SHA256','INITIAL_SEAL','2026-11-15','UNATTESTED','1557','3615','root-clearance','PRIVATE_EDITORIAL']:need(token not in text,'no private audit narrative '+token)
 metadata=load(E/'SCHOLARLY_METADATA.json');need(metadata['canonical_url'] is None and metadata['citation_pdf_url'] is None and metadata['jsonld']['url'] is None,'unfinalized scholarly template')
 names=controls(pub,prom,req)
 if not args.preseal:
  need(sha(E/'MANIFEST.json')==load(E/'SEAL.json')['manifest_sha256'],'final manifest/seal')
  for x in load(E/'MANIFEST.json')['owned_files']:
   p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'final owned binding')
 print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL_RELATIONS_CUSTODY_AND_WITHHELD_GATES','scope':'Read-only static editorial/custody checks; no mathematical replay, source program, renderer, network or publication verification.','original_bindings_verified':len(old['original_bindings']),'prior_immutable_bindings_verified':len(old['protected_prior_immutable_bindings']),'whole_object_copies_verified':len(copies),'native_source_manifest_bindings':len(manifest['files']),'native_ZIP_payloads_CRC_and_identity':181,'literal_transport_objects':6,'historical_standalone_manifest_status':'UNATTESTED','negative_controls_rejected':len(names),'negative_control_names':names,'all_original_objects_schemas_and_historical_states_unchanged':True,'canonical_url':None,'AA':None,'follow_up':None,'publication_clearance':False,'final_envelope_verified':not args.preseal},indent=2))
if __name__=='__main__':main()
