"""Offline pure custody check. No writes/network/extraction/scientific replay."""
from preflight_core import *
checks=0
def ck(ok,label):
    global checks
    checks+=1
    if not ok:raise RuntimeError(label)
def check_rows(base,rows):
    for r in rows:ck(bind(base/r['path'])=={k:r[k] for k in ['bytes','sha256']},'input '+r['path'])
def response(name):return json.loads(load(O/name)['structuredContent']['content'])
opening=response('REMOTE_MAIN_GET.json');closing=response('REMOTE_MAIN_CLOSING_GET.json')
ck(opening['object']['sha']=='d44aa027d3afa222cc3b34f8861f2c24b740a000','opening remote epoch')
ck(closing['object']['sha']=='37d30a4a33221457b0dfb892768f93ea767a0041','closing remote epoch')
for name in ['REMOTE_ROOT_TREE_GET.json','REMOTE_CLOSING_ROOT_TREE_GET.json']:
    r=response(name);ck(r['truncated'] is False and next(x['sha'] for x in r['tree'] if x['path']=='docs')==TREE,'same released docs tree')
for folder in ['artin-devissage-preflight-sol-20261025','yamabe-birational-unitary-bianchi-preflight-sol-20261114']:
    base=O.parent/folder;s=load(base/'FINAL_SEAL.json');m=base/s['manifest']
    ck(sha(m.read_bytes())==s['manifest_sha256'],'prior manifest seal '+folder)
    ck(load(base/'DOCS_OBJECT_BINDINGS.json')==load(O/'DOCS_OBJECT_BINDINGS.json'),'same original254-blob binding '+folder)
    ck(load(base/'REUSED_EXTRACT_BINDINGS.json')==load(O/'REUSED_EXTRACT_BINDINGS.json'),'same original76-derivative binding '+folder)
# Existing fixed-object reader reauthenticates all bytes; it does not extract PDFs
# or run any source/candidate scientific programme. No lexical search is rerun.
bindings,extracts,reps,html,data=corpus()
ck((len(bindings),len(extracts),len(reps),len(html))==(254,76,260,47),'exact bounded corpus coverage')
ck(sum(x['pages'] for x in extracts)==854,'reused PDF page count')
check_rows(Path('/'),load(O/'PROTECTED_INPUTS.json')['files'])
target=load(O/'TARGET_IDENTITIES.json')
for id,version,date in [('23441890','1.0.0','2026-10-17'),('23174283','1.0','2026-10-05')]:
    r=target[id];base=P/'papers'/id;d=O/'target-inputs'/id
    ck((r['native_version'],r['declared_publication_date'])==(version,date),'exact target edition '+id)
    ck(r['whole_native_source_ready']==load(base/'sources/SOURCE_READY.json'),'literal source-ready/old flags '+id)
    for name in ['SOURCE_READY.json','record.raw.json']:ck((d/name).read_bytes()==(base/'sources'/name).read_bytes(),'raw target JSON copy')
    ap=P/('verification/root-clearance-'+id+'-20261114.json');ck((d/ap.name).read_bytes()==ap.read_bytes() and r['whole_root_authority']==load(ap),'whole root authority')
    record=load(base/'sources/record.raw.json')
    ck(record['files']==[x['native_object'] for x in r['all_assets_in_original_order']],'whole native ordered file objects')
    for a in r['all_assets_in_original_order']:
        b=Path(a['path']).read_bytes();ck(len(b)==a['bytes'] and sha(b)==a['sha256'] and 'md5:'+hashlib.md5(b).hexdigest()==a['native_object']['checksum'],'whole original target asset')
    for c in r['whole_configuration_snapshots']:
        b=Path(c['original_path']).read_bytes();ck(bind(c['original_path'])=={k:c[k] for k in ['bytes','sha256']} and b==(O/c['snapshot']).read_bytes() and json.loads(b)==c['whole_original_object'],'whole unchanged config schema')
    ck(r['canonical_url'] is None and r['AA'] is None and r['redirect_authorized'] is False,'no target transition')
summary=load(O/'CORPUS_RECEIPT.json');stored=load(O/'SEARCH_RESULTS.json')
ck(summary['exact_full_native_asset_hash_matches']==[],'no exact full-asset match stored')
ck(len(stored['representations'])==260,'stored complete representation coverage')
for group,count in summary['hit_representation_counts'].items():
    ck(count==sum(bool(r['groups'][group]) for r in stored['representations']),'stored search consistency '+group)
    if group.endswith(('record_or_DOI','exact_title','distinctive')):ck(count==0,'no exact/distinctive candidate '+group)
ck(all(r['passed'] for r in load(O/'QUERY_CONTROLS.json')),'stored positive controls')
for r in load(O/'CANDIDATE_ASSET_ASSOCIATIONS.json'):ck(data[r['path']] and sha(data[r['path']])==r['sha256'],'actual candidate asset association')
for f in (O/'candidate-evidence').glob('*.html'):ck(data[f.name.replace('__','/')]==f.read_bytes(),'actual candidate whole HTML')
v=load(O/'VERDICT.json')
ck(v['redirect_authorized'] is False and v['redirect_created'] is False and v['canonical_url'] is None and v['AA'] is None,'all live gates remain pending')
if (O/'INPUT_MANIFEST.json').exists():check_rows(Path('/'),load(O/'INPUT_MANIFEST.json')['files'])
if (O/'OWNED_MANIFEST.json').exists():
    rows=load(O/'OWNED_MANIFEST.json')['files'];check_rows(O,rows)
    ck({str(f.relative_to(O)) for f in O.rglob('*') if f.is_file() and f.name not in ['OWNED_MANIFEST.json','SEAL.json']}=={r['path'] for r in rows},'complete owned inventory')
sealed=(O/'SEAL.json').exists()
if sealed:
    for n,h in load(O/'SEAL.json')['bound_files_sha256'].items():ck(sha((O/n).read_bytes())==h,'final seal '+n)
print(json.dumps({'status':'PASS_BOUNDED_LEGACY_CORRESPONDENCE_PURE_CUSTODY','sealed':sealed,'checks':checks,'public_blobs':254,'complete_reused_PDFs':76,'PDF_pages':854,'stored_search_representations':260,'bounded_negative_records':['23441890','23174283'],'writes':0,'network_requests':0,'PDF_extractions':0,'source_program_replays':0,'Git_ref_index_worktree_mutations':0,'redirect_authorized':False,'canonical_url':None,'AA':None},indent=2))
