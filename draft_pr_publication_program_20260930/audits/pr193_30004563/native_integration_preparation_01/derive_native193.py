"""Inert PR193-specific phase95 renderer: no writes, APIs, Git or mutation.
Root supplies actual verified receipt pins and true fresh MAIN/QUEUE bytes after
DOI/tracker and merge gate. Only returns in-memory bytes for Root adoption.
Phase100 requires a separately pinned actual Root merge-acceptance receipt and
remains a prospective factual postimage until separate actual-main acceptance.
"""
from pathlib import Path
import datetime, hashlib, json, re

HERE=Path(__file__).resolve().parent
CASE=HERE.parent
HEAD='b9a399eeac816dbb8f0e50e81b498c26e5acef81'
NATIVE='unsolved_math_prioritization/attempts/30004563/'
PR_URL='https://github.com/AlecKriebel/Math/pull/193'
CLAIM=('At alpha=16, one fixed admissible incoming realization admits at least five distinct outgoing centers; crossings permitted. '
       'The published <=3 expectation is contradicted in this scope. Proper embeddings excluded; exact total/global maximum unknown; alpha<1 outside. '
       'Old curve family credited to Ash--Bolker (1986), Bourne--Peletier--Roper (2014), Bourne--Roper (2015). '
       'No earlier >=4 pure-power shared-focus witness located in checked corpus through 15 October 2026; historical novelty/firstness unestablished. '
       'Extensive AI; unrefereed; no conventional human peer review.')

# Unchanged pure low-level definitions from accepted191 lifecycle_common.py.
def require(x,msg):
 if not x:raise RuntimeError(msg)
def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def byte_pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

def read_json(path):return json.loads(Path(path).read_bytes())
def assert_pin(data,expected,label):
 actual=byte_pin(data)
 require(isinstance(expected,dict) and actual['sha256']==expected.get('sha256') and actual['bytes']==expected.get('bytes'),label+' bytes/hash mismatch')
 return {k:actual[k] for k in ('bytes','sha256')}
def inside_case(value):
 p=Path(value);p=p if p.is_absolute() else CASE/p
 require(p.resolve().is_relative_to(CASE.resolve()),'Input path outside PR193 case')
 require(not any(q.is_symlink() for q in [p,*p.parents] if q.is_relative_to(CASE)),'Symlink in input path')
 return p
def utc(value):
 require(isinstance(value,str),'UTC timestamp required')
 try:t=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
 except ValueError:raise RuntimeError('Invalid UTC timestamp')
 require(t.utcoffset()==datetime.timedelta(0),'Timestamp is not UTC')
 return t

