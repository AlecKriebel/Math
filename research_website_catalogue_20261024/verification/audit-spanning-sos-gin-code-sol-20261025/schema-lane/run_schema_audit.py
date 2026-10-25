from pathlib import Path, PurePosixPath
import ast, builtins, copy, datetime, hashlib, json, sys, types
from unittest.mock import patch

sys.dont_write_bytecode=True
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S=P/'verification/local-spanning-sos-gin-stage-sol-20261025'
E=P/'verification/audit-spanning-sos-gin-code-sol-20261025/schema-lane'
IDS=['23181280','23442760','23395703']
START=datetime.datetime.now(datetime.timezone.utc).isoformat()
rb=Path.read_bytes
rt=Path.read_text
sha=lambda b:hashlib.sha256(b).hexdigest()
md5=lambda b:hashlib.md5(b).hexdigest()

def write(name,obj):
    target=E/name
    assert target.parent==E
    if isinstance(obj,str): target.write_text(obj)
    else: target.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def binding(path):
    data=rb(path)
    return {'path':str(path),'bytes':len(data),'sha256':sha(data)}

def baseline():
    files=set(S.rglob('*'))
    for rid in IDS: files.update((P/'papers'/rid).rglob('*'))
    for t in authority['targets']:
        files.update(Path(x['path']) for x in t['bindings'])
        g=json.loads(rb(P/'papers'/t['record_id']/'promotion.json'))
        sc=g['root_clearance_record']
        files.update([P/sc['root_review'],P/sc['root_custody_receipt']])
    files.update([P/'scripts/bosonic_source.py',P/'scripts/published_assets.py'])
    return [binding(x) for x in sorted(files) if x.is_file()]

pins=json.loads(rb(S/'INPUT_PINS.json'))
authority=json.loads(rb(S/'AUTHORITY_SOURCE_BINDINGS.json'))
before=baseline()
write('CUSTODY_BEFORE.json',{'utc':START,'stage_files':sum(Path(x['path']).is_relative_to(S) for x in before),'bindings':before,'scope':'Entire sealed stage and complete three original paper trees, original authority refs, imported-helper dependencies; stage control outputs hashed only, not parsed.'})

# Import only the specific dependency functions from their actual AST nodes.
# No unrelated original source program or top-level dependency code executes.
bos_src=rt(P/'scripts/bosonic_source.py')
assets_src=rt(P/'scripts/published_assets.py')
def extract_functions(src,names,namespace):
    tree=ast.parse(src)
    ns=dict(namespace)
    selected=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
    assert {n.name for n in selected}==set(names)
    exec(compile(ast.Module(body=selected,type_ignores=[]),'<actual audited dependency functions>','exec'),ns)
    return types.SimpleNamespace(**{n:ns[n] for n in names})
bos=extract_functions(bos_src,['contained_file','digest'],{'Path':Path,'PurePosixPath':PurePosixPath,'hashlib':hashlib})
assets=extract_functions(assets_src,['safe_relative'],{'PurePosixPath':PurePosixPath})
original_import=builtins.__import__
def imports(name,*args,**kwargs):
    if name=='bosonic_source':return bos
    if name=='published_assets':return assets
    return original_import(name,*args,**kwargs)
helper_source=rt(S/'spanning_sos_gin_source.py')
ns={'__builtins__':dict(vars(builtins),__import__=imports),'__name__':'audit_memory_spanning_sos_gin_source'}
exec(compile(helper_source,str(S/'spanning_sos_gin_source.py'),'exec'),ns)
assert ns['PINS']==pins['target_pins']

pristine={rid:(json.loads(rb(P/'papers'/rid/'publication.json')),json.loads(rb(P/'papers'/rid/'promotion.json'))) for rid in IDS}
results=[]
def control(name,rid,fn,expect_reject=True,mode='ordinary intact pins'):
    try:
        out=fn()
        error=None
    except Exception as ex:
        out=None;error={'type':type(ex).__name__,'message':str(ex)}
    passed=(error is not None)==expect_reject
    result={'name':name,'record_id':rid,'mode':mode,'expected':'reject' if expect_reject else 'accept','passed':passed,'error':error}
    if out is not None and isinstance(out,(str,int,bool,list,dict)):result['evidence']=out
    results.append(result)
    return result

