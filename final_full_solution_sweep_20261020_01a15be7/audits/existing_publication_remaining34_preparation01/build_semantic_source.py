"""Exact carrier-specific source preparation. No service providers, authority or mutation."""
from pathlib import Path
import gzip,json,hashlib,re,datetime,html,unicodedata,os
O=Path(__file__).resolve().parent;D=O.parent/'existing_publication_remaining_rows_inventory01'
def sha(b):return hashlib.sha256(b).hexdigest()
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def gz(root,n):return json.loads(gzip.decompress((root/'private'/(n+'.json.gz')).read_bytes()))
def save(n,v,z=False):
 b=(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=None if z else 2,separators=(',',':')if z else None)+'\n').encode();p=O/(('private/'+n+'.json.gz')if z else n+'.json');assert not p.exists();b=gzip.compress(b,mtime=0)if z else b;assert sum(q.lstat().st_blocks*512 for q in[O,*O.rglob('*')])+len(b)+4096<=10*1024*1024;p.write_bytes(b);return {'path':str(p.relative_to(O)),'sha256':sha(b),'bytes':len(b)}
def norm(v):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',html.unescape(str(v)))if not unicodedata.combining(c)).casefold().split())
F=json.loads((D/'FROZEN_PROPOSALS.json').read_bytes())['items'];INV={x['pr']:x for x in json.loads((D/'REMAINING_ROWS_INVENTORY.json').read_bytes())['items']};contracts=json.loads((D/'IDENTITY_CONTRACTS.json').read_bytes())['contracts'];groups=gz(O,'SEMANTIC_READING_GROUPS')['groups'];idx=gz(D,'TERMINAL_CARRIER_INDEX')['index'];base={x['key']:x['full_carrier']for x in gz(D,'closing_FULL_CARRIERS')};owned=gz(D,'terminal_owned_complete_pass1')['records'];local=gz(D,'terminal_LOCAL_SCIENTIFIC_CARRIERS')['items'];sheet=gz(O,'numeric_complete')['values'];assert len(sheet)==237 and sheet[:236]==gz(D,'closing_complete_numeric')['values'];full=[]
for x in idx:
 ref=x['complete_body_source'];body=owned[ref['records_key']]if'records_key'in ref else local[ref['items_index']]if'items_index'in ref else base[x['key']]
 full.append({'key':x['key'],'kind':x['kind'],'body':body,'body_sha256':sha(can(body)),'inherited_canonical_sha256':x['full_carrier_sha256'],'source':ref})
full.append({'key':'sheet:237','kind':'sheet','body':sheet[236],'body_sha256':sha(can(sheet[236])),'source':{'capture':'private/numeric_complete.json.gz','values_index':236}})
notes={}
for p in sorted(O.glob('SEMANTIC_SCOPE_NOTES_*.json')):
 for i,n in json.loads(p.read_bytes())['notes'].items():assert int(i)not in notes;notes[int(i)]=n
sheetnotes={g['key']:notes[i]for i,g in enumerate(groups)if g['key'].startswith('sheet:')};links={i:row for i,key,row,title in json.loads((O/'SHEET_RECORD_READING_LINKS.json').read_bytes())['linked']};carrier_to_group={c['index']:i for i,g in enumerate(groups)for c in g['carriers']};scope_notes={}
for i,g in enumerate(groups):
 if i in notes:note=notes[i];basis='Fresh complete scoped claim reading recorded in per-group notes.'
 elif g['key'].startswith('proposal:'):
  pr=int(g['key'].split(':')[1]);note=INV[pr]['scope_accounting_note'];basis='Full original literal proposal and adopted qualified source contract, previously read in closed inventory and retained byte-exact.'
 else:
  row=links.get(i);assert row and 'sheet:'+str(row)in sheetnotes,(i,g['key']);note=sheetnotes['sheet:'+str(row)];basis='Exact DOI/version integer links this complete record to the full43-cell ledger claim read in full; no title/author-only link. All complete metadata/alternate versions stay bound separately.'
 scope_notes[i]={'note':note,'basis':basis,'complete_claim':g['claim'],'additional_claim_versions':g.get('additional_claim_versions',[]),'key':g['key']}
