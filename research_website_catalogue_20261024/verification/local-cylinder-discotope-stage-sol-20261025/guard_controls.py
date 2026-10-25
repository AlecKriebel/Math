"""Exercise changed reads of actual objects in memory; no source fixture writes."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,sys
from cylinder_discotope_source import CD_IDS,PINS,cylinder_discotope_source_view,validate_original_receipt

O=Path(__file__).resolve().parent;R=O.parents[1]
rb,rt=Path.read_bytes,Path.read_text
checks=[]
def expect(rid,name,call,tag):
    try:call()
    except ValueError as e:
        reason=str(e)
        if tag not in reason:raise RuntimeError((rid,name,reason,tag))
        checks.append({'record_id':rid,'case':name,'rejected':True,'guard':reason})
    else:raise RuntimeError('accepted_changed_input:'+rid+':'+name)

for rid in sorted(CD_IDS):
    p=R/'papers'/rid;pin=PINS[rid]
    c=json.loads(rb(p/'publication.json'));g=json.loads(rb(p/'promotion.json'))
    raw=json.loads(rb(p/'sources/receipt.json'));api=json.loads(rb(p/'sources/zenodo-record.raw.json'))
    before=json.dumps([c,g,raw,api],sort_keys=True)
    original,view,assets=cylinder_discotope_source_view(p,c,g)
    if original!=raw or len(view['files'])!=2:raise RuntimeError('positive_control_failed')
    checks.append({'record_id':rid,'case':'exact_original_positive','accepted':True})
    for objname,obj in [('publication',c),('promotion',g)]:
        changed=deepcopy(obj);changed['status']='CHANGED_ACTUAL_ARGUMENT'
        expect(rid,'changed_passed_'+objname,lambda:cylinder_discotope_source_view(p,changed,g) if objname=='publication' else cylinder_discotope_source_view(p,c,changed),'passed_objects_equal_actual_configs')
    paths=[('publication.json','pinned_config_bytes'),('promotion.json','pinned_config_bytes'),('sources/receipt.json','receipt_bytes'),('sources/metadata.normalized.json','metadata_bytes'),('sources/zenodo-record.raw.json','raw_record_bytes'),(c['source_binding']['source_tex_path'],'actual_controlling_TeX'),('reviews/editorial/FINAL_SEAL.json','exact_editorial_seal_manifest'),('reviews/editorial/FINAL_MANIFEST.json','exact_editorial_seal_manifest'),(g['reviews']['analytic']['verdict_file'],'whole_custom_verdict_original_shape')]
    programme_paths=[('verification/root-clearance-'+rid+'-20261025.json','exact_scientific_authority'),('verification/root-editorial-'+rid+'-20261025.json','exact_editorial_authority')]
    for rel,tag in paths+programme_paths:
        path=(R/rel if rel.startswith('verification/') else p/rel).resolve()
        replacement=rb(path)+b'\nCHANGED_READ_CONTROL\n'
        Path.read_bytes=lambda q,_path=path,_data=replacement:_data if q.resolve()==_path else rb(q)
        Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or 'utf-8')
        try:expect(rid,'changed_read:'+rel,lambda:cylinder_discotope_source_view(p,c,g),tag)
        finally:Path.read_bytes=rb;Path.read_text=rt
    for filename in [pin['pdf'],pin['zip']]:
        path=(p/'sources'/filename).resolve();replacement=rb(path)+b'CHANGED_BYTES'
        Path.read_bytes=lambda q,_path=path,_data=replacement:_data if q.resolve()==_path else rb(q)
        try:expect(rid,'changed_actual_asset:'+filename,lambda:cylinder_discotope_source_view(p,c,g),'actual_asset_bytes')
        finally:Path.read_bytes=rb
        data=rb(path);replacement=bytes([data[0]^1])+data[1:]
        Path.read_bytes=lambda q,_path=path,_data=replacement:_data if q.resolve()==_path else rb(q)
        try:expect(rid,'same_length_changed_actual_asset:'+filename,lambda:cylinder_discotope_source_view(p,c,g),'actual_asset_MD5')
        finally:Path.read_bytes=rb
    key=pin['asset_key']
    cases=[]
    bad=deepcopy(raw);bad['actual_assets' if key=='exact_assets' else 'exact_assets']=bad.pop(key);cases.append(('other_paper_schema',bad,'receipt_original_asset_key'))
    bad=deepcopy(raw);bad['files']=[];cases.append(('invented_files_alias',bad,'receipt_no_schema_alias'))
    bad=deepcopy(raw);bad[key][0]['sha256' if pin['sha_key']=='SHA256' else 'SHA256']=bad[key][0].pop(pin['sha_key']);cases.append(('wrong_SHA_field_case',bad,'receipt_exact_original_asset_fields'))
    bad=deepcopy(raw);bad[key][0]['file_object'].pop('links');cases.append(('truncated_API_file_object',bad,'actual_API_file_object_exact'))
    bad=deepcopy(raw);bad[key][0]['bytes']+=1;cases.append(('wrong_API_size',bad,'receipt_API_size'))
    bad=deepcopy(raw);bad[key][0][pin['md5_key']]='0'*32;cases.append(('wrong_API_MD5',bad,'API_MD5_checksum'))
    bad=deepcopy(raw);bad[key][0]['path']=str(p/'sources/../publication.json');cases.append(('path_escape',bad,'original_contained_asset_path'))
    bad=deepcopy(raw);next(x for x in bad[key] if x['file_object']['key']==pin['pdf'])['pages']=5;cases.append(('historical_or_incomplete_reader_page_count',bad,'selected_reader_page_count'))
    bad=deepcopy(raw);bad[key][1]=deepcopy(bad[key][0]);cases.append(('duplicate_asset',bad,'exact_selected_asset_names'))
    if rid=='23387774':
        bad=deepcopy(raw);bad['selected_PDF']=[];cases.append(('selected_PDF_original_object_lost',bad,'original_selected_PDF_object'))
    for name,bad,tag in cases:expect(rid,name,lambda bad=bad:validate_original_receipt(p,rid,bad,api),tag)
    if before!=json.dumps([c,g,raw,api],sort_keys=True):raise RuntimeError('actual_objects_mutated')
expect('UNSUPPORTED','unrelated_94_ID',lambda:cylinder_discotope_source_view(R/'papers/23181280',{},{}),'unsupported_id')
print(json.dumps({'status':'PASS','python_optimization':sys.flags.optimize,'scope':'Actual objects/bytes intercepted only in memory; no source, receipt, asset or fixture writes.','checks':checks},indent=2))