def authenticated_sources():
 """Read final gate, accepted20 templates and immutable original19 custody."""
 bindings=read_json(HERE/'SOURCE_BINDINGS.json')
 for n,pin in bindings['static_inputs'].items():assert_pin(inside_case(n).read_bytes(),pin,n)
 gate=read_json(CASE/'ROOT_PUBLICATION_GATE.json')
 require(gate['PR']==193 and gate['original_head']==HEAD and gate['publication_ready'] is True,'Wrong/not-ready final Root gate')
 require(gate['mathematical_clearance'] is True and gate['qualified_note_priority_clearance'] is True,'Root scientific clearance missing')
 reviews=gate['whole_package_reviews']
 require(len(reviews)==2 and len({r['reviewer_id'] for r in reviews})==2 and all(r['disposition']=='CLEAN_PASS' for r in reviews),'Final two clean package reviews required')
 for r in reviews:
  for key in ('report','manifest','Root_acceptance'):
   spec=r[key];assert_pin(inside_case(spec['path']).read_bytes(),spec,'Root-bound '+key)
 package=inside_case(gate['package_name'])
 require(set(gate['package_files'])=={q.relative_to(package).as_posix() for q in package.rglob('*') if q.is_file()},'Final package15 inventory mismatch')
 require(len(gate['package_files'])==15 and not any(q.is_symlink() for q in package.rglob('*')),'Final package exact15 nonsymlink files')
 payload={}
 for n,spec in gate['package_files'].items():
  require(not Path(n).is_absolute() and '..' not in Path(n).parts,'Unsafe package member')
  data=(package/n).read_bytes();assert_pin(data,spec,'Final package '+n);payload[n]=data
 auth=read_json(CASE/'ROOT_NATIVE_TEMPLATE_AUTHENTICATION_02.json')
 require(auth['PR']==193 and auth['original_submitted_status_effort']==['claimed_solved','2/5'],'Wrong accepted template provenance')
 require(len(auth['safe_files'])==20,'Accepted native template20 inventory')
 template={}
 for n,spec in auth['safe_files'].items():
  data=inside_case('native_text_preparation_02/'+n).read_bytes();assert_pin(data,spec,'Accepted template '+n);template[n]=data
 original=read_json(CASE/'ORIGINAL_FILE_MANIFEST.json')
 require(original['original_head']==HEAD and original['PR']==193 and len(original['files'])==19,'Original19 custody identity/count')
 baseline={};custody=[]
 for spec in original['files']:
  require(spec['path'].startswith(NATIVE),'Original archive scope')
  rel=spec['path'][len(NATIVE):];require(rel and not Path(rel).is_absolute() and '..' not in Path(rel).parts,'Original relative path')
  data=inside_case('original_submission/files/'+spec['path']).read_bytes();assert_pin(data,spec,'Original custody '+rel)
  require(rel not in baseline,'Duplicate original archive path');baseline[rel]=data;custody.append({'path':spec['path'],**assert_pin(data,spec,rel)})
 require(len(baseline)==19,'Original19 unique custody')
 return gate,payload,template,baseline,custody