assert len(scope_notes)==392
# Preserve old literal vector; propose one narrow, explicit access-language revision separately.
x=next(x for x in F if x['pr']==1263);old=x['row'];new=list(old);a='DOI/version/concept identity authenticated via DataCite; current direct Zenodo endpoints403, so no new deposited-byte/MD5 comparison is claimed.';b='DOI/version/concept identity authenticated via DataCite. Direct Zenodo endpoints returned HTTP403 during the prior source audit; the public native metadata endpoint returned HTTP200 in the dated 22October2026 accounting checks. Those metadata-only checks make no fresh deposited-payload or MD5 comparison claim.';assert new[3].count(a)==1;new[3]=new[3].replace(a,b)
rev={'pr':1263,'original_four_cells':old,'proposed_four_cells':new,'original_sha256':sha(can(old)),'proposed_sha256':sha(can(new)),'exact_replacement':{'old':a,'new':b},'reason':'Qualify the prior403 as route/time-specific after public native metadata returned200; no scientific, authorship, proof or payload-verification expansion.','source_evidence':{'inventory_seal':'11c3a6b59f16f8d2a1d87af3151325f30ca3824a77548b7c5ca15521a4107b4d','metadata_capture':'registry_pr1263_native.json.gz under closed inventory private/','observation_report':'REGISTRY_NATIVE_READS.json'},'root_literal_revision_adopted':False,'fresh_independent_literal_revision_accepted':False,'action_readiness':False};revpin=save('PR1263_EXPLICIT_MINIMAL_LITERAL_REVISION',rev)
items=[]
for x,c in zip(F,contracts):
 assert x['pr']==c['pr'];pr=x['pr'];row=new if pr==1263 else x['row'];leads=[]
 for kind,vals in [('catalog_id',INV[pr]['problem_ids']),('source_id',c['original_source_ids']),('pr_reference',['https://github.com/AlecKriebel/Math/pull/'+str(p)for p in x['associated_prs']]),('selected_C_DOI',[c['selected_C_DOI']]if c['selected_C_DOI']else[]),('same_or_joint_family_alias',c['same_or_joint_result_family_alias_leads_not_blanket_equivalence']),('source_dependency_or_alternative_DOI',c['other_source_or_dependency_or_alternative_DOI_leads']),('registered_title',c['registered_titles']),('author',c['registered_author_names']),('scope_or_name',c['conservative_scope_and_name_terms'])]:
  for v in vals:
   if {'kind':kind,'value':v}not in leads:leads.append({'kind':kind,'value':v})
 if pr in[1263,1265,1276,1294,1296,1345]:leads +=[{'kind':'author','value':v}for v in['Ferudun','Alper Ferudun','Ferudun, Alper']]
 if pr in[1311,1312]:leads.append({'kind':'author','value':'Anonymous'})
 if pr==1292:leads +=[{'kind':'author','value':v}for v in['Ghimire','Dinesh Ghimire']]
 if pr==1310:leads +=[{'kind':'author','value':v}for v in['Wang','Darvas','Peng','Tao']]
 for v in c['registered_author_names']:
  parts=v.split(',',1);variants=[' '.join(p.strip()for p in parts[::-1]),parts[0].strip()]if len(parts)==2 else[v.split()[-1]]
  leads +=[{'kind':'author','value':v}for v in variants if v]
 # Exact canonical source URL leads complement identifiers, including shared report containers.
 for u in re.findall(r'https?://[^\s<>"\\]+',json.dumps(x['row'],ensure_ascii=False)):
  u=u.rstrip('.,;)');u=u.split('#',1)[0].split('?',1)[0]
  if any(v in u for v in['ems.press','problem','erdos','arxiv','hdl.handle','krex','aimath','notebook']):leads.append({'kind':'canonical_source_URL','value':u})
 leads=list({(l['kind'],l['value']):l for l in leads}.values())
 items.append({'pr':pr,'associated_prs':x['associated_prs'],'original_problem_ids':INV[pr]['problem_ids'],'row':row,'original_root_adopted_row':x['row'],'literal_status':'EXPLICIT_MINIMAL_REVISION_PROPOSED_NOT_ADOPTED'if pr==1263 else'ROOT_ADOPTED_EXACT_UNCHANGED','row_sha256':sha(can(row)),'scope_note':INV[pr]['scope_accounting_note'],'original_source_contract':{'root_adoption_path':x['root_adoption_path'],'root_adoption_pin':x['root_adoption_pin'],'proposal_path':x['proposal_path'],'proposal_pin':x['proposal_pin']},'full_root_source_identity_contract':x['root_adoption'],'full_literal_proposal_contract':x['proposal'],'identity_leads':leads,'new_publication':False})
