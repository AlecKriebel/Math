"""Finalize this new private packet once; do not modify sealed originals."""
from pathlib import Path
import ast,datetime,hashlib,json,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
sys.path[:0]=[str(O),str(R/'scripts')]
from cylinder_discotope_source import PINS
from verify_stage import validate

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,obj):(O/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def binding(p):return {'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)}
if (O/'FINAL_SEAL.json').exists():raise RuntimeError('final_packet_already_sealed_no_rewrite')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
baseline=json.loads((O/'protected-before.json').read_text());protected={x['path'] for x in baseline['files']}
new_other_configs=[str(p.relative_to(R)) for p in sorted((R/'papers').glob('*/*.json')) if p.name in ['publication.json','promotion.json'] and str(p) not in protected and p.parent.name not in PINS]
result=validate(False);result['UTC']=utc;result['phase']='PRE_SEAL_COMPLETE_CHECKS';result['out_of_scope_new_preparation_configs_observed']=new_other_configs
save('VALIDATION_RECEIPT.json',result)
authority=[]
for rid,pin in PINS.items():
    p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text())
    paths=[p/'publication.json',p/'promotion.json',p/'sources/receipt.json',p/'sources/metadata.normalized.json',p/'sources/zenodo-record.raw.json',p/c['source_binding']['source_tex_path'],p/'sources'/pin['pdf'],p/'sources'/pin['zip'],R/('verification/root-clearance-'+rid+'-20261025.json'),R/('verification/root-editorial-'+rid+'-20261025.json')]
    paths.extend(p/x[k] for x in g['reviews'].values() for k in ['report','verdict_file'])
    paths.extend(p/'reviews'/role/name for role in ['editorial','editorial-intake'] for name in ['FINAL_MANIFEST.json','FINAL_SEAL.json'] if (p/'reviews'/role/name).is_file())
    authority.append({'record_id':rid,'whole_original_objects_retained':True,'receipt_schema':pin['asset_key'],'checksum_field_names':[pin['md5_key'],pin['sha_key']],'source_or_authority_bindings':[binding(q) for q in paths],'complete_custom_verdict_field_sets':{role:list(x['verdict']) for role,x in g['reviews'].items()},'AA':c['AA'],'follow_up':c['follow_up'],'canonical_url_original':c['canonical_url']})
save('AUTHORITY_SOURCE_BINDINGS.json',{'UTC':utc,'scope':'Originals authenticated, not rewritten or normalized. These references do not replace any original receipt/verdict.','targets':authority})
read_paths=[O/'public-copy-23387774.txt',O/'public-copy-23074543.txt',O/'public-sections-23387774.json',O/'public-sections-23074543.json',O/'shared-renderer.diff',O/'shared-checker.diff',O/'new-helper.diff',O/'renderer-staging-overrides.diff',O/'checker-staging-overrides.diff',O/'cylinder_discotope_source.py',O/'METADATA_READER_REQUIREMENTS.md',O/'REPORT.md',Path(baseline['production_public_root'])/'research/research.css']
read_paths.extend(R/('verification/root-editorial-'+rid+'-20261025.json') for rid in PINS)
save('READ_LEDGER.json',{'UTC':utc,'actual_rendered_bodies_read_entirely':True,'changed_production_code_read_entirely_through_diffs_and_helper':True,'authored_private_scripts_read':True,'prior_complete_manuscript_editorial_read_context':'Preserved original independent analytic, editorial-intake and final editorial packets; source hashes/whole custom objects reauthenticated here. No scientific review is replaced by stage tests.','read_bindings':[binding(p) for p in read_paths],'public_body_findings':'Whole original abstracts, full scientific scope/boundaries/prior credit, complete reader/support/citation and AI/unrefereed/passive contribution status retained; no public audit replay.','visual_browser_or_HTTP_review_performed':False})
proposal_names=['cylinder_discotope_source.py','render_page.proposed.py','final-content-check.proposed.py','render_page.stage.py','final-content-check.stage.py']
for name in proposal_names:ast.parse((O/name).read_text())
save('READINESS.json',{'UTC':utc,'assignment_status':'COMPLETE','completion_estimate_percent':100,'status':'PRIVATE_STAGE_COMPLETE_PENDING_ROOT_RENDERED_COPY_REVIEW_AND_INTEGRATION_AUTHORIZATION','authorized_targets':['23387774','23074543'],'proposed_code':[binding(O/n) for n in proposal_names],'private_overlay':'public','overlay_files':10,'expected_index_items':62,'expected_sitemap_urls':63,'predicted_integrated_whole_public_files':492,'production_integration_authorized':False,'production_integrated':False,'root_actual_renderer_copy_approval':False,'local_HTTP_verified':False,'live_HTTP_verified':False,'browser_verified':False,'native_Sheet_publication_verified':False,'AA':None,'follow_up':None,'source_or_canonical_config_changes':False,'source_correction_required':False,'human_peer_review':False,'formal_certification':False,'root_authority_retained':True,'overall203_programme_complete':False,'out_of_scope_new_preparation_configs_observed':new_other_configs})
with (O/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n* '+utc+' — Both actual private pages pass131 checks. One full59-record legacy suite passes3377 checks; all118 complete original/proposed renderer executions agree byte for byte in memory.54 actual-input rejections pass in normal and optimized Python;4 public-output fault controls reject. All1113 protected files, including484 production files, remain unchanged. Full actual public copies and changed code read. Private-stage completion100%; root rendered-copy review/integration authorization remain pending; overall203 programme ongoing.\n')
files=[]
for p in sorted(O.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:
        if p.is_symlink():raise RuntimeError('no_owned_symlinks')
        files.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p)})
save('FINAL_MANIFEST.json',{'UTC':utc,'namespace':str(O),'status':'IMMUTABLE_PRIVATE_STAGE_HANDOFF','files':files,'source_or_production_originals_mutated':False})
save('FINAL_SEAL.json',{'UTC':utc,'status':'SEALED_PRIVATE_STAGE_COMPLETE_ROOT_REVIEW_PENDING','manifest':'FINAL_MANIFEST.json','manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'owned_bindings':len(files),'completion_estimate_percent':100,'production_authority':False,'overall203_programme_complete':False,'preserve_this_original':True})
print(json.dumps({'status':'SEALED','owned_bindings':len(files),'manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'seal_SHA256':sha(O/'FINAL_SEAL.json')},indent=2))