def invoke(rid,c=None,g=None,overlay=None,blind=()):
    c0,g0=pristine[rid]
    c=copy.deepcopy(c0) if c is None else c
    g=copy.deepcopy(g0) if g is None else g
    overlay={str(k):v for k,v in (overlay or {}).items()}
    old_digest=ns['digest']
    blind={str(x) for x in blind}
    def readbytes(path):
        return overlay.get(str(path),rb(path))
    def readtext(path,*args,**kwargs):
        if str(path) in overlay:return overlay[str(path)].decode(kwargs.get('encoding') or 'utf-8')
        return rt(path,*args,**kwargs)
    def digest(path):
        return sha(rb(path)) if str(path) in blind else sha(readbytes(path))
    ns['digest']=digest
    try:
        with patch.object(Path,'read_bytes',readbytes),patch.object(Path,'read_text',readtext):
            return ns['spanning_sos_gin_source_view'](P/'papers'/rid,c,g)
    finally:ns['digest']=old_digest

facts=[]
for target in authority['targets']:
    rid=target['record_id'];paper=P/'papers'/rid;c,g=pristine[rid];b=c['source_binding']
    for x in target['bindings']:
        actual=binding(Path(x['path']))
        assert actual['bytes']==x['bytes'] and actual['sha256']==x['SHA256']
    raw=json.loads(rb(paper/b['source_receipt_path']));api=json.loads(rb(paper/b['raw_record_path']));meta=json.loads(rb(paper/b['metadata_path']));trans=json.loads(rb(paper/b['transport_receipt_path']))
    key,sh,mh,count=ns['SCHEMAS'][rid]
    assert len(raw[key])==len(api['files'])==count
    assert all(x['api_file_object']==a for x,a in zip(raw[key],api['files']))
    assert api['metadata']==meta['metadata']
    assets_facts=[]
    for x in raw[key]:
        data=rb(Path(x['path']));a=x['api_file_object']
        assert len(data)==x['bytes']==a['size'] and sha(data)==x[sh] and 'md5:'+md5(data)==a['checksum']=='md5:'+x[mh]
        assets_facts.append({'name':a['key'],'bytes':len(data),'sha256':sha(data),'MD5':md5(data),'url':a['links']['self'],'fields':list(x)})
    headers_key='headers' if rid=='23395703' else 'response_headers'
    raw_headers=[{'path':e['path'],'oc-checksum':e[headers_key].get('oc-checksum')} for e in trans if 'oc-checksum' in e[headers_key]]
    tex=rb(paper/b['source_tex_path'])
    assert sha(tex)==b['source_tex_sha256']==g['root_clearance_record']['source_tex_sha256']
    facts.append({'record_id':rid,'original_source_schema':{'key':key,'sha256_field':sh,'md5_field':mh,'asset_count':count},'metadata_path':b['metadata_path'],'raw_record_path':b['raw_record_path'],'metadata_top_level_fields':list(meta),'raw_top_level_fields':list(api),'raw_version_present':'version' in api['metadata'],'raw_version_value':api['metadata'].get('version'),'source_tex_path':b['source_tex_path'],'source_tex_sha256':sha(tex),'source_tex_bytes':len(tex),'assets':assets_facts,'transport_count':len(trans),'transport_fields':[list(e) for e in trans],'raw_checksum_headers_preserved':raw_headers})

    def positive(rid=rid):
        c,g=copy.deepcopy(pristine[rid]);before_args=copy.deepcopy((c,g));before_serial=json.dumps((c,g),sort_keys=True)
        raw_view,derived,root=invoke(rid,c,g)
        assert (c,g)==before_args and json.dumps((c,g),sort_keys=True)==before_serial
        assert derived['record_id']==rid and len(derived['files'])==ns['SCHEMAS'][rid][3]
        assert root==P/'papers'/rid/'sources'
        original=json.loads(rb(P/'papers'/rid/c['source_binding']['source_receipt_path']))
        assert raw_view==original and raw_view is not c['source_binding']['source_receipt_record'] and raw_view is not g['source_receipt_record']
        assert [x['name'] for x in derived['files']]==[x['api_file_object']['key'] for x in original[ns['SCHEMAS'][rid][0]]]
        derived['files'][0]['name']='AUDIT ONLY MUTATION OF RETURNED DERIVED VIEW'
        assert (c,g)==before_args and raw_view==original
        return {'input_deep_snapshot_unchanged':True,'caller_raw_record_aliased':False,'returned_view_mutation_isolated':True,'files':[x['api_file_object']['key'] for x in original[ns['SCHEMAS'][rid][0]]]}
    control('pristine_full_helper_and_caller_immutability',rid,positive,False)
    
    for field,newvalue in [('title','altered title'),('version','1.0' if rid=='23395703' else '2.0'),('canonical_url','https://example.invalid/audit'),('follow_up','invented follow-up')]:
        c2=copy.deepcopy(c);c2[field]=newvalue
        control('caller_config_'+field,rid,lambda c2=c2,g=g:invoke(rid,c2,copy.deepcopy(g)))
    for field,newvalue in [('status','FAIL'),('disposition_by','other'),('AA','https://example.invalid/audit'),('follow_up','invented'),('canonical_url','https://example.invalid/audit'),('rendered_copy_verified',True),('native_verified',True)]:
        g2=copy.deepcopy(g);g2[field]=newvalue
        control('caller_gate_'+field,rid,lambda g2=g2,c=c:invoke(rid,copy.deepcopy(c),g2))
    
    # Every source and authority pin is tested without trusting stage controls.
    tamper_paths=[paper/'publication.json',paper/'promotion.json',paper/b['source_receipt_path'],paper/b['metadata_path'],paper/b['raw_record_path'],paper/b['transport_receipt_path'],paper/b['source_tex_path'],P/g['root_clearance_file'],P/f'verification/root-editorial-{rid}-20261025.json',paper/'reviews/editorial/SEAL.json',paper/'reviews/editorial/MANIFEST.json']
    tamper_paths += [Path(x['path']) for x in raw[key]]
    for path in dict.fromkeys(tamper_paths):
        control('read_bytes_changed:'+str(path.relative_to(P)),rid,lambda path=path:invoke(rid,overlay={path:rb(path)+b'\n'}))
    
    def asset_control(name,mutate):
        r2,a2=copy.deepcopy((raw,api));mutate(r2,a2)
        control(name,rid,lambda:ns['validate_sg_assets'](paper,rid,r2,a2),mode='direct actual schema validator; no digest layer')
    asset_control('receipt_alias_added',lambda r,a:r.__setitem__('assets',copy.deepcopy(r[key])))
    asset_control('receipt_wrong_asset_key',lambda r,a:r.__setitem__('files',r.pop(key)))
    asset_control('receipt_asset_removed',lambda r,a:r[key].pop())
    asset_control('API_asset_removed',lambda r,a:a['files'].pop())
    asset_control('API_asset_order_changed',lambda r,a:a['files'].reverse())
    asset_control('API_custom_object_trimmed',lambda r,a:r[key][0]['api_file_object'].pop('id'))
    asset_control('receipt_custom_field_added',lambda r,a:r[key][0].__setitem__('normalized',True))
    asset_control('wrong_SHA_field_case',lambda r,a:r[key][0].__setitem__(sh.swapcase(),r[key][0].pop(sh)))
    asset_control('wrong_MD5_field_case',lambda r,a:r[key][0].__setitem__(mh.swapcase(),r[key][0].pop(mh)))
    asset_control('uppercase_SHA_value',lambda r,a:r[key][0].__setitem__(sh,r[key][0][sh].upper()))
    asset_control('uppercase_MD5_value',lambda r,a:r[key][0].__setitem__(mh,r[key][0][mh].upper()))
    asset_control('receipt_size_bool',lambda r,a:r[key][0].__setitem__('bytes',True))
    asset_control('receipt_path_alias',lambda r,a:r[key][0].__setitem__('path','sources/'+r[key][0]['api_file_object']['key']))
    def dupe(r,a):
        r[key][-1]=copy.deepcopy(r[key][0]);a['files'][-1]=copy.deepcopy(a['files'][0])
    asset_control('duplicate_asset_names',dupe)
    
    # Type-alias exploration: exact bytes still pinned; caller snapshot equality
    # is Python value equality, not strict recursive JSON type equality.
    c2=copy.deepcopy(c);c2['review_metadata']['completion_percent']=float(c2['review_metadata']['completion_percent'])
    def type_alias():
        invoke(rid,c2,copy.deepcopy(g))
        return {'integer_original':type(c['review_metadata']['completion_percent']).__name__,'caller_type':type(c2['review_metadata']['completion_percent']).__name__,'value':c2['review_metadata']['completion_percent'],'effect':'accepted caller-only type alias; returned source/asset bytes still original'}
    control('caller_integer_float_value_equality_boundary',rid,type_alias,False,mode='bounded equality limitation exploration')