# All old complete conservative leads, plus exact literal-ID and source/author variants, remain present. New standard aliases add leads; they never suppress any.
oldmatrix=gz(D,'terminal_ALL_PAIR_LEAD_MATRIX')['rows'];oldextra=gz(D,'terminal_SUPPLEMENTAL_SOURCE_AUTHOR_LEADS')['rows'];idextra=gz(D,'ADDITIVE_LITERAL_A_CATALOG_ID_MATRIX')['rows'];forced={}
for row in oldmatrix:
 for i,hits,code in row['comparisons']:
  if hits:forced.setdefault((row['pr'],i),[]).extend(hits)
for row in oldextra:
 for i,hits,code in row['leads']:forced.setdefault((row['pr'],i),[]).extend(hits)
for row in idextra:
 for i,yes in row['comparisons']:
  if yes:forced.setdefault((row['pr'],i),[]).extend([['literal_A_catalog_id',v]for v in row['literal_A_derived_problem_ids']])
def matches(body,item):
 text=norm(json.dumps(body,ensure_ascii=False,sort_keys=True));result=[]
 for lead in item['identity_leads']:
  v=norm(lead['value']);kind=lead['kind']
  if kind in ['catalog_id','author']:yes=bool(re.search(r'(?<![a-z0-9])'+re.escape(v)+r'(?![a-z0-9])',text))
  else:yes=v in text
  if yes:result.append([kind,lead['value']])
 return result
sem=[];allpairs=[]
for item in items:
 for i,carrier in enumerate(full):
  hits=forced.get((item['pr'],i),[])+matches(carrier['body'],item);hits=sorted({tuple(v)for v in hits});allpairs.append([item['pr'],i,[list(x)for x in hits]])
  if not hits:continue
  if carrier['key']=='proposal:'+str(item['pr']):classification='SELF_PROPOSAL_EXACT';reason='The exact target proposal itself is not evidence of a prior ledger entry.';witness={'scope':item['scope_note']}
  else:
   gi=carrier_to_group.get(i)
   if carrier['kind']=='proposal':
    other_pr=int(carrier['key'].split(':')[1]);witness={'note':INV[other_pr]['scope_accounting_note'],'basis':'Exact other complete root-adopted proposal and qualified scope; separately pinned original source contract.','complete_claim':json.dumps(carrier['body'],ensure_ascii=False)}
   elif gi is not None:witness=scope_notes[gi]
   else:
    assert carrier['key']=='sheet:237','Unreviewed new carrier cannot use another result scope'
    witness={'note':notes[391],'basis':'Fresh full published1407 scientific claim, plus exact fresh237th ledger row.','complete_claim':json.dumps(carrier['body'],ensure_ascii=False)}
   same=carrier['key']=='native:'+str(item['pr'])or (item['row'][2].startswith('https://doi.org/10.5281/zenodo.')and witness.get('key')=='record:'+item['row'][2].split('.')[-1])
   if same:classification='SAME_SELECTED_EXISTING_PUBLICATION_NOT_LEDGER_COVERAGE';reason='This is the exact already-published source selected by the root contract; it supports recording that existing publication and prohibits new publication. It is not itself a spreadsheet row.'
   else:classification='DISTINCT_SPECIFIC_CARRIER_SCOPE_PROPOSED';reason=witness['note']+' Target has the exact separate scope: '+item['scope_note']
  sem.append({'pr':item['pr'],'carrier_index':i,'carrier_key':carrier['key'],'complete_carrier_sha256':carrier['body_sha256'],'complete_carrier_source':carrier['source'],'matched_leads':[list(v)for v in hits],'target_four_cells':item['row'],'target_four_cells_sha256':item['row_sha256'],'classification':classification,'scientific_reason':reason,'scope_witness':witness,'root_adopted':False,'action_authority':False})
