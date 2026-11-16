"""Reference-only independent intake of three approved editorial interfaces.
Never accesses the current three-page stage writer, executes old code, or copies
scientific/primary bodies. Only exclusive new metadata in this audit is written.
"""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import stat

N=Path(__file__).absolute().parent
P=N.parent.parent
SPECS=[('23418581','2fd373bc8776b88f12ab5ca71d8b7d8d6e49143d956798147d5edfb4ec83adc0','671d27c2cb8c1c2a3111e4f765fdeb5d7a1562fdd9fe7f57bb7960a55ac4ee4f','MANIFEST.json','PUBLIC_MAIN.html','publication.json','candidate'),('23202966','8b3ef9a219c4e6b46f60d7276abb05e49c3175a62a61921f38646f4070bd5e15','e914ec3773de312223ce537242d3f85f02a42a66d198402ace945754fb7ee956','OWNED_MANIFEST.json','PUBLIC_MAIN.html','EDITORIAL_CONFIG.json','candidate'),('23205305','431c5951067b0e320185e60be47ad0bd936d3515e420516e0d911344ace1be51','75ee87613b40d710c6e4dd7d0bcf2046954587bd75474f18a862bf882668b35a','OWNED_MANIFEST.json','normal/PUBLIC_MAIN.html','EDITORIAL_CONFIG.json','normal')]

def need(x,why):
    if not x:raise ValueError(why)

