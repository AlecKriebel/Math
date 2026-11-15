#!/usr/bin/env python3
"""Pure informed editorial audit custody: no project imports, network, subprocesses, writes or science."""
from pathlib import Path,PurePosixPath
import hashlib,html,json,re,sys
R=Path(__file__).resolve().parent
P=R.parents[1]
S=P/'papers/23392409/sources'
E=P/'papers/23392409/reviews/editorial'
EXCLUDED={'AUDIT_MANIFEST.json','AUDIT_CLOSURE.json','AUDIT_SEAL.json'}
N=0;typed=0;wrappers=0

def need(ok,why):
 global N
 N+=1
 if not ok:raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need(p.is_file()and not p.is_symlink(),'regular original/snapshot');return p.read_bytes()
def load(p):return json.loads(read(p))
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b)and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def binding(root,row,relative=False):
 name=row['path']
 if relative:
  q=PurePosixPath(name);need(not q.is_absolute()and '..'not in q.parts and str(q)==name,'safe owned relative path');p=root/q
 else:p=Path(name)
 b=read(p);need(len(b)==row['bytes']and sha(b)==row['SHA256'],'whole binding '+str(p));return b

def main(preseal):
 global typed,wrappers
 source=load(R/'FROZEN_EXPECTATION_INPUTS.json');owner=load(R/'OWNER_FROZEN_INPUTS.json')
 need(len(source['source_namespace'])==121 and source['source_namespace_count']==121,'whole121 source expectation extent')
 need(sorted(str(p)for p in S.rglob('*')if p.is_file())==source['source_namespace']and not any(p.is_symlink()for p in S.rglob('*')),'whole original source namespace unchanged')
 for collection in[source['files'],owner['files']]:
  for row in collection:
   original=binding(R,row);snap=read(R/row['snapshot']);need(original==snap,'whole original/snapshot bytes')
   if row['path'].endswith('.json'):
    need(same(json.loads(original),json.loads(snap)),'strict whole JSON type/key/list/null/history equality');typed+=1
 need(owner['owner_whole_namespace_count']==69 and len(owner['files'])==69,'complete owner69 extent')
 ownnames=sorted(p.relative_to(E).as_posix()for p in E.rglob('*')if p.is_file());need(ownnames==[r['owner_relative_path']for r in owner['files']]and not any(p.is_symlink()for p in E.rglob('*')),'entire owner namespace unchanged')
 need(sha(read(E/'SEAL.json'))=='7e0b08a45a2edbc0d54cb633d5a79177a4495e341ef3c2218818e7f98f438eee','actual neutral ownerFINAL')
 need(sha(read(E/'MANIFEST.json'))=='493e17adc74c295a79e8d8ec07baf530f6a49bace1ce414aedf2b99893e3c28f','actual full owner manifest')
 om=load(E/'MANIFEST.json');need(len(om['files'])==67 and set(om['special_exclusions'])=={'MANIFEST.json','SEAL.json'},'owner exact67+2')
 need({r['relative_path']for r in om['files']}==set(ownnames)-{'MANIFEST.json','SEAL.json'},'whole owner manifest coverage')
 for row in om['files']:binding(E,{'path':row['relative_path'],'bytes':row['bytes'],'SHA256':row['SHA256']},True)
 initial=load(R/'EXPECTATION_SEAL.json')
 for row in initial['files']:binding(R,row,True)
 need(initial['stage']=='INFORMED_EXPECTATIONS_BEFORE_OWNER_FINAL','early expectation stage')
 reception=load(R/'OWNER_FINAL_RECEPTION.json');need(reception['owner_copy_not_read_until_whole_FINAL_frozen']is True and reception['preowner_expectation_seal_SHA256']==sha(read(R/'EXPECTATION_SEAL.json')),'copy-read ordering')
 clear=load(P/'verification/root-clearance-23392409-20261115.json');ready=load(S/'SOURCE_READY.json');pub=load(E/'publication.json');promotion=load(E/'promotion.json');protocol=load(E/'SOURCE_PROTOCOL_BINDINGS.json')
 need(same(clear['source_ready_whole_original'],ready),'root whole original SOURCE_READY preserved')
 need(same(pub['source_binding']['whole_original_source_ready'],ready),'publication whole original SOURCE_READY preserved')
 need(same(promotion['whole_source_binding'],pub['source_binding']),'promotion entire source binding preserved')
 need(same(pub['source_binding']['native_assets_in_original_order'],ready['all_native_assets_in_original_order']),'all3 whole native asset objects in original order')
 def walk(x,path):
  global wrappers,typed
  if isinstance(x,dict):
   if {'copy','bytes','SHA256','whole_literal_object'}<=set(x):
    q=PurePosixPath(x['copy']);need(not q.is_absolute()and '..'not in q.parts,'safe literal wrapper copy')
    b=read(E/q);need(len(b)==x['bytes']and sha(b)==x['SHA256'],'whole wrapper raw bytes '+path)
    need(same(x['whole_literal_object'],json.loads(b)),'whole wrapper strict typed object '+path);wrappers+=1;typed+=1
   for key,v in x.items():walk(v,path+'/'+key)
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,path+'/'+str(i))
 for name in['publication.json','promotion.json','SOURCE_PROTOCOL_BINDINGS.json','PRIMARY_SCOPE_AND_EDITION_LIMITS.json']:walk(load(E/name),name)
 for field in['root_authority','whole_original_custom_verdicts']:
  pfield=pub['review_metadata'][field]
  need(same(pfield,protocol['whole_root_scientific_authority']if field=='root_authority'else protocol['whole_original_scientific_custom_verdicts']),'whole review authority/custom objects retained')
 need(same(pub['review_metadata']['root_primary_reading_scope'],clear['root_primary_reading_scope']),'complete root edition/reading limits retained')
 need(same(pub['review_metadata']['root_authority']['whole_literal_object'],clear),'entire actual root authority object in publication')
 need(same(promotion['whole_root_scientific_authority']['whole_literal_object'],clear),'entire actual root authority object in promotion')
 need(same(protocol['source_ready']['whole_literal_object'],ready),'entire actual protocol READY')
 for left,right in zip(pub['review_metadata']['whole_original_custom_verdicts'],clear['whole_original_scientific_verdicts']):need(same(left['whole_literal_object'],right['whole_literal_object']),'entire actual heterogeneous scientific verdict in owner')
 need(len(pub['review_metadata']['whole_original_custom_verdicts'])==len(clear['whole_original_scientific_verdicts'])==2,'exact two current scientific dispositions')
 api=ready['whole_native_API_objects'];need(len(api)==len(protocol['whole_native_API_objects'])==len(pub['source_binding']['whole_original_native_API_objects'])==4,'complete ordered native API extent')
 for original,wrapped,other in zip(api,protocol['whole_native_API_objects'],pub['source_binding']['whole_original_native_API_objects']):
  need(same(load(Path(original['path'])),wrapped['whole_literal_object'])and same(wrapped,other),'whole actual API in original ordered association')
 for field,name in [('whole_ordered_transport_receipts','ALL_TRANSPORT_RECEIPTS.json'),('whole_native_schema_types','NATIVE_SCHEMA_TYPES.json'),('whole_archive_custody','ARCHIVE_CUSTODY.json'),('whole_original_queue_binding','QUEUE_BINDING.json'),('whole_original_native_identity_subset','NATIVE_IDENTITY_MATCH.json')]:need(same(protocol[field]['whole_literal_object'],load(S/name)),'whole actual native protocol '+field)
 protected=load(E/'PROTECTED_INPUTS.json');need(len(protected['source_files'])==121,'owner protects complete121source files')
 for row in protected['source_files']+protected['other_files']:binding(R,row)
 for x in clear['whole_original_scientific_verdicts']:need(same(x['whole_literal_object'],load(Path(x['file']['path']))),'root entire original custom scientific verdict')
 rec=load(S/'record.response.body');assets=rec['files'];need([x['key']for x in assets]==['five_centers.pdf','five_centers.tex','verification-package.zip'],'native3 asset order')
 need('version'not in rec['metadata']and pub['version_field_present']is False and pub['version']is None and pub['printed_version_field_present']is False and pub['printed_version']is None,'ABSENT native and absent printed version retained')
 need(rec['metadata']['publication_date']==pub['publication_date']=='2026-10-15'and pub['native_record_created']==rec['created']and pub['native_record_updated']==rec['updated'],'original date and separate created/updated')
 for a in assets:
  b=read(S/'assets'/a['key']);need(read(E/'candidate'/a['key'])==b,'complete unchanged candidate native asset');algorithm,value=a['checksum'].split(':',1);need(len(b)==a['size']and hashlib.new(algorithm,b).hexdigest()==value,'actual native checksum')
 need(read(E/'candidate/citation.bib')==read(E/'citation.bib')==pub['prepared_bibtex'].encode(),'whole BibTeX bytes')
 need('version'not in load(E/'SCHOLARLY_METADATA.json')and not re.search(r'^\s*version\s*=',read(E/'citation.bib').decode(),re.M|re.I),'no invented scholarly/Bib version')
 main=read(E/'PUBLIC_MAIN.html').decode();candidate=read(E/'candidate/index.html').decode();need(candidate.count(main)==1 and candidate.count('<main>')==1 and candidate.count('</main>')==1,'actual complete candidate main byte identity')
 scripts=re.findall(r'<script type="application/ld\+json">(.*?)</script>',candidate,re.S);need(len(scripts)==1 and same(json.loads(scripts[0]),load(E/'SCHOLARLY_METADATA.json')),'whole embedded scholarly object')
 need('<meta name="citation_version"'not in candidate and 'noindex,nofollow,noarchive'in candidate,'private candidate and no version meta')
 abstract=html.unescape(re.search(r'<h2>Original abstract</h2><p>(.*?)</p>',main,re.S)[1]);need(abstract==pub['abstract']==load(E/'SCHOLARLY_METADATA.json')['abstract'],'whole visible/config/JSONLD abstract identity')
 expected=('We specify six algebraic boundary points, an incoming center, and at least five distinct outgoing centers for a cube move of 16-realizations. Existence follows from strict rational sign bounds for two continuous one-variable residuals. The boundary parameters are uniquely defined real roots of monotone polynomials. This contradicts the at-most-three expectation for construction curves sharing a focus in Remark 4.8 of Melotti–Ramassamy–Thévenin, in the realization setting allowing crossings. The fixed boundary is crossed, so the example concerns no proper embedding. Neither the exact number of centers for this boundary nor a universal maximum is determined.')
 need(abstract==expected,'entire actual manuscript abstract without dropped qualifications')
 need(pub['license']=='CC BY 4.0'and pub['authored_package_license']=='CC BY 4.0'and pub['code_license']is None and 'no separate code-specific instrument'in pub['code_license_basis'],'broad CC BY support/code and separate instrument null')
 for gate in['rendered_public_copy_approved','production_integration_authorized','ready_to_publish','installed','deployed','live_verified','local_http_verified','browser_verified','native_verified','native_sheet_publication_verified','canonical_verified','public_page_published','all203_complete_claimed']:need(promotion[gate]is False,'separate future publication gate '+gate)
 for field in['follow_up','canonical_url','AA','native_sheet_aa_url']:need(pub[field]is None and promotion[field]is None,'literal null private publication/follow-up '+field)
 need(load(E/'inputs/scope-VERDICT.json')['root130_gate_at_final_seal']=='CLOSED'and load(E/'inputs/adversarial-VERDICT.json')['root_gate_at_final_preparation']=='CLOSED','historical CLOSED unchanged')
 need(load(E/'inputs/SOURCE_READY.json')['printed_title_date_version_inspected']is False and load(E/'inputs/SOURCE_READY.json')['printed_version']is None,'historical source unread/null flags unchanged')
 need(load(R/'AUDIT_FINDINGS.json')['literal_custom_verdict'].startswith('PASS_INFORMED_EDITORIAL_FACT_AUDIT')and load(R/'AUDIT_FINDINGS.json')['new_scientific_family_claimed']is False,'informed family disposition only')
 if not preseal:
  seal=load(R/'AUDIT_SEAL.json');need(sha(read(R/'AUDIT_MANIFEST.json'))==seal['MANIFEST_SHA256']and sha(read(R/'AUDIT_CLOSURE.json'))==seal['CLOSURE_SHA256'],'final audit terminal seal')
  am=load(R/'AUDIT_MANIFEST.json');names={p.relative_to(R).as_posix()for p in R.rglob('*')if p.is_file()}-EXCLUDED
  need(names=={x['path']for x in am['files']}and len(names)==len(am['files']),'whole own audit namespace')
  for row in am['files']:binding(R,row,True)
 print(json.dumps({'status':'INFORMED_EDITORIAL_AUDIT_CUSTODY_PASS','mode':'preseal'if preseal else'sealed','checks':N,'strict_whole_typed_objects':typed,'whole_literal_wrappers':wrappers,'source_namespace':121,'owner_namespace':69,'original_native_assets':3,'network_requests':0,'subprocesses':0,'writes':0,'science_or_owner_program_execution':False},sort_keys=True))
if __name__=='__main__':
 need(sys.argv[1:]in[[],['--preseal']],'bounded audit option');main(sys.argv[1:]==['--preseal'])