# Every scientific pair is separately considered, not grouped merely by common author.
intra=[]
for a in items:
 for b in items:
  if a['pr']==b['pr']:continue
  hit=matches({'row':b['row'],'source_contract':b['full_root_source_identity_contract']},a)
  intra.append({'pr':a['pr'],'other_pr':b['pr'],'other_four_cells':b['row'],'other_row_sha256':b['row_sha256'],'target_four_cells_sha256':a['row_sha256'],'matched_leads':hit,'classification':'DISTINCT_RESULT_FAMILIES_PROPOSED','scientific_reason':'Other exact result scope: '+b['scope_note']+' Target exact result scope: '+a['scope_note'],'source_identity_evidence':{'target':a['original_source_contract'],'other':b['original_source_contract']},'root_adopted':False,'action_authority':False})
assert len(intra)==1122 and len(allpairs)==34*728
sem_pin=save('SEMANTIC_DECISIONS',{'decisions':sem,'all_pairs':allpairs,'intrabatch':intra,'blanket_author_waivers':False,'all_scope_witnesses':scope_notes,'explicit_old_publication_source_role_never_cleared_as_distinct':True,'root_adopted':False,'fresh_independent_review_accepted':False},True)
car_pin=save('FULL_CARRIER_REFERENCE_INDEX',{'carriers':[{k:v for k,v in x.items()if k!='body'}for x in full],'record_ledger_links':'SHEET_RECORD_READING_LINKS.json','full_body_reference_root':str(D),'full_body_capture_integrity':json.loads((O/'INPUT_BINDINGS.json').read_bytes()),'action_authority':False},True)
plan={'schema_version':'remaining34-preparation01','spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'sheet_title':'Math Puzzles','schema':['Original Problem','Solution Chat URL','DOI','Notes'],'new_rows':34,'associated_PRs':35,'new_publications':0,'items':items,'semantic_packet':sem_pin,'carrier_index':car_pin,'literal_revision':revpin,'scope':'Existing-publication accounting only. No authoring/republication/DOI creation.','excluded_no_row':[{'pr':1224,'status':'GAP_NO_ADOPTED_LITERAL_ROW','row':None}],'excluded_completed':'CF25 rows212–236; B1 rows193–208;14 other reconciled external entries;9 own publications through1407 row237.','preparation_readiness':False,'root_action_accepted':False,'fresh_independent_whole_review':False,'fresh_independent_action_review':False,'unresolved_holds':['PR1263 exact minimal literal revision lacks root and fresh independent adoption.','All new carrier-specific semantic decisions require independent whole review and root adoption; preparation cannot grant this.','Current source/DOI/native/PR/payload roles retain inherited root access and verification limits; every future service effect must obtain fresh exact guards.'],'known_reply_policy':'Exactly spreadsheetId+replies=[{}], optionally commentUpdateState=NO_UPDATES_REQUESTED; all other parsed keys/types contradict; missing/unparseable reply unknown and only GET reconciliation.','native_write_attempt_limit':1,'dated_numeric_observation':'NUMERIC_DATED_OBSERVATION.json','dated_account_basis':'Closed inventory terminal two equal202-record passes at19:13:56UTC22Oct2026, not a current action lock.','action_authority':False}
save('PROPOSAL',plan);print(json.dumps({'items':len(items),'associated_PRs':35,'carrier_pairs':len(allpairs),'semantic_decisions':len(sem),'intrabatch_pairs':len(intra),'literal1263_revision':revpin,'physical_bytes':sum(q.lstat().st_blocks*512 for q in[O,*O.rglob('*')])}))