# Inner-schema controls use read overlays plus explicit bypass only of listed
# digest anchors, to independently reach checks below the cryptographic layer.
rid='23395703';paper=P/'papers'/rid;c,g=copy.deepcopy(pristine[rid]);b=c['source_binding']
api_path=paper/b['raw_record_path'];meta_path=paper/b['metadata_path']
a2=json.loads(rb(api_path));m2=json.loads(rb(meta_path));a2['metadata']['version']='1.0';m2['metadata']['version']='1.0'
control('Gin_invented_raw_version_inner_guard',rid,lambda:invoke(rid,overlay={api_path:json.dumps(a2).encode(),meta_path:json.dumps(m2).encode()},blind=[api_path,meta_path]),mode='inner guard: deliberately blinded raw+metadata digest anchors; immutable config pins unchanged')

# Caller presence false->0 would pass Python equality, but explicit `is False`
# blocks the promotion and binding presence flags used by the helper.
for location in ['binding','gate']:
    c2,g2=copy.deepcopy(pristine[rid]);obj=c2['source_binding'] if location=='binding' else g2;obj['version_field_present']=0
    control('Gin_false_presence_numeric_alias_'+location,rid,lambda c2=c2,g2=g2:invoke(rid,c2,g2))

# Rewriting a raw header alone fails intact full-object authentication. The
# exact original unusual text must remain; it is not a canonical API checksum.
transpath=paper/pristine[rid][0]['source_binding']['transport_receipt_path']
t2=json.loads(rb(transpath));pdf=next(x for x in t2 if str(x['path']).endswith('/seven_plane_gin.pdf'));pdf['headers']['oc-checksum']='MD5:'+pdf['MD5']
control('Gin_repaired_raw_MD5_header',rid,lambda:invoke(rid,overlay={transpath:json.dumps(t2).encode()}))

