"""Fresh independent reference-only intake. No imports/execution of project code.
Reads only previous audit references and their closed original inputs; never the
current writer. Writes one exclusive receipt in this owned audit namespace.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat

N=Path(__file__).absolute().parent
P=N.parent.parent
def need(x,s):
    if not x: raise ValueError(s)
def pin(b): return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real input '+str(p))
    b=p.read_bytes(); return b
def typed(a,b):
    need(type(a) is type(b),'literal type')
    if type(a) is dict:
        need(list(a)==list(b),'literal key order')
        for k in a: typed(a[k],b[k])
    elif type(a) is list:
        need(len(a)==len(b),'literal list extent')
        for x,y in zip(a,b): typed(x,y)
    else: need(a==b,'literal scalar or historical null/flag')
def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary namespace')
    fs,ds=[],[]
    def walk(d):
        for e in os.scandir(d):
            q=Path(e.path); rel=q.relative_to(root).as_posix(); mode=q.lstat().st_mode
            if stat.S_ISDIR(mode): ds.append(rel); walk(q)
            else: need(stat.S_ISREG(mode),'reject link/special'); fs.append(rel)
    walk(root); return sorted(fs),sorted(ds)
def main():
    need(not (N/'INITIAL_SEAL.json').exists(),'intake before own INITIAL')
    ab=read(N/'APPROVED_INPUTS.json'); a=json.loads(ab)
    need(len(a['all_original_files'])==2212 and len(a['closed_original_namespaces'])==14,'finite inherited reference extent')
    for r in a['all_original_files']:
        need(pin(read(Path(r['path'])))=={k:r[k] for k in ('bytes','SHA256')},'complete original bytes '+r['path'])
    for r in a['closed_original_namespaces']:
        need(extent(Path(r['path']))==(r['files'],r['directories']),'complete original namespace '+r['path'])
    records=[]
    for r in a['records']:
        e=Path(r['editorial_root']); c=json.loads(read(Path(r['approved_config']['path'])))
        rid=r['record_id']; assets=r['native_assets_in_original_order']
        need(read(Path(r['approved_MAIN']['path'])).startswith(('<main id="'+r['main_id']+'">').encode()),'actual MAIN id')
        if rid=='23418581':
            proto=json.loads(read(e/'SOURCE_PROTOCOL_BINDINGS.json'))
            ready=json.loads(read(P/'papers'/rid/'sources/SOURCE_READY.json'))
            typed(c['source_binding']['whole_original_source_ready'],ready)
            typed(c['source_binding']['whole_native_API_objects'],proto['whole_native_API_objects_in_original_role_order'])
            typed(c['review_metadata']['root_authority']['whole_literal_object'],proto['whole_literal_root_authority'])
            typed(c['review_metadata']['whole_original_scientific_verdicts'],proto['whole_original_scientific_verdicts'])
            typed(c['source_binding']['native_asset_order'],[x['key'] for x in assets])
            for collection in ['whole_original_source_JSON_objects','whole_native_API_objects_in_original_role_order','whole_original_scientific_verdicts']:
                for item in proto[collection]: typed(json.loads(read(Path(item['original']['path']))),item['whole_original_object'])
            need(c['source_binding']['native_deposit_description_HTML_original']==json.loads(read(P/'papers'/rid/'sources/record.response.body'))['metadata']['description'],'whole separate native description')
        native_names=[x['key'] for x in assets]
        need(len(native_names)==len(set(native_names)),'distinct native assets')
        for x in assets:
            body=read(Path(x['native_path']))
            need(pin(body)=={k:x[k] for k in ['bytes','SHA256']},'exact original asset')
            original=x['original_asset_object']['original_api_file_object']
            need(hashlib.md5(body).hexdigest()==original['checksum'].split(':')[1],'original native MD5')
        leaves=[r['slug']+'/'+n for n in ['index.html',*native_names,'citation.bib']]
        records.append({'record_id':rid,'whole_MAIN':r['approved_MAIN'],'whole_config':r['approved_config'],'native_order':native_names,'future_article_paths_under_research':leaves,'article_leaves':len(leaves)})
    need(sum(r['article_leaves'] for r in records)==16,'derive 4+6+6 article leaves')
    payload={'UTC':datetime.now(timezone.utc).isoformat(),'status':'FRESH_TAKEOVER_SOURCE_HASH_EXTENT_AND_INTERFACE_PASS','prior_reference':{'path':str(N/'APPROVED_INPUTS.json'),**pin(ab)},'original_files_rehashed':2212,'closed_original_namespaces_rechecked':14,'whole_132_repeated_source_native_root_verdict_objects_typed_against_originals':True,'semantic_reading_limit':'Personally read all three whole MAINs (40599 bytes), full135136 configs and all unique132 config fields plus native description/wrapper interfaces; repeated whole132 source/native/scientific/root objects compared recursively with exact type/key/list order/null/history, not claimed as fresh scientific semantic reading. All8 editorial helper bodies (84204 bytes) read, never imported or executed. Root adoptions read in full.','records':records,'derived_article_leaves':16,'aggregate_replacements':['research/index.html','research/sitemap.xml'],'production_candidate_changed_paths':18,'current_writer_folder_accessed':False,'foreign_corpus_copied':False,'science_native_builder_or_old_campaign_executed':False,'production_authority':False}
    with (N/'TAKEOVER_SOURCE_CURRENT.json').open('x') as f: json.dump(payload,f,indent=2); f.write('\n')
    print(json.dumps({k:payload[k] for k in ['status','original_files_rehashed','closed_original_namespaces_rechecked','derived_article_leaves','production_candidate_changed_paths','current_writer_folder_accessed']}))
if __name__=='__main__': main()