def actual_facts(gate,receipt_pins,factual_utc):
 """Only Root's agreed actual receipt files; caller pins come after real actions."""
 actual=read_json(HERE/'ACTUAL_FACT_BINDINGS.json')
 require(receipt_pins==actual['receipts'],'Actual receipt pins differ from Root-provided bindings')
 pub_bytes=(CASE/'ROOT_PUBLICATION_RECEIPT.json').read_bytes()
 tr_bytes=(CASE/'ROOT_TRACKER_RECEIPT.json').read_bytes()
 pub_pin=assert_pin(pub_bytes,receipt_pins['publication'],'Actual Root publication receipt')
 tr_pin=assert_pin(tr_bytes,receipt_pins['tracker'],'Actual Root tracker receipt')
 z=json.loads(pub_bytes);tr=json.loads(tr_bytes)
 gate_sha=byte_pin((CASE/'ROOT_PUBLICATION_GATE.json').read_bytes())['sha256']
 require(z['PR']==193 and z['original_head']==HEAD and z['gate_sha256']==gate_sha,'Publication receipt original HEAD/gate')
 require(z['metadata_exact_verified'] is True and z['environment']=='production' and z['state']=='published','No verified production publication')
 require(re.fullmatch(r'[0-9a-f]{64}',z['kit_sha256']) is not None,'Actual kit SHA256')
 require(str(z['id']).isdigit() and int(z['id'])>0,'Actual record ID')
 require(re.fullmatch(r'10\.5281/zenodo\.[0-9]+',z['doi']) is not None,'Actual Zenodo DOI')
 require(z['doi_url']=='https://doi.org/'+z['doi'],'Actual DOI URL')
 require(z['record_url'] in ['https://zenodo.org/records/'+str(z['id']),'https://zenodo.org/record/'+str(z['id'])],'Actual record URL')
 require(z['receipt_saved'] is True and z['doi_resolution']['status']=='resolved' and z['doi_resolution']['http_status']==200 and z['doi_resolution']['url']==z['doi_url'],'Actual saved DOI HTTP200 resolution required')
 inspect_spec=actual['published_inspect'];inspect_bytes=inside_case(inspect_spec['path']).read_bytes();assert_pin(inspect_bytes,inspect_spec,'Root fresh published inspect')
 inspect=json.loads(inspect_bytes)
 require(inspect['id']==z['id'] and inspect['doi']==z['doi'] and inspect['state']=='published' and inspect['metadata_exact_verified'] is True and inspect['files']==z['files'],'Fresh published inspect identity/files/metadata')
 manifest=z['manifest'];assert_pin(inside_case(manifest['path']).read_bytes(),manifest,'Root actual kit manifest')
 expected={n:(gate['package_files'][n]['bytes'],gate['package_files'][n]['sha256']) for n in ('five_centers.pdf','five_centers.tex','verification-package.zip')}
 files=z['files'];require(len(files)==3 and len({f['name'] for f in files})==3,'Published exact three files')
 require({f['name']:(f['size'],f['sha256']) for f in files}==expected,'Published files differ from final gate')
 require(tr['PR']==193 and tr['gate_sha256']==gate_sha and tr['doi']==z['doi'],'Tracker identity/gate/DOI')
 require(tr['append_performed'] is True and tr['own_row_readback_verified'] is True and tr['foreign_rows_retained'] is True,'Tracker actual append/readback/preservation')
 require(isinstance(tr['spreadsheet_id'],str) and bool(tr['spreadsheet_id']),'Tracker spreadsheet ID')
 require(tr['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and tr['gid']==1254632077 and tr['tab']=='Math Puzzles','Actual tracker identity')
 require(tr['header']==['Original Problem','Solution Chat URL','DOI','Notes'] and isinstance(tr['values'],list) and len(tr['values'])==1 and isinstance(tr['values'][0],list) and len(tr['values'][0])==4,'Actual tracker exact1x4 shape/header')
 cells=tr['values'][0];require(all(isinstance(s,str) for s in cells),'Exact tracker four-cell strings')
 require(cells[2]==z['doi_url'] and tr['actual_fresh_reads']==2 and tr['range']==actual['tracker_range'],'Actual tracker DOI/two-read/range mismatch')
 require(re.fullmatch(r"(?:'[^']+'|[^'!]+)!A([1-9][0-9]*):D\1",tr['range']) is not None,'Tracker exact own four-cell range')
 stamp=utc(factual_utc)
 require(stamp>=utc(z['verified_utc']) and stamp>=utc(z['UTC']) and stamp>=utc(tr['UTC']),'Native factual stamp precedes actual receipts')
 return z,tr,{'publication':pub_pin,'tracker':tr_pin},gate_sha

def queue_postimage(before,doi,doi_url):
 """Accepted191 row replacement mechanism adapted to193 and fresh-parent proof."""
 require(isinstance(before,bytes),'Fresh QUEUE bytes required')
 text=before.decode('utf-8')
 rows=[line for line in text.splitlines() if '| 30004563 /' in line]
 require(len(rows)==1,'Fresh target QUEUE identity/count')
 row=rows[0];cells=row.split('|');require(len(cells)==14,'Fresh QUEUE schema')
 require('30004563 / OWR-2654831-006' in cells[2],'Wrong target catalogue row')
 changed=list(cells)
 changed[8]=' claimed_solved ';changed[9]=' 2/5 ';changed[10]=' '+PR_URL+' '
 changed[11]=' '+CLAIM+' ';changed[12]=' ['+doi+']('+doi_url+') '
 require(all(cells[i]==changed[i] for i in range(14) if i not in (8,9,10,11,12)),'Non-owned target cell changed')
 after=text.replace(row,'|'.join(changed)).encode('utf-8')
 old_lines,new_lines=before.splitlines(keepends=True),after.splitlines(keepends=True)
 require(len(old_lines)==len(new_lines) and sum(a!=b for a,b in zip(old_lines,new_lines))==1,'Foreign QUEUE row/bytes delta')
 return after,{'before_status':cells[8].strip(),'before_effort':cells[9].strip(),'after_status':'claimed_solved','after_effort':'2/5','owned_cell_slots':[8,9,10,11,12],'all_other_target_cells_and_foreign_rows_exact':True}

def split_body(raw):
 text=raw.decode();require(text.startswith('> INERT PROPOSED TEXT:'),'Expected accepted preparation banner')
 return text.split('\n\n',1)[1]

def derive_phase95(*,receipt_pins,fresh_main,factual_utc):
 """Pure in-memory derivation; Root supplies fresh MAIN data after actual gates.
fresh_main={branch:'main',commit:<40hex>,QUEUE:<bytes>,QUEUE_pin:{bytes,sha256},
            verified_utc:<UTC>,merge_gate_authorized:True}
No actual external pins or parent values are embedded in this source.
"""
 gate,payload,tpl,files,custody=authenticated_sources()
 z,tr,receipts,gate_sha=actual_facts(gate,receipt_pins,factual_utc)
 require(fresh_main['branch']=='main' and re.fullmatch(r'[0-9a-f]{40}',fresh_main['commit']) is not None,'Fresh MAIN branch/parent identity')
 require(fresh_main['merge_gate_authorized'] is True,'Root actual merge gate not supplied')
 require(utc(fresh_main['verified_utc'])>=utc(tr['UTC']) and utc(factual_utc)>=utc(fresh_main['verified_utc']),'Fresh MAIN snapshot must follow tracker verification')
 queue_pin=assert_pin(fresh_main['QUEUE'],fresh_main['QUEUE_pin'],'True fresh MAIN QUEUE preimage')
 queue,queue_change=queue_postimage(fresh_main['QUEUE'],z['doi'],z['doi_url'])
 facts={'UTC':factual_utc,'PR':193,'problem_id':30004563,'original_head':HEAD,'status':'ACTUAL_PUBLISHED_TRACKED_MERGE_AND_FACTUAL_ACCEPTANCE_PENDING','case_percent':95,'publication_ready':True,'whole_package_reviews_complete':True,'completed_new_whole_package_reviews':2,'actual_Zenodo_published':True,'DOI':z['doi'],'DOI_URL':z['doi_url'],'actual_tracker_updated':True,'tracker_range':tr['range'],'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'goal_complete':False,'programme_counters_unchanged_until_actual_factual_acceptance':{'fully_completed_count':40,'published_count':24},'proposed_integrated_queue_status':'claimed_solved','proposed_integrated_effort':'2/5','fresh_MAIN_parent':fresh_main['commit'],'fresh_QUEUE_preimage':queue_pin,'gate_sha256':gate_sha,'receipt_pins':receipts,'scope':CLAIM}
 sentence=('The two NEW whole-package adversaries completed clean and Root authenticated the final exact package. '
           'The note is actually published at '+z['doi_url']+'; tracker row '+tr['range']+' was appended and its own-row readback verified, with foreign rows retained. '
           'Original-HEAD merge and separate actual-main factual acceptance remain pending. This snapshot is 95%; programme40/24 remains unchanged until actual factual acceptance.')
 oldproof=split_body(tpl['native/CURRENT_PROOF.md'])
 core=oldproof.split('## Theorem and precise scope',1)[1].split('## Verification, geometry and attribution',1)[0]
 tail=oldproof.split('The verified boxes exclude',1)[1].split('Final accepted package:',1)[0]
 proof=('# Five outgoing centers in a 16-realization cube move\n\nAlec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · Unrefereed research note\n\n'
        'This is the current proof entrypoint. The final published scientific package is '+gate['package_name']+'; its exact15 source files are retained under publication/. Original CANDIDATE.md, original checker/certificate and original review remain historical prepublication 10^17 evidence. This current presentation uses 10^16 with the analytic endpoint below.\n\n'
        '## Theorem and precise scope'+core+'## Verification, geometry and attribution\n\n'
        'Run python3 publication/verify_five_centers.py. The final support verifier and exact certificate are present under publication/ and match Root\'s final gate. Default verification recomputes and compares without writing. It uses standard-library integer/Fraction decisions, checked 10^-36 eighth-root bounds, 128 boundary bisections and 100 sign-preserving outgoing bisections. It derives from the algebra/analysis audit implementation and is not a newly independent code implementation. Original independent audit records remain separately labeled historical evidence.\n\n'
        'The verified boxes exclude'+tail+sentence+'\n')
 files['CURRENT_PROOF.md']=proof.encode()
 files['README.md']=('''# Five outgoing centers in a 16-realization cube move

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

'''+CLAIM+'\n\n'+sentence+'''

The current proof is [CURRENT_PROOF.md](CURRENT_PROOF.md); exact final manuscript, verifier, certificate and support are in [publication/README.md](publication/README.md). Run python3 publication/verify_five_centers.py; it recomputes and compares certificates without writing by default. The final endpoint is 10^16 with an analytic concavity bound. The publication verifier derives from the algebra/analysis audit implementation; no new code-independence claim is made.

Original CANDIDATE.md, certify_five_centers.py, turn2_exact_certificate.json, original review and original research log are historical prepublication 10^17 evidence with contemporaneous status labels. Their original19 bytes remain in the immutable audit archive authenticated by ORIGINAL_SUBMISSION_CUSTODY.json. Contemporaneous planning flags in frozen publication support files are historical snapshots; current verified review/publication/tracker facts are in PUBLICATION.json.

Original submitted HEAD records claimed_solved and 2/5 recovered author turns; earlier historical effort is unknown. The queue postimage restores those original values at gated integration and retains them through publication. Status, effort, PR/reference, claim/findings and DOI are the only owned cells. Every other target field and foreign row is exact from the fresh parent.

The older curve family is credited in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). Historical priority, firstness and independent awareness remain unestablished. AI was used extensively; unrefereed; no conventional human peer review. The note and original support use CC BY 4.0; primary-source PDFs/derivatives are excluded and third-party rights unchanged.

Original-HEAD merge and factual100 are not claimed here. Any factual100 update requires separate actual-main acceptance after the real merge.
''').encode()
 oldsource=split_body(tpl['native/SOURCE_AUDIT.md'])
 source=oldsource.split('## Verification and review provenance',1)[0]+'''## Verification, review and actual publication provenance

Original 10^17 proof/checker/certificate/review remain historical prepublication evidence. Current publication presentation uses 10^16 with the analytic concavity bound. Its verifier derives from the algebra/analysis audit implementation, not an additional independent implementation. Root authenticated three mathematical audit families and two clean NEW whole-package adversaries against the same exact final15 package.

'''+sentence+'''

AI assistance was extensive in exploration, drafting, code generation and adversarial checks. Unrefereed; no conventional human peer review. No external individual was contacted or outreach prepared. Primary-source PDFs and derivatives are excluded. Precise actual receipt bindings and final package hashes are in PUBLICATION.json.
'''
 files['SOURCE_AUDIT.md']=source.encode()
 sm=json.loads(tpl['native/source_manifest.json'])
 for key in ('template_mode','final_package'):sm.pop(key,None)
 sm.update(current_status=facts['status'],publication_gate_sha256=gate_sha,actual_DOI=z['doi'],actual_published=True,actual_tracker_range=tr['range'],whole_package_reviews_complete=True,actual_original_PR_merged=False,case_percent=95,final_package=gate['package_name'])
 files['source_manifest.json']=encoded(sm)
 files['readiness.json']=encoded({**facts,'current_proof':'CURRENT_PROOF.md','publication_assets':'publication/','original_dataset_provenance':{k:sm[k] for k in ('dataset','revision','review_hash','statement_hash')},'historical_review_not_final_package_review':True,'code_provenance':'Publication verifier derives from algebra_analysis_audit_01; not newly independent code.','AI_and_review':'Extensive AI; unrefereed; no conventional human peer review.','original19_custody':'ORIGINAL_SUBMISSION_CUSTODY.json','remaining_required':'Actual original-HEAD merge, then separate actual-main factual acceptance; no factual100.'})
 files['continuity.json']=encoded({**facts,'historical_turns_used':None,'historical_count_status':'unknown, not reset to zero','historical_partial_artifacts_available':False,'recovered_substantive_turns_used':2,'recovered_turn_limit':5,'original_submitted_status':'claimed_solved','original_effort':'2/5','historical_candidate':'CANDIDATE.md (10^17)','current_proof':'CURRENT_PROOF.md (10^16 publication presentation)','remaining_required':'Actual original-HEAD merge and separate actual-main factual acceptance.'})
 public={**facts,'title':'Five outgoing centers in a 16-realization cube move','record_url':z['record_url'],'environment':z['environment'],'record_id':z['id'],'publication_verified_utc':z['verified_utc'],'files':z['files'],'kit_sha256':z['kit_sha256'],'metadata_exact_verified':z['metadata_exact_verified'],'metadata_normalizations':z.get('metadata_normalizations'),'kit_manifest_pin':{k:z['manifest'][k] for k in ('bytes','sha256')},'tracker':{k:tr[k] for k in ('spreadsheet_id','range','header','values','append_performed','own_row_readback_verified','foreign_rows_retained')},'final_package_files':gate['package_files'],'whole_package_review_root_acceptances':[r['Root_acceptance'] for r in gate['whole_package_reviews']]}
 files['PUBLICATION.json']=encoded(public)
 files['FINAL_DISPOSITION.md']=('# Final disposition for 30004563\n\n'+CLAIM+'\n\n'+sentence+'\n\nOriginal submitted HEAD: '+HEAD+'. Original claimed_solved / 2/5 is restored in the proposed integrated queue row; earlier historical effort unknown. Fresh parent: '+fresh_main['commit']+'. Its target preimage was '+queue_change['before_status']+' / '+queue_change['before_effort']+'. Only cells8--12 change; every foreign row and other target field remains fresh-parent exact.\n\nActual facts are in PUBLICATION.json. Original-HEAD merge and factual100 remain pending; a factual100 record must be derived separately after real merge and accepted against actual MAIN. This helper provides no such phase.\n').encode()
 files['RESEARCH_LOG.md']=files['RESEARCH_LOG.md']+('\n## '+factual_utc+' — actual publication/tracker snapshot, 95% workflow\n\n'+sentence+'\n\n'+CLAIM+' Original effort2/5 retained; earlier historical effort unknown. Original19 custody unchanged. Actual original-HEAD merge and separate factual-main acceptance remain required.\n').encode()
 files['ORIGINAL_SUBMISSION_CUSTODY.json']=encoded({'original_head':HEAD,'archive_case_relative':'original_submission/files/'+NATIVE,'files':custody,'count':19,'immutable_original_bytes_verified':True,'native_historical_paths_retained':['CANDIDATE.md','certify_five_centers.py','turn2_exact_certificate.json','review/'],'current_metadata_changes_do_not_rewrite_archive':True})
 for n,data in payload.items():files['publication/'+n]=data
 oldfreeze=json.loads(tpl['native/frozen_artifacts.json'])['immutable_original_freeze_record']
 files['frozen_artifacts.json']=encoded({'UTC':factual_utc,'status':facts['status'],'case_percent':95,'immutable_original_freeze_record':oldfreeze,'current_native_files':{n:byte_pin(data) for n,data in sorted(files.items()) if n!='frozen_artifacts.json'},'self_hash_excluded':True,'actual_DOI':z['doi'],'actual_tracker_range':tr['range'],'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'final_package_gate_sha256':gate_sha,'receipt_pins':receipts})
 for n in ('CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md','readiness.json','continuity.json','source_manifest.json','FINAL_DISPOSITION.md','PUBLICATION.json','frozen_artifacts.json'):
  text=files[n].decode()
  require('UNRESOLVED' not in text and 'INERT PROPOSED' not in text and 'template_mode' not in text,'Preparation narrative remains in '+n)
  require('At v1 preparation time' not in text and 'adversary is active' not in text,'Obsolete review narrative '+n)
 _,_,_,_,custody_after=authenticated_sources();require(custody_after==custody,'Original19 custody changed during derivation')
 pr_body=CLAIM+'\n\n'+sentence+'\n\nCurrent proof: '+NATIVE+'CURRENT_PROOF.md. Original 10^17 evidence remains historical; current publication support uses 10^16 and an analytic endpoint. Publication verifier derives from algebra/analysis audit code.\n\nOnly target status/effort/PR/claim/DOI cells change against true fresh parent; other target fields and all foreign rows remain exact. Original submitted HEAD '+HEAD+'. Actual merge and factual acceptance remain pending.\n'
 return {'phase':95,'original_head':HEAD,'facts':facts,'native_files':{NATIVE+n:data for n,data in files.items()},'native_inventory':{NATIVE+n:byte_pin(data) for n,data in sorted(files.items())},'QUEUE_postimage':queue,'QUEUE_change_proof':queue_change,'fresh_MAIN_parent':fresh_main['commit'],'PR_title':tpl['PR_TITLE.txt'].decode().strip(),'PR_body':pr_body,'no_mutation_performed':True,'factual_sentence':sentence,'factual100':'Separate pinned actual merge acceptance and actual-main acceptance required'}



def derive_phase100(*,phase95,merge_acceptance,factual_utc):
 """Pure separate factual postimage after an actual Root-accepted phase95 merge.
merge_acceptance={receipt_bytes:<Root-issued JSON bytes>,receipt_pin:{bytes,sha256}}
The actual100 MAIN acceptance is still separate; this function writes nothing.
"""
 require(phase95['phase']==95 and phase95['original_head']==HEAD,'Use exact phase95 derivation')
 for n,b in phase95['native_files'].items():require(byte_pin(b)==phase95['native_inventory'][n],'Phase95 native inventory drift')
 require(set(merge_acceptance)=={'receipt_bytes','receipt_pin'},'Pinned actual merge acceptance required')
 raw=merge_acceptance['receipt_bytes'];require(isinstance(raw,bytes),'Actual receipt bytes required')
 merge_pin=assert_pin(raw,merge_acceptance['receipt_pin'],'Root actual merge acceptance');m=json.loads(raw)
 require(m['PR']==193 and m['original_head']==HEAD and m['accepted'] is True,'Not actual accepted original-HEAD merge')
 require(re.fullmatch(r'[0-9a-f]{40}',m['merge_commit']) is not None,'Actual merge commit identity')
 require(m['parents']==[phase95['fresh_MAIN_parent'],HEAD],'Actual merge true-parent/original-HEAD mismatch')
 f95=phase95['facts']
 require(m['DOI']==f95['DOI'] and m['tracker_range']==f95['tracker_range'] and m['gate_sha256']==f95['gate_sha256'],'Actual merge receipt DOI/tracker/gate mismatch')
 require(utc(m['UTC'])>=utc(f95['UTC']) and utc(factual_utc)>=utc(m['UTC']),'Factual100 time precedes actual merge acceptance')
 authenticated_sources() # Recheck immutable original19, accepted20 and exact final15.
 files=dict(phase95['native_files']);prefix=NATIVE
 updates={'UTC':factual_utc,'status':'FACTUAL100_POSTIMAGE_REQUIRES_SEPARATE_ACTUAL_MAIN_ACCEPTANCE','case_percent':100,'actual_original_PR_merged':True,'actual_merge_commit':m['merge_commit'],'actual_merge_acceptance_receipt_pin':merge_pin,'actual_factual_MAIN_accepted':False,'completed':False,'goal_complete':False,'factual_postimage_programme_counts':{'fully_completed_count':41,'published_count':25},'factual_postimage_not_adopted_until_actual_MAIN_acceptance':True}
 facts={**f95,**updates};facts.pop('programme_counters_unchanged_until_actual_factual_acceptance',None)
 new_sentence=('The two NEW whole-package adversaries completed clean and Root authenticated the final exact package. The note is actually published at '+f95['DOI_URL']+'; tracker row '+f95['tracker_range']+' was appended/read back with foreign rows retained. Original-HEAD merge '+m['merge_commit']+' was actually accepted by Root. This is a factual100 postimage with prospective programme41/25; its separate actual-main factual acceptance remains required and is not asserted here.')
 old_sentence=phase95['factual_sentence']
 for rel in ('CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md'):
  text=files[prefix+rel].decode();require(text.count(old_sentence)==1,'Unique phase95 current sentence required '+rel)
  text=text.replace(old_sentence,new_sentence)
  if rel=='README.md':
   old='Original-HEAD merge and factual100 are not claimed here. Any factual100 update requires separate actual-main acceptance after the real merge.'
   require(text.count(old)==1,'Unique phase95 README closing narrative')
   text=text.replace(old,'Original-HEAD merge was actually accepted. This factual100 postimage still requires separate actual-main factual acceptance; the helper does not assert that later acceptance.')
  files[prefix+rel]=text.encode()
 files[prefix+'FINAL_DISPOSITION.md']=('# Final disposition for 30004563\n\n'+CLAIM+'\n\n'+new_sentence+'\n\nOriginal submitted HEAD: '+HEAD+'. Actual accepted merge: '+m['merge_commit']+'. Integrated queue remains claimed_solved / 2/5. Original19 and all scientific/publication bytes remain unchanged from the accepted95 derivation. This is a separately derived factual100 postimage; actual MAIN adoption must still be authenticated independently.\n').replace('\n','\n').encode()
 for rel in ('readiness.json','continuity.json','source_manifest.json','PUBLICATION.json'):
  j=json.loads(files[prefix+rel]);j.update(updates);j.pop('programme_counters_unchanged_until_actual_factual_acceptance',None)
  if 'remaining_required' in j:j['remaining_required']='Separate actual-main factual acceptance of this100 postimage; actual merge already accepted.'
  files[prefix+rel]=encoded(j)
 files[prefix+'RESEARCH_LOG.md']+=('\n## '+factual_utc+' — factual100 postimage after actual merge acceptance\n\n'+new_sentence+' Original submitted effort2/5 and earlier unknown history retained. No source/science/original19 bytes changed.\n').replace('\n','\n').encode()
 oldfreeze=json.loads(files[prefix+'frozen_artifacts.json'])
 oldfreeze.update(updates);oldfreeze.pop('programme_counters_unchanged_until_actual_factual_acceptance',None)
 oldfreeze['current_native_files']={n[len(prefix):]:byte_pin(b) for n,b in sorted(files.items()) if n!=prefix+'frozen_artifacts.json'}
 files[prefix+'frozen_artifacts.json']=encoded(oldfreeze)
 allowed={prefix+n for n in ('CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md','FINAL_DISPOSITION.md','readiness.json','continuity.json','source_manifest.json','PUBLICATION.json','RESEARCH_LOG.md','frozen_artifacts.json')}
 require(set(files)==set(phase95['native_files']),'Factual100 inventory changed')
 require(all(files[n]==b for n,b in phase95['native_files'].items() if n not in allowed),'Science/support/original bytes changed')
 # The mathematical theorem/proof block remains byte-identical even within current prose.
 def core(b):return b.split(b'## Theorem and precise scope',1)[1].split(b'## Verification, geometry and attribution',1)[0]
 require(core(files[prefix+'CURRENT_PROOF.md'])==core(phase95['native_files'][prefix+'CURRENT_PROOF.md']),'Mathematical proof changed')
 pr_body=CLAIM+'\n\n'+new_sentence+'\n\nCurrent proof: '+NATIVE+'CURRENT_PROOF.md. Original 10^17 evidence remains historical; final publication support uses 10^16 with the analytic endpoint. Publication verifier derives from the algebra/analysis audit implementation. Original-HEAD merge '+m['merge_commit']+' was actually accepted; the separately derived factual100 postimage still requires actual-main factual acceptance. No actual factual acceptance is claimed by this metadata.\n'
 return {'phase':100,'original_head':HEAD,'facts':facts,'native_files':files,'native_inventory':{n:byte_pin(b) for n,b in sorted(files.items())},'actual_merge_commit':m['merge_commit'],'merge_acceptance_receipt_pin':merge_pin,'factual_sentence':new_sentence,'PR_title':phase95['PR_title'],'PR_body':pr_body,'QUEUE_unchanged_from_actual_main_required':True,'no_mutation_performed':True,'actual_factual_MAIN_accepted':False}