# An explicit semantic control for transport and private gates can be reached
# by blinding only publication/promotion/transport byte pins in memory.
def coherent_overlay(rid,change):
    c2,g2=copy.deepcopy(pristine[rid]);extra={};change(c2,g2,extra)
    cp=P/'papers'/rid/'publication.json';gp=P/'papers'/rid/'promotion.json'
    extra[cp]=json.dumps(c2).encode();extra[gp]=json.dumps(g2).encode()
    return invoke(rid,c2,g2,overlay=extra,blind=list(extra))
for rid in IDS:
    def wrong_headers(c2,g2,extra,rid=rid):
        path=P/'papers'/rid/c2['source_binding']['transport_receipt_path'];t=json.loads(rb(path));h='headers' if rid=='23395703' else 'response_headers';t[0][h]={}
        c2['source_binding']['transport_receipt_record']=copy.deepcopy(t);g2['transport_receipt_record']=copy.deepcopy(t);extra[path]=json.dumps(t).encode()
    control('transport_empty_headers_inner_guard',rid,lambda rid=rid:coherent_overlay(rid,wrong_headers),mode='inner guard: deliberately blinded coherent config/promotion/transport pins')
    for field,value in [('AA','invented'),('follow_up','invented'),('rendered_copy_verified',True)]:
        def mutate_gate(c2,g2,extra,field=field,value=value):g2[field]=value
        control('gate_'+field+'_inner_guard',rid,lambda rid=rid,change=mutate_gate:coherent_overlay(rid,change),mode='inner guard: deliberately blinded coherent config/promotion pins')

    def wrong_editorial(c2,g2,extra,rid=rid):
        path=P/f'verification/root-editorial-{rid}-20261025.json';ed=json.loads(rb(path));ed['production_integration_authorized']=True;extra[path]=json.dumps(ed).encode()
    control('editorial_production_authority_inner_guard',rid,lambda rid=rid:coherent_overlay(rid,wrong_editorial),mode='inner guard: deliberately blinded exact editorial digest anchor')

    def payload_without_digest_blind(rid=rid):
        c2,g2=pristine[rid];tpath=P/'papers'/rid/c2['source_binding']['transport_receipt_path'];t=json.loads(rb(tpath));sh='sha256' if rid=='23442760' else 'SHA256';t[0][sh]='0'*64
        return invoke(rid,overlay={tpath:json.dumps(t).encode()})
    control('transport_payload_SHA_changed_intact_pins',rid,payload_without_digest_blind)

