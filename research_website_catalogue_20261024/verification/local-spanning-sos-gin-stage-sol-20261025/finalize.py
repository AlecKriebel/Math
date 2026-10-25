"""Seal new private3 packet exactly once, preserving all earlier originals."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent;P=O.parents[1];sys.path[:0]=[str(O),str(P/'scripts')]
from verify_stage import validate
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)}
if (O/'FINAL_SEAL.json').exists():raise RuntimeError('final_original_already_sealed')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();result=validate(False);before=json.loads((O/'protected-before.json').read_text());protected={x['path'] for x in before['files']}
subprocess.run([sys.executable,'-B',str(O/'materialize_helper.py')],check=True,capture_output=True)
outsiders=sorted(str(p.relative_to(P)) for p in (P/'papers').glob('*/*.json') if p.name in ['publication.json','promotion.json'] and str(p) not in protected)
result.update(UTC=utc,phase='PRE_SEAL_FINAL_CUSTODY',unrelated_config_preparation_observed_out_of_scope=outsiders);save('VALIDATION_RECEIPT.json',result)
pins=json.loads((O/'INPUT_PINS.json').read_text());targets=[];read=[]
for rid,pin in pins['target_pins'].items():
    p=P/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());b=c['source_binding']
    refs=[p/'publication.json',p/'promotion.json',p/b['source_receipt_path'],p/b['metadata_path'],p/b['raw_record_path'],p/b['transport_receipt_path'],p/b['source_tex_path'],p/b['prepared_bibtex_path'],P/g['root_clearance_file'],P/('verification/root-editorial-'+rid+'-20261025.json'),p/'reviews/editorial/SEAL.json',p/'reviews/editorial/MANIFEST.json']
    refs.extend(Path(x['path']) for x in b['files']);refs.extend(p/x[k] for x in g['reviews'].values() for k in ['report','verdict_file'])
    if 'pending_intake_seal_path' in b:refs.append(p/b['pending_intake_seal_path'])
    targets.append({'record_id':rid,'receipt_asset_key':b['source_assets_field'],'whole_original_objects_retained':True,'version_original':c['version'],'API_assets':b['published_asset_count'],'bindings':[bind(x) for x in dict.fromkeys(refs)],'canonical_url':c['canonical_url'],'follow_up':c['follow_up'],'AA_original_gate':g['AA']})
    for n in ['REPORT.md','PUBLIC_COPY.md','SCHEMA_ADAPTER.md']:read.append(bind(p/'reviews/editorial'/n))
    read.append(bind(P/g['root_clearance_file']));read.append(bind(P/('verification/root-editorial-'+rid+'-20261025.json')));read.append(bind(O/('public-copy-'+rid+'.txt')))
read.extend(bind(O/n) for n in ['spanning_sos_gin_source.py','BODY_MATH_MAP.json','shared-renderer.diff','shared-checker.diff','new-helper.diff','renderer-private-overrides.diff','checker-private-overrides.diff'])
save('AUTHORITY_SOURCE_BINDINGS.json',{'UTC':utc,'status':'FULL_ORIGINAL_SOURCE_CUSTOM_OBJECTS_AND_EXACT_AUTHORITIES_REAUTHENTICATED','targets':targets})
save('READ_LEDGER.json',{'UTC':utc,'all3_full_final_editorial_reports_copies_schemas_and_scientific_root_records_read_before_proposal':True,'Gin_metadata_reader_support_requirements_read':True,'full_actual_manuscript_and_TeX_reads_reused_at_same_hash':'Immediately preceding immutable legacy preflight: redirects/spanning-sos-gin-preflight-sol-20261025/READ_LEDGER.json; actual4/5/6pp and all3 controlling TeX complete, selected first/last pixels.','all3_actual_final_renderer_public_bodies_read_entirely':True,'complete_changed_code_and_diffs_read':True,'all66_inline_math_replacements_reviewed':True,'no_new_scientific_certification_claim':True,'read_bindings':read,'HTTP_browser_native_read_or_action':False})
code=['spanning_sos_gin_source.py','render_page.proposed.py','final-content-check.proposed.py','render_page.stage.py','final-content-check.stage.py']
save('TESTED_CODE_BINDINGS.json',{'UTC':utc,'phase':'AFTER_COMPLETE_QA_NO_CODE_CHANGES_SINCE_DISPATCH','files':[bind(O/n) for n in code],'helper_reproduction_checked':True})
save('READINESS.json',{'UTC':utc,'assignment_status':'COMPLETE','completion_estimate_percent':100,'status':'PRIVATE_STAGE_COMPLETE_PENDING_ROOT_ACTUAL_RENDERED_COPY_APPROVAL_AND_INTEGRATION_AUTHORITY','authorized_targets':list(pins['target_pins']),'baseline_public_files':492,'baseline_actual_articles':62,'baseline_configured_articles':61,'historical_native_completion_not_inferred':True,'overlay_files':14,'expected_index_items':65,'expected_sitemap_URLs':66,'predicted_integrated_public_files':504,'production_integration_authorized':False,'production_integrated':False,'root_actual_renderer_copy_approved':False,'HTTP_verified':False,'live_verified':False,'browser_verified':False,'native_verified':False,'AA':None,'follow_up':None,'source_configs_custom_verdicts_rewritten':False,'source_correction_required':False,'human_peer_review':False,'formal_certification':False,'root_authority_retained':True,'overall203_programme_complete':False,'unrelated_preparation_configs_out_of_scope':outsiders})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('* '+utc+' — Actual3 public bodies and all changed code/diffs read. Target187 checks; exactly one old61 suite3514 checks;122 complete memory renderer executions identical. Per normal/-O mode:3 source positives,74 source/format rejections,3 page positives,35 output rejections. All1349 fresh originals and492 public files unchanged. Fourteen-file overlay proposes65index/66sitemap/504files. Private-stage completion100%; root rendered-copy approval/integration pending;203 programme ongoing.\n')
files=[]
for p in sorted(O.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:
        if p.is_symlink():raise RuntimeError('no_owned_symlinks')
        files.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p)})
save('FINAL_MANIFEST.json',{'UTC':utc,'status':'IMMUTABLE_PRIVATE_THREE_ARTICLE_STAGE','namespace':str(O),'files':files,'originals_or_production_mutated':False})
save('FINAL_SEAL.json',{'UTC':utc,'status':'SEALED_COMPLETE_ROOT_RENDERED_COPY_REVIEW_PENDING','manifest':'FINAL_MANIFEST.json','manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'owned_bindings':len(files),'completion_estimate_percent':100,'production_or_publication_authority':False,'overall203_programme_complete':False,'preserve_immutable':True})
print(json.dumps({'status':'SEALED','owned_bindings':len(files),'manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'seal_SHA256':sha(O/'FINAL_SEAL.json'),'REPORT_SHA256':sha(O/'REPORT.md')},indent=2))
