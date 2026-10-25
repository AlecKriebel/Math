"""Actual source/schema changed reads in memory, normal and optimized safe."""
from pathlib import Path
from copy import deepcopy
import json,sys
from spanning_sos_gin_source import SG_IDS,SCHEMAS,spanning_sos_gin_source_view,validate_sg_assets,display_sg_text
O=Path(__file__).resolve().parent;P=O.parents[1];rb,rt=Path.read_bytes,Path.read_text;checks=[]
def reject(rid,name,call):
    try:call()
    except (ValueError,FileNotFoundError) as e:checks.append({'record_id':rid,'case':name,'rejected':True,'reason':str(e)})
    else:raise RuntimeError('accepted_changed_input:'+rid+':'+name)
for rid in sorted(SG_IDS):
    p=P/'papers'/rid;c=json.loads(rb(p/'publication.json'));g=json.loads(rb(p/'promotion.json'));b=c['source_binding'];raw=json.loads(rb(p/b['source_receipt_path']));api=json.loads(rb(p/b['raw_record_path']));before=deepcopy([c,g,raw,api])
    original,view,root=spanning_sos_gin_source_view(p,c,g)
    if original!=raw or len(view['files'])!=b['published_asset_count']:raise RuntimeError('pristine_source_view')
    checks.append({'record_id':rid,'case':'pristine','accepted':True})
    bad=deepcopy(c);bad['version']='9.9';reject(rid,'changed_passed_version',lambda:spanning_sos_gin_source_view(p,bad,g))
    badgate=deepcopy(g);badgate['reviews']['scope']['verdict']={};reject(rid,'changed_passed_complete_custom_verdict',lambda:spanning_sos_gin_source_view(p,c,badgate))
    paths=[p/'publication.json',p/'promotion.json',p/b['source_receipt_path'],p/b['raw_record_path'],p/b['metadata_path'],p/b['transport_receipt_path'],p/b['source_tex_path'],p/b['prepared_bibtex_path'],p/g['reviews']['analytic']['verdict_file'],P/g['root_clearance_file'],P/('verification/root-editorial-'+rid+'-20261025.json'),p/'reviews/editorial/SEAL.json',p/'reviews/editorial/MANIFEST.json']
    paths += [Path(x['path']) for x in b['files']]
    if 'pending_intake_seal_path' in b:paths.append(p/b['pending_intake_seal_path'])
    for path in dict.fromkeys(x.resolve() for x in paths):
        data=rb(path);replacement=bytes([data[0]^1])+data[1:]
        Path.read_bytes=lambda q,_p=path,_d=replacement:_d if q.resolve()==_p else rb(q)
        Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or 'utf-8')
        try:reject(rid,'changed_actual_read:'+str(path.relative_to(P)),lambda:spanning_sos_gin_source_view(p,c,g))
        finally:Path.read_bytes=rb;Path.read_text=rt
    key,sh,mh,count=SCHEMAS[rid]
    bad=deepcopy(raw);bad['files']=[];reject(rid,'invented_source_files_alias',lambda:validate_sg_assets(p,rid,bad,api))
    bad=deepcopy(raw);bad['actual_assets' if key=='all_actual_assets' else 'all_actual_assets']=bad.pop(key);reject(rid,'other_paper_receipt_schema',lambda:validate_sg_assets(p,rid,bad,api))
    bad=deepcopy(raw);bad[key][0]['SHA256' if sh=='sha256' else 'sha256']=bad[key][0].pop(sh);reject(rid,'wrong_checksum_field_case',lambda:validate_sg_assets(p,rid,bad,api))
    bad=deepcopy(raw);bad[key][0]['api_file_object'].pop('links');reject(rid,'incomplete_API_file_object',lambda:validate_sg_assets(p,rid,bad,api))
    bad=deepcopy(raw);bad[key].pop();reject(rid,'dropped_actual_asset',lambda:validate_sg_assets(p,rid,bad,api))
    bad=deepcopy(raw);bad[key][0]['path']=str(p/'publication.json');reject(rid,'wrong_asset_path',lambda:validate_sg_assets(p,rid,bad,api))
    reject(rid,'unrecognized_math_source',lambda:display_sg_text(rid,'Scope $\\unrecognized{x}$'))
    if before!=[c,g,raw,api]:raise RuntimeError('original_arguments_mutated')
reject('UNSUPPORTED','exclude97_and_others',lambda:spanning_sos_gin_source_view(P/'papers/99999999',{},{}))
print(json.dumps({'status':'PASS','optimized':sys.flags.optimize,'checks':checks,'original_arguments_unchanged':True,'source_fixture_writes':0},indent=2))
