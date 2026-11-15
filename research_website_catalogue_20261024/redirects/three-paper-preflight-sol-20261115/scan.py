"""Bounded article correspondence only; no PDF extraction or science replay.
Uses inspected old pure corpus reader; writes only this new evidence folder.
"""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,hashlib,re,shutil
O=Path(__file__).resolve().parent;P=O.parent.parent
OLD=O.parent/'dlab-fibonacci-preflight-sol-20261114'
spec=importlib.util.spec_from_file_location('old_bounded_corpus_reader',OLD/'preflight_core.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def write(name,d):(O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def bind(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def native(name):return json.loads(json.loads((O/name).read_text())['structuredContent']['content'])
assert not (O/'SEARCH_RESULTS.json').exists()
targets={};snap=O/'target-inputs';snap.mkdir()
for rid in ('23430498','23149775','23331080'):
 f=P/'papers'/rid/'sources/SOURCE_READY.json';d=json.loads(f.read_text());(snap/rid).mkdir();shutil.copyfile(f,snap/rid/'SOURCE_READY.json')
 if rid in ('23430498','23149775'):
  date=d['publication_date_declared'];created=d['record_created'];updated=d['record_updated'];doi=d['DOI'];assets=d['all_native_assets_in_original_order'];sha_key='SHA256';md5_key='MD5'
 else:
  date=d['publication_date'];created=d['created'];updated=d['updated'];doi=d['doi'];assets=d['all_assets_in_original_order'];sha_key='sha256';md5_key='md5'
 full=[]
 for a in assets:
  b=Path(a['path']).read_bytes();assert len(b)==a['bytes'] and hashlib.sha256(b).hexdigest()==a[sha_key] and hashlib.md5(b).hexdigest()==a[md5_key] and a['original_api_file_object']['checksum']=='md5:'+a[md5_key]
  full.append({'original_native_file_object':a['original_api_file_object'],'path':a['path'],'bytes':len(b),'SHA256':a[sha_key],'MD5':a[md5_key]})
 targets[rid]={'record_id':rid,'title':d['title'],'DOI':doi,'conceptrecid':str(d['conceptrecid']),'version':d['version'],'declared_date':date,'created':created,'updated':updated,'SOURCE_READY':bind(f),'whole_SOURCE_READY_snapshot':str(snap/rid/'SOURCE_READY.json'),'native_assets_in_original_order':full,'selected_actual_PDF':d['selected_actual_PDF'],'scientific_reassessment':False,'live_replacement_verified':False,'redirect_authorized':False}
assert targets['23430498']['version']=='1.0' and targets['23430498']['declared_date']=='2026-10-13'
assert targets['23149775']['version']=='1.0' and targets['23149775']['declared_date']=='2026-10-04'
assert targets['23331080']['version']=='1.0' and targets['23331080']['declared_date']=='2026-10-12'
bindings,extracts,oldreps,html,data=m.corpus()
tree=native('REMOTE_DOCS_TREE_GET.json');assert tree['truncated'] is False
current={'docs/'+x['path']:x for x in tree['tree'] if x['type']=='blob'};prior={x['path']:x for x in bindings}
assert current.keys()==prior.keys() and len(current)==254
delta=[{'path':path,'old_blob':prior[path]['blob'],'new_blob':current[path]['sha'],'bytes':current[path]['size']} for path in sorted(current) if current[path]['sha']!=prior[path]['blob']]
assert delta==[{'path':'docs/papers/gromov-unitary-lipschitz/index.html','old_blob':'a19d14821dc44c36def20b345dcbcd82a85d572b','new_blob':'b3e1157aebc6b9a30fba4367a368c5be20de863d','bytes':913}]
changed=(O/'current-unitary-leaf.html').read_bytes();assert len(changed)==913 and hashlib.sha1(b'blob 913\0'+changed).hexdigest()==delta[0]['new_blob']
doc=m.HTML();doc.feed(changed.decode());reps=[]
for r in oldreps:
 if r['path']==delta[0]['path']:
  r={**r,'text':changed.decode() if r['kind']=='raw_UTF8_blob' else ''.join(doc.text)}
 reps.append(r)
data[delta[0]['path']]=changed
q={}
for rid,t in targets.items():
 q[rid+'_record_DOI_concept']=[re.escape(rid),re.escape(t['DOI']),re.escape(t['conceptrecid'])]
 q[rid+'_exact_title']=[re.escape(m.norm(t['title']))]
q.update({
 '23430498_distinctive':[r'free.exterior',r'string.link',r'stanford',r'order.seven',r'order.7',r'seven.wheel',r'2[.]13'],
 '23430498_broad':[r'finite.type.{0,35}invariant',r'\bmilnor\b',r'\bmeilhan\b',r'\bnogueira\b',r'\bduzhin\b',r'\bkarev\b'],
 '23149775_distinctive':[r'focal.{0,20}pedal',r'pedal.{0,20}area',r'elliptic.{0,20}billiard'],
 '23149775_broad':[r'\bbilliard',r'\bponcelet\b',r'\bpedal\b',r'\bkoiller\b',r'\breznik\b',r'\bstachel\b'],
 '23331080_distinctive':[r'normalized.{0,25}relative.{0,25}kahler',r'total.space.{0,25}positiv',r'\bnaumann\b',r'relative.{0,30}ricci'],
 '23331080_broad':[r'\bricci\b',r'\bkahler\b',r'\bsemipositiv',r'\bberman\b']})
oldresults=m.search(oldreps,q);results=m.search(reps,q)
controls=[{'name':'Unicode normalization','pass':m.norm('Kähler ﬁnite non\u00adnegative prime-\nfield')==m.norm('Kahler finite nonnegative primefield')},{'name':'target title positive self controls','pass':all(re.search(q[rid+'_exact_title'][0],m.norm(t['title'])) for rid,t in targets.items())},{'name':'target DOI positive self controls','pass':all(re.search(re.escape(t['DOI']),t['DOI']) for t in targets.values())},{'name':'known unchanged complete PDF positive control','pass':any('positive recurrence for single-linkage bimolecular' in m.norm(r['text']) for r in reps)},{'name':'actual changed unitary leaf positive control','pass':any(r['path']==delta[0]['path'] and 'paper moved' in m.norm(r['text']) and 'lipschitz-nonincreasing' in m.norm(r['text']) for r in reps)}]
assert all(c['pass'] for c in controls)
asset_hashes={a['SHA256']:rid for rid,t in targets.items() for a in t['native_assets_in_original_order']}
assetmatches=[{'record_id':asset_hashes[m.sha(b)],'public_path':path,'blob':current[path]['sha'],'SHA256':m.sha(b)} for path,b in data.items() if m.sha(b) in asset_hashes]
hitcounts=lambda rr:{g:sum(bool(r['groups'][g]) for r in rr) for g in q}
summary={'UTC':datetime.now(timezone.utc).isoformat(),'opening_remote_main_commit':'624d7176b828ccf6d8db30b6916cf121719c09fc','historical_docs_tree':m.TREE,'current_docs_tree':tree['sha'],'current_equals_unitary_commit_docs_tree':True,'historical_and_current_blobs':254,'raw_UTF8_representations':137,'decoded_HTML_representations':47,'reused_complete_PDFs':76,'reused_PDF_pages':854,'search_representations_each_epoch':260,'new_PDF_extractions':0,'binary_support_archives_recursively_expanded_or_text_searched':False,'only_current_leaf_delta':delta,'historical_hit_representation_counts':hitcounts(oldresults),'current_hit_representation_counts':hitcounts(results),'native_full_asset_hash_matches':assetmatches,'candidate_paths':sorted({r['path'] for r in results if any(r['groups'].values())}),'no_redirect_prepared_or_written':True,'no_scientific_reassessment':True}
write('TARGET_IDENTITIES.json',targets);write('CORPUS_RECEIPT.json',summary);write('SEARCH_RESULTS.json',{'queries':q,'historical':oldresults,'current':results});write('QUERY_CONTROLS.json',controls);write('CURRENT_DOCS_DELTA.json',delta);write('HISTORICAL_DOCS_BINDINGS.json',bindings);write('REUSED_EXTRACT_BINDINGS.json',extracts);write('CURRENT_HTML_IDENTITIES.json',[*filter(lambda x:x['path']!=delta[0]['path'],html),{'path':delta[0]['path'],'blob':delta[0]['new_blob'],'SHA256':m.sha(changed),'title':''.join(doc.title),'hrefs':doc.links}])
print(json.dumps(summary,indent=2))
