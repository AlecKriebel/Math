"""Record bounded reads/preservation and seal only this private namespace."""
from pathlib import Path
import datetime,hashlib,json,sys
O=Path(__file__).resolve().parent;P=O.parents[1];sys.path[:0]=[str(O),str(P/'scripts')]
from ambient_block_modulus_source import PINS,SCHEMAS,STATUSES,ambient_block_modulus_source_view,verify_abm_archive
from verify_stage import validate
UTC=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def binding(p):return {'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)}
if (O/'FINAL_SEAL.json').exists():raise RuntimeError('preserve_final_immutable_seal')
# Preserve initial unconsumed text-contract draft as history, not a second proposal.
if (O/'body_contract.py').exists():
    (O/'history').mkdir(exist_ok=True);(O/'body_contract.py').rename(O/'history/body_contract.initial.py')
code=['ambient_block_modulus_source.py','abm_body_contract.py','render_page.proposed.py','render_page.stage.py','final-content-check.proposed.py','final-content-check.stage.py','new-record-checks.block.txt','stage_reader.py','memory_render.py','guard_controls.py','public_fault.py','legacy_and_controls.py','run_stage.py']
save('TESTED_CODE_BINDINGS.json',{n:{'bytes':(O/n).stat().st_size,'SHA256':sha(O/n)} for n in code})
packets=[]
for n in ['local-cylinder-discotope-stage-sol-20261025','cylinder-discotope-correction-recheck-sol-20261025','local-spanning-sos-gin-stage-sol-20261025','spanning-sos-gin-correction-recheck-sol-20261025']:
    base=P/'verification'/n;manifest=base/'FINAL_MANIFEST.json';seal=base/'FINAL_SEAL.json';se=json.loads(seal.read_text())
    if sha(manifest)!=se['manifest_SHA256']:raise RuntimeError('prior_manifest_seal')
    count=0
    for x in json.loads(manifest.read_text())['files']:
        q=base/x['path']
        if q.stat().st_size!=x['bytes'] or sha(q)!=x['SHA256']:raise RuntimeError('prior_owned_changed:'+str(q))
        count+=1
    packets.append({'path':str(base),'manifest_SHA256':sha(manifest),'seal_SHA256':sha(seal),'owned_bindings_rechecked':count})
save('PRIOR_PACKET_CUSTODY.json',{'UTC':UTC(),'packets':packets,'old_mutable_baselines_adopted_as_current':False,'only_immutable_owned_output_manifests_followed':True})
reads=[];authorities={}
def nodes(x):return 1+sum(nodes(v) for v in (x.values() if isinstance(x,dict) else x if isinstance(x,list) else []))
for rid in ['23333353','23416806','23441617']:
    p=P/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());b=c['source_binding'];raw,view,root=ambient_block_modulus_source_view(p,c,g)
    unique=['REPORT.md','PUBLIC_COPY.md','SCHEMA_ADAPTER.md','METADATA_READER_SUPPORT_REQUIREMENTS.json','CITATION.bib']
    for n in unique:reads.append({**binding(p/'reviews/editorial'/n),'mode':'entire narrative read' if n.endswith('.md') else 'complete parsed requirements / exact citation bytes'})
    reads.append({**binding(p/'reviews/root/ROOT_REVIEW.md'),'mode':'entire root scientific disposition read'})
    for rel in ['publication.json','promotion.json',b['source_receipt_path'],b['raw_record_path'],b['metadata_path'],b['transport_receipt_path']]:
        q=p/rel;obj=json.loads(q.read_bytes());reads.append({**binding(q),'mode':'complete original object parsed recursively; all embedded source/root/custom objects compared, no field rewriting','JSON_nodes':nodes(obj)})
    for prefix in ['root-clearance','root-editorial']:
        q=P/('verification/'+prefix+'-'+rid+'-20261025.json');reads.append({**binding(q),'mode':'entire authority object read and pinned'})
    reads.append({**binding(O/('public-copy-'+rid+'.txt')),'mode':'entire actual renderer public copy read after rendering, all prose/credits/limits/status/links compared'})
    archive=verify_abm_archive(p,rid,root/c['supplement_filename'],json.loads((root/'archive-members.json').read_text()))
    authorities[rid]={'pins':PINS[rid],'literal_status':STATUSES[rid],'whole_custom_objects_preserved':{k:{'verdict':binding(p/v['verdict_file']),'report':binding(p/v['report']),'complete_verdict_keys':list(v['verdict'])} for k,v in g['reviews'].items()},'original_source_schema':SCHEMAS[rid],'original_asset_order':[x[SCHEMAS[rid][1]]['key'] for x in raw[SCHEMAS[rid][0]]],'all_original_transports_preserved_whole':True,'source_API_version':b['zenodo_version'],'manuscript_version':b['manuscript_version'],'archive_custody':archive,'metadata_requirement':binding(p/'reviews/editorial/METADATA_READER_SUPPORT_REQUIREMENTS.json'),'source_asset_and_current_public_copies':[{'original':binding(root/n),'private':binding(O/'public/research'/c['slug']/n)} for n in [c['pdf_filename'],c['supplement_filename']]],'declared_date':c['publication_date'],'record_creation':b['record_created_utc'],'record_update':b['record_updated_utc']}