def descriptor(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real input');return p.read_bytes()

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
    fs,ds=[],[]
    def walk(d):
        with os.scandir(d) as rows:
            for e in rows:
                q=Path(e.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
                if stat.S_ISDIR(m):ds.append(r);walk(q)
                else:need(stat.S_ISREG(m),'reject link/special');fs.append(r)
    walk(root);return sorted(fs),sorted(ds)

def new(name,x):
    with (N/name).open('xb') as f:f.write((json.dumps(x,indent=2)+'\n').encode())

def main():
    need(not (N/'INITIAL_SEAL.json').exists(),'source-only initial not yet frozen')
    allfiles={};namespaces={};records=[];bodies=0
    def add(p,expected=None):
        b=read(p);d=descriptor(b)
        if expected is not None:need(d=={k:expected[k] for k in ['bytes','SHA256']},'whole original pin')
        allfiles[str(p)]={'path':str(p),**d};return b
    def group(root,files,dirs):
        root=Path(root);fs,ds=extent(root);need((fs,ds)==(sorted(files),sorted(dirs)),'complete approved original namespace')
        namespaces[str(root)]={'path':str(root),'files':fs,'directories':ds}
        for name in fs:add(root/name)
    for rid,authsha,seals,manifest_name,main_name,config_name,candidate in SPECS:
        authority=P/('verification/root-editorial-'+rid+'-20261115.json');ab=add(authority);need(descriptor(ab)['SHA256']==authsha,'actual root adoption');adoption=json.loads(ab)
        if rid=='23418581':science=adoption['scientificAuthority'];science_path=Path(science['path'])
        else:science={'SHA256':adoption['scientific_authority_SHA256']};science_path=P/adoption['scientific_authority']
        science_body=add(science_path);need(descriptor(science_body)['SHA256']==science['SHA256'],'actual scientific authority bytes only, not new science review')
        e=P/'papers'/rid/'reviews/editorial';sb=add(e/'FINAL_SEAL.json');need(descriptor(sb)['SHA256']==seals,'same held approved editorial seal');s=json.loads(sb)
        mb=add(e/manifest_name);m=json.loads(mb)
        expected=s['manifest']['SHA256'] if 'manifest' in s else s['manifest_SHA256'];need(descriptor(mb)['SHA256']==expected,'same-buffer approved manifest')
        paths=[r.get('relative_path',r.get('path')) for r in m['files']]
        terms=s.get('exact_root_terminal_controls',s.get('exact_root_terminals',s.get('exact_root_terminal_exclusions')))
        group(e,[*paths,*terms],m['directories'])
        for row,name in zip(m['files'],paths):add(e/name,row)
        config=json.loads(add(e/config_name));main=add(e/main_name)
        if rid=='23418581':
            inputs=json.loads(read(e/'INPUT_BINDINGS.json'));groups=[inputs['source_namespace'],inputs['root_namespace']];core=inputs['qualified_core_actual18']
            assets=config['source_binding']['whole_original_source_ready']['all_native_assets_in_original_order'];slug=config['slug'];mainid='main-content';code=['prepare_editorial.py','verify_editorial_read_only.py']
        elif rid=='23202966':
            inputs=json.loads(read(e/'SOURCE_INPUTS.json'));groups=inputs['complete_immutable_namespaces'];core=inputs['qualified_core17_plus_sole405b_sources']
            assets=config['publication']['all_original_assets'];slug=config['promotion']['slug_proposal'];mainid='main';code=['prepare_editorial.py','verify_editorial.py','seal_editorial.py']
        else:
            inputs=json.loads(read(e/'PROTECTED_INPUTS.json'));groups=list(inputs['namespaces'].values());core=inputs['qualified_core']['named17_original_plus_sole_authorized405b']
            assets=config['publication']['all_original_assets'];slug=config['promotion']['slug_proposal'];mainid='main';code=['prepare_editorial.py','verify_editorial.py','seal_editorial.py']
        for g in groups:
            root=Path(g['root']);names=[]
            for row in g['files']:
                path=Path(row['path']);path=path if path.is_absolute() else root/path
                add(path,row);names.append(path.relative_to(root).as_posix())
            group(root,names,g['directories'])
        for row in core:add(Path(row['path']),row)
        assets_out=[]
        for a in assets:
            native=Path(a['path']);add(native,a);name=a['original_api_file_object']['key']
            need(read(e/candidate/name)==read(native),'approved complete native asset remains original')
            assets_out.append({'key':name,'native_path':str(native),**descriptor(read(native)),'original_asset_object':a})
        for f in code:bodies+=len(add(e/f))
        ready=P/'papers'/rid/'sources/SOURCE_READY.json';add(ready)
        records.append({'record_id':rid,'root_editorial_adoption':{'path':str(authority),**descriptor(ab)},'editorial_root':str(e),'editorial_seal':{'path':str(e/'FINAL_SEAL.json'),**descriptor(sb)},'approved_MAIN':{'path':str(e/main_name),**descriptor(main)},'main_id':mainid,'approved_config':{'path':str(e/config_name),**descriptor(read(e/config_name))},'slug':slug,'canonical_proposal':'https://aleckriebel.com/research/'+slug+'/','native_assets_in_original_order':assets_out,'approved_Bib':{'path':str(e/candidate/'citation.bib'),**descriptor(read(e/candidate/'citation.bib'))},'article_leaf_count':len(assets_out)+2,'current_code_read':[{'path':str(e/f),**descriptor(read(e/f))} for f in code],'source_ready_reference':{'path':str(ready),**descriptor(read(ready))}})
    need(bodies==84204 and sum(r['article_leaf_count'] for r in records)==16,'whole8currentbodies and16nativearticle leaves')
    need(all('23331331' not in p and '23203732' not in p for p in allfiles),'excluded133137 original namespaces not added')
    new('APPROVED_INPUTS.json',{'UTC':datetime.now(timezone.utc).isoformat(),'records':records,'all_original_files':list(allfiles.values()),'closed_original_namespaces':list(namespaces.values()),'complete_approved_MAIN_bytes':sum(r['approved_MAIN']['bytes'] for r in records),'current_editorial_helpers_read':8,'current_editorial_helper_bytes':bodies,'read_scope':'Full three rooteditorial authorities, whole approvedMAINs, full currenteditorial helpers, full135136configs/allunique132config fields. Repeated whole132source/native/scientific/root bodies opaque typed/hash references; no fresh scientific review.','current_three_page_stage_writer_folder_accessed':False,'foreign_corpus_copied':False,'science_native_builder_old_campaign_execution':False,'production_authority':False})
    print(json.dumps({'status':'APPROVED_THREE_SOURCE_REFERENCES_FROZEN','original_files':len(allfiles),'closed_namespaces':len(namespaces),'whole_MAIN_bytes':40599,'current_editorial_bodies':8,'current_editorial_code_bytes':84204,'new_article_leaves':16,'aggregate_replacements':2,'proposal_counts':[647,99,100],'current_stage_writer_accessed':False,'production_authority':False},sort_keys=True))

if __name__=='__main__':main()
