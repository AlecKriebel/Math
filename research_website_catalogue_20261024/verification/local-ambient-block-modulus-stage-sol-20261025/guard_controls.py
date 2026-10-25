"""Bounded in-memory source/schema changes; no altered source tree."""
from pathlib import Path
from copy import deepcopy
import json,sys
from ambient_block_modulus_source import *
O=Path(__file__).resolve().parent;P=O.parents[1];rb,rt=Path.read_bytes,Path.read_text;checks=[]
def reject(rid,name,call):
    try:call()
    except (ValueError,FileNotFoundError,KeyError) as e:checks.append({'record_id':rid,'case':name,'rejected':True,'reason':str(e)[:240]})
    else:raise RuntimeError('accepted_changed_input:'+rid+':'+name)
for rid in sorted(ABM_IDS):
    p=P/'papers'/rid;c=json.loads(rb(p/'publication.json'));g=json.loads(rb(p/'promotion.json'));b=c['source_binding'];raw=json.loads(rb(p/b['source_receipt_path']));api=json.loads(rb(p/b['raw_record_path']));before=deepcopy([c,g,raw,api])
    original,view,root=ambient_block_modulus_source_view(p,c,g)
    if original!=raw or len(view['files'])!=2:raise RuntimeError('pristine_source_view')
    checks.append({'record_id':rid,'case':'pristine','accepted':True})
    for name,kind in [('changed_passed_version','version'),('changed_complete_custom_verdict','verdict'),('changed_scalar_type_completion','scalar')]:
        bc,bg=deepcopy(c),deepcopy(g)
        if kind=='version':bc['version']='9.9'
        elif kind=='verdict':bg['reviews']['scope']['verdict']={}
        else:bc['review_metadata']['completion_percent']=100.0
        reject(rid,name,lambda:ambient_block_modulus_source_view(p,bc,bg))
    paths=[p/'publication.json',p/'promotion.json',p/b['source_receipt_path'],p/b['raw_record_path'],p/b['metadata_path'],p/b['transport_receipt_path'],p/b['source_tex_path'],p/b['prepared_bibtex_path'],p/g['reviews']['analytic']['verdict_file'],P/g['root_clearance_file'],P/('verification/root-editorial-'+rid+'-20261025.json'),p/'reviews/editorial/SEAL.json',p/'reviews/editorial/MANIFEST.json']
    paths += [Path(x['path']) for x in raw[SCHEMAS[rid][0]]]
    paths += [p/'sources'/fn for fn in ['SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_MANIFEST.json','SOURCE_SEAL.json','archive-members.json']]
    for path in dict.fromkeys(x.resolve() for x in paths):
        data=rb(path);replacement=bytes([data[0]^1])+data[1:]
        Path.read_bytes=lambda q,_p=path,_d=replacement:_d if q.resolve()==_p else rb(q)
        Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or 'utf-8')
        try:reject(rid,'changed_actual_read:'+str(path.relative_to(P)),lambda:ambient_block_modulus_source_view(p,c,g))
        finally:Path.read_bytes=rb;Path.read_text=rt
    key,objkey=SCHEMAS[rid]
    for name,mutation in [('invented_files_alias',lambda x:x.update(files=[])),('wrong_array_schema',lambda x:x.update({('all_assets' if key=='all_actual_assets' else 'all_actual_assets'):x.pop(key)})),('wrong_SHA_case',lambda x:x[key][0].update(SHA256=x[key][0].pop('sha256'))),('wrong_API_object_key',lambda x:x[key][0].update({('original_api_file_object' if objkey=='api_file_object' else 'api_file_object'):x[key][0].pop(objkey)})),('reordered_original_assets',lambda x:x[key].reverse()),('dropped_actual_asset',lambda x:x[key].pop()),('invented_transport_in_asset',lambda x:x[key][0].update(http_status=200))]:
        bad=deepcopy(raw);mutation(bad);reject(rid,name,lambda:validate_abm_assets(p,rid,bad,api))
    if rid=='23416806':
        inventory=json.loads(rb(p/'sources/archive-members.json'));bad=deepcopy(inventory);bad['members']=[x for x in bad['members'] if x['container']==c['supplement_filename']]
        reject(rid,'erase_nested_qualified_occurrences',lambda:verify_abm_archive(p,rid,p/'sources'/c['supplement_filename'],bad))
        bad=deepcopy(inventory);bad['archive_containers'][1]['extraction_root']=str(p/'sources/published-source')
        reject(rid,'collapse_nested_extraction_mapping',lambda:verify_abm_archive(p,rid,p/'sources'/c['supplement_filename'],bad))
    if rid=='23441617':
        for name,kind in [('generic_PASS_substitution','status'),('unbounded_PASS_prefix','prefix'),('erase_root_bibliographic_defect','defect'),('invent_printed_manuscript_version','version'),('public_HK_180_regression','reference')]:
            bc,bg=deepcopy(c),deepcopy(g)
            if kind=='status':bg['status']='PASS'
            elif kind=='prefix':bg['status']='PASS_ANY_UNAUTHENTICATED_SUFFIX'
            elif kind=='defect':bg['root_clearance_record']['noncentral_bibliographic_defect']={}
            elif kind=='version':bc['source_binding']['manuscript_version']='1.0'
            else:
                for x in bc['background']:
                    if 'Heinonen' in x['title']:x['title']=x['title'].replace('181','180')
            reject(rid,name,lambda:ambient_block_modulus_source_view(p,bc,bg))
    if before!=[c,g,raw,api]:raise RuntimeError('original_arguments_mutated')
reject('UNSUPPORTED','exclude100_101_103_and_all_others',lambda:ambient_block_modulus_source_view(P/'papers/23441976',{},{}))
print(json.dumps({'status':'PASS','optimized':sys.flags.optimize,'checks':checks,'original_arguments_unchanged':True,'source_fixture_writes':0},indent=2))