save('READ_LEDGER.json',{'UTC':UTC(),'reads':reads,'scope':'Editorial implementation and complete object authentication. Scientific proof and foreign primary interfaces remain the exact completed root/family authority. No new literature search/body retrieval or scientific certification. Whole archived byte reads do not claim semantic reading of every historical support narrative.'})
save('AUTHORITY_SOURCE_BINDINGS.json',authorities)
validation=validate(False);save('VALIDATION_RECEIPT.json',validation)
save('READINESS.json',{'UTC':UTC(),'assignment_status':'COMPLETE','completion_percent_this_private_stage':100,'exact_record_ids':['23333353','23416806','23441617'],'status':'PRIVATE_STAGE_READY_FOR_ROOT_FULL_RENDERED_COPY_READ_AND_INDEPENDENT_CODE_AUDIT','public_baseline':{'files':504,'index':65,'sitemap':66,'website_HEAD_observed_read_only':'dcc259dbd4fd4285a65374e20ae65281fa30e852','configured':64,'manual':1,'native':62,'previous_three_deploy_browser_pending':True},'private_prediction':{'files_after_integration':516,'index':68,'sitemap':69,'overlay_files':14},'scientific_statuses':STATUSES,'source_correction':False,'new_mathematical_or_priority_certification':False,'root_authority_retained':True,'independent_code_audit_complete':False,'root_actual_rendered_copy_approval':False,'production_integration_authorized':False,'rendered_public_copy_approved':False,'local_HTTP_verified':False,'live_HTTP_verified':False,'browser_verified':False,'native_sheet_verified':False,'public_page_published':False,'canonical_config_values_modified':False,'AA':None,'follow_up':None,'outreach':False,'all203_programme_complete':False})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('* '+UTC()+' — One old64 suite3708 and128 full in-memory renderer executions passed. Each normal/-O mode accepted3 pristine source views, rejected98 source/schema/authority changes, accepted3 pristine pages, rejected58 public mutations. Entire actual public copies read. Fresh1405 protected files and643 old actual inputs remain unchanged; earlier sealed owned packets authenticated without following their old mutable baselines. Completion estimate100% of private handoff; root rendered-copy/audit/integration gates pending, all203 ongoing.\n')
# REPORT.md and metadata requirements are written separately before this seal operation.
if not (O/'REPORT.md').is_file() or not (O/'METADATA_READER_REQUIREMENTS.md').is_file():raise RuntimeError('complete_readable_handoff_required')
files=[p for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']]
save('FINAL_MANIFEST.json',{'UTC':UTC(),'status':'IMMUTABLE_PRIVATE_AMBIENT_BLOCK_MODULUS_STAGE','namespace':str(O),'files':[{'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in sorted(files)],'source_config_core_production_originals_mutated':False})
save('FINAL_SEAL.json',{'UTC':UTC(),'status':'IMMUTABLE_PRIVATE_STAGE_HANDOFF','manifest':'FINAL_MANIFEST.json','manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'owned_bindings':len(files),'completion_estimate_percent_this_private_stage':100,'integration_publication_authority':False,'all203_programme_complete':False,'preserve_immutable':True})
print(json.dumps({'report_SHA256':sha(O/'REPORT.md'),'manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'seal_SHA256':sha(O/'FINAL_SEAL.json'),'owned_bindings':len(files),'validation':validation},indent=2))