# Remove Gin's standalone TeX coherently across original object interfaces,
# while deliberately suppressing their digest anchors to reach the real count
# check. Actual source TeX and all source bytes remain on disk, unchanged.
rid='23395703'
def remove_gin_tex(c2,g2,extra):
    paper=P/'papers'/rid;b=c2['source_binding']
    rawpath=paper/b['source_receipt_path'];apipath=paper/b['raw_record_path'];metapath=paper/b['metadata_path']
    raw=json.loads(rb(rawpath));api=json.loads(rb(apipath));meta=json.loads(rb(metapath))
    raw['all_actual_assets'].pop(0);api['files'].pop(0);meta['all_file_objects'].pop(0);meta['assets'].pop(0)
    b['source_receipt_record']=copy.deepcopy(raw);g2['source_receipt_record']=copy.deepcopy(raw)
    b['files']=copy.deepcopy(raw['all_actual_assets']);g2['source_files']=copy.deepcopy(raw['all_actual_assets'])
    b['published_file_objects']=copy.deepcopy(api['files']);g2['published_file_objects']=copy.deepcopy(api['files'])
    extra[rawpath]=json.dumps(raw).encode();extra[apipath]=json.dumps(api).encode();extra[metapath]=json.dumps(meta).encode()
    transpath=paper/b['transport_receipt_path'];trans=json.loads(rb(transpath))
    for event in trans:
        if Path(event['path'])==apipath:
            event['bytes']=len(extra[apipath]);event['SHA256']=sha(extra[apipath]);event['MD5']=md5(extra[apipath])
    b['transport_receipt_record']=copy.deepcopy(trans);g2['transport_receipt_record']=copy.deepcopy(trans);extra[transpath]=json.dumps(trans).encode()
control('Gin_drop_original_TeX_full_helper_inner_count',rid,lambda:coherent_overlay(rid,remove_gin_tex),mode='inner guard: coherently removed TeX across caller/raw/normalized objects and transport payload bookkeeping; deliberately blinded config/promotion/source/raw/metadata/transport digest anchors')

# Original spanning API-comparison flags require Boolean identity, whereas the
# receipt byte count rejects integer-lookalike booleans and floats directly.
rid='23181280';paper=P/'papers'/rid;c,g=pristine[rid];raw=json.loads(rb(paper/c['source_binding']['source_receipt_path']));api=json.loads(rb(paper/c['source_binding']['raw_record_path']))
for field,value in [('size_equals_API',1),('checksum_equals_API',1),('bytes',float(raw['actual_assets'][0]['bytes']))]:
    r2=copy.deepcopy(raw);r2['actual_assets'][0][field]=value
    control('spanning_receipt_strict_identity_'+field,rid,lambda r2=r2:ns['validate_sg_assets'](paper,rid,r2,api),mode='direct actual schema validator; no digest layer')

assert all(r['passed'] for r in results)
assert all(r['error']['type']=='ValueError' and r['error']['message'].startswith('spanning_sos_gin:') for r in results if r['error'])
expected_deep_errors={'Gin_invented_raw_version_inner_guard':'honest_missing_version','Gin_drop_original_TeX_full_helper_inner_count':'all_actual_asset_count','transport_empty_headers_inner_guard':'actual_transport_interface','editorial_production_authority_inner_guard':'private_stage_authority_only','gate_AA_inner_guard':'unchanged_null_gates','gate_follow_up_inner_guard':'unchanged_null_gates','gate_rendered_copy_verified_inner_guard':'unchanged_false_publication_gates'}
for r in results:
    if r['name'] in expected_deep_errors:
        assert r['error']['message']=='spanning_sos_gin:'+expected_deep_errors[r['name']]

write('SOURCE_SCHEMA_FACTS.json',{'utc':START,'independent_reconstruction':facts,'authority_bindings_checked':sum(len(t['bindings']) for t in authority['targets']),'pin_dictionary_equals_INPUT_PINS':True})
write('CONTROLS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper_sha256':sha(helper_source.encode()),'helper_source_lines':len(helper_source.splitlines()),'control_count':len(results),'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'results':results})
after=baseline();changed=[{'before':a,'after':b} for a,b in zip(before,after) if a!=b]
assert len(before)==len(after) and not changed
write('CUSTODY_AFTER.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bindings_checked':len(before),'stage_files':sum(Path(x['path']).is_relative_to(S) for x in after),'all_before_bindings_unchanged':True,'changed':changed,'before_manifest_sha256':sha(rb(E/'CUSTODY_BEFORE.json'))})
print(json.dumps({'controls':len(results),'passed':sum(r['passed'] for r in results),'unexpected':[r for r in results if not r['passed']],'custody_files':len(before),'stage_files':sum(Path(x['path']).is_relative_to(S) for x in after),'output_dir':str(E)},indent=2))
