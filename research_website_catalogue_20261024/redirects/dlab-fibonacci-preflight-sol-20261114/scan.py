"""Write evidence only into this new preflight folder."""
from preflight_core import *
from datetime import datetime,timezone
import shutil
def write(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
require(not (O/'SEARCH_RESULTS.json').exists(),'do not overwrite completed scan')
now=datetime.now(timezone.utc).isoformat();targets={};snap=O/'target-inputs';snap.mkdir()
for id in ['23441890','23174283']:
    base=P/'papers'/id;d=snap/id;d.mkdir();ready=load(base/'sources/SOURCE_READY.json');record=load(base/'sources/record.raw.json')
    for name in ['SOURCE_READY.json','record.raw.json']:shutil.copyfile(base/'sources'/name,d/name)
    auth=P/('verification/root-clearance-'+id+'-20261114.json');shutil.copyfile(auth,d/auth.name)
    configs=[]
    for name in ['publication.json','promotion.json','publication/promotion/promotion.json']:
        f=base/name
        if f.exists():
            shutil.copyfile(f,d/name.replace('/','__'));configs.append({'original_path':str(f),'snapshot':str((d/name.replace('/','__')).relative_to(O)),**bind(f),'whole_original_object':load(f)})
    actual=[]
    for r in ready['all_assets_in_original_order']:
        b=Path(r['path']).read_bytes();require(bind(r['path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'native source full asset hash')
        require(r['original_api_file_object']==record['files'][len(actual)] and 'md5:'+hashlib.md5(b).hexdigest()==record['files'][len(actual)]['checksum'],'native file order/MD5')
        actual.append({'native_object':r['original_api_file_object'],'path':r['path'],**bind(r['path'])})
    targets[id]={'title':record['metadata']['title'],'doi':record['doi'],'conceptrecid':record['conceptrecid'],'native_version':record['metadata']['version'],'declared_publication_date':record['metadata']['publication_date'],'created':record['created'],'updated':record['updated'],'whole_native_source_ready':ready,'whole_root_authority':load(auth),'whole_configuration_snapshots':configs,'all_assets_in_original_order':actual,'canonical_url':None,'AA':None,'redirect_authorized':False}
require(targets['23441890']['native_version']=='1.0.0' and targets['23441890']['declared_publication_date']=='2026-10-17','exact113 identity')
require(targets['23174283']['native_version']=='1.0' and targets['23174283']['declared_publication_date']=='2026-10-05','exact114 identity')
bindings,extracts,reps,html,data=corpus();q=queries(targets);results=search(reps,q)
controls=[{'name':'known current unitary actual HTML title','passed':any(r['path']=='docs/papers/gromov-unitary-lipschitz/index.html' and 'lipschitz-nonincreasing' in norm(r['text']) for r in reps)}, {'name':'known positive recurrence complete PDF derivative','passed':any('positive recurrence for single-linkage bimolecular' in norm(r['text']) for r in reps)}, {'name':'accent/ligature/soft-hyphen and line wrap normalization','passed':norm('ﬁnite déformation non\u00adnegative prime-\nfield')==norm('finite deformation nonnegative primefield')}, {'name':'target DOI search positive self-control','passed':all(re.search(q[id+'_record_or_DOI'][-1],norm(t['doi'])) for id,t in targets.items())}, {'name':'exact target title positive self-control','passed':all(re.search(q[id+'_exact_title'][0],norm(t['title'])) for id,t in targets.items())}]
require(all(x['passed'] for x in controls),'search positive controls')
hashes={r['sha256']:id for id,t in targets.items() for r in t['all_assets_in_original_order']}
matches=[{'record_id':hashes[r['sha256']],**r} for r in bindings if r['sha256'] in hashes]
write('TARGET_IDENTITIES.json',targets);write('HTML_IDENTITIES.json',html);write('SEARCH_RESULTS.json',{'queries':q,'representations':results});write('QUERY_CONTROLS.json',controls)
summary={'UTC':now,'current_remote_main_commit':'d44aa027d3afa222cc3b34f8861f2c24b740a000','docs_tree':TREE,'public_blobs':len(bindings),'HTML':len(html),'raw_UTF8_blobs':sum(r['kind']=='raw_UTF8_blob' for r in reps),'complete_reused_PDFs':len(extracts),'complete_reused_PDF_pages':sum(r['pages'] for r in extracts),'search_representations':len(reps),'new_PDF_extractions':0,'binary_archives_recursively_text_expanded':False,'exact_full_native_asset_hash_matches':matches,'hit_representation_counts':{g:sum(bool(r['groups'][g]) for r in results) for g in q},'candidate_paths':sorted({r['path'] for r in results if any(r['groups'].values())}),'no_Git_ref_index_worktree_mutation':True}
write('CORPUS_RECEIPT.json',summary)
print(json.dumps(summary,indent=2))
